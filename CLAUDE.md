# Flood insurance data site

One static page per place, built from public federal data. Own domain, own Search Console, own ad
account, no shared template or link with the car-repair (calcscrape) or river sites — that separation
is the GSC-cliff protection. The owner is a non-coder and never runs commands: do the work, short
plain replies, decide sensible defaults, no "Next:" line. Model: riverwaterlevels (one page per
entity, government data only, no verdict). This file is the whole spec; keep it under ~200 lines,
reader first, orders not descriptions, one file, no competing side docs.

## Line 0 — be the single most helpful flood-insurance page for this place. That is the whole job.
Not "rank," not "run ads," not "cover more pages" — those are downstream and must never be the goal
that shapes a page. The goal is: a homeowner at THIS place gets every answer a flood-insurance decision
needs, each from public federal data with its exact source and as-of date — how risky it is, whether
they're required to buy it, what it costs (and what it costs in THEIR flood zone), how far below FEMA's
true-risk price, what floods have actually paid out, and how to pay less. More helpful than NerdWallet,
Policygenius, Bankrate or floodfigures.com — not by having more URLs, but by answering more of the real
question with real data they don't show. A page that shows only an average has failed. The reader is a DESPERATE person — at a closing with a
flood-zone letter, a renewal that jumped, a purchase to decide, or a street that flooded last night — on a
phone, 60 seconds. So "most helpful" means they also learn, fast and in plain words, how urgent it is and
exactly what to do next (how and where to buy, the 30-day waiting period, the coverage limits), not only
complete data. Showing that reader anything buggy, wrong, mislabeled, or misleading is the one unforgivable
sin. A page that is factually complete but that a scared reader can't understand or act on in a minute has
also failed. If a public dataset bears on the decision and we are not showing it, that is a bug (see Line
0b). No quote, no advice prose, no "safe / you should" verdict, no hedging.

**Maximize information gain. Hunt the data gaps.** The target is the single most useful flood-insurance
page on the internet for this place — every public figure that changes a homeowner's decision, present
and sourced. Each pass asks: what does a reader still not know, and which public dataset would tell
them? Name every gap and the exact data to pull next (that is the honest answer to "are we done"); the
loop never closes while a decision-relevant public dataset is unshown. The only valid reasons to leave
one out are the hard four — wrong, misleading, padding (denser but changes no decision), or no mechanism
— never "small sample", "confounded", or "not actionable". When a gap can't be closed by us (an owner
key, a per-address lookup, a dataset that doesn't exist yet), it stays a printed gap line naming the
source, not a silence.

## Line 0b — we are the dataset catalog (the moat)
Competitors (NerdWallet, LendingTree, Policygenius, floodfigures.com) show one stale average and a
count. We join every public dataset that bears on the decision. **TEN distinct federal datasets** (the
page says "joins 10 of them" and the gate enforces that the stated count equals the sources listed — keep
it at 8 everywhere). Item 2 is a field of item 1, not a separate fetch; the PIF workbook is a
reconciliation benchmark, not a dataset. All verified live 2026-10-22 (item 9 added 2026-10-24):
1. NFIP Policies v3 — cost spread p25/p50/p75/p90 (they show only a median).
2. NFIP Policies v3 `fullRiskPremium` — the gap to FEMA's true price, share paying below it. (Same dataset as 1 — a field, not a separate source.)
3. NFIP Claims v3 — claims per 100 policies + paid-by-year (they show raw counts).
4. National Risk Index — flood expected-annual-loss + national percentile, per county.
5. DisasterDeclarationsSummaries — flood/hurricane declarations, per county.
6. HousingAssistanceOwners — FEMA aid paid to owners after floods, per ZIP/county.
7. NfipCommunityStatusBook — the CRS discount (5–45% off premiums), per community. NOBODY shows it.
8. Census ACS 5-year B25001 — take-up (NFIP policies per 100 homes), per county. Needs a free Census
   key in `.env` (`CENSUS_KEY`); if absent the panel shows a gap line.
9. IndividualAssistanceMultipleLossFloodProperties v1 — repetitive-loss (RL) + severe repetitive-loss
   (SRL) counts per county, the chronic-repeat-flood signal nobody else joins.
(Eight DISTINCT datasets: items 1–9 minus item 2, which is a field of item 1.)
Reconciliation benchmark (not counted as a dataset): FEMA PIF workbook — checks our count to FEMA's official figure.
A reader question with no dataset = a visible gap line naming the data to pull next. A dataset that
answers no reader question = left out. Verified endpoints: `docs/reader-spec.md`.

## Line 1 — user first, clean presentable UI, never Google first
Every choice serves the person reading, not a crawler. The page is clean and legible: one colour
system, generous whitespace, the headline answer and the first decision-driving panels on the first
screen, readable on a phone, fast (static, no client frameworks). We never do anything FOR Google that
we wouldn't do for the reader — no keyword stuffing, doorway or near-duplicate pages, fake freshness,
hidden text, or clutter added to chase rankings. If a layout or wording choice helps SEO but hurts the
reader, the reader wins. Good ranking is a side effect of being the clearest, most useful page — never
the thing we design for. When the two ever conflict, this line decides.

