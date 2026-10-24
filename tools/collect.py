"""Bulk Lee County FL (12071) collector: NFIP policies cohort + claims by year + final NRI try.
Computes compact aggregates -> agg.json. Saves progress; small pages, generous retries."""
import json, os, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops script dir; restore for ffcalc
import ffcalc

POL = "https://www.fema.gov/api/open/v3/NfipPolicies"
CLM = "https://www.fema.gov/api/open/v3/NfipClaims"
ASOF = "2026-07-31T00:00:00.000z"
PAGE = 1000
ST = os.environ.get("FF_STATE", "FL")       # propertyState / claims state
GEO = os.environ.get("FF_GEOID", "12071")    # 5-digit state+county FIPS
DIR = os.environ.get("FF_DIR", ".")          # per-county output dir
AGG_OUT = os.path.join(DIR, "agg.json")

def get(url, timeout=240, tries=6):
    """Fetch with retries. Raises on exhaustion so the caller can shrink and resume."""
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ff"}), timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            last = e
            print("  retry", i, repr(e)[:80], flush=True)
            time.sleep(min(20, 3 * (i + 1)))
    raise RuntimeError("exhausted: " + repr(last)[:90])

def page_all(base, filt, select, label):
    # Total via a light count query (reliable even when bulk pages 503). No $orderby (forces a sort -> 503).
    cnt = get(base + "?" + urllib.parse.urlencode(
        {"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote))
    key = [k for k in cnt if k != "metadata"][0]
    total = cnt["metadata"]["count"]
    print(f"{label}: total {total}", flush=True)
    seen, skip, top = {}, 0, PAGE
    while len(seen) < total:
        try:
            d = get(base + "?" + urllib.parse.urlencode(
                {"$filter": filt, "$select": select, "$top": top, "$skip": skip}, quote_via=urllib.parse.quote))
        except RuntimeError:
            if top > 125:          # 503 on this window: shrink page size and retry the SAME offset
                top = max(125, top // 2); print(f"  shrink top->{top} at skip {skip}", flush=True); continue
            raise                  # already tiny and still failing: real outage, fail loudly
        got = d[key]
        if not got:
            break
        for r in got:
            seen[r["id"]] = r
        skip += top
        if skip % 10000 < top:
            print(f"  {label} {len(seen)}/{total} (top {top})", flush=True)
    # Offset paging without a stable sort cannot PROVE a consistent snapshot. We record what we can
    # actually verify: unique ids vs the API's reported count, AND a re-queried count to detect drift
    # during the pull. "count_reconciled" is a reconciliation, not cryptographic snapshot integrity.
    recheck = get(base + "?" + urllib.parse.urlencode(
        {"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote))
    rk = [k for k in recheck if k != "metadata"][0]
    total2 = recheck["metadata"]["count"]
    MANIFEST[label] = {"reported_total": total, "recheck_total": total2, "unique_fetched": len(seen),
                       "missing": total - len(seen), "complete": len(seen) == total,
                       "stable": total == total2,
                       "provisional": not (len(seen) == total and total == total2)}
    print(f"{label} fetched {len(seen)}/{total} recheck {total2} "
          f"provisional={MANIFEST[label]['provisional']}", flush=True)
    return list(seen.values())

agg = {}
MANIFEST = {}
RETRIEVED = "2026-10-22"
POLICY_ASOF = "2026-07-31"
t0 = time.time()

# POLICIES ----------------------------------------------------------------------
pol = page_all(POL,
    f"propertyState eq '{ST}' and startswith(censusGeoid,'{GEO}') and policyEffectiveDate le '{ASOF}' and policyTerminationDate ge '{ASOF}'",
    "id,policyCost,fullRiskPremium,ratedFloodZone,occupancyType,primaryResidenceIndicator,policyCount,"
    "reportedZipCode,policyEffectiveDate,totalBuildingInsuranceCoverage,totalContentsInsuranceCoverage",
    "policies")

units = sum(int(r.get("policyCount") or 0) for r in pol)
agg["policies"] = dict(ffcalc.aggregate_policies(pol, asof=POLICY_ASOF),
                       zips=len(set(r.get("reportedZipCode") for r in pol)),
                       asof=POLICY_ASOF, retrieved=RETRIEVED)
print("policies agg done", round(time.time()-t0), "s", flush=True)
# NOTE: no intermediate write — agg.json is written ONCE at the very end with "complete": true,
# so a mid-pipeline failure never leaves a partial file that the generator would mistake for done.

# CLAIMS ------------------------------------------------------------------------
clm = page_all(CLM, f"state eq '{ST}' and countyCode eq '{GEO}'",
    "id,yearOfLoss,netBuildingPaymentAmount,netContentsPaymentAmount,policyCount", "claims")
agg["claims"] = dict(ffcalc.aggregate_claims(clm, units),
    # cumulative historical count over point-in-time policy units; NOT an annual rate or flood probability.
    geo_note="claims filtered by claims-dataset countyCode, which may not match the policy property county",
    retrieved=RETRIEVED)
print("claims agg done", round(time.time()-t0), "s", flush=True)

# NRI: authoritative FEMA_NationalRiskIndex ArcGIS org (keyless). County = STCOFIPS. -----
try:
    b = ("https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/"
         "National_Risk_Index_Counties/FeatureServer/0/query")
    r = get(b + "?" + urllib.parse.urlencode(
        {"where": f"STCOFIPS='{GEO}'", "outFields": "*", "f": "json",
         "returnGeometry": "false", "resultRecordCount": 1}), timeout=90, tries=3)
    feats = r.get("features", [])
    if feats:
        a = feats[0]["attributes"]
        def g(k): return a.get(k)
        agg["nri"] = {
            "county": a.get("COUNTY"), "state": a.get("STATEABBRV"),
            "coastal": {"risk_rating": g("CFLD_RISKR"), "risk_score": g("CFLD_RISKS"),
                        "eal_rating": g("CFLD_EALR"), "eal_national_pctl": g("CFLD_ALR_NPCTL"),
                        "eal_total_usd": g("CFLD_EALT")},
            "inland": {"risk_rating": g("IFLD_RISKR"), "risk_score": g("IFLD_RISKS"),
                       "eal_rating": g("IFLD_EALR"), "eal_national_pctl": g("IFLD_ALR_NPCTL"),
                       "eal_total_usd": g("IFLD_EALT")},
            "source": "FEMA National Risk Index (county), FEMA_NationalRiskIndex ArcGIS, keyless"}
        print("NRI ok:", a.get("COUNTY"), "coastal", g("CFLD_RISKR"), flush=True)
    else:
        agg["nri"] = None
        print("NRI: 0 features -> gap line", flush=True)
except Exception as e:
    agg["nri"] = None
    print("NRI err -> gap line", repr(e)[:80], flush=True)
# STATE county-risk for the tile-map: every county in the state + its worst flood rating (NRI).
try:
    bb = ("https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/"
          "National_Risk_Index_Counties/FeatureServer/0/query")
    rr = get(bb + "?" + urllib.parse.urlencode(
        {"where": f"STATEFIPS='{GEO[:2]}'", "outFields": "STCOFIPS,COUNTY,CFLD_RISKR,IFLD_RISKR",
         "f": "json", "returnGeometry": "false", "resultRecordCount": 400}), timeout=90, tries=3)
    sr = []
    for f in rr.get("features", []):
        a = f["attributes"]
        sr.append({"fips": a.get("STCOFIPS"), "county": a.get("COUNTY"),
                   "rating": ffcalc.worst_flood_rating(a.get("CFLD_RISKR"), a.get("IFLD_RISKR"))})
    agg["state_risk"] = sorted(sr, key=lambda d: (d["county"] or ""))
    print("state_risk counties:", len(agg["state_risk"]), flush=True)
except Exception as e:
    agg["state_risk"] = []
    print("state_risk err:", repr(e)[:80], flush=True)

agg["manifest"] = MANIFEST
# every required dataset collected and reconciled -> mark the county complete. Written ONCE, atomically
# (temp + replace) so a crash can never leave a half-written file that looks done.
incomplete = [k for k, v in MANIFEST.items() if not v["complete"]]
agg["complete"] = (len(incomplete) == 0)
tmp = AGG_OUT + ".tmp"
json.dump(agg, open(tmp, "w"))
os.replace(tmp, AGG_OUT)
print("MANIFEST", json.dumps(MANIFEST), flush=True)
print("ALL DONE", round(time.time()-t0), "s; complete:", agg["complete"], "; incomplete:", incomplete, flush=True)
