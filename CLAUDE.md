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
question with real data they don't show. A page that shows only an average has failed. If a public
dataset bears on the decision and we are not showing it, that is a bug (see Line 0b). No quote, no
advice prose, no "safe / you should" verdict, no hedging.

## Line 0b — we are the dataset catalog (the moat)
Competitors (NerdWallet, LendingTree, Policygenius, floodfigures.com) show one stale average and a
count. We join every public dataset that bears on the decision. Eight, all verified live 2026-10-22:
1. NFIP Policies v3 — cost spread p25/p50/p75/p90 (they show only a median).
2. NFIP Policies v3 `fullRiskPremium` — the gap to FEMA's true price, share paying below it.
3. NFIP Claims v3 — claims per 100 policies + paid-by-year (they show raw counts).
4. National Risk Index — flood expected-annual-loss + national percentile, per county.
5. DisasterDeclarationsSummaries — flood/hurricane declarations, per county.
6. HousingAssistanceOwners — FEMA aid paid to owners after floods, per ZIP/county.
7. NfipCommunityStatusBook — the CRS discount (5–45% off premiums), per community. NOBODY shows it.
8. PIF workbook — reconciliation of our count to FEMA's official figure.
A reader question with no dataset = a visible gap line naming the data to pull next. A dataset that
answers no reader question = left out. Verified endpoints: `docs/reader-spec.md`.

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

## Gates — three only (no gate zoo)
1. It builds.  2. Numbers on the page equal the JSON and reconcile to FEMA's official count within 5%
(documented cause otherwise).  3. The live page is up and its body reads real content this session.
A rule without a check is a note. "Live" = curl/browser confirms real content this session.

## What the data cannot say (printed on every page)
Your own premium; private (non-NFIP) prices; your address's exact zone (link FEMA's map); why prices
rise (we show the gap, not the cause). Aggregates only, never a record-level or address-level figure.

## Owner alone decides (`docs/OPEN-ITEMS.md`)
Domain, Search Console property, ad account and consent banner, publisher name/email, opening pages to
the index, cutting any block. No ads until a four-week Search Console review passes.
