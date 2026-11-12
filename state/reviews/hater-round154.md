# Hater round 154 (light): home table scroll box, single answer arrow
Checked at 390x844 (Playwright is_mobile). Figures and layout otherwise unchanged from round 153; no new text diff found.

## home
- MINOR Previous MAJOR FIXED: documentElement.scrollWidth = 390 (body 390); no element pokes past 392 outside a scroll box. The state table (413px) now sits in div.tw (overflow-x:auto, box 350px, scrollWidth 413), so it scrolls inside its box and the five columns stay readable.
- MINOR The scroll box has no visible hint (no shadow or edge fade) that more columns sit to the right; the last column(s) "NFIP claims on record" / "Paid on them" are cut at the edge on first view. Not misleading, reader can swipe.
Verdict: PASS

## louisiana
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- GAP (carried) State page shows four of six answers, no printed line for the missing "How risky?" and "Can I pay less?".
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); all anchors resolve.
Verdict: PASS

## palm-beach-county-fl
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); the six answer lines and their anchors (#required, #zone-cost, #gap, #payout, #crs) present and still read correctly. Round 153 figure checks carried (text unchanged).
Verdict: PASS

## new-york-county-ny
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); the six answer lines and their anchors (#required, #zone-cost, #gap, #payout, #crs) present and still read correctly. Round 153 figure checks carried (text unchanged).
Verdict: PASS

## dixie-county-fl
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); the six answer lines and their anchors (#required, #zone-cost, #gap, #payout, #crs) present and still read correctly. Round 153 figure checks carried (text unchanged).
Verdict: PASS

## levy-county-fl
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); the six answer lines and their anchors (#required, #zone-cost, #gap, #payout, #crs) present and still read correctly. Round 153 figure checks carried (text unchanged).
Verdict: PASS

## sonoma-county-ca
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); the six answer lines and their anchors (#required, #zone-cost, #gap, #payout, #crs) present and still read correctly. Round 153 figure checks carried (text unchanged).
Verdict: PASS

## wakulla-county-fl
- MINOR Previous item FIXED: doubled arrow gone. Text has 0 "→" in the answer lines, CSS adds exactly one (" →" on each jump link); no "→ →" in any built page.
- MINOR (carried, unchanged) "Is it rising? N% ... rising toward it" is true for that N% only; the 18% cap is not on screen 1.
- MINOR (carried, unchanged) Cost line says "median, single-family homes"; base is single-family primary homes, premium + fees (the tile below says it right).
- MINOR No sideways scroll (scrollWidth 390); the six answer lines and their anchors (#required, #zone-cost, #gap, #payout, #crs) present and still read correctly. Round 153 figure checks carried (text unchanged).
Verdict: PASS

## Classes
- Doubled arrow fixed on state and county template.
- Carried: cost-line base label; "rising toward it" scope; state pages show four of six answers with no gap line.
- Home: scroll box has no overflow hint (MINOR).
