# Hater round 55 (text review, narrow)

Level: light, text only. Scope: year-of-term label (one figure, three sentences).

## home
Verdict: PASS (no change this round; this figure is not on the home page).

## louisiana
- Label true: as-of 2026-07-31, `_yr_span` returns "Jan–Jul 2026"; every counted policy is in force on Jul 31 with a 2026 effective date, so none can sit outside Jan 1-Jul 31 (assuming no future-dated effective dates in the snapshot; not checked in raw data). No "2025" row remains.
- Figure matches data/states/louisiana/agg.json: cost_by_year."2026" median 1215, n 170,190. Page shows "$1,215" and "170,190 policies". Screen 1 and the quote-checker text show the same $1,215.
- MINOR: "This year’s bills: policies whose term began Jan–Jul 2026 (renewals and policies sold this year together) typically pay $1,215" does not say the base is single-family primary-home policies. The table row above it says "single-family homes" and the card text states the base, so the reader is not misled in the table, but the screen-1 sentence and the quote-checker sentence omit it.
- MINOR: policies that began in Jan-Jul 2026 and have already ended are not counted. The label says "term began", not "still in force". Acceptable because the whole card is in-force policies as of Jul 31, 2026.
- "Is it rising" is answered by the full-risk-premium card ("their bills are rising toward it"). Dropping the 2025 row removes the year-on-year comparison, which was cohort-mix-confounded anyway. No gap line is needed.
Verdict: PASS

## palm-beach-county-fl
- Label true (same logic). Page: "Jan–Jul 2026 $679, 28,268 policies". agg.json cost_by_year."2026" is median 679, n 28,268. Match. No leftover 2025 row.
- Sentences read: screen 1, table row and quote-checker text agree. No duplicate paragraph; the three uses are different surfaces.
- MINOR: same missing "single-family primary-home" base on the screen-1 and quote-checker sentences. The n of 28,268 is the priced single-family subset, not all 132,945 policies, and the table row says only "policies".
Verdict: PASS

## Gaps
Did not check raw policy rows for effective dates after the as-of date, or the other 3,000+ pages. Did not render on a phone. Did not check the state pages' build gate. Did not check whether "past year" new-policy wording is consistent with the term-began figure (not in scope).
