# Hater round 126 (light)

Method: text read from dist/ HTML, data files, rules_registry.py, extras_raw.py; legal text re-read live (Cornell 42 USC 4015, 44 CFR 59.24; FEMA flood-zones glossary; FloodSmart premiumcosts and eligibility).

## home
- MINOR: "until that group's average rate reaches the level the law sets" is vague — 4015(e)(4) says: until the average rate for those properties equals the average rate of the properties in paragraph (3) (the 15%-average-cap group) — say "reaches the average rate of the other capped properties" or cut the clause.
- PASS checks: 18% and 25% match 4015(e) and 4014(a)(2)(A) and (D); "including" keeps the list open; "FloodSmart puts the limit at 18 to 25%" matches "18–25% per year for most policyholders"; "usually does not apply to new policies" matches FloodSmart.
Verdict: PASS

## claims
- MINOR: "on 1,968,497 claims" sits before the base is stated; the base (claims with recorded building damage and a building payment) is only in the note below. Reader may compare it with the 2005–2024 table's "claims on record". Fix: "on 1,968,497 such claims" or move the note up.
- PASS checks: data/us/claim_size.json p50 12384, n 1968497, as-of 2026-08-31 equals the page; NAT_PB uses the same base as the state medians; "50 states and DC" matches (51 keys); "since 1978" matches the table range.
Verdict: PASS

## renters
- PASS: the sentence is supported. 44 CFR 59.24 says "Flood insurance shall not be sold or renewed in those communities" (suspended or withdrawn); FloodSmart says availability depends on the town participating. "No one can buy" is accurate (renewal is also barred, which the sentence does not claim, so it understates, not overstates).
Verdict: PASS

## palm-beach-county-fl
- Numbers match data (12099): known_n 926, out_pct 56.6, out_paid_pct 43.3 (7,286,755 / 16,839,094 = 43.27%), 2016 to 2025.
- "zones X, B, C and D" is correct for the data: the national by-zone keys outside A/V are only X, C, B, D (blank is excluded and counted in blank_n = 0 here). Old numbered A and V zones, A99, AOB, AHB and AR are counted as A/V, so the label is right.
- "dollars paid on those claims" is right: building + contents + ICC net payments, in dollars as paid, on claims with a zone; denominators match (known_paid).
- MINOR: loss year 2025 is a partial reporting year (as-of 2026-08-31); the page does not say late-filed 2025 claims may be missing. Effect on a 10-year share is small. Fix: add "recent years may still gain claims" or end at 2024.
- MINOR: zone D (possible but undetermined hazard) is grouped under "outside the high-risk zones"; only 166 claims nationally, the zone list is printed, so not misleading.
Verdict: PASS

## new-york-county-ny
- Data (36061) matches: 162 claims, 56.2%, 50.9% (1,840,401 / 3,614,096).
- MINOR: small base (91 outside claims, 61 paid, 10 years); percentages are printed to one decimal with no "few claims" note. Counts are not printed beside the percents, but the 162 is.
- MINOR: same 2025 open-year note as Palm Beach.
Verdict: PASS

## levy-county-fl
- Data (12075) matches: 640 claims, 0.5%, 0.4%.
- MINOR: 0.5% is 3 claims; a percent of 3 claims reads as precision. Fix: print the count ("3 of 640") when out_n is under 10.
- MINOR: same 2025 open-year note.
Verdict: PASS

## sonoma-county-ca
- Data (06097) matches: 925 claims, 8.6%, 7.4% (2,436,283 / 33,120,728 = 7.36%).
- MINOR: same 2025 open-year note.
Verdict: PASS

## wakulla-county-fl
- Data (12129) matches: 305 claims, 1.6%, 1.0% (111,678 / 10,653,540 = 1.05%).
- MINOR: 5 outside claims only; same as Levy. Same 2025 open-year note.
Verdict: PASS

## flood-zones
- MAJOR (zone X): "Shaded zone X ... so its mapped chance of flooding is under 1 percent" is an inference the quoted source does not make. The FEMA glossary sentence only says shaded X is "the areas between the limits of the base flood and the 0.2-percent-annual-chance flood". Modern FEMA maps also put some 1-percent-chance areas (shallow flooding under 1 foot, small drainage areas, levee-protected) in shaded X, and that is not quoted in the registry. The "so ... under 1 percent ... under 26%" chain is therefore beyond the quoted text. Fix: say "between the 1 percent and 0.2 percent flood: about 5.8% to 26% over 30 years at those two limits", drop "so", and keep the sentence to what the glossary says, or add a raw FEMA source that supports the shallow-flooding and levee groups.
- MINOR: "under 26%" and "under 5.8%" are strict. At exactly 1% the 30-year chance is 26.03%, and just under 1% a year can exceed 26.0%; likewise just under 0.2% a year gives 5.8%. Fix: "under about 26%" or "up to 26%"; "under about 5.8%".
- PASS (zone AE): floodway text matches 44 CFR 59.1 (channel and adjacent land areas reserved to discharge the base flood) and 60.3(d) (prohibit encroachments incl. fill, new construction, substantial improvements and other development in the adopted floodway unless hydrologic and hydraulic analysis shows no increase in base-flood levels, or the community first applies for a conditional FIRM and floodway revision). Scope "Where a community has adopted one" is kept. MINOR: "first applies for a map and floodway revision" omits that the revision must follow 44 CFR 65.12; harmless but could cite it.
- FIXED (Claude, 11-09): rule odds_30_x deleted from the zone X page, the registry, test_calc and manual-rule-read; the shaded-X definition stays as FEMA wrote it. Nothing new printed, so no re-review needed.
Verdict: PASS
