# Flood insurance data site (floodinsurancedata.com)

Strategy and status: PLAN.md (read at session start, update after every batch).
Session start, first reply: report every deploy since the last session (`gh run list` for publish-counties and refresh-data, `git log` "publish:" lines, live sitemap count). Owner 2026-10-29.

## Reader
A US homeowner or buyer at one place, on a phone, 30-60 seconds, days of urgency: at a closing with a flood-zone letter, a renewal that jumped, or a street that flooded last night. Page answers, in order, above the long tables: how risky here, am I required to buy it, what it costs (in my zone), is it rising, what floods pay out here, can I pay less; plus how urgent and what to do next (where to buy, 30-day wait, coverage limits). One static page per place from public federal data. Run flood sessions from this folder; calcscrape and river rules do not apply.

**User, not Google (HARD, owner 2026-10-28).** Every choice is judged by the scared reader on a phone, never by
what a crawler wants. If something helps SEO but confuses or slows the reader, the reader wins. The full
helpfulness checklist is in PLAN.md; every review brief must judge every item on it.

## Hard rules
- Owner is a non-coder: do the work, decide defaults, short plain replies, no "Next:" line.
- Separate from calcscrape and river: own domain, Search Console and ad account; no shared template or links.
- Line 0: be the most helpful flood-insurance page for this place. Every public dataset that changes the decision is shown with exact source and as-of date; withhold only if wrong, misleading, padding or no mechanism (never "small sample", "confounded", "not actionable").
- A reader question with no dataset = a printed gap line naming the data to pull; a dataset answering no question = left out.
- Showing anything wrong, mislabelled or misleading is the one unforgivable sin. Label every figure's base (median vs mean, premium vs cost, homes vs all policies).
- No quote, no advice prose, no "safe / you should" verdict, no hedging. No premium-rise or premium-estimate calculator (owner). Quote checker and ZIP lookup stay.
- User first, never Google first: no stuffing, doorway, near-duplicate pages, fake freshness, hidden text. One colour system; answers on screen 1; static, no client frameworks.
- Datasets shown: NFIP Policies v3, NFIP Claims v3, National Risk Index, Disaster Declarations, Housing Assistance Owners (flood disasters only), Community Status Book, IA Multiple-Loss Flood Properties. Methodology says "Seven"; keep the count equal to the sources listed. Cut on purpose (`tools/card_spec.py`): Census take-up, NOAA storm events, tile maps.
- Pages: 51 state pages; county pages (floor: 30 priced single-family policies for a median); ZIPs fold into the county page (standalone only with enough policies, a decision-changing difference and an answer the county lacks); no city pages; ceiling ~2,000 pages. New counties a few at a time, never hundreds.
- Every page prints what the data cannot say: your own premium, private prices, your address's exact zone (link FEMA's map), why prices rise. Aggregates only, never record- or address-level.
- Builder rules: every number through `tp(key, path)` or `m(key, shown)`; size/direction words only via `claim()`; law text only via `rule()` (effective date, coverage, official URL, exact quote from this session); places named from Census/NRI; county/parish/borough from `UNIT`; shares via `_share_words()`. Never type a number, date, law or source into a template.
- Never fake or estimate a figure; null and a gap line beat a guess. Never from memory.
- Data traps: SUM `policyCount`, never count rows; negative premiums are refunds; claims `countyCode` may not match the property county.
- The same paragraph never appears twice on a page; shared definitions live on `/methodology/`.
- Five steps, in order: question the requirement, delete waste (never an answer), simplify, accelerate (each defect becomes a rule or check with a mutation test the same day), automate last. No card or page-length caps.
- Data pipeline runs in GitHub Actions, never on the laptop. Locally only `build_all.py` and the gates.
- Ship only via `release.py`; never push or run wrangler by hand (every push redeploys the committed dist).
- One background job at a time; no polling; batch fixes, gates once.
- No paid referrals until a state-licensing + FTC disclosure check; no ads until a four-week Search Console review passes. A free link to FEMA's agent finder is allowed.

