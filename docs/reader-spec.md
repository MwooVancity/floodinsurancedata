# Flood insurance data site — reader spec + dataset catalog

Planning doc. Does not change any site. Written 2026-10-22. River-style: the product is a
**flood dataset catalog**, one panel per public dataset that bears on a homeowner's flood decision,
in the reader's priority order, every number with its exact federal source and as-of date.
No quote, no advice prose, no verdict. Supersedes the narrower cost-only framing in
`flood-site-build-plan.md` section 3 (that plan's data pipeline and compliance sections still hold).

Labels: VERIFIED = probed the live API this session; PLAN = from flood-site-build-plan.md (2026-10-12),
to re-confirm; MEMORY = dataset believed to exist, must probe before it enters a page (null beats memory).

## 1. Reader (one paragraph)

A US homeowner or home buyer at a specific place — on a phone, holding a lender's flood-zone
determination, a renewal notice, or the question "do I even need this." Deciding a purchase or a
renewal, days of urgency. Wants the truth about THIS place, not a national average. Not a pro,
not a researcher. Reads for 60 seconds.

## 2. The reader's questions, in priority order

Every page answers these in this order, each from its own dataset, above any long tables:

1. **How much flood risk is actually here?**
2. **Am I legally required to carry flood insurance?**
3. **How much does flood insurance cost here?** (the spread, not one average)
4. **Is it going up?**
5. **What do floods actually pay out here?**
6. **Can I pay less than the sticker price?**

A question with no dataset is printed as a visible gap line ("Not available at this place: ...").
A dataset that answers no reader question is left out.

## 3. Dataset catalog — every public API vs each question

| # | Reader question | Dataset / endpoint | Per-place unit | Evidence (probed 2026-10-22) |
|---|---|---|---|---|
| 1 | How much risk here? | FEMA National Risk Index `National_Risk_Index_Counties` FeatureServer (FEMA_NationalRiskIndex ArcGIS org; Coastal `CFLD_*` + Inland `IFLD_*`: expected annual loss, rating, national percentile) | county, tract | ✅ VERIFIED in production (`tools/nri.py`), match on `STCOFIPS` |
| 1b | What flood zone am I in? | FEMA NFHL ArcGIS MapServer layer 28, point query | address/point | ⚠️ UNREACHABLE from this env (connection reset, both hosts). Covered: per-place zone MIX comes free from NFIP `ratedFloodZone`; point lookup = client-side link to FEMA map |
| 2 | Required to buy it? | Derived: SFHA zone + quoted federal mandatory-purchase rule | zone | rule is quotable |
| 3 | How much does it cost here? | OpenFEMA NFIP Policies v3 `policyCost`, spread p25/p50/p75/p90 | ZIP, county | ✅ VERIFIED endpoint (count 90,224 Lee) |
| 3b | How far below true (full-risk) price? | NFIP Policies v3 `fullRiskPremium`, share below | ZIP, county | ✅ VERIFIED field exists |
| 4 | Is it rising? | NFIP Policies v3 by effective year; the full-risk gap closing | county | PLAN — needs cohort care |
| 5 | What do floods pay out here? | OpenFEMA NFIP Claims v3, claims per 100 in-force policies + raw | ZIP, county | ✅ VERIFIED endpoint |
| 5b | Did the govt pay owners after floods? | OpenFEMA `HousingAssistanceOwners` v2 (160,655 rows): `totalApprovedIhpAmount`, `validRegistrations`, `averageFemaInspectedDamage`, `zipCode`, `county` | ZIP, county | ✅ VERIFIED — fields confirmed |
| 5c | How often is this county a flood disaster? | OpenFEMA `DisasterDeclarationsSummaries` v2 (70,571 rows) by `fipsCountyCode` + `incidentType` | county | ✅ VERIFIED — Lee FL = 21 flood/hurricane declarations |
| 6 | Can I pay less? | OpenFEMA `NfipCommunityStatusBook` v1 (25,130 rows): `classRating`, `sfhaDiscount`, `nonSfhaDiscount` | community | ✅✅ VERIFIED — Lee FL: Cape Coral 25%, Sanibel 25%, Fort Myers 20%. No competitor shows this |
| ctx | Share of homes insured? | NFIP official PIF workbook ÷ Census ACS B25001 housing units | county | MEMORY — ACS needs free key |
| ctx | Does our count match FEMA? | FEMA official PIF workbook (reconciliation line) | county | PLAN 1.9% |

### Verified endpoints (2026-10-22)
- NFIP Policies/Claims: `https://www.fema.gov/api/open/v3/NfipPolicies` (page `$top=1000`, `propertyState` required, county = censusGeoid[:5]).
- Disaster declarations: `https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries` (`state`, `fipsCountyCode`, `incidentType`).
- Housing assistance: `https://www.fema.gov/api/open/v2/HousingAssistanceOwners` (filter field is `zipCode`, not `damagedZipCode`).
- CRS discount: `https://www.fema.gov/api/open/v1/NfipCommunityStatusBook` (filter `state`, `county`).
- National Risk Index (production): `https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query` (keyless FEMA_NationalRiskIndex org; `where STCOFIPS='<geoid>'`; coastal `CFLD_*`, inland `IFLD_*`). The earlier `services2.arcgis.com/EiGeaCDLpVDPqdJ5` copy was a non-national (Utah) sample and is NOT used.
- NFHL point: `hazards.fema.gov/arcgis/.../NFHL/MapServer/28` — reset from this env; revisit from the collector host or use client-side.

## 4. API behaviour (VERIFIED this session, 2026-10-22)

- Endpoint live: `https://www.fema.gov/api/open/v3/NfipPolicies`, total records 74,739,464
  (plan recorded 74,739,461 on 2026-10-12 — grew by 3).
- County in-force filter that works: `propertyState eq 'FL' and startswith(censusGeoid,'12071')
  and policyEffectiveDate le '<asof>' and policyTerminationDate ge '<asof>'`. Returns Lee FL
  count = 90,224, matching the plan's row count exactly.
- `propertyState` is REQUIRED in the filter. `startswith(censusGeoid,...)` alone returns 503.
- There is no `countyCode` field on Policies (`countyCode eq ...` returns HTTP 400); county = first
  5 chars of `censusGeoid`.
- `$top=10000` with this filter + `$orderby` + `$inlinecount` reliably returns 503 (server load).
  Collector must page at `$top=1000`, request `$inlinecount` once, keep `$orderby id` for stable paging.

## 5. Page set (river-style: one entity per page, catalog on each)

Primary unit decision: **county is the core page** (official reconciliation exists at county,
counts large enough for a spread, FF skips county entirely). **ZIP pages only where the spread and
full-risk gap add something a median can't**, with a policy floor. **State pages are rollups +
the entry for the only verified demand family.** No city pages (no city field in the data; the
join is the mass-produced pattern Google and our pSEO rules forbid).

- `/flood-insurance/<state>/` — county table (policy units, median, full-risk gap, claims/100, CRS),
  state tile map, risk map.
- `/flood-insurance/<state>/<county>/` — the core catalog page, all six questions.
- `/flood-insurance/<state>/<county>/<zip>/` — only ZIPs above the floor; else a row in the county.
- `/flood-insurance/lookup/` — ZIP or county search landing on the county page.
- `/methodology/`, `/data/` — definitions, reconciliation log, downloadable county CSV.

## 6. What the data honestly cannot answer (printed on the page)

- Your own premium (depends on elevation, coverage, deductible — we show where real policies fall).
- Private flood insurance prices (NFIP only).
- Why the price is rising (we show the gap closing, not the cause).
- Exact flood risk at your address (that's the FEMA map; we link it, not reproduce it).
- Any place below the cohort floor (count only, suppressed charts).

## 7. Differentiation vs the real competition (floodfigures.com + floodcostzip.com, 2026-10-23)

Two direct competitors exist, both built on the same OpenFEMA source. Our earlier claim that "nobody
shows full-risk or percentiles" is NOT true — floodcostzip does. The honest moat is breadth, the county
layer, CRS, and sourcing — not having a cost lookup.

- **floodfigures.com** (Rowan & Maple LLC, as-of 2026-07-21): NFIP-only — counts, a median + mean, raw
  claims since 1978, zone-definition prose. States "Percentiles: not reported. Full-risk premium: not
  reported." 51 states, ZIP pages for FL/LA/TX only, 7,663 city pages, NO county pages.
- **floodcostzip.com**: single-family median, **full-risk comparison**, historical premium comparison,
  **future-cost projections**, claims stats, storm-surge exposure. ZIP-level. This site already answers
  "what will it cost me," so full-risk and a ZIP lookup are NOT our differentiators.

Where we are NOT ahead: raw ZIP cost lookup (both tie us); future-cost projection (floodcostzip has it,
we don't — a modeled series would break our no-verdict/no-modeled-number rule unless clearly labelled).

Our real, still-unique edge (the bet):
1. **Breadth joined per place** — risk (NRI) + legal requirement + disaster history + FEMA aid + CRS +
   take-up on ONE page. Both competitors are NFIP-cost-only. Nobody joins all seven datasets.
2. **County layer** — FF skips counties entirely; our reconciliation to FEMA's official PIF count lives
   at county.
3. **CRS discount** — the only panel that lowers the reader's actual bill. Neither competitor shows it.
4. **Sourcing / E-E-A-T** — exact federal source + as-of on every number, public reconciliation, a real
   methodology page. The transparency a homeowner (and an AI engine citing us) can trust.
This is a narrower moat than the cost-only framing implied. It holds only if every page is genuinely
seven datasets deep and place-specific — a thin rollout of near-duplicate county pages forfeits all of it.

## 8. Biggest risk

Many near-identical geographic pages (the ad-network and pSEO risk). Controls: county pages only where
cohort >= 100; ZIP only above the floor and only when it differs from its county; no city pages; each
catalog panel is place-specific with a mechanism sentence; 3–5 sibling links per page; pilot of ~5
counties spanning extremes before any scale. "All the APIs" is not a licence to pad: a panel stays only
if a homeowner deciding HERE would act on it and one plain sentence ties the dataset to that decision.
