# Hater round 57 (text review, narrow: wait_exceptions + start-date tool) - re-review after fixes

Manual pages 2-14 to 2-18 read in round 57's first pass (raw pypdf text); the fixes below were re-checked against those pages, then against the fixlog.

## home
Verdict: PASS (no change this round; neither item is on the home page).

## louisiana
- A1 fixed: wait_exceptions now says "a loan secured by the insured property (making, increasing, extending or renewing it)". Matches p. 2-14 and p. 2-16 ("making, increasing, extending, or renewing a loan secured by the insured property"). No new inference.
- T1 fixed: option label now "making, increasing, extending or renewing it"; "refinancing" gone.
- T2 fixed: start_loan rule now ends "Contents-only coverage qualifies only if the contents are part of the security for the loan." Matches p. 2-17. It sits in the paragraph above the tool, not in the loan result sentence; MINOR, since the paragraph is directly above the controls.
- T3 fixed: start_map says more than 13 months after the revision's effective date the 30-day wait applies (p. 2-16); every map result now ends "This holds only if the insurer receives them within 13 months of the map revision's effective date; after that, the 30-day wait applies." Error results (not a date, receipt before application) correctly do not get it. The fix did not change the none or loan wording; no regression seen.
- Remaining MINORs from first pass (A2 post-wildfire exception not listed, T4 insurer confirms the loan, T5 payment must clear, T6 renewals) unchanged; they do not fail.
Verdict: PASS

## palm-beach-county-fl
Same text, labels and JS as louisiana; all four fixes verified in this page's HTML and script.
Verdict: PASS

## broward-county-fl
Same as louisiana (tool present, fixes in place per the rebuilt rule line and the rule paragraph; identical template).
Verdict: PASS

## new-york-county-ny
Line A only: new wait_exceptions text carries the "secured by the insured property" scope and the four verbs; 13-month wording unchanged and correct.
Verdict: PASS

## wyoming
Line A only: as new-york-county-ny.
Verdict: PASS

## nueces-county-tx
Line A only: as new-york-county-ny.
Verdict: PASS

## Gaps
- No field for the map revision's effective date, so the 13-month limit is printed, not checked.
- Contents-only caveat is in the paragraph above the tool, not in the loan result.
- Tool does not say renewals are out of scope or that the insurer confirms the loan paperwork.
- Post-wildfire exception (manual p. 2-14, 2-18) not printed anywhere in the card.
