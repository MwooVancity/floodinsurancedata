
## broward-county-fl

Checked page text against agg.json/extras.json (and Florida state files).

Changed parts: title "$831 median a year, single-family homes" equals policies.p50 831 (OK). Zone select #qzs options AE/X/AH/AHB and the Z table equal cost_by_zone (853/53,125; 830/25,375; 792/19,591; 788/564); zq() logic is correct, clears when empty. Condo note "3.4% ... 0.0%" equals condo_unit_pct 3.4 and condo_building_pct 0.0. Unpaid lead "top specific reason ... not an actual flood" equals the table's first row (36.9%, 5,832). Private-flood note cites 12 CFR 339.3(c), says price not in FEMA data (OK). No "severe repeat-loss (SRL)" wording appears on this page (only "repeat-flood damage records 636 ... damage events, not distinct homes"), so nothing to mislead. Sibling line reads "Bordering and other counties" and lists Collier, Lee, Pinellas, Hillsborough, which are not all bordering; label is honest ("and other").

Flagged figures: 50.2% unpaid = 17,609/35,049 (OK); 49.8% paid, 17,440 paid (OK); average paid $26,180 = 456,568,107/17,440 (OK); Florida 30.1% unpaid / 69.9% paid equal 135,172 and 313,446 of 448,618 (OK); decade table equals by_decade (OK); unpaid table sums to 17,609 with "Smaller reasons, or none" 4,429 (OK).

- MINOR: Florida "$61,756" average paid does not equal state total_paid / paid_n ($61,580); it matches a stored state value, so likely a different basis (ICC or filter). Not a county error.
- MINOR: The page shows Broward unpaid share (50.2%) far above Florida's 30.1% but never says why it is unusual. The decade table (2000s 33.8% paid vs 2020s 78.3%) and the "paperwork, not a denied flood" note give the honest context; a reader will not be misled.
- MINOR: Top reason "not an actual flood" is 36.9% of unpaid, but "Other" plus unrecorded together exceed it; wording says "top specific reason", which is accurate.

No BLOCKER, no MAJOR.

Verdict: PASS
