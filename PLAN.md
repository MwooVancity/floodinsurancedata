# PLAN: floodinsurancedata.com
State, dated numbers, next moves, owner-only items. Rules: CLAUDE.md. History: git log and state/reviews/fixlog-*.md (a DONE line is deleted). Cap 6 KB.

## Goal and scoreboard
Most helpful flood-insurance page for every US place a homeowner or buyer searches, on a phone. Scoreboard: pages indexed, impressions, clicks, page-1 queries, AI citations.
- Search Console 28 days to 11-08: 7 clicks, 1,130 impressions, position 41.8, 295 queries. Town/city 386 impr, zone/map 99, cost 82, claims 34, NFIP 4.
- Indexing to 11-05: 344 indexed, 892 not (434 http/www copies, 280 data.csv, 177 crawled-not-indexed). http/www 301 to the https apex since 11-11.
- GA4 28 days to 11-08: 4 organic + 4 ChatGPT sessions. Bing: 0 impressions; IndexNow 403 (recheck 11-15).
- Live 11-11: 363 pages (home, 51 states, 292 counties, 7 zones, map tool, /nfip/ with #rules, renters, claims + 3 CSVs, ZIP lookup, methodology). Data as of 2026-08-31.

## Revenue (owner 11-09): $1,500 a month by 2027-11
~50,000 pageviews a month at a $30 RPM (third-party estimate). Milestones (GA4 pageviews a month): 02-2027 2,000; 05 8,000; 08 20,000; 11 50,000; two misses in a row = re-plan. Links are the lever and wait on the owner's contact address. Ads only above 1,000 sessions a month; referrals only after the licensing + FTC check.

## Next, in order
3. WAITING 11-13: read the daily run's build time (map_status out of the global fingerprint 11-12: local rebuild 67 s, unchanged rerun 16 s; CI was ~340 s at 312 pages).
4. WAITING 11-15: weekly Search Console + GA4 read; IndexNow recheck.
5. WAITING 11-18/11-20: start-date tool and address tool to "all" after 7 green nightly live tests.
6. WAITING 12-09: monthly top-3 compare on every keyword group; each gap built or decided.
7. WAITING 12-12: NFIP extension past 12-11? During a lapse set `start` to [].
8. WAITING 2027-01-05: .git (241 MB on 11-11, ~12 MB/day). At 1 GB move built pages to a 'site' branch (deploy.yml, publish-counties commit and rollback, google_gate S7, lastmod.py, hater carry, indexnow, hotfix guard move with it).
Sameness (tools/sameness.py, warning only, owner 11-08): 50.0% median of sentence words shared by all 8 sample counties (11-11). What is left is headings, the question list, screen-1 answers and per-figure labels; the next move is a new per-place fact, never a cut of a reader answer.

Review cost 11-11/12 (rounds per shipped batch, ~50-110k each): batch 1 4 (132-135), rules move 3 (136-138), sources 2 (139-140), cap 2 (141-142), labels 3 (143-145), screen-1 reorder 4 (146-149), screen-1 answers 2 (150-151), screen-1 rework 2 (153-154). Screen 1 DONE 11-12, read live at 390x844: all six answers on screen 1 on 7 counties incl. Staten Island and Palm Beach; home no sideways scroll; phone_check P8 + home in release. Two of every three re-reviews caught a real label defect (r133 9999 date, r136 flooded link, r143 LOMA scope, r146 'That', r147 ZIP base). Rule: no visible-text change = `hater.py carry`, no review.

## Backlinks (Claude builds, owner sends)
- Owner first: a corrections/contact address. Drafts ready in `state/outreach/pitches.md` (waves 1-3, disaster kit).
- Assets live: claims page (claims by county, unpaid reasons, outside-zones, cause, moved; CSVs), /data/counties.csv. To build later: dated fact box on new flood declarations; oldest-map tracker; take-up among flood-declared counties, repeat-flood and oldest-map rankings (need every county pulled first).
- Lead pitch: 83.4% of 267,655 NFIP claims since 2020 had a recorded payment (52.7% Terrebonne LA to 94.4% Somerset NJ).
- Targets: local newsrooms within 48 h of a declaration; data desks (Floodlight, Inside Climate News, ProPublica, E&E); ASFPM, CRS coordinators, extension services, realtor associations, library guides.
- Numbers: 11-26 baseline; 12-15 2+ referring domains; 01-15 5+; 03-01 15+. An asset with 0 links after 15 pitches is cut. Never: paid links, PBNs, swaps.

## Checkpoints (continue or kill)
- 11-26: master audit (`docs/AUDIT-PROMPT.md`) + black-hat prompt (`docs/BLACKHAT-PROMPT.md`) + 4-week Search Console review; http/www and csv rows falling, county indexing judged on https HTML only.
- 12-04: 30+ impressions on "flood zone/map" queries, else restore old titles.
- 01-04: unfreeze zero-demand counties only if 5+ county pages have US non-brand impressions, 3+ in top 30, 1+ US click.
- 01-08 zone pages position 15 or better; 01-29 /flood-zone-map/ 200+ impressions; 02-01 claims page 1+ referring domain or 100+ impressions; 02-03 continue / consolidate / stop.

## Runs on its own
Daily `publish-counties.yml` (20 counties, gates, deploy via deploy.yml, live gate); monthly `refresh-data.yml` (skips in ~20 s when current; at most one forced refresh per batch of new fields); `map-status.yml`; nightly `watch.yml`. Rollback drill passed 11-11 (run 43090849533). Failed job: a note on its run page; Claude reads failed runs every session start.

## Never in copy
That FEMA data shows open vs closed claims; "denied"; a period or base left out; a promise of AI citations; IndexNow as proof of indexing.

## Owner only
By 11-17: corrections/contact address, then send wave 1; `gh auth refresh -s user` so Claude can read Actions billing. 11-26: publisher identity, Keyword Planner seeds (condo, deductible, LOMA, elevation certificate, claim denied), GitHub failed-run email setting, ads decision. Referral licensing + FTC check when sessions pass 5,000 a month (reviewed 02-03).
