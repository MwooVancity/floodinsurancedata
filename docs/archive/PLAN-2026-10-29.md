# PLAN: floodinsurancedata.com

## Goal
The most helpful flood-insurance page for each US state and county, from public federal data. Reader: a homeowner or buyer with a flood-zone letter or a renewal, on a phone, 60 seconds (see CLAUDE.md).

## User, not Google: the helpfulness checklist (owner 2026-10-28: "literally everything, down to the UI")
Every page is judged against every line below by the scared reader on a phone, never by a crawler.
`docs/HATER-PROMPT.md` makes each review judge every line. A line a script can check becomes a gate.
Status per line: OPEN until a review or gate passes it.
**A. The reader's job.** Screen 1 answers: how much, am I required, how fast it starts, does it pay out, is my
quote normal. Each answer comes with its next step: where to buy, the phone number, the deadline. Nothing makes
the reader scroll to learn whether to worry.
**B. Every situation served.** Buyer at a closing, renewal that jumped, just flooded, renter, condo owner,
landlord or second home, business, a town not in the NFIP, a lender letter, a map change. Each finds its answer,
or a plain line saying the data cannot answer it.
**C. Truth.** Each figure equals its source and names its base: homes vs all policies, median vs mean, premium vs
cost, units vs policies, claims filed vs paid. Years are calendar years. Dollars are nominal and say so.
As-of dates are shown. No two blocks contradict each other. Each caveat sits beside its figure.
**D. Confusion traps.**
- Similar figures with different bases side by side.
- One word with two meanings.
- Codes without plain words: legacy zones A01-A30, A99, AHB, B, C, SRL, RCBAP, ICC, CRS class.
- An unclear "here" (county or state?).
- Percentages vs counts mixed.
- Rounding that disagrees between blocks.
- Old dollar amounts read as today's.
- Tables whose first row is not what the lead sentence names.
**E. Plain language.** About 8th-grade reading level. Every term is defined in plain words where it first
appears. Headings are the questions readers ask. No double negatives, no hedging fog, no alarm, no false comfort.
**F. Action and contacts.** NFIP phone, FloodSmart, FEMA map and claim steps, all linked and working. Deadlines:
30-day wait, 60-day proof of loss. Official local contacts (state insurance department, floodplain office):
OPEN, needs a sourced list.
**G. UI on a phone (390px).**
- No sideways scroll; tables readable, long tables searchable.
- Body text 16px+, tap targets 44px+.
- Colour contrast WCAG AA; colour never the only signal.
- Charts carry direct labels and a text equivalent.
- Inputs labelled, with a number keypad.
- "On this page" menu and back-to-top; nothing hidden or collapsed.
- No layout shift; works without JavaScript for every figure.
**H. Accessibility.** Heading order, `lang`, labels on every control, alt text or text for every chart,
keyboard reachable, screen-reader sensible.
**I. Trust.** Says plainly who runs it: anonymous, by choice, with no FEMA link. Shows the methodology,
the sources with dates, and that there are no ads or paid links. A way to report an error: OPEN, owner decision.
**J. Navigation.** Breadcrumbs, state ↔ county, bordering counties, site search with a no-match message, a helpful
404 page, no broken internal links.
**K. Speed and tech.** Fast on 4G, small page weight, no JS errors, printable (a print stylesheet: OPEN).
**L. Language.** Spanish for FL, TX, LA, PR readers: OPEN, large.
**M. Freshness.** Data as-of on every page, monthly refresh, dates move only when the data changes.
**N. Consistency.** The same card says the same thing the same way on every page; state and county pages agree.

