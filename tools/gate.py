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

# 7. no event shown with a year beyond now (catches FEMA fiscal-year mislabels like FY2027 on an Oct 2026 date)
import datetime
this_year = datetime.date.today().year
for y in re.findall(r"<li>(\d{4}) — ", html):   # recent-event items "<li>YYYY — ..."
    if int(y) > this_year:
        fails.append(f"declaration shows future year {y} (fiscal-year mislabel?)")

# 8. DATA-INTEGRITY & DISCLOSURE AUDIT — the arithmetic QC, every number reconciled to agg,
#    every ratio's denominator disclosed, no figure that reads as something it is not.
units = P.get("units") or 0
sfha = P.get("sfha_units")

# 8a. SFHA share must equal sfha_units/units recomputed (a wrong denominator is the exact bug we shipped),
#     and that exact percentage must appear on the page.
if units and sfha is not None:
    recomputed = round(100 * sfha / units, 1)
    if P.get("sfha_share_units") != recomputed:
        fails.append(f"sfha_share_units {P.get('sfha_share_units')} != sfha_units/units {recomputed} (wrong denominator)")
    if f"{P.get('sfha_share_units')}%" not in html:
        fails.append(f"SFHA share {P.get('sfha_share_units')}% not shown on page")

# 8b. Denominator disclosure: the share is of POLICY UNITS, not of all buildings — the page must say so,
#     and the truncated zone list must disclose the units it does not show (so summing rows can't mislead).
if sfha is not None:
    if "of all buildings" not in html:
        fails.append("SFHA share shown without disclosing the denominator ('not ...% of all buildings')")
    # the template lists the top 8 zones; a remainder disclosure is required only when those 8 don't
    # account for every unit (i.e. the list is actually truncated).
    shown8 = sum(list(P.get("zone_units", {}).values())[:8])
    if shown8 < units and "other or unclassified" not in html.lower():
        fails.append("zone list is truncated but does not disclose the remaining (other/unclassified) units")

# 8c. Dataset count self-consistency: the count the page states must equal the sources it actually lists.
blk = re.search(r'srclist">(.*?)</ul>', html, re.S)
if not blk:
    fails.append("no visible federal-sources block on page")
else:
    n_listed = len(re.findall(r"<li>", blk.group(1)))
    m = re.search(r"joins\s+(\d+)\s+of them", html)
    if m and int(m.group(1)) != n_listed:
        fails.append(f"stated dataset count {m.group(1)} != {n_listed} sources actually listed")

# 8d. A ratio that reads like a risk score must carry its caveat.
if re.search(r"per 100", html, re.I) and not re.search(r"cumulative|not an annual rate", html, re.I):
    fails.append("claims-per-100 shown without a 'cumulative / not an annual rate' caveat")

# 8e. Claims totals reconcile to agg: grand total and the single largest loss year must both be on the page.
tp = C.get("total_paid")
if tp and money(tp) not in html:
    fails.append(f"claims total {money(tp)} not on page")
by = C.get("by_year") or {}
if by:
    ty, (tc, typaid) = max(by.items(), key=lambda kv: kv[1][1])
    if money(typaid) not in html:
        fails.append(f"largest loss year {ty} ({money(typaid)}) not reconciled on page")

# 8f. Full-risk comparison must be framed as a distribution, never an individual forecast/quote.
if P.get("frp_median") and money(P["frp_median"]) in html and not re.search(r"not a quote", html, re.I):
    fails.append("full-risk shown without a 'not a quote' caveat")

# 9. freshness metadata present (strongest AI-citation correlate; must reflect a real data date)
if '"dateModified"' not in html:
    fails.append("no dateModified in schema (freshness metadata missing)")

if fails:
    print("GATE FAIL:")
    for f in fails: print("  -", f)
    sys.exit(1)
print("GATE PASS:", html_path, f"(units {P.get('units')}, median {money(P['p50'])}, reconc "
      + (f"{abs(P['units']-official)/official*100:.1f}%" if official else "n/a") + ")")
