# Methods review: Damage over coverage (formerly Underinsured), round 2 (2026-11-13)

Verdict: MAJOR REVISION (one MAJOR; all round-1 MAJORs otherwise fixed)

Recomputed: all 268 CSV rows, Wilson 90% (z=1.645) and share: 0 mismatches. Sum n = 273,450, sum numerator = 13,326 (4.9%). Hand spot-checks: Humphreys TN 54/103 = 52.4% (44.4-60.4); Walton FL 0/107 (0.0-2.5); Newton TX 74/306 (20.4-28.4): all match. 21 zero-share counties = 21 (matches abstract). Texas 28 listed, 10 of top 50: matches. Median county 2.1%: matches. Fifths 54/55/52/62/45.

## Prior items
| # | Prior | Status |
|---|---|---|
| 1 | MAJOR base words dropped damage/coverage conditions | FIXED: unit string "with recorded damage and coverage" used in lede, Methods, Results, Reproduce; Data Base sentence complete |
| 2 | MAJOR single-family undefined | FIXED: condominiumCoverageTypeCode and primaryResidenceIndicator listed; "not a condominium coverage type" |
| 3 | MAJOR "Underinsured" title | FIXED: title, H1, CSV and URL say damage over building coverage; Limitations says it is not the uninsured loss |
| 4 | MAJOR no size (M1.4) | FIXED: "Median amount damage was over coverage" column and CSV median_excess_usd; blank for 0-numerator rows |
| 5 | MAJOR one event (M1.8) | PARTLY FIXED: column added, but see N1 |
| 6 | winner's curse | FIXED enough: n beside the maximum in the abstract |
| 7 | mixed bases in one sentence | MINOR open: lede still joins "4.9% of 303,311 ... all U.S. counties" and "4.9% (90% range...)" in one sentence; the first has no range, and "all U.S. counties" still omits blank/unmatched countyCode |
| 9 | Texas bare ratio | FIXED: "which has 28 of the 268 listed counties" |
| 10 | unaudited damage values | MINOR open: Limitations has no line that damage is as recorded and extreme values are not audited |
| 12 | prior-work queries | MINOR open: one query still logged |
| shared | "paid" conflict | FIXED: "unless a paper's Base says otherwise" |

## New findings

N1. MAJOR (label vs data). Limitations: "Where one loss year holds over half of a county's claims over coverage (marked in the table), those claims come largely from one flood and are not independent". A loss year is not a flood (several events fall in one year; FEMA's floodEvent field is not used). Also the flag is near-uninformative: 208 of 247 counties with any claim over coverage are marked, 104 of them with fewer than 10 such claims (3 of 5 in one year is "over half"). Yet only 58 of 60 counties with 30+ numerator claims are marked, so the column marks nearly everyone. Fix: say "from one loss year (which may be one flood or several)", and either require a minimum numerator (for example 10) before marking or mark by a larger threshold; state the rule in the table caption. A reader cannot tell Harris 2017 (Harvey) from a 2-of-3 county.

N2. MINOR. Same sentence says the 90% range "is narrower than it should be" only for marked counties; claims cluster by event in every county, so every printed binomial range is conditional on independence. Shared methods card says claims are not independent but not what it does to the per-county range. Fix: one clause in the shared card: "county ranges assume independent claims and are narrower than the true uncertainty".

N3. MINOR. Table column header "Loss year with over half of them" is ambiguous (over half of what). Fix: "Loss year holding over half of the claims over coverage".

N4. MINOR. Abstract names Humphreys (n=103) as the "highest share"; n and range are printed in Results but ranking by point estimate still picks the smallest-n counties (18 of 54 top-fifth counties have n under 150). Acceptable; keep n adjacent.

No causal words, no "significant", no advice found. Reproduce text matches the code base (building payment, damage, coverage above $0; single-family primary home; 2016-2025; 98/99 out).

## Round 2b (N1 re-check)

Verdict: MINOR REVISION

N1 FIXED. CSV: 104 counties flagged, minimum numerator among flagged = 10 (rule holds); 113 counties have 10+ claims over coverage, so 9 of them have no year over half (flag now discriminates). Humphreys 54 in 2021 and Harris 3,618 in 2017 still marked. Limitations now reads "cluster in one year, which may hold one flood or several"; header "(only with 10 or more)"; abstract states the 2021 year and the 104 count, matching the CSV. No new BLOCKER/MAJOR. Remaining MINOR: N2-N4 and round-1 items 7, 10, 12 unchanged.
