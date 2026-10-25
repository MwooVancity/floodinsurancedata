# floodinsurancedata.com — Master Brief (exhaustive, portable)

Paste this whole file to seed a fresh AI or session with the complete project at full depth. It is the
portable brief; `CLAUDE.md` stays the lean operational spec. Last updated 2026-10-23.

---

## 0. One line
A static website that is the single most helpful, most trustworthy page on the internet about flood
insurance **for a specific US place**, built entirely from public federal data, every number sourced and
dated, no verdicts, no quotes, no sales. Live at https://floodinsurancedata.com.

## 1. The reader (who we build for — not Google)
A US homeowner or home-buyer at a specific place, on a phone, holding a lender's flood-zone letter or a
renewal notice, 30–60 seconds, a decision in days. Not a pro, not a researcher. Their questions, in order:
(1) how much flood risk is here, (2) am I required to carry it, (3) how much does it cost here, (4) is it
rising, (5) what do floods actually pay out here, (6) can I pay less. Every page answers these from its own
data, money questions high. If a homeowner deciding HERE wouldn't act on a block, it goes.

## 2. Product thesis — the dataset catalog is the moat
Competitors show one stale average. We join every public federal dataset that bears on the decision and
show each with its exact source and as-of date. A reader question with no dataset becomes a visible gap
line naming the data to pull next; a dataset that answers no reader question is left out. Valid reasons to
withhold a dataset: wrong, misleading (reporting-habit artifact), padding (changes no decision), or no
mechanism. NOT valid: "confounded", "small sample", "not actionable" — print the caveat and show it.

## 3. Honest strategic reality (do not pretend otherwise)
- **#1 for commercial "flood insurance cost [place]" is NOT winnable** for a new no-authority domain:
  commercial intent + publisher/carrier authority (NerdWallet, Bankrate, Policygenius, lead-gen) + 2026
  core updates demoting data aggregators. This ceiling is the same for every tier-1 money topic.
- **What IS winnable:** the informational long-tail (county NFIP facts publishers never compute) and
  **AI-answer citations** on Perplexity/ChatGPT, where a heavily-sourced sub-authority specialist out-cites
  big publishers (NOT Google AI Overviews, which ~86% track organic). Timeline: 6–12+ months.
- **Prove before scaling:** build 25–50 deep, genuinely distinct county pages, index them, earn a few real
  links/citations, and confirm ranking BEFORE building the next thousand. Scaling thin is the fatal trap.
- **Direct competitors (both rank for nothing yet, a cautionary tale):** floodfigures.com (NFIP
  counts/median, ~1,729 ZIP + 7,663 city pages, no counties) and floodcostzip.com (median + full-risk +
  5-yr projection + storm surge, ZIP + county). floodcostzip already matches much of our cost layer, so our
  durable edge is breadth + county layer + CRS + transparency, not "we show full-risk."

## 4. The data catalog
**EIGHT distinct federal datasets** (the page states "joins 8", the gate enforces stated-count == sources
listed). Items that look like more are a field or a benchmark, not separate fetches.
1. NFIP Policies v3 (OpenFEMA, keyless) — cost spread p25/p50/p75/p90; `fullRiskPremium` field = gap to
   FEMA's true price + share paying below; `ratedFloodZone` = zone mix; per-ZIP units/median.
2. NFIP Claims v3 (OpenFEMA) — paid-by-year since 1978, total paid, claims-per-100 (a cumulative tally,
   never an annual rate).
3. FEMA National Risk Index (ArcGIS org `services.arcgis.com/XG15cJAlne2vxtgt`, layer
   `National_Risk_Index_Counties`, match `STCOFIPS`) — flood expected annual loss + national percentile,
   coastal `CFLD_*` + inland `IFLD_*`. NOT hazards.fema.gov (TLS-blocks), NOT the Utah-sample copy.
4. NFIP Community Status Book v1 (OpenFEMA) — the CRS discount (5–45% off), per community. Nobody else shows it.
5. Disaster Declarations Summaries v2 (OpenFEMA) — distinct flood/hurricane/storm declarations per county.
6. Housing Assistance (Owners) v2 (OpenFEMA) — FEMA aid paid to owners after floods.
7. U.S. Census ACS 5-year B25001 — take-up (policies per 100 homes). Needs a free `CENSUS_KEY` in `.env`.
8. IndividualAssistanceMultipleLossFloodProperties v1 (OpenFEMA) — repetitive-loss (RL/SRL) property
   counts per county, a chronic-repeat-flood signal competitors do not join.
Reconciliation benchmark (not a dataset): FEMA official PIF workbook — checks our count within 5%.

**OpenFEMA pull traps baked into code:** SUM `policyCount` (never count rows — condo rows carry >1 unit);
`propertyState` REQUIRED in the policies filter or it 503s; county = first 5 of `censusGeoid` (no
`countyCode` field); page at `$top=1000` with NO `$orderby` (orderby forces a server sort → 503), dedup by
id; negative `policyCost` = refunds (excluded); claims `countyCode` may not match property county.

