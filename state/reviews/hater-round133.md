# Hater round 133 (light, text only)

Checked against data/c/<slug>/{agg,data,extras}.json, data/us/map_status.json, state agg/extras (FL, CA). Changed-this-week items verified: opening sentence gone and median tile label carries basis and in-force date (all four PASS); "more zones below" (true only on Levy, where Zone X is priced; absent and correct on Dixie, Wakulla, Sonoma); decade sentence (Wakulla names 2010s as latest decade with 30+ claims and 2020s as 26 claims, matches by_decade); "within one percent" (Dixie $987 vs FL $985, rounds to 0%, values differ: correct); payout note wording present on all four; outside-zones counts printed under 30 (Dixie 4 of 325, Levy 3 of 640, Wakulla 5 of 305; Sonoma 80 of 925 no count, correct); map-service source line one date (November 9, 2026) on all four. Ranks (25th/55, 4th/55, 5th/55, 12th/42), LOMA splits, decade sums, unpaid-reason sums, zone-unit shares, p25/p75/p90, deductibles all recompute.

## dixie-county-fl
- **MAJOR** Flood-map card: "the oldest in effect since September 29, 2006 and the newest since September 9, 9999". `data/us/map_status.json` 12029 has `newest: "9999-09-09"`, FEMA's placeholder for a panel with no effective date. The page prints a sentinel as a real date; a reader sees an impossible year. Check that should have caught it: a date-range/sanity gate on `map_panel_date` (year > as-of year = drop the value or say "one or more panels have no effective date yet"). Same data path can hit any county whose newest panel carries the placeholder.
- MINOR "FEMA gives no county for 1.2% of this state's policy units and 1,403 of its claims": a percent and a count in one sentence, different bases (units vs claims). Give the claim share (0.3%) or both counts.
- MINOR Ranked "Bordering and other counties" row lists Miami-Dade, Broward, Lee, Pinellas, Palm Beach beside Levy; only Levy borders Dixie. Label says "Bordering and other", so true, but 5 of 6 links are not neighbours.
- **GAP** Priced base is small (182 single-family, 134 in Zone AE); page prints the counts everywhere it matters, so no defect. Top results show the same thin base.
Verdict: FAIL

## levy-county-fl
- MINOR Screen 1 "Zone VE, 21.5% of policy units, has too few to price; more zones below." Correct (Zone X $753, 51 priced, is in the card), but the screen-1 line never names Zone X, so "more zones" is only resolvable by scrolling. Acceptable by the new rule.
- MINOR Same percent-and-count mix as Dixie in the "gives no county" line.
- MINOR "Policies first bought in the past year typically pay $2,034" rests on 37 policies; the count is printed in the comparison table ("37 policies, past year") but not on screen 1 where the figure first appears.
Verdict: PASS

## sonoma-county-ca
- MINOR "By ZIP it ranges from $1,139 (94931) to $1,757 (95462 Monte Rio)": 94931 (37 priced policies) is not in the ZIP table, which shows only the top 8 ZIPs by priced policies and does not say it is cut off. The number is right (data: 94931 median 1,139) but the reader cannot find it on the page except through the lookup.
- MINOR California has 286 claims with no county (0.6% of its claims, `no_county.claims`); the Florida pages say so, this page prints no such line because unplaced policy units are 0.0%. Claims on this page are therefore understated by an unstated amount, unlike the FL pages.
- MINOR "Of the NFIP claim dollars paid here (1978–2026), 10.6% ... outside high-risk zones" next to "8.6% ... (2016–2025) ... 7.4% of dollars": different bases, both labelled; a quick reader may take them as a contradiction.
- **GAP** Event table leads with the catch-all "Flooding (1978–1997)" row ($67.3 million) above the named floods; labelled as many floods, so not wrong. 1995 and 2019 (two costliest years) have no named flood row.
Verdict: PASS

## wakulla-county-fl
- MINOR Screen 1 lists zones as "AE, VE, A, X"; the card sorts "AE, VE, X, A" (by priced count). Same four, same figures, different order.
- MINOR 2.5% (all years, "outside high-risk zones") and 1.0% (2016–2025 dollars) both appear; different bases, both labelled.
- MINOR Disaster list shows "October 2026 — Hurricane Isaias" as one line for an emergency (Oct 9) and a major declaration (Oct 27); the merge rule says it states how many, and no count is shown for the merged line.
Verdict: PASS

## Classes
- Sentinel-date class (map card, every county page): any county whose newest panel effective date is FEMA's placeholder 9999-09-09 prints it verbatim. Scan all `map_status.json` rows for `newest` or `oldest` year > 2030; add a gate and a test_factory case with a 9999 panel date.
- Percent-and-count mix in the "gives no county" line (every FL page).
- ZIP range sentence can cite a ZIP the capped ZIP table omits (any county with more than 8 ZIPs).
