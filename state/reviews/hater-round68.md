# Round 68 (LIGHT: page text only, no screenshots viewed)

Method: read built HTML text of the 6 pages plus zone pages ae, x, ve, ah, d. Checked rules bfe, loma, odds_30, zone_codes, zone_x against rules_registry.py and raw 44 CFR 59/64.3/70 text. No WebSearch SEO pass (light mode), so no GAP-vs-#1 list. Checklist A-N: text-checkable lines (A, C, D, E, F, I, J, M, N) judged; G, H, K (layout, tap targets, contrast, speed) NOT judged, no screenshots. Open lines F (local contacts), I (error report), K (print), L (Spanish) are GAP.

Previous items: round 67 was a machine carry (no BLOCKER/MAJOR listed). Nothing to tally: 0 FIXED, 0 NOT FIXED, 0 PARTLY.

## home
Reached zone pages ae, x, ve, ah, d included.
- **MAJOR** Zone D page (`/flood-zones/d/`): title says "who must insure", but the "Must I buy?" line is the generic "Federal law requires it in a high-risk zone ... outside those zones a lender may still require it." Page never says D is NOT a high-risk zone, so a D-zone reader cannot tell whether they must buy. Zone D text: "land where flood hazards are possible but have not been determined". Reader hesitates or assumes yes/no wrongly. Fix: one sourced line saying D is not in the high-risk zones (so the federal mandate does not apply by zone) and a lender may still require it, or say the data cannot answer it.
- **MAJOR (registry, not yet on dist)** `zone_x` now has a source marked "browser" (fema.gov/about/glossary/flood-zones). `recheck.py` cannot re-fetch it and `state/manual-rule-read.json` has no glossary entry (16 lines, no "glossary" match). CLAUDE.md truth guardrail 6 requires the entry. Wording vs quote otherwise matches: "land between the limits of the 1 percent flood and the 0.2-percent-annual-chance (500-year) flood" for the quote's "between the limits of the base flood and the 0.2-percent-annual-chance (or 500-year) flood" (base flood = 1 percent chance, 44 CFR 59.1, fine); "higher than the 0.2-percent-annual-chance flood" matches; "outside the high-risk areas" = "outside the SFHA", fine. Block ship until the manual-read entry exists.
- **MINOR** `zone_x` repeats itself: "The same rule lists zone B with the moderate kind and zone C with the minimal kind" then "FEMA labels the moderate kind Zone B or Zone X (shaded)". Same fact twice in one paragraph. Also 64.3 text adds "or areas of future-conditions flood hazard" to the moderate row; omitted, harmless.
- **MINOR** Zone X page heading "Do homes in zone X flood?" answers with a share of claim dollars "outside zones A and V", which is not zone X (the text says so, and "not a chance of flooding"). The heading promises a yes/no it never gives; the table column is long and unlike the cost columns. Reader may read North Dakota 62.9% as "zone X floods 63%". Fix: heading "Where do claims come from outside high-risk zones?" or state plainly that homes outside high-risk zones do flood and file claims.
- **MINOR** AE page: H1 "zone AE ... what it costs" but the big first-screen $1,159 / $802-$1,769 / 1,241,599 are "all A zones (AE, A, AH, AO and others)". Labelled right under the figure, so not wrong, but the AE cost sits in the state table below, not on screen 1. Same on VE ($1,787, "all V zones"). Reader on a phone sees a number that is not the zone in the title. Fix: show a national AE median, or lead with the label.
- **MINOR** AH page and D page: no cost figure on screen 1 ("No national median for zone AH alone yet"). Gap line is honest; "yet" implies it will come. AH still shows 25 state rows; D has almost none (47 states under 50 policies).
- **MINOR** `bfe` sentence sits as a bare line under "Buying, refinancing or questioning the zone" with no use for the reader (what a base flood elevation means for building height or price is not said; "base flood" is defined, "water surface elevation" is not). Text matches 59.1: "determination ... of the water surface elevations of the base flood, that is, the flood level that has a one percent or greater chance of occurrence in any given year." Zones AE, AH, VE match 64.3 ("with water surface elevations determined"). Not wrong.
- **MINOR** `loma`: matches 70.1/70.3/70.5 ("owner or lessee" -> "owner or renter" fine; "as a result of the transposition of the curvilinear line to either street or to other readily identifiable features"; "identification of the property to be excluded"). Not wrong. But it presents only the line-drawing reason; 70.1 also says it does not apply after land alteration (omitted), and it gives no link or step for how to ask, and no warning that FEMA may refuse. A homeowner on a hill may think LOMA does not fit. Belongs in GAP: link FEMA's LOMA page.
- **MINOR** `zone_codes` (all state/county pages, not home): "D is not yet studied" is not what 64.3 says ("undetermined but possible, flood hazards"); "V ... coastal high-risk with waves" says waves where the 64.3 row says "with velocity", and the VE zone page says "fast-moving water". Three phrasings for the same zone, none matching the quote exactly.
- **MINOR** `zone_codes`: "B and X are ... moderate, C and X ... minimal" lists X twice; the reader with X cannot tell which. The new `zone_x` shaded/unshaded text resolves it on the X page only; the state/county line stays ambiguous.
- Checked and PASS: `odds_30`. 1 - 0.99^30 = 0.2603, "26% or greater" correct for 1% or greater; scope is "at least one such flood"; no verdict word. Sits after the zone-code list as a non sequitur, MINOR placement only. Zone AE/VE/AH/D/X definitions match the 64.3 quotes. Federal-law "Must I buy?" matches home. FEMA map link goes to msc.fema.gov/portal/home (works as a "check your address" button but a portal home, not an address search; GAP).
- Zone page screen 1 clarity (AE): meaning, must-I-buy, map link and cost all present in that order; clear except the all-A-zones base above. X: clear. VE: clear. AH: no cost. D: must-I-buy unanswered.
- GAP: no sourced list of state insurance dept and floodplain office (F); no error-report route (I); no print stylesheet (K); no Spanish (L).
Verdict: FAIL

