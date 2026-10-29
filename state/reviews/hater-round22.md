# Hater round 22: disaster list, merged same-day lines

Scope: one change, duplicate disasters (same month, title, type) shown as one line with "(N separate declarations)". Read from dist/ page text only, plus data/states/maine/data.json.

## home

No disaster list on this page (no "How often" card, no "declaration" text). Tokens scanned: no undefined, NaN, null or [object. Nothing broken.

Verdict: PASS

## louisiana

No merged line on this page. Visible list: "June 2026 — Tropical Storm Arthur", "September 2024 — Hurricane Francine", "September 2021 — Tropical Storm Nicholas (emergency declaration)", "August 2021 — Hurricane Ida", "June 2021 — Severe Storms, Tornadoes, and Flooding", "October 2020 — Hurricane Zeta". No repeated lines, no bad tokens.

Not checked: the "70 federal disasters" count and the list against a Louisiana data file (none was given for this round).

Verdict: PASS

## palm-beach-county-fl

No merged line on this page. Visible list: "October 2024 — Hurricane Milton", "November 2022 — Hurricane Nicole", "September 2022 — Hurricane Ian", "August 2020 — Hurricane Isaias (emergency declaration)", "August 2019 — Hurricane Dorian", "September 2017 — Hurricane Irma". No repeated lines, no bad tokens.

Not checked: the "19 federal disasters" count and the list against county data (none given for this round).

Verdict: PASS

## broward-county-fl

No merged line on this page. Visible list: "October 2024 — Hurricane Milton", "April 2023 — Severe Storms, Tornadoes, and Flooding", "November 2022 — Hurricane Nicole", "September 2022 — Hurricane Ian", "August 2020 — Hurricane Isaias (emergency declaration)", "August 2019 — Hurricane Dorian". No repeated lines, no bad tokens.

Not checked: the "23 federal disasters" count and the list against county data (none given for this round).

Verdict: PASS

## maine

MAJOR: the note under the list says "Only the latest are listed, newest first, one line per disaster", but the merged line directly above it covers two disasters. "September 2023 — Severe Storm and Flooding (two separate declarations)". A reader is told one line equals one disaster, and this line is two. Fix the note to say "one line per disaster, or per same-title group of declarations" (or similar), so the sentence stays true.

MINOR: the merged line gives no declaration numbers or dates, so a newcomer cannot see that the two are different disasters. The source has DR 4736 (declared 2023-09-05) and DR 4737 (declared 2023-09-06). "(two separate declarations)" would read clearer as "(two declarations, Sept 5 and Sept 6)" or show the numbers. Also "declarations" is not explained at this line.

Checked against data: the "September 2023 — Severe Storm and Flooding (two separate declarations)" line is TRUE. data.json has exactly two distinct disasterNumbers for SEVERE STORM AND FLOODING DR in 2023-09: 4736 and 4737. The merge counts distinct disasterNumbers, not rows. Other recent lines (March 2024 DR 4764, January 2024 DR 4754, July 2023 DR 4719, and others) each have one distinct number, so no count is shown, which is correct.

Not checked: the "46 federal disasters" count was not recomputed. Hurricane Lee (EM) has 16 identical rows with disasterNumber 3598. The page shows it once, which is right, but the source is padded with duplicate rows.

Verdict: FAIL

