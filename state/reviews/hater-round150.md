# Hater round 150 (light: six answers on screen 1; compare/ZIP card moved)

Checked: N = agg.json policies.share_below on all 7 (52.8, 23.2, 33.9, 29.7, 51.4, 78.2, 56.9). Quote checker no longer in the quick list (it is the next card). Card placement and checker output rendered in Chromium 390x844: no sideways scroll (scrollWidth 390), quick-answer links 81 px tall.

## home
- MINOR Home HTML is byte-identical in text to HEAD (dist/index.html unchanged); none of the four changes apply. Its own 'Is my quote normal?' section is intact with a stated U.S. base.
Verdict: PASS

## louisiana
- **MAJOR** Quick answer "Is it rising? 52.8% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (52.8) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $1,114, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR 52.8% appears twice within ~500 px (hero stat 4 and the new quick answer); the quick answer adds only the claim, not a new fact.
- MINOR 'Already flooded? What to do now, and FEMA aid.' jumps to #covered, whose heading is 'How do I actually get covered — and how fast?'; the flood steps are mid-section. Same anchor as 'How fast does it start?'.
- MINOR (GAP) no 'Can I pay less?' quick answer on the state page, unlike county pages.
Verdict: FAIL

## palm-beach-county-fl
- **MAJOR** Quick answer "Is it rising? 23.2% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (23.2) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $673, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR ZIP line ("the median ranges from ...") also lacks base and says "priced policies" with no definition; the low ZIP is not linked, only the high one.
- MINOR Provenance line says '10,000 claim records' and agg.json claims.rows = reported_total = 10,000 exactly (state total 448,618). A round number like that can be a fetch cap; if so the 46.8% payout figure is wrong. Unverified; confirm reported_total from FEMA is a true count.
- MINOR Order after 'Is it rising?': payout, already flooded, can I pay less. Fine and true; the quick list is now 8 items so 'Can I pay less?' lands far down screen 2.
Verdict: FAIL

## new-york-county-ny
- **MAJOR** Quick answer "Is it rising? 33.9% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (33.9) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $1,021, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR The 33.9% rests on 171 policies (below_n) and the quick answer, unlike the #gap section, does not show the count; a thin base stated as a flat % on screen 1.
- MINOR No ZIP line on this page (none qualify); nothing says so. Acceptable.
Verdict: FAIL

## dixie-county-fl
- **MAJOR** Quick answer "Is it rising? 29.7% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (29.7) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $987, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR ZIP line ("the median ranges from ...") also lacks base and says "priced policies" with no definition; the low ZIP is not linked, only the high one.
- MINOR 'By ZIP (the 2 with 25+ priced policies)' gives a 'range' from only two ZIPs ($654 to $1,011); reads as a range but is two points. 29.7% rests on 182 policies, not shown.
Verdict: FAIL

## levy-county-fl
- **MAJOR** Quick answer "Is it rising? 51.4% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (51.4) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $1,628, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR ZIP line ("the median ranges from ...") also lacks base and says "priced policies" with no definition; the low ZIP is not linked, only the high one.
Verdict: FAIL

## sonoma-county-ca
- **MAJOR** Quick answer "Is it rising? 78.2% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (78.2) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $1,266, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR ZIP line ("the median ranges from ...") also lacks base and says "priced policies" with no definition; the low ZIP is not linked, only the high one.
Verdict: FAIL

## wakulla-county-fl
- **MAJOR** Quick answer "Is it rising? 56.9% of single-family policies pay under FEMA's full-risk price" drops the base. The number equals agg.json policies.share_below (56.9) but that is single-family PRIMARY-HOME policies, premium before fees vs full-risk before fees (hero stat 4 and the #gap section say so, 500 px above). "Single-family policies" reads as all single-family incl. second homes and, next to "$ ... premium plus fees" figures, as a fees-included comparison. Label (count whose base differs from its label) is MAJOR. Check that should catch it: C10-C14 label-vs-base on data-q="qa" claims.
- **MAJOR** The compare/ZIP card ("The median, $1,471, is ...") now sits inside the quote-checker card, below the checker's input, zone select and "Enter an amount above." The hero label it used to sit under (single-family primary home, premium plus fees, in force August 31, 2026) is gone, so "The median" has no base, no premium-vs-fees label and no date, and its antecedent is ~700 px up the page. After a number is typed the checker prints its own "typical" figure right above it and the two read as one block. Say "median single-family primary-home policy (premium plus fees, in force August 31, 2026)" in the sentence.
- MINOR ZIP line ("the median ranges from ...") also lacks base and says "priced policies" with no definition; the low ZIP is not linked, only the high one.
Verdict: FAIL

## Classes
- County and state: quick answer 'Is it rising?' says 'single-family policies' where the data is single-family primary-home, premium before fees (fix the template string; one word).
- County and state: compare/ZIP card lost its base and as-of date when it left the hero (template: put the base in the first sentence).
- County: thin-base percentages (n under ~200) shown on screen 1 without n.
