# Hater round 47 (light, text only)

Scope: the seven changed-wording items. Built text read from dist/flood-insurance/<slug>/index.html, figures recomputed from data/c and data/states. No build, no commit, no screenshots.

## home
Verdict: FAIL
MAJOR: "None are coded to this county" / "How often is this county a flood disaster?" (template, shown on virginia-beach-city-va). Virginia Beach is an independent city, not a county; the page header says "city" and the body says "this county". Cause: tools/build_page.py:48 sets UNIT to "county" for every state except LA (parish) and AK (borough), so city pages get the wrong label. Fix: take the unit from the place type. Not on this page's text; counted against every sample under the template rule.

## louisiana
Verdict: FAIL
MAJOR: "Hurricane Katrina alone paid $13.3 billion including code-upgrade (ICC) pay" is correct (13,303,427,706), but the shared template defect above ("this county", tools/build_page.py:48) counts against every sample. Fix as above.

## palm-beach-county-fl
Verdict: FAIL
MAJOR: "None are coded to this county" template defect (see home). Not on this page's text; counted against every sample under the template rule. Checked and correct: data.csv has the "row" column, pct_vs rows read "state below, 32%" ($670 vs $983) and "us below, 36%" ($670 vs $1,055); "FEMA gives no county for 1.1% ... 1,444 of its claims" matches Florida; repeat card 216 matches county 12099.

## broward-county-fl
Verdict: FAIL
MAJOR: "None are coded to this county" template defect (see home). Not on this page's text; counted against every sample under the template rule. Checked and correct: "April Florida Flooding alone paid $244.5 million" (244,475,829); repeat card 636 matches county 12011; no-county line matches Florida.

## new-york-county-ny
Verdict: FAIL
MAJOR: "None are coded to this county" template defect (see home). Not on this page's text; counted against every sample under the template rule. Checked and correct: "Hurricane Sandy alone paid $111.4 million" (111,415,427); repeat card 8 matches county 36061.
MINOR: "2008: 1 claims" and "2020: 1 claims" in the year list. Grammar only. Fix: singular/plural on the year-count label in the template.

## Gaps
- fairfield-county-ct: PASS on items 1, 2, 3, 4, 5. Aid $26.0M and $2,199 per registration recomputed from the seven flood disasters (11,836 registrations, $26,032,794). Payout "Hurricane Sandy alone paid $155.4 million" (155,385,404) matches. The Connecticut sentence is true: the nine NRI rows are planning regions 09110 to 09190, and county 09001 is absent. Repeat card 1,316 and uncoded 1 match.
- virginia-beach-city-va: aid $6.3M and $914 per registration recomputed (6,914 registrations, $6,322,464) and belongs to Virginia Beach. "Hurricane Matthew alone paid $52.2 million" (52,187,373) matches. Uncoded 1,001 reproduces with the builder rule; "may have some" is a fair hedge. Defect: "this county" on a city page, MAJOR (see home).
- miami-dade-county-fl: PASS. Repeat 4,506 = 785 (code 12086) + 3,721 (old code 12025); SRL 12 = 6 + 6; uncoded 5 matches the builder rule; no-county 1.1% and 1,444 match Florida. The merge is correct.
- ocean-county-nj: PASS. "Hurricane Sandy alone paid $2.5 billion" (2,481,896,683) matches. The "which pulls the average up" clause is true (ICC is added to the total).
- sacramento-county-ca: PASS. "Flooding alone paid" is gone and nothing replaces it badly. Year list has "1985: 1 claims" (MINOR, same grammar slip as NY).
- kanawha-county-wv: UNVERIFIED. No-county 10.5% and 708 claims were not recomputed (West Virginia data not checked). Year list has "1984: 1 claims" and "2017: 1 claims" (MINOR).
- Not exercised by any page checked: the singular path ("1 community", "the worst year was"). Also the "state above" branch of pct_vs (every check here was "below"). Both unverified.
- Tiles: "Half pay between" is absent on home, where no spread is shown, and present on the other five pages. Nothing reads broken.
