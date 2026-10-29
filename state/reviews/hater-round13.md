# Hater round 13 (light check, page text only)

## home
- MINOR: Search no-match message ("No page matches yet. Every county's typical cost is in its state page's county table: find your state below.") is correct and the #nomatch element exists. It is set only on input events; fine.
- MINOR: Home quote checker line "of U.S. single-family policies (half pay $713 to $1,309)" is consistent with the $1,055 tile; no defect found.
- Title and meta description contain no unsupported claim ("typical cost ... what floods have paid out"). Items 1-8 not present on home except the tile caption "Median and per month: what existing single-family primary-home policies pay, premium plus fees", which is accurate.

Verdict: PASS

## louisiana
- MINOR: Quote checker zone list includes tiny legacy zones with no minimum (e.g. A12 has 53 priced policies, V15 167). The message does print the n ("53 priced policies"), so it is disclosed, but a "typical cost" from 53 policies is thin.
- MINOR: Zone medians for Zone C, A99 and B are all exactly $1,086, identical to the state median. Matches agg.json cost_by_zone, so the page is faithful, but three identical values look like a fallback and a skeptical reader will wonder. Unverified at source level.
- MINOR: In the quote checker, clearing the amount returns early ("Enter an amount above.") before zq() runs, so an earlier zone line ("In Zone AE here ... $X is N% above it") stays on screen with a stale amount.
- MINOR: The zone message does not say "single-family", while the line above it does. The values (cost_by_zone) are consistent with single-family medians (X 1,080 / AE 1,247 around state 1,086), so low risk.
- MINOR: Condo note "whole condo buildings 0.0%" reads as zero; extras.json condo_building_pct is 0.0 (rounded). Condo unit 1.1% equals extras 1.1; sentence about single-family exclusion is consistent with the page.
- Checked OK: median tile label, title and meta ($1,086, 56.6%); SRL wording (6,132 of 85,549 records, sourced to IA Multiple-Loss list); unpaid lead "not an actual flood" = first table row (20,318; rows sum to 107,750); private-flood note matches 12 CFR 339.3(c) and says price is not in FEMA data; "Find your parish in the table" links to #counties which exists; "Not in the NFIP (34 communities here)" lists exactly 34 names; zone message arithmetic (percent vs zone median, n shown) is correct and predicts nothing.

Verdict: PASS

## palm-beach-county-fl
- MINOR: Sibling bar label "Bordering and other counties" lists Broward, Miami-Dade, Lee, Pinellas, Collier, Hillsborough. Only Broward actually borders Palm Beach. Martin, Okeechobee, Glades and Hendry (the other bordering counties) have data folders but no built pages, so they are not linked. The "and other" wording is honest but a reader may assume the list is the neighbours.
- MINOR: Same stale zone line after clearing the amount as on Louisiana; same "0.0%" condo-building wording (units 6.1% equals extras 6.1).
- MINOR: Unpaid lead says "the top specific reason FEMA recorded was 'not an actual flood'" and the table's first row is "Not an actual flood 1,706" (Other 1,107 is second); consistent.
- Checked OK: tile label, title and meta ($670); private-flood note present; no SRL card and no state-only items on this page (no #counties link, none needed); zone Z values equal cost_by_zone in agg.json with n >= 116; message logic correct and non-predictive.

Verdict: PASS
