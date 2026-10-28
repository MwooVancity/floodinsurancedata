# Hater round 9 (built dist/ pages + 87 phone screenshots in round9/)

**Scope (narrowed by the caller):**
1. home, louisiana, palm-beach-county-fl passed round 8. Verify the four text edits made since then, then skim every screenshot for anything wrong or misleading.
2. broward-county-fl has never been reviewed. It was flagged because its unpaid-claim share sits 20+ points from Florida's. Full truth review: spot-check figures against its data files, check the claims are Broward's, and check every rule.

No SEO search this round. GAPs are carried over or ranked from the data; at most five per page.

**Method:**
- **Pages:** I extracted the visible text and inline scripts (quote checkers, ZIP lookup `ZD`) of all four built pages.
- **Screenshots:** I looked at every screenshot, home-00..08, louisiana-00..27, palm-beach-county-fl-00..24 and broward-county-fl-00..24, as 4-up sheets at native 390px width.
- **Data:** I recomputed the figures from `data/c/broward-county-fl/{agg,data,extras}.json`, `data/states/florida/{agg,extras,data}.json` and `data/us/cost_hist.json` (pooled: n = 2,351,712; p25/p50/p75/p90 = 713/1,055/1,309/2,150).
- **Rules:** I read the rule text and sources in `tools/rules_registry.py`. I did not re-fetch the statutes this round.
- **Not read:** the gate code, apart from one grep in `build_page.py`/`extras_raw.py` for how the decade and rebuild fields are defined.
- **Not run in a browser:** the checkers and the ZIP lookup. I computed their outputs from the scripts.

**The four edits:**
- **(a) By-decade header: VERIFIED.** It reads "Decade of the flood / Claims filed / Share that paid something" on louisiana, palm-beach-county-fl and broward-county-fl. Every row on all three pages matches `extras.claims.by_decade` exactly:
  - **Louisiana:** 13,341/87.8%, 68,083/83.7%, 73,706/84.6%, 237,464/72.8%, 63,662/82.6%, 29,487/72.9%.
  - **Palm Beach:** 856/54.4%, 1,100/48.2%, 3,004/52.8%, 3,514/34.9%, 1,858/39.0%, 426/34.7%.
  - **Broward:** 2,171/44.1%, 1,805/38.2%, 9,570/53.9%, 10,239/33.8%, 5,197/46.7%, 6,067/78.3%.
  - **Totals:** the decade counts sum to the all-claims totals (485,743; 10,758; 35,049).
- **(b) ZIP note: VERIFIED** on both county pages. It reads "ZIPs exactly as FEMA recorded them on policies here; a ZIP with only a policy or two may be a ZIP from elsewhere, as entered on the policy." This now honestly covers the far-away single-unit ZIPs: Palm Beach 32507/32333/344xx, and Broward 30362 (Atlanta area), 33032, 33036 and several Miami ZIPs.
- **(c) Quote checker (state and county): VERIFIED.** The code is `v<=P.p25` → "in the cheapest quarter".
  - **Louisiana** (P = 863/1,086/1,273/1,905):
    - $863 → "$863 is in the cheapest quarter of existing policies here (half pay $863 to $1,273, typical $1,086). Renewing? Policies whose term began in 2026 typically pay $1,215."
    - $1,086 → "$1,086 is the typical cost here (…)".
    - $800 → "$800 is in the cheapest quarter …".
  - **Palm Beach and Broward:** the same script. Palm Beach $517 / $670 / $500 and Broward $660 / $831 / $500 print "cheapest quarter" / "the typical cost here" / "cheapest quarter".
  - **The input:** it is `type=number`, so "1,200" cannot be misparsed as 1.
- **(d) Home checker at the median: VERIFIED.** $1,055 → "$1,055 is right at the middle of U.S. single-family policies (half pay $713 to $1,309)." The other bands: $713 → "in the lowest quarter"; $500 → "in the lowest quarter"; $1,309 → "in the top quarter"; $2,150 → "in the top tenth". The bounds match the pooled national histogram.

