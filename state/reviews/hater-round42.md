# Hater round 42

Scope: rule text seller_assign, lender_amount, lender_force, zone_review, odds_30, flood_def, not_covered, claim_appeal, substantial_damage, lapse_discount (cards "Am I required to buy it?", "How do I actually get covered", "What does it cost in my flood zone?", "How do current premiums compare"). Grep-only; text is identical on all four county/state pages, so findings repeat. Checked against 44 CFR 65.17, 44 CFR 61 App. A(1) (Dwelling Form), floodsmart.gov appeal page. 42 USC 4012a and the FEMA PDFs were judged from the registry's own quoted fragments, not re-fetched.

## home
Verdict: PASS
- Unaffected: none of the changed sentences appear in dist/index.html (grep count 0).

## louisiana
Verdict: FAIL
- **MAJOR** lender_amount: "The law sets the required amount at the loan balance or the NFIP's limit..., whichever is less". The statute quote is "at least equal to". The page turns a minimum into the exact amount. A reader can conclude the lender may not ask for more (many lenders require replacement-cost-level coverage) and push back wrongly at a closing. Say "the law requires at least the loan balance or the NFIP limit, whichever is less; a lender can ask for more."
- **MAJOR** claim_appeal: "Claim denied? You can appeal to FEMA within 60 days ... sue within one year". It never says this is for NFIP policies only. Sibling paragraph says "An NFIP policy"; this one does not. A private-policy or Group Flood holder reads a deadline that is not theirs (their contract limit may be shorter) and may lose rights. Prefix "NFIP claim denied?".
- **MINOR** lender_amount / lender_force: do not say these apply only to regulated lenders on loans for buildings in a high-risk zone; a cash buyer or someone with a private-lender loan outside the high-risk zone is not told it may not apply to them.
- **MINOR** zone_review: FEMA reviews only whether the building is in the high-risk zone on the map (65.17); elevation data is excluded. A reader with a high-ground lot may think this is the route; the elevation route is not named.
- **MINOR** flood_def: "generally counts a flood only when..." leaves out the cause (overflow, fast runoff, mudflow); fine as plain words, but a sewer or sump backup reader is not told it is a different question.
- **MINOR** not_covered: true for the Dwelling Form; a condo owner (Residential Condominium form) or General form holder may differ on contents and basement. Say "most NFIP policies".
- **MINOR** substantial_damage: "pays up to $30,000" does not say it is only on top of a covered flood claim, and the 50 percent is the federal minimum (a community can be stricter). Jargon: "Increased Cost of Compliance", "substantially damaged".
- **MINOR** lapse_discount: "30 days or more after" leaves day 30 itself unclear; "statutory discounts" is jargon; does not say a new policy brings the 30-day wait.
- **MINOR** seller_assign: "its discount" does not say which discount. Placed under "Am I required to buy it?" though it is not a requirement.
- **MINOR** label: card "How do I actually get covered" holds "What it won't pay" and "Claim denied?", which are not how to get covered.
- Fine: odds_30 (1 - 0.99^30 = 26.0%, correct); no "you should" or verdict wording anywhere; zone_review 45-day, joint request, fee match 65.17; flood_def, ALE, outside-building, basement, ACV match the Dwelling Form.

## palm-beach-county-fl
Verdict: FAIL
- Same sentences as louisiana: **MAJOR** lender_amount (minimum vs exact), **MAJOR** claim_appeal (no NFIP scope). MINORs as above.

## broward-county-fl
Verdict: FAIL
- Same sentences as louisiana: **MAJOR** lender_amount, **MAJOR** claim_appeal. MINORs as above.

## new-york-county-ny
Verdict: FAIL
- Same sentences as louisiana: **MAJOR** lender_amount, **MAJOR** claim_appeal. Condo-heavy county: the not_covered MINOR (Dwelling Form only) matters most here.

## Gaps
- GAP: private flood and Group Flood policies: no appeal or deadline rule printed; name the data (the policy contract) as not in FEMA records.
- GAP: condo (Residential Condominium form) and General Property form differences on contents, basement, and ACV are not covered.
