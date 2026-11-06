# Fixlog round 68
- MAJOR 1, zone D "Must I buy?" generic: layer template (build_site zone page used purchase_short, which never names the zones). Fix: screen 1 now prints purchase_answer ("only in a high-risk zone (A or V)") + lender_any_zone on every zone page, so D and X readers see their zone is outside the rule. Proof: dist/flood-zones/d/ text contains "(A or V)".
- MAJOR 2, zone_x glossary source not in manual-rule-read: layer registry log. Already added ("zone_x": "2026-11-06") before record; repetition cut: zone_x now states the two kinds once, then FEMA's shaded/unshaded labels. Proof: grep zone_x state/manual-rule-read.json.
- MINOR zone_codes: "waves" -> "with velocity, flooded by tides" (64.3 quote added), "D is not yet studied" -> "possible but undetermined flood hazards".
