# Round 83 (LIGHT, text only)

Method: built HTML text only, no screenshots, no web search. Own list first, then hater-round82.md. Changed items only: (1) home H2 "How much is flood insurance?" sentence; (2) zone X page H2 "Zone X, shaded X, zone B and zone C"; (3) state/county titles "$N/yr median, single-family". Checklist lines C, D, E, N judged; A, B, F-M unchanged from round 82 (PASS).

Check of home sentence against data/us/cost_hist.json (policy-weighted, 2,320,412 policies, all states pooled; quantile = first cost where running count reaches q x total): p25 = $715, median = $1,066, p75 = $1,330, p90 = $2,170. All four equal the page. Base on the page ("existing NFIP policies on single-family primary homes ... premium plus fees") matches the hero caption and the "Typical cost, existing single-family homes (median)" table row.

Repeat check: $1,066 appears on the home page in the hero tile, the new sentence, and the "Measure / Amount" table row (the Tulsa County $1,066 is a coincidence). The new sentence is not word-for-word any other sentence; it adds the $715-$1,330 and $2,170 figures that appear nowhere else.

## home

- **MINOR** The median $1,066 now shows twice within screen 1-2 (hero tile "$1,066 U.S. median a year" and the new sentence), plus the table row further down. Same figure and same base each time, so not contradictory.
- **MINOR** "one in ten pays $2,170 or more": the 90th percentile is the first cost at which 90% of policies are at or below it, so "10% pay $2,170 or more" is true only to within ties at $2,170 (a histogram step can hold many policies). Wording is close enough; not misleading.

Checklist C/D/E/N: PASS. Quartiles and 90th equal the histogram; base named; no repeat of an existing sentence.

Verdict: PASS

## louisiana

Title "Louisiana flood zones and flood insurance: $1,114/yr median, single-family" equals lede "$1,114 a year (premium plus fees, ...)". Round 82 MINOR (no unit) is FIXED.

Checklist C/D/E/N: PASS.

Verdict: PASS

## palm-beach-county-fl

Title "$673/yr median, single-family" equals lede and meta description ($673 a year).

- **MINOR** Title says "FL", H1 says "Florida" (unchanged, deliberate).

Checklist C/D/E/N: PASS.

Verdict: PASS

## new-york-county-ny

Title "$1,021/yr median, single-family" equals lede and meta description.

- **GAP** Manhattan not named in H1 (unchanged).

Checklist C/D/E/N: PASS.

Verdict: PASS

## utah

Title "Utah flood zones and flood insurance: $614/yr median, single-family" equals lede ($614 a year).

Checklist C/D/E/N: PASS.

Verdict: PASS

## st-johns-county-fl

Title "$1,087/yr median, single-family" equals lede and meta description.

Checklist C/D/E/N: PASS.

Verdict: PASS

## Zone X page (extra, changed this round: dist/flood-zones/x/index.html)

New H2 "Zone X, shaded X, zone B and zone C" sits directly under the H1 and above the meaning paragraph, which defines both pairs in plain words (B = shaded X moderate hazard, C = unshaded X minimal hazard) with the 44 CFR 64.3 citation. Heading order H1 then H2 is correct; it is a topic label, not a question, but it names the codes a reader meets on older maps. No defect.

## Classes

- state/county: title now carries unit ("/yr"); class fixed. "/yr" abbreviation in a title is fine; the lede says "a year".
- county: title "FL/NY" vs H1 full state name (MINOR, deliberate).

## Previous items

Round 82: no BLOCKER or MAJOR open. Only MINOR "title figure lacks a year": FIXED (all five titles now "/yr median").
