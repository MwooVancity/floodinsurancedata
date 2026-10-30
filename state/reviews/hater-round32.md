# Hater round 32 (light review: payout "typical claim" note, unpaid wording)

Checked against extras.json / agg.json: median = claims.paid_building_median, storm = claims.events[0], total = claims.total_paid. All match the page text. Storm part appears only where storm paid over half: Louisiana Katrina 13.30B/20.68B = 64%, Broward April FL Flooding 244.5M/456.6M = 54%, Manhattan Sandy 111.4M/120.6M = 92%. Palm Beach top storm (Frances 11.3M/72.0M = 16%) correctly omitted.

## home
- Text extracted: no NaN, undefined, None, [object], or unfilled {{ }}. Dollar figures render ($1,055, $88, $995, $400,000).
- MINOR: not graded further (scope).
Verdict: PASS

## louisiana
- Verified: "the median paid building claim was $21,898" = 21898; "Hurricane Katrina alone paid $13.3 billion of the $20.7 billion total" = 13,303,427,706 / 20,682,152,359. Screen 1 "typical paid building claim was $21,898". Average $55,453 unchanged.
- MINOR: "alone" plus "median" is a little jargon for a newcomer; "pulls the average up" is plain enough.
- MINOR: median is building-only while the total includes code-upgrade (ICC) pay; the card already labels the average "incl. code-upgrade (ICC) pay", so not misleading.
Verdict: PASS

## palm-beach-county-fl
- Verified: median $4,472 = 4472. No storm clause (Frances 16% of total), correct.
- MINOR: median $4,472 beside average $15,396 gets no explanation of the gap; the reader sees "Typical claim" and the average and can still infer the average is higher. Not misleading.
- MINOR: "Closed without payment can mean paperwork (a duplicate, a claim opened in error) ..." - "duplicate" is not a row in the table (it would sit in "Other" 1,107); the clause "the table shows which" slightly over-promises. Top reason is 1,706 "Not an actual flood" and 432 "Assigned in error", so the table does split paperwork from not-flood.
Verdict: PASS

## broward-county-fl
- Verified: median $5,093 = 5093; "April Florida Flooding alone paid $244.5 million of the $456.6 million total" = 244,475,829 / 456,568,107 (53.5%, over half, so the clause is allowed).
- MINOR: "April Florida Flooding" is FEMA's event name; the page does not say it is the 2023 flood in this sentence (the event table below gives the year). Not misleading.
- MINOR: same "duplicate" wording point as Palm Beach.
Verdict: PASS

## new-york-county-ny
Round 31 MAJORs:
- MAJOR 1 (average $131,524 read as typical, Sandy skew): now FIXED. Card says "Typical claim: the median paid building claim was $28,756 ; Hurricane Sandy alone paid $111.4 million of the $120.6 million total, which pulls the average up." Values match extras (28756; 111,415,427) and agg (120,592,136). Screen 1 now says "the typical paid building claim was $28,756".
  - MINOR remaining: the opening card sentence still leads with "The average paid claim was $131,524" and the stat tile still shows "$131,524 New York: $39,718" with no Sandy mark on the tile itself; the caveat is one sentence away in the same card, so a reader would not misread it.
- MAJOR 2 (paperwork vs "not an actual flood"): now FIXED. Wording is "Closed without payment can mean paperwork (a duplicate, a claim opened in error) or damage the policy did not count as flood damage; the table shows which here." Table splits Not an actual flood 160, Other 101, Damage less than the deductible 81, Assigned in error 47, No demonstrable damage 45. Screen 1: "Unpaid can mean paperwork or damage the policy did not count as flood." No longer calls the unpaid share paperwork.
  - MINOR: "Damage less than the deductible" (81) is neither paperwork nor not-flood; the sentence does not name it, though the table lists it.
- No NaN/undefined/None in extracted text.
Verdict: PASS
