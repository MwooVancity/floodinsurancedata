# PLAN: floodinsurancedata.com
State, dated numbers, next moves, owner-only items. Rules: CLAUDE.md. History: git log + state/reviews/fixlog-*.md (a DONE line is deleted, never kept here). Cap ~12 KB.

## Goal and scoreboard
Most helpful flood-insurance page for every US place a homeowner or buyer searches, on a phone. Scoreboard: pages indexed, impressions, clicks, page-1 queries, AI citations.
- GSC 28 d to 11-10: 13 clicks, 1,430 impressions, position 41.7; 329 indexed; crawled-not-indexed 215 (177 CSVs, 36 county pages = 12%, kill line 25%).
- GA4 28 d to 11-08: 4 organic + 4 ChatGPT sessions. Bing: sitemap error 11-10 ("page not accessible", 0 URLs), IndexNow 403.
- Live 11-14: 419 pages (home, 51 states, 329 counties, 7 zones, map tool, /nfip/, renters, claims, ZIP, 9 guides, 5 papers, methodology). Data as of 2026-08-31.
- Cost 11-14: one "do the rest" workflow = 2.63M tokens, 18 agents; every prose stage ended on a FAIL review. Lesson: review loops do not converge (each pass finds new style MAJORs); cap at one fix pass, owner sees the cost first for any run over ~200k.

## Revenue (owner 11-09): $1,500 a month by 2027-11
~50,000 pageviews a month at ~$30 RPM (third-party estimate). Milestones (GA4 pageviews/month): 02-2027 2,000; 05 8,000; 08 20,000; 11 50,000; two misses in a row = re-plan. Links are the lever. Ads only after the 4-week GSC review and above 1,000 sessions/month; referrals after licensing + FTC check.

## Next, in order
1. DONE 2026-11-15 (shipped 21:4x UTC) as a wrong-text hotfix (owner: "why tonight instead of now"): flood zone map titles, FEMA address lookup on every page (msc.fema.gov NFHLQuery), homeowners + SFHA label fixes, hub duty-word fixes. Read live: Pinellas + Louisiana titles, no "Half of homeowners", new SFHA sentence, lookup block, zonemap.js on msc. Two release stops first (town_check T4 title regex, hub_words W-T1/W-E2): workflow builders must run `release.py` without --ship, never a hand-picked check list.
2. DONE 11-15: prose_check --record, baseline 0 faults.
2b. WAITING 2026-11-17 00:00 UTC (next site-wide slot): ship branch worktree-wf_5a8b86cb-0ef-1 (2 guides + 11-17 batch, merged with master 357d10675). Done on it 11-15: /flood-zone-map/ card MAJOR fixed; home find-your-county box moved back to screen 1 (it was at 1142px of 844 LIVE since the cost answer moved up; new phone_check P9, old layout fails); full release checks without --ship running. Before ship: code review of the branch diff, one light review of changed pages, merge into master.
3. WAITING 2026-11-22 (weekly GSC read): guides: build the next one only when a live guide shows impressions in GSC (none have yet); queue in "Guides" below.
4. WAITING 2026-11-16 (after the template ship, so the reviewed text is final): outreach batch: editor gate (`hater.py prep --editor`), owner approves list + text, Claude sends.
5. WAITING 2026-12-01 Actions reset: Flood Map Age data pull via `tools/cloud_run.py` (one forced refresh a month, batch every queued field).

