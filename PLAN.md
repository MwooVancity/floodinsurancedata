# PLAN: floodinsurancedata.com
State, dated numbers, next moves, owner-only items. Rules: CLAUDE.md. History: git log + state/reviews/fixlog-*.md (a DONE line is deleted, never kept here). Cap ~12 KB.

## Goal and scoreboard
Most helpful flood-insurance page for every US place a homeowner or buyer searches, on a phone. Scoreboard: pages indexed, impressions, clicks, page-1 queries, AI citations.
- GSC 28 d to 11-19 (read 11-21): 23 clicks, 4,480 impressions, CTR 0.5%, position 45.9; 369 pages with impressions; US 20 clicks / 4,309 impressions (the earlier "zero US clicks" is over). By type: counties 233 pages 13 clicks 1,982 impr; states+papers 52 pages 4 clicks 2,161 impr; zone+map 8 pages 0 clicks 514 impr (/flood-zone-map/ 315, /flood-zones/x/ 112); guides 8 pages 1 click 174 impr; ZIP page 3 clicks on 31 impr (best CTR, query "flood insurance rates by zip code" 3/25). City queries land on county pages (salt lake city 42, bradenton 34, grand forks 24 impr, 0 clicks).
- GSC 28 d to 11-10 (earlier): 13 clicks, 1,430 impressions, position 41.7; 329 indexed; crawled-not-indexed 215 (177 CSVs, 36 county pages = 12%, kill line 25%).
- GA4 28 d to 11-08: 4 organic + 4 ChatGPT sessions. Bing: sitemap error 11-10 ("page not accessible", 0 URLs), IndexNow 403.
- Live 11-14: 419 pages (home, 51 states, 329 counties, 7 zones, map tool, /nfip/, renters, claims, ZIP, 9 guides, 5 papers, methodology). Data as of 2026-08-31.
- Cost 11-14: one "do the rest" workflow = 2.63M tokens, 18 agents; every prose stage ended on a FAIL review. Lesson: review loops do not converge (each pass finds new style MAJORs); cap at one fix pass, owner sees the cost first for any run over ~200k.

## Revenue (owner 11-09): $1,500 a month by 2027-11
~50,000 pageviews a month at ~$30 RPM (third-party estimate). Milestones (GA4 pageviews/month): 02-2027 2,000; 05 8,000; 08 20,000; 11 50,000; two misses in a row = re-plan. Links are the lever. Ads only after the 4-week GSC review and above 1,000 sessions/month; referrals after licensing + FTC check.

