# Methods review: Flood Calendar, round 1 (hostile biostatistics reviewer, 2026-11-13)

Verdict: MAJOR REVISION

Checked: all 416 CSV rows recomputed (Wilson 90%, z=1.645) for share and both interval ends: 0 mismatches. Rows 1 (Pamlico 1279/1288 = 99.3, 98.8-99.6), 201 (Pierce WA 78/133 = 58.6, 51.5-65.4) and 416 (Dallas 90/473 = 19.0, 16.2-22.2) also by hand. Fifths: 84/84/85/80/83, equal printed shares share a fifth. 404 CSV rows carry a year_month_over_half value, matching the page. NOT checked: counts against the raw OpenFEMA files (cloud-only; the page's own numerators are taken as given).

## BLOCKER
None.

## MAJOR
1. Ranking is confounded by n and has no null benchmark (misleading ranking). The statistic is the maximum of 12 monthly shares, so even with NO seasonality its expected value depends on n. My simulation (uniform months, 300 draws): expected peak share 13.3% at n=100, 10.6% at n=473, 9.4% at n=2000 (floor 8.3%). The page calls Dallas "the lowest share, 19.0%" and sorts all counties into fifths by this share; low-n counties are pushed up by construction. Fix: print the no-seasonality expectation by n (or a permutation/simulated null per county) beside each share, and rank on excess over that null or within n bands; state in Results that 1/12 = 8.3% is the floor.
2. Label vs data: title and measure say "Flood Calendar / peak month", but 404 of 416 counties (97%) have one year holding over half of the peak month ("not a yearly season", Abstract). The measure is mainly storm concentration, not calendar seasonality; the headline "69.9% fell in their county's peak month" will be read as seasonality. Fix: rename (e.g. "Peak month of NFIP claims") and lead the Abstract with the 404/416 finding; add a seasonality-bearing field such as the count of distinct loss years with claims in the peak month, or the peak-month share after removing the single largest year-month.
3. Intervals mislead on precision. "90% range 98.8-99.6%" for Pamlico treats 1,288 claims as independent, yet over half the peak month is September 2018 alone (one storm). The only warning ("not independent") sits in the second Limitations bullet and does not say that the printed range is therefore far too narrow for the quantity the page wants (a yearly pattern); the "narrower than it should be" bullet blames only the max-selection. Fix: say both causes in the Table note, and either drop per-row ranges for flagged rows or label them "range if claims were independent".

## MINOR
4. Left-out comparison is not like for like: left-out counties (n<100, median 54.9%) have inflated shares from small n (see 1), so "not a sample of every county" compares different n regimes. Compare within n bands or drop the median comparison.
5. Abstract opens with 68.8% of 555,028 (all counties pooled) and then 69.9% of 515,295 (listed counties): two bases in one lede. Keep one in the Abstract, move the other to Results.
6. "11 of the 50 ... are in Florida, which has 44 of the 416" is descriptive but invites a causal reading; add base rate in words (22% vs 11%) or cut.
7. Prior work rests on 3 searches and cites nothing. Seasonality of flood claims (hurricane-season claim volume, national monthly claim counts, the 30-day-wait seasonality of policy purchase) is discussed in NFIP literature; name at least one source and say what this adds (county level, storm-concentration flag, CSV). I did not search, so this is unverified as a defect.
8. Window is by yearOfLoss while the month is read from dateOfLoss; state that the two fields were verified consistent (a year-boundary claim would fall in the wrong window).

## Clean
No causal words found in findings; no "significant"; base named with each share; Wilson implementation correct; ties named; min n = 100 stated.
