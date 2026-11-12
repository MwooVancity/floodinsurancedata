# Hater round 151 (light, text only: quick-answer base and compare card base/date)

Previous items (round 150): both MAJORs FIXED on all 7 pages. Quick answer now says single-family primary-home policies, premium under FEMA's full-risk premium (not a quote); compare card now carries base (single-family primary home, premium plus fees) and as-of date, and every comparison and rank recomputed from data/c and data/states agg.json matches.

## louisiana
- Checked: policies.share_below 52.8 equals the quick answer; p50 1114 = $1,114; as-of 2026-08-31 = "August 31, 2026"; state p50 rank 16 of 51 (50 states + DC) = "16th highest"; 1114/1066 = +4.5% shown as 5% above U.S. median. Compare card sits after the checker and now carries base and date.
- MINOR 52.8% appears twice within about 500 px (hero stat 4 and quick answer); adds only the claim. Unchanged from round 150.
- MINOR 'Already flooded? What to do now, and FEMA aid.' jumps to #covered, whose heading is about getting covered and how fast; same anchor as 'How fast does it start?'. Unchanged.
- MINOR (GAP) No 'Can I pay less?' quick answer on the state page, unlike county pages. Unchanged.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 52.8% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
Verdict: PASS

## palm-beach-county-fl
- Checked: share_below 23.2, p50 673, county rank 8th lowest of 55 FL counties with 100+ priced, FL median 985 (-31.7% shown 32%), U.S 1066 (-36.9% shown 37%). All true.
- Round-150 MINOR '10,000 claim records' is closed: owner verified FEMA returns 10,758 records, 758 coded deleted/assigned in error and left out. Not re-raised.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 23.2% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
- MINOR ZIP line: "priced policies" is not defined on that line, and only the high ZIP is linked (low ZIP plain text). Verified true: 51 ZIPs with cost_n 25+, 33484 $451 to 33480 $1,830.
Verdict: PASS

## new-york-county-ny
- Checked: share_below 33.9, p50 1021, NY median 1261 (-19.0%, 19% below), U.S -4.2% (4% below), 11th lowest of 48 NY counties with 100+ priced. All true.
- MINOR 33.9% rests on 171 policies (below_n) and the quick answer does not show the count; a thin base as a flat % on screen 1. Still true from round 150.
- MINOR No ZIP line (none qualify) and no line saying so. Acceptable.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 33.9% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
Verdict: PASS

## dixie-county-fl
- Checked: share_below 29.7, p50 987, 'within one percent' of FL 985 (+0.2%), U.S -7.4% shown 7% below, rank 25th highest of 55. All true.
- MINOR 29.7% rests on 182 policies, not shown on screen 1.
- MINOR 'the median ranges from' with only 2 ZIPs reads as a range but is two points.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 29.7% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
- MINOR ZIP line: "priced policies" is not defined on that line, and only the high ZIP is linked (low ZIP plain text). Verified true: 2 ZIPs: 32628 $654 to 32680 $1,011.
Verdict: PASS

## levy-county-fl
- Checked: share_below 51.4, p50 1628, FL +65.3% shown 65%, U.S +52.7% shown 53%, 4th highest of 55. All true.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 51.4% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
- MINOR ZIP line: "priced policies" is not defined on that line, and only the high ZIP is linked (low ZIP plain text). Verified true: 4 ZIPs: 32626 $1,087 to 34498 $3,204.
Verdict: PASS

## sonoma-county-ca
- Checked: share_below 78.2, p50 1266, CA median 1055 (+20.0%), U.S +18.8% shown 19%, 12th highest of 42 CA counties. All true.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 78.2% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
- MINOR ZIP line: "priced policies" is not defined on that line, and only the high ZIP is linked (low ZIP plain text). Verified true: 13 ZIPs: 94931 $1,139 to 95462 $1,757.
Verdict: PASS

## wakulla-county-fl
- Checked: share_below 56.9, p50 1471, FL +49.3% shown 49%, U.S +38.0% shown 38%, 5th highest of 55. All true.
- MINOR Quick answer 'Is it rising?' says "premium" with no "before fees", while the card below and the checker say "premium plus fees". The page's #gap section states "both before fees"; the quick answer is now true and based-labelled (single-family primary-home, share_below 56.9% equals agg.json), but a reader may still compare it with the fees-included median. Label is correct, so MINOR.
- MINOR ZIP line: "priced policies" is not defined on that line, and only the high ZIP is linked (low ZIP plain text). Verified true: 4 ZIPs: 32358 $1,173 to 32346 $3,984.
Verdict: PASS

## Classes
- County and state: quick answer says "premium" without "before fees" (one phrase in the template).
- County: thin-base percentages (n under about 200) on screen 1 without n.
- County: ZIP line undefined "priced policies", low ZIP not linked.
