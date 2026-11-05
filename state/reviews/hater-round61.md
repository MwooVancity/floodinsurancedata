# Round 61: light review (final build)

Method: own list made from the rebuilt page text first (changed parts only, text only); the fixlog was not needed to judge. FIM wording judged from the quotes in the brief and the registry's listed quotes; the FIM PDF itself was not opened.

## home
- Round 60 MAJOR (homeowners_excl) fixed: now the sentence is exactly the first clause FloodSmart supports ("most homeowners insurance does not cover flood damage"). No unquoted second clause remains.
- MINOR: howto_answer says "if the insurer is paid within 10 days (30 if the lender, title company or settlement attorney pays)". The manual requires the application AND the full amount due within the window, so "is paid" is weaker than the source. It is not misleading in practice (payment normally goes with the application) and the 10/30-day split now matches the quotes. Optional: "gets the application and full payment within 10 days of closing". Also "within 10 days" does not say "of closing" (a reader could count from purchase); the county quick answer still says "paid in time", so the two screens differ in precision (not contradictory).
- No other defects in the changed text.
Verdict: PASS

## louisiana
- Card openings read correctly for a state: "In Louisiana, typically about $1,114 a year ($93 a month), fees included", "Floods in Louisiana have led to 485,743 NFIP flood claims ... since 1978", "Most do : 77.8% of claims in Louisiana paid something", "52.8% of policies in Louisiana pay less than...". Grammar fine.
- MINOR: tile "52.8% / Of these homes, pay below FEMA's full-risk price" reads as a fragment (capital "Of", stray comma after "homes"). Suggest "Of these homes, % pay below..." or "Homes paying below FEMA's full-risk price".
- MINOR: gap card says "52.8% of policies" with no base; the population is single-family primary-residence policies that have both premiums, not all policies (the tile says "homes", the card says "policies"). The "(premiums only, before fees)" note is correct.
- Out of this round's scope, noted: the "Exceptions" paragraph prints "within 13 months" for the newly-mapped-zone one-day wait while FloodSmart buy-a-policy says "within 12 months" (I read it this session). Two official sources disagree; the project rule is to print only what both support (or cite the manual by name, which it does). Not a regression.
Verdict: PASS

## palm-beach-county-fl
- "In Palm Beach County, typically about $673 a year ($56 a month), fees included"; "Floods in Palm Beach County have led to 10,758 NFIP flood claims and $72.0 million in payouts since 1978"; "23.2% of policies in Palm Beach County pay less than..." Grammar and place name correct; numbers match agg.json (p50 673, share_below 23.2, 10,758 claims).
- MINOR: same tile fragment and "policies" vs "homes" base point as louisiana.
Verdict: PASS

## harrison-county-ms
- "In Harrison County, typically about $1,233...", "Floods in Harrison County have led to 15,939 NFIP flood claims", "Most do : 83.2% of claims in Harrison County paid something", "67.1% of policies in Harrison County..." Correct and consistent with the screen-1 figures (83.2%).
- MINOR: same tile and base points.
Verdict: PASS

## glynn-county-ga
- "In Glynn County, typically about $979...", "Floods in Glynn County have led to 1,996 NFIP flood claims", "68.1% of claims in Glynn County paid something", "34.4% of policies in Glynn County..." Correct and consistent with screen 1 (68.1%, $979, 34.4%).
- MINOR: same tile and base points.
Verdict: PASS
