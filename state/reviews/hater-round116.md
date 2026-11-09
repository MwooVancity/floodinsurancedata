# Hater round 116 (very light, text only, "Find your ZIP" card)

Method: one `python -I` script per page stripping tags; X and Y checked against the page's own "In-force count" (2,368 / 131,028) and the ZIP table; rule behind "mostly outside any town" read in `tools/fetch_zip_places.py` (a ZIP gets a town only if one Census place covers at least 25% of its land).

## sonoma-county-ca
- **MINOR** "ZIPs that lie mostly outside any town hold 1,804 of the 2,368 policy units here, so they are not in that ranking." Y equals the page's in-force units (2,368), so X and Y are consistent and the missing 95446 (611) is now explained. But the rule is land area: a ZIP with no place on at least a quarter of its land has no town. So 95448 (Healdsburg area, 122 units), 94952 (Petaluma area, 171) and 95476 (Sonoma area, 161) are "outside any town" only by land. A local reader who knows those towns may read the sentence as wrong. Suggest "mostly outside any town by land area". Reader hurt: slight doubt, no wrong number.
- **MINOR** Title "(Monte Rio)": the town line says it is the top-ranked town, but Monte Rio's ZIP holds 222 of 2,368 units (9%), and the sentence says 76% of units are in no ranked town. The title does not claim largest, so it is not wrong; it does lead a reader to think Monte Rio is the county's centre. Not misleading enough for MAJOR.
- Card otherwise unchanged and fine: price range line (94931 $1,139 to 95462 Monte Rio $1,757), "All 37 ZIPs ... in the lookup", ZIP table, caveats. Town ranking order is plausible (Monte Rio 222, Windsor 83 visible in the table).
Verdict: PASS

## palm-beach-county-fl
- **MINOR** Same land-area wording as Sonoma: 35,565 of 131,028 units (27%) sit in ZIPs with no town, including four of the eight listed ZIPs (33437, 33446, 33428, 33467). X and Y match the page's in-force units (131,028). Sentence is true by land (these are largely unincorporated Boca/Delray-area ZIPs) and the title town (Boca Raton) is top-ranked, so no misleading effect.
- Nothing else in the card changed for the worse.
Verdict: PASS

## dixie-county-fl
- No town line (fewer than two towns), so no new sentence appears. Card intact: price range (32628 $654 to 32680 $1,011), "All 10 ZIPs ... in the lookup", two-row ZIP table. Title has no town, consistent with no town line.
- **MINOR** The table lists 2 of 10 ZIPs and the caption says it shows ZIPs with the largest number of priced policies; this is disclosed, no change.
Verdict: PASS

## Classes
- County template: "outside any town" is land-area based but not labelled as such; counties with big unincorporated or rural ZIPs (Sonoma, Palm Beach) show a large unranked share. Wording fix once in `_town_line`, not per page.
- Title town is the top-ranked town by ZIP units, not necessarily the county's best-known town; fine while the town line sits on the page.

Tally: sonoma 0 BLOCKER / 0 MAJOR / 2 MINOR; palm-beach 0/0/1; dixie 0/0/1. Previous round's Sonoma FAIL item is resolved.
