# Rater review: flood-calendar, round 3 (2026-11-13)
Checked: built page text, CSV (416 rows), PAPER-GATE-PROMPT rater part. pagead2 = 0 (no ads, PASS). Grep "you should / recommend / safe": 0 advice hits (the only "should" is "narrower than they should be", a statistics caveat).
CSV recompute: 416 rows, 515,295 claims, 404 rows with a one-year mark, median share 56.85%, median largest-year share 95.55% (page says 95.5%, rounding only), median 10+ years = 1. Matches page.

Verdict: ACCEPT (no BLOCKER, no MAJOR)

- Title/labels vs data: "Peak month of NFIP claims by county: 416 U.S. counties" matches; base (claims with a month of loss, paid or not, codes 98/99 out, 100-claim floor) stated; "not a grade, risk score or prediction" and the 2,104 left-out counties (pooled 54.3%) are disclosed. No overclaim.
- Who/how/why: byline, no insurance-expertise claim, AI-tools disclosure, recompute check, cite block, versions, corrections, contact all present.
- Thin/padded/scaled: none. Original measure with chance baseline, one-year concentration columns and a prior-work search line; not a template.
- Advice: none; the 30-day wait line is a FEMA rule statement, not a "you should".
- Ads: none.

MINOR (not blocking)
- The CSV note under the table lists nine columns ("FIPS code, county, state, share, 90% range, numerator, denominator, loss years, as-of date") but the CSV has 18 (adds fifth, expected share, excess, peak months, year, largest-year share, loss-year counts). Fix: list all columns or say "and the columns shown above".
- Title omits the loss-year window (2016-2025); it is in the description and first paragraph. Optional.
- Page text prints "Median ... 95.5%" while CSV rounds to 95.55; state it is computed unrounded or print 95.6%.
