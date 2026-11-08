# Hater round 113 (very light, text only: FEMA map card + source line)

Checked: outcome parts = total rulings (Levy 21+4+17+2 = 44; Sonoma 364+52+57+10 = 483); zone table sums and high-risk shares recomputed (Levy 851/932 = 91.3%; Sonoma 1,715/2,368 = 72.4%); each map claim sits in a card with a labelled FEMA National Flood Hazard Layer source line; nothing says the reader's own zone or an official determination ("rulings for owners who applied, not a share of all homes", "Check your own address on FEMA's flood map").

## levy-county-fl
- **MINOR** Source line reads "Data: FEMA's map service, retrieved 2026-11-08; retrieved November 8, 2026." The date is printed twice, once in ISO form. Reader sees a stutter; fix the template so the line prints one date.
- **MINOR** "2 other or mixed" does not say what "mixed" means. A hurried reader cannot tell if it is good or bad news.
- **GAP** The LOMA counts have no time span (all rulings since when?). The oldest/newest panel dates are given, but the 44 rulings have no "since" year, so a reader cannot tell if these are recent. Top results for LOMA give no span either, so not blocking.
- **GAP** No plain-words line that the outcomes of past rulings do not predict the reader's own result (the "not a share of all homes" line comes close).
- Claim not re-verified by me against the rule text: "FEMA charges no review or processing fee for a Letter of Map Amendment request (44 CFR 72.5)". The builder states it comes through `rule()`; confirm the recheck log has the quote read this session.

Verdict: PASS

## sonoma-county-ca
- **MINOR** Same doubled "retrieved" date in the NFHL source line.
- **MINOR** "12 Letters of Map Revision, 4 of them in effect since January 1, 2021" is ambiguous: reads as if 8 are older, with no date for those. Say "8 earlier" or give the span.
- **MINOR** "10 other or mixed" is undefined (see Levy).
- **GAP** "364 took the building or some or all of the lot out" out of 483 can read as a high odds of success. The sentence "rulings for owners who applied" helps, but it is not said that owners who applied are a self-selected group. Not blocking.
- **GAP** Same missing time span for the LOMA counts.

Verdict: PASS

## Classes
- County template, both pages: the doubled NFHL "retrieved" date (MINOR, every county page).
- County template: "other or mixed" is undefined (MINOR).
- No label/data contradictions found in the map card: totals add up, panel dates agree with the stated current-map effective date on both pages, and the county-versus-community counting basis is printed beside the figures.
