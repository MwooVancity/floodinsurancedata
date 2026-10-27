# Hater round 5 (full review, built dist/ pages + 57 phone screenshots in round5/)

Method: I looked at all 57 screenshots (home-00..06, louisiana-00..25, palm-beach-county-fl-00..23), read the title, meta, H1 and JSON-LD of the three built pages, and checked numbers against data/ JSON. I also recomputed four figures myself from the raw OpenFEMA policy files in `.cache/raw/NfipPolicies/` (in-force rows effective 2025-08..2026-07, occupancy 1/11, primary residence). I read tools/metrics.py and tools/rules_registry.py for definitions. I did not read the gate code. I read the round-4 review only after writing the defect list below.

SERP (WebSearch, 2026-10-27):
- "flood insurance cost": Kiplinger ($888 avg, Policygenius/FEMA), NerdWallet ($899/yr, $75/mo, by state and by FL county, drivers, ways to save), Bankrate. They all give one national average plus a by-state list, what drives the price and how to lower it.
- "flood insurance cost Louisiana": MoneyGeek ($750 avg), Insurify ($1,470 single-family median, "Plaquemines Parish most expensive at $4,752"), Policygenius ($752; $560 in B/C/X; by zone).
- "flood insurance cost palm beach county FL": NerdWallet FL guide (Palm Beach County $528 avg, West Palm Beach $349, NFIP incl. commercial), MoneyGeek FL ($466), Insurify ($709).

Checked and correct (no defect): LA 17th of 51; LA +3% vs U.S.; PB −32% vs FL and −36% vs U.S.; PB "8th lowest of 55 Florida counties with 100+ priced policies" (recomputed from states/florida/agg.json); LA unpaid reasons sum to 107,750 = 485,743 − 377,993; PB unpaid reasons sum to 6,077; LA zone shares sum to 51.0% high-risk; NRI parish counts sum to 64; Tropical Storm Arthur DR 2026-06-30 is in the declarations data. The three zone medians of $1,086 on the LA page (C, A99, B) are real: raw rows show 7,222 single-family policies at exactly $1,084, 5,440 at $1,086 and about 9,100 at $1,266–1,267. My Zone X median was $1,081 and the state median $1,086.

## home

