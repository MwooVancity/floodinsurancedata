# Hater round 50: narrow recheck of the eight round-49 MAJOR rules

Checked: current text in tools/rules_registry.py, grep of dist/flood-insurance pages, and FEMA's NfipClaims field dictionary for nonPaymentReasonBuilding (read 2026-11-02 via the API). Source quotes are the ones round 49 read raw.

## home
Verdict: PASS
None of the eight rules print on this page (round 49 checked the ten rules; not re-grepped this round).

## louisiana
Verdict: FAIL
- MAJOR cap: the comparator "for other property" is not in any quoted source. The quote (42 U.S.C. 4015(e)(4)) names "properties described under paragraph (3)", and round 49 proposed "primary homes", which is also not quoted. Fix: quote paragraph (3) and name its group, cite (e)(4). The stop wording "until it reaches the average rate" is in place (grep: 1 match).
- MAJOR glide: "at each renewal" and "limited by the yearly cap" are not in the quoted FIM p.110 text ("gradually phase out through a statutory annual increase cap discount"). Fix: state only what that quote says; drop "at each renewal" unless a source says it. The Emergency Program exclusion and the "Those discounts" wording are fixed.
- MAJOR cwop: "a claim" is wider than the source. The NFIP dictionary entry is nonPaymentReasonBuilding (building claims only). Fix: "a building claim closes without payment..." The four reasons (01 less than deductible, 02 seepage, 03 backup drains, 06 not actual flood) are supported by the dictionary.
- PASS aid_insurance: "buy or build" scope and "at least the amount of the aid" match the round-49 raw read.
- PASS nfip_not_sold: "withdrawn" dropped; "once a suspension takes effect" matches 44 CFR 59.24.
- PASS rr2_zone: "Risk Rating 2.0" and "existing policies" removed; the sentence matches the FloodSmart quote.
- PASS zone_price: "Your flood zone is set at your exact address." is cut (not on the built page); "for the term of a loan" added.
- PASS seller_assign: scoped to a finished home with a building policy; both exceptions covered.

## palm-beach-county-fl
Verdict: FAIL
- MAJOR cap: same defect as louisiana (comparator "for other property" on the built page).
- MAJOR glide: same defect as louisiana ("at each renewal", "limited by the yearly cap" on the built page).
- MAJOR cwop: same defect as louisiana ("a claim closes without payment" on the built page).

## broward-county-fl
Verdict: FAIL
- MAJOR cap: same defect as louisiana (comparator "for other property" on the built page).
- MAJOR glide: same defect as louisiana ("at each renewal", "limited by the yearly cap" on the built page).
- MAJOR cwop: same defect as louisiana ("a claim closes without payment" on the built page).

## new-york-county-ny
Verdict: FAIL
- MAJOR cap: same defect as louisiana (comparator "for other property" on the built page).
- MAJOR glide: same defect as louisiana ("at each renewal", "limited by the yearly cap" on the built page).
- MAJOR cwop: same defect as louisiana ("a claim closes without payment" on the built page).

## Gaps
- cap: 42 U.S.C. 4015(e)(3) was not read this round; the comparator wording needs it.
- glide: FIM p.110 full sentence not re-read this round; only the round-49 quote is checked.
- cwop: the registry cites only "Claim denied that was less than deductible" and "Not actual flood". Seepage and backup drains are in the dictionary but have no quote in the registry.
- Round-49 gap closed: "Since FEMA" and "withdrawn" are not on any of the four built pages (grep: no match). The palm-beach rr2_zone sentence is therefore not printed.
- home not grepped this round; its PASS stands from round 49.
- Not rebuilt, committed or pushed. The round-49 FIM PDF in the scratchpad still exists; the owner should delete it.
