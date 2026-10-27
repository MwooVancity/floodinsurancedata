# Hater review, round 1 (2026-10-26)

Pages: home, /flood-insurance/louisiana/, /flood-insurance/palm-beach-county-fl/. I read the phone screenshots (home-00..05, louisiana-00..23, palm-beach-00..21; the files after those are byte-identical repeats of the page bottom), the built HTML, the agg/data/extras JSON, tools/metrics.py, the methodology page and the about page. I made one web check, on the CRS rule under Risk Rating 2.0 (LA County DPW "What IS Changing Under Risk Rating 2.0"; ASFPM CRS RR2.0 fact sheet, April 2022). I did not read any gate code or review docs.

Severity: BLOCKER = wrong or misleading information a reader could act on. MAJOR = confusing, untrustworthy or broken. MINOR = polish.

---

## Home (dist/index.html)

1. **MAJOR**, home-00: "4.6M INSURED UNITS IN FORCE" sits under the caption "Single-family primary homes, premium plus fees, NFIP policies in force on July 31, 2026." The 4.6M counts every occupancy type (condo units, rentals, businesses): Florida alone is 1,795,894 units, which is all of its policies. The caption covers only the two cost tiles. An analyst would call this a mislabeled denominator.
2. **MAJOR**, home-04/05: the county table has no state names. "Orange County $1,083" is Orange County, **CA** (href orange-county-ca), and an Orlando reader will take it as theirs. "Jefferson County" is TX, "Harrison County" is MS, "St. Louis County" is MO, "Nassau County" and "Suffolk County" are NY, and "Monroe County" is FL. Every one of those names exists in several states.
3. **MAJOR**, home-00: "What flood insurance really costs where you live ... what people near you pay." There are 42 county pages for about 3,000 counties, so almost every reader gets only a state median. Also, "really costs" is a median of existing, often discounted policies. A new buyer is quoted at the full-risk price, and the Louisiana page itself shows the median full-risk premium 42% above the median charged ($1,220 vs $859). The homepage never says these are existing policies, not quotes.
4. **MAJOR** (trust/YMYL), footer links and /about/: no named person or organisation, and no contact ("Corrections: a public contact address is being set up"). For a money/insurance topic this fails a quality rater's "who is responsible" check on its own.
5. **MAJOR**, /about/ (linked from home) contradicts the pages it vouches for:
   - It says "counts are reconciled to FEMA's official policy figure", but every page says "FEMA's official policy count is not yet joined".
   - It says "no estimates, no modelled or private data", but the pages show the National Risk Index (a model) and penetration rates ("the structure count is a FEMA estimate").
6. **MAJOR**, home-00: "matched to FEMA's own count" is the API's own record total, not FEMA's official policies-in-force count. The state pages admit the official count is not joined, so the trust line overclaims.
7. **MAJOR**, the methodology page (linked as "How we check them") contradicts the pages:
   - It says "Suppression: cost charts need ≥100 cohort policies". The pages publish zone medians at 50 or more, parish medians at 30 or more, and ZIP medians at 25 or more.
   - It defines Repetitive-Loss as "FEMA-designated RL/SRL properties", but the pages call the same figure "disaster-aid applications".
   - It lists Census ACS for "the take-up ratio (policies per 100 homes)", but the pages use FEMA penetration rates.
8. **MINOR**, home-00: "51 STATES". The 51st is the District of Columbia.
9. **MINOR**, home-01..05: "Insured units" is never explained, and "Median / yr" does not say single-family primary homes only. A condo owner compares against the wrong cohort.

Counts: 0 BLOCKER, 7 MAJOR, 2 MINOR. **Verdict: FAIL**

---

## Louisiana (dist/flood-insurance/louisiana/index.html)

