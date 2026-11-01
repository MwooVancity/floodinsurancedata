# Round 38 (light, changed text only)

## home
Verdict: PASS
No condo or town line on this page; nothing contradicts it.

## louisiana
Verdict: FAIL
**MAJOR** "the single-family figures are not a condo price": the cohort (tools/ffcalc.py line 18 `isone` = occupancy 1 or 11, plus primary residence, no condo filter) keeps occupancy 11 (single residential unit, which is how condo units are normally recorded). Condo-unit policies on primary residences can therefore sit inside the "single-family" median. The sentence states as fact something the code does not enforce. Fix: either exclude condo coverage type U from the cohort, or reword to say how many condo units the single-family figures may include; prove with a count of cohort rows with condominiumCoverageTypeCode U.
**MINOR** "policy units" base is stated; fine.

## palm-beach-county-fl
Verdict: FAIL
**MAJOR** Same condo sentence ("the single-family figures are not a condo price"): same cohort defect as above, and condo share is large in Florida.
**MINOR** Town line is correct for Palm Beach County: Palm Beach, Boca Raton, North Palm Beach, Riviera Beach, Delray Beach are all in the county (33480, 33431/33432, 33408, 33404, 33483/33445 per zip_places.json). Readers may take a USPS ZIP name as the city limits (a Boca Raton ZIP includes unincorporated land), and the line does not say "ZIP mailing names"; consider "Mailing-address towns". "Ranked by policy units per ZIP" is understandable but the top ZIP, not the town total, drives the order.

## broward-county-fl
Verdict: FAIL
**MAJOR** Same condo sentence (3.4% condo-unit share) contradicted by the unfiltered occupancy 1/11 cohort.

## new-york-county-ny
Verdict: FAIL
**MAJOR** Same condo sentence (3.6%); worst case for a Manhattan reader, where most homes are condo or co-op units that may sit inside the single-family figures.
