# Hater round 114 (LIGHT, text only)

Method: tag-stripped text of the named cards plus a skim of screen 1, per page. Arithmetic spot checks: event rows (claims x average = total) and zone shares add up. One web check: citizensfla.com/flood confirms Citizens does not sell flood and the 2023/2026/2027 phase-in, so the Citizens rule wording passes. Not read: fixlog, gate code. Not done: screenshots, JS behaviour of the search box, FEMA live service.

## home
- **MINOR** "What does it cost by flood zone?" count column "Policies" (AE 961,977, X 1,018,718 ...) sits under a note that says "NFIP policies in force on August 31, 2026" and "96,809 policies ... left out". The five rows plus 96,809 add up to about 2.3M, against 4.5M policy units in force, so these are single-family priced policies, not all policies. A hurried reader takes the column as all NFIP policies. Name the base in the column header.
- **MINOR** "Rules from agents.floodsmart.gov, ecfr.gov, ..." lists domains with no dates. The county cards give "checked October 25, 2026". Same line, same trust.
- **GAP** "Where do I buy it?" gives the phone number, FloodSmart and agents, but not the 30-day wait next to the buy line (it is in the line above, so fine on screen).
- Checked and PASS: kicker "(not Puerto Rico or other U.S. territories)" matches "50 states and DC"; $1,066 / 12 = $89; the "Where do I buy it?" line and the private-flood sentence are scoped (federally regulated lenders, federal definition).
Verdict: PASS

## louisiana
- **MINOR** Parish table search box (`#cf`): placeholder and aria-label only, no `type=search` and no `inputmode`. Nothing says what happens when no row matches: all 64 rows just disappear, with no "no match" line (checklist J asks for a no-match message). Mostly a GAP, not a block, because the table still works.
- **MINOR** Table column "Below full-risk" has no unit or base in the header. The share of what is not stated beside the table.
- **MINOR** Two lists of parishes: "Pick your parish (those with their own page)" has 23 names, and the table has 64. The wording is fair, but a reader may think 23 is the full list.
- Checked and PASS: risk card sums are 64 for coastal (2+8+11+4+4+35) and 64 for inland (0+6+13+24+21+0); the lead "10 ... Very High or Relatively High coastal, 6 inland" equals 2+8 and 0+6. "No rating for this kind of flooding" has 35 coastal and 0 inland, and the label is honest. Event table sorted by total, the share column is plausible, Katrina $13.3B / 128,268 = $103.7k matches. Screen 1 "Zones X $1,082, AE $1,259 a year (median, single-family homes)" matches the base label. Table "too few" rows (Winn) are labelled.
Verdict: PASS

## palm-beach-county-fl
- **MINOR (unverified, same class as the sonoma-county-ca MAJOR)** "Towns here, ranked by NFIP policy units in their ZIPs: Boca Raton, Palm Beach, West Palm Beach, Delray Beach, Boynton Beach." The ZIP table above shows 33418 Palm Beach Gardens (3,127 units) and 33410 Palm Beach Gardens (2,386), together 5,513, plus Jupiter 2,504 and Royal Palm Beach 2,935. None of these towns is in the ranked list. The page data does not show Palm Beach's own units, so I cannot prove the ranking wrong here, but the list looks name-filtered, not ranked.
- **MINOR** The ZIP table names a town for some rows (33418, 33411, 33458, 33410) and not for others (33437, 33446, 33428, 33467), so a reader cannot tell Boca from Delray.
- **MINOR** The ZIP table shows 8 of 61 ZIPs. "The ZIPs with the largest number of priced single-family policies" says it is a subset but not how many; it is weakly disclosed. Say "8 of 61".
- Checked and PASS: new penetration card, 13.0% is "about 1 in 8" (1 in 7.7); high-risk 43.4%; FL 13.7% base shown. Condo line "median cost of $526 a year ... 7,901 priced policies", with the single-family exclusion stated beside it. Event table: Frances 507 x $22,332 = $11.3M; Wilma 12.3% paid with 81 paid claims is consistent (about 660 filed); claims versus share make sense; the note defines base. Screen 1 "Zones X $620, AE $1,228" matches the zone table below it.
Verdict: PASS

## new-york-county-ny
- **MINOR** Find-your-ZIP table has ONE row (10014, $1,369, 37 priced policies, 75.7% below full-risk) out of 53 ZIPs, and there is no range line. A single-row table of 37 policies reads as "the" Manhattan ZIP price, next to a county median of $1,021. The note says "largest number", but not "only ZIP with 30+".
- **MINOR** Penetration card "Residential policies in FEMA's count 1,854" and zone card "159 priced" are different bases on one page, and each is labelled. Fine, but they are close to each other in the reader's head.
- Checked and PASS: title and H1 both read "(Manhattan)". Screen 1 "Zone X $953 a year (median, single-family homes); Zone AE, 41.8% of policy units, has too few to price" agrees with the zone card (X only, AE under the 50-policy floor). Condo-unit line $725 / 525 priced policies is labelled. Penetration 1.5% equals "1 in 67". Event table: Sandy 442 x $252,071 = $111.4M; Ida 58 x $32,590 = $1.9M; sorted by total; share column makes sense (Irene 23 paid at 39.7% is about 58 filed).
Verdict: PASS

