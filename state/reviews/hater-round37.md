# hater-round37 (light, one sentence: "The NFIP also offers policies for renters and businesses. The median here is for single-family primary-home policies, not businesses or second homes.")

Filter checked: `ffcalc.py` aggregate_policies, `coh = occupancyType in (1, 11) AND primaryResidenceIndicator true`. Businesses (non-residential occupancy) and non-primary (second) homes are excluded, so both stated exclusions are enforced. Sentence present once in the cost card on louisiana, palm-beach-county-fl, broward-county-fl, new-york-county-ny; absent from dist/index.html.

## home
Verdict: PASS
Sentence not present (0 matches in dist/index.html).

## louisiana
Verdict: PASS
**MINOR** The filter does not test condo coverage code or contents-only policies, so a renter's contents-only policy on a primary-residence single-family record would be inside the median. The sentence only says the NFIP offers renter policies and that the median excludes businesses and second homes; it does not claim renters are excluded, so it is not false. Optional tightening: "the NFIP also offers..." is fine as is.
**MINOR** Nearby "Condo owners" note says the single-family figures "leave both out", but `isone` accepts occupancy code 11 and never checks `condominiumCoverageTypeCode`. Pre-existing text, not the changed sentence; worth an oracle check that code 11 excludes condo units. Not judged here.

## palm-beach-county-fl
Verdict: PASS
Same MINOR notes as louisiana (renter contents-only and condo-note vs code 11 are unverified by the filter). No contradiction with "across all Palm Beach County policies" (coverage line is labelled a different base).

## broward-county-fl
Verdict: PASS
Same MINOR notes as louisiana. Coverage line labelled "across all Broward County policies", a distinct labelled base.

## new-york-county-ny
Verdict: PASS
Same MINOR notes as louisiana. Cohort is 172 policies here; the sentence's wording still matches the population used.
