# Hater round 23: light check of two wording changes

Scope: page text extracted from dist/ (no screenshots, no web search). Two changes checked: (1) the disaster card note, (2) the NFIP deadline planner (louisiana, palm-beach-county-fl, broward-county-fl).

## home

- MAJOR: "Florida: Citizens homes with wind cover need it in a high-risk zone since 2023; outside one, since January 2026 if they cost $400,000 or more to rebuild, and from January 2027 for all others." Stated as a legal fact with no source on the page. Not verified here (no web search). Fix: cite the rule's source next to it, or cut it.
- MINOR: The disaster card note is not on this page (0 hits for "disaster" or "declaration"), so change 1 cannot be checked here. Confirm that is intended.
- MINOR: "every record the download listed for each state, none missing" is vague to a newcomer. Fix: "every FEMA record for each state; none left out."

Verdict: FAIL

## louisiana

- MAJOR: "send a signed proof of loss within 60 days of the flood" and the planner output "An NFIP proof of loss is due by ..." use "proof of loss" with no definition anywhere on the page. A flooded owner does not know what document this is. Fix: add one clause saying what it is (a signed statement of the loss and its amount).
- MINOR: "Report the loss to your insurer now if you have not." and "Contact your insurer now." are imperatives inside computed output. Not a promise, but advice. Keep one next step; drop the rest.
- MINOR: Note: "the count covers every flood, hurricane ... declaration FEMA lists here" names a count the card never shows, and "declaration" is never defined. Fix: "FEMA disaster declarations (each one a federal approval for a named event)" or similar, one clause.
- MINOR: The planner's intro says FEMA's disaster-aid window is "60 days from that declaration date (44 CFR 206.112)". Not verified here.
- Checked OK: planner math. The code sets due = date entered + 60 days, and the three outputs match the wording. "may have extended the date" is a real hedge, so the output is not a promise. The note's new merge rule is not exercised on this card (no merged line).

Verdict: FAIL

## palm-beach-county-fl

- MAJOR: Same as louisiana. "An NFIP proof of loss is due by ..." and "send a signed proof of loss within 60 days" use the term with no definition. Fix: one clause defining it.
- MINOR: "Contact your insurer now; it may have extended the date." Imperative advice in a computed result. Keep, but cut the duplicate imperative in the other two outputs.
- MINOR: Note: "the count" names no visible total; "declaration" undefined. Same fix as louisiana.
- MINOR: "(44 CFR 206.112)" and the 60-day disaster-aid window are not verified here.
- Checked OK: planner math (date + 60 days), outputs match wording, hedged past-date output, no merged line on this card.

Verdict: FAIL

## broward-county-fl

- MAJOR: Same as louisiana and palm-beach. "proof of loss" is used in the planner outputs and the body with no definition. Fix: one clause defining it.
- MINOR: Imperative "Contact your insurer now" in the computed outputs. Same as palm-beach.
- MINOR: Note: "the count" names no visible total; "declaration" undefined.
- MINOR: "(44 CFR 206.112)" and the 60-day disaster-aid window are not verified here.
- Checked OK: planner math and output wording. Card dates are in the form "Month Year — Title", consistent with the note.

Verdict: FAIL

## maine

- MINOR: "September 2023 — Severe Storm and Flooding (two separate declarations)". The note's "says how many" holds (the line gives a count), but "two separate declarations" can read as two storms. Fix: "(2 FEMA declarations, one storm event)" only if that is true; otherwise keep the wording and say "two FEMA declarations".
- MINOR: Note: "share one line, which says how many" has a dangling "which" (the reader cannot tell if the title or the line says the count). Fix: "...share one line that states how many."
- MINOR: Note: "the count covers ..." and "declaration" are undefined for a newcomer (same as the other pages).
- Q1 answer: the merged line matches the note's rule (same month, same title, count shown). Clear enough for an expert; a newcomer needs "declaration" defined.

Verdict: PASS

## Summary of verdicts

home FAIL (unsourced Florida rule); louisiana FAIL; palm-beach-county-fl FAIL; broward-county-fl FAIL (all three on the undefined "proof of loss"); maine PASS.
