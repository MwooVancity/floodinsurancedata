# Hater review, round 2 (2026-10-26)

Pages: home, /flood-insurance/louisiana/, /flood-insurance/palm-beach-county-fl/, plus /about/ and /methodology/.

**What I read**
- Every unique phone screenshot: home-00..06, louisiana-00..25, palm-beach-00..21. I checked by md5 that the later files are byte-identical repeats of the page bottom.
- The built HTML: text, head, JSON-LD, the checker script and the chart SVG.
- The JSON files: data/states/louisiana/{agg,extras,data}.json, data/states/florida/agg.json and data/c/palm-beach-county-fl/{agg,extras,data}.json.
- tools/metrics.py and tools/rules_registry.py.
- tools/collect.py, but only the grep lines that show which NRI fields are pulled. I read no gate code.

**One web check**: FEMA's NRI riverine-flooding page (hazards.fema.gov/nri/riverine-flooding). It confirms that NRI expected annual loss covers buildings, population (population equivalence) **and** agriculture, not buildings alone.

I wrote this defect list before opening hater-round1.md.

Severity: BLOCKER = wrong or misleading information a reader could act on. MAJOR = confusing, untrustworthy or broken. MINOR = polish.

---

## Home (dist/index.html)

1. **MAJOR**, home-00: "Built from 3,490,299 NFIP policy records ... matched to FEMA's own count."
   - "FEMA's own count" is the API's record total for the same download (methodology: "check the count against the API's own record total"), so the check is circular.
   - /about/ itself says "FEMA's separate official policy count is not yet compared", and the methodology lists the "Official Policy Information by State and Community workbook" as a benchmark that no page uses.
   - The national figure (3.49M records shown as "4.6M insured units") has never been checked against FEMA's published policies-in-force. The trust line overclaims.
2. **MAJOR** (YMYL), /about/: no named person, no organisation, and no contact or corrections address. The meta description promises "Who runs Flood Insurance Data", and the page never says who. An anonymous money and insurance site fails a rater's "who is responsible" check on its own.
3. **MAJOR**, home-01: "Am I required to buy it? Only if your home is in a high-risk zone (A or V) and your mortgage is from a federally regulated lender, or federal help to buy or build."
   - Unlike the state and county pages, the home page leaves out both "federally backed" and "a lender can still require coverage" (the lender_any_zone rule).
   - A reader outside the A/V zones is told "only if" and walks away believing nobody can require it.
4. **MAJOR**, home-00/03..06: the H1 says "What flood insurance costs in your state **and county**", and the search box says "Type your state or county…". There are 42 county pages for about 3,100 counties, and the selection rule is never stated. Kanawha County, WV (1,283 units) and St. Louis County, MO (3,126) have pages. For most readers, typing their county returns nothing.
5. **MINOR**, home-00: "$88 PER MONTH". This is the yearly median ÷ 12, but the tile reads as if NFIP bills monthly. Say "≈ $88 a month if spread over 12".
6. **MINOR**, home-00: "50 STATES AND DC". Puerto Rico, the USVI and Guam (all NFIP participants) are silently excluded.
7. **MINOR**, home: the page has zero data-m or data-p tags. "$1,055 U.S. median" cannot be traced to a JSON path or reproduced from the table (the median of the state medians is $1,027).
8. **MINOR**, home-01: "Buy it now:" is a sales imperative on a site whose About says "a reference, not a sales page".
9. **MINOR**, home-01: "Most homeowners insurance does not cover flood damage." Standard homeowners policies exclude flood. "Most" invites "maybe mine does".

Counts: 0 BLOCKER, 4 MAJOR, 5 MINOR. **Verdict: FAIL**

---

## Louisiana (dist/flood-insurance/louisiana/index.html)

### MAJOR
1. **MAJOR**, louisiana-21, "How often is Louisiana a flood disaster?": three of the six listed storms carry the wrong name.
   - The list reads "2024 — Tropical Storm Francine", "2021 — Tropical Storm Ida" and "2020 — Tropical Storm Zeta".
   - data.json has DR-4817 "HURRICANE FRANCINE", DR-4611 "HURRICANE IDA" and DR-4577 "HURRICANE ZETA". The page takes the pre-landfall emergency (EM) title instead: EM-3614, EM-3568, EM-3549.
   - The same page's claims table says "Hurricane Ida (2021)".
   - Ida made landfall at Category 4. Calling it a tropical storm is the line a competitor screenshots.
