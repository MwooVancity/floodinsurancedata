# Hater round 205 (light, text only, Read/Grep)

Scope read: home (whole body, county list not read); flood-zone-map, AO, AH, VE, renters, both guides (whole); NJ, Pinellas, Louisiana, Palm Beach (hero, quick-answer nav, and the "Am I required to buy it?" card; the other cards on those four pages were not changed this round and were not re-read). Arithmetic re-checked: AO/AH/VE average paid claim, AH "86% in Florida" (91,505 of 106,626), Pinellas / Louisiana / Palm Beach / NJ high-risk share and zone table sums, Pinellas LOMA split (1,371+115+331+215 = 2,032), renters state sum (<= 6,397), both guide state tables (51 rows, sorted, min/max in the lead sentence match).

## home
Verdict: PASS
- MINOR "What people with federal flood insurance actually pay where you live, whether you are required to buy it, and how fast it starts." | The searched question ("how much is flood insurance") gets no number in the first ~40 words; the lede, the search box and the heading come first, and "$1,066" is the first figure, about word 60 (still on screen 1). Owner chose search-box-first, so this is logged, not blocked. | If a gate wants it: put the median in the lede sentence.
- MINOR "$89 / Per month" | Label alone does not say it is the median divided by 12; the caption below does ("median and per-month figures are what existing policies on single-family primary homes pay"). | "Median per month".
- MINOR "Highest typical cost: Connecticut $1,510 ... Lowest: Maryland $569, District of Columbia $384, Alaska $368" | "typical" here is the single-family median; the table header says "Median / yr". Consistent, but the lowest three are listed highest-first inside the "Lowest" list. | Optional.
- Checked, fine: $1,066 / 12 = $89; "Policy units ... including condos, rentals and businesses" is stated next to the 4.5M; the "Does my homeowners policy cover floods?" link target (homeowners-insurance-flooding) does contain the outside-the-zone text it promises; #prices anchor exists; zone table footnote says which rows are left out and why.

## louisiana
Verdict: PASS
- MINOR Cost trend line "The median policy cost $572 in 2021" | Palm Beach shows the identical 2021 figure ($572). Probably a coincidence (different 2026 values, $1,114 vs $673) but worth one data spot-check; not claimed wrong. | Spot-check extras.policies.cost_trend.0.median for both counties.
- Checked: 51.3% high-risk = (157,736 + 21,130 + 6,151 + 21,022) / 401,925; zone shares add up; "(34 communities)" list agrees with its count text; hero gives the median on screen 1.

## palm-beach-county-fl
Verdict: PASS
- MINOR "Does it pay out? 46.8% of claims ... paid something (FL 72.8%)" | Far below the state; the sentence "No recorded payment can mean paperwork or damage the policy did not count as flood" is on that line, so it is not misleading. A reader may still read 46.8% as a denial rate. | Optional: say "no recorded payment" instead of "paid something" share.
- Checked: 42.1% = 55,199 / 131,028; X 57.2%; map-panel and LOMA counts add up (1,200+289+127+106 = 1,722); Citizens rule is the quoted rule; "Community discount up to 30% (Boynton Beach)" is labelled with the community.

## flood-zone-map/
Verdict: PASS
- MINOR "If no zone shows, or a zone line crosses your lot" | The card's first half says what FEMA's data covers and points to the Map Service Center, but never states plainly what a reader with no zone result should do or conclude (no zone shown is not "no risk"). The quoted rule (over 90 percent of U.S. population; other FEMA products may cover the rest) is not wrong. | One plain sentence: "No zone shown means FEMA's digital map has nothing for that point, not that the point is safe"; only if backed by a rule line.
- MINOR "this is what its rules compare" | Reads as clipped before the long quoted rule. | "FEMA's rules compare ..."
- Checked: lede answers the query in the first 40 words; the new card's LOMA link names its target ("review your property's zone" to /guides/loma-lomr/) and the page does list LOMA text; the quoted 44 CFR 70.5/70.9 rule text is unchanged from the registry; "FEMA's map, not an official determination" present; JS-off shows the FEMA button and all cards.

## flood-zones/ao
Verdict: PASS
- MINOR "Zone AO ... Median / yr $899" in the table above vs "$894" full-risk median | Explained directly under the stats ("premium alone, before fees, so it does not compare dollar for dollar"). Fine; logged only because a reporter could lift the two figures side by side.
- MINOR Page has no "most insured units are not in this median" note like VE has | AO lists 26,959 single-family policies in the median and county table counts "policy units rated AO" of every type; labels are right in each place, but the AO page never says the unit total is larger. | Optional parity with VE.
- Checked: opens with the 44 CFR 59.1/64.3 definition in the first 40 words; 26% over 30 years is the registry line; 126,615,766 / 2,371 = $53,402; table high-risk column "Yes" for AO is consistent with the A-or-V purchase rule; county table "too few priced" defined under it.

## flood-zones/ah
Verdict: PASS
- MINOR "86% of them are in Florida" | Correct (91,505 / 106,626 = 85.8%); it counts single-family primary-home policies in the median, and the sentence sits right after that base. Fine.
- Checked: opens with the definition; $364,431,772 / 5,141 = $70,887; state table cut at 51 policies, "18 more states ... under 50 priced" says so; bfe_floor rule scoped to "zones AE and AH" as quoted.