## Next, in order
3. WAITING 2026-11-22 (weekly GSC read): guides: build the next one only when a live guide shows impressions in GSC (none have yet); queue in "Guides" below.
4. DONE 11-22: outreach #1 sent to LSU AgCenter FloodMaps (owner approved text; owner waived the 2nd editor round; figures re-read live 11-22; guard recorded). Review rule from the 11-22 ChatGPT debate: factual gates stay, severity-ranked, max 2 review passes per outreach email, a missing feature is a GAP never a MAJOR. Round-208 page fixes are committed unshipped (need code review + S12 carry in one template batch).
4c. OWNER 11-22: outreach #2 draft (UF/IFAS Extension Hillsborough, address read on their page) is in state/outreach/pitches.md awaiting owner approval of text; then re-read figures, guard check+record, send. #3-5 candidates still to find (Florida Sea Grant address unverified: flseagrant.org/flood-insurance did not load). Original list: draft 4 more resource-page owners (UF/IFAS county extension, Florida Sea Grant, county CRS coordinators in Pinellas/Hillsborough/Palm Beach), each address read on its own official page, each quoting one figure read live that day; owner approves text before sending. TFMA address unverified (site did not load 11-21).
4b. DECIDED 11-22 ChatGPT round 7 (logged-out chat, brief had no identity data): agreed: 28 multi-county city pages at most and only after each passes an independent-information test (all 2,577 rejected; its 0-30 clicks/month for 28 is a guess); keep factual gates, cut review loops; improve the ZIP page (3 clicks on 31 impressions) before more pages; one paid B2B report test is the owner's go/no-go (item 6). Disagreed: it says stop generic backlink outreach, ours is targeted resource-page asks and links are the lever at position 45.9.
4d. DECIDED 11-22 ChatGPT round 8 (logged-out, no identity data): keep the county pages; do not delete or noindex. Its tiers are ITS guesses, not Google rules: 90-day window; 100+ impressions or 2+ clicks = keep; 10-99 = improve (county vs state comparison, sample sizes, limits); under 10 impressions and 0 clicks = review for merge into the state page (301 only if equivalent, else 410), never permanent noindex. Review the bottom 20% only after 90 days of data (about 2027-01-20). Our check: counties are 13 of 23 clicks; 36 crawled-not-indexed county pages = 12% vs our 25% kill line.
5. WAITING 2026-12-01 Actions reset: FIRST switch the 5 workflows back on (owner 11-16 "no GitHub failure emails": deploy, publish-counties, watch, refresh-data, map-status were switched off on 11-16; actions_check prints RE-ENABLE NOW when the minutes are back; `gh workflow enable <name>`). Then: Flood Map Age data pull via `tools/cloud_run.py` (one forced refresh a month, batch every queued field).
6. OWNER decision (11-21 ChatGPT round 6, same thread as rounds 1-5; its replies are claims, not facts): (a) its one new idea: sell custom county/regional claims reports to law firms, adjusters, consultants (its $250-500 price is a guess; competitors publish the same FEMA county tables free, so willingness to pay is unproven). It needs the owner for sends, invoices, money and publisher identity; say go/no-go. (b) Rejected with evidence: "we show 'closed without payment'" (0 hits in dist and live /data/; only a prose_check bad-example string); CRS lookup and repetitive-loss pages (0 Planner rows in state/keyword-map.csv, so no demand shown); mortgage-requirement page (owned: home 100/mo, lender guides). (c) Taken: reconcile GA4 4 organic vs GSC 13 clicks (windows differ: to 11-08 vs 11-10; GSC clicks include Canada); stop adding CSVs to chase indexing; keep counties frozen at what is live; links first.

## Queued small fixes (next template batch; shipped items deleted, see git)
- Held, need a source quote read raw first (no unsourced definition): Elevation Certificate definition in save_ways; "Emergency Program discount" meaning in glide.
- Next batch: Damage Over Coverage top-county sentence split (paper_gate Abstract regex must change with it); "How risky?" on state pages gives the count of Very High/Relatively High counties (new tagged figure).
- Data check (next cloud batch): 179 of 379 places have a 2021 median of exactly $572 (63 at $633). A guess, unverified: fixed pre-Risk Rating 2.0 Preferred Risk rates make the median land on one price. Verify with the share of 2021 policies at exactly $572 before it goes in an outreach pitch.

## Cloud budget (Actions 2,000 min/month exhausted 11-14: 2,204 used, 33 forced refreshes)
- Built and committed 0853000a2: `tools/cloud_run.py` (median cost + month left, refuses past 50% before the 15th / 90% after), refresh_plan one forced run per month, `tools/actions_check.py` at session start, release.py local deploy fallback when GitHub refuses.
- Open: the new-field queue file (fields wait for the one monthly forced refresh).
- Owner options that remove the cap: Actions spending limit (a few dollars) or public repo.

## Research papers (/flood-insurance/<key>/, standard: docs/PAPER-GATE-PROMPT.md, tools/paper_gate.py)
| Paper | Status |
| Damage Over Coverage | LIVE + indexed 11-13 |
| Outside the Zone | LIVE + indexed 11-13 |
| Deductible Choice | LIVE + indexed 11-13 |
| Flood Calendar | LIVE + indexed 11-14 (correction: Taylor FL 56.5 to 56.4) |
| Price Gap | LIVE staged noindex 11-14; owner opens to index on/after 11-21 (max 2 papers/week) |
| Flood Map Age | BLOCKED on data: share of countywide FIRM panels 15+ years old needs pull_mapstatus --panels grouped by DFIRM_ID,EFF_DATE (US cloud, after 12-01). Edge cases: blank EFF_DATE out; ~636 counties with no digital map printed as excluded, never zero; effective date is not study age; no "outdated/wrong" words |
| Repeat Flood | CUT (IA rows one per property per disaster, no base) |
No new papers for now (owner 11-14: guides over research).