**Pending data adds (ranked, each needs a VERIFIED fetch before it ships — never fake a number):**
1. NFHL flood-zone mix per county (SFHA land/building share vs our policy-zone mix) — the mandatory-purchase
   answer; FEMA MSC/NFHL, county aggregate; individual zone is address-level (caveat).
2. RR2.0 county/ZIP premium-change files (FEMA NFIP Pricing Approach State Profiles) — "is my premium
   rising here" with sourced numbers.
3. NOAA Storm Events county flood counts + damages; NOAA high-tide-flooding; NHC SLOSH storm-surge category
   (coastal) — all free, county-joinable, with screening-level caveats.
4. FEMA HMA (BRIC/FMA) mitigation dollars per county — caveat: no new HMA funding obligated since Mar 2025.
**Honest gaps to print, never fake:** per-property RR2.0 rating factors (address-level, non-public); First
Street (paid/unclear free tier); USGS gauges + Base Flood Elevation (point-level, no clean county join).

## 5. Page types (lean, not vast — quality beats volume)
- `/flood-insurance/<state>/<county>/` — the core catalog page. Floor: ≥100 single-family priced policies.
- `/flood-insurance/<state>/` — state rollup: county table + risk tile-map. (NOT yet built.)
- `/flood-insurance/<state>/<county>/<zip>/` — ONLY if it passes the 3-part test (statistical sufficiency,
  decision-relevant difference, distinct intent); else fold into the county. (None built.)
- Data-story pages (ranked, linkable, same data): counties paying furthest below full-risk; most claims
  since 1978; biggest CRS discounts; event pages. The backlink engine. (NOT yet built.)
- `/methodology/`, `/data/` (CSV), `/about/`. No city pages (mass-produced pattern, forbidden).
Ceiling ~2,000 quality pages (51 states + ~1,500 counties + a few hundred real ZIPs), never ~14,000 thin.

## 6. County page anatomy and order (money-first, live now)
Hero: median $/yr + $/mo + middle-half + % below full-risk, a "check your address on FEMA's map" button,
and the not-a-quote caveat. Then, in order: how-risky (NRI) → am-I-required (SFHA + zone mix, denominator
disclosed, remainder line) → how-much-cost (spread p25–p90) → cost-by-zone → find-your-ZIP → full-risk
comparison + **years-to-full-risk glide-path** (statutory 18% HFIAA cap, a rule not a model) → can-I-pay-less
(CRS) → what-floods-pay-out (claims by year; per-100 demoted to a note with both numbers) → state tile-map →
take-up → disaster declarations → (collapsible) FEMA aid + reconciliation → what-this-data-cannot-tell-you →
federal-sources block (7 links) → premium-position widget → same-state sibling links.

## 7. Build pipeline (one command)
`python -I tools/build_all.py` reads `tools/counties.json`, and per county runs collect_small.py →
collect.py → nri.py (pull → `data/<slug>/agg.json`, written once atomically with `complete:true`), then
build_page.py (renders static HTML, inline-SVG charts, no client framework) → gate.py. Then the duplication
guard, then build_site.py (home, methodology, data CSV, about, sitemap, robots, llms.txt). Parameterized by
env (FF_STATE/GEOID/COUNTY/COUNTYLABEL/COUNTYSHORT/SLUG/OFFICIAL/DIR/PLACES/BASEURL). Resumable (skips a
county whose agg is complete). Deploy: `npx wrangler deploy` (static assets to Cloudflare Workers
`floodinsurancedata`). Source backed up at github.com/MwooVancity/floodinsurancedata (private).

## 8. The gate — correctness is non-negotiable (`tools/gate.py`, one all-in-one audit)
A page ships only if ALL pass: build succeeds; manifest complete; percentiles monotonic; reconciliation to
FEMA official ≤5%; median on page == agg; **SFHA share == sfha_units/units recomputed** (no wrong
denominator); truncated zone table discloses its remainder; claims total + largest loss year reconcile to
agg; claims-per-100 carries its cumulative caveat; full-risk framed "not a quote"; stated dataset count ==
sources listed; `dateModified` present; NRI present or an explicit gap line; spread chart ⟺ cost_n≥100; no
future-year declaration. The **duplication guard** (build_all.py) drops the lower-data page of any pair
sharing >80% masked (numbers + place names blanked) prose. Thin counties (cost_n<100) are suppressed by the
`data_ok` floor. A rule that isn't a check is only a note.

## 9. Hard content rules
No verdicts, no "you should" advice prose, no hedging. Every number has its exact source + as-of date. No
modeled number passed off as measured (the glide-path is a labeled statutory RULE, not a forecast).
Aggregates only — never an individual property, policy, or quote. One home per figure. Dates move only on a
real data change (no fake freshness). What the data cannot say is printed on every page (your own premium,
private prices, your exact zone, why prices rise). LOOK at the rendered page before shipping; defect list
worst-first (filler, a chart restating its title, a label disagreeing with its number, clipped text).

