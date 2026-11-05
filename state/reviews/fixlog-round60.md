# Fixlog round 60

- MAJOR home, homeowners_excl: "bought separately, through the federal NFIP or a private insurer" had no source quote. Root layer: rule text wider than its quote. Fix: rule cut to the quoted clause "Most homeowners insurance does not cover flood damage." Proof: tools/rules_registry.py homeowners_excl text equals its source's sentence.
- MINOR home, howto_answer: "in time" now states the window (10 days after closing, 30 if the lender, title company or settlement attorney pays), with both FIM quotes added as sources.
- MINOR places, tile label: now "Of these homes, pay below FEMA's full-risk price" (same single-family primary-home base as the median tile beside it).
