# Hater review, round 3 (2026-10-26)

Pages: https://floodinsurancedata.com/, /flood-insurance/louisiana/, /flood-insurance/palm-beach-county-fl/

**What I read**
- Every phone screenshot in state/reviews/round3: home-00..06, louisiana-00..25, palm-beach-county-fl-00..21.
- The built HTML for all three pages: the text, head, JSON-LD, outbound links and the ZIP-lookup script. I also read dist/about/index.html.
- Data: data/states/louisiana/{agg,extras,data}.json and data/c/palm-beach-county-fl/{agg,extras,data}.json.
- tools/metrics.py, the field definitions only.
- I read no gate code.

**Web checks**
- Google SERP for each page's query (WebSearch): "flood insurance cost", "flood insurance cost Louisiana" and "flood insurance cost palm beach county FL".
- One rule check: Florida's Citizens Property Insurance flood requirement (s. 627.351, Fla. Stat.).

I built the defect list below before I opened hater-round2.md. The "Previous items" section was added after that.

Severity:
- **BLOCKER**: wrong or misleading information a reader could act on, or a page that would not beat the #1 result for its own query.
- **MAJOR**: confusing, untrustworthy or broken, or a clear gap against the #1 result.
- **MINOR**: polish.

---

## home

**SERP today ("flood insurance cost")**
1. Kiplinger, "Flood Insurance: What It Costs and Why You Need It".
2. A second Kiplinger URL with the same title.
3. Bankrate, "cost of flood insurance": NFIP average about $926 a year (July 2025), a state table and private vs NFIP.
4. NerdWallet: $899 a year, or $75 a month.

All four answer with one national average, a state table, the price factors, Risk Rating 2.0 increases, private vs NFIP, and the 30-day wait. All four carry named authors and editors.

1. **BLOCKER** (SEO): this page would not beat #1 for "flood insurance cost".
   - **What we show.** The first screen (home-00) gives "$1,055 U.S. median a year", "$88 per month" and "4.6M insured units". After that come three FAQs (home-01) and two long tables (home-01..06).
   - **What #1–#4 have that we lack:**
     - what drives the price (elevation, foundation, coverage, deductible, distance to water);
     - how to lower it;
     - what private flood insurance costs;
     - any Risk Rating 2.0 explanation on the home page;
     - a cheapest and most expensive state callout;
     - a quote checker (the state pages have one, the home page does not);
     - a named author or reviewer.
   - **Our information gain** is real (record-level medians for 51 places and 42 counties, plus unit counts). But it is only two bare tables, and a searcher who wanted "what will I pay and why" goes back to Google after home-00.
   - On a head term held by Kiplinger, Bankrate and NerdWallet, an anonymous new domain with roughly 120 words of prose does not win.
2. **MAJOR**, home-00: "$1,055 U.S. median a year" is 14–17% above every top result (Bankrate $926, NerdWallet $899, Insurify $786), and the home page never says why.
   - The reason exists: single-family primary homes, premium plus fees, median not mean. It only appears in the Louisiana block "Why do sites quote different averages", which home does not have.
   - A searcher comparing tabs concludes that we are the outlier.
3. **MAJOR**, home-01: "Am I required to buy it? Only if your home is in a high-risk zone (A or V) and your mortgage is from a federally regulated lender, or federal help to buy or build". The word "only" is wrong in three ways:
   - It leaves out federally backed loans (FHA, VA, Fannie and Freddie). The state and county tiles say "regulated or backed".
   - It leaves out that a lender can require cover in any zone.
   - It leaves out Florida's Citizens rule: Citizens policyholders must carry flood by dwelling value, in any zone. See palm-beach-county-fl 1.
   - Florida is the site's largest state (1,795,894 units), and this home page is its entry point.
4. **MAJOR**, home-00: "Built from 3,490,299 NFIP policy records ... matched to FEMA's own count."
   - "FEMA's own count" is the API's record total for the same download, so the check is circular.
   - /about/ says "FEMA's separate official policy count is not yet compared". The first-screen trust line overclaims.
5. **MAJOR** (YMYL trust): no named person, organisation or contact anywhere.
   - /about/ says only "an independent, non-commercial project".
   - JSON-LD gives `creator` as "Flood Insurance Data", with no person.
   - Every top-3 competitor names its writer and editor. A money and insurance page with no responsible party fails a rater's first check.
