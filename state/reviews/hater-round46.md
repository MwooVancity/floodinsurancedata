# Hater round 46

Scope: zone_labels note, zone_price note, CRS card (crs_what, "lower CRS class" note, multi-county cities, zero-community wording), cap and deductible notes (one sentence cut each), surcharge source now 42 U.S.C. 4015a. Sources read raw with curl --compressed this session: Cornell 42 USC 4015a and 4015, floodsmart.gov/premiumcosts, eCFR 44 CFR 64.3. Pages read as text from dist; grepped to the changed parts. Review level: light, text only. Not re-fetched: govinfo 4012a (zone_price clause 1 sentence checked by meaning against the page's own "Am I required" card only).

## home
Verdict: PASS
- Only the deductible line (index.html) and the "FEMA's ways to lower" line changed; both read true. No zone, CRS or surcharge text on this page.

## louisiana
Verdict: PASS
- surcharge: 4015a(b) reads $25 otherwise; $250 for a policy on a non-residential property or a residential property that is not the primary residence of an individual. Page says "Homes that are not your primary residence, such as second homes and rentals you own, pay ... $250 a year, against $25 for a primary home." Same scope and strength. floodsmart premiumcosts agrees ("$25 for primary residences; $250 for all other occupancies").
- zone_labels: 44 CFR 64.3 lists A, A1-30/AE, A0, A99, AH, AR, V, V1-30/VE, V0 all as "special flood hazard"; the note matches, A1-30 and AE share one description.
- crs_what: floodsmart says "Discount if building is in a participating Community Rating System community and meets eligibility requirements. Applies to all eligible policies ... regardless of flood zone." Page keeps "eligible" and "take part". Matches.
- CRS table note "a lower CRS class goes with a bigger discount": true on every row printed (class 3 = 35%, 4 = 30%, 5 = 25% ...). It is a pattern in the printed table, labelled as FEMA's list. OK.
- **MINOR** zone_price: "decides whether a federally regulated lender must require coverage" drops the other conditions (community in the NFIP, a mortgage or federal aid); the "Am I required" card below carries them. Say "is a main test of whether...".
- **MINOR** zone_price: last clause "FEMA's full-risk price is its price for that risk" is circular; a scared reader learns nothing. Say what full-risk means (price before statutory discounts, per premiumcosts: "The premium after subtracting statutory discounts from the full-risk premium").
- **MINOR** zone_labels: "high-risk" is FEMA's plain word; 64.3 says "special flood hazard". "Every zone starting with A or V" is an inference from the table, not a quoted sentence. True for every code in 64.3.
- **MINOR** cap note: "By law a primary home's premium cannot rise more than 18% a year" — floodsmart says "most policyholders" and 42 USC 4015(e)(1) lists exceptions (e.g. community rating downgrade). The next sentences hedge new policies. Add "usually"/"most". "Second homes and businesses ... up to 25%": floodsmart says "18-25%" without naming who; 4015(e)(4) says 25 percent each year for the 4014(a)(2) group (which includes non-primary residences and non-residential), a required step, not a ceiling. Not false; no source quote ties the two. Carries round-45 GAP.
- **MINOR** CRS card, state page: the counts "42 discounted, 277 no discount" were not recomputed; a city that spans two counties could be counted once per county if the state page sums county lists. Check dedupe.
- **MINOR** surcharge: "Homes" leaves out non-residential buildings and primary homes held by an entity (4015a: "primary residence of an individual"). Carried from round 45.

## palm-beach-county-fl
Verdict: PASS
- Same rule texts as louisiana; the same findings and MINORs apply (surcharge, zone_labels, zone_price, cap).
- CRS card: 25 listed discounted communities plus "No CRS discount (15)" list. Class-to-discount order holds in the table (4 = 30%, 5 = 25%, 6 = 20%, 7 = 15%, 8 = 10%, 9 = 5%). Matches FEMA's schedule shape.
- **MINOR** CRS table shows no marker for a city that also lies in another county; a reader in Boynton Beach cannot tell the 30% applies to the whole city. Harmless and not wrong: the discount belongs to the community, FEMA says it applies to all eligible policies in it. Multi-county cities on each county they span cannot mislead on the discount itself.

## broward-county-fl
Verdict: PASS
- Same texts and findings as palm-beach-county-fl. 33 communities listed in data; card and table consistent, "No CRS discount (...)" row present.

## new-york-county-ny
Verdict: PASS
- Card reads: "Not through a community discount: New York County's only NFIP community has none." Data (data/c/new-york-county-ny/data.json crs) has one row, NEW YORK, CITY OF, spans Richmond, Queens, New York, Kings (and Bronx) counties, classRating null, participatingInNFIP true. Wording true to FEMA's Community Status Book as stored. The card now names "New York" under "No CRS discount (1)", which is correct and no longer empty. Kings County has the same single row.
- The sentence "FEMA's Community Rating System gives a discount to eligible policies in communities that take part" directly follows a "none" finding; clear, not misleading.
- **MINOR** "Community discount: see [link]" in the quick answers reads clipped on a phone; give the answer in the line ("None here") as the card now does.
- **MINOR** same zone_price, zone_labels, cap MINORs as louisiana.

## Gaps
- GAP: nothing printed on whether a private flood policy carries the surcharge or CRS discount (NFIP only); name the data if a reader asks.
- GAP: 25% ceiling source naming second homes and businesses; the cap rule has no quote for it (floodsmart "18-25%" only). Add a 4015(e)(4) quote or cut the clause.
