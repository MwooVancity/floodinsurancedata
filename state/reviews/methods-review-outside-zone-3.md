# Methods review: Outside the Zone, round 3 (hostile statistician, 2026-11-13)

Inputs read: dist/flood-insurance/outside-the-zone/index.html (whole page), dist/data/outside-the-zone.csv (364 rows),
tools/papers.py (spec, rows, wilson, context, pooled_boot, excluded), tools/build_site.py 975-1035 (paper builder),
tools/extras_raw.py claims() (zone accumulator, events), tools/ffcalc.py aggregate_policies (sfha_share_units),
tools/rules_registry.py fema_outside_third, data/all-counties/*.json (3,027 files), docs/PAPER-GATE-PROMPT.md,
round 2 review. FloodSmart "What is my flood risk" page read live this session (curl).
Scripts (python -I, scratchpad): otz3.py (recompute, CSV compare, 3 independent cluster bootstraps B=5,000, left-out
counties, policy-share stats, event flag, ties), otz3b.py (event-list cap, window straddle, blank-zone bound).

Severity: BLOCKER = wrong or misleading on the page; MAJOR = a referee would reject; MINOR.

## Recompute

- All 364 rows: fifth, share, 90% Wilson range, numerator, denominator match the CSV, 0 mismatches.
- Pooled 109,947 / 424,932 = 25.87% (page 25.9%); median county 25.55% (page 25.6%).
- Montgomery MD 97.0% (93.5-98.7), 130 of 134, unique top value; Holt MO 0 of 246, unique 0.0% row. Correct.
- New policy column (100 - policies.sfha_share_units): present for 364 of 364. Unknown-zone policy units are 0 in every
  ranked county, so "outside A and V" on policies is not inflated by blank zones. First 10 rows match the page
  (92.2, 61.6, 89.7, 75.1, 57.2, 77.0, 62.5, 44.8, 83.7, 60.3).
- New largest-named-flood column: first 10 rows match context() (Ida 15, Hanna 91, Harvey 633, Ophelia 2, ...).
- Cluster bootstrap (resample counties): page 19.0-32.7. Independent seeds, B=5,000: 19.0-33.0, 19.0-32.7, 19.2-32.5.
  Reproduces within Monte Carlo error.
- Left-out counties: 2,042, median 33.33%, pooled 34.72% (12,593 of 36,265). Page 33.3% / 34.7%. All-US pooled 26.57%.
- "One named flood had more paid claims (all zones) than half the county's base": 168 of 364. Reproduces.
- "19 of the 50 ... in Texas": 19 reproduces (TX is 32 of 364 ranked; 21 of 73 in the top fifth).
- FEMA figure: FloodSmart live text reads "29%" beside "Over the past 10 years (2014 - 2024), nearly one-third of NFIP
  flood insurance claims came from areas located outside of current high-risk flood areas". The page's wording matches.
- Causal and banned words: because / due to / driven / caused / significant / best / worst / safest: 0. Page is noindex.

## Round 2 MAJORs: point by point

| Round 2 | Status | Evidence |
|---|---|---|
| M1 policy share not shown | Resolved (MINOR left) | Column on every row, labelled "Policy units outside A and V today"; lede says the share "mostly follows" it. r = 0.70, median claim/policy ratio 0.72, claim share above policy share in 96 of 364 - none printed (m1). Time mismatch not stated (m2). |
| M2 pooled interval | Resolved | County-cluster bootstrap replaces the binomial range; reproduces. County Wilson limitation line still missing (m3). |
| M3 selection | Resolved | Median 33.3% and pooled 34.7% of left-out counties printed in Methods and Results. |
| M4 one flood dominates | Partly | Count (168) and per-row event printed. "Largest" not verifiable for most rows (MAJOR 1); no per-row flag; CSV lacks the column (m4). |
| M5 reproducibility | Mostly resolved (MINOR left) | Paid sum, 98/99 codes, countyCode now stated. Flow counts, zone normalisation, loss-year rule, out-of-state countyCode drop, bootstrap seed, commit still missing (m5). |
| M6 prior work / FEMA figure | Partly | FEMA's figure added and verified, Penn State linked. The two figures are set side by side with no base reconciliation (MAJOR 2). |

## BLOCKER

None. Every printed number reproduces from the raw county files and the live FEMA page.

## MAJOR

**MAJOR 1 - "Largest named flood in these years" is a label the data cannot prove for most rows.**
context() takes the max-claims event from extras.claims.events, but that list is the county's top 8 named events by
DOLLARS, all years. In 241 of 364 ranked counties the list is full (8) and older floods (1993 Midwest, Ike 2008,
"Flooding" 1982-1998) take slots, so an in-window flood with more paid claims but fewer dollars than the 8th entry is
invisible: the shown "largest" may not be the largest, and 168 is only a lower bound. Second hole: an event whose paid
claims span the window edge is dropped entirely. "Early winter storms" (Dec 2015 - Jan 2016, loss years 2015 and 2016) is
dropped in 10 ranked counties, among them Jefferson MO 29099 (184 claims; the row shows Late spring severe storms 2017:
175), Franklin MO 29071 (190 vs 148 shown), St. Louis County MO 29189 (257), St. Charles MO 29183 (174). Project rule:
label-vs-data is MAJOR.
Fix: in extras_raw.claims() keep, per named event, paid claims inside LOSS_FROM..LOSS_TO (all events, not top 8 by
dollars); pick the largest from that; count only in-window claims of straddling events. Add a factory case for a
straddling event and a capped list.

**MAJOR 2 - FEMA's 29% is set beside 25.9% with no statement of how the bases differ (R0.1 "reconcile").**
Lede and Prior work print 25.9% then "FEMA's own figure ... nearly one-third (29%)". A reader takes 25.9 vs 29 as a
disagreement or as the same number. They are different measures: FEMA = all NFIP claims (paid or not, as worded),
national, 2014-2024, zone on CURRENT maps; paper = paid claims with a RATED zone, 364 counties with 100+, 2016-2025.
The repo has two bridges and prints neither: all-US pooled share on this base is 26.6%; of claims rated outside A/V in
ranked counties, 9.1% are A/V on floodZoneCurrent (round 2 m3) - map change moves the figure in both directions, so the
direction of the gap is not knowable from the rated zone alone. Penn State is linked with no figure or base.
Fix: one Prior work sentence: "FEMA's 29% counts all NFIP claims nationally in 2014-2024 by current maps; this paper
counts paid claims by the zone rated on the claim, 2016-2025, in counties with 100+ (all U.S. counties on this base:
26.6%). The two are not the same measure." Move the FEMA line out of the lede or keep it there only with that sentence.
Give Penn State's figure and base, or drop the link.

## MINOR

**m1 - "Mostly follows" is a quantity with no number.** r = 0.70 (r-squared 0.49), median claim share / policy share 0.72,
claim share above policy share in 96 of 364. Fix: print r and the 96-of-364 count in Results; say "tracks" not "mostly".

**m2 - Policy column timing and base.** "today" = policies in force at the Policies v3 as-of date (not printed), claims are
2016-2025 losses; policy units count every occupancy. Fix: header "Policy units outside A and V (in force, as of <date>)",
one Limitations line on the time mismatch.

**m3 - County Wilson ranges assume independent claims.** Methods itself says claims in one county are not independent,
then applies Wilson per county. Ascension LA: one 2016 storm is 3,528 of 3,867 base claims. Fix: Limitations line
"County ranges treat claims as independent and are too narrow where one flood dominates (see the flood column)."

**m4 - New columns are not in the CSV.** Policy share and largest flood appear in the table only; the CSV header list on
the page omits them; no per-row one-flood flag (gate M1.8 "the row says so"). Fix: add pol_out_pct, flood_name,
flood_paid_claims, one_flood_over_half to the CSV and a marker in the table.

**m5 - Reproduce still incomplete.** Missing: ratedFloodZone trimmed and upper-cased; loss year = first 4 characters of
yearOfLoss; claims whose countyCode is outside the state file dropped; filter flow counts (pulled -> window -> not 98/99
-> paid -> zoned -> listed); bootstrap seed 20261113 and percentile method; code commit. Reproduce section omits the
bootstrap. Fix: numbered filter list with counts plus commit hash.

**m6 - Event comparison label.** Event paid claims include claims with no rated zone; the base excludes them. Building
type and 98/99 are handled the same on both sides (base is every building type; both drop 98/99; same paid rule), so the
comparison is fair except for blanks: at most 6 of 168 flags could flip if every blank-zone claim were in the event
(e.g. Newton TX 48351, 239 vs base 278, 105 blank). Also the flag compares the flood to the denominator, not to the
outside numerator the share is about. Fix: label "(including claims with no rated zone)"; once events carry a zone split,
flag on the numerator too.

**m7 - What the pooled range describes.** Resampling the 364 listed counties gives a range for counties like these, not
for all counties: the left-out pool (34.7%) falls outside it. Fix: "(90% range 19.0-32.7% if the listed counties were
drawn again)" or a Methods line saying the same.

**m8 - Carried from round 2:** top-50 Texas count with no base rate (expected 4.4 of 50; say "19 of 50; Texas is 32 of
364 listed counties, most of its top rows Harvey 2017"); fifth-boundary tie Perry 21193 and Fond du Lac 55039 both 10.3%
in different fifths, unnamed; claim-county caveat ("can differ from the property's county") still missing from this
spec's limits; rated-vs-current 9.1% not printed; versioned permalink /outside-the-zone/2026-08-31/ absent (M2.5).

## Verdict

**MAJOR REVISION.** Arithmetic is clean on all 364 rows and the new bootstrap, policy, left-out and event figures all
reproduce; four of six round 2 MAJORs are resolved or reduced to MINOR. It does not ship: the "largest named flood"
column is drawn from a top-8-by-dollars list that hides in-window floods and drops window-straddling ones (MAJOR 1), and
FEMA's 29% sits beside 25.9% with no statement that the base, years, paid rule and map differ (MAJOR 2). Both are small
fixes; with them and m1-m4 this would be MINOR REVISION.