## Commands
- Build: `python -I tools/build_all.py`.
- Gates: `python -I tools/release.py` (build, `gate.py` 9 questions, truth check, `test_gate.py` mutations, `phone_check.py` 390 px, `google_gate.py`). Independent recompute: `python -I tools/recheck.py` as its own background job.
- Ship: `python -I tools/release.py --ship` (build, every gate incl. hater review, commit dist, push, deploy, live gate). `--hotfix "reason"` skips only the hater review, only to remove or correct wrong live text a review named.
- Live gate: `python -I tools/release.py --live`.
- Cloud: `refresh-data.yml` monthly (pull_raw, agg_raw, extras_raw, collect_state_small; commits `data/`); `publish-counties.yml` daily adds reviewed counties via `add_counties.py`.
- No dry runs of cloud jobs (owner 2026-10-29): the next scheduled run is the test; a failing gate ships nothing.
- Alerts: a failed cloud job opens one GitHub issue (GitHub emails the owner) and closes it when it passes again; nothing
  else emails (owner 2026-10-29). Jobs fail closed and self-heal (PLAN "Runs without Claude").
- Gap backlog: `state/reviews/backlog.md` (google_gate S14 fails a release when an item is 3 review rounds old).

## Procedure (every build or fix)
0. Stop the harm: wrong live text a reader could act on is fixed or removed first (`--hotfix`).
1. Work the open defect list (latest `state/reviews/hater-round<N>.md`), not a new review. Each BLOCKER/MAJOR gets one line in `state/reviews/fixlog-round<N>.md`: defect, root-cause layer, fix, proof. No line = not fixed. Fix the class at its source.
2. Truth: every screen-1 figure has a definition in `tools/metrics.py` and is recomputed independently; labels match the population.
3. Rules: dated, quoted, re-fetched by `recheck.py`; a rule changing on a future date states both states.
4. Beat #1: WebSearch the real query; show what the top 3 give from our data or print a gap line.
5. Gates once. 6. Review only when the fixlog is complete. 7. Ship only on PASS.

## One-shot a batch: failures first (HARD, owner 2026-10-29; each pre-check is a failure that happened)
Before editing, write each item's likely failure and its pre-check. Then:
- Edit through a script file or Edit, never a heredoc with quotes; `ast.parse` every edited file at once (an
  apostrophe broke the build 3 times).
- Screen 1 holds only the answers and their links; any new line goes below the quick answers (P3/P4 failed 4 times).
- Words: read gate.py's word rules first (A6 new-policy words, B2 unchecked size words, E2 repeats, V1 untagged
  numbers); every number through `tp`/`m`; a new metric field needs `metrics.py --refresh`.
- A new figure: state its base and how blanks are handled, recompute it from raw before wording it (round 19:
  blank zones were counted as "outside").
- Fast loop: `build_counties.py --only <geoid>` for palm-beach-county-fl (states and home have no single-page build;
  run build_states.py + build_site.py) with gate and phone check until clean; then ONE full build
  and ONE release.py run; then one light check; then ship and read one live page.
- Never record a review for a template that changed after it; one writer per project; pull before work.
- A template change no reader can see (markup, scripts): `hater.py carry <round> <last passed release> <samples>`
  keeps the PASS only if every sample's visible text is identical (`carry <round> passed <samples>` compares with the snapshot saved when it passed); any difference needs a light review.

## Ponytail ladder before building anything (HARD, owner 2026-10-29)
Stop at the first rung that holds: does it need to exist (does a sentence already on the page answer it?) ->
already in this codebase -> Python stdlib -> what the browser already does (input type=date, two tabs, find-in-page)
-> one line -> only then the minimum code. Tests scale with harm: logic that can hurt a reader gets one oracle
check; nothing else gets a test suite. Reviews cost the tokens, code is cheap: never spend a review on a nice-to-have.

## Reader tools ship standard (HARD, owner 2026-10-29: "bugs or being wrong will destroy this site")
A tool ships only when ALL hold: (1) a truth table written before code (inputs -> exact output, each tied to a
rules_registry source; the finite set of output sentences reviewed once); (2) an independent Python oracle computes
every expected answer and the page's JS output must equal it; (3) edge suites: dates (Feb 29 + 60, Dec 31 rollover,
Hawaii/Guam time zones), numbers ($1,234.56, spaces, 0, negative, 1e9, letters, pasted text, monthly-for-yearly),
data (all 1,803 queued counties: missing fields, one zone, zeros); (4) fuzz: thousands of random inputs, never a
crash, never NaN/undefined/Infinity, never a verdict word; (5) Chromium + WebKit + JavaScript off; (6) a kill switch
(`tools/tools_flags.json`, off = removed on the next hotfix); (7) staged: the 3 sample pages for 2 weeks, then all;
(8) rule wording checked by a second model. Never generate a page per input pair (scaled-content abuse): one tool URL.

