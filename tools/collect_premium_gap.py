"""Like-for-like full-risk gap per county: re-pulls ONLY the fields the gap needs (premium charged +
fullRiskPremium + cohort fields) with collect.py's exact in-force filter, runs ffcalc.premium_gap, and
merges the result into agg.json["policies"]. Fixes the 2026-10-25 bug where policyCost (premium + fees)
was compared with fullRiskPremium (premium only). Usage: python -I tools/collect_premium_gap.py [slug ...]"""
import json, os, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffcalc

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
POL = "https://www.fema.gov/api/open/v3/NfipPolicies"
ASOF = "2026-07-31T00:00:00.000z"                       # same snapshot as collect.py
SELECT = f"id,{ffcalc.PREM},fullRiskPremium,occupancyType,primaryResidenceIndicator"
counties = json.load(open(os.path.join(HERE, "counties.json")))
if sys.argv[1:]: counties = [c for c in counties if c["slug"] in sys.argv[1:]]

def get(u, tries=6):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ff"}), timeout=240) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(min(20, 3 * (i + 1)))
    raise RuntimeError("exhausted: " + repr(last)[:90])

def q(params): return POL + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

for c in counties:
    filt = (f"propertyState eq '{c['state']}' and startswith(censusGeoid,'{c['geoid']}') "
            f"and policyEffectiveDate le '{ASOF}' and policyTerminationDate ge '{ASOF}'")
    try:
        total = get(q({"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}))["metadata"]["count"]
        seen, skip, top = {}, 0, 1000
        while len(seen) < total:
            try:
                d = get(q({"$filter": filt, "$select": SELECT, "$top": top, "$skip": skip}))
            except RuntimeError:
                if top > 125: top = max(125, top // 2); continue
                raise
            got = d[[k for k in d if k != "metadata"][0]]
            if not got: break
            for r in got: seen[r["id"]] = r
            skip += top
        if len(seen) != total:
            print(f"  {c['slug']}: INCOMPLETE {len(seen)}/{total} - skip (no partial)"); continue
    except Exception as e:
        print(f"  {c['slug']}: FAIL {repr(e)[:70]}"); continue
    rows = list(seen.values())
    if rows and ffcalc.PREM not in rows[0]:
        print(f"  {c['slug']}: SCHEMA DRIFT, {ffcalc.PREM} absent - skip"); continue
    coh = [r for r in rows if ffcalc.isone(r.get("occupancyType")) and ffcalc.istrue(r.get("primaryResidenceIndicator"))]
    gap = ffcalc.premium_gap(coh)
    ap = os.path.join(DATA, c["slug"], "agg.json")
    a = json.load(open(ap))
    old = {k: a["policies"].get(k) for k in ("frp_median", "share_below")}
    a["policies"].update(gap)
    json.dump(a, open(ap, "w"))
    print(f"  {c['slug']}: n={gap['below_n']} premium median ${gap['prem_median']} full-risk ${gap['frp_median']} "
          f"below {gap['share_below']}% (was {old['share_below']}% vs cost-with-fees)", flush=True)
print("done")
