# Methods review: Outside the Zone, round 5 (narrow confirmation, 2026-11-13)

Inputs: dist/flood-insurance/outside-the-zone/index.html, tools/build_site.py (line 1016, lede, table note), tools/papers.py (spec outside-the-zone), tools/rules_registry.py fema_outside_third, round 4 review, one live fetch of the FloodSmart page. No full recompute.

## Answers
1. FEMA sentence limited to FloodSmart? Mostly yes. New page text: "FEMA's figure uses current high-risk areas and the years 2014 to 2024, and does not say whether it counts only paid claims; this page counts paid claims by the zone rated on each claim." The "all claims" overstatement is gone. Round 4 MAJOR 1 is resolved for that sentence.
2. Hard-coded in shared template? No. build_site.py:1016 now prints html.escape(_sp.get("prior_note") or "") from the paper spec, once per prior rule; the wording lives in papers.py. Remaining small point (MINOR): the note is still emitted beside every key in prior_rules, so a paper with two prior rules would repeat one note. No such paper exists.
3. New label-vs-base errors? None found. Lede "across all U.S. counties combined" (26.6% of 461,197, all counties with a FEMA countyCode) matches the base round 4 reproduced; the 364-county figures are labelled as the separate base. Policy-column note ("share of NFIP policy units in force in the county, every policy type, rated outside zones A and V") matches round 4's CSV check (364 of 364). It does not say policy units are as-of the Policies date while claims are 2016-2025 (round 4 m2, still open, MINOR). "All U.S. counties" slightly overstates: claims with blank or unmatched countyCode are not in it (round 4 m1, MINOR).
4. Remaining BLOCKER/MAJOR from earlier file: round 4 MAJOR 1 resolved. NEW MAJOR 2 (surfaced by this check, not raised in round 4): the printed rule text says "nearly one-third (29%)", but the quoted source excerpt in rules_registry (and the FloodSmart page I fetched today) says only "nearly one-third"; I found no "29%" in the fetched page text. Unless a raw read this session shows 29% in the source, the 29% is unsupported ("keep the source's strength; every sentence quoted"). Fix: drop "(29%)" from the rule text, or add the raw excerpt containing it. Note the page's prior_note no longer compares 29% to 25.9%, so cutting it loses nothing.
Also carried MINOR: Penn State link has no figure or base (round 3/4 m3).

## Verdict
MINOR REVISION once "(29%)" is cut or sourced (as written it is one MAJOR: an unverifiable figure). Everything else confirmed.
