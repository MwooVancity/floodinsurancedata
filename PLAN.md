# PLAN: floodinsurancedata.com

## Goal
The most helpful flood-insurance page for each US state and county, from public federal data. Reader: a homeowner or buyer with a flood-zone letter or a renewal, on a phone, 60 seconds (see CLAUDE.md).

## Where we are (2026-10-28)
- Built site: `dist/flood-insurance/` has 104 folders (51 states, 52 counties and parishes, index.html); `tools/counties.json` 52 counties; `state/county-queue.json` 1,803 counties queued. Last dist commit 514d1559 (publish: added 10).
- Live: rounds 10-12 fixes, shipped 2026-10-28 as a hotfix (commit 5a56b096): live gate 110 pages = build; horry-county-sc read live.
- Data as-of: 2026-07-31 (`data/us/asof.json`).
- Reviews (`state/reviews/*.json`): PASS home, orange-county-ca, atlantic-county-nj, broward-county-fl, palm-beach-county-fl; FAIL horry-county-sc, louisiana, montgomery-county-tx, nevada, oklahoma (round 12, wording MAJORs, fixed in code since). Round 13 not run.
- Search Console: verified 2026-10-23, sitemap submitted (commit 289d7f3c). Traffic: not measured, status unknown.
- The template has no current PASS, so the daily county job adds nothing until one light check passes (step 1).

## Site structure (silo) — checked in the built HTML 2026-10-28
- Tree: home `/` → hub `/flood-insurance/` → 51 state pages `/flood-insurance/<state>/` → county pages
  `/flood-insurance/<county>-<st>/`. URLs are flat (state not in the path); the hierarchy lives in links and
  BreadcrumbList schema (Home › State › County). Decision: keep flat URLs; moving them now costs redirects and gains nothing.
- Down links: each state page's county table links every published county in that state (screen 1 jumps to it).
- Up links: each county links its state in the breadcrumb and in the sibling bar.
- Across: a state links its bordering states; a county links up to 6 published counties in the same state.
- Weak spots as counties publish:
  1. County siblings are the 6 BIGGEST in the state, so in Texas every page would link the same 6 and small
     counties would get links only from the state table. Fix: neighbours first, from the Census county
     adjacency file (public), then fill by size.
  2. Under 3 published counties in a state, the bar fills with big out-of-state counties (Horry links Broward,
     Harris, Miami-Dade). Fix with 1: no cross-state fill once neighbours exist.
  3. One sitemap (110 URLs); an index is needed only past 50,000 URLs. `lastmod` must stay the real data date.

## Scaling to every county (2026-10-28; counts read from the repo today)
The numbers: 3,028 counties have data (`data/all-counties/`); 1,803 of them pass the page build and sit in
`state/county-queue.json`, largest first; 52 are published. The other ~1,225 are too thin for a page (under 30 priced
single-family policies for a median, or a failed build).
1. **Who gets a page:** only the 1,803 queued counties, largest first. A thin county never gets its own page; it stays
   a row in its state's county table, and the home search sends its readers there. No noindex filler pages.
2. **Before the queue speeds up (one time):** the template has a current PASS (light check, step 1 below);
   neighbour sibling links are in (step 5b); the all-county stress scan has the data-triggered cases (step 2) and
   passes on every queued county. The stress scan, not a reviewer, is what checks 1,800 pages.
3. **Pace:** the daily GitHub job publishes 10 a day (about 6 months for the queue). google_gate S7 caps any release
   at 25 new indexable pages. Never more, even if all pass (owner 2026-10-26: no bulk publish).
4. **Per-page review only where code says the data is odd:** `review.flags()` (unpaid share 20+ points from the
   state's, claims per policy under 0.2x or over 5x) sends that county to its own quick look (cheap model, the
   flagged cards only), batched weekly. Every other county ships on the template PASS plus the gates.
5. **Watch Google, then decide the speed (Search Console, weekly):**
   - Speed up to 25 a day only if, after 4 weeks, most published pages are indexed and impressions grow.
   - Hold at 10 if indexing lags (pages "crawled, not indexed").
   - Stop and investigate if site-wide impressions fall sharply. The car site's 2026-09-14 cliff was site-wide.
6. **Keep it fresh at scale:** the monthly cloud refresh rebuilds every published page's data; `lastmod` moves only
   when a page's data changes. Pages whose county later falls under the floor go back to a state-table row with a
   redirect to the state page.
7. **Later layer:** ZIP pages only after counties index well, and only ZIPs that pass the three-part test.
   Not before.

## What works
- Builder rules make wrong text hard (`tp`, `m`, `claim`, `rule`); 9-question gate on built and live HTML; mutation suite of real shipped bugs.
- Template review on 3 samples plus flags for odd pages; S12 blocks unreviewed pages; S14 ages gaps.
- FEMA pull runs in GitHub Actions monthly; daily job publishes only reviewed counties.

## What does not (yet)
- Twelve hater rounds; louisiana and four other pages still FAIL at round 12.
- No traffic data yet, so no evidence the pages earn search demand.
- PIF workbook listed but pages are not checked against it.

## Next steps (in order)
1. Light check of the changed cards (median label, SRL label, unpaid lead, private-flood rule, county jump link, search message, home zone table) on 2-3 pages, cheap model, after the monthly data job lands. Done when the template has a PASS and the daily job publishes again.
2. Add the data-triggered cases ("Other" is the top unpaid reason; single-family homes a small share of units) to the all-county stress scan. Done when the scan flags them.
3. Read Search Console (impressions and queries per page). Done when numbers with a date are recorded here.
4. Gap backlog top 3 (`state/reviews/backlog.md`): name non-NFIP communities on state pages; USPS-preferred ZIP town names; condo/RCBAP cost line. Done when each is a card or a printed gap and leaves the backlog.
5. Official FEMA policy-count comparison (PIF workbook) on every page, or delete the "not yet compared" line. Done when the gate checks it.
5b. Neighbour sibling links (Census county adjacency file) before counties publish in bulk. Done when a county's
   bar lists its bordering published counties first and no page links out of state while neighbours exist.
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
