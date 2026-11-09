# floodinsurancedata.com: rules
State and next moves: PLAN.md (read at session start, update after every batch). History: git. Two docs only; this file under 8 KB. Global CLAUDE.md applies, not repeated.
Session start: report deploys since last session (`gh run list`, `git log` "publish:", live sitemap count); fix any failed run.
Run from this folder; nothing shared with calcscrape or river. Owner is a non-coder: decide defaults, short plain replies. Claude is project manager (owner 11-08): no "next" lines or open-item menus; finish every open item Claude owns before reporting; a report ends "Nothing left missing" only when true, plus owner-only items named once.

## Reader (HARD)
US homeowner or buyer at one place, on a phone, 30-60 seconds, urgent. Above tables, in order: how risky, am I required, cost in my zone, is it rising, what floods pay here, can I pay less; plus urgency and next steps (where to buy, 30-day wait, limits). One static page per place from public federal data. Reader beats SEO. Reviews judge the checklist in `docs/HATER-PROMPT.md`.

## Truth (HARD)
- Wrong, mislabelled or misleading is the one unforgivable sin. Label every base (median/mean, premium/cost, homes/all policies). Never fake, estimate or recall a figure; null and a gap line beat a guess.
- Every public dataset that changes the decision is shown with source and as-of date; withhold only if wrong, misleading, padding or no mechanism. A reader question with no dataset = a printed gap line; a dataset answering no question = left out.
- No quote, advice prose, "safe / you should" verdict, hedging, premium-rise or premium-estimate calculator. Quote checker and ZIP lookup stay.
- Every page prints what the data cannot say: your premium, private prices, your exact zone (link FEMA's map), why prices rise. Aggregates only, never record- or address-level NFIP data.
- Address tool (owner 11-06, 11-08): never compute, draw or store a zone; for a confirmed pin show FEMA's live zone, panel, date, base flood elevation / AO depth (feet only, one zone only) and map letters (LOMR date at the pin; LOMA counts within 150 m, never names or case numbers) as returned, labelled "FEMA's map, not an official determination", every zone within 15 m; a failed lookup prints nothing.
- Datasets: NFIP Policies v3, Claims v3 (FEMA codes 98/99 out), NRI, Disaster Declarations, Housing Assistance Owners (flood only), Community Status Book, IA Multiple-Loss, NOAA Sea Level, FEMA NFHL (US cloud). Cut on purpose (`card_spec.py`): Census take-up, NOAA storm events, tile maps; FEMA's take-up (penetration) card restored by the owner 11-08.
- Data traps: SUM `policyCount`, never count rows; negative premiums are refunds; claims `countyCode` may not match the property county.
- Builder: numbers via `tp()`/`m()`; size words `claim()`; law `rule()` (exact quote read this session); county word `UNIT`; shares `_share_words()`. Never type a number, date, law or source into a template. New figure: state base and blanks, recompute from raw first. No paragraph twice; shared definitions on `/methodology/`.
- Rule guardrails (each failure happened): raw source text only (a search summary is a lead); scope in the sentence (program, form, occupancy, lender, state); keep the source's strength ("at least", "may"); every sentence quoted, inference cut; two official sources disagree = print only what both support; one example is not a rule; `recheck` re-reads live text, unreachable sources go in `state/manual-rule-read.json` (183 days max); new FEMA codes labelled from the data dictionary. FEMA and bot-walled sites: read via the US runner (`fema-probe.yml`).

## Site (HARD)
- 51 states; counties (median floor `metrics.CONST["min_priced"]` = 30, gate C14); ZIPs fold into the county page; no city pages; ceiling ~2,000.
- Counties last (owner 11-07): 20 a day, queue "kw" > 0 only; live pages stay indexed.
- No stuffing, doorway, near-duplicate pages, fake freshness, hidden text. One colour system; answers on screen 1; static, no client frameworks. No card or page-length caps.
- No paid referrals before a licensing + FTC check; no ads before a 4-week Search Console review.
- Owner alone: domain, Search Console, ads and consent banner, publisher identity (site anonymous), opening pages to the index, paid referrals, cutting any block.

## Internal links (HARD, owner 11-08; google_gate S16 = `tools/linkcheck.py`, tests in test_calc.py)
- State/county pages link home, state, up to 6 bordering counties, each named zone's page, every `linkcheck.HUBS` hub. Home links every state and hub; a state every live county; zone pages their top 10 counties (Z8). S16 fails a missing hub, broken link, orphan.
- Anchor = destination in searcher's words ("Zone AE", "Harris County"), never "here". Links in the sentence that needs them; no link blocks or footer farms.
- A new page type joins `HUBS` with home and state links the same day; a hub linked from under half of state + county pages is a defect.

## Backlinks (HARD, owner 11-08)
Every keyword group gets a link asset, target list and pitch with one exact figure (PLAN "Backlinks"); Claude builds, owner sends. Never buy, swap or farm links.

## Decide before building (HARD)
Name the scoreboard number it moves; none = delete it. Each defect becomes a check with a mutation test the same day; reader-harm logic gets one oracle check. Phone bytes (gzipped) and tokens are the hot paths; never trade a wrong-number check for speed. A build writes no tracked file; a step skips when its input did not change.

## Commands
- `python -I` always. Build `build_all.py`; gates `release.py` (build, gate, truth proof, mutations, factory, phone, google_gate); `recheck.py` independent recompute.
- Ship only `release.py --ship` (`--hotfix "reason"` skips only the review, only for wrong live text; `--live` = live gate). No wrangler by hand.
- Data runs in the cloud (`refresh-data.yml`, `publish-counties.yml`); locally only build and gates. No emails; jobs fail closed. One background job, one writer, pull first. Backlog `state/reviews/backlog.md` (S14).

## Every fix
- Wrong live text first (`--hotfix`). Work the latest `hater-round<N>.md`; each BLOCKER/MAJOR gets a `fixlog-round<N>.md` line (defect, root cause, fix, proof); fix the class at its source. Anything the gates passed: `docs/GATE-FIX-PROMPT.md`.
- Screen-1 figures live in `metrics.py`, recomputed independently. Beat #1: give what the top 3 give, or a gap line.

## One-shot a batch
- Likely failure first; `ast.parse` each edited file. Read gate.py word rules first (A6, B2 `claim()`, E2, V1, F1 40-word openings, truth-proof banned phrases). New metric field: `metrics.py --refresh`.
- Screen 1 = answers only; P4: quote checker inside screen 2 (390x844).
- Fast loop: `build_counties.py --only <slugs>` (+ `--all` for queued, in review/) + gate; then ONE release.py, one light review, ship, one live read.

## Reviews (HARD)
- Name the defect gates cannot catch first; none = no review. Say level and cost. Once per batch; a FAIL re-reviews that page only.
- Light: one cheap-model agent, changed cards, text only, ~50k (measured 115k at 7 pages: keep to changed cards). Full (~320k): redesign or new source, owner's OK.
- S12: samples home, louisiana, palm-beach-county-fl, new-york-county-ny on the template hash cover all, except `review.flags()` pages: own PASS or a same-kind example at most 2x out.
- `hater.py prep <round> <slugs> --local --light`, fresh agent, `hater.py record <round>`; unchanged text: `hater.py carry <round> passed <slugs>`. PASS = zero BLOCKER/MAJOR; fixlog read after its own list.

## Reader tools ship standard (HARD)
Truth table tied to rules_registry; Python oracle = page JS; edge suites (Feb 29, Dec 31, Hawaii/Guam, 0, negative, 1e9, letters, monthly-for-yearly); fuzz (no crash/NaN/verdict word); Chromium + WebKit + JS off; kill switch `tools/tools_flags.json`; 3 samples for 2 weeks, then all; rule wording checked by a second model. One tool URL.

## Labels are claims (HARD, owner 11-08: "we keep shipping what gates miss")
Gates checked number = data, not label = data. Every "left out / only / excluded / not final / costliest / largest / since" is checked against the data it labels (gate C10-C14); a table or range that drops rows says which; rank by value, never file order. Reviewers: label-vs-data is MAJOR, never MINOR. A new data shape (empty, one row, reordered, huge, date edge) becomes a case in `tools/test_factory.py` (per-place pages) or `tools/test_site_factory.py` (national pages) the same day; both run in release.