## Batch: round 16 fixes (2026-10-28; full review against checklist A-N; no wrong figures, wording/UI MAJORs) — SHIPPED 2026-10-29 (rounds 17-18 light checks PASS, live gate 111 pages)
Each line: DONE with the proof, or OPEN. Ship only when every MAJOR is DONE (one light check, then release).
1. Quote checker: say these are existing policies (many below full-risk) and show the new-policy median beside the result. DONE
2. "Renewing?" label: the term-year row includes new buyers; relabel it. DONE
3. Hero tile: define "full-risk price" in plain words on screen 1; no alarm when the gap is small. DONE
4. Screen-1 payout line: caveat beside it (many unpaid claims are paperwork or "other"). DONE
5. NRI: rating word vs loss percentile shown as two different FEMA measures. DONE
6. Events lead: when a bigger year has no named flood, say so in the lead (Maine 2024). DONE
7. Disaster list: month and FEMA disaster number on each line, so same-title disasters differ. PARTLY (month + emergency label; disaster number OPEN)
8. Zone codes: plain risk words on every zone (B/X shaded moderate, C/X low, A99, AH/AO, A01-A30 high-risk); dropdown A-Z. DONE
9. Non-NFIP list: a county-named community says "unincorporated area only". DONE
10. County-table dashes: a legend line ("fewer than 30 priced single-family policies"). DONE
11. Average paid claim: "1978-2026 dollars, not adjusted for inflation, includes code-upgrade payments" beside it. DONE
12. Home: policy records vs insured units explained; county list header matches its column. DONE
13. "No named flood in <year>" must not contradict a multi-year label row covering that year. DONE
14. Phone UI: tap-to-call NFIP number, note text 15px+, back-to-top link, search box on long tables. PARTLY (tap-to-call, 15px notes, back-to-top DONE; long-table search DONE 10-29)
15. Site: a 404 page; About says the site is run anonymously. DONE
Next GAP (top): show NFIP take-up (homes with flood insurance) and the share of claims from outside high-risk zones; both are in data. Outside-zone share: DONE 10-29 (one line on "Am I required"). Take-up: OPEN (cut 10-28; verify its source first).

## Strategy: Musk's five steps on the whole project (owner 2026-10-28: "elon musk it to #1")
Scoreboard (the only measure of progress): pages indexed, impressions, clicks, queries on page 1, AI-answer citations.
Work that cannot move one of these is suspect.
1. **Question every requirement.** What gets us to #1 for "flood insurance cost <county>": (a) a page exists for that
   county, (b) Google indexes it, (c) it answers better than #1, (d) other sites link to us. Everything else is
   overhead. Twelve review rounds, a growing gate and side docs moved none of the four.
2. **Delete.**
   - Review rounds as the default (see budget below).
   - Docs: CLAUDE.md holds the rules, PLAN.md holds the state, nothing else. `docs/MASTER-PROMPT.md` and
     `REVIEW-PROMPT.md` fold in or go to `docs/archive/`; only `docs/HATER-PROMPT.md` stays, because `hater.py` reads it.
   - Dead tools for cut features: the NOAA, take-up and per-place API collectors. Grep for callers, then delete.
   - Weak cards: each page is 20-25 phone screens. A card a scared reader would not miss goes; the answers stay.
3. **Simplify.** One template, one gate run per batch, one all-county scan. Correctness lives in the builder, so a
   wrong sentence cannot be written; no new check without a defect it catches.
4. **Accelerate where it moves the scoreboard.**
   - (a) Coverage: one template PASS unblocks the 1,803-county queue. 10/day now, 25/day once Google indexes most pages.
   - (c) Answers: the helpfulness list below, cheapest first.
   - (d) Links: data stories (rankings from data we hold), built once, pitched to local news. The one way past
     NerdWallet's authority.
   - (b) Indexing: sitemap, internal links, bordering-county links (done in code).
5. **Automate last.** Already automated: monthly FEMA data, daily publishing. Next: a weekly Search Console pull into
   `state/gsc.json` (needs an owner-made service account key). Then the scoreboard updates itself and decides the pace.

## Where we are (2026-10-28)
- Built site: `dist/flood-insurance/` has 104 folders (51 states, 52 counties and parishes, index.html); `tools/counties.json` 52 counties; `state/county-queue.json` 1,803 counties queued. Last dist commit 514d1559 (publish: added 10).
- Live: rounds 10-12 fixes, shipped 2026-10-28 as a hotfix (commit 5a56b096): live gate 110 pages = build; horry-county-sc read live.
- Data as-of: 2026-07-31 (`data/us/asof.json`).
- Reviews (`state/reviews/*.json`): PASS home, orange-county-ca, atlantic-county-nj, broward-county-fl, palm-beach-county-fl; FAIL horry-county-sc, louisiana, montgomery-county-tx, nevada, oklahoma (round 12, wording MAJORs, fixed in code since). Round 13 not run.
- Search Console: verified 2026-10-23, sitemap submitted (commit 289d7f3c). Traffic: not measured, status unknown.
- The template has no current PASS, so the daily county job adds nothing until one light check passes (step 1).

## Site structure (silo) — checked in the built HTML 2026-10-28
- Tree: home `/` → hub `/flood-insurance/` → 51 state pages `/flood-insurance/<state>/` → county pages
  `/flood-insurance/<county>-<st>/`. URLs are flat (state not in the path); the hierarchy lives in links and
  BreadcrumbList schema (Home › State › County). Decision: keep flat URLs; moving them now costs redirects and gains nothing.
