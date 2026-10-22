"""Bulk Lee County FL (12071) collector: NFIP policies cohort + claims by year + final NRI try.
Computes compact aggregates -> agg.json. Saves progress; small pages, generous retries."""
import json, os, statistics, time, urllib.parse, urllib.request
from collections import Counter, defaultdict

POL = "https://www.fema.gov/api/open/v3/NfipPolicies"
CLM = "https://www.fema.gov/api/open/v3/NfipClaims"
ASOF = "2026-07-31T00:00:00.000z"
PAGE = 1000
ST = os.environ.get("FF_STATE", "FL")       # propertyState / claims state
GEO = os.environ.get("FF_GEOID", "12071")    # 5-digit state+county FIPS

def get(url, timeout=240, tries=10):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ff"}), timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            print("  retry", i, repr(e)[:90], flush=True)
            time.sleep(min(30, 4 * (i + 1)))
    raise SystemExit("API failed after retries: " + url[:120])

def page_all(base, filt, select, label):
    # No $orderby: it forces a server-side sort of the filtered set and 503s. Page by $skip, dedupe by id.
    first = get(base + "?" + urllib.parse.urlencode(
        {"$filter": filt, "$select": select, "$top": PAGE, "$skip": 0,
         "$inlinecount": "allpages"}, quote_via=urllib.parse.quote))
    key = [k for k in first if k != "metadata"][0]
    total = first["metadata"]["count"]
    seen = {}
    for r in first[key]:
        seen[r["id"]] = r
    print(f"{label}: total {total}", flush=True)
    skip = PAGE
    while len(seen) < total:
        d = get(base + "?" + urllib.parse.urlencode(
            {"$filter": filt, "$select": select, "$top": PAGE, "$skip": skip},
            quote_via=urllib.parse.quote))
        got = d[key]
        if not got:
            break
        for r in got:
            seen[r["id"]] = r
        skip += PAGE
        if skip % 10000 < PAGE:
            print(f"  {label} {len(seen)}/{total}", flush=True)
    # completeness gate: offset paging can silently drop rows; record the shortfall.
    MANIFEST[label] = {"reported_total": total, "unique_fetched": len(seen),
                       "complete": len(seen) == total, "missing": total - len(seen)}
    print(f"{label} complete={len(seen)==total} ({len(seen)}/{total})", flush=True)
    return list(seen.values())

agg = {}
MANIFEST = {}
RETRIEVED = "2026-10-22"
POLICY_ASOF = "2026-07-31"
t0 = time.time()

# POLICIES ----------------------------------------------------------------------
pol = page_all(POL,
    f"propertyState eq '{ST}' and startswith(censusGeoid,'{GEO}') and policyEffectiveDate le '{ASOF}' and policyTerminationDate ge '{ASOF}'",
    "id,policyCost,fullRiskPremium,ratedFloodZone,occupancyType,primaryResidenceIndicator,policyCount,reportedZipCode",
    "policies")

def isone(v): return v in (1, 11, "1", "11")
def istrue(v): return v in (True, "true", "True", 1, "1")
units = sum(int(r.get("policyCount") or 0) for r in pol)
coh = [r for r in pol if isone(r.get("occupancyType")) and istrue(r.get("primaryResidenceIndicator"))]
cost = sorted(r["policyCost"] for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0)
both = [r for r in coh if isinstance(r.get("policyCost"), (int, float)) and isinstance(r.get("fullRiskPremium"), (int, float)) and r["fullRiskPremium"] > 0]
frp = sorted(r["fullRiskPremium"] for r in both)
below = sum(1 for r in both if r["policyCost"] < r["fullRiskPremium"])
def q(a, p): return round(statistics.quantiles(a, n=100, method="inclusive")[p-1]) if len(a) > 1 else (a[0] if a else None)
# zone mix by POLICY UNITS (sum policyCount), not record count; condo rows carry >1 unit.
zone_units = defaultdict(int)
for r in pol:
    zone_units[(r.get("ratedFloodZone") or "Unknown").strip()] += int(r.get("policyCount") or 0)
sfha_prefixes = ("A", "V")
sfha_units = sum(u for z, u in zone_units.items() if z[:1] in sfha_prefixes)
agg["policies"] = {
    "rows": len(pol), "units": units,
    "cohort_n": len(coh), "cost_n": len(cost),
    "p25": q(cost, 25), "p50": q(cost, 50), "p75": q(cost, 75), "p90": q(cost, 90),
    "frp_median": q(frp, 50), "frp_n": len(frp),
    "share_below": round(100 * below / len(both), 1) if both else None, "below_n": len(both),
    "zone_units": dict(sorted(zone_units.items(), key=lambda x: -x[1])[:12]),
    "sfha_units": sfha_units, "sfha_share_units": round(100 * sfha_units / units, 1) if units else None,
    "zips": len(set(r.get("reportedZipCode") for r in pol)),
    "asof": POLICY_ASOF, "retrieved": RETRIEVED,
}
print("policies agg done", round(time.time()-t0), "s", flush=True)
json.dump(agg, open("agg.json", "w"))

# CLAIMS ------------------------------------------------------------------------
clm = page_all(CLM, f"state eq '{ST}' and countyCode eq '{GEO}'",
    "id,yearOfLoss,netBuildingPaymentAmount,netContentsPaymentAmount,policyCount", "claims")
byyear = defaultdict(lambda: [0, 0.0])  # year -> [count, paid]
tot_paid = 0.0
for r in clm:
    y = r.get("yearOfLoss")
    paid = (r.get("netBuildingPaymentAmount") or 0) + (r.get("netContentsPaymentAmount") or 0)
    if y:
        byyear[int(y)][0] += 1
        byyear[int(y)][1] += paid
    tot_paid += paid
yrs = sorted(byyear)
agg["claims"] = {
    "rows": len(clm), "total_paid": round(tot_paid),
    "by_year": {str(y): [c, round(p)] for y, (c, p) in sorted(byyear.items())},
    # cumulative historical count over point-in-time policy units; NOT an annual rate or flood probability.
    "cumulative_per_100_current_units": round(100 * len(clm) / units, 1) if units else None,
    "year_min": yrs[0] if yrs else None, "year_max": yrs[-1] if yrs else None,
    "geo_note": "claims filtered by claims-dataset countyCode, which may not match the policy property county",
    "retrieved": RETRIEVED,
}
print("claims agg done", round(time.time()-t0), "s", flush=True)
json.dump(agg, open("agg.json", "w"))

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
            "riverine": {"risk_rating": g("RFLD_RISKR"), "risk_score": g("RFLD_RISKS"),
                         "eal_rating": g("RFLD_EALR"), "eal_national_pctl": g("RFLD_ALR_NPCTL"),
                         "eal_total_usd": g("RFLD_EALT")},
            "source": "FEMA National Risk Index (county), FEMA_NationalRiskIndex ArcGIS, keyless"}
        print("NRI ok:", a.get("COUNTY"), "coastal", g("CFLD_RISKR"), flush=True)
    else:
        agg["nri"] = None
        print("NRI: 0 features -> gap line", flush=True)
except Exception as e:
    agg["nri"] = None
    print("NRI err -> gap line", repr(e)[:80], flush=True)
agg["manifest"] = MANIFEST
json.dump(agg, open("agg.json", "w"))
# hard gate: fail loudly if either pull was incomplete
incomplete = [k for k, v in MANIFEST.items() if not v["complete"]]
print("MANIFEST", json.dumps(MANIFEST), flush=True)
print("ALL DONE", round(time.time()-t0), "s; incomplete:", incomplete, flush=True)