## flood-zones/ve
Verdict: PASS
- MINOR "The regulation's coastal high hazard area runs from offshore to the inland limit of a primary frontal dune along an open coast, plus other land subject to high velocity wave action ..." | Long and heavy for a phone reader in the first 40 words; the first clause ("coastal high hazard area ... 1 percent or greater chance of flooding in any given year") answers the question. Rule text stays verbatim by owner order. | None.
- Checked: $1,156,277,086 / 11,914 = $97,052; the "148,141 units rated VE vs 18,181 in the median" note is present and its base is named; TWIA rule scoped to Texas windstorm policies and sourced (twia.org listed).

## new-jersey
Verdict: PASS
- MINOR "New Jersey's environmental agency (NJDEP) offers New Jersey's Flood Indicator Tool" | Sits in "Am I required to buy it?" although the tool is a screening tool, not an answer to "required". Link anchor is descriptive and the sentence keeps NJDEP's own limits ("does not calculate actual risk ... absence of indicators does not mean a property is free from flood risk"), so no promise beyond the target. | Optional move to the zone-lookup area.
- MINOR "Zone A08 (high-risk)" and "Zone A07 (high-risk)" rows have no link, unlike AE/X | Explained by the note below ("A1 to A30 and AE are the same kind of area"). Fine.
- Checked: 85.0% = 166,318 / 195,686; shares add to 100.1 by rounding (not shown as a total); hero shows median $1,231 on screen 1; "6 communities" list agrees.

## pinellas-county-fl
Verdict: PASS
- MINOR "the county also maps County Flood Hazard Areas ... which it treats as high-risk" followed two sentences later by "81.0% of Pinellas County's NFIP policy units are in high-risk zones" | Two meanings of "high-risk" in one card (county's own areas vs FEMA zones A/V). The share sentence is about FEMA zones by the zone table under it, and the new sentence "That is a share of insured policy units, not of all buildings" is correct and helps. A hurried reader could still blur the two. | Optional: "FEMA high-risk zones (A or V)" in the share sentence.
- Checked: 81.0% = 106,713 / 131,666; zone shares add to 100.0; "Pinellas County Flood Map Service" link names the county's own service and the sentence says the county points residents there, which the rule text supports; LOMA split adds to 2,032; Citizens rule is the registered quote.

## flood-insurance/renters
Verdict: PASS
- MINOR Lede "Renters with a National Flood Insurance Program (NFIP) policy on their belongings paid a median of $369 a year ..." then the new "Does my renters insurance cover floods?" line | The new answer line is second paragraph, about word 50. The page's own query (cost for renters) is answered in the lede; the coverage question is answered just below. Not blocked. | Optional: swap order if search data shows the coverage question leads.
- MINOR "Whether you are required to buy it is not in FEMA's data: only your lease or landlord can say." | Reasonable, but stated flatly with no source line; a renter whose lender or condo rules apply is not covered by "lease or landlord". | "usually your lease or landlord".
- Checked: "FEMA's FloodSmart site says most homeowners and renters insurance does not cover flood damage" matches the rule; $100,000 contents limit is the rule text; state table is "at least 30 priced policies, most first" and is in descending order (Hawaii's 49 sits above Massachusetts 42, correct); the Texas landlord notice rule is scoped to Texas.

## guides/100-year-floodplain
Verdict: PASS
- MINOR "62.9% of the 4,529,364 NFIP policy units ... are rated in zones A or V, the zones FEMA's map uses for that area." | The list that follows names A99, AR, VO and others; the page counts every code starting with A or V (matches the site's zone_labels rule), but the lede says only "zones A or V". The next card gives the full code list. | "zones starting with A or V".
- MINOR Title is 112 characters ("... the share of NFIP policy units rated in those zones, by state") | Will truncate in results; not a reader-misleading issue.
- MINOR The stat "62.9%" is a share of insured units, not of buildings in the floodplain | Labelled correctly in the stat label, the grey caption and the closing "cannot tell you" ("Buildings without NFIP flood insurance are not in these counts"). No change needed; logged because a reporter could quote the number alone.
- Checked: opens with the 44 CFR 59.1 definition (special flood hazard area, base flood, 100-year flood) in the first 40 words; 26% / 29% lines are registry rules; table has 51 rows (50 states + DC), sorted by units, range line (24.9% DC to 85.0% NJ) matches; link "flood zone map" goes to a page that does show FEMA's map at an address; the page says the map is "not an official determination".

## guides/flood-insurance-contents-coverage
Verdict: PASS
- MINOR "The policy generally counts a flood only when water covers two or more acres ..." sits under "What flood insurance does not cover" next to the not-covered sentence | It is the policy's definition of a flood, not a list of what is excluded; the card heading slightly overpromises for its first sentence. | Own short heading, or "What counts as a flood, and what is not paid".
- MINOR "77% ... building coverage of $250,000 or more" beside "81% ... some contents coverage" | Both labelled "of all 2,320,412 ... single-family primary-home policies"; the 77% figure counts coverage at the home maximum, and the caption says so ("the most a home can buy"). Fine.
- Checked: lede answers "what does it cover" in two parts in the first 40 words; building-coverage and contents lists are quoted from FloodSmart; basement text is the Dwelling Form quote with its 1974 condition; "$2,500" valuables limit is within the quoted sentence; state table has 51 rows, sorted by policy count, 43.8% (WV) to 95.3% (DC) matches the lead; "Condo units, second homes and other building types are not in these shares" is on the page.

## Classes
- No class-wide defect found this round. One class to watch: "high-risk" now has two meanings on county pages that carry a county-own flood map sentence (Pinellas); the share sentence should name FEMA's A or V zones.
- Not re-raised: county papers card lacking "if claims were independent"; rule() quote text staying verbatim.
