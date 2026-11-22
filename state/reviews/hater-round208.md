# Hater round 208 (louisiana, claims)

Coverage: read every word of both built pages and spot-checked numbers against data (52.8% = 151,987/287,832 in agg.json; 83.4% and 78.8% claims shares recomputed from the page's own counts; claims-page Louisiana parish claim counts equal the state page's). Screenshots viewed: Louisiana phone 00,03,06,09,12,15,18,21,24,27,30 + desktop, dark-0/1, nojs-0/1; claims phone 00,03,06,12,21,24,27,33,35 + dark/nojs-1. Skipped (cost): the other two of every three phone shots, and claims-desktop/claims-dark-0/claims-nojs-0 (dark-0 and nojs-0 are byte-identical to phone 00 on both pages, which proves screen 1 needs no JS and that there is no dark theme: no prefers-color-scheme CSS exists, so the dark shots are simply the light page). Desktop is a 20,000 px single narrow column, too tall to read at the size shown; layout only checked.
SEO search (WebSearch, standard): "flood insurance cost Louisiana" top results are Policygenius, Bankrate, MoneyGeek, Insurify, LendingTree, ValuePenguin (averages quoted $750 to $1,470; Plaquemines named most expensive parish). "flood insurance claims": FEMA "How do I start my flood claim", FloodSmart, FEMA claims blog, state handbooks (steps, photos, advance payment up to $5,000, denial appeal, NFIP has paid $87.5 billion).
No earlier BLOCKER/MAJOR items exist for these two pages (round 207 reviewed louisiana with PASS and no items; claims is new). Previous items: none to tally.

## louisiana

Checklist (A-N, PASS or defect):
- A reader's job: PASS on cost/required/pay-out answers with next steps (NFIP (877) 336-2627, FloodSmart, 30-day wait). "How risky?" answers "the ratings are below" (GAP 1).
- B situations: buyer/closing, just flooded, condo, renter pointer, town not in NFIP, map change covered. Landlord/second home only as "not businesses or second homes". PASS with that note.
- C truth: figures match data; bases labelled. Defects M3, M4 below.
- D traps: M3 (column base), MINOR on A01-A15/V15 codes in the dropdown and the headline range.
- E plain language: PASS except the long NFIP-start paragraph (about 200 words of rule text above the date calculator, louisiana-09).
- F contacts: PASS; state regulator is only the generic NAIC directory (OPEN line, GAP).
- G phone UI: tables fit, no sideways scroll, 16px inputs. Defect M2 (JS-off). "Pick your parish" is collapsed under a closed disclosure (MINOR).
- H accessibility: parish filter and inputs labelled; chart has a text equivalent. PASS.
- I trust: byline/contact are accepted; "no ads / no paid links" statement is not on the page, and the head carries an AdSense loader (MINOR).
- J navigation: breadcrumb, on-this-page, back to top, neighbouring states, parish filter. PASS.
- K speed: not measured; no print stylesheet (OPEN).
- L Spanish: OPEN (GAP).
- M freshness: as-of August 31, 2026 and download November 14, 2026 shown. PASS.
- N consistency: parish claim counts equal the claims page; median paid claim $21,899 equals the claims page. PASS.

