# PLAN: floodinsurancedata.com
State, dated numbers, next moves, owner-only items. Rules: CLAUDE.md. History: git (a DONE line is deleted, not kept). Cap ~8 KB.

## Goal and scoreboard
Most helpful flood-insurance page for every US place a homeowner or buyer searches, on a phone. Scoreboard: pages indexed, impressions, clicks, page-1 queries, AI citations. Polish only where a number says a page fails.
- Search Console 28 days to 11-06: 5 clicks, 872 impressions, 225 pages and 235 queries seen, avg position 39.5. Best: Brevard pos 8.2 (41 impr, 1 click), New London CT pos 2 (2 clicks), Florida state pos 25.9, zone X 83, zone AE 75; /flood-zone-map/ not yet in the top 10 pages by impressions.
- GA4 11-01..08: 7 real visitors (13 more were our nightly test, filtered since 11-08): 4 from ChatGPT (no query passed, so no keywords), 3 organic, all engaged. GA4 28 days to 11-08: 4 organic + 4 ChatGPT sessions, all engaged (Santa Clara 2m14s, Elkhart, Brevard, Dallas ~50s). Bing Webmaster Tools verified by the owner 11-09: 0 impressions, 0 AI citations; sitemap submitted 11-09 (Processing); IndexNow still 403 "UserForbiddedToAccessSite" right after verification (key file serves 200 to bingbot), recheck 11-15. llms.txt labelled 11-08 (test_site_factory checks it).
- Index 11-06: home, 51/51 states, 204/232 counties, 6/7 zones indexed; our canonical kept everywhere. Low rank = age and no links, not a technical block.
- Search Console 28 days to 11-08: 7 clicks, 1,130 impressions, position 41.8, 295 queries. By group: town/city 170 queries 386 impr; zone/map 67/99; cost 46/82; claims 11/34 ("flood damage claims maryland/bethesda/baltimore", answered by the 11-10 claims-by-county table); NFIP 1/4. Top: flood insurance massachusetts 22, florida 21, maine 13, grand forks 11.
- Indexing to 11-05: 344 indexed, 892 not: 434 http/www copies, 126+154 data.csv, 177 crawled-not-indexed (~152 csv, ~20 county pages). 11-11 http/www now 301 to https apex (Cloudflare: Always Use HTTPS + 1 redirect rule); 11-26 checkpoint: http/www and csv rows should be falling; judge county indexing only on https HTML rows.

## Live now (11-09)
- ~343 live pages: home, 51 states, ~280 counties, 7 zone pages, /flood-zone-map/ (address tool), /nfip/, renters, claims (+CSV), ZIP lookup, methodology. Address and start-date tools on 3 samples (`tools/tools_flags.json`). Data as of 08-31 (FEMA bulk files).

## Money order (owner 11-07: money groups first, counties last)
Keyword Planner volume x top bid: state insurance $190k, map $90k, towns $47k, zones $37k, cost $37k, NFIP $36k, state map $25k, renters $18k, county map $15.5k. Not targeted: head term "flood insurance" (FloodSmart), quote and companies (forbidden). Every money page is live; counties now run 20 a day, queue "kw" > 0 only (~1,200 zero-demand counties wait for the Jan 4 rule).

