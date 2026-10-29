# Gap backlog (owner 2026-10-28: a gap does not block a ship until it is 3 review rounds old; google_gate S14)
Ranked by reader value. hater.py record appends each round's **GAP** lines below.

1. Cost by flood zone on home (high-risk A/V vs X); every top result has it. (since round 9)
2. Private flood: lenders must accept it (42 U.S.C. 4012a(b)); Florida readers shop it; no 30-day wait at some carriers. (since round 9)
3. "Find your parish/county" link on screen 1 of state pages (the table sits about 11 phone screens down). (since round 9)
4. Pages are 24-26 phone screens long; cut or reorder so the answers sit higher. (since round 9)
5. County-level full-risk and mean figures, to reconcile competitor county numbers (Insurify Plaquemines $4,752). (since round 9)
6. Same paragraphs word for word on every page (Already flooded, Yearly cap, waiting exceptions, claim-closure explainer). (since round 9)
7. Per-parish take-up and multiple-loss counts on state pages; NOAA panel on state pages. (since round 9)
8. What the search box does for the ~3,050 counties without a page. (since round 9)

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