2. **MAJOR**, louisiana-01: the page says "Your flood zone is set at your exact address and **drives your price** and whether coverage is required. Look it up first, then read your zone's row".
   - Its own zone card (louisiana-11) says "price is set from each building's own flood risk, not its zone".
   - Its data shows Zone X at $1,080 above Zone A ($1,012), AH ($906) and AO ($623).
   - The first-screen instruction is built on the premise that Risk Rating 2.0 removed.
3. **MAJOR**, louisiana-06 and the meta description: "485,743 claims since 1978 against 407,916 **policies** in force today". 407,916 is policy units; the page's own count of records is 395,032. The meta description says "395,032 policies".
   - The page carries five different "policy" counts: 395,032 records, 407,916 units, 359,013 "residential policies", 292,018 single-family and 212,784 reporting a rebuild cost.
   - They are reconciled only in the last card, in small print.
4. **MAJOR**, louisiana-09, "Would a policy here pay to rebuild my home?":
   - "21.5% rebuilding cost above the building limit (of 212,784 policies reporting one)" sits next to "64.8% single-family policies insured to the building maximum (all of them, not only those above)". Read literally, about 43% of homes are insured for more than their own rebuild cost. Either the replacement-cost field is unreliable or the label is wrong, and the page says neither.
   - The headline "Not in full for 21.5% of insured single-family homes" rests on the 73% that report a rebuild cost.
   - The third tile ("16.1% damage was more than the coverage, of 361,020 claims") covers every claim of every occupancy since 1978, placed in a single-family card.
5. **MAJOR**, louisiana-01 vs louisiana-23, and JSON-LD:
   - Top: "matched to FEMA's own count, none missing".
   - Bottom: "FEMA also publishes a separate official policy count, which we have not yet compared for Louisiana", followed by "Count reconciliation (not a snapshot proof)", which no homeowner can parse.
   - Schema: "reconciled to FEMA's published record count".
   - It is the same circular check as Home 1, so the verification claim on the first screen is contradicted by the last.
6. **MAJOR**, louisiana-03: "21.4% of the flood-insurance claim money paid in Louisiana went to homes outside the high-risk zones, which hold 49.0% of policies here: less per policy than inside".
   - The numerator is cumulative 1978–2026 claim dollars (building payments only, per metrics.py, all occupancies, so not "homes"). The denominator is the July-2026 unit share.
   - Maps were redrawn, and Katrina dominates the numerator. The "less per policy" inference compares two different eras.
7. **MAJOR**, louisiana-22: "FEMA approved $4.6 billion ... about $2,513 per registration, against an average paid flood-insurance claim of $55,453."
   - The first figure is per registration, including $0 approvals, since 2002. The second is per *paid* claim, including ICC, in nominal dollars since 1978.
   - metrics.py gives these two figures different units (usd_aid_paid vs usd_claim_paid), and the page puts them in one sentence with "against". The reader concludes insurance pays 22x aid. The ratio is an artefact.
8. **MAJOR**, louisiana-18/19: "Does my town get a community discount? **Yes**, in 42 of the 353 NFIP communities here."
   - For 311 of 353 (88%) the true answer is no.
   - Also, "Lafayette City-Parish (Lafayette Parish)" and "Lafayette (Lafayette Parish)" are both listed at 15%/class 7 with no explanation, and "A community named for the **county**" appears on a parish page.
9. **MAJOR**, louisiana-05/06/07, numbers that do not reconcile:
   - The chart caption gives 2005 as "$13,559,493,222". The event table gives Katrina $13.3 billion + Rita $412.9 million = $13.7 billion, more than the whole year. The events include ICC and the years exclude it, and neither basis is named next to the other.
   - $20,682,152,359 ÷ 377,993 paid claims = $54,716, not the "$55,453" average printed twice. This is disclosed in small print, but a copy editor still fails it.
10. **MAJOR**, louisiana-10/11: Zone C, Zone A99 and Zone B are all "$1,086", identical to the state median of $1,086.
    - The new note says "Several **low-risk** zones show the same median because many policies pay one of a few standard amounts". A99 is high-risk, and the page's own zone table labels it "Zone A99 (high-risk)".
    - No evidence of the "standard amounts" is shown. It is still unproven.
