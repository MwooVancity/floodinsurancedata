# Round 69 (LIGHT: page text only, no screenshots, no WebSearch SEO pass, so no GAP-vs-#1 list)

Method: own defect list first from built HTML text of zone pages d, x, ae, ve (judged under home) and the zone_codes line on the five state/county pages; checked against rules_registry.py and the 44 CFR 64.3 raw text (eCFR 2026-10-01) and the FEMA glossary quote supplied. Other cards unchanged since round 68 (not re-read). Checklist A-N judged for the changed text only: C, D, E pass except as listed.

Previous items (round 68 MAJORs): 2 FIXED, 0 NOT FIXED, 0 PARTLY.
- MAJOR 1 zone D "Must I buy?": FIXED. d page now prints "only in a high-risk zone (A or V) ... Outside them, a lender may still require it." Under "Zone D is land where flood hazards are possible but have not been determined." A D reader can see D is not A or V.
- MAJOR 2 zone_x glossary source missing from manual-rule-read: FIXED. state/manual-rule-read.json has "zone_x": "2026-11-06". Page wording matches the glossary quote (shaded = moderate, between base flood and 0.2% flood; unshaded = minimal, outside SFHA and above the 0.2% flood). Repetition gone: two kinds stated once, labels once.

## home
- **MINOR** zone_codes V: "coastal high-risk with velocity, flooded by tides". Matches 64.3 ("with velocity, that is inundated by tidal floods") but "with velocity" is unexplained jargon, and the VE zone page says "fast-moving water". Two phrasings of one thing. Reader hesitates.
- **MINOR** zone D/X/AE/VE "Must I buy?": "Outside them" has a singular antecedent ("a high-risk zone"). Say "Outside it". Also "only ... (A or V)" omits the M and E zones that 64.3(b) lists with mandatory purchase; rare, and 4012a says special flood hazard area. Not misleading for D/X readers.
- **MINOR** zone_x omits 64.3's "or areas of future-conditions flood hazard" on the moderate kind. Glossary-based wording is not wrong.
- **MINOR** zone_codes (carry-over): X is listed in both "B and X moderate" and "C and X minimal"; the unshaded/shaded split is explained only on the X page.
- **MINOR** X page heading "Do homes in zone X flood?" answers with a share of claim dollars outside A and V (labelled "not zone X alone", "not a chance for any one home"). Heading promises more than the data gives.
- **GAP** AE and VE screen 1 shows the all-A-zones / all-V-zones median, correctly labelled right under the figure; exact-zone data due next refresh. D and AH show no national cost (honest gap line). No local contacts list, error-report route, print stylesheet, Spanish.
- Checked PASS: zone_ae, zone_ve, zone_d, zone_x match 64.3 and 59.1 quotes; odds_30 (26%) correct; D table threshold line ("50 or more", "47 more states under 50") consistent.
Verdict: PASS

## louisiana
- **MINOR** zone_codes line: V "with velocity" jargon, X listed twice (see home). Text otherwise matches 64.3 ("possible but undetermined" for D now correct).
Verdict: PASS

## palm-beach-county-fl
- **MINOR** same zone_codes items. Zone B/C/X rows consistent with the line.
Verdict: PASS

## new-york-county-ny
- **MINOR** same zone_codes items.
Verdict: PASS

## bossier-parish-la
- **MINOR** same zone_codes items.
Verdict: PASS

## connecticut
- **MINOR** same zone_codes items.
Verdict: PASS

## Classes
- Zone pages: "Outside them" grammar; "(A or V)" omits M/E; X heading promises more than the claims share gives; AE/VE headline is the group median (labelled; GAP).
- State and county: shared zone_codes line: "with velocity" unexplained, X listed in both moderate and minimal. Fix once in the registry.
- All templates: GAPs unchanged (local contacts, error report, print, Spanish).
