# Methods review: Peak month of NFIP claims by county, round 2 (hostile biostatistics reviewer, 2026-11-13)

Verdict: MAJOR REVISION

Checked by script from the CSV: all 416 rows, Wilson 90% with the exact z (1.6448536) = 0 mismatches (with the z = 1.645 the page prints, 4 rows differ by 0.1: Richmond, Bertie, Sussex, St. Mary). Expected-at-random column: re-ran the seeded 4,000-draw null per county, 416/416 equal to the digit; an independent seed (20,000 draws) gives 13.3 / 10.6 / 8.8 at n = 100 / 473 / 8,636,. Excess = share minus expected within 0.05 for all rows; rows sorted by excess. Pooled 360,391 / 515,295 = 69.9%; claim-weighted expectation 9.31%; county-resampling range by my own bootstrap 66.35-72.75 (page 66.4-72.7); median share 56.85 and median expected 11.3; 44 FL counties, 11 FL in the top 50; 404 flagged rows; peak-month counts September 113, August 74, October 50. Hand check: Iroquois 196/200 = 98.0 (95.6-99.1), Linn 169/179 = 94.4 (90.9-96.6), Dallas 90/473 = 19.0 (16.2-22.2). NOT checked: numerators against raw OpenFEMA (cloud only).

Round 1 majors 1-3 are fixed (null per n and ranking on excess; renamed, no calendar/season word, 404/416 leads; ranges labelled "if claims were independent" with both causes).

## BLOCKER
None.

## MAJOR
1. Label vs data: the flag does not measure what the sentence claims. Abstract and Limitations: "the peak month is mostly one year's flood, not a pattern that repeats each year". The flag is only "one year-month holds over half of the peak month's claims". Over half in one year does not show the month does not recur: Monroe County is flagged (September 2017) yet its table column says claims fell in the peak month in 7 of 10 loss years; Baldwin AL 5, Escambia FL 6, Ouachita 6. With 10 years and clustered claims, "largest year over half" is expected for almost any county, so 404/416 (97%) has almost no power to separate storm-driven from recurring. Fix: replace the claim with what is measured ("one year-month holds over half of the peak month's claims; the peak month also had claims in N of 10 loss years"), drop "not a pattern that repeats each year", and add a graded measure (share of the peak month held by its largest year, or the peak-month share with the largest year-month removed and the peak re-picked) as a CSV column.
2. Label vs data: "Loss years with claims in the peak month" counts a year with even one claim (Greenbrier WV: 2 years, 344 claims; Monroe FL: "7" says nothing about 8,529 claims being mostly one September). Read beside "recurs", it overstates regularity. Fix: rename to "loss years with at least one claim in the peak month" and give the number of years with a material count (e.g. 10 or more), or the largest year's share.

## MINOR
3. Reproduce says "z = 1.645"; the code uses 1.6448536, and 4 rows differ in the last digit if the stated z is used. Say "z = 1.6449" or the exact value.
4. Left-out comparison (54.9% median, 54.3% pooled vs 69.9%) is still across different n regimes: the chance expectation for n under 100 is above 13.3%, so shares are not comparable. Print the left-out counties' own expected-at-random figure (claim-weighted) or drop the comparison. (Round 1 minor 4, not addressed.)
5. Abstract and Methods: "since the largest of twelve months always holds more than a twelfth" should read "at least a twelfth" and avoid "since" (reads causal, M1.9 spirit).
6. Window by yearOfLoss but month from dateOfLoss, and the year-month key (the flag source) is built from yearOfLoss plus the date's month (tools/extras_raw.py lines 183-187). If a claim's yearOfLoss differs from the year in its dateOfLoss, the flag names a wrong month-year. Page does not state the two fields were checked consistent. (Round 1 minor 8, not addressed; unverified, raw data not available locally.) Fix: key on dateOfLoss[:7] or print the count of mismatches.
7. Prior work still cites nothing and rests on 3 searches (R0.1 asks 3+ extended). Seasonality of NFIP claims and policy purchase by hurricane season is a known theme in NFIP literature; name a source or state the search found none in the literature databases. I did not search, so this is unverified as a defect.
8. Ranking by excess over a uniform-month null still mixes two things (concentration in one month and one storm); it is labelled, but the Abstract's "largest excess" example (Monroe 98.8% vs 8.8%) is Hurricane Irma-scale concentration and reads as seasonality; the Limitations bullet about day-length is trivial next to this. Add one sentence that a high excess can be one event.

## Clean
No causal words in findings other than item 5; no "significant" or test; base named with each share; Wilson implemented correctly; ties named (none occur in the table); min n = 100 stated; rows, CSV, and fifths consistent.
