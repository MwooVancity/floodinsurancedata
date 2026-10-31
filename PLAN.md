# PLAN: floodinsurancedata.com
State and next moves only; rules in CLAUDE.md, history in git. Under 80 lines: done = delete.

## Goal and scoreboard
Most helpful flood-insurance page for every US county, for a scared reader on a phone. Measure: pages indexed, impressions, clicks, page-1 queries, AI citations. We built before proving demand: the weekly scoreboard decides; polish only where a number says a page fails.
2026-10-29 Search Console (data 10-23..27): 101 impressions, 1 click, position 46; sitemap 110 read, 0 errors. Read: `tools/gsc_read.mjs`.

## Who uses it (audit 2026-10-31; small sample, keyword volumes not measured)
Known: 271 impressions, 3 clicks, position 44, 7 days; all 3 clicks from Canada (guess: the owner). No proven outside reader. 79% of impressions desktop, so "on a phone" is unproven. About two thirds of 182 query impressions are "flood insurance <place>", many towns we have no page for; cost words 29, zones 18, claims 4, condo 3. Why it may fail: new anonymous site, no links, position 44.
Search results: zone queries are led by spam pages and insurers with conflicting prices; claim appeals by FEMA; map changes by scattered local government pages; condos by forums and agents. Canada: no public flood price data and no national program, so dropped. County averages exist elsewhere but are state-level or stale.
Try in order, each smallest test first, 4 weeks of Search Console before more:
1. Zone pages: 3 national pages (AE, X, VE), NFIP median by zone, claims, what it means. Not a page per place.
2. Towns: county pages name their main towns from Census, in a sentence, no lists; test on 20 counties.
3. "Claim denied": one page, deadlines via `rule()`, why claims closed unpaid from NFIP data.
4. Condo: one sourced page; check NFIP condo figures first.
5. "Get out of a flood zone": one page, LOMA steps via `rule()`, lender can still require it.
Rules tested: truth, no advice, 2,000 ceiling, no name-swap pages stay. Open: county-only pages (habit). Procedures from official sources are facts, not advice. Hold compare and decode-policy tools until a test shows demand. Dropped: Canada, embed, alerts. Owner: anonymity may cost trust on an insurance topic.

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
7. Pace: 20 a day. After 4 weeks of data (11-26): 25 if most pages indexed, 10 if not, stop if impressions fall. Write the decision here.

## Runs without Claude (subscription ends about 2026-11-19)
A failed check ships nothing; the live site stays. Failed job = one issue "Job failed: <job>" (`tools/job_alert.sh`). Daily and monthly watch each other (3 and 40 days). Group site-deploy: one deploy at a time; deploy.yml uses latest master.
- After deploy every live page must equal what passed, else previous release redeploys (`tools/deploy_verified.sh`). Idle days check too and redeploy once. Over 19,000 files stops (free plan 20,000).
- Pinned: ubuntu-26.04, wrangler 4.86.0, playwright 1.64.1, Python 3.12, Node 20.
- Warnings on the daily run: Cloudflare token (30 days), domain (45 days; expires 2027-10-23) via `tools/token_check.py`.
- Refresh side sources cannot stop it; sea level keeps the file on a short answer; cache saves after download. Unreachable law page warns, fails after 14 days (`state/rule-fetch-ok.json`). Missing browser fails in cloud.
Owner only after 11-19: domain card; renew Cloudflare token; a moved law page (release stays stopped, re-point the rule); a 25% median jump stops the refresh (old data stays); a retired runner (one line).

## What can break
- FEMA down or renamed: pull_raw stops; last month stays, as-of ages. State count mismatch: full re-pull, else refresh stops.
- Claims cache evicted (10 GB): one slow full pull. Refresh 2.3 h/month.
- Rule pages change: recheck.py stops on a missing excerpt.
- Big storm: no code change; check the events lead that week.
- NFIP lapse (deadlines often Sep 30): OPEN, add a sourced "no new policies during a lapse" rule that day.
- January: year ranges, "since 1978", decade labels roll over; check one page.
- Flagged queue: 183 of 1,803. 31 extreme ones need own looks; script numbers, one cheap review per flag type.
- Before ZIP pages: verify files per deploy (3 a page).

## Calendar
Weekly Search Console. Monthly: refresh time, git size, prune backlog. Quarterly: light review on samples. Yearly: domain, NRI and CSB updates.
11-03 refresh -> 11-12 planner to all -> 11-19 subscription ends -> 11-26 pace decision -> late January queue done -> decide ZIP pages and AdSense.

## Open checklist and parked
Open: B audience lines; F state contacts; G table search; I error-report contact (owner); K print; L Spanish. Parked: ZIP pages, Spanish, print, AdSense.
