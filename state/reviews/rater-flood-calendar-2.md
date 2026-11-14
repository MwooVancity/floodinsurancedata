# Rater review: flood-calendar, round 2 (2026-11-13)
Checked: built page text (48.4k chars), CSV (416 rows), PAPER-GATE-PROMPT rater part. pagead2 = 0 (no ads, PASS). robots = noindex,follow (staged, PASS). Grep "you should / we recommend / safe to": 0 hits.
Recomputed from CSV: 404 one-year rows, September 113 / August 74 / October 50, pooled 69.94% of 515,295, median share 56.85%, median expected 11.3%, FL 44 listed and 11 in top 50. All match the page.

Verdict: ACCEPT (no BLOCKER, no MAJOR)

## Round 1 MAJOR: fixed
Chance baseline now in title area, Abstract, Methods and every row (9.3% expected vs 69.9%; median 11.3%). Limitations says the peak is the highest of twelve by construction.

## Passes
- Title and labels match data: 416 counties with 100+ claims, "peak month", "share of claims". Fifth explained as position, not grade.
- Who (named publisher, no insurance expertise claimed, AI-tools disclosure, accountable), how (Methods, Reproduce, numerator/denominator in CSV), why (Question), as-of, left-out counties with their own median/pooled share.
- No advice; the 30-day wait line is a fact. No causal claim ("mostly one year's flood" is data-labelled and hedged: one or several floods).
- Not scaled content: prose names specific counties and figures, table is data.

## BLOCKER
none

## MAJOR
none

## MINOR (not blocking)
1. CSV link text says columns are "FIPS code, county, state, share, 90% range, numerator, denominator, loss years, as-of date", but the CSV also has fifth, expected_share_at_random_pct, excess_points, peak_months, year_month_over_half, peak_month_loss_years. Fix: list those too (label vs data).
2. No Dataset JSON-LD on the page (M2.9 allows it only with true fields). Fine while noindex; add before indexing if wanted.
3. Round 1 minors (pooled share is claim-weighted so big counties dominate; own-county-not-listed line near the top) not visibly added. Fix: one clause each.

R3.6: Page Quality High (transparent, sourced, accountable, baseline given); Needs Met Fully for journalists, Moderately for homeowners (own county often not listed, stated).
