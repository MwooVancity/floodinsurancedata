# Hater round 11 (built dist/ pages + 142 phone screenshots in round11/)

**Method.**
- I extracted the visible text, JSON-LD and inline scripts of all 7 built pages, plus methodology and about.
- I recomputed by hand:
  - the home averages table from the 51 state `extras.json` files (sf mean $1,251.54, premium mean $999.66, all-type mean $1,623.93, new-policy n 197,562), and the U.S. medians from `data/us/cost_hist*.json` ($1,055, new $995);
  - every "% above/below" and rank line on screen 1 (all correct);
  - the non-NFIP counts from `data.json` crs `participatingInNFIP` (LA 34 False, OK 122 False; all 4 counties 0);
  - disaster counts from `data.json` declarations: distinct `disasterNumber` against the page count, and which distinct DR numbers the page folds together;
  - event-table headlines against each page's own yearly chart (`extras.claims.events`, `claims.by_year`);
  - ZIP unit totals against county units.
- I read `tools/metrics.py`, `tools/rules_registry.py`, and the declarations/CRS block of `tools/build_page.py` (lines 72-110, page-building code, not gate code), to find why the disaster counts were off.
- I looked at all 142 screenshots as 6-up sheets.
- I ran 2 WebSearches: Oklahoma and Montgomery County TX. For the other five pages I relied on round 10's SERP notes; their queries were not re-run.

**Not done:** I did not run the checkers in a browser; their outputs are computed from the scripts. Rules were not re-fetched from their sources.

