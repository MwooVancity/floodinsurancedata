# Round 70 (LIGHT: page text only from dist HTML, no screenshots, no Google search; checklist A-N judged on changed parts only, all other lines unchanged since round 69 = PASS)

Previous items (round 69): zero BLOCKER/MAJOR were open. Round 68 MAJORs stay FIXED: zone D "Must I buy?" still says D is not A or V and now ends "Outside those zones, a lender may still require it."; zone_x source still in manual-rule-read. 0 NOT FIXED.

Checked:
- Home and /flood-insurance/ state table: Connecticut 31,454 / 29,492 / $544,191,966; Hawaii 65,818 / 6,285 / $167,844,607; New Jersey 195,686 / 202,340 / $6,250,856,025; Alaska and DC also match data\states\built.json (claims, paid). Louisiana row 485,743 / $20,682,152,359 equals the Louisiana page's claim card (485,743 claims, $20.7 billion, "Total paid $20,682,152,359"). Note text "every claim record, paid or not, for losses from 1978 to 2026. Paid on them: building plus contents payments, in dollars as paid, not adjusted for inflation" matches tools/ffcalc.py (rows = all records; paid = netBuilding + netContents; year range 1978-2026 in agg.json). H2 "Flood insurance policies and claims by state" matches the table.
- Rule text: lender_any_zone matches its Federal Reserve quote ("a lender may require flood insurance as a condition of making the loan, as a matter of safety and soundness"). zone_codes V part: eCFR quotes say "inundated by tidal floods (coastal high hazard area)" and "with velocity"; "fast-moving water" is a plain gloss of "velocity", not a quote.
- Zone pages: x heading and table last column agree ("share of the state's paid claim dollars outside zones A and V"). d page: "14 more states have zone D policies but under 50 priced ones" equals 16 states with a D cost entry minus the 2 in the table (California, Hawaii).

## home
- MINOR: new columns put "Insured units" (a snapshot on Aug 31, 2026) next to "NFIP claims on record" (cumulative since 1978). In New York, 175,430 claims sit beside 166,378 units and in New Jersey 202,340 beside 195,686; a scared reader may read it as more than one claim per policy. The note under the table labels the claims base but does not say the units are a today-only count (that sits in the line above the table). Add "since 1978" to the column head or "vs units in force today" to the note.
- MINOR: "Paid on them" is a bare dollar figure to the dollar ($5,681,770,494) while county and state pages round to "$20.7 billion"; same figure, two rounding styles on one site.
- GAP: sorted by typical cost, so the largest-loss states (LA, FL, TX, NJ) are scattered; no way to sort by claims. Never blocking.
Verdict: PASS

## louisiana
- Cost card heading "Flood insurance cost in Louisiana" fits its content (median, spread, coverage in force, surcharge). Claims card heading "Flood insurance claims in Louisiana: what floods pay out" fits (claims count, payouts, paid share, unpaid reasons, biggest events).
- MINOR: H1 is "Flood insurance cost in Louisiana: $1,114 median a year..." and the cost H2 repeats the same words; harmless but repetitive.
- MINOR: "coastal high-risk, flooded by tides with fast-moving water (velocity)" is a gloss beyond the CFR wording; reads correctly, not misleading.
- Rule line "Outside those zones, a lender may still require it." reads correctly and carries its scope (lender, not law).
Verdict: PASS

## palm-beach-county-fl
- Both card headings fit their cards (cost: median $673, range, coverage; claims: 10,758 claims, $72.0 million, since 1978). Claim total in text equals agg.json (10,758; $71,995,287 rounds to $72.0 million).
- MINOR: same H1/H2 repetition as Louisiana.
Verdict: PASS

## new-york-county-ny
- Headings fit. The cost card is built on only 171 single-family primary-home policies and says so ("from 171 single-family primary-home policies"), so the thin base is shown beside the figure.
- MINOR: 1,498 claims since 1978 against 14,925 units is labelled as a cumulative tally, not a rate; OK.
Verdict: PASS

## dorchester-county-sc
- Headings fit. "since 1979" and "~47 years" agree with each other and with the first yearly row (1979). Claims card shows 779 claims, $16.8 million, consistent.
Verdict: PASS

## nassau-county-ny
- Headings fit. 51,523 claims against 40,981 units is correctly framed as a cumulative tally vs a present snapshot.
Verdict: PASS

## Classes
- Home/state index: claims column (cumulative) beside units column (snapshot) invites a claims-per-policy misreading (MINOR); exact-dollar vs rounded-dollar styles differ between the table and the cards (MINOR).
- State and county template: H1 and cost-card H2 repeat the same words (MINOR). New headings match their card contents on all five pages checked. No BLOCKER or MAJOR in any class.
- Not done in light mode: no Google top-3 comparison, no screenshots, no source re-fetch of the Fed Q&A or eCFR (judged from registry quotes plus the gate-side checks already in place; the registry's own excerpt is not an independent source check).
