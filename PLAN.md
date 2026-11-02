# PLAN: floodinsurancedata.com
State and next moves only; rules in CLAUDE.md, history in git. Under 80 lines: done = delete.

## Goal and scoreboard
Most helpful flood-insurance page for every US county, for a scared reader on a phone. Measure: pages indexed, impressions, clicks, page-1 queries, AI citations. We built before proving demand: the weekly scoreboard decides; polish only where a number says a page fails.
2026-10-29 Search Console (data 10-23..27): 101 impressions, 1 click, position 46; sitemap 110 read, 0 errors. Read: `tools/gsc_read.mjs`.

## Who uses it (audit 2026-10-31; small sample, keyword volumes not measured)
Known: 271 impressions, 3 clicks, position 44, 7 days; all 3 clicks from Canada (guess: the owner). No proven outside reader. 79% of impressions desktop, so "on a phone" is unproven. About two thirds of 182 query impressions are "flood insurance <place>", many towns we have no page for; cost words 29, zones 18, claims 4, condo 3. Why it may fail: new anonymous site, no links, position 44.
Search results: zone queries are led by spam pages and insurers with conflicting prices; claim appeals by FEMA; map changes by scattered local government pages; condos by forums and agents. Canada: no public flood price data and no national program, so dropped. County averages exist elsewhere but are state-level or stale.
Full audit 10-31 tested the pages. Done 11-01: lapse line (`nfip_lapse`, covered card, no dates), outside-zone claim share (required card, 1,727 of 1,803 queued; gate L19; under 10 paid claims = no line), renters and businesses line in cost card, methodology Eight confirmed (NOAA counts). Open: error-report route (owner picks address); no statement that the median excludes contents-only or mobile homes, because the filter does not prove it; check FEMA's occupancy codes before saying more. Condo note now says the single-family figures have no separate condo filter; at the next refresh count cohort rows with condo code U in the cloud, then state it or filter them. Done 10-31: all 1,803 queued pass today's gate (671 had failed on missing zone-code text; would have stopped publishing about 11-15); `add_counties.py` fails loudly on a stall. A county failing after a refresh still stops that day's release and alerts. Before any template change: `build_counties.py --all`, then delete review/. Also: territories never pulled; methodology says Eight, rule says Seven; home has no ZIP box; save edge scripts as one tool, run quarterly.
Try in order, each smallest test first, 4 weeks of Search Console before more:
1. Zone pages: LIVE 11-01 at /flood-zones/ae, x, ve, linked from home and county zone tables. National median exists by zone group only; claims by exact zone are a printed gap (add to agg_raw if the pages earn impressions). Read their Search Console numbers 11-26.
2. Towns: county pages name their main towns from Census, in a sentence, no lists; test on 20 counties.
3. "Claim denied": one page, deadlines via `rule()`, why claims closed unpaid from NFIP data.
4. Condo: one sourced page; check NFIP condo figures first.
5. "Get out of a flood zone": one page, LOMA steps via `rule()`, lender can still require it.
Rules tested: truth, no advice, 2,000 ceiling, no name-swap pages stay. Open: county-only pages (habit). Procedures from official sources are facts, not advice. Held until a number asks: claim-denied, condo, get-out-of-zone pages, compare and decode tools, table search, glossary, `data-p`. Town names (test 2) run first. Dropped: Canada, embed, alerts. Owner: anonymity may cost trust on an insurance topic.

## State (2026-10-30)
- Live: 151 pages, sitemap 150 (home, 51 states, 92 counties, site pages). Queue 1,803; daily job adds 20 reviewed (25 max a release); done about late January 2027.
- Data as of 2026-07-31; refresh on the 3rd (claims carry over, last 3 loss years re-pulled).
- Analytics: GA4 property 561730563, `G-EXCYW0PJYG`, account 163330170; `notes.GA_TAG`, real host only; google_gate S15.
- Proven in real cloud runs: daily publish unattended; fail, idle, rollback drills; first full refresh (10-31 00:06 UTC, jump check PASS).
- Measured: daily run 249 s (build + checks 33%, deploy + live gate 31%, phone 20%, add counties 10%); limit 45 min; leave it. Live gate 78 s at 151 pages, about 17 min at 2,000 (scaled; re-measure at 500; then changed pages + a sample). Build unchanged 7 s (`tools/fingerprint.py`).
- Bytes (gzip): median page 19 KB, largest 29 KB, Palm Beach 21.7 KB. Google script 182 KB, async. `data-p` tags 2.8 KB a page, no reader use. Structured data 0.9 KB: keep. Disk (dist 20 MB, data 104 MB, git 68 MB) costs no reader.
- Pipeline audit 10-31: tokens are the bottleneck (a full review ~320k, 34 rounds so far; machine time is nearly free). Actions month: refresh 139 min (download 60, compute 78), daily ~4 min, deploy 38 s; private repo, 2,000 free minutes; about 850 at 2,000 pages (scaled). Cloud failures stopped by checks: law page, phone height + mutation.
- Bottlenecks: tokens per change, pages indexed.