**Quote checker at the page median** (from each page's `P` and `R`). Every state and county page prints "$<median> is the typical cost here (half pay $<p25> to $<p75>, typical $<median>). Renewing? Policies whose term began in 2026 typically pay $<x>.":
- louisiana: $1,086 / $863–$1,273 / renewing $1,215
- palm-beach-county-fl: $670 / $517–$1,034 / $679
- orange-county-ca: $1,083 / $854–$1,265 / $1,226
- atlantic-county-nj: $1,246 / $918–$1,691 / $1,299
- montgomery-county-tx: $1,001 / $707–$1,225 / $1,003
- oklahoma: $1,047 / $720–$1,290 / $1,081

All are correct against the data files.

**Changes since round 10, verified:**
- **NOAA storm card, premium-trend card, state "dropping insurance" card, risk tile map, outside-the-zone note and take-up cards: REMOVED.** None appears in any page's text or screenshots, and no page lists NOAA or Census among its datasets. The methodology still describes tile maps (MINOR, see Classes).
- **Events table states its 20-claim floor and names the catch-all rows: VERIFIED.** The "filed under a general label" reason is gone from the footnote.
- **Disaster list says only the latest are shown: VERIFIED.** But the count and list now carry a new defect (MAJOR, see Classes).
- **ZIP+4 records count toward their ZIP: VERIFIED.** `by_zip` units sum to county units on all 4 counties. The leading-zero ZIP "8037" (Atlantic, 1 unit) is still dropped from the lookup.
- **"Not in the NFIP" line: counts VERIFIED, wording VERIFIED** against `nfip_not_sold` (FloodSmart eligibility page and FEMA glossary). It appears only where the count is above 0 (LA, OK), which is correct. **It does not name the communities**, though the brief says it does: it prints only "(34 communities here)" / "(122 communities here)".
- **Home averages table: VERIFIED** (figures above).
- **Methodology and about list only datasets shown: PARTLY.** The source list is now 7 datasets plus the PIF workbook. But the methodology still describes "a tile map shows the worse of the two" and "Tile maps name the two highest ratings". It also calls the PIF workbook a "reconciliation benchmark" while About says "FEMA's separate official policy count is not yet compared".

---

## home

- **MINOR** (meta description). The description says "...and what floods have paid out". The home page has no payout figure (home-00..08); the payouts are only on state pages.
- **MINOR** (carried, NOT FIXED; home-06): "52 counties so far, listed by number of policies". The column and the sort are "Insured units".
- **MINOR** (carried): the home checker's wording differs from the state and county checkers. There are no `data-p` tags on home (I verified its figures by hand: all correct).
- **MINOR** (carried): the Florida Citizens sentence sits in the middle of the national "Am I required" answer.
- **GAP 1.** NerdWallet, Policygenius and Insurify headline figures are not named in "Why do sites quote different prices?" (round-10 SERP).
- **GAP 2.** No cost by flood zone nationally.
- **GAP 3.** No private-flood acceptance rule.
- **GAP 4.** No territories (PR, USVI).
- **GAP 5.** No JSON-LD.

**SEO:** I did not re-run the search; round 10 found title, H1 and screen 1 answer "flood insurance cost" outright ($1,055, $88/month) faster than #1.

**Screenshot skim:** nothing wrong. The state table has 51 rows, the county table 52.

Verdict: PASS

## louisiana

- **MAJOR** (disaster count and list; louisiana-22). "67 federal disasters for floods or storms here".
  - **What the code does:** `event_key` folds any declarations with the same title within one calendar year into one "storm" (`build_page.py` 92-107). That rule was meant for EM+DR pairs of one named storm. With generic titles it also merges separate major disasters. Louisiana has 8 such DR-into-DR merges, among them:
    - DR-4263 (March 2016 floods) and DR-4277 (the August 2016 Great Flood, $652M of homeowner aid, the state's 3rd-largest) are folded into DR-4228 (July 2015), all titled "SEVERE STORMS AND FLOODING";
    - DR-556/565/604/616/622 (1978-80) are folded in the same way.
  - **Why it is wrong:** two DR numbers are always two separate disasters. The count understates them. The methodology promises "one storm's emergency and major-disaster declarations are counted once", which is not what the code does.
  - **Why the reader is hurt:** the 2016 Great Flood, the event every Louisiana reader remembers, is not counted as its own disaster.
- **MINOR** (carried, NOT FIXED): "Among the five costliest years, these have no named flood in this table: 1995". The plural subject "these have" governs one year.
- **MINOR**: event-table averages are rounded inconsistently: "$103,300", "$92,400" against "$68,576", "$53,042".
- **MINOR** (carried): checker aria-label "Your annual premium" while the prompt asks for premium plus fees; the "Renewing?" pool includes new 2026 buyers; `dateModified` 2026-10-25 while the page says newest download October 26.
- **GAP 1.** The "Not in the NFIP (34 communities here)" line does not name them (Vienna, Creola, Shongaloo, Atlanta and the rest), so a reader in one of those villages cannot tell that it applies to them. The brief says the line names them; it does not.
- **GAP 2.** No "years to reach full risk at 18% a year".
- **GAP 3.** No parish jump link on screen 1.
- **GAP 4.** Insurify's Plaquemines figure is not reconciled with ours.
- **GAP 5.** Private flood.

**SEO:** I did not re-run the search; round 10 found the first screen beats MoneyGeek, Bankrate and Insurify. No doorway look: the parish and event tables are unique.

**Screenshot skim:** the orange bars (2005, 2016, 2021) match the text; the CRS table is labelled as the top 15 of 42. Nothing else is wrong.

Verdict: FAIL

## palm-beach-county-fl

- **MINOR** (carried, NOT FIXED; palm-beach-county-fl-12): ZIPs 33437 and 33446 show no town; 33428 shows "Watergate", a CDP that readers know as Boca Raton.
- **MINOR** (carried, NOT FIXED): the ZIP lookup prints `d.u+" policy units"`, so a ZIP with one unit reads "1 policy units".
- **MINOR** (carried, NOT FIXED; -00): comma splice, "downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing."
- **MINOR**: the 20-claim floor drops Hurricane Opal (1995, $1.36M, 7 claims) while Wilma ($1.1M, 81 claims) is shown. This is now stated ("only floods with 20 or more paid claims"), so it is no longer false.
- **MINOR** (class): rcv_80 omits the under-80% settlement; no 44 CFR 61.11(c); the "Renewing?" pool; `dateModified`.
- **GAP 1.** NerdWallet, MoneyGeek and Insurify county figures are not reconciled with ours.
- **GAP 2.** No ZIP-level full-risk gap.
- **GAP 3.** Private flood and Citizens' acceptance of it.
- **GAP 4.** No cost by municipality.
- **GAP 5.** The community names in the "Not in NFIP" line do not apply here (all 40 participate); nothing is missing.

**Checks:**
- The disaster count of 22 has no DR-into-DR merges.
- Frances ($11.3M) does out-pay every unnamed year (2025 $6.86M), so "costliest single flood" holds.
- The "Am I required" card correctly carries no non-NFIP line.

**SEO:** I did not re-run the search. Round 10: screen 1 wins against statewide pages, and the ZIP table is information gain.

**Screenshot skim:** nothing wrong or misleading.

Verdict: PASS

## orange-county-ca

- **MAJOR** (events headline contradicts the page; orange-county-ca-06/07).
  - **The text:** "The costliest single flood here was Pineapple Express Southern (1998): $2.2 million across 314 NFIP flood claims."
  - **The page's own chart:** 1997 paid $3,194,090 and 1995 paid $2,613,484, both before ICC. The footnote says those years have no named flood in this table (they sit under the "Flooding (1978–1997)" catch-all). The 1997 dollars come mainly from the December 1997 storm, and the January/March 1995 storms (DR-1044/1046) are each a single flood.
  - **Why it is wrong:** the headline states as fact something the data shows is not established. It should say "costliest named flood".
- **MAJOR** (escalated from round-10 MINOR, NOT FIXED; orange-county-ca-17). "Do the same homes flood again here? Not in FEMA's records: no disaster-aid applications here came from homes that flooded more than once. 0."
  - **Why it is wrong:** the dataset covers only Individual Assistance registrants since 2002. Here, homeowner aid comes from one disaster (DR-1577, $464,857). The same page shows 3,839 NFIP claims over ~49 years on 9,496 units.
  - **Why the reader is hurt:** "Not in FEMA's records" reads as "homes here do not re-flood". A reader would act on that.
  - **Fix:** "No repeat-flood records in FEMA's disaster-aid list (since 2002); NFIP repeat claims are not in this dataset."
- **MINOR**: "Most do: 53.1% of claims here paid something". "Most" for 53% is true but thin.
- **MINOR**: "FEMA approved $464,857 for homeowners here after floods and storms" is from a single 2005 disaster, and the card does not say so.
- **MINOR** (class): comma splice, "1 policy units", rcv_80, 61.11(c) (Silverado burn scar), "Renewing?", `dateModified`.
- **GAP 1.** Insurify's $795 / $892 are not reconciled with ours.
- **GAP 2.** Post-wildfire waiting-period exception and debris-flow risk.
- **GAP 3.** No line on why cities without CRS get no discount.
- **GAP 4.** Private flood.
- **GAP 5.** No cost by city.

**SEO:** I did not re-run the search. Round 10: the top 3 are statewide, and screen 1 answers with the ZIP range.

**Screenshot skim:** the disaster list (2023 ×2 EM, 2017, 2011, 2005 ×2) is correct against the data (17 distinct, no merges). Nothing else is wrong.

Verdict: FAIL

## atlantic-county-nj

- **MINOR** (carried, NOT FIXED): "up to 25% in Linwood". Brigantine, Longport, Margate City and Ventnor City are also 25%.
- **MINOR** (carried, NOT FIXED): "Erin HU (2025)" is FEMA's code; "Hurricane Erin" is meant.
- **MINOR** (carried, NOT FIXED): "All 37 ZIPs on NFIP policy records here are in the lookup". `by_zip` holds 38; "8037" (08037 Hammonton, 1 unit) is dropped.
- **MINOR**: "2016 — Severe Winter Storm and Snowstorm" and "2012 — Severe Storms and Straight-Line Winds" (the derecho) sit under "How often is this county a flood disaster?". Jonas did flood the shore (96 claims), but the derecho was wind.
- **MINOR** (class): comma splice, "1 policy units", rcv_80, 61.11(c), "Renewing?", `dateModified`.
- **GAP 1.** Insurify $1,022 and Clovered $1,899 are not reconciled with ours.
- **GAP 2.** No Risk Rating 2.0 transition pace.
- **GAP 3.** No cost by municipality.
- **GAP 4.** Private flood.
- **GAP 5.** No Elevation Certificate next step tied to the elevated/not-elevated rows.

**Checks:**
- Sandy ($418.7M) is the true costliest flood.
- The disaster count of 19 has no DR-into-DR merges.
- The round-10 NOAA BLOCKER is gone with the card.

**SEO:** I did not re-run the search. Round 10: screen 1 answers outright; the Sandy table is information gain.

**Screenshot skim:** nothing wrong or misleading.

Verdict: PASS

## montgomery-county-tx

- **MAJOR** (events table mislabel; montgomery-county-tx-07).
  - **The text:** "Tropical Storm Allison (1989–2001): FEMA's general label, many separate floods | 491 | $16.6 million".
  - **Why it is wrong:** Allison is not a general label. It is two specific named storms, Tropical Storm Allison of June 1989 and of June 2001 (the name was retired after 2001). `extras.claims.events` years are ["1989","2001"]. The catch-all wording is applied because the years span more than one, and here it is false.
- **MAJOR** (disaster count and list; montgomery-county-tx-16).
  - **The text:** "20 federal disasters ... 2016 — Severe Storms and Flooding".
  - **What the data holds:** DR-4269 (April 2016, Tax Day flood) and DR-4272 (May-June 2016 floods) are separate major disasters with the same title. The same-title merge folds them into one, so the count is 21 events, not 20, and the 2016 list line hides a second flood disaster. The cause is the same as in Louisiana.
- **MINOR**: "77386 Houston". 77386 is Spring; the reader knows it as Spring.
- **MINOR**: "Only some: 1 of the 15 NFIP communities here get one, up to 15% in Conroe". The grammar is wrong ("gets") and "up to" is used with a single community.
- **MINOR**: "A tenth pay $1,292 or more" is just $67 above p75 $1,225. That is true to the data (many policies at ~$1,084 and ~$1,266), but the bar reads oddly; no note explains it.
- **MINOR** (class): comma splice, "1 policy units", rcv_80, 61.11(c), "Renewing?", `dateModified`.
- **GAP 1.** MoneyGeek "$568 average" and Insurify "$1,040" (search results today) are not reconciled with our $1,001.
- **GAP 2.** No 2018 Montgomery County map-change note (Community Impact covers the map dates).
- **GAP 3.** No cost by city or The Woodlands.
- **GAP 4.** Private flood.
- **GAP 5.** No Spring/Lake Conroe dam-release context for 2017 (Harvey) claims.

**SEO ("flood insurance cost montgomery county TX"):**
- **The results:** MoneyGeek (TX statewide, with a Montgomery row of $568), Insurify (Houston page, Montgomery $1,040) and Community Impact (policy counts). No county-specific cost page ranks.
- **Our screen 1:** $1,001, the spread, the ZIP range and the rank. It answers faster and with sourced figures.
- **Where a searcher bails:** if they come from MoneyGeek's $568, we do not reconcile it; the "Why sites differ" table has no competitor row.

**Screenshot skim:** the orange bars are 2017, 2016 and 2019, matching the text. Nothing else is wrong.

Verdict: FAIL

## oklahoma

- **MAJOR** (events headline false against the page; oklahoma-07/08).
  - **The text:** "The costliest single flood here was Thunderstorms (2007): $17.8 million across 436 NFIP flood claims."
  - **The page's own chart:** 2019 paid $42.9M (the May-June 2019 Arkansas River flood, DR-4438) and 1984 paid $32.6M (the Memorial Day 1984 Tulsa flood). The footnote admits both have "no named flood in this table".
  - **Why it is wrong:** the reader is told a $17.8M thunderstorm event was the state's worst flood when the two biggest were roughly 2x larger. It should say "costliest named flood".
- **MAJOR** (disaster count wrong, list skips a disaster; oklahoma-21).
  - **The text:** "55 federal disasters for floods or storms here".
  - **What the data holds:** `data.json` declarations hold 75 distinct flood/storm disaster numbers (72 DR, 3 EM). The same-title merge folds 19 separate DRs into others, e.g. DR-317 (1972) with 404 and 409 (1973), DR-1384 with 1395 (2001), and DR-4791 (June 2024) with 4862 (March 2025).
  - **The list:** it says "newest first" but omits DR-4862 (declared 2025-03-18, "Severe Storms, Straight-Line Winds, Tornadoes, and Flooding"), jumping from 2026 to 2024.
- **MAJOR** (flood heading over non-flood events; oklahoma-21). "How often is Oklahoma a flood disaster?" lists "2026 — Severe Storm and Straight-Line Winds", "2023 — Severe Storms, Straight-Line Winds, and Tornadoes" and "2023 — Severe Winter Storm". Three of six lines name no flooding. FEMA files them as incidentType "Severe Storm", which `FLOOD_STORM` counts. The reader reads an inflated flood frequency.
- **MAJOR** (aid note false; oklahoma-22). "COVID, fire, ice-storm and tornado aid are left out."
  - **What is excluded:** only incidentType "Tornado" is dropped.
  - **What is counted:** the largest aid disasters here are tornado outbreaks filed as "Severe Storm", e.g. DR-4222 $16.5M "Severe Storms, Tornadoes, Straight-Line Winds, and Flooding", DR-4438 $14.2M, and DR-1917 $2.5M "Severe Storms, Tornadoes, and Straight-Line Winds" (no flooding at all). The DR-4690 "Severe Winter Storm" aid is counted too.
  - **Why it is wrong:** the $63.7M "after floods and storms" includes tornado and winter-storm aid that the note says is left out.
- **MINOR**: "Mcclain County" (CRS row) against "McClain County" (county table).
- **MINOR**: "The 13 largest discounts of 13 discounted communities are shown".
- **MINOR**: "Thunderstorms (2007)" is FEMA's label for the August 2007 Tropical Storm Erin flooding; a reader cannot tell what it was.
- **MINOR** (class): rcv_80, 61.11(c), checker aria-label, "Renewing?", `dateModified`.
- **GAP 1.** "Not in the NFIP (122 communities here)" names none (Greenfield, Osage, Springer, unincorporated McCurtain County and others). A reader in one cannot tell.
- **GAP 2.** Kin's "NFIP median $793" and MoneyGeek's "$995 average" are not reconciled with our $1,047.
- **GAP 3.** No Tulsa city figure. Tulsa, CRS class 1 with a 45% discount, is the state's best-known flood story, and searchers see "$892 in Tulsa".
- **GAP 4.** Private flood.
- **GAP 5.** No Oklahoma Insurance Department "Get Ready" next step.

**SEO ("flood insurance cost Oklahoma"):**
- **The results:** OKCFox/QuoteWizard ("ranks 23rd"), MoneyGeek (~$995 average) and Kin ("$793 NFIP median").
- **Our screen 1:** $1,047, the spread and "23rd highest", the same rank as #1 with a sourced median. It answers faster.
- **Our information gain:** the county table and the CRS table, on screens 10-17.

**Screenshot skim:** the orange bars are 2019, 1984 and 2007, matching the text (and contradicting the events headline).

Verdict: FAIL

## Classes

**State + county template:**
- **MAJOR (all pages with repeated generic titles).** `event_key` merges declarations by title within one calendar year, so distinct DR numbers with the same generic title ("Severe Storms and Flooding") become one "storm". Counts are low and list lines vanish: LA 8 merges, OK 19, Montgomery 1; PB, Orange and Atlantic 0. Fix: merge only EM into DR (or named-storm titles), never two DRs.
- **MAJOR (where an unnamed year out-pays the top named event).** "The costliest single flood here was X" is printed while the yearly chart shows bigger years under no name or the catch-all (Orange, Oklahoma). The headline needs "named", or must compare against unnamed years.
- **MAJOR (where the event spans few years).** The catch-all phrase "FEMA's general label, many separate floods" is triggered by a multi-year span, which mislabels a reused storm name (Allison 1989/2001). Match the literal label "Flooding", not the year span.
- **MAJOR (tornado/wind states).** "COVID, fire, ice-storm and tornado aid are left out" is false where tornado outbreaks are filed as "Severe Storm". The flood-disaster list includes winter-storm and wind-only "Severe Storm" declarations.
- **MAJOR where IA data is thin.** "Not in FEMA's records" on the repeat-flood card.
- **MINOR.** Comma splice in the download line (counties); "1 policy units" in the ZIP lookup; plural subject for one year; rcv_80 under-80% settlement; no 61.11(c); checker aria-label; "Renewing?" pool; `dateModified` lags the newest download.
- **GAP.** The non-NFIP line gives a count but no names.

**County template:**
- **MINOR.** ZIP town names from Census places (Watergate, Houston for Spring), blank towns, 4-digit ZIPs dropped.
- **MINOR.** "up to X% in <one town>" ignores ties and singular counts.
- **MINOR, SEO.** The same sentence frames on every county page (carried).

**Site pages:**
- **MINOR.** The methodology still describes tile maps that were removed.
- **MINOR.** The methodology calls the PIF workbook a reconciliation benchmark, while About says the official count is "not yet compared".

**Home template:**
- **MINOR.** "number of policies" over the "Insured units" column.
- **MINOR.** The description promises payouts the page does not show.
- **MINOR.** No `data-p` tags.

## Previous items (round-10 BLOCKER/MAJOR)

| Round-10 item | Status | Evidence |
|---|---|---|
| atlantic BLOCKER: NOAA card omits zone-coded Sandy/surge | FIXED | Card removed; no NOAA text or dataset on the page (atlantic-county-nj-00..20) |
| palm-beach MAJOR: NOAA card mislabels scope | FIXED | Card removed |
| orange MAJOR: NOAA card misses coastal events | FIXED | Card removed |
| palm-beach MAJOR: events table hides Opal with an unstated floor; false "general label" footnote; methodology says catch-all excluded | FIXED | The floor is stated ("20 or more paid claims"); the footnote now says only "no named flood in this table"; the methodology says the catch-all "gets its own row" |
| orange MAJOR: events table hides 2020s floods; false footnote; hidden rule | PARTLY | The floor and footnote are fixed. The same card now states a false headline ("costliest single flood ... Pineapple Express") against its own 1997 and 1995 totals |
| class MAJOR: unstated event floor, false footnote | FIXED | As above, on all 6 state and county pages |

**Tally:** 6 items. FIXED 5, PARTLY 1, NOT FIXED 0.

**Round-10 MINOR escalated:** the orange "Not in FEMA's records" repeat-flood line, NOT FIXED, is now a MAJOR.
