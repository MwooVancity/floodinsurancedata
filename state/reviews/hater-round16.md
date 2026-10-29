# Hater round 16 (full read: every screenshot in round16/, built HTML, data JSON spot-checks, Google top results)

Method: all 107 phone screenshots looked at (in 4-up sheets), page text pulled from dist/ HTML, numbers spot-checked
against data/*.json (hero medians, percentiles, share below full-risk, claims paid + unpaid = total, NRI fields,
deductible counts, disaster numbers). Google searched for the five reader queries. I did not crawl links, run the pages
in a browser, measure contrast, or test keyboard use; those are marked "unverified".

Spot-check result: every figure I traced matched its JSON (e.g. LA p50 1086, share_below 56.6, units 407,916; PB
p25/p50/p75/p90 517/670/1034/1297; ME claims 4,154 paid + 1,518 unpaid = 5,672; NE 4,494 + 1,575 = 6,069; ranks
"17th highest" LA, "20th lowest" ME, "12th lowest" NE recount correctly from the home table). The defects below are
about labels, bases and what a newcomer would read into the numbers, not arithmetic.

Google top results (what #1-#3 give):
- "flood insurance cost": NerdWallet ($899/yr, $75/mo), Bankrate, Kiplinger ($888). One average, state table, buy steps, quotes.
- "flood insurance cost Louisiana": MoneyGeek ($750 avg, parish table incl. "Plaquemines $4,752"), Insurify ($1,470 median SF), Policygenius, Bankrate ("not required if you own outright").
- "...palm beach county FL": NerdWallet FL guide (county $528, city rows: West Palm $349), MoneyGeek ($466), Miami Herald ZIP increases (33469 +342%).
- "...Maine": MoneyGeek, Jerry, Press Herald (county averages), WABI ("only 1% of Maine households have flood insurance"), FEMA Maine state profile PDF.
- "...Nebraska": MoneyGeek ($1,061), StateCalc (FEMA-data median $744 of recent policies), WOWT on Risk Rating 2.0.

Our information gain (none of the top 3 has it): full-record medians with the middle-half range, share below full-risk,
claim pay rate and unpaid reasons, named-flood payouts, rebuild-limit shortfall, CRS discount by town, non-NFIP towns,
ZIP lookup. Most of it is on screen 1 as a link list, not as answers; the payout answer is on screen 1.

## home

1. **MAJOR** Quote checker compares a quote with existing policies. "Is my quote normal? Type your yearly cost... to see where it sits among U.S. single-family policies"; result line: "$X is in the top quarter of U.S. single-family policies (half pay $713 to $1,309)". A quote is a new policy, priced at full risk; the distribution is existing policies, many still discounted below full risk. A buyer with a normal full-risk quote is told it is high and may walk away or shop for nothing. The result line never mentions the $995 new-policy figure the hero already has.
2. **MAJOR** "Built from 3,490,299 NFIP policy records" next to the hero card "4.6M INSURED UNITS IN FORCE" (home-00). To a newcomer, 3.5M records next to 4.6M units looks like a contradiction. The explanation ("condo-association records carry more than one unit") is only on state pages, in "Are these counts complete?".
3. **GAP** No buying step anywhere on home: no NFIP phone (877) 336-2627, no FloodSmart link, no 30-day/60-day deadline line beyond "30 days". NerdWallet and Bankrate give "how to buy" on the page. The only next step is "Check your zone on FEMA's flood map".
4. **MINOR** "County pages: 52 counties so far, listed by number of policies", but the column is "Insured units" and the sort is by units (home-01). Policies and units mean different things.
5. **MINOR** "In Florida, Citizens homes with wind cover need it..." in the national "Am I required" answer. "Citizens" is never expanded on home (it is Citizens Property Insurance Corp.). Readers outside Florida have to read it to learn it does not apply to them.
6. **MINOR** "Lowest: Maryland $568, District of Columbia $384, Alaska $368": this reads in descending order under a "lowest" label. "Lowest: Alaska $368, DC $384, Maryland $568" reads correctly.
7. **MINOR** Hero layout: the third stat card (4.6M) sits alone on a second row, half width, with empty space beside it (home-00).
8. **MINOR** Footer and note text is 11.5-14px (inline styles `font-size:11.5px`, `13px`, `14px`), below the 16px line G asks for. The definitions under the hero, which matter most, are at about 13px.
9. **GAP** No Spanish (L, OPEN); no error-report route (I, OPEN); no print stylesheet (K, OPEN).
10. **GAP** NerdWallet/Bankrate show a "cheapest/most expensive" narrative and private-market context; we say only "Private flood insurance is not in this data". That is acceptable per the brief. Noted, not counted.

Checklist A-N (home):
- A: defect. How much, required and how fast are on screen 1; "does it pay out" is not on home at all; there is no buying next step (item 3).
- B: GAP. Only buyer and lender cases are addressed; renter, condo, business, just-flooded and map-change have no line on home.
- C: PASS for figures; defect in base wording (items 2, 4).
- D: defect (items 2, 4: records vs units vs policies).
- E: PASS mostly; "Citizens homes with wind cover" (item 5).
- F: GAP (item 3); local contacts OPEN.
- G: defect (item 8). No sideways scroll (PASS in home-00..08). Search box, inputmode=numeric (PASS).
- H: PASS (lang=en, h1 then h2, aria-labels on both inputs). No visible label, only placeholder + aria-label (MINOR). Keyboard unverified.
- I: PASS for methodology/sources/no-FEMA-endorsement line. /about/ never says "anonymous" in the body (see Classes). Error report OPEN.
- J: PASS (search with a #nomatch message, state and county links). No 404.html in dist/ (see Classes).
- K: PASS (23.8 KB HTML). JS errors unverified. Print OPEN.
- L: GAP (OPEN). M: PASS ("on July 31, 2026" stated). N: PASS against state pages (medians match the home table).

Verdict: FAIL

## louisiana

1. **MAJOR** Quote checker compares against existing, partly discounted policies (56.6% below full risk here). A buyer typing a full-risk quote near $1,466 ("Full-risk premium plus average fees") is told "in the top quarter, more than about 75% of existing policies here". The result line then appends "Renewing? Policies whose term began in 2026 typically pay $1,215", never the buyer figure $1,139. A reader acts on this line.
2. **MAJOR** "Renewing? Policies whose term began in 2026 typically pay $1,215" (hero, louisiana-00; also the checker output). Policies whose term began in 2026 include the 30,754 first bought in the past year, so this is not a renewal figure. The 2025-term vs 2026-term rows ($1,080 vs $1,215) also cover different calendar months of the same snapshot, which a reader will take as "renewals jumped 12%".
3. **MAJOR** Hero "Does it pay out here? 77.8% of claims here paid something; the average paid claim was $55,453" has no caveat next to it. The $55,453 mixes 1978-2026 nominal dollars, includes ICC pay, and is pulled up by Katrina's $103,300 average. The caveats ("Dollars are as paid at the time", "Some closed claims are paperwork") sit several screens down. Checklist C says each caveat sits beside its figure.
4. **MAJOR** Codes with no plain words in the zone table, zone cost table and checker dropdown: "Zone C", "Zone B" (old labels for low/moderate risk, shown with no "(low-risk)" tag, while every A/V row gets "(high-risk)"), "Zone A99", "Zone AHB", "Zone V15", "A01...A15" (louisiana-00, -03). A newcomer whose letter says "Zone B" cannot tell from the page whether that is good or bad. "CRS class" (column in the discount table) is never explained (lower = bigger discount). The dropdown lists 25 zones in count order (X, AE, A, C, A99, B, A10, A01...), not a findable order.
5. **MAJOR** Hero card "56.6% PAY LESS THAN FEMA'S FULL-RISK PRICE, SO THEIR BILLS RISE EACH YEAR" (louisiana-00). It is screen 1's fourth big number, and "full-risk price" is not defined there. A frightened reader reads "bills rise each year" as "mine will rise", which E rules out as alarm. The defining sentence and the 18% cap are 12 cards down.
6. **MINOR** "Already flooded? What to do now, and what FEMA aid covers." links to #covered, which says only that aid "is open to people in counties designated in a federally declared disaster". What aid covers is in a different card ("Did FEMA aid homeowners...").
7. **MINOR** "Among the five costliest years, these have no named flood in this table: 1995", while the same table has the row "Flooding (1978–1998): FEMA's records use this name for claims in several years", whose span covers 1995. These two lines read as a contradiction.
8. **MINOR** "Other low-risk or unclassified zones | 6 | 0.0%": a non-zero count shown as 0.0%. Use "<0.1%".
9. **MINOR** Parish table column "Below full-risk" is never defined in the table or its caption (louisiana-03).
10. **MINOR** "Not in the NFIP (34 communities here): Athens; Atlanta; ..." gives no parish for each town (Atlanta, LA vs Atlanta, GA confusion). The CRS table does name parishes.
11. **MINOR** "Condo owners: ...The single-family figures above leave both out": "both" has no second item (round 15 minor, NOT FIXED).
12. **MINOR** NFIP phone "(877) 336-2627" is plain text, not a tap-to-call `tel:` link, on a phone-first page (F: "linked and working").
13. **MINOR** "70 federal disasters for floods or storms here": a naive recount from data.json declarations (flood, hurricane, tropical storm, coastal storm, plus severe storms whose title names flooding) gives 81. The page's de-duplication rule (EM+DR pairs?) is not stated on the card. Unverified which is right.
14. **GAP** The 64-row parish table has no search or filter; only the county page has a lookup (G: long tables searchable). There is also no back-to-top link on a 27-screen page (G).
15. **GAP** Data already held but not shown: residential take-up (penetration 22.0% overall, 73.1% in high-risk zones, data.json) and the share of claims from outside high-risk zones (21.4%, claims_extra.outside_sfha_pct). WABI ranks for "only 1% of Maine households"; this is the same reader question. These were cut earlier as "take-up"; the cut should be revisited.
16. **GAP** No Spanish (L, OPEN). No state insurance department or floodplain office contact (F, OPEN). Renter, landlord/second home and business readers get no line (B).
17. **GAP** MoneyGeek has a parish table with averages; ours is better (medians, n, claims). We have no "how to buy from a private insurer" line.

Checklist A-N (louisiana):
- A: defect. All five answers are on screen 1, but the next steps (buy phone, deadline) are behind links, and the payout answer carries no caveat (item 3).
- B: GAP. Buyer, renewal (mislabelled, item 2), just flooded, condo line, non-NFIP towns and map change (one-day wait) are served; renter, landlord, second home and business are not.
- C: defect (items 2, 3, 7).
- D: defect (item 4 codes; item 8 rounding; "policy units" vs "priced policies" vs "policies" across tables).
- E: defect (item 5 alarm; "HFIAA surcharge", "reserve fund assessment" not explained in plain words).
- F: PASS for content: phone, FloodSmart, start-a-claim link, 30-day wait, 60-day proof of loss. Phone is not tappable (item 12). Local contacts OPEN.
- G: defect. Note text 11.5-14px; no search on the 64-row table; no back-to-top. No sideways scroll seen (PASS); the yearly chart has no bar labels beyond the three orange years, and its text equivalent is only an aria-label ("NFIP claim dollars paid per year"), not the yearly values.
- H: PASS: lang, h1 then 21 h2s, svg role=img + aria-label. Defect: the checker aria-label says "Your annual premium in dollars" while the instruction says "premium plus fees". No visible labels. Keyboard unverified.
- I: PASS: source line on every card with dates, methodology links, "Not endorsed by FEMA". Error report OPEN.
- J: PASS: breadcrumb, parish pages linked, neighboring states. Site search is on home only; no 404 page (Classes).
- K: PASS (102 KB). Print OPEN.
- L: GAP (OPEN). M: PASS ("policies as of July 31, 2026", "downloaded October 25, 2026").
- N: defect. "Assigned in error" here vs "Claim deleted in error" on Nebraska; the SRL row appears only when it is non-zero.

Verdict: FAIL

## palm-beach-county-fl

1. **MAJOR** Hero "Does it pay out here? 43.5% of claims here paid something (Florida: 69.9%)... Claims filed for losses in the 2020s: 34.7% paid something" (palm-beach-county-fl-00). A homeowner reads "flood insurance here mostly does not pay" and may skip buying. 3,376 of the 6,077 unpaid claims are "Other", "Assigned in error" or "Smaller reasons, or none recorded", and "Some closed claims are paperwork, not a denied flood" sits two cards down. The caveat must sit beside the hero figure.
2. **MAJOR** "How much flood risk is here? Relatively High for coastal flooding and Relatively High for inland (river) flooding", then "inland flood loss here is higher than in about 30% of U.S. counties" (palm-beach-county-fl-04). "Relatively High" next to "higher than only 30%" contradicts itself for a newcomer. It is also two different measures: the rating is from NRI risk_score 98.9 (which weighs social vulnerability), the 30% is an EAL-rate percentile, and inland EAL is $178.9M vs coastal $7.5M. The sentence "it can differ from the loss percentile below" points "below" at text in the same paragraph.
3. **MAJOR** Quote checker compares a new quote with existing policies (same as LA item 1). The output appends "Renewing? ... $679", not the $620 buyer figure.
4. **MAJOR** "Renewing? Policies whose term began in 2026 typically pay $679" includes new buyers (same as LA item 2).
5. **MAJOR** Hero card "29.5% PAY LESS THAN FEMA'S FULL-RISK PRICE, SO THEIR BILLS RISE EACH YEAR", while median premium $507 vs full-risk $514 is a 1% gap here. "Bills rise each year" overstates what is a near-zero gap for most readers in this county.
6. **MAJOR** Zone codes "Zone C", "Zone B", "Zone AO", "Zone AH", "AOB" have no plain words (round 15 minor "zones B and C unexplained", NOT FIXED, now judged by a newcomer). "Zone C $544" is the cheapest row and is not marked low-risk. "CRS class" is unexplained.
7. **MINOR** ZIP rows are inconsistent: "33437" and "33446", "33428", "33467" and the hero "$450 (33484)" have no place name, while "33480 Palm Beach" and "33458 Jupiter" do. A reader cannot tell which town 33484 (Delray Beach) is.
8. **MINOR** "Built from all 75,140 in-force NFIP policy records... downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing." is a comma splice and hard to parse.
9. **MINOR** Hero "Am I required" carries the full Citizens paragraph; "Citizens homes with wind cover" is undefined until the card below.
10. **MINOR** "Bordering and other counties: Broward · Miami-Dade · Lee · Pinellas · Collier · Hillsborough": only Broward borders Palm Beach. Martin, Hendry, Glades and Okeechobee have no pages.
11. **MINOR** Dangling "leave both out" (condo-building share is 0) (round 15 minor, NOT FIXED).
12. **MINOR** "Flooding (1979–2000)" row vs "these have no named flood: 2025, 1995, 2014": the 1995 overlap is the same contradiction as LA item 7.
13. **MINOR** The phone number is not a tel: link.
14. **GAP** City-level costs (NerdWallet lists West Palm Beach $349): our ZIP lookup covers this, but town names are missing on most ZIPs (item 7).
15. **GAP** The Miami Herald/Sun-Sentinel rank with "rates will double/triple near the coast" (Risk Rating 2.0 glide path by ZIP). We have share below full-risk only at county level, not by ZIP.
16. **GAP** Take-up held but not shown (penetration 13.0% overall, 43.4% in high-risk zones). No Spanish (L, OPEN, FL). No county floodplain office contact (F, OPEN).

Checklist A-N (palm-beach-county-fl):
- A: defect (item 1 payout without caveat). Answers otherwise on screen 1 with the map button; the buy step is behind a link.
- B: GAP: renter, business, landlord. Citizens/lender cases are well served (PASS).
- C: defect (items 1, 2, 4, 5).
- D: defect (items 2, 6, 7).
- E: defect (item 5; NRI paragraph is a 120-word sentence chain).
- F: PASS content (phone, FloodSmart, claim link, 60 days). Not tappable. Local contacts OPEN.
- G: PASS for ZIP lookup (inputmode numeric, 5-digit, 18px) and no sideways scroll. Defect: note text under 16px. No back-to-top.
- H: PASS (lang, headings, aria-labels). Checker aria-label "annual premium" vs "premium plus fees".
- I: PASS (sources with dates per card).
- J: PASS (breadcrumb Florida, state link, all places). Bordering list mislabelled (item 10). No 404 (Classes).
- K: PASS (80 KB). L: GAP (OPEN, FL). M: PASS.
- N: PASS mostly. The payout card heading opens with the unpaid share here ("56.5% of claims here closed with no payment") but with "Most do" on states; it is data-driven, acceptable.

Verdict: FAIL

## maine

1. **MAJOR** "Which floods paid out the biggest totals here? The costliest flood FEMA named here was Flooding (1987): $10.0 million" (maine-02), while the yearly chart's costliest year is 2024 at $29.3 million (744 claims, the January 2024 coastal storms), almost three times as much. "Flooding" is not a flood name, and a Maine reader comes away thinking 1987 was the worst. The disclaimer "these have no named flood in this table: 2024" is in small print below. True but misleading.
2. **MAJOR** Disaster list: "2024 — Severe Storms and Flooding / 2024 — Severe Storm and Flooding / 2023 — Severe Storm and Flooding / 2023 — Severe Storm and Flooding / 2023 — Severe Storm and Flooding" (maine-04). These are DR-4764, 4754, 4737, 4736 and 4719 in data.json, distinct disasters, but with no month, number or county they read as a duplicated-row bug.
3. **MAJOR** Quote checker and "Renewing?" mislabel (class; see LA items 1-2).
4. **MAJOR** Hero card "48.0% PAY LESS THAN FEMA'S FULL-RISK PRICE, SO THEIR BILLS RISE EACH YEAR" (class, LA item 5).
5. **MAJOR** "Zone C" (3.4% of units; median $1,018, above Zone A's $866) has no plain words, so a reader may think C is a risk class above A. The A02/V02 labels and "CRS class" are unexplained.
6. **MINOR** "Only some: 15 of the 991 NFIP communities here get one": 991 participating communities is far above Maine's roughly 490 towns, cities and plantations (CSB rows include unorganized townships). Readers will doubt it. Say what a "community" is.
7. **MINOR** "The 15 largest discounts of 15 discounted communities are shown": template text. It should say "All 15 discounted communities are shown".
8. **MINOR** The "Not in the NFIP" list has no county per town, and includes "Penobscot Indian Nation" and islands ("Two Bush Island", "Wheaton Island") with no context.
9. **MINOR** The 2023 claim year shows $8.2M while "December Nor'easter (2023)" alone is $7.5M across 145 claims. That is consistent, but the 2024 bar plus the named Dec 2023 storm split one storm season across two cards with no sentence joining them.
10. **MINOR** JSON-LD temporalCoverage "1978/2025", while the hero and other cards run to 2026 (policies as of July 31, 2026). The claim sources say 1978–2025, which is right, but the Dataset claims less than the page shows.
11. **GAP** "Only 1% of Maine households have flood insurance" (WABI, ranking #6) answers "do my neighbours carry it?". We hold 1.2% overall and 78.5% in high-risk zones (data.json penetration) and do not show it.
12. **GAP** Press Herald gives county averages; ours exist (PASS). The FEMA Maine state profile PDF has the official NFIP state figures; we do not link it.
13. **GAP** No back-to-top; no state floodplain office (Maine Floodplain Management Program) contact (F, OPEN).

Checklist A-N (maine):
- A: defect (class: buy step behind a link; payout figure without its caveat). Answers are on screen 1.
- B: GAP (renter, business, second home; Maine has many second homes, the 25% cap line is the only mention).
- C: defect (item 1; item 10).
- D: defect (items 5, 6).
- E: defect (item 4 alarm).
- F: PASS content; not tappable; local OPEN.
- G: defect (small note text; no back-to-top). The 16-row county table is short enough (PASS).
- H: PASS (as LA).
- I: PASS.
- J: PASS (breadcrumb, neighbouring state NH). No county pages exist for Maine, so the county table has no links (acceptable).
- K: PASS (73 KB). L: n/a for ME. M: PASS.
- N: defect. Item 2 format; the SRL row is missing here (srl = 0) while LA and NE show it. Say "0 records flagged SRL" rather than hiding the row.

Verdict: FAIL

## nebraska

1. **MAJOR** Disaster list repeats "2024 — Severe Storms, Straight-Line Winds, Tornadoes, and Flooding" three times (nebraska-05; DR-4838, 4822, 4808). It reads as a bug (class, Maine item 2).
2. **MAJOR** Quote checker and "Renewing? Policies whose term began in 2026 typically pay $931" (class). Here 2025-term $854 vs 2026-term $931 reads as a 9% renewal jump.
3. **MAJOR** Hero card "35.7% ... SO THEIR BILLS RISE EACH YEAR" (class).
4. **MAJOR** County table: "Keith County | 47 | — | —" and "Knox County | 76 | — | —" sit beside "Custer County | 44 | $695" and "Kearney County | 41 | $870" (nebraska-03). The dash rule counts "priced single-family policies", a column the table does not show, while the visible column is "Policy units". A newcomer sees 76 policies with no price next to 41 with one. Show the priced count, or base the dash on the shown column.
5. **MAJOR** "Not in the NFIP (96 communities here): ... Box Butte County; ..." while the county table lists "Box Butte County | 5" policy units (nebraska-01, -03). A Box Butte reader is told no one can buy NFIP, then sees 5 policies. The note "A community named for the county covers its unincorporated area only" exists only in the CRS card, not beside this list.
6. **MINOR** Hero "Claims filed for losses in the 2020s: 57.5% paid something" rests on 127 claims; the n is not shown on screen 1.
7. **MINOR** 50 of 78 county rows are dashes: a thin wall of "— —" for a reader in a small county. Collapse rows under 30 into one line "Counties with too few priced policies: ..." with their unit counts.
8. **MINOR** "Claim deleted in error" here vs "Assigned in error" on other pages: same code family, two labels (N).
9. **MINOR** "Flooding (1984–1990) ... $434,455" sits next to "these have no named flood in this table: 2010, 1984": the 1984 overlap again (class).
10. **MINOR** "From about $752 a year (Zone AH) to $976 (Zone X)": the explanation box is present (PASS), but the lead sentence still invites "high-risk is cheaper, so I don't need to worry". Lead with "Zone makes little difference to price here".
11. **GAP** The 78-row county table has no search (G). No back-to-top.
12. **GAP** StateCalc gives "median of the 1,000 most-recent real NFIP policies" ($744), a buyer-oriented figure; our $874 first-bought-in-past-year figure is better sourced but sits in the hero only as a "Buying?" line.
13. **GAP** Take-up (0.7% overall, 15.3% in high-risk zones) and claims outside high-risk zones (21.3%) are held but not shown. Answering "most homes in the floodplain here are uninsured" is a strong information gain.

Checklist A-N (nebraska):
- A: defect (class).
- B: GAP (renter, farm/business, second home).
- C: defect (items 2, 5).
- D: defect (items 4, 5).
- E: defect (item 3).
- F: PASS content; not tappable; local OPEN.
- G: defect (no table search on 78 rows, small note text, no back-to-top).
- H: PASS (as LA).
- I: PASS.
- J: PASS (breadcrumb, six neighbouring states). No Nebraska county pages, so the table is unlinked.
- K: PASS (91 KB). L: n/a. M: PASS ("declarations through 2026", July 31, 2026 as-of).
- N: defect (item 8; disaster list format).

Verdict: FAIL

## Classes

Template-wide (state and county; home where noted):
- **Quote checker basis** (home, state, county): it compares a reader's quote with existing, partly discounted policies, and the result line never cites the "first bought in the past year" figure. Fix once in the checker: add "New policies here typically pay $X" to every result, or compare with the new-policy distribution.
- **"Renewing?" label** (state, county; also inside the checker output): it labels term-start-year cohorts that include new buyers. Rename to "Policies that started or renewed in 2026" and drop the renewal claim.
- **"so their bills rise each year"** on the hero card (state, county): undefined "full-risk price" plus alarm on screen 1. Define it in the card ("FEMA's own price for the risk; discounted bills step up toward it, by law at most 18% a year for a main home").
- **Hero payout line without its caveat** (state, county): put "some unpaid claims are paperwork or opened in error" and "dollars as paid at the time" on the same line.
- **Zone codes without plain words** (state, county, dropdown): tag every row high-risk / moderate-low (B, C, X) / old map label, and sort the dropdown by zone family. Explain "CRS class" (1 is best, 10 none).
- **Disaster list without month/number** (state, county): add the month or DR number so same-title disasters are distinct.
- **"Flooding (yyyy–yyyy)" generic row vs "no named flood: <year in that span>"** (state, county): one sentence contradicts the other. Treat the generic "Flooding" name as unnamed in both places. Also, when the costliest year exceeds the costliest named flood, lead with the year (Maine).
- **Dash rule on a column not shown** (state county tables).
- **Not-in-NFIP county names** without "unincorporated area only" beside the list (state).
- **Dangling "leave both out"** when the condo-building share is 0 (state, county).
- **Phone not tap-to-call** (state, county); no back-to-top; no search on long state tables.
- **Note text 11.5-14px** below the 16px line (all templates).
- **Checker aria-label** "annual premium" vs instruction "premium plus fees" (state, county).
- **No 404 page**: dist/ has no 404.html (J). Cloudflare will serve its default.
- **/about/ never says "anonymous" in the body** (I says plainly who runs it: anonymous, by choice). The meta description promises "Who runs Flood Insurance Data" and the body does not answer it.
- **Held data not shown**: residential take-up and the share of claims outside high-risk zones (GAP; ranked first among gaps because competitors rank on exactly this fact).

## Previous items (hater-round15.md)

Round 15 recorded no BLOCKER and no MAJOR, so there is nothing to mark FIXED / NOT FIXED / PARTLY at those levels.
Its MINORs, for the record:
- dangling "leave both out" (louisiana, palm-beach, broward): NOT FIXED (still in louisiana and palm-beach-county-fl text).
- obscure legacy zones in the dropdown with no gloss (louisiana): NOT FIXED. Re-graded MAJOR this round under the newcomer test (checklist D).
- zones B and C unexplained (palm-beach): NOT FIXED. Re-graded MAJOR (same reason).

Tally: 0 BLOCKER/MAJOR carried over; 3 of 3 earlier MINORs NOT FIXED (2 now graded MAJOR).
