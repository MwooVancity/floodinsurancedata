# Gap backlog (owner 2026-10-28: a gap does not block a ship until it is 3 review rounds old; google_gate S14)
Ranked by reader value. hater.py record appends each round's **GAP** lines below.


## Closed round-12 items (2026-10-28, round 15)
- Non-NFIP communities named on state pages: DONE (light round 13 checked Louisiana's 34 names).
- ZIP town labels: DONE; a place must cover 25%+ of the ZIP's land (77386 no longer "Houston").
- Condo line: DONE in the averages card (light round 13 checked the shares).

## Closed round-9 items (2026-10-28, round 12)
- "Years to full-risk at 18% a year" / premium-rise calculator: DROPPED by the owner (2026-10-28: "no calc. way too risky"). A projection of one reader's own premium is the highest-risk thing on a money page. Reviewers: do not raise it again as a gap.
- Cost by flood zone on home: DONE in code. extras_raw.py writes data/us/cost_hist_zone.json in the monthly cloud refresh; home shows the V / A / B-C-X table once all 51 states have it.
- Private flood: DONE. Rule private_accept (12 CFR 339.3(c), eCFR excerpt) on every "Am I required" card.
- "Find your county" link on screen 1 of state pages: DONE (_jump in build_page.py).
- Page length: CLOSED. The owner rule is no caps on blocks; the answers (cost, required, quote check) are on screens 1-2, and state pages now jump to the county table.
- County full-risk and mean figures: DONE earlier. Every county page carries the averages card (median, mean, premium-only, all-policy mean) and the full-risk gap.
- Same paragraphs on every page: CLOSED. They are registry rule texts with their sources, by design; S13 fails a county page whose prose is mostly shared.
- Per-parish take-up and the NOAA panel on state pages: CLOSED. Both card types were cut in the card review (tools/card_spec.py).
- Search box with no match: DONE. The home and hub pages say no page matches and point to the state's county table.

## home (round 8)
- No cost by flood zone on home, although every top result answers it second.
- Nothing names the SERP's figures ($899 NerdWallet, $888 Policygenius, $786 Insurify) or says which of our rows each one matches.
- Private flood: when a lender must accept it, and whether it can be cheaper.
- No territories (PR, USVI, Guam), and no line saying they are left out.
- Home has no JSON-LD (`grep application/ld+json dist/index.html` finds 0), while the state and county pages have it.

## louisiana (round 8)
- No "find your parish" link on screen 1; the parish table starts at louisiana-12.
- Insurify's Plaquemines $4,752 vs our $1,231 is not reconciled, and there is no parish mean or full-risk column.
- No "years to reach full risk at 18% a year" figure.
- Private flood.
- No NOAA storm-events panel at state level, though the county template has one.

## palm-beach-county-fl (round 8)
- Private flood: whether a lender or Citizens accepts it, and how its price compares.
- No row naming NerdWallet's $528 or MoneyGeek's $466; our "Typical premium only $507" sits between them, unmentioned.
- No ZIP-level below-full-risk share or full-risk median; news results answer "how much will my ZIP rise".
- No cost by municipality.
- No paid share by named storm. It would show whether a real hurricane flood claim here pays more often than the 43.5% all-claims figure.

## home (round 9)
- No cost by flood zone on home.
- No row naming the SERP's figures ($899 NerdWallet, $888 Policygenius, $786 Insurify) against our rows.
- Private flood: when a lender must accept it, and its price.
- No line on territories (PR, USVI, Guam).
- No JSON-LD on home.

## louisiana (round 9)
- No "find your parish" link on screen 1.
- No parish mean or full-risk column; Insurify's Plaquemines figure is not reconciled.
- No "years to reach full risk at 18% a year".
- Private flood.
- No NOAA storm-events panel at state level.

## palm-beach-county-fl (round 9)
- Private flood: whether a lender or Citizens accepts it, and its price.
- No row naming NerdWallet's $528 or MoneyGeek's $466 against our $507 premium-only figure.
- No ZIP-level below-full-risk share or full-risk median.
- No cost by municipality.
- No paid share by named storm.

## broward-county-fl (round 9)
- No neighbor-county comparison on the claims card (Miami-Dade, Palm Beach). It is the one figure on this page a reader most needs context for.
- No paid share by named storm. It would show that the April 2023 flood claims paid far more often than the 49.8% all-claims figure.
- Private flood: whether a lender or Citizens accepts it, and its price.
- No cost by municipality, though the CRS table already lists the 32 communities.
- No ZIP-level below-full-risk share or full-risk median.

## home (round 10)
- The SERP's #1–#3 (NerdWallet "$899/yr", Policygenius via Kiplinger "$888", Insurify "$786 median") are not named against our rows. Our "Why do sites quote different prices?" table is the right place, and no competitor has one (information gain).
- No cost by flood zone on home. Policygenius and Bankrate give zone figures.
- Private flood: when a lender must accept it.
- No territories (PR, USVI, Guam).
- No JSON-LD on home.

## louisiana (round 10)
- Insurify's "Plaquemines Parish $4,752" (a search result) is not reconciled with our Plaquemines median of $1,231 (mean against median, and which policies).
- No "years to reach full risk at 18% a year" for the 56.6% below full risk.
- No "find your parish" jump link on screen 1. The parish table is our information gain over MoneyGeek and Bankrate, and it sits on screen 12.
- Private flood.
- No state-level NOAA panel.

## palm-beach-county-fl (round 10)
- NerdWallet $528 / $488, MoneyGeek $466 and Insurify $709 (search results) are not named against our $507 premium and $670 cost.
- No ZIP-level full-risk gap. The Miami Herald's "33469 +342%" story is what a Jupiter or Tequesta searcher has read.
- Private flood and Citizens acceptance of private flood.
- No cost by municipality.
- No paid share by named storm.

## orange-county-ca (round 10)
- Insurify lists Orange County at $795 and $892 (two of its pages disagree); our $1,083 is not reconciled with them. Our "Why do sites quote different prices" table could name them.
- The post-wildfire waiting-period exception (44 CFR 61.11(c)) and debris-flow risk after fire, the local flood type in 92676 and 92679.
- OC Public Works' "25% discount for unincorporated homeowners" press release is matched by our CRS row, which is information gain. But nothing tells a city resident (Santa Ana, Garden Grove: no discount) why their city gets none.
- Private flood.
- No cost by city. The ZIP table half-covers it.

## atlantic-county-nj (round 10)
- Insurify's "Atlantic County $1,022" and Clovered's "$1,899 under Risk Rating 2.0" (search results) are not reconciled with our $1,246 median and $2,017 all-policy mean.
- No Risk Rating 2.0 transition line. The Press of Atlantic City reported that most of 27,000 policies saw $0–$10 increases; we have the 58.5% below full risk but no "how fast it closes".
- No cost by municipality. The CRS table lists the towns, and Brigantine, Margate, Ventnor and Longport are what searchers type.
- Private flood.
- No elevation-certificate or "elevated vs not" next step tied to the 2,478 elevated policies (median premium $894 against $1,051).

## site review (2026-10-28, browser test)
- ZIP town labels come from GeoNames and can name the metro, not the postal town: 77386 shows "Houston" (USPS: Spring). Source a USPS-preferred city name.
- Home search with no match showed an empty table; patch ready (no-match message pointing to the state page), ships after round 11.

## home (round 11)
- NerdWallet, Policygenius and Insurify headline figures are not named in "Why do sites quote different prices?" (round-10 SERP).
- No cost by flood zone nationally.
- No private-flood acceptance rule.
- No territories (PR, USVI).
- No JSON-LD.

## louisiana (round 11)
- The "Not in the NFIP (34 communities here)" line does not name them (Vienna, Creola, Shongaloo, Atlanta and the rest), so a reader in one of those villages cannot tell that it applies to them. The brief says the line names them; it does not.
- No "years to reach full risk at 18% a year".
- No parish jump link on screen 1.
- Insurify's Plaquemines figure is not reconciled with ours.
- Private flood.

## palm-beach-county-fl (round 11)
- NerdWallet, MoneyGeek and Insurify county figures are not reconciled with ours.
- No ZIP-level full-risk gap.
- Private flood and Citizens' acceptance of it.
- No cost by municipality.
- The community names in the "Not in NFIP" line do not apply here (all 40 participate); nothing is missing.

## orange-county-ca (round 11)
- Insurify's $795 / $892 are not reconciled with ours.
- Post-wildfire waiting-period exception and debris-flow risk.
- No line on why cities without CRS get no discount.
- Private flood.
- No cost by city.

## atlantic-county-nj (round 11)
- Insurify $1,022 and Clovered $1,899 are not reconciled with ours.
- No Risk Rating 2.0 transition pace.
- No cost by municipality.
- Private flood.
- No Elevation Certificate next step tied to the elevated/not-elevated rows.

## montgomery-county-tx (round 11)
- MoneyGeek "$568 average" and Insurify "$1,040" (search results today) are not reconciled with our $1,001.
- No 2018 Montgomery County map-change note (Community Impact covers the map dates).
- No cost by city or The Woodlands.
- Private flood.
- No Spring/Lake Conroe dam-release context for 2017 (Harvey) claims.

## oklahoma (round 11)
- "Not in the NFIP (122 communities here)" names none (Greenfield, Osage, Springer, unincorporated McCurtain County and others). A reader in one cannot tell.
- Kin's "NFIP median $793" and MoneyGeek's "$995 average" are not reconciled with our $1,047.
- No Tulsa city figure. Tulsa, CRS class 1 with a 45% discount, is the state's best-known flood story, and searchers see "$892 in Tulsa".
- Private flood.
- No Oklahoma Insurance Department "Get Ready" next step.

## home (round 12)
- (SEO, "flood insurance cost").
- #1-#3 give cost by flood zone nationally ("$560 in B/C/X, $2,795 in D"-style tables). The home page has no national zone table; it exists only on state pages.
- No national private-flood figure. The page says so ("Private flood insurance is not in this data"), so this is allowed and is not a defect.

## louisiana (round 12)
- (SEO "flood insurance cost Louisiana": MoneyGeek $750, Insurify $1,470 "NFIP median, single-family" with a U.S. median of $1,290, Policygenius $752). Insurify's $1,470 vs our $1,086, both called NFIP medians, is not reconciled; a searcher will see both.
- Insurify's Plaquemines $4,752 against our $1,231 (carried).
- The NFIP-not-sold line counts 34 communities but does not name them (carried).
- No parish jump on screen 1 (carried).
- No years-to-full-risk at 18% a year (carried).
- No NRI flood-risk card on the state page; county pages have one.

## orange-county-ca (round 12)
- (SEO "flood insurance cost orange county CA": Insurify CA guide with an OC row $795 / older $892; LendingTree CA; MoneyGeek CA $909).
- County Public Works says unincorporated homeowners get 25% CRS. We show that (Orange County 25%, class 5), but not which cities' residents are "unincorporated".
- No cost by city; the ZIP table covers it partly.

## montgomery-county-tx (round 12)
- (SEO "flood insurance cost montgomery county TX": MoneyGeek TX with a Montgomery row of $568, Insurify Houston guide $1,040, Community Impact).
- No The Woodlands figure (three Woodlands ZIPs exist in the table, but no combined line).
- No 2018/2014 map-change note.

## oklahoma (round 12)
- (SEO "flood insurance cost Oklahoma": OKCFox/QuoteWizard "ranks 23rd", MoneyGeek about $995, Jerry $937, Kin "$793 NFIP median").
- The 122 non-NFIP communities are counted, not named (carried).
- No Tulsa city figure (carried).
- No OID "Get Ready" / FloodSmart OneStep next step.

## nevada (round 12)
- (SEO "flood insurance cost Nevada": MoneyGeek $799 with county rows, Nye $468 and Lander $1,421; 1-800 Insurance $1,038; StateCalc $696 "median of recent NFIP policies").
- No Las Vegas / Clark County Regional Flood Control District context; the AO zone is 48% of units and is not explained.
- The state's division-of-insurance note ("available in every county except Esmeralda") is not used. Our page says one community is non-NFIP but not which.

## horry-county-sc (round 12)
- (SEO "flood insurance cost horry county SC": WBTW, WMBF, MoneyGeek SC with a Horry row of $493, Policygenius SC $747 with "risk-based $929").
- 1-800 Insurance's "$2,000–$6,000 for most Little River properties" (likely condo/VE) has no answer; our 29566 Little River median is $493 single-family. That is the same base problem as the MAJOR above.
- No new-map (2003 FIRM, pending update) note; WBTW and WMBF both lead on it.
- No condo/RCBAP cost line at all.

## light round 13 MINORs (2026-10-28; fix in the next template batch)
- Quote checker: clearing the amount leaves the old zone line (zq must clear when the amount is empty).
- Zone dropdown lists thin zones (Louisiana A12, 53 policies); consider the zone card's own floor.
- Condo note prints "0.0%" for condo buildings; say "none" or drop the clause at 0.

## home (round 16)
- No buying step anywhere on home: no NFIP phone (877) 336-2627, no FloodSmart link, no 30-day/60-day deadline line beyond "30 days". NerdWallet and Bankrate give "how to buy" on the page. The only next step is "Check your zone on FEMA's flood map".
- No Spanish (L, OPEN); no error-report route (I, OPEN); no print stylesheet (K, OPEN).
- NerdWallet/Bankrate show a "cheapest/most expensive" narrative and private-market context; we say only "Private flood insurance is not in this data". That is acceptable per the brief. Noted, not counted.

## louisiana (round 16)
- The 64-row parish table has no search or filter; only the county page has a lookup (G: long tables searchable). There is also no back-to-top link on a 27-screen page (G).
- Data already held but not shown: residential take-up (penetration 22.0% overall, 73.1% in high-risk zones, data.json) and the share of claims from outside high-risk zones (21.4%, claims_extra.outside_sfha_pct). WABI ranks for "only 1% of Maine households"; this is the same reader question. These were cut earlier as "take-up"; the cut should be revisited.
- No Spanish (L, OPEN). No state insurance department or floodplain office contact (F, OPEN). Renter, landlord/second home and business readers get no line (B).
- MoneyGeek has a parish table with averages; ours is better (medians, n, claims). We have no "how to buy from a private insurer" line.

## palm-beach-county-fl (round 16)
- City-level costs (NerdWallet lists West Palm Beach $349): our ZIP lookup covers this, but town names are missing on most ZIPs (item 7).
- The Miami Herald/Sun-Sentinel rank with "rates will double/triple near the coast" (Risk Rating 2.0 glide path by ZIP). We have share below full-risk only at county level, not by ZIP.
- Take-up held but not shown (penetration 13.0% overall, 43.4% in high-risk zones). No Spanish (L, OPEN, FL). No county floodplain office contact (F, OPEN).

## maine (round 16)
- "Only 1% of Maine households have flood insurance" (WABI, ranking #6) answers "do my neighbours carry it?". We hold 1.2% overall and 78.5% in high-risk zones (data.json penetration) and do not show it.
- Press Herald gives county averages; ours exist (PASS). The FEMA Maine state profile PDF has the official NFIP state figures; we do not link it.
- No back-to-top; no state floodplain office (Maine Floodplain Management Program) contact (F, OPEN).

## nebraska (round 16)
- The 78-row county table has no search (G). No back-to-top.
- StateCalc gives "median of the 1,000 most-recent real NFIP policies" ($744), a buyer-oriented figure; our $874 first-bought-in-past-year figure is better sourced but sits in the hero only as a "Buying?" line.
- Take-up (0.7% overall, 15.3% in high-risk zones) and claims outside high-risk zones (21.3%) are held but not shown. Answering "most homes in the floodplain here are uninsured" is a strong information gain.

## light round 21 MINORs (deadline planner; next template batch)
- Heading says "claim deadline" but computes only the NFIP proof-of-loss date.
- "Your NFIP proof of loss" also reads to uninsured or private-policy readers; say "An NFIP proof of loss".
- Past-date sentence: add that the insurer may have extended the date.
- Spell out "NFIP" once inside the tool.

## site-wide decisions (2026-10-29, after 3 light rounds on the home source line)
- How the home "Three things to know first" card cites its rules: decide ONE format for the whole site (today county
  pages name the official hosts; home names none). A per-claim link vs a host list; then apply everywhere at once.
- Define "Citizens" (Florida's state-backed insurer) where the Florida rule appears; split its three dates.

## home (round 69)
- AE and VE screen 1 shows the all-A-zones / all-V-zones median, correctly labelled right under the figure; exact-zone data due next refresh. D and AH show no national cost (honest gap line). No local contacts list, error-report route, print stylesheet, Spanish.

## new-york-county-ny (round 82)
- Query 'flood insurance cost new york county NY' is a Manhattan reader; the H1 does not say Manhattan. Not wrong.