## home

- **MINOR** (new, wording mismatch).
  - **The two wordings:** the home checker says "in the lowest quarter", while the state and county checkers now say "in the cheapest quarter". Home says "right at the middle"; the others say "the typical cost here".
  - **Why it matters:** a reader who uses both sees two phrasings for the same band. Polish only.
- **MINOR** (carried over). "42 counties so far, listed by number of policies" (home-04). The column and the sort are "Insured units".
- **MINOR** (carried over). The search box prints nothing when no row matches.
- **MINOR** (carried over). "3,490,299 NFIP policy records" sits next to "4.6M insured units" on screen 1 (home-00). The note explains it.
- **GAP 1.** No cost by flood zone on home.
- **GAP 2.** No row naming the SERP's figures ($899 NerdWallet, $888 Policygenius, $786 Insurify) against our rows.
- **GAP 3.** Private flood: when a lender must accept it, and its price.
- **GAP 4.** No line on territories (PR, USVI, Guam).
- **GAP 5.** No JSON-LD on home.

**Screenshot skim (home-00..08):** nothing wrong or misleading.
- The Citizens line on screen 1 matches `fl_citizens_short`.
- The "Buying? $995 (197,562 policies)" line agrees with the "Why do sites quote different prices?" table.
- The state table holds 51 rows, sorted by median.
- The county table is sorted by insured units.

Verdict: PASS

## louisiana

- **MINOR** (carried over, rcv_80). "The NFIP pays the cost to rebuild (not a depreciated value) only for … insured for at least 80%…" (louisiana-08/09) leaves out the under-80% settlement: the greater of actual cash value or a proportional share of rebuilding cost.
- **MINOR** (carried over, checker). The checker is now right at p25. But a cost between p25 and p50 (e.g. $900) still prints "cheaper than about half of existing policies", when $900 is cheaper than roughly 70%. The input's aria-label is "Your annual premium in dollars", while the prompt asks for premium plus fees.
- **MINOR** (carried over). "Among the five costliest years, these have no named event in this table …: 1995" (louisiana-08) uses a plural subject for one year.
- **MINOR** (carried over). "Half of homeowners here pay between $863 and $1,273" means half of single-family primary-home policies.
- **MINOR** (carried over). The parish sort is case-sensitive: "Jefferson Davis Parish" sorts before "Jefferson Parish" (louisiana-12).
- **MINOR** (carried over). The JSON-LD says "v3" while its citation URLs are v2 pages. `dateModified` is 2026-10-25, but the page says the newest download was October 26, 2026 (louisiana-24).
- **MINOR** (carried over). The waiting exceptions leave out the post-wildfire exception (44 CFR 61.11(c)).
- **GAP 1.** No "find your parish" link on screen 1.
- **GAP 2.** No parish mean or full-risk column; Insurify's Plaquemines figure is not reconciled.
- **GAP 3.** No "years to reach full risk at 18% a year".
- **GAP 4.** Private flood.
- **GAP 5.** No NOAA storm-events panel at state level.

**Screenshot skim (louisiana-00..27):** nothing wrong or misleading.
- The zone table on screen 1 sums to 100%.
- The costliest years in the text (2005, 2016, 2021) match the orange bars and their values.
- "Most do: 77.8%" agrees with 22.2% closed with no payment, and 107,750 / 485,743 = 22.2%.
- The decade table is as verified above.
- The CRS table, penetration (22.0% / 73.1%), disasters list and source list are consistent with each other.

Verdict: PASS

## palm-beach-county-fl

