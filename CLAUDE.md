# floodinsurancedata.com: rules
State and next moves: PLAN.md (read at session start, update after every batch). History: git. Keep this file under 8 KB; two docs only.
First reply of a session: report every deploy since the last one (`gh run list` publish-counties + refresh-data, `git log` "publish:", live sitemap count).
Run flood sessions from this folder; calcscrape and river rules do not apply. Owner is a non-coder: decide defaults, short plain replies, no "Next:" line.

## Reader (HARD)
US homeowner or buyer at one place, on a phone, 30-60 seconds, urgent: a closing with a flood-zone letter, a renewal that jumped, a street that flooded last night. Page answers, in order, above long tables: how risky here, am I required to buy, what it costs in my zone, is it rising, what floods pay out here, can I pay less; plus how urgent and what next (where to buy, 30-day wait, coverage limits). One static page per place from public federal data.
User, not Google: if something helps SEO but confuses or slows the reader, the reader wins. Every review judges the helpfulness checklist in `docs/HATER-PROMPT.md`.

## Truth (HARD)
- Wrong, mislabelled or misleading is the one unforgivable sin. Label every base (median vs mean, premium vs cost, homes vs all policies).
- Never fake, estimate or recall a figure; null and a gap line beat a guess.
- Line 0: most helpful page for this place. Every public dataset that changes the decision is shown with exact source and as-of date; withhold only if wrong, misleading, padding or no mechanism (never "small sample", "confounded", "not actionable"). A reader question with no dataset = a printed gap line naming the data; a dataset answering no question = left out.
- No quote, advice prose, "safe / you should" verdict or hedging. No premium-rise or premium-estimate calculator. Quote checker and ZIP lookup stay.
- Every page prints what the data cannot say: your premium, private prices, your exact zone (link FEMA's map), why prices rise. Aggregates only, never record- or address-level.
- Datasets: NFIP Policies v3, NFIP Claims v3, National Risk Index, Disaster Declarations, Housing Assistance Owners (flood disasters only), Community Status Book, IA Multiple-Loss Flood Properties, NOAA Sea Level Trends. Methodology's "Eight" must equal the sources listed. Cut on purpose (`tools/card_spec.py`): Census take-up, NOAA storm events, tile maps.
- Data traps: SUM `policyCount`, never count rows; negative premiums are refunds; claims `countyCode` may not match the property county.
- Builder: every number via `tp(key, path)` or `m(key, shown)`; size/direction words via `claim()`; law text via `rule()` (effective date, coverage, official URL, exact quote from this session); places from Census/NRI; county/parish/borough from `UNIT`; shares via `_share_words()`. Never type a number, date, law or source into a template.
- New figure: state its base and how blanks are handled, recompute from raw before wording it. Same paragraph never twice on a page; shared definitions live on `/methodology/`.

## Site (HARD)
- 51 states; counties (floor: 30 priced single-family policies for a median); ZIPs fold into the county page (standalone only with enough policies, a decision-changing difference and an answer the county lacks); no city pages; ceiling ~2,000. New counties 20 a day (owner 2026-11-01); no holding pages back, no pauses, no noindex holds.
- No stuffing, doorway, near-duplicate pages, fake freshness, hidden text. One colour system; answers on screen 1; static, no client frameworks. No card or page-length caps.
- Separate from calcscrape and river: own domain, Search Console, ad account; no shared template or links.
- No paid referrals until a state-licensing + FTC check; no ads until a four-week Search Console review passes. A free link to FEMA's agent finder is allowed.
- Owner alone: domain; Search Console; ad account and consent banner; publisher identity (site stays anonymous); opening pages to the index; paid referrals; cutting any block.

## Decide before building (HARD)
1. Name the scoreboard number it moves: pages indexed, impressions, clicks, page-1 queries, AI citations. None = delete it.
2. Five steps, on the work AND the machinery: question, delete (never an answer), simplify, accelerate, automate last. Each defect becomes a rule or check with a mutation test the same day.
3. Ponytail: does a sentence on the page answer it -> already in the code -> stdlib -> what the browser does (input type=date, two tabs, find-in-page) -> one line -> least code. Tests scale with harm: reader-harm logic gets one oracle check.
4. Old-school optimization: measure from a real run, never guess. One bottleneck at a time. Under 10% of the total = leave it. Cost that grows with pages gets "only what changed"; fixed cost waits. Bytes crossing a phone connection (gzipped, per page) and tokens are the hot paths; every byte must serve the reader. Never trade a check that catches wrong numbers for speed. Re-measure; no drop = revert. A build writes no tracked file. Audit the whole pipeline, source to phone, not files: each step shows its cost and the defect it caught; never caught and catches no wrong number or law = cut. A step skips when its input did not change.
5. Process follows harm: name what can go wrong with THIS change, run only checks that could catch it.

## Commands
- Build `python -I tools/build_all.py`. Gates `python -I tools/release.py` (build, `gate.py`, truth check, `test_gate.py` mutations, `phone_check.py` 390 px, `google_gate.py`). `python -I tools/recheck.py` = independent recompute, its own background job.
- Ship `python -I tools/release.py --ship` (all gates incl. review stamp, commit dist, push, deploy, live gate). `--hotfix "reason"` skips only the review, only to remove or correct wrong live text. Live gate `--live`.
- Ship only via `release.py`; no wrangler by hand; a push redeploys committed dist, so hand-push docs and workflows only.
- Cloud, never the laptop, for data: `refresh-data.yml` monthly; `publish-counties.yml` daily via `add_counties.py`. Locally only build and gates. No dry runs: drills or the next scheduled run; a failing gate ships nothing.
- A failed job opens one GitHub issue (emails owner), closes on pass; nothing else emails. Jobs fail closed and self-heal (PLAN).
- One background job; no polling; one writer; pull before work. Gap backlog `state/reviews/backlog.md` (S14 fails an item 3 rounds old).

## Every fix
0. Wrong live text a reader could act on goes first (`--hotfix`).
1. Work the open list (latest `state/reviews/hater-round<N>.md`), not a new review. Each BLOCKER/MAJOR: one line in `fixlog-round<N>.md` (defect, root-cause layer, fix, proof). No line = not fixed. Fix the class at its source.
2. Screen-1 figures: defined in `tools/metrics.py`, recomputed independently, labels match the population.
3. Rules dated, quoted, re-fetched by `recheck.py`; a future rule change states both states.
4. Beat #1: WebSearch the real query; show what the top 3 give from our data or print a gap line.
5. Gates once, review only with a complete fixlog, ship only on PASS.

## One-shot a batch (each is a failure that happened)
Write each item's likely failure and pre-check first.
- Edit via Edit or a script file, never a heredoc with quotes; `ast.parse` each edited file at once.
- Screen 1 holds only answers and their links; new lines go below the quick answers.
- Read gate.py's word rules first (A6 new-policy words, B2 size words, E2 repeats, V1 untagged numbers). New metric field: `metrics.py --refresh`.
- Fast loop: `build_counties.py --only <geoid>` for palm-beach-county-fl (states, home: `build_states.py` + `build_site.py`) with gate and phone check; then ONE full build, ONE release.py, one light check, ship, read one live page.
- Change no reader can see (tag, markup): one build, `hater.py carry <round> <last passed release> <every slug on the old hash, flagged examples too>` (`passed` compares the saved snapshot); text differs = light review; one ship, one live read.
- Never record a review for a template that changed after it.

## Reviews (HARD: "we've blown a million tokens")
- Before any review name the defect gates and the all-county scan cannot catch. None = no review. Say level and cost first. Once per batch; a FAIL re-reviews only that page; a defect class found once becomes a check.
- None: nothing visible changed, or a machine check covers it. Light: one cheap-model agent, changed cards, 2 pages, text only, under ~50k tokens (wording, label, one card, a rule). Full: 6 judges, screenshots, search, ~320k: only a major redesign or new data source, on the samples, with the owner's OK.
- S12 fails any indexable page without a current PASS in `state/reviews/<slug>.json`; `add_counties.py` queues only reviewed counties. Samples home, louisiana, palm-beach-county-fl passing the template hash cover every page, except `review.flags()` pages (unpaid share 20+ points off the state's; claims per policy under 0.2x or over 5x), which need their own PASS or a same-kind example at most twice as far out.
- Run: `hater.py prep <round> <slugs>` (`docs/HATER-PROMPT.md`), a fresh agent that did not build the page, `hater.py record <round>`. PASS = zero BLOCKER and MAJOR. The reviewer reads the fixlog only after its own list.

## Reader tools ship standard (HARD: "bugs or being wrong will destroy this site")
All must hold: (1) truth table before code, each output tied to a rules_registry source, sentences reviewed once; (2) independent Python oracle equals the page's JS; (3) edge suites: dates (Feb 29 + 60, Dec 31, Hawaii/Guam), numbers ($1,234.56, spaces, 0, negative, 1e9, letters, pasted text, monthly-for-yearly), all queued counties (missing fields, one zone, zeros); (4) fuzz thousands: no crash, NaN, undefined, Infinity or verdict word; (5) Chromium + WebKit + JS off; (6) kill switch `tools/tools_flags.json`; (7) 3 sample pages for 2 weeks, then all; (8) rule wording checked by a second model. One tool URL, never a page per input pair.
