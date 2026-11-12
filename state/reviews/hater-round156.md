# Hater round 156 (light, text + one 390x844 Playwright pass)
Checked against data/c/<slug>/agg.json and data/states/louisiana/agg.json. Screen 1 at 390x844: all six answers end by y=678 (Louisiana, NY, Raleigh) to y=720 (Levy), no sideways scroll; the button sits beside the median tile (top 682-745), reads clearly, 44px+ target.

## home
- MINOR Home has no six-answer block and no map button (dist/index.html unchanged); nothing to judge from the change.
Verdict: PASS

## louisiana
- **MAJOR** "How risky? FEMA gives no flood rating for this place; check your address on FEMA's map": false for the page it sits on. FEMA's National Risk Index rates every parish (data/states/louisiana/agg.json `state_risk` lists all of them), and the same page prints "FEMA flood risk rating ... Each parish page shows its own rating" with counts (Very High 2, Relatively High 8, ...). FEMA rates counties, not states, so "no rating for this place" contradicts the table below it and reads as "FEMA has not assessed Louisiana". Same wording is on all 54 state, DC and CT-county pages (grep: 54 files). Check that should catch it: label-vs-data (C10-C14 class) comparing the gap line to `state_risk` presence. Suggested truth: "FEMA rates parishes, not whole states; see ratings below" with a link to that table.
- MINOR "Can I pay less? FEMA's ways to lower a bill are below" is true (#save exists) but names nothing; the reader still has to scroll to learn what.
- MINOR Button label "Your address on FEMA's map" is a noun phrase, not an action; fine beside the arrow, but "Check your address on FEMA's map" would match the How risky line.
- Cost line TRUE: X $1,082 (127,267 priced) and AE $1,259 (108,782) are the two biggest zones by units (174,352 and 157,736); "more zones below" is true (A, C, A99, ...). Is it rising 52.8% matches share_below.
Verdict: FAIL

## palm-beach-county-fl
- MINOR Zone line names X and AE (top two by units, 74,991 and 44,970) and says "more zones below": TRUE (AO, AH, C, B, VE are priced in the table).
- MINOR Button placement good; tile text wraps to four lines at 390px but stays readable.
Verdict: PASS

## new-york-county-ny
- MINOR "Zone AE, 41.8% of policy units, has too few to price" is TRUE (6,232 of 14,925 units; cost_by_zone holds only X, n=159). Base is all policy units while the price is single-family only; the wording says "of policy units", so it is labelled.
- MINOR Only 171 priced policies sit under the $953/$1,021 figures; pre-existing, page prints the base elsewhere.
Verdict: PASS

## dixie-county-fl
- MINOR "Zone A, 10.4% of policy units, has too few to price" TRUE (59 of 567). VE (24 units) and X (22) are not named; both smaller than A, so the big zones are named.
Verdict: PASS

## levy-county-fl
- MINOR Line shows AE $2,357 and A $958, names VE (21.5%, 200 of 932 units) as unpriced, and says "more zones below": all TRUE (X priced n=51 sits in the table). Longest screen 1 of the set still ends at y=720, inside 844.
Verdict: PASS

## sonoma-county-ca
- MINOR Line shows AE $1,588 and X $1,201 with no "more zones" tail: TRUE, the other zones (A 52, AO 32 units) are not priced.
Verdict: PASS

## wakulla-county-fl
- MINOR Four zones listed (AE, VE, A, X), all match cost_by_zone (n 336, 209, 129, 136); VE $4,496 stands next to X $1,092, the spread is real data.
Verdict: PASS

## raleigh-county-wv
- MINOR "Too few priced policies per zone for a zone median (Zone AE, Zone A, Zone X); county median $1,244 a year" is TRUE: cost_by_zone is empty, zone_units AE 39, A 38, X 31, 66 priced policies in total. The three zones named are all the zones the county has. "County median" omits "single-family" here, but the tile directly below carries the full label.
- MINOR The same gap line also appears on calaveras-county-ca and tooele-county-ut and is true for both (cost_by_zone empty).
- Not testable: the "No single-family primary-home premium here is under...", "no full-risk comparison" and "Too few NFIP claims" lines appear on no built page (grep: 0 files), so their truth could not be checked.
Verdict: PASS

## Classes
- State template: the "How risky?" gap line is false on every state, DC and CT-county page whose NRI rating exists only per county (MAJOR above).
- County template: gap lines for zone cost are true on the pages sampled; named zones are the largest by units.
- Untested gap lines (share 0, no full-risk comparison, few claims) have no live example; they need a test_factory case.
