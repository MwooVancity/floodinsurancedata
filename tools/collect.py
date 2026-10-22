"""Bulk Lee County FL (12071) collector: NFIP policies cohort + claims by year + final NRI try.
Computes compact aggregates -> agg.json. Saves progress; small pages, generous retries."""
import json, statistics, time, urllib.parse, urllib.request
from collections import Counter, defaultdict

POL = "https://www.fema.gov/api/open/v3/NfipPolicies"
CLM = "https://www.fema.gov/api/open/v3/NfipClaims"
ASOF = "2026-07-31T00:00:00.000z"
PAGE = 1000

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
    return list(seen.values())

agg = {}
t0 = time.time()

# POLICIES ----------------------------------------------------------------------
pol = page_all(POL,
    f"propertyState eq 'FL' and startswith(censusGeoid,'12071') and policyEffectiveDate le '{ASOF}' and policyTerminationDate ge '{ASOF}'",
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
agg["policies"] = {
    "rows": len(pol), "units": units,
    "cohort_n": len(coh), "cost_n": len(cost),
    "p25": q(cost, 25), "p50": q(cost, 50), "p75": q(cost, 75), "p90": q(cost, 90),
    "frp_median": q(frp, 50), "frp_n": len(frp),
    "share_below": round(100 * below / len(both), 1) if both else None, "below_n": len(both),
    "zones": dict(Counter((r.get("ratedFloodZone") or "?").strip() for r in pol).most_common(12)),
    "zips": len(set(r.get("reportedZipCode") for r in pol)),
}
print("policies agg done", round(time.time()-t0), "s", flush=True)
json.dump(agg, open("agg.json", "w"))

# CLAIMS ------------------------------------------------------------------------
clm = page_all(CLM, "state eq 'FL' and countyCode eq '12071'",
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
agg["claims"] = {
    "rows": len(clm), "total_paid": round(tot_paid),
    "by_year": {str(y): [c, round(p)] for y, (c, p) in sorted(byyear.items())},
    "claims_per_100_policies": round(100 * len(clm) / units, 1) if units else None,
}
print("claims agg done", round(time.time()-t0), "s", flush=True)
json.dump(agg, open("agg.json", "w"))

# NRI final attempt -------------------------------------------------------------
try:
    b = "https://services2.arcgis.com/EiGeaCDLpVDPqdJ5/ArcGIS/rest/services/NRI_Counties_EAL/FeatureServer/0/query"
    r = get(b + "?" + urllib.parse.urlencode({"where": "State_County_FIPS_Code=12071", "outFields": "*", "f": "json", "returnGeometry": "false"}), timeout=90, tries=3)
    feats = r.get("features", [])
    if feats:
        a = feats[0]["attributes"]
        agg["nri"] = {k: v for k, v in a.items() if any(t in k for t in ("Flooding", "Risk_Index___Rating___Composite", "County_Name", "State_Name"))}
        print("NRI ok:", len(agg["nri"]), "fields", flush=True)
    else:
        agg["nri"] = None
        print("NRI: 0 features -> gap line", flush=True)
except Exception as e:
    agg["nri"] = None
    print("NRI err -> gap line", repr(e)[:80], flush=True)
json.dump(agg, open("agg.json", "w"))
print("ALL DONE", round(time.time()-t0), "s", flush=True)
