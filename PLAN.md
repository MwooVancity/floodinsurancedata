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
- 11-12 ORIGINALITY (owner: "I need originality info gain"; full crawl 399 pages: county pages 4,138 words median but 12% sentences their own, 82% on 20+ pages). Lesson from slabcalc.co: no per-city template pages; original value = derived national indexes nobody publishes (freeze-thaw, soil risk, cost index: key findings, "why the surprise", as-of date, method), pitched as press pieces + embeddable widgets. Build: (1) Flood Insurance Price Gap Index page = 329 counties ranked by share of single-family primary-home premiums below FEMA's full-risk premium (counties.csv fields, already gated per page), key findings, method, CSV; each county page gets its own rank sentence (unique per-place fact). (2) Then claims-payout and repeat-flood indexes the same way. Outside review 11-12 also: privacy said "no ads" (fixed, adsense_check guards it); Palm Beach 10,000 claims verified exact against FEMA (50,523 Pinellas also exact); moving shared county paragraphs to one page = owner's call (cutting a block).
  SCALE (owner 11-12: "not a handful, a fuckton"): slabcalc.co = 368 pages: 173 guides (one question each, ~1,150 words, table), 118 glossary, 44 calculators, 17 diagnose, 4 research indexes; zero place templates. Ours: (a) indexes: price gap, claim payout, repeat floods, oldest maps, take-up after declarations, deductibles chosen; (b) guides, one searched question each, answered only by rule() quotes + our national/state tables (topic list from GSC queries + People-also-ask; KWP generic list has only ~20 with demand); (c) glossary = FEMA definitions quoted raw; (d) tools under the reader-tools standard. Each new type joins linkcheck.HUBS; county pages link the guide that answers each moved paragraph. Owner OK 11-12: move shared county paragraphs to one page, one line + link each.
