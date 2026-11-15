# floodinsurancedata.com: rules
State and next moves: PLAN.md (read at session start, update after every batch). History: git. Two docs only; this file under 8 KB. Global CLAUDE.md applies, not repeated.
Session start: deploys since last session (`gh run list`, live sitemap count) + `tools/actions_check.py`; fix any failed run. Nothing shared with calcscrape or river. "Nothing left missing" only when PLAN "Next" is done (hook plan-gate.mjs).
ONLY GOAL (HARD, owner 11-09): helpfulness, information gain, Google HCU; every change names which it moves, none = don't build. Never "nothing to do": run the top-3 compare (PLAN Next) on a keyword group and build its gaps.

## Reader (HARD)
US homeowner or buyer at one place, on a phone, 30-60 s, urgent. Above tables, in order: how risky, am I required, cost in my zone, is it rising, what floods pay here, can I pay less; then next steps (where to buy, 30-day wait, limits). Every page opens with the answer in plain words (NFIP spelled out once) and, where rows exist, a find-your-county lookup on screen 1 (owner 11-14). Reader beats SEO. Reviews use `docs/HATER-PROMPT.md`.

## Truth (HARD)
- Wrong, mislabelled or misleading is the one unforgivable sin. Label every base (median/mean, premium/cost, homes/all policies). Never fake, estimate or recall a figure; null and a gap line beat a guess.
- A label names what the source records, never more (11-14: IA rows called "damage records", ~30% have no damage; LOMA layer rows called LOMAs though LOMR-F is mixed in; Pima and Maricopa both called "bordering"). Use the source's own category; a mixed group gets one label per part.
- Every dataset that changes the decision shows source and as-of; a question with no dataset = a printed gap line; a dataset answering no question = left out. Every page prints what the data cannot say (your premium, private prices, your exact zone).
- No quote, advice, verdict, hedging, premium-rise or premium estimate. Aggregates only. Address tool: FEMA's live answer as returned, "FEMA's map, not an official determination"; a failed lookup prints nothing.
- Datasets, cuts, address-tool and rule detail: PLAN "Reference". Traps: SUM `policyCount`; negative premiums are refunds; claims `countyCode` may differ from the property county.
- Builder: numbers `tp()`/`m()`, size words `claim()`, law `rule()` (exact quote read this session), county word `UNIT`. Never type a number, date, law or source into a template. No paragraph twice.
- Rules: raw source text only; scope in the sentence; keep the source's strength; every sentence quoted, inference cut; two sources disagree = print what both support. FEMA/bot-walled: US runner `fema-probe.yml`.

## Site (HARD)
- 51 states, counties (median floor 30), no city pages, ceiling ~2,000. At most 25 new pages a day, all kinds (`new_pages_cap.py`, owner 11-14). Counties 20/day after the money groups.
- Template text (on every county/state page) changes at most once a day, batched, reviewed (PLAN "Template batch"); same-day fix-on-fix only for wrong live text (11-14: 6 site-wide releases in a day, one dropped 312 state links).
- No stuffing, doorway, near-duplicates, fake freshness, hidden text. No ads before the 4-week Search Console review; no paid referrals before a licensing + FTC check.
- Owner alone: domain, Search Console, ads, publisher identity, opening pages to the index, paid referrals, cutting any block, money, sends.

## Internal links (HARD, owner 11-14, replaces 11-08; S16 = `tools/linkcheck.py`)
Follow Google's "Link best practices" (developers.google.com/search/docs/crawling-indexing/links-crawlable, read 11-14): every page linked from at least one other page; link related pages "in context"; anchor "descriptive, reasonably concise, and relevant" and makes sense alone; never "click here"/"read more"/empty; no keyword cramming; don't chain links in a sentence; real `<a href>` only; "no magical ideal number of links". Test: would a reader click it right there?
- Structure only is enforced: breadcrumb home > state > county; home lists every state and hub; a state every county; /guides/ every guide; zone pages their top counties. S16 fails a broken link, an orphan, or a county without its state link.
- Topic links per page only: where the page's own sentence covers the topic, on words already there; never a sentence added for a link, never "on every page", no link-count target (calcscrape model).
- No link blocks, footer farms, "related" boxes. A link must not promise what the target lacks (a paper that does not list the county is named, not linked).

## Outreach and backlinks (HARD)
Claude drafts; sends from the owner's Gmail only after the owner approves each batch's final list and text; one email per organization, ever (outreach guard). Before any batch, every linked page passes `hater.py prep <round> <pages> --editor` (phone, desktop, dark, no-JS screenshots + Forbes-editor reviewer) and `tools/outreach_gate.py` on send day. Never buy, swap or farm links.

## Owner accounts (HARD, 11-14)
Read-only in the owner's Google Ads, Search Console, Cloudflare, GitHub, Gmail: no saving plans, no setting or location changes, no sign-ups. A tool that would save or change anything: stop and say so first (a Keyword Planner run saved a plan and switched its location).

## Decide before building (HARD)
Name the scoreboard number; none = delete it. Each defect becomes a check with a mutation test the same day. A step skips when its input did not change.

## Commands
- `python -I` always. Build `build_all.py`; gates `release.py`; ship only `release.py --ship` (`--hotfix "reason"` only for wrong live text, skips only the content review). Deploy is deploy.yml; release.py deploys locally only when GitHub never starts it. No wrangler by hand.
- Code bug review before ship: `release.py --ship` stops unless `code_stamp.py` matches; stamp only code you reviewed this session (`/code-review medium`, every finding fixed). Never restamp another agent's or a later edit unread.
- While release.py runs: no edits to tools/, dist/, CLAUDE.md-listed state files; one release at a time; a stopped release is rerun whole (11-14 mixed commit).
- Data runs in the cloud (2,000 Actions min/month: batch new fields into one forced refresh). One background job, one writer per file, pull first. Never regex or backslash code through a heredoc: Write/Edit.

## Agents and workflows (HARD, 11-14)
Before launch, 5-step every prompt: say the cost; builders and reviewers never run release.py, test_factory, test_site_factory or phone_check (the ship step runs them once); no background shells or polling; read-only agents say so. Flag a redundant running task at once with its cost.

## Every fix
- Wrong live text first. Each review BLOCKER/MAJOR gets a `fixlog-round<N>.md` line (defect, root cause, fix, proof); fix the class at its source; a third fix of one thing = wrong target.
- Beat #1: give what the top 3 give, or a gap line.

## One-shot a batch
Likely failure first; `ast.parse` each edit; gate.py word rules first (V1 no typed numbers, F1 40-word openings). New metric: `metrics.py --refresh`. Loop: `build_counties.py --only a,b` + gate; one release, one review, ship, one live read.

## Reviews (HARD)
- Name the defect gates cannot catch first; none = no review. Say level and cost. Once per batch; a FAIL re-reviews that page only.
- Light (~50k): one cheap-model agent, changed text only. Full/editor (~250-320k): new page type, redesign or outreach.
- S12: samples home, louisiana, palm-beach-county-fl, new-york-county-ny cover the template; a carry needs a word-level visible-text diff of every committed page showing only the reviewed change.

## Reader tools (HARD)
Truth table tied to rules_registry; Python oracle = page JS; edge suites; fuzz; Chromium + WebKit + JS off; kill switch `tools_flags.json`.

## Labels are claims (HARD, owner 11-08)
Every "left out / only / excluded / costliest / largest / since / bordering" is checked against its data (gates C10-C14); a table that drops rows says which; rank by value. Label-vs-data is MAJOR. A new data shape becomes a case in `test_factory.py` / `test_site_factory.py` the same day.
