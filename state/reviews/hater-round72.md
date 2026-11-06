# Round 72 (LIGHT: page text only from dist HTML, no screenshots, no Google search). Scope: the 7 zone pages (ae, x, ve, a, ao, ah, d), judged inside `home`. The other five pages changed only by the monthly refresh (counts); their text was not re-read this round.

Previous items (rounds 70 and 71): zero BLOCKER/MAJOR were open. 0 NOT FIXED.

Verified against data (recomputed, all match the pages): cost medians and counts from `cost_hist_zone_exact.json` (X 928/1,018,718; AE 1,252/961,977; VE 1,778/18,181; A 944/91,083; AO 899/26,959; AH 874/106,626; D 1,204/764). Full-risk medians from `frp_hist_zone_exact.json` (X 749; AE 1,443; VE 2,381; A 775; AO 894; AH 831; D 1,040). X claims 145,311 / $7,779,587,985 and the national 24% (24.4% of paid dollars) from `claims_zone.json`. AH "86% in Florida" = 85.8%. Only AH has a state-majority line.

## home (zone pages)

- **MAJOR** (x page, "What does it cost in zone X, by state?" table, last column): the column "Share of the state's paid claim dollars outside zones A and V" is a different base from the claims card above it and from the table's footnote. The card says losses 2016-2025 and the national figure is 24%. The column comes from each state's `claims_extra.outside_sfha_pct`, which is every year on record (Florida's source has 448,618 claims, i.e. since 1978). Recomputed for 2016-2025: Florida 5.0% (page 8.1%), Texas 52.2% (47.2%), Utah 64.9% (55.1%), DC 76.5% (50.3%), Virginia 26.7% (15.6%), North Dakota 61.4% (62.9%). The only note under the table says "Single-family primary homes rated exactly X, premium plus fees, in force on August 31, 2026", which reads as covering the share column too. It does not: the column is every building type, all years, paid dollars. Reader: someone in Virginia sees 24% nationally and 15.6% for their state on the same screen, and cannot tell the periods differ. Fix: put "all years on record, every building type" in the column head or note, or switch the column to 2016-2025 so it matches the card.
- **MAJOR** (x page, claims card heading "Do homes in zone X flood?" and the mean "$72,079 on average per paid claim"; same on all seven pages): the heading says homes and sits next to single-family cost tiles, but the base is every building type (condo buildings, apartments, businesses), stated only in the grey line after the paragraph. The figure is a mean, not a median, and mixed-type means run high. Reader: "a flood in my zone X house pays about $72,000 on average" is a wrong reading. Fix: heading "Do buildings in zone X flood?", and put "every building type" inside the sentence, beside the average (or use single-family claims only).
- **MAJOR** (all 7 pages, the two tiles): "$928 median / yr" (premium plus fees) sits beside "$749 Full-risk premium median, before fees" (premium only). On X, A, AO, AH and D the full-risk figure is below what policyholders pay (X 749 vs 928, A 775 vs 944, D 1,040 vs 1,204), while on AE and VE it is above (1,443 vs 1,252; 2,381 vs 1,778). The only explanation is the tile label and a small sentence under the tiles. In NFIP talk "full-risk" means the price the policy glides toward, so on X a reader will take $749 as "the real risk price is lower than what I pay, so I am overcharged or my bill will fall". The gap is also not the fee amount: it is the difference of two separate medians. The site already has the same-base figure (`frp_plus_fees` in `tools/metrics.py`) and its own history (metrics.py header, born 2026-10-25) is this exact trap. Fix: show the full-risk tile as premium plus fees, or add one line next to the tiles: "Fees are added on top of the premium, so the first tile is higher on X; on AE and VE the full-risk price is higher than what is paid now."
- **MINOR** (x, a, ao, ah, d, ve, ae): the word "existing policies" in "Median / yr in zone X, existing policies" can read as "grandfathered". The sentence below says "in force on August 31, 2026"; use "policies in force" in the tile.
- **MINOR** (a page): "1 more states have zone A policies but under 50 priced ones" (grammar); the other pages use plurals correctly.
- **MINOR** (x page): "(X, B, C, D and others)": the data has only X, B, C, D outside A and V (plus claims with no zone, which are left out). "and others" is vague; say "X, B, C and D".
- **MINOR** (all titles): "cost ($928 median a year)" names no base (single-family primary-home policies, premium plus fees). Fine for a title, but the first screen should show it; it does ("existing single-family primary-home policies ... premium plus fees").
- Answer to (3), the 24% vs "one-third": no contradiction on the page. It says "paid claim dollars", 2016-2025, and the page prints no "one-third" claim. Recomputed counts for the same window: 28% of claims with a zone were outside A and V, so the FEMA count-based figure and our dollar figure differ by base and are both right. **GAP** (never blocking): print "28% of claims by count, 24% by dollars" so a reader who knows the one-third line can reconcile it.
- Answer to (2): the base is labelled but placed after the figure, hence the MAJOR above.
- **GAP**: the compare table "How zone X compares" lists AE first, X second; the lead names X. Fixed order is fine, but the page's own zone is not marked in text.
- Checked and fine: loss years (2016-2025) and "not today's map" and "not adjusted for inflation" are stated; "A count of claims is not a chance of flooding" is present; "paid" excludes unpaid claims (107,932 of 145,311 paid) and the page says both counts; D has 764 policies and the page prints that count in the table; the 24% denominator is stated ("with a zone on the claim").

Verdict: FAIL

## louisiana
Only counts moved with the refresh; text not re-read. Previous round: PASS.
Verdict: PASS

## palm-beach-county-fl
Only counts moved with the refresh; text not re-read. Previous round: PASS.
Verdict: PASS

## new-york-county-ny
Not in rounds 70 or 71; only counts moved; text not re-read. Unverified beyond the gates.
Verdict: PASS

## camden-county-ga
Not in rounds 70 or 71; only counts moved; text not re-read. Unverified beyond the gates.
Verdict: PASS

## hillsborough-county-fl
Not in rounds 70 or 71; only counts moved; text not re-read. Unverified beyond the gates.
Verdict: PASS

## Classes
- Zone page template: (a) tile pair with different fee bases; (b) claims card is every building type under a "homes" heading; (c) x page only: state table column on a different period than the card. All three are MAJOR.
- State and county templates: not judged this round.