## Research papers (owner 11-12: "max info gain, plan it")
Each at /flood-insurance/<name>/: definition, method, 3 computed findings, "why it surprises" (data only), full ranked table (ties share a rank), CSV in /data/, as-of, rank line on every county page (data-m tagged), embed badge later, press draft in state/outreach (owner sends). Machinery: ONE spec table in build_site.py (key, field path, base, pool min, sort direction, label) driving page + CSV + county line; ONE generic tools/index_check.py recompute + mutations; refactor Price Gap into it when paper 2 lands. Hub /research/ lists all papers (joins linkcheck.HUBS; home + state link it).
| # | Paper | Field (data/c/<slug>) | Base, pool | Status |
| 1 | Price Gap | agg policies.share_below / below_n | SF primary-home priced both ways, 30+ | built 11-12, gates running |
| 2 | Claim Payout | data claims_extra.cwop_share, paid_n, claims | claims excl. 98/99, 100+ | next |
| 3 | Outside the Zone | data claims_extra.outside_sfha_pct | claims with a zone, 100+ | next |
| 4 | Underinsured | extras claims.damage_over_coverage_pct / damage_n; policies.at_building_max_pct | claims with damage recorded, 100+ | then |
| 5 | Repeat Flood | data multiloss.total, srl per 1,000 policy units | units 1,000+ | then |
| 6 | Protection Gap | data penetration.overall_pct, sfha_pct + agg nri rating | FEMA penetration rows | then |
| 7 | Flood Calendar | data claims_extra.loss_months | claims 100+; peak month per county | then |
| 8 | Deductible Choice | extras policies.deductibles | SF policies, 30+ | then |
| 9 | Community Discount | data crs list | NFIP communities in county | then |
| 10 | Flood Map Age | map-status data (verify field first) | counties with a map date | then |
Cut: "After the Disaster" (no historical policy counts: would need a guess). Storm events stay cut (card_spec).
### Paper standard (owner 11-12: "PubMed worthy", every paper, no exceptions)
National data only: pool = every U.S. county in data/all-counties (3,027) meeting the paper's minimum, never just counties with a page here.
Page sections, in order, each required (tools/paper_check.py fails a page missing one): Abstract (question, data, n, main result, one sentence each) / Data (dataset, version, FEMA field names, as-of, retrieved) / Methods (inclusion rule, exclusions with counts, base, statistic, tie rule, minimum n and why) / Results (3 findings, each with n and the exact figure) / Full table + CSV / Limitations (what the data cannot say, biases: county coded on the policy, missing fields, small-n) / Reproduce (CSV columns, the filter in words, FEMA API link per dataset) / How to cite (title, site, as-of, URL) / Changelog (as-of per version).
Statistics: report n beside every share; no rank shown for n under the minimum; no claim of cause ("why") unless a quoted official source states it; differences called "higher/lower", never "significant" (no test run); medians named as medians.
Checks before ship (all must pass): build gates, index_check recompute from raw files with zero shared code + mutations, paper_check sections + mutations, hub_words, site factory case (empty, one row, all tied, huge), phone budget, S16 links, recheck of any quoted rule, then a FULL hater review of each new paper (owner-approved cost ~80k each) plus one adversarial methods reviewer agent ("find the flaw a statistician would") on the first paper of each kind. A FAIL is fixed at the source and re-reviewed on that page only.
"Only published here": a search the same day; claim dropped if anyone publishes the same ranking.
Methods review 162 (11-12, hostile statistician, state/reviews/methods-review-162.md): Price Gap MAJOR REVISION, Outside the Zone REJECT; both off (papers.READY empty) until fixed. Rules learned, now part of the standard:
- ORIGINALITY SEARCH IS STEP 1, before any code (Price Gap already published by Neptune Flood "$2.6+ Billion That Remains" incl. counties, and GAO-23-105977 county tool). A paper that exists elsewhere ships only with a "Prior work" section reconciling numbers (Collier 82.2% here vs Neptune 76.8%) and a real difference (newer data, every county, CSV, like-for-like premium base).
- No bare ranks: show the share with its 90% interval (Wilson) and bands; 75-81% of rows were tied, top ranks spanned 2nd-26th.
- Numerator, denominator and n are the SAME base (Outside the Zone used dollars over zoned claims but n = all paid claims).
- Materiality: report the median gap among those below (below_gap_median exists); 71 counties under $50/yr.
- Quote FEMA's data-dictionary definition of every field the measure rests on (fullRiskPremium: raw read).
- Report the pooled national figure and the excluded counties' median beside the county median (selection bias: 33.6% excluded vs 24.6% ranked).
- Records vs policyCount: verify single-family records carry policyCount 1 (API filter) or sum policyCount.
- Pooled multi-decade claims: restrict to a stated window (e.g. last 10 loss years) and exclude zone D / pre-1986 B,C or report them apart; say dollars are not inflation-adjusted.
- Reproduce section lists exact field filters and values, record counts in and out, pull date.
Originality search 11-12 (step 1, WebSearch): ORIGINAL (nothing found) = Underinsured (damage over coverage by county), Flood Calendar (claims by month by county), Deductible Choice (state/county). EXISTS = Repeat Flood (NRDC "Losing Ground" county tool, data to 2022), Map Age (unvetted personal project, nationalflooddata commercial), Price Gap (Neptune, GAO). CUT = Protection Gap (FEMA publishes the rates itself). New order: Underinsured, Flood Calendar, Deductible Choice, then Price Gap revised, Map Age, Repeat Flood (each with Prior work), Outside the Zone after its cloud field.
Gates to add before the next paper (methods review caught what gates could not): G1 same base: each spec declares numerator/denominator/n fields and the base sentence; index_check fails when n is not the denominator's count field (Outside the Zone: paid_n vs zoned dollars). G2 no bare rank: a paper page or county line printing a rank without the share's 90% interval fails. G3 site factory with papers on: missing_state, state_not_built, claims_by_zone_empty failed on the 11-12 run (with papers on, overlapping build) - rerun alone, fix in papers section.
Outside the Zone needs a cloud field: zoned_paid_n (claims with a rated zone and a payment) per county, per window.