6. **MAJOR**, home-00: the H1 says "What flood insurance costs in your state **and county**", and the search box reads "Type your state or county…".
   - There are 42 county pages for about 3,100 counties, and the selection rule is never stated.
   - Most readers who type their county get nothing.
7. **MAJOR**, home-01..03: the state table is sorted by insured units, not by cost, and has no rank and no high/low callout.
   - To answer "which states cost most?" (a Bankrate table headline), a phone reader has to scan 51 rows.
   - Connecticut ($1,501) and Hawaii ($1,395) sit mid-table, and Alaska ($368) and DC ($384) sit at the bottom by accident.
8. **MINOR**, home-00: "$88 PER MONTH" is the yearly median ÷ 12. The tile reads as monthly billing; the state pages now say "a month, spread over the year".
9. **MINOR**, terms: the column is "Insured units" on home but "Policy units" on state and county pages, for the same field.
10. **MINOR**: "50 states and DC". Puerto Rico, the USVI and Guam (all NFIP participants) are left out without a word.
11. **MINOR**: all of the home page's "Three things to know first" text is repeated word for word on every state and county page.
12. **MINOR**: every official citation (FEMA's map, FloodSmart, the OpenFEMA pages) is `rel="nofollow"`. Citing a primary source and then disowning the link is an odd trust signal.

Counts: 1 BLOCKER, 6 MAJOR, 5 MINOR.

Verdict: FAIL

---

## louisiana

**SERP today ("flood insurance cost Louisiana")**
1. MoneyGeek, "How Much Is Flood Insurance in Louisiana? Average Flood Insurance Cost and Coverage": about $750 a year, by city, by coverage level, cheapest companies.
2. Insurify, "Louisiana Flood Insurance: Complete Guide for Homeowners in 2026": "median ... $1,470 per year for a single-family home, according to the NFIP", and a parish table with Plaquemines at $4,752.
3. Fox8, a news piece on rising costs.

Also high: Bankrate ($955 average) and Policygenius ($752).

1. **BLOCKER** (SEO): this page would not beat MoneyGeek or Insurify for "flood insurance cost Louisiana".
   - **Title and H1.** "Flood insurance cost in Louisiana: $1,086 median a year (FEMA data)" matches the query better than #1's title.
   - **First screen.** louisiana-00 answers outright, faster than #1 ($1,086, $90, the middle half, and 56.6% below full risk). That part wins.
   - **What #1 and #2 have that we lack:**
     - cost by coverage amount or home value;
     - cost by city or town (we have parishes only);
     - private-market prices and the cheapest companies;
     - a "how to lower your premium" answer. Our own extras.json holds the deductible mix (53.2% at $1,250) and the elevated vs not-elevated medians ($854 vs $859), and the page shows neither;
     - a named author or reviewer.
   - **Insurify's figure is never reconciled.** #2 prints "$1,470 median, single-family, NFIP", 35% above our $1,086, and claims to use the same source. Our "Why do sites quote different averages" table (louisiana-16/17) lists six measures, and none of them is $1,470.
     - Our median full-risk premium $1,220 plus the average fees ($47 + $25 + $174 = $246) comes to about $1,466. That is very likely Insurify's basis, and the page never says so.
     - Insurify's Plaquemines $4,752 against our $1,231 is the same gap.
     - A searcher who opens both tabs trusts the brand.
   - **Our information gain is buried.** The quote checker sits on screen 1–2. The parish table (median, below full risk and claims per parish) only arrives on screens 11–16, the "why sites differ" table on 16–17, and claims and unpaid reasons on 5–8.
   - **Where readers bail.** louisiana-02 opens a policy-unit-by-zone table before the cost section, so a reader looking for prices hits a share-of-units table first.
   - **Scale.** The page runs to 26 phone screens.
2. **MAJOR**, louisiana-00/04 and the checker: the headline "$1,086 median" mixes policy terms that began in 2025 with terms that began in 2026.
   - agg.json gives 2025-effective median $1,080 (n=121,828) and 2026-effective median $1,215 (n=170,190), which is +12.5%.
   - Someone renewing today is quoted near $1,215. The checker compares that against a pool in which 42% are last year's prices, and tells them they are above typical.
   - The page holds the split and hides it. Its only reference is "A per-effective-year median is shown only where several years of policies exist" (louisiana-24), and nothing is shown.
3. **MAJOR**, louisiana-10/11 and 12..16: medians cluster on one value, with no explanation.
   - Zone C, Zone A99 and Zone B are each $1,086, the state median. Zone X is $1,080, the 2025-term median.
   - Parishes: St. Helena $1,080, Beauregard $1,083, East Feliciana $1,084, West Feliciana $1,086, Tangipahoa $1,087, St. Bernard $1,088, Vernon $1,077 and Washington $1,079.
   - The note "many policies pay one of a few common amounts under FEMA's current rating, whatever the zone" offers no evidence: no amount, no share and no cause.
   - A Zone C or A99 owner reads "my zone costs exactly the state typical". Either a mass point (a statutory or minimum amount) drives the medians, which makes "median" the wrong summary here, or something in the pipeline is wrong. Neither is shown.
4. **MAJOR**, louisiana-20: "Each parish page lists its own towns."
   - Only 5 of 64 parishes have a page: Jefferson, Orleans, St. Tammany, East Baton Rouge and Terrebonne. Those are the only five linked rows in the parish table.
   - For 59 parishes the promise is false.
5. **MAJOR**: the meta description, the thing the searcher sees on Google, says "395,032 policies". On the page that number is records; the page says "407,916 policy units".
   - The page also prints 359,013 "residential policies in force" (the penetration dataset), 292,018 single-family policies and 212,784 reporting a rebuild cost.
   - The home page shows Louisiana as 407,916.
6. **MAJOR**, louisiana-09: "Not in full for 21.5% of insured single-family homes here".
   - The rate comes from 212,784 of 292,018 policies (73%) that report a rebuild cost. The headline states it for all of them.
   - The new sentence ("many owners insure to the building maximum even when that figure is lower") explains why it sits beside 64.8% at maximum. It does not justify stretching the 73% subset to every home.
7. **MAJOR**, louisiana-22/23: "FEMA also publishes a separate official policy count, which we have not yet compared for Louisiana."
   - It is the round-1 item, still open. A data site that says it has not checked itself against FEMA's own published count hands a competitor the screenshot.
8. **MAJOR** (rater, scaled content):
   - 56% of the Palm Beach page's prose (1,560 of 2,779 words, in sentences over 40 characters, tables excluded) appears word for word on this page.
   - The repeated blocks are "How do I actually get covered", "Already flooded?", "Yearly cap", the CRS definition, "What this data cannot tell you", "Are these counts complete", the source lists, and the rebuild and claims captions.
   - The purchase rule appears three times: the tile, the card, and "is under 'Am I required to buy it?'".
   - Across about 94 pages, that is the templated pattern Google's scaled-content policy describes.
9. **MINOR**, louisiana-00: "$90 a month". $1,086 ÷ 12 = $90.50.
10. **MINOR**, louisiana-07: the sentence names "not an actual flood" (20,318) as the "top reason". The largest row is "Smaller reasons, or none recorded" (35,155).
11. **MINOR**, louisiana-17: the "Average cost, every policy type $1,337" row has an empty "What it counts" cell.
12. **MINOR**, louisiana-02 and louisiana-17: "51.0% of Louisiana's NFIP **policies**" and "56.6% of **policies** here". The first is units; the second is the single-family cohort.
13. **MINOR**, louisiana-19: "Lafayette City-Parish (Lafayette Parish)" and "Lafayette (Lafayette Parish)" are both listed at 15%, class 7, with no explanation.
14. **MINOR**, louisiana-08: "Mid summer severe storms (2016)". FEMA's name, in extras.json, is "Mid-summer severe storms". Readers know it as the August 2016 flood.
15. **MINOR**, louisiana-05/06: on a phone the 2005 bar flattens every other year to nothing. There is no y-axis, and the values sit in hover-only titles.
16. **MINOR**, louisiana-10/11: the zone table runs 25 rows (A01..A15, V15, AHB). An AE owner scrolls past 20 legacy codes.
17. **MINOR**, sources:
   - The page links the "fima-nfip-redacted-policies-v2" and "claims-v2" pages, while JSON-LD says "NfipPolicies v3 and NfipClaims v3".
   - It cites "NRI 2023 release", a vintage that is unverified.
   - Dates: "downloaded October 25" against "newest ... October 26".
18. **MINOR**: the basis of "below full-risk" (totalInsurancePremiumOfThePolicy vs fullRiskPremium) is never stated. The page does not say whether the CRS discount and the ICC premium sit on both sides of that comparison.

Counts: 1 BLOCKER, 7 MAJOR, 10 MINOR.

Verdict: FAIL

---

## palm-beach-county-fl

**SERP today ("flood insurance cost palm beach county FL")**
1. NerdWallet, "Flood Insurance in Florida: Cost and Coverage Guide": Palm Beach $528.
2. MoneyGeek, "How Much Is Flood Insurance in Florida?": county average $466.
3. AOL, "Flood insurance costs will soar in Florida. See the expected increases in your ZIP code": ZIP 33469 +342%.
4. Palm Beach County's own 2018 policy-statistics page.

Insurify's 2026 guide gives $709. No top-3 result is a county page, which is a real opening for us.

1. **BLOCKER**, palm-beach-county-fl-00 and -02: "Am I required to buy it? **Only** in a high-risk zone with a federally regulated or backed mortgage or federal building help." This is false for a large share of this county's readers.
   - Under Florida law (s. 627.351), Citizens Property Insurance personal-lines policyholders with wind cover must carry flood insurance to stay eligible, **in any zone**.
   - The phase-in: replacement cost $600k+ from Jan 1, 2024; $500k+ from 2025; **$400k+ from Jan 1, 2026**; all others from Jan 1, 2027.
   - The page's own data says 50.6% of single-family rebuild costs here are over $250k.
   - A Zone X Citizens customer told "only in a high-risk zone" risks losing their Citizens eligibility.
   - Sources: news4jax 2025-09-16; citizensfla.com, "new flood requirements begin January 1".
2. **BLOCKER**, the ZIP lookup (script `ZD`, palm-beach-county-fl-11): the lookup holds only the 25 largest ZIPs.
   - For any other ZIP it prints "No NFIP data for ZIP 33470 in this county." That is false.
   - The 25 ZIPs hold 107,279 of the county's 132,945 policy units. The other 25,666 units sit in ZIPs the lookup reports as having no data: 33470 Loxahatchee, 33413, 33415, 33417, 33426, 33436, 33449, 33478 Jupiter Farms, 33430 Belle Glade, and others.
   - The caption "smaller ZIPs show count only" is also false; they show nothing.
   - A reader whose ZIP is missing concludes that NFIP does not insure there, or that nobody does.
3. **BLOCKER** (SEO): as published, the page would not beat NerdWallet for its query, despite being the only county-specific result.
   - **First screen.** palm-beach-county-fl-00 answers faster than any top-3 result: "$670 median", the ZIP range $450–$1,825, and the Florida and U.S. comparison. That wins.
   - **Gaps against the top 3:**
     - The Citizens requirement (1 above). It is the most-asked Florida flood question, and NerdWallet and Bankrate both cover it.
     - The ZIP-level increase ahead. AOL ranks with "expected increases in your ZIP code". We have the premium vs full-risk gap but only county-wide, and the ZIP table holds none.
     - Town names. "33480" means nothing to a Town of Palm Beach owner, and there is no Boca Raton, Jupiter or Wellington row, even though the CRS table names all of them.
     - Private flood prices. Florida has the largest private flood market.
     - Why NerdWallet says $528, MoneyGeek $466 and Insurify $709 while we say $670. The Louisiana page has a "Why do sites quote different averages" block; **this page has none**.
     - A named author.
   - **Where readers bail.** palm-beach-county-fl-01, "Does it pay out here? 43.5% of claims here paid something" (see 5), and the ZIP box that answers "No NFIP data".
4. **MAJOR**, palm-beach-county-fl-06/07 and -03: three county figures are each extreme against Florida, and they are published as facts without a check.
   - **Unpaid claims.** 56.5% closed without payment; Florida is 30.1%.
   - **Claim dollars outside the high-risk zones.** 45.5% of claim dollars paid outside A/V zones; Florida is 8.1%.
   - **Claim volume.** 10,758 claims, or 8.1 per 100 current units (agg.json `cumulative_per_100_current_units`). Round 2 gave Broward 14.9 and Miami-Dade 16.9 per 100.
   - The page itself says "Claims are matched by the claims dataset's county code, which may not exactly match a policy's property county". All three outliers are what a county-assignment problem would produce.
   - Nothing on the page tests this, and nothing reconciles it with FEMA's published county loss statistics.
5. **MAJOR**, palm-beach-county-fl-01, first-screen tile: "Does it pay out here? 43.5% of claims here paid something; the average paid claim was $15,396."
   - For a just-flooded owner with 30 seconds, this says "file and you probably get nothing", from a figure that may be an artefact (4).
   - The caveat ("some closed claims are paperwork") is four screens down, in small print.
6. **MAJOR**, palm-beach-county-fl-09: "Not in full for 50.6% of insured single-family homes here".
   - The rate rests on 27,755 of 50,781 policies (55%) that report a rebuild cost, stated as a fact about all insured homes.
   - It is the scariest number on the page, and it comes from a field half the records leave blank.
7. **MAJOR**, palm-beach-county-fl-14/15, NRI:
   - "FEMA models roughly $178.9 million of flood loss a year" inland. The same page shows NFIP payouts of $72.0 million in 48 years and NWS damage of $71.1 million in 30 years. The model's single year is 2.5 times the whole recorded history, and the gap is never explained.
   - The rating says "Relatively High" inland, while the next sentence says per-dollar loss is "higher than in about 30% of U.S. counties".
   - The caveat paragraph is honest, but a homeowner cannot reconcile three numbers 70x apart.
8. **MAJOR**, counts:
   - The meta description says "75,140 policies"; the page says "132,945 policy units" (palm-beach-county-fl-06/19); the home page says 132,945.
   - The penetration card prints "Residential policies in force 69,154" (palm-beach-county-fl-18). That is half the units, and it is unexplained.
   - Four different "policy" totals reach the searcher, the first of them in the Google snippet.
9. **MAJOR**, palm-beach-county-fl-11: the ZIP table mixes two bases in one row.
   - "Policy units" counts condo units; "Median annual cost" covers single-family policies only.
   - 33480 shows 9,412 units beside $1,825, but that median comes from 988 policies. 33484 shows 4,991 units, but its $450 comes from 640 policies.
   - The visible list is the 8 largest ZIPs by condo-inflated units. 33437 (2,845 priced policies at $474) and 33418 (2,564 at $620) are hidden behind the box.
10. **MAJOR** (rater, scaled content): 56% of this page's prose is word for word on the Louisiana page (louisiana 8), including the triple purchase rule.
11. **MAJOR**, palm-beach-county-fl-01/19: the records are verified only at state level ("with every record for Florida"), and the page adds "FEMA also publishes a separate official policy count, which we have not yet compared for Palm Beach County."
12. **MINOR**, palm-beach-county-fl-01: "downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing." This is a comma splice that reads as two half-sentences.
13. **MINOR**, palm-beach-county-fl-14: the prose says "river flooding and ... coastal flooding", while the tiles read "Coastal" then "**Inland**", in the reverse order and with different words.
14. **MINOR**, palm-beach-county-fl-06: 2025 is highlighted as a top-three year ($6,857,416, 99 claims, about $69k each), and no event in the table explains it.
15. **MINOR**, palm-beach-county-fl-10: the Zone VE row ($1,393, n=116) has no small-sample caution. VE is the highest-stakes zone.
16. **MINOR**, palm-beach-county-fl-13: "Palm Beach 20%" (the town) sits near "Palm Beach County 25%" (unincorporated only), and the town is not labeled.
17. **MINOR**, palm-beach-county-fl-02: "Other low-risk or unclassified zones 835" is Zone C (616) plus Zone B (219), named low-risk zones. Zone X 57.5% plus 0.6% gives 58.1%, against "58.2%" in the next card.
18. **MINOR**: "$56 PER MONTH". "Half of homeowners here pay…" is half of insured single-family policyholders. "29.5% of policies here" is the single-family cohort.
19. **MINOR**: extras.json holds the deductible mix (70.8% at $1,250) and the elevated vs not-elevated premium medians ($856 vs $506), and the page shows neither. "How do I lower it?" is a top reader question.
20. **MINOR**, dates and sources:
   - "downloaded October 25" against "newest ... October 26".
   - "Data effective 1996-2025" uses a hyphen where other ranges use an en dash.
   - It cites "NRI 2023 release" (vintage unverified), and v2 dataset links against v3 in the JSON-LD.

Counts: 3 BLOCKER, 8 MAJOR, 9 MINOR.

Verdict: FAIL

---

## Classes

**home**
- The purchase rule says "only", with no backed loans, no lender-can-require caveat, and no Florida Citizens rule.
- The circular trust line "matched to FEMA's own count".
- The county promise (H1 and search) against 42 county pages.
- No author, owner or contact.
- The U.S. median is higher than every competitor and goes unexplained.
- The state table is sorted by units, with no ranking.

**state** (Louisiana pattern)
- The headline median mixes 2025-term and 2026-term policies; the split sits in agg.json and is hidden.
- The checker benchmarks renewals against last year's prices.
- Clustered medians: zone and parish medians equal the state or 2025-term median, with an unproven "common amounts" note.
- "Each parish/county page lists its own towns" while only a few county pages exist.
- The meta description counts records as "policies"; four or five unreconciled policy totals per page.
- The rebuild headline extends a reporting subset to all homes.
- No reconciliation with the competitor figure that ranks #2. Insurify's NFIP median is very likely full-risk premium plus fees.
- No cost-lowering data (deductible, elevation), although extras.json has it.
- v2 source links against v3 JSON-LD; the NRI vintage is unverified.

**county** (Palm Beach pattern)
- The ZIP lookup holds only the top-25 ZIPs and tells every other ZIP "No NFIP data". This is wrong on every county page that uses the same `by_zip` truncation.
- The ZIP table mixes condo-inflated units with single-family medians, and gives no place names.
- Claims are assigned by the claims county code. Extreme unpaid, outside-SFHA and claims-per-unit figures are published without a check.
- A first-screen "Does it pay out here?" tile shows a possibly artefactual unpaid rate.
- The NRI modeled loss is never reconciled with the NFIP and NWS totals on the same page.
- No "why sites quote different averages" block; it exists on state pages only.
- Florida counties: the Citizens flood requirement is missing from "Am I required to buy it?". The same applies to every FL county page and the Florida state page.

**state + county**
- About 56% of prose is verbatim across pages, and the purchase rule appears three times per page.
- "$X a month" tiles; "half of homeowners" or "policies here" used for the single-family cohort.
- Dates of Oct 25 against Oct 26; hover-only chart values; nofollow on every official citation.

---

## Previous items (every round-2 BLOCKER and MAJOR; round 2 had no BLOCKERs)

### Home (4 MAJOR)
| # | R2 item | Status | Evidence |
|---|---|---|---|
| 1 | Circular "matched to FEMA's own count" | NOT FIXED | home-00 still says "every record for each state shown, matched to FEMA's own count". |
| 2 | No named person, organisation or contact | NOT FIXED | /about/ says "an independent, non-commercial project"; no name, no contact. |
| 3 | Purchase rule has no "backed" and no lender caveat | NOT FIXED | home-01 is unchanged: "...from a federally regulated lender, or federal help to buy or build". |
| 4 | "State and county" promise against 42 county pages | NOT FIXED | The H1 and "Type your state or county…" are unchanged; the table still lists 42 counties. |

### Louisiana (14 MAJOR)
| # | R2 item | Status | Evidence |
|---|---|---|---|
| 1 | EM titles ("Tropical Storm Ida/Francine/Zeta") | FIXED | louisiana-22/23: "Hurricane Francine", "Hurricane Ida", "Hurricane Zeta". |
| 2 | "Zone drives your price" | FIXED | louisiana-01: "decides whether a lender must require coverage; your price comes mainly from your own building's flood risk". |
| 3 | "407,916 policies" in prose; "395,032 policies" in the meta description | PARTLY | Prose now says "407,916 policy units". The meta description still says "395,032 policies" (louisiana 5). |
| 4 | Rebuild card: 21.5% vs 64.8%, subset base | PARTLY | The "measure different things" sentence and "all building types" were added. The headline still extends the 73% subset (louisiana 6). |
| 5 | Verification claim top vs bottom; schema | PARTLY | The top claim and the schema are now honest ("every record the download listed was received", "reconciled to the API's record count"). The official count is still "not yet compared" (louisiana 7). |
| 6 | Outside-zone dollars vs units across eras; "less per policy" | FIXED | louisiana-03: "since 1978 ... Today 49.0%"; "buildings"; the inference is removed. |
| 7 | Aid per registration "against" the paid claim | FIXED | The comparison is gone (louisiana-23). |
| 8 | CRS "Yes" for 12%; "county" on a parish page; duplicate Lafayette | PARTLY | "Only some: 42 of the 353" and "A community named for the parish" are fixed. Both Lafayette rows remain (louisiana 13). |
| 9 | Event totals vs year totals, ICC bases | FIXED | louisiana-08/07 captions name the ICC basis in both places: "Event totals include code-upgrade (ICC) payments, which the yearly totals ... leave out." |
| 10 | C/A99/B = $1,086 with "low-risk" note | PARTLY | The note no longer says low-risk. The identical medians and the unproven "common amounts" remain, and the clustering extends to parishes (louisiana 3). |
| 11 | "How often ... Yes" | FIXED | louisiana-20: the heading is now "Do the same homes flood again here?" |
| 12 | Templated, triple purchase rule | PARTLY | The question names now agree. The rule still appears three times, and 56% of prose is verbatim across pages (louisiana 8). |
| 13 | NRI called "a model of expected loss" | FIXED | louisiana-21: "a model of expected loss, adjusted for social vulnerability and resilience". |
| 14 | JSON-LD creator "FEMA OpenFEMA" | FIXED | JSON-LD: `"creator": {"@type": "Organization", "name": "Flood Insurance Data"}`. |

### Palm Beach (11 MAJOR)
| # | R2 item | Status | Evidence |
|---|---|---|---|
| 1 | "Tropical Storm Ian/Nicole" | FIXED | palm-beach-county-fl-18: "Hurricane Nicole", "Hurricane Ian". |
| 2 | NRI EALT labelled "buildings"; never reconciled | PARTLY | The label is fixed ("buildings, people and farmland ... a model, not insurance payouts") and "heavy rain" is gone. It is still not reconciled with $72.0M and $71.1M (palm-beach 7). |
| 3 | "Zone drives your price" | FIXED | Same wording as Louisiana 2 (palm-beach-county-fl-01). |
| 4 | "132,945 policies" in prose | PARTLY | Prose now says "policy units". The meta description says "75,140 policies", and 69,154 "residential policies" is unexplained (palm-beach 8). |
| 5 | Rebuild 50.6% vs 91.5%, subset base | PARTLY | The explanation sentence was added. The headline still covers all homes from the 55% that report (palm-beach 6). |
| 6 | County verification; claims anomaly against neighbours | NOT FIXED | "with every record for Florida"; "not yet compared for Palm Beach County"; the anomalies are unexamined (palm-beach 4, 11). |
| 7 | "Most don't" scare; 2x state rate | PARTLY | The headline is softened. A first-screen tile now gives "43.5% ... paid something", and the 2x rate is unexamined (palm-beach 5). |
| 8 | Outside-zone cross-era; B/C "unclassified"; 58.1 vs 58.2 | PARTLY | The wording is fixed. B and C are still "Other low-risk or unclassified", and the rounding gap remains (palm-beach 17). |
| 9 | Aid "against" the paid claim | FIXED | Removed (palm-beach-county-fl-19). |
| 10 | Templated | PARTLY | Same as Louisiana 12. |
| 11 | JSON-LD creator FEMA | FIXED | creator is "Flood Insurance Data". |

**Round-2 tally (29 MAJOR items): 12 FIXED, 12 PARTLY, 5 NOT FIXED.**

Sources (SERP and rule check):
- [Kiplinger](https://www.kiplinger.com/article/insurance/t028-c000-s002-lessons-from-the-floods.html)
- [Bankrate](https://www.bankrate.com/insurance/homeowners-insurance/cost-of-flood-insurance)
- [NerdWallet](https://www.nerdwallet.com/insurance/homeowners/learn/flood-insurance-cost)
- [MoneyGeek LA](https://moneygeek.com/insurance/flood/louisiana-flood-insurance-costs)
- [Insurify LA](https://insurify.com/homeowners-insurance/louisiana-flood-insurance/)
- [Fox8](https://www.fox8live.com/2023/04/28/flood-insurance-policyholders-voice-frustrations-over-rising-costs)
- [NerdWallet FL](https://www.nerdwallet.com/article/insurance/flood-insurance-florida)
- [MoneyGeek FL](https://moneygeek.com/insurance/flood/florida-flood-insurance-costs)
- [AOL ZIP increases](https://www.aol.com/flood-insurance-costs-soar-south-202537107.html)
- [Citizens flood requirement, news4jax](https://news4jax.com/news/local/2025/09/16/flood-insurance-will-be-mandatory-for-most-citizens-property-insurance-policyholders-by-2027)
- [Citizens](https://www.citizensfla.com/-/new-flood-requirements-begin-january-1)
