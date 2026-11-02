# Hater round 49: rewritten legal and program sentences

Checked against source text read raw (curl, text stripped), not the registry excerpts. FIM = Oct 2025 Flood Insurance Manual, pdf pages 110, 144, 158, 161 read by pypdf. Rule keys are in tools/rules_registry.py. A MAJOR line lists its full fix under louisiana; the same key repeats below with a pointer, because the sentence is identical on each page.

## home
Verdict: PASS
None of the ten rules print on this page (checked by data-rule tags and sentence text), so no sentence here is judged in this round.

## louisiana
Verdict: FAIL
- MAJOR cap: quote "the rate for some property, including homes that are not a primary residence and business property, rises 25% a year." Why: 42 U.S.C. 4015(e)(4) applies the 25% a year only "until the average risk premium rate for such properties is equal to the average of the risk premium rates for properties described under paragraph (3)". The sentence has no stop, so it reads as permanent. Fix: end it "...rises 25% a year until it reaches the average rate for primary homes (42 U.S.C. 4015(e)(4))."
- MAJOR glide: quote "Those discounts phase out at each renewal until the policy reaches its full-risk premium, limited by the yearly cap." Why: FIM p.110 says "Except for the Emergency Program discount, statutory discounts gradually phase out through a statutory annual increase cap discount". "Those discounts" has no antecedent and includes the Emergency Program discount, which does not phase out. Fix: "Statutory discounts other than the Emergency Program discount phase out at each renewal, through the annual increase cap discount, until the policy reaches its full-risk premium (FIM p.110)."
- MAJOR aid_insurance: quote "If FEMA housing aid after a flood goes to a home in a high-risk zone, you must buy and keep flood insurance on it..." Why: 44 CFR 206.110(c)(3) applies only to aid "for acquisition or construction purposes", not all housing aid, and requires insurance "for at least the assistance amount". Fix: "If FEMA aid to buy or build a home after a flood goes to a home in a high-risk zone, you must buy and keep flood insurance on it for at least the amount of the aid, or you cannot get federal aid for later flood damage to it (44 CFR 206.110(c)(3))."
- MAJOR nfip_not_sold: quote "in a community that has not joined, has withdrawn or is suspended, no one can buy an NFIP policy." Why: no source read says "withdrawn". 44 CFR 59.24 makes a suspension effective only "upon the expiration of the six month period", so it is not immediate. Fix: "...in a community that has not joined, or whose eligibility has been suspended once the suspension takes effect, no one can buy an NFIP policy (42 U.S.C. 4012(c); 44 CFR 59.24)." Drop "withdrawn" unless a source is read.
- MAJOR rr2_zone: quote "Since FEMA's Risk Rating 2.0, the premium is based on the flood risk of the building, and these are existing policies whose buildings differ." Why: the cited FloodSmart premium page has the flood-risk sentence but never names Risk Rating 2.0 (0 matches) and gives no start date; "existing policies whose buildings differ" has no source. Fix: "The premium is based on the flood risk of the building (FloodSmart premium costs). The reason for any one zone is not in this data."
- MAJOR zone_price: quote "Your flood zone is set at your exact address." Why: no source read or cited supports it. Fix: cut the sentence, or read FEMA's map source raw and cite it.
- MAJOR cwop: quote "FEMA lists reasons a claim closes without payment..." Why: the cited source (44 CFR 61, flood definition) does not list claim-closing reasons. The four labels match tools/codes.py NONPAY_REASON codes 01, 06, 02, 03, but the FEMA NFIP Claims data dictionary entry for nonPaymentReasonBuilding was not read. Fix: read that dictionary entry raw and cite it; until then, print a gap line instead.
- MAJOR seller_assign: quote "the seller can assign the policy to you in writing when title transfers." Why: 44 CFR Part 61 says "You may assign this policy in writing when you transfer title... except under these conditions: a. When this policy insures only personal property; or b. When this policy insures a building under construction." The sentence drops the policy-form scope and both exceptions. Fix: "On a standard NFIP policy that insures a finished building, the seller can assign the policy to you in writing when title transfers (44 CFR Part 61)."
- MINOR surcharge: "$250 a year" is supported (42 U.S.C. 4015a(a)-(b); policies newly issued or renewed after March 21, 2014). Add: "The surcharge ends once every property's rate reaches full risk (42 U.S.C. 4015a(c))." Scope and amounts are otherwise correct.
- MINOR zone_price: add "for the term of the loan" after "must require coverage on a loan" (42 U.S.C. 4012a(b)(1)).
- PASS lapse_discount: "30 days or more" matches FIM p.158 and p.161; the full-risk consequence is not printed but not wrong.
- PASS cap (18% part), CRS and cap-exception wording: FIM p.144 "except when increasing coverage, decreasing the amount of the deductible" matches.

## palm-beach-county-fl
Verdict: FAIL
- MAJOR cap, glide, aid_insurance, zone_price, cwop, seller_assign: same sentences and same defects as louisiana; use the louisiana fixes.
- MINOR surcharge, zone_price: as louisiana.
- nfip_not_sold and rr2_zone are not tagged on this page; see Gaps for one untagged "Since FEMA" sentence.

## broward-county-fl
Verdict: FAIL
- MAJOR cap, glide, aid_insurance, rr2_zone, zone_price, cwop, seller_assign: same defects as louisiana; use the louisiana fixes.
- MINOR surcharge, zone_price: as louisiana.
- nfip_not_sold is not printed on this page.

## new-york-county-ny
Verdict: FAIL
- MAJOR cap, glide, aid_insurance, zone_price, cwop, seller_assign: same defects as louisiana; use the louisiana fixes.
- MINOR surcharge, zone_price: as louisiana.
- nfip_not_sold and rr2_zone are not printed on this page.

## Gaps
- cwop: the FEMA NFIP Claims data dictionary (nonPaymentReasonBuilding) was not read. The verdict on the cwop sentence stands on the missing source.
- rr2_zone on palm-beach-county-fl: the phrase "Since FEMA" appears once in the built page, but I could not isolate the sentence with grep, so its wording is unverified.
- FEMA Risk Rating 2.0 page and FEMA map pages: not read (fema.gov blocks scripts; no manual read this round).
- surcharge: 4015a(c) is read as printed; the date in 4015a(a) is confirmed as March 21, 2014.
- The manual PDF was downloaded to C:/Users/mwoo7/AppData/Local/Temp/claude/C--Users-mwoo7-Desktop-floodinsurance/c9e0918c-80c3-42b3-ba23-c5d471be6cd8/scratchpad/src/fim/fim.pdf and is NOT deleted: the delete command was refused by the safety check, so the owner should remove it. The text caches in the sibling src folder are also left behind.
- No build, commit or push was run. This file is the only output.
