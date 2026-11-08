# Fixlog round 103 (+ round 97 item 1), 11-08
Root cause of the class: every gate checked "number = data"; none checked "label = what the data is". Reviewers filed
these as MINOR, and MINOR lists never age out of S14, so they sat live. Fix: four checks, each with a mutation in
test_gate.py; HATER-PROMPT now makes this class at least MAJOR.

- Decade table dropped a decade silently (Dixie 1980s, 27 claims). Root: `_decs` filter, no note. Fix: build_page lists
  left-out decades with their counts. Check C10. Proof: Dixie review page "not listed: 1980s (27 claims)"; mutation C10 PASS.
- Cost answer left out a big unpriced zone (Levy VE 21.5%, NY County AE 41.8%); "Largest zones" over one zone. Root:
  top-2 of priced zones only. Fix: zones with 10%+ of units are named ("has too few to price") or priced; singular
  wording. Check C11 (+ "too few to price" must be true: caught my own Brevard AE slip before ship). Mutations PASS.
- "Costliest flood" beaten by a catch-all row (Sonoma $3.5M vs $67.3M "Flooding"). Fix: lead wording kept (r11 banned "single");
  catch-all rows say "many floods". Check C12. Mutation PASS.
- "Latest two years not final" on 2024 data in 2026 (Dixie). Fix: note names the as-of year and the year before, only
  when charted. Check C13; card_spec "must" removed (C13 owns it). Mutation PASS.
- Claims count included FEMA codes 98/99 (Sonoma 187). Fixed 87ef60179; numbers move with the 12-03 refresh.
- "COVID aid excluded" yet included (Levy, Dixie): checked the aid rows; no COVID disaster is in them. Reviewer
  error, no change.