- **BLOCKER** (SEO, would not beat #1). NerdWallet and Kiplinger answer "flood insurance cost" with a national figure, a by-state table, what drives the price (zone, elevation, building, coverage, deductible) and how to lower it. Our home page has the figure, the state table and the county table, and nothing on price drivers or lowering the cost. The site already holds data for this (deductible mix in extras.json, e.g. LA 53.2% at $1,250; elevated vs not-elevated premiums; CRS discounts), but none of it reaches the home page. Home also has no quote checker, while every state and county page has one. A searcher who wants "why is mine so high / how do I pay less" goes back to Google after home-02.
- **BLOCKER** (wrong rule a reader can act on). home-01 says: "In Florida, homes insured by Citizens with wind cover need it in any zone." As of today (Oct 2026) that is false for a Citizens home outside the SFHA that costs less than $400,000 to rebuild. Its requirement starts January 1, 2027 (Citizens notice and §627.351, the same sources the registry cites for `fl_citizens`). The sentence also contradicts the site's own longer rule on the county page. A Florida reader with a $300K X-zone home is told they are already non-compliant.
- **MAJOR** (gap vs #1, expectations). Our "$1,055 U.S. median" sits beside every top result's "$888 / $899 average". The "Why our prices differ" card (home-01/02) explains this in words, but it never shows the mean or the all-policy-type figure that would land near $899. The reader has to take the explanation on trust. The state pages print that reconciliation table and the home page does not.
- **MAJOR** (thin/templated). Below the fold the page is "Three things to know first" (the same purchase, waiting-period and homeowners-exclusion text that appears on every state and county page) plus two long tables. The only home-specific text is the high/low callout. For a YMYL money query, a Google quality rater would class this as a directory page, not an answer page.
- **MINOR**. "County pages: 42 counties so far, the ones with the most policies first" (home-04). The list is sorted by policies, but it is not the top 42: Kanawha County, WV (1,283 units) and St. Louis County, MO (3,126) are listed, while much larger counties are not. Read naturally, the sentence says these are the 42 biggest.
- **MINOR**. home-03: the "Florida" row renders as plain black text with no underline, unlike every other state. The HTML link exists (`/flood-insurance/florida/`), so this is probably the visited-link colour, but on a phone it looks like the one state without a page.
- **MINOR**. "Insured units in force on July 31, 2026" and "4.6M": the base (units, not policies) is explained in grey small print below. Competitors say "policies", so the bigger number can look inflated.
- **MINOR**. Home has no JSON-LD while the state and county pages carry Dataset markup. This is not wrong, just inconsistent.

Verdict: FAIL

## louisiana

- **BLOCKER** (misleading figure a shopper acts on). louisiana-16/17 say: "a new one is priced at full risk: about $1,466 with fees", the row "Full-risk premium plus average fees $1,466 — close to what a new single-family policy pays", and in the checker (louisiana-01) "A new policy is priced at FEMA's full-risk rate, so a fair new quote can land high." $1,466 is the median full-risk premium of the existing stock ($1,220) plus mean fees ($246). That stock is weighted toward older, higher-risk buildings still on the glide path. People who actually bought recently pay much less. In the raw in-force files, Louisiana single-family primary policies with `originalNBDate` in the last 12 months have a median policyCost of **$1,139** (n = 30,622). Since Risk Rating 2.0 (Oct 2021) the figure is $1,099 (n = 76,815), and the site's own extras.json gives a $869 median *premium* for post-RR2.0 policies. The page tells a buyer holding a $1,450 quote that it is normal, when real new buyers' median is about 22% lower.
- **MAJOR** (analyst, true but misleading). "Which floods paid out the biggest totals here?" (louisiana-08) leaves out FEMA's catch-all "Flooding" label: 97,855 claims and $1.14B across 1978–1998, including the May 1995 flood. On the chart, 1995 ($605.5M) is the 4th costliest year, above Isaac 2012 ($529.9M). The footnote about "a catch-all label spanning many years" is accurate. But a Louisiana reader scanning "biggest floods here" never sees 1995. The page should show the 1995 year total as its own row ("1995 floods, unnamed in FEMA's data").
- **MAJOR** (clustered medians, unexplained). Zone C, Zone A99 and Zone B all show "$1,086", the same as the state median (louisiana-10). The note says only: "Some zones share the same median; each is computed from that zone's own policy records." I recomputed it and the numbers are right: about 21,700 single-family policies sit at exactly $1,083–1,086 or $1,266–1,267. But the page does not say so. To an analyst or a competitor it looks like a fill-down bug, and it is the obvious screenshot to mock.
- **MAJOR** (trust). louisiana-24: "FEMA also publishes a separate official policy count, which we have not yet compared for Louisiana." The page admits its headline count is unchecked against FEMA's own published state figure. A YMYL rater reads that as "not verified".
- **MAJOR** (gap vs #1). Policygenius and Insurify cover price by zone and parish, which we match or beat. Both also cover how to lower the bill (deductible, elevation certificate, CRS). We print CRS, but not the deductible mix (53.2% at $1,250, 34.5% at $2,000, from extras.json) or the elevated vs not-elevated premiums. Those are reader questions the page's own data answers. Insurify's headline "Plaquemines $4,752, most expensive" conflicts with our Plaquemines $1,231. Our "why sites differ" table explains median vs mean statewide, but never at parish level, so a reader comparing the two sites thinks one of them is wrong.
- **MAJOR** (scaled/templated). The purchase rule appears three times: the screen-1 tile, the "Am I required to buy it?" card, and "is under 'Am I required to buy it?'" in the outside-zone card. The waiting-period rule appears twice (tile plus card). These cards are word for word the same on the Palm Beach page: "Yearly cap", the rebuild-cost explainer, the CWOP explainer, "Already flooded?", the penetration definition and the disaster-aid caveat. On a 3,000-page site this is the shared-text pattern that gets a page demoted as scaled content.
- **MAJOR** (2025 vs 2026 pools). The headline $1,086 and the quote checker use the mixed pool. The 2026-term figure ($1,215, 170,190 policies) is the one a renewing reader will see, and it is 12% higher. It appears only as a secondary line on screen 1.
- **MINOR** (mixed bases, disclosed). "Average paid claim $55,453, incl. ICC" and "Total paid $20,682,152,359: net building + contents". Multiplied out, 377,993 × $55,453 = $20.96B, which is not $20.7B. The text discloses this, but two figures in adjacent cards do not reconcile on a phone.
- **MINOR**. "$1,466 = full-risk median + *average* fees" mixes a median and a mean. The reserve-fund assessment is about 18% of premium, so on a $1,220 premium it is about $220, not the $174 mean.
- **MINOR**. Hero: "$90 a month". $1,086 ÷ 12 = $90.50, which rounds to $91 by ordinary rounding (this looks like banker's rounding). The CSV says $90 too.
- **MINOR**. Chart footnote (louisiana-06): "2005 ($13,559,493,222)". Ten-digit dollar figures are unreadable on a 390px screen and inconsistent with "$13.3 billion" in the event table.
- **MINOR**. The chart includes 2025 and partial 2026 (claims still open and developing) with no "year in progress / claims still open" flag.
- **MINOR**. "67 federal disasters for floods or storms here" gives no period (since 1953?). The list labels "2021 — Severe Storms, Tornadoes, and Flooding" as a "distinct storm".
- **MINOR**. Dates disagree: "downloaded October 25, 2026" (louisiana-01) vs "The newest of these downloads was October 26, 2026" (louisiana-25). The multiple-loss panel says retrieved October 26.
- **MINOR**. Hero tile "56.6% BELOW FULL-RISK PRICE: BILLS STEP UP YEARLY" uses the jargon "full-risk price" on screen 1, unexplained until screen 18.
- **MINOR**. JSON-LD says "OpenFEMA NfipPolicies v3 and NfipClaims v3", but its `citation` URLs point to the "...-redacted-policies-v2" / "-claims-v2" pages.

Verdict: FAIL

## palm-beach-county-fl

- **BLOCKER** (misleading figure a shopper acts on). palm-beach-county-fl-12/13: "a new one is priced at full risk: about $710 with fees", and in the checker "a fair new quote can land high". Recomputed from the raw FL files (censusGeoid 12099, single-family primary, in force): policies first bought in the last 12 months have a median cost of **$620.50** (n = 4,112), and post-RR2.0 policies $612 (n = 20,769). That is *below* the $670 existing median. extras.json agrees: new-policy median premium $458 vs older policies $544. Here the page's whole "new is pricier" story runs the wrong way. A Palm Beach buyer with a $700 quote is told it is typical, when recent buyers' median is about $620.
- **BLOCKER** (wrong rule, Florida). palm-beach-county-fl-00/01 tile: "In Florida, homes insured by Citizens with wind cover need it in any zone." This is false today for non-SFHA homes under $400K, whose requirement starts January 1, 2027. The long version (palm-beach-county-fl-02) is also wrong by omission: "must also carry flood insurance, in any flood zone: from January 1, 2026 if it would cost $400,000 or more to rebuild, and from January 1, 2027 for all other Citizens homes." That leaves out that Citizens homes **in the SFHA have been required to carry flood since 2023 regardless of value** (Citizens 2023 notice; §627.351). A reader with a $300K AE-zone Citizens home reads that they have until 2027 and risks non-renewal. The two versions on one page also contradict each other.
- **MAJOR** (gap vs #1). NerdWallet's Palm Beach figure is "$528 avg" (NFIP, includes commercial). Our "Why do sites quote different prices for Palm Beach County?" table (palm-beach-county-fl-12/13) has no mean row and no all-policy-type row. The Louisiana table has both ("Average (mean) cost" / "Average cost, every policy type"). So on the one page where a reader holds NerdWallet's $528 against our $670, the reconciliation row is missing.
- **MAJOR** (extreme county figures, unverified). "43.5% of claims here paid something (Florida: 69.9%)", "45.5% of the flood-insurance claim money … went to buildings outside the high-risk zones" (Florida 8.1%), and an average paid claim of $15,396 vs Florida $61,756. Each is 3–6x off the state figure, and the only caveat is the county-code matching note. Nothing tests these against a FEMA-published county figure. If the county-code join is wrong, these are the most mockable numbers on the site.
- **MAJOR** (NRI contradicts itself on one page). palm-beach-county-fl-16 calls it "FEMA's plain risk rating", while palm-beach-county-fl-19 calls the same rating "FEMA's model of expected loss, adjusted for social vulnerability and community resilience." The headline says "Relatively High for river flooding and Relatively High for coastal", but the tiles are ordered Coastal then Inland. "Inland: … $178.9 million … per dollar of building value, that loss is higher than in about 30% of U.S. counties" sits under a "Relatively High" inland tile. A frightened homeowner reads "high risk, but lower than 70% of counties" in one card.
- **MAJOR** (trust). palm-beach-county-fl-21: "FEMA also publishes a separate official policy count, which we have not yet compared for Palm Beach County."
- **MAJOR** (gap vs #1). The page lacks "how to lower it". The data is present and unused: 70.8% of policies carry the $1,250 deductible, and the elevated median premium is $856 vs $506 not elevated (n = 440, which looks counter-intuitive and needs its caveat). CRS is shown.
- **MAJOR** (scaled/templated). The same shared blocks as the Louisiana page appear word for word (purchase rule three times, waiting rule twice, cap, rebuild explainer, CWOP, Already flooded, penetration and aid definitions). Only the numbers change.
- **MINOR**. ZIP table (palm-beach-county-fl-11): "33437" and "33446" have no town name (Boynton Beach / Delray Beach postal areas) while the other six do. "33428 Watergate" is a Census CDP name that residents would call Boca Raton.
- **MINOR**. There are five different policy counts within a few screens: 75,140 records, 132,945 units, 69,154 residential policies, 50,781 single-family, and 27,755 reporting a rebuild cost. Each is labelled, but on a phone the reader cannot tell which one "policies here" means.
- **MINOR**. The chart flags 2025 as the 3rd costliest year ($6,857,416 from 99 claims). No event explains it, and claims from the year are still open. The 2026 bar is a partial year with no flag.
- **MINOR**. "Data effective 1978–2026" for claims vs "1996-2025" for NOAA, and "downloaded October 25" vs "newest … October 26, 2026". The dates are in different formats and disagree.
- **MINOR**. Hero "29.5% BELOW FULL-RISK PRICE: BILLS STEP UP YEARLY" while the median premium ($507) is within $7 of the median full-risk premium ($514). The tile implies rising bills for a county where most policies are at or near full risk.
- **MINOR**. JSON-LD has the same v3 text vs v2 citation URLs as Louisiana.

Verdict: FAIL

## Classes

**Every state and county page (shared template):**
- The "new policy ≈ full-risk median + mean fees" claim, and "a fair new quote can land high" in the checker. It uses the wrong population (existing stock instead of recent buyers). Fix it once from `originalNBDate` in the last 12 months and print that median.
- Citizens text (`fl_citizens`, `fl_citizens_short`) on every Florida page and on home: the short form is false until 2027 for non-SFHA homes under $400K, and the long form omits the SFHA requirement that has applied since 2023.
- "FEMA also publishes a separate official policy count, which we have not yet compared": an unverified-count admission on every page.
- Shared paragraphs are word for word identical across pages: the purchase rule printed three times, the waiting rule twice, plus cap, CWOP, rebuild, Already flooded, aid and penetration definitions.
- No "how to lower it" panel, although deductible and elevation data are already in extras.json.
- Event table drops catch-all FEMA labels with no year fallback (Louisiana loses 1995).
- Zones that share a median get no explanation of the mass point at one price.
- Partial and still-developing claim years (2025 and 2026) appear on the chart with no flag.
- Download dates disagree (Oct 25 in the header vs Oct 26 in the dataset list). JSON-LD says v3 but cites v2 URLs.
- Jargon "full-risk price" on screen 1. $X/12 monthly uses banker's rounding.

**County template only:**
- The "why sites differ" table lacks the mean and all-types rows that the state table has, so it cannot reconcile NerdWallet or MoneyGeek county averages.
- NRI is defined two different ways on the same page ("plain risk rating" vs "adjusted for social vulnerability"), and the headline order (river then coastal) does not match the tile order.
- County vs state ratio figures (paid share, outside-SFHA dollars, average claim) have no plausibility check against FEMA county data.
- ZIP town labels are blank for some ZIPs.

**Home template:**
- Directory plus shared "three things" text. No price drivers, no ways to save, no checker, no mean figure to reconcile with the $888/$899 averages every top result shows.
- The Citizens short rule (above).

## Previous items (round 4 BLOCKER/MAJOR)

home
- BLOCKER SEO: **NOT FIXED**. The page still has no price drivers, no how-to-lower and no checker (home-00..06). A named author is no longer a defect (owner 2026-10-27).
- MAJOR no named person/contact: **WAIVED** (owner 2026-10-27, anonymous by choice).

louisiana
- BLOCKER SEO: **PARTLY**. The reconciliation table and the zone and parish tables are present. How to lower it (deductible and elevation) is still absent. Cost by home value is waived only if the page says it is unavailable, and the limits line lists "your own premium, private prices, your exact zone" but not home value.
- MAJOR 2025 vs 2026 terms: **PARTLY** (unchanged since round 4). The split is shown, but the headline and checker still use the mixed $1,086 pool.
- MAJOR clustered medians: **NOT FIXED**. The text is now weaker: "Some zones share the same median; each is computed from that zone's own policy records." No amount, share or cause is given. The raw data shows about 21,700 policies at $1,083–1,086 / $1,266–1,267.
- MAJOR parish towns: **PARTLY**. The claim was narrowed to "Parishes with their own page list their towns" (louisiana-20), which is now true. Still only 5 of 64 parishes are linked.
- MAJOR FEMA count: **NOT FIXED** (louisiana-24, same sentence).
- MAJOR scaled content: **NOT FIXED** (the triple purchase rule and shared blocks remain word for word).

palm-beach-county-fl
- BLOCKER SEO: **PARTLY**. ZIP lookup, Citizens rule and reconciliation table are present. How to lower it is absent, and the reconciliation table lacks the mean rows (new MAJOR above). Private prices are waived (the page says they are not in the data).
- MAJOR extreme county figures: **NOT FIXED** (same 45.5% / 43.5% / $15,396 with only the county-code caveat).
- MAJOR payout tile: **PARTLY** (unchanged; the caveat is on the tile, but the figure is unchecked).
- MAJOR NRI $178.9M vs payouts: **FIXED**. palm-beach-county-fl-17 now says: "Any loss figure is a whole-county model estimate of all flood loss, insured or not, averaged per year, so it runs far above the insurance payouts shown elsewhere on this page." A different NRI defect (two definitions on one page) is logged above.
- MAJOR counts 69,154 vs 132,945: **FIXED**. The tile now reads "Residential policies in FEMA's insured-homes count (each condo building counts once)".
- MAJOR scaled content: **NOT FIXED**.
- MAJOR state-level verification: **NOT FIXED** (palm-beach-county-fl-21, same sentence).

Tally: 15 items. FIXED 2, PARTLY 5, NOT FIXED 7, WAIVED 1.
