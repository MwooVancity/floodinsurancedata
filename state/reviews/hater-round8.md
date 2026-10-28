# Hater round 8 (built dist/ pages + 62 phone screenshots in round8/)

**Scope (narrowed by the caller):**
1. Verify every round-7 BLOCKER/MAJOR.
2. Truth-check the cards that changed since round 7.
3. Skim every screenshot for anything wrong or misleading.

No new SEO search; at most five GAPs per page.

**Method:**
- **Pages:** I extracted the visible text of all three built pages and their inline scripts (quote checkers and the ZIP lookup's `ZD` object).
- **Screenshots:** I looked at the screenshots: home 00–04, 06, 08; louisiana 00–14, 17–22, 24, 26; palm-beach-county-fl 00–02, 05, 07–13, 18. I skimmed the rest of the tables and footers via the extracted text only.
- **Data:**
  - **Decade table:** checked against `extras.claims.by_decade` for both pages.
  - **ZIPs:** parsed the `ZD` object (61 keys, all five digits; units sum to 132,935 against 132,945 in force).
  - **Raw claims:** read the raw FL claims (`.cache/raw/NfipClaims/FL/2020–2026.csv.gz`, countyCode 12099) to test whether open claims distort the 2020s paid share.
- **Rules:**
  - **44 CFR 61.11:** I did not re-fetch it this round. I relied on round 7's govinfo reading: (a) map revision, (b) loan, (c) post-wildfire, (d) 30-day rule, (e) mid-term increases wait.
  - **44 CFR Part 61 App. A(1) §VII.V:** one WebSearch did not return the SFIP text. It found only FEMA bulletin W-14058, which confirms that §VII(V) holds the replacement-cost conditions. The 80% wording below is therefore checked against my own reading of the SFIP and is **not verified on the web this round**.
- **Not read:** the gate code.
- **Not run in a browser:** the checkers and the lookup. I computed their outputs from the scripts.

**Quote checkers, computed from the scripts:**
- **home** (`<713 lowest quarter / <1055 below the middle / ==1055 typical / <1309 above the middle / <2150 top quarter / else top tenth`; non-digits stripped):
  - 1055 → "$1,055 is the U.S. typical cost of U.S. single-family policies (half pay $713 to $1,309)."
  - 713 (p25) → "…below the middle of U.S. single-family policies…"
  - 700 → "…in the lowest quarter of U.S. single-family policies…"
  - The bands are correct. The median sentence is clumsy ("the U.S. typical cost of U.S. … policies").
- **louisiana** (`P={863,1086,1273,1905}`; `type=number`):
  - 1086 → "$1,086 is the typical cost here (half pay $863 to $1,273, typical $1,086). Renewing? Policies whose term began in 2026 typically pay $1,215."
  - 863 (p25) → "$863 is below the typical cost, cheaper than about half of existing policies here (…)." This is true, but it understates: $863 is cheaper than about 75% of policies.
  - 800 → "$800 is in the cheapest quarter of existing policies here (…)."
- **palm-beach-county-fl** (`P={517,670,1034,1297}`): the same script.
  - 670 → "the typical cost here".
  - 517 → "below the typical cost, cheaper than about half".
  - 500 → "in the cheapest quarter".
- **Round-7 checker defects:**
  - Fixed: "upper-middle" for the median, the ". (" double ending, and "below the lowest quarter".
  - Left: at exactly p25 the sentence says "about half" instead of about three-quarters.

## home

- **MINOR** (checker copy). At the median it prints "$1,055 is the U.S. typical cost of U.S. single-family policies". "U.S." appears twice and "typical cost of … policies" is ungrammatical. It should read "is the typical cost among U.S. single-family policies".
- **MINOR** (carried over from round 7: the search box gives no "no match" message). The script hides every row and prints nothing when a query matches no row (e.g. "orange county fl").
- **MINOR** (carried over: label vs value). "42 counties so far, listed by number of policies" (home-06), but the column and the sort are "Insured units".
- **MINOR** (carried over: two bases on screen 1). "3,490,299 NFIP policy records" sits next to "4.6M insured units" (home-00). The units note explains it, but a reader still sees two "policy" counts.
- **MINOR** (carried over). "Premium plus fees except the last row" (home-03) repeats what the last row's label already says.
- **GAP 1.** No cost by flood zone on home, although every top result answers it second.
- **GAP 2.** Nothing names the SERP's figures ($899 NerdWallet, $888 Policygenius, $786 Insurify) or says which of our rows each one matches.
- **GAP 3.** Private flood: when a lender must accept it, and whether it can be cheaper.
- **GAP 4.** No territories (PR, USVI, Guam), and no line saying they are left out.
- **GAP 5.** Home has no JSON-LD (`grep application/ld+json dist/index.html` finds 0), while the state and county pages have it.

Verdict: PASS

## louisiana

- **MINOR** (new card: rebuild rule wording; louisiana-10).
  - **What it says:** "The NFIP pays the cost to rebuild (not a depreciated value) only for a single-family home that is your principal residence and is insured for at least 80% … or for the $250,000 maximum."
  - **What it matches:** the replacement-cost eligibility in SFIP Dwelling Form §VII.V. The two conditions (principal residence; 80% of full replacement cost or the program maximum) are right.
  - **What it overstates:** the SFIP pays a home under 80% the *greater of* actual cash value or a proportional share of replacement cost (insurance carried ÷ 80% of replacement cost). So "not a depreciated value only for…" makes under-insured owners sound worse off than the rule makes them.
  - **Fix:** add "below 80%, it pays the larger of depreciated value or a share of rebuilding cost."
  - **Caveat:** not web-verified this round (see Method).
- **MINOR** (new card: decade table header; louisiana-06/07).
  - **The mismatch:** the first column header reads "Claims that paid something, by decade of the flood", but the "Claims" column holds *all* claims filed. 13,341 + 68,083 + 73,706 + 237,464 + 63,662 + 29,487 = 485,743, the all-claims total, not the 377,993 that paid.
  - **Values:** they match `extras.claims.by_decade` exactly.
  - **Fix:** relabel the first column "Decade of the flood" and the second "Claims filed".
- **MINOR** (waiting exceptions; louisiana-05).
  - **Now correct:** "no wait if you buy while making, increasing, extending or renewing a mortgage; a one-day wait if a map revision puts the property in a high-risk zone and you buy within 13 months of the revision (44 CFR §61.11)". This now matches 61.11(a)/(b), and the renewal clause is gone.
  - **Still missing:** the post-wildfire exception (61.11(c)). That is low-stakes in Louisiana.
  - **Not stated:** the loan exception requires applying and paying at or before closing.
- **MINOR** (checker). At exactly p25, $863 is called "cheaper than about half", when it is cheaper than about 75%. The input's aria-label says "annual premium in dollars", while the prompt asks for "yearly cost (premium plus fees)".
- **MINOR** (carried over). "Half of homeowners here pay between $863 and $1,273" (louisiana-03). It means half of single-family primary-home *policies*.
- **MINOR** (carried over). "To check a quote, use the checker at the top" (louisiana-03/04). The checker is the section below the hero, not at the top.
- **MINOR** (carried over).
  - **The gap:** event totals include ICC, the yearly bars do not, and the events note does not say so. The payout card now says this for the *average*, but not for the events table.
  - **Visible clash:** Katrina $13.3B + Rita $412.9M are above the 2005 bar of $13.56B.
- **MINOR** (carried over). "Among the five costliest years, these have no named event … : 1995" uses a plural subject for one year (louisiana-09).
- **MINOR** (carried over). "Mid summer severe storms (2016)" has lost its hyphen.
- **MINOR** (carried over). The parish sort is case-sensitive: Jefferson Davis comes before Jefferson, and LaSalle before Lafayette (louisiana-14).
- **MINOR** (carried over). The JSON-LD says "NfipPolicies v3 / NfipClaims v3", while the citation URLs are the -v2 pages. `dateModified` is 2026-10-25, but "The newest of these downloads was October 26, 2026" (louisiana-26).
  - Breadcrumb fixed: `dist/flood-insurance/index.html` now exists.
- **MINOR** (carried over). "up to 35% in Jefferson Parish" (louisiana-20) is qualified only later: "A community named for the parish covers its unincorporated area only".
- **MINOR** (carried over). The H1 "Flood insurance in Louisiana" drops "cost".
- **GAP 1.** No "find your parish" link on screen 1; the parish table starts at louisiana-12.
- **GAP 2.** Insurify's Plaquemines $4,752 vs our $1,231 is not reconciled, and there is no parish mean or full-risk column.
- **GAP 3.** No "years to reach full risk at 18% a year" figure.
- **GAP 4.** Private flood.
- **GAP 5.** No NOAA storm-events panel at state level, though the county template has one.

Verdict: PASS

## palm-beach-county-fl

- **MINOR** (ZIP lookup; downgraded from round-7 MAJOR, see Previous items).
  - **What is still in the lookup:** `ZD` still holds five ZIPs far outside the county: 32507 "Warrington" (Pensacola), 32333 "Havana", and 34401, 34417 and 34394 (Ocala area). Each has 1 unit.
  - **Why the new caveat doesn't cover them:** it says "a ZIP with only a policy or two may mostly lie in a neighboring county", but these are 250–500 miles away. These are mis-geocoded records, not ZIPs in a neighboring county.
  - **What the lookup prints:** "32507 (Warrington): 1 policy units; too few priced policies for a median." "1 policy units" is still ungrammatical.
  - **Fix:** drop ZIPs whose 3-digit prefix is not 334, or reword the caveat to "may be a mis-recorded address".
- **MINOR** (new hero line; palm-beach-county-fl-01).
  - **The line:** "Claims from floods in the 2020s: 34.7% paid something. Top reason for unpaid claims: 'not an actual flood'."
  - **Is the figure right?** Yes. It matches `by_decade` (426 claims).
  - **Do open claims distort it?** No. In the raw FL 2020–2026 rows for countyCode 12099, only about 11 unpaid claims have no reason code, which is the most that could still be open.
  - **What is wrong is the wording:** "claims from floods" for a pool whose top unpaid reason is "not an actual flood". Of the 2024–2026 unpaid claims, most are coded 06 (not a flood) or 99 (assigned in error).
  - **Fix:** say "Claims filed in the 2020s".
- **MINOR** (new card: decade table header; palm-beach-county-fl-07). Same as Louisiana: the header reads "Claims that paid something", but the column holds all 10,758 claims.
  - **Values:** they match extras exactly.
  - **Arithmetic:** the 2020s share works out to 4,681 paid, which matches "Claims that paid 4,681".
- **MINOR** (rebuild rule wording; palm-beach-county-fl-10). The same under-80% overstatement as Louisiana.
  - **The headline** is now correct: "Not in full for at least 50.6% … above the $250,000 building limit". The unsourced "can carry the full limit…" note is gone, and the different bases are stated.
  - **The numbers:** 91.5% at the maximum vs 50.6% above the limit implies many homes are insured above their reported rebuilding cost. The page no longer explains this, which is acceptable.
- **MINOR** (waiting exceptions; palm-beach-county-fl-05). Correct now. Only the post-wildfire exception is missing.
- **MINOR** (checker). The same p25 "about half" and aria-label issues as Louisiana.
- **MINOR** (carried over: Opal). "these have no named event in this table, because FEMA filed their claims under a general label: 2025, 1995, 2014" (palm-beach-county-fl-09).
  - **Why it is false for 1995:** 1995 does have a named event, Hurricane Opal (7 claims, $1,356,819, `extras.claims.events[6]`). It is dropped from the table, yet it out-pays the listed Wilma ($1.12M).
  - **Data flag:** a $193,831 average for a Panhandle-landfall storm is itself a geocoding warning sign.
- **MINOR** (carried over). ZIPs 33437 and 33446 have no town, and 33428 is "Watergate", a CDP name (palm-beach-county-fl-12).
- **MINOR** (carried over). "downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing" is a comma splice (palm-beach-county-fl-01).
- **MINOR** (carried over). "Half of homeowners here pay…" and "use the checker at the top": the same as Louisiana.
- **MINOR** (carried over). The "No CRS discount (15)" list is not alphabetical; it starts "Westlake; Atlantis; Belle Glade…".
- **MINOR** (carried over). The NOAA "$71.1 million" (1996-2025, hyphen) sits a few screens from the NFIP "$72.0 million" (1978–2026).
- **MINOR** (carried over). The "How often is this county a flood disaster?" heading lists hurricane declarations that were mostly wind (Milton, Nicole).
- **MINOR** (carried over). The JSON-LD has v3 text with v2 URLs, and `dateModified` is 10-25 against a newest download of 10-26.
- **GAP 1.** Private flood: whether a lender or Citizens accepts it, and how its price compares.
- **GAP 2.** No row naming NerdWallet's $528 or MoneyGeek's $466; our "Typical premium only $507" sits between them, unmentioned.
- **GAP 3.** No ZIP-level below-full-risk share or full-risk median; news results answer "how much will my ZIP rise".
- **GAP 4.** No cost by municipality.
- **GAP 5.** No paid share by named storm. It would show whether a real hurricane flood claim here pays more often than the 43.5% all-claims figure.

Verdict: PASS

## Classes

**State + county template:**
- **MINOR.** The decade table's first header says "Claims that paid something", but the column is all claims filed.
- **MINOR.** The rcv_80 sentence leaves out the under-80% settlement: the greater of ACV or a proportional share of replacement cost.
- **MINOR.** The waiting exceptions leave out the post-wildfire exception (61.11(c)).
- **MINOR.** The checker at exactly p25 says "cheaper than about half". The aria-label says "annual premium", while the prompt asks for premium plus fees.
- **MINOR.** "Claims from floods in the 2020s" in the hero tile should be "claims filed".
- **MINOR** (carried over).
  - Events include ICC and the year bars don't, and the events note doesn't say so.
  - "Half of homeowners" means policies.
  - "checker at the top".
  - JSON-LD v3/v2 and the dateModified lag.

**County template:**
- **MINOR.** The lookup keeps out-of-region single-unit ZIPs, and the "neighboring county" caveat misdescribes them. "1 policy units".
- **MINOR.** The events table drops low-count named events, while the note says those years have none.

**State template:**
- **MINOR.** The parish sort is case-sensitive.
- **GAP.** No parish link on screen 1 and no NOAA panel.

**Home template:**
- **MINOR.** No "no match" message in the search box.
- **MINOR.** "number of policies" sits over an "Insured units" column.
- **MINOR.** The checker's median sentence is ungrammatical.

## Previous items (round-7 BLOCKER/MAJOR)

**home:** none in round 7.

**louisiana**
- **BLOCKER** "or change coverage at renewal" in the waiting exceptions: **FIXED**.
  - **Now reads:** "Exceptions: no wait if you buy while making, increasing, extending or renewing a mortgage; a one-day wait if a map revision … within 13 months … (44 CFR §61.11)" (louisiana-05; extracted text line 165).
  - **Check:** the renewal clause is absent, and the remaining clauses match 61.11(a)/(b).
- **MAJOR** rebuild headline counts only the cap, plus an unsourced note: **FIXED**.
  - **Headline now:** "Not in full for **at least** 21.5%…".
  - **Note:** the unsourced "can carry the full limit on a home whose reported rebuilding cost is lower" is gone. In its place: "Homes insured for less than their own rebuilding cost can also fall short", plus the different-bases sentence (louisiana-09/10).

**palm-beach-county-fl**
- **BLOCKER** renewal waiting exception: **FIXED**, with the same text as Louisiana (palm-beach-county-fl-05).
- **MAJOR** ZIP lookup (ZIP+4 keys, out-of-county ZIPs, "All 71"): **PARTLY**.
  - **Fixed:**
    - `ZD` now has 61 keys, all five digits; the ZIP+4 keys are gone.
    - The copy says "All 61 ZIPs on NFIP policy records here", which is literally true.
    - A caveat was added.
  - **Still there:**
    - 32507, 32333, 34401, 34417 and 34394 remain, at 1 unit each.
    - The caveat calls them "neighboring county".
    - "1 policy units".
  - **New tag:** the count is no longer wrong and the stray ZIPs carry 1 unit each, so this is now a MINOR.
- **MAJOR** rebuild card: **FIXED** (same changes as Louisiana; palm-beach-county-fl-10).
- **MAJOR** scary "43.5% paid" with no era context: **FIXED**.
  - **Added:** the by-decade table (palm-beach-county-fl-07, matching `extras.claims.by_decade`) and a 2020s line on screen 1.
  - **What the data shows:** the round-7 guess that unpaid claims were old small-rain claims was wrong. Recent decades pay less often (2000s 34.9%, 2020s 34.7%).
  - **Open claims:** the raw 2020–2026 rows show only about 11 unpaid claims with no reason code, so open claims do not distort the share.
  - **Where the reader stands now:** the figure is real, and the reason ("not an actual flood") sits beside it on screen 1.
  - **Left over:** wording only ("claims from floods"), logged as a MINOR.

**Tally (6 round-7 BLOCKER/MAJOR items):** FIXED 5, PARTLY 1 (the Palm Beach ZIP lookup, now a MINOR), NOT FIXED 0.

**Round-7 minors fixed this round:**
- The checker's "upper-middle" for the median, the ". (" double ending, and "below the lowest quarter".
- The breadcrumb 404 (`dist/flood-insurance/index.html` now exists).