## Next, in order
0. Bytes: strip `data-p` after gates, keeping the live gate's comparison right. Decide delaying the Google script (saves 182 KB on quick visits, undercounts them).
1. Weekly Search Console. Owner: "Validate fix" on the Datasets report.
2. 11-03 refresh: record time, download size, 51 states done; note whether FEMA's data changed since 10-31 (if months repeat, check FEMA's dataset date first and skip the 2.3 h). Issue #1 closes on the next daily publish.
3. After 2, one batch, one light check (≤ ~90k tokens):
   - #3 claims by flood zone and #7 claims outside high-risk zones (ChatGPT list; same FEMA data): the "Outside a high-risk zone?" line on "Am I required", worded "of paid claim dollars", with period.
   - Search boxes on tables of 16+ rows, with a "no matches" line.
   - Take-up: verify the source, show it or delete the idea.
   - Gate check + mutation for each defect class in rounds 16-19.
   - MINORs: condo "leave both out"; glide wording where the gap is tiny; Maine duplicate disaster line; "Assigned in error" vs "Claim deleted in error"; thin zones in dropdown.
   - Sourced glossary; one line each for renters, landlords, second homes, businesses; ZIP "near <place>" fallback where no place covers 25%.
4. Reader tools (CLAUDE.md standard; each gets an edge script and one light review; nothing leaves the phone, below the quote checker, readable without JS):
   - Deadline planner LIVE on 3 samples; 11-12 go "all" in `tools_flags.json` if no errors, then round-21 MINORs.
   - First try a "compare with" link opening two pages. Only if short: compare tool (published places, same level, base labelled, "too few", one lazy JSON, no "safer/cheaper").
   - Decode my policy: FEMA field names; flag monthly-for-yearly and out-of-range; premium vs median, deductible vs mix, coverage vs $250,000, zone in plain words; FEMA's pay-less text only.
   - Dropped: renewal-jump check.
5. Links, guards first: monthly dead-link check stopping a release; outside links only .gov or FloodSmart; 3-5 related links from data; link text names the destination. Add DisasterAssistance.gov, FEMA provider finder, state insurance departments (sourced 51), bordering county. Sea level on state pages (open).
6. One data story: "counties paying furthest below FEMA's full-risk price". Local-news pitch needs the owner.
7. Pace: 20 a day (owner 11-01), no pauses, no noindex holds; queue done about late January; 31 flagged counties need own looks. Watch indexed count weekly. Towns test: 20 counties in `tools_flags.json` `towns`, shipped 11-01; compare their town-name impressions with the other counties after 4 weeks; no lift = remove.

## Runs on its own (owner goes to the Pro plan about 2026-11-19; Claude stays, smaller token budget)
A failed check ships nothing; the live site stays. Failed job = one issue "Job failed: <job>" (`tools/job_alert.sh`). Timeouts and cancels alert too. `watch.yml` checks the daily job every night (alert after 2 days); daily and monthly also watch each other (3 and 40 days). Group site-deploy: one deploy at a time; deploy.yml uses latest master.
- After deploy every live page must equal what passed, else previous release redeploys (`tools/deploy_verified.sh`). Idle days check too and redeploy once. Over 19,000 files stops (free plan 20,000).
- Pinned: ubuntu-26.04, wrangler 4.86.0, playwright 1.64.1, Python 3.12, Node 20.
- Warnings on the daily run: Cloudflare token (30 days), domain (45 days; expires 2027-10-23) via `tools/token_check.py`.
- Refresh side sources cannot stop it; sea level keeps the file on a short answer; cache saves after download. Unreachable law page warns, fails after 14 days (`state/rule-fetch-ok.json`). Missing browser fails in cloud.
Short session fixes: a moved law page (release stays stopped, re-point the rule); a 25% median jump stops the refresh (old data stays); a retired runner (one line); a county failing after a refresh (no auto-skip on purpose: it could hide a wrong page). Owner: domain card; renew Cloudflare token.

