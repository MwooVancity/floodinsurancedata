# Fix log, round 5 (docs/MASTER-PROMPT.md step 1)
One line per BLOCKER/MAJOR in `hater-round5.md`: defect | root layer | fix | proof. No proof = not fixed.
Status: FIXED (proof checked this session), GAP (no public data or check yet; said plainly), LIVE (already shipped).
Build of 2026-10-27: 42 counties + 51 states pass gate.py, test_gate (every mutation caught), phone check, google gate
S1-S11 and S13; S12 (hater review) is what is left.

## Blockers
- B home + B palm-beach: Citizens rule wrong today | rule | `fl_citizens`/`fl_citizens_short` rewritten from s. 627.351(6) para 1 (rebuild-cost phase-in: 2026 at $400K+, 2027 all others) and para 2 (SFHA: new policies April 1, 2023, renewals July 1, 2023) | FIXED + LIVE: excerpts curl-found on flsenate.gov; live Palm Beach page has "in a high-risk zone since 2023". Class check: test_gate fails a rule whose source excerpt states a year the rule text omits.
- B louisiana + B palm-beach: existing stock's full-risk price + mean fees sold as a new policy's price; "a fair new quote can land high" | metric definition | claim removed (LIVE); new metric cost_new = single-family primary policies first written in the 12 months to July 31, 2026 (originalNBDate >= 2025-08-01), on screen 1 ("Buying?") and in the prices table | FIXED: Louisiana $1,139 (n 30,754; reviewer's raw recompute $1,139, n 30,622), Palm Beach $620 (n 4,112; reviewer $620.50, n 4,112). Class check: gate A6 (words "new policy" only on a past-year figure) with a mutation; test_gate checks NB_FROM is 12 months before pull_raw.ASOF.
- B home: no price drivers, no way to pay less, no quote check | missing cards | FIXED: home has "Is my quote normal?" (U.S. single-family quartiles from the national histogram), "What sets the price, and how do I pay less?" (rules price_drivers and save_ways, both curl-verified on floodsmart.gov, plus the U.S. deductible mix) and the four-row "Why do sites quote different prices?" table.

## Majors
- M home: no mean / all-types figure to reconcile with the $888/$899 averages | missing rows | FIXED: home table shows the median, past-year buyers, single-family mean and every-policy-type mean (exact weighted means from each state's records).
- M home: directory, not an answer | template | FIXED in part: the three cards above sit before the tables. The "Three things to know first" rules stay (a rule has one registry text).
- M louisiana: biggest-floods table hid 1995 under the catch-all label | template | FIXED: the event card names every top-3 paid year that has no named event ("Costly years with no named event ... 1995 ...").
- M louisiana: zones C/A99/B share $1,086, unexplained | template note | FIXED: note says many policies are charged exactly the same amount, so several zones' middle policy lands on one price (reviewer confirmed ~21,700 at $1,083-1,086).
- M louisiana + M palm-beach: "official policy count ... not yet compared" | missing check | GAP: the line is removed (it answered no reader question). Comparing to FEMA's published policies-in-force figure needs that table; fema.gov blocks scripts (403), so it is not wired. Not claimed as checked anywhere on the page.
- M louisiana + M palm-beach: no deductible mix / elevated vs not | missing card | FIXED: "Can I pay less?" card on every state and county page: deductible mix table, elevated vs not-elevated median premium with n and the selection caveat, FEMA's ways (save_ways rule), link to the CRS card.
- M louisiana + M palm-beach: shared explainer paragraphs on every page | template | FIXED: 13 how-it-is-counted notes moved to /methodology/#<key> (tools/notes.py), each card keeps only the caveat a reader needs beside the figure plus a "How this is counted" link. google_gate S13 measures it: shared prose per county page median 39%, max 40% (was about 50%); fails above 50%. Same-state similarity fell from 45% to 40% median.
- M louisiana: renewal-term figure secondary | order | FIXED: screen 1 has "Renewing? Policies whose term began in 2026 typically pay $1,215" and "Buying? ... $1,139".
- M palm-beach: county prices table lacked mean and all-types rows | missing data | FIXED: extras_raw now computes averages per county (Palm Beach: single-family mean $882, every-policy-type mean $1,243; its single-family median $670 equals the page's headline, a cross-check).
- M palm-beach: county figures 3-6x the state's | check | FLAGGED: review.flags() routes Palm Beach and Broward to their own review (unpaid share 20+ points from the state's). Earlier proof: 98% of claims in Palm Beach ZIPs carry county code 12099. No FEMA-published county figure exists to compare against.
- M palm-beach: NRI defined two ways; order mismatch | template | FIXED: one definition (rating = modeled loss adjusted for social vulnerability and community resilience) on the page and in notes.nri; lead order coastal then inland, same as the tiles.

## Minors fixed in passing
- Monthly cost rounds half up ($1,086 / 12 = $90.50 -> $91), on every page and home.
- Home county sentence no longer implies these are the 42 largest counties.
- Methodology no longer says pages show "what a new full-risk policy typically costs".
