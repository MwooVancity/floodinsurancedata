# Hater round 28 (light check: Flood map note, Local sea level note, methodology count)

## home
Checked: no NaN / undefined / None / [object in extracted text. Nothing else graded.
Methodology side check (no own section): "Eight federal datasets" matches the list if Policies and Claims count as two (Policies, Claims, Community Status Book, Disaster Declarations, Housing Assistance, NOAA Sea Level Trends, National Risk Index, Multiple-Loss Flood Properties = 8). The PIF workbook is correctly called a reference.
- MINOR (methodology): the list shows 7 bullet entries plus the workbook, because Policies and Claims share one bullet; a reader counting bullets gets 7. The sentence "the full-risk premium is a field within Policies..." is hard to parse.
- MAJOR (methodology, see broward): it says "county pages show a gauge in the county or a bordering one, never a far-away gauge", but Broward shows Naples, a Gulf-coast gauge on the other side of the state.
Verdict: PASS

## louisiana
data.json crs: 353 communities, zero with "(>)" (dates are plain, (M) 57, (L) 6, (NSFHA) 13, None 4). The page has no "Flood map:" note, which is correct: nothing new is coming, and no "0 communities" line is shown.
- MINOR: (M), (L) and (NSFHA) communities get no note; acceptable, not asked for.
Verdict: PASS

## palm-beach-county-fl
Flood map: "FEMA's current flood map for unincorporated Palm Beach County took effect December 20, 2024." data.json: PALM BEACH COUNTY 12/20/24, matches. No community has "(>)", so no new-map clause; correct.
Local sea level: "Lake Worth Pier ... +1.62 inches per decade (give or take 0.10) from 1970 to 2025". sealevel.json 12099: 1.62, 0.10, 05/1970 to 12/2025, matches. Gauge is in the county, so no "bordering" label is needed.
- MINOR: "give or take 0.10" has no unit (inches per decade).
- MINOR: the note does not say the trend also includes land sinking or rising at that gauge. "The water there got higher" is fair for a plain reader.
Verdict: PASS

## broward-county-fl
Flood map: "unincorporated Broward County took effect July 31, 2024". data.json: BROWARD COUNTY 07/31/24, matches. No "(>)" communities.
Local sea level values match sealevel.json: Naples 1.32 +/-0.08 (1965-2023, geoid 12021 Collier), Virginia Key 1.26 +/-0.04 (1931-2025, Miami-Dade), Lake Worth Pier 1.62 +/-0.10 (1970-2025, Palm Beach). All three counties border Broward per county_adjacency.json.
- MAJOR: the label "(in a bordering county; there is no NOAA tide gauge in Broward County)" sits only after the third gauge, so it reads as applying to Lake Worth Pier only. Naples and Virginia Key show no label. It also never names the county.
- MAJOR: Naples is in Collier County on the Gulf coast, on the opposite side of Florida from an Atlantic-coast Broward homeowner. Listing it first with no label makes it look local. This also contradicts the methodology line "never a far-away gauge".
- MINOR: "give or take 0.08" has no unit.
Verdict: FAIL

## miami-dade-county-fl
Flood map: "New FEMA flood maps take effect February 19, 2027 for Cutler Bay, Miami-Dade County, Coral Gables, Miami Beach, Palmetto Bay, Aventura, Miami, Miami Shores Village and 25 more." data.json: 33 of 35 communities are "(>)", all dated 02/19/27. 8 named plus 25 more is 33, matches. The date is in the future relative to today (2026-10-29) and the wording is a plain statement, with no promise about rates or zones.
- MINOR: it does not say the current map still applies until that date. A frightened reader could think the new maps already apply.
- MINOR: it does not say that the two remaining communities are not covered.
Local sea level: Virginia Key +1.26 (give or take 0.04) 1931-2025, matches sealevel.json 12086. Gauge is in the county, so no label is needed.
- MINOR: the "give or take" figure has no unit.
Verdict: PASS

## galveston-county-tx
Flood map: "unincorporated Galveston County took effect August 15, 2019". data.json: GALVESTON COUNTY 08/15/19, matches. No "(>)" communities.
Local sea level: Eagle Point +4.80 (0.27) 1993-2025; Galveston Bay Entrance +2.59 (0.10) 1957-2025; Galveston Pier 21 +2.61 (0.04) 1904-2025. All match sealevel.json 48167, and all three are in the county.
- MINOR: Eagle Point's +4.80 is almost double the other two and is shown without comment. It has the shortest record (32 years), shown only as a date range. A reader may be alarmed. The "one spot on the coast" disclaimer covers it only partly.
- MINOR: "give or take 0.27" has no unit.
Verdict: PASS
