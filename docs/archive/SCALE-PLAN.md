# floodinsurancedata.com — Scale Plan (for review)

How this goes from a 2-county pilot to real coverage without committing the thin-page suicide that the
whole strategy warns against. Written 2026-10-23. Companion to `MASTER-PROMPT.md` (full project brief).

## 0. Where we are
Live, gated, committed: 2 county pages (Lee FL, Kanawha WV), home, `/flood-insurance/` hub, /about,
/methodology, /data. All-in-one correctness gate + duplication guard + thin-tail suppression in place.
Freshness/citation schema, OG cards, publisher identity, glide-path, money-first order shipped. Private
GitHub repo + CI auto-deploy. Search Console verified. Math audited sound.

## 1. The honest constraint (do not pretend around it)
- A new no-authority domain cannot win commercial "flood insurance cost [place]" head terms. The prize is
  the **informational long-tail + AI citations**. Horizon: 6–12+ months. Cannot be forced.
- **Prove before scaling.** Thousands of near-identical pages is the failure mode that sank both
  competitors and triggers Google's scaled-content demotion. Recovery is slow or never.
- Therefore scaling is **demand-gated in waves**, not a one-shot 1,500-county dump.

## 2. Prerequisites to add ANY county (hard, enforced)
A county page ships only if ALL hold — this is why we can't just dump a county list:
1. **Correct county FIPS (5-digit `geoid`)** — a wrong FIPS silently builds the wrong county. Source of
   truth: Census/FEMA county FIPS (or the NRI state endpoint, which returns `STCOFIPS` + name per state).
2. **Official PIF count** (`official` in counties.json) — from FEMA's "Policy Information by State and
   Community" workbook. Without it the gate's reconciliation check fails and `data_ok` blocks the page.
   So the workbook must be fetched + parsed per state before that state's counties can ship.
3. **The FEMA API pull succeeds + reconciles** (`collect.py`) — policies/claims complete, ≤5% vs official.
4. **Passes the correctness gate** (`gate.py`) — denominators, claims reconciliation, caveats, dataset
   count, dateModified.
5. **Passes the duplication guard** (`build_all.py`) — <80% masked overlap with every kept page.
6. **`data_ok`** — ≥100 priced single-family policies (statistical sufficiency). Thin counties are
   suppressed, not shipped.

## 3. Wave 1 — the real pilot (25–50 counties) — the unblocker
Everything (ranking test, state hubs, data stories, citations) is blocked until this exists.
- **Selection (distinctness is the point, not raw count):** pick for maximum data variance, not just size —
  a spread across coastal high-NFIP (FL, TX, LA, NJ, NY, SC, NC, VA), inland river-flood (WV, MO, IA, PA),
  low-take-up, high-CRS-discount, and high-claims counties. Each page must surface a genuinely different
  story, or the dup guard (correctly) drops it.
- **Build:** fetch the PIF workbook for the target states (official counts + confirm FIPS), append rows to
  `tools/counties.json`, run `python -I tools/build_all.py` (resumable; one background job; FEMA API
  throughput-bound). Every page through gate + dup guard + data_ok.
- **Ship:** sitemap + index day 1; confirm `/flood-insurance/` hub lists them; LOOK at a sample of rendered
  pages (not just gate PASS).
- **Measure:** Search Console (indexing, impressions, queries), Bing Webmaster AI tab (citations), GA4
  referrers (Perplexity/ChatGPT). Wire before/at launch.

## 4. Stop/Go gate before Wave 2 (the discipline that saves the domain)
Do NOT build the next wave until, on the Wave-1 pages:
- Search Console shows real **impressions + queries** (pages are indexed and surfacing), AND
- at least a few pages show position movement or an AI citation appears (Bing AI tab / referrers), AND
- the duplication similarity across the live set stays **under the block threshold** and every page clears
  `data_ok`.
If demand is flat after the honest window, the answer is "fix the pages / pick better query families,"
not "add more pages."

## 5. Wave 2+ — expand by demand, add the depth
Only where Search Console shows demand:
- More counties in the states/query-families that showed traction.
- **State rollup pages** (`/flood-insurance/<state>/`) — county table + risk tile-map (data already in each
  `agg.json`). Internal-link hubs.
- **Data-story / ranked-list pages** — "counties paying furthest below full-risk," "most claims since
  1978," "biggest CRS discounts." The backlink engine: one dataset, localized per place for reporters.
- **Buildable data adds** (keyless, county-level, each a verified fetch — never faked): FEMA Hazard
  Mitigation grants, NOAA Storm Events county counts/damages, RR2.0 premium-change distribution. NFHL
  stays an address-level link, not a fabricated county number.
