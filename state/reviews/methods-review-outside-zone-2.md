# Methods review: Outside the Zone, round 2 (hostile statistician, 2026-11-13)

Inputs read: dist/flood-insurance/outside-the-zone/index.html (whole page), dist/data/outside-the-zone.csv (364 rows),
tools/papers.py (spec, rows, wilson), tools/extras_raw.py claims() (zone accumulator, zone_split, moved), data/all-counties/*.json
(3,027 files), data/us/claims_zone.json, docs/PAPER-GATE-PROMPT.md, state/reviews/methods-review-162.md.
Raw per-claim files (.cache/raw) are not on this laptop: per-record checks below use the county aggregates.
Script: scratchpad otz.py (recompute, parametric binomial bootstrap B=1000, design-effect-5 bootstrap B=300,
county-cluster bootstrap B=2000, named-event dominance, rated-vs-current zone, policy-exposure comparison).

Severity: BLOCKER = wrong or misleading on the page; MAJOR = a referee would reject; MINOR.

## What passes

- Recompute, 15 rows (top 3, bottom 2, 10 random seed 7): share, 90% Wilson range, numerator, denominator, fifth all match the
  CSV, 0 mismatches. All 364 rows: k, n, fifth 0 mismatches. CSV county set = recomputed pool set.
- Pool 364, left out 2,042 with 1-99, 621 with none: 364 + 2,042 + 621 = 3,027 files. Matches the page.
- Pooled 109,947 / 424,932 = 25.87%; median county 25.55%. Matches the page (25.9%, 25.6%).
- Base consistency (M1.1): numerator out_paid_n is a subset of known_paid_n, both summed from the same zone accumulator
  (loss years 2016-2025, net building + contents + ICC > 0, ratedFloodZone not blank, 98/99 dropped). Minimum applies to that same n.
- Wilson implementation: hand-checked 10/100 = 6.1-16.0; Holt MO 0 of 246 gives 0.0-1.1, correct for k = 0.
- Zone value set (all 51 states, window, paid): outside = X 107,884, C 7,537, B 7,154, D 129. No malformed code exists, so
  "first letter not A or V" = exactly {X, B, C, D} as the page says. D is 0.1% of outside claims: the D-as-outside choice
  cannot move a county. A99/AR/AHB/AOB go inside (1,883 claims), consistent with "zones A and V".
- Top-fifth stability: all of the top 20 stay in the top fifth in 100% of 1,000 binomial redraws, and in 99-100% under a design
  effect of 5 (effective n = n/5, a crude stand-in for event clustering). Montgomery MD rank 90% interval [1,1].
- Labels: every share is "claims with a payment and a rated zone"; no "homes" base anywhere except the limitation saying it is
  not a share of homes. No causal word (because / due to / driven by / caused) and no "significant" on the page.

## Prior review 162: point by point

| 162 point | Status | Evidence |
|---|---|---|
| B1 tie stated as unique lowest | Resolved | Holt MO 0 of 246 is the only 0.0% row; abstract names it alone. |
| B2 n not the base; minimum on wrong count; dollars vs counts | Resolved | Measure is now a count share; n = known_paid_n; minimum on it; duplicate column gone. |
| B3 title asserts present geography; era pooling; zone list | Mostly resolved | Title says "rated"; window 2016-2025; zones listed. Rated-vs-current number exists in data but is not printed (MINOR m3). |
| M1 false-precision ranks | Resolved for ranks | Fifths + 90% Wilson. But see MAJOR 2 (pooled interval) and m1 ("50 highest" is a rank). |
| M5 selection bias | NOT resolved | Counts of left-out counties printed; their median and pooled share are not (MAJOR 3). |
| M6 single events drive ranks; nominal dollars | Half resolved | Dollars and 48-year pooling gone; no one-event flag per row (MAJOR 4). |
| M7 claim county vs property county | NOT resolved | This spec's limits omit the countyCode caveat that the Underinsured spec carries (m4). |
| M8 methods not reproducible | Partly | Fields listed; 98/99 codes, payment sum, county field, flow counts and code version still missing (MAJOR 5). |
| M9 prior work | NOT resolved | Two un-cited names, no reconciliation of the national figure (MAJOR 6). |
| m1 rounding before ranking | Resolved | Sort is on exact k/n. One displayed tie straddles a fifth boundary (m2). |
| m2 no base rate for state clustering | NOT resolved | "19 of the 50 ... in Texas": TX is 32 of 364, expected 4.4 of 50 (m1). |
| m4 "no test" vs ordinal claims | Resolved | Fifths only, plus m1. |

## BLOCKER

None. Every printed number reproduces from the raw county files.

## MAJOR

**MAJOR 1 - Misleading-but-true: the share mostly reflects where the policies are, and the page gives no exposure base.**
A reader sees "Fort Bend County, TX: 68.6% of paid claims outside A and V" and concludes floods hit outside the map there. But
92.5% of Fort Bend's in-force policies (policyCount by rated zone, `policies.zone_units_all`) are outside A and V, so outside
policies produced claims at well under their share. Across the 358 ranked counties with 100+ zoned policies, county claim share
vs policy share outside A/V: Pearson r = 0.70; median ratio claim share / policy share = 0.72. Top-fifth median policy share
outside = 53.9% vs 34.8% for all ranked counties. Top row Montgomery MD: 97.0% of claims vs 92.2% of policies; Chambers TX
89.1% vs 89.7%; Jefferson TX 75.8% vs 83.7%. The counties where claims outrun policies are elsewhere: Honolulu 29.2% vs 8.3%
(3.5x, third fifth), Avoyelles LA 67.2% vs 31.1%, Cook IL 49.5% vs 26.2%. The ranking therefore mostly ranks "share of NFIP
business written outside A/V". The limitation "not the chance that any home floods" does not cure it.
Fix: print beside every share the county's share of policies (policyCount) rated outside A/V, with its as-of date, and say in
the Abstract and Results that the claim share tracks it (r, median ratio); state the time mismatch (policies in force at as-of vs
claims 2016-2025). Better: add the ratio as a second column, labelled as a ratio of two shares, no interval unless bootstrapped.

**MAJOR 2 - The pooled 90% range claims ~30x too much precision.**
"25.9% (90% range 25.8-26.0%)" treats 424,932 claims as independent draws. They are clustered by county and event (Harris alone
is 13.0% of the base; Harvey is 69% of Jefferson TX's window claims). County-cluster bootstrap of the pooled share (B=2,000):
90% range 19.1-32.3%. County Wilson ranges have the same blind spot (claims in one flood share one map and one storm), though
the design-effect-5 run shows the top fifth survives it.
Fix: drop the interval on the pooled figure, or replace it with the county-cluster bootstrap range and say what it resamples;
add a limitation that county ranges assume independent claims and understate uncertainty when one flood dominates.

**MAJOR 3 - Selection bias not shown (gate M1.6, open since 162 M5).**
Left-out counties (1-99 claims): pooled 34.7% (12,593 of 36,265), median 33.3%, 30.5% above 50% - vs ranked 25.9% pooled,
median 25.6%, 14.0% above 50%. All-US pooled share = 26.6%. The page prints only the counts of left-out counties.
Fix: one Results line: "The 2,042 counties left out (36,265 claims, 7.9% of the national base) have a median of 33.3% and a
pooled share of 34.7%; all counties together: 26.6%."

**MAJOR 4 - One flood dominates many rows, unflagged (gate M1.8, open since 162 M6).**
Proxy (named event in the county's top 8 by dollars, all its loss years inside 2016-2025, paid claims of all zones / paid claims
in the window): 168 of 364 ranked counties have one named event above 50%; 31 of the 73 in the top fifth. Examples: Jefferson
TX 69% Harvey, Chambers TX 63% Harvey, Bastrop TX 55%, San Patricio TX 50% Harvey, Pamlico NC (37137) 98% Florence, Craven NC 97% Florence. The Texas cluster in
the Results is largely Harvey (2017). zone_split has no loss-year split, so the gate's own test cannot be run on these files.
Fix: add per-loss-year paid and out-paid counts to zone_split in extras_raw.claims(); flag each row where one loss year is over
half of the numerator or the denominator; print the count of flagged counties and mark them in the table and CSV.

**MAJOR 5 - Methods are still not reproducible from the text alone (open since 162 M8).**
Missing: (a) "paid" = netBuildingPaymentAmount + netContentsPaymentAmount + netIccPaymentAmount summed, > $0 (a reader using
building only gets different counts); (b) "deleted or assigned in error" = nonPaymentReasonBuilding codes 98 and 99 (never
named); (c) county = countyCode, and claims whose countyCode is outside the state file are dropped; (d) ratedFloodZone trimmed
and upper-cased, first letter A or V = inside; (e) loss year = first 4 characters of yearOfLoss; (f) a flow table: claims pulled
-> in window -> not 98/99 -> paid -> zoned (blank 2,369 paid claims nationally) -> in ranked counties (424,932); (g) pull date vs
as-of date; (h) code file and commit.
Fix: a numbered filter list with field = value and the count after each step, plus the commit hash.

**MAJOR 6 - Prior work is named, not cited or reconciled (gate R0.1, open since 162 M9).**
"Penn State (PA counties, 2022) and UNC (2025)" has no title, author, link or figure. FEMA itself publishes a national share of
claims from outside high-risk areas that is widely quoted; the paper's 25.9% (ranked counties, paid, rated zone, 2016-2025)
must be set beside it with the base difference named, or a reader assumes one of them is wrong. 162 also listed RFF/Wharton
(policies outside the SFHA by county) and the Penn State dollar ratio; neither is reconciled.
Fix: full citations with links read this session; one reconciliation line per figure (base, years, paid vs filed, rated vs mapped).

## MINOR

**m1 - "19 of the 50 counties with the highest shares are in Texas" is a rank claim with no base rate.** The page bans numbered
ranks yet uses a top-50 cut. Texas is 32 of 364 ranked counties (4.4 expected in 50). Fix: "19 of the 73 counties in the highest
fifth ..." with the expected count, and note the Harvey dominance (MAJOR 4).

**m2 - A displayed tie straddles a fifth boundary.** Perry County 10.3% (11 of 107) is fourth fifth; Fond du Lac 10.3% (12 of 117)
is lowest fifth. Sort is on exact k/n so it is correct, but the reader sees equal shares in different fifths. Fix: name ties at
boundaries (gate M1.3 "ties named") or show two decimals there.

**m3 - Rated vs current map: the data has the number, the page only says "can differ".** Of claims rated outside A/V in ranked
counties (2016-2025, all claims), 9.1% (11,589 of 126,968 with a current zone) are in A/V on floodZoneCurrent; 7.0% have no
current zone. Highest: 12021 FL 68%, 25009 MA 61% (both rated outside, now inside). Fix: print the pooled 9.1% in Limitations.
(Note: moved counts all claims, not paid; label it so.)

**m4 - Claim county caveat missing.** The Underinsured spec carries "Counties are those FEMA codes on the claim, which can differ
from the property's county"; this spec does not, yet uses the same countyCode. Fix: add the line.

**m5 - Blank-zone exclusion not quantified per county.** Pooled blank share is 0.45% of window claims, but Newton TX (48351) has
105 blank of 399 (26%), 45067 SC 21%, 37155 NC 16%. Fix: CSV column blank_n; flag counties where blank exceeds 10%.

**m6 - Recent-year completeness.** Losses in 2025 with claims still open at the as-of date (2026-08-31) are absent from the paid
base; if open claims differ by zone, the latest year is biased. Fix: one limitation line, or end the window at 2024.

**m7 - Versions.** The page says each refresh "replaces the figures"; gate M2.5 wants a kept permalink per as-of. No
/outside-the-zone/2026-08-31/ exists in dist. Fix: write the versioned copy (gate item, not a statistical one).

**m8 - Dollars as co-measure.** Pooled dollar share outside A/V is 24.1% vs 25.9% by count; only 10 of 364 counties move more
than one fifth by dollars. The count choice is not driving results; say so in one line (answers 162 B2's dollar point).

## Verdict

**MAJOR REVISION.** The arithmetic is now clean (0 mismatches on 364 rows, one base, sound Wilson, top fifth stable under
bootstrap), and 162's three blockers are fixed. It does not ship: the headline measure mostly mirrors where NFIP policies are
written and the page never shows that exposure (MAJOR 1), the pooled interval overstates precision about 30-fold (MAJOR 2), and
four items 162 raised remain open (selection, one-event flag, reproducible methods, prior work).
