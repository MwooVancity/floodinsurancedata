# Hater round 44

Scope: wording check of five registry rules: lapse_discount, surcharge, tx_twia, fl_disclosure, zone_review. Text read from tools/rules_registry.py. tx_twia and fl_disclosure compared with twia.org/flood-requirement and flsenate.gov 689.302 fetched this session (page text via summarizer, not raw); the other three judged from the registry's quoted fragments, not re-fetched. Placement from grep of data-rule in dist (current build, may predate the uncommitted registry edits): lapse_discount and zone_review on louisiana, palm-beach, broward, new-york; surcharge and fl_disclosure on palm-beach and broward only; tx_twia on none of the five; home carries none.

## home
Verdict: PASS
- Unaffected: none of the five rules appear in dist/index.html (grep count 0).

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
Verdict: FAIL
- **MAJOR** surcharge: "Second homes also pay a higher federal surcharge: $250 a year, against $25 for a primary home." The cited FEMA text covers every home that is not a primary residence (rentals, investment and business-use buildings too, per the "$250 per year" for non-primary wording). A buyer or landlord of a rental reads "second homes", decides it does not apply, and under-budgets $250 a year. Misleading by omission. Fix: "Homes that are not your main residence (second homes, rentals) also pay...". Source fragment cited is cut off ("...primary residences and $250 per year"); quote the full sentence.
- fl_disclosure: matches 689.302: seller to buyer, residential real property, at or before the sales contract, form asks about known flood damage during ownership, flood insurance claim, flood-damage assistance. No false statement.
- **MINOR** fl_disclosure: the statute page gives no effective date (history lists ch. 2024-215 and ch. 2025-166 only); the registry text prints none, which is correct, but the project rule asks for an effective date. Record it as a gap or source it.
- **MINOR** fl_disclosure: "received flood aid" is shorter than the statute's "flood-damage assistance, including FEMA"; fine, but private or state aid is also meant.
- **MINOR** fl_disclosure: statute page is marked unverified by the Senate site; re-fetch by recheck.py.
- lapse_discount, zone_review: as louisiana, both MINORs apply.
- **MINOR** tx_twia (Texas only, not on this page, noted for when it ships): matches TWIA's three conditions and the September 1, 2009 date. "when any part of the property is in a V zone": the fetched page says "the property is in a V, VE, or V1-V30 flood zone"; "any part" is not confirmed by my fetch, check the full page. The sentence says TWIA "requires"; TWIA also says "some properties must" and strongly recommends all buy; the rule is a condition of the windstorm policy, which the text says.

## broward-county-fl
Verdict: FAIL
- Same sentences as palm-beach-county-fl; the surcharge MAJOR applies here. MINORs as above.

## new-york-county-ny
Verdict: PASS
- Carries lapse_discount and zone_review only; both are accurate. MINORs as louisiana.
- Not placed in dist: surcharge. Condo and rental-heavy county: when surcharge ships here, the "Second homes" MAJOR bites hardest.

## Gaps
- GAP: whether a loss in the 30-day grace period is covered (FEMA renewal rules) is not printed; name the data (NFIP Flood Insurance Manual renewal rules).
- GAP: fee amount for a 44 CFR 65.17 review is not printed.
- GAP: the surcharge for a primary home ($25) applies to policies, not to private flood; page does not say private policies differ.