## Revenue target (owner 11-09): $1,500 a month by 2027-11
- Math (third-party estimates, searched 11-09, not our data): US finance/insurance page RPM $15-40 (weforads, organicarbitrage). At $30, $1,500 = ~50,000 pageviews a month. Today: 5 Search Console clicks in 28 days. Gap ~1,000x; links are the lever (patent note below), and links wait on the owner's contact address.
- Ad networks (secondary sources, recheck the official page before applying): Mediavine Journey from 1,000 sessions a month; Raptive from 25,000 pageviews. Ezoic now wants 250,000+.
- Traffic milestones (GA4 pageviews a month): 2027-02 2,000; 2027-05 8,000; 2027-08 20,000; 2027-11 50,000. Two misses in a row: re-plan (new keyword group or page type), not more of the same.
- Money switches, owner only: ads after the 11-26 review, when sessions pass 1,000 a month (one slot below screen 1, phone bytes measured); paid referrals only after the licensing + FTC check, done when sessions pass 5,000 a month (at today's traffic a referral earns ~0).

## Next, in order
2. WAITING 11-15: weekly Search Console + GA4 read (bot-free GA from 11-08).
3. WAITING 11-17 (2 weeks on samples since 11-03; address tool samples since 11-06): 11-18 start-date tool "all"; 11-20 address tool "all" after 7 green nightly live tests (watch.yml; a FEMA outage fails safe, as on 11-08).
4. WAITING 12-12: did Congress extend the NFIP past 2026-12-11? During a lapse set `start` to [].
5. WAITING 12-09: Top-3 compare (owner 11-09, ONLY GOAL): every keyword group's Google top 3 vs our page; each real gap built or decided. Monthly: next 12-09. Run 11-09 built: claim limits on home; lowest-floor law (60.3(c)(2)) on AE/AH; 50% rule on high-risk zone pages (rewritten from raw 59.1 + SFIP D, live on every county); claims page: ten costliest loss years + claim-size range by state (claims_check C6-C8); ZIP result shows the county median beside the ZIP's; second batch LIVE 11-09: U.S. median paid building claim ($12,384, 1,968,497 claims; claims_check C7b), county note on claims rated outside zones A/V (236 counties, loss years 2016-2025), rate-rise cap on home, "NFIP sold only in participating communities" on renters, floodway rule on AE (review 126 PASS; zone X 30-year odds deleted: shaded X also holds some 1% areas, FEMA gives no odds). Decided, not printed: evacuation vs flood zone (Florida's official page calls evacuation zones flood zones: sources disagree); renters "landlord policy does not cover your things" (not in FloodSmart's raw text); ZIP-level preliminary-map compare (FEMA's tool, address-level); county "draft maps out" line (11-09 probe: FEMA's Prelim_NFHL service lists 0 panels for Harris County although FEMA issued Harris drafts in Feb 2026, and still lists 2014 Hawaii drafts and 1899 placeholder dates, so neither "none" nor "yes" is reliable; pages keep the general preliminary-map note + FEMA link).
6. Audit 11-10 (3 fresh auditors + Lighthouse/W3C/linkinator) batch 2, in order: screen 1 at 390x844 shows only 3 of 6 answers on 5 random counties (drop the opening sentence the tile repeats, Q&A above tiles; F1/P4 first); gate.py word rules on hub pages; .git 230 MB in 19 days from committing dist (deploy from CI build); daily build ~5 min whatever changed (gate only changed pages; ~30 min at 2,050); runner minutes (measured 11-10: scheduled refresh skips in ~20 s; the cost is ~17 manual forced refreshes in November at ~62 min each on a PRIVATE repo, 2,000 free min; rule from 11-10: at most one forced refresh per batch of new aggregation fields, else they wait for the monthly run; billing read needs the owner's `gh auth refresh -s user`, owner by 11-17); release.py deploys locally and via deploy.yml (drop the local wrangler); November rollback drill; ZIP floor 25 vs 30; src() repeats; review 132 MINORs: by-county total (2,567,024) vs home 2,680,429 needs the no-county line, the two left-out counts differ without a reason, Texas notice has more exemptions than "shorter than 30 days" (say "some leases are exempt, including"), retrieved date prints the UTC day (stamp in US time). Batch 1 shipped 11-10: claims-by-county table (C12), error-code label (C8b, N5), S2/S13 notices only, decade/zone screen-1 labels, double date, Texas tenant notice, Harris MAAPnext, favicon, sitemap lastmod (tools/lastmod.py), claims_check names/headers/years (34 mutations). Decided: renters living-expenses line exists (not_covered); unmapped-area line not built (no FEMA text a script can read).
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
- News stories 11-10 (report `reports/Viral flood data story ideas.md`), on /flood-insurance/claims/ + `/data/claims-stories-counties.csv`, claims_check C9-C11 (rows, rank, range, left-out, CSV; mutations), factory story_edges: all three LIVE 11-10 (2016-2025 losses, 500+ claims per county): #outside 130 counties, 0.5% Levy FL to 89.3% Cameron TX; #cause 111 counties, rain/snowmelt 9.3% Plymouth MA to 88.2% Hudson NJ; #moved 42 counties, rated outside A/V now listed in A/V 0.3% Hidalgo TX to 67.6% Collier FL (reviews 128, 129 PASS). Pitch figures ready for the data-desk wave. Decided, not built: grants vs NFIP per storm (claims link to a disaster only via eventDesignationNumber from 2020; a name match guesses); policies lost since 2021 (FEMA disputes the cause; snapshot counts); "deepest floods" (waterDepth units mixed); premiums vs claims (years don't match); blended "worst county" scores. Need every county first (data/c holds 1,040, map_status 293): lowest take-up among flood-declared counties, repeat-flood ranking, oldest-maps ranking.
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
Dated 11-10 (audit: an owner blocker with no date stalls the money path). By 11-17: corrections/contact address (anonymous Gmail, then Cloudflare Email Routing); every pitch waits on it. By 11-17: send wave 1 (claims page to reporters: Houston Chronicle, Houston Public Media, Texas Tribune, ProPublica, Floodlight, Inside Climate News). 11-26 (with the audit): publisher identity stays anonymous or not; Keyword Planner seeds (condo, deductible, LOMA, elevation certificate, claim denied); GitHub failed-run email setting. Ads: decided at the 11-26 review, on only above 1,000 sessions a month. Referral licensing + FTC check: start when sessions pass 5,000 a month, reviewed 02-03 whatever the number.
