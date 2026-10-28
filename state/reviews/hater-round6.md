# Hater round 6 (built dist/ pages + 60 phone screenshots in round6/)

**Method.** I looked at all 60 screenshots: home-00..08, louisiana-00..26 and palm-beach-county-fl-00..23. I pulled the text, title, meta and JSON-LD of the three built pages with their `data-p` paths. I spot-checked the figures against data/states/louisiana/{agg,data,extras}.json and data/c/palm-beach-county-fl/{agg,data,extras}.json. For definitions I read tools/metrics.py, tools/extras_raw.py (to find how `at_building_max_pct` is defined) and the `fl_citizens` rule in tools/rules_registry.py. I did not read the gate code, and I did not run the quote-checker or search-box JavaScript, so neither is verified to work. I wrote the defect list before reading hater-round5.md or fixlog-round5.md.

**SERP (WebSearch, 2026-10-27):**
- "flood insurance cost": Kiplinger, NerdWallet ($899 a year, $75 a month), Bankrate. Policygenius gives $888 from FEMA; Insurify gives a $786 NFIP median.
- "flood insurance cost Louisiana": MoneyGeek ($750 average), Insurify ($1,470 single-family median, and "Plaquemines Parish $4,752, most expensive"), Policygenius ($752, by zone).
- "flood insurance cost palm beach county FL": NerdWallet FL guide (Palm Beach $528; West Palm Beach $349), MoneyGeek ($466), Insurify ($709).

One FEMA rule check: "CRS discount the same in every flood zone" is correct under Risk Rating 2.0. FEMA's manual, the ASFPM fact sheet and Louisiana's 2024 hazard mitigation plan all say so, even though the CSB data still carries a legacy `nonSfhaDiscount` column (Palm Beach: 25% / 10%). That is not a defect.

**Checked and correct:**
- Louisiana: 17th of 51; 3% above the U.S. median; $1,086 / 12 = $91.
- Louisiana claims: unpaid 107,750 = 485,743 − 377,993. Zone shares add up to 51.0%. NRI parish counts add up to 64, and all 64 parishes are in the table.
- Palm Beach: 32% below Florida and 36% below the U.S. ZIP range $450 (33484, n = 640) to $1,825 is the true minimum and maximum. Unpaid claims 6,077 = 10,758 − 4,681.
- Palm Beach: CRS 25 discounted + 15 not = 40 communities, and Palm Beach Gardens and Highland Beach really are class 10 in the CSB.
- Tropical Storm Arthur DR-4927 (2026-06-30) is in the Louisiana declarations data.
- cost_new: Louisiana $1,139 (n = 30,754), Palm Beach $620 (n = 4,112).
- The Citizens rule text matches s.627.351 as cited.

## home

