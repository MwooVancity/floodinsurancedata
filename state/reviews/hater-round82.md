# Round 82 (LIGHT, text only; title/H1 change)

Method: built HTML text only, no screenshots, no web search; round 81 verdicts skimmed only for the verdict lines. Checklist lines A-N: only title/H1 changed, so only C (base), D (confusion), E, N judged; all other lines unchanged from round 81 (PASS).

## home

Unchanged this round (title 'Flood insurance cost by state and county (FEMA data)', H1 'What flood insurance costs in your state'). Screen 1 states the base: 'existing single-family primary-home policies pay, premium plus fees'.


Checklist C/D/E/N: PASS (title base 'median, single-family' is correct and matches the lede; unit is the only gap).

Verdict: PASS

## louisiana

Title 'Louisiana flood zones and flood insurance: $1,114 median, single-family'; H1 'Louisiana flood zones and flood insurance'. Lede: 'median NFIP flood insurance policy on a single-family primary home costs $1,114 a year (premium plus fees, ... August 31, 2026)'. Screen 1 has 'Find your flood zone on FEMA's map' and the address form; zone table ('What does it cost in my flood zone?') is below screen 1.

- **MINOR** Title '$1,114 median' has no unit: 'a year' and 'premium plus fees' appear only in the lede and meta description. A searcher could read '$1,114 median' as a one-time or home figure. Base (median, single-family) is clear; unit is not. Suggest '$1,114/yr median'.
- **MINOR** Title/H1 promise 'flood zones': delivered on screen 1 by the FEMA map button and address lookup; the zone-by-zone cost table is further down. No zone key (A, AE, V, X in plain words) was found by search of the page text under that name; zones are explained inline instead. Acceptable.

Checklist C/D/E/N: PASS (title base 'median, single-family' is correct and matches the lede; unit is the only gap).

Verdict: PASS

## palm-beach-county-fl

Title 'Palm Beach County, FL flood zones and flood insurance: $673 median, single-family'; H1 'Palm Beach County, Florida flood zones and flood insurance'. Same lede and screen-1 structure as Louisiana. H1 reads fine at this length.

- **MINOR** Same unit gap as Louisiana: '$673 median' without 'a year' in the title.
- **MINOR** Title says 'FL', H1 says 'Florida'. Different on purpose (title length) but the two disagree in form.

Checklist C/D/E/N: PASS (title base 'median, single-family' is correct and matches the lede; unit is the only gap).

Verdict: PASS

## new-york-county-ny

Title 'New York County, NY flood zones and flood insurance: $1,021 median, single-family'; H1 'New York County, New York ...'. A reader who means New York City (Manhattan) is told 'New York County'; the H1 'New York County, New York' repeats the word New York but is accurate and what FEMA calls the unit.

- **MINOR** Unit gap in title ('$1,021 median', no 'a year').
- **GAP** Query 'flood insurance cost new york county NY' is a Manhattan reader; the H1 does not say Manhattan. Not wrong.

Checklist C/D/E/N: PASS (title base 'median, single-family' is correct and matches the lede; unit is the only gap).

Verdict: PASS

## fairfield-county-ct

Title 'Fairfield County, CT flood zones and flood insurance: $1,512 median, single-family'; H1 'Fairfield County, Connecticut flood zones and flood insurance'. Reads well. Note Connecticut counties are not active governments; FEMA data still lists county, so label is accurate.

- **MINOR** Unit gap in title ('$1,512 median', no 'a year').

Checklist C/D/E/N: PASS (title base 'median, single-family' is correct and matches the lede; unit is the only gap).

Verdict: PASS

## travis-county-tx

Title 'Travis County, TX flood zones and flood insurance: $1,012 median, single-family'; H1 'Travis County, Texas flood zones and flood insurance'. Reads well.

- **MINOR** Unit gap in title ('$1,012 median', no 'a year').

Checklist C/D/E/N: PASS (title base 'median, single-family' is correct and matches the lede; unit is the only gap).

Verdict: PASS

## Classes

- county/state: title figure lacks 'a year' (MINOR, one template fix in build_page.py).
- county: title uses state abbreviation, H1 full name (MINOR).
- county: Extra H1 checks beyond the six (built HTML, text only): portsmouth-city-va H1 'Portsmouth city, Virginia flood zones and flood insurance' (title 'Portsmouth city, VA ... $597 median'); orleans-parish-la 'Orleans Parish, Louisiana ...'; st-louis-county-mo 'St. Louis County, Missouri ...'. All read acceptably; lowercase 'city' is the Census name and a little clipped, MINOR. portsmouth-city-va screen 1 shows only the link 'Check your address on FEMA's flood map', not the address form that Louisiana and Palm Beach have, so the 'flood zones' promise is weaker there (MINOR, consistency N).

## Previous items

Round 81: no BLOCKER or MAJOR open; nothing to mark FIXED or NOT FIXED.