- **MINOR** (carried over, Opal). "Among the five costliest years, these have no named event in this table, because FEMA filed their claims under a general label: 2025, 1995, 2014" (palm-beach-county-fl-08). 1995 does have a named event, Hurricane Opal, which is dropped from the table for its low claim count.
- **MINOR** (carried over). The ZIP lookup still prints "1 policy units" for single-unit ZIPs.
- **MINOR** (carried over). ZIPs 33437 and 33446 show no town (palm-beach-county-fl-12), and 33428 is "Watergate", a CDP name.
- **MINOR** (carried over). The rcv_80 under-80% overstatement, the checker's mid-band "about half" and the "annual premium" aria-label: the same as Louisiana.
- **MINOR** (carried over). "downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing" is a comma splice (palm-beach-county-fl-00).
- **MINOR** (carried over). "How often is this county a flood disaster?" lists mostly-wind hurricane declarations (Milton, Nicole, Ian).
- **GAP 1.** Private flood: whether a lender or Citizens accepts it, and its price.
- **GAP 2.** No row naming NerdWallet's $528 or MoneyGeek's $466 against our $507 premium-only figure.
- **GAP 3.** No ZIP-level below-full-risk share or full-risk median.
- **GAP 4.** No cost by municipality.
- **GAP 5.** No paid share by named storm.

**Round-8 minors fixed this round:**
- The hero line now reads "Claims filed for losses in the 2020s".
- The decade headers are fixed.
- The ZIP caveat no longer says "neighboring county".

**Screenshot skim (palm-beach-county-fl-00..24):** nothing wrong or misleading.
- 43.5% paid (hero) agrees with 56.5% closed with no payment (card).
- The costliest years (2004, 1999, 2025) match the bars.
- The ranking table bolds Palm Beach under "Relatively High", which agrees with the rating card.

Verdict: PASS

## broward-county-fl

**Is this Broward's data?** Yes, on every test I ran.

- **County code and ZIPs:**
  - `agg.geoid` is 12011 (Broward).
  - Every Broward ZIP I listed is in the lookup: 33004–33029, 33060–33076, 33301–33334, 33351 and 33441/2.
  - The lookup's unit total is 234,729, against 234,789 in force.
- **Claims match Broward's flood history:**
  - **April 2023:** the largest year is 2023 ($249.2M; April Florida Flooding $244.5M across 3,025 paid claims). That is the Fort Lauderdale rain flood, DR-4709, which is in `declarations` for county 011.
  - **Earlier events:** Irene 1999 (6,520 claims that year), Wilma 2005 and Irma 2017 match Broward's known events.
- **The flagged unpaid share (50.2% against Florida 30.1%) is real and regional, not a join error:**
  - **Neighbors:** Miami-Dade (12086) is 40.9% unpaid and Palm Beach (12099) 56.5%. Florida's 30.1% is pulled down by Gulf surge counties. Florida: 135,172 unpaid of 448,618.
  - **Where Broward's unpaid claims come from:** the 2000s (10,239 claims, 33.8% paid). Wilma alone had 4,853 claims filed in 2005, but only 649 paid claims sit under its name. That is consistent with wind damage filed against flood policies; the top reason is "not an actual flood", 5,832 claims.
  - **The 2020s:** 78.3% paid, and the page prints this on screen 1.

**Figures checked against the data files (all match):**
- **Cost:**
  - $831 / $69 / $660–$1,087 / p90 $1,475 / 98,708 policies.
  - 15% below Florida's $983 (831/983 = 0.845) and 21% below the U.S. $1,055.
  - "15th lowest of 55": I recomputed it from the Florida `counties` with cost_n of 100 or more.
  - The ZIP range runs from $614 (33026) to $1,657.
  - 2025 $798 / 2026 $876 / new $771 (8,159).
  - Premium $643, full-risk $673, full-risk plus average fees $883 (673 + 47 + 25 + 138).
  - Means: $974 single-family, $1,298 all policies.