Defects, worst first:
1. **MAJOR** (Forbes editor / link check) Section "How Louisiana appears in the national research papers": the intro promises "Each paper sorts the U.S. counties ... into five groups ... from highest fifth to lowest fifth", but each bullet only says "30 of this state's parishes have at least 100 paid ... claims ... and are listed". Louisiana's position (which fifth) is never shown, so the heading and intro promise a result the section does not give; five links lead to papers with no stated reason to click. Reader is misled into expecting a ranking. Check that should catch it: label-vs-content gate (C10-C14 style) on "how X appears".
2. **MAJOR** (editor, JS-off, louisiana-nojs-1) With JavaScript off the "Is my quote or renewal normal here?" card still shows an empty amount box, zone dropdown and "Enter an amount above.", and the proof-of-loss and coverage-start calculators (louisiana-09) show date boxes and checkboxes that do nothing. A form with nothing behind it; a frightened reader types a number and gets no answer. Check: a no-JS screenshot gate that fails any interactive control without a static fallback sentence.
3. **MAJOR** (analyst, copy editor) Parish table column "Below full-risk" (e.g. Lafourche "89.3%") has no base in its header. It is the share of single-family policies whose premium (before fees) is below FEMA's full-risk premium; the header reads like a dollar gap or a percentage below price. Reader at Cameron/Lafourche may read "89.3% below" as a discount. Check: column labels must name base ("Share of policies below full-risk premium").
4. **MAJOR** (analyst) "Which floods paid out the biggest totals" table: column headed "Claims" counts only claims that paid (Katrina 128,268), while the decade table headed "Claims filed" counts all (2000s 227,852) and the 2005 chart year counts 181,486. A reader comparing Katrina's 128,268 "claims" with the 181,486 for 2005 reads a contradiction; the base is explained only in the footnote. Check: header must say "Claims that paid" (count whose base differs from its label).
5. **GAP** (SEO) First phone screen (louisiana-00) does not show a dollar answer: the big "$1,114" starts at the very bottom of screen 1 and the top row "How risky?" says only "ratings are below". #1 results (Bankrate, ValuePenguin) open with a state average in the first sentence. Our H1 "Louisiana flood insurance and flood zones" carries no number; the number is in the title only.
6. **GAP** (SEO) Title says "flood zone map" but the page has no map, only a link and address lookup to FEMA's map; ranking pages promise cost and "average". Title and H1 differ in wording.
7. **GAP** (SEO) Competitors name the most expensive parish and give a rounded "average"; our gap-explaining table "Why do sites quote different prices" (which no top-3 result has, our information gain) sits about two-thirds down the page; a searcher seeing $750 (MoneyGeek) vs our $1,114 would bail before reaching it. Move or link it from screen 1.
8. **GAP** "How risky?" (first question) is answered only at the bottom of a 20,000 px page; no local official contact beyond the generic NAIC link; no Spanish; no print stylesheet.
9. **MINOR** "Damage was more than the coverage (of 361,000 claims paid with a damage figure)" is rounded while every neighbouring base is exact (377,052 paid; 208,696); inconsistent rounding.
10. **MINOR** "Of the five costliest years, those with no flood of their own in the table above: 1995 (totals in the yearly chart above)." is a fragment for a single year. "Hurricane Katrina alone paid $13.3 billion ..., which pulls the average up" reads as if paying Katrina inflated the claim; say the few very large claims do.
11. **MINOR** Zone table: B and X both appear under "moderate" and X again under "minimal" in the legend; copied from 44 CFR but confusing for a newcomer. Headline range "(Zone V15) $2,821" rests on 167 policies and a legacy code; zone dropdown lists A01-A15 without plain words.
12. **MINOR** "Highest:" list includes Webster Parish ($1,269) on 147 policy units while the footnote warns medians from under 100 policies swing; parish table headers are not sticky, so mid-scroll a reader cannot see which column is which (louisiana-21).
13. **MINOR** The head loads an AdSense script and account meta though no ad appears and the page never says whether ads exist; project rule is no ads before the Search Console review (owner check). Dark mode: no dark styles (shots identical to light), readable.
14. **MINOR** "Pick your parish" disclosure is collapsed by default on screen 1 (checklist G "nothing hidden or collapsed"); a separate visible "Find your parish in the table" link exists.

Verdict: FAIL

## claims

Checklist (A-N):
- A reader's job: the page answers "does it pay out" outright (83.4%) in the first sentence, but not "how do I file / what happens next" beyond one paragraph. See M3.
- B situations: just flooded served; renter, condo, landlord not addressed (data cannot; no gap line saying so).
- C truth: hero 83.4% / 267,368 / 44,379 unpaid reconcile (222,989/282,806 = 78.8% as stated); Louisiana median $21,899 matches state page. Three different periods on one page (losses 2020 on; 1978-2026; 2016-2025), each labelled (MINOR).
- D traps: a "share of claims filed" vs "share of dollars" column (M-less, MINOR 7); "Other" 14.8% next to "No reason recorded, or a code without a FEMA label" 14.9%.
- E plain language: PASS; "rated outside A and V" is explained once.
- F contacts: NFIP phone and FloodSmart absent from this page (M3); FEMA claim-steps link present; 60-day proof of loss present.
- G phone UI: defect M1 (clipped table), M2 (no finder, no on-this-page, no back-to-top, 130-row tables).
- H accessibility: no inputs at all; tables have headers; headings in order (h1, h2s). PASS.
- I trust: sources and "not endorsed by FEMA" present; as-of August 31, 2026 present.
- J navigation: breadcrumb absent on this page (only "Flood Insurance Data" bar); county links present; Buncombe, Pamlico, Pike and others unlinked (no page, so correct).
- K/L: no print, no Spanish (OPEN).
- M freshness: as-of shown once (hero), not on the later tables (MINOR).
- N consistency: top bar is black with blue H1 like the state page; shares differ from the Louisiana page (80.2% all years vs 83.4% 2020-on) and the state page explains it, this page does not mention the other period.

