# Hater round 147 (light): compare line reworded after screen-1 reorder

Checked: the median vs median tile and agg.json, % above/below state and U.S., rank and N (recomputed from every county agg.json with 100+ priced policies), ZIP range vs by_zip, reading position. U.S. median $1,066 used.

## louisiana
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $1,114 vs U.S. $1,066 = 4.5%, shown "5%" (rounds up); 16th highest of 51 (50 states + DC) is correct.
- MINOR "The median, $1,114, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $1,114 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
- MINOR (round 146, still true) "Pick your parish" is now a real collapsed `<details>` (no `open`), so the parish links are hidden behind a tap; checklist G says nothing hidden or collapsed. Not a defect in the compare line.
- MINOR (round 146, still true) The state quick-answer list has no "How risky" or "Can I pay less" item, unlike counties (GAP at most). No ZIP line on a state page, correct.
Verdict: PASS

## palm-beach-county-fl
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $673: -31.7% vs FL $985 ("32%"), -36.9% vs U.S. ("37%"); 8th lowest of 55 correct.
- **MAJOR** Range drops rows without saying so (label-vs-data, HATER-PROMPT D/C). "By ZIP, the median ranges from $451 (33484) to $1,830 (33480 Palm Beach); find your ZIP." is built from only 51 of the 61 ZIPs on policy records here (the rest have no median: too few priced policies) (10 left out). A reader whose ZIP is one of the unpriced ones reads "the median ranges from A to B" as covering their ZIP, and it may not. The line does not say "of the 51 ZIPs with enough priced policies". Check that should have caught it: a gate that a ZIP-range sentence names how many ZIPs it covers when any ZIP is left out (same class as the C10-C14 label checks).
- MINOR "The median, $673, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $673 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
- MINOR (round 146, still true) "Cost in my zone?" starts just below the first screen because the long Citizens clause precedes it; the $673 tile covers cost.
Verdict: FAIL

## new-york-county-ny
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $1,021: -19.0% vs NY $1,261, -4.2% vs U.S.; 11th lowest of 48 correct. Only one ZIP (10014) has a median, so no ZIP line prints: correct.
- MINOR "The median, $1,021, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $1,021 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
- MINOR (round 146, still true) "Cost in my zone?" shows one zone only (X); no defect.
Verdict: PASS

## dixie-county-fl
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $987: +0.2% vs FL $985, so "within one percent" is true; -7.4% vs U.S. ("7%"); 25th highest of 55 correct (rank by $987; FL median is lower than the county's by $2, wording does not call it "above", fine).
- **MAJOR** Range drops rows without saying so (label-vs-data, HATER-PROMPT D/C). "By ZIP, the median ranges from $654 (32628) to $1,011 (32680); find your ZIP." is built from only 2 of the 10 ZIPs on policy records here (the rest have no median: too few priced policies) (8 of 10 left out, so "ranges" is between just two ZIPs). A reader whose ZIP is one of the unpriced ones reads "the median ranges from A to B" as covering their ZIP, and it may not. The line does not say "of the 2 ZIPs with enough priced policies". Check that should have caught it: a gate that a ZIP-range sentence names how many ZIPs it covers when any ZIP is left out (same class as the C10-C14 label checks).
- MINOR "The median, $987, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $987 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
- MINOR Same wording in the ZIP section ("Typical costs run from $654 ... to $1,011") has the same left-out-rows issue.
Verdict: FAIL

## levy-county-fl
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $1,628: +65.3% vs FL ("65%"), +52.7% vs U.S. ("53%"); 4th highest of 55 correct.
- **MAJOR** Range drops rows without saying so (label-vs-data, HATER-PROMPT D/C). "By ZIP, the median ranges from $1,087 (32626) to $3,204 (34498 Yankeetown); find your ZIP." is built from only 4 of the 13 ZIPs on policy records here (the rest have no median: too few priced policies) (9 left out). A reader whose ZIP is one of the unpriced ones reads "the median ranges from A to B" as covering their ZIP, and it may not. The line does not say "of the 4 ZIPs with enough priced policies". Check that should have caught it: a gate that a ZIP-range sentence names how many ZIPs it covers when any ZIP is left out (same class as the C10-C14 label checks).
- MINOR "The median, $1,628, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $1,628 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
Verdict: FAIL

## sonoma-county-ca
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $1,266: +20.0% vs CA $1,055, +18.8% vs U.S. ("19%"); 12th highest of 42 correct.
- **MAJOR** Range drops rows without saying so (label-vs-data, HATER-PROMPT D/C). "By ZIP, the median ranges from $1,139 (94931) to $1,757 (95462 Monte Rio); find your ZIP." is built from only 13 of the 37 ZIPs on policy records here (the rest have no median: too few priced policies) (24 left out). A reader whose ZIP is one of the unpriced ones reads "the median ranges from A to B" as covering their ZIP, and it may not. The line does not say "of the 13 ZIPs with enough priced policies". Check that should have caught it: a gate that a ZIP-range sentence names how many ZIPs it covers when any ZIP is left out (same class as the C10-C14 label checks).
- MINOR "The median, $1,266, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $1,266 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
Verdict: FAIL

## wakulla-county-fl
- Verified: The median matches the tile and data (agg.json policies.p50); the percent, the state/U.S. medians and the rank were recomputed and are true. $1,471: +49.3% vs FL ("49%"), +38.0% vs U.S.; 5th highest of 55 correct.
- **MAJOR** Range drops rows without saying so (label-vs-data, HATER-PROMPT D/C). "By ZIP, the median ranges from $1,173 (32358) to $3,984 (32346); find your ZIP." is built from only 4 of the 6 ZIPs on policy records here (the rest have no median: too few priced policies) (2 left out). A reader whose ZIP is one of the unpriced ones reads "the median ranges from A to B" as covering their ZIP, and it may not. The line does not say "of the 4 ZIPs with enough priced policies". Check that should have caught it: a gate that a ZIP-range sentence names how many ZIPs it covers when any ZIP is left out (same class as the C10-C14 label checks).
- MINOR "The median, $1,471, ..." does not say median of what (yearly single-family cost, premium plus fees); the base sits only in the tile label about 1.5 screens up, and the list just above it prints zone medians ("Cost in my zone? ... a year (median, single-family homes)"), so the reader can take $1,471 for a zone median. Far smaller than last round's dangling "That": the figure is now printed, so the reader can match it to the tile. Previous MAJOR (dangling "That"): FIXED.
Verdict: FAIL

## Classes
- County pages with 2+ priced ZIPs: the ZIP-range line omits unpriced ZIPs without saying so; fix by naming the count ("of the N ZIPs with enough priced policies") in the sentence.
- All pages: "The median" lacks its base next to the figure.
