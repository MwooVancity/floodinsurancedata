## dixie-county-fl
- (a) Label: "Advertisement" sits above the iframe, same markup as the round 210 pages. Clear label. MINOR: the 300x250 creative has no border or frame, so on a phone it can read like part of the page. Not rendered in a browser; checked the markup only.
- (b) Placement: PASS. The aside is the first element after the opening answer's closing tag and comes before the quote checker. No ad sits between the checker input and its result.
- (c) Truth: no visible sentence says "no ads". Checked, no false claim about ads.
- MAJOR: "Bordering counties: Levy County". The repo's adjacency data (data/us/county_adjacency.json, FIPS 12029) lists four neighbors: Gilchrist, Lafayette, Levy and Taylor. The page shows Levy only. Gilchrist, Lafayette and Taylor have no page in dist, so the builder appears to drop neighbors without a page while keeping the label "Bordering counties". The label names a set the page does not show. Fix: list every neighbor (plain text for those without a page) or relabel "Neighboring counties with a page here".
- MINOR: "The usual building deductible here is $1,250 (40.6% of single-family policies)." The $2,000 and $5,000 rows are each 22.8%. "Most common" is accurate; "usual" implies more than it shows.
- MINOR: "Outside the high-risk zones: 325 claims ... 1.2% (4 claims)". The count is shown, but four claims is too few for a percentage headline. Add the base in the sentence and a short-sample note.
- MINOR: "Not in full for at least 13.0% of the 77 single-family policies" and the 182-policy quartile line. Bases are shown; the headline shares rest on about 10 and about 180 policies, and the page has no small-sample note. Add one.
- MINOR: "Built from all 435 in-force NFIP policy records and 885 of the claim records FEMA publishes" reads as a subset, while the next clause says every record was received. Drop "of" or say "all 885".
- MINOR: "1 were other or mixed" (LOMA list). Use "1 was".
- MINOR: the same deductible-note link text ("Deductibles in zone AE and zones X, B or C nationwide") under a Dixie-only table, the "claims page" reference, the "which says how many" line with no counts, and the "Records in this state with no usable county code, not counted above 5" line on a county page.
- GAP: the page has no overall small-sample note, although the county rests on 435 policy records and 885 claims. Check whether a single caveat line is needed.
- Checked, no defect: 96.1% high-risk share = 545 / 567; zone rows sum to 567; 151 unpaid = 82.9% paid + 17.1% unpaid of 885; decade rows sum to 885 with the 1980s note; reason rows sum to 151; yearly claim rows sum to 885 and dollars to $21,276,979 (stated $21.3 million); $987 is within one percent of the Florida median $985 and 7% below U.S. $1,066.
Verdict: FAIL

## levy-county-fl
- (a) Label: "Advertisement" sits above the iframe, same markup as the other pages. Clear label. MINOR: the creative has no border or frame. Not rendered in a browser; checked the markup only.
- (b) Placement: PASS. The aside follows the opening answer and comes before the quote checker. No ad sits between the checker input and its result.
- (c) Truth: no visible sentence says "no ads". Checked, no false claim about ads.
- MAJOR: "Bordering counties: Citrus County · Marion County · Alachua County · Dixie County". The repo's adjacency data (FIPS 12075) also lists Gilchrist County. Gilchrist has no page in dist, so the builder drops it while keeping the label "Bordering counties". Fix as for Dixie: list every neighbor or relabel to "Neighboring counties with a page here".
- MINOR: "The usual building deductible here is $1,250 (29.5% of single-family policies)." $2,000 is 29.2%, so the two are a near tie. Say "most common" and give both shares.
- MINOR: "From about $753 a year (Zone X) to $2,357 (Zone AE) here." The range leaves out Zone VE, which holds 21.5% of policy units and is said to have too few single-family homes to price. The sentence is accurate as written; add "(Zone VE is not priced here)" so the range is not read as the full span.
- MINOR: "Of these, 0.5% (3 claims) were rated outside zones A and V ... They got 0.4% of the dollars." Counts are shown; three claims is too few for a percentage headline. Add a short-sample note.
- MINOR: "Built from all 750 in-force NFIP policy records and 1,288 of the claim records FEMA publishes" reads as a subset. Drop "of" or say "all 1,288".
- MINOR: "$792,424" next to "$4.1 million" in the flood-loss sentence mixes exact and rounded figures in one line. Use the same style for both.
- MINOR: the same deductible-note link text, "claims page" reference, "which says how many" line and "Records in this state" line as Dixie.
- GAP: "Half pay between $939 and $3,680" and the top decile rest on 397 policies. The base is shown; a short-sample note would help.
- Checked, no defect: high-risk share 91.3% = 851 / 932; zone rows sum to 932; 164 unpaid = 12.7% of 1,288; 1,124 paid + 164 unpaid = 1,288; decade rows sum to 1,288; reason rows sum to 164; yearly claim rows sum to 1,288 and dollars to $55,147,970 (stated $55.1 million); 65% above Florida $985 and 53% above U.S. $1,066 are arithmetically right; 3 of 9 communities with a discount is consistent with the CRS list.
Verdict: FAIL