The universal version is the global ~/.claude/CLAUDE.md "Master engineering prompt" (every project; a global hook
prints its trigger on every request). Apply it to the machinery too: the daily full rebuild survived because it never was.

## Whole project: Musk's five steps toward #1 (HARD, owner 2026-10-28; strategy and scoreboard in PLAN.md)
Before any task, name which scoreboard number it moves: pages indexed, impressions, clicks, page-1 queries,
AI-answer citations. None = question it, then delete it. Order: question, delete, simplify, accelerate, automate last.
Two files only: CLAUDE.md = rules, PLAN.md = strategy and state.
Old-school optimization (owner 2026-10-30; Knuth, Amdahl, Goldratt, Pike): (1) measure first: no speed or cost work without a
number from a real run; a guess is not a reason. (2) One bottleneck at a time: name the single slowest or costliest step; work
anywhere else moves nothing. (3) Amdahl: a step's share of the total caps the gain; under 10% of total = leave it. (4) Big-O
before constants: per-job cost that grows with pages gets "only what changed" before it hurts; a fixed cost waits. (5) Bytes are the hot
path: count what crosses a phone connection, gzipped, per page, and every byte must serve the reader; a one-off stays simple. (6) Correct first: never trade a
check that catches wrong numbers for speed. (7) Re-measure after; no drop = revert. Process follows harm: a change no reader can
see (a tag, markup) gets one build, the text-identical proof, one ship and one live read.

## Review and gate budget (HARD, owner 2026-10-28: "be like Elon Musk with review/gates, we've blown a million tokens")
1. Question the requirement: before any review, name the defect it could catch that the gates and the all-county
   scan cannot. None named = no review.
2. Delete: no full hater round for wording, labels, one card or a rule (a round cost ~320k tokens). Wrong live text
   ships on gates with `--hotfix`. Never review the same defect class twice: after one finding it is a gate check.
3. Simplify: the default check is scripts (gates + all-county scan, near zero tokens). A light check is one cheap-model
   agent, changed cards only, 2 pages, page text only (no screenshots, no web search), under ~50k tokens.
4. Accelerate: batch every change, run gates ONCE per batch, one light check per batch, never per fix.
5. Automate: FULL mode (6 judges, screenshots, search) at most once per major template redesign or new data source,
   and only with the owner's OK and a stated token cost first.

## Review (signed-review gate)
- Enforced: `google_gate.py` S12 fails a release with any indexable page lacking a current PASS in `state/reviews/<slug>.json`; `add_counties.py` queues only reviewed counties.
- Size the review to the change (global CLAUDE.md "Size every review to the change"); say level and cost in one line first:
  - None: nothing a reader sees changed, or a machine check covers it.
  - Light / FIRST mode: re-check only the changed cards on the samples (first screen + text, cheap model). Wording, a label, a format, one card.
  - FULL mode: a full round on the 3 samples (home, louisiana, palm-beach-county-fl) after a template change, new card or data source.
  - Once per batch, never per fix; a FAIL re-reviews only that page.
- Template review: when the 3 samples PASS under the current template hash, every page from it may ship, except pages `review.flags()` marks (unpaid share 20+ points off the state's, claims per policy under 0.2x or over 5x), which each need their own PASS. A template change resets only the samples.
- Steps: `python -I tools/hater.py prep <round> <slugs>` (screenshots + brief from `docs/HATER-PROMPT.md`), run it in a fresh agent that did not build the page, `python -I tools/hater.py record <round>`. PASS only with zero BLOCKER and zero MAJOR. The reviewer reads the fixlog only after its own list.
- Every defect class becomes a builder rule, a truth definition, a rule date/quote or a gate check with a mutation test.

## Owner alone
Domain; Search Console; ad account and consent banner; publisher identity (site stays anonymous); opening pages to the index; paid referrals; cutting any block.
