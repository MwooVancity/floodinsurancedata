# Rater review 1: /flood-insurance/underinsured/ (local build, noindex) - 2026-11-13

Rater stance: Search Quality Rater Guidelines, YMYL (insurance / money), strict, PAPER-GATE-PROMPT M2/M3/R3.6. Files read: dist/flood-insurance/underinsured/index.html, dist/data/underinsured.csv, dist/about (Who runs it), dist/methodology (papers card). Publisher credentials and AI use are owner-decided: not raised. Nothing edited.

Checks run: CSV has 268 rows, numerators sum 13,326, denominators 273,450 = 4.87% = "4.9%". Humphreys 54/103 = 52.4%. "10 of the 50 in Texas" counted from the table = 10. Page is noindex,follow.

## 1. Needs Met
- "flood insurance not enough coverage": Slightly Meets. Analyst title and lede ("recorded building damage above the building coverage"). No plain answer to the homeowner's question (how common is it, what do I do), and no pointer to the site's own coverage-limit, contents or increased-cost pages.
- "nfip claim damage exceeded coverage": Highly Meets. Exact measure, FEMA fields quoted, 4.9% national, county table, CSV.
- "underinsured flood claims by county": Moderately Meets, upper end. Every county, interval, n, CSV. Held back by the label problem (MAJOR 1), no size of the excess (MAJOR 2), and the top row's single-event question (MAJOR 3).

## 2. Page Quality: Medium+ (not High)
Purpose clear; main content strong and reproducible; responsibility named (owner decision, not penalised here); reputation signals: none external. Ads load on this page (see MAJOR 5). Below High because of the MAJORs below.

## 3. Findings

1. MAJOR [label vs data] Headline and title "Underinsured: flood claims where damage passed the building coverage". "Underinsured" states the policyholders' condition; the data only shows FEMA's recorded actual-cash-value damage above the policy's building limit on paid claims. Many NFIP buildings carry the program maximum, and damage above a limit is not a choice or an error by the owner. A reader can take "Underinsured: Humphreys County 52.4%" as "52% of people there are underinsured". Limitations says it is not the owner's uninsured loss, but that sits at the bottom. Fix: title/H1 "Flood claims where recorded damage passed the building coverage" (drop "Underinsured:" or put it in quotes as the search term); add to the lede "this is not the share of policyholders or homes."

2. MAJOR [M1.4 materiality] Shares only, no size. Nothing says how far damage passed coverage (median excess in dollars, or share within 10% over). A 4.9% share could be 1,000 dollars over or 100,000. Reader cannot tell if the finding matters. Fix: add median excess (damage minus coverage, claims over only), dollars labelled "not adjusted for inflation", to Results and CSV.

3. MAJOR [M1.8 one event] Top row "Humphreys County, TN at 52.4% (54 of 103)" is in the Abstract as the headline county, and the CSV loss_years is a flat "2016-2025". No line says whether most of those 54 are one loss year. Small high-share counties are typically one flood. The reader is invited to read it as a standing county trait. Fix: for every row, flag when one loss year is over half the numerator (page note plus CSV column); the Abstract line names it or drops the county.

4. MAJOR [M2.4 base conflict] Three statements of the base disagree. Data: base requires "a building payment above $0, recorded building damage above $0 and building coverage above $0". Methods: denominator is "all single-family primary-home claims with a building payment". Methodology papers card: "a claim counts as paid when building, contents and Increased Cost of Compliance payments add to more than $0". Zero-damage claims are either in or out of the denominator, and "paid" means building-only here but any-payment in the shared card. Fix: one base sentence, used identically in Data, Methods, CSV header and the methodology card (or the card says "this paper uses building payment above $0").

5. MAJOR [M3.4 gate] The AdSense snippet (ca-pub-8997828618122077) is in the page head. PAPER-GATE says it is left off paper pages, with adsense_check exempting the READY papers. The sibling outside-the-zone page carries it too, so this is a gate not yet built or enforced. A YMYL research page with ads is the combination the gate was written to avoid. Fix: remove the snippet on paper pages and exempt the paper URLs in tools/adsense_check.py; add the check.

6. MINOR Prior work: "No published ranking of this measure by county was found in searches on 2026-11-12 (WebSearch: NFIP claims damage exceeded coverage by county)." One query is below the R0.1 three-query rule as printed; the sentence also reads as a claim of first. Fix: print all queries run, or say "found none" and cite any adjacent study.

7. MINOR Methodology card says "The overall figure pools every listed county's counts." This paper's lede leads with all counties combined (303,311), different from the listed-county pool (273,450). The paper explains it, the shared card does not. Fix: card wording "the listed-county pool; a paper may also show the all-county figure."

8. MINOR "Highest fifth" label on 54 rows reads as a grade next to "Underinsured" (partly offset by the Limitations line "not a grade"). Fix: heading "Fifth by share" with the position note beside the table, not only in Limitations.

9. MINOR Lede states 4.9% twice (all counties, then the 268), the same number; the second adds only the range. Merge to one sentence.

10. MINOR No state jump or filter on a 268-row table on a phone; no state in the page's text for a homeowner to find their county quickly.

## 4. Misread check
- As advice: no advice words; Limitations is clear. But "Underinsured" in the title invites "I should buy more". Covered by MAJOR 1; adding a link to the site's coverage-limit / contents page would help the reader, not advise.
- As a prediction: "A fifth is ... not a risk score or a prediction" is present; no forecast words found. OK.
- As a risk score: the table sorted by share beside county names could read as "worst counties". Fifth labels and Limitations mitigate; "highest" is data-true.
- As the reader's own uninsured loss: Limitations covers it, in the right words (contents, deductibles, other insurance, aid), but late. Move one sentence into the lede (MAJOR 1).
- Selection: left-out counties are reported (1,981 with at least one claim, median 0.0%, pooled 5.0%). Good.
- Private insurance and uninsured homes: stated.

## 5. Changes that raise the rating (ranked)
1. Rename and re-lede (MAJOR 1), add excess size (MAJOR 2).
2. One-event flag (MAJOR 3) and one base sentence everywhere (MAJOR 4).
3. Remove ads on paper pages (MAJOR 5).
4. Plain-words answer first for the homeowner query, with a link to the site's coverage-limit and increased-cost pages.
5. Minors 6-10.