### Harm cases (owner 11-12: how a paper hurts us; each guard needs a test before the paper ships)
H1 viral wrong number: methods review + versioned URL + public corrections log. H2 "worst county" backlash/property value (Zillow-First Street 2025): no best/worst words, intervals not bare ranks, neutral titles. H3 re-identification: min n on every figure, no claim-level extremes. H4 press misread: base in the same sentence + "how to quote this" line. H5 stale citation: each version at /flood-insurance/<paper>/<asof>/, "cite this version". H6 anonymous research: never "peer reviewed"; say "reviewed by AI agents and recomputed"; publisher identity = owner. H7 scaled look: each paper its own question + findings; generic findings = not shipped. H8 table-heavy: abstract + findings first, table below, CSV for the rest. H9 cannibalizing county/claims pages: one target query per paper, county pages link not copy. H10 copying: Prior work section names Neptune/GAO/NRDC. H11 disaster timing: no press push within 14 days of a new flood declaration in a top-ranked county. H12 FEMA endorsement: required OpenFEMA line on every paper. H13 one paper breaks deploy: paper auto-off (READY), rest ships. H14 upkeep: 0 impressions and 0 links after 90 days = cut. H15 causation: no "why" without a quoted official source. H16 rank churn: ranks frozen at monthly refresh.