- **Zones:** AE 142,779 (60.8%), X 51,835 (22.1%), AH 32,874 (14.0%), VE 4,857 (2.1%); 77.9% in high-risk zones.
- **Coverage:** $53.7B building, $8.4B contents.
- **Claims:**
  - 35,049 claims; $456,568,107 paid. The yearly series sums correctly, and paid plus unpaid is 17,440 + 17,609 = 35,049.
  - Average $26,180 (Florida $61,756). ICC is one claim of $14,000, so the average and the yearly totals agree.
  - The unpaid reasons sum to 17,609.
  - The events table matches `extras.claims.events`.
  - 7.6% of claim dollars went outside A/V zones.
- **Rebuild:** 32.6% of 43,646; 86.3% at the maximum; 0.5% of 16,418.
- **CRS:** 26 of 32 communities get a discount. Every class and percentage matches `crs`.
- **Risk and history:**
  - NRI: coastal Very High (pctl 70.6, $14.1M); inland Very High (pctl 66.3, $289.0M).
  - NOAA: 110 events, $83.0M.
  - Repeat-flood records: 636.
- **Penetration:** 19.2% / 76.1% / 125,204 (Florida 13.7%).
- **FEMA aid:** $166.4M over 311,121 registrations is $535. I recomputed this excluding DR-4486 (COVID) and 9801.
- **Download check:** 137,127 / 35,049, complete.

**Rules checked against `rules_registry.py` (all correct as worded):**
- **Federal purchase requirement:** 42 U.S.C. §4012a.
- **Florida Citizens:** high-risk zones since 2023 (new policies April 1, renewals July 1); elsewhere $400k+ since January 1, 2026 and all others from January 1, 2027. This is s. 627.351(6), F.S.
- **Waiting period (44 CFR 61.11):** 30 days, with no wait for a loan and a one-day wait after a map revision.
- **Limits:** $250k building and $100k contents.
- **Rate cap:** 18% for primary homes, 25% for others; new policies usually exempt.
- **CRS:** the discount applies in every zone.
- **FEMA aid:** the requirement to buy and keep flood insurance after aid.
- **Contacts:** NFIP (877) 336-2627; every NFIP insurer offers the same rates.
- **Exceptions:** the rcv_80 wording and the missing post-wildfire exception are the carried class MINORs (see below).

**Defects, worst first:**

- **MINOR** (context on the flagged figure; broward-county-fl-01, -06).
  - **The line:** "Does it pay out here? 49.8% of claims here paid something (Florida: 69.9%)".
  - **Why it is not wrong:** the 2020s line (78.3%) and the decade table keep it from misleading.
  - **What is missing:** the only comparison offered is a state total dominated by Gulf surge claims. A reader can still conclude that Broward claims are uniquely denied, while next-door Miami-Dade (59.1% paid) and Palm Beach (43.5%) look the same.
  - **Fix:** name the neighbors, or say the gap is mostly 2005-era claims.
- **MINOR** (grammar; broward-county-fl-20). "About 2 in 10 homes here has flood insurance" should read "have". Louisiana's "2 in 10 … have" and Palm Beach's "1 in 8 … has" are right, so the verb rule fails only for plural numerators.
- **MINOR** (broward-county-fl-16). "up to 25% in Dania Beach": Pembroke Pines is also 25% (class 5). Naming one implies a single top community.
- **MINOR** (broward-county-fl-00, -12). "to $1,657 (33301 Fort Lauderdale)": 33316 Fort Lauderdale ties at $1,657 (789 priced policies), so the pick is arbitrary. The fix is to name both, or say "about $1,660 in two Fort Lauderdale ZIPs".
- **MINOR** (broward-county-fl-00; also a template class). "Renewing? Policies whose term began in 2026 typically pay $876." The 2026-term pool includes policies first bought in 2026, not only renewals. The difference is small here (new-buyer median $771), but the label claims more than the measure.
- **MINOR** (broward-county-fl-20; class). "23 federal disasters for floods or storms".
  - **EM counted as a disaster:** the list shows "2020 — Hurricane Isaias", which is an emergency declaration only (EM-3533), not a major disaster.
  - **Wind shown as flood:** the heading "a flood disaster" sits over mostly-wind hurricane declarations.