11. **MAJOR**, louisiana-19: "How often do the same homes flood here? Yes: FEMA's disaster-aid records hold 85,549 damage records". "Yes" answers a "how often" question, and no frequency is ever given, so the block does not answer its heading.
12. **MAJOR** (rater, templated), the whole page:
    - The purchase rule appears three times: the "Am I required to buy it?" tile, the "Am I required to carry it?" card, and "Whether a lender can require coverage ... is under 'Am I required to carry it?'". The tile and the card use different question names.
    - $250,000/$100,000 appears twice (the tiles and the rebuild-card sentence). "How fast" appears twice.
    - Whole paragraphs ("Insured claims only, by each policy's rated zone…", "Yearly cap…", "The Community Rating System cuts…", "What this data cannot tell you") are word-for-word on the county page.
13. **MAJOR**, louisiana-21: "FEMA's National Risk Index rating (coastal and inland flooding, the worse of the two), **a model of expected loss**." The NRI risk rating is expected annual loss × social vulnerability ÷ community resilience, not expected loss. An analyst would call this a mis-definition.
14. **MAJOR** (trust), JSON-LD: `"creator": {"@type": "Organization", "name": "FEMA OpenFEMA"}`. The structured data tells Google that FEMA created this page's dataset, while the footer says "not endorsed by FEMA". FEMA did not create these aggregates.

### MINOR
15. louisiana-00: "$90 PER MONTH" (÷12, reads as monthly billing).
16. louisiana-16: "56.6% of **policies here** pay less than FEMA's full-risk price". The cohort is 292,018 single-family primary policies, not the 395,032 "policies here". The tile one screen down gets it right ("56.6% of 292,018").
17. louisiana-04: "Half of **homeowners** here pay between $863 and $1,273". It is half of *insured* single-family policyholders, and 78% of homes have no NFIP policy.
18. louisiana-04: "To check a quote, use the checker at the top". The checker is the second card, not the top. It also duplicates the top tile "Is my quote normal?". The checker benchmarks single-family policies only but says "existing policies here", so a condo or rental owner compares against the wrong cohort.
19. louisiana-09/04: "$100,000 on contents, **which is a separate policy**". Contents is separately purchased coverage on the same NFIP policy. The wording comes from FloodSmart, but readers will think they need a second policy.
20. louisiana-07: "Of the 107,750 claims ... the top reason ... was 'not an actual flood' (20,318 claims)". The largest bucket is "Smaller reasons, or none recorded 35,155" (33%), bigger than the "top reason" (19%). The heading "Why do flood claims here go unpaid?" calls every closed-without-payment claim unpaid.
21. louisiana-08, rounding: "$103,300" and "$92,400" vs "$68,576" and "$53,042"; "$13.3 billion" vs "$691.8 million"; "~49 years" with a tilde in prose.
22. louisiana-08: "Mid summer severe storms (2016)". extras.json has FEMA's "Mid-summer severe storms". The page drops the hyphen (open since round 1).
23. louisiana-05: the chart has no y-axis, and per-year values exist only in SVG `<title>` hover tooltips, which a phone cannot hover.
24. Dates: "downloaded October 25, 2026" (louisiana-01) vs "The newest of these downloads was October 26, 2026" (louisiana-24).
25. louisiana-11: a 25-row zone table (A01..A15, V15, AHB) on a 390px screen is a wall of legacy codes, and the AE reader scrolls past 20 rows that do not apply.
26. Meta description and JSON-LD: "middle half $863–$1,273" is jargon; the page itself now says "Half pay between".
27. louisiana-24: "A per-effective-year median is shown only where several years of policies exist." This is jargon, and agg.json holds exactly such a split (2025-effective median $1,080 vs 2026-effective $1,215, +12.5%), which the page does not show. A renewal reader would want it.
28. Every NRI source line: "NRI 2023 release". A secondary site cites a December 2025 NRI release. That is unverified, but the vintage should be checked.

Counts: 0 BLOCKER, 14 MAJOR, 14 MINOR. **Verdict: FAIL**

---

## Palm Beach County, FL (dist/flood-insurance/palm-beach-county-fl/index.html)