- Standalone ZIP pages only where the 3-part publish test passes.

## 5a. Queued data blocks, ranked (from the 2026-10-25 gap research — build when ready, each verified-fetch-first, never faked)
The site shows the insurance but never the flood itself, and misses homeowners' most-asked questions. Build in this order:

**Tier 1 — need NO new dataset (recompute from the OpenFEMA Policies/Claims files already ingested; highest leverage, cheapest):**
1. **Payout reality** — average paid claim + the share of claims closed WITH NO payment, per county. Source: NFIP Claims (already have; uses the closed-without-payment flag). Answers "is NFIP even worth it / do claims actually pay?" Nobody publishes this. Caveat: closed-without-payment ≠ "denied" (withdrawn, below-deductible, duplicate all count).
2. **Local premium trend** — median cost by policy effective year, per county. Source: NFIP Policies (already have). Answers "are premiums here rising?" Caveat: cohort-mix + RR2.0 phase-in, not a like-for-like index (already noted on page).
3. **Claims paid OUTSIDE the high-risk zone** — share of paid claim dollars in Zone X / non-SFHA, per county. Source: NFIP Claims `floodZone` (already have). Answers the #1 reader question "do I need it outside the 100-year floodplain?" Caveat: insured-claims only, not all flood damage.

**Tier 2 — one new keyless federal dataset each (verified endpoints):**
4. **NCEI Storm Events** (highest info-gain NEW dataset) — actual flood/flash-flood event counts + NWS damage $ per county, 1950–present. Source (VERIFIED, keyless bulk CSV): `https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/` (`StormEvents_details-ftp_v1.0_d{YEAR}_c*.csv.gz`), county FIPS + event type. Adds the missing PHYSICAL-flood axis ("has it actually flooded here, how badly"), distinct from insured claims. Caveat: NWS damage dollars are field estimates, not audited.
5. **NfipResidentialPenetrationRates** (VERIFIED OpenFEMA, 3,159 rows, county) — take-up overall AND inside the SFHA. A cleaner "how many homes here actually carry it" than our Census proxy; could replace/augment the take-up card. Caveat: NFIP-only, estimated denominator.

**Also captured (lower priority / bigger lift):** NfipMultipleLossProperties (real 240k-row repetitive-loss file, county/ZIP, richer than the IA one we use); RR2.0 county/ZIP premium-change XLSX files (static, binned, off May-2020 data). Honest explainer wedge (not data): the pre-2021 vs RR2.0 correction — grandfathering gone (→ glide path), elevation certificates no longer required, "assume the seller's rate" now = inheriting a glide-path discount; the web still repeats the obsolete rules.

**Genuinely unanswerable (leave as printed gap lines, never fake):** a property's exact future full-risk premium, live private-insurer quotes, why a specific claim was closed without payment, and county %-in-SFHA without our own GIS intersection. NFHL zone-mix / SLOSH surge / First Street are address-only / GIS / paywalled — out of scope unless we add a GIS step.

## 6. Infra for scale (built or named)
- ✅ CI auto-deploy (committed `dist/` → Cloudflare on push; gate on PR).
- ✅ FEMA schema-drift alarm (`collect.py` fails loud if a field vanishes).
- ✅ Reproducibility: sha256 fingerprint of the id-set per dataset in the manifest.
- Needed: a monthly data-refresh runbook; sitemap stays flat (fine under the ~2,000-page ceiling — no
  index needed until >50k URLs, which this site will never hit).

## 7. Owner-only (cannot be closed in code)
Contact/corrections email (for About); GA4 + Bing Webmaster accounts; the ads decision (none until a
4-week Search Console review); and the go/no-go on each wave.

## 8. The one rule
A page ships only if it is genuinely distinct and passes every gate; the site scales only as fast as
real demand proves. Coverage is earned per wave, never assumed. Scaling thin is not a faster version of
this plan — it is the one move that forecloses it.

## Questions for the reviewer
1. Is the wave/stop-go discipline the right risk control, or too conservative given the 6–12mo horizon?
2. Wave-1 county selection: optimize for raw NFIP size (data density) or for variance (distinctness)? The
   plan says variance — is that right for both ranking and the dup guard?
3. Is sourcing official PIF counts per state the real bottleneck, and is there a cheaper reconciliation
   that doesn't gate-block new counties?
4. Which single data-story page would most likely earn the first real backlinks?
5. Anything in sections 2–5 that is still a way to fail at scale that we haven't guarded?