## sonoma-county-ca
- (a) Label: "Advertisement" sits above the iframe, same markup as the other pages. Clear label. MINOR: the creative has no border or frame. Not rendered in a browser; checked the markup only.
- (b) Placement: PASS. The aside follows the opening answer and comes before the quote checker. No ad sits between the checker input and its result.
- (c) Truth: no visible sentence says "no ads". Checked, no false claim about ads.
- MAJOR: "The costliest flood FEMA named here was Pineapple Express - Southern (1998): $3.5 million over 284 claims." The same paragraph and the table name "Flooding (1978–1997): many floods" at $67.3 million, which is larger. The page's own text calls that name a FEMA name ("FEMA's records use this name for claims in several years"). The lead sentence is therefore false as written. Fix: "The costliest named flood, excluding the catch-all 1978–1997 row, was Pineapple Express (1998)" or lead with the $67.3 million catch-all and say it is many floods.
- MAJOR: "Bordering counties: Marin County · Contra Costa County · Solano County · Napa County". The repo's adjacency data (FIPS 06097) also lists Lake County and Mendocino County. Neither has a page in dist, so the builder drops them while keeping the label "Bordering counties". Fix as for Dixie: list every neighbor or relabel to "Neighboring counties with a page here".
- GAP: "Not in FEMA's disaster-aid records since 2002: no aid applications here came from homes that flooded more than once." The source is FEMA's current multiple-loss list (0 records here). The "since 2002" start date and "no aid applications" are wider than that source. Check the list's coverage before keeping either phrase; a narrower wording is "The multiple-loss list has 0 records for this county".
- MINOR: the title "Sonoma County, CA (Monte Rio) flood zone map ..." names a town in the county title, which reads as if the page is about Monte Rio. Same pattern as Palm Beach "(Boca Raton)" and New York "(Manhattan)".
- MINOR: "Yes: FEMA approved $835,040 ... about $1,546 per registration." About 540 registrations; add a short-sample note or the count.
- MINOR: "Built from all 2,295 in-force NFIP policy records and 7,237 of the claim records" reads as a subset. Drop "of" or say "all 7,237".
- MINOR: "The costliest year, 1995 ... has no single named flood." and the five-year line are correct but read as a second caveat; combine them into one sentence.
- Checked, no defect: high-risk share 72.4% = 1,715 / 2,368; zone rows sum to 2,368; 1,007 unpaid = 13.9% of 7,237; 6,230 paid + 1,007 unpaid = 7,237; decade rows sum to 7,237; reason rows sum to 1,007; yearly claim rows sum to 7,237 and dollars to $131,648,683 (stated $131.6 million); "the five costliest years 1995, 2019, 2005, 1986, 1997" is right; 20% above California $1,055 and 19% above U.S. $1,066 are right.
Verdict: FAIL

## wakulla-county-fl
- (a) Label: "Advertisement" sits above the iframe, same markup as the other pages. Clear label. MINOR: the creative has no border or frame. Not rendered in a browser; checked the markup only.
- (b) Placement: PASS. The aside follows the opening answer and comes before the quote checker. No ad sits between the checker input and its result.
- (c) Truth: no visible sentence says "no ads". Checked, no false claim about ads.
- MAJOR: "Bordering counties: Leon County". The repo's adjacency data (FIPS 12129) lists four neighbors: Franklin, Jefferson, Leon and Liberty. The page shows Leon only. Franklin, Jefferson and Liberty have no page in dist, so the builder drops them while keeping the label "Bordering counties". Fix as for Dixie: list every neighbor or relabel to "Neighboring counties with a page here".
- GAP: "Of these, 1.6% (5 claims) were rated outside zones A and V ... They got 1.0% of the dollars." Five claims is too few for a percentage headline. Add a short-sample note.
- GAP: "Of 118 paid single-family primary-home claims ... 8.5% ... had recorded building damage over the building coverage. That ranks in the highest fifth of 268 U.S. counties." About ten claims. The 90% range (5.1 to 13.7%) is shown, but the "highest fifth" ranking rests on that small base. Add the count to the sentence.
- MINOR: "Built from all 1,197 in-force NFIP policy records and 1,534 of the claim records FEMA publishes" reads as a subset. Drop "of" or say "all 1,534".
- MINOR: "Yes, 2 of the 3 NFIP communities here get one, up to 15% in Wakulla County." Correct against the list; the phrase "in Wakulla County" repeats the county name for the unincorporated area. Say "unincorporated Wakulla County" to match the table.
- MINOR: the same deductible-note link text, "claims page" reference, "which says how many" line and "Records in this state" line as Dixie.
- Checked, no defect: high-risk share 87.5% = 1,088 / 1,244; zone rows sum to 1,244; 267 unpaid = 17.4% of 1,534; 1,267 paid + 267 unpaid = 1,534; decade rows sum to 1,534 with the 2020s note; reason rows sum to 267; yearly claim rows sum to 1,534 and dollars to $33,307,012 (stated $33.3 million); Hurricane Dennis $15.4 million over 397 claims is consistent with the yearly 2005 total plus the ICC note; 49% above Florida $985 and 38% above U.S. $1,066 are right; 33.2% = 19.2% + 14.0% is right.
Verdict: FAIL
