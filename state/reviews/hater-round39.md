# hater round 39: cost-card sentence

Scope: one sentence, "The every-policy-type average includes them. The single-family figures use FEMA's occupancy code with no separate condo filter, so condo units could be in them." Checked against tools/ffcalc.py lines 18 and 49 and the built page text. Nothing else reviewed.

Code evidence:
- ffcalc.py:18 `isone()` = occupancy type 1 or 11 (the code labels these single-family).
- ffcalc.py:49 single-family cohort = `isone(occupancyType)` AND `primaryResidenceIndicator`. No condo-specific test.
- ffcalc.py:48 all-policy units sum every row with no occupancy filter, so the every-policy figure does include condos.
- Result: the sentence is accurate. ffcalc.py does not say what code 11 is.

## home
Verdict: PASS
The sentence is not on this page (dist/index.html has no "no separate condo filter"). Its cost table reads "Average cost, every policy type (adds condos, rentals, businesses)". Not reviewed further.
**MINOR**: none for this sentence.

## louisiana
Verdict: PASS
**MINOR**: Jargon ("occupancy code", "condo filter", "every-policy-type average") and "them" is ambiguous (condo units vs whole condo buildings). A homeowner cannot tell what it means. "could be" hedges a point the code settles; if code 11 is condo units, the sentence understates it.

## palm-beach-county-fl
Verdict: PASS
**MINOR**: Same jargon and ambiguous "them" as louisiana. Same hedge note.

## broward-county-fl
Verdict: PASS
**MINOR**: Same jargon and ambiguous "them" as louisiana. Same hedge note.

## new-york-county-ny
Verdict: PASS
**MINOR**: Same jargon and ambiguous "them" as louisiana. Same hedge note.
