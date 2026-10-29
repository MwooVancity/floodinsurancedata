# Hater round 17 (light check, page text only)

Marks are against round-16 BLOCKER/MAJOR lines. Round 16 had no BLOCKER.

Shared state-page findings (apply to louisiana, palm-beach-county-fl, maine, nebraska, broward-county-fl):
- FIXED: "Renewing?" mislabel. Now "This year's bills: policies whose term began in 2026 (renewals and policies sold this year together) typically pay $1,215. Buying? Policies first bought in the past year typically pay $1,139."
- FIXED: quote checker message (inline R string): "These are existing policies, many still below FEMA's full-risk price, so a new quote often lands higher. Policies first bought in the past year typically pay $1,139." Buyer figure now shown.
- NOT FIXED (MAJOR): hero card text unchanged: "Pay less than FEMA's full-risk price, so their bills rise each year". The defining sentence ("FEMA's full-risk price is its price for that risk") sits below the hero cards, and the 18% cap is still not beside the card.
- PARTLY (MINOR now): zone codes. A "What the zone codes mean (44 CFR 64.3)" note exists, with "Zone C" and "Zone B" glossed as minimal/moderate risk, but table rows still read "Zone C", "Zone B" with no "(low-risk)" tag while A/V rows get "(high-risk)"; the checker dropdown has no gloss (now alphabetical, so findability is FIXED).
- NOT FIXED (MAJOR): "CRS class" column ("Jefferson Parish 35% 3") is still never explained (lower class = bigger discount).
- FIXED: disaster lines now carry month and "(emergency declaration)", e.g. "September 2023 - Hurricane Lee (emergency declaration)", "August 2020 - Hurricane Isaias (emergency declaration)".
- No new wrong text found in: "(unincorporated area only)" note ("A community named for the parish covers its unincorporated area only."), NRI wording, About anonymity line ("The site is run anonymously, by choice: there is no named author."), dist\404.html.

## home
- Round-16 MAJOR "3,490,299 records next to 4.6M units": FIXED. Now "(one record can cover several insured units, such as a condo building)" in the same sentence.
- Round-16 MAJOR quote checker: NOT FIXED. Inline script: "$X is in the top quarter of U.S. single-family policies (half pay $713 to $1,309)." The text above it says only "Type your yearly cost (premium plus fees) to see where it sits among U.S. single-family policies". Nothing says these are existing, partly discounted policies, and the $995 new-buyer figure is not in the output.
- MAJOR (open): the above.
- MINOR: "(top tenth)" branch reads "in the top tenth of U.S. single-family policies", same caveat gap.
- 404 and About: no defect.
Verdict: FAIL

## louisiana
- Quote checker: FIXED (R string above). Renewing mislabel: FIXED.
- Screen-1 payout caveat: PARTLY. "77.8% of claims here paid something; the average paid claim was $55,453 (all years, not inflation-adjusted)... Some unpaid claims are paperwork, not denied floods." The unpaid-claims caveat is now beside it; but the $55,453 still mixes 1978-2026 dollars and Katrina with no note beside it. (MINOR remaining.)
- Hero "bills rise each year": NOT FIXED (MAJOR).
- Zone codes: PARTLY; the gloss note is at the zone-cost table, ~100 lines below the zone share table with "Zone C 16,047 3.9%" and "Zone B 5,899 1.4%" untagged. CRS class: NOT FIXED (MAJOR).
- Disaster lines: FIXED. "(unincorporated area only)": note present, no defect.
Verdict: FAIL

## palm-beach-county-fl
- Payout caveat: FIXED. "43.5% of claims here paid something (Florida: 69.9%)... Some unpaid claims are paperwork, not denied floods." sits in the same screen-1 paragraph.
- NRI contradiction: FIXED. "Relatively High for coastal flooding and Relatively High for inland (river) flooding, by FEMA's county rating", then "a separate FEMA measure, loss per dollar of building value: inland flood loss here is higher than in about 30% of U.S. counties." Two measures are named. MINOR: a reader may still read High vs 30% as odd.
- Quote checker and Renewing: FIXED.
- Hero "29.5% ... bills rise each year" with "Median premium $507, full-risk $514" (1% gap): NOT FIXED (MAJOR). The page's own line says "their bills are rising toward it" yet the gap is $7.
- Zone C $544 cheapest row, untagged but note follows the table: PARTLY (MINOR). CRS class: NOT FIXED (MAJOR).
Verdict: FAIL

## maine
- Costliest-year sentence: FIXED. "The costliest flood FEMA named here was Flooding (1987): $10.0 million across 481 NFIP flood claims. The costliest year, 2024 ($29,311,445), has no single named flood." MINOR: two 2024 disasters exist, "no single named flood" is slightly vague.
- Disaster list repeats: PARTLY (MINOR). Months added, but "September 2023 - Severe Storm and Flooding" appears twice, plus the Lee line in the same month.
- Quote checker/Renewing: FIXED. Hero "bills rise each year" (48.0%): NOT FIXED (MAJOR). "Zone C" / A02 / V02 labels: PARTLY. CRS class: NOT FIXED (MAJOR).
Verdict: FAIL

## nebraska
- Disaster repeats: FIXED (August/September/October 2024 now distinguish them).
- Box Butte contradiction: FIXED. "Box Butte County (unincorporated area only)" in the Not-in-NFIP list.
- County table dashes: NOT FIXED (MAJOR). "Keith County | 47 | - | -" and "Knox County" style rows next to "Kearney County | 41 | $870 | 42.4%"; column is "Policy units", lead says "30 or more priced policies" but priced counts are never shown.
- Quote checker/Renewing: FIXED. Hero "35.7% ... bills rise each year": NOT FIXED (MAJOR). CRS class: NOT FIXED (MAJOR).
Verdict: FAIL

## broward-county-fl
- Quote checker/Renewing: FIXED ("$771" buyer, "$876" this-year term).
- Payout line: "49.8% of claims here paid something (Florida: 69.9%)... Claims filed for losses in the 2020s: 78.3% paid something. Some unpaid claims are paperwork" - caveat beside it, FIXED.
- NRI wording: "Coastal flood risk rating (FEMA) Very High" and "a separate FEMA measure, loss per dollar of building value: coastal flood loss here is higher than in about 71% of U.S. counties" - FIXED, no new defect.
- Hero "bills rise each year" (46.4%, median $643 vs full-risk $673): NOT FIXED (MAJOR). CRS class: NOT FIXED (MAJOR).
Verdict: FAIL