- Down links: each state page's county table links every published county in that state (screen 1 jumps to it).
- Up links: each county links its state in the breadcrumb and in the sibling bar.
- Across: a state links its bordering states; a county links up to 6 published counties in the same state.
- Weak spots as counties publish:
  1. County siblings are the 6 BIGGEST in the state, so in Texas every page would link the same 6 and small
     counties would get links only from the state table. Fix: neighbours first, from the Census county
     adjacency file (public), then fill by size.
  2. Under 3 published counties in a state, the bar fills with big out-of-state counties (Horry links Broward,
     Harris, Miami-Dade). Fix with 1: no cross-state fill once neighbours exist.
  3. One sitemap (110 URLs); an index is needed only past 50,000 URLs. `lastmod` must stay the real data date.

## Scaling to every county (2026-10-28; counts read from the repo today)
The numbers: 3,028 counties have data (`data/all-counties/`); 1,803 of them pass the page build and sit in
`state/county-queue.json`, largest first; 52 are published. The other ~1,225 are too thin for a page (under 30 priced
single-family policies for a median, or a failed build).
1. **Who gets a page:** only the 1,803 queued counties, largest first. A thin county never gets its own page; it stays
   a row in its state's county table, and the home search sends its readers there. No noindex filler pages.
2. **Before the queue speeds up (one time):** the template has a current PASS (light check, step 1 below);
   neighbour sibling links are in (step 5b); the all-county stress scan has the data-triggered cases (step 2) and
   passes on every queued county. The stress scan, not a reviewer, is what checks 1,800 pages.
3. **Pace:** the daily GitHub job publishes 10 a day (about 6 months for the queue). google_gate S7 caps any release
   at 25 new indexable pages. Never more, even if all pass (owner 2026-10-26: no bulk publish).
4. **Per-page review only where code says the data is odd:** `review.flags()` (unpaid share 20+ points from the
   state's, claims per policy under 0.2x or over 5x) sends that county to its own quick look (cheap model, the
   flagged cards only), batched weekly. Every other county ships on the template PASS plus the gates.
5. **Watch Google, then decide the speed (Search Console, weekly):**
   - Speed up to 25 a day only if, after 4 weeks, most published pages are indexed and impressions grow.
   - Hold at 10 if indexing lags (pages "crawled, not indexed").
   - Stop and investigate if site-wide impressions fall sharply. The car site's 2026-09-14 cliff was site-wide.
6. **Keep it fresh at scale:** the monthly cloud refresh rebuilds every published page's data; `lastmod` moves only
   when a page's data changes. Pages whose county later falls under the floor go back to a state-table row with a
   redirect to the state page.
7. **Later layer:** ZIP pages only after counties index well, and only ZIPs that pass the three-part test.
   Not before.

## Helpfulness and information gain (owner asked 2026-10-28; in order, cheapest first)
Data already held (template changes, one light check covers all five):
1. Quote checker by flood zone (`policies.cost_by_zone`): compare the reader's quote with their own zone, not the county.
2. "Why sites differ" names the figure the searcher just saw (MoneyGeek, Insurify, NerdWallet) and which of our rows it matches.
3. Elevated vs not-elevated premium (`prem_elevated_median` / `prem_not_elevated_median`) with the Elevation Certificate step.
4. Condo line (`condo_unit_pct`, `condo_building_pct`): what condo owners are and are not in our cost figures.
5. Non-NFIP communities named on state pages (`crs_out`).
One more breakdown in the monthly cloud job:
6. Paid share per named storm (claims file), beside the all-claims paid share.
7. Community flood-map date (Community Status Book, if the field is in our pull; check first).
Rules: each addition replaces something weaker or goes inside an existing card (pages are already 20-25 phone screens);
Search Console queries decide what is missing; one phone read per change, not a full review round.
Ranking, beyond the page: data stories (rankings) for links; Search Console read first.

## What works
- Builder rules make wrong text hard (`tp`, `m`, `claim`, `rule`); 9-question gate on built and live HTML; mutation suite of real shipped bugs.
- Template review on 3 samples plus flags for odd pages; S12 blocks unreviewed pages; S14 ages gaps.
- FEMA pull runs in GitHub Actions monthly; daily job publishes only reviewed counties.

## What does not (yet)
- Twelve hater rounds; louisiana and four other pages still FAIL at round 12.
- No traffic data yet, so no evidence the pages earn search demand.
- PIF workbook listed but pages are not checked against it.