### MAJOR
1. **MAJOR**, palm-beach-18: "2022 — Tropical Storm Nicole" and "2022 — Tropical Storm Ian". data.json has DR-4673 "HURRICANE IAN" and DR-4680 "HURRICANE NICOLE". The page took EM-3584 "TROPICAL STORM IAN" and EM-3587 "TROPICAL STORM NICOLE". Ian was among the deadliest hurricanes in Florida's history, and a Florida reader will stop trusting the page here.
2. **MAJOR**, palm-beach-14: "Inland: FEMA models roughly **$178.9 million of flood loss a year across all its buildings** ... Any loss figure is a whole-county estimate across all buildings".
   - The value is IFLD_EALT (tools/collect.py), NRI's *total* expected annual loss, which FEMA defines over buildings, population (population equivalence) and agriculture. It is not buildings only, so the label is wrong.
   - It sits two cards from NFIP payouts of "$72.0 million" over 48 years and NWS damage of "$71.1 million" over 30 years, with no word on why a model says 2.5x the whole insured history every single year. The reader is either terrified or concludes the site is broken.
   - "Relatively High for rivers and heavy rain": NRI's inland hazard is riverine flooding, and "heavy rain" is not in its definition.
   - The state-compare card again calls the rating "a model of expected loss" (Louisiana 13).
3. **MAJOR**, palm-beach-01: "Your flood zone ... drives your price". This is the same false premise as Louisiana 2. Here Zone AO (high-risk) costs $645, Zone X $618 and Zone C $544.
4. **MAJOR**, palm-beach-06: "10,758 claims since 1978 against 132,945 **policies** in force today". The top of the page says "75,140 in-force NFIP policy records", so "policies" inflates the count by 77%. Other counts on the page are 69,154 "residential policies", 50,781 single-family and 27,755 reporting a rebuild cost.
5. **MAJOR**, palm-beach-09: "50.6% rebuilding cost above the building limit" beside "91.5% single-family policies insured to the building maximum (all of them...)".
   - About 41% of homes would then be insured above their own rebuild cost, and the page explains nothing.
   - The headline "Not in full for 50.6% of insured single-family homes" rests on 27,755 of 50,781 (55%) that report a rebuild cost. It frightens half the county with a field that half the records leave blank.
6. **MAJOR**, palm-beach-01/19, verification:
   - "matched to FEMA's own count **for the state**": the county itself is never checked, and claims are assigned by the claims file's county code ("may not exactly match a policy's property county").
   - The county's claims look anomalous and the page does not say so. Palm Beach has 8.1 claims per 100 current units, against Broward 14.9, Miami-Dade 16.9 and St. Lucie 20.8 (florida/agg.json).
   - St. Lucie, with 19,192 units, has been paid $84.3M, more than Palm Beach's $72.0M with 132,945 units.
   - None of this is reconciled with FEMA's published loss statistics.
7. **MAJOR**, palm-beach-07: "Do flood claims here actually pay out? **Most don't**: 56.5% of claims here closed with no payment" (Florida 30.1%).
   - A just-flooded reader sees "Most don't" and may not file.
   - Of the 6,077 claims closed without payment, 3,376 (56%) carry no substantive reason: "Smaller reasons, or none recorded" 1,837, "Other" 1,107 and "Assigned in error" 432.
   - Why the county runs at almost twice the state rate is never examined. The "some closed claims are paperwork" caveat is in the small print, while the headline is the scare.
8. **MAJOR**, palm-beach-03: "45.5% of the flood-insurance claim money ... went to homes outside the high-risk zones, which hold 58.2% of policies here".
   - It has the same cross-era mismatch as Louisiana 6: 1978–2026 building dollars of all occupancies against 2026 unit shares.
   - In the zone table (palm-beach-02), "Zone X 57.5%" + "Other or unclassified zones 0.6%" = 58.1%, not 58.2%.
   - The "unclassified" 835 units are Zone C (616) + Zone B (219) (agg.json). These are named low-risk zones that the Louisiana page lists by name.
9. **MAJOR**, palm-beach-18/19: "about $591 per registration, against an average paid flood-insurance claim of $15,396". This is the same apples-to-oranges comparison as Louisiana 7, and the aid here is almost all hurricane (wind) aid.
10. **MAJOR** (rater, templated): Louisiana 12, verbatim, including the triple purchase rule and the identical card paragraphs.
11. **MAJOR** (trust), JSON-LD `"creator": "FEMA OpenFEMA"`: same as Louisiana 14.