### BLOCKER
1. **BLOCKER**, louisiana-16/17, CRS table "High-risk zone 35% | Other areas 10%" (also 25/10, 20/10, 15/5). Under Risk Rating 2.0 the CRS discount is set by class and applies equally to every policy in the community, whatever the zone: "a policy in Zone X receives the same discount as a policy in Zone V". The "Other areas" column is the pre-2021 split carried over from the Community Status Book. A Zone X homeowner in Jefferson Parish (43.6% of policies here are Zone X) is told 10% when it is 35%.
2. **BLOCKER**, louisiana-15/16: "Can I pay less than the sticker price? Yes, in 42 of the 353 towns here: up to 35% off in Jefferson Parish." The CRS discount is automatic and already inside every premium and median on this page, including Jefferson's $1,172. Nothing extra is available to the reader. A homeowner will budget "$1,172 minus 35%" or ask an agent for a discount they already get.
3. **BLOCKER**, louisiana-05, claims chart: bar height is the claim **count** (SVG rects scale with claims; Palm Beach proves it, see below). The headline, the orange highlight and the caption are all about **dollars**: "the worst years were 2005, 2016 and 2021 ... Orange bars are the three costliest years". The 1995 bar (38,330 claims, $606M) is drawn taller than the orange 2016 bar (36,026 claims, $2.78B). There is no axis or unit. The reader reads flood severity off a count chart that the caption says is money.

### MAJOR
4. **MAJOR**, louisiana-02, flood-zone table:
   - "51.0% of Louisiana's NFIP policies are in high-risk zones", but the rows marked "(high-risk)" add to 45.8% (39.1 + 5.2 + 1.5).
   - The remaining 5.2 points hide in "Other or unclassified zones 21,239", which holds Zone VE (2,047 units, the coastal high-hazard zone), A01–A30, AH and AO.
   - A V-zone owner looking up "Am I required to carry it?" cannot find their zone, and the table calls their zone "unclassified".
5. **MAJOR**, louisiana-09: "Zone C $1,086 / Zone A99 $1,086 / Zone B $1,086" are three different zones with the identical median, which also equals the state median ($1,086, agg.json policies.p50). This looks like a fallback value, not a measurement, and nothing on the page explains it. Prove it from the records or remove it.
6. **MAJOR**, louisiana-01, "Is my quote or renewal normal here?": the checker compares against existing policies, and 56.6% of those are below full-risk. A new-policy quote is priced at full risk (median full-risk premium $1,220 vs $859 charged), so a fair new quote lands "in the top quarter — more than about 75% of existing policies here". The result messages never say this. A new buyer will think a fair quote is a rip-off.
7. **MAJOR**, louisiana-00 and 15:
   - The hero tile "56.6% PAY UNDER FEMA'S FULL-RISK PRICE" reads as good news to a frightened homeowner. It means those bills are on a yearly increase path.
   - The body says "56.6% of bills here can keep rising", which implies the other 43.4% will not. Full-risk bills also rise with FEMA's yearly rate updates and with the fees and surcharges.
8. **MAJOR**, louisiana-15, "By law most premiums cannot rise more than 18% a year (FloodSmart puts it at 18–25% for most policyholders)":
   - The sentence contradicts itself. 18% is the cap for primary residences, and 25% applies to specific classes (non-primary homes, businesses, severe repetitive loss). "Most" cannot be both.
   - "At least about 3 annual renewals" divides the median premium by the median full-risk premium. Those come from different policies, so the result is not a property of any policy.
9. **MAJOR**, louisiana-00/06, average paid claim:
   - "Average paid claim $55,453" includes ICC payments (metrics.py avg_paid uses netIccPaymentAmount), while "Total paid $20,682,152,359: net building + contents" excludes them. $20.68B ÷ 377,993 paid claims = $54,716, not $55,453, so the page's own numbers do not reconcile.
   - The average mixes nominal 1978–2026 dollars, is dominated by Katrina ($103,300 average), and is then sold as "about 51 years of the typical bill here". That is a promotional ratio, not a finding.
10. **MAJOR**, louisiana-20/21: "Did the government pay homeowners after floods? ... FEMA approved $4.6 billion". Joining data.json housing to declarations by incident type gives:
    - Hurricane $3.76B, mostly wind
    - Flood $738M
    - Severe Ice Storm $5.0M
    - Biological (COVID-19) $2.5M
    - Tornado $2.0M

    "After floods" is false for part of the total. "Not much per household" is then backed by "$2,508 per registration", and a registration is not a household; registrations include people approved for $0.
