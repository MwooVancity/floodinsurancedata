# Round 74 (LIGHT: page text only from dist HTML, no screenshots, no Google search). Scope: the "Flood map:" note (FIRM panels, LOMR, LOMA), the address tool (palm-beach-county-fl, louisiana, new /flood-zone-map/ page judged inside `home`), methodology "Nine". Checklist lines A-N not re-run on unchanged text (round 73 passed).

Own list built first, from `map_status.json`, `tools/static/zonemap.js`, `rules_registry.py` and the built HTML. Round 73 read after.

Recomputed from raw (palm 12099): 1,722 LOMA = removed 25+129+1,046 = 1,200; denied 5+5+3+114 = 127; out as shown 149+140 = 289; other (Multiple 72, None 33, UNKNOWN 1) = 106. Sums match the page. Wake 498 = 350/46/49/53 matches. Dallas 731 = 555/53/98/25 matches. LOMR 45 / 42 since 2021, panels 215, dates 2017-10-05 and 2024-12-20 match. The arithmetic is right; the wording of the "out as shown" group is the problem.

## home
(Judged: /flood-zone-map/ page, dist/methodology, tool markup on state and county pages.)
- **MAJOR** (shared sentence, every county page with a LOMA count): "found the property already outside the zone as mapped in 289". 140 of Palm Beach's 289 (48%) are FEMA's outcome "Structure out as shown-Property partially inundated": the building is outside the zone but part of the lot is still in it. Wake: 31 of 49; Dallas: 73 of 98, plus 1 "Portion of property out as shown". "Property already outside" is wrong for those, and a reader with a house that is out but a lot that is in will think the whole lot is out. The "removed" group has the same shape (1,046 of 1,200 are "Structure removed-Property partially inundated") but "the building or all or part of the property" covers it. Fix: name the group "found the building outside the zone as mapped (the lot may be partly inside)", or split structure from property.
- **MAJOR** (same note): "FEMA removed the building or all or part of the property in 1,200". "Removed the building" reads as demolished. It means removed from the high-risk zone. The lead sentence says "take ... out of the high-risk zone" but the outcome sentence drops "from the zone". With "denied 127" next to it, a reader also computes a 70% success rate; the page gives no period for the 1,722 (all years the map service holds) and says nothing about who applies (owners who think they are out), so it is not a chance of winning. Add the period and "owners who applied", or "not a success rate".
- **MINOR** (tool result sentence, zonemap.js): "FEMA does not mark this spot as a Special Flood Hazard Area." is also printed for Zone D (possible but undetermined) and for "Zone OPEN WATER" or "Zone AREA NOT INCLUDED" (zoneName prints any FLD_ZONE string after "Zone "). For D it reads as comfort. The mandatory label follows, and the D link explains, so not blocking. Skip the SFHA line for D and non-letter zones.
- **MINOR** (/flood-zone-map/ zone codes): "B and X are areas of moderate flood hazard, C and X areas of minimal hazard". X appears twice with no explanation of shaded vs unshaded. The tool prints the subtype ("0.2 pct annual chance" or "area of minimal flood hazard"), and links to the zone X page, which explains it. Add "(shaded)" and "(unshaded)".
- **MINOR** (tool, map step): the FEMA zone colours are drawn at 0.6 opacity on the map before the pin is confirmed, with no legend. No zone is NAMED before confirm (checked: `ask()` shows only "Is the pin on your building?"; `confirm()` is the only caller of describe()), so the rule holds, but colour is the only signal on the map. Add one line "Shaded colours are FEMA's flood zones; the zone for your pin appears after you confirm."
- **MINOR** (methodology, "What the data cannot tell you"): "Your address's exact flood zone: use FEMA's Flood Map Service Center." now sits beside a tool that shows a zone at an address. Still true (not a determination) but reads as a contradiction. Add "the address tool relays FEMA's map; it is not a determination".
- **MINOR** (methodology): the NFHL entry says the LOMA/LOMR counts are "counted monthly" but gives no definition of the four LOMA groups or the period. One line would settle both MAJORs above.
- **GAP** (home): dist/index.html has no link to /flood-zone-map/ (0 occurrences). The standalone page is reachable only from other pages if linked there; the home reader cannot find the tool.
- **GAP** (tool placement): on the palm-beach page the address box sits between the stat row and "Am I required to buy it?", pushing the quick answers down by a box. Owner rule says screen 1 holds answers and links.
- **GAP**: Census geocoder is called by injecting a JSONP script; a public-agency source, but the address typed is sent to a third party. The disclosure line is shown ("Your address goes to the Census Bureau's address finder and the map point to FEMA's map service, not to this site.") and is accurate, but it is inside the hidden panel and appears only after the reader taps open. Fine; noted.
- Checked and fine: fema_asis wording matches the catalog record ("provides this data 'as is' ... no express or implied guarantees of accuracy"); label "FEMA's map, not an official determination" printed in the static markup and again in every result; "none" result says "not a finding of no flood risk"; "down" and "none" give only the FEMA link; geocode and location messages make no claim about risk and say the pin is an estimate; near-line case names every zone within 15 m (about 50 feet, correct: 15 m = 49 ft); panel line says "in effect since" the EFF_DATE; no-JS shows only the FEMA link (the panel is `hidden`); methodology "Nine" equals nine listed sources (Policies, Claims, NRI, Disaster Declarations, Housing Assistance Owners, Community Status Book, IA Multiple-Loss, NOAA Sea Level, NFHL).
Verdict: PASS

