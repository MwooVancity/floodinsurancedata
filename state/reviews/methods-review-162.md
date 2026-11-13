# Methods review 162: Price Gap Index and Outside the Zone (hostile peer review, 2026-11-12)

Reviewer stance: statistician / actuary / FEMA-data referee. Inputs read: built pages (text extracted at start of session; both
`dist/flood-insurance/price-gap/` and `outside-the-zone/` were then deleted from dist by a concurrent build, so the HTML-side spot
check below ran on the earlier extraction for the top rows only), `dist/data/price-gap.csv` (1,029 rows), `dist/data/outside-the-zone.csv`
(1,152 rows), `tools/papers.py`, `tools/ffcalc.py` (`premium_gap`, `is_sf_home`), `tools/agg_raw.py` (`claims_extra`, lines 60-101),
`tools/pull_raw.py` (in-force filter), `data/all-counties/*.json` (3,027 files). Raw `.cache/raw/` is not on this laptop, so per-record
claims were not re-tested. Analysis script: scratchpad `rev.py` (binomial bootstrap B=300, Wilson CIs, selection split).

Severity: BLOCKER = wrong or misleading on the page; MAJOR = a referee would reject; MINOR.

## Data integrity (point 8): passes
- CSV vs `data/all-counties` JSON: 13 rows per paper (10 random, seed 1, plus top 3): 0 mismatches in value or n.
  Top rows on the page (extracted text) match the CSV (Wyoming WV 93.9% n=148; Benson ND 98.5% n=208).
- Median 36.2 / 24.6, ">50%" counts 233 / 119, pool 1,029 / 1,152 all reproduce from the CSV.
- Encoding: "Doña Ana" is correct UTF-8 in the CSV (the garbling seen was the terminal).

## BLOCKER

**B1 — Outside the Zone — "the lowest is Saline County, NE at 0.0%" is a tie, stated as a unique result.**
Evidence: CSV last rows `1151, Holt County, MO, tied=True` and `1151, Saline County, NE, tied=True`, both 0.0%. The page's own table
says "(tied)"; the abstract does not. Label-vs-data, the site's own MAJOR-minimum class.
Fix: abstract names every county at the extreme value ("the lowest, at 0.0%, are Holt County, MO and Saline County, NE"), or "N counties at 0.0%".
Add a factory case: extreme value tied (top and bottom) for every paper.

**B2 — Outside the Zone — n is not the base of the share, and the minimum guards the wrong count.**
The measure is dollars on paid claims *with a rated zone* (`zoned_total`); `n` and the minimum use `paid_n` = all paid claims, zoned or not
(`agg_raw.claims_extra`). So a county can qualify with 100 paid claims of which only a handful carry a zone, and the share then rests on those few.
The abstract's "1,152 counties with at least 100 NFIP claims with a recorded payment each, 2,004,117 in all" presents that count as the base.
Second, the measure is a *dollar* share but n is a *claim count*: dollar shares are dominated by a few large claims, so even the right count
overstates precision. Third, the table's "Claims with a payment" column is identical to `n` in 1,152 of 1,152 rows (padding, two labels on one number).
Fix: store `zoned_n` and `zoned_dollars`; apply the minimum to `zoned_n`; print n as "paid claims with a rated zone"; drop the duplicate column;
print the zoned/unzoned split; add effective sample size (Σw)²/Σw² over claim dollars, or a cluster bootstrap by flood event, as the precision measure.

**B3 — Outside the Zone — title and abstract claim geography the data cannot give.**
"Flood Claim Dollars Paid Outside High-Risk Areas" says where the house is. The field is `ratedFloodZone`, the zone used to *rate the policy at
the time of loss*, pooled over 1978-2026 across many FIRM revisions, legacy grandfathering, and pre-map Emergency Program years. The rule
"not starting with A or V" puts zone D (undetermined risk, not low risk), legacy B/C, and any malformed code on the "outside" side; AR/A99
(levee residual risk) go "inside". A 1985 claim rated C in a parish since remapped to AE counts as "outside high-risk". The limits line
("can differ from today's map") does not cure a title that says the opposite.
Evidence: zone value set never enumerated on the page; Wyoming WV policies already carry legacy zone "C" (`zone_units`), so legacy codes are live in this data.
Fix: retitle to "rated outside A and V zones at the time of the claim"; enumerate every zone value and which side it falls; report D and blank separately;
add a post-2009 (or post-current-FIRM-effective-date) sensitivity column; better, split by decade.

## MAJOR

**M1 — Both — ranks are presented with false precision; bands, not ranks.**
Binomial bootstrap 90% rank intervals (Price Gap, count share, which is the right model there):