## The reader is the judge
A homeowner or buyer at a specific place, on a phone, holding a flood-zone letter or a renewal,
30–60 seconds, a deadline of days. Page order, answered above the long tables, from the page's own
data: (1) how risky here, (2) am I required to buy it, (3) how much does it cost, (4) is it rising,
(5) what do floods pay out here, (6) can I pay less. A block stays only if a person deciding HERE
would act on it and one plain sentence ties the dataset to that decision. "All the APIs" is not a
licence to pad.

## Pages — lean, not vast (quality beats volume)
- `/flood-insurance/<state>/` — 51 state rollups: county table + state tile/risk map.
- `/flood-insurance/<state>/<county>/` — the core page. County floor: >=100 single-family policies.
- ZIP folds INTO the county page as a section, EXCEPT a standalone `/.../<zip>/` that passes the
  **3-part publish test** (all three, not just one): (1) statistical sufficiency — enough eligible
  policies for a stable estimate, not merely >=20; (2) decision-relevant difference — the ZIP changes
  the reader's answer on cost, full-risk gap, claims or CRS discount in a way that matters, not just a
  different number; (3) distinct intent/answer — it gives something the county page does not. Fails any
  one -> fold into the county. This, not an arbitrary count, is what decides a page exists.
- No city pages (no city field; the ZIP->city join is the mass-produced pattern Google and pSEO forbid).
- Data stories (ranked, linkable, same data): counties paying furthest below full-risk; most claims
  paid since 1978; biggest CRS discounts; event pages ("Hurricane Ian claims by county").
- `/compare/` quote-position widget; `/methodology/`; `/data/` (downloadable CSV + embed widget).
Ceiling ~2,000 quality pages (51 + ~1,500 counties + a few hundred real ZIPs), not ~14,000 thin ones.
Launch wave 1 ~350 (all states + top flood counties); scale only where Search Console shows demand.

## How a new domain actually ranks (honest, no #1 guarantee)
1. Unique data competitors lack (the catalog above) — the only durable moat.
2. E-E-A-T: exact source + as-of on every number, a real methodology page, public reconciliation.
3. Backlinks from data stories — the one way past NerdWallet/Bankrate authority. Pitch the rankings.
4. Zero thin/duplicate pages (the GSC-cliff risk). Lean count, each page 8 datasets deep.
5. Fast static pages, 3–5 sibling internal links each, sitemap index, real `lastmod` = real data change.
6. GEO: llms.txt + Dataset/Place/FAQ schema, self-contained quotable stat sentences, embed widget —
   win AI-Overview/ChatGPT/Perplexity citations where a new domain can rank before organic does.

## Data pipeline (monthly, one command)
`tools/collect.py` is the only network code: pulls per place, computes compact aggregates -> JSON.
Parameterized by env (FF_STATE, FF_GEOID, FF_COUNTY, FF_COUNTYLABEL, FF_OFFICIAL) so every county
runs the same code. `tools/collect_small.py` pulls CRS/declarations/housing; `tools/nri.py` pulls the
National Risk Index flood fields and merges them in. `tools/build_page.py` reads the JSON only and
renders static HTML (inline-SVG charts, no client lib).
NRI source (keyless, reachable): `services.arcgis.com/XG15cJAlne2vxtgt` (FEMA_NationalRiskIndex org),
layer `National_Risk_Index_Counties`, match on `STCOFIPS`. NOT hazards.fema.gov (TLS-blocks some envs)
and NOT the third-party `EiGeaCDLpVDPqdJ5` copy (a non-national sample).
Traps baked into a check: SUM `policyCount`, never count rows (condo rows carry >1 unit; Lee rows
undercount ~32%); `propertyState` required in every policies query or it 503s; page at `$top=1000`
with NO `$orderby` (orderby forces a server sort of the filtered set and 503s), dedupe by id;
negative premiums are refunds; claims `countyCode` may not match property county; suppress cost charts
under 100 cohort policies, ZIP under 20.

## Musk's five steps, in order, in service of the reader (HARD, owner 2026-10-27: "smart like Elon Musk ... we still want maximum helpfulness for the user")
The goal is the most helpful page a frightened reader can find, not the shortest page or the most pages. The five
steps remove waste between the reader and the answer; they never remove an answer. Before any build, gate or page
change, in this order:
1. **Question the requirement.** For every card, rule and gate: which reader question does it answer, and is that
   answer correct for THIS place? A requirement with no reader behind it (page count, a word floor, a check nobody
   can name a defect for) is suspect. Code gates do not catch everything (proven); a hostile reader does.
2. **Delete what stands between the reader and the answer, never the answer.** Delete: wrong or misleading text,
   the same sentence twice, a second copy of a rule, filler, jargon, a figure with no use to the reader, a duplicate
   page. Do NOT delete true, useful local data to shorten a page; fix it (e.g. disaster aid limited to flood events,
   not dropped). No card or page-length caps. Test per card: would this reader miss it if it vanished?
