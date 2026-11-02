# Hater round 52 (text review, narrow)

Level: light, text only, 5 pages plus 2 checks. Cost: about 3 tool calls. Source: dist/flood-insurance pages against data/c and data/states files, read this session.

## home
Verdict: PASS (visible text only; first ~3,000 characters read). State and county medians shown (Florida $983, Palm Beach $670, Broward $831) match the county and state pages. No wrong sentence found in the part read.

## louisiana
Verdict: PASS (visible text only). "3% above the U.S. median of $1,055" checks: $1,086 / $1,055 = 2.9%. "Half pay between $863 - $1,273" and the 2020s claim share read as labelled. The rest of the page was not read.

## palm-beach-county-fl
Verdict: FAIL with MAJOR

Quote: "FEMA lists another $342,813 in this state under tribal or school-area names, not counted here."

Why:
- The $342,813 is one row only: Miccosukee Tribe of Indians of Florida, disaster 4834 (data/states/florida/data.json, housing). The unplaced rows for Florida total $387,423 across six disasters (4341, 4673, 4675, 4834, 4844, 1544), so "in this state" is understated by $44,610.
- The base is not flood. Every unplaced Florida row sits under a Hurricane declaration (declarations incidentType). The brief rule is flood disasters only, and the flood-only total is $0.
- "School-area" does not appear in Florida's unplaced rows. All 17 groups are tribal or reservation names (Seminole/Miccosukee: Tampa Reservation, Big Cypress, Brighton, Immokalee, Hollywood, Fort Pierce) plus one non-tribal name, Sorrento Shores, at $0.

Exact fix: delete the sentence. The dataset is flood-only and these rows are not flood. If the owner keeps any version, it must state the hurricane base and the full $387,423, not $342,813.

NRI card (checked): "Source: FEMA - National Risk Index (flood). Data: NRI December 2025 release; retrieved October 26, 2026." Renders as one sensible line. "NRI 2023" has no matches in dist (Grep of dist: no files). PASS for this item.

Rest of page (visible text, first ~3,000 characters): medians and the "32% below Florida / 36% below U.S." figures check out. Not checked: the Citizens rule sentence (see Gaps).

## broward-county-fl
Verdict: PASS (visible text only). Broward median $831 matches the home page. "15% below Florida $983" and "21% below U.S. $1,055" check. Florida claim share (69.9%) matches the Palm Beach page. The Citizens rule sentence is unverified (see Gaps).

## new-york-county-ny
Verdict: PASS (visible text only). Median $1,022 and "17% below New York $1,233" check (1 - 1022/1233 = 17%). "3% below U.S. $1,055" checks. Rest of page not read.

## Gaps
- Not read: the rest of the five pages beyond the first ~3,000 visible characters.
- Citizens rule sentence on palm-beach-county-fl and broward-county-fl ("need it in a high-risk zone since 2023; ... since January 2026 ... January 2027"): not checked against the current Florida source. Guardrail 1 requires a raw read. Not a verdict this pass.
- Wider risk, not checked: the flood-only rule. Unplaced rows include non-flood disasters: Florida all Hurricane; Alaska includes Severe Storm and Mud/Landslide. Other housing figures on the pages may have the same gap. Needs a separate check of the incidentType filter in the builder.
- Sorrento Shores (Florida, $0) and Sealaska (Native Regional Corporation, Alaska, $76,980) are neither school nor tribe names. Sealaska is borderline "tribal"; decide wording.
- review/flood-insurance/bethel-census-area-ak (outside the five sections):
  Verdict: FAIL with MAJOR
  Quote: "FEMA lists $78.6 million in this state under tribal or school-area names, which may include it."
  Why: Alaska unplaced rows total $78,707,735.54 across all disaster types ($78.7 million), not $78.6 million. Flood-only rows total $72,682,765.60 ($72.7 million). Neither base gives $78.6 million, and the page is flood-only, so the flood figure is the right base.
  Exact fix: "FEMA lists $72.7 million in this state from flood disasters under school-area and Native-entity names, which may include it." The hedge "may include it" is fair; the Lower Kuskokwim and Lower Yukon school-area groups are the large ones. Bethel-specific match not verified this pass.
