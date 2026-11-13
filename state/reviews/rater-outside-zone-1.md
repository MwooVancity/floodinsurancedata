# Rater review: /flood-insurance/outside-the-zone/ (local build, noindex) - 2026-11-13

Rater stance: Google Search Quality Rater Guidelines, YMYL (financial / insurance). Files read: dist/flood-insurance/outside-the-zone/index.html, dist/about/index.html, dist/methodology/index.html. Nothing edited.

## 1. Purpose and benefit
Purpose: a data report ranking 364 U.S. counties by the share of paid NFIP claims (losses 2016-2025, FEMA Claims v3 as of 2026-08-31) whose rated zone is outside A and V (X, B, C, D), with 90% intervals, counts, a CSV, method, limitations, citation and corrections.
Beneficial: yes. It answers a real question with original computation from a primary federal source; the counts and CSV make it checkable. No harmful or deceptive purpose.

## 2. Needs Met
- "flood claims outside flood zone by county": Highly Meets (not Fully). Exact data, every county with n >= 100, counts and CSV. Held back by: no state jump or filter (364-row table on a phone), no comparison to how many policies sit outside A/V in the same county, so the number cannot be read on its own.
- "do floods happen outside high risk flood zones": Moderately Meets. The answer (yes: about 1 in 4 paid claims in these counties, 25.9%) is there, but only as "25.9% ... of claims with a payment and a rated zone meet the measure" inside an "Abstract". A homeowner has to decode "meet the measure", "rated zone", "Wilson score", "fifths". No plain one-line answer on screen 1, no national figure from FEMA to compare, no statement of what this does and does not mean for a zone X owner.

## 3. Page Quality: Medium
Positives a rater would write: original analysis of a primary federal dataset; source, fields, as-of date, window and exclusions stated; uncertainty shown per county; reproducible (method + CSV with numerators/denominators); limitations section; corrections policy with contact; FEMA non-endorsement disclaimer; no sales intent.

Reasons it is not High (each MAJOR):
- MAJOR - E-E-A-T on a YMYL topic: the site is anonymous by choice; About gives no person, role, background, or reason anyone with flood-insurance or data experience made it, and no independent review. For YMYL, "trust the method, not the author" earns Medium at best on a new site with no reputation (no external mentions, no citations found). The page itself has no author line and no published/updated date (only a data date).
- MAJOR - Misleading-by-omission risk: a county's claim share outside A/V mostly tracks where its policies are. Montgomery County MD (97%) or Holt County MO (0%) may simply reflect few A-zone policies or few X-zone policies, not that zone X is riskier or safer there. The page never shows the policy share outside A/V beside the claim share, and Limitations does not name this base-rate effect. A homeowner reading "Highest fifth" next to their county can infer "zone X is dangerous here" (or "safe" at 0.0%). Label-vs-meaning gap on a YMYL decision.
- MAJOR - Hard to understand for the stated reader: academic-paper template (Abstract, Question, Methods, Prior work, Reproduce, How to cite, Versions) built for researchers, not a homeowner on a phone. Jargon: "meet the measure", "base", "rated zone", "Wilson score interval", "fifths", "pools every listed county's counts". The first plain answer appears nowhere.
- MAJOR - Ad disclosure contradiction: the page (and About, Methodology, home, county pages; also live About) loads the AdSense script (pagead2.googlesyndication.com ca-pub-...), while About says "Any advertising, if added later, will be disclosed here" and discloses none. A rater checking the source sees undisclosed monetisation on a YMYL site whose trust claim is "non-commercial". Either remove the tag or disclose it.
- MAJOR - Prior work is unlinked and vague: "Penn State (PA counties, 2022) and UNC (2025)" with no titles or links, and "no national county ranking ... found in searches" with no search scope. FEMA's own published statement about claims outside high-risk areas is the figure every top result quotes; it is absent, so the reader cannot see whether 25.9% agrees with FEMA.

## 4. Scaled / auto-generated / untrustworthy / confusing signals
- "Highest fifth", "Second fifth"... repeated in every one of 364 rows (73 times each): reads as machine output; a grouped header row per fifth would read as edited.
- The phrase "claims with a payment and a rated zone" repeats about 8 times; template phrasing ("meet the measure") is visible.
- Title "Outside the zone: paid flood claims rated outside high-risk zones: 364 U.S. counties" has two colons and is a count-in-title pattern common to scaled pages. Meta description is a long method sentence, not an answer.
- Pooled 25.9% is event-weighted: Harris County TX alone is 55,323 of 424,932 records (13.0%, mostly Harvey), and Harris + Lee + Pinellas FL are 113,327 (26.7%). The page gives the median (25.6%) but never says the pooled figure is dominated by a few storms.
- Zone D (undetermined hazard) is counted as "outside high-risk". Correct per FEMA definitions of A/V, but a homeowner reads "outside high-risk" as "low risk"; D should be shown separately or the label should say "outside A and V, including undetermined (D)".
- "19 of the 50 counties with the highest shares are in Texas" picks an arbitrary 50 while the table is in fifths (73 per fifth). Looks like an auto-generated stat.
- Rated zone vs current map: stated in Limitations (good), but grandfathered and pre-FIRM ratings can make "X" claims sit in today's A zones; not explained in reader words.
- No search/filter or state index: a reader looking for their county must scroll or use find-in-page.
- No JSON-LD (Dataset) despite being a dataset page with CSV; not a rater item, but a missed signal.
- Positive: not thin, not doorway, not duplicated; every number has a count beside it.

## 5. Changes that would raise the rating (ranked)
1. Show each county's share of NFIP policies (policy units) rated outside A/V next to its claim share, plus one plain sentence: "A high share can mean most policies here are outside A/V, not that zone X floods more." Without this the ranking can mislead (moves Needs Met and PQ; removes the main YMYL risk).
2. Put a plain answer first, in homeowner words, before "Abstract": "Yes. In these 364 counties, about 1 in 4 paid NFIP flood claims from 2016-2025 (25.9%) were on buildings FEMA rated outside its high-risk zones." Add FEMA's own published figure (quoted from FEMA, linked, read this session) for comparison. Replace "meet the measure", "base", "fifths" with plain labels; collapse Reproduce/How to cite/Versions into one short section at the end.
3. Fix trust signals: resolve the AdSense tag vs About disclosure; add a published and last-updated date to the page; on About, say who runs it in some verifiable form (role, relevant experience, or an accountable organisation) and how the page was checked (independent recompute exists - say so); link the Penn State and UNC studies by title.
4. Add a state index (jump links per state, static) or per-state sections so a phone reader reaches their county in one tap.
5. Show zone D separately; state that the pooled figure is weighted toward Harvey/Ian counties and name their share; drop the arbitrary "top 50 in Texas" line or tie it to the fifths.
6. Group rows under one heading per fifth instead of repeating the label 364 times; shorten the title (one colon, answer words).
