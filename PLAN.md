# PLAN: floodinsurancedata.com
State, dated numbers, next moves, owner-only items. Rules: CLAUDE.md. History: git (a DONE line is deleted, not kept). Cap ~8 KB.

## Goal and scoreboard
Most helpful flood-insurance page for every US place a homeowner or buyer searches, on a phone. Scoreboard: pages indexed, impressions, clicks, page-1 queries, AI citations. Polish only where a number says a page fails.
- Search Console 28 days to 11-06: 5 clicks, 872 impressions, 225 pages and 235 queries seen, avg position 39.5. Best: Brevard pos 8.2 (41 impr, 1 click), New London CT pos 2 (2 clicks), Florida state pos 25.9, zone X 83, zone AE 75; /flood-zone-map/ not yet in the top 10 pages by impressions.
- GA4 11-01..08: 7 real visitors (13 more were our nightly test, filtered since 11-08): 4 from ChatGPT (no query passed, so no keywords), 3 organic, all engaged. ChatGPT search reads Bing's index; IndexNow gets 403 until the owner verifies the site in Bing Webmaster Tools. llms.txt labelled 11-08 (test_site_factory checks it).
- Index 11-06: home, 51/51 states, 204/232 counties, 6/7 zones indexed; our canonical kept everywhere. Low rank = age and no links, not a technical block.

## Live now (11-09)
- ~343 live pages: home, 51 states, ~280 counties, 7 zone pages, /flood-zone-map/ (address tool), /nfip/, renters, claims (+CSV), ZIP lookup, methodology. Address and start-date tools on 3 samples (`tools/tools_flags.json`). Data as of 08-31 (FEMA bulk files).

## Money order (owner 11-07: money groups first, counties last)
Keyword Planner volume x top bid: state insurance $190k, map $90k, towns $47k, zones $37k, cost $37k, NFIP $36k, state map $25k, renters $18k, county map $15.5k. Not targeted: head term "flood insurance" (FloodSmart), quote and companies (forbidden). Every money page is live; counties now run 20 a day, queue "kw" > 0 only (~1,200 zero-demand counties wait for the Jan 4 rule).

