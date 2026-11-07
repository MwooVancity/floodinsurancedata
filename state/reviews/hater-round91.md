## home
No findings: no changed sentence or "closed" wording on the home page (0 hits).
Verdict: PASS

## louisiana
**MAJOR** Payout card still says "FEMA's claim records give a reason when a building claim closes without payment" (source: tools/rules_registry.py line 249), the same false open/closed premise, and it contradicts the next note "FEMA's data has no open or closed field". Fix: "give a reason when a building claim has no recorded payment".
**MAJOR** "These shares count every FEMA claim record, including ones FEMA coded as entered in error, which the claims page leaves out, so its shares run higher." Code: county card counts net <= 0 over all years and all records (agg_raw/collect_claims_extra); claims page (build_site.py ~510) is losses 2020 on only, drops codes 98/99. So the gap is also a time window, and "run higher" is not guaranteed against an all-years card. Fix: "The claims page counts only losses from 2020 on and leaves out records FEMA coded as entered in error; these shares cover all years and every record."
**MINOR** Quick-answer link text "Unpaid can mean paperwork or damage the policy did not count as flood." uses "Unpaid" while the card says "no recorded payment" (and may still be paid). Fix: "No recorded payment can mean...".
Verdict: FAIL

## palm-beach-county-fl
**MAJOR** Payout card still says "FEMA's claim records give a reason when a building claim closes without payment" (source: tools/rules_registry.py line 249), the same false open/closed premise, and it contradicts the next note "FEMA's data has no open or closed field". Fix: "give a reason when a building claim has no recorded payment".
**MAJOR** "These shares count every FEMA claim record, including ones FEMA coded as entered in error, which the claims page leaves out, so its shares run higher." Code: county card counts net <= 0 over all years and all records (agg_raw/collect_claims_extra); claims page (build_site.py ~510) is losses 2020 on only, drops codes 98/99. So the gap is also a time window, and "run higher" is not guaranteed against an all-years card. Fix: "The claims page counts only losses from 2020 on and leaves out records FEMA coded as entered in error; these shares cover all years and every record."
**MINOR** Quick-answer link text "Unpaid can mean paperwork or damage the policy did not count as flood." uses "Unpaid" while the card says "no recorded payment" (and may still be paid). Fix: "No recorded payment can mean...".
Verdict: FAIL

