# Fresh audit 2026-11-08: zone map soundness, path to #1, backlinks
📄 Planning doc only — doesn't change the site.
Auditor: fresh agent, read-only on code. Evidence: V = VERIFIED (read the file, live page or run log in this audit); I = INFERRED (reasoning or memory, not read).

Read: CLAUDE.md, PLAN.md, `tools/static/zonemap.js`, `tools/zonemap_block.py`, `tools/test_zonemap.py`, `tools/live_zonemap.py`, `tools/tools_flags.json`, `.github/workflows/fema-probe.yml`, `watch.yml` (grep), fema-probe run 42434461010 log (11-08), `kwp_rank.py` output, live home / hub / palm-beach / zone AE / claims pages, `data/us/map_status.json`. 10 WebSearches, 3 competitor page reads.

---------------------------------------------------------------------------------------------------

## PART 1: address tool infrastructure (before "all" on 11-20)

### What it does today (V)
- Loader (`zonemap_block.py` LOADER): nothing loads before the tap; tap loads `/vendor/leaflet.css`, `/vendor/leaflet.js` (147 KB raw, self-hosted), `/zonemap.js` (9.4 KB). Load failure prints "The map did not load" + FEMA link. JS off: plain link to msc.fema.gov.
- Geocode (`zonemap.js:57-70`): Census `onelineaddress`, benchmark `Public_AR_Current`, JSONP (Census sends no CORS header), first match only (`addressMatches[0]`), 8 s timeout.
- Pin: reader must press "Yes, the pin is on my building" before any zone is named (`zonemap.js:94-98`, tested in the click path).
- FEMA (`zonemap.js:99-112`): three parallel queries to `hazards.fema.gov/.../NFHL/MapServer`: layer 28 at the point (FLD_ZONE, ZONE_SUBTY, SFHA_TF); layer 28 with an envelope of +-15 m (Web Mercator, scaled by 1/cos(lat)); layer 3 at the point (FIRM_PAN, EFF_DATE). 8 s timeout via AbortController.
- Map overlay: FEMA's own `/export` image tiles of layer 28 over the USGS topo basemap (`zonemap.js:80-86`).
- Output strings are escaped (`esc`, `zonemap.js:15`, `:116-118`); Census's matched address is escaped (`:124`).
- Live gate 11-08 (run 42434461010, V): PASS in Chromium and WebKit on 5 real addresses (zones X, AE, X, X, AE). FEMA layers 3 (FIRM Panels), 1 (LOMRs), 34 (LOMAs, with LAT/LON, OUTCOME, CASENUMBER), 0 (NFHL Availability) all answer from the US runner.

