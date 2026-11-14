# Methods review: price-gap, round 1 (2026-11-14)
Verdict: MINOR REVISION. No BLOCKER, no MAJOR verified.

Verified: Wilson 90% (z=1.6449) recomputed by hand for Pike IL 62/65 (89.0-98.1), Plaquemines LA 2433/2733 (88.0-90.0), Cheatham TN 150/216 (64.1-74.3), Davidson TN 50/173 (23.6-34.9), Tooele UT 0/44 (0.0-5.8); then all 1,793 rows by script: 0 mismatches. Sum numerator 835,905 / denominator 2,307,620 = 36.2%, matches the page. Fifths 359/359/359/357/356 (sizes fine). Rows sorted by share. 19 of top 50 in WV and 44 WV counties: both match CSV. Median gap blank exactly where below-any-amount n < 30 (0 violations); below_any_n >= numerator in every row. 19 zero-share counties all in fifth 5, named as a tie in the Abstract.

MINOR
1. Ranking by point share ignores n: Pike (n=65) is "highest" over Plaquemines (n=2,733); 20 of the next 99 counties have an upper bound above Pike's lower bound, so rank 1 is not distinguishable. Fixed in part by fifths, but the table is ordered by point share. Fix: add one sentence "ranks within a fifth are not distinguishable; counties with n under about 100 have wide ranges", or state the count of overlapping intervals.
2. Wilson interval is per county, assumes independent policies; policies in one county are clustered by flood event/map/community, so true uncertainty is wider. Limitations does not say this. Fix: one limitation line.
3. No multiple-comparison note on 1,793 simultaneous 90% intervals (about 180 expected to miss). Fix: one line in shared methods.
4. Limitations say the cause of the gap is unknown; the page does not mention the known statutory premium-increase cap as a candidate in the Prior-work or Limitations text, only in a parenthetical list. Not wrong; cite FEMA's rule if a source was read this session.
5. Prior work reconciliation: Collier example reconciles GAO by base and date; good. No numeric reconciliation of Neptune's 42% against the 43.7% any-amount pooled share (different base); add the base difference in one clause.

No causal language found; base words match code (single-family, primary, premium>0, fullRiskPremium>0); window (as of 2026-08-31) and exclusions (1,140 under 30, 94 none) stated; left-out counties' pooled share printed.