## 10. SEO / GEO (how a new data domain actually gets found)
Win long-tail informational queries, not head terms. Earn AI citations with self-contained quotable stat
sentences (exact source, plain %), exact-question H2s (7+ word place questions), answer-first 120–180-word
blocks, and a visible freshness date (strongest citation correlate). Structured data: Dataset + Place +
FAQPage + Breadcrumb + Organization publisher (accurate to visible content). 3–5 real sibling links per
page. Sitemap with real lastmod = data change. **Measurement day 1:** Search Console, Bing Webmaster AI
tab, GA4 referrer segmentation. **What does NOT work / is forbidden:** thousands of near-identical pages,
exact-match-domain reliance (no boost since 2012), bought links / PBNs / reciprocal schemes, keyword
stuffing, fake freshness, fabricated authors, llms.txt (near-useless — add as a cheap hedge only), schema
as a citation lever (add for rich results, expect no citation lift).

## 11. Backlinks / data-story path (the only way past publisher authority)
One localizable ranked dataset sliced per state/county = a story each local newsroom can localize (~50–100
targeted reporter emails → ~10 editorial links). Resource-page links from state floodplain sites, ASFPM,
university extension LibGuides, flood-research projects (lowest-risk, most durable — be a free
non-commercial tool). Citability compounds: per-page CSV/JSON, a persistent methodology page, a "cite this
page" credit line, stable `#chart` permalinks. HARO is dead; expert-quote platforms (Featured/Qwoted) are
weak for data — opportunistic only.

## 12. Infra / ops
Static files on Cloudflare Workers (nothing to crash). Private GitHub repo = backup + history. `.env` holds
keys (CENSUS_KEY etc.), git-ignored, never committed. **Open ops gaps:** no CI/auto-deploy from GitHub yet
(manual wrangler from one machine); no FEMA API schema-drift alarm (a renamed field could silently produce
wrong numbers — add a field-presence check); raw source rows not persisted/hashed (aggregates not
reproducible from source); no uptime/deploy monitoring; no staging.

## 13. Trust / E-E-A-T (YMYL insurance = high bar)
About page states it's an independent, non-commercial project, how numbers are compiled + gate-checked, and
independence (not FEMA-endorsed, no insurer/lead-gen relationship). Organization publisher in schema. NEVER
fabricate a named author or credentials. Contact/corrections email still needed (owner input — do not
publish a personal address). No ads until a 4-week Search Console review passes; disclose any ads on About.

## 14. Separation rule (GSC-cliff protection — HARD)
Own repo, own domain, own Search Console, own ad account. NO shared template, link, or footprint with the
car-repair (calcscrape) or river sites. Never cross-link them. A shared footprint risks a site-level
penalty spreading across all of them.

## 15. Current state (2026-10-23)
Live + verified: 2 county pages (Lee FL, Kanawha WV — the pilot), home directory, /about, /methodology,
/data (CSV). Search Console wired (FILE verification). Private GitHub repo created. Both counties pass the
full gate. Math audited sound (percentiles, sums, pagination). Honest verdict from a full audit: NOT ready
to scale past the pilot until 25–50 distinct pages prove they pass the dup gate and show Search Console
demand.

## 16. Done recently (so a fresh session doesn't redo it)
dateModified/citation schema + visible federal-sources block; SFHA denominator + zone remainder; all-in-one
gate; duplication guard; claims-per-100 demoted; premium-trend card removed; same-state-only nearby links;
Organization publisher schema + About page; years-to-full-risk glide-path; money-first reorder; private
GitHub repo.

## 17. Still missing (highest-leverage first; a completeness audit may extend this)
1. Reach a real 25–50-county pilot (add to counties.json, run build_all) — but ONLY distinct, data-rich
   counties, each passing the dup gate; prove ranking before scaling further.
2. NFHL flood-zone mix (verified fetch) — the mandatory-purchase answer, a genuine new data view.
3. State rollup pages + 2–3 data-story/ranked-list pages (the backlink engine).
4. Contact email + corrections policy (owner); FEMA schema-drift alarm; CI/auto-deploy from GitHub.
5. Measurement wired end to end (Search Console + Bing AI tab + GA4) and a monthly data-refresh runbook.

## 18. Runbook — add a county
Append a row to `tools/counties.json` (`slug, state, geoid, county, countytitle, label, short, official`),
run `python -I tools/build_all.py`, confirm GATE PASS + no DUP BLOCK + data_ok, LOOK at the page, then
`npx wrangler deploy` and read the live body this session. One page at a time.

## 19. Pre-mortem — the ways this dies (watch these)
Scaling thin before proving the pilot (fatal); shipping a wrong/unsourced number (gate guards most);
chasing commercial head terms and quitting when they don't rank; adding ads too early; faking an author or
implying FEMA endorsement; losing the source (now backed up); FEMA API schema drift producing silent wrong
numbers; whack-a-mole fixes instead of fixing the rule.
