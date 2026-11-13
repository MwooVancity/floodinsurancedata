# Research paper gate (owner 11-12: strictest, PubMed level; no penalty risk left unguarded)

A paper ships only when EVERY line below passes. Machine gates (M) run in release.py and fail closed for that paper only
(papers.READY drops it; the rest of the site ships). Review gates (R) are two fresh agents that never saw the build:
a hostile statistician and a Google quality rater. Any BLOCKER or MAJOR = not shipped. Nothing here is waived.

## 0. Before any code (stop if any fails)
- R0.1 Originality: search (3+ queries, extended mode) for the same measure at the same geography. Found = cite and
  reconcile in "Prior work", and name the real difference (newer data, every county, like-for-like base, CSV). No
  difference = do not build.
- R0.2 Reader question: one sentence a homeowner, buyer, reporter or official would ask, and the decision it changes.
  None = do not build.
- R0.3 Harm list (PLAN H1-H16) answered for this paper in writing, each with its guard.
- R0.4 Field definitions: FEMA data-dictionary text for every field the measure uses, read raw this session, quoted.

## 1. Measure (statistics; machine where possible)
- M1.1 Same base: numerator, denominator and n are counted on the same records; the spec declares all three and
  index_check recomputes each from the raw files with its own code.
- M1.2 Minimum n per county, stated with its reason; every displayed share has n beside it.
- M1.3 Uncertainty: every share shows a 90% interval: Wilson for a share of counted records; for a share of dollars, a bootstrap over the county's claims (cloud job), else no interval and no rank. No bare rank. Ranks are shown as bands (fifths) or with
  a rank range; ties named.
- M1.4 Materiality: a share of "below/over" also reports the size (median gap, median excess).
- M1.5 Window: pooled history is restricted to a stated window or split by era; dollars labelled "not adjusted for inflation".
- M1.6 Selection: pooled national figure, the excluded counties' count and median, shown beside the county median.
- M1.7 Units: records vs policies (policyCount) verified for the base; the check fails if they differ.
- M1.8 One event: if one loss year is over half a county's value, the row says so.
- M1.9 No causal word (because, due to, driven by, caused) unless inside a quoted official source.
- M1.10 No test, no "significant": the word is banned.

## 2. Page (machine)
- M2.1 Sections in order: Abstract, Question, Data, Methods, Results, Prior work, Table, Limitations, Reproduce,
  How to cite, Versions, Corrections. Missing one = fail.
- M2.2 Every number tagged and recomputed (V1/V2 style); CSV rows = table rows = recompute; CSV has FIPS, n, interval, as-of.
- M2.3 Banned words: best, worst, safest, most dangerous, peer reviewed, significant, only published here (unless R0.1
  found nothing, logged with date and queries), denied, forecast/will rise.
- M2.4 Base named in the same sentence as every share (label-vs-data gate C10-C14 style).
- M2.5 Versioned permalink /flood-insurance/<paper>/<asof>/ kept forever; the current page links every version;
  sitemap lastmod = as-of, never build day.
- M2.6 Required OpenFEMA attribution and "not endorsed by FEMA".
- M2.7 Phone: abstract + 3 findings within the first two screens at 390x844; page under the byte budget; table
  beyond 500 rows lives in the CSV only.
- M2.8 Re-identification: no figure from fewer than the minimum records; no single-claim maximum.
- M2.9 Structured data: Dataset schema only with true fields (name, description, creator = site, temporalCoverage,
  distribution = the CSV, license = FEMA terms); no Review, no fake author, no ratings.

## 3. Google and AdSense penalty triggers (machine + rater)
- M3.1 Scaled content (our own threshold, not a Google number): each paper's findings text must share under 30% of its sentences with any other paper (sameness
  check across papers); a paper whose 3 findings are generic templates fails.
- M3.2 Doorway / cannibalization: one target query per paper, not the same as any county, state or hub title; county
  pages link the paper, never repeat its table.
- M3.3 Freshness honesty: dates move only with new data.
- M3.4 No ads on paper pages: the AdSense snippet is left off paper pages and tools/adsense_check.py exempts exactly the READY paper URLs (the check requires the snippet everywhere else).
- M3.5 Staged indexing: a new paper ships noindex; indexable only after both reviews PASS and 7 days live with no
  correction; at most 2 papers made indexable per week.
- R3.6 Quality rater (Google's Search Quality Rater Guidelines, YMYL money topic): rates Needs Met and Page Quality;
  anything below "High" with a stated reason = MAJOR.

## 4. Hostile statistician prompt (R)
"You are a statistician and FEMA-data expert reviewing for a journal that rejects most submissions. Recompute 15 rows
from the raw files by script. Attack: base consistency, small-n instability (bootstrap the top 20), selection bias,
time pooling, units (records vs policyCount), materiality, misleading-but-true findings, causal language, prior work,
reproducibility from the Methods text alone. Each finding: BLOCKER/MAJOR/MINOR, evidence, fix. Verdict ACCEPT /
MINOR REVISION / MAJOR REVISION / REJECT. Only ACCEPT or MINOR REVISION ships."

## 5. After ship
- Corrections log on the page; a correction re-runs both reviews on that paper.
- Monthly: refresh, recompute, new version URL; ranks frozen between refreshes.
- 90 days with 0 impressions and 0 referring domains: cut (301 to the hub).