## sonoma-county-ca
- **MAJOR** "Towns here, ranked by NFIP policy units in their ZIPs: Monte Rio, Santa Rosa, Windsor, Rohnert Park, Bodega Bay." Data (`agg.json` by_zip) and the ZIP table on the page: 95446 has 611 units (the largest ZIP in the county, no town named), 95462 Monte Rio 222, 94952 171, 95476 161, 94954 147, 95436 134, 95448 122. Windsor 95492 has 83 units and is listed third, while ZIPs with 171, 161, 147, 134 and 122 units are not. The "ranked by policy units" label is broken, and the biggest ZIP is missing. A reader looking for Guerneville or Petaluma finds neither. Check that should have caught it: a gate that recomputes the town list from by_zip units and compares it with the printed order.
- **MAJOR** Title "Sonoma County, CA (Monte Rio) ..." names Monte Rio as the county's place, but Monte Rio has 222 units against 611 in 95446. Same root cause (the place-name picker). Only the Google snippet and the tab show it, but it is the first thing a searcher reads.
- **MINOR** Event table has 3 rows (Flooding 1978-1997, Pineapple Express 1998, Atmospheric River 2022-23), and the note says "among the five costliest years, these have no flood of their own: 1995, 2019, 2005, 1986, 1997". All five costliest years are absent, so the table covers none of them. The note says so, which is honest, but the table adds little for this county.
- **MINOR** Condo-unit median "$636 ... 32 priced policies" is just over the 30 floor. Say "only 32 policies" or hold it back.
- Checked and PASS: LOMA card: 364 + 52 + 57 + 10 = 483, and "not the odds for your home, and FEMA's map service gives no dates for them" is present and true to the counts. Pineapple Express 284 x $12,188 = $3.46M. Penetration 1.1% = "1 in 91". Screen 1 zone line AE $1,588, X $1,201 matches the base label.
Verdict: FAIL

## levy-county-fl
- **MINOR** The ZIP table shows 4 of 13 ZIPs with no "4 of 13" wording (the range line above it names the extremes, so a reader is not misled).
- **MINOR** Screen 1: "Zones AE $2,357, A $958" are 2.5x apart with no hint why (Zone A has no elevation-based pricing). A reader may think A is a bargain. A GAP, not a block.
- Checked and PASS: screen 1 "Zone VE, 21.5% of policy units, has too few to price" is on the right base (units, not policies) and VE is absent from the priced table. LOMA card: 21 + 4 + 17 + 2 = 44, and the "not the odds ... no dates" sentence is present. Florida Citizens rule matches citizensfla.com (flood from NFIP or private, not Citizens; $400k from 2026, all from 2027; condo and no-wind exempt). Penetration 4.3% = "1 in 23". Event table sorted by total; Helene 253 x $99,684 = $25.2M. No condo line (no condos), which is right.
Verdict: PASS

## dixie-county-fl
- **MINOR** "That is the same as the Florida median of $985" while the county is $987. Two dollars apart is "about the same", and a copy editor will flag "same as".
- **MINOR** Three counts, three bases: "435 in-force policy records", 567 policy units in the zone table, 556 residential policies in the penetration card. Each is labelled, but the first line of the sources block says "all 435 ... records" next to a table that sums to 567 units.
- **MINOR** Screen 1 prices only Zone AE and says Zone A is "too few to price"; Zone VE (4.2%) gets no mention. The zone card is correct (AE only), and VE is the one the reader at the coast cares about. A GAP.
- **MINOR** ZIP table shows 2 of 10 ZIPs. Range line names the extremes, so no one is misled.
- Checked and PASS: penetration 5.8% = "1 in 17"; condo line absent (none shown, fine). Event table: Helene 124 paid at 87.3%, Idalia 58 at 77.3% (about 75 filed), all sorted by total, "Blizzard of 1993" is FEMA's name for the March 1993 storm. High-risk share 96.1% = (458+59+24+4)/567. New column "Premium below full-risk" definition note sits under the table.
Verdict: PASS

## Classes
- **County, MAJOR class:** the "Towns here, ranked by NFIP policy units" line and the title's place name come from a name map, not from the by_zip units. Sonoma proves it; Palm Beach looks the same. Fix: build the town list from by_zip (sum units by place), or cut the word "ranked". Add a check S/Z-level that recomputes the order.
- **County, MINOR class:** the ZIP table shows the top N ZIPs without "N of M"; a one-row table on a county with 53 ZIPs (New York) reads as a fact about the whole county.
- **County, MINOR class:** screen 1 "too few to price" names only the zone with the largest share; a smaller coastal zone (VE) goes unmentioned.
- **State:** the parish and county search box has no "no match" line; the "Below full-risk" column header has no base.
- **Home:** the zone-table "Policies" column does not say it counts single-family priced policies.

Counts: home 0 BLOCKER / 0 MAJOR; louisiana 0 / 0; palm-beach 0 / 0; new-york 0 / 0; sonoma 0 / 2; levy 0 / 0; dixie 0 / 0.
