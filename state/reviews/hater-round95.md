# hater round 95 (light text review, changed parts only)

## home
**MINOR** Zone cost card order "AE, X, VE, A, AO, AH": neither policy count (X is largest, VE 18k sits above A 91k) nor cost order; reader may read it as a ranking. Fix: sort by policy count, or say "main zones" in the caption.
**MINOR** "Bought with a new or refinanced mortgage: Can start at closing" (palm table, same on home flow): the manual says making, increasing, extending or renewing a loan; "new or refinanced" is narrower but not wrong. Fix: reuse the manual's four verbs.
Figures checked: zone medians and counts on home equal the AE page table; 6 zones, none with a count under 50.
Verdict: PASS

## louisiana
**MINOR** "Pick your parish" lists 23 parishes (those with a page) while the state has 64; the summary does not say so, and "Find your parish in the table" below covers the rest. Fix: "Pick your parish (23 with their own page)".
**MINOR** Tile "52.8% Still pay less than FEMA's full-risk price" names no base. The base (single-family primary-home policies) is only in the card further down. Fix: add "of single-family policies" to the tile label.
**MINOR** Regulator line is the NAIC directory fallback; correct and honest.
Figures checked: "Zone X $1,082, Zone AE $1,259" match the policy-count order in the zone table (X 174,352 then AE 157,736); the AE national table gives Louisiana AE $1,259.
Verdict: PASS

## palm-beach-county-fl
**MINOR** Tile "23.2% Still pay less than FEMA's full-risk price" has no base on screen 1 (50,039 policies, single-family primary homes, appears only in the card). Fix: label it.
**MINOR** "Your state's insurance regulator: Florida Department of Financial Services (consumer help)": Florida's rate regulator is the Office of Insurance Regulation; the page is DFS consumer help. The "(consumer help)" tag keeps it true, but "regulator" is loose. Fix: "Your state's insurance help line" or name both.
**MINOR** "Policies first bought in the past year typically pay $627": "typically" is not tied to median on this card. Fix: "median".
Checked and correct: 1,200+289+127+106 = 1,722 LOMA rulings; 34.3+4.7+1.9+1.2 = 42.1% high-risk; community discount "25 of 40, up to 30% (Boynton Beach, CRS class 4)" matches the table; zone line order X then AE matches policy counts; loma_fee and loma_online wording stay within their quotes; the "no new flood map" sentence is scoped to FEMA's Community Status Book. The 44 CFR 72.5 "no fee" line sits near the 65.17 "a fee applies" line, but each is scoped to its own request type.
Verdict: PASS

## new-york-county-ny
**MINOR** Quick answer "Zones with the largest policy counts here: Zone X $953" omits Zone AE (41.8% of policy units) with no hint why (fewer than 50 priced single-family policies). A reader in AE gets no number and no gap line on screen 1. Fix: append "Zone AE: too few single-family policies for a median".
**MINOR** "FEMA's latest Community Status Book lists no new flood map taking effect" may read as "no map change coming" while preliminary maps can exist before the book lists them; the next sentence (prelim link) partly covers it. Fix: join them: "...lists none yet; preliminary data may come earlier".
**MINOR** The flood-map note omits the current map date, which the CSB gives (09/05/07) and Palm Beach prints. Inconsistent, not wrong.
Checked: "No community discount here" matches the CSB record (classRating null); 41.8+1.0 = 42.8% high-risk.
Verdict: PASS

## national pages (ae, flood-zone-map, renters)
**MINOR** renters: "A standard NFIP home policy does not pay for a hotel..." on a page about contents-only renter policies. The source (44 CFR Part 61 Appendix A(1), the dwelling form) is the form that policy uses, so the facts hold, but "home policy" makes a renter ask "is that mine?". Fix: "A standard NFIP policy" (the not_covered rule text is shared, so change it once).
**MINOR** ae and flood-zone-map: "FEMA charges no ... fee for a Letter of Map Amendment request" is followed directly by "Online LOMC ... Letter of Map Change". LOMC covers other letters (revisions) that do carry fees, so a skimmer may read "free" as covering LOMC. Fix: put the fee sentence last or say "a Letter of Map Amendment is free; other map changes may cost".
**MINOR** ae: "Full-risk price ... median $1,443 (premium only before fees), not comparable with the cost above" is honest; the glide sentence uses "statutory discounts" and "increase cap discount" without a plain gloss. Fix: add a plain clause.
**MINOR** flood-zone-map: the heading "Is my map about to change?" gets only a link to preliminary data, not an answer. Fix: "Early look at proposed map changes".
Checked: the ae zone table equals the home table; no "you should" in any added line; the prelim and loma rules stay within their quotes.
Verdict: PASS
