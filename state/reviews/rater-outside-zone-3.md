# Rater review 3: /flood-insurance/outside-the-zone/ (local build, noindex) - 2026-11-13

Rater stance: Search Quality Rater Guidelines, YMYL (financial / insurance), final re-rating, strict. Files read: dist/flood-insurance/outside-the-zone/index.html, dist/about/index.html, dist/data/outside-the-zone.csv; live https://floodinsurancedata.com/about/ (publisher name present). Previous: rater-outside-zone-2.md (Medium). Nothing edited.

Checks run by the rater: correlation recomputed from the 364 table rows (claim share vs policy-unit share) = 0.702, matches "0.70". Every-county figure cross-checked: 25.9% of 424,932 plus 34.7% of the 36,265 left-out claims = about 122,600 of 461,197 = 26.6%, consistent. CSV has 364 rows plus header and now carries policy_units_outside_a_v_pct. FloodSmart wording not re-read by the rater (commit cc131f65a says it was re-read today).

## 1. Needs Met
- "flood claims outside flood zone by county": Highly Meets (unchanged). Every county row has share, range, count and the policy-unit share, all in the CSV. Not Fully: no state jump on a 364-row table on a phone; policy-unit column base not defined (see MAJOR 2).
- "do floods happen outside high risk flood zones": Moderately Meets, upper end, close to Highly. The lede now opens with the every-county figure (26.6% of 461,197) and FEMA's 29% with a link and the base difference. Held back: still analyst phrasing, no plain "Yes, about 1 in 4 paid claims"; nothing for the zone X owner who asked (not required by lenders, still available, 30-day wait), although the site has those pages.

## 2. Page Quality: Medium+ (up from Medium; not High)

## 3. Previous reasons: status
1. No named owner: PARTLY RESOLVED. About names Michael Woo, contact email, ads, AI use. No stated experience, role or qualification, and no named human reviewer of the method. See MAJOR 1.
2. Policy and named-flood columns without source/date, not in CSV, mixed bases: MOSTLY RESOLVED. Header names "FEMA NFIP Policies, August 31, 2026"; CSV carries the column; the named-flood column and the mixed-base sentence are gone. Left: the Data section still lists only Claims v3; the policy column's base (policies in force on that date? units? zone field? current map vs claim-time rating) is not stated. See MAJOR 2.
3. FEMA 29% unlinked and twice: RESOLVED. Printed once, FloodSmart linked, base difference stated in one sentence.
4. Headline was the 364-county figure: RESOLVED. Lede leads with the all-county 26.6%, then 25.9% with a county-resampled 90% range; Results and Methods state the 34.7% for left-out counties.
5. "Mostly follows" untested: RESOLVED. Replaced by "correlation 0.70, descriptive, no test"; rater recompute gives 0.702.

## 4. Reasons it is not High (each MAJOR)
1. MAJOR [OWNER ONLY - expertise] A name is now given, but a YMYL money page needs a reason to trust the person: no experience, role or background line, and no named human who checked the method. With ads, AI authorship and no external citations or reputation, a rater stops at Medium+. Fix: one true line on the publisher's relevant experience, or a named independent (human) reviewer of the method with their role.
2. MAJOR [PAGE FIX] Policy-unit column base undefined. "Policy units outside A and V (FEMA NFIP Policies, August 31, 2026)" does not say: dataset version (NFIP Policies v3), policies in force on that date or written over a period, units vs policies vs homes, which zone field, and that it describes today's book while claims are 2016-2025 rated at the time. The lede tells readers to "compare the two columns", so the reader must know they are different time bases. One Data-section sentence fixes it.
3. MAJOR [PAGE FIX] Lede label ambiguity: "26.6% of 461,197 claims ... in every U.S. county" reads as "each county is 26.6%". Say "across all U.S. counties combined". Same lede still has no plain-words answer for the homeowner query (see Needs Met).

## 5. New items: trust
- AI disclosure: HELPS on balance. Google's guidance asks for "how" disclosure where readers would expect it; stating AI use plus fixed recompute rules is honest and matches the visible method sections. Two cautions: (a) "independent AI reviewers" overclaims; AI reviewers built by the same vendor under the same rules are separate, not independent - say "separate AI review passes"; (b) disclosure of AI authorship with no human expertise line makes MAJOR 1 more visible, not less. It does not lower the rating by itself.
- About "Who runs it" repeats the corrections email already given two paragraphs up (minor duplication).
- Wide overall range (19.0-32.7%) is honest but sits in the lede next to FEMA's 29%, which falls inside it; one could say "FEMA's figure falls inside this range" only if gated. Not a defect.
- Unchanged minors: title has two colons and a count; meta description is a method sentence, not the answer; Abstract/Question/Data/Methods sit between lede and table; Harris County is 13% of the 364-county base (55,323 of 424,932) with no note; zone D folded into "outside" (stated in Data); "19 of the 50" uses an arbitrary 50; no Dataset JSON-LD (not a rater item).

## 6. Changes that would raise the rating (ranked)
1. Owner: add the publisher's relevant experience, or a named human reviewer of the method (only path to High on YMYL).
2. Data section: define the policy-unit column (NFIP Policies v3, in-force units on 2026-08-31, zone field, today's book vs claims rated at loss).
3. Lede: "across all U.S. counties combined"; plain answer first ("Yes: about 1 in 4 paid flood claims ...") and one line for zone X owners linking the site's existing required / 30-day-wait pages.
4. About: "independent AI reviewers" to "separate AI review passes"; drop the repeated email.
5. Meta description as the answer; one-colon title.
6. Move Abstract/Methods/Reproduce below the table; state jump links.
7. Harris weight note; zone D shown separately; replace "of the 50" with a fifth-based statement.