## Next, in order
2. 11-15: weekly Search Console + GA4 read (bot-free GA from 11-08).
3. 11-18 start-date tool "all"; 11-20 address tool "all" after 7 green nightly live tests (watch.yml; a FEMA outage fails safe, as on 11-08).
4. 12-12: did Congress extend the NFIP past 2026-12-11? During a lapse set `start` to [].
5. Top-3 compare (owner 11-09, ONLY GOAL): every keyword group's Google top 3 vs our page; each real gap built or decided. Monthly: next 12-09. Run 11-09 built: claim limits on home; lowest-floor law (60.3(c)(2)) on AE/AH; 50% rule on high-risk zone pages (rewritten from raw 59.1 + SFIP D, live on every county); claims page: ten costliest loss years + claim-size range by state (claims_check C6-C8); ZIP result shows the county median beside the ZIP's. Decided, not printed: evacuation vs flood zone (Florida's official page calls evacuation zones flood zones: sources disagree); renters "landlord policy does not cover your things" (not in FloodSmart's raw text); ZIP-level preliminary-map compare (FEMA's tool, address-level); national median claim (needs per-claim amounts; state range shown instead).
Backlog (`state/reviews/backlog.md`): every item BUILDING or DECIDED (11-08).

## HCU + Google patent review (11-09)
- Rater view: local, sourced, labelled answers with real information gain; gaps now come from the monthly top-3 compare (Next 5).
- Patents (info gain US11354342, site quality US9031929, Panda US8682892, long clicks US10229166): 0 links and 0 branded searches cap every page; only links and mentions move them (Backlinks).
- Decided, not built: elevated / foundation medians (confounded); author byline (owner: anonymous); zone breadcrumb schema (no reader number).
- Edge cases and guards: `docs/EDGE-CASES.md`; fix procedure for anything the gates passed and every data feed: `docs/GATE-FIX-PROMPT.md`.

## Backlinks (owner 11-08: basics, Claude drives; owner only presses send)
Why: 0 referring domains, position ~44; page 1 for money terms needs links. Claude builds each asset, the named target list and the draft pitch; the owner sends.
- First, owner: a corrections/contact address (reporters and .gov pages won't link a source they can't write to).
- Drafts ready 11-08 (`state/outreach/pitches.md`): waves 1-3 + disaster kit; all wait only on the owner's contact address. Next asset is built when the first has 15 pitches out (cut rule below), not before.
- Assets: claims page + CSV (live); all-counties CSV (live, /data/counties.csv); dated fact box on counties with a new flood declaration; oldest-FEMA-map tracker by county (oldest panel today: Prince William County VA, 1995); counties still paying under FEMA's full-risk price.
- Targets: local newsrooms within 48 h of a flood declaration; data desks (Floodlight, Inside Climate News, ProPublica, E&E); ASFPM state chapters and CRS coordinators; extension (UF IFAS, LSU AgCenter, Sea Grant); realtor associations; library research guides; county/state "flood resources" pages.
- Lead pitch (live, checked): 83.4% of 267,655 NFIP claims since 2020 had a recorded payment, 52.7% Terrebonne Parish LA to 94.4% Somerset County NJ.
- Never: paid links, PBNs, link swaps, self-added Wikipedia links.
- Numbers (Search Console Links): 11-26 baseline; 12-15 2+ referring domains; 01-15 5+ incl. one news/.gov/.edu; 03-01 15+. An asset with 0 links after 15 pitches is cut.
- Trust basics with it: About page and corrections route without naming the owner.

## Checkpoints (continue or kill)
- 11-26: master audit (`docs/AUDIT-PROMPT.md`) + 4-week Search Console review in one pass. Sameness: if over 25% of 3-week-old county pages are crawled-not-indexed or duplicate, cut the shared rule paragraphs (gate S2 today: 53% median, 60% max, under 80%).
- 12-04: 30+ impressions on "flood zone/map" queries, else restore old titles.
- 01-04 counties: unfreeze zero-demand counties only if 5+ county pages have US non-brand impressions, 3+ in top 30, 1+ real US click. Fold a county into its state page only if indexed with no impressions and nothing the state lacks.
- 01-08 zone pages: position 15 or better on "zone ae/x cost", worse than 40 = stop zone work.
- 01-29 /flood-zone-map/: 200+ impressions at position 20 or better; under 50 = fold into home.
- 02-01 claims page: 1+ new referring domain or 100+ impressions.
- 02-03: continue / consolidate / stop on US clicks and top-20 non-brand queries.

## Never in copy
That FEMA data shows open vs closed claims; "denied"; a period or denominator left out; a promise of AI citations; IndexNow as indexing proof.

## Runs on its own
- Daily 15:00 UTC `publish-counties.yml` (20 counties, gates, deploy, live gate); monthly `refresh-data.yml` (3rd-10th, skips when data current); `map-status.yml` monthly (US runner); `watch.yml` nightly.
- A failed gate ships nothing; the live site stays. After deploy every live page must equal what passed, else the previous release redeploys. A new county failing a gate is set aside; an environment error (missing library) stops the run instead.
- Failed job: a note on its run page only, no email or issue (owner 11-07). Claude reads failed runs at every session start.
- Warnings in the daily run: Cloudflare token (30 days), domain (expires 2027-10-23). Over 19,000 files stops (free plan 20,000).
- Measured: daily run ~4 min; refresh 63 min; median page 19 KB gz. Live gate scales to ~17 min at 2,000 pages: re-measure at 500.

## What can break
- FEMA down or renamed: refresh stops, last month stays. FEMA hosts refuse the laptop (outside US): use the US runner.
- Law page moves: recheck stops the release; re-point the rule. Manual reads older than 183 days stop the release (`state/manual-rule-read.json`).
- A 25% median jump stops the refresh. A live county drifting past 2x a reviewed example stops the release (S12): one own light review.
- January: year ranges, "since 1978", decade labels roll over; check one page.
- IndexNow returns 403 on most sends: notice only, not a blocker.

## Owner only
FIRST: Bing Webmaster Tools, import the site from Google Search Console (2 minutes; unblocks IndexNow and ChatGPT's source). corrections/contact address; publisher identity; link outreach (claims page to reporters: Houston Chronicle, Houston Public Media, Texas Tribune, ProPublica, Floodlight, Inside Climate News); Keyword Planner seeds not yet in the file (condo, deductible, LOMA, elevation certificate, claim denied); GitHub failed-run email setting; ads and paid referrals stay off until their checks.
