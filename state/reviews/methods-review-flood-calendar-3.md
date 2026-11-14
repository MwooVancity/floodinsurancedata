# Methods review: Peak month of NFIP claims by county, round 3 (hostile biostatistics reviewer, 2026-11-13)

Verdict: MINOR REVISION

Checked by script from the CSV: all 416 rows, Wilson 90% (z = 1.6448536) = 0 mismatches against share, low, high. Hand rows: Monroe 8529/8636 = 98.8 (98.5-98.9), Pamlico 1279/1288 = 99.3 (98.8-99.6), Dallas 90/473 = 19.0 (16.2-22.2), Erie 24/110 (16.1-28.9). Rows sorted by excess (descending, true); fifths are contiguous, sizes 84/83/84/83/82, no excess value straddles a boundary. Excess = share minus expected within 0.1 (rounding). Peak months: Sept 113, Aug 74, Oct 50 match the page; 44 FL counties, 11 FL in the top 50 match. Flag column (404) equals "largest year share over 50" in every row (0 disagreements). No tied peak months occur in the table. Median largest-year share 95.55 (page prints 95.5), median years-with-10+ = 1.0. NOT checked: numerators against raw OpenFEMA (cloud only); expected-at-random re-simulation (done in round 2, unchanged code).

Round 2 majors 1 and 2 are fixed: the "not a pattern that repeats" claim is gone, the flag is described as "one year holds over half", graded columns (largest year's share, years with any claim, years with 10+) are in page and CSV, "at least a twelfth" and "z = 1.6449" are corrected.

## BLOCKER
None.

## MAJOR
None verified.

## MINOR
1. Selection comparison still crosses n regimes (round 1 minor 4, round 2 minor 4, third time). Methods: "the median share of claims in the peak month is 54.9% and the pooled share 54.3%, so the listed counties are not a sample of every county". Counties under 100 claims have a higher chance-level peak share (13.3% at n=100, higher below), so 54.3% vs 69.9% is not like for like, and "so ... not a sample" is an inference from it. Fix: print the left-out counties' claim-weighted expected share at random beside 54.3%, or drop the "so" clause.
2. Year-month key mixes fields. The window is by yearOfLoss but the month comes from dateOfLoss[5:7] and the year-month key is yearOfLoss + that month (tools/extras_raw.py, the `a["ym"]` line). A claim whose yearOfLoss differs from the year in dateOfLoss would be filed under a wrong month-year, which feeds the "September 2017" flag and the largest-year share. Not shown wrong (raw data not local). Fix: key on dateOfLoss[:7], or print the mismatch count in Methods.
3. Prior work reconciles nothing. It states no ranking was found after three web searches and cites no source. The finding "September in 113 counties" is the Atlantic hurricane season; say that agreement with the known season is a consistency check, and name one seasonality reference or state that literature databases were not searched.
4. Peak month is chosen and measured on the same claims; no out-of-sample check. Limitations says the share is biased up and the range is too narrow, which is honest, but a split (pick the peak on 2016-2020, measure on 2021-2025) would show whether the peak month repeats, the question readers actually bring. Optional; if not built, say the page does not test it.
5. Abstract median "95.5%" is the midpoint of two rounded CSV values (95.5 and 95.6 gives 95.55); the printed digit depends on float rounding. Print 95.6 or "about 96%".
6. Feb 29 and month lengths: the null treats months as equal; stated in Limitations, but 2016 and 2020 leap days are not mentioned. Trivial.

## Clean
No causal language in findings; the "so" in the 30-day sentence is about policy timing, not about the data. "Significant" and tests absent. Window (loss years 2016-2025), exclusions (codes 98 and 99, no-month, under-100 counties, 2,104 and 507 counted) stated. Bases named with each share. Ranges labelled "if claims were independent" with both reasons. Fifths used, no bare rank. Limitations present (single flood, claims not floods, short record, countyCode caveat, NFIP only).