## Demand by kind (tools/kwp_rank.py on the 11-05 Planner export, band floors per month; fixed 11-15: it read the newest file, a hand list)
National heads 38,800 (flood zone map, fema flood map by address, flood insurance: 10K+ each; owners /flood-zone-map/ and home) > states 13,510 (flood zone map <state> 1K+ for FL NJ NY LA NC) > zone meanings 7,530 (x, ae, a, ao 1K+) > counties 7,350 (260 of 271 map keywords already have a page) > towns 3,050 (5,180 keywords; chicago 1K+, rest under 1K). More county or town pages is the smallest prize; the national hubs and state pages are the largest.
## Keyword map (owner 11-15 "all the keywords"): `python -I tools/kwp_rank.py --map` writes state/keyword-map.csv (every Planner keyword, floor/mo, kind, owning built page)
WIDE PULL 11-15 (US, 2,223 ideas, data/kwp/us-2026-11-15-1..4.csv): floor 254,000/mo; 123,630 owned, 130,000 not: FEMA disaster aid 58,160 (navigational, not ours), storm surge 11,500 and basement water 8,420 (off-topic), insurer brands 5,310 and quotes 3,970 (not ours), floodplain 11,000 and what-does-it-cover 7,940 (guides live). More traffic = ranking the owned pages + links, not more pages.
## Open from the growth audit
- Links to us (0 referring domains): the head terms (flood insurance, fema flood map, nfip) are held by FEMA and regulators and need authority, not pages.
6. City pages (owner 11-15 "we can do city too"): towns are 3,050/mo floor over 5,180 keywords (chicago 1K+, sacramento/new orleans/houston/hartford 100+). Build only after 1-4, for the top 25 cities by KWP, each with its own ZIP-level policy and claim figures (ZIP lookup data) and the FEMA lookup; a city whose ZIPs mostly sit in one county page with the same figures = no page. New page type = full review (~250k) before any ships. Edge cases before code: ZIP straddles two cities (count once, name the rule); city across two counties; ZIP with under 30 policies (no median); city name shared by many states (slug with state); claims reportedZipCode vs policy ZIP; 25/day cap.

## Guides (standard: one searched question per URL, answer in 40 words, our FEMA table, rule() quotes only, G6 = a figure no top-3 result has)
Live: homeowners vs flooding, private flood, condo, buying a house in a flood zone, deductibles, Risk Rating 2.0, LOMA/LOMR, claims section; built: contents coverage.
Queue (each needs G1 owner check + G6 figure): flood vents (obstructionType code 15 after FEMA code list read raw); glossary pages only if GSC shows term queries.
Cut with reason: elevation certificate (legacy field, zone-confounded), basement (field 65% blank), cars (no FEMA figure), ICC/limits/required/waiting period (owned by existing pages), FEMA aid vs insurance (mixed incident types).
Edge cases kept: K1 never print a search volume; K2 a KWP file without "United States" is not used; K3 one page per question, never per phrasing; G4 no company names or "best"; G8 0 impressions after 90 days = merge into nearest page (301).

## Backlinks (Claude drafts and sends after owner approves each batch)
- One email per organization ever (outreach guard), one exact figure + the page that holds it, reply address contact@floodinsurancedata.com; CAPTCHA forms left to the owner.
- Send day: `tools/outreach_gate.py <urls>` PASS (editor review, live text unchanged, indexed).
- Drafts: state/outreach/pitches.md (11-15: Wave 2 "homeowners pay" mislabel fixed; all figures dated 11-08, re-read live on send day).
- Batch 1 (owner 11-15 "send them yourself"; owner approves list + text first): resource-page owners who add links (extension services, county CRS coordinators, floodplain-manager chapters, library guides); newsroom tip lines use forms (owner-only). Lead figure read live 11-21: 83.4% of 267,368 NFIP claims since 2020 had a recorded payment.
- Targets: local newsrooms within 48 h of a declaration; data desks; ASFPM, CRS coordinators, extension services, library guides. Numbers: 12-15 2+ referring domains; 01-15 5+; 03-01 15+. Never paid links or swaps.

