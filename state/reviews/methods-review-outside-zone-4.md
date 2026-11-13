# Methods review: Outside the Zone, round 4 (hostile statistician, 2026-11-13)

Inputs read: dist/flood-insurance/outside-the-zone/index.html (whole page, text), dist/data/outside-the-zone.csv (364 rows),
tools/papers.py (whole), tools/build_site.py 1015-1016 (lede + FEMA sentence), tools/rules_registry.py fema_outside_third,
data/all-counties/*.json (3,027 files), dist/flood-insurance/harris-county-tx/index.html (paper card), docs/PAPER-GATE-PROMPT.md,
round 3 review. Script (python -I, scratchpad): otz4.py (independent recompute; own Pearson and Spearman; CSV policy column).

Severity: BLOCKER = wrong or misleading on the page; MAJOR = a referee would reject (project rule: label-vs-data is MAJOR); MINOR.

## Recompute

- Every-county figure: 122,540 / 461,197 = 26.57% (page 26.6% of 461,197). 2,406 counties with at least one record.
  461,197 = 424,932 (ranked) + 36,265 (left out): consistent with round 3.
- Correlation of claim share and policy-unit share outside A and V, 364 counties: Pearson 0.7016 (page 0.70);
  Spearman 0.698, so the figure is not driven by a few extreme rows. Claim share above policy share in 96 of 364.
- CSV policy_units_outside_a_v_pct matches 100 - policies.sfha_share_units for 364 of 364, 0 mismatches.
- Pooled 25.9%, bootstrap 19.0-32.7%, median 25.6%, extremes, 2,042 left out (33.3% / 34.7%), "19 of the 50 ... Texas":
  unchanged from round 3, which reproduced them.
- Banned/causal words on the page (because, due to, driven, significant, mostly, largest, named flood): 0. robots noindex,follow.
- Harris County card: 49.8% (49.4-50.1%) of 55,323, highest fifth of 364: matches the CSV row.

## Round 3 MAJORs: point by point

| Round 3 | Status | Evidence |
|---|---|---|
| M1 "largest named flood" column | Resolved | Column, context() event output on the page, and the "one named flood" results sentence are gone (0 hits for "largest", "named flood"). context() still computes the event, now unused (m4). |
| M2 FEMA 29% vs 25.9% bases | Partly | Lede now leads with 26.6% of 461,197 on the paper's base (reproduces) and adds a base sentence. But that sentence states a fact about FEMA's base the source does not give (MAJOR 1). |
| m1 "mostly follows" | Resolved | "go together (correlation 0.70, descriptive, no test)"; reproduces. |
| m2 policy column date | Partly | Header names "FEMA NFIP Policies, August 31, 2026"; no Limitations line on policies-in-force vs 2016-2025 losses (m2). |

## BLOCKER

None. Every printed number reproduces from the raw county files.

## MAJOR

**MAJOR 1 - "FEMA counts all claims against current maps for 2014-2024" says more than FEMA's text.**
Evidence: the only source (rules_registry fema_outside_third, FloodSmart raw read) says "nearly one-third of NFIP flood
insurance claims came from areas located outside of current high-risk flood areas". It does not say whether the count is all
claims or paid claims, closed or open, or national. "All claims" is an inference - the project's rule is "every sentence quoted,
inference cut", and the round 3 review's suggested wording ("counts all NFIP claims") made the same error; this round corrects
it. The sentence is also typed into the template (build_site.py:1016: "all claims", "2014-2024" hard-coded, not from rule()),
and it is emitted once for EVERY key in prior_rules, so any future prior rule on any paper would print this FEMA base
sentence beside an unrelated source.
Fix: say only what both sources support, e.g. "FEMA's figure places claims on current maps for 2014-2024 and does not say
whether it counts only paid claims; this page counts paid claims by the zone rated on each claim for 2016-2025. The two are not
the same measure." Move the sentence into the rule's registry entry (or a per-paper spec field) so it is not attached to every
prior rule, and take the years from the rule source, not the template.

## MINOR

**m1 - "in every U.S. county" overstates the base slightly.** The 461,197 are claims whose FEMA countyCode maps to one of the
3,027 county files; claims with a blank or unmatched countyCode are not in it. Fix: "in every county FEMA codes on the claim"
(the Methods wording) or print the dropped count.

**m2 - Policy column time base.** Policy units are those in force at the Policies v3 as-of date; claims are 2016-2025 losses,
and units count every occupancy. No Limitations line says so (carried from round 3 m2). Fix: one Limitations line.

**m3 - Penn State link with no figure or base** (carried from round 3 M2 fix text). Fix: give its figure and base, or drop it.

**m4 - Dead code.** papers.context() still computes the event field the page no longer prints. Fix: delete the event part so a
future template cannot revive the unverifiable label (round 3 M1).

**m5 - County card has no loss window.** Harris card prints "49.8% ... of 55,323 claims with a payment and a rated zone here"
with no "losses 2016-2025"; the county page shows other claim counts on other windows. Fix: add the window to the card sentence.

**m6 - Reproducibility items from round 3 m5** (flow counts, zone normalisation, loss-year rule, countyCode drop count,
bootstrap seed, commit) are still not in Reproduce. Fix as round 3.

## Verdict

MAJOR REVISION. One MAJOR: a one-sentence fix (cut the unsupported "all claims" and move the sentence out of the shared
template). Both round 3 MAJORs' numbers reproduce (26.6% of 461,197; r = 0.70). With MAJOR 1 fixed and nothing else
changed, the next round should be ACCEPT or MINOR REVISION.
