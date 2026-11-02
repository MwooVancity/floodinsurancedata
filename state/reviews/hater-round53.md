# Hater round 53 (text review, narrow)

Level: light, text only. Cost: 3 tool calls. Source: dist/flood-insurance/palm-beach-county-fl/index.html as it stands now (the rebuild was not waited for; if dist is older than the rebuild, re-read after it lands), and tools/build_page.py template strings.

## home
Verdict: PASS (visible text only, as in round 52). Not re-read this round; no change to home text was reported.

## louisiana
Verdict: PASS (visible text only, as in round 52). Not re-read this round.

## palm-beach-county-fl
Verdict: FAIL with MAJOR

Quote: "For the same disasters FEMA lists another $342,813 elsewhere in this state under names that match no county, such as tribal or school areas, not counted here."

Why:
- The base is now stated, and the wording is clearer. But the number is still the one row for disaster 4834 (Miccosukee Tribe of Indians of Florida).
- The declarations for 4834 show incidentType Hurricane (data/states/florida/data.json). The page's own note says only disasters in the flood-disaster card are included, and the card is flood-only. If 4834 is not in that card, the sentence should not show this figure at all.
- This pass did not confirm which disasters the flood card counts. The Palm Beach data file lists 41 declarations, so "the same disasters" is not checkable from this sentence alone.

Exact fix: check the flood-card disaster list for Florida. If 4834 is not on it, delete the sentence (Florida's flood-only unplaced total is $0). If it is on it, name the disasters in the sentence, for example "from disasters 4834 and ..." so the base is visible. Do not show $342,813 as the state total.

NRI card: no change this round (round 52 PASS: source line renders; "NRI 2023" absent from dist).

## broward-county-fl
Verdict: PASS (visible text only, as in round 52). Not re-read this round.

## new-york-county-ny
Verdict: PASS (visible text only, as in round 52). Not re-read this round.

## Gaps
- Bethel (review/flood-insurance/bethel-census-area-ak, not rebuilt): judged from tools/build_page.py line 1103. Template reads "None is on record under this {UNIT}'s name, but for the same disasters FEMA lists {unplaced} elsewhere in this state under names that match no {UNIT}, such as tribal or school areas, which may include it." Wording is clear: the base is stated, and "may include it" is a fair hedge. Verdict: PASS on wording. Base not verified: it depends on h_unplaced using the same disaster set as the page. Re-read after the Bethel rebuild.
- Template line 1105 (palm-beach and other county pages) carries the same "for the same disasters ... such as tribal or school areas" wording. Florida's unplaced rows are tribal names only, so "school areas" does not apply there. Consider naming only the categories that occur in that state.
- Flood-card disaster list for Florida not verified this pass (see palm-beach FAIL).
- Round 52 items still open: Citizens rule sentence not checked against source; other housing figures may include non-flood incidents; Sealaska and Sorrento Shores category question.
