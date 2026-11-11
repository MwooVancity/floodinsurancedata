# Hater round 132 (light, text only; changed parts)

Checked against data\c\<slug>\{agg,extras}.json, data\states\louisiana\agg.json, data\all-counties\*.json, dist\data\claims-by-county.csv, maapnext.org and Texas Property Code 92.0135 (live text).

## home
- MINOR Footer says "2,680,429 claim records" while /claims/ by-county card counts 2,567,024 claims on record (excludes "deleted/assigned in error"); the home note does not say it counts those records, so the two totals differ without explanation.
- Nothing from the changed parts is broken here: tile label, no opening sentence, no stray fragments.
Verdict: PASS

## louisiana
- PASS "Cost in my zone?" "Zones X $1,082, AE $1,259 ...; more zones below." True: agg cost_by_zone prices 25 zones.
- PASS median tile label carries base and as-of (August 31, 2026); "5% above the U.S. median" = 1114/1066 = 4.5%.
- PASS payout note wording matches /claims/ exclusion wording.
- MINOR Data retrieved date prints "November 11, 2026" although the review date is Nov 10 (clock/time-zone); a reader sees a date in the future.
Verdict: PASS

## palm-beach-county-fl
- PASS "more zones below": X, AE shown; AO, AH, C, B, VE also priced (n >= 100).
- PASS decade line: 2020s n=330 (>=30), 44.8% paid; all-years 46.8% recomputed from by_decade (46.76).
- PASS comparison 32% below FL median (673/985), 37% below U.S.
- MINOR retrieved date November 11 is after today (see louisiana).
Verdict: PASS

## new-york-county-ny
- PASS "Zone X $953 ...; Zone AE, 41.8% of policy units, has too few to price": only X priced; no false "more zones below" (guard works).
- PASS 63.9% all years recomputed from by_decade (63.9); 2020s 152 claims 63.2%.
- PASS "4% below the U.S. median": 1021/1066 = 0.958.
- MINOR the median tile is basis-labelled, but the removed opening sentence also carried the "Manhattan" name; h1 still has it, so no loss.
Verdict: PASS

## claims
- PASS New card "NFIP claims by county, 1978–2026": recomputed from all 2,905 data\all-counties claims.rows / total_paid; top 25 order and every claim count and dollar figure match (Harris 165,626 / $8,730,916,333 ... Jackson MS 11,113 / $706,938,735); 26th is Kings NY $692.5M, correctly out. Ranked by paid, label says "most paid first". 2,905 matches; CSV has 2,905 rows, sorted by paid, 51 states incl. DC.
- PASS Card note states base (claims on record excl. deleted/assigned in error; paid = building plus contents, ICC not in it, nominal dollars, county as coded, 2025-26 not final). Harris 165,626 equals Harris county page.
- PASS Cause card note "other causes (alluvial fan, closed basin lake, erosion, earth movement, other) are not shown" is consistent with the rows shown.
- MINOR "Left out: counties with 1 to 499 such claims (2,296 counties)" and "(2,101 counties)" differ between cards; each is its own base, but a reader scanning may see two different "left out" counts with no sentence saying why.
- GAP Ranking is by dollars, not by dollars per policy or per claim, so big-population counties dominate; the card says "most paid" only, which is accurate.
Verdict: PASS

## renters
- MINOR Texas sentence lists one exemption ("Leases shorter than 30 days are exempt"). Statute 92.0135(a-1) also exempts temporary tenancies from a sale contract of 90 days or less, and (c) lets a landlord skip disclosing floodplain awareness when the dwelling is raised above 100-year levels. The sentence reads as the whole exemption list. Still true as written; wording "one exemption" or "among the exemptions" would match the source.
- PASS Strength and scope: statute says "shall provide ... written notice"; page says "must give"; five-year look-back for the flooding notice matches (d) ("at least once during the five-year period immediately preceding the effective date of the lease").
- GAP "100-year floodplain" is not explained (statute: FEMA flood hazard area, 1% yearly chance); the tenant's right to end the lease within 30 days after a large flood loss (f) when the landlord broke this section is not mentioned.
Verdict: PASS

## harris-county-tx
- PASS MAAPnext sentence vs maapnext.org: site says maps are draft, "not final, cannot be used for insurance or regulatory decisions", FEMA "anticipated to release Preliminary FIRMs after ... federal review". Page paraphrase ("expected") keeps the strength. Attributing the site to the flood control district is not on the home page text fetched (it says "Harris County MAAPNext"); plausible, unproven here.
- PASS "within one percent of the Texas median of $1,083": 1087 vs 1083 = 0.37%, values differ.
- PASS "more zones below": A, AO, VE, B also priced; decade line prints plain (2020s n=2,810).
- PASS payout note and decade table sum to 165,626 claims.
- PASS map-service source line has one retrieved date (November 9, 2026).
- MINOR retrieved November 11 is after today (clock).
Verdict: PASS

## greene-county-ar
- PASS Decade sentence: 2000s (n=63, 71.4%) is the latest decade with >= 30 claims; 2010s 27 and 2020s 11 are named "too few for a share"; the lower table lists 1990s and 2000s and the too-few decades with counts. All match extras by_decade; all-years 73.0% recomputed.
- PASS Cost line shows no "more zones below" since only AO and AE are priced; Zone A "21.5% of policy units" = 76/353 correct.
- MINOR Phone: the 3-clause decade sentence is long for screen 1 and spells "thirty" while the rest uses digits.
- MINOR Page shows no "outside high-risk zones" 2016–2025 note (too few claims), so nothing to check for the under-30 count variant on this page.
Verdict: PASS

## brevard-county-fl
- PASS "Zones X $913, A $627, AE $1,182 ...; more zones below": VE ($1,542, n=180) and AH ($663, n=136) are also priced.
- PASS all-years 54.0% recomputed (54.06); 2020s 59.1% n=345.
- PASS comparison "12% below FL median $985, 19% below U.S." correct.
- PASS outside-zones note: 1,355 claims, 60.4% / 56.2%, basis and years stated.
Verdict: PASS

## Classes
- Retrieved dates one day after the review date (Nov 11 vs Nov 10): every page; confirm it is a UTC/time-zone artefact.
- No label-vs-data defect found in the changed parts; "more zones below" and the decade variants follow the data in all six checked pages.
