# PLAN: floodinsurancedata.com
State, dated numbers, next moves, owner-only items. Rules: CLAUDE.md. History: git (a DONE line is deleted, not kept). Cap ~8 KB.

## Goal and scoreboard
Most helpful flood-insurance page for every US place a homeowner or buyer searches, on a phone. Scoreboard: pages indexed, impressions, clicks, page-1 queries, AI citations. Polish only where a number says a page fails.
- Search Console 10-24..11-04: 3 clicks (likely owner), position ~44-64; best query "flood insurance florida" pos 20.5. No outside reader proven yet.
- Index 11-06: home, 51/51 states, 204/232 counties, 6/7 zones indexed; our canonical kept everywhere. Low rank = age and no links, not a technical block.

## Live now (11-08)
- 323 live pages: home, 51 states, ~250 counties, 7 zone pages, /flood-zone-map/ (address tool), /nfip/, renters, claims (+CSV), ZIP lookup, methodology.
- Address tool and policy start-date tool on 3 samples (palm-beach, harris, louisiana) via `tools/tools_flags.json`.
- Screen 1 (HCU batch 11-07, r91-96): risk rating, cost in the 2 largest priced zones, CRS pay-less, regulator link, state county picker.
- Data as of 08-31 (FEMA bulk files, 63 min refresh). Forced refresh 42436345515 running: brings the condo filter (single-family figures without condo units).

## Money order (owner 11-07: money groups first, counties last)
Keyword Planner volume x top bid: state insurance $190k, map $90k, towns $47k, zones $37k, cost $37k, NFIP $36k, state map $25k, renters $18k, county map $15.5k. Not targeted: head term "flood insurance" (FloodSmart), quote and companies (forbidden). Every money page is live; counties now run 20 a day, queue "kw" > 0 only (~1,200 zero-demand counties wait for the Jan 4 rule).

## Next, in order
1. DONE 11-08: condo filter live; link audit + S16 gate (every money hub linked from ~305 pages, was /nfip/ 2, renters 1).
2. Zone pages link down to the counties with the most homes in that zone (zone pages, best #1 odds, link 0 counties today; 11-08 link audit). Then round-97 MINORs (backlog). One light review.
3. US-runner raw reads (fema-probe links job): Elevation Certificate who/where (AE page); retry the 12 NAIC-fallback regulators (AK AZ KS LA MA MI MN NH NJ RI WV WY).
4. One claims base everywhere: county payout shares drop FEMA codes 98/99 like the claims page (extras_raw + recheck, lands with the next refresh).
5. Renter tenant-flag check (does FEMA's data catch every renter policy?). County floodplain contacts: no dataset, so a printed gap line.
6. 11-18 start-date tool "all", 11-20 address tool "all", if no errors on the samples (first a US-runner live test vs real FEMA).
7. 12-12: did Congress extend the NFIP past 2026-12-11? During a lapse set `start` to [].
8. Open truth item: "policies whose term began in 2025" on an 08-31 as-of holds only Sep-Dec 2025; label the month span or drop the partial year.
9. Backlog (`state/reviews/backlog.md`): table search on 16+ rows, glossary, titles over 70 / descriptions over 160 chars if CTR is low.

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
- Pinned: ubuntu-26.04, wrangler 4.86.0, playwright 1.64.1, Python 3.12, Node 20.
- Measured: daily run ~4 min; refresh 63 min; median page 19 KB gz. Live gate scales to ~17 min at 2,000 pages: re-measure at 500.

## What can break
- FEMA down or renamed: refresh stops, last month stays. FEMA hosts refuse the laptop (outside US): use the US runner.
- Law page moves: recheck stops the release; re-point the rule. Manual reads older than 183 days stop the release (`state/manual-rule-read.json`).
- A 25% median jump stops the refresh. A live county drifting past 2x a reviewed example stops the release (S12): one own light review.
- January: year ranges, "since 1978", decade labels roll over; check one page.
- IndexNow returns 403 on most sends: notice only, not a blocker.

## Owner only
Bing Webmaster Tools sitemap; corrections/contact address; publisher identity; link outreach (claims page to reporters: Houston Chronicle, Houston Public Media, Texas Tribune, ProPublica, Floodlight, Inside Climate News); Keyword Planner seeds not yet in the file (condo, deductible, LOMA, elevation certificate, claim denied); GitHub failed-run email setting; ads and paid referrals stay off until their checks.
