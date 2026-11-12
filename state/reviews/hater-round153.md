# Hater round 153 (light): screen-1 six answers, one tile, new h1
Checked at 390x844 (Playwright is_mobile), figures vs data/c/<slug>/agg.json + extras.json + data.json crs. Verified true: share_below, paid-something % (rows minus unpaid_n), NRI ratings, cost_by_zone medians and the zone-unit shares, top community discount names; middle-half spread still in the cost card ("Half of homeowners here pay between ..."). All six answers start by y=661 (<=844) on every county; all anchors (#required, #zone-cost, #gap, #payout, #crs) resolve; no sideways scroll on state/county pages. Parish/county link lists unchanged (23 on Louisiana, none lost).

## home
- **MAJOR** Sideways scroll on the phone: the table after "Highest typical cost: Connecticut $1,510, Hawaii $1,407..." is 413px wide inside a 350px card (right edge 433 at y~4843), so the page layout widens to 433 at a 390 viewport (documentElement.scrollWidth 433). Checklist G (no sideways scroll). Not caused by this change (home unchanged), but live and wrong for the phone reader. Check that should have caught it: a 390px scrollWidth test on home in the phone gate.
- MINOR Home was not changed; its screen 1 (h1 "What flood insurance costs in your state", $1,066 median, $89 a month, 4.5M units) is consistent with its own paragraph below.
Verdict: FAIL

## louisiana
- GAP State page shows only four of the six owner-ordered answers: no "How risky?" and no "Can I pay less?" and no printed line saying why (state has no single FEMA rating; crs is per community). Owner order says all six on screen 1; a gap line or a count (e.g. parishes by rating, from state_risk) is missing.
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR h1 "Louisiana flood insurance and flood zones" vs counties "... flood insurance and zones": two wordings of the same pattern.
- MINOR Figures checked: $1,114 p50, 52.8% share_below, 80.2% paid (470,045 rows, 92,993 unpaid), zones X $1,082 and AE $1,259 (ordered by units, X 174,352 > AE 157,736) all match.
Verdict: PASS

## palm-beach-county-fl
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR "Community discount up to 30% (Boynton Beach)": true (sfhaDiscount 30%, 25 of 40 communities have one) but only the one city; the unincorporated county is 25% and 15 communities have none. The name is shown, so not misleading; the card below has the full list.
- MINOR Claims rows = exactly 10,000 (manifest reported_total 10,000, by_year sums to 10,000, state_total 448,618). Matches, but a round number; confirm it is not a download cap before the 46.8% paid figure is trusted. Figures otherwise match: 46.8% (4,678 of 10,000), FL 72.8%, 23.2% share_below, X $620, AE $1,228, rating High/High.
Verdict: PASS

## new-york-county-ny
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR h1 says "Manhattan, NY" while breadcrumb and title say "New York County"; fine for a Manhattan searcher, but a reader who typed the county name sees the h1 name change. The tile base is only 171 single-family primary homes of 14,925 units (zone X n=159); the page does name AE (41.8% of units) as too few to price, which is honest.
- MINOR Figures match: 63.9% (918 of 1,435 paid), NY 84.3%, 33.9%, X $953, Moderate coastal / Very High inland.
Verdict: PASS

## dixie-county-fl
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR Zone X (22 units, 3.9%) is neither priced nor named as too few; only Zone A (10.4%) is. Harmless, but the sentence names one unpriced zone of two.
- MINOR Figures match: 82.9% (734 of 885), FL 72.8%, 29.7%, AE $1,001, A 59/567 = 10.4%, Moderate / Very Low, no community discount (no sfha discount in data).
Verdict: PASS

## levy-county-fl
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR Zone X $753 (n=51) is priced but hidden behind "more zones below"; the line has two priced zones and one unpriced; OK because the pointer is there. Figures match: AE $2,357, A $958, VE 200/932 = 21.5%, 51.4%, 87.3% (1,124 of 1,288), up to 20% Yankeetown.
Verdict: PASS

## sonoma-county-ca
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR Figures match: AE $1,588, X $1,201, 78.2%, 86.1% (CA 69.2%), 20% Petaluma (county unincorporated has none). Longest answer 2 lines; all six end by y~640.
Verdict: PASS

## wakulla-county-fl
- MINOR Every answer line shows a doubled arrow "→ →" (the text carries a "→" and CSS adds another; source tools/build_page.py ~line 1124 `→</a>`). Looks like a bug on all six lines. Check that should catch it: a text test that an answer anchor's text does not end in the CSS-added glyph.
- MINOR Answer 3 says "a year (median, single-family homes)" but the base is single-family PRIMARY homes, premium + fees (cost_n cohort); the tile right below says it correctly. Label the line the same way.
- MINOR "Is it rising? N% ... under FEMA's full-risk premium: rising toward it" is true for that N% only (by law, most rates rise at most 18% a year, shown in the card below); the rest of the policies are not addressed and the cap is not on screen 1. Reader may read it as "yes, mine rises."
- MINOR Four zones in one line (AE, VE, A, X) is the longest cost sentence; still one line item, ordered by units, and VE $4,496 vs tile $1,471 is a big spread readers see with no note on screen 1 that VE is coastal high-hazard (zone letters are not defined on screen 1; the link goes to the card). Figures match: 82.6%, 56.9%, 15% Wakulla County, Moderate / Very Low.
Verdict: PASS

## Classes
- Template: doubled "→ →" on every answer line (state and county).
- Template: cost line base label drops "primary home / premium + fees".
- State pages: four of six answers, no gap line for the missing two.
- Zone letters (X, AE, VE, A) on screen 1 are not defined in the line itself.
- No wrong figure found. Middle-half spread confirmed in the cost card; nothing a reader needs was lost from screen 1 (2020s paid rate and Citizens rules remain in the body).
