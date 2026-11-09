# Gap backlog (owner 2026-10-28: a gap does not block a ship until it is 3 review rounds old; google_gate S14)
Ranked by reader value. hater.py record appends each round's **GAP** lines below. 11-08 (owner: "project manager, nothing
left missing"): all 179 items triaged against the built pages (`backlog-triage.md`); 91 fixed and removed; every remaining
ask is either BUILDING or DECIDED with its reason. Reviewers: a DECIDED item is not raised again as a gap.

## Building (11-08; new raw fields land with a forced cloud refresh)
- Paid share by named flood (PBC, Broward r8-r10): count unpaid claims per FEMA flood event; events table gets "share that paid".
- Share of policies below full-risk premium by ZIP (PBC, Broward, Atlantic r8-r11; Miami Herald 33469 story): per ZIP, 25+ priced.
- Condo cost line (Horry r12): median yearly cost of condo-unit policies where 30+ are priced.

## Decided (11-08)
- Competitors' figures (NerdWallet, Policygenius, Insurify, MoneyGeek, Kin, Clovered, 1-800 Insurance; ~20 items): never printed. Their base, date and method cannot be verified (Truth: never print a figure we cannot recompute); "Why published prices differ" explains measures, years and private policies with our own figures.
- Cost by city / municipality / Tulsa / The Woodlands (~12 items): site rule, no city pages; the county ZIP table names each ZIP's town and the ZIP lookup answers it.
- Take-up / share of homes insured: BUILT 11-08 on the owner's go (FEMA NFIP Residential Penetration Rates card).
- Neighbor-county comparison (Broward): each page links its bordering counties, which show their own figures; no cross-county table.
- Dam-release context for Harvey (Montgomery): no public dataset ties claims to a dam release; not stated.
- State floodplain office contact (Maine, Louisiana): no national dataset; pages print FloodSmart's sourced "ask your local floodplain manager" rule (`ec_get`).
- FEMA state profile PDF (Maine): a PDF summary, not a dataset; the page already shows the underlying figures.
- Spanish pages: built when Search Console shows Spanish queries (scoreboard rule); none on 11-06.
- Error-report route: needs the owner's contact address (PLAN, owner only).
- Thin zones in the zone table and quote-checker dropdown (Louisiana A12, 53 policies): kept; each row is a real, priced zone (50+ policies) with its count shown.
- Home "Where do I buy it?" without the 30-day wait (r114): the wait is on the line directly above; no change.
- "the land" vs "the ZIP's land" in the town-line note (r118 MINOR): the sentence's subject is the ZIPs; no change.
- Already answered on the pages: Risk Rating 2.0 pace (cap + glide rules), wildfire wait exception (`wait_wildfire`, 11-08), Elevation Certificate step (`ec_get`, 11-08), state regulator "Get Ready" (regulator link, 42 states; 9 bot-walled states link NAIC's directory), claims outside high-risk zones, recent-buyer median (policies first bought in the past year), print stylesheet (11-08), back-to-top.
- Years to full risk at 18% a year / premium-rise calculator: dropped by the owner (2026-10-28: "no calc. way too risky").
- Page length, shared rule paragraphs, per-parish take-up, NOAA panel on state pages: closed 10-28 (card review, `tools/card_spec.py`).