- **BLOCKER** (would not beat #1).
  - **The headline figure:** home-00 leads with "$1,055 U.S. median a year". Every top result shows $786–$899: NerdWallet $899 / $75 a month, Policygenius $888, Insurify $786 median.
  - **No row reconciles it:** the "Why do sites quote different prices?" table (home-03) has no premium-only row. The state pages have one: Louisiana "$859 before the federal fee". A home row like that would land near $899, but here nothing does. All four rows are $995–$1,624, so the table makes our number look even further from everyone else's.
  - **No cost by flood zone:** home has no cost by zone (high-risk A/V vs X). That is the second question every top result answers (NerdWallet, Policygenius, Bankrate). The site holds `cost_by_zone` for every state, but home shows none of it.
  - **Result:** a searcher who sees a number unlike all of Google's, with no zone breakdown, goes back to Google at home-03.
- **MAJOR** (templated).
  - **Shared text:** "Three things to know first" (home-01) is the same waiting-period, purchase-rule and homeowners-exclusion text found on every state and county page, word for word: "Most policies start 30 days after you buy, but there is no wait if you buy it with a new or refinanced mortgage."
  - **Home-specific text:** only the high/low callout and one deductible sentence.
  - **The rest:** two long tables (51 states, 42 counties). A quality rater still sees a directory with shared boilerplate.
- **MAJOR** (gap vs #1, private flood).
  - **One line only:** "Private flood insurance is not in this data" (home-03) is all the page says about private flood. NerdWallet and Bankrate both say whether private flood can be cheaper, when it is allowed in place of NFIP for a mortgage, and that it has no 30-day wait for some carriers.
  - **Not exempt:** the owner exemption covers private *prices*. It does not cover the public rule that lenders must accept private flood (42 U.S.C. 4012a(b)).
  - **Effect:** the reader's obvious next step, "can I get it cheaper elsewhere?", gets no answer.
- **MINOR**. The Citizens sentence (home-01) is now correct, but the tense is off: "outside one, from 2026 if they cost $400,000 or more" is written as if 2026 were still ahead. It is October 2026, so "now required at $400,000+; all Citizens homes from January 1, 2027" reads right.
- **MINOR**. The quote checker placeholder is "e.g. 1200" on home and "e.g. 1800" on every state and county page. That includes Alaska ($368 median) and Palm Beach ($670, where $1,800 is above the 90th percentile). It is a template constant, not a local example.
- **MINOR**. On screen 1 the 4.6M tile sits alone, leaving an empty slot in the 2-column grid (home-00).
- **MINOR**. "NFIP records · 50 states and DC". Puerto Rico, USVI and the other territories are left out without a line saying so.
- **MINOR**. The title promises "by state and county", but only 42 of about 3,100 counties have pages. Nothing says what happens when someone types an uncovered county into the search box (not tested).
- **MINOR**. Home still has no JSON-LD (`grep ld+json` = 0), while the state and county pages carry Dataset markup.

Verdict: FAIL

## louisiana

- **MAJOR** (true but misleading; round-5 item claimed fixed, not fixed).
  - **What the card says:** "Which floods paid out the biggest totals here?" (louisiana-07/08) lists Katrina, the 2016 storms, Ida, Isaac, Rita, Ike and the late-winter 2016 storms. It silently drops `extras.claims.events.2`, FEMA's catch-all "Flooding": 97,855 claims, $1.14 billion, 1978–1998. That includes the May 1995 flood, which is $605.5M on the chart and the 4th costliest year, above Isaac.
  - **The fix log:** it says "Costly years with no named event ... 1995 ..." now appears. It does not: `grep "Costly years"` on the Louisiana page = 0. The fix only names years that are in the top 3, and 1995 is 4th.
  - **Effect:** a Louisiana reader still never sees 1995.
- **MAJOR** (gap vs #2, unreconciled).
  - **The conflict:** Insurify's headline "Plaquemines Parish ... $4,752" sits next to our Plaquemines "$1,231" (louisiana-14).
  - **What we reconcile:** the "why sites differ" table works only at state level. Insurify's $1,470 state median matches our "Full-risk premium plus average fees $1,466" row, but the page never says so.
  - **What we don't:** there is no parish-level full-risk or mean figure, so a Plaquemines reader thinks one site is wrong by 4x.
- **MAJOR** (reader cannot find their parish).
  - **Screen 1:** it has no "find your parish" link. The county page has "find your ZIP" on screen 1.
  - **The parish table:** it starts at louisiana-11, after the claims chart, the unpaid reasons, the events table, the rebuild card and a 27-row zone table.
  - **Search intent:** the searcher's second question ("what about my parish?") is answered 11 phone screens down. This is the point where they go back to Google and click Insurify's parish list.
- **MAJOR** (confusing, contradicts itself).
  - **The note:** "Every zone starting with A or V is high-risk, including older numbered labels such as A1 to A30 (now shown as AE)" (louisiana-02).
  - **The table:** the zone-cost table then prices A01 through A15, V15 and AHB as separate rows (louisiana-10/11), with A06 at "$2,038" next to AE at "$1,247".
  - **Effect:** 27 rows of legacy codes face a homeowner whose determination says "AE". The page tells them these are AE, then prices them differently.
- **MAJOR** (analyst, misleading reassurance).
  - **The two tiles (louisiana-09):** "Rebuilding cost above the building limit (of 212,784 policies reporting one) 21.5%" and "Single-family policies insured to the building maximum 64.8%".
  - **Note text:** "The rebuilding-cost share and the insured-to-the-maximum share count different policies."
  - **What the code actually does:** `at_building_max_pct` = building coverage ≥ $250,000 over *all* single-family policies (extras_raw.py line 60). The rebuild share uses the 73% that report a rebuild cost.
  - **What the figures imply:** a large block of policies is insured above its own reported rebuilding cost, and the NFIP never pays above that cost. Either that, or the rebuild cost is unreported for exactly the high-value homes.
  - **What is missing:** the page explains neither. It also never says that the NFIP pays replacement cost only to primary homes insured to 80% or more of rebuilding cost, which is the real answer to "would it pay to rebuild".
- **MAJOR** (stale headline pool; round-5 item partly fixed).
  - **Headline:** the title, meta, H1 tile and quote checker all use $1,086. That is the mixed 2025/2026-term pool.
  - **Current renewals:** the page's own row says policies whose term began in 2026 pay "$1,215" (170,190 policies), which is 12% higher.
  - **Effect:** a reader renewing now compares a $1,250 bill with "$1,086 typical" and thinks they are overcharged. The "Renewing?" line on screen 1 helps, but the checker still ranks them against the older pool.
- **MAJOR** (scaled, partly fixed).
  - **Still word for word on both pages:** "Already flooded? Insured: report the loss…", the full "Yearly cap: Those prices step up toward full-risk each year…" paragraph, the waiting-period exceptions paragraph, the claim-closure explainer "FEMA lists reasons a claim closes without payment…", and "Premium before fees, single-family primary homes. Elevated and other buildings here differ…" (louisiana-05, -07, -18, -19 vs palm-beach-county-fl-05, -07, -14, -15).
  - **Effect:** on a 3,000-page site, this is still the shared-text pattern.
- **MINOR**. The screen-1 tile says "Many unpaid claims are no-damage or paperwork closures." The page's own top reason is "Not an actual flood" (20,318), which is a coverage denial. No-damage plus assigned-in-error is 24% of unpaid claims. The same sentence appears on Palm Beach, where the reasons differ.
- **MINOR**. "Mid summer severe storms (2016)": the data label is "Mid-summer severe storms", so the hyphen was lost. Readers know it as the August 2016 flood.
- **MINOR**. The parish order puts "Jefferson Davis" before "Jefferson" and "LaSalle" before "Lafayette" (case-sensitive sort, louisiana-13).
- **MINOR**. The stat card "56.6% of 292,018" (louisiana-18) is two numbers jammed into one headline figure.
- **MINOR**. The elevated vs not-elevated premiums, "$854" vs "$859", tell a scared reader that elevating does nothing. A caveat is present, but the tile invites the wrong conclusion.
- **MINOR**. The chart footnote still uses ten-digit dollars, "2005 ($13,559,493,222)", next to "$13.3 billion" in the events table.
- **MINOR**. 2025 and the partial year 2026 are on the claims chart with no "claims still open" flag.
- **MINOR**. "67 federal disasters for floods or storms here" gives no period. "2021 — Severe Storms, Tornadoes, and Flooding" is listed as a "distinct storm".
- **MINOR**. The dates disagree: "downloaded October 25, 2026" (louisiana-01) vs "The newest of these downloads was October 26, 2026" (louisiana-25).
- **MINOR**. JSON-LD says "NfipPolicies v3 and NfipClaims v3", but the `citation` URLs are the "-redacted-policies-v2" / "-claims-v2" pages.
- **MINOR**. Per-parish penetration (data.json `penetration.by_county`, e.g. Jefferson 64.9%) and multiple-loss counts are in the data but not in the parish table. The state card gives only the state total.
- **MINOR**. The state page has no NOAA storm-events panel, while the county page does. That breaks the "we are the dataset catalog" promise at state level.
- **MINOR**. The hero tile "Below full-risk price: bills step up yearly" uses unexplained jargon on screen 1.

Verdict: FAIL

## palm-beach-county-fl

- **MAJOR** (scary figure on screen 1, unexplained).
  - **Screen 1 tile (palm-beach-county-fl-01):** "Does it pay out here? 43.5% of claims here paid something (Florida: 69.9%); the average paid claim was $15,396."
  - **What the reader takes from it:** a homeowner who has just flooded reads "my claim probably won't pay".
  - **What the page doesn't say:** whether the 6,077 unpaid claims come from particular years (1979, 1999 Irene and 2004 had many small claims) or are spread evenly. Nothing is checked against a FEMA county figure either. The fix log cites "98% of claims in Palm Beach ZIPs carry county code 12099", but that proof is not on the page and I could not see it.
  - **Weak backing:** the card under it now says "many with no specific reason recorded". The data shows reasons for 86.9% of unpaid claims (`unpaid_with_reason_pct`), so even that line is weak.
- **MAJOR** (analyst, misleading reassurance).
  - **The tiles (palm-beach-county-fl-09):** "Rebuilding cost above the building limit 50.6% (of 27,755)" vs "Single-family policies insured to the building maximum 91.5%".
  - **Coverage of the rebuild figure:** only 55% of the 50,781 policies report a rebuild cost.
  - **What the 91.5% means:** coverage ≥ $250,000 across all single-family policies, so roughly 40% or more appear insured above their own reported rebuild cost.
  - **Wrong explanation:** the note says the two shares "count different policies". That is not the real explanation.
  - **Damage figure:** "Damage was more than the coverage 0.8%" sits beside it unexplained.
- **MAJOR** (scaled, partly fixed). The same shared paragraphs appear word for word as on the Louisiana page: "Already flooded?", "Yearly cap", the waiting-period exceptions, the claim-closure explainer, the elevated-premium caveat, the penetration and aid definitions, and the "Many unpaid claims are no-damage or paperwork closures" tile.
- **MAJOR** (gap vs #1, private flood and Citizens context).
  - **Why it matters here:** Florida is the state where private flood is a real alternative (NerdWallet FL covers it), and where Citizens customers are being pushed to buy flood.
  - **What the page gives:** one clause, "through the federal NFIP or a private insurer". There is no line on whether a lender or Citizens accepts private flood, and nothing on how a $670 NFIP median compares.
  - **Effect:** the reader's next step after "am I required?" (where to buy cheapest) is left open.
- **MINOR**. ZIP table (palm-beach-county-fl-11): "33437" and "33446" still have no town (Boynton Beach / Delray Beach postal areas). "33428 Watergate" is a Census CDP name; residents say Boca Raton. Not fixed from round 5.
- **MINOR**. Two near-identical dollar totals mean different things: NFIP "$72.0 million in payouts since 1978" (palm-beach-county-fl-06) and NOAA "$71.1 million in property damage" since 1996 (palm-beach-county-fl-18). A reader merges them.
- **MINOR**. NRI: the inland tile says "Relatively High", while the text says inland per-dollar loss "is higher than in about 30% of U.S. counties" and the modeled loss is "$178.9 million … a year" against $72.0M paid in 48 years. It is caveated, but it is still the screenshot a competitor would mock.
- **MINOR**. The events table silently drops Hurricane Opal 1995 ($1.36M, more than the listed Wilma $1.12M) and the catch-all "Flooding" ($1.64M, which would rank 5th). The "Costly years" note mentions only 2025.
- **MINOR**. "Why do sites quote different prices?" has no row near NerdWallet's $528 or MoneyGeek's $466 apart from "premium only $507", and it does not say that NerdWallet's figure includes commercial policies.
- **MINOR**. The "No CRS discount (15)" list is not alphabetical: "Westlake; Atlantis; Belle Glade; …".
- **MINOR**. Dates: "1978–2026" (en dash) vs NOAA "1996-2025" (hyphen); "downloaded October 25" vs "newest … October 26, 2026".
- **MINOR**. The checker placeholder "e.g. 1800" is above this county's 90th percentile ($1,297).
- **MINOR**. The hero tile "29.5% Below full-risk price: bills step up yearly" appears where the median premium ($507) is within $7 of full-risk ($514).
- **MINOR**. JSON-LD has the same v3 text vs v2 citation URLs as Louisiana.

Verdict: FAIL

## Classes

**Every state and county page (shared template):**
- The rebuild card's "count different policies" note is wrong: the insured-to-max share is coverage ≥ $250K over all single-family policies, and the rebuild share is over reporters only. There is no explanation of policies insured above their own rebuild cost, and no 80%-of-replacement-cost rule.
- The event table drops FEMA's catch-all "Flooding" and small-n events. The "Costly years" fallback covers only the top-3 years, so Louisiana's 1995 (4th) is still lost.
- Shared paragraphs are word for word the same: Already flooded, Yearly cap, waiting-period exceptions, the claim-closure explainer, the elevated caveat, and the "Many unpaid claims are no-damage or paperwork closures" tile (which is wrong where the top reason is a denial).
- The headline and checker use the mixed-term pool, not the latest term.
- The checker placeholder is a constant ("e.g. 1800"), not the local median.
- Nothing on private flood: whether lenders and Citizens must accept it, or why someone would shop it.
- Ten-digit dollars in chart notes. Partial and open claim years are not flagged. Download dates disagree (Oct 25 vs Oct 26). JSON-LD says v3 but cites v2 URLs.
- "Below full-risk price" jargon on screen 1.

**State template:**
- There is no parish/county jump link on screen 1, and the county table sits about 11 screens down.
- The zone-cost table lists legacy numbered zones as separate rows right after saying they "now show as AE".
- There is no county-level full-risk or mean figure to reconcile competitor county numbers (Insurify Plaquemines $4,752).
- County penetration and multiple-loss data are fetched but not shown. There is no NOAA panel.
- Table sort is case-sensitive.

**County template:**
- Screen-1 payout ratio vs state with no era breakdown or external check.
- ZIP town labels are blank or CDP-named.
- The NRI modeled-loss figure sits beside the much smaller NFIP and NOAA totals.

**Home template:**
- The headline median is not reconciled with the $786–$899 every top result shows (no premium-only row).
- No national cost by flood zone.
- The shared "Three things" text.
- No JSON-LD.
- Territories missing without a note.

## Previous items (round-5 BLOCKER/MAJOR)

home
- BLOCKER Citizens rule wrong today: **FIXED**. home-01 now reads "need it in a high-risk zone since 2023; outside one, from 2026 if they cost $400,000 or more … and from 2027 for all others". That matches the registry text and §627.351. Only a tense minor remains.
- BLOCKER no drivers / no way to pay less / no checker: **FIXED**. home-01/02 has "Is my quote normal?", "What sets the price, and how do I pay less?" and the U.S. deductible mix ($1,250, 51.7%). The checker script was not run by me.
- MAJOR no mean or all-types figure for the $888/$899 averages: **PARTLY**. The rows $1,252 / $1,624 were added (home-03), but there is no premium-only row, and nothing lands near $899. Logged as part of this round's BLOCKER.
- MAJOR directory / templated: **PARTLY**. The answer cards now sit before the tables, but "Three things to know first" is still the shared text.

louisiana
- BLOCKER $1,466 existing full-risk sold as a new policy's price: **FIXED**. The claim and checker line are gone. "Buying? … $1,139" (n = 30,754) matches the data, and the $1,466 row is now labelled "what these existing policies would cost at FEMA's full price".
- MAJOR 1995 hidden under the catch-all label: **NOT FIXED**. The fix log says "Costly years with no named event ... 1995", but `grep "Costly years"` on the Louisiana page returns 0. The fallback only covers top-3 years, and 1995 is 4th.
- MAJOR clustered $1,086 medians unexplained: **PARTLY**. The note now says "many policies here are charged exactly the same amount" (louisiana-11), but it gives no amount, count or share. Round 5 measured about 21,700 policies at $1,083–1,086 / $1,266–1,267.
- MAJOR "official policy count … not yet compared": **PARTLY**. The sentence is removed (`grep` = 0), but the comparison was never done. The admission was hidden, not resolved.
- MAJOR gap vs #1 (how to lower; Plaquemines conflict): **PARTLY**. The "Can I pay less?" card exists (louisiana-18/19), but the parish-level conflict with Insurify's $4,752 is still unreconciled.
- MAJOR scaled shared text: **PARTLY**. The counting notes moved to methodology, but Already flooded, Yearly cap, waiting exceptions and the claim-closure explainer are still word for word the same as Palm Beach.
- MAJOR 2025 vs 2026 pools: **PARTLY**. The "Renewing? … $1,215" line is on screen 1, but the title, meta, hero and checker still use the mixed $1,086.

palm-beach-county-fl
- BLOCKER new-policy price ran the wrong way: **FIXED**. "Buying? … $620" (n = 4,112) matches extras.json, and the claim is removed.
- BLOCKER Citizens short and long forms wrong or contradictory: **FIXED**. The long form (palm-beach-county-fl-02) has the SFHA requirement since 2023 (April 1 / July 1) plus the rebuild-cost phase-in, and the short form agrees.
- MAJOR prices table lacked mean / all-types rows: **FIXED**. "$882" and "$1,243" rows are present (palm-beach-county-fl-13). A residual minor remains: no row explains NerdWallet's $528.
- MAJOR extreme county figures unverified: **NOT FIXED**. The same 43.5% / 45.5% / $15,396 are still there, now on the screen-1 tile. There is no external check or era breakdown on the page, and the fix log's ZIP-code proof is not shown or verifiable.
- MAJOR NRI defined two ways / order mismatch: **FIXED**. There is one definition ("weighs modeled loss with social vulnerability and community resilience"), and the lead order coastal-then-inland matches the tiles (palm-beach-county-fl-17).
- MAJOR "official policy count … not yet compared": **PARTLY**. The line is removed, but the check was not done.
- MAJOR no how-to-lower: **FIXED**. The "Can I pay less?" card has the 70.8% / 22.5% / 3.9% / 1.4% deductible mix and the elevated $856 vs $506 premiums (palm-beach-county-fl-14/15).
- MAJOR scaled shared text: **PARTLY**. Same as Louisiana.

Tally: 19 items. FIXED 8, PARTLY 9, NOT FIXED 2.
