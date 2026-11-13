# Rater review 2: Flood damage over building coverage (damage-over-coverage) - 2026-11-13

Verdict: MINOR REVISION. Page quality: High-minus (Medium+ to High). Needs Met: "nfip claim damage exceeded coverage" Highly Meets; "underinsured flood claims by county" Highly Meets (now accurately labelled); "flood insurance not enough coverage" Slightly Meets (no plain-words answer or pointer for the homeowner).
Scope: read doc.txt only (table truncated). Ads, CSV file and methodology card not inspected: marked unverified.

## Prior items
| # | Prior | Status | Evidence |
|---|---|---|---|
| 1 | MAJOR "Underinsured" label | FIXED | Title/H1 now "Flood damage over building coverage"; base is claims, not people. Limitations still holds the "not the owner's uninsured loss" line; no "not the share of homes" line in the lede (MINOR). |
| 2 | MAJOR no size of excess | MOSTLY FIXED | Table column "Median amount damage was over coverage" added. Not in Abstract/Results, not in the CSV column list, no "not inflation-adjusted" label. |
| 3 | MAJOR one-event flag | PARTLY FIXED | Column "Loss year with over half of them" and Limitations line added. Abstract still leads with Humphreys 52.4% with no flag (its table row says 2021). |
| 4 | MAJOR base conflict | FIXED in this page | Data, Methods and Results use one base (building payment, damage and coverage above $0). Shared methodology card unverified. |
| 5 | MAJOR ads on paper pages | UNVERIFIED | Head markup not in doc.txt. |
| 6 | MINOR Prior work, one query | NOT FIXED | Still "(WebSearch: NFIP claims damage exceeded coverage by county)", one query vs R0.1 three. |
| 7 | MINOR card wording | UNVERIFIED | |
| 8 | MINOR "Highest fifth" | FIXED | Header "Fifth by share"; "not a grade" line remains in Limitations only. |
| 9 | MINOR 4.9% twice | NOT FIXED | Lede states 4.9% for 303,311 claims and again for the 268 counties. |
| 10 | MINOR phone state filter | UNVERIFIED | |

## New findings
1. MAJOR [M1.8 one event] Abstract: "The highest share is Humphreys County, TN at 52.4% (54 of 103)". The headline county is a one-flood small-n county (table: 2021 holds over half) but the Abstract and Results present it as a standing county fact. Fix: add "(over half in 2021, one flood)" in Abstract and Results, or lead with a county without the flag.
2. MINOR [materiality] No national median excess in Abstract/Results; CSV header omits the median-amount column. Fix: add one Results line "median excess $X on claims over, not inflation-adjusted" and the CSV column.
3. MINOR [reader] No plain-words sentence for a homeowner ("about 1 in 20 paid claims") and no link to the site's coverage-limit/contents/increased-cost pages. Fix: one lede sentence and one in-sentence link.
4. MINOR [lede] "had recorded building damage over the building coverage; across the 268 counties with at least 100 each, 4.9%" is long and repeats 4.9%. Fix: one number, then "268 listed counties: 4.9% (90% range 3.9-5.8%)".
5. MINOR [prior work] single query, reads as a claim of first. Fix: print three queries or "found none".
6. MINOR [labels] Limitations says "Counties are those FEMA codes on the claim"; the Abstract and title say "by county" without that caveat. Fix: add "FEMA's county code" to the Abstract.

No overclaimed expertise, no scaled-content signs, no thin text. Byline, method, limits, cite, CSV, corrections present.

## Round 2b (re-check of the two open MAJORs only)
Verdict: ACCEPT (page quality High-minus; MINORs from round 2 unchanged and not re-checked).
- One-event flag: FIXED. Abstract now says over half of Humphreys' 54 are from 2021 and may hold one flood or several; Limitations states the 10+ claims rule. Wording is honest about "one flood or several".
- Ads: FIXED. Built page has no "pagead2" and no adsbygoogle script. Only remaining match is the inert `<meta name="google-adsense-account" content="ca-pub-...">` tag (loads no ads) plus gtag analytics. MINOR: the PAPER-GATE M3.4 wording says the "snippet" is left off; confirm adsense_check treats the meta tag as allowed, or drop it from paper pages.
- Remaining BLOCKER/MAJOR: none.