- **MINOR** (broward-county-fl-08; class). "Among the five costliest years, these have no named event …: 2009" uses a plural subject for one year.
- **MINOR** (broward-county-fl-08; class). The rcv_80 under-80% overstatement, as on Louisiana.
- **MINOR** (class).
  - **Quote checker:** the aria-label says "Your annual premium in dollars", while the prompt asks for premium plus fees.
  - **ZIP lookup:** prints "1 policy units" (e.g. 30362).
  - **Hero source line:** comma splice ("…with every record for Florida, every record the download listed was received…").
- **MINOR** (broward-county-fl-20).
  - **The clash:** the NOAA card ("about $83.0 million in property damage", 1996–2025, all buildings) sits a few screens below NFIP payouts of $244.5M for the April 2023 flood alone.
  - **What the page already says:** the card does say "weather-service estimate, not audited".
  - **What is missing:** one clause saying NOAA's estimate can run far below insured payouts would stop a reader from thinking one figure is wrong.
- **GAP 1.** No neighbor-county comparison on the claims card (Miami-Dade, Palm Beach). It is the one figure on this page a reader most needs context for.
- **GAP 2.** No paid share by named storm. It would show that the April 2023 flood claims paid far more often than the 49.8% all-claims figure.
- **GAP 3.** Private flood: whether a lender or Citizens accepts it, and its price.
- **GAP 4.** No cost by municipality, though the CRS table already lists the 32 communities.
- **GAP 5.** No ZIP-level below-full-risk share or full-risk median.

No BLOCKER or MAJOR.
- **Plausibility:** every figure I spot-checked matches its file, and the claims are plausibly Broward's.
- **The flagged share:** real and explained on screen 1.
- **Rules:** each one matches its registry source.

Verdict: PASS

## Classes

**State + county template:**
- **MINOR.** rcv_80 leaves out the under-80% settlement (the greater of ACV or a proportional share of rebuilding cost).
- **MINOR.** The waiting exceptions leave out the post-wildfire exception (61.11(c)).
- **MINOR.** In the checker, a mid-band cost says "cheaper than about half". The aria-label says "annual premium".
- **MINOR.** "Among the five costliest years, these have …: <one year>" uses a plural subject for one year.
- **MINOR.** "Renewing?" labels the 2026-term median, which includes new 2026 purchases.
- **MINOR.** "How often is this … a flood disaster?" counts EM declarations and mostly-wind hurricanes.
- **MINOR.** The JSON-LD has v3 text with v2 URLs, and `dateModified` lags the newest download.
- **MINOR.** The comma splice in the download line.

**County template:**
- **MINOR.** "N in 10 homes here has": the verb is wrong whenever N > 1.
- **MINOR.** The ZIP lookup prints "1 policy units".
- **MINOR.** "up to X% in <one community>" ignores ties. The ZIP-range extremes ignore ties.
- **MINOR.** The events table drops low-count named events (Opal 1995 on Palm Beach), while the note says those years have none.
- **MINOR.** The claims card compares only with the state total, never with neighbors.

**State template:**
- **MINOR.** The parish sort is case-sensitive.

**Home template:**
- **MINOR.** The checker's wording differs from the state and county checkers.
- **MINOR.** No "no match" message in the search box.
- **MINOR.** "number of policies" sits over an "Insured units" column.

## Previous items (round-8 BLOCKER/MAJOR)

Round 8 recorded no BLOCKER or MAJOR on any page: home, louisiana and palm-beach-county-fl all passed.

**Tally:** 0 items. FIXED 0, PARTLY 0, NOT FIXED 0.

**Round-8 minors fixed since then:**
- The decade header, on both pages.
- The Palm Beach hero line, now "Claims filed for losses in the 2020s".
- The ZIP caveat no longer says "neighboring county".
- The checker at exactly p25 no longer says "cheaper than about half".
- The home checker's ungrammatical median sentence.
