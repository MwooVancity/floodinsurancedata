# Everything wrong, 2026-10-27 (after round 6)
Source: hater-round6.md, fixlog-round5.md, and what I (Claude) did across rounds 1-6. Nothing here is fixed yet.

## A. Why the rounds themselves are bad (process)
1. Builder and reviewer are both Claude. Same blind spots, same habits. No human reader and no real search data have judged a page.
2. My fix log claimed fixes that are not on the page. Louisiana 1995 was marked FIXED; the page has zero matches. The reviewer caught it, not me.
3. The gates check that numbers match our files. They never check that a sentence is TRUE. The Citizens rule was wrong and passed every gate.
4. The review is open-ended ("beat #1"), so every round finds a fresh set of gaps. Six rounds, zero passes. No fixed finish line.
5. Fixes patch the example, not the class. Example: I named unnamed years only if they were in the top 3, so the 4th (1995) still vanished.
6. I wrote explanations without checking the code. "The two shares count different policies" was a guess; the real reason is different.
7. Only 3 pages are reviewed. The other 90 are assumed fine because they share a template.
8. The quote checker and the search box have never been tested by a reviewer.
9. Each round costs about 200,000 tokens, mostly spent reading screenshots instead of fixing.
10. No real-user signal: Search Console is 25 days stale and unused in review.

## B. Wrong or misleading on the page (reader harm, fix first)
1. Louisiana: the 1995 flood ($605M, 4th costliest year) is missing from the "biggest floods" card. FEMA's catch-all "Flooding" row (97,855 claims, $1.14B) is silently dropped.
2. Palm Beach: Hurricane Opal 1995 and the catch-all "Flooding" ($1.64M) are dropped the same way.
3. Rebuild card (every page): the note "count different policies" is wrong. Insured-to-max = $250K cover over ALL single-family policies; the rebuild share = only those reporting a rebuild cost. Many look insured above their own rebuild cost; the page never says so.
4. Rebuild card: missing the rule that NFIP pays replacement cost only to a primary home insured to 80% of its rebuild cost.
5. Zone table (state pages): the note says A1-A30 are "now shown as AE", then the table prices A01-A15, V15 and AHB as separate rows at different prices.
6. Screen 1, every page: "Many unpaid claims are no-damage or paperwork closures." In Louisiana the top reason is "Not an actual flood", which is a denial.
7. Palm Beach screen 1: "43.5% of claims paid (Florida 69.9%)" with no context. The card below says "many with no specific reason recorded"; reasons exist for 86.9%.
8. Louisiana headline, title, meta and quote checker use $1,086 (mixed 2025/2026 terms). Renewals in 2026 pay $1,215. A renewing reader is judged against the older pool.
9. Home headline $1,055 vs $786-$899 everywhere else, with no premium-only row to explain the gap.
10. Elevated vs not elevated ($854 vs $859, Louisiana) reads as "elevating does nothing".
11. Palm Beach: NFIP "$72.0M paid since 1978" sits near NOAA "$71.1M damage since 1996". Different things, easy to merge.
12. Palm Beach: NRI modeled loss $178.9M a year sits beside $72M paid in 48 years.
13. "Below full-risk price: bills step up yearly" on Palm Beach, where the median ($507) is within $7 of full risk ($514).
14. "67 federal disasters" has no period; one 2021 entry is called a "distinct storm".
15. Claims chart shows 2025 and the partial 2026 with no "claims still open" flag.

## C. Gaps vs the top Google results (to-do, not blocking)
1. No cost by flood zone on home (A/V vs X). Every top result has it.
2. Private flood: one line only. Lenders must accept private flood (42 U.S.C. 4012a(b)); Florida readers shop it.
3. Insurify's Plaquemines $4,752 vs our $1,231: no county-level full-risk or mean figure to reconcile.
4. No "find your parish/county" link on screen 1 of state pages. Parish table is 11 phone screens down.
5. Pages are 24-26 phone screens long. Answers are buried.
6. Same paragraphs word for word on every page: Already flooded, Yearly cap, waiting exceptions, claim-closure explainer, elevated caveat. Home "Three things to know first" too.
7. Per-parish penetration and multiple-loss counts are in the data but not shown. State pages have no NOAA panel.
8. Only 42 of about 3,100 counties have pages. Unknown what the search box does for the rest.

## D. Sloppy basics (minor)
1. Parish sort is case-sensitive ("Jefferson Davis" before "Jefferson").
2. "Mid summer" lost its hyphen.
3. "56.6% of 292,018" crammed into one headline figure.
4. Chart notes use ten-digit dollars ($13,559,493,222) next to "$13.3 billion".
5. Download dates disagree (October 25 vs October 26).
6. JSON-LD says v3 datasets but links v2 pages. Home has no JSON-LD.
7. Quote checker placeholder is "e.g. 1800" everywhere, above Palm Beach's 90th percentile.
8. ZIP towns blank (33437, 33446) or Census names ("Watergate").
9. No-CRS community list not alphabetical.
10. Dash style mixed (1978–2026 vs 1996-2025).
11. Territories (PR, USVI) left out with no note.
12. Home: lone tile leaves an empty slot on screen 1.
13. Citizens sentence tense: "from 2026" reads as future in October 2026.
14. Jargon on screen 1: "Below full-risk price".
