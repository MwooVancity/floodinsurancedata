# Methods review: price-gap, round 3 (2026-11-14)
Verdict: MINOR REVISION. No BLOCKER, no MAJOR.

Verified by script over all 1,793 CSV rows: Wilson 90% (z=1.64485) low/high and share match in every row (0 mismatches); hand-checked Pike IL 62/65 (89.0-98.1), Plaquemines LA 2433/2733 (88.0-90.0), Taney MO 43/49 (78.0-93.5). Sum numerator 835,905 / denominator 2,307,620 = 36.2%; any-amount 43.7%; median county 29.0%; 19 counties at 0.0%; 19 of the top 50 are WV and WV has 44 listed counties; table sorted by share; equal shares share one fifth (0 splits); no tie across the top-50 cut (rows 50/51 are 77.2 and 76.5); below_any >= numerator everywhere; median gap blank exactly where below_any_n < 30. Round-2 MAJOR (CSV column label) is fixed: the page now lists all 14 columns and which are the $100 base and which the any-amount base. No causal words, window and exclusions (1,140 under 30, 94 none), independence and multiplicity limits all stated.

MINOR (carried from round 2, still on the page)
1. Median gap over any-amount policies is pulled down by the few-dollar gaps the $100 line excludes; Limitations names the base but not the effect. Fix: one clause.
2. Count of records dropped by the premium > 0 / full-risk > 0 rule is not printed. Fix: print it.
3. Collier: 82.2% (any amount) vs GAO 76.5% is a 5.7-point gap explained by base and date only; say the two causes cannot be split with the data given.
4. Ranking is by share alone, so the top is small-n counties (Pike IL n=65); already disclosed in Limitations, and fifths and ranges are shown. Optional: a count-weighted note near the top-100 table.
