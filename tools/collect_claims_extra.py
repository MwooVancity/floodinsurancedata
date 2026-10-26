"""Payout reality + claims-outside-SFHA per county, from the SAME NFIP Claims dataset (keyless), re-pulled
with ratedFloodZone + net payments. Merges into data.json as 'claims_extra':
  avg_paid         = mean net payment over paid claims (building+contents+ICC)
  cwop_share       = share of claims closed with NO payment (net total == 0)
  outside_sfha_pct = share of PAID claim dollars on claims rated in a non-high-risk (X) zone
Answers "do claims actually pay?" and "do claims happen outside the 100-year zone?". The share-outside-SFHA
is the direct, local rebuttal to "I'm not in the flood zone, I don't need it." Usage: python -I tools/collect_claims_extra.py"""
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
CLM = "https://www.fema.gov/api/open/v3/NfipClaims"
counties = json.load(open(os.path.join(HERE, "counties.json")))

def get(u, tries=6):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ff"}), timeout=180) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(min(20, 3 * (i + 1)))
    raise RuntimeError("exhausted: " + repr(last)[:90])

def page(filt, select):
    cnt = get(CLM + "?" + urllib.parse.urlencode({"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote))
    total = cnt["metadata"]["count"]; seen = {}; skip = 0; top = 1000
    while len(seen) < total:
        try:
            d = get(CLM + "?" + urllib.parse.urlencode({"$filter": filt, "$select": select, "$top": top, "$skip": skip}, quote_via=urllib.parse.quote))
        except RuntimeError:
            if top > 125: top = max(125, top // 2); continue
            raise
        got = d[[x for x in d if x != "metadata"][0]]
        if not got: break
        for r in got: seen[r["id"]] = r
        skip += top
    return list(seen.values()), total

def net(r): return (r.get("netBuildingPaymentAmount") or 0) + (r.get("netContentsPaymentAmount") or 0) + (r.get("netIccPaymentAmount") or 0)

for c in counties:
    filt = f"state eq '{c['state']}' and countyCode eq '{c['geoid']}'"
    try:
        rows, total = page(filt, "id,ratedFloodZone,netBuildingPaymentAmount,netContentsPaymentAmount,netIccPaymentAmount")
        if len(rows) != total:
            print(f"  {c['slug']}: INCOMPLETE {len(rows)}/{total} — skip (no partial)"); continue
    except Exception as e:
        print(f"  {c['slug']}: FAIL {repr(e)[:70]}"); continue
    n = len(rows)
    if not n:
        print(f"  {c['slug']}: 0 claims"); continue
    paid = [r for r in rows if net(r) > 0]
    cwop = sum(1 for r in rows if net(r) <= 0)
    paid_total = sum(net(r) for r in paid)
    outside = sum(net(r) for r in paid if (r.get("ratedFloodZone") or "")[:1] not in ("A", "V"))
    rec = {"claims": n, "avg_paid": round(paid_total / len(paid)) if paid else 0,
           "cwop_share": round(100 * cwop / n, 1),
           "outside_sfha_pct": round(100 * outside / paid_total, 1) if paid_total else None,
           "paid_n": len(paid), "retrieved": "2026-10-25",
           "source": "OpenFEMA NFIP Claims v3 (ratedFloodZone + net payments)"}
    dp = os.path.join(DATA, c["slug"], "data.json")
    try: dd = json.load(open(dp))
    except Exception: dd = {}
    dd["claims_extra"] = rec; json.dump(dd, open(dp, "w"))
    print(f"  {c['slug']}: avg ${rec['avg_paid']:,} cwop {rec['cwop_share']}% outside-SFHA {rec['outside_sfha_pct']}% (n={n})")
print("done")
