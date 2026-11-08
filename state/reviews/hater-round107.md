# Hater round 107 (LIGHT, text only, no screenshots, no WebSearch)

Method: visible text pulled per page with one script; read the three changed cards (biggest-totals card, screen-1 "Cost in my zone?", decade table note and claims-chart "not final" note) against each page's own tables, then skimmed. Sums checked: decade claim counts add to each page's claim total on all six county/state pages (Sonoma 7,403; Palm Beach 10,758; New York 1,498; Levy 1,316; Dixie 916 incl. the 27 unlisted 1980s claims; Louisiana 485,743).

## home
- **MAJOR** "What does it cost by flood zone?" table lists only AE, X, VE, A, AO, AH. The note under it says "zone D and policies with no zone are left out". That is not true: zones B, C, A99 and the legacy A01-A30 / V01-V30 codes are also left out (Louisiana's own table shows B 4,116, C 13,863, A99 5,169, A10 2,848 priced policies; the builder hard-codes the six zones, `build_site.py` loop over `("AE","X","VE","A","AO","AH")`). A reader in zone B/C/A99 finds no row and is told only D is missing. Check that should have caught it: a "table leaves rows out" oracle comparing the zones listed with every zone code with at least 50 priced policies, and the note naming what is left out.
- MINOR Same table is in no order (AE, X, VE, A, AO, AH): not by cost, not by policy count (X 1.02M is largest, listed second). A hurried reader cannot tell why.
- MINOR The same note links "zone D" as "what each means" although zone D is said to be left out.
- GAP No range sentence ("from $X to $Y") above the zone table as the state pages have.
- Everything else skimmed (median, per month, bases labelled, "Why sites differ" table) reads consistently; bases are named.
Verdict: FAIL

## louisiana
- Biggest-totals card: lead names Katrina ($13.3 billion, 128,785 claims) and table row 1 is Katrina; table is sorted by total paid (13.3B, 2.5B, 1.1B, 691.8M, 513.0M, 412.9M, 334.2M, 244.8M). The catch-all row "Flooding (1978-1998): many floods" ($1.1 billion) sits third and is explained in its own label. It paid less than the lead flood, so no catch-all clause is needed. PASS.
- Screen-1 zone line: "Zone X $1,082, Zone AE $1,259" equals the two largest rows of the cost table (127,267 and 108,782 priced policies). PASS.
- Decade table sums to 485,743; no unlisted decades; no note needed. PASS.
- Chart "Totals for 2025 and 2026 are not final" present. PASS.
- MINOR "Among the five costliest years, these have no flood FEMA named for that year alone: 1995 (their totals are in the yearly chart above)". "their" for one year; and the chart labels only the three costliest years, so 1995 is not readable there.
- MINOR Zone range "From about $624 a year (Zone AO) to $2,821 (Zone V15)": the top end is a legacy code most readers have never heard of and sets a 4.5x span for the whole parish list; the common zones sit at $1,017-$1,259.
- MINOR The "Claims" column in the biggest-totals table counts only claims that paid; the explanation is in the note under the table, while the lead says "over 128,785 claims".
Verdict: PASS

## palm-beach-county-fl
- Biggest-totals card: lead "Hurricane Frances (2004): $11.3 million over 507 claims" equals row 1; sorted descending (11.3, 6.4, 4.6, 4.2, 1.6, 1.5, 1.1). The catch-all "Flooding (1979-2000)" ($1.6 million) is fourth-from-last, labelled "many floods", smaller than the lead, so no catch-all clause. PASS.
- Screen-1: "Largest zones by priced policies here: Zone X $620, Zone AE $1,228" matches the table (38,310 and 9,661). VE (4.7% of units, 115 priced) is below the 10% rule and is in the table. PASS.
- Decades add to 10,758; chart note names 2025 and 2026 and 2025 is one of the three orange years, so the note sits beside the figure. PASS.
- MINOR "Among the five costliest years, these have no flood FEMA named ...: 2025, 1995, 2014": 2025 is both "not final" and unnamed; the reader is not told that 2025 may still rise or that it is the cause of the unnamed total.
Verdict: PASS

## new-york-county-ny
- **MAJOR** Biggest-totals table row "Unnamed flood (1979-1980) | 26 | $156,647". The column is headed "Flood (FEMA's name)" and the lead says "the costliest flood FEMA named", yet this row is a relabel of FEMA's "not a named storm" (`build_page.py` line 777). It spans two years and 26 claims, so it is very likely several floods, but unlike the "Flooding (...): many floods" rows it carries no explanation. The label implies one flood; the data under it cannot show that. This is the same class that failed Sonoma last round (an unexplained catch-all row). Check that should have caught it: any row whose year span is more than one calendar year and which is not a FEMA-named event must carry the "many floods" wording.
- Biggest-totals lead "Hurricane Sandy (2012): $111.4 million over 442 claims" equals row 1; sorted descending. The catch-all "Flooding (1978-1996)" ($624,518) is correctly labelled. PASS apart from the row above.
- Screen-1 zone line: "Largest zone by priced policies here: Zone X $953 a year (...; Zone AE, 41.8% of policy units, has too few to price)". Matches the cost table (only X, 159 priced policies) and the units table (AE 6,232 = 41.8%). Good fix. PASS.
- Decades add to 1,498; no unlisted decade. PASS.
- MINOR The cost-in-zone section has one row (159 priced policies) against 14,925 policy units; the section says "find its row below" without saying AE has no row. Screen 1 says it; the section heading block does not.
Verdict: FAIL

## sonoma-county-ca
- Previous failure (lead $3.5M above an unexplained $67.3M row): FIXED. Lead now reads "The costliest flood FEMA named here was Pineapple Express Southern (1998): $3.5 million over 284 claims. The costliest year, 1995 ($35,936,682), has no single named flood. Catch-all Flooding (1978-1997), many floods: $67.3 million." The table is sorted by total paid with the $67.3 million row first, labelled "Flooding (1978-1997): many floods; FEMA's records use this name for claims in several years" (3,742 claims, average $17,984 = 67.3M/3,742). The reader can now reconcile lead and table. PASS.
- Check that 67.3 + 3.5 + 0.24 million stays below the yearly total $131.7 million: yes.
- Screen-1 zone line "Zone AE $1,588, Zone X $1,201" matches the table (651 and 348 priced policies). PASS.
- Decades add to 7,403; chart note "Totals for 2025 and 2026 are not final" present. PASS.
- MINOR Phone: row 1's first cell is a two-line label (about 90 characters) in a narrow first column; the fix is correct but heavy on a 390 px screen. Shorten to "Flooding (1978-1997): many floods" and move the explanation under the table.
- MINOR "Among the five costliest years ... 1995, 2019, 2005, 1986, 1997": the sentence says the totals are in the chart, but the chart labels only three bars.
Verdict: PASS

## levy-county-fl
- Biggest-totals lead "Hurricane Helene (2024): $25.2 million over 253 claims" equals row 1; sorted descending; no catch-all row. PASS. Helene 253 claims, Idalia 148 claims; yearly 2024 $26.5M and 2023 $13.0M agree with $25.2M / $13.0M within ICC and other 2024 claims.
- Screen-1: "Largest zones by priced policies here: Zone AE $2,357, Zone A $958 ... (Zone VE, 21.5% of policy units, has too few to price)". Matches the table (228, 72; X has 51) and the units table (VE 200 = 21.5%). PASS.
- Decades (77, 480, 85, 181, 493) add to 1,316; chart note names only 2026 (no 2025 claims shown in the top years); fine.
- MINOR The cost-in-zone lead "From about $753 a year (Zone X) to $2,357 (Zone AE) here" leaves out Zone VE (21.5% of the policy units, coastal, likely the dearest). The footnote says zones under 50 priced policies are omitted but does not name VE here; the range reads as the whole county. Name the omitted zone in that sentence.
- MINOR "Blizzard of 1993 (1993)" repeats the year.
Verdict: PASS

## dixie-county-fl
- Biggest-totals lead "Hurricane Helene (2024): $9.0 million over 125 claims" equals row 1; sorted descending (9.0, 3.1, 3.0, 1.5, 1.2, 0.77); no catch-all. PASS.
- Screen-1: "Largest zone by priced policies here: Zone AE $1,001 a year (...; Zone A, 10.4% of policy units, has too few to price)". Matches the cost table (AE 134 priced only) and the units table (A 59 = 10.4%). VE (4.2%) and X (3.9%) fall under the 10% rule. PASS.
- Decade note "Decades with too few claims for a share are not listed: 1980s (27 claims)": 458+89+80+262+27 = 916, equal to the page's claim total. PASS.
- Chart: no "not final" note, and the data reads "1980-2024" (policies as of August 2026). Consistent, but a reader is not told that no 2025-2026 claims are in the file; MINOR.
- MINOR Cost-in-zone section shows one row; the other zones are said omitted but not named in that section.
Verdict: PASS

## Classes
- All county/state templates: a biggest-totals row that is not a FEMA-named single event must say so. "Flooding (...)" rows do; "Unnamed flood (...)" (New York) does not. Fix at the source in `build_page.py` line 777 (give the relabelled row the same "many floods" wording whenever the year span is more than one year), and add a mutation test.
- Home / national tables: any "leaves out" note must name every omitted class, and the row list must come from data, not a hard-coded list of six zones.
- Cost-in-zone section on county pages with a zone omitted for too few priced policies: the range sentence and the table should name the omitted zone, as screen 1 now does.
- "Among the five costliest years ... (their totals are in the yearly chart above)" refers to a chart that labels only three years; hold this to MINOR but reword.

## Tally
home FAIL (1 MAJOR), louisiana PASS, palm-beach-county-fl PASS, new-york-county-ny FAIL (1 MAJOR), sonoma-county-ca PASS, levy-county-fl PASS, dixie-county-fl PASS. Previous-round items checked: Sonoma lead/row contradiction FIXED. The three changes under review (biggest-totals lead and sorted table, screen-1 zone naming and "too few to price", decade note and "not final" note) are correct on every page where they appear; the two failures are the national zone table's false "only D left out" note and New York's unexplained "Unnamed flood" row.
