# Hater round 51: recheck of the round-50 rewrites (cap, glide, cwop)

Checked: current text in tools/rules_registry.py (read 2026-11-02); the FIM PDF downloaded from the FIM constant (line 8, curl -sL -A "Mozilla/5.0") and page index 109 (manual p.110) extracted with pypdf; the NFIP dictionary for nonPaymentReasonBuilding (read 2026-11-02). Built dist pages were not re-grepped this round; they still carry round-50 wording until rebuilt.

## home
Verdict: PASS
None of the eight rules print on this page (not re-judged this round; round 49 stands).

## louisiana
Verdict: PASS
- PASS glide: the manual p.110 reads "Except for the Emergency Program discount, statutory discounts gradually phase out through a statutory annual increase cap discount at each renewal date until the policy reaches its full-risk premium." The registry sentence has the same exclusion, "at each renewal date" and "until the policy reaches its full-risk premium". It drops "statutory" before "annual increase cap discount"; the sentence still opens with "statutory discounts", so the scope holds.
- PASS cap: "until that group's average rate reaches the level the law sets" is supported by the quoted rule (average rate equal to the average for the paragraph (3) group). The endpoint is vague (see Gaps).
- PASS cwop: "a building claim closes without payment" matches the NFIP nonPaymentReasonBuilding dictionary; the four reasons are in it.

## palm-beach-county-fl
Verdict: PASS
- PASS glide, cap, cwop: as louisiana (registry text is shared; built page not yet rebuilt).

## broward-county-fl
Verdict: PASS
- PASS glide, cap, cwop: as louisiana (registry text is shared; built page not yet rebuilt).

## new-york-county-ny
Verdict: PASS
- PASS glide, cap, cwop: as louisiana (registry text is shared; built page not yet rebuilt).

## Gaps
- glide: the registry's machine-check source quotes only the fragment "gradually phase out through a statutory annual increase cap discount". Extend it to the full p.110 sentence so the check covers "at each renewal date" and the Emergency exclusion.
- cap: the page does not name the paragraph (3) group, and "the level the law sets" is vague for a reader. 42 U.S.C. 4015(e)(3) and (e)(4) not read this round.
- Built dist pages still show round-50 wording; a rebuild is needed before any page-text check.
- The FIM PDF is in the scratchpad at ...\scratchpad\fim\fim.pdf; delete it when done.
- Not built, committed or pushed.
