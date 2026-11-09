# Hater round 124 (light, re-review)

Previous items: claims MAJOR (label "every claim record") FIXED. flood-zones-ae MAJOR (unquoted "can require elevating") FIXED. flood-zones-ae MAJOR (no citation, cost basis dropped) FIXED.

## home
- Previous MINORs on "How much can it pay?" (a cap, not a typical payout; which buildings count) are unchanged. They are still MINOR.
- FIXED: the state-table note now reads 'every claim record, paid or not, except records FEMA coded "deleted in error" or "assigned in error", for losses from 1978 to 2026'. This matches `agg_raw.py`, which drops codes 98 and 99. I checked the 1978 to 2026 range against the 51 state data files.
Verdict: PASS

## claims
- years card, FIXED: the label now names the exclusion. Ranking by dollars paid is still correct (2005, 2017, 2012, 2024, 2022, 2016, 2008, 2011, 2004, 2021, descending). Counts and dollars match my recompute.
- years card, MINOR: "all 50 states and DC" still does not say that Puerto Rico and the other territories are out of the sum. The card still has no not-final note on 2024, because the note window is only the as-of year and the one before it.
- size card, label vs data: the label matches the data. I recomputed from `extras.json` in each state's data folder. The base is `buildingDamageAmount > 0` and `netBuildingPaymentAmount > 0`, with codes 98 and 99 skipped, over all loss years. The card says "claims with recorded building damage and a building payment, every loss year since 1978". 49 states qualify at 500 or more such claims; the range runs from Montana at $2,998 (1,480 claims) to Louisiana at $21,899 (361,000 claims). Both ends are correct. DC (258) and Wyoming (294) are left out.
- size card, MINOR: "49 of the 50 states and DC" reads as 49 of 50. It is 49 of 51, and the card does not name DC or Wyoming as left out. Fix: "49 of 51 (the 50 states and DC); DC and Wyoming have fewer than 500". A table or range that drops rows should say which.
- size card, MINOR: this is a median of nominal dollars across 1978 to 2026, so it mixes eras. The card says "not adjusted for inflation", so it is labelled. "Typical" in the title is accepted since the median is stated.
Verdict: PASS

## flood-zones-ae
- FIXED: the 50 percent sentence now cites 44 CFR §59.1 and states the restoration-cost basis and "before the damage". It matches the quoted regulation text.
- FIXED: the ICC sentence matches the quoted SFIP lines. It has the $30,000 maximum, building coverage (Coverage A) only, compliance with a state or local floodplain law, and the list of eligible work (elevating, floodproofing, moving, demolishing). The unsupported "can require elevating" clause is gone.
- MINOR (carried over): the lowest-floor paragraph says "new homes, and homes being substantially improved". The regulation says "residential structures". Zones, "must" strength, FEMA's final elevations and the basement exception all match 60.3(c)(2).
- MINOR: the paragraph gives no consequence of being substantially damaged (the building must then meet the lowest-floor rule above). The reader gets the definition and the ICC payout but not the link between them. Fix: add one cited clause, but only if the exact 60.3(c)(2) text supports it.
- No repetition on the page.
Verdict: PASS

## louisiana
- MINOR: the substantial-damage sentences sit inside the "NFIP claim denied?" note, directly after the appeal and one-year-suit sentences, with no lead-in. A reader whose claim was denied meets an unrelated definition. The text itself is correct and cited. Fix: split it into its own "After a flood:" note, as on the AE page.
Verdict: PASS

## palm-beach-county-fl
- MINOR: same placement as Louisiana, inside the "NFIP claim denied?" note. The text is identical, correct and cited. Same fix.
Verdict: PASS

## new-york-county-ny
- MINOR: same placement as Louisiana, inside the "NFIP claim denied?" note. The text is identical, correct and cited. Same fix. The text keeps its own (44 CFR §59.1) cite, so the source line below it remains consistent.
Verdict: PASS

## zip
- Base check: the ZIP median (`by_zip`) and the county `p50` both come from the same cohort in `ffcalc.py` (priced single-family primary-home policies, premium plus fees). The two figures are on one base. The 25 and 30 thresholds are each applied correctly.
- MINOR: "The Harris County median is $1,087 a year." This does not say "priced single-family policies", while the ZIP half does. The static note covers the base, but a reader could take the county figure as all policies. Fix: "The Harris County median for the same kind of policy is ...".
- MINOR: the ZIP figure and the county figure sit side by side ($1,810 against $1,087) with no "not a quote" beside them. A reader could take the gap as "my ZIP is overpriced" or as a quote. "Not a quote" appears only in the static note above. Fix: add "Not a quote or a verdict; price depends on each building" in the result line.
- A ZIP that spans several counties gets one county median per county, each labelled with its county name. That is correct.
Verdict: PASS

## levy-county-fl
- The substantial-damage sentences read correctly in the "NFIP claim denied?" note. They have the 44 CFR §59.1 cite and the $30,000 Increased Cost of Compliance (ICC) cap, as passed. The shared claims-record label does not appear on this page.
- Nearby: the "code-upgrade (ICC) pay" average ($49,162, against Florida's $61,801) is labelled "average" and "incl. code-upgrade". It does not contradict the $30,000 cap, which is per policy and not an average.
- MINOR (carried over): the definition is placed after the appeal sentences with no lead-in.
Verdict: PASS

## sonoma-county-ca
- The sentences read correctly in context, with the cite and cap as passed. The label does not appear on this page.
- Nearby: the median paid building claim ($9,945) and the average including ICC ($21,182) are both labelled by statistic. The "five costliest years" note is unrelated to the new text. No contradiction.
- MINOR (carried over): same placement.
Verdict: PASS

## wakulla-county-fl
- The sentences read correctly in context, with the cite and cap as passed. The label does not appear on this page.
- Nearby: the median ($10,409) and the average including ICC ($27,162) are each labelled. "Data effective 1984 to 2026" is consistent. No contradiction.
- MINOR (carried over): same placement.
Verdict: PASS
