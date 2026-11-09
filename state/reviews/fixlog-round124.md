# Fixlog round 124 (light review: home, claims, flood-zones-ae, samples for the 50% rule)

- MAJOR claims/home: "every claim record, paid or not" while FEMA codes 98/99 are dropped. Root cause: label written before the 98/99 rule. Fix: label names the exclusion (build_site.py, both places). Proof: claims_check C8 sweeps every built page; mutation planted page caught.
- MAJOR flood-zones-ae (live on all state/county pages): substantial_damage said "local floodplain rules can require elevating" with no quote. Root cause: inference in rule text. Fix: rewritten from 44 CFR 59.1 and SFIP Coverage D read raw 11-09; unclear clause and its manual source cut (rules_registry.py). Proof: re-review PASS on louisiana, palm-beach-county-fl, new-york-county-ny, flood-zones-ae.
- MAJOR flood-zones-ae: 50% test dropped 59.1's cost basis ("cost of restoring the structure to its before damaged condition"). Fix: same rewrite quotes it. Proof: as above.