Defects, worst first:
1. **MAJOR** (phone, claims-21 and claims-24) The "Rain, river or tide" table has four columns and the last one ("Tidal water overflow") is cut off at the right edge of the 390 px screen: values read "6.0", "41.5", "1.5", "53.6", "34.7", "22.5"; the percent sign and last digit are clipped, and the header for the column is off-screen. A reader sees truncated numbers and cannot tell what the third column is. Check: no-sideways-scroll / clipped-cell gate at 390 px for every table.
2. **MAJOR** (checklist G, project "find-your-county lookup on screen 1") The page has no county search, no "On this page" menu and no back-to-top; it is about 22,000 px tall with a 130-row table, a 111-row table, a 68-row table and a 42-row table. The H1 is "claims by county: how often they get paid", yet the county table that answers that, headed only "County by county", is the last section, after four other big tables. A reader looking for their county scrolls roughly 20 screens. Check: S-gate that any page with 30+ rows has a finder and a jump menu.
3. **MAJOR** (checklist F; the searcher who just flooded) No NFIP phone number, no FloodSmart link, no claim-steps beyond one paragraph and a link to FEMA's steps; no mention of advance payment, photos, adjuster or the appeal path (the page sends the reader off for "NFIP claim appeal deadlines"). The "Already flooded?" box on the Louisiana page has the phone and FloodSmart; this page does not. Check: contacts line must appear on every page that tells a flooded reader to act.
4. **GAP** (SEO, "flood insurance claims") Top 3 (FEMA "How do I start my flood claim", FloodSmart, FEMA blog) give a numbered how-to: notify the insurer, document and photograph, adjuster visit, advance payment up to $5,000, payment check goes to mortgage company, denial and appeal. We give one paragraph. We give what none of them has (share paid by county, FEMA's recorded no-payment reasons) but it sits behind the filing paragraph, which is fine; the county table is too deep (defect 2).
5. **GAP** Title "payouts since 1978 and how often claims get paid (FEMA data)" says 1978; the first answer (83.4%) is for losses 2020 on. A searcher expecting a lifetime rate does not see the 1978-2026 figure (the Louisiana page has 80.2% all years) on screen 1.
6. **MINOR** (editor) The "Which years paid the most?" table lists 2024 (4th, $8.79 billion) with no note that recent years may still be open, while the county table below and the hero both carry that caveat; a reporter could quote "2024 was the fourth costliest year" without it.
7. **MINOR** Column header "Claims rated outside A and V: share of dollars paid on claims with a zone" is 17 words in a narrow column (claims-06) and is next to "Rated outside A and V" (a share of claims); two shares with different bases side by side, kept apart only by that header.
8. **MINOR** Reasons table lists "the ten most common reasons" but the ten rows add to 44,155 of 44,379 claims (99.5%); the 224 omitted are not mentioned. "Not an actual flood" (29.0% of unpaid) beside "Damage less than the deductible" is explained by the footnote only.
9. **MINOR** Three time windows on one page (losses 2020 on, 1978-2026, 2016-2025) with section titles that carry only some of them; the "Flood claims rated outside the high-risk zones" H2 omits its years, which sit in the first sentence.
10. **MINOR** Dark shots are identical to light (no dark theme); the AdSense loader and account meta are in the head (see louisiana item 13). Some county names are unlinked (no page) while their neighbours link, with no hint why.

Verdict: FAIL

## Classes

- State template (louisiana): any "How X appears" / research-paper card that gives counts but no position; any interactive card (quote checker, calculators, address box) that renders inert with JavaScript off; unlabelled table-column bases ("Below full-risk"); tables whose "Claims" count differs from the nearby "Claims filed" count.
- Claims/guide template: any wide table at 390 px (clipped last column) and any page with 30+ rows and no finder, jump menu or back-to-top; flooded-reader pages lacking the NFIP phone and FloodSmart line.
- County template: not reviewed this round; the parish-table "Below full-risk" header and unlabeled A01-A15 zone codes are likely repeated there.
- Every page: AdSense loader in the head versus the no-ads rule; no dark theme; no print or Spanish (OPEN lines).