## louisiana
- **MINOR** zone-codes paragraph: see home items on "not yet studied", "waves", and X listed twice. Applies here verbatim.
- **MINOR** `odds_30` sentence appended to the zone-code paragraph; correct arithmetic, odd place.
- Rest unchanged since round 67 PASS (text compared only on changed rules). Not re-read in full.
Verdict: PASS

## palm-beach-county-fl
- **MINOR** same zone-code items. The zone table lists "Zone C $546, 123 policies" and "Zone B $870, 116" next to the text "C and X areas of minimal hazard, B and X moderate": consistent. Zone X row is the large one ($620, 38,310) with no moderate/minimal split; the page does not say it cannot split them (the zone X page does).
- Screen 1 (text): $673 / $56 / $518-$1,041 / 23.2% below full risk, then the 32%/37% compare line and the map button. Clear.
Verdict: PASS

## new-york-county-ny
- **MINOR** same zone-code items (line 136).
Verdict: PASS

## utah
- **MINOR** same zone-code items (line 132).
Verdict: PASS

## worcester-county-md
- **MINOR** same zone-code items (line 139). "Other low-risk or unclassified zones" row lumps zone D (undetermined) with low-risk; D is not low-risk by 64.3. Row label could mislead a D-zone reader. MINOR.
Verdict: PASS

## Classes
- Home/zone pages: zone D must-I-buy unanswered (MAJOR); zone_x browser-only source needs manual-rule-read entry before release (MAJOR); AE/VE first-screen number is the wider A or V group; X page heading promises more than the data gives.
- State and county: shared `zone_codes` line wording ("not yet studied", "waves", X in both rows) and appended `odds_30` sentence. Fix once in the registry. Worcester-style "low-risk or unclassified" label.
- All templates: LOMA step and link missing (GAP); no local contacts, error-report route, print stylesheet, Spanish (GAP).