## Checkpoints and waiting
- 11-21: Price Gap to index (owner). Weekly: GSC + GA4 read, IndexNow recheck.
- 11-26: master audit (docs/AUDIT-PROMPT.md) + black-hat prompt + 4-week GSC review; ads decision.
- 12-01: Actions minutes reset. 12-04: 30+ impressions on "flood zone/map" queries, else restore old titles; shorten titles/descriptions.
- 12-09: monthly top-3 compare on every keyword group. 12-12: NFIP authorization past 12-11? If it lapses set `start` to [].
- 01-04: unfreeze zero-demand counties only if 5+ county pages have US non-brand impressions, 3+ in top 30, 1+ click. Then 20/day, cap 25 new pages/day all kinds.
- 01-05: .git size (241 MB 11-11, ~12 MB/day); at 1 GB move built pages to a 'site' branch.
- 01-08 zone pages position 15 or better; 01-29 /flood-zone-map/ 200+ impressions; 02-01 claims page 1+ referring domain or 100+ impressions; 02-03 continue / consolidate / stop.

Nightly in the public repo MwooVancity/flood-lookup-watch (03:41 UTC, free minutes); actions_check reads it (W1 red, W2 older than 2 days, W3 test copies differ: push tools/live_zonemap.py + test_zonemap.py there, W4 unreachable). Uses FEMA's Map Service Center NFHL copy (msc.fema.gov/arcgis/rest/services/NFHL_Print/NFHLQuery/MapServer, LOMAs layer 2) because hazards.fema.gov returns 504. Passed 11-16. Still on hazards: tools/pull_mapstatus.py (after 12-01 switch it, LOMA layer 34 becomes 2).
Nightly in the public repo MwooVancity/flood-lookup-watch (03:41 UTC, free minutes); actions_check reads it (W1 red, W2 older than 2 days, W3 the two test copies differ: push tools/live_zonemap.py + test_zonemap.py there, W4 unreachable). First runs 11-15: FEMA's map service answered HTTP 504 Gateway Time-out for all 5 addresses (FEMA's side, as on 11-13); the page matched FEMA (showed no zone, linked FEMA's map). FIXED 11-15: diagnosis from the US runner showed hazards.fema.gov's whole NFHL service returning 504 (even its front page), while FEMA's Map Service Center copy (msc.fema.gov/arcgis/rest/services/NFHL_Print/NFHLQuery/MapServer: same layers 28/3/1, LOMAs layer 2, map images, CORS allows this site) answered in 0.3 s. zonemap.js, live_zonemap.py and test_zonemap.py now use it (local tool test PASS, carry r203); ships tonight, so the 03:41 UTC run on 11-16 is the first that can pass. Still on hazards: tools/pull_mapstatus.py (cloud data pull, after 12-01): switch it the same way before its next run (LOMA layer 34 becomes 2).
## Runs on its own
Daily `publish-counties.yml` (paused with Actions minutes), monthly `refresh-data.yml` (skips when current), `map-status.yml`, nightly `watch.yml`. Session start: `tools/actions_check.py` reads refused/failed runs.

## Never in copy
Open vs closed claims; "denied"; a period or base left out; a promise of AI citations; IndexNow as proof of indexing; a premium estimate or rise.

## Owner only
Decisions, sends, money, identity. (Bing sitemap DONE: read 11-15, submitted + crawled 11-15, Success, 412 URLs, 0 errors.) GA: mark home IP as internal traffic. AdSense "Request review". Price Gap to index. Drop the second table of contents (yes/no). Actions spending limit or public repo (optional).

## Reference
- Datasets: NFIP Policies v3, Claims v3 (codes 98/99 out), NRI, Disaster Declarations, Housing Assistance Owners (flood only), Community Status Book, IA Multiple-Loss, NOAA Sea Level, FEMA NFHL (US cloud). Cut on purpose (`card_spec.py`): Census take-up, NOAA storm events, tile maps.
- Address tool: never compute, draw or store a zone; show FEMA's live zone, panel, date, BFE/AO depth and map letters as returned.
- Rules: one example is not a rule; `recheck` re-reads live text; unreachable sources in `state/manual-rule-read.json` (183 days max).
- S12: `review.flags()` pages need their own PASS or a same-kind example at most 2x out. `hater.py prep <round> <slugs> --local --light [--proofread|--editor]`, `hater.py record <round>`, `hater.py carry <round> passed <slugs>`.
- Paper harms H1-H16 and edge cases E1-E31 (built into paper_gate.py mutations): full lists in PLAN.md at commit 0853000a2 (`git show 0853000a2:PLAN.md`).
