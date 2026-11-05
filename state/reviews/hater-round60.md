# Round 60: light review (changed screen-1 wording and rules)

Checked in raw text this session: floodsmart buy-a-policy (30 days; four exceptions; "no wait ... making, increasing, extending or renewing a mortgage"), floodsmart flood-insurance-basics, agents.floodsmart.gov paying-less article, Federal Reserve Q&A, data/c/palm-beach-county-fl/agg.json. The FIM (Oct 2025) PDF was not opened; its wording was judged from the quotes given in the brief (effective at closing if application and full amount reach the insurer within 10 days, 30 if lender/title/attorney pays).
Data: $673 = policies.p50 in agg.json (cohort_n 50,039 single-family primary-residence policies with a cost; metric unit "premium plus fees"); asof 2026-08-31 is the policy-snapshot filter date from pull_raw, so "policies in force as of" is the right label. Not recomputed from raw (no raw on this laptop; recheck.py is the independent check).

## home
- MAJOR: homeowners_excl second clause, "flood insurance is bought separately, through the federal NFIP or a private insurer", has no quote behind it. The cited floodsmart flood-insurance-basics page says only "most homeowners insurance does not cover flood damage"; the word "private" does not appear there, and "separately" is inference. True in substance, but the project's own rule 3 cuts inferences. Fix: print only the first clause, or add a source quote that says flood cover is a separate policy and private insurers sell it.
- MINOR: howto_answer says "if the insurer gets the application and full payment in time", which is no stronger than the FIM quotes (10 days, 30 if the lender/title company pays). It does not say the window is counted from closing, so a reader may think "in time" means before closing. Optional: "within days of closing".
- No other defects: purchase text keeps "only", scope (A or V, federally regulated or backed mortgage, federal help) and adds "a lender may still require it" (Fed Q&A: "a lender may require flood insurance as a condition of making the loan, as a matter of safety and soundness"; it also says a lender may require it even when the building is not in an SFHA). save_ways keeps "may" and names deductible, risk work and Elevation Certificate, matching FEMA's article ("can help to lower"). Home headline numbers carry their bases.
Verdict: FAIL

## louisiana
- No defects in the changed text. Lead sentence base is right ("single-family primary home", premium plus fees, as of Aug 31, 2026); "Does it pay out here?" now says "(all years on record) paid something", and the 2020s figure is separate.
- MINOR: tile "52.8% Pay below FEMA's full-risk price" no longer names its base. It is single-family primary-residence policies with both premiums (the same cohort as the median), implied only by the neighbouring tiles. Optional: "of these policies".
Verdict: PASS

## palm-beach-county-fl
- No defects in the changed text. $673 equals agg.json policies.p50 for the single-family primary-home cohort; "policies in force as of August 31, 2026" matches asof. Quick answers are consistent with the sources; the Florida Citizens sentence is separate, scoped and unchanged.
- MINOR: same tile-base point as louisiana (23.2%).
Verdict: PASS

## harrison-county-ms
- No defects in the changed text. Lead and quick answers match the pattern verified above; the "(all years on record)" claim sentence names its base and the state comparison.
- MINOR: same tile-base point (67.1%).
Verdict: PASS

## glynn-county-ga
- No defects in the changed text. Same wording pattern as above; the 68.1% (all years) and 71.1% (2020s) figures are labelled apart.
- MINOR: same tile-base point (34.4%).
Verdict: PASS