## What can break
- FEMA down or renamed: pull_raw stops; last month stays, as-of ages. State count mismatch: full re-pull, else refresh stops.
- Claims cache evicted (10 GB): one slow full pull. Refresh 2.3 h/month.
- Rule pages change: recheck.py stops on a missing excerpt.
- Big storm: no code change; check the events lead that week.
- NFIP lapse: pages state the general rule, never whether one is on now.
- January: year ranges, "since 1978", decade labels roll over; check one page.
- Flagged queue: 183 of 1,803. 31 extreme ones need own looks; script numbers, one cheap review per flag type.
- Before ZIP pages: verify files per deploy (3 a page).

## Calendar
Weekly Search Console. Monthly: refresh time, git size, prune backlog. Quarterly: light review on samples. Yearly: domain, NRI and CSB updates.
11-03 refresh -> 11-12 planner to all -> 11-19 Pro plan -> late January queue done -> decide ZIP pages and AdSense.

## Reader gaps batch (11-01)
Shipped as rules: closing facts (legal minimum, 45-day force-placement, 45-day zone review, seller can assign policy and discount), what a policy won't pay (flood definition, hotel, outside items, basement, used value), NFIP appeal 60 days and suit one year, 50% substantial damage and $30,000 ICC, 26% over 30 years, lapse. Dropped: aid-stays-with-property (statute covers purchase aid; wording unproven).
After the 11-03 refresh, one batch from new fields in data: `claims_extra.loss_months` (paid dollars by month: "when floods hit here" beside the 30-day wait), `policies.below_gap_median` (typical gap among policies below full risk; the two medians hide it), `policies.contents_share` (how many carry contents cover). Each needs `metrics.py` entry, recompute from raw, 10+ paid claims floor for months. Also collected from that refresh: `policies.frp_by_zone` (full-risk median by zone, closer to a new buyer's price), `cost_by_foundation`, `cost_by_floors` (FEMA codes; label from the data dictionary before showing). Shipped 11-02: unquoted zone-review clause cut; lapse line reduced to what FEMA's 2021 manual and later guide both say (they differ on 30-90 days late; current manual not read); non-primary surcharge; Texas TWIA rule; Florida seller disclosure. Other states' disclosure laws: no official 50-state list found, left out.

## Truth holes (closed 11-02)
Closed 11-02: every rule now rests on text read raw: law (Cornell, govinfo), FloodSmart, FEMA's data dictionary, the October 2025 Flood Insurance Manual. No rule depends on a fema.gov page any more; `cap`, `glide`, `lapse_discount`, `nfip_lapse`, `substantial_damage` are PDF reads in `state/manual-rule-read.json` (183-day expiry). Edge-case audit all 15 fixed; all 1,803 eligible counties pass the gate; timeout alert proven by a real timed-out run.
Standing limits, no fix exists: T1 catches duty words only, so other typed program facts rely on review; an excerpt proves a phrase, not its meaning.
Next: after the 11-03 refresh, new figures (recompute from raw; month chart base paid dollars incl. ICC, zero-paid out; foundation codes labelled from FEMA).

## After the queue (measured 11-01)
About 1,660 reviewed counties at 20 a day: last one about 2027-01-24. Then 31 stay unpublished until reviewed: 26 have claims per policy over 5x the state's, no passing example exists, so one own review of the most extreme unlocks those up to 2x as far out; do it in January, since each template change voids it, not now. Daily job then runs idle as the watchdog (drill passed); monthly refresh keeps going.
Measured, no action: a refresh adds 1.6 MB to git, a publish 0.7 MB. Live pages near the review limit: 0; 5 queued are close. A live county drifting past 2x an example stops the release (S12) and opens an issue: short session, one own review. A county falling under the floor drops out at build and its page 404s until Google drops it: accepted. Queue is fixed: counties crossing the floor later need a yearly `--all` + `--refresh`.
Yearly by hand: re-read manual rules (`recheck.py` lists them), NRI and CSB updates, the `--all` above. January: year labels on one page.

## Open checklist and parked
Open: B audience lines; F state contacts; G table search; I error-report contact (owner); K print; L Spanish. Parked: ZIP pages, Spanish, print, AdSense.
