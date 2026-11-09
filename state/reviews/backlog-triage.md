1. FIXED | Closed round-12 items (2026-10-28, round 15) | Non-NFIP communities named on state pages: DONE (light round 13 checked Louisiana's 34 nam | Louisiana: "Not in the NFIP ( 34 communities here): Athens ..." names them
2. FIXED | Closed round-12 items (2026-10-28, round 15) | ZIP town labels: DONE; a place must cover 25%+ of the ZIP's land (77386 no longer "Houston | Montgomery ZIP table row "77386 | $958 | 2,992 | 3,333", no "Houston" label
3. FIXED | Closed round-12 items (2026-10-28, round 15) | Condo line: DONE in the averages card (light round 13 checked the shares). | "Condo owners: condo-unit policies are 2.5% of NFIP policy units here."
4. DECIDED | Closed round-9 items (2026-10-28, round 12) | "Years to full-risk at 18% a year" / premium-rise calculator: DROPPED by the owner (2026-1 | Backlog: "DROPPED by the owner (2026-10-28: 'no calc. way too risky')"
5. FIXED | Closed round-9 items (2026-10-28, round 12) | Cost by flood zone on home: DONE in code. extras_raw.py writes data/us/cost_hist_zone.json | Home: "What does it cost by flood zone?" Zone AE $1,252, X $928, VE $1,778
6. FIXED | Closed round-9 items (2026-10-28, round 12) | Private flood: DONE. Rule private_accept (12 CFR 339.3(c), eCFR excerpt) on every "Am I re | "A private flood policy can meet a lender's flood requirement ... (12 CFR §339.3(c))"
7. FIXED | Closed round-9 items (2026-10-28, round 12) | "Find your county" link on screen 1 of state pages: DONE (_jump in build_page.py). | Louisiana: "Find your parish in the table ↓"
8. DECIDED | Closed round-9 items (2026-10-28, round 12) | Page length: CLOSED. The owner rule is no caps on blocks; the answers (cost, required, quo | Backlog: "CLOSED. The owner rule is no caps on blocks"
9. FIXED | Closed round-9 items (2026-10-28, round 12) | County full-risk and mean figures: DONE earlier. Every county page carries the averages ca | Orange: "Average (mean) cost, single-family homes"; "Pay below full-risk 42.5%"
10. DECIDED | Closed round-9 items (2026-10-28, round 12) | Same paragraphs on every page: CLOSED. They are registry rule texts with their sources, by | Backlog: "CLOSED ... registry rule texts with their sources, by design"
11. DECIDED | Closed round-9 items (2026-10-28, round 12) | Per-parish take-up and the NOAA panel on state pages: CLOSED. Both card types were cut in  | Backlog: "CLOSED. Both card types were cut in the card review"
12. FIXED | Closed round-9 items (2026-10-28, round 12) | Search box with no match: DONE. The home and hub pages say no page matches and point to th | Home: "No page matches yet. Every county's typical cost is in its state page's county table"
13. FIXED | home (round 8) | No cost by flood zone on home, although every top result answers it second. | Home zone table: "Zone AE $1,252 / 961,977"
14. FEATURE | home (round 8) | Nothing names the SERP's figures ($899 NerdWallet, $888 Policygenius, $786 Insurify) or sa | Home "Why do sites quote different prices?" lists own measures only; $899/$888/$786 not named
15. STILL | home (round 8) | Private flood: when a lender must accept it, and whether it can be cheaper. | Home has only "Private flood insurance is not in this data"; no lender-must-accept rule (only on /nfip/, states)
16. STILL | home (round 8) | No territories (PR, USVI, Guam), and no line saying they are left out. | Home: "NFIP records · 50 states and DC · 272 counties"; no PR/USVI/Guam line
17. FIXED | home (round 8) | Home has no JSON-LD (`grep application/ld+json dist/index.html` finds 0), while the state  | Home has application/ld+json (stripper flagged it)
18. FIXED | louisiana (round 8) | No "find your parish" link on screen 1; the parish table starts at louisiana-12. | Louisiana: "Find your parish in the table ↓"
19. FEATURE | louisiana (round 8) | Insurify's Plaquemines $4,752 vs our $1,231 is not reconciled, and there is no parish mean | Plaquemines only a table row; no third-party figure reconciled
20. DECIDED | louisiana (round 8) | No "years to reach full risk at 18% a year" figure. | Backlog item 4: premium-rise projection dropped by owner
21. FIXED | louisiana (round 8) | Private flood. | Louisiana: "A private flood policy can meet a lender's flood requirement"
22. DECIDED | louisiana (round 8) | No NOAA storm-events panel at state level, though the county template has one. | Backlog item 11: NOAA state panel cut in card review
23. STILL | palm-beach-county-fl (round 8) | Private flood: whether a lender or Citizens accepts it, and how its price compares. | PBC has lender rule but nothing on Citizens accepting private flood (Citizens text is only the flood-required rule)
24. FEATURE | palm-beach-county-fl (round 8) | No row naming NerdWallet's $528 or MoneyGeek's $466; our "Typical premium only $507" sits  | PBC text has no NerdWallet/MoneyGeek names or figures
25. FEATURE | palm-beach-county-fl (round 8) | No ZIP-level below-full-risk share or full-risk median; news results answer "how much will | PBC ZIP table columns: "ZIP | Median / yr | Priced policies | Policy units"; no full-risk column
26. FEATURE | palm-beach-county-fl (round 8) | No cost by municipality. | PBC: no cost-by-municipality table (only CRS "Does my town get a community discount?")
27. FEATURE | palm-beach-county-fl (round 8) | No paid share by named storm. It would show whether a real hurricane flood claim here pays | PBC claims card has no paid share by named storm
28. FIXED | home (round 9) | No cost by flood zone on home. | Home zone table present (AE $1,252)
29. FEATURE | home (round 9) | No row naming the SERP's figures ($899 NerdWallet, $888 Policygenius, $786 Insurify) again | Home still does not name $899/$888/$786 against its rows
30. STILL | home (round 9) | Private flood: when a lender must accept it, and its price. | Home: only "Private flood insurance is not in this data"; no lender-accept line
31. STILL | home (round 9) | No line on territories (PR, USVI, Guam). | Home has no territories line
32. FIXED | home (round 9) | No JSON-LD on home. | Home has application/ld+json
33. FIXED | louisiana (round 9) | No "find your parish" link on screen 1. | Louisiana: "Find your parish in the table ↓"
34. FEATURE | louisiana (round 9) | No parish mean or full-risk column; Insurify's Plaquemines figure is not reconciled. | Parish table header: "Parish | Policy units | Median / yr | Below full-risk | Claims since 1978"; full-risk col added, n
35. DECIDED | louisiana (round 9) | No "years to reach full risk at 18% a year". | Backlog item 4: dropped by owner
36. FIXED | louisiana (round 9) | Private flood. | Louisiana private-flood lender rule present (12 CFR §339.3(c))
37. DECIDED | louisiana (round 9) | No NOAA storm-events panel at state level. | Backlog item 11: NOAA state panel cut
38. STILL | palm-beach-county-fl (round 9) | Private flood: whether a lender or Citizens accepts it, and its price. | PBC: lender rule present; no Citizens-acceptance line
39. FEATURE | palm-beach-county-fl (round 9) | No row naming NerdWallet's $528 or MoneyGeek's $466 against our $507 premium-only figure. | PBC has no NerdWallet/MoneyGeek comparison row
40. FEATURE | palm-beach-county-fl (round 9) | No ZIP-level below-full-risk share or full-risk median. | PBC ZIP table has no below-full-risk or full-risk median column
41. FEATURE | palm-beach-county-fl (round 9) | No cost by municipality. | PBC: no cost by municipality
42. FEATURE | palm-beach-county-fl (round 9) | No paid share by named storm. | PBC: no paid share by named storm
43. FEATURE | broward-county-fl (round 9) | No neighbor-county comparison on the claims card (Miami-Dade, Palm Beach). It is the one f | Broward "Bordering and other counties: Miami-Dade County · Palm Beach County" are links only; claims card has no neighbo
44. FEATURE | broward-county-fl (round 9) | No paid share by named storm. It would show that the April 2023 flood claims paid far more | Broward claims card has no storm-level paid share
45. STILL | broward-county-fl (round 9) | Private flood: whether a lender or Citizens accepts it, and its price. | Broward has Citizens flood-required rule and lender rule; no Citizens private-flood acceptance
46. FEATURE | broward-county-fl (round 9) | No cost by municipality, though the CRS table already lists the 32 communities. | Broward: no cost-by-municipality (CRS table only)
47. FEATURE | broward-county-fl (round 9) | No ZIP-level below-full-risk share or full-risk median. | Broward ZIP table has no full-risk share
48. FEATURE | home (round 10) | The SERP's #1–#3 (NerdWallet "$899/yr", Policygenius via Kiplinger "$888", Insurify "$786  | Home table does not name NerdWallet/Policygenius/Insurify figures
49. FIXED | home (round 10) | No cost by flood zone on home. Policygenius and Bankrate give zone figures. | Home: "What does it cost by flood zone?"
50. STILL | home (round 10) | Private flood: when a lender must accept it. | Home has no lender-must-accept-private-flood line
51. STILL | home (round 10) | No territories (PR, USVI, Guam). | Home has no territories line
52. FIXED | home (round 10) | No JSON-LD on home. | Home has application/ld+json
53. FEATURE | louisiana (round 10) | Insurify's "Plaquemines Parish $4,752" (a search result) is not reconciled with our Plaque | No Insurify/Plaquemines reconciliation on Louisiana page
54. DECIDED | louisiana (round 10) | No "years to reach full risk at 18% a year" for the 56.6% below full risk. | Backlog item 4: dropped by owner
55. FIXED | louisiana (round 10) | No "find your parish" jump link on screen 1. The parish table is our information gain over | Louisiana: "Find your parish in the table ↓"
56. FIXED | louisiana (round 10) | Private flood. | Louisiana private-flood lender rule present
57. DECIDED | louisiana (round 10) | No state-level NOAA panel. | Backlog item 11: NOAA state panel cut
58. FEATURE | palm-beach-county-fl (round 10) | NerdWallet $528 / $488, MoneyGeek $466 and Insurify $709 (search results) are not named ag | PBC text has no NerdWallet/MoneyGeek/Insurify figures
59. FEATURE | palm-beach-county-fl (round 10) | No ZIP-level full-risk gap. The Miami Herald's "33469 +342%" story is what a Jupiter or Te | PBC ZIP table has no full-risk gap column
60. STILL | palm-beach-county-fl (round 10) | Private flood and Citizens acceptance of private flood. | PBC: lender rule present; no Citizens-acceptance line
61. FEATURE | palm-beach-county-fl (round 10) | No cost by municipality. | PBC: no cost by municipality
62. FEATURE | palm-beach-county-fl (round 10) | No paid share by named storm. | PBC: no paid share by named storm
63. FEATURE | orange-county-ca (round 10) | Insurify lists Orange County at $795 and $892 (two of its pages disagree); our $1,083 is n | Orange text has no Insurify $795/$892 reconciliation
64. FEATURE | orange-county-ca (round 10) | The post-wildfire waiting-period exception (44 CFR 61.11(c)) and debris-flow risk after fi | Orange: no wildfire/debris-flow or 61.11(c) text (grep wildfire|debris: none)
65. FIXED | orange-county-ca (round 10) | OC Public Works' "25% discount for unincorporated homeowners" press release is matched by  | Orange CRS table: "Orange County 25% class 5 ... No CRS discount (26): Aliso Viejo; Brea ..."
66. FIXED | orange-county-ca (round 10) | Private flood. | Orange has private-flood lender rule (12 CFR §339.3(c))
67. FEATURE | orange-county-ca (round 10) | No cost by city. The ZIP table half-covers it. | Orange: no cost-by-city table (ZIP table only)
68. FEATURE | atlantic-county-nj (round 10) | Insurify's "Atlantic County $1,022" and Clovered's "$1,899 under Risk Rating 2.0" (search  | Atlantic text has no Insurify/Clovered figures
69. FEATURE | atlantic-county-nj (round 10) | No Risk Rating 2.0 transition line. The Press of Atlantic City reported that most of 27,00 | Atlantic: no Risk Rating 2.0 transition-pace text (grep: none)
70. FEATURE | atlantic-county-nj (round 10) | No cost by municipality. The CRS table lists the towns, and Brigantine, Margate, Ventnor a | Atlantic: no cost by municipality; CRS table lists "Brigantine", "Margate City" only
71. FIXED | atlantic-county-nj (round 10) | Private flood. | Atlantic private-flood lender rule present
72. FEATURE | atlantic-county-nj (round 10) | No elevation-certificate or "elevated vs not" next step tied to the 2,478 elevated policie | Atlantic: no elevated-vs-not rows (grep "elevated": none)
73. FIXED | site review (2026-10-28, browser test) | ZIP town labels come from GeoNames and can name the metro, not the postal town: 77386 show | Montgomery ZIP row "77386 | $958" carries no "Houston"; 25% land rule noted done in item 2
74. FIXED | site review (2026-10-28, browser test) | Home search with no match showed an empty table; patch ready (no-match message pointing to | Home: "No page matches yet. Every county's typical cost is in its state page's county table"
75. FEATURE | home (round 11) | NerdWallet, Policygenius and Insurify headline figures are not named in "Why do sites quot | Home table does not name NerdWallet/Policygenius/Insurify
76. FIXED | home (round 11) | No cost by flood zone nationally. | Home zone table present
77. STILL | home (round 11) | No private-flood acceptance rule. | Home: no private-flood acceptance rule
78. STILL | home (round 11) | No territories (PR, USVI). | Home: no territories line
79. FIXED | home (round 11) | No JSON-LD. | Home has application/ld+json
80. FIXED | louisiana (round 11) | The "Not in the NFIP (34 communities here)" line does not name them (Vienna, Creola, Shong | Louisiana: "Not in the NFIP ( 34 communities here): Athens ..."
81. DECIDED | louisiana (round 11) | No "years to reach full risk at 18% a year". | Backlog item 4: dropped by owner
82. FIXED | louisiana (round 11) | No parish jump link on screen 1. | Louisiana: "Find your parish in the table ↓"
83. FEATURE | louisiana (round 11) | Insurify's Plaquemines figure is not reconciled with ours. | No Insurify/Plaquemines reconciliation
84. FIXED | louisiana (round 11) | Private flood. | Louisiana private-flood lender rule present
85. FEATURE | palm-beach-county-fl (round 11) | NerdWallet, MoneyGeek and Insurify county figures are not reconciled with ours. | PBC has no third-party county figures
86. FEATURE | palm-beach-county-fl (round 11) | No ZIP-level full-risk gap. | PBC ZIP table has no full-risk gap column
87. STILL | palm-beach-county-fl (round 11) | Private flood and Citizens' acceptance of it. | PBC: lender rule present; no Citizens-acceptance line
88. FEATURE | palm-beach-county-fl (round 11) | No cost by municipality. | PBC: no cost by municipality
89. FIXED | palm-beach-county-fl (round 11) | The community names in the "Not in NFIP" line do not apply here (all 40 participate); noth | PBC page has no "Not in the NFIP" line (all participate); nothing missing, as the item says
90. FEATURE | orange-county-ca (round 11) | Insurify's $795 / $892 are not reconciled with ours. | Orange: no Insurify figures
91. FEATURE | orange-county-ca (round 11) | Post-wildfire waiting-period exception and debris-flow risk. | Orange: no wildfire/debris-flow text
92. FIXED | orange-county-ca (round 11) | No line on why cities without CRS get no discount. | Orange: "No CRS discount (26): Aliso Viejo; Brea ..." plus "a lower CRS class goes with a bigger discount"
93. FIXED | orange-county-ca (round 11) | Private flood. | Orange private-flood lender rule present
94. FEATURE | orange-county-ca (round 11) | No cost by city. | Orange: no cost by city
95. FEATURE | atlantic-county-nj (round 11) | Insurify $1,022 and Clovered $1,899 are not reconciled with ours. | Atlantic: no Insurify/Clovered figures
96. FEATURE | atlantic-county-nj (round 11) | No Risk Rating 2.0 transition pace. | Atlantic: no Risk Rating 2.0 pace
97. FEATURE | atlantic-county-nj (round 11) | No cost by municipality. | Atlantic: no cost by municipality
98. FIXED | atlantic-county-nj (round 11) | Private flood. | Atlantic private-flood lender rule present
99. FEATURE | atlantic-county-nj (round 11) | No Elevation Certificate next step tied to the elevated/not-elevated rows. | Atlantic: no elevated-vs-not rows or EC next step
100. FEATURE | montgomery-county-tx (round 11) | MoneyGeek "$568 average" and Insurify "$1,040" (search results today) are not reconciled w | Montgomery: no MoneyGeek/Insurify figures
101. FIXED | montgomery-county-tx (round 11) | No 2018 Montgomery County map-change note (Community Impact covers the map dates). | Montgomery: "FEMA's current flood map for unincorporated Montgomery County took effect August 18, 2014"
102. FEATURE | montgomery-county-tx (round 11) | No cost by city or The Woodlands. | Montgomery: no city/Woodlands cost line (title says "(The Woodlands)" only)
103. FIXED | montgomery-county-tx (round 11) | Private flood. | Montgomery private-flood lender rule present
104. FEATURE | montgomery-county-tx (round 11) | No Spring/Lake Conroe dam-release context for 2017 (Harvey) claims. | Montgomery: no dam-release/Harvey context (grep: none)
105. FIXED | oklahoma (round 11) | "Not in the NFIP (122 communities here)" names none (Greenfield, Osage, Springer, unincorp | Oklahoma: "Not in the NFIP ( 122 communities here): Achille ; Addington ;"
106. FEATURE | oklahoma (round 11) | Kin's "NFIP median $793" and MoneyGeek's "$995 average" are not reconciled with our $1,047 | Oklahoma: no Kin/MoneyGeek figures
107. FEATURE | oklahoma (round 11) | No Tulsa city figure. Tulsa, CRS class 1 with a 45% discount, is the state's best-known fl | Oklahoma has "Tulsa County" row; no Tulsa city figure
108. FIXED | oklahoma (round 11) | Private flood. | Oklahoma private-flood lender rule present
109. FEATURE | oklahoma (round 11) | No Oklahoma Insurance Department "Get Ready" next step. | Oklahoma names "Oklahoma Insurance Department"; no "Get Ready" next step
110. DECIDED | home (round 12) | (SEO, "flood insurance cost"). | Item is only a "(SEO ...)" context label, no defect
111. FIXED | home (round 12) | #1-#3 give cost by flood zone nationally ("$560 in B/C/X, $2,795 in D"-style tables). The  | Home: "What does it cost by flood zone?" national table
112. DECIDED | home (round 12) | No national private-flood figure. The page says so ("Private flood insurance is not in thi | Backlog: "this is allowed and is not a defect"
113. FEATURE | louisiana (round 12) | (SEO "flood insurance cost Louisiana": MoneyGeek $750, Insurify $1,470 "NFIP median, singl | No Insurify $1,470 reconciliation on Louisiana page (item is a label plus figure gap)
114. FEATURE | louisiana (round 12) | Insurify's Plaquemines $4,752 against our $1,231 (carried). | No Insurify/Plaquemines reconciliation
115. FIXED | louisiana (round 12) | The NFIP-not-sold line counts 34 communities but does not name them (carried). | Louisiana: "Not in the NFIP ( 34 communities here): Athens ..."
116. FIXED | louisiana (round 12) | No parish jump on screen 1 (carried). | Louisiana: "Find your parish in the table ↓"
117. DECIDED | louisiana (round 12) | No years-to-full-risk at 18% a year (carried). | Backlog item 4: dropped by owner
118. STILL | louisiana (round 12) | No NRI flood-risk card on the state page; county pages have one. | Louisiana h2s have no flood-risk card; PBC has "How much flood risk is here?"
119. DECIDED | orange-county-ca (round 12) | (SEO "flood insurance cost orange county CA": Insurify CA guide with an OC row $795 / olde | Item is only a "(SEO ...)" context label
120. STILL | orange-county-ca (round 12) | County Public Works says unincorporated homeowners get 25% CRS. We show that (Orange Count | Orange: CRS lists "Orange County 25%" and 26 no-discount cities; does not say which cities are unincorporated
121. FEATURE | orange-county-ca (round 12) | No cost by city; the ZIP table covers it partly. | Orange: no cost by city
122. DECIDED | montgomery-county-tx (round 12) | (SEO "flood insurance cost montgomery county TX": MoneyGeek TX with a Montgomery row of $5 | Item is only a "(SEO ...)" context label
123. FEATURE | montgomery-county-tx (round 12) | No The Woodlands figure (three Woodlands ZIPs exist in the table, but no combined line). | Montgomery: no Woodlands combined figure
124. FIXED | montgomery-county-tx (round 12) | No 2018/2014 map-change note. | Montgomery: "unincorporated Montgomery County took effect August 18, 2014"
125. DECIDED | oklahoma (round 12) | (SEO "flood insurance cost Oklahoma": OKCFox/QuoteWizard "ranks 23rd", MoneyGeek about $99 | Item is only a "(SEO ...)" context label
126. FIXED | oklahoma (round 12) | The 122 non-NFIP communities are counted, not named (carried). | Oklahoma: "Not in the NFIP ( 122 communities here): Achille ; Addington ;"
127. FEATURE | oklahoma (round 12) | No Tulsa city figure (carried). | Oklahoma: "Tulsa County" row only, no Tulsa city figure
128. FEATURE | oklahoma (round 12) | No OID "Get Ready" / FloodSmart OneStep next step. | Oklahoma: no OID "Get Ready"/OneStep step
129. DECIDED | nevada (round 12) | (SEO "flood insurance cost Nevada": MoneyGeek $799 with county rows, Nye $468 and Lander $ | Item is only a "(SEO ...)" context label
130. FIXED | nevada (round 12) | No Las Vegas / Clark County Regional Flood Control District context; the AO zone is 48% of | Nevada codes line: "AO and AH are high-risk with shallow flooding"; Las Vegas/Flood Control context not added (feature p
131. FIXED | nevada (round 12) | The state's division-of-insurance note ("available in every county except Esmeralda") is n | Nevada: "Not in the NFIP ( 1 community here): Washoe Tribe of Nevada and California"
132. DECIDED | horry-county-sc (round 12) | (SEO "flood insurance cost horry county SC": WBTW, WMBF, MoneyGeek SC with a Horry row of  | Item is only a "(SEO ...)" context label
133. FEATURE | horry-county-sc (round 12) | 1-800 Insurance's "$2,000–$6,000 for most Little River properties" (likely condo/VE) has n | Horry: no 1-800 Insurance/Little River condo-VE figure
134. FIXED | horry-county-sc (round 12) | No new-map (2003 FIRM, pending update) note; WBTW and WMBF both lead on it. | Horry: "FEMA's current flood map for unincorporated Horry County took effect"; preliminary-map line present
135. FEATURE | horry-county-sc (round 12) | No condo/RCBAP cost line at all. | Horry: only "Condo owners: condo-unit policies are ..% of units"; no condo/RCBAP cost line
136. FIXED | light round 13 MINORs (2026-10-28; fix in the next template batch) | Quote checker: clearing the amount leaves the old zone line (zq must clear when the amount | zq(): "if(!s||!s.value||!(v>0)){o.textContent='';return;}"
137. STILL | light round 13 MINORs (2026-10-28; fix in the next template batch) | Zone dropdown lists thin zones (Louisiana A12, 53 policies); consider the zone card's own  | Louisiana zone table still lists "Zone A12 $1,656 53" and A01/A15/AHB/V15; dropdown has same options
138. FIXED | light round 13 MINORs (2026-10-28; fix in the next template batch) | Condo note prints "0.0%" for condo buildings; say "none" or drop the clause at 0. | Scan of 326 state/county pages: 0 contain a condo clause with 0.0%
139. STILL | home (round 16) | No buying step anywhere on home: no NFIP phone (877) 336-2627, no FloodSmart link, no 30-d | Home has no (877) 336-2627 or FloodSmart link (they are on /nfip/ and /renters/)
140. FEATURE | home (round 16) | No Spanish (L, OPEN); no error-report route (I, OPEN); no print stylesheet (K, OPEN). | Home: no Spanish, print stylesheet, error-report route, contacts list
141. DECIDED | home (round 16) | NerdWallet/Bankrate show a "cheapest/most expensive" narrative and private-market context; | Backlog: "That is acceptable per the brief. Noted, not counted."
142. STILL | louisiana (round 16) | The 64-row parish table has no search or filter; only the county page has a lookup (G: lon | Louisiana parish table has no search input (inputs: address, dates, checkboxes only); "Back to top ↑" exists
143. FEATURE | louisiana (round 16) | Data already held but not shown: residential take-up (penetration 22.0% overall, 73.1% in  | Louisiana: no penetration/take-up or outside-high-risk share (grep: none)
144. FEATURE | louisiana (round 16) | No Spanish (L, OPEN). No state insurance department or floodplain office contact (F, OPEN) | Louisiana: only "NAIC's directory of state insurance departments"; no Spanish, no floodplain office
145. FEATURE | louisiana (round 16) | MoneyGeek has a parish table with averages; ours is better (medians, n, claims). We have n | Louisiana: no private-insurer buying line
146. FIXED | palm-beach-county-fl (round 16) | City-level costs (NerdWallet lists West Palm Beach $349): our ZIP lookup covers this, but  | PBC ZIP rows carry towns: "33418 Palm Beach Gardens", "33411 Royal Palm Beach"
147. FEATURE | palm-beach-county-fl (round 16) | The Miami Herald/Sun-Sentinel rank with "rates will double/triple near the coast" (Risk Ra | PBC: no ZIP-level below-full-risk
148. FEATURE | palm-beach-county-fl (round 16) | Take-up held but not shown (penetration 13.0% overall, 43.4% in high-risk zones). No Spani | PBC: no take-up figure; no Spanish/floodplain office
149. FEATURE | maine (round 16) | "Only 1% of Maine households have flood insurance" (WABI, ranking #6) answers "do my neigh | Maine: no take-up figure (grep: none)
150. FEATURE | maine (round 16) | Press Herald gives county averages; ours exist (PASS). The FEMA Maine state profile PDF ha | Maine: no FEMA state-profile PDF link
151. FEATURE | maine (round 16) | No back-to-top; no state floodplain office (Maine Floodplain Management Program) contact ( | Maine: "Back to top ↑" exists; no Maine Floodplain Management Program contact
152. STILL | nebraska (round 16) | The 78-row county table has no search (G). No back-to-top. | Nebraska has no <input>, so the county table has no search; "Back to top ↑" exists
153. FEATURE | nebraska (round 16) | StateCalc gives "median of the 1,000 most-recent real NFIP policies" ($744), a buyer-orien | Nebraska "Buying?" line only; figure placement is a design wish, not a defect
154. FEATURE | nebraska (round 16) | Take-up (0.7% overall, 15.3% in high-risk zones) and claims outside high-risk zones (21.3% | Nebraska: no take-up or outside-high-risk share
155. FIXED | light round 21 MINORs (deadline planner; next template batch) | Heading says "claim deadline" but computes only the NFIP proof-of-loss date. | Heading now: "Work out the proof-of-loss deadline for an NFIP (National Flood Insurance Program) policy."
156. FIXED | light round 21 MINORs (deadline planner; next template batch) | "Your NFIP proof of loss" also reads to uninsured or private-policy readers; say "An NFIP  | JS: "An NFIP proof of loss is due by ..."
157. FIXED | light round 21 MINORs (deadline planner; next template batch) | Past-date sentence: add that the insurer may have extended the date. | JS: "The 60-day NFIP proof-of-loss date was ... it may have extended the date."
158. FIXED | light round 21 MINORs (deadline planner; next template batch) | Spell out "NFIP" once inside the tool. | "NFIP (National Flood Insurance Program)" spelled out in the tool heading
159. STILL | site-wide decisions (2026-10-29, after 3 light rounds on the home source line) | How the home "Three things to know first" card cites its rules: decide ONE format for the  | State pages: "Source: floodsmart.gov, law.cornell.edu (official pages, checked ...)"; home has no such host list
160. STILL | site-wide decisions (2026-10-29, after 3 light rounds on the home source line) | Define "Citizens" (Florida's state-backed insurer) where the Florida rule appears; split i | Home says "Citizens homes with wind cover"; PBC spells out "Citizens Property Insurance"; home not defined
161. FEATURE | home (round 69) | AE and VE screen 1 shows the all-A-zones / all-V-zones median, correctly labelled right un | Home shows all-A/V median; exact-zone data due; no contacts/error route/print/Spanish
162. STILL | new-york-county-ny (round 82) | Query 'flood insurance cost new york county NY' is a Manhattan reader; the H1 does not say | New York County H1: "New York County, NY flood zones and flood insurance: $1,021/yr median"; no "Manhattan"
163. STILL | new-york-county-ny (round 83) | Manhattan not named in H1 (unchanged). | Same H1; Manhattan not named
164. STILL | home (round 86) | No "am I required to buy" line on /nfip/. | /nfip/ has no "Am I required to buy" line (sections: how it works, where policies are)
165. STILL | home (round 86) | r88 (11-07) renters: drop `private_accept` (lender rule, off-topic for renters); add rule( | Renters: private_accept gone and actual-cash-value line present; no "required? only a lender or landlord can say" gap li
166. FIXED | screen-1 quick answers (round 94) | Risk line: say "FEMA's county rating" (a bare "Very High" can differ from the loss percent | PBC: "FEMA's county rating: Relatively High coastal, Relatively High inland (river) flood risk"
167. FIXED | screen-1 quick answers (round 94) | Zone cost line: say "Most common zones here" so readers in other zones look in the table. | PBC: "Largest zones by priced policies here: Zone X"
168. FIXED | round 95 MINORs | Hero tile "Still pay less than FEMA's full-risk price": add its base (single-family primar | PBC tile: "Single-family primary-home policies with a premium under FEMA's full-risk premium"
169. FIXED | round 95 MINORs | Zone line: say when a zone with many units (NY County AE) is left out for too few priced p | NY County: "Zones with fewer than ... (... of policy units, has too few to price)"
170. FIXED | round 95 MINORs | "No new map" line: pair with "preliminary maps may exist" so it never reads as nothing com | PBC: "lists no new flood map taking effect ...; that does not cover maps still preliminary (below)"
171. STILL | round 95 MINORs | State picker: say it lists only places with their own page. | Home search: placeholder "Type your state or county…"; no "only places with their own page" note
172. STILL | round 95 MINORs | Renters: not_covered says "home policy"; scope it to the contents policy. | Renters: "The standard NFIP Dwelling Policy does not pay for a hotel or other living costs"; not scoped to contents poli
173. FIXED | round 95 MINORs | LOMA "no fee" sits beside Letter of Map Change, which can cost: scope. | Levy: "FEMA charges no review or processing fee for a Letter of Map Amendment request (44 CFR §72.5)."
174. STILL | round 95 MINORs | AE zone: Elevation Certificate who/where (needs a raw FEMA source; FEMA.gov refuses the la | Zone AE page: no Elevation Certificate who/where (only generic "an Elevation Certificate" in ways to pay less)
175. STILL | round 95 MINORs | Insurance regulators: 12 states fell back to NAIC (403 from the laptop); retry from the US | Louisiana, Atlantic: "NAIC's directory of state insurance departments" fallback still shown
176. FIXED | round 97 MINORs (11-08) | Tile "paying under FEMA's full-risk price": say "premium" (premium before fees vs headline | PBC tile: "a premium under FEMA's full-risk premium" ("premium" now used)
177. STILL | round 97 MINORs (11-08) | not_covered rule: FEMA's form name is "Dwelling Form" (44 CFR 61 App. A(1)); condo unit ow | Renters says "standard NFIP Dwelling Policy" not "Dwelling Form"; no condo-unit form gap line
178. STILL | round 97 MINORs (11-08) | Condo note "(FEMA's condominium coverage code)" vague; map note "NFIP communities filed un | "(FEMA's condominium coverage code)" and "NFIP communities filed under this county" still on PBC
179. STILL | levy-county-fl (round 113) | The LOMA counts have no time span (all rulings since when?). The oldest/newest panel dates | Levy: "FEMA's map service lists 44 rulings for owners here ..."; no since-year
180. STILL | levy-county-fl (round 113) | No plain-words line that the outcomes of past rulings do not predict the reader's own resu | Levy: only "These are rulings for owners who applied, not a share of all homes"; no "past rulings do not predict yours"
181. STILL | sonoma-county-ca (round 113) | "364 took the building or some or all of the lot out" out of 483 can read as a high odds o | Sonoma: "These are rulings for owners who applied"; self-selection not said
182. STILL | sonoma-county-ca (round 113) | Same missing time span for the LOMA counts. | Sonoma LOMA counts have no time span

SUMMARY: DECIDED 20, FEATURE 67, FIXED 60, STILL 35, total 182

STILL items by template part (fix one, close several):
- Home body: buying step (877/FloodSmart), private-flood accept rule, territories line, state picker note, host list, Citizens definition: 15, 16, 30, 31, 50, 51, 77, 78, 139, 159, 160, 171
- Private-flood rule on state/county: Citizens acceptance line (Florida pages): 23, 38, 45, 60, 87
- Long county/parish tables: search box: 142, 152
- Zone table + quote-checker zone dropdown: floor for thin zones: 137
- Zone AE page: Elevation Certificate who/where: 174
- Renters page and /nfip/: scope not-covered text, "Dwelling Form", gap line on required, /nfip/ required-to-buy line: 164, 165, 172, 177
- Footnote jargon: condominium coverage code, "NFIP communities filed under this county": 178
- Insurance regulator link (NAIC fallback in 12 states): 175
- LOMA / map-change card: since-year, past rulings do not predict yours, self-selected applicants: 179, 180, 181, 182
- Title/H1 of New York County: add Manhattan: 162, 163
- Louisiana state page: NRI flood-risk card: 118
- Orange CRS card: which cities are unincorporated: 120
