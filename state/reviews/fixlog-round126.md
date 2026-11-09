# Fixlog round 126

- MAJOR zone X odds_30_x: defect = "so its mapped chance is under 1 percent" inferred beyond the FEMA glossary quote (shaded X also holds some 1%-chance areas). Root cause = a "so" clause derived from a definition, not quoted. Fix = rule deleted (delete over reword; no raw FEMA text gives shaded-X odds). Proof = grep odds_30_x in tools/ and dist/ returns nothing after rebuild.