## Next steps (in order)
1. Light check of the changed cards (median label, SRL label, unpaid lead, private-flood rule, county jump link, search message, home zone table) on 2-3 pages, cheap model, after the monthly data job lands. Done when the template has a PASS and the daily job publishes again.
2. Add the data-triggered cases ("Other" is the top unpaid reason; single-family homes a small share of units) to the all-county stress scan. Done when the scan flags them.
3. Read Search Console (impressions and queries per page). Done when numbers with a date are recorded here.
4. Gap backlog top 3 (`state/reviews/backlog.md`): name non-NFIP communities on state pages; USPS-preferred ZIP town names; condo/RCBAP cost line. Done when each is a card or a printed gap and leaves the backlog.
5. Official FEMA policy-count comparison (PIF workbook) on every page, or delete the "not yet compared" line. Done when the gate checks it.
5b. Neighbour sibling links (Census county adjacency file) before counties publish in bulk. Done when a county's
   bar lists its bordering published counties first and no page links out of state while neighbours exist.
6. Keep the daily county job adding reviewed counties a few at a time. Done when published counties rise each day with PASS signatures.
7. After four weeks of Search Console data: AdSense review. Done when the owner decides.

## Owner only
- Search Console review after four weeks; AdSense and consent banner.
- Paid quote referrals: only after a state-licensing + FTC disclosure check.
- Opening pages to the index; cutting any block; domain.

## Open decisions
- ZIP pages (~2,500 with 100+ priced policies): wait until county pages pass review and Google shows indexing.
- Data stories (county rankings) for backlinks: not built.
- Territories (PR, USVI, Guam): left out, no line says so yet (round 8 backlog).

## Facts kept from the old reader spec (2026-10-22)
- Competitors: floodfigures.com (NFIP-only, no county pages, no percentiles or full-risk); floodcostzip.com (ZIP-level, full-risk and projections). Our edge: seven datasets joined per county, CRS discount, sourcing.
- Endpoints: OpenFEMA v3 NfipPolicies/NfipClaims (`propertyState` required; county = `censusGeoid[:5]`; `$top=1000`), v2 DisasterDeclarationsSummaries, v2 HousingAssistanceOwners (`zipCode`), v1 NfipCommunityStatusBook; NRI ArcGIS `National_Risk_Index_Counties` (`STCOFIPS`). NFHL point query unreachable; link FEMA's map.

## Done recently
- 2026-10-28 dropped the premium-rise calculator (owner: too risky); cited 42 U.S.C. 4015(e) (2e46c79b).
- 2026-10-28 round 12 fixes and private-flood lender rule 12 CFR 339.3 (8c970f16).
- 2026-10-28 round 11: one flood-disaster rule for counts, aid and claim checks (1f638128).
- 2026-10-28 stress test on 1,803 counties: repeated NRI sentence and FEMA sequence numbers fixed (d8e204f6).
- 2026-10-28 published 10 more counties (514d1559).

## Review and gate budget (owner 2026-10-28; rule in CLAUDE.md)
About a million tokens went to 12 review rounds. From now: scripts first (gates + all-county scan), one cheap light
check per batch (changed cards, 2 pages, text only, under ~50k tokens), a full round only for a major redesign with
the owner's OK. Every defect a review finds becomes a gate check, so no review hunts it again.

## Session 2026-10-28 (late): built in code, NOT yet built/gated/reviewed
- Done in code: quote checker zone choice (item 1); condo line (item 4); non-NFIP names on state pages (item 5);
  bordering-county sibling links from data/us/county_adjacency.json (5b); ZIP names need a place covering 25%+ of
  the ZIP's land (77386 no longer "Houston").
- Already on the page: elevated vs not elevated + Elevation Certificate (item 3).
- Dropped on purpose: naming competitors' figures (item 2): not public data, changes without notice.
- Left: run build_all + release.py gates once (fix anything they catch); light check of changed cards; ship;
  cloud data job for the zone table; items 6-7; all-county scan; Search Console read (owner).

## Next batch (held 2026-10-29; light round 19 reviewed a withdrawn version, not recorded)
- Long-table search boxes: script read correct in round 19; re-add, plus a "no matches" line.
- "Outside a high-risk zone?" line: data fixed in agg_raw.py (blank zones now leave both sides; share of paid dollars
  on zoned claims, building + contents + ICC). Re-add after the 2026-11-03 refresh, worded "of paid claim dollars"
  (not "buildings"), with the period, and its takeaway for the "Am I required" reader.
- Take-up (homes with flood insurance): verify the penetration source first (cut 10-28).

## Monthly data refresh (2026-10-29)
Policies are re-downloaded each month; claims keep last month's copy and re-pull only the last 3 loss years plus
"no year" (`pull_raw.py` RECENT). If FEMA's state total stops matching, that state's claims are re-pulled in full.
The job log prints the raw download size (`du -sh`). Check the 2026-11-03 run: time, size, all 51 states done.