## louisiana
- Tool box and label present and identical to the other pages; no zone named before confirm; "Federal law requires it in a high-risk zone with a federally regulated or backed mortgage ..." unchanged.
- **GAP**: no "Flood map:" note on the state page (no FIRM/LOMR/LOMA line, and no new-map line). Nothing wrong is printed; the brief expected a state note, none exists. If a state roll-up is intended it is missing; if not, fine.
- **MINOR**: same as home: tool box above "Am I required" pushes the quick answers down.
Verdict: PASS

## palm-beach-county-fl
- **MAJOR**: "found the property already outside the zone as mapped in 289" (140 of 289 are "Structure out as shown-Property partially inundated"). See home, first item.
- **MAJOR**: "FEMA removed the building or all or part of the property in 1,200" (1,046 of them are "Structure removed-Property partially inundated"; "removed the building" reads as demolished; no period; invites a success-rate reading). See home, second item.
- **MINOR**: "FEMA's current flood map for unincorporated Palm Beach County took effect December 20, 2024" followed at once by panels "the oldest in effect since October 5, 2017". Both are true (panels are updated one at a time) but a reader sees 2024 and 2017 for "the current map". Say "panels are updated one at a time".
- Checked: 215 panels, 45 LOMR, 42 since 2021-01-01, newest panel date equals the county map date; Source line for FEMA NFHL present with retrieval date.
Verdict: FAIL

## new-york-county-ny
- No "Flood map:" note (panels = 0 in `map_status.json`, which the builder treats as no data and prints nothing). Correct fail-closed: no zero is shown as a fact. **GAP**: no gap line saying "FEMA's map service returned no panel data for this county"; 26 counties are in this state.
- Address tool not on this page (not in scope).
Verdict: PASS

## wake-county-nc
- **MAJOR**: same "already outside the zone as mapped in 49" (31 of 49 are structure-out, property partly in). Same "removed the building or all or part of the property in 350" (203 of 350 "Structure removed-Property partially inundated").
- Checked: 268 panels, 17 LOMR / 17 since 2021 (reads naturally as "17 of them", fine), 498 = 350+46+49+53.
Verdict: FAIL

## dallas-county-tx
- **MAJOR**: same "already outside the zone as mapped in 98" (73 "Structure out as shown-Property partially inundated" + 1 "Portion of property out as shown": 74 of 98 are not whole-property). Same "removed the building or all or part" wording.
- **MINOR**: "current flood map ... took effect March 21, 2019" with "oldest in effect since August 23, 2001" (same issue as Palm Beach).
- Checked: 103 panels, 160 LOMR / 70 since 2021, 731 = 555+53+98+25; "Not in the NFIP (1 community here): Combine" fine.
Verdict: FAIL

## Classes
- County (any county with a LOMA count, hence palm, wake, dallas and all queued counties): the LOMA outcome sentence. Two MAJORs from one template line in `_nfhl_lines()` (`tools/build_page.py`); fix once. Grouping code is right; labels over-claim for the "Structure ... Property partially inundated" outcomes (about half of every group). Add a mutation test: a county whose "out as shown" group is all "Structure out as shown-Property partially inundated" must not print "property already outside".
- County: "current map took effect X" next to an older "oldest panel" date (MINOR, all counties with panels).
- State: no "Flood map:" note on Louisiana (GAP, check all 51).
- Tool (state, county, home, /flood-zone-map/): sentence set is safe (label always shown, nothing named before confirm, FEMA link on every failure); only the D / open-water SFHA line and the map-colour legend are MINOR.

## Previous items (round 73)
- Round 73 MAJOR 1 (zone X state column bases): FIXED (not touched this round, no change in scope).
- Round 73 MAJOR 2 (claims card heading over all-building mean): FIXED (not re-read).
- Round 73 MINORs ("existing" in the compare-table footnote; zone D "No" cell; "outside zones A and V" column head): not in scope this round, not re-read; treated as still open.
Tally: 2 FIXED, 0 NOT FIXED, 0 PARTLY; 3 MINORs carried unchecked.
