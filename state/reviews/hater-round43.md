# Hater round 43

Scope: re-check of round 42 MAJORs after rule-text rewrite: seller_assign, lender_amount, lender_force, zone_review, odds_30, flood_def, not_covered, claim_appeal, substantial_damage, lapse_discount. Text read from tools/rules_registry.py; all ten confirmed by grep in dist/flood-insurance/palm-beach-county-fl/index.html (1 hit each). Text is identical on the four place pages; home does not carry it (grep count 0). Fixlog-round42 read after my own list. Statute and FEMA quotes judged from the registry's quoted fragments, not re-fetched.

## home
Verdict: PASS
- Unaffected: none of the changed sentences appear in dist/index.html (grep count 0).

## louisiana
Verdict: PASS
- Round 42 MAJOR lender_amount closed: now "Where a federally regulated lender must require it, the legal minimum is the loan balance or the NFIP's limit..., whichever is less". "Minimum" matches "at least equal to" and the scope is stated. No false statement.
- Round 42 MAJOR claim_appeal closed: now "NFIP claim denied?"; 60-day appeal and one-year suit match the quoted floodsmart text.
- **MINOR** lapse_discount: "paid 30 days or more after it expires" leaves day 30 itself unclear (NFIP accepts renewal payment within 30 days of expiry); say "more than 30 days" only if the source confirms it.
- **MINOR** lender_amount: "minimum" implies but does not say a lender can ask for more.
- **MINOR** not_covered: "A standard NFIP home policy" is safer than before but condo and General forms may differ (see Gaps).
- **MINOR** zone_review: "checks only the zone finding" is right but the elevation-data route is not named.
- **MINOR** label: card "How do I actually get covered" holds "What it won't pay" and "Claim denied?".
- Fine: seller_assign (discount move is FEMA's wording), lender_force (scoped by "such a lender"), odds_30 (26.0%), flood_def, substantial_damage (now scoped to NFIP with building coverage, official letter before work), no verdict or "you should" wording.

## palm-beach-county-fl
Verdict: PASS
- Same sentences as louisiana; both MAJORs closed, grep confirms new wording live in dist. MINORs as above.

## broward-county-fl
Verdict: PASS
- Same sentences as louisiana; both MAJORs closed. MINORs as above.

## new-york-county-ny
Verdict: PASS
- Same sentences as louisiana; both MAJORs closed. Condo-heavy county: the not_covered MINOR (Residential Condominium form may differ) still matters most here.

## Gaps
- GAP: private flood and Group Flood policies: no appeal or deadline rule printed; name the data (the policy contract) as not in FEMA records.
- GAP: condo (Residential Condominium form) and General Property form differences on contents, basement, and ACV are not covered.