### Edge cases (written before code; each: how it breaks / where at full size / test that fails without the guard)
Input
- E1 Field null or missing in one county (old pull lacks it): row crashes build or prints "None%" / any paper, 1,803 counties after widening / index_check "null row shown" mutation; rule: left out, counted in method line "N counties without this field".
- E2 Field stored as text ("20%") or 0-100 vs 0-1 scale: rank inverted or 100x / penetration, deductibles / check parses both and fails on value >100 or <0.
- E3 Mixed as-of dates across counties (half refreshed): ranks compare different months / every paper during a monthly refresh / check fails if >1 distinct asof in pool.
- E4 Ties (Price Gap already has 10 tied values): same share, different ranks = mislabel / 30+ ties at 3,000 counties / check: equal values must share rank, next rank skips; page prints "(tied)".
- E5 Tiny base (7 claims, Tooele): 100% or 0% tops the list / Payout, Outside, Underinsured / pool minimum per paper (100 claims, 30 policies), check fails on any row under it.
- E6 Rate per units with units 0 or tiny: divide by zero or 5,000 per 1,000 / Repeat Flood / pool units 1,000+, check recomputes ratio.
- E7 Same county name in two states (Washington Co. x30): wrong link or merged row / every table / rows keyed by slug, state shown on every row; check on duplicate slugs.
- E8 Parish/borough/census-area/independent city names: label "County" added wrongly / LA, AK, VA / use places.json "short" as is; test_site_factory case.
Missing
- E9 Pool under 50 counties (first run, failed refresh): page with 12 rows = thin page / any paper / no page built, no county lines, hub omits it; site factory case.
- E10 A county page fails its gate and is removed: index links a dead page / any day / pool = places that passed this build; linkcheck S16 catches broken link.
- E11 FEMA drops or renames a field: whole paper silently empty / any refresh / E9 rule plus a release notice line "paper X off: field missing".
Scale
- E12 3,000-row table on a phone: 400+ KB page / after widening / table shows top/bottom 25 + state filter is NOT a fix (JS); full table only in CSV beyond 500 rows; phone_check byte budget fails first.
- E13 County build reads every county's JSON per page (n squared): 329x329 ok, 3,000x3,000 = 9M reads / after widening / build_counties computes ranks once, pages read one small file; build time measured in release step timer.
- E14 10 papers x rank line each: county page grows 10 lines, screen 1 pushed / P8 phone check / lines go in one "How this county ranks" card below screen 2, never screen 1; P8 must still pass.
Two writers, two copies
- E15 Rank computed twice (build_page and build_site) drifts: county says 5th, index says 6th / any paper / index_check compares every county line to the index table (built for Price Gap).
- E16 Pool rule typed in two places (30 in build_site, 30 in build_page): one changes / any / single spec table imported by both; check reads the same constant.
- E17 Daily publish adds counties: every rank on every county page shifts, 329 pages change daily, fake freshness in sitemap / daily / lastmod moves only when a page's own data changes, not its rank (lastmod.py rule + test).
Who can't see it
- E18 New hub /research/ not in linkcheck.HUBS: orphan papers / day 1 / S16 fails unless added.
- E19 State pages have no line: S16 "hub linked from under half" / day 1 / state page gets "Highest-ranked county in this state" line per paper.
- E20 hater review prompt never reads index pages (national page type): label errors ship / every paper / add each paper to S12 sample list.
The check itself is wrong
- E21 Regex in index_check too loose (matches any table): passes a broken page / any / mutation "row dropped", "share changed", "rank wrong" must fail (3 built).
- E22 Recompute shares code with the builder: both wrong together / any / index_check reads data files only, never imports build_site.
Readers and Google
- E23 Reader reads rank 1 as "best" when it means "most below full-risk" / every paper / direction sentence next to every rank; hater checklist item.
- E24 "Claim Payout" read as denial rate: "denied" banned (Never in copy); unpaid = "no recorded payment", reasons table linked.
- E25 Outside-the-Zone read as "zone X is risky": base is claims, not homes; sentence names base "of NFIP claims here, not of homes".
- E26 Underinsured: damage over coverage limit is not "uninsured loss" for contents/deductible; label exactly FEMA field meaning, data dictionary quote.
- E27 Protection Gap uses FEMA penetration (residential contracts / housing units, FEMA's own estimate) at a different as-of than policies: both dates printed.
- E28 Ten near-identical paper pages = scaled content: each paper gets its own findings and why-section computed from its data; a paper whose 3 findings are not distinct is not shipped.
- E29 Press claim "only published here": must be checked by a search the same day; else drop the claim.
Unattended
- E30 Monthly refresh changes a top-3 county: findings text stale / monthly / findings computed at build, never typed; sameness of findings to last build logged.
- E31 A paper breaks for a week and nobody sees: release fails closed on index_check; doctor reports at session start.
Done = page live, index_check PASS + mutations, county lines on every live county, sitemap, hub link, light review PASS. Then widen refresh-data.yml to all ~3,000 counties so papers rank the whole US.
  Edge cases: county with null share (left out and counted in the method line); ties (same rank, "tied"); rank sentence must name base and pool ("of 329 counties with 30+ priced policies"); index never called a forecast or premium rise.
- 11-12 owner applied to AdSense; ownership verified. Owner 11-12 "add it like riverwaterlevels": meta tag + AdSense code snippet in every <head> + /ads.txt live (tools/adsense_check.py, 5 mutations, in release; fails on a hand-placed ad unit; auto ads stay off in the account). contact@floodinsurancedata.com routes to owner Gmail (Cloudflare Email Routing rule active); owner clicks "Add missing records" (MX/SPF/DKIM), then Claude puts it on /methodology/ + About and owner clicks Request review. "No ads before a 4-week Search Console review" still governs ad units. FloodSmart reworded its renters text 11-12: renters_cover/limits excerpts re-read and updated.
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
- 12-04: 30+ impressions on "flood zone/map" queries, else restore old titles. Same day: titles (median 91 chars, research said 60-70) and descriptions (median 295, ~155 shown) shortened, keeping town name and base label; held until then so the title test reads clean.
- GSC 11-12 (28 d to 11-10): 13 clicks, 1,430 impr, pos 41.7. Indexed 329. Crawled-not-indexed 215 = 177 CSVs + 36 https county pages (12% of 292; research kill line 25%) + /nfip/. Noindex 163 = CSVs (intended).
- 01-04: unfreeze zero-demand counties only if 5+ county pages have US non-brand impressions, 3+ in top 30, 1+ US click.
- 01-08 zone pages position 15 or better; 01-29 /flood-zone-map/ 200+ impressions; 02-01 claims page 1+ referring domain or 100+ impressions; 02-03 continue / consolidate / stop.

## Runs on its own
Daily `publish-counties.yml` (20 counties, gates, deploy via deploy.yml, live gate); monthly `refresh-data.yml` (skips in ~20 s when current; at most one forced refresh per batch of new fields); `map-status.yml`; nightly `watch.yml`. Rollback drill passed 11-11 (run 43090849533). Failed job: a note on its run page; Claude reads failed runs every session start.

## Never in copy
That FEMA data shows open vs closed claims; "denied"; a period or base left out; a promise of AI citations; IndexNow as proof of indexing.

## Owner only
By 11-17: corrections/contact address, then send wave 1; `gh auth refresh -s user` so Claude can read Actions billing. 11-26: publisher identity, Keyword Planner seeds (condo, deductible, LOMA, elevation certificate, claim denied), GitHub failed-run email setting, ads decision. Referral licensing + FTC check when sessions pass 5,000 a month (reviewed 02-03).