11. **MAJOR**, louisiana-17/18, repeat-flood block:
    - The source is named "Repetitive-Loss Flood Properties", which an analyst reads as the NFIP RL/SRL list. The text says "disaster-aid applications", and the methodology says "FEMA-designated RL/SRL properties". These are three different things.
    - "6,132 ... records came from homes hit in four or more" is the `srl` field. Severe Repetitive Loss is an NFIP claims definition (4+ claims over $5k, or 2+ exceeding the building value), not "hit four or more times".
    - The lead "Some homes here flood again and again: 85,549" counts records, as the card itself admits.
12. **MAJOR**, louisiana-07, "Why do flood claims here go unpaid?":
    - The three rows shown (49,359) are 46% of the 107,750 unpaid claims.
    - Hidden are "Other" 13,257 (more than the third row shown) and "Assigned in error" 9,979, and 21.7% carry no reason at all.
    - The "top reason" headline is technically true, but the table implies a complete picture.
13. **MAJOR**, louisiana-02/11/19, the word "policies" means four different numbers:
    - The "Policies" column in the zone and parish tables holds insured units (the zone rows add to 407,916 units, not 395,032 records).
    - The homepage calls the same numbers "Insured units".
    - The page also shows 395,032 records, "Residential policies in force 359,013" and 292,018 single-family policies, with no line reconciling them.

    The copy editor and the analyst both catch this.
14. **MAJOR**, louisiana-08: "CARRY THE MAXIMUM BUILDING COVERAGE 64.8%" has no denominator. It could be of all single-family policies, or of the 21.5% whose rebuild cost is over $250k. The reader cannot tell whether underinsurance is common or rare.
15. **MAJOR**, louisiana-03: "Low end $863 · Typical $1,086 · High end $1,273". These are the 25th and 75th percentiles, so a quarter of policies pay less than the "low end" and a quarter pay more than the "high end". The labels disagree with the values.
16. **MAJOR**, louisiana-20: "71 federal disasters ... Distinct storms by calendar year (one storm's ... declarations are counted once)". Yet the list shows "2021 — Hurricane Zeta" (landfall October 28, 2020), and data.json also has "TROPICAL STORM ZETA" in 2020. Zeta is counted twice under two years, and the latest-six list gives the wrong year.
17. **MAJOR**, louisiana-21: "FEMA's official policy count is not yet joined for Louisiana ... Count reconciliation (not a snapshot proof)". The page admits its headline total has never been checked against FEMA's official policies-in-force count, in jargon no homeowner can parse. The About page claims the opposite.
18. **MAJOR** (rater, thin/templated content), louisiana-00/01/04:
    - "Am I required to buy it? Only if your home is in a high-risk zone ..." appears verbatim twice on this page and again on the homepage.
    - "Buy it now: most policies start 30 days after you buy ..." appears twice.
    - "NFIP covers up to $250,000 on the building and $100,000 on contents, which is a separate policy" appears twice.
    - All of these sentences are identical on the county page.
19. **MAJOR**, louisiana-05, "Already flooded? ... FEMA disaster aid is open to people in counties designated ...". It omits the one rule a just-flooded high-risk-zone owner must know: accepting FEMA flood aid there requires buying and keeping flood insurance, or they are ineligible for aid next time.
20. **MAJOR**, louisiana-10/13: "Zones with fewer than 50 priced single-family policies are omitted" and "Parishes with fewer than 30 ...", while the methodology says ≥100. The page also warns "medians from under 100 policies move more", which concedes the rows it does publish are unstable.

### MINOR
21. **MINOR**, louisiana-00: "17th highest of 51 states". DC is not a state.
22. **MINOR**, louisiana-15..17, CRS table names:
    - "42 of the 353 towns": the 353 are NFIP communities, including parishes and unincorporated areas.
    - "Jefferson Parish (Jefferson Parish)" repeats itself.
    - "St. John The Baptist Parish" here, but "St. John the Baptist Parish" in the parish table.
    - "Lafayette City- Parish Consolidated Government" is a raw database string.
23. **MINOR**, source lines that are not dates:
    - "Data effective current Community Status Book"
    - "Data effective FEMA's current list"
    - "Data effective owner registrations by disaster"
