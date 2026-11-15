"""Every legal / program fact the county page states, with the official page that says it.
The page prints rule text ONLY from here (build_page uses rule(key)); gate.py checks each data-rule span on a
page equals its registry text; recheck.py re-fetches each source and checks the excerpt is still there.
method: "curl" = machine-verifiable; "manual" = the host blocks scripts (fema.gov), excerpt verified by a human
read on `checked` (re-read it when it goes stale). Never add a rule without a source and an excerpt."""

FS = "https://www.floodsmart.gov"
FIM = "https://agents.floodsmart.gov/sites/default/files/media/document/2025-09/fema_nfip-FloodInsuranceManual-October2025-508c.pdf"   # pdf, read by hand 2026-11-02
CHECKED = "2026-10-25"
# FEMA's own dataset description (fema.gov pages block scripts; the OpenFEMA metadata API does not)
IA_META = "https://www.fema.gov/api/open/v1/OpenFemaDataSets?$filter=name%20eq%20'IndividualAssistanceHousingRegistrantsLargeDisasters'"

CFR64 = "https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64"
CFR59 = "https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=59&section=59.1"
WIND_FS = "https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-wind-vs-floodwater-damage-fact-sheet-03-2023.pdf"   # pdf, read by hand 2026-11-03
CFR70 = "https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=70"
CFR60 = "https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=60&section=60.3"   # read raw 2026-11-13 (compressed)
CONDO_B ="https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-flood-insurance-condominium-associations-brochure-01-2025.pdf"   # pdf, read raw 2026-11-12
CONDO_P = "https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-condo-association-flood-policies-dont-protect-belongings-postcard-01-2023.pdf"   # pdf, read raw 2026-11-12
RR2 = "https://www.fema.gov/sites/default/files/documents/fema_rr-2.0_2025.pdf"   # pdf, read raw 2026-11-13
LOMC = "https://hazards.fema.gov/femaportal/onlinelomc/signin"
PRELIM = "https://hazards.fema.gov/femaportal/prelimdownload/"
CFR72 = "https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=72"
CFR61 ="https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61"
CFR60 = "https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=60&section=60.3"
USC4012A = "https://www.law.cornell.edu/uscode/text/42/4012a"