3. **Simplify.** Order by the reader's urgency: cost, am I required, how fast it starts, does it pay out, my zone or
   ZIP, then the deeper data. One template, reviewed deeply on 3 pages; fix each defect at its source for every page;
   then a lighter per-page review of only what varies (odd numbers, gaps, strange names).
4. **Accelerate.** Each defect a review finds becomes a builder rule or gate check with a mutation test the same day,
   so the next review starts higher.
5. **Automate last.** The daily 10-county job ships only reviewed pages (S12). Never automate a step before 1-4.
Next layer (ZIP pages, ~2,500 with 100+ priced policies) waits until county pages pass review and Google shows indexing.

## Nothing goes live without a hater review (HARD, owner 2026-10-27: "we are not going to put out any pages live unless it's scrutinized like the worst hater in the world")
The code gates check only what someone thought to code; they passed "since None" and a false "Yes". So every page
(home, each state, each county) ships only with a current PASS in `state/reviews/<slug>.json` (`tools/review.py`):
- The reviewer is hostile and was not the builder: a fresh agent running `docs/HATER-PROMPT.md` (six judges: frightened
  reader, FEMA analyst, competitor, Google rater, copy editor, and an SEO strategist who searches the page's real
  query and must show it beats today's #1 result). PASS only with zero BLOCKER and zero MAJOR.
- Steps: `python -I tools/hater.py prep <round> <slugs>` (live phone screenshots + filled brief), run the brief in a
  fresh agent, `python -I tools/hater.py record <round>` (writes the verdicts). Fix every defect at its source, gate it,
  and run the next round on the same pages until they pass.
- Review the TEMPLATE, not every page (owner 2026-10-27, Musk steps): the hater reads 3 samples in depth (home,
  louisiana, palm-beach-county-fl). When all 3 PASS under the current template hash, every page built from it may ship,
  except pages `review.flags()` marks (unpaid share 20+ points from the state's, claims per policy under 0.2x or over 5x
  the state's): each of those needs its own quick look and PASS. Any template change resets only the 3 samples.
  After a small fix, re-check only the changed cards on the samples (cheap model), never a full round.
- Enforced: `google_gate.py` S12 fails a release with any indexable page lacking a current PASS, and `add_counties.py`
  (the daily GitHub job) only queues reviewed counties. Every defect class found becomes a builder rule or gate check.

## The gate — one, small, nothing unchecked (2026-10-26; why: docs/GATE-PROMPT.md)
Two rounds proved a big gate misses things: 29 checks passed 9 shipped defect classes, then 45 checks passed a page a
reader found 15 defects on. So correctness lives in the BUILDER, and the gate asks 9 questions:
- **Builder rules (make wrong text impossible):** every number through `tp(key, path)` (reads the data path, tags it)
  or `m(key, shown)` for a derived figure; words of size/direction only through `claim()`; law text only through
  `rule()`; source lines built from metrics; places named from Census/NRI, never codes; county/parish/borough from
  `UNIT`; shares through `_share_words()`. Never type a number, date, law or source into a template.
- **`tools/gate.py`** (every page, at build AND on the live HTML via `gate_live.py`): 1 inputs complete, 2 every number
  tagged (V1) and equal to the data at its path (V2), 3 nouns/bases/panels agree, 4 words agree with numbers,
  5 sources and rules generated, 6 reader words (no codes, jargon, dead pointers, undated storms, None), 7 each card
  opens with a 40-word answer. 8 **`phone_check.py`**: 390px, nothing wider, text 11px+, answers on screen 1, no
  collapsed data, no overlapping chart labels. 9 **live**: `release.py --live` gates every live page.
- **Outside the per-page gate:** `test_gate.py` (each check proven by a mutation of a real shipped bug; the pull
  covers all 51 states; no imported module does I/O; every metric field has a recorded FEMA definition) and
  `recheck.py` (independent recompute from the API, FEMA definition drift, rule excerpts still on official pages).
- **What code can't judge** ("true but misleading", order, tone): after any template change, read one random page
  per template on a phone, screen by screen, as the frightened reader. Each defect becomes a class, is scanned
  across all pages, then becomes a builder rule or a gate check with a mutation, never a one-off patch.
Ship ONLY with `python -I tools/release.py --ship` (build + every gate + Google gate incl. hater review, commit dist,
push, deploy, live gate). Never run wrangler or push by hand: every push redeploys the committed dist (2026-10-27 a
docs push put old pages back live). `--hotfix "reason"` skips only the hater review, only to remove wrong live text.
`recheck.py` runs as its own background job.

## What the data cannot say (printed on every page)
Your own premium; private (non-NFIP) prices; your address's exact zone (link FEMA's map); why prices
rise (we show the gap, not the cause). Aggregates only, never a record-level or address-level figure.

## Owner alone decides (`docs/OPEN-ITEMS.md`)
Domain, Search Console property, ad account and consent banner, publisher name/email, opening pages to
the index, cutting any block. No ads until a four-week Search Console review passes.