24. **MINOR**, louisiana-07/08, event table: averages are rounded inconsistently ("$103,300", "$92,400" vs "$68,576", "$53,042"), and "Mid summer severe storms" drops FEMA's hyphen ("Mid-summer").
25. **MINOR**, louisiana-14: "Average premium only ... the figure many sites quote" is an unsupported claim. The "Average cost, every policy type" row has an empty "What it counts" cell.
26. **MINOR**, louisiana-11..13, parish table:
    - It says parishes under 30 policies "show a dash", but none do; instead "34 smaller parishes are not listed".
    - Webster Parish appears in the "Highest" list but not in the table.
    - Some parish names are links and others are not, with no cue why.
27. **MINOR**, louisiana-09/10: rows A01–A15 and V15 are listed as separate zones. The page never says these are older map labels, so a reader with "A10" on a determination does not know it is an AE-type zone.
28. **MINOR**, louisiana-22: "Other states: Iowa · Kansas · Kentucky · Maine · Maryland · Massachusetts" are alphabetical neighbours. A Louisiana reader wants Mississippi and Texas.
29. **MINOR**: "downloaded October 25, 2026" (top) vs "Last pulled October 26, 2026" (datasets box).
30. **MINOR**, louisiana-19: the tile "ALL HOMES INSURED 22.0%" reads as "all homes are insured".
31. **MINOR**, louisiana-02/05: "Source: govinfo.gov, federalreserve.gov (official pages ...)" names domains, not the exact page.
32. **MINOR**, louisiana-20: "Severe Storms, Tornadoes, And Flooding" has a capital "And". The hero tile "MIDDLE HALF" is jargon for a 30-second reader.

Counts: 3 BLOCKER, 17 MAJOR, 12 MINOR. **Verdict: FAIL**

---

## Palm Beach County, FL (dist/flood-insurance/palm-beach-county-fl/index.html)

### BLOCKER
1. **BLOCKER**, palm-beach-14, flood-risk percentiles:
   - The page says "Inland: expected annual flood loss above about 30% of U.S. counties; FEMA models roughly $178,899,133 of flood loss a year". The percentile is the NRI field `IFLD_ALR_NPCTL` (tools/collect.py), the expected-loss **rate** (loss per dollar of exposed value) percentile, not expected loss.
   - A county with $179M of modeled inland loss a year is near the top nationally; the inland risk score in agg.json is 98.9.
   - The page tells a Palm Beach reader their river and rain flood loss beats only 30% of counties, beside a "Relatively High" tile. The coastal "69%" has the same mislabel.
   - "$7,538,748" is false precision on a model output.
2. **BLOCKER**, palm-beach-12/13, CRS "Other areas 10% / 5%" column: this is the same pre-Risk Rating 2.0 split as Louisiana. A Zone X home in Boynton Beach gets the class-4 30% discount, not 10%, and 57.5% of policies here are Zone X.
3. **BLOCKER**, palm-beach-12: "Can I pay less than the sticker price? Yes ... up to 30% off in Boynton Beach." The discount is automatic and already inside the $670 median and every figure on the page, so the reader is promised a saving that does not exist.
4. **BLOCKER**, palm-beach-05, claims chart:
   - Bar heights are claim counts. SVG: 2004 is 1,926 claims at height 126; 2025 is 99 claims at height 6.5.
   - The orange "three costliest years" include 2025 ($6.86M), which is drawn as the **shortest** bar on the chart. 1979 ($784k) is drawn about 7x taller than 2025.
   - The headline and caption are dollars, and there is no axis. The chart contradicts its own caption.

### MAJOR
5. **MAJOR**, palm-beach-00 vs palm-beach-10, headline vs ZIP table:
   - The headline says "$670 Median / yr ... 32% below the Florida median ... 8th lowest of 55 Florida counties".
   - But 7 of the 8 largest ZIPs in the ZIP table pay $1,145–$1,825 (33480 $1,825, 33483 $1,769, 33432 $1,261). The county median is pulled down by inland Zone X subdivisions.
   - A coastal reader, who is the one most likely to be frightened, is told they live somewhere cheap.
