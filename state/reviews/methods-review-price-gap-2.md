# Methods review: price-gap, round 2 (2026-11-14)
Verdict: MINOR REVISION. No BLOCKER. One label-vs-data defect (rule: always MAJOR).

Verified by script/hand: Wilson 90% (z=1.6449) for Pike IL 62/65 (89.0-98.1), Plaquemines LA 2433/2733 (88.0-90.0), Uinta WY 9/31 (17.7-43.7), Tooele UT 0/44 (0.0-5.8); all 1,793 CSV rows: 0 interval mismatches, min denominator 30, fifths 359/362/359/357/356, FIPS all 5 digits with leading zeros, median gap blank in exactly the 637 rows with below-any-amount n < 30, below_any_n >= numerator in every row. Abstract pooled 36.2% is consistent with listed 36.2% plus left-out 34.8% (12,727 policies). No causal words. Window (snapshot 2026-08-31), base, exclusions (1,140 under 30, 94 none) and clustering/multiplicity limits are stated. Round-1 minors 1-3, 5 are now fixed on the page.

MAJOR
1. CSV label vs data. Page: "Download all 1,793 rows as CSV (FIPS code, county, state, share, 90% range, numerator, denominator, in-force date, as-of date)". The CSV has 14 columns: it also holds fifth, below_any_amount_n, below_any_amount_pct and median_gap_usd_below_any_amount, and the page lists none of them. Fix: list all 14 columns, and say share_pct/numerator are the $100 line while below_any_amount_* and the median gap are the any-amount base.

MINOR
2. Table columns mix bases side by side ($100 share/count, then any-amount share, then median over any-amount policies); the any-amount column shows no count (62 of 65 vs 63 hidden). Fix: show the any-amount count in the CSV description or cell.
3. The median gap over any-amount policies is dragged down by gaps of a few dollars the $100 line was meant to exclude; the Limitations line says the base but not this effect. Fix: one clause.
4. Number of records dropped by the premium > 0 / full-risk > 0 rule is not stated on the page (only "refunds and blanks left out"). Fix: print the count.
5. Collier reconciliation leaves a 5.7-point gap (82.2% vs GAO 76.5%) explained only by base and date; say that the size of that difference from the base alone cannot be split out with the data given.
