# Cold review: tear this flood-insurance data SITE apart (final form)

You have no history with this project. Unzip it, open the pages in a browser, read the code, then
scrutinize hard as (a) a Google Search quality rater, (b) a demanding data journalist, (c) a skeptical
SEO. Assume it is wrong until proven otherwise. Quote file and line.

## What this is
A complete static data site: one page per US county showing, from public FEMA data, what NFIP
flood-insurance policyholders actually pay (cost spread p25/p50/p75/p90), the gap to FEMA's full-risk
price, claims history, National Risk Index flood risk, FEMA disaster history, homeowner aid paid, and
the CRS premium discount per community. Competitors (NerdWallet, LendingTree, Policygenius,
floodfigures.com) show one stale average and a count. Built by a solo non-coder with an AI assistant.
Ads only after a 4-week Search Console review.

## Open it
- `dist/index.html` — home + client-side county search.
- `dist/flood-insurance/lee-county-fl/index.html` — huge coastal county (134,473 policy units).
- `dist/flood-insurance/kanawha-county-wv/index.html` — tiny inland county (1,283 units) — proves the
  template generalizes across extremes.
- `dist/methodology/index.html`, `dist/data/counties.csv`, `dist/sitemap.xml`, `dist/llms.txt`.

## The pipeline (audit for correctness)
- `tools/collect.py` — NFIP policies+claims+NRI per county. Note: pages at `$top=1000`, NO `$orderby`
  (it 503s), adaptive page-shrink on 503, dedupe by id, completeness manifest.
- `tools/collect_small.py` — CRS, disaster declarations, housing assistance.
- `tools/nri.py` — National Risk Index flood fields (CFLD coastal, IFLD inland) from FEMA's ArcGIS org.
- `tools/build_page.py` — renders a county page (inline-SVG charts, JSON-LD, quote widget).
- `tools/build_site.py` — home/methodology/data/sitemap/robots/llms.
- `tools/build_all.py` — generator: builds every county in `tools/counties.json`, then the site, resumable.
- `tools/gate.py` — correctness gate (fail = no ship): page numbers == JSON, completeness, reconciliation
  ≤5%, required panels, no None/nan leak, NRI present or explicit gap.

## Verified facts (don't re-litigate; attack what's built on them)
- Lee FL: 134,473 policy units (sum of policyCount, reconciles to FEMA official 132,012 within 1.9%);
  single-family cohort median $1,658, full-risk median $3,461, 65.7% below full risk; 48,496 claims /
  $3.95B since 1978; coastal flood risk Very High (80th pctl).
- Kanawha WV: 1,283 units (0.8% vs official 1,293); median $1,450; inland flood risk Relatively High
  (96th pctl); no community carries a CRS discount.

## Tear into these
1. **Thin/duplicate risk.** The owner's previous site lost ~99% of Google impressions and was rejected
   as thin. Plan: ~2,000 quality pages, released to the index in Search-Console-gated waves, with a
   3-part publish test (statistical sufficiency + decision-relevant difference + distinct intent) for ZIP
   pages. Is that test strong enough? Where do near-duplicates still slip through?
2. **Can a new domain rank** vs NerdWallet/Bankrate, or is the only realistic path AI-Overview/Perplexity
   citations + backlinks from data stories? Be blunt.
3. **The two pages.** As a quality rater: genuinely more useful than a competitor, or just denser? Which
   block would you cut? Which missing thing would most change a homeowner's decision? Anything misleading
   (e.g. existing-policyholder median read as a new-buyer quote)?
4. **The code.** Any correctness bug in the percentile math, policyCount summing, the no-$orderby paging +
   dedupe, the completeness manifest, the gate, or the NRI coastal/inland mapping?
5. **FEMA terms.** Aggregate-only, attributed, no record-level output — does an ad-supported site sit
   honestly inside "statistical research or reporting"? Where's the risk?
6. **Keyword priority & the single weakest assumption in the whole plan.** Name it.

Give a ranked defect list, worst first, then a go / no-go and the one change that most improves the odds.
