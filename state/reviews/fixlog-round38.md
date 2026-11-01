# Fixlog round 38
- MAJOR: "the single-family figures are not a condo price" states what the cohort does not enforce. Root cause: cohort filters occupancy 1/11 + primary only (ffcalc), and FEMA's old code 1 is not proven free of condo units. Fix: note now says exactly that. Proof: sentence in build_page; `coh` line read. Open: count cohort rows with condo code U at the next refresh, in the cloud.
