## home
- (1) Ad: no ad slot on this page. Not applicable; checked the markup (no adslot element).
- (2) Bordering: not applicable (home has no bordering line).
- (3) Sonoma: not applicable.
- (4) Checked, no defect: text unchanged from the round 210 read; state table and county count (329) agree with the county list. MINOR carried over: "Lowest: Maryland $569, District of Columbia $384, Alaska $368" is in table order, not lowest-first.
Verdict: PASS

## louisiana
- (1) Ad: "Advertisement" label sits above the 300x250 iframe. The aside follows the first closing section tag of the opening answer and comes before the quote checker input ("Type your yearly cost"). No ad sits between the checker and its result. MINOR: the creative has no border or frame. Checked the markup, not a browser render.
- (2) Bordering: not applicable (state page; uses "Neighboring states", left as instructed). Checked, no defect: "Neighboring states: Arkansas · Mississippi · Texas" matches Louisiana's borders.
- (3) Sonoma: not applicable.
- (4) Text re-read: the rule-text block changed only in line breaks, not in wording. Visible text otherwise unchanged from round 210. Carried-over MINOR items (costliest-years sentence, "says how many" line, "claims page" reference, long buying-now paragraph, deductible-note link text) and GAP ("the same in every flood zone") remain. No MAJOR.
Verdict: PASS

## palm-beach-county-fl
- (1) Ad: label present; aside sits after the opening answer and before the quote checker. Not between checker and result. MINOR: frameless creative, as above.
- (2) Bordering: the rebuilt label "Bordering counties with a page here:" lists Broward, Martin, Okeechobee and Hendry. data\us\county_adjacency.json (FIPS 12099) lists those four plus Glades (12043). Glades has no page in dist, so the list is correct against the data and the label is now true.
- (3) Sonoma: not applicable.
- (4) Checked, no defect: text unchanged from the round 210 read. GAP carried over: the 10,000-claim count (no cap visible in tools/collect.py; confirm the county's OpenFEMA count). MINOR carried over: "10,000 of the claim records" wording.
Verdict: PASS

## new-york-county-ny
- (1) Ad: label present; aside sits after the opening answer and before the quote checker. Not between checker and result. MINOR: frameless creative.
- (2) Bordering: "Bordering counties with a page here: Hudson · Queens · Kings · Bergen · Bronx". data\us\county_adjacency.json (FIPS 36061) lists exactly those five; each has a page in dist. True.
- (3) Sonoma: not applicable.
- (4) Checked, no defect: text unchanged from the round 210 read. MINOR and GAP carried over (ZIP table with one row, AE "too few single-family homes to price", CRS "New York" with no discount, disaster feed "through 2021").
Verdict: PASS

## dixie-county-fl
- (1) Ad: label present; aside sits after the opening answer and before the quote checker. Not between checker and result. MINOR: frameless creative.
- (2) Bordering: "Bordering counties with a page here: Levy County" (other Florida counties listed separately). data\us\county_adjacency.json (FIPS 12029) lists Gilchrist, Lafayette, Levy and Taylor. Gilchrist, Lafayette and Taylor have no page in dist. Levy is the only neighbour with a page. True.
- (3) Sonoma: not applicable.
- (4) Checked, no defect: text unchanged from the round 211 read. MINOR carried over: "The usual building deductible here is $1,250 (40.6%)" (the $2,000 and $5,000 rows are each 22.8%; "most common" is the accurate term); "885 of the claim records" wording; "1 were other or mixed". GAP: no page-level small-sample note for 435 policy records and 885 claims.
Verdict: PASS

## levy-county-fl
- (1) Ad: label present; aside sits after the opening answer and before the quote checker. Not between checker and result. MINOR: frameless creative.
- (2) Bordering: "Bordering counties with a page here: Citrus County · Marion County · Alachua County · Dixie County". data\us\county_adjacency.json (FIPS 12075) lists those four plus Gilchrist (12041), which has no page in dist. True.
- (3) Sonoma: not applicable.
- (4) Checked, no defect: text unchanged from the round 211 read. MINOR and GAP carried over (near-tie "usual" deductible $1,250 29.5% vs $2,000 29.2%; "From about $753 ... to $2,357" range excludes Zone VE; 3-claim share; "$792,424" next to "$4.1 million").
Verdict: PASS

## sonoma-county-ca
- (1) Ad: label present; aside sits after the opening answer and before the quote checker. Not between checker and result. MINOR: frameless creative.
- (2) Bordering: "Bordering counties with a page here: Marin County · Contra Costa County · Solano County · Napa County". data\us\county_adjacency.json (FIPS 06097) lists those four plus Lake (06033) and Mendocino (06045), which have no page in dist. True.
- (3) MAJOR, still open. The paragraph now reads: "The costliest flood FEMA named here was Pineapple Express - Southern (1998): $3.5 million over 284 claims. The costliest year, 1995 ( $35,936,682 ), has no single named flood. Catch-all Flooding (1978–1997), many floods: $67.3 million." The table in the same section names "Flooding (1978–1997): many floods" as a FEMA name, at $67.3 million, and the page says its own table uses FEMA's names. The lead sentence therefore states a superlative the page's own table contradicts. The next sentence contradicts it rather than qualifying it, so a reader who stops at the first sentence is misled, and the builder's rule for "costliest" is not met. The catch-all sentence does not make the lead true as written. Exact fix: replace "The costliest flood FEMA named here was Pineapple Express - Southern (1998): $3.5 million over 284 claims." with "The costliest named flood, leaving out the 1978–1997 catch-all, was Pineapple Express - Southern (1998): $3.5 million over 284 claims." Keep the catch-all sentence after it.
- (4) Checked, no defect beyond the above: the bordering list is now correct; the title "(Monte Rio)" pattern and the "since 2002" / "no aid applications" wording remain as GAP and MINOR from round 211 (the latter is a wording issue against the multiple-loss list source, not a shown false figure). Figures unchanged: 72.4% high-risk, 7,237 claims, 1,007 unpaid, five costliest years correct.
Verdict: FAIL

## wakulla-county-fl
- (1) Ad: label present; aside sits after the opening answer and before the quote checker. Not between checker and result. MINOR: frameless creative.
- (2) Bordering: "Bordering counties with a page here: Leon County". data\us\county_adjacency.json (FIPS 12129) lists Franklin, Jefferson, Leon and Liberty. Franklin, Jefferson and Liberty have no page in dist. Leon is the only neighbour with a page. True.
- (3) Sonoma: not applicable.
- (4) Checked, no defect: text unchanged from the round 211 read. GAP carried over: 5-claim share (1.6%) and about-10-claim "highest fifth" ranking need a short-sample note. MINOR: "1,534 of the claim records" wording; "unincorporated" label for the county discount.
Verdict: PASS
