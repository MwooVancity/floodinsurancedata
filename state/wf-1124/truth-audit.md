# Truth audit, 2026-11-24

Scope: 20 county pages (5 largest, 5 median, 5 smallest, 5 "zero-kw" by policy count), all 7 zone pages, /flood-zone-map/, /flood-insurance/zip/.
Read-only. Nothing under tools/, dist/, PLAN.md, CLAUDE.md or state/*.json was edited. Live pages were fetched from floodinsurancedata.com on 2026-11-24 and compared with the source data under data/ and dist/data/.

Labels: VERIFIED = read or recomputed in a file or page this run. GUESS = not read.

## Result

No BLOCKER (no wrong number, no label-vs-data contradiction) was found on any of the 29 pages. One MAJOR (a judgment call on a base label), five MINOR. Details below, ranked.

## Pages sampled

Largest (policy units): miami-dade-county-fl 362,515; broward-county-fl 232,960; harris-county-tx 226,917; lee-county-fl 133,325; pinellas-county-fl 131,666.
Median (of 329): santa-cruz-county-ca 3,270; fulton-county-ga 3,268; currituck-county-nc 3,261; beaufort-county-nc 3,256; kern-county-ca 3,250.
Smallest: lincoln-county-ne 146; pottawatomie-county-ok 131; calaveras-county-ca 123; raleigh-county-wv 108; tooele-county-ut 50.
Zero-kw: 297 of the 329 county pages have a keyword-map.csv floor of 0 for "<county> flood insurance", so the flag does not discriminate. I took 5 evenly spaced from the 297, outside the other groups: montgomery-county-tx, norfolk-county-ma, dorchester-county-sc, onondaga-county-ny, desoto-county-ms.
Zone pages: /flood-zones/ a, ae, ah, ao, d, ve, x. Plus /flood-zone-map/ and /flood-insurance/zip/.

## What was checked and how (VERIFIED)

Live text equals built text: for all 29 pages, the visible text fetched live is identical to the text of dist/ (the raw HTML differs in bytes, most likely line endings; not investigated further).

Counted: 20 county pages hold 7,920 sentence fragments, 4,619 numeric tokens after skipping statute numbers, years and tiny integers. Of these, 3,989 matched a number in the raw county, state or national JSON (data/all-counties, data/c, data/states, data/us), 493 matched only the builder's own per-page data.csv (derived percentages, checked separately below), 137 matched neither. The 137 are fixed constants ($250,000 and $100,000 NFIP limits, 80%, the NFIP phone number, $400,000 Citizens threshold), glued table-cell artifacts of my text extractor, and the FEMA housing-aid sums; the aid sums were then recomputed from data/c/<slug>/data.json (19 pages, 0 differences; Tooele has none). 6,669 sentences on the 20 county pages reduce to 1,055 distinct sentence templates; I read the 70 containing rank or scope words (largest, most, only, since, left out, every, costliest, ranked).

Independent recomputation, county pages (0 differences in 1,800 or so comparisons):
- median, p25, p75, p90, units, record counts, state median, U.S. median (recomputed from cost_hist.json: $1,066), percent-below/above wording and direction;
- "Nth lowest/highest of M counties with 100+ priced policies" recomputed from the state agg (Miami-Dade 24th and Fulton 15th: each is tied with another county at the same median, so the position is correct within the tie);
- worst years and their dollars, totals, paid/no-payment shares, claims that paid, average paid claim;
- unpaid-reason table sums to the unpaid count; top specific reason (the page excludes "Other", consistent with "specific");
- six-year cost trend table (median and priced policies), zone share table and its high-risk total (zone sums, including "Other high-risk zones" and "Other low-risk" rows), zone cost table and the "from about $X (Zone) to $Y" range, the "why can a high-risk zone cost less than Zone X" note appears exactly when the data says so;
- decade table: sums to total claims once the "too few claims" decades named under it are added back (that disclosure is present);
- CRS block: count with a discount, count of NFIP communities, top discount and place, the no-discount count, table rows exist in the source;
- penetration percentages and the "1 in N" wording; flood-event table (claims, paid, average, share, sort order, all events with 20+ paid claims listed) and the "costliest flood FEMA named" sentence;
- the five national research-paper lines on each page (share, 90% range, denominator, fifth, pool size) against dist/data/*.csv; and globally, the fifth assignment of all five CSVs is monotone in the ranked measure, equal printed shares sit in the same fifth, and fifths are of about equal size (damage-over-coverage is the loosest: 54/55/52/62/45);
- peak-month sentence against flood-calendar.csv; map panels (count, oldest, newest), LOMR counts, LOMA total and its four parts against data/us/map_panels.json and map_status.json;
- ZIP blocks on county pages against dist/data/zip (count of ZIPs, 25+ count, min/max median, every table row, sort order); ZIP data globally: no row with 25+ priced policies lacks a median, none with fewer than 25 has one, none has more priced policies than units; 21,632 single-county ZIPs match the state by_zip medians except 9 explained by units with no county or ZIPs entered in another state;
- meta description (median, middle half, share below, units) and title median on all 20 pages;
- "Towns here, ranked by NFIP policy units in their ZIPs": tools/town_check.py run read-only, PASS on all 329 county pages;
- bordering-county lists against data/us/county_adjacency.json: every listed county is adjacent (DeSoto lists Shelby, TN, which is a real cross-state neighbour).

Independent recomputation, zone pages (888 comparisons, 0 real differences): headline median, half-pay range, policy count, full-risk median and count, claims count, paid count, dollars and average per paid claim, the 7-zone comparison table, every state row (median, count, which states are omitted, the "N more states" line), the 10-county table (units rated that exact zone, medians), the X page's "24% outside A and V" (recomputed 24.4% over claims with a zone), AH "86% in Florida" (85.8%), VE "148,141 units" (sum of the state aggregates), the 26%-over-30-years figure. tools/zone_check.py (the project's own independent check) also passes. My first run showed ~45 differences of 1 to 50 dollars on small-state medians and four "more states" counts; all came from my using the binned histograms where the page uses the exact per-state medians in agg.json, and from my counting only priced states, so they are not page defects.

FEMA's own dataset page (read this run through its API): the IA Multiple Loss Flood Properties description says it holds applications "from DR1439 (declared in 2002)", which supports the templated "since 2002" and "flooded in at least 2 different Federally declared flooding events".

## Findings

### MAJOR (misleading base, judgment call)

M1. Meta description: "pay below FEMA's full-risk price" next to a cost figure.
- Pages: all 20 sampled county pages (e.g. https://floodinsurancedata.com/flood-insurance/miami-dade-county-fl/ ); the same template phrase is in tools/build_site.py line 201 (state or home text, read in code only, live page not read).
- Sentence (meta description, Miami-Dade): "Median NFIP flood insurance cost for a single-family primary home in Miami-Dade County (Miami, Miami Beach, North Miami) is $898 a year (middle half $648-$1,210); 43.8% pay below FEMA's full-risk price."
- Source: P.share_below 43.8 with gap_basis "premium": the share whose premium before fees is under FEMA's full-risk premium before fees (body text says exactly this). The page's own table calls the fee-inclusive figure "full-risk premium plus average fees $1,096 ... what these existing policies would cost at FEMA's full price".
- Why it matters: $898 is premium plus fees; "price" can be read as the fee-inclusive figure, so a snippet reader may take 43.8% to compare their bill with a fee-inclusive price. The number is right; the premium/cost base is not stated.
- Fix class: builder. build_page.py line 1006 (county meta) and build_site.py line 201: say "pay a premium, before fees, below FEMA's full-risk premium" and keep one word for the full-risk figure. Goes in the next template batch, not a hotfix (the body text is correct).

### MINOR

m1. Rounding at exact ties prints the lower value (round half to even).
- https://floodinsurancedata.com/flood-insurance/lincoln-county-ne/ : "Damage was more than the coverage (of 32 claims paid with a damage figure) 6.2%". The only count out of 32 that prints 6.2 or 6.3 is 2, and 2/32 = 6.25%, which a reader rounds to 6.3%. (Numerator itself not stored; inferred, GUESS on that detail.)
- https://floodinsurancedata.com/flood-insurance/waller-county-tx/ (dist read, not sampled live): "26.2% of Waller County's NFIP policy units are in high-risk zones"; source 546 / 2,080 = 26.25% exactly.
- Scan of 987 stored percentages (share_below, high-risk share, no-payment share) across all 329 counties: 1 differs from half-up rounding (Waller). Damage-over-coverage and others not scanned.
- Fix class: source rounding in tools/extras_raw.py line 27 (`round(100 * a / b, 1)`) and the matching policy aggregator: use half-up (decimal) rounding. One rebuild of the aggregates, no template change.

m2. Zone-page claims sentence omits "exactly".
- https://floodinsurancedata.com/flood-zones/a/ : "FEMA records 21,712 NFIP claims rated zone A, on every building type". Claims coded A01 to A30 (14,490 claims in the same years) are counted under their own codes, not in 21,712. Same pattern: AH excludes AHB (1,834 claims vs 6,666 shown), AO excludes AOB (443 vs 3,031), VE excludes V01-V22 (about 600 vs 15,567).
- The policy side says "rated exactly A" and the county pages explain that A1 to A30 are counted on their own; the claims line does not, while the same page defines "A, AE, A1-A30: high-risk".
- Fix class: builder zone template: "rated exactly zone A (numbered A1-A30 zones are counted on their own)" on the claims sentence, same wording as the policy side.

m3. "no flood of their own" for a year that appears in a multi-year named row.
- https://floodinsurancedata.com/flood-insurance/harris-county-tx/ : "Of the five costliest years, those with no flood of their own in the table above: 2001". The table has "Tropical Storm Allison (1989-2001): many floods; FEMA's records use this name for claims in several years", $899.8 million; the 2001 year total is $868.7 million, so nearly all of that row is the 2001 flood. The sentence is true under the builder's rule (no single-year row) but reads as "2001 has no named flood".
- Fix class: builder wording, e.g. "with no row of their own (only a multi-year row)". Same sentence on miami-dade (2000, catch-all Flooding 1979-2000, correct), santa-cruz, norfolk, montgomery, dorchester, fulton, broward.

m4. "Bordering counties:" lists only neighbours that have a page.
- https://floodinsurancedata.com/flood-insurance/kern-county-ca/ lists Los Angeles, Ventura, Tulare, Santa Barbara; the adjacency file has 8 neighbours for Kern (4 listed). Pottawatomie: 1 of 7; Beaufort NC: 2 of 6. Every listed county is a true neighbour; the label implies the full list. (Not checked: whether the line also says "with a page" in a title attribute.)
- Fix class: builder label: "Bordering counties with a page" or list all and link only those with pages.

m5. Tie at the 10th place of a zone county table.
- https://floodinsurancedata.com/flood-zones/d/ : "These are the 10 county pages ... with the most policy units rated D." Madera County, CA is listed 10th with 5 units; Skagit County, WA also has 5 and is not listed. The sentence is true but not marked as a tie.
- Fix class: builder: include all tied counties or say "ties at the cut are cut by name". Other zone pages: no tie found.

Nit (not counted): "the worst years were 2000, 1992 and 2005" names years by dollars paid; the next sentence ("Orange bars are the three costliest years") states the base. Fix class: builder wording "the costliest years".

## GAPs (missing features, not defects)

- Four to six county pages with fewer than two qualifying named floods (kern, pottawatomie, raleigh, onondaga) show no "which floods paid out the biggest totals" table although one or two events have 20+ paid claims; builder threshold, not an error.
- Zone-map page cost lines per zone are rendered by JavaScript; no static figures to check.

## Not read or not verified

- /flood-zone-map/ interactive output (map, FEMA answer, per-zone cost lines drawn by zonemap.js) and the ZIP lookup result for any ZIP: the pages' static text is only legal and explanatory text; nothing was typed into the tools. Static sentences (44 CFR, 42 U.S.C., FEMA "covers over 90 percent of the U.S. population") were not re-fetched from ecfr.gov, govinfo.gov or fema.gov; they rest on the rules registry and are UNVERIFIED this run. Florida Citizens dates, s. 627.715 and s. 689.302 text likewise.
- "Premium below full-risk" column in the county ZIP tables, "ZIPs where no single town covers a quarter of the land" figures, NRI percentile sentences and dollar loss estimates: matched a raw number but the derivation was not recomputed (the town ranking is covered by town_check.py).
- Place names beside ZIPs, city lists in meta descriptions, link targets, structured data, images, layout, phone and dark views: out of scope.
- State and home pages, the other 309 county pages, paper pages: not read.
- 493 numbers matched only builder-written data.csv; of these the derived ones were rechecked above, the remainder (for example condo-unit medians, deductible shares, mean costs, claim-damage medians) were not independently recomputed.
- Pages were fetched once on 2026-11-24; a later release can change them.

Scripts used (in the session scratchpad, python -I, ast-checked): zv.py (zone pages), cv.py, cv2.py to cv11.py (county pages), pick.py, tpl.py, ties.py. Not saved in the project.
