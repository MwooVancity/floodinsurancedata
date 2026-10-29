# Hater round 10 (built dist/ pages + 112 phone screenshots in round10/)

**Method.** I extracted the visible text, JSON-LD and inline scripts (quote checkers, ZIP lookup `ZD`) of all five built pages. Every `data-p` figure was re-read from its JSON path: 425 on louisiana, 157 on palm-beach, 143 on orange, 158 on atlantic. All match after rounding, so there are no wrong numbers.

I recomputed these by hand:
- the state ranks of the counties (PB 8th lowest of 55, Orange 15th lowest of 42, Atlantic 11th of 21)
- the state comparison figures (FL, CA, NJ files)
- the home "Average premium alone" row: premium-count-weighted over 52 state files, it comes to $999.66, so $1,000 is correct
- the ZIP unit totals
- the event and year totals

I read every rule in `tools/rules_registry.py` against its cited source text. The rules were not re-fetched. I looked at all 112 screenshots as 4-up sheets. I read `tools/collect_stormevents.py` (a fetch script, not gate code) to check what the NOAA card counts. I ran one WebSearch per page.

**Not done:** I did not run the checkers or the ZIP lookup in a browser; their outputs are computed from the scripts. I did not re-download NOAA files.

**Quote checker at the page median** (computed from each page's `P` and `R`):
- **home**, $1,055: "$1,055 is right at the middle of U.S. single-family policies (half pay $713 to $1,309)."
- **louisiana**, $1,086: "$1,086 is the typical cost here (half pay $863 to $1,273, typical $1,086). Renewing? Policies whose term began in 2026 typically pay $1,215."
- **palm-beach-county-fl**, $670: "... the typical cost here (half pay $517 to $1,034, typical $670). Renewing? ... $679."
- **orange-county-ca**, $1,083: "... the typical cost here (half pay $854 to $1,265, typical $1,083). Renewing? ... $1,226."
- **atlantic-county-nj**, $1,246: "... the typical cost here (half pay $918 to $1,691, typical $1,246). Renewing? ... $1,299."
- All five are correct.

**Changes since round 9, verified:**
- **ZIP+4 merged: VERIFIED.** ZIP units sum to county units: Orange 9,496 = 9,496; PB 132,945 = 132,945; Atlantic 23,137 = 23,137 in `by_zip`. One exception: the Atlantic lookup holds 23,136, see MINOR.
- **Events note "Totals include code-upgrade (ICC) payments": VERIFIED** on all four state and county pages. It explains Sandy $418.7M against 2012 $400.1M (Atlantic has 697 ICC claims).
- **A to Z ignoring case: VERIFIED** in the parish table (Lafayette < Lafourche < LaSalle; Jefferson Davis < Jefferson) and in the no-CRS lists on Orange, PB and Atlantic.
- **"N in 10 homes has/have": VERIFIED.** "2 in 10 ... have" (LA), "1 in 8 ... has" (PB), "1 in 100 ... has" (Orange), "1 in 7 ... has" (Atlantic; 14.4% ≈ 1/7).
- **FEMA source links now v3: VERIFIED.** Source list and JSON-LD `citation` URLs point to `nfip-redacted-policies-v3` / `-claims-v3`.
- **Home "Average premium alone" weighted by premium count: VERIFIED.** $1,000 (999.66 over n = 2,351,712).

**The two new counties: their own claims, not another county's?**
- **orange-county-ca: YES.** geoid 06059. The costly years are 1983, 1995, 1997–98 and 2010: the El Niño and atmospheric-river winters of Southern California. The named events (Pineapple Express Southern 1998, the 2022–24 California atmospheric rivers, Tropical Storm Hilary 2023) are Californian. Orange County FL would show 2004, 2017 and 2022 (Ian) hurricane peaks; 2022 here is 2 claims. The ZIPs are 926xx/927xx/928xx/906xx. The total of $21.1M over 3,839 claims is plausible for ~9.5k policies.
- **atlantic-county-nj: YES.** geoid 34001. The events are Sandy 2012 (10,425 paid claims), the December 1992 nor'easter, the 1984 nor'easter, Gloria 1985, the 1991 Halloween storm, Irene 2011, Jonas 2016 and Erin 2025: the NJ shore record. The ZIPs are 082xx/084xx, from Brigantine to Longport.

---

## home

- **MINOR** (carried, NOT FIXED; home-04): "52 counties so far, listed by number of policies". The column and the sort are "Insured units".
- **MINOR** (carried): the checker says "in the lowest quarter" and "right at the middle"; the state and county checkers say "cheapest quarter" and "the typical cost here".
- **MINOR** (carried; home-00): "3,490,299 NFIP policy records" sits beside "4.6M insured units". The note explains it.
- **MINOR**: the home page carries no `data-p` tags, so none of its figures can be traced to a file (the state pages can). I verified the state table, county table and averages against the state and county files by hand.
- **MINOR**: the national "Am I required" answer has a Florida-only Citizens sentence in the middle of it (home-00). It is correct (`fl_citizens_short` matches s. 627.351(6)), but it slows a non-Florida reader.
- **GAP 1.** The SERP's #1–#3 (NerdWallet "$899/yr", Policygenius via Kiplinger "$888", Insurify "$786 median") are not named against our rows. Our "Why do sites quote different prices?" table is the right place, and no competitor has one (information gain).
- **GAP 2.** No cost by flood zone on home. Policygenius and Bankrate give zone figures.
- **GAP 3.** Private flood: when a lender must accept it.
- **GAP 4.** No territories (PR, USVI, Guam).
- **GAP 5.** No JSON-LD on home.

**SEO (query "flood insurance cost").**
- **Title, H1 and first screen:** they answer outright ($1,055 median, $88/month, from FEMA records) faster than NerdWallet or Bankrate, whose answers sit below ads and introductions.
- **Where we are weaker:** a searcher who saw "$899" or "$786" elsewhere sees our $1,055 with no reconciliation until screen 3.
- **Templating:** no doorway look on home.

**Screenshot skim (home-00..08):** nothing wrong or misleading. The state table has 51 rows sorted by median; the county table has 52 rows sorted by units.

Verdict: PASS

## louisiana

- **MINOR** (carried, NOT FIXED; louisiana-08): "Among the five costliest years, these have no named event ...: 1995" uses a plural subject for one year. The fact is true here: the 1995 claims sit under the "Flooding (1978–1998)" catch-all.
- **MINOR** (carried): rcv_80 leaves out the under-80% settlement (the greater of ACV or a proportional share of rebuilding cost).
- **MINOR** (carried): the waiting-period exceptions leave out 44 CFR 61.11(c) (post-wildfire).
- **MINOR** (carried): the checker's mid-band says "cheaper than about half" for a cost between p25 and p50. The aria-label "Your annual premium in dollars" disagrees with the prompt, which asks for premium plus fees.
- **MINOR** (carried): "Renewing? Policies whose term began in 2026 typically pay $1,215". That pool includes new 2026 buyers.
- **MINOR** (carried): JSON-LD `dateModified` 2026-10-25, while the page says the newest download was October 26, 2026.
- **MINOR**: "67 federal disasters for floods or storms" counts EM-only declarations and wind hurricanes, and lists 6 of 67 under "One line per disaster" with no "latest six" label (louisiana-24).
- **GAP 1.** Insurify's "Plaquemines Parish $4,752" (a search result) is not reconciled with our Plaquemines median of $1,231 (mean against median, and which policies).
- **GAP 2.** No "years to reach full risk at 18% a year" for the 56.6% below full risk.
- **GAP 3.** No "find your parish" jump link on screen 1. The parish table is our information gain over MoneyGeek and Bankrate, and it sits on screen 12.
- **GAP 4.** Private flood.
- **GAP 5.** No state-level NOAA panel.

**SEO (query "flood insurance cost Louisiana").**
- **The top results disagree:** MoneyGeek $750, Bankrate $955, Insurify "$1,470 median".
- **Our first screen** answers with $1,086, the spread and the rank. It is faster and better sourced than any of them.
- **Templating:** no doorway risk; the parish table and the Katrina/2016 event table are unique.

**Screenshot skim (louisiana-00..27):** nothing wrong or misleading. The orange bars are 2005, 2016 and 2021, matching the text. The 22.2% unpaid share equals 107,750 / 485,743. The 15-row CRS table is labelled as the top 15 of 42.

Verdict: PASS

## palm-beach-county-fl

- **MAJOR** (NOAA card mislabels its scope; palm-beach-county-fl-16).
  - **The text:** "98 flood events here since 1996 ... about $71.1 million in property damage the weather service estimated (all buildings, insured or not)", and the methodology says "Recorded flood/flash-flood/coastal-flood events".
  - **What the code counts:** `tools/collect_stormevents.py` keeps only `CZ_TYPE == "C"` rows. NOAA files Coastal Flood and Storm Surge/Tide on forecast zones (`CZ_TYPE "Z"`, NWS Directive 10-1605). So the card has no coastal-flood or surge events at all, on a coastal county whose top NFIP losses are hurricanes.
  - **Why it hurts:** a reader judging "has it actually flooded here" sees an undercount presented as complete.
  - **Fix:** map NOAA zones to counties (or count zone events whose name holds the county), or relabel the card "river and rain floods (county-coded events only)".
- **MAJOR** (events table and its footnote; palm-beach-county-fl-08).
  - **The text:** "Among the five costliest years, these have no named event in this table, because FEMA filed their claims under a general label: 2025, 1995, 2014."
  - **1995 is named:** it has a named event, Hurricane Opal ($1,356,819 across 7 claims, `extras.claims.events`). Opal is dropped by an unstated claim-count floor, while Hurricane Wilma ($1,122,503, smaller) is shown. A table titled "Which floods paid out the biggest totals here?" ranks wrongly as printed.
  - **2025 and 2014 are not under the general label:** that label spans 1979–2000 (its own row says so). Their claims carry no event name; they are not "filed under a general label".
  - **The methodology contradicts the page:** it says catch-all labels "are left out of the event table", yet the table shows the "Flooding (1979–2000)" row.
  - Round 9 rated this MINOR. I disagree: this is a false sentence printed as fact, next to a ranking that is wrong as shown.
- **MINOR** (carried, NOT FIXED): ZIPs 33437 and 33446 show no town; 33428 is "Watergate", a CDP name that readers know as Boca Raton (palm-beach-county-fl-12).
- **MINOR** (carried, NOT FIXED): the ZIP lookup prints "1 policy units" (`d.u.toLocaleString()+" policy units"`).
- **MINOR** (carried, NOT FIXED; palm-beach-county-fl-00): comma splice, "downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing."
- **MINOR** (carried): "22 federal disasters for floods or storms" lists mostly-wind hurricanes and EM-only Isaias. Six lines are shown under "One line per disaster".
- **MINOR** (class, carried): rcv_80, 61.11(c), checker mid-band and aria-label, "Renewing?" label, `dateModified`.
- **GAP 1.** NerdWallet $528 / $488, MoneyGeek $466 and Insurify $709 (search results) are not named against our $507 premium and $670 cost.
- **GAP 2.** No ZIP-level full-risk gap. The Miami Herald's "33469 +342%" story is what a Jupiter or Tequesta searcher has read.
- **GAP 3.** Private flood and Citizens acceptance of private flood.
- **GAP 4.** No cost by municipality.
- **GAP 5.** No paid share by named storm.

**SEO (query "flood insurance cost palm beach county FL").**
- **The top 3** are statewide pages (NerdWallet, MoneyGeek, Insurify) with one county row each.
- **We win screen 1 outright:** $670, the spread, the ZIP range and the rank. The ZIP table is clear information gain.
- **Templating:** the page shares about 90% of its sentence frames with the other county pages (see Classes).

Verdict: FAIL

## orange-county-ca

- **MAJOR** (events table hides recent, larger floods; orange-county-ca-08).
  - **What the table shows:** three rows, Pineapple Express Southern 1998 ($2.2M), "Winter storm (2010)" ($488,781, 24 claims) and the 1978–1997 catch-all.
  - **What it leaves out:** `extras.claims.events` also holds February California Atmospheric River 2024 ($615,063, 8 claims, average $76,883), California Atmospheric River 2022–23 ($385,653), December California Flooding 2023 and Tropical Storm Hilary 2023. Feb 2024 out-paid the 2010 row, so "Which floods paid out the biggest totals here?" ranks wrongly as printed. It also hides every flood of the 2020s, the ones a 2026 buyer remembers.
  - **The footnote:** "1997, 1995, 1983 ... FEMA filed their claims under a general label." The general-label row totals $5.1M, while those three years alone paid $7.84M, so at least $2.7M of them sits under no label at all.
  - **The rule is hidden:** the methodology states no claim floor, and it says the catch-all row is excluded, yet the row is shown.
- **MAJOR** (NOAA card, same class as Palm Beach; orange-county-ca-16).
  - **The text:** "136 flood events here since 1996 ... all buildings, insured or not."
  - **What it misses:** zone-coded Coastal Flood and surf/surge events (Seal Beach, Newport, Huntington) are excluded by `CZ_TYPE == "C"`, though the page rates coastal flood risk "Relatively High".
- **MINOR**: "17 federal disasters for floods or storms" lists 6 under "One line per disaster" with no "latest six" label (orange-county-ca-20). The latest two, 2023 "Severe Winter Storms, Flooding ...", are EM declarations (emergency declarations, not major disasters).
- **MINOR**: "Not in FEMA's records: no disaster-aid applications here came from homes that flooded more than once" (orange-county-ca-16).
  - **The problem:** the dataset covers IA records since 2002 only. The claims card shows the same county filing NFIP claims across many floods.
  - **Fix:** "No repeat-flood records in FEMA's disaster-aid list (since 2002)".
- **MINOR**: the rebuild card puts 49.1% (rebuilding cost above $250,000) next to 90.9% (insured to the maximum).
  - **What a reader concludes:** about 40% of homes carry $250,000 of cover on a smaller rebuilding cost, which the NFIP will not pay out.
  - **What the page omits:** it never says "insuring above your rebuilding cost buys nothing". The bases differ and the note says so, but the inference is left to the reader.
- **MINOR** (class): comma splice in the download line; "1 policy units"; rcv_80; 61.11(c), which matters here because Silverado (92676, the costliest ZIP) is a 2020 burn-scar canyon; checker mid-band and aria-label; "Renewing?"; `dateModified`.
- **GAP 1.** Insurify lists Orange County at $795 and $892 (two of its pages disagree); our $1,083 is not reconciled with them. Our "Why do sites quote different prices" table could name them.
- **GAP 2.** The post-wildfire waiting-period exception (44 CFR 61.11(c)) and debris-flow risk after fire, the local flood type in 92676 and 92679.
- **GAP 3.** OC Public Works' "25% discount for unincorporated homeowners" press release is matched by our CRS row, which is information gain. But nothing tells a city resident (Santa Ana, Garden Grove: no discount) why their city gets none.
- **GAP 4.** Private flood.
- **GAP 5.** No cost by city. The ZIP table half-covers it.

**SEO (query "flood insurance cost orange county CA").**
- **No county-specific top result:** the top 3 are statewide (Insurify, LendingTree, MoneyGeek), plus OC Public Works.
- **Screen 1 answers outright** with the ZIP range, which beats #1.
- **Templating risk:** the same frames as every county page, with only the numbers and names swapped.

Verdict: FAIL

## atlantic-county-nj

- **BLOCKER** (NOAA card omits the county's worst flood; atlantic-county-nj-16).
  - **The text:** "How often has it actually flooded here? 63 flood events here since 1996 ... about $85.1 million in property damage the weather service estimated (all buildings, insured or not; not NFIP payouts)."
  - **What the code counts:** `collect_stormevents.py` keeps only county-coded (`CZ_TYPE "C"`) Flood and Flash Flood rows. NOAA records coastal flooding and storm surge, including Hurricane Sandy 2012 and every nor'easter tide flood on Absecon Island, as zone-coded Coastal Flood and Storm Surge/Tide events. None of them are in the 63 or the $85.1M.
  - **The same page contradicts it:** NFIP alone paid $418.7M for Sandy here (insured buildings only), five times the "all buildings, insured or not" NOAA total.
  - **Why the reader is hurt:** a shore homeowner deciding whether to keep coverage reads that the weather service counts $85M of flood damage in 30 years. That is wrong, and it understates the risk.
  - **Fix:** add the zone-coded coastal and surge events for the county's NWS zones, or relabel the card "inland rain and river floods only" and drop "all buildings".
- **MINOR** (events footnote; atlantic-county-nj-08): "these have no named event ... because FEMA filed their claims under a general label: 1984, 2018".
  - **1984:** true; it sits in "Flooding (1978–2000)".
  - **2018:** its 120 claims ($2.6M) carry no event name, and the label row ends in 2000, so the stated reason is wrong for 2018. The table itself is complete: all 8 entries in `extras.claims.events` are shown.
- **MINOR**: "up to 25% in Linwood". Brigantine, Longport, Margate City and Ventnor City are also 25% (class 5), so naming one implies a single top town (atlantic-county-nj-16).
- **MINOR**: "Erin HU (2025)" prints FEMA's code "2025-08-Erin-HU". "HU" is jargon; "Hurricane Erin (2025)" is meant.
- **MINOR**: ZIP "8037" (1 policy unit, leading zero lost on the FEMA record) is neither merged into 08037 nor in the lookup.
  - **Effect here:** the lookup holds 23,136 units against 23,137, and the page says "All 37 ZIPs".
  - **Why it is a class defect:** the ZIP+4 merge does not cover 4-digit ZIPs, so every NJ and New England page can lose units the same way.
- **MINOR**: "19 federal disasters for floods or storms" lists 6 under "One line per disaster" (atlantic-county-nj-20). It includes "Severe Storms and Straight-Line Winds (2012)", the derecho, which was a wind event.
- **MINOR** (class): comma splice; "1 policy units"; rcv_80; 61.11(c); checker mid-band and aria-label; "Renewing?"; `dateModified`.
- **GAP 1.** Insurify's "Atlantic County $1,022" and Clovered's "$1,899 under Risk Rating 2.0" (search results) are not reconciled with our $1,246 median and $2,017 all-policy mean.
- **GAP 2.** No Risk Rating 2.0 transition line. The Press of Atlantic City reported that most of 27,000 policies saw $0–$10 increases; we have the 58.5% below full risk but no "how fast it closes".
- **GAP 3.** No cost by municipality. The CRS table lists the towns, and Brigantine, Margate, Ventnor and Longport are what searchers type.
- **GAP 4.** Private flood.
- **GAP 5.** No elevation-certificate or "elevated vs not" next step tied to the 2,478 elevated policies (median premium $894 against $1,051).

**SEO (query "flood insurance cost atlantic county NJ").**
- **The top results** are statewide guides with one county row.
- **We answer screen 1 outright:** $1,246, the spread, the ZIP range and the rank.
- **Information gain:** the Sandy claims table and the 94.5% high-risk take-up, on screens 8 and 20.
- **Where a searcher bails:** at the NOAA card, if they know Sandy.

Verdict: FAIL

## Classes

**County template (every county page):**
- **BLOCKER on surge counties, MAJOR elsewhere.** The NOAA "How often has it actually flooded here?" card counts only county-coded Flood and Flash Flood events (`CZ_TYPE == "C"`). Zone-coded Coastal Flood and Storm Surge/Tide are dropped, while the card and the methodology claim coastal floods and "all buildings, insured or not". Every coastal county undercounts, worst where surge dominates (Atlantic, Cape May, Ocean, Monroe, Lee, Charlotte, Galveston, Jefferson Parish and others).
- **MAJOR.** The events table applies an unstated claim-count floor (it drops events with fewer than about 12–24 claims, e.g. Opal with 7 and Feb 2024 AR with 8) while sorting by dollars. The "no named event ... filed under a general label" footnote is false for years after the catch-all label's span and for years whose named event was dropped. The methodology says the catch-all row is excluded, but it is shown.
- **MINOR.** The "How often is this county a flood disaster?" list shows the latest 6 of N under "One line per disaster". It counts EM declarations and wind events.
- **MINOR.** The ZIP lookup prints "1 policy units". 4-digit (leading-zero-stripped) ZIPs are dropped. There are blank or CDP town names.
- **MINOR.** "up to X% in <one community>" ignores ties.
- **MINOR.** Comma splice in the download line.
- **MINOR, SEO risk.** Every county page uses the same sentence frames with names and numbers swapped (the diff of Orange and Palm Beach with digits stripped differs only in names, the zone and event rows and the CRS rows). The data differ, but the prose is the "mad-libs" pattern. A Google rater would see scaled pages.

**State + county template:**
- **MINOR.** rcv_80 leaves out the under-80% settlement.
- **MINOR.** No 61.11(c) post-wildfire exception.
- **MINOR.** Checker mid-band "about half"; aria-label "annual premium".
- **MINOR.** "Renewing?" labels the 2026-term median, which includes new buyers.
- **MINOR.** `dateModified` lags the newest download.
- **MINOR.** A plural subject is used for one year in the events footnote.

**Home template:**
- **MINOR.** "number of policies" sits over the "Insured units" column.
- **MINOR.** Checker wording differs from the state and county checkers.
- **MINOR.** The search box has no "no match" message.
- **MINOR.** No `data-p` tags.

## Previous items (round-9 BLOCKER/MAJOR)

Round 9 recorded no BLOCKER or MAJOR on any page: home, louisiana, palm-beach-county-fl and broward-county-fl all passed.

**Tally:** 0 items. FIXED 0, PARTLY 0, NOT FIXED 0.

**Round-9 minors since then:**

| Item | Status | Evidence |
|---|---|---|
| "2 in 10 ... has" | FIXED | LA "have", others "has" |
| Parish sort is case-sensitive | FIXED | |
| JSON-LD v3 text with v2 URLs | FIXED | |
| Events ICC clash (Broward) | PARTLY | The events note now names ICC, but the NOAA-vs-NFIP clash remains and is worse than thought (see the BLOCKER) |
| "1 policy units" | NOT FIXED | |
| Comma splice | NOT FIXED | |
| Plural subject for one year | NOT FIXED | |
| `dateModified` | NOT FIXED | |
| Home "number of policies" | NOT FIXED | |
| "up to X% in one town" ties | NOT FIXED | Atlantic "Linwood" |
| Opal footnote (palm-beach-county-fl) | NOT FIXED | Escalated to MAJOR this round |