## Template batch (next site-wide release; built 11-14, uncommitted until code review, not shipped)
In it: papers prose rewrite (plain-words cards, shorter Results/Limitations, Price Gap "exact order is not reliable"); hub prose rewrite (home, /nfip/, zones, guides, methodology, about, data; long rule runs split); county template (papers card explains the five groups, 0-county state lines dropped, LOMA paragraph split, "Is it rising?" from the trend card, "52.8% of these policies pay a premium, before fees, below..."); link-only sentences removed on home and /nfip/; footer gains "Guides" (S16 caught /guides/ orphaned); new guide /guides/flood-insurance-contents-coverage/ (U.S. 81% of 2,320,412 SF primary-home policies carry contents; WV 43.8% to DC 95.3%; claims_check --guides 27 mutations).
Gates 11-14 after rebuild: build PASS, paper_gate + --test PASS, prose 0 faults (was 1,071), S16 clean, S12 needs review (template hash changed).
Open review findings to fix before ship (the rest are style, decided no):
- Done 11-15: 30-day wait exceptions split into two (mortgage, new map); contents basement rule definition first, elevated-building sentence split; TWIA spelled out (name read raw from twia.org); costliest-years note grammar (C15 phrase kept); Flood Calendar plain words lead with the median (paper_gate regex accepts "peak month held"). Gates PASS, stamp updated.
- Held, need a source quote read raw first (no unsourced definition): Elevation Certificate definition in save_ways; "Emergency Program discount" meaning in glide.
- Next batch: Damage Over Coverage top-county sentence split (paper_gate Abstract regex must change with it); "How risky?" on state pages gives the count of Very High/Relatively High counties (new tagged figure).
- Done 11-15 (code review): answer 4 is now "How has the cost changed?" with two labelled medians, no Yes/No verdict; buyer_lender rule dropped (sources did not hold it), buying guide uses purchase_answer + lender_any_zone; unsourced "Miss that..." sentence cut; typed zone meanings cut; About regains the recompute + methodology lines.
- Data check (next cloud batch): 179 of 379 places have a 2021 median of exactly $572 (63 at $633). A guess, unverified: fixed pre-Risk Rating 2.0 Preferred Risk rates make the median land on one price. Verify with the share of 2021 policies at exactly $572 before it goes in an outreach pitch.
- Decided no: restoring "if claims were independent" on county cards (the caveat lives on each paper page, paper_gate checks it there).
Owner decision: drop the second 21-item table of contents on county/state pages (cutting a block).

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
WIDE PULL 11-15 (owner "go wide"; 4 Planner searches, US, 40 seeds, 2,223 ideas: data/kwp/us-2026-11-15-1..4.csv; kwp_rank now reads every export, newest row wins): searched floor now 254,000/mo; 123,630 owned, 130,000 not. Unowned by topic: FEMA disaster aid 58,160 (mostly people looking for disasterassistance.gov: navigational, not ours; an aid-vs-insurance guide only if its top 3 are thin), floodplain/100-year flood 11,000, base flood elevation + elevation certificate 11,000, storm surge/hurricane 11,500 (mostly trip insurance: off-topic), basement water 8,420 (mostly cleanup: off-topic), "what does flood insurance cover" 7,940 (95 kw: a real gap), insurer brands 5,310 (not ours), quotes/companies 3,970 (no quotes), small rest.
GUIDES BUILT 11-15 on branch worktree-wf_5a8b86cb-0ef-1 (commit 5032f3cb8, not merged; workflow 297k tokens): (1) "what does flood insurance cover" folded into the contents guide (G1: a new page would twin it; retitled, building + not-covered cards; G6: 81% carry contents, 77% have building coverage of $250,000+, none of the top 3 gives a share); (2) /guides/100-year-floodplain/ built (G6: 62.9% of 4,529,364 policy units rated in zones A/V, DC 24.9% to NJ 85.0%; claims-outside figure dropped, Neptune already prints FEMA's one-third); (3) base flood elevation CUT (no BFE field held; lookup already on /flood-zone-map/ and zone AE page). Review: contents PASS; floodplain FAIL on the title only (fixed: "share of NFIP policy units rated in those zones"). WAITING 2026-11-16 00:00 UTC ship: merge the branch into master after it (tools/ only; release rebuilds dist), /code-review medium on its tools diff, hater round recording both guides, ship in the 11-17 UTC batch. MINORs queued: basement rule order, one "bought separately" wording, tile wording.
11-17 BATCH on the same branch (commit 95b94dbf6, workflow 371k): zone AO/AH/VE open with 44 CFR 59.1 text (X/AE/A/D already matched), home cost answer under the H1, NJ Flood Indicator Tool + Pinellas Flood Map Service sentences (Florida FDEM viewer SKIPPED: no official page names it), /flood-zone-map/ "no zone / split lot" card, renters "most homeowners and renters insurance does not cover flood" (FloodSmart). Review: zone X/AE/AO + renters PASS. Fix on the branch before merge: (1) MAJOR /flood-zone-map/ split-lot card promises an answer it does not give, 70.5/70.9 quote dense: plain lead + "how FEMA reviews a request, not how to read the pin" + LOMA guide link, or retitle; (2) owner rule: home lookup must stay on screen 1 (moved cost answer may push it down): phone_check proof; (3) MINORs: "no zone shown is not no flood risk" only if sourced; NJ anchor on "Flood Indicator Tool"; Pinellas link host = page read raw; zone X 24% period named. The "(not 81.0% of all buildings)" self-contradiction was a live template defect: fixed on master 11-15 (gate A2c, round 204), ships tonight.
New guide queue from it (each: top-3 compare + G6 figure before code; 25 new pages/day): 1 what does flood insurance cover (rules contents_*/flood_def/not_covered + our contents share and building-at-limit share); 2 floodplain / 100-year flood (FEMA definition via rule() + share of NFIP claims outside the high-risk zones); 3 base flood elevation (FEMA definition + the address lookup shows BFE at the pin); 4 FEMA disaster aid vs flood insurance (only if top 3 are thin; HousingAssistanceOwners labels per incident type read first).
11-15 earlier (narrow list): 65,930 of 70,240/mo (94%) already had a page; unowned = towns 3,050 (city pages, move 6), "flood insurance quote" 1,000 (no quotes, by design), "flood insurance companies" 100, small shared county names 100. So more traffic = ranking the owned pages (moves 1-5) + a wider keyword list: the 11-05 export came from narrow seeds. Next: one read-only Planner pull in the owner's Chrome with the GROW seed list (no saving plans, no setting changes), plus GSC queries with impressions, then rerun --map; each new unowned group goes through the top-3 compare before any page.
## Growth audit 11-15 (workflow flood-serp-gap, 2 agents, 210k tokens; top 3 for the 20 biggest searches). Top moves, in order:
1. Zone pages (x, ae, ao, a, ve, d; 7,530/mo, top 3 all insurer blogs = winnable): open with FEMA's definition via rule(), read raw: shaded vs unshaded X + old B/C, BFE + 1% annual chance for AE, AO 1-3 ft sheet flow. Next template batch (11-17 UTC). Check: claims_check zone cases + review of 1 zone page.
2. Home for "how much is flood insurance" / "flood insurance cost" (affiliate pages with conflicting averages = winnable): the cost answer first under the H1 with the county lookup, plus the existing by-zone cost table (MoneyGeek leads with zone prices). Check: phone P8 screen 1.
3. Map intent on state/county pages: link the official viewer on existing words where read raw: Florida (FDEM statewide viewer), New Jersey (NJDEP), Harris (HCFCD MAAPnext, rule harris_maapnext exists), Pinellas (pinellas.gov/flood-maps). No map drawn.
4. /flood-zone-map/: FEMA's own text on a no-result/unmapped answer and on a point vs the whole parcel; FEMA Map Service Center linked on those words. Renters: a sourced early sentence that renters insurance usually leaves out flood.
5. Links to us (0 referring domains): outreach batch after tonight's ship; the head terms (flood insurance, fema flood map, nfip) are held by FEMA and regulators and need authority, not pages.
Not winnable now: "flood insurance", "fema flood map by address", "flood zone map" (FEMA, county viewers, a working map tool hold them); "flood insurance quote" (we give no quotes).
6. City pages (owner 11-15 "we can do city too"): towns are 3,050/mo floor over 5,180 keywords (chicago 1K+, sacramento/new orleans/houston/hartford 100+). Build only after 1-4, for the top 25 cities by KWP, each with its own ZIP-level policy and claim figures (ZIP lookup data) and the FEMA lookup; a city whose ZIPs mostly sit in one county page with the same figures = no page. New page type = full review (~250k) before any ships. Edge cases before code: ZIP straddles two cities (count once, name the rule); city across two counties; ZIP with under 30 policies (no median); city name shared by many states (slug with state); claims reportedZipCode vs policy ZIP; 25/day cap.
## "Flood zone map" demand; SERP read 11-15 (WebSearch, top results only, no traffic numbers)
- "[county] flood zone map" (Pinellas, Harris): won by the county's own address viewer (pinellas.gov/flood-maps, HCFCD MAAPnext) and FEMA's map; the rest is local news and spam pages. Reading: searchers want their address on the official map. No new page type; the answer is the address lookup on county pages (WAITING 11-20: address tool to "all" after 7 green nightly tests) and linking the county's own viewer where FEMA's community data names it.
- "flood zone x meaning": won by private insurers' articles (Kin, Compare.com, Insurify) with definitions only. /flood-zones/x/ already has what none of them shows (zone X cost, share of claims outside A/V). Move: zone pages lead with the definition in plain words (rule-quoted) in the next template batch; no twin page.
- Owner check still useful (Ahrefs traffic of each #1) before retitling county pages to "flood zone map".
- 11-15: address lookup flag set to "all" (ships with tonight's batch): the 7-green gate was already met (8 green 11-05 to 11-12). Nightly monitor is refused until 12-01; free alternative = a separate public repo holding only live_zonemap.py + test_zonemap.py (public repos get free Actions minutes), owner OK needed (publishes that code).
- Order (11-15): 1 address lookup on every county page, 2 then titles say "flood zone map" (a title must not promise a map the page lacks). Edge case found 11-15: the rollout gate (7 green nightly live_zonemap runs) cannot pass: watch.yml is refused for Actions minutes (11-13 fail, 11-15 refused; green 11-11, 11-12, 11-14) and FEMA's map service refuses this laptop (curl SSL error 35; local live_zonemap 0 of 5 zones). Unblocks: Actions spending limit (owner) or 12-01 reset, then 7 nights. A failed lookup prints nothing (CLAUDE.md), so a broken tool hides itself rather than misleads.

## Guides (standard: one searched question per URL, answer in 40 words, our FEMA table, rule() quotes only, G6 = a figure no top-3 result has)
Live: homeowners vs flooding, private flood, condo, buying a house in a flood zone, deductibles, Risk Rating 2.0, LOMA/LOMR, claims section; built: contents coverage.
Queue (each needs G1 owner check + G6 figure): flood vents (obstructionType code 15 after FEMA code list read raw); glossary pages only if GSC shows term queries.
Cut with reason: elevation certificate (legacy field, zone-confounded), basement (field 65% blank), cars (no FEMA figure), ICC/limits/required/waiting period (owned by existing pages), FEMA aid vs insurance (mixed incident types).
Edge cases kept: K1 never print a search volume; K2 a KWP file without "United States" is not used; K3 one page per question, never per phrasing; G4 no company names or "best"; G8 0 impressions after 90 days = merge into nearest page (301).

## Backlinks (Claude drafts and sends after owner approves each batch)
- One email per organization ever (outreach guard), one exact figure + the page that holds it, reply address contact@floodinsurancedata.com; CAPTCHA forms left to the owner.
- Send day: `tools/outreach_gate.py <urls>` PASS (editor review, live text unchanged, indexed).
- Drafts: state/outreach/pitches.md (11-15: Wave 2 "homeowners pay" mislabel fixed; all figures dated 11-08, re-read live on send day).
- Batch 1 (owner 11-15 "send them yourself"; owner approves list + text first): resource-page owners who add links (extension services, county CRS coordinators, floodplain-manager chapters, library guides), not big-newsroom tip lines (Floodlight, ICN, Houston Chronicle, Tampa Bay Times publish no tips email; ICN and the Times use forms or secure channels: low link yield, forms are owner-only). Order: after the 11-16 ship, editor gate (`hater.py prep --editor`, ~250k) on the linked pages, then 10 named contacts with published emails, then owner approval, then send + outreach guard. Lead figure: 83.4% of 267,655 NFIP claims since 2020 had a recorded payment.
- Targets: local newsrooms within 48 h of a declaration; data desks; ASFPM, CRS coordinators, extension services, library guides. Numbers: 12-15 2+ referring domains; 01-15 5+; 03-01 15+. Never paid links or swaps.

## Checkpoints and waiting
- 11-21: Price Gap to index (owner). Weekly: GSC + GA4 read, IndexNow recheck.
- 11-26: master audit (docs/AUDIT-PROMPT.md) + black-hat prompt + 4-week GSC review; ads decision.
- 12-01: Actions minutes reset. 12-04: 30+ impressions on "flood zone/map" queries, else restore old titles; shorten titles/descriptions.
- 12-09: monthly top-3 compare on every keyword group. 12-12: NFIP authorization past 12-11? If it lapses set `start` to [].
- 01-04: unfreeze zero-demand counties only if 5+ county pages have US non-brand impressions, 3+ in top 30, 1+ click. Then 20/day, cap 25 new pages/day all kinds.
- 01-05: .git size (241 MB 11-11, ~12 MB/day); at 1 GB move built pages to a 'site' branch.
- 01-08 zone pages position 15 or better; 01-29 /flood-zone-map/ 200+ impressions; 02-01 claims page 1+ referring domain or 100+ impressions; 02-03 continue / consolidate / stop.

## Live lookup test (11-15)
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
