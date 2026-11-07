# Round 87 (LIGHT, text only)

Scope: the new "Towns here" line in the ZIP card and the meta-description "Includes ..." sentence. Recomputed from data/all-counties/*.json by_zip, data/us/zip_places.json, data/us/zip_place_counties.json (place and ZIP both in the county, units summed per town).

## palm-beach-county-fl
Recomputed top 5: Boca Raton 20,643; Palm Beach 9,293; West Palm Beach 9,168; Delray Beach 8,372; Boynton Beach 8,237 (next: Jupiter 7,258). Page line and meta list exactly these, same order. All five are real towns; none is a non-place. "Palm Beach" is one ZIP (33480) and matches the ZIP line above it.
- **MINOR** "ranked by NFIP policy units in their ZIPs" is honest about the base (units, not homes; town = its ZIPs) but "policy units" is unexplained at that spot and the line gives no counts, so a reader cannot see the gap sizes. Not misleading.
- **MINOR** Meta description is now ~330 characters; Google will cut it before "Includes ...", so the town sentence may never show.
Verdict: PASS

## new-york-county-ny
Recomputed: every NFIP ZIP in the county maps to one place, "New York" (14,911 units), so only 1 town; the rule drops the line under 2 towns. Page has no town line and the meta has no "Includes" sentence. Correct.
- No defects.
Verdict: PASS

## Classes
- county: the town line appears only where 2+ towns qualify; two ordinary cases checked. No wrong town found. A county where one ZIP is split across places (below 25% land share) simply loses that ZIP's units; this under-counts but never invents a town.
