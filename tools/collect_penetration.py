"""Add NFIP residential take-up per county from OpenFEMA NfipResidentialPenetrationRates (keyless),
merging into data.json as 'penetration'. Overall + inside-SFHA rates answer "how many homes here actually
carry flood insurance, including in the high-risk zone". Usage: python -I tools/collect_penetration.py"""
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
BASE = "https://www.fema.gov/api/open/v1/NfipResidentialPenetrationRates"
counties = json.load(open(os.path.join(HERE, "counties.json")))

def get(u, tries=5):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ff"}), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise RuntimeError(repr(last)[:90])

for c in counties:
    u = BASE + "?" + urllib.parse.urlencode({"$filter": f"fipsCode eq '{c['geoid']}'", "$top": 1}, quote_via=urllib.parse.quote)
    try:
        d = get(u); rows = d[[x for x in d if x != "metadata"][0]]
        if not rows:
            print(f"  {c['slug']}: no penetration row"); continue
        r = rows[0]
        rec = {"overall_pct": round((r.get("resPenetrationRate") or 0) * 100, 1),
               "sfha_pct": round((r.get("resPenetrationRateSfha") or 0) * 100, 1),
               "contracts": r.get("resContractsInForce"), "sfha_contracts": r.get("resContractsInForceSfha"),
               "asof": (r.get("asOfDate") or "")[:10],
               "source": "OpenFEMA NfipResidentialPenetrationRates v1"}
    except Exception as e:
        print(f"  {c['slug']}: FAIL {repr(e)[:60]}"); continue
    dp = os.path.join(DATA, c["slug"], "data.json")
    try: dd = json.load(open(dp))
    except Exception: dd = {}
    dd["penetration"] = rec; json.dump(dd, open(dp, "w"))
    print(f"  {c['slug']}: overall {rec['overall_pct']}% / SFHA {rec['sfha_pct']}%")
print("done")
