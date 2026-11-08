# Hater round 106 (light, text only)

Method: pages stripped to text and read; the four changed items checked against each page's own tables and year lists
(decade sums recomputed from the yearly list). No screenshots, so "fits on screen 1" is judged by text length only and
is unverified; the phone gate (P4) must confirm it. Checklist A-N: PASS on every page except where a defect is named.
Open items (F local contacts, I error report, K print, L Spanish) are known GAPs and not repeated.

## home
- No changed item appears on this page. Zone cost table (AE $1,252 / X $928 / VE $1,778 / A $944) is labelled single-family primary-home, existing policies, with counts. Screen-1 "three things" are answers with next steps.
- MINOR: none new.
Verdict: PASS

## louisiana
- MINOR: events table under "Which floods paid out the biggest totals here?" is ordered by total, then the catch-all row "Flooding (1978–1998)... $1.1 billion" sits last, bigger than Ida ($691.8 million), Isaac, Rita, Ike and Late winter storms above it. "Biggest totals" heading plus a bigger row at the bottom reads as a mis-sort. The "costliest" sentence (Katrina $13.3 billion) is still true. Check that should catch it: events table sorted by total, or catch-all labelled "not one flood" in the sort note.
- Change 1 OK: "Largest zones by priced policies here: Zone X $1,082, Zone AE $1,259" matches the zone table (127,267 and 108,782 priced). Zone A (5.3%) is under the 10% line, so no "too few" clause: correct.
- Change 3 OK: "Totals for 2025 and 2026 are not final while their claims stay open." Chart has 2025 and 2026.
- Change 4: wording, see Classes.
Verdict: PASS

## palm-beach-county-fl
- Change 1 OK: X $620 (38,310) and AE $1,228 (9,661) match the table; VE 4.7% and AO/AH under 10%, no clause needed. Only 2 of 7 priced zones named, which "Largest zones" covers.
- Change 3 OK: 2025 is the third costliest year ($6,857,416) and the note names 2025 and 2026.
- Change 4 OK in truth: "Flooding (1979–2000)... 625 | $1.6 million" is smaller than Frances ($11.3 million) so the "costliest" sentence holds.
- MINOR: 1970s decade row counts only 1978-79 (chart starts 1978); the row label does not say so.
Verdict: PASS

## new-york-county-ny
- Change 1 true: "Zone X $953 a year (... Zone AE, 41.8% of policy units, has too few to price)". Table agrees (AE 6,232 units = 41.8%; only X in the priced table with 159).
- MINOR: "policy units" and "too few to price" are not explained on screen 1. A Manhattan reader sees that the high-risk zone (41.8%) has no price but is not told why (the price table counts only single-family primary homes, so condo-heavy zones drop out). The page does carry the base in the same parenthesis, so not MAJOR. Also mixes two bases in one sentence (ranking by priced policies, share by policy units); both labelled.
- Change 3 OK (2025 and 2026 in chart). Change 4: catch-all $624,518 is below the costliest named row, so no "costliest" contradiction.
Verdict: PASS

## sonoma-county-ca
- **MAJOR** Events block: "The costliest flood FEMA named here was Pineapple Express Southern (1998): $3.5 million across 284 NFIP flood claims." The table directly under it ends with "Flooding (1978–1997): many floods: FEMA's records use this name for claims in several years | 3,742 | $67.3 million", 19 times the "costliest" row and the biggest figure in the table, and the row sits out of order after a $239,918 row. A hurried reader takes $67.3 million as the answer or distrusts the sentence. The change-4 wording says "many floods" in the label but nothing links it to the "costliest" sentence. Check that should have caught it (new rule): a "costliest" sentence must be compared to every row including catch-alls; either say "costliest single flood" and keep the catch-all visibly separate, or sort and flag it.
- Change 1 OK: AE $1,588 (651) and X $1,201 (348) match; A 2.2%, AO 1.4% under 10%.
- Change 3 OK. Change 2 not applicable (all decades listed; 1970s 187, shown).
Verdict: FAIL

## levy-county-fl
- Change 1 true: "Zone AE $2,357, Zone A $958 a year (... Zone VE, 21.5% of policy units, has too few to price)". Table: VE 200 units = 21.5%, not in the priced table (under 50). Zone X (8.6%, 51 priced, $753) is in the table but not named on screen 1; "Largest zones" covers it. Sentence is long (about 190 characters in this answer); fit on screen 1 not verified.
- Change 3 true and well scoped: "Totals for 2026 are not final" (no 2025 bar exists).
- Change 2 not applicable: all five decades listed; 1980s (77 claims) still shown, so the cut-off is below 77 and above 27 (see dixie).
- Change 4 not applicable (no catch-all row). No "Among the five costliest years" line here: correct, 2024, 2023 and 2016 all have named floods.
Verdict: PASS

## dixie-county-fl
- Change 1 true: "Zone AE $1,001 a year (... Zone A, 10.4% of policy units, has too few to price)". 59 units = 10.4%, not in priced table. OK.
- Change 2 true: 1980s = 3+1+1+7+11+3+1 = 27 claims; decade rows 458+89+80+262 plus 27 = 916 = headline total. OK.
- MINOR: "too few claims for a share" gives no threshold; Levy shows a 77-claim decade and Dixie hides 27, so the reader cannot tell the rule. State it (for example "under 50").
- Change 3: no note, correct under the rule (chart ends 2024). Note 2024 is the costliest year ($9,213,116) and Helene claims can stay open; the page says nothing. GAP only.
- MINOR: Source line says "Data effective 1980–2024" while Levy says "1982–2026": the range is the county's loss years, not an as-of date, and reads like one.
Verdict: PASS

## Classes
- Template (state and county): the catch-all "Flooding (years): many floods: ..." row is placed last and can outrank every row above it; any "costliest flood" sentence on a page where the catch-all total is larger is contradicted by its own table (seen: sonoma MAJOR; louisiana MINOR). Machine check: for the events table, if catch-all total > the "costliest" row total, the sentence must say so or the row must be separated.
- Template: the catch-all label has two colons and runs over 90 characters in a phone table's first cell: "Flooding (1978–1997): many floods: FEMA's records use this name for claims in several years". Likely wraps to 3-4 lines at 390 px; shorter: "Flooding, many floods (1978–1997)" with the explanation in the note under the table. MINOR.
- Template: screen-1 "Cost in my zone?" now carries up to three bases (priced policies, policy units, single-family primary-home median). "has too few to price" does not say too few of what; MINOR.
- Template: decade tables start with a partial decade (1970s = 1978-79) without saying so. MINOR.
