# Hater round 36 (light)

## home
Verdict: PASS
No "claim dollars paid", "Congress" or "renters and businesses" text present (grep: 0 hits; only CSS "collapse" matched "lapse"); nothing contradicts the new lines.

## louisiana
Verdict: FAIL
**MAJOR** "The median here is for single-family primary homes, not a price for contents-only cover" - the cohort (tools/ffcalc.py aggregate_policies) filters only occupancyType 1/11 + primary residence, with no building-coverage filter, so contents-only policies on a single-family occupancy (e.g. a tenant in a house) can sit inside the median; the exclusion is asserted but not enforced (also "Half of homeowners" label sits on the same cohort). Either add the filter or drop the clause.
**MINOR** "Of the NFIP claim dollars paid here (1978-2026), X% went to claims rated outside high-risk zones A and V" - base (paid dollars on claims with a zone, building+contents+ICC), period, and zone-on-claim caveat are all printed; matches agg_raw.claims_extra. Residual: "paid here" rests on claims countyCode, which the site's own data-trap rule says may not match the property county; "outside A and V" could be read as "outside floodplains" by a frightened reader, and does not say it covers all occupancy types.
**MINOR** "Congress has to keep renewing the NFIP's authority..." faithful to 42 USC 4026 / W-23012, true with or without a lapse; "may be limited" is attributed to FEMA. No contradiction nearby.
**GAP** the card never says whether authority is in force today or when it expires, so a reader cannot tell if the lapse sentence applies now.
**MINOR** "The NFIP also offers policies for renters and businesses." is accurate and not repeated elsewhere on the page.

## palm-beach-county-fl
Verdict: FAIL
**MAJOR** "The median here is for single-family primary homes, not a price for contents-only cover" - the cohort (tools/ffcalc.py aggregate_policies) filters only occupancyType 1/11 + primary residence, with no building-coverage filter, so contents-only policies on a single-family occupancy (e.g. a tenant in a house) can sit inside the median; the exclusion is asserted but not enforced (also "Half of homeowners" label sits on the same cohort). Either add the filter or drop the clause.
**MINOR** "Of the NFIP claim dollars paid here (1978-2026), X% went to claims rated outside high-risk zones A and V" - base (paid dollars on claims with a zone, building+contents+ICC), period, and zone-on-claim caveat are all printed; matches agg_raw.claims_extra. Residual: "paid here" rests on claims countyCode, which the site's own data-trap rule says may not match the property county; "outside A and V" could be read as "outside floodplains" by a frightened reader, and does not say it covers all occupancy types.
**MINOR** "Congress has to keep renewing the NFIP's authority..." faithful to 42 USC 4026 / W-23012, true with or without a lapse; "may be limited" is attributed to FEMA. No contradiction nearby.
**GAP** the card never says whether authority is in force today or when it expires, so a reader cannot tell if the lapse sentence applies now.
**MINOR** "The NFIP also offers policies for renters and businesses." is accurate and not repeated elsewhere on the page.

## broward-county-fl
Verdict: FAIL
**MAJOR** "The median here is for single-family primary homes, not a price for contents-only cover" - the cohort (tools/ffcalc.py aggregate_policies) filters only occupancyType 1/11 + primary residence, with no building-coverage filter, so contents-only policies on a single-family occupancy (e.g. a tenant in a house) can sit inside the median; the exclusion is asserted but not enforced (also "Half of homeowners" label sits on the same cohort). Either add the filter or drop the clause.
**MINOR** "Of the NFIP claim dollars paid here (1978-2026), X% went to claims rated outside high-risk zones A and V" - base (paid dollars on claims with a zone, building+contents+ICC), period, and zone-on-claim caveat are all printed; matches agg_raw.claims_extra. Residual: "paid here" rests on claims countyCode, which the site's own data-trap rule says may not match the property county; "outside A and V" could be read as "outside floodplains" by a frightened reader, and does not say it covers all occupancy types.
**MINOR** "Congress has to keep renewing the NFIP's authority..." faithful to 42 USC 4026 / W-23012, true with or without a lapse; "may be limited" is attributed to FEMA. No contradiction nearby.
**GAP** the card never says whether authority is in force today or when it expires, so a reader cannot tell if the lapse sentence applies now.
**MINOR** "The NFIP also offers policies for renters and businesses." is accurate and not repeated elsewhere on the page.

## new-york-county-ny
Verdict: FAIL
**MAJOR** "The median here is for single-family primary homes, not a price for contents-only cover" - the cohort (tools/ffcalc.py aggregate_policies) filters only occupancyType 1/11 + primary residence, with no building-coverage filter, so contents-only policies on a single-family occupancy (e.g. a tenant in a house) can sit inside the median; the exclusion is asserted but not enforced (also "Half of homeowners" label sits on the same cohort). Either add the filter or drop the clause.
**MINOR** "Of the NFIP claim dollars paid here (1978-2026), X% went to claims rated outside high-risk zones A and V" - base (paid dollars on claims with a zone, building+contents+ICC), period, and zone-on-claim caveat are all printed; matches agg_raw.claims_extra. Residual: "paid here" rests on claims countyCode, which the site's own data-trap rule says may not match the property county; "outside A and V" could be read as "outside floodplains" by a frightened reader, and does not say it covers all occupancy types.
**MINOR** "Congress has to keep renewing the NFIP's authority..." faithful to 42 USC 4026 / W-23012, true with or without a lapse; "may be limited" is attributed to FEMA. No contradiction nearby.
**GAP** the card never says whether authority is in force today or when it expires, so a reader cannot tell if the lapse sentence applies now.
**MINOR** "The NFIP also offers policies for renters and businesses." is accurate and not repeated elsewhere on the page.
