"""Correctness gate for one built county page. Fail (exit 1) blocks ship.
Usage: python -I tools/gate.py <agg.json> <page.html> [official_count]"""
import json, re, sys

agg_path, html_path = sys.argv[1], sys.argv[2]
official = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 0
agg = json.load(open(agg_path))
html = open(html_path, encoding="utf-8").read()
fails = []

# 1. pull completeness
mani = agg.get("manifest", {})
if not mani: fails.append("no manifest")
for k, v in mani.items():
    if not v.get("complete"):
        fails.append(f"{k} incomplete: {v.get('unique_fetched')}/{v.get('reported_total')} (missing {v.get('missing')})")

# 2. required aggregates present and sane
P, C = agg.get("policies", {}), agg.get("claims", {})
for k in ("units", "p25", "p50", "p75", "frp_median", "share_below", "zone_units", "sfha_share_units"):
    if P.get(k) in (None, "", {}): fails.append(f"policies.{k} missing")
for k in ("rows", "total_paid", "by_year", "year_min", "year_max"):
    if C.get(k) in (None, "", {}): fails.append(f"claims.{k} missing")
if P.get("p25") and P.get("p75") and not (P["p25"] <= P["p50"] <= P["p75"]):
    fails.append("percentiles not monotonic")

# 3. reconciliation to FEMA official (if known)
if official and P.get("units"):
    diff = abs(P["units"] - official) / official * 100
    if diff > 5: fails.append(f"reconciliation {diff:.1f}% > 5% (units {P['units']} vs official {official})")

# 4. page content matches the data and is sourced
def money(n): return "$" + format(int(round(n)), ",")
if P.get("p50") and money(P["p50"]) not in html: fails.append(f"median {money(P['p50'])} not on page")
if "OpenFEMA" not in html: fails.append("no FEMA source attribution on page")
if re.search(r">\s*(None|nan|NaN|undefined)\s*<", html): fails.append("None/nan leaked into page text")
if "$None" in html or "None%" in html: fails.append("None leaked into a number")

# 5. NRI present or an explicit gap line (never silently missing)
if not agg.get("nri") and "Gap:" not in html:
    fails.append("NRI missing without a gap line")

# 6. suppression consistency: spread chart shown iff >= 100 VALID COST observations (cost_n), not raw cohort
cn = P.get("cost_n") or 0
spread_ok = P.get("spread_ok", cn >= 100)
has_spread = "Annual NFIP cost spread" in html
if not spread_ok and has_spread: fails.append(f"cost_n {cn} < 100 but percentile spread chart shown")
if spread_ok and not has_spread: fails.append(f"cost_n {cn} >= 100 but spread chart missing")

if fails:
    print("GATE FAIL:")
    for f in fails: print("  -", f)
    sys.exit(1)
print("GATE PASS:", html_path, f"(units {P.get('units')}, median {money(P['p50'])}, reconc "
      + (f"{abs(P['units']-official)/official*100:.1f}%" if official else "n/a") + ")")
