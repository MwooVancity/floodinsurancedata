# Hater round 109 (light, text only)

Method: extracted visible text of both pages; recomputed the home zone note from `data/us/cost_hist_zone_exact.json` and the NY flood table from `data/all-counties/36061.json`. Fixlog not read.

## home

Checked the target fix first. Summing the zone data: 57 zone codes in total. The six rows shown (AE, X, VE, A, AO, AH) hold 2,223,544 policies, leaving 96,809. The note's figures (A99 26,585; C 26,541; B 14,237; 48 smaller codes; zone D present with 764; old numbered A and V zones present) all match the data exactly. The left-out count is true and the note is clear. Previous item 1: FIXED.

Other checks: the state table sorts correctly by median, and the "Highest / Lowest" lead matches its rows. The county list is sorted by insured units. The "why prices differ" rows are labelled with their base. The Florida Citizens rule is scoped to Florida. Nothing found that misleads a hurried phone reader.

- **MINOR** "What does it cost by flood zone?" The row order (AE, X, VE, A, AO, AH) follows neither median nor policy count, and nothing says how it is ordered. A phone reader scanning for "highest" or "most common" has to read every row. Fix: sort by policy count, or say the order.
- **MINOR** The same table shows "Zone X" but leaves out B and C (40,778 policies), the older names for the same low-risk kind of area. The note discloses this, but it does not say B and C mean the same as X. A newcomer may not connect them.
- **GAP** The note names three left-out codes (A99, C, B) without a plain-word meaning. The "What each means" links cover only the shown zones plus D.

Verdict: PASS

## new-york-county-ny

Previous item 2 (the "Unnamed flood" row): FIXED on the main point. The row now reads "Floods FEMA did not name (1979–1980): many floods; FEMA's records use this name for claims in several years", so it no longer reads as one flood. The lead names Sandy, which is correct. The table is sorted by total paid ($111.4M, $1.9M, $1.3M, $946,774, $624,518, $182,102, $156,647). Claims times average equals total for every row. The values match the data (FEMA's own label is "Not a named storm"). Everything else on the page is internally consistent. Claim counts sum to 1,498; decades sum to 1,498; unpaid reasons sum to 581; zone units sum to 14,925.

- **MAJOR** "Which floods paid out the biggest totals here?" The closing note says: "Among the five costliest years, these have no flood FEMA named for that year alone: 2023". This is false. The data holds a FEMA-named 2023 flood, "Late-September New York Flooding" (16 paid claims, $811,379, year 2023 only). It is missing from the table only because of the 20-paid-claim cut-off. A reader is told FEMA named nothing for 2023 when it did, and that flood paid more than three of the rows shown. Check that should have caught it: the note must test "no named event in the data for that year", not "no event in the table". Fix: reword to "no flood in the table", or list the named event.
- **MINOR** Same table. Because of the 20-claim cut-off, the "biggest totals" list shows Flooding ($624,518), Halloween ($182,102) and the unnamed row ($156,647) while leaving out a bigger named flood ($811,379). The cut-off is disclosed under the table, but the heading promises the biggest totals. Fix: add "among floods with 20+ paid claims" to the heading or the lead.
- **MINOR** The row "Floods FEMA did not name (1979–1980): many floods; ... several years" asserts "many floods" and "several years", but the data says only two calendar years (1979, 1980) and cannot say how many floods. Fix: "possibly more than one flood; FEMA's records use this name for claims in 1979 and 1980".
- **MINOR** The row "December Storm   Nor'easter (1992)" has lost its dash (FEMA's name is "December Storm - Nor'easter"). The display shows a gap of three spaces.
- **MINOR** The claims lead says "Floods ... have led to 1,498 NFIP flood claims". That count includes 160 claims FEMA recorded as "not an actual flood" and 47 "assigned in error". The unpaid-claims card discloses this. The lead overstates the number of floods.
- **MINOR** "Hurricane Sandy alone paid $111.4 million including code-upgrade (ICC) pay". The data shows exactly one ICC claim in the county ($15,660), and Sandy's total ($111,415,427) equals the 2012 yearly total, which leaves ICC out. So the ICC wording cannot be right for Sandy. The effect on the reader is nil, but the sentence is wrong.
- **MINOR** The risk card on screen 1 says "Very High inland (river) flood risk". The detail below says loss per dollar of building value is "higher than about 27% of U.S. counties". The page explains that the rating weighs other things, but a hurried reader sees "Very High" on screen 1 and the lower figure only far below.
- **MINOR** "Average cost, every policy type $4,844" sits next to a typical cost of $1,021. It is labelled (adds condos, rentals, businesses), but a scared homeowner could take it for a typical price.
- **MINOR** "Data: declarations through 2021" on the disasters card. Other county pages say "through 2024". This looks like "latest declaration in this county", but it reads as the dataset's end date.
- **GAP** "Find your ZIP in this county" lists one ZIP row out of 53, so the table helps little (the lookup box does the work).

Verdict: FAIL

## Classes

- County template: the "five costliest years ... no flood FEMA named" note compares against the filtered table, not the named events. It is false on any county where a named event with fewer than 20 paid claims falls in a top-5 year. Fix at the source: take the check from all named events, and add a mutation test with a 19-claim named event.
- County template: the event table's 20-claim cut-off plus a "biggest totals" heading. The same mismatch appears wherever a smaller named flood out-paid a shown generic row.
- County template: event names are shown with punctuation stripped ("Storm   Nor'easter").
- Home template: no class defects found. The zone note is now computed from the data and is true.
