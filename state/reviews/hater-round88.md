# Hater round 88 (light, text only)

Recomputed from data/us/renter_hist.json (51 states, running count reaching p of total): U.S. n=6,397, quartiles $307 / $369 / $513 (page matches). FL n=2,215, $320/$398/$595 (page $398, 2,215 matches). HI n=49, median $610 (matches). No zero or negative costs in the histogram. All 7 FloodSmart quotes (renters_cover x3, limits x3, wait_30, same-rates) found in raw https://www.floodsmart.gov/get-insured/buy-a-policy page text fetched with curl; "$500,000" business line is real.

## home
Checked: tile "Policy units in force" (4.5M) with its note ("every NFIP policy unit ... including condos, rentals and businesses"); link "What renters pay".
- PASS: tile label now matches the base; the note beside it defines units; the nearby "3,446,101 NFIP policy records" line explains records vs units, so no contradiction.
- PASS: "What renters pay." link sits with the other three links, text-only, goes to a real page.
- MINOR: the link text "What renters pay." is a sentence fragment, like the neighbours; fine, but it says nothing about it being NFIP-only.
nfip:
- PASS: the `limits` sentence ("For a home, ... $250,000 ... contents ... $100,000; a renter's contents coverage ... $100,000; for a business, building and contents each go up to $500,000") equals FloodSmart's three sentences (home / renters / business). Scope named (home, renter, business). "Goes up to" keeps the source's "up to".
- MINOR: FloodSmart says the $250,000/$100,000 figures are for "a home"; the page does not say these are the maximums for residential one-to-four family, not 5+ unit buildings. Source does not say either, so not wrong.
Verdict: PASS

## renters
Numbers: all verified (see top). Labels: "Median / yr, NFIP renter policy", "Middle half / yr", "Priced renter policies" match the base (tenant flag, residential codes, building 0, contents > 0, cost > $0). "premium plus fees" matches the home pages' base. State table: 19 states with n >= 30, most policies first, floor stated. Four rule() sentences equal their quoted sources (renters_cover, wait_30, same rates, FDIC 339.3(c) text).
- MINOR: private_accept sentence says "federally regulated lenders" but its one quote is the FDIC rule (12 CFR 339.3); OCC, Fed, NCUA and FCA rules are not quoted. Guardrail 2/3 (scope, quote behind each sentence). Not a renter-actionable error, but the scope word is wider than the quote.
- MINOR: that lender sentence is aimed at mortgages; a renter has no mortgage, so on this page it reads as off-topic. A renter's real question is "do I have to buy?": the page does not say (no source printed that renters are never required; absence is not a defect, but a GAP below).
- MINOR: 6,397 renter policies against ~4.5M units is a rare product; the page does not say how few renters carry it. Not wrong; a renter might wonder if $369 is typical of many people.
- GAP: no "does a renters policy cover my belongings at actual cash value, what is excluded (living costs, items outside the building)" line; the county pages have it (`rule()` exists for homes). A renter's top question #2.
- GAP: no "am I required / do I need it if my landlord has a policy" answer; no dataset, so a printed gap line would be right.
- GAP: no ZIP/county renter cost link (data thin; renters link to ZIP lookup of single-family homes, labelled as such, honest).
Verdict: PASS

## palm-beach-county-fl
Checked (a) meta description names "(Boca Raton, Palm Beach, West Palm Beach)" after the county; (b) LMA last sentence.
- PASS: towns come from `_towns()` (Census place in this county, ranked by NFIP policy units in their ZIPs), same list the page's ZIP card prints; "Palm Beach" is a small town but ranks high by policy units, true to the stated method. The description does not claim "largest towns".
- MINOR: description is now ~300 characters; Google will cut it in the results page, so the "131,028 insured units" tail may be dropped. No wrong text.
- PASS: LMA sentence "They are counted by the NFIP communities FEMA's Community Status Book files under this county, so a city that reaches into a neighboring county counts in full here." States the base honestly and agrees with the 1,722 count line before it. Adjacent sentence "These are rulings for owners who applied, not a share of all homes." intact.
Verdict: PASS

## new-york-county-ny
Checked (a) description; (b) LMA sentence.
- PASS: description shows no parenthetical (the page prints no town list, fewer than two towns), so no empty "()" and no wrong name.
- PASS: page has no Letters of Map Amendment paragraph, so the new sentence is correctly absent (no stray text found).
- MINOR: New York County is Manhattan; a reader who searches "Manhattan flood insurance" sees only "New York County" in the description. Not wrong; a GAP at most.
Verdict: PASS

## Classes
- Description now variable length with town list (county template): long county names plus 3 towns can push past ~160 characters; trimmed by Google, not wrong.
- Lender sentence (`private_accept`) scope wider than its single FDIC quote: any page using it.
