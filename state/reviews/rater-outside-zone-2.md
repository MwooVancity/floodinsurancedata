# Rater review 2: /flood-insurance/outside-the-zone/ (local build, noindex) - 2026-11-13

Rater stance: Search Quality Rater Guidelines, YMYL (financial / insurance). Files read: dist/flood-insurance/outside-the-zone/index.html, dist/about/index.html, dist/methodology/index.html, dist/data/outside-the-zone.csv. Previous: rater-outside-zone-1.md (Medium). Nothing edited.

## 1. Needs Met
- "flood claims outside flood zone by county": Highly Meets (unchanged). Policy-share and largest-named-flood columns now let a reader read a county's number in context. Not Fully: no state jump on a 364-row, 7-column table on a phone; the two new columns have no stated source or date and are not in the CSV.
- "do floods happen outside high risk flood zones": Moderately Meets, upper end (up from Moderately). The lede now answers before "Abstract" and quotes FEMA's 29%. Held back: it never says "Yes" in homeowner words ("25.9% of claims with a payment and a rated zone ... rated outside zones A and V" is still analyst phrasing); the headline 25.9% comes from the 364 largest counties while the 2,042 left-out counties pool to 34.7%, and the lede does not say so; no line on what this means for a zone X owner (NFIP not required, still available, 30-day wait).

## 2. Page Quality: Medium (unchanged; closer to Medium+)

## 3. Previous reasons: status
- Ad script with no ad disclosure: RESOLVED. About now names Google AdSense and says ads never change a figure.
- Claim share without policy share: PARTLY. Column added, but it is unlabelled as to source (NFIP Policies v3 is not named in "Data"), as-of date, base (in-force policies today vs claims 2016-2025 rated at the time) and is missing from the CSV. See MAJOR 2.
- Prior studies unlinked, no FEMA figure: PARTLY. Penn State PSIRC one-pager linked. FEMA's 29% quoted but with no link, no document name and no date; UNC study dropped silently (fine if not verifiable). See MAJOR 3.
- Research layout hard for homeowners: PARTLY. Plain lede and first-published date added; Abstract / Question / Data / Methods (Wilson score, fifths, "meet the measure", "base") still sit between the lede and the table; Reproduce / How to cite / Versions still separate sections.
- Anonymous site: NOT RESOLVED (owner's decision; About states it openly, which is honest but still caps E-E-A-T on YMYL).

## 4. Reasons it is not High (each MAJOR)
1. MAJOR [OWNER ONLY - identity] No accountable person or organisation on a YMYL money topic. About now says "run anonymously, by choice". With ads disclosed and no reputation, no named reviewer and no external citations, a rater stops at Medium. Only the owner can change this (a named editor, role and relevant experience, or an accountable organisation; or a named independent reviewer of the method).
2. MAJOR [PAGE FIX] New column is a label-vs-data risk. "Policy units outside A and V today" compares current policies with claims rated at loss over 2016-2025; the page does not name its dataset, as-of date, or say "policy units" (not homes, not policies) in the Data section, and the CSV omits it, so it cannot be checked. Same for "Largest named flood": the FEMA field (floodEvent) is not in the "fields used" list, the count is "all zones" (includes claims with no rated zone, a different base from the Count column) and the Results line "more paid claims (all zones) than half the county's base" mixes the two bases. Rows like "Hurricane Isaias (2020): 1" as a county's "largest named flood" read as machine output.
3. MAJOR [PAGE FIX] FEMA comparison is unsourced and printed twice. The 29% sentence appears verbatim in the lede and again in Prior work, with no link, publication name or date. Its base differs from the page's (all NFIP claims nationally, 2014-2024, outside *current* high-risk areas vs paid claims with a rated zone, 2016-2025, 364 counties, zone at rating) and the page does not say so; a reader sees 25.9% vs 29% and cannot tell whether they disagree.
4. MAJOR [PAGE FIX] Headline figure is the selected-county figure. The lede leads with 25.9% for 364 big-claim counties; the left-out 2,042 counties pool to 34.7% (stated only in Methods). For the question "do floods happen outside high-risk zones", the all-county figure (and the 34.7%) belongs in the lede; otherwise the page understates the answer next to FEMA's 29%.
5. MAJOR [PAGE FIX] "A county's share mostly follows where its policies are written" is an unquantified inference in the lede. Either print the measured relationship (for example how many counties have claim share within X points of policy share, computed and gated) or cut "mostly follows" to the instruction to compare the two columns.

## 5. New items that lower trust or could mislead
- Duplicate paragraph (FEMA 29% twice) reads as template assembly.
- Title still "Outside the zone: ...: 364 U.S. counties" (two colons, count-in-title); meta description still a method sentence, not an answer.
- "Highest fifth" still repeated in every row (73x each).
- Pooled 25.9% still dominated by Harris (55,323 of 424,932) with no note; the new named-flood column shows Harvey 42,343 there, so the weighting is now visible but unexplained.
- Zone D still folded into "outside A and V" in the headline (stated in Data only).
- "19 of the 50 counties with the highest shares are in Texas" still uses an arbitrary 50.
- No Dataset JSON-LD (not a rater item).

## 6. Changes that would raise the rating (ranked)
1. Owner: give the site an accountable identity or a named independent reviewer of the method (only path from Medium to High on YMYL).
2. Name the source, as-of date and base of the policy-unit column (NFIP Policies v3, in-force units, rated zone today) and of the named-flood column (floodEvent, all zones) in Data; add both to the CSV; fix the mixed-base Results sentence; show "none named" for counties whose largest named flood is under a set floor or drop the floor-less rows.
3. Link FEMA's 29% source by document name and date (raw text read), print it once, and add one line on how its base differs from this page's.
4. Lede in homeowner words: "Yes." + all-county pooled share (and 34.7% for counties not listed) + what it means for a zone X owner (not required by lenders, available, 30-day wait), linked to the site's existing pages.
5. Quantify or cut "mostly follows".
6. State index or per-state jump links; one fifth heading per group instead of 364 row labels; one-colon title with the answer; move Abstract/Methods/Reproduce/Cite below the table.
7. Note Harris/Harvey weight and show zone D separately.
