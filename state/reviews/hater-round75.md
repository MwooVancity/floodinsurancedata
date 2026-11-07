# Hater round 75 (LIGHT: dist HTML text only, no screenshots, no SEO search)
Scope: the "Flood map:" note (LOMA sentence), the zone-X-only line in the lookup tool, /flood-zone-map/ links. Checklist lines A-N not re-run on unchanged text (no GAP list this round).
Recompute (from data/us/map_status.json, raw outcome strings, regrouped by me): palm 1046/129/25/140/149/denied 127 (5+5+3+114)/other 106 (72+33+1) = 1,722 OK; wake 203/33/114/31/18/denied 46 (1+3+4+2+36)/other 53 (19+33+1) = 498 OK; dallas 482/52/21/73/25 (24+1)/denied 53 (1+7+3+3+39)/other 25 (1+16+8) = 731 OK; santa-rosa (extra) 157/14/7/8/4/27/11 = 228 OK. Every printed number equals the raw sum; groups sum to the lead total.

## home
- **MINOR**: lookup link now present ("or with the flood zone lookup", href /flood-zone-map/). No other change in scope.
Verdict: PASS

## louisiana
- State page has no "Flood map:" note and no lookup link (0 matches). Nothing changed in scope.
Verdict: PASS

## palm-beach-county-fl
- **MINOR**: "FEMA's map service lists 1,722 rulings" gives no period (all years the service holds). Round 74 asked for it; the "owners who applied, not a share of all homes" line removes the misleading base, so not a MAJOR.
- **MINOR**: "denied, 127" next to "building taken out ... 1,046" can still be read as a 93% win rate; "not a share of all homes" does not say "not a success rate".
- **MINOR**: "other or mixed, 106" silently holds FEMA's "None" (33), "Multiple" (72), "UNKNOWN" (1); no definition on the page.
Verdict: PASS

## new-york-county-ny
- No map-service data for 36061 (panels 0), so no "Flood map:" note and no lookup link (0 matches). Correct: nothing is printed that the data lacks.
Verdict: PASS

## wake-county-nc
- **MINOR**: same period and success-rate and "other or mixed" notes as palm-beach.
Verdict: PASS

## dallas-county-tx
- **MINOR**: same as palm-beach. "other or mixed, 25" holds "Dropped or Withdrawn" (1), "Multiple" (16), "UNKNOWN" (8); a withdrawn request is not "mixed".
Verdict: PASS

## south-dakota
- State page, nothing changed in scope.
Verdict: PASS

## Classes
- County: LOMA outcome sentence. Remaining MINORs: no period, no "not a success rate", "other or mixed" undefined. Could be one line on /methodology/.
- Tool/zone pages: zonemap.js prints "does not mark this spot as a Special Flood Hazard Area" only when SFHA_TF is F, one zone feature, and FLD_ZONE = X (tools/static/zonemap.js line 41). /flood-zone-map/ linked from home and all 7 zone pages (a, ae, ah, ao, d, ve, x) and the county notes.

## Previous items (round 74)
- MAJOR 1 (palm, wake, dallas) "already outside the zone as mapped" lumped building-out with property-out: FIXED. Page now prints "the building already outside the zone as mapped (part of the lot inside), 140 ; the property or part of it already outside as mapped, 149" (palm); wake 31 / 18; dallas 73 / 25. Counts match raw strings.
- MAJOR 2 (palm, wake, dallas) "removed the building or all or part of the property": FIXED. Page now says "asked FEMA to take a building or lot out of the high-risk zone", splits 1,046 / 129 / 25, and adds "These are rulings for owners who applied, not a share of all homes." Period and "success rate" wording not added (MINOR above).
Tally: 2 of 2 FIXED.
