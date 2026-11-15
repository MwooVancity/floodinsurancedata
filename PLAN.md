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
1. Template batch (below): code review medium DONE 11-15 (8 findings fixed, stamp 821f8e5cd818). WAITING 2026-11-16 UTC (last template ship 11-15 03:14 UTC; release.py refuses a second): fix the rule-text items below after a raw re-read, one S12 proofread review of home/louisiana/palm-beach/new-york (~80k, light), one ship.
2. WAITING 2026-11-16 (after the ship): `prose_check.py --record` lowers the baseline to today's 0 faults (ratchet then holds every page at 0).
3. WAITING 2026-11-22 (weekly GSC read): guides: build the next one only when a live guide shows impressions in GSC (none have yet); queue in "Guides" below.
4. WAITING 2026-11-16 (after the template ship, so the reviewed text is final): outreach batch: editor gate (`hater.py prep --editor`), owner approves list + text, Claude sends.
5. WAITING 2026-12-01 Actions reset: Flood Map Age data pull via `tools/cloud_run.py` (one forced refresh a month, batch every queued field).

## Template batch (next site-wide release; built 11-14, uncommitted until code review, not shipped)
In it: papers prose rewrite (plain-words cards, shorter Results/Limitations, Price Gap "exact order is not reliable"); hub prose rewrite (home, /nfip/, zones, guides, methodology, about, data; long rule runs split); county template (papers card explains the five groups, 0-county state lines dropped, LOMA paragraph split, "Is it rising?" from the trend card, "52.8% of these policies pay a premium, before fees, below..."); link-only sentences removed on home and /nfip/; footer gains "Guides" (S16 caught /guides/ orphaned); new guide /guides/flood-insurance-contents-coverage/ (U.S. 81% of 2,320,412 SF primary-home policies carry contents; WV 43.8% to DC 95.3%; claims_check --guides 27 mutations).
Gates 11-14 after rebuild: build PASS, paper_gate + --test PASS, prose 0 faults (was 1,071), S16 clean, S12 needs review (template hash changed).
Open review findings to fix before ship (the rest are style, decided no):
- Rule text, needs raw re-read before rewording (rules_registry): /nfip/ 30-day wait exceptions as a 3-item list; LOMA/lender-review split; TWIA spelled out; Elevation Certificate defined; "Emergency Program discount" defined or cut from zone pages; contents guide elevated-building sentence (65 words) split.
- Copy: "Among the five costliest years..." note reworded (test_gate.py pins the string); Flood Calendar plain-words lede and the 404-of-416 clause said once; Damage Over Coverage top-county sentence split (paper_gate regex pins it); "How risky?" on state pages gives the count of Very High/Relatively High counties.
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

## Guides (standard: one searched question per URL, answer in 40 words, our FEMA table, rule() quotes only, G6 = a figure no top-3 result has)
Live: homeowners vs flooding, private flood, condo, buying a house in a flood zone, deductibles, Risk Rating 2.0, LOMA/LOMR, claims section; built: contents coverage.
Queue (each needs G1 owner check + G6 figure): flood vents (obstructionType code 15 after FEMA code list read raw); glossary pages only if GSC shows term queries.
Cut with reason: elevation certificate (legacy field, zone-confounded), basement (field 65% blank), cars (no FEMA figure), ICC/limits/required/waiting period (owned by existing pages), FEMA aid vs insurance (mixed incident types).
Edge cases kept: K1 never print a search volume; K2 a KWP file without "United States" is not used; K3 one page per question, never per phrasing; G4 no company names or "best"; G8 0 impressions after 90 days = merge into nearest page (301).

## Backlinks (Claude drafts and sends after owner approves each batch)
- One email per organization ever (outreach guard), one exact figure + the page that holds it, reply address contact@floodinsurancedata.com; CAPTCHA forms left to the owner.
- Send day: `tools/outreach_gate.py <urls>` PASS (editor review, live text unchanged, indexed).
- Drafts: state/outreach/pitches.md. Lead figure: 83.4% of 267,655 NFIP claims since 2020 had a recorded payment.
- Targets: local newsrooms within 48 h of a declaration; data desks; ASFPM, CRS coordinators, extension services, library guides. Numbers: 12-15 2+ referring domains; 01-15 5+; 03-01 15+. Never paid links or swaps.

## Checkpoints and waiting
- 11-21: Price Gap to index (owner). Weekly: GSC + GA4 read, IndexNow recheck.
- 11-26: master audit (docs/AUDIT-PROMPT.md) + black-hat prompt + 4-week GSC review; ads decision.
- 12-01: Actions minutes reset. 12-04: 30+ impressions on "flood zone/map" queries, else restore old titles; shorten titles/descriptions.
- 12-09: monthly top-3 compare on every keyword group. 12-12: NFIP authorization past 12-11? If it lapses set `start` to [].
- 01-04: unfreeze zero-demand counties only if 5+ county pages have US non-brand impressions, 3+ in top 30, 1+ click. Then 20/day, cap 25 new pages/day all kinds.
- 01-05: .git size (241 MB 11-11, ~12 MB/day); at 1 GB move built pages to a 'site' branch.
- 01-08 zone pages position 15 or better; 01-29 /flood-zone-map/ 200+ impressions; 02-01 claims page 1+ referring domain or 100+ impressions; 02-03 continue / consolidate / stop.

## Runs on its own
Daily `publish-counties.yml` (paused with Actions minutes), monthly `refresh-data.yml` (skips when current), `map-status.yml`, nightly `watch.yml`. Session start: `tools/actions_check.py` reads refused/failed runs.

## Never in copy
Open vs closed claims; "denied"; a period or base left out; a promise of AI citations; IndexNow as proof of indexing; a premium estimate or rise.

## Owner only
Decisions, sends, money, identity. Bing: Re-submit sitemap in Bing Webmaster. GA: mark home IP as internal traffic. AdSense "Request review". Price Gap to index. Drop the second table of contents (yes/no). Actions spending limit or public repo (optional).

## Reference
- Datasets: NFIP Policies v3, Claims v3 (codes 98/99 out), NRI, Disaster Declarations, Housing Assistance Owners (flood only), Community Status Book, IA Multiple-Loss, NOAA Sea Level, FEMA NFHL (US cloud). Cut on purpose (`card_spec.py`): Census take-up, NOAA storm events, tile maps.
- Address tool: never compute, draw or store a zone; show FEMA's live zone, panel, date, BFE/AO depth and map letters as returned.
- Rules: one example is not a rule; `recheck` re-reads live text; unreachable sources in `state/manual-rule-read.json` (183 days max).
- S12: `review.flags()` pages need their own PASS or a same-kind example at most 2x out. `hater.py prep <round> <slugs> --local --light [--proofread|--editor]`, `hater.py record <round>`, `hater.py carry <round> passed <slugs>`.
- Paper harms H1-H16 and edge cases E1-E31 (built into paper_gate.py mutations): full lists in PLAN.md at commit 0853000a2 (`git show 0853000a2:PLAN.md`).
