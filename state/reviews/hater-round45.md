# Hater round 45

Scope: re-check of the round-44 surcharge MAJOR, plus carry-over of round-44 MINORs. Surcharge text read from tools/rules_registry.py and confirmed in dist/flood-insurance/palm-beach-county-fl/index.html (current build: "Homes that are not your primary residence, such as second homes and rentals you own, pay a higher federal surcharge: $250 a year, against $25 for a primary home."). Broward uses the same rule text; its dist page was not grepped this round. FEMA text checked against the brief quoted in the task. lapse_discount, zone_review, fl_disclosure, tx_twia: carried from round 44, not re-fetched.

## home
Verdict: PASS
- Unaffected: none of the five rules appear in dist/index.html (round 44 grep count 0; not re-grepped this round).

## louisiana
Verdict: PASS
- lapse_discount: "after the 30-day grace period leaves a lapse" and "FEMA says a lapse may affect a policy's statutory discounts" match the two FEMA excerpts and are hedged as FEMA's words. No advice or verdict.
- zone_review: joint request, 45 days of the lender's notice, fee, 44 CFR 65.17 all match the quoted fragment. No verdict.
- **MINOR** lapse_discount: "(what keeps a bill below full risk)" is a loose gloss; statutory discounts are the rate breaks that some older or grandfathered policies carry. Say "the reduced rates some policies carry".
- **MINOR** lapse_discount: says a lapse exists after the grace period but not whether a loss during the grace days is paid; a reader may assume cover continues. Print the FEMA wording or a gap line.
- **MINOR** zone_review: "a fee applies" is not in the quoted fragment; add a source quote for the fee.
- **MINOR** zone_review: "high-risk-zone finding" is plain but a reader may not know this only reviews the lender's finding that the building is in a mapped high-risk area, not the map itself.
- Not placed on this page in dist: surcharge, fl_disclosure, tx_twia (no finding).

## palm-beach-county-fl
Verdict: PASS
- **Closed** surcharge (round-44 MAJOR): the live text now names every non-primary home ("second homes and rentals you own") instead of second homes only. Matches FEMA's "$250 per year for owners of non-primary residences". Still open as a MINOR, below.
- **MINOR** surcharge (new): the text says "Homes", but FEMA's $250 also covers non-residential buildings (business-use property). A homeowner reader is not misled; print "non-residential buildings" if the page ever covers business property. Renters paying $25 are not named either; not false, not on the reader's question.
- fl_disclosure: matches 689.302: seller to buyer, residential real property, at or before the sales contract, form asks about known flood damage during ownership, flood insurance claim, flood-damage assistance. No false statement.
- **MINOR** fl_disclosure: the statute page gives no effective date (history lists ch. 2024-215 and ch. 2025-166 only); the registry text prints none, which is correct, but the project rule asks for an effective date. Record it as a gap or source it.
- **MINOR** fl_disclosure: "received flood aid" is shorter than the statute's "flood-damage assistance, including FEMA"; fine, but private or state aid is also meant.
- **MINOR** fl_disclosure: statute page is marked unverified by the Senate site; re-fetch by recheck.py.
- lapse_discount, zone_review: as louisiana, both MINORs apply.
- **MINOR** tx_twia (Texas only, not on this page, noted for when it ships): matches TWIA's three conditions and the September 1, 2009 date. "when any part of the property is in a V zone": the fetched page says "the property is in a V, VE, or V1-V30 flood zone"; "any part" is not confirmed, check the full page. The sentence says TWIA "requires"; TWIA also says "some properties must" and strongly recommends all buy.

## broward-county-fl
Verdict: PASS
- Same sentences as palm-beach-county-fl; the surcharge fix and the new surcharge MINOR apply here. Other MINORs as above.

## new-york-county-ny
Verdict: PASS
- Carries lapse_discount and zone_review only; both are accurate. MINORs as louisiana.
- Not placed in dist: surcharge. When surcharge ships here, the new "rentals you own" wording covers the condo and rental-heavy case; the non-residential MINOR still applies.

## Gaps
- GAP: whether a loss in the 30-day grace period is covered (FEMA renewal rules) is not printed; name the data (NFIP Flood Insurance Manual renewal rules).
- GAP: fee amount for a 44 CFR 65.17 review is not printed.
- GAP: the surcharge for a primary home ($25) applies to policies, not to private flood; page does not say private policies differ.
- GAP (out of scope, seen in dist palm-beach line 167): the cap sentence says "some policies, such as second homes and businesses, can rise up to 25%". Not checked this round; the next wording check should test it against the cap source.
- Fixlog-round44 line has no proof column (CLAUDE.md asks defect, layer, fix, proof). Round 45 should record the proof: the dist grep above.