| Rank | County | Share | n | 95% CI | rank 90% interval |
|---|---|---|---|---|---|
| 1 | Wyoming WV | 93.9 | 148 | 88.8-96.8 | 1-2 |
| 5 | Boone WV | 88.3 | 111 | 81.0-93.0 | 2-18 |
| 11 | Bell KY | 86.2 | 145 | 79.6-90.9 | 3-23 |
| 12 | Camden MO | 86.0 | 100 | 77.9-91.5 | 3-26 |
| 3 | Plaquemines LA | 89.5 | 2,733 | 88.3-90.6 | 3-7 |
| 20 | Collier FL | 82.2 | 31,301 | 81.8-82.6 | 18-23 |

At n=100 the 95% CI half-width is up to ±10 points; the table separates counties 0.1 point apart. 773 of 1,029 Price Gap rows and 938 of 1,152
Outside the Zone rows share a rank; 10 of the top 20 in each paper have n<300. For Outside the Zone the binomial model *understates* noise (dollar-weighted,
event-clustered), so its apparently tight intervals (Benson 1-1) are not credible.
Fix: replace rank with tiers (e.g. ≥80%, 60-80, 40-60, 20-40, <20) or print a 95% CI and rank interval per row; set the minimum by a precision target
(CI half-width ≤5 points at p=0.5 needs n≈385; ≤3 points needs n≈1,070), or shrink small counties toward the state mean (empirical Bayes) before ranking.

**M2 — Price Gap — "below full-risk" counts any shortfall over $0, so the index mixes $1 and $3,000 gaps.**
71 ranked counties have a median per-policy gap (among policies below) under $50/yr (Sacramento CA 27.0% share, median gap $36; Fond du Lac WI $33;
El Paso TX $38); top counties sit at $1,766-$3,362. Neptune Flood's national figure uses "more than $10 per year below". Bottom rows show median
premium = median full-risk premium (Concordia $302/$302, Catahoula $273/$274): the index is sensitive to rounding and minimum-premium effects at the margin.
Fix: state and justify a materiality threshold (≥$10, or ≥5% of full-risk); show the share and the median gap side by side; sensitivity table at $0/$10/$100.

**M3 — Price Gap — the definition of `fullRiskPremium` relative to `totalInsurancePremiumOfThePolicy` is not established on the page.**
The page asserts both are "premiums only, before fees and surcharges" but quotes no FEMA data-dictionary text for `fullRiskPremium`. Unresolved:
is the CRS discount inside or outside full-risk? Is the ICC premium in one and not the other? Are short-term / mid-term-endorsement premiums prorated
in one and not the other? If CRS sits outside full-risk, every policy in a CRS community reads "below" and the index partly measures CRS class
(Collier, Lee, Monroe, Charlotte FL are strong CRS communities and all rank high). I found no source settling it in this review.
Fix: quote the OpenFemaDataSetFields definition of both fields (read this session); run share_below by `crsClassCode` (already pulled, `POL_STR`)
and by `preFIRMConstructionIndicator`; if CRS class predicts share with no premium change, the measure is confounded and must be redefined.

**M4 — Price Gap — counts records, not `policyCount`, against the site's own data rule.**
`premium_gap` counts rows; CLAUDE.md data trap: "SUM policyCount, never count rows". 540 counties have rows ≠ units overall. For single-family
non-condo policies policyCount should be 1, but that is not tested. Also untested: whether one policy term can appear as more than one record (endorsements).
Fix: assert policyCount == 1 for every cohort row (gate), and assert one row per policy id per term, or weight by policyCount.

**M5 — Both — selection bias in the headline median and ">50%" counts.**
Counties with a value but below the minimum: Outside the Zone excluded median 33.6% vs included 24.6% (9 points); share >50% among excluded 35.1% vs 10.3%
included. Price Gap: excluded median 37.8% vs 36.2%; >50% among excluded 30.7% vs 22.6%. Small-n counties are systematically different (rural, riverine,
event-driven), so "the median county" is "the median qualifying county", a population defined by NFIP volume.
Also the unweighted county median (Price Gap 36.2%) is not the national figure: the pooled policy share is 43.7% (2,263,483 ranked policies; same 43.7%
across all 2,320,347). A reader reads "median county 36.2%" as "about a third of policies"; the true policy share is 44%.
Fix: abstract states the pooled national share alongside the county median, and states what the minimum excludes and how its median differs.

