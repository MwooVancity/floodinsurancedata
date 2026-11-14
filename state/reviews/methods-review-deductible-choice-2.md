# Methods review, deductible-choice, round 2 (hostile biostatistics)
Verdict: MINOR REVISION (zero BLOCKER, zero MAJOR; round-1 MAJOR "choice" label is fixed; five round-1 MINORs still open)

## Verified this round (own script, raw county files plus CSV)
- CSV: 1,793 rows, 1,793 unique FIPS, min denominator 30. All 1,793 rows recomputed with Wilson 90% (z = 1.6448536): zero differences in share, low or high. Hand rows: Marengo AL 36/53 = 67.9 (56.7-77.4); Delaware County 198/924 = 21.4 (19.3-23.7); King George VA 0/37 = 0.0 (0.0-6.8). All match.
- Page numbers: listed pool 345,151 / 2,300,276 = 15.0%; median county 21.5%; 6 counties at 0.0%; Alabama 5 of top 50, 39 listed counties. All match. All counties (incl. under 30): 348,278 / 2,312,971 = 15.1%; left-out counties 1,139 with 12,695 units, pooled 24.6%, median 21.4%; 95 counties with none. All match the page.
- Base in code vs words: extras_raw.py sums policyCount (u) into deductible_units only for codes in codes.DEDUCTIBLE; blank or other codes go to deductible_units_blank (7,376 units, 0.3%). Numerator (codes 5, A-E = $5,000+) and denominator (all 14 listed codes) come from the same dict and the same records. Words match code. paper_gate line 20 checks sf_n = sum(units) + blank.
- Label-vs-data: title, question, measure, "meets" all say "on record"; no "choice" word in any label; Limitations says the recorded deductible is not shown to be the owner's choice. Zero label mismatches found. Ties: the 0.0% tie is named (6 counties). No causal word, no "significant".

## BLOCKER
None.

## MAJOR
None.

## MINOR (repeats from round 1 marked R1)
m1 (R1) Ranking by point share with wide, overlapping ranges: top row is 36 of 53 (56.7-77.4), most top-100 rows have n under 100. "Highest share is Marengo County" reads as a clear leader. Fix: add to Results "ranges of nearby rows overlap; the top rows are mostly small counties" (n is already beside each row).
m2 (R1) Prior work not reconciled: Taylor & Francis 2020 (national, owner-occupied single-family, "maximum" deductible) is cited but the page's national 15.1% at $5,000 or more is not compared. Fix: one sentence naming the base, threshold and window differences, so the numbers are not read side by side; do not quote their figure unless read from source this session.
m3 (R1) Michel-Kerjan and Kousky (Florida) is introduced as "work on NFIP deductible choice" (sentence says "Published work on NFIP deductible choice"); its subject is purchase and renewal. Fix: relabel the link "(Florida purchase behaviour, not a county ranking of deductibles)" or drop it unless a deductible finding in it is read.
m4 (R1) Wilson range treats units as independent draws from a population, but the data are a census of policies on one date and units in a county share agents, lenders and program rules. Methodology states the independence caveat only for the county-resampling range. Fix: one Methods sentence: "the county range shows count noise from the size of the base, not sampling error."
m5 (R1) Excluded units not printed on this page: 7,376 units (0.3%) left out for a blank or unlisted code; the page only says they are left out. Fix: print the number and share (deductible_units_blank is already in the data).
m6 Limitations does not say who can set a deductible (program minimums by coverage level, lender or agent practice). It says only "not shown to be the owner's choice". Fix: add "program rules, lenders or agents may set or limit it" only if quoted from FEMA text read this session; otherwise leave as is.
m7 (R1) "5 of the 50 ... are in Alabama, which has 39 of the 1,793 listed counties" gives no expected count (50 x 39 / 1,793 = 1.1), so it implies clustering without a base. Fix: add "about 1 expected if spread evenly" or cut the sentence.
m8 Machine check suggestion: m2, m4, m5 and m7 survived two rounds; add a paper_gate line that every paper prints its left-out unit count and an expected-count clause for any "N of top 50 in state" sentence.
