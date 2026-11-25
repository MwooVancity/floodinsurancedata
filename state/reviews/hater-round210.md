## home
- Checked, no defect: no ad slot on this page (no adslot markup in the HTML); the AdSense script sits in the head only, as on every page.
- MINOR: "Lowest: Maryland $569, District of Columbia $384, Alaska $368." The three are in table order, not lowest-first, and Alaska is the lowest. A reader has to re-sort them. Fix: list Alaska $368, DC $384, Maryland $569.
- Checked, no defect: 329 counties in the county list matches the "329 counties" header; U.S. median $1,066 and Louisiana $1,114 agree with the state pages.
Verdict: PASS

## louisiana
- (a) Label: "Advertisement" sits above the iframe in small grey capitals (11px). The label is clear and the ad is not inside the data. MINOR: the 300x250 creative has no border or frame, so on a phone it can read like part of the page. Not rendered in a browser; checked the CSS only (iframe width 300, max-width 100%, fits a 343px gutter at 375px wide).
- (b) Placement: PASS. The aside follows the closing tag of the opening answer and comes before the quote checker. No ad falls between the checker input and its result. MINOR: the box sits directly above the heading "Is my quote or renewal normal here?", so a reader could take it for part of the checker. The label mitigates this.
- (c) Truth on this page: no visible sentence says "no ads". Checked, no false claim here.
- Privacy page (/privacy/), re-read on the rebuilt page: checked, no serious defect.
  - Checked, true: "Last updated November 24, 2026" now matches the new Adsterra paragraph. The "It" sentence is fixed. The Adsterra paragraph names the banner's domain (bauval.org), says the frame is sandboxed, and says a click opens the advertiser in a new tab. The sandbox attributes in the HTML match that description (no allow-same-origin, no allow-top-navigation, popups allowed). "Ads, from Google or Adsterra, never change a figure" now covers both vendors.
  - Checked, true: the Adsterra banner appears on the 380 state and county pages only (51 states plus 329 counties), and on no home, guide, ZIP or address page, as the privacy text says. "Every page loads Google AdSense's code" matches the ca-pub script on the pages checked.
  - GAP: the bauval.org host and key were copied from the Adsterra dashboard, which this review cannot see. The repo cannot confirm the host is Adsterra's. Confirm it once in the dashboard.
  - GAP: "the ad cannot ... send you to another site on its own" is true for top-level navigation (no allow-top-navigation), but the frame allows popups. Whether a script-opened popup is blocked depends on the browser's popup blocker, which the page does not mention. Reword to "cannot take over this page" or add the popup caveat.
- Visible text, read twice or confusing (unchanged in the rebuilt page):
  - MINOR: "Of the five costliest years, those with no flood of their own in the table above: 1995 (totals in the yearly chart above)." Garbled. The answer is correct (the five costliest are 2005, 2016, 2021, 1995, 2012; only 1995 has no table row). Fix: "The costliest year with no flood row in the table: 1995 (see the yearly chart)."
  - MINOR: "Disasters with the same month and title share one line, which says how many." No line in the list shows a count. Show the count or drop the clause.
  - MINOR: "(the claims page uses losses from 2020 on, so its shares differ)" points to a page the reader is not on and gives no link. Name the page with a link or drop the clause.
  - MINOR: the "Buying now?" rule paragraph is one block of about 250 words. A phone reader will re-read it. Split it into steps. The rule wording itself is not changed by this.
  - MINOR: under the deductible table, the note ends with a link whose text is "Deductibles in zone AE and zones X, B or C nationwide". Under a Louisiana-only table it reads as a caption for that table, so the table looks national. Same on Palm Beach.
  - GAP: "It is automatic, already in these prices, and the same in every flood zone." (community discount). No source on this page states the "same in every flood zone" part. Check it before release.
- Checked, no defect: high-risk share 51.3% = 206,039 / 401,925; zone rows sum to 401,925; 92,993 unpaid claims = the sum of the reason rows; 80.2% paid + 19.8% unpaid = 100; 34 non-NFIP towns listed; 64 parishes; CRS 42 of 319 with 15 shown; coastal and inland rating rows each sum to 64; Tensas $380 and Cameron $1,525 are the extremes.
Verdict: PASS