### Failure walk (each input from the brief)
| Case | What happens today | Evidence |
|---|---|---|
| FEMA down / 5xx / CORS removed | `get` returns null -> "FEMA's map service did not answer. Check this spot on FEMA's map." + FEMA link. Safe. | V `zonemap.js:28,50-52` |
| FEMA slow > 8 s | Same "did not answer" message. Safe but loses readers if FEMA is often slow; 11-08 run answered within 8 s on 5/5. | V |
| FEMA returns empty features | "no flood zone at this pin ... does not cover every place". Honest for a true gap; misleading if FEMA's layer is empty for everyone (migration). | V `:30`, I |
| FEMA field rename | ArcGIS rejects unknown outFields with an error -> "did not answer". | I (ArcGIS behaviour, not tested) |
| FEMA layer renumbered | If 28 becomes a layer without FLD_ZONE: error -> safe. If the response is 200 with no FLD_ZONE values: "no flood zone at this pin" for every reader. Nothing checks `fields`. | V code, I behaviour |
| FLD_ZONE "OPEN WATER" / "AREA NOT INCLUDED" | Printed as "FEMA's map shows Zone OPEN WATER at this pin." The fuzz even feeds "OPEN WATER" and the oracle accepts it. | V `:21-24`, `test_zonemap.py:57` |
| ZONE_SUBTY raw codes | Printed lowercased: "Zone X (0.2 pct annual chance flood hazard)". Readable-ish, jargon "pct". | V `:24` |
| LOMA for one building (not in the zone polygons) | Tool says "FEMA marks this spot as a Special Flood Hazard Area" while FEMA's own layer 34 may hold a LOMA that removed that building. Not queried, no gap line. | V (layer 34 exists in probe log; not queried) |
| LOMR newer than panel / newer than layer | Only the panel's EFF_DATE is printed ("in effect since"). A LOMR at the point (layer 1) is not queried, so the date the reader sees can be older than the map revision that set the zone. | V |
| Preliminary / draft maps (e.g. Harris County MAAPnext 2026) | Not shown. Hub carries `rule("prelim")` text; county pages carry it in the map note. | V hub code; Harris drafts V via search |
| Census no match | "did not match that address. Check the spelling, or use your location". OK. | V `:123` |
| Census down / offline / Census returns HTML error | Same "did not match ... check the spelling" message: blames the reader's spelling for an outage. | V `:66-68`, I for HTML error path |
| Multiple Census matches | First silently taken; matched address shown; reader must confirm pin. Mitigated, not surfaced. | V `:62` |
| PO box | Census does not match -> no-match message. OK. | I |
| Wrong-state match | Matched address (with state) shown above the pin prompt; reader confirms. Mitigated. | V |
| Territories PR / GU / VI | Geolocation path works anywhere; Census `Public_AR_Current` coverage of GU/VI unknown; NFHL coverage of territories unknown; site has no territory pages. | I |
| Reader offline before tap | Loader fails -> "map did not load" + FEMA link. Good. | V |
| JS off | Plain FEMA link, tested. | V `test_zonemap.py:113-116` |
| Old Safari (no AbortController / fetch / Object.assign) | No AbortController: no timeout, can hang on "Asking FEMA's map...". No fetch: `get` throws inside `confirm`, the page stays on "Asking" forever. Tiny share. | V code, I share |
| Pin dragged while FEMA query is in flight | Drag -> `ask()` shows the confirm prompt; then the old promise resolves and overwrites it with the zone for the OLD point under the pin's NEW position. No request token. | V `:88,96-119` |
| Second address typed while first geocode in flight | Late first answer can move the map to the first address. | V `:120-126` |
| 15 m rule | Envelope half-width 15 m; corners reach 21.2 m. Sentence says "A zone line is within 15 meters" when the other zone may be 15-21 m away. Superset satisfies "name every zone within 15 m"; the sentence itself can be false. | V `:103-105` |
| Scale x100 | Every map view pulls ~6-12 FEMA `/export` server-rendered tiles + 3 queries; every pan/zoom more. 10,000 lookups/day = ~100k+ FEMA export calls. FEMA's limits unpublished; throttling would show as "did not answer" for everyone. Census single-line geocoder: no published limit. | V code, I limits |
| Privacy | Address goes only to Census (in Census's URL, disclosed), never in our URL, no storage, no form submit (no `<form>`, no `name`). Referrer-Policy strict-origin-when-cross-origin (V live header), so Census/FEMA see only the origin. GA4 (G-EXCYW0PJYG) loads on every page; GA4 does not read input values (I). The notice omits that USGS basemap tile requests reveal the area (~150 m). | V |
| Security | JSONP runs Census-served script on our origin; no CSP. Census compromise = XSS on our domain. | V headers, I risk |
| Kill switch | `tools_flags.json` "zonemap" list; needs a full build + `release.py --ship` to change. | V |
| Monitoring | `live_zonemap.py` runs only in `fema-probe.yml`, `on: workflow_dispatch` (hand-run). `watch.yml` (nightly) does not touch FEMA or the tool. After "all" on 11-20, a week of FEMA trouble is seen by nobody. | V |
| Page weight before tap | Block + loader under 1 KB inline; county page 28.0 KB gz (palm-beach, V), hub 5.1 KB gz (V). After tap ~45-50 KB gz (I). GA gtag.js (third-party, every page) is likely larger than the page itself (I). | V/I |
| CLS | Map div goes `display:none` -> 320 px block after the async geocode (> 500 ms after the tap, so CLS counts it). On county pages content below jumps 320 px. | V code, I CWV effect |

### Do the tests catch them? (V, `test_zonemap.py`, `live_zonemap.py`)
Caught: every `describe()` branch, 3,000 fuzz answers (no NaN/undefined), confirm-before-zone, matched address shown, label + FEMA link shown, JS off, live page vs real FEMA on 5 addresses in 2 browsers.
NOT caught:
1. The oracle is not independent: it mirrors the JS line by line (same box, same `Zone <raw code>` naming), so it shares every logic error (OPEN WATER, 21 m corners).
2. Fixtures ignore geometry: the route returns the box fixture whenever "Envelope" is in the URL, so the 15 m math is never checked.
3. Live test passes when FEMA is broken: if every query errors, Python and page both say "did not answer" and the test PASSES. It prints zones but never asserts one.
4. No test of: Census no-match, Census timeout/offline, multiple matches, FEMA timeout path in the browser, drag-then-confirm (re-query at the new point), stale-result race, "Use my location" (the context grants geolocation but never clicks it), loader failure (Leaflet 404), old-browser path.
5. `release.py` runs `test_zonemap.py` in Chromium only (default); WebKit only on hand-run.

### Defects ranked
| # | Sev | Defect | Concrete failure | Smallest fix | Ev |
|---|---|---|---|---|---|
| D1 | MAJOR | Stale FEMA result after pin drag | Reader confirms, sees "Asking", drags the pin 40 m onto the real house; 3 s later the page prints the zone for the first spot under the new pin. Wrong zone for the point the reader confirmed last. | A request counter in `start()`: `confirm` and `ask` bump it; `.then` drops results whose number is stale. Same for `geocode`. Test: fixture with 2 s delay, drag, assert prompt stays. | V |
| D2 | MAJOR | Unlabelled FEMA codes printed raw | Pin on a lake or outside a mapped community: "FEMA's map shows Zone OPEN WATER at this pin" / "Zone AREA NOT INCLUDED". A mislabel (CLAUDE truth rule 8: new FEMA code needs a data-dictionary label). | Allow-list zone codes with labels from FEMA's FIRM Database Technical Reference (read raw); anything else -> "FEMA's map shows '<code>' here; see FEMA's map". Oracle gets its own table, not the JS one. | V code, I values |
| D3 | MAJOR | LOMA/LOMR not shown; date misleads | Buyer's house was removed from AE by a LOMA in 2019; tool says "Special Flood Hazard Area (high-risk)" and the panel date from 2009. Reader pays for a policy the lender may waive with the letter. | Query layer 34 (LOMAs) within ~50 m and layer 1 (LOMRs) at the point (already probed, fields known). Print FEMA's case number, date and outcome exactly; always print one gap line: a letter for a single building is not drawn on the zone map. | V |
| D4 | MAJOR | Live gate passes when FEMA is broken, and nobody runs it | FEMA migrates the service 11-25; every reader gets "did not answer" or "no flood zone" for a week; no job looks. The one live test would also PASS. | (a) `live_zonemap.py`: fail unless 4 of 5 addresses return a zone and Miami Beach returns SFHA_TF T. (b) Add the `live-tool` job to `watch.yml` nightly (cost ~2 runner-min/night + Claude reading it at session start). | V |
| D5 | MAJOR | "Within 15 meters" sentence can be false | Other zone 18 m away diagonally: page says a zone line is within 15 m. Truth wording on the only per-address claim the site makes. | Replace the envelope with the point + `distance=15&units=esriSRUnit_Meter` (ArcGIS query buffer; probe on US runner first). Deletes the Mercator math too. | V code, I param support |
| D6 | MAJOR | No scale/throttle plan for FEMA export tiles | 11-20 "all" + a hurricane week: thousands of readers x 6-12 server-rendered FEMA tiles each; FEMA throttles; tool fails for everyone during the exact week it matters. | Measure first: tiles per lookup from one real run. If > 5: drop the overlay below zoom 16 or show it only after confirm. Pin + text answer is the product. | I |
| D7 | MINOR | Outage reported as reader's spelling | Census down: "did not match that address. Check the spelling". | Distinguish onerror/timeout ("The Census Bureau's address finder did not answer") from an empty match. | V |
| D8 | MINOR | Field-rename / empty-layer blind spot | FEMA returns 200 with features but no FLD_ZONE field -> "no flood zone" to everyone. | Treat a response whose `fields` lacks FLD_ZONE as "down". | I |
| D9 | MINOR | CLS 320 px jump on county pages | CWV "poor" CLS bucket for tool users after 11-20. | Reserve the map height when the UI opens (set the div's height at tap, not after geocode). | V/I |
| D10 | MINOR | Old browsers hang on "Asking" | No AbortController/fetch -> stuck forever. | Feature-check `fetch` in the loader; else show the FEMA link. | V |
| D11 | MINOR | Privacy notice incomplete | Notice names Census and FEMA, not USGS basemap tiles. | Add "and map tiles from USGS". | V |
| D12 | MINOR | JSONP = third-party script on our origin | Census compromise = XSS. | Accept (gov source) and note; a Worker proxy costs a cron/KV-free Worker but adds a second host to watch. | I |
| D13 | MINOR | Multiple Census matches hidden | "100 Main St Springfield" lands in the wrong state; mitigated by the shown matched address + confirm. | If >1 match, list up to 3 to pick. | V |
| D14 | MINOR | Kill switch needs a full release | Hurricane-week FEMA outage: removing the tool takes a full build and gates. | Acceptable: the tool already fails to the FEMA link. No change. | V |

No BLOCKER: every failure path ends at a FEMA link and no path invents a zone. D1-D5 should land before 11-20 "all"; D6 measured before 11-20.

---------------------------------------------------------------------------------------------------

## PART 2: how to be #1, per keyword group
KWP bands (V, `kwp_rank.py`): flood zone map 50k, fema flood map by address 50k, flood zone map by address 5k, flood zone by address 5k, what flood zone am i in 500; state maps NC/NY/NJ/LA/FL 5k each; zone x / x meaning / ae / ae meaning / ao / a 5k each; Pinellas + Harris county map 5k; how much is flood insurance 5k, cost 5k; flood insurance TX/FL/CA 5k; renters 5k; nfip 5k; town "flood insurance chicago" 5k.

### G1. flood zone map / fema flood map by address / flood zone by address / what flood zone am I in
- Top results (V search; Mappr page read): msc.fema.gov; Mappr (map visible on load, tap/GPS/address, zone + SFHA + **base flood elevation**, shaded zones, territories, from Esri Living Atlas copy of NFHL); county viewers (Cape Coral, Hernando, Palm Bay, Manatee, which Axios Tampa linked); programmatic clones (zipradar, hazard-data, landrecords, policyrisk).
- They give, we don't: map on screen with no extra tap; BFE; zones drawn instantly (Esri cache, fast).
- We give, they can't: FEMA's live answer with a named zone line within 15 m; panel + date; after the zone, what policies in that zone cost and what claims there paid (Mappr's "20% of claims outside high-risk zones" has no source; we can print the real figure).
- Our hub is 5.1 KB gz with the tool behind a tap (V): thin vs every top result.
- Additions (decision-changing, dataset):
  1. Hub: tool open on load (the tool is the page there). Dataset: none new.
  2. After the zone: "In <county>, policies rated <zone> cost a median $X" + "claims rated <zone> paid ..." from our own county/zone aggregates (NFIP Policies v3, Claims v3). Needs a point -> county lookup: Census geocoder `geographies` endpoint returns county FIPS (I).
  3. LOMA/LOMR near the pin (D3): NFHL layers 34 and 1.
  4. BFE and depth: STATIC_BFE / DEPTH are in FEMA's same layer-28 answer (I field names). **Owner decision**: the address-tool rule lists zone, panel, effective date only.
  5. "Is the map changing here?": FEMA preliminary data. Probe on US runner whether a preliminary map service answers a point query; if not, a printed gap line + link to FEMA's preliminary download (already in `rule("prelim")`).

### G2. flood zone map <state> (NC, NY, NJ, LA, FL)
- Top (V search): county/city GIS viewers (Miami-Dade, Martin, Venice), Florida DEM Forerunner (effective FIRM layer, warns evacuation "Zone A" is not flood Zone A), UF GeoPlan; spam pages.
- They give: the official state viewer. We give: per-county costs and claims; nobody gives map age.
- Additions:
  1. State's official viewer link (NC FRIS, FDEM Forerunner, NJ, NY, LA) via `rule()` after a raw read. Gap line where none.
  2. Map age by county (oldest/newest panel date) table: NFHL layer 3 (`map_status.json` has 225 counties, V; extend via `map-status.yml` to all counties in the state).
  3. Which counties have preliminary maps pending: FEMA preliminary data (probe) else gap line.
  4. "Evacuation zone is not a flood zone" line where the state uses lettered evac zones (FL): from FDEM text, raw read.

### G3. <county> flood zone map (Pinellas, Harris 5k; ~285 counties 10+/mo)
- Top (V search, Harris): FEMA MSC, Harris County Flood Control District MAAPnext (draft maps released 2026-02, meetings), local TV (click2houston, abc13), HAR.com flood tool.
- They give: the county's own viewer and draft-map news. We give: map panels/dates, LOMR count, LOMA outcomes by group (V `build_page.py:425-448`), cost, claims.
- Additions:
  1. Put the map-status lines (panels, newest date, LOMRs, LOMA outcomes) directly under the address tool for these queries, not lower.
  2. County's own flood viewer link: no national dataset -> a printed gap line, or a hand-read list for the top-50 kw counties in `state/manual-rule-read.json`.
  3. Draft/preliminary status (as G2.3).
  4. Policies by zone in the county (share of priced policies in A/V vs X): NFIP Policies v3, already aggregated (I).

### G4. zone meanings (x, ae, ao, a, ve, d)
- Top (V search): Amica, Neptune, county definition PDFs, hazard-data/landrecords clones, appraiser quiz pages (one says AE = "Annual Elevation", wrong).
- They give: definitions; private insurers push quotes. We give (V live AE page): 44 CFR definition, mandatory-purchase law, median $1,252 on 961,977 policies, full-risk median $1,443, claims paid in AE 2016-2025.
- Additions:
  1. Counties with the most policies in this zone, linked (PLAN item 2): Policies v3.
  2. Share of all NFIP claims (and paid dollars) rated outside A/V zones: Claims v3 `ratedFloodZone`. The real figure behind everyone's unsourced "20-25%".
  3. Zone X: shaded vs unshaded cannot be split in Policies v3 (I) -> gap line naming it; B/C/X grouped is how FEMA codes it.
  4. AO/AH: depth in feet is on the FEMA map (DEPTH field) -> link to the address tool rather than any statement.

### G5. how much is flood insurance / flood insurance cost
- Top (V search; Policygenius read): Progressive, NerdWallet ($899 avg), Bankrate, LendingTree ($1,064 avg NFIP), Insurify ($786 median), Hippo. Figures conflict, bases rarely stated (mean vs median, all policies vs homes).
- We give: one labelled base everywhere (single-family primary home, premium + fees, in force 08-31-2026), by state, county, ZIP, zone; full-risk gap.
- Additions:
  1. One national answer block on the home page: U.S. median $1,066 (V palm-beach page) + quartiles + by-zone row, with the base spelled out: Policies v3.
  2. "Why the numbers online disagree": one sentence each on mean vs median, premium vs premium-plus-fees, homes vs all policies, linked to methodology. Unique, truthful, citable by AI answers.
  3. Contents-only (renter) median: Policies v3 (pending PLAN item 5 tenant-flag check).
  4. Private prices: printed gap line (no public dataset).

### G6. flood insurance <state> / <town> ($190k state money)
- Top (V search; Policygenius read): Bankrate, Policygenius ($964, no source; 2.5M FL homes in SFHA, 43% insured), NerdWallet, Florida CFO/OIR (57 private flood carriers), Insurify, Kin.
- They give: private-carrier lists, Citizens flood requirement, quote forms. We give: county medians and ranks, ZIP range, CRS discounts, claims, Citizens rule (V palm-beach screen 1).
- Additions:
  1. "Is it rising": median by year for the state from Policies v3 history (policies in force at each year-end), labelled.
  2. Regulator's private-carrier list link via `rule()` (FL OIR etc.), no names copied.
  3. Take-up (policies per housing unit): cut on purpose in `card_spec.py`; competitors lead with it. **Owner decision** to revisit.
  4. Towns: county titles already carry the largest city (V "Palm Beach County, FL (Boca Raton)"); add the top-2 cities by policies to the H1 subtitle for "flood insurance chicago" style queries (Cook County). No city pages (rule).

### G7. renters
- Top (V search): FloodSmart agents pages, NerdWallet, The Zebra, FEMA press release, MoneyGeek. They give: contents-only up to $100,000, ~$100/yr entry, USAA exception, no loss-of-use.
- Additions:
  1. Median contents-only renter premium by state: Policies v3 (after tenant-flag check).
  2. Renter contents claims paid by state: Claims v3 contents payments with occupancy.
  3. "Can I buy here": community participates in the NFIP (Community Status Book), from ZIP lookup. Sanctioned/suspended communities = no NFIP policy.

### G8. nfip
- Top (V search): CRS reports (everycrsreport 2026-10-05 R44593), PGPF, FloodSmart, Wharton.
- Additions:
  1. Authorization end date and what a lapse means for new policies/renewals: `rule()` from current statute/CRS raw text (PLAN item 7, 12-11).
  2. Policies in force nationally by year: Policies v3.
  3. Communities participating / probation / suspended: Community Status Book.
  4. Program debt: only with a raw-read CRS or Treasury figure; else omit.

### G9. claims
- Top (V search): FloodSmart historical claims tool, NRDC tract map, E&E "8 counties got half of 2020 claims", Apify scraper. Nobody publishes paid share by county with FEMA's reason codes; we do (V live: 83.4% of 267,655 claims since 2020 had a recorded payment; 52.7% Terrebonne to 94.4% Somerset; "Not an actual flood" 29.0% of no-payment claims; CSV `/data/claims-2020-counties.csv`).
- Additions:
  1. Median paid amount per paid claim by county: Claims v3.
  2. Paid share by zone (inside vs outside A/V): Claims v3.
  3. Repeat-flooded properties count by county: IA Multiple-Loss Flood Properties.
  4. Per-event table for the largest declared floods: Disaster Declarations + Claims v3 date of loss.

### G10. rates by zip
- Top (V search): Policygenius (~14,000 ZIPs, floor 5 policies), Pew 2021 map, Saferate (estimates: a trap for us), Bradenton Herald / Sun-Sentinel / WLRN 2023 Risk Rating 2.0 ZIP stories, floodinsuranceguru Houston.
- We give: ZIP medians with a policy floor, inside the county page + `/zip/`.
- Additions:
  1. Per ZIP: share of single-family policies paying under FEMA's full-risk price (the "is it rising" answer, aggregate, no calculator): Policies v3 (already computed per county, V 23.2% palm-beach).
  2. Per ZIP: policies in A/V zones share: Policies v3.
  3. Printed floor line where a ZIP has too few policies ("fewer than 30 priced policies: county figure shown").

### Tools: help vs trap
Help (and link-earning):
- Address tool (existing), after D1-D5. Strongest money keyword (100k+/mo band).
- "LOMA near me" inside the address tool (FEMA layer 34): unique, buyer-decisive.
- ZIP lookup (existing) + full-risk share per ZIP.
- Policy start-date / 30-day wait tool (existing, 11-18 "all").
- Embeddable county fact table (static HTML snippet with source line and link back): link asset.
Traps under our rules: premium estimate or rise calculator; "do I need it" verdict; any address-level claims history; drawing, caching or mirroring zones (incl. Esri Living Atlas copy as a fallback: it is not FEMA's live service); per-address risk scores (no public dataset, would be an estimate); carrier comparison/quotes (paid referrals off).

---------------------------------------------------------------------------------------------------

## PART 3: backlinks for an anonymous 3-week-old site

Prerequisite (owner): a corrections/contact address on /about/ (PLAN owner list). Journalists and .gov pages do not link a data source they cannot write to. Publisher can stay anonymous; the contact cannot be absent.

### Link assets to build (from data we already hold)
1. Claims payment page + CSV (exists, V). Add median paid per claim and a per-county permalink anchor.
2. County data CSVs (exist, `data.csv` noindex, V `_headers`): one "download all counties" CSV with a data dictionary and as-of date. Data journalists link downloads.
3. Disaster kit: when OpenFEMA Disaster Declarations lists a new flood declaration, the county page shows a dated "Flood declared <date>" fact box (policies in force, median, homes in A/V, claims since 2016). Owner sends it to that county's newsrooms within 48 h.
4. Map-age tracker: "counties whose FEMA flood map is oldest" from NFHL layer 3 for every county (today 225, V; oldest panel 1995-01-05 Prince William County VA). Updated monthly by `map-status.yml`.
5. Full-risk gap table: share of homes paying under FEMA's full-risk price by county/ZIP (the Risk Rating 2.0 story newsrooms ran in 2023, refreshed).
6. Embeddable county table (static snippet, source line, link).
Skip: annual report PDF (no reader), infographics without data, quizzes.

### Targets by type
- Local newsrooms after flood declarations: metro desk + consumer reporter at the 2-3 TV stations and the daily in the declared county (e.g. Houston: Houston Chronicle, Houston Public Media, click2houston, abc13; Tampa Bay: Tampa Bay Times, WUSF, Axios Tampa Bay, which already links county flood-zone tools, V search).
- Data/climate journalists: Floodlight, Inside Climate News, ProPublica, E&E News (ran county claims analysis, V search), Texas Tribune, WLRN, Pew (2021 ZIP map), First Street press list.
- Floodplain managers: ASFPM state chapters (Florida FFMA, Texas TFMA, Louisiana LFMA, NC NCAFPM, NJAFM); CRS coordinators (CRS Activity 330 outreach needs local flood-insurance facts, I).
- Real estate / mortgage educators: state Realtor associations' news (Florida Realtors appears in results, V), HAR.com flood page, buyer-education nonprofits, HUD-approved housing counselors.
- University extension / Sea Grant: UF IFAS (ask.ifas.ufl.edu ranks for "nfip", V), LSU AgCenter, NC Sea Grant, Texas A&M AgriLife, Penn State PSIRC (publishes NFIP one-pagers, V search).
- Libraries: public and university LibGuides on flood insurance / home buying / GIS data.
- .gov resource pages: county emergency management and floodplain pages that list "flood insurance resources"; state insurance department consumer pages (FL CFO, TX TDI, LA LDI).
- Wikipedia: low value (nofollow), conflict-of-interest risk; only flag a stale figure on the Talk page with the FEMA primary source. Never add our own links.

### Pitch angles (exact figures, all V on live pages 11-08)
- "1 in 6 NFIP flood claims since 2020 had no recorded payment: 83.4% of 267,655 paid; from 52.7% in Terrebonne Parish, LA to 94.4% in Somerset County, NJ." (claims page)
- "The top recorded reason for no payment: 'not an actual flood', 29.0% (12,866 claims)." (claims page)
- "A zone AE single-family home pays a median $1,252 a year (961,977 policies, Aug 31 2026)." (zone AE page)
- "In Palm Beach County 23.2% of single-family homes still pay under FEMA's full-risk price" (county page; repeat per county for each newsroom).
- Map age per county (asset 4) once built.

### Cadence
- Week of 11-10: contact address live (owner); build nothing new for links until it is.
- From then: 5 personal pitches a week (owner), each with that recipient's county figure; plus a disaster-kit email within 48 h of each new flood declaration.
- Monthly (after the refresh): one "what changed this month" note to the reporters who replied.

### Never
Paid links, PBNs, link exchanges, guest-post farms, directory/citation spam, "sponsored" without rel, buying expired domains, fake personas or fake credentials, mass HARO-style answers, self-added Wikipedia links, comment/forum spam, any link from calcscrape or river (CLAUDE: separate sites).

### Checkpoints (Search Console Links report, free)
- 11-26: baseline referring domains (expect 0) with the 4-week review.
- 12-15: 2+ referring domains from pitches; else change the angle (claims -> map age).
- 01-15: 5+ referring domains, 1+ news, .gov or .edu.
- 02-01: claims page 1+ new referring domain or 100+ impressions (PLAN); 0 = stop pitching claims, pitch the disaster kit only.
- 03-01: 15+ referring domains; an asset kind with 0 links after 15 pitches is cut.

---------------------------------------------------------------------------------------------------

## ONE ranked build list (smallest test first; each with a dated continue/kill number)
| Rank | Item | Size | Test that fails first | Continue / kill |
|---|---|---|---|---|
| 1 | D1 stale-result token (pin drag + geocode race) | ~10 lines JS | click-path fixture with 2 s FEMA delay, drag, assert no zone under the new pin | Truth fix; ship before 11-20 or hold "all" |
| 2 | D4 live gate asserts real zones + nightly in `watch.yml` | ~10 lines | live run with layer id 999 must FAIL | 11-20: 7 green nights in a row, else hold "all" |
| 3 | D2 zone-code allow-list with data-dictionary labels (own oracle table) | ~20 lines + raw read | fixture "OPEN WATER" must not print "Zone OPEN WATER" | Truth fix; before 11-20 |
| 4 | D5 circle buffer (`distance=15`) after a US-runner probe | ~5 lines, deletes Mercator math | fixture asserts `distance=15` and `units` in the query; probe shows FEMA honours it | Before 11-20; if FEMA ignores `distance`, keep box and say "about 15 to 20 meters" |
| 5 | D3 LOMA/LOMR near the pin + always-on gap line | ~30 lines | fixture with a layer-34 hit must print case number, date, outcome | 01-29: hub 200+ impressions at pos <= 20 (PLAN) |
| 6 | Contact/corrections address (owner) | owner | n/a | Prerequisite for 7-9 |
| 7 | Hub: tool open on load + cost and claims for the answered zone in that county | ~40 lines | hub page shows the address field without a tap; oracle for county figure | 01-29: 200+ impressions pos <= 20, under 50 = fold into home (PLAN) |
| 8 | Zone pages: counties with most policies in the zone + claims outside A/V share (PLAN item 2) | builder | gate: figure via `tp()`, recompute matches | 01-08: pos <= 15 on "zone ae/x cost"; worse than 40 = stop zone work (PLAN) |
| 9 | Disaster kit box on declared counties (Disaster Declarations) + all-counties CSV | builder | build with a fixture declaration shows the dated box only for that county | 02-01: 1+ referring domain from 10 kit pitches, else stop |
| 10 | Map-age tracker for all counties (NFHL layer 3 via `map-status.yml`) | runner job + 1 page | page count equals counties FEMA answers for | 03-01: 1+ referring domain or 100+ impressions, else fold into states |
| 11 | ZIP full-risk share + A/V share | builder | recheck recompute equals page | 02-03: ZIP impressions > 0 on "flood insurance rates by zip" queries, else drop |
| 12 | D6 measure FEMA tiles per lookup; drop overlay if > 5 | measure first | one real run count | Before 11-20 |
| 13 | D7-D11 minors | small | each its own fixture | with the next batch |

Owner decisions surfaced (not built): BFE/depth in the address tool (rule lists zone, panel, date only); take-up figure (cut in `card_spec.py`, competitors lead with it); Esri Living Atlas as a fallback (not FEMA's live service: recommend no).