### MINOR
12. palm-beach-00: "$56 PER MONTH".
13. palm-beach-15: "How often do the same homes flood here? Yes: FEMA's disaster-aid records hold 216 damage records". This is the same non-answer as Louisiana 11.
14. palm-beach-05/06: 2025 is highlighted orange as a top-three year ($6,857,416), from only 99 claims. That is an average of about $69k, 4.5x the county average, and no named flood event explains it. It is an outlier like round 1's Opal, published unchecked.
15. palm-beach-00: "36% below the U.S. median" ($670/$1,055 = 36.5% below). Neighbouring figures round to the nearest point, so this should be 37%.
16. palm-beach-12/13: "Palm Beach 20%" (the Town of Palm Beach) sits a few rows from "Palm Beach County 25%" (unincorporated only). The town is still unlabeled.
17. palm-beach-04: "Half of homeowners here pay…" and "To check a quote, use the checker at the top" (Louisiana 17/18).
18. palm-beach-10: "$100,000 on contents, which is a separate policy" (Louisiana 19).
19. palm-beach-12: "29.5% of policies here pay less than FEMA's full-risk price". The cohort is the 50,781 single-family policies.
20. palm-beach-10: the Zone VE row ($1,393, n=116), the highest-stakes zone, has no small-sample caution, and the ZIP medians are published at 25 policies.
21. palm-beach-11: the ZIPs still have no place names (33480 is the Town of Palm Beach, 33484 is west Delray Beach).
22. Dates: "downloaded October 25, 2026" vs "newest of these downloads was October 26, 2026". "Data effective 1996-2025" uses a hyphen where the other ranges use an en dash.
23. Chart: no axis, and values only in hover tooltips (Louisiana 23).
24. "NRI 2023 release": vintage unverified (Louisiana 28).

Counts: 0 BLOCKER, 11 MAJOR, 13 MINOR. **Verdict: FAIL**

---

## Classes (likely on every page of the template)

**state + county**
- Disaster list prefers the EM title ("Tropical Storm X") over the DR title ("Hurricane X") for the same storm. Expect wrong names wherever an emergency was declared before landfall: Ian, Nicole, Ida, Francine, Zeta, probably Laura/Marco, Sally, Michael and others.
- "Your flood zone ... drives your price" in the intro, contradicted by the Risk Rating 2.0 note further down.
- "N claims since 1978 against N **policies** in force today" prints units as policies. Five unreconciled counts per page.
- The rebuild card pairs "% rebuild cost over $250k" with "% insured to the building maximum" in a way that implies mass over-insurance. The denominator is only the records that report a rebuild cost, and the damage tile mixes all occupancies.
- "matched to FEMA's own count" (circular) on the first screen vs "not yet compared" at the bottom. The schema claims reconciliation.
- Outside-zone dollar share (cumulative, building-only, all occupancies) compared with the current unit share, then labeled "homes" and "less per policy".
- Aid per registration "against" the average paid claim.
- "How often do the same homes flood here? Yes:" never answers how often.
- "Does my town get a community discount? Yes" whenever any one community has CRS.
- Event totals include ICC and year totals exclude it; the average includes ICC and the total excludes it. The bases are never named side by side.
- Templated triple purchase rule and verbatim cross-page paragraphs.
- NRI described as "a model of expected loss" (it is risk = EAL × vulnerability ÷ resilience).
- JSON-LD names FEMA as the creator.
- "$X PER MONTH" tile; "half of homeowners"; "policies here" for the single-family cohort; "which is a separate policy"; the hover-only chart values; the Oct 25 vs Oct 26 dates; inconsistent rounding.

**county**
- NRI EALT printed as loss "across all its buildings" (it includes population and agriculture), and never reconciled with the NFIP and NWS totals on the same page.
- Records are verified only at state level, and claims are assigned by the claims county code. Anomalies against neighbouring counties are not flagged.
- B and C zones are lumped into "Other or unclassified".
- Outlier years and events (few claims, huge dollars) are highlighted without a check.

**state**
- Identical zone medians equal to the state median (C/A99/B $1,086), with a note that mislabels A99 as low-risk.
- "A community named for the county" on parish pages; duplicate community names in the CRS table.
- Year-split medians are held in agg.json but hidden.

**home**
- No lender-can-require caveat on the purchase rule.
- The county promise is not matched by 42 pages.
- No owner or contact.
- No traceability tags.
- Territories dropped silently.