## palm-beach-county-fl
- (a) Label: "Advertisement" is present above the iframe, same as Louisiana. Clear label; same MINOR as Louisiana about the frameless creative.
- (b) Placement: PASS. The ad follows the opening answer and comes before the quote checker. No ad sits between the checker input and its result.
- (c) Truth on this page: no visible "no ads" sentence. Checked, no false claim here.
- GAP (unverified, not a found defect): the claim count is exactly 10,000. The page says "10,000 of the claim records FEMA publishes for Palm Beach County" and "received every record the download listed". The repo data (data/c/palm-beach-county-fl/agg.json, manifest.claims) shows reported_total = unique_fetched = 10,000, complete = true, state_total = 448,618. Among the 1,043 county claim manifests in data/c, Palm Beach is the only one at a round 10,000. tools/collect.py page_all takes reported_total from $inlinecount and loops until unique ids reach it; its only break is an empty page, which would leave unique below reported and show complete = false. No row cap is visible in the code. Confirm the county's NfipClaims count in OpenFEMA before release.
- MINOR: the sentence "10,000 of the claim records FEMA publishes" reads as a subset, while the next clause says every record was received. Drop "of" or say "all 10,000".
- Checked, no defect: the 2021 and 2022 medians are both $572, which is what the source records (extras.json, cost_trend), not a copy error.
- MINOR: "about 1 in 8 homes here has NFIP flood insurance (13.0%)". 13.0% is about 1 in 7.7. Say "13%".
- MINOR: two "outside high-risk zones" shares on one page with different bases: 56.6% of 926 claims (line "Outside the high-risk zones") and 54.1% of 362 paid claims (research box). Both are labelled, but a reader will take them as a conflict. Put the base in the same sentence as each share.
- MINOR: "Records in this state with no usable county code, not counted above 5" sits on a county page with no explanation. Explain it or drop it.
- MINOR: same deductible-note link text, "claims page" reference and "Disasters ... says how many" line as Louisiana. The "five costliest years" line is correct (2025, 1995, 2014 have no flood row) but needs the same rewrite.
- Checked, no defect: zone rows sum to 131,028; high-risk share 42.1% = 55,199 / 131,028; reason rows sum to 5,322; decade rows sum to 10,000; CRS 25 + 15 = 40; deductible 5.3% = 3.9% + 1.4%; full-risk median $514 matches the opening; 32% below Florida and 37% below U.S. median is arithmetically right ($673 vs $985 and $1,066).
Verdict: PASS

## new-york-county-ny
- (a) Label: "Advertisement" sits above the iframe, same markup as Louisiana and Palm Beach. Clear label. MINOR: the 300x250 creative has no border or frame, so on a phone it can read like part of the page. Not rendered in a browser; checked the markup only.
- (b) Placement: PASS. The aside is the first element after the opening answer's closing tag and comes before the quote checker. No ad sits between the checker input ("Type your yearly cost") and its result ("The median here is $1,021").
- (c) Truth: no visible sentence says "no ads". Checked, no false claim.
- Numbers checked, no defect: high-risk share 42.8% = (6,232 + 151) / 14,925; zone rows sum to 14,925; 63.9% paid + 36.1% unpaid; 917 paid + 518 unpaid = 1,435; decade rows sum to 1,435; reason rows sum to 518; yearly claim rows sum to 1,435 claims; 19% below NY median $1,261 and 4% below U.S. median $1,066 are arithmetically right; 1 in 67 = 1.5%; deductible 7.8% = 6.6% + 1.2%; "the five costliest years" line is right (2023 is the only one of 2012, 2021, 2023, 1992, 2011 with no flood row).
- MINOR: "Total paid $120,592,136" but the displayed yearly dollar figures sum to $120,592,138. A $2 gap; likely a rounding artifact in the builder. Check the total's source.
- MINOR: "Built from all 2,587 in-force NFIP policy records and 1,435 of the claim records FEMA publishes" reads as a subset, and the next clause says every record was received. Same wording as Palm Beach: drop "of" or say "all 1,435".
- MINOR: the ZIP section says "ZIPs with the largest number of priced single-family policies" and shows one row (10014, 37 priced). Either show the list or say why only one ZIP qualifies.
- MINOR: "Yes: FEMA's disaster-aid records hold 8 records" and the 90-policy rebuilding base ("Not in full for at least 87.8% of the 90 single-family policies") are small bases; the 90 is shown, but the headline share has no small-sample note. Same for the deductible base of 167 and the quartile base of 171.
- MINOR: the same "Disasters with the same month and title share one line, which says how many" line with no count shown; the same deductible-note anchor "Deductibles in zone AE and zones X, B or C nationwide" under a New York-only table; the same "(the claims page uses losses from 2020 on...)" reference.
- GAP: "Zone AE, 41.8% of policy units, has too few single-family homes to price." AE is the zone most Manhattan policies sit in, and the page gives no cost for it. The statement follows the 50-policy rule and is not false, but a reader in AE gets no number. Check the reason before release.
- GAP: "No CRS discount (1): New York" and "New York County's only NFIP community has none." Not verified in this review. Confirm against FEMA's Community Status Book for New York City before release.
- GAP: the disaster source line says "declarations through 2021", while Louisiana says "through 2026" and Palm Beach "through 2024". Confirm the feed is current for New York County, since the latest listed disaster is from 2021.
- Checked, no defect: the 2021 to 2026 trend ($633 to $1,021), the full-risk and premium medians ($807 and $804), and the 33.9% below-full-risk share all match the opening and the tables.
Verdict: PASS
