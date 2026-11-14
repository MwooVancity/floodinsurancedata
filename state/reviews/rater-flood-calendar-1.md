# Rater review: flood-calendar, round 1 (2026-11-13)
Checked: built page (41.6k chars text), CSV (416 rows + header, matches "416"), PAPER-GATE-PROMPT rater part. pagead2 count = 0 (no ads, PASS). robots = noindex,follow (staged, PASS). Causal/advice/ban-word grep: 0 hits.

Verdict: MAJOR REVISION (one MAJOR; rest passes)

## Passes
- Byline, how (Methods, Reproduce, CSV with numerator/denominator), why (Question), as-of, FEMA field quotes, left-out counties (2,104 + 507) with their median/pooled share, 90% ranges, one-year flag, all present.
- Title/labels match data: 416 counties, peak month, share of claims. "Fifth" is explained as position, not grade.
- No advice, no "you should"; 30-day wait line is a fact, not a verdict.
- Not scaled content: table is data; prose is specific (Pamlico, Dallas, 404 of 416).

## BLOCKER
none

## MAJOR
1. No chance baseline, so the headline can mislead. Quote: "69.9% ... of NFIP claims with a month of loss fell in their county's peak month". The peak is the largest of 12 months by construction (Limitations admits this), so even 12 equal months would show a share well above 8.3%. A reader or reporter cannot tell if 69.9% or Dallas 19.0% means "seasonal" or "nothing". Fix: add one sentence in Abstract/Results with the expected share if claims fell at random across 12 months (simulate with each county's own n, report the median simulated share, computed by script and tagged), and say how far above it the observed median 56.9% is. Without it the "calendar" framing (title, "not a yearly season" only appears after the number) overclaims a seasonal pattern.

## MINOR (not blocking)
- Title says "each county's peak month" but only 416 of about 3,100 counties are listed; most readers' counties are absent. The Abstract says it, but put "416 counties with 100+ claims" in the H1 subtitle line too (it is in the title tag already). Fix: add one line near the top: "Your county not listed? It has under 100 claims; see Methods."
- 404 of 416 are one-year-dominated: the useful reader answer ("is my county's peak a season or one flood?") is buried; consider promoting that sentence above the 69.9% figure.
- Disclose in Results that pooled 69.9% is dominated by big-claim counties (Monroe FL 8,636, Collier 11,920) since it is claim-weighted; one clause.

R3.6 rating: Page Quality High on E-E-A-T-for-data (transparent, sourced, accountable); Needs Met Highly-to-Fully for journalists, Moderately for homeowners (own county mostly absent, no baseline). Below High on interpretability = MAJOR #1.
