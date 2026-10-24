"""Add FEMA repetitive-loss (RL/SRL) property aggregates per county via light COUNT queries (no full
row pull), merging into each county's data.json as 'multiloss'. Source: OpenFEMA
IndividualAssistanceMultipleLossFloodProperties v1 (keyless), join fipsStateCode + fipsCountyCode.
These are FEMA-designated properties with multiple flood losses over time — a chronic-flood signal
distinct from one-time claims, and the share still uninsured is a real coverage-gap stat.
Usage: python -I tools/collect_multiloss.py   (runs all counties in tools/counties.json)"""
import json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
BASE = "https://www.fema.gov/api/open/v1/IndividualAssistanceMultipleLossFloodProperties"
counties = json.load(open(os.path.join(HERE, "counties.json")))

def count(filt, tries=5):
    u = BASE + "?" + urllib.parse.urlencode(
        {"$filter": filt, "$top": 1, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote)
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ff"}), timeout=90) as r:
                return json.load(r)["metadata"]["count"]
        except Exception as e:
            last = e; time.sleep(3 * (i + 1))
    raise RuntimeError(f"exhausted: {last!r}")

for c in counties:
    geo = c["geoid"]; st, co = geo[:2], geo[2:]      # 5-digit FIPS -> state + county (leading zeros kept)
    base_f = f"fipsStateCode eq '{st}' and fipsCountyCode eq '{co}'"
    # NOTE: floodInsurance is false for every record in this IA dataset (IA goes to uninsured losses), so a
    # "% uninsured" would be a tautology — deliberately NOT collected. total = RL + SRL; SRL broken out.
    try:
        total = count(base_f)
        srl = count(base_f + " and highRiskPropertyType eq 'SRL'") if total else 0
    except Exception as e:
        print(f"  {c['slug']}: FAIL {repr(e)[:80]} — skipped (panel shows gap)"); continue
    dpath = os.path.join(DATA, c["slug"], "data.json")
    try:
        d = json.load(open(dpath))
    except Exception:
        d = {}
    d["multiloss"] = {"total": total, "srl": srl,
                      "retrieved": "2026-10-24", "source": "OpenFEMA IndividualAssistanceMultipleLossFloodProperties v1"}
    json.dump(d, open(dpath, "w"))
    print(f"  {c['slug']}: total={total} srl={srl}")
print("done")