---

## Round 1 items (every round-1 BLOCKER and MAJOR)

### Home
| # | R1 item | Status | Evidence |
|---|---|---|---|
| 1 | 4.6M units under a single-family caption | FIXED | home-00 caption now: "Insured units: every NFIP policy unit in force on July 31, 2026, including condos, rentals and businesses." |
| 2 | County table without state names | FIXED | home-03..06: "Orange County, CA", "Jefferson County, TX", "Monroe County, FL". |
| 3 | "really costs / near you" overclaim | PARTLY | Now "From FEMA's own records of existing policies and claims, not quotes", but the H1 still promises "your state and county" with 42 county pages (Home 4). |
| 4 | No named person or organisation, no contact | NOT FIXED | /about/ names nobody and gives no contact, while its meta description promises "Who runs". |
| 5 | About contradicts the pages | FIXED | /about/: "FEMA's separate official policy count is not yet compared"; "Two figures are FEMA models". |
| 6 | "matched to FEMA's own count" overclaim | NOT FIXED | home-00 still says "matched to FEMA's own count", which is the API's own total (methodology). |
| 7 | Methodology contradicts the pages | FIXED | Methodology lists the 100/50/30/25 minimum sizes, the multiple-loss definition and "ACS ... used only where FEMA's own penetration rate is missing". New, minor: "We do not use FEMA's summary tables", yet the penetration rates are one. |

### Louisiana
| # | R1 item | Status | Evidence |
|---|---|---|---|
| 1 | BLOCKER: CRS "Other areas" pre-Risk Rating 2.0 column | FIXED | One "Discount" column; "the same in every flood zone" (louisiana-18). |
| 2 | BLOCKER: "pay less than the sticker price" | FIXED | "It is automatic, already in these prices" (new defect: the "Yes" for 12%, Louisiana 8). |
| 3 | BLOCKER: chart drew counts captioned as dollars | FIXED | "Bar height is dollars paid that year". The SVG confirms it: Palm Beach 2025 is 52.5/126 of the 2004 height, the same ratio as $6.86M/$16.47M. |
| 4 | Zone table did not add up; VE hidden | FIXED | 39.1+5.2+1.5+5.2 = 51.0; "Other high-risk zones (A10, A01, AH, VE and others)". |
| 5 | C/A99/B = $1,086 = state median | PARTLY | Still identical. The new note is unproven and calls A99 "low-risk" (Louisiana 10). |
| 6 | Checker bias against new quotes | FIXED | Every result ends "If this is a new policy, it is priced at full risk, which is often higher." |
| 7 | Full-risk tile read as good news | FIXED | "BELOW FULL-RISK PRICE: BILLS STEP UP YEARLY"; "Bills already at full risk still change with FEMA's yearly rate updates." |
| 8 | 18% vs 18–25% contradiction; years to full-risk | FIXED | "a primary home's premium cannot rise more than 18% ... second homes and businesses, can rise up to 25%". The years ratio is gone. |
| 9 | Average includes ICC, total excludes it; "years of bill" | PARTLY | The "years of the typical bill" line is gone and the ICC basis is disclosed, but $20.68B ÷ 377,993 = $54,716 ≠ $55,453 is still printed (Louisiana 9). |
| 10 | Aid "after floods" included all disaster types | FIXED | "after floods and storms ... COVID, fire, ice-storm and tornado aid are left out"; "including those approved for nothing". |
| 11 | Repeat-flood source, text and methodology mismatch | FIXED | The source is now "Individual Assistance Multiple-Loss Flood Properties"; "damage records"; "records from homes on FEMA's severe repetitive loss list". |
| 12 | Unpaid table showed 3 rows (46%) | FIXED | Five rows plus "Smaller reasons, or none recorded 35,155" = 107,750. |
| 13 | "Policies" meant four numbers | PARTLY | Table headers now say "Policy units" or "Priced policies", but the prose says "407,916 policies in force today" and the meta says "395,032 policies" (Louisiana 3). |
| 14 | "Maximum building coverage" had no denominator | PARTLY | Denominator added ("all of them"), which exposes the contradiction with 21.5% (Louisiana 4). |
| 15 | "Low end / High end" labels on percentiles | FIXED | "A quarter pay under $863 · Typical $1,086 · A quarter pay over $1,273". |
| 16 | Zeta double-counted and given the wrong year | PARTLY | Now "2020" and the total is 67, but it is now named "Tropical Storm Zeta" (DR-4577 is HURRICANE ZETA), and Ida and Francine are renamed the same way (Louisiana 1). |
| 17 | Official count never checked, in jargon | NOT FIXED | "which we have not yet compared for Louisiana"; "Count reconciliation (not a snapshot proof)" is still printed. |
| 18 | Templated repetition | PARTLY | The short tile and full card now differ, but the purchase rule appears 3 times, $250k/$100k twice, and the paragraphs are identical across pages (Louisiana 12). |
| 19 | "Already flooded" omitted the aid purchase rule | FIXED | "If FEMA aid pays to repair a home in a high-risk zone, you must buy and keep flood insurance". |
| 20 | Thresholds vs the methodology's ≥100 | FIXED | Methodology now lists 100/50/30/25, matching the pages. |