RULES = {
    "fema_outside_third": {   # outside-the-zone paper 11-13, FloodSmart "What is my flood risk" read raw
        "text": "FEMA's own figure: over the 10 years 2014 to 2024, nearly one-third (29%) of NFIP flood insurance claims came from areas outside "
                "of current high-risk flood areas.",
        "sources": [(FS + "/flood-zones-and-maps/what-is-my-flood-risk", "Over the past 10 years (2014 - 2024), nearly one-third of NFIP flood insurance claims came from areas located outside of current high-risk flood areas", "curl"),
                    (FS + "/flood-zones-and-maps/what-is-my-flood-risk", "29% Over the past 10 years (2014 - 2024)", "curl")]},   # r5: the 29% is FloodSmart's headline figure beside the sentence
    "openings_rule": {   # vents guide 11-13, 44 CFR 60.3(c)(5) read raw from eCFR (scope: (c) header)
        "text": "Where FEMA has given a community final flood elevations, the community must require, for new construction and substantial improvements, "
                "that fully enclosed areas below the lowest floor that are usable only for parking, building access or storage (not a basement) and are subject to flooding let floodwater in and out: "
                "either a design certified by a registered professional engineer or architect, or at least two openings with a total net area of at least "
                "one square inch for every square foot of enclosed area, their bottoms no higher than one foot above grade (44 CFR §60.3(c)(5)).",
        "sources": [(CFR60, "has provided a notice of final flood elevations", "curl"),
                    (CFR60, "fully enclosed areas below the lowest floor that are usable solely for parking of vehicles, building access or storage", "curl"),
                    (CFR60, "must either be certified by a registered professional engineer or architect", "curl"),
                    (CFR60, "A minimum of two openings having a total net area of not less than one square inch for every square foot of enclosed area subject to flooding", "curl"),
                    (CFR60, "The bottom of all openings shall be no higher than one foot above grade", "curl")]},
    "condo_rcbap": {   # condo guide 11-12, FEMA brochure 01-2025 read raw
        "text": "The NFIP's Residential Condominium Building Association Policy (RCBAP) is available to condominium associations to insure "
                "against direct physical damage to the building from a flood, and it can pay up to $250,000 in building loss payments for any one unit.",
        "sources": [(CONDO_B, "is available to condominium associations to insure against direct physical damage to your building from a flood", "manual"),
                    (CONDO_B, "$250,000 in building loss payments for any one unit", "manual")]},
    "condo_contents": {   # FEMA postcard P-2311, January 2023, read raw
        "text": "An association's RCBAP does not cover the unit owner's personal belongings; the NFIP offers a contents-only policy with a $100,000 coverage limit.",
        "sources": [(CONDO_P, "but it does not cover your personal belongings", "manual"),
                    (CONDO_P, "offers a contents-only flood insurance policy with a $100,000 coverage limit", "manual")]},
    "condo_own": {
        "text": "FEMA says condominium associations should encourage unit owners to buy contents or building coverage of their own.",
        "sources": [(CONDO_B, "should encourage individual unit owners to purchase contents or building coverage of their own", "manual")]},
    "homeowners_excl": {
        "text": "Most homeowners insurance does not cover flood damage.",
        "sources": [(FS + "/flood-insurance-basics", "most homeowners insurance does not cover flood damage", "curl")]},
    "wait_30": {
        "text": "Most NFIP policies take effect <b>30 days after you buy</b>, so a policy bought today will not cover a "
                "flood this week.",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl")]},
    "wait_exceptions": {
        # review 11-15: one 80-word run split into the two exceptions, same words and sources
        "text": "FEMA's flood insurance manual lists two exceptions. With a mortgage: when you are making, increasing, extending or renewing a loan secured "
                "by the insured property, coverage you apply for on or before closing can start at the time of the loan closing, if the "
                "insurer gets the form and full amount due in time. With a new map: when a FEMA map revision newly shows the building in a high-risk zone, "
                "the wait is one day if the insurer gets them within 13 months of the revision's effective date.",
        # 11-03: was "(44 CFR §61.11)" on a 2024 CFR snapshot. Current 61.11(a) gives the 1-day wait for ANY initial purchase in the 13 months
        # after a map revision; the October 2025 manual (what insurers apply) limits it to buildings newly mapped into an SFHA. Rule 4: the
        # narrower case is the one both support, so the page prints the manual's (a reader never reads "1 day" when FEMA applies 30).
        "sources": [(CFR61, "During the 13-month period beginning on the effective date of a revised", "curl"),
                    (FIM, "coverage becomes effective as of the time of the loan closing", "manual"),
                    (FIM, "making, increasing, extending, or renewing a loan secured by the insured property", "manual"),
                    (FIM, "must apply for flood insurance (or request an endorsement to add or increase coverage) on or before the closing date", "manual"),
                    (FIM, "revises an FHBM or a FIRM to show that the building is now in an SFHA when it was not previously", "manual"),
                    (FIM, "within 13 months from the effective date of the map revision", "manual")]},
    "start_30": {   # policy start-date tool (11-03); FIM October 2025, Table 8
        "text": "Without an exception, the earliest start is 12:01 a.m. local time on the 30th calendar day after the application date, if the insurer receives the "
                "form and full amount due within 10 calendar days of that date or they are mailed by certified mail within 4 calendar days; otherwise it is the "
                "30th calendar day after the insurer receives them.",
        "sources": [(FIM, "on the 30th calendar day after the application date", "manual"),
                    (FIM, "within 10 calendar days from the application date", "manual"),
                    (FIM, "mailed by certified mail within 4 calendar days from the application date", "manual"),
                    (FIM, "on the 30th calendar day after the insurer", "manual")]},
    "start_map": {   # FIM Table 9
        "text": "With the map exception the same receipt rules apply, but the start is the next calendar day instead of the 30th.",
        "sources": [(FIM, "on the next calendar day after the application date", "manual"),
                    (FIM, "on the next calendar day after the insurer", "manual")]},
    "start_map_13": {   # round 57 T3: printed in the tool's rules and appended to every map result (JS reads this span)
        "text": "The map exception holds only if the insurer receives the form and full amount due within 13 months of the map revision's effective date; "
                "after that, the 30-day wait applies.",
        "sources": [(FIM, "within 13 months from the effective date of the map revision", "manual"),
                    (FIM, "after 13 months from the effective date of the map revision, the 30-day waiting period applies", "manual")]},
    "start_loan": {   # FIM Table 10
        "text": "Exception for a policy bought while making, increasing, extending or renewing a mortgage: coverage starts at the time of the loan closing if the insurer receives the form and full amount due within 30 calendar "
                "days of closing when the lender, title company or settlement attorney pays, or within 10 calendar days when you or anyone else pays; otherwise "
                "the earliest start is the 30th calendar day after the insurer receives them. Contents-only coverage qualifies only if the contents are part of "
                "the security for the loan.",
        "sources": [(FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making, increasing, extending or renewing a mortgage", "curl"),   # r-private2: the exception named by FEMA's own words
                    (FIM, "Contents-only policies and endorsements can only be eligible for the loan exception if the contents are part of the security for a loan", "manual"),
                    (FIM, "If the lender, title company, or settlement attorney pays the premium", "manual"),
                    (FIM, "within 30 calendar days from the closing", "manual"),
                    (FIM, "within 10 calendar days from the loan transaction closing", "manual"),
                    (FIM, "The effective date will be the date and time of the loan closing", "manual")]},
    "howto_answer": {
        "text": "Most policies start <b>30 days</b> after you buy. Bought while making, increasing, extending or renewing a mortgage, "
                "it can start at closing if the insurer is paid within 10 days (30 if the lender, title company or settlement attorney pays).",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl"),
                    (FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making, increasing, extending or renewing a mortgage", "curl"),
                    (FIM, "The effective date will be the date and time of the loan closing", "manual"),
                    (FIM, "within 10 calendar days from the loan transaction closing", "manual"),
                    (FIM, "If the lender, title company, or settlement attorney pays the premium", "manual"),
                    (FIM, "within 30 calendar days from the closing", "manual")]},
    "howto_tiles": {
        "text": "<ul class='kv'><li><b>Waiting period</b><span>30 days</span></li>"
                "<li><b>Bought with a new or refinanced mortgage</b><span>Can start at closing, if paid in time</span></li>"
                "<li><b>NFIP building limit</b><span>$250,000</span></li>"
                "<li><b>NFIP contents limit</b><span>$100,000</span></li></ul>",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl"),
                    (FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making", "curl"),
                    (FIM, "The effective date will be the date and time of the loan closing", "manual"),   # hcu 11-07: "No wait" dropped the paid-in-time condition
                    (FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl")]},
    "renters_cover": {   # renters page (11-07), FloodSmart's "Renters" section read raw with curl
        "text": "An NFIP renters policy protects the things you own inside your home, such as furniture, clothes, televisions, "
                "computers, rugs and some artwork, for up to <b>$100,000</b> of damage. It is contents coverage.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Flood insurance for renters is also called Contents coverage and it protects the things you own inside your home", "curl"),   # FloodSmart reworded 11-12; read raw this session
                    (FS + "/get-insured/buy-a-policy", "Such as your furniture, clothes, television, computers, rugs and some artwork", "curl"),
                    (FS + "/get-insured/buy-a-policy", "This policy covers your belongings for up to $100,000 of damage", "curl")]},
    "limits": {
        "text": "For a home, NFIP building coverage goes up to <b>$250,000</b> and contents coverage up to <b>$100,000</b>; "
                "a renter's contents coverage goes up to <b>$100,000</b>; for a business, building and contents each go up to <b>$500,000</b>.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000 of flood damage and contents policies cover up to $100,000 of flood damage for belongings kept inside your home", "curl"),
                    (FS + "/get-insured/buy-a-policy", "This policy covers your belongings for up to $100,000 of damage", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Each type of coverage (building and contents) covers up to $500,000 in flood damage", "curl")]},
    "building_cap": {
        "text": "the NFIP's <b>$250,000</b> building limit.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl")]},
    "how_to_buy": {
        "text": "To buy: call the NFIP at <a href='tel:+18773362627'><b>(877) 336-2627</b></a>, go to <a href='https://www.floodsmart.gov' rel='nofollow "
                "noopener' target='_blank'>FloodSmart.gov</a>, or ask any licensed insurance agent. Every NFIP insurer "
                "offers the same rates.",
        "sources": [(FS + "/contact", "Call the NFIP at (877) 336-2627", "curl"),
                    (FS + "/get-insured/buy-a-policy", "vary by insurance provider, who sells through the program", "curl")]},   # FloodSmart reworded 11-13 (was "Each one offers the same rates.")
    "already_flooded": {
        "text": "<b>Already flooded?</b> Insured: report the loss to your insurance agent or company now (FEMA's steps: "
                "<a href='https://www.floodsmart.gov/recover/start-a-claim' rel='noopener' target='_blank'>how "
                "to start a flood claim</a>), and send a proof of loss (your signed, sworn statement of the amount you are claiming) within 60 days of the flood (44 CFR 61, "
                "App. A(1), Art. VII). Not insured: a policy bought today will not cover a flood that already "
                "happened, and FEMA disaster aid is open to people in counties designated in a federally declared "
                "disaster.",
        "sources": [(FS + "/contact", "Report your loss immediately to your insurance agent or carrier.", "curl"),
                    (IA_META, "in designated counties who sustained damage", "curl"),
                    (IA_META, "resulting from a federally declared disaster may apply", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "Within 60 days after the loss, send us a proof of loss", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "your statement of the amount you are claiming under the policy signed and sworn to by you", "curl")]},
    "fl_citizens": {   # Florida only (s. 627.351(6), F.S.): SFHA homes since 2023 (para 2), everywhere else phased in by rebuild cost (para 1); round 5 blocker
        "text": "In Florida, a home insured by Citizens Property Insurance with wind coverage must also carry flood insurance. "
                "In a high-risk zone (A or V) this has applied since 2023 (new policies from April 1, renewals from July 1), "
                "whatever the home is worth. Outside those zones it phases in by rebuilding cost: from January 1, 2026 at "
                "$400,000 or more, and from January 1, 2027 for all other Citizens homes. Condo-unit and no-wind policies are exempt.",
        "sources": [("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "located within the special flood hazard area defined by the Federal Emergency Management Agency must have flood coverage in place", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "policies renewing on or after July 1, 2023", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "January 1, 2026, for a structure that has a dwelling replacement cost of $400,000 or more", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "January 1, 2027, for all other personal lines residential property insured by the corporation", "curl")]},
    "wait_wildfire": {   # 44 CFR 61.11(c), read raw 11-08 (eCFR, curl --compressed); hater r10/r11 Orange County
        "text": "One more exception (44 CFR 61.11(c)): coverage starts the day after you apply and pay when FEMA determines the "
                "property is affected by flooding on federal land caused or made worse by post-wildfire conditions, and you buy "
                "it within 60 days after the fire's containment date.",
        "sources": [(CFR61, "flooding on Federal land that is a result of, or is exacerbated by, post-wildfire conditions", "curl"),
                    (CFR61, "not later than 60 calendar days after the fire containment date", "curl")]},
    "fl_citizens_private": {   # s. 627.351(6), F.S., read raw 11-08 (flsenate.gov, curl): who supplies Citizens' required flood cover
        "text": "Citizens does not sell flood insurance: the required flood policy comes from another insurer, the NFIP or a private "
                "one, and must at least match the NFIP's dwelling coverage or meet Florida's private flood insurance rules (s. 627.715).",
        "sources": [("https://www.flsenate.gov/Laws/Statutes/2025/627.351", "flood insurance is not provided by the corporation", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/627.351", "must meet, at a minimum, the dwelling coverage available from the National Flood Insurance Program or the requirements of s. 627.715", "curl")]},
    "fl_citizens_short": {   # must not contradict fl_citizens: same two tracks, no "now" that goes stale
        # owner 11-15 review: was one run-on with four time conditions; same two tracks, three short sentences
        "text": "Florida has its own rule for homes insured by Citizens, the state-backed insurer, that have wind cover. In a high-risk zone, flood cover "
                "has been required since 2023. Outside one, it has been required since January 2026 for homes that cost $400,000 or more to rebuild, "
                "and from January 2027 for all others.",
        "sources": [("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "located within the special flood hazard area defined by the Federal Emergency Management Agency must have flood coverage in place", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "January 1, 2026, for a structure that has a dwelling replacement cost of $400,000 or more", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "January 1, 2027, for all other personal lines residential property insured by the corporation", "curl")]},
    "aid_register_60": {   # deadline planner (2026-10-29): stated as a rule, never computed (the page cannot know the declaration date)
        "text": "If the President declares a major disaster or emergency for your area, FEMA's standard window to register "
                "for disaster aid is 60 days from that declaration date, and FEMA can extend it (44 CFR §206.112).",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=206&section=206.112",
                     "The standard FEMA registration period is 60 days following the date that the President declares", "curl")]},
    "private_deadlines": {
        "text": "A private (non-NFIP) flood policy sets its own claim deadlines; they are in that policy.",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-12.xml?part=339&section=339.3",
                     "must accept private flood insurance, as defined in § 339.2", "curl")]},
    "zone_codes": {   # round 16: B, C, A99, AH, A01-A30 shown with no plain words
        "text": "What the zone codes mean (44 CFR §64.3): A, AE and A1–A30 are high-risk; AO and AH are high-risk with "
                "shallow flooding; A99 is high-risk behind a flood barrier FEMA treats as complete; V, VE and V1–V30 are "
                "coastal high-risk, flooded by tides with fast-moving water (velocity); B and X are areas of moderate flood hazard, C and X areas of minimal hazard; D has possible but undetermined flood hazards.",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "B, X Areas of moderate flood hazards", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "C, X Area of minimal hazards", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "D Area of undetermined but possible, flood hazards", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "and with velocity, that is inundated by tidal floods (coastal high hazard area)", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "A99 Area of special flood hazard where enough progress has been made on a protective system", "curl")]},
    "private_accept": {   # r-private 11-13 MAJOR: was a paraphrase cited to the FDIC rule only; now the statute's duty, quoted
        # (42 U.S.C. 4012a(b)(1)(B), govinfo read raw 11-13), scope = "regulated lending institutions" as the statute says
        # r-private2 11-13 MAJOR: one plain clause, no "subparagraph (A)" cross-reference, no back-to-back quotes (claims_check Q2)
        "text": "Federal law tells federal lending regulators to direct regulated lending institutions \"to accept private flood insurance as "
                "satisfaction of the flood insurance coverage requirement\" when the private policy's coverage \"meets the requirements for coverage\" "
                "under that requirement (42 U.S.C. §4012a(b)(1)(B)). A private policy's price is not in FEMA's records.",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "shall by regulation direct regulated lending institutions", "curl"),
                    ("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "to accept private flood insurance as satisfaction of the flood insurance coverage requirement under subparagraph (A) if the coverage provided by such private flood insurance meets the requirements for coverage under such subparagraph", "curl")]},
    "limits_quoted": {   # r-private 11-13 MAJOR: limits with the source in the sentence (floodsmart buy-a-policy, read raw 11-13)
        "text": "FEMA's <a href='https://www.floodsmart.gov/get-insured/buy-a-policy' rel='noopener'>FloodSmart buying page</a> says, for a home: "
                "\"Building policies cover up to $250,000 of flood damage and contents policies cover up to $100,000 of flood damage for "
                "belongings kept inside your home.\" For a business: \"Each type of coverage (building and contents) covers up to $500,000 in flood damage.\"",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000 of flood damage and contents policies cover up to $100,000 of flood damage for belongings kept inside your home", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Each type of coverage (building and contents) covers up to $500,000 in flood damage", "curl")]},
    "private_statement": {   # private flood guide 11-13: 12 CFR 339.3(c)(2) read raw (eCFR, curl --compressed); FDIC scope and "may" kept
        "text": "Under the FDIC's rule, a lender it supervises may treat a private policy as meeting the federal definition of private flood insurance, without further review, "
                "if the policy or an endorsement says: \"This policy meets the definition of private flood insurance contained in "
                "42 U.S.C. 4012a(b)(7) and the corresponding regulation.\" (12 CFR §339.3(c)(2)).",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-12.xml?part=339&section=339.3",
                     "without further review of the policy, if the following statement is included within the policy or as an endorsement to the policy", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-12.xml?part=339&section=339.3",
                     "This policy meets the definition of private flood insurance contained in 42 U.S.C. 4012a(b)(7) and the corresponding regulation.", "curl")]},
    "rcv_80": {   # hater r6: the real answer to "would it pay to rebuild" (SFIP Dwelling Form, 44 CFR 61 App. A(1), Art. VII)
        "text": "The NFIP pays the cost to rebuild (not a depreciated value) only for a single-family home that is your "
                "principal residence and is insured for at least 80% of its full rebuilding cost, or for the $250,000 maximum.",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "the amount of insurance in this policy that applies to the dwelling is 80 percent or more of its full replacement cost immediately before the loss, or is the maximum amount of insurance available under the NFIP", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "It is your principal residence", "curl")]},
    "save_ways": {   # hater r5: every top result answers "how do I pay less"; FEMA's own list
        "text": "FEMA's ways that may lower an NFIP bill: a higher deductible (you pay more of any loss), work that lowers "
                "the building's flood risk, and an Elevation Certificate.",
        "sources": [("https://agents.floodsmart.gov/articles/paying-less-flood-insurance",
                     "Choose a Higher Deductible", "curl"),   # 2026-10-28: FEMA moved the old headline into page metadata
                    (FS + "/premiumcosts", "In return, your overall flood insurance premium may be lower.", "curl")]},
    "price_drivers": {   # hater r5 (home): every top result says what drives the price
        "text": "FEMA prices each building from where it is (distance to the coast, rivers and other flood sources, and how high "
                "the ground sits), how it is built (foundation type, first-floor height) and what the policy covers (coverage "
                "amounts and deductibles).",
        "sources": [(FS + "/premiumcosts", "distance to flooding sources, including the distance to the coast", "curl"),
                    (FS + "/premiumcosts", "The elevation of the ground where the building is located", "curl"),
                    (FS + "/premiumcosts", "Foundation Type: The building", "curl"),
                    (FS + "/premiumcosts", "Buildings whose first floor is higher off the ground generally have", "curl"),
                    (FS + "/premiumcosts", "Choosing a higher deductible means you will need to cover more out of pocket", "curl")]},
    "purchase_short": {   # the screen-1 summary; the full rule sits in its card (no sentence printed twice)
        "text": "Federal law requires it in a high-risk zone with a federally regulated or backed mortgage or federal "
                "building help; outside those zones a lender may still require it.",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "regulated lending institutions", "curl"),
                    ("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "financial assistance for acquisition or construction purposes", "curl"),
                    ("https://www.federalreserve.gov/frrs/regulations/interagency-questions-and-answers-regarding-flood-insurance.htm",
                     "a lender may require flood insurance as a condition of making the loan, as a matter of safety and soundness", "curl")]},
    "howto_short": {
        "text": "Usually 30 days after you buy; bought while making, increasing, extending or renewing a mortgage, it can start "
                "at closing if the insurer is paid in time.",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl"),
                    (FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making, increasing, extending or renewing a mortgage", "curl"),
                    (FIM, "The effective date will be the date and time of the loan closing", "manual"),
                    (FIM, "within 10 calendar days from the loan transaction closing", "manual")]},
    "aid_insurance": {   # owner of a flood-damaged home in a high-risk zone: FEMA aid comes with an insurance duty
        "text": "If FEMA aid after a flood goes to buy or build a home in a high-risk zone, you must buy and keep flood insurance on it for at least the amount of the aid, or "
                "you cannot get federal aid for later flood damage to it (44 CFR §206.110).",
        "sources": [("https://www.law.cornell.edu/cfr/text/44/206.110", "in order to receive any Federal assistance for future flood damage to any insurable property", "curl"),
                    ("https://www.law.cornell.edu/cfr/text/44/206.110", "must buy and maintain flood insurance", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/5154a", "having failed to obtain and maintain flood insurance", "curl")]},
    "purchase_answer": {
        "text": "Federal law requires it only in a high-risk zone (A or V) with a federally regulated or backed mortgage, "
                "or federal help to buy or build (42 U.S.C. §4012a).",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "regulated lending institutions", "curl"),
                    ("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "financial assistance for acquisition or construction purposes", "curl")]},
    "lender_any_zone": {
        "text": "Outside those zones, a lender may still require it.",
        "sources": [("https://www.federalreserve.gov/frrs/regulations/interagency-questions-and-answers-regarding-flood-insurance.htm",
                     "a lender may require flood insurance as a condition of making the loan, as a matter of safety and soundness", "curl")]},
    "cap": {
        "text": "By law, most premium rates may not rise more than 18% a year; the rate for some property, including homes that are not a primary "
                "residence and business property, rises 25% a year until that group's average rate reaches the level the law sets (42 U.S.C. §4015(e)). FloodSmart puts the limit at 18 to 25% a year for most policyholders. It usually does "
                "not apply to new policies, raising your coverage or lowering your deductible can go past it, and fees and surcharges are added on top.",
        "sources": [(FS + "/premiumcosts", "per year for most policyholders. This usually does not apply to new policies.", "curl"),
                    (FS + "/premiumcosts", "Additional charges added to the discounted premium.", "curl"),
                    (FIM, "Most premium rates may not increase by more than 18 percent each year, whether at renewal or by endorsement, except when increasing coverage, decreasing the amount of the deductible", "manual"),
                    ("https://www.govinfo.gov/link/uscode/42/4015?link-type=html", "may not be increased by more than 18 percent each year", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/4015", "shall be increased by 25 percent each year", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/4014", "any residential property which is not the primary residence of an individual", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/4014", "any business property", "curl")]},
    "rr2_zone": {
        "text": "The premium is based on the flood risk of the building. The reason for any one zone is not in this data.",
        "sources": [(FS + "/premiumcosts", "The premium amount is based on the flood risk of the building.", "curl")]},
    "glide": {
        # owner 11-15 review: "statutory discounts ... annual increase cap discount" was jargon a newcomer cannot parse; same rule, plain words
        "text": "Some policies pay less than FEMA's full-risk premium because of discounts set by law. Except for the Emergency Program discount, "
                "those discounts shrink a little at each renewal, within the yearly cap on increases, until the policy reaches its full-risk premium.",
        "sources": [(FS + "/premiumcosts", "Limits annual premium increases to a set percentage.", "curl"),
                    (FS + "/premiumcosts", "after subtracting statutory discounts from the full-risk premium", "curl"),
                    (FIM, "gradually phase out through a statutory annual increase cap discount", "manual")]},
    "rr2_start": {   # risk-rating-2 guide 11-13: FEMA's Risk Rating 2.0 fact sheet (April 2025 PDF), read raw 2026-11-13
        "text": "Under Risk Rating 2.0, FEMA calculates premiums from the value of the home and the property's own flood risk. "
                "New NFIP policies beginning Oct. 1, 2021, and all policies renewing on or after April 1, 2022, are subject to it; "
                "a policyholder whose premium goes down moves to the lower rate at the first renewal.",
        "sources": [(RR2, "based on the value of their home and individual property", "manual"),
                    (RR2, "New policies beginning Oct. 1, 2021 will be subject to the Risk Rating 2.0 rating methodology", "manual"),
                    (RR2, "All policies renewing on or after April 1, 2022 will be subject to the Risk Rating 2.0 rating", "manual"),
                    (RR2, "will transition to the lower rate immediately at the first renewal of their policy", "manual")]},
    "nfip_not_sold": {   # 2026-10-28 site review: 34 Louisiana, 137 Texas communities are not in the NFIP; the page called them "no discount"
        "text": "Federal flood insurance (NFIP) is sold only in communities that take part in the NFIP; in a community that "
                "has not joined, or once a suspension takes effect, no one can buy an NFIP policy.",
        "sources": [("https://www.floodsmart.gov/get-insured/eligibility",
                     "You can get flood insurance from the National Flood Insurance Program if your city or town participates in the NFIP", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/4012", "shall make flood insurance available in only those States or areas", "curl"),
                    ("https://www.law.cornell.edu/cfr/text/44/59.24", "loss of eligibility for the sale of flood insurance", "curl")]},
    "crs_auto": {
        "text": "It is automatic, already in these prices, and the same in every flood zone.",
        "sources": [(FS + "/premiumcosts", "Applies to all eligible policies within the community, regardless of flood zone.", "curl")]},
    "cwop": {
        "text": "FEMA's claim records give a reason when a building claim has no recorded payment, such as damage less than the deductible, not an actual flood, "
                "seepage or backed-up drains.",
        "sources": [("https://www.fema.gov/api/open/v1/OpenFemaDataSetFields?$filter=name%20eq%20%27nonPaymentReasonBuilding%27", "Claim denied that was less than deductible", "curl"),
                    ("https://www.fema.gov/api/open/v1/OpenFemaDataSetFields?$filter=name%20eq%20%27nonPaymentReasonBuilding%27", "Not actual flood", "curl")]},
    "nfip_lapse": {
        "text": "Congress has to keep renewing the NFIP's authority. During a lapse, NFIP policies cannot be bought, renewed or increased until "
                "the authority returns. Policies already in force run to their expiration date and claims on them are still handled, though "
                "FEMA says the money to pay claims may be limited.",
        # no dates on purpose: true before, during and after any lapse. FEMA bulletin W-23012 (Sept. 25, 2023); pdf, so read by hand.
        "sources": [("https://www.law.cornell.edu/uscode/text/42/4026", "No new contract for flood insurance under this chapter shall be entered into after", "curl"),
                    ("https://agents.floodsmart.gov/sites/default/files/bulletins/W-23012/w-23012.pdf", "will remain in force until their expiration date", "manual"),
                    ("https://agents.floodsmart.gov/sites/default/files/bulletins/W-23012/w-23012.pdf", "funding available to pay claims may be limited", "manual")]},
    "zone_labels": {
        "text": "Every zone starting with A or V is high-risk; A1 to A30 and AE are the same kind of area (44 CFR §64.3).",
        "sources": [(CFR64, "A1-30, AE Area of special flood hazard with water surface elevations determined", "curl")]},
    "zone_price": {
        "text": "A federally regulated lender must require coverage for the term of a loan on a building in a high-risk zone where NFIP cover is available; your premium is based on your own building's flood risk.",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm", "regulated lending institutions", "curl"),
                    (FS + "/premiumcosts", "The premium amount is based on the flood risk of the building.", "curl"),
                    (FS + "/premiumcosts", "after subtracting statutory discounts from the full-risk premium", "curl")]},
    "crs_what": {
        "text": "FEMA's Community Rating System gives a discount to eligible policies in communities that take part.",
        "sources": [(FS + "/premiumcosts", "Discount if building is in a participating Community Rating System community and meets eligibility requirements.", "curl")]},
    "other_buyers": {
        "text": "The NFIP also offers policies for renters and businesses.",
        "sources": [(FS + "/get-insured/buy-a-policy", "offers flood insurance policies for homeowners, renters and businesses", "curl")]},
    "zone_ae": {
        "text": "Zone AE is a high-risk area: land with a 1 percent or greater chance of flooding in any given year, where FEMA has "
                "worked out how high the water from that flood would reach (44 CFR §59.1, §64.3).",
        "sources": [(CFR64, "with water surface elevations determined", "curl"),
                    (CFR59, "subject to a 1 percent or greater chance of flooding in any given year", "curl")]},
    "zone_ve": {
        # 11-15: 64.3 calls VE a "coastal high hazard area"; 59.1 defines that term (offshore to the dune, or high velocity wave
        # action), read raw this session. Edge: "any other area" is kept as "or other land", never "all VE land has waves".
        "text": "Zone VE is a coastal high hazard area: land with a 1 percent or greater chance of flooding in any given year, inundated by "
                "tidal floods with velocity, where FEMA has worked out how high the water would reach. The regulation's coastal high hazard area runs from offshore "
                "to the inland limit of a primary frontal dune along an open coast, plus other land subject to high velocity wave action from storms or seismic sources (44 CFR §59.1, §64.3).",
        "sources": [(CFR64, "with water surface elevations determined and with velocity, that is inundated by tidal floods (coastal high hazard area)", "curl"),
                    (CFR59, "subject to a 1 percent or greater chance of flooding in any given year", "curl"),
                    (CFR59, "extending from offshore to the inland limit of a primary frontal dune along an open coast and any other area subject to high velocity wave action from storms or seismic sources", "curl")]},
    "zone_x": {
        "text": "Zone X is outside the high-risk zones and covers two kinds of land (44 CFR §64.3). FEMA labels the moderate-hazard kind Zone B or Zone X (shaded): land between the limits of the 1 percent flood and the "
                "0.2-percent-annual-chance (500-year) flood. It labels the minimal-hazard kind Zone C or Zone X (unshaded): land outside the "
                "high-risk areas and higher than the 0.2-percent-annual-chance flood.",
        "sources": [(CFR64, "B, X Areas of moderate flood hazards", "curl"),
                    (CFR64, "C, X Area of minimal hazards", "curl"),
                    ("https://www.fema.gov/about/glossary/flood-zones", "Moderate flood hazard areas, labeled Zone B or Zone X (shaded) are also shown on the FIRM, and are the areas between the limits of the base flood and the 0.2-percent-annual-chance (or 500-year) flood", "browser"),
                    ("https://www.fema.gov/about/glossary/flood-zones", "the areas outside the SFHA and higher than the elevation of the 0.2-percent-annual-chance flood, are labeled Zone C or Zone X (unshaded)", "browser")]},
    "zone_a": {
        "text": "Zone A is a high-risk area: land with a 1 percent or greater chance of flooding in any given year, where FEMA has "
                "not worked out how high the water from that flood would reach (44 CFR §59.1, §64.3).",
        "sources": [(CFR64, "Area of special flood hazard without water surface elevations determined", "curl"),
                    (CFR59, "subject to a 1 percent or greater chance of flooding in any given year", "curl")]},
    "zone_ao": {
        # 11-15 ("flood zone ao" searches): 59.1's "area of shallow flooding" read raw this session; "ponding or sheet flow" is the
        # regulation's for AO and AH alike, so neither page claims one kind only. Edge: recheck fails if the eCFR wording moves.
        "text": "Zone AO is a high-risk area of shallow flooding: a 1 percent or greater annual chance of flooding to an average depth of 1 to 3 feet, "
                "where no clearly defined channel exists and the path of flooding is unpredictable. Such flooding is characterized by ponding or sheet flow (44 CFR §59.1, §64.3).",
        "sources": [(CFR64, "Area of special flood hazards having shallow water depths and/or unpredictable flow paths between (1) and (3) ft", "curl"),
                    (CFR59, "with a 1 percent or greater annual chance of flooding to an average depth of 1 to 3 feet where a clearly defined channel does not exist, where the path of flooding is unpredictable", "curl"),
                    (CFR59, "Such flooding is characterized by ponding or sheet flow", "curl")]},
    "zone_ah": {
        "text": "Zone AH is a high-risk area of shallow flooding: a 1 percent or greater annual chance of flooding to an average depth of 1 to 3 feet, "
                "where FEMA has worked out how high the water would reach. Such flooding is characterized by ponding or sheet flow (44 CFR §59.1, §64.3).",
        "sources": [(CFR64, "between (1) and (3) feet, and with water surface elevations determined", "curl"),
                    (CFR59, "with a 1 percent or greater annual chance of flooding to an average depth of 1 to 3 feet", "curl"),
                    (CFR59, "Such flooding is characterized by ponding or sheet flow", "curl")]},
    "zone_d": {
        "text": "Zone D is land where flood hazards are possible but have not been determined (44 CFR §64.3).",
        "sources": [(CFR64, "D Area of undetermined but possible, flood hazards", "curl")]},
    "seller_assign": {
        "text": "Buying a finished home with an NFIP building policy: the seller can assign the policy to you in writing when title transfers.",
        "sources": [(CFR61, "You may assign this policy in writing when you transfer title of your property to someone else", "curl")]},
    "lender_amount": {
        "text": "Where a federally regulated lender must require it, the legal minimum is the loan balance or the NFIP's limit for the property, whichever is less (42 U.S.C. §4012a(b)).",
        "sources": [(USC4012A, "in an amount at least equal to the outstanding principal balance of the loan or the maximum limit of coverage", "curl")]},
    "lender_force": {
        "text": "If such a lender notifies you that coverage is needed and you do not buy it within 45 days, the lender must buy it for you and "
                "can charge you for it (42 U.S.C. §4012a(e)).",
        "sources": [(USC4012A, "within 45 days after notification under paragraph (1), the lender or servicer for the loan shall purchase the insurance", "curl")]},
    "zone_review": {
        "text": "If you think a lender's high-risk-zone finding is wrong, you and the lender together can ask FEMA to review it within 45 days of "
                "the lender's notice; a fee applies (44 CFR §65.17).",
        "sources": [("https://www.law.cornell.edu/cfr/text/44/65.17", "must be submitted within 45 days of the lender's notification to the borrower", "curl")]},
    "floodway": {   # top-3 compare 11-09 (AE results explain the floodway); 44 CFR 59.1 and 60.3(d)(3)-(4) read raw 11-09 (eCFR, curl --compressed)
        "text": "Some AE areas also have a regulatory floodway: the river channel and the land beside it that must be kept clear to carry the base flood (44 CFR §59.1). "
                "Where a community has adopted one, it must prohibit fill, new construction, substantial improvements and other development there unless engineering "
                "analysis shows the work would not raise flood levels during the base flood, or the community first applies for a map and floodway revision (44 CFR §60.3(d)).",
        "sources": [(CFR59, "Regulatory floodway means the channel of a river or other watercourse and the adjacent land areas that must be reserved in order to discharge the base flood", "curl"),
                    (CFR60, "Prohibit encroachments, including fill, new construction, substantial improvements, and other development within the adopted regulatory floodway unless it has been demonstrated through hydrologic and hydraulic analyses", "curl"),
                    (CFR60, "would not result in any increase in flood levels within the community during the occurrence of the base flood discharge", "curl"),
                    (CFR60, "provided that the community first applies for a conditional FIRM and floodway revision", "curl")]},
    "odds_30": {
        "text": "A 1 percent or greater chance a year works out to a 26% or greater chance of at least one such flood over 30 years.",
        # arithmetic, tested in test_calc.py: 1 - 0.99**30 = 0.2603; the 1 percent is the regulation's
        "sources": [(CFR59, "subject to a 1 percent or greater chance of flooding in any given year", "curl")]},
    "fema_asis": {   # address tool (owner 11-06): FEMA's own disclaimer on the NFHL, read raw 11-06 from its catalog record
        "text": "FEMA provides its flood map data \"as is\", with no guarantee of its accuracy.",
        "sources": [("https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json",
                     "express or implied guarantees of accuracy of the data", "curl")]},
    "bfe": {   # debate 11-05: readers see elevations on the map; the term comes from 59.1, read raw 11-06
        "text": "In zones AE, AH and VE, FEMA has worked out the water surface elevation of the base flood: the flood level that has a 1 "
                "percent or greater chance of occurrence in any given year (44 CFR §59.1, §64.3).",
        "sources": [(CFR59, "water surface elevations of the base flood, that is, the flood level that has a one percent or greater chance of occurrence in any given year", "curl"),
                    (CFR64, "with water surface elevations determined", "curl")]},
    "loma": {   # 44 CFR 70.1 and 70.5, read raw 11-06; scope: a property shown in an A or V zone by how the line was drawn
        "text": "An owner or renter who believes the property was put in a high-risk A or V zone by mistake, because of how the zone line "
                "was drawn against streets or other features, can send FEMA technical information and ask for a Letter of Map Amendment, "
                "which identifies the property to be excluded from the zone (44 CFR part 70).",
        "sources": [(CFR70, "believes his property has been inadvertently included in designated A, AO, A1-30, AE, AH, A99", "curl"),
                    (CFR70, "the transposition of the curvilinear line to either street or to other readily identifiable features", "curl"),
                    (CFR70, "The identification of the property to be excluded from a designated", "curl")]},
    "loma_fee": {   # 44 CFR 72.5, read raw (eCFR, curl --compressed) 11-07
        "text": "FEMA charges no review or processing fee for a Letter of Map Amendment request (44 CFR §72.5).",
        "sources": [(CFR72, "Requesters are exempt from submitting review and processing fees for", "curl"),
                    (CFR72, "Requests for a Letter of Map Amendment (LOMA)", "curl")]},
    "lomr_def": {   # 44 CFR 72.1 and 72.2, read raw (eCFR versioner XML, curl --compressed) 11-14; LOMA guide
        "text": "A Letter of Map Revision (LOMR) is FEMA's change to the flood map itself. It is generally based on physical work that changes how a river "
                "or other flooding source behaves, such as changing a channel or building a bridge, culvert or levee, and it officially revises the map (44 CFR §72.1, §72.2).",
        "sources": [(CFR72, "A LOMR is FEMA's modification to an effective Flood Insurance Rate Map (FIRM)", "curl"),
                    (CFR72, "LOMRs are generally based on the implementation of physical measures that affect the hydrologic or hydraulic characteristics of a flooding source", "curl"),
                    (CFR72, "modification of a channel; construction or modification of a bridge, culvert, levee, or similar measure", "curl"),
                    (CFR72, "The LOMR officially revises the FIRM", "curl")]},
    "lomr_f_def": {   # 44 CFR 72.2, read raw 11-14
        "text": "A Letter of Map Revision Based on Fill (LOMR-F) is FEMA's change to the high-risk zone shown on the map based on fill placed outside the regulatory floodway (44 CFR §72.2).",
        "sources": [(CFR72, "A LOMR-F is FEMA's modification of the SFHA shown on the FIRM based on the placement of fill outside the existing regulatory floodway", "curl")]},
    "lomr_fees": {   # 44 CFR 72.1 and 72.5, read raw 11-14: LOMR/LOMR-F come under cost recovery; some map-change requests are exempt
        "text": "FEMA's review fees cover requests for a LOMR or a LOMR-F; requests based on mapping or study errors are among those exempt (44 CFR §72.1, §72.5).",
        "sources": [(CFR72, "cost-recovery procedures for the engineering review and administrative processing", "curl"),
                    (CFR72, "Letters of Map Revision Based on Fill (LOMR-Fs), Letters of Map Revision (LOMRs)", "curl"),
                    (CFR72, "Requests for map changes based on mapping or study analysis errors", "curl")]},
    "ec_get": {   # FloodSmart (FEMA's NFIP site), read raw 11-08 (curl --compressed): who completes one, where one may be on file
        "text": "Your home may already have an Elevation Certificate on file with your community: ask your local floodplain manager, "
                "often in the city or county building, permitting or engineering department. If none is on file, a land surveyor, "
                "engineer or architect completes one.",
        "sources": [("https://www.floodsmart.gov/get-insured/elevation-certificates", "on file with your community", "curl"),
                    ("https://www.floodsmart.gov/get-insured/elevation-certificates", "contact your local floodplain manager", "curl"),
                    ("https://www.floodsmart.gov/get-insured/elevation-certificates", "land surveyor, engineer or architect to complete one", "curl")]},
    "loma_online": {   # read raw from a US runner 11-07 (fema-probe links job; FEMA refuses the laptop): manual-rule-read
        "text": "FEMA's <a href='https://hazards.fema.gov/femaportal/onlinelomc/signin' rel='noopener'>Online LOMC site</a> lets home owners or their representatives ask FEMA for a Letter of Map Change.",
        "sources": [(LOMC, "The Online LOMC web application allows home owners or their designated representatives to easily request a Letter of Map Change (LOMC)", "manual")]},
    "prelim": {   # read raw from a US runner 11-07 (fema-probe links job): manual-rule-read
        "text": "FEMA's <a href='https://hazards.fema.gov/femaportal/prelimdownload/' rel='noopener'>preliminary flood map data</a> give an early look at a home's or community's projected flood risk and may include new or revised flood maps.",
        "sources": [(PRELIM, "Preliminary flood hazard data (preliminary data) provide the public an early look at their home or community", "manual"),
                    (PRELIM, "Preliminary data may include: new or revised Flood Insurance Rate Maps (FIRM)", "manual")]},
    "flood_def": {
        "text": "The policy generally counts a flood only when water covers two or more acres of normally dry land or two or more properties, "
                "one of them yours.",
        "sources": [(CFR61, "two or more acres of normally dry land area or of two or more properties", "curl")]},
    "not_covered": {
        "text": "The NFIP's standard policy for homes (the Dwelling Form) does not pay for a hotel or other living costs while you are out of the home, or for belongings outside the "
                "building, and it limits what it pays for in a basement. Belongings are paid at actual cash value (their used value), not the cost of new ones.",
        "sources": [(CFR61, "Dwelling Form of the Standard Flood Insurance Policy", "curl"),   # hater r97: the form's own name, read 11-08
                    (CFR61, "Any additional living expenses incurred while the insured building is being repaired", "curl"),
                    (CFR61, "Personal property not inside", "curl"),
                    ("https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61", "in a basement regardless of the zone", "curl"),
                    ("https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61", "subject to actual cash value", "curl")]},
    "claim_appeal": {
        "text": "NFIP claim denied? You can appeal to FEMA within 60 days of the date on the denial letter, and you can sue within one year of the denial. "
                "An appeal does not extend that year.",
        "sources": [(FS + "/recover/appeal-a-claim", "within 60 days of the date written on your denial letter", "curl"),
                    (FS + "/recover/appeal-a-claim", "does not extend the one-year period", "curl")]},
    "bfe_floor": {   # top-3 compare 11-09: every AE result states the build rule; 44 CFR 60.3(c)(2) read raw 11-09 (eCFR, curl --compressed)
        "text": "Where FEMA has published final flood elevations, a community in the NFIP must require new homes, and homes being substantially improved, in zones AE and AH "
                "to have the lowest floor, including the basement, at or above the base flood level, unless FEMA has granted the community a basement exception (44 CFR §60.3(c)(2)).",
        "sources": [(CFR60, "When the Federal Insurance Administrator has provided a notice of final flood elevations", "curl"),
                    (CFR60, "Require that all new construction and substantial improvements of residential structures within Zones A1-30, AE and AH zones on the community's FIRM have the lowest floor (including basement) elevated to or above the base flood level", "curl")]},
    "substantial_damage": {
        # hater r124 (11-09): "local rules can require elevating" had no quote and "repairs would cost" dropped 59.1's cost basis; rewritten from 59.1 and
        # SFIP Coverage D read raw 11-09 (eCFR, curl --compressed); the unclear "local official's letter" clause and its manual PDF source cut
        "text": "Under the NFIP's rules, a building is substantially damaged when restoring it to its condition before the damage would cost 50 percent or more of its "
                "market value before the damage (44 CFR §59.1). An NFIP policy with building coverage pays up to $30,000 under Increased Cost of Compliance to comply "
                "with a state or local floodplain law when repairing a flood-damaged building.",
        "sources": [(CFR59, "the cost of restoring the structure to its before damaged condition would equal or exceed 50 percent of the market value of the structure before the damage occurred", "curl"),
                    (CFR61, "We will pay you up to $30,000 under this Coverage D", "curl"),
                    (CFR61, "which only applies to policies with building coverage (Coverage A)", "curl"),
                    (CFR61, "This policy pays you to comply with a State or local floodplain management law or ordinance affecting repair or reconstruction of a building suffering flood damage", "curl")]},
    "lapse_discount": {
        "text": "Paying a renewal 30 days or more after the policy expires causes a lapse in coverage. You then need a new application, and the lapse may cost you "
                "statutory discounts (what keeps a bill below full risk), including the yearly cap.",
        "sources": [(FIM, "causes a lapse in coverage that may result in the loss of Statutory Discounts including the Annual Increase Cap", "manual"),
                    (FIM, "A new application is required", "manual")]},
    "surcharge": {
        "text": "Property that is not your primary residence, such as a second home, a rental you own or a non-residential building, pays a higher federal surcharge: $250 a year, against $25 for a primary home.",
        "sources": [("https://www.law.cornell.edu/uscode/text/42/4015a", "(1) $25, except as provided in paragraph (2); and (2) $250, in the case of a policy for any property that is", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/4015a", "a residential property that is not the primar", "curl")]},
    "tx_tenant_notice": {   # audit 11-10 (renters top 3: TDI); Texas Property Code 92.0135 read raw 11-10 from tcss.legis.texas.gov (curl)
        "text": "In Texas, a landlord must give a tenant a written notice saying whether the landlord is aware the home is in a 100-year floodplain, and, if the landlord knows "
                "flooding damaged it at least once in the five years before the lease, a notice saying whether the landlord is aware it flooded in that time. Some leases are exempt, including leases shorter than 30 days "
                "(Texas Property Code §92.0135).",
        "sources": [("https://tcss.legis.texas.gov/resources/PR/htm/PR.92.htm", "A landlord shall provide to a tenant a written notice substantially equivalent to the following", "curl"),
                    ("https://tcss.legis.texas.gov/resources/PR/htm/PR.92.htm", "is located in a 100-year floodplain", "curl"),
                    ("https://tcss.legis.texas.gov/resources/PR/htm/PR.92.htm", "If a landlord knows that flooding has damaged any portion of a dwelling at least once during the five-year period immediately preceding the effective date of the lease", "curl"),
                    ("https://tcss.legis.texas.gov/resources/PR/htm/PR.92.htm", "a lease with a term of less than 30 days", "curl")]},
    "harris_maapnext": {   # audit 11-10 (Harris top 3 carry the 2026 draft maps); Harris County Flood Control District MAAPnext site read raw 11-10 (curl)
        "text": "Harris County's flood control district shares draft flood maps on its <a href='https://www.maapnext.org/' rel='noopener'>MAAPnext site</a>. It says they are not final "
                "and cannot be used for insurance or regulatory decisions, and that FEMA is expected to release preliminary flood maps after its federal review.",
        "sources": [("https://www.maapnext.org/", "MAAPnext flood maps are currently in draft form", "curl"),
                    ("https://www.maapnext.org/", "These draft maps are not final, cannot be used for insurance or regulatory decisions", "curl"),
                    ("https://www.maapnext.org/", "FEMA is anticipated to release Preliminary Flood Insurance Rate Maps (FIRMs) after completion of its federal review", "curl")]},
    # 11-15 official map viewers (one sourced sentence each, linked on the viewer's own name). Edge cases:
    # - the page moves or the wording changes: recheck.py fails the curl excerpt (Pinellas); NJ is Incapsula-walled, so "manual"
    #   and state/manual-rule-read.json dates it (recheck fails it after 183 days)
    # - shown on the wrong page: build_page prints nj only when IS_STATE and state NJ, pinellas only on geoid 12103 (checked in dist)
    # - overclaim: the NJ tool "does not calculate actual risk" and no-indicator is not no-risk, both kept in the sentence
    # - Florida (FDEM statewide viewer) skipped: no floridadisaster.org page naming one could be read raw 11-15 (floodplain pages
    #   link none; Know Your Zone is evacuation zones), and a vendor/help-center page is not the official source
    "nj_flood_tool": {   # NJDEP climatechange/flood-tool page read raw 11-15 in a browser (curl gets an Incapsula wall)
        "text": "New Jersey's environmental agency (NJDEP) offers <a href='https://dep.nj.gov/climatechange/flood-tool/' rel='noopener'>New Jersey's Flood Indicator Tool</a>, "
                "a screening tool that shows indicators of potential flood risk on or near a property, among them FEMA flood zones and State Flood Hazard Areas. "
                "NJDEP says it does not calculate actual risk, and that the absence of indicators does not mean a property is free from flood risk.",
        "sources": [("https://dep.nj.gov/climatechange/flood-tool/", "This screening tool provides users with information regarding the presence of indicators of potential flood risk on or near a property of interest", "manual"),
                    ("https://dep.nj.gov/climatechange/flood-tool/", "Flood indicators include waterbodies, watercourses, FEMA Flood Zones, and State Flood Hazard Areas", "manual"),
                    ("https://dep.nj.gov/climatechange/flood-tool/", "This tool does not calculate actual risk", "manual"),
                    ("https://dep.nj.gov/climatechange/flood-tool/", "the absence of indicators does not mean that a property is free from flood risk", "manual")]},
    "pinellas_floodmaps": {   # pinellas.gov/floodmaps/ (pinellas.gov/flood-maps redirects there) read raw 11-15 (curl)
        "text": "Pinellas County points residents to its own <a href='https://floodmaps.pinellascounty.org/' rel='noopener'>Pinellas County Flood Map Service</a> to find their flood risk. "
                "The county also maps County Flood Hazard Areas, land with a 1% or greater chance of flooding in any given year, which it treats as high-risk and subject to specific regulation, like FEMA's high-risk zones.",
        "sources": [("https://pinellas.gov/floodmaps/", "Visit the Pinellas County Flood Map Service to find your flood risk", "curl"),
                    ("https://pinellas.gov/floodmaps/", "Pinellas County Flood Hazard Areas (FHAs) are areas that have a 1% or greater chance of flooding in any given year", "curl"),
                    ("https://pinellas.gov/floodmaps/", "Like with the FEMA SFHA, these floodplains are also considered high-risk areas and subject to specific regulation", "curl")]},
    # 11-15 /flood-zone-map/: what a blank answer means and why a pin can differ from the lot. Edge cases:
    # - the catalog JSON breaks lines with a literal "\n": every excerpt sits inside one line (checked against recheck's own
    #   normalization 11-15), else recheck would report a false "excerpt gone"
    # - overclaim: FEMA says other products "may" cover a gap, so the page says "may"; the lot/building line names only what
    #   44 CFR 70 says (a portion of a property; parcel or structure compared), no claim about any one address
    "nfhl_coverage": {   # FEMA's NFHL catalog record (same item as fema_asis), read raw 11-15 (curl)
        "text": "FEMA says its digital flood map data covers over 90 percent of the U.S. population and new data is added continuously; for areas it does not cover, "
                "other FEMA flood hazard products may. The simplest way to reach FEMA's flood hazard data is <a href='https://msc.fema.gov/portal/home' rel='noopener'>FEMA's Map Service Center</a>.",
        "sources": [("https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json", "NFHL digital data covers over 90", "curl"),
                    ("https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json", "percent of the U.S. population. New and revised data is being added", "curl"),
                    ("https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json", "If you need information for areas not covered by the NFHL", "curl"),
                    ("https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json", "which provide coverage for those areas", "curl"),
                    ("https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json", "simplest way for you to access the flood hazard data", "curl")]},
    "lot_vs_building": {   # 44 CFR 70.5 and 70.9, read raw 11-15 (eCFR versioner XML, curl --compressed)
        "text": "FEMA's rules allow that only a portion of a property may be in a high-risk zone: when FEMA reviews a property's zone, it compares either the ground "
                "of an entire legally defined parcel of land or the ground next to a structure with the elevation of the base flood (44 CFR §70.5, §70.9).",
        "sources": [(CFR70, "build one or more structures on a portion of property that may be included inadvertently in a Special Flood Hazard Area", "curl"),
                    (CFR70, "the ground elevations of an entire legally defined parcel of land or the elevation of the lowest adjacent grade to a structure with the elevation of the base flood", "curl")]},
    "renters_excl": {   # renters page 11-15: FloodSmart buy-a-policy read raw (curl); "most" kept (the source's strength)
        "text": "FEMA's FloodSmart site says most homeowners and renters insurance does not cover flood damage.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Most homeowners and renters insurance does not cover flood damage", "curl")]},
    "tx_twia": {   # Texas only
        # review 11-15: TWIA spelled out once (name read raw from twia.org 11-15)
        "text": "In Texas, a windstorm policy from the Texas Windstorm Insurance Association (TWIA) requires flood insurance when any part of the property is in a V, VE or V1-V30 zone, NFIP cover "
                "is available for it, and the structure was built, altered, remodeled or enlarged after September 1, 2009.",
        "sources": [("https://www.twia.org/", "Texas Windstorm Insurance Association", "curl"),
                    ("https://www.twia.org/flood-requirement", "Flood insurance is required when all three of the following conditions are met", "curl"),
                    ("https://www.twia.org/flood-requirement", "constructed, altered, remodeled, or enlarged after September 1, 2009", "curl")]},
    "fl_disclosure": {   # Florida only
        "text": "In Florida, a home seller must give the buyer a flood disclosure at or before the sales contract, saying whether the seller knows of "
                "flood damage during their ownership, filed a flood claim, or received flood aid (s. 689.302, F.S.).",
        "sources": [("https://www.flsenate.gov/Laws/Statutes/2025/689.302", "at or before the time the sales contract is executed", "curl"),
                    ("https://www.flsenate.gov/Laws/Statutes/2025/689.302", "relating to flood damage on the property", "curl")]},
    "wind_excl": {   # 11-03 Search Console: "hurricane insurance cost" queries; CFR (current) and FEMA's fact sheet agree on wind
        "text": "Hurricanes can cause both wind and flood damage. A standard NFIP policy does not pay for wind damage, including rain blown in by "
                "wind or water coming through a roof the wind damaged; it does pay for water entering from the ground up, such as storm surge. "
                "Other policies, such as homeowners policies, may cover wind-driven rain, so you will likely file claims with both.",
        "sources": [(CFR61, "Theft, fire, explosion, wind, or windstorm", "curl"),
                    (WIND_FS, "considered wind-driven rain and is not covered under your flood insurance policy", "manual"),
                    (WIND_FS, "water entering your home from the ground up due to storm surge", "manual"),
                    (WIND_FS, "may cover damage from other perils, such as wind-driven rain", "manual"),
                    (WIND_FS, "You will likely need to file insurance claims with both entities", "manual")]},
    "ia_partial": {
        "text": "FEMA disaster aid helps with uninsured and underinsured losses, and is separate from NFIP insurance.",
        "sources": [(IA_META, "uninsured and underinsured personal property losses", "curl")]},
    # ---- owner 11-15 plain-words rewrites for the national pages: same sources as the long rule each one shortens; the long rules
    # stay as they are on county pages (template text changes once a day, batched) ----
    "start_loan_plain": {   # buying guide; start_loan's sources (FIM Table 10); 10 days first, as on the home page (howto_answer)
        "text": "Bought while taking out, increasing, extending or renewing a mortgage, coverage can start at the loan closing. The insurer must get "
                "the form and full amount due within 10 calendar days of closing, or within 30 if your lender, title company or settlement attorney pays. "
                "Contents-only coverage qualifies only if the "   # review 11-15: "Miss that ..." sentence cut, no source quote held it
                "contents are part of the security for the loan.",
        "sources": [(FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making, increasing, extending or renewing a mortgage", "curl"),
                    (FIM, "Contents-only policies and endorsements can only be eligible for the loan exception if the contents are part of the security for a loan", "manual"),
                    (FIM, "If the lender, title company, or settlement attorney pays the premium", "manual"),
                    (FIM, "within 30 calendar days from the closing", "manual"),
                    (FIM, "within 10 calendar days from the loan transaction closing", "manual"),
                    (FIM, "The effective date will be the date and time of the loan closing", "manual")]},
    "zone_codes_list": {   # flood-zone-map and zone pages: zone_codes as a list; review 11-15: "B and X ... C and X" read as a contradiction.
        # 44 CFR 64.3 lists "B, X" and "C, X" only; the shaded/unshaded split is FEMA's flood zone glossary (zone_x's source), so both are named
        "text": "<ul><li><b>A, AE, A1–A30:</b> high-risk.</li><li><b>AO, AH:</b> high-risk, shallow flooding.</li>"
                "<li><b>A99:</b> high-risk, behind a flood barrier FEMA treats as complete.</li>"
                "<li><b>V, VE, V1–V30:</b> coastal high-risk, flooded by tides with fast-moving water.</li>"
                "<li><b>B and shaded X:</b> moderate flood hazard.</li><li><b>C and unshaded X:</b> minimal flood hazard.</li>"
                "<li><b>D:</b> flood hazard possible but not determined.</li></ul>"
                "<p class='mut'>Zone codes from 44 CFR §64.3; the shaded and unshaded X labels from FEMA's flood zone glossary.</p>",
        "sources": [(CFR64, "B, X Areas of moderate flood hazards", "curl"),
                    (CFR64, "C, X Area of minimal hazards", "curl"),
                    (CFR64, "D Area of undetermined but possible, flood hazards", "curl"),
                    (CFR64, "and with velocity, that is inundated by tidal floods (coastal high hazard area)", "curl"),
                    (CFR64, "A99 Area of special flood hazard where enough progress has been made on a protective system", "curl"),
                    ("https://www.fema.gov/about/glossary/flood-zones", "Moderate flood hazard areas, labeled Zone B or Zone X (shaded)", "browser"),
                    ("https://www.fema.gov/about/glossary/flood-zones", "are labeled Zone C or Zone X (unshaded)", "browser")]},
    "private_plain": {   # private guide opening; private_accept's statute, in plain words; "must" kept (the statute's "shall ... direct")
        "text": "Under federal law, regulated lenders are directed to accept a private flood policy in place of an NFIP policy when its coverage "
                "meets the federal flood insurance requirement (42 U.S.C. §4012a(b)(1)(B)).",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "shall by regulation direct regulated lending institutions", "curl"),
                    ("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "to accept private flood insurance as satisfaction of the flood insurance coverage requirement", "curl")]},
    "condo_layers": {   # condo guide opening: condo_rcbap + condo_contents in one plain answer (same FEMA brochure and postcard)
        "text": "Condo flood insurance comes in two layers. The condominium association can buy one NFIP policy for the building. That policy does "
                "not cover your own belongings: for those, the NFIP offers a contents-only policy with a $100,000 coverage limit.",
        "sources": [(CONDO_B, "is available to condominium associations to insure against direct physical damage to your building from a flood", "manual"),
                    (CONDO_P, "but it does not cover your personal belongings", "manual"),
                    (CONDO_P, "offers a contents-only flood insurance policy with a $100,000 coverage limit", "manual")]},
    "buyer_lender": {   # buying guide opening: purchase_answer + zone_price in a buyer's words
        "text": "If the house is in a high-risk zone (A or V) and your mortgage is federally regulated or backed, the lender must require flood "
                "insurance (42 U.S.C. §4012a). Outside those zones, a lender may still require it.",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "regulated lending institutions", "curl"),
                    ("https://www.federalreserve.gov/frrs/regulations/interagency-questions-and-answers-regarding-flood-insurance.htm",
                     "a lender may require flood insurance as a condition of making the loan, as a matter of safety and soundness", "curl")]},
    # ---- contents guide 11-15 (KWP "flood insurance contents coverage"): 44 CFR 61 (eCFR, curl --compressed) and FloodSmart
    # buy-a-policy read raw this session; Dwelling Form = Part 61 Appendix A(1) ----
    "contents_separate": {
        "text": "NFIP building coverage and contents coverage are bought separately. The NFIP's standard home policy covers your belongings only if you bought "
                "contents coverage, which the policy calls personal property coverage (44 CFR §61.3 and Part 61, Appendix A(1)).",
        "sources": [(CFR61, "Insurance coverage under the Program is available for buildings and their contents. Coverage for each may be purchased separately.", "curl"),
                    (CFR61, "If you have purchased personal property coverage, we insure against direct physical loss by or from flood to personal property inside a building at the described location", "curl")]},
    "contents_what": {
        "text": "FloodSmart lists what contents coverage pays for: clothing, furniture and electronic equipment; curtains; a clothes washer and dryer; "
                "portable and window air conditioners; a microwave; carpet installed over wood floors; and valuable items such as original artwork and furs, "
                "up to $2,500. For a home, contents coverage goes up to <b>$100,000</b>.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Covers physical damage to the personal property inside the building: Clothing, furniture and electronic equipment.", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Portable and window air conditioners. Microwave. Carpet installed over wood floors.", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Valuable items such as original artwork and furs (up to $2,500)", "curl"),
                    (FS + "/get-insured/buy-a-policy", "contents policies cover up to $100,000 of flood damage for belongings kept inside your home", "curl")]},
    "contents_acv": {
        "text": "Belongings are paid at actual cash value: what it costs to replace an item at the time of the loss, less its physical depreciation "
                "(Dwelling Form, 44 CFR Part 61, Appendix A(1)).",
        "sources": [(CFR61, "Actual Cash Value. The cost to replace an insured item of property at the time of loss, less the value of its physical depreciation.", "curl"),
                    (CFR61, "are subject to actual cash value (or in the case of R.4.a.2., below, proportional) loss settlement", "curl"),
                    (CFR61, "e. Personal property. f. Appliances, carpets, and carpet pads.", "curl")]},
    "contents_basement": {
        # r-contents MAJOR 11-15: one 90-word sentence, and the post-1974 scope read as if it covered basements too (the CFR limits
        # basements "regardless of the zone", post-FIRM only for elevated buildings); "not covered" = what "limited to" leaves out
        # review 11-15: definition first; the 65-word elevated-building sentence split in two (same conditions)
        "text": "A basement is a floor below ground level on all sides. "
                "In a basement, in any flood zone, contents coverage pays for only a short list: portable or window air conditioners, "
                "clothes washers and dryers, and food freezers (not walk-in) with the food in them. "
                "Furniture, clothing and other belongings kept there are not covered by contents coverage. "
                "Each item must be installed where it works and, if needed, connected to power. "
                "The same short list applies below the lowest elevated floor of an elevated building in FEMA zones A1-A30, AE, AH, AR, V1-V30 or VE. "
                "That holds only if the building was built or substantially improved after 1974, or after the area's first flood insurance rate map took effect if that was later "
                "(Dwelling Form, 44 CFR Part 61, Appendix A(1)).",
        "sources": [(CFR61, "or in a basement regardless of the zone, is limited to the following items, if installed in their functioning locations and, if necessary for operation, connected to a power source: a. Air conditioning units, portable or window type; b. Clothes washers and dryers; and c. Food freezers, other than walk-in, and food in any freezer.", "curl"),
                    (CFR61, "Coverage for items of property below the lowest elevated floor of an elevated post-FIRM building located in Zones A1-A30, AE, AH, AR, AR/A, AR/AE, AR/AH, AR/A1-A30, V1-V30, or VE", "curl"),
                    (CFR61, "having its floor below ground level on all sides", "curl"),
                    (CFR61, "A building for which construction or substantial improvement occurred after December 31, 1974, or on or after the effective date of an initial Flood Insurance Rate Map (FIRM), whichever is later", "curl")]},
    # ---- coverage guide 11-15 (KWP "what does flood insurance cover", ~7,900/mo): FloodSmart buy-a-policy read raw this session (curl --compressed) ----
    "cover_two": {
        "text": "NFIP (National Flood Insurance Program) flood insurance has two parts: building coverage, for physical damage to the insured building, "
                "and contents coverage, for your belongings inside it. They are typically bought separately and have separate deductibles.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building and contents coverage are typically purchased separately and have separate deductibles", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Covers physical damage to the insured structure", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Covers physical damage to the personal property inside the building", "curl")]},
    "building_what": {
        "text": "FloodSmart lists what building coverage pays for: electrical and plumbing systems; furnaces and water heaters; refrigerators, stoves and built-in "
                "appliances such as dishwashers; permanently installed carpeting, cabinets, paneling and bookcases; window blinds; foundation walls, anchorage "
                "systems and staircases; detached garages; and fuel tanks, well water tanks and pumps, and solar energy equipment. For a home, building coverage "
                "goes up to <b>$250,000</b>.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Covers physical damage to the insured structure: Electrical and plumbing systems. Furnaces and water heaters.", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Refrigerators, stoves and built-in appliances like dishwashers. Permanently installed carpeting. Permanently installed cabinets, paneling and bookcases. Window blinds.", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Foundation walls, anchorage systems and staircases. Detached garages. Fuel tanks, well water tanks and pumps and solar energy equipment.", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000 of flood damage", "curl")]},
    # ---- floodplain guide 11-15 (KWP "floodplain" / "100 year flood", ~11,000/mo): 44 CFR 59.1 read raw this session (eCFR, curl --compressed) ----
    "floodplain_100": {
        "text": "In FEMA's rules, the land in the flood plain with a 1 percent or greater chance of flooding in any given year is the special flood hazard area. "
                "The flood with a one percent chance of being equalled or exceeded in any given year is the base flood, also called the 100-year flood (44 CFR §59.1).",
        "sources": [(CFR59, "Area of special flood hazard is the land in the flood plain within a community subject to a 1 percent or greater chance of flooding in any given year", "curl"),
                    (CFR59, "Base flood means the flood having a one percent chance of being equalled or exceeded in any given year", "curl"),
                    (CFR59, "100-year flood see base flood", "curl")]},
    "floodplain_any": {
        "text": "The same rules use flood plain more widely: any land area that can be flooded by water from any source (44 CFR §59.1).",
        "sources": [(CFR59, "Flood plain or flood-prone area means any land area susceptible to being inundated by water from any source", "curl")]},
    "sfha_zones": {
        "text": "On FEMA's flood insurance rate map, the special flood hazard area usually shows as zones A, AO, AH, A1-30, AE, A99, AR, VO, V1-30, VE or V (44 CFR §59.1).",
        "sources": [(CFR59, "After detailed ratemaking has been completed in preparation for publication of the flood insurance rate map, Zone A usually is refined into Zones A, AO, AH, A1-30, AE, A99, AR, AR/A1-30, AR/AE, AR/AO, AR/AH, AR/A, VO, or V1-30, VE, or V", "curl")]},
}
# owner 11-11 move: the place page keeps the cap's first clause; the full cap rule lives on /nfip/#rules (same sources, no new wording)
RULES["cap_short"] = {"text": RULES["cap"]["text"].split(";")[0] + " (42 U.S.C. §4015(e)).",
                      "sources": [s for s in RULES["cap"]["sources"] if "18 percent" in s[1]]}


def rule(key):
    """The one way the page prints a rule: the registry text inside an element the gate can check
    (a div when the rule is a block such as a tile list, otherwise a span)."""
    tag = "div" if RULES[key]["text"].startswith("<ul") else "span"
    return f'<{tag} data-rule="{key}">{RULES[key]["text"]}</{tag}>'
