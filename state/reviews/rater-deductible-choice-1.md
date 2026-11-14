# Rater: deductible-choice, round 1 (2026-11-13)
Verdict: MAJOR REVISION (Page Quality below High for the stated reasons; no overclaim, no ads, no advice).

Checked clean: no pagead2; no "you should/best/worst/significant/because/due to/driven"; byline honest (publisher, not an expert); base named beside every share; 15.1% (all counties) vs 15.0% (listed counties) both labelled; left-out counties (1,139 at 24.6% pooled) disclosed; CSV (1,793 rows, FIPS, n, interval, as-of) matches page; "not endorsed by FEMA" present; Limitations say reasons for choosing are not in the data.

BLOCKER: none.

MAJOR
1. Needs Met: reader cannot find their own county. Page shows only top and bottom 100 of 1,793; a homeowner in any other county gets nothing but a CSV download. Fix: add a county/state lookup (static, from the CSV) or a per-state median/range table on the page.
2. Missing "why it matters": nowhere says what a $5,000+ deductible means for a claim (you pay the first dollars of a covered loss) or what FEMA's standard/minimum options are, so the headline 15% has no meaning to a non-expert. Fix: two sourced sentences quoting FEMA's deductible definition and the code list's lowest options, no advice.
3. Versions section contradicts PAPER-GATE M2.5: "each monthly refresh replaces the figures" but the gate requires a kept versioned permalink /flood-insurance/deductible-choice/<asof>/ listing every version. Fix: publish the as-of permalink and list versions.
4. Staged indexing (M3.5): page has no noindex, canonical is set, and the URL is in dist/sitemap.xml. If both reviews have not PASSed and 7 days live have not passed, this is early indexing. Fix: noindex and leave out of sitemap until gate conditions are met (owner opens indexing).

Minor (not blocking)
- Median county 21.5% vs pooled 15.0% is a 6-point gap with no one-line reason (small counties differ from big ones is a fact the table can show; do not say why people choose). Add the size split: pooled share of counties under/over 500 units.
- Outliers like Santa Clara County, CA (50.2% of 5,848 units) are unexplained; a "reasons not in the data" gap line next to the top table would help.
- 6 counties tie at 0.0% but only 3 of them appear in the bottom list; say the other ties are in the CSV.
