# Round 103: light review of 3 flagged queue counties

Method: read built HTML text and agg/data/extras JSON. Recomputed per page: median/p25/p75/p90, share below full-risk, yearly claim sums, decade sums, paid share, unpaid-reason sums, zone shares, SFHA share, housing-aid total and per-registration, and the "% above state/U.S. median" lines. All matched the page. The flag driver (claims per current policy: Sonoma 7,403 claims / 2,368 units = 312.6 per 100; Levy 141.2; Dixie 161.6) is never printed as a ratio on any page. Each page prints the claim count with "since 1978/1982/1980" next to it and the policy count separately, so the high ratio is not presented as a risk rate.

## sonoma-county-ca
- MINOR: Claims lead "Floods in Sonoma County have led to 7,403 NFIP flood claims and $131.7 million in payouts since 1978" counts all 7,403 records, including 100 "Claim deleted in error" and 87 "Not an actual flood" (shown in the unpaid-reasons table). The decade note says the shares include entered-in-error records, but the lead calls them "flood claims". Overstates by about 2.5% at most.
- MINOR: "The costliest flood FEMA named here was Pineapple Express Southern (1998): $3.5 million", yet the table directly below lists "Flooding (1978-1997) ... 3,742 ... $67.3 million". The catch-all row is larger than the "costliest", and the lead does not say the catch-all is excluded from "costliest".
- MINOR: "No CRS discount ( 9 ): Cloverdale; Cotati; ..." The 9 is a count of towns, but the table column is "CRS class" where Petaluma is class 6. A reader can take "(9)" as class 9 = no discount. Levy's page shows class 9 earning 5%, so the sites disagree on what 9 means.
- MINOR: "Bordering counties: ... Contra Costa County". Contra Costa does not share a land border with Sonoma (San Pablo Bay water only at most). Unverified, check the adjacency source.
Verdict: PASS

## levy-county-fl
- MINOR: "Cost in my zone ... From about $753 a year (Zone X) to $2,357 (Zone AE)". Zone VE is 21.5% of Levy's policy units (200) but has no row because of the 50-policy floor. The omission rule is printed below the table, but a Yankeetown or Cedar Key VE reader finds no price and the "from ... to" range reads as complete.
- MINOR: "Disasters for COVID, fire, winter storms or tornadoes alone are left out", but data.json housing includes disaster 4486 (COVID-19 pandemic, 1 registration, $1,185) in the $14.8 million and $1,572 per registration. Effect is negligible, the sentence is false.
- MINOR: "No CRS discount ( 6 ): Bronson; ..." The 6 is a count, but Yankeetown's table row is CRS class 6 with a 20% discount. Reads as class 6 = no discount, which contradicts the table.
Verdict: PASS

## dixie-county-fl
- MINOR: The decade table shows 1990s 458, 2000s 89, 2010s 80, 2020s 262 = 889, but the page says 916 claims. extras.json has a 1980s row (27 claims, 66.7% paid) that is dropped without a note, so the rows do not add up to the stated total. Not misleading on payout share, but unlabelled.
- MINOR: "Totals for the latest two years are not final while their claims stay open." Dixie's claim data ends in 2024 (year_max 2024, "Data effective 1980-2024"), retrieved November 2026. The "latest two years" are 2023 and 2024, so the warning attaches to Idalia and Helene totals that are two years old. Harmless, but the page does not say there are no 2025-26 claims.
- MINOR: Same COVID wording as Levy: housing includes disaster 4486 (1 registration, $0), while the page says COVID is left out. No dollar effect.
- MINOR: "By ZIP it ranges from $654 (32628) to $1,011 (32680)". Only 2 of 10 ZIPs have enough priced policies for a median (91 and 48 priced). "Ranges" over two ZIPs is thin, but the ZIP table shows both.
Verdict: PASS
