# Cold review: tear this flood-insurance data site apart

You have no history with this project. Read every file in this zip, then scrutinize it hard as (a) a
Google Search quality rater, (b) a demanding data journalist, and (c) a skeptical SEO. Assume it is
wrong until proven otherwise. Be specific; quote the file and line.

## What this is
A planned static data site: one page per US place showing what NFIP flood-insurance policyholders
actually pay, the gap to FEMA's full-risk price, claims history, flood risk, and the CRS premium
discount — all from public federal APIs. Built by a solo non-coder with an AI assistant. Competitors
(NerdWallet, LendingTree, Policygenius, floodfigures.com) show one stale average and a policy count;
this site shows the spread, the full-risk gap, claims per 100 policies, and the CRS discount nobody
else surfaces. Monetization: display ads after a 4-week Search Console review.

## Files
- `CLAUDE.md` — the whole doctrine (reader, dataset catalog, page plan, ranking strategy, gates).
- `docs/reader-spec.md` — the 8-dataset catalog with verified live endpoints.
- `docs/OPEN-ITEMS.md` — owner decisions still open.
- `dist/lee-county-fl.html` — the first real page (Lee County, FL). Open it in a browser.
- `data/agg.json` — the exact numbers on that page, from the live FEMA APIs 2026-10-22.
- `tools/collect.py`, `tools/collect_small.py` — the only network code (pulls + aggregates).
- `tools/build_page.py` — turns the JSON into the static page. Audit all three for correctness bugs
  (percentile math, policyCount summing, the no-$orderby paging + id dedupe, the cohort filter).

## Verified facts (don't re-litigate these; attack what's built on them)
- NFIP Policies v3 + Claims v3 APIs are live and keyless. Lee County in-force = 134,473 policy units
  (sum of policyCount, not row count), reconciles to FEMA's official 132,012 within 1.9%.
- Lee single-family cohort (53,965 policies): annual cost p25/p50/p75/p90 = $1,095 / $1,658 / $2,870 /
  $4,257; median full-risk premium $3,461; 65.7% pay below full risk.
- Lee claims since 1978: 48,496 paid, $3.95B, 36.1 per 100 policies (Hurricane Ian 2022 dominates).
- CRS discounts are real per community (Cape Coral 25%, Fort Myers 20%).

## Tear into these specifically
1. **Thin/duplicate risk.** The owner's previous site lost ~99% of Google impressions and was rejected
   by AdSense as thin. Plan is ~8,000–15,000 pages, released to the index in Search-Console-gated
   waves, with a duplication test (a ZIP page exists only if it differs from its county). Is that test
   strong enough? Where will near-duplicate pages still slip through? Is the wave-release real
   protection or theater?
2. **Can a brand-new domain rank at all** against NerdWallet/Bankrate for these queries, or is the
   only realistic path AI-Overview/Perplexity citations + backlinks from data stories? Be blunt.
3. **The page itself** (`lee-county-fl.html`). As a quality rater: is it genuinely more useful than a
   competitor, or just denser? Which block would you cut? Which single missing thing would most change
   a homeowner's decision? Is anything misleading — e.g. presenting an existing-policyholder median as
   what a new buyer will pay?
4. **FEMA terms / compliance.** Data is for "statistical research or as a reporting record," attribution
   required, no record-level output, no determinations affecting eligibility. Does an ad-supported
   aggregate site sit honestly inside that? Where is the risk?
5. **Keyword priority.** Verified autocomplete demand is state-level and "flood insurance rates by zip
   code." County demand is unproven. Is county-primary-with-ZIP-folded-in the right call, or should it
   launch ZIP-first? What demand families are being missed (renewal increase, Risk Rating 2.0, "do I
   need flood insurance in [zone]", city queries)?
6. **The single weakest assumption in the whole plan.** Name it.

Give a ranked defect list, worst first, then a go / no-go with the one change that would most improve
the odds.