6. **MAJOR**, palm-beach-12/13, CRS names: "Palm Beach County 25%" means unincorporated county only, and "Palm Beach 20%" means the Town of Palm Beach. Neither is labeled. A Palm Beach Gardens owner (listed under "No CRS discount") or anyone in a town will read "Palm Beach County 25%" as countywide.
7. **MAJOR**, palm-beach-06/07, unpaid claims:
   - "Most don't: 56.5% of claims here closed with no payment" will scare a reader out of buying.
   - The unpaid table shows 3 rows (2,701), only 44% of the 6,077. It hides "Other" 1,107 (larger than rows 2 and 3) and "Assigned in error" 432, and 13.1% have no reason.
   - Part of the 56.5% is filing noise, not denied floods, and the page does not say so.
8. **MAJOR**, palm-beach-08: "Hurricane Opal (1995) | 7 | $1.4 million | $193,831". Opal struck the Florida Panhandle. Seven claims averaging 12x the county's $15,396 is almost surely a mis-assigned event or county code, and it is published as fact in a "biggest floods here" table.
9. **MAJOR**, palm-beach-01, quote checker: the same bias as Louisiana item 6. A new full-risk quote is compared against existing policies, 29.5% of which are below full-risk. The effect is smaller here, but the messages never warn about it.
10. **MAJOR**, palm-beach-00/11, full-risk block:
    - The tile "29.5% PAY UNDER FEMA'S FULL-RISK PRICE" and the text "29.5% of bills here can keep rising" imply the rest will not rise.
    - The 18% vs 18–25% contradiction repeats from Louisiana.
    - "Would take at least about 1 annual renewal" to go from $507 to $514 is a 1.4% gap; "at least about" is self-cancelling and the sentence says nothing.
11. **MAJOR**, palm-beach-08: "CARRY THE MAXIMUM BUILDING COVERAGE 91.5%" has no denominator. It cannot be all single-family policies when only 50.6% have a rebuild cost over $250,000, because the rest could not sensibly insure to $250k. The label disagrees with what the number must be.
12. **MAJOR**, palm-beach-01/06, average paid claim:
    - "$15,396" includes ICC, while "Total paid $71,995,287" excludes it: $71,995,287 ÷ 4,681 = $15,380.
    - It mixes nominal 1978–2026 dollars and is pitched as "about 23 years of the typical bill here".
    - The Florida comparison "$61,756" uses the same mixed basis.
13. **MAJOR**, palm-beach-18: "Did the government pay homeowners after floods? ... $161.5 million". By incident type, $160.9M is Hurricane aid (Irma, Matthew and others, overwhelmingly wind) and $579k is Biological (COVID-19). Almost none of it is flood aid. "Not much per household" is then backed by "$593 per registration".
14. **MAJOR**, palm-beach-15: the repeat-flood dataset mislabel is the same as Louisiana item 11 ("Repetitive-Loss Flood Properties" source vs "disaster-aid applications" text vs "RL/SRL" in the methodology). "Some homes here flood again and again: 216 ..." counts records, not homes.
15. **MAJOR**, palm-beach-02/10/17, counts: the page shows four counts with no reconciliation (132,945 units, 75,140 records, "Residential policies in force 69,154", 50,781 single-family). "Policies" headers hold units, while the ZIP table on the same page correctly says "Policy units".
16. **MAJOR**, palm-beach-02, zone table: "41.8% ... in high-risk zones", but the rows marked high-risk add to 40.6%. Zone AH (1,223 units, high-risk) is inside "Other or unclassified zones".
17. **MAJOR**, palm-beach-19: "FEMA's official policy count is not yet joined for Palm Beach County". The record count is checked only at state level ("matched to FEMA's own count for the state"), and claims are assigned by the claims file's county code ("may not exactly match a policy's property county"). The county totals have never been verified.
18. **MAJOR**, palm-beach-00/01/04: templated repetition, the same verbatim blocks as Louisiana item 18, twice on the page and on every page.
19. **MAJOR**, palm-beach-05, "Already flooded?": it omits the flood-insurance purchase requirement that comes with FEMA flood aid (Louisiana item 19).
20. **MAJOR**, palm-beach-03: "Low end $517 · High end $1,034" are the 25th and 75th percentiles mislabeled as ends.
21. **MAJOR**, palm-beach-10/09: the ZIP median is published at 25 or more policies and the zone median at 50 or more, against a methodology that says ≥100. Zone VE ($1,393, n=116), the highest-stakes row, rests on 116 policies with no caution.