**M6 — Outside the Zone — single events drive the ranking; nominal dollars over 48 years.**
Ward County ND (rank 2, 94.9%): 96% of all its claim dollars are from 2011 (Souris River / Minot). Monroe IL (0.5%): 97% from 1993. Saline NE: 70% from
2015. Arlington VA: 59% from 2019. The rank measures "did this county's biggest flood overtop the mapped floodplain", not a stable property of the county.
Nominal dollars weight recent events heavily (a 1983 dollar ≈ 3 of today's).
Fix: CPI-adjust (or share of claims as a co-measure); report the largest single event's share of the county's dollars per row; flag rows where one year is >50% of dollars.

**M7 — Outside the Zone — county assignment differs across the two papers and is a known FEMA trap.**
Policies are assigned by `censusGeoid` (property location); claims by `countyCode`, which the site's own rules say "may not match the property county".
"The county FEMA codes on the record" hides that the two papers use different geographies.
Fix: say which field per paper; quantify the countyCode vs censusGeoid mismatch where both exist (claims v3 has censusTract/latitude-longitude); use the property field if available.

**M8 — Both — methods section is not reproducible.**
Missing: exact API filter (`policyEffectiveDate le ASOF and policyTerminationDate gt ASOF`), occupancyType values (1, 11), primaryResidenceIndicator
values, condominiumCoverageTypeCode values kept (N, blank) and dropped (U/A/H/L); that the 98/99 exclusion uses `nonPaymentReasonBuilding` only; the zone
classification rule and value list; "paid" = building + contents + ICC net > 0 (negative nets?); pull date vs "as of" (as-of is set to the end of the month
3 months before the pull, not FEMA's own data date); a flow table (records pulled → in cohort → priced → in ranked counties); code location and version.
"Fields used" lists `nonPaymentReasonBuilding` but never says how.
Fix: a numbered filter list with field = value, record counts at each step, pull timestamp, and a link to the code/commit.

**M9 — Price Gap — not original; must cite and reconcile prior work.**
Neptune Flood Research Group ("The $2.6+ Billion That Remains", five years into Risk Rating 2.0) publishes the share of NFIP policies below full-risk
nationally (44%), by state (WV 67.0%) and for counties (Collier 76.8%); GAO-23-105977 has an interactive county data tool on full-risk premiums.
This paper's Collier figure is 82.2% (different base: SF primary homes, strict < $0): a referee will ask why they differ. Outside the Zone is less covered
(RFF/Wharton map *policies* outside the SFHA by county; Penn State maps PA county ratios of non-SFHA claim dollars; Scientific American / CRS give national claim shares),
so a national county ranking of claim dollars appears new, but the computation is a one-line ratio, not a method.
Fix: a "Prior work" paragraph citing these, and a reconciliation line for Collier (base, threshold, date).

## MINOR

**m1 — Both — rounding before ranking.** Values are stored rounded to 0.1 in the county JSON and ties are formed on the rounded value, so ties are
rounding artifacts; harmless only because ranks should not be shown (M1).

**m2 — Price Gap — "9 of the 50 highest-ranked counties are in Louisiana" has no base rate.** LA is 51 of 1,029 ranked counties (expected 2.5 of 50);
WV 7 vs 0.7 expected, KY 6 vs 1.1. Same for Outside the Zone "15 of the 50 are in Texas" (87 of 1,152, expected 3.8). The clustering is real; say so with the expectation.

**m3 — Price Gap — implied mechanism.** The cap and glide-path quotes beside the ranking invite "these counties are below because of the cap".
The data cannot separate cap glide, pre-FIRM, newly-mapped, Emergency Program, and tenure (Neptune: 22-27% subsidized under 5 years tenure, 54-59% above).
No causal sentence is printed; keep it that way and add "the data does not say which discount applies".

**m4 — Both — "No statistical test is run" is stated but the page still ranks and compares.** Either give uncertainty (M1) or drop the ordinal claims.

**m5 — Price Gap — n label.** CSV column `n` is `below_n`, which is actually the priced-cohort count (`frp_n`), not the number below. Correct on the page, misleading field name in code.

## Verdicts
- **Price Gap Index: MAJOR REVISION.** Numbers reproduce, but the measure's definition (M3), materiality (M2), row-vs-policy count (M4) and rank precision (M1) are unestablished, and it is not original (M9).
- **Outside the Zone: REJECT in current form.** The base, the n and the minimum disagree (B2), the title asserts present-day geography the rated-zone field cannot give (B3), the abstract misstates a tie (B1), and single floods drive the ranks (M6). Resubmit after a zoned-n base, retitle, decade split, CPI adjustment, and tiers.

Sources: [Neptune Flood: The $2.6+ Billion That Remains](https://neptuneflood.com/?p=8505); [InsuranceNewsNet on Neptune analysis](https://insurancenewsnet.com/oarticle/2-6-billion-in-nfip-subsidies-remain-five-years-into-risk-rating-2-0-neptune-flood-research-group-analysis-of-fema-data-shows);
[GAO-23-105977 interactive](https://files.gao.gov/multimedia/gao-23-105977/interactive/index.html); [RFF: demand outside the 100-year floodplain](https://rff.org/publications/issue-briefs/perspectives-on-flood-insurance-demand-outside-the-100-year-floodplain);
[Penn State NFIP insights PA](https://www.psirc.psu.edu/assets/NFIP_Insights_for_PA.one-pager.2022-09-05.pdf); [CRS IN10890](https://www.everycrsreport.com/reports/IN10890.html).