### Palm Beach
| # | R1 item | Status | Evidence |
|---|---|---|---|
| 1 | BLOCKER: NRI percentile mislabeled; false precision | FIXED | "per dollar of building value, that loss is higher than about 30%"; "$7.5 million". New: EALT labeled "across all its buildings" (Palm Beach 2). |
| 2 | BLOCKER: CRS "Other areas" column | FIXED | Single "Discount" column. |
| 3 | BLOCKER: "sticker price" discount | FIXED | "It is automatic, already in these prices". |
| 4 | BLOCKER: chart counts vs dollars | FIXED | SVG heights are proportional to dollars (2025 at 52.5, 2004 at 126). |
| 5 | Headline median hid ZIP spread | FIXED | First screen: "By ZIP it ranges from $450 (33484) to $1,825 (33480); find your ZIP." |
| 6 | Unlabeled county and town CRS rows | PARTLY | "A community named for the county covers its unincorporated area only" was added, but "Palm Beach 20%" (the town) is still unlabeled. |
| 7 | "Most don't" scare; hidden reasons | PARTLY | All reasons are now shown and "some closed claims are paperwork" was added, but the "Most don't" headline remains and the 2x-state rate is unexamined (Palm Beach 7). |
| 8 | Hurricane Opal outlier | FIXED | Opal is gone from the event table. A similar outlier, 2025, is now highlighted (Palm Beach 14). |
| 9 | Checker bias | FIXED | Same full-risk caveat in every result. |
| 10 | Full-risk tile, 18/25%, "1 renewal" | FIXED | Same wording as Louisiana; the renewal-count sentence is gone. |
| 11 | 91.5% max coverage had no denominator | PARTLY | Denominator stated; the contradiction with 50.6% is unexplained (Palm Beach 5). |
| 12 | Average includes ICC, total excludes it | PARTLY | Disclosed, but $71,995,287 ÷ 4,681 = $15,380 ≠ $15,396 is still printed side by side. |
| 13 | Aid totals (COVID, wind) | FIXED | COVID removed ($160.9M), "Hurricane aid includes wind damage". |
| 14 | Repeat-flood mislabel | FIXED | Same fix as Louisiana 11. |
| 15 | Four unreconciled counts | PARTLY | Headers fixed; the prose still says "132,945 policies" (Palm Beach 4). |
| 16 | High-risk rows did not add to 41.8% | FIXED | 34.1+4.6+1.9+1.2 = 41.8. New, minor: B and C are called "unclassified". |
| 17 | County totals never verified | NOT FIXED | "matched to FEMA's own count for the state"; "not yet compared for Palm Beach County". |
| 18 | Templated repetition | PARTLY | Same as Louisiana 18. |
| 19 | "Already flooded" omitted the aid rule | FIXED | Rule present (palm-beach-04). |
| 20 | "Low end / High end" | FIXED | "A quarter pay under $517". |
| 21 | Thresholds; VE n=116 with no caution | PARTLY | The methodology now matches, but the VE row still has no small-sample caution. |

**Round-1 tally (48 BLOCKER + MAJOR items): 30 FIXED, 4 NOT FIXED, 14 PARTLY.** All 7 round-1 BLOCKERs are fixed.

Sources: [FEMA NRI — Riverine Flooding](https://hazards.fema.gov/nri/riverine-flooding); [secondary, NRI vintage only, unverified](https://mapscaping.com/nevada-flood-zones/)