### MINOR
22. **MINOR**, palm-beach-14, NRI paragraph: "The rating multiplies expected flood loss by a community factor for social vulnerability and resilience" is analyst jargon in a homeowner card.
23. **MINOR**, palm-beach-10: the ZIPs have no place names. Nobody knows 33480 is the Town of Palm Beach or 33484 is west Delray.
24. **MINOR**, palm-beach-09: Zone AO (high-risk) is $645 against Zone X at $618, with no "why can high-risk cost about the same" note, although the Louisiana page has one.
25. **MINOR**: the same non-date "Data effective ..." lines as Louisiana item 23. "Data effective 1996-2025" uses a hyphen where the other ranges use an en dash.
26. **MINOR**, palm-beach-17: the tile "ALL HOMES INSURED 13.0%" reads as "all homes are insured".
27. **MINOR**: "downloaded October 25, 2026" vs "Last pulled October 26, 2026".
28. **MINOR**, palm-beach-14/15: "$71.1 million" of NWS damage sits two cards from "$72.0 million" of NFIP payouts. The near-identical figures invite a false match, and nothing says they measure different things.

Counts: 4 BLOCKER, 17 MAJOR, 7 MINOR. **Verdict: FAIL**

---

## Classes (likely on every page of the template)

**state + county**
- CRS "Other areas" column is pre-Risk Rating 2.0 (BLOCKER).
- "Can I pay less than the sticker price? Yes" offers a CRS discount that is already in every figure (BLOCKER).
- The claims-per-year chart is drawn as claim counts but captioned and highlighted as dollars (BLOCKER).
- "Low end / High end" labels on the 25th and 75th percentiles.
- "Policies" headers on columns that hold units, plus four unreconciled counts.
- Average paid claim includes ICC but total paid excludes it, the dollars are nominal, and it is pitched as "N years of the typical bill".
- "Did the government pay homeowners after floods?" totals all disaster types (hurricane wind, COVID, ice, tornado) and reports "per registration" as "per household".
- Repeat-flood block: source name, text and methodology disagree, and `srl` is printed as "hit four or more times".
- The unpaid-reasons table shows 3 rows covering about 45%, hiding "Other" and "Assigned in error".
- The zone requirement table sends VE, AH and numbered A zones to "Other or unclassified", so the high-risk rows do not add to the stated share.
- The full-risk tile reads as good news; the 18% vs 18–25% contradiction; "years to full-risk" divides medians of different policies.
- The quote checker benchmarks new full-risk quotes against discounted existing policies.
- "Carry the maximum building coverage" has no denominator.
- "Already flooded" omits the purchase requirement that comes with FEMA aid.
- Verbatim boilerplate (required / how fast / $250k-$100k / homeowners does not cover) appears twice per page and is identical across all pages.
- "Official policy count is not yet joined", written in jargon.
- Suppression thresholds of 25/30/50 vs the methodology's ≥100.
- Non-date "Data effective" lines; the Oct 25 vs Oct 26 date mismatch; "ALL HOMES INSURED" tiles.
- Disaster list: storm year taken from the declaration date, with possible double counts (Zeta).
- CRS community names printed as raw database strings with redundant parentheses.

**county**
- The NRI percentile is the loss-rate percentile labeled as expected loss (BLOCKER on every county page that shows it).
- The headline county median hides ZIP-level spread, misleading wherever coastal ZIPs pay 2–3x.
- Unlabeled "<County name>" CRS rows that cover only unincorporated areas.
- Event-name outliers (Opal-type misassignment) are published unchecked.
- County records are verified only at state level, and claims are assigned by county code.

**state**
- "N of 51 states" counts DC as a state.
- "Other states" links are alphabetical neighbours, not geographic ones.
- Identical zone medians that equal the state median (Zone C/A99/B $1,086); check every state for this pattern.

**home**
- County list without state names.
- "4.6M units" mislabeled as single-family primary homes.
- The "near you / really costs" overclaim.
- No author or contact; About and Methodology contradict the pages.
