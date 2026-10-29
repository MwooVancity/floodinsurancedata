# Hater review, round 12 (2026-10-28)

**How I checked:**
- **Screenshots:** all 141 phone screenshots in `state/reviews/round12/` (home 00-08, louisiana 00-25, oklahoma 00-23, nevada 00-18, orange-county-ca 00-20, montgomery-county-tx 00-20, horry-county-sc 00-20).
- **Tagged numbers:** I re-read every `data-p` figure from the built HTML (1,349 tags on the six state/county pages) against its JSON path, using my own script, not the gate. **0 mismatches.**
- **Home page:** it carries no `data-p` tags, so I recomputed it from the data files:
  - all 103 state and county rows (median and units) match their `agg.json`;
  - the U.S. median $1,055 (n 2,351,712) and the new-policy median $995 (n 197,562) recompute from `data/us/cost_hist*.json`;
  - the $1,252 / $1,624 / $1,000 averages recompute as weighted means of the state `extras.json`;
  - 4.6M units = 4,580,802; 3,490,299 policy records and 2,680,429 claim records match.
- **Other checks:**
  - field meanings against `tools/metric_defs.json` (FEMA's own field definitions), since the brief names `metrics.py`;
  - disaster counts recounted from `data.json` with `metrics.flood_decl`;
  - aid, multi-loss and CRS counts recounted from `data.json`;
  - ZIP names read from `data/us/zip_places.json`.
- **Searches:** I ran the seven SEO searches today.

**Not checked:**
- the JavaScript quote checker and ZIP lookup outputs (the screenshots show only empty inputs);
- the methodology page;
- the CSV downloads;
- the live site.

My own defect list was written before I read round 11.

## home

- **GAP 1** (SEO, "flood insurance cost").
  - **What ranks:** the top 3 are Kiplinger, NerdWallet and Bankrate. Snippets quote about $888-$899 "average" (FEMA via Policygenius and NerdWallet) and $786 "median" (Insurify).
  - **What we show:** $1,055 median.
  - **The gap:** the "Why do sites quote different prices?" table (home-03) explains the bases but never names the numbers a searcher just saw. A reader coming from NerdWallet's $899 sees a figure 17% higher and no line saying why.
- **GAP 2.** #1-#3 give cost by flood zone nationally ("$560 in B/C/X, $2,795 in D"-style tables). The home page has no national zone table; it exists only on state pages.
- **GAP 3.** No national private-flood figure. The page says so ("Private flood insurance is not in this data"), so this is allowed and is not a defect.
- **MINOR** (home-03). "Lowest: Maryland $568, District of Columbia $384, Alaska $368" lists the lowest in descending order, so the lowest state comes last. Read fast, it says Maryland is the cheapest.
- **MINOR** (home-02). "The usual building deductible on U.S. single-family policies is $1,250 (51.7% of them)". It carries no `data-p` and cannot be re-derived from the shipped files (summing state `ded_counts` / `sf_n` gives 51.5%). The base is probably the policies that carry a deductible code, but the page does not say so.

**Information gain:** the 51-state and 52-county medians with insured units, all from FEMA records, sit on screens 3-8. **Doorway look:** none; the page is unique.

**Screens:** screen 1 answers the query ($1,055, $88 a month, the base stated in the note under the tiles) faster than NerdWallet or Bankrate, which open with prose.

Verdict: PASS

## louisiana

- **MAJOR** (louisiana-21/22). "6,132 records are from homes on FEMA's severe repetitive loss list", with the tile label "Records from homes on the severe repetitive loss list".
  - **What the data is:** FEMA's field definition (`highRiskPropertyType`, IA Multiple-Loss Flood Properties) says "SRL denotes properties impacted by 4 or more disaster declarations", an Individual Assistance flag.
  - **What the page claims:** "FEMA's severe repetitive loss list" is a defined NFIP term (4+ NFIP claims over $5,000, or 2+ claims above the building value) with its own list and surcharges.
  - **Why the reader is hurt:** an analyst or agent reads the page as an NFIP SRL count. A homeowner reads it as the list that drives NFIP rules for their house. Neither is what this number is.
  - **Fix:** "records from homes hit in 4 or more declared disasters (FEMA's disaster-aid 'severe repetitive' flag, not the NFIP list)".
- **MINOR** (louisiana-17/18). "Full-risk premium plus average fees $1,466 | what these existing policies would cost at FEMA's full price".
  - **How it is built:** median full-risk premium $1,220 + mean fees from `extras.json` (fee_mean 47 + hfiaa_mean 25 + reserve_mean 174).
  - **Why it is off:** it adds a median to means. The reserve-fund mean comes from charged premiums, but the assessment is a share of the premium, so at the full-risk premium it would be higher.
  - **Why it matters:** this is a derived estimate, and the dataset footer promises "estimates are labeled where they appear". It is not labeled.
- **MINOR** (louisiana-08). "Among the five costliest years, these have no named flood in this table: 1995".
  - **Overlap:** the same table has a "Flooding (1978–1998)" row that covers 1995.
  - **Grammar:** "these have" governs one year (carried from round 11).
- **MINOR** (louisiana-07). "the top reason FEMA recorded was 'not an actual flood' (20,318)". True as stated. But "Smaller reasons, or none recorded 35,155" is the largest row, and about 21.7% of unpaid claims carry no reason (`unpaid_with_reason_pct` 78.3), about 23,400 claims. Splitting out "none recorded" would be more honest.
- **MINOR** (carried). Event averages rounded inconsistently: "$103,300", "$92,400" against "$68,576".
- **MINOR** (carried). "Renewing? Policies whose term began in 2026 typically pay $1,215". That pool includes new 2026 policies.
- **MINOR** (louisiana-19, louisiana-18). Tiles "$854 (31,019 policies)" and "56.6% of 292,018" put the n inside the headline type. They wrap to two lines and read as one number.
- **MINOR** (louisiana-18). "56.6% of policies here" in the sentence, while the base is single-family primary homes (the tile says "of 292,018").
- **GAP 1** (SEO "flood insurance cost Louisiana": MoneyGeek $750, Insurify $1,470 "NFIP median, single-family" with a U.S. median of $1,290, Policygenius $752). Insurify's $1,470 vs our $1,086, both called NFIP medians, is not reconciled; a searcher will see both.
- **GAP 2.** Insurify's Plaquemines $4,752 against our $1,231 (carried).
- **GAP 3.** The NFIP-not-sold line counts 34 communities but does not name them (carried).
- **GAP 4.** No parish jump on screen 1 (carried).
- **GAP 5.** No years-to-full-risk at 18% a year (carried).
- **GAP 6.** No NRI flood-risk card on the state page; county pages have one.

**Checks:**
- **Disaster count:** "70 federal disasters". `data.json` holds 81 flood/storm disaster numbers: 61 DR and 20 EM. 70 = all 61 DRs + 9 EMs with no matching DR, so no DR is merged into another DR any more.
- **Aid:** $4,549,799,066 / 1,809,943 registrations = $2,514 ✓.
- **CRS:** 319 participating + 34 not = 353 rows ✓; 42 + 277 = 319 ✓.

**SEO:**
- **Screen 1:** $1,086, the middle-half range, the share below full risk, and the rank against the U.S. All of it is sourced, and it beats every top-3 snippet.
- **Information gain:** the parish table (screens 12-16) and named-flood payouts (screen 8) appear in no top result.
- **Doorway risk:** the card scaffolding is identical across states (see Classes); the tables differ.

Verdict: FAIL

## orange-county-ca

- **MINOR** (orange-county-ca-08). "Among the five costliest years, these have no named flood in this table: 1997, 1995, 1983". The "Flooding (1978–1997)" row in the same table spans all three years. The reader is told "not in the table" right under a row that covers them.
- **MINOR** (orange-county-ca-01). Comma splice: "downloaded October 25, 2026 with every record for California, every record the download listed was received, none missing" (carried).
- **MINOR** (orange-county-ca-06). "Most do: 53.1%" (carried). True but thin; the closed-without-payment rate (46.9%) is the story here.
- **MINOR** (orange-county-ca-17). "Data: NRI 2023 release". If FEMA has published a newer NRI, the card is a version behind. I did not verify which release is current.
- **MINOR** (orange-county-ca-20). "Compare other counties: Sacramento, Miami-Dade, Broward, Harris, Lee". Four of the five are across the country; the related-page links are weak for this reader.
- **MINOR** (orange-county-ca-00, class). The hero tiles "$1,083 Median / yr" and "Half pay between" do not say "single-family primary homes" on screen 1. The base first appears on screen 3.
- **GAP 1** (SEO "flood insurance cost orange county CA": Insurify CA guide with an OC row $795 / older $892; LendingTree CA; MoneyGeek CA $909).
  - Our $1,083 is 36% above Insurify's $795 for the same county, and nothing reconciles it.
  - **Where the reader bails:** they leave thinking we are wrong.
- **GAP 2.** County Public Works says unincorporated homeowners get 25% CRS. We show that (Orange County 25%, class 5), but not which cities' residents are "unincorporated".
- **GAP 3.** No cost by city; the ZIP table covers it partly.

**Checks:**
- **ZIPs:** the range ends 92679 ($707, 43 priced) and 92676 ($1,982, 84 priced) both clear the 25-policy floor ✓.
- **Repeat-flood card:** it now reads "Not in FEMA's disaster-aid records since 2002 ... NFIP insurance claims are counted separately" ✓.
- **Event headline:** it now says "costliest flood FEMA named" ✓.

**SEO:**
- **Top results:** all statewide; no county page ranks.
- **Screen 1:** our county median, the ZIP range and the rank against CA counties answer faster.
- **Information gain:** the ZIP table and the payout history.

Verdict: PASS

## montgomery-county-tx

- **MAJOR** (montgomery-county-tx-16/17). "1,132 records are from homes on FEMA's severe repetitive loss list". This is the same IA-flag vs NFIP-list mislabel as Louisiana (FEMA: "SRL denotes properties impacted by 4 or more disaster declarations").
- **MINOR** (montgomery-county-tx-11, carried, NOT FIXED). "77386 Houston". 77386 is Spring, in Montgomery County; Houston is the Harris County city. `data/us/zip_places.json` maps it so.
  - It is the county's largest ZIP (3,374 units) and the first row of the table, an easy screenshot for a competitor.
  - "77354 Pinehurst" (Magnolia) and "77316 Conroe" (Montgomery) are also not the USPS names.
- **MINOR** (montgomery-county-tx-08). "Tropical Storm Allison (1989–2001): FEMA's records use this name for claims in several years".
  - **What it is:** two different storms (June 1989 and June 2001) folded into one row.
  - **What changed:** the round-11 wording "general label, many separate floods" is gone, so it is no longer false. But a reader still sees one event.
  - **Fix:** split the row, or say "two storms named Allison".
- **MINOR** (montgomery-county-tx-08). "these have no named flood in this table: 1994". The "Flooding (1979–2002)" row covers October 1994 (class).
- **MINOR** (carried). "Only some: 1 of the 15 NFIP communities here get one, up to 15% in Conroe". The verb should be "gets", and "up to" is used with a single community.
- **MINOR** (carried, montgomery-county-tx-03). "A tenth pay $1,292 or more" is only $67 above p75 ($1,225). The bar's two right ticks overlap, and no note explains the price clustering.
- **MINOR** (montgomery-county-tx-17). "2020 — Tropical Storms Marco and Laura" (EM-3540, a pre-landfall emergency declaration) is listed under "How often is this county a flood disaster?". It is disclosed ("including emergency declarations") but inflates the flood count for an inland county.
- **MINOR** (comma splice, montgomery-county-tx-01; carried).
- **GAP 1** (SEO "flood insurance cost montgomery county TX": MoneyGeek TX with a Montgomery row of $568, Insurify Houston guide $1,040, Community Impact).
  - MoneyGeek's $568 is not reconciled with our $1,001.
  - **Where the reader bails:** a reader coming from MoneyGeek bails at the hero.
- **GAP 2.** No The Woodlands figure (three Woodlands ZIPs exist in the table, but no combined line).
- **GAP 3.** No 2018/2014 map-change note.

**Checks:**
- **Disaster count:** "20 federal disasters" = 18 DR + 2 EMs with no matching DR. DR-4269 and DR-4272 (2016) are no longer merged ✓.
- **Aid:** $134,552,262 / 106,825 = $1,260 ✓.

Verdict: FAIL

## oklahoma

- **MAJOR** (oklahoma-20). "23 records are from homes on FEMA's severe repetitive loss list". The same IA-flag mislabel (class).
- **MINOR** (oklahoma-08). "these have no named flood in this table: 2019, 1984, 1986". The "Flooding (1981–1993)" row covers 1984 and 1986. Only 2019 truly has no row.
- **MINOR** (carried, oklahoma-20). "Oklahoma City (Pottawatomie County/Oklahoma County/Mcclain County/...)" against "McClain County" in the county table.
- **MINOR** (carried, oklahoma-20). "The 13 largest discounts of 13 discounted communities are shown".
- **MINOR** (carried). "Thunderstorms (2007)" is FEMA's label for the Tropical Storm Erin / June 2007 floods; a reader cannot tell what it was.
- **MINOR** (oklahoma-21). "Data: declarations through 2025". Louisiana says "through 2026" from the same download, so the line reads as a data cutoff when it is the latest declaration year.
- **MINOR** (oklahoma-21). Two identical lines, "2022 — Severe Storms, Tornadoes, and Flooding". They are separate DRs, which is correct, but they read as a duplicate. Add the DR number or month.
- **GAP 1** (SEO "flood insurance cost Oklahoma": OKCFox/QuoteWizard "ranks 23rd", MoneyGeek about $995, Jerry $937, Kin "$793 NFIP median").
  - Kin's $793 "NFIP median" vs our $1,047 median is not reconciled.
  - Our "23rd highest" matches #1's headline, but our figure is sourced.
- **GAP 2.** The 122 non-NFIP communities are counted, not named (carried).
- **GAP 3.** No Tulsa city figure (carried).
- **GAP 4.** No OID "Get Ready" / FloodSmart OneStep next step.

**Checks (round-11 items):**
- **Disaster count:** "56" = 55 DR + 1 EM, no merges; the list now includes DR-4862 (2025) ✓.
- **List lines:** all six name flooding ✓.
- **Aid note:** it now says aid "can still cover wind or tornado damage from the same storm ... tornadoes alone are left out" ✓.
- **Event headline:** it now says "costliest flood FEMA named" ✓.

**Screenshot note:** the county table runs 7 screens, many rows a dash. That is fine for a data page.

Verdict: FAIL

## nevada

- **MAJOR** (nevada-07, and the screen-1 card nevada-01). The headline and table disagree.
  - **The headline:** "Of the 680 claims here closed without payment, the top reason FEMA recorded was 'not an actual flood' (129 claims)." The screen-1 card repeats: "Top reason for unpaid claims: 'not an actual flood'".
  - **The table directly below:** "Other | 149" is the first row, above "Not an actual flood | 129".
  - **Why it is wrong:** the sentence's label disagrees with its own table. It is true only if "Other" is silently not a reason. A copy editor or competitor sees a top reason that is not the top row.
  - **Fix:** say "the top named reason", or drop "Other" from the ranking explicitly. It is wrong only on Nevada of the six pages, but any page where "Other" leads will do this.
- **MINOR** (nevada-02). "Not in the NFIP (1 communities here)". The plural is wrong for one community; the noun needs to follow the number.
- **MINOR** (nevada-16). Two identical lines, "2017 — Severe Winter Storms, Flooding, and Mudslides" (DR-4303 and DR-4307, both real). They read as a duplicate.
- **MINOR** (nevada-16). "Data: declarations through 2023" (same as Oklahoma).
- **MINOR** (nevada-15). The repeat-flood card is a single "0" tile; a thin card. The wording is now correct ("since 2002 ... NFIP insurance claims are counted separately").
- **GAP 1** (SEO "flood insurance cost Nevada": MoneyGeek $799 with county rows, Nye $468 and Lander $1,421; 1-800 Insurance $1,038; StateCalc $696 "median of recent NFIP policies").
  - MoneyGeek's Nye $468 and Lander $1,421 are the reverse of our Nye $850 and Lander $651, and nothing reconciles them. A searcher comparing will doubt one of us.
- **GAP 2.** No Las Vegas / Clark County Regional Flood Control District context; the AO zone is 48% of units and is not explained.
- **GAP 3.** The state's division-of-insurance note ("available in every county except Esmeralda") is not used. Our page says one community is non-NFIP but not which.

**Checks:**
- **County units:** they sum to 9,160 ✓.
- **Aid:** $1,730,454 / 264 = $6,555 ✓.
- **Rank:** "9th lowest" ✓ (43rd of 51).

Verdict: FAIL

## horry-county-sc

- **MAJOR** (horry-county-sc-00, the title, meta description and hero). "Flood insurance cost in Horry County, South Carolina: $583 median a year" and "Half pay between $487–$820".
  - **The base:** single-family primary homes, 14,356 priced policies.
  - **The county:** 53,412 insured units, dominated by condo associations and second homes (29577 Myrtle Beach: 12,512 units but 1,530 priced; 29582: 13,412 units but 1,471 priced).
  - **The page's own figure:** "Average cost, every policy type $1,554" (horry-county-sc-12), 2.7x the headline, and second homes pay the $250 HFIAA surcharge instead of $25.
  - **Where the base appears:** only on screen 3, never on screen 1.
  - **Why the reader is hurt:** in a resort county most readers own a condo or second home. One holding a $1,400 quote reads the title and hero and concludes they are being overcharged by 2.4x.
  - **Fix:** name "single-family primary homes" in the hero tile labels and the title or description where the single-family share of units is low, and put the all-policy mean on screen 1.
- **MAJOR** (horry-county-sc-16/17). "191 records are from homes on FEMA's severe repetitive loss list". The same IA-flag mislabel (class).
- **MINOR** (comma splice, horry-county-sc-01; carried).
- **MINOR** (horry-county-sc-12/13). Zone VE has 3,479 units (6.5%) but no row in "What does it cost in my flood zone?". Fewer than 50 single-family primary VE policies are priced, and the page states that floor. But the beachfront reader is the one most likely to ask, and gets nothing.
- **GAP 1** (SEO "flood insurance cost horry county SC": WBTW, WMBF, MoneyGeek SC with a Horry row of $493, Policygenius SC $747 with "risk-based $929").
  - Policygenius's $929 full-risk figure is not reconciled with our full-risk $437 premium-only plus $614 with fees.
  - MoneyGeek's $493 equals our cheapest ZIP and should be noted.
- **GAP 2.** 1-800 Insurance's "$2,000–$6,000 for most Little River properties" (likely condo/VE) has no answer; our 29566 Little River median is $493 single-family. That is the same base problem as the MAJOR above.
- **GAP 3.** No new-map (2003 FIRM, pending update) note; WBTW and WMBF both lead on it.
- **GAP 4.** No condo/RCBAP cost line at all.

**Checks:**
- **Disaster count:** "16" = 13 DR + 3 EMs with no matching DR; DR+EM pairs (Ian, Dorian, Debby) merged ✓.
- **Aid:** $26,879,860 / 17,129 = $1,569 ✓.
- **CRS:** 4 + 5 = 9 ✓.

Verdict: FAIL

## Classes

**State + county template:**
- **MAJOR (every page with a nonzero multi-loss count).** The "severe repetitive loss list" label. The data is FEMA IA's `highRiskPropertyType` = SRL ("impacted by 4 or more disaster declarations"), not the NFIP Severe Repetitive Loss list. Relabel the tile and the sentence on all pages, and "RL" as "hit in 2–3 declared disasters".
- **MAJOR (any page where "Other" is the largest unpaid reason).** The "top reason FEMA recorded" sentence skips "Other" but the table shows it first (Nevada now). Say "top named reason", or rank without "Other" in both places.
- **MAJOR (counties where single-family primary homes are a minority of insured units; Horry; likely Myrtle Beach-type resort counties such as Dare, Cape May, Monroe and Baldwin).** The headline median is single-family primary only, and the hero never says so. Every state and county page has the same unlabeled hero (MINOR elsewhere). A rule: name the base in the tile label always.
- **MINOR (all pages).** "these have no named flood in this table: <years>" while the "Flooding (YYYY–YYYY)" catch-all row covers those years. Say "no single named flood" or exclude the catch-all years.
- **MINOR (all pages).** "Full-risk premium plus average fees" adds a median to means and uses a reserve-fund mean taken from charged premiums. Label it an estimate, or compute the per-policy full-risk cost and take its median.
- **MINOR (all pages).** Tiles with the n inside the big number ("56.6% of 292,018", "$854 (31,019 policies)").
- **MINOR (all pages).** "Data: declarations through <year>" reads as a cutoff.
- **MINOR (all pages).** Identical disaster titles in the list need a month or DR number.
- **MINOR (counties).** Comma splice in the download line; GeoNames ZIP names that are not the USPS city (Montgomery: "77386 Houston").
- **MINOR (state pages).** No NRI card; county pages have one.
- **GAP (all pages, SEO).** "Why sites differ" explains bases but never names the competitor figure the searcher just saw:
  - MoneyGeek county rows: Montgomery $568, Horry $493, Nye $468;
  - Insurify: OC $795, LA $1,470;
  - Kin: OK $793.
  - Every top-3 set had at least one such figure.
- **GAP (all pages).** Non-NFIP communities counted, not named.
- **SEO / templating.** The card scaffolding and the legal paragraphs (waiting period, already flooded, rcv_80, yearly cap, CRS, elevated note, aid note) are word-for-word the same on every state and county page.
  - **Why it passes:** the tables (zones, parishes/counties, ZIPs, events, CRS) differ, so this is not name-swap mad-libs.
  - **The risk:** the shared prose is about 40% of each page's words.
  - Rated MINOR because the owner chose data pages, but it is the one templating signal a rater would flag.

**Home:** no class defects beyond the GAPs.

## Previous items (round-11 BLOCKER/MAJOR)

| Round-11 item | Status | Evidence |
|---|---|---|
| louisiana MAJOR: same-title merge folds separate DRs (2016 Great Flood) | FIXED | 70 = 61 DR + 9 unmatched EM; no DR-into-DR merge (`data.json` recount) |
| orange MAJOR: "costliest single flood" headline contradicts 1997/1995 | FIXED | Now "The costliest flood FEMA named here was Pineapple Express Southern (1998)" (orange-county-ca-07) |
| orange MAJOR: "Not in FEMA's records" repeat-flood line | FIXED | Now "Not in FEMA's disaster-aid records since 2002 ... NFIP insurance claims are counted separately" (orange-county-ca-17) |
| montgomery MAJOR: Allison called "FEMA's general label, many separate floods" | PARTLY | The false phrase is gone. Now "FEMA's records use this name for claims in several years", which is true, but the row still merges two storms (montgomery-county-tx-08); now MINOR |
| montgomery MAJOR: DR-4269/4272 merged, count 20 | FIXED | 20 = 18 DR + 2 unmatched EM; both 2016 DRs are counted |
| oklahoma MAJOR: "costliest single flood" Thunderstorms 2007 | FIXED | Now "costliest flood FEMA named" (oklahoma-07) |
| oklahoma MAJOR: count 55 with 19 DR merges; list skipped DR-4862 | FIXED | 56 = 55 DR + 1 EM; the list opens with 2025 DR-4862 (oklahoma-21) |
| oklahoma MAJOR: non-flood "Severe Storm" lines under the flood heading | FIXED | All six list lines name flooding; `flood_decl` requires "FLOOD" in Severe Storm titles |
| oklahoma MAJOR: aid note "tornado aid left out" false | FIXED | Now "their aid can still cover wind or tornado damage from the same storm ... tornadoes alone are left out" (oklahoma-22) |
| class MAJOR: same-title DR merges | FIXED | As above, on LA, OK and Montgomery |
| class MAJOR: "costliest single flood" | FIXED | "named" on all six pages |
| class MAJOR: multi-year span triggers catch-all wording | PARTLY | Wording softened; Allison still one row |
| class MAJOR: tornado/wind aid note and wind-only list lines | FIXED | As Oklahoma |
| class MAJOR: "Not in FEMA's records" | FIXED | As Orange; same wording on Nevada |

**Tally:** 12 FIXED, 2 PARTLY, 0 NOT FIXED.

**Carried MINORs still open:**
- 77386 Houston;
- Montgomery "1 ... get one";
- "Mcclain";
- "13 of 13";
- the comma splice;
- "these have" for one year;
- event-average rounding;
- the "Renewing?" pool.
