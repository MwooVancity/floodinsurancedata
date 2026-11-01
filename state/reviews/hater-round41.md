# Hater round 41

Scope: zone pages /flood-zones/ae, /x, /ve (hero labels, X table header, "Does zone X flood?" text), plus "What each means" sentence and home link on the four county/state pages. Grep-only check; no page edited.

## home
Verdict: PASS
- **MINOR** dist/index.html links to /flood-zones/ae/ (line 40): confirmed.

## louisiana
Verdict: PASS
- **MINOR** "What each means: zone AE, zone X, zone VE" is present (line 129), but it is three links with no explanation of each zone. Same on all four pages.

## palm-beach-county-fl
Verdict: PASS
- Zone pages: AE and VE hero labels now say "all A zones (AE, A, AH, AO and others); zone AE alone is in the state table" and "all V zones (VE, V and others); zone VE alone is in the state table". A reader can tell the figure is not one zone. Clear.
- **MINOR** zone X page (dist/flood-zones/x/index.html line 39): the table column "Share of state's paid claim dollars outside zones A and V" sits beside "Median / yr, zone X". The text under "Does zone X flood?" (line 41) says "not zone X alone", so the mislabel is fixed below the table, but the header itself should say "all zones except A and V". Not a wrong action, so MINOR.
- **MINOR** "What each means" sentence is present (line 129) but lists links only.

## broward-county-fl
Verdict: PASS
- **MINOR** "What each means" sentence is present (line 129), links only, no explanation.

## new-york-county-ny
Verdict: PASS
- **MINOR** "What each means" sentence is present (line 129), links only, no explanation.
