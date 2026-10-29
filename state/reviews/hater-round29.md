# Hater review round 29: "Local sea level" note (in-county gauges only)

Checked: dist/flood-insurance/<slug>/index.html against data/us/sealevel.json under each county's geoid (from data/c/<slug>/agg.json). Read-only; no other file touched.

## palm-beach-county-fl

- Geoid 12099 lists one gauge: Lake Worth Pier (station 8722670), trend 1.62, error 0.10, 1970 to 2025. Page: "NOAA's tide gauge at Lake Worth Pier measured a sea-level trend of +1.62 inches per decade (give or take 0.10 inches per decade) from 1970 to 2025." Matches.
- Sentence is clear and plain. No BLOCKER, no MAJOR, no MINOR.

Verdict: PASS

## broward-county-fl

- Geoid 12011 has no entry in sealevel.json. The page contains no "Local sea level" text at all. Matches requirement (b).
- No BLOCKER, no MAJOR, no MINOR.

Verdict: PASS

## miami-dade-county-fl

- Geoid 12086 lists one gauge: Virginia Key (station 8723214), trend 1.26, error 0.04, 1931 to 2025. Page: "NOAA's tide gauge at Virginia Key measured a sea-level trend of +1.26 inches per decade (give or take 0.04 inches per decade) from 1931 to 2025." Matches.
- Sentence is clear. No BLOCKER, no MAJOR, no MINOR.

Verdict: PASS

## galveston-county-tx

- Geoid 48167 lists three gauges. Page shows all three with matching trend, error and years:
  - Eagle Point (8771013): 4.80, error 0.27, 1993 to 2025. Matches.
  - Galveston Bay Entrance (8771341): 2.59, error 0.10, 1957 to 2025. Matches.
  - Galveston Pier 21 (8771450): 2.61, error 0.04, 1904 to 2025. Matches.
- MINOR: "Local sea level:" is one run-on sentence joining three gauges with semicolons (about 90 words before the "A plus sign" line). It is correct but hard to scan on a phone. Consider one line per gauge.
- Not checked: whether each station sits geographically inside Galveston County. The request was to confirm listing under the county's own geoid, which holds.

Verdict: PASS
