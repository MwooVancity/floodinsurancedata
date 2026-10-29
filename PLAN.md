# PLAN: floodinsurancedata.com

## Goal
The most helpful flood-insurance page for each US state and county, from public federal data. Reader: a homeowner or buyer with a flood-zone letter or a renewal, on a phone, 60 seconds (see CLAUDE.md).

## Where we are (2026-10-28)
- Built site: `dist/flood-insurance/` has 104 folders (51 states, 52 counties and parishes, index.html); `tools/counties.json` 52 counties; `state/county-queue.json` 1,803 counties queued. Last dist commit 514d1559 (publish: added 10).
- Live: the round 9 release (home, 51 states, 52 counties) per the previous CLAUDE.md; rounds 10-12 fixes are committed, not live. Not read live this session: status unknown.
- Data as-of: 2026-07-31 (`data/us/asof.json`).
- Reviews (`state/reviews/*.json`): PASS home, orange-county-ca, atlantic-county-nj, broward-county-fl, palm-beach-county-fl; FAIL horry-county-sc, louisiana, montgomery-county-tx, nevada, oklahoma (round 12, wording MAJORs, fixed in code since). Round 13 not run.
- Search Console: verified 2026-10-23, sitemap submitted (commit 289d7f3c). Traffic: not measured, status unknown.
- Uncommitted local changes in `data/c/` and `dist/` (git status): status unknown, not part of any release.

## What works
- Builder rules make wrong text hard (`tp`, `m`, `claim`, `rule`); 9-question gate on built and live HTML; mutation suite of real shipped bugs.
- Template review on 3 samples plus flags for odd pages; S12 blocks unreviewed pages; S14 ages gaps.
- FEMA pull runs in GitHub Actions monthly; daily job publishes only reviewed counties.

## What does not (yet)
- Twelve hater rounds; louisiana and four other pages still FAIL at round 12.
- No traffic data yet, so no evidence the pages earn search demand.
- PIF workbook listed but pages are not checked against it.

## Next steps (in order)
1. Hater round 13 on the round-12 FAIL pages (FIRST/light: changed cards only). Done when all 5 have PASS in `state/reviews/`.
2. Ship rounds 10-13 via `python -I tools/release.py --ship`. Done when the live gate passes and a live page is read.
3. Read Search Console (impressions and queries per page). Done when numbers with a date are recorded here.
4. Gap backlog top 3 (`state/reviews/backlog.md`): name non-NFIP communities on state pages; USPS-preferred ZIP town names; condo/RCBAP cost line. Done when each is a card or a printed gap and leaves the backlog.
5. Official FEMA policy-count comparison (PIF workbook) on every page, or delete the "not yet compared" line. Done when the gate checks it.
6. Keep the daily county job adding reviewed counties a few at a time. Done when published counties rise each day with PASS signatures.
7. After four weeks of Search Console data: AdSense review. Done when the owner decides.

## Owner only
- Search Console review after four weeks; AdSense and consent banner.
- Paid quote referrals: only after a state-licensing + FTC disclosure check.
- Opening pages to the index; cutting any block; domain.

## Open decisions
- ZIP pages (~2,500 with 100+ priced policies): wait until county pages pass review and Google shows indexing.
- Data stories (county rankings) for backlinks: not built.
- Territories (PR, USVI, Guam): left out, no line says so yet (round 8 backlog).

## Facts kept from the old reader spec (2026-10-22)
- Competitors: floodfigures.com (NFIP-only, no county pages, no percentiles or full-risk); floodcostzip.com (ZIP-level, full-risk and projections). Our edge: seven datasets joined per county, CRS discount, sourcing.
- Endpoints: OpenFEMA v3 NfipPolicies/NfipClaims (`propertyState` required; county = `censusGeoid[:5]`; `$top=1000`), v2 DisasterDeclarationsSummaries, v2 HousingAssistanceOwners (`zipCode`), v1 NfipCommunityStatusBook; NRI ArcGIS `National_Risk_Index_Counties` (`STCOFIPS`). NFHL point query unreachable; link FEMA's map.

## Done recently
- 2026-10-28 dropped the premium-rise calculator (owner: too risky); cited 42 U.S.C. 4015(e) (2e46c79b).
- 2026-10-28 round 12 fixes and private-flood lender rule 12 CFR 339.3 (8c970f16).
- 2026-10-28 round 11: one flood-disaster rule for counts, aid and claim checks (1f638128).
- 2026-10-28 stress test on 1,803 counties: repeated NRI sentence and FEMA sequence numbers fixed (d8e204f6).
- 2026-10-28 published 10 more counties (514d1559).
