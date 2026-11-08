# floodinsurancedata.com: rules
State and next moves: PLAN.md (read at session start, update after every batch). History: git. Two docs only; this file under 8 KB. Global CLAUDE.md applies, not repeated.
Session start: report deploys since last session (`gh run list`, `git log` "publish:", live sitemap count); fix any failed run.
Run from this folder; nothing shared with calcscrape or river. Owner is a non-coder: decide defaults, short plain replies, never ask what is next.

## Reader (HARD)
US homeowner or buyer at one place, on a phone, 30-60 seconds, urgent. Above tables, in order: how risky, am I required, cost in my zone, is it rising, what floods pay here, can I pay less; plus urgency and next steps (where to buy, 30-day wait, limits). One static page per place from public federal data. Reader beats SEO. Reviews judge the checklist in `docs/HATER-PROMPT.md`.

## Truth (HARD)
- Wrong, mislabelled or misleading is the one unforgivable sin. Label every base (median/mean, premium/cost, homes/all policies). Never fake, estimate or recall a figure; null and a gap line beat a guess.
- Every public dataset that changes the decision is shown with source and as-of date; withhold only if wrong, misleading, padding or no mechanism. A reader question with no dataset = a printed gap line; a dataset answering no question = left out.
- No quote, advice prose, "safe / you should" verdict, hedging, premium-rise or premium-estimate calculator. Quote checker and ZIP lookup stay.
- Every page prints what the data cannot say: your premium, private prices, your exact zone (link FEMA's map), why prices rise. Aggregates only, never record- or address-level NFIP data.
- Address tool (owner 11-06): the site never computes, draws or stores a zone. For a point the reader placed and confirmed, it may show FEMA's zone, panel and effective date exactly as FEMA's live service returns them, labelled "FEMA's map, not an official determination", naming every zone within 15 m; FEMA silent = only a link.
- Datasets: NFIP Policies v3, NFIP Claims v3, National Risk Index, Disaster Declarations, Housing Assistance Owners (flood only), Community Status Book, IA Multiple-Loss Flood Properties, NOAA Sea Level Trends, FEMA NFHL (US cloud only). Methodology's "Nine" = sources listed. Cut on purpose (`tools/card_spec.py`): Census take-up, NOAA storm events, tile maps.
- Data traps: SUM `policyCount`, never count rows; negative premiums are refunds; claims `countyCode` may not match the property county.
- Builder: numbers via `tp()` / `m()`; size words via `claim()`; law via `rule()` (date, coverage, official URL, exact quote read this session); places from Census/NRI; county word from `UNIT`; shares via `_share_words()`. Never type a number, date, law or source into a template. New figure: state base and blank handling, recompute from raw before wording. Same paragraph never twice on a page; shared definitions on `/methodology/`.
- Rule guardrails (each failure happened): (1) read the source in raw text, a search summary is a lead; (2) scope in the sentence: program, form, occupancy, lender, state; (3) keep the source's strength ("at least", "may"); no sentence without a quote, inference cut; (4) two official sources disagree: print only what both support, a dated guide never beats the current manual; (5) one example is not a rule; (6) law checked against current text (`recheck.LIVE`); unreachable source goes in `state/manual-rule-read.json`, older than 183 days stops the release; (7) reviewers read the source too; (8) a new FEMA code is labelled from the data dictionary. FEMA refuses the laptop: read via the US runner (`fema-probe.yml`).

## Site (HARD)
- 51 states; counties (floor 30 priced single-family policies for a median); ZIPs fold into the county page (standalone only with enough policies and a decision-changing answer the county lacks); no city pages; ceiling ~2,000.
- Counties last (owner 11-07: "money keywords first then county last"; a debate does not decide): 20 a day, queue "kw" > 0 only; live pages stay indexed, no noindex holds.
- No stuffing, doorway, near-duplicate pages, fake freshness, hidden text. One colour system; answers on screen 1; static, no client frameworks. No card or page-length caps.
- No paid referrals before a licensing + FTC check; no ads before a 4-week Search Console review. FEMA's agent finder link is fine.
- Owner alone: domain, Search Console, ads and consent banner, publisher identity (site anonymous), opening pages to the index, paid referrals, cutting any block.

## Internal links (HARD, owner 11-08; google_gate S16 = `tools/linkcheck.py`, tests in test_calc.py)
- Every state and county page links home, its state, up to 6 bordering counties, the zone page for each zone it names, and every hub in `linkcheck.HUBS` (zone map lookup, /nfip/, renters, claims, ZIP). Home links every state and hub; a state links every live county. S16 fails a missing hub link, a broken internal link, an orphan.
- Zone pages should link the counties with the most homes in that zone (OPEN).
- Anchor = the destination in the searcher's words ("flood zone map lookup by address", "Zone AE", "Harris County"), never "here" or "click".
- Links sit in the sentence where the reader needs them; never a link block, keyword list or footer farm; screen 1 holds answers only (P4).
- A new page type joins `HUBS` and gets home and state links the same day. After a template change, re-count inbound links (script, no review): a hub linked from under half of state + county pages is a defect.

## Decide before building (HARD)
Name the scoreboard number it moves; none = delete it. Each defect becomes a check with a mutation test the same day; reader-harm logic gets one oracle check. Phone bytes (gzipped) and tokens are the hot paths; never trade a wrong-number check for speed. A build writes no tracked file; a step skips when its input did not change.

## Commands
- Build `tools/build_all.py`; gates `tools/release.py` (build, gate, truth, mutations, phone 390 px, google_gate); `tools/recheck.py` = independent recompute (background). Always `python -I`.
- Ship only `release.py --ship` (gates, review stamp, commit dist, push, deploy, live gate). `--hotfix "reason"` skips only the review, only to fix wrong live text. `--live` = live gate. No wrangler by hand; hand-push only docs and workflows.
- Data runs in the cloud (`refresh-data.yml` monthly, `publish-counties.yml` daily); locally only build and gates. No dry runs. No emails (owner 11-07): a failed job notes its run page; jobs fail closed.
- One background job; no polling; one writer; pull before work. Backlog `state/reviews/backlog.md` (S14: item 3 rounds old fails).

## Every fix
- Wrong live text a reader could act on goes first (`--hotfix`). Work the latest `hater-round<N>.md`, not a new review; each BLOCKER/MAJOR gets a `fixlog-round<N>.md` line (defect, root cause, fix, proof), fix the class at its source.
- Screen-1 figures live in `tools/metrics.py`, recomputed independently. Beat #1: search the real query; give what the top 3 give, or a gap line.

## One-shot a batch
- Write each item's likely failure first; `ast.parse` each edited file.
- Screen 1 holds only answers and their links. P4: the quote checker must stay inside screen 2 (390x844), so a longer screen-1 line needs a cut elsewhere.
- Read gate.py's word rules first: A6 new-policy words, B2 size words ("most" fails unless via `claim()`), E2 repeats, V1 untagged numbers (even "Top 2"). New metric field: `metrics.py --refresh`.
- Fast loop: `build_counties.py --only <geoid>` (states/home: `build_states.py`, `build_site.py`) + gate + phone check; then ONE release.py, one light check, ship, one live read.
- No visible change: `hater.py carry <round> <last passed> <slugs>`; text differs = light review. Never record a review for a template changed after it.

## Reviews (HARD)
- Name the defect gates cannot catch first; none = no review. Say level and cost. Once per batch; a FAIL re-reviews only that page.
- Light: one cheap-model agent, changed cards, sample pages, text only, under ~50k tokens. Full (~320k): only a major redesign or new data source, with the owner's OK.
- S12 fails any indexable page without a current PASS. Samples home, louisiana, palm-beach-county-fl, new-york-county-ny passing the template hash cover every page, except `review.flags()` pages (unpaid share 20+ points off the state's; claims per policy under 0.2x or over 5x): own PASS or a same-kind example at most 2x as far out.
- Run: `hater.py prep <round> <slugs> --local --light`, a fresh agent that did not build the page, `hater.py record <round>`. PASS = zero BLOCKER and MAJOR. The reviewer reads the fixlog only after its own list.

## Reader tools ship standard (HARD)
(1) truth table first, each output tied to a rules_registry source; (2) a Python oracle equals the page's JS; (3) edge suites (Feb 29, Dec 31, Hawaii/Guam; $1,234.56, 0, negative, 1e9, letters, monthly-for-yearly; all queued counties); (4) fuzz: no crash, NaN, undefined, Infinity or verdict word; (5) Chromium + WebKit + JS off; (6) kill switch `tools/tools_flags.json`; (7) 3 sample pages for 2 weeks, then all; (8) rule wording checked by a second model. One tool URL, never a page per input pair.
