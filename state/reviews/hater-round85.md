# Round 85 (LIGHT, text only)

Method: built HTML text only, no screenshots, no web search. Changed items only: (1) new page /nfip/; (2) home "Buying?" link to /nfip/. Checklist C, D, E, N judged; A, B, F-M unchanged from round 83/84 (PASS) except where noted.

Recompute: data/states/built.json (51 rows) sums: units 4,529,364; claims 2,680,429; paid $88,422,296,888 = page lead sentence exactly. Top-10 units and shares (units / 4,529,364) recomputed: FL 1,777,001 39.2%, TX 569,743 12.6%, LA 401,925 8.9%, NJ 195,686 4.3%, SC 190,918 4.2%, CA 172,348 3.8%, NY 166,378 3.7%, NC 130,556 2.9%, VA 89,994 2.0%, GA 70,395 1.6%: all equal the table, sorted correctly. $1,066 equals data/us/cost_hist.json median (verified round 83). Rule texts equal rules_registry (nfip_not_sold, limits, wait_30, how_to_buy, nfip_lapse, private_accept).

## home

Buying? line: "...typically pay $1,011 (187,522 policies). Why sites differ. The NFIP in numbers." Link href="/nfip/" resolves to dist/nfip/index.html (exists, in sitemap). Link text names its target; no screen-1 clutter beyond one link.

- **MINOR** Home tile says "Insured units in force" while /nfip/ title says "4.5 million policies" (see nfip below); same number, two words.

Checklist C/D/E/N: PASS.

Verdict: PASS

## nfip (judged inside "home")

Distinct from home: yes. It is a short national summary (about 13 KB), with its own title, a top-10 table the home page lacks, and a national claims total in one sentence; the home page is the long page with the full state table, zone tables and answers. Shared sentences (median, limits, 30 days, how to buy) come from the same rule() text, so repeated facts are identical, not conflicting. Not a near-duplicate and not a name-swap page.

- **MAJOR** Lead sentence: "Since 1978 FEMA's records list 2,680,429 NFIP claims, with $88,422,296,888 paid on them." Reads as if all 2.68M claims were paid ($33,000 average). The 2,680,429 counts every claim record, paid or not (home states this: "every claim record, paid or not"; a rule in the registry notes many close without payment). The nfip page drops "paid or not"; the footnote only says "Claims paid: building plus contents payments" and does not say the count includes unpaid ones. A reader dividing the two numbers gets a wrong average. Fix: "...2,680,429 claim records (paid or not), with $88,422,296,888 paid in total" and add the home's footnote line. Checklist C (claims filed vs paid) fails.
- **MINOR** Title "4.5 million policies" vs body "4,529,364 policy units" and the hero "Policy units in force". Units are not policies (one record/policy can cover several units; home says 3,446,101 policy records). Also the median is over 2,320,412 single-family policies, not units. The body names the bases correctly ("every NFIP policy unit, including condos, rentals and businesses"; "single-family primary-home"); only the title blurs it. Use "policy units" in the title.
- **MINOR** Bases side by side: units today (4.5M, as of Aug 31, 2026) vs claims since 1978 (cumulative). The caption gives the as-of date and "since 1978" in the tile label, so not misleading.
- **MINOR** "dollars as paid" in the tile and "not adjusted for inflation" in the caption: both present; dollars are nominal and say so (C passes).
- **MINOR** "NFIP covers up to $250,000 on the building and $100,000 on contents" sits next to a count that includes businesses and condos, with no scope (residential building; commercial limits differ). Shared rule text used on other passed pages, so a class fix in the rule's source, not this page.
- **GAP** No "am I required to buy it" line and no flood-zone link up top beyond a footer sentence; the home page answers it. For a national-numbers page that is acceptable.
- **GAP** Heading style: H2 "How the NFIP works", "Where the policies are", "What these numbers cannot tell you" are labels, not reader questions (checklist E). Heading order H1 then H2 is correct.

Checks passed: "What these numbers cannot tell you" prints premium, private prices, why prices change, and says the median is not a quote. Source line and OpenFEMA non-endorsement present. Canonical correct. Description matches body. No verdict or advice words.

Checklist: A PASS (not an answer page; links onward), B n/a, C FAIL on the claims line above, D PASS except the title word, E PASS, F PASS (phone, FloodSmart), I PASS, J PASS (links to states, zones, ZIP), M PASS (as-of date shown), N PASS.

Verdict: FAIL

## Classes

- Template home: the new "/nfip/" link adds no defect.
- New national page: claim counts must say "paid or not" wherever they sit near a dollars-paid figure (home does; /nfip/ did not). Candidate machine check: any page showing the claims total and the paid total must contain "paid or not".
- Rule text without scope (limits, $250,000): residential building only is not stated; same on every page that prints it.

## Previous items

Round 83: no BLOCKER or MAJOR open (all PASS). No carry-over.
