# Hater round 15 (light check, page text only)

## home
Items 1-2 not present on home (no nav.toc, no "Already flooded?" text); no duplicate ids. Nothing to judge.
Verdict: PASS

## louisiana
1. TOC: 18 links, every href matches an existing id, link text equals card heading, order equals page order, no duplicate ids. OK.
2. Proof-of-loss text: "send a signed proof of loss within 60 days of the flood (44 CFR 61, App. A(1), Art. VII)". Correct (SFIP Art. VII) and clear.
3. Quote checker: zone line cleared by zq() when amount empty/<=0 (input handler calls zq()). Dropdown = 25 zones, all in Z with 53+ priced policies. OK.
4. Condo: "Condo owners: condo-unit policies are 1.1% of NFIP policy units here. The single-family figures above leave both out; ..." 
- MINOR: "leave both out" has no second item when the building clause is omitted (building share is 0/absent). Source: tools/build_page.py lines 482-483 keep "both" unconditionally.
- MINOR: dropdown shows obscure legacy zones (A01-A15, V15, AHB, A99) with no gloss; reader may not know theirs.
Verdict: PASS

## palm-beach-county-fl
1. TOC: 19 links, hrefs all resolve, text equals headings, order matches, no duplicate ids. OK.
2. Proof-of-loss sentence correct and clear.
3. Zone dropdown: X, AE, AO, AH, C, VE, B; all 116+ priced policies. Clearing amount clears zone line. OK.
4. Condo: "condo-unit policies are 6.1% ... leave both out"
- MINOR: same dangling "both" (building clause omitted).
- MINOR: zones B and C are old labels for X-type areas, unexplained.
Verdict: PASS

## broward-county-fl
1. TOC: 19 links, hrefs all resolve, text equals headings, order matches, no duplicate ids. OK.
2. Proof-of-loss sentence correct and clear.
3. Zone dropdown: AE, X, AH, AHB (564+ each). Clearing amount clears zone line. OK.
4. Condo: "condo-unit policies are 3.4% ... leave both out"
- MINOR: same dangling "both".
Verdict: PASS
