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
CFR61 ="https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61"
USC4012A = "https://www.law.cornell.edu/uscode/text/42/4012a"

RULES = {
    "homeowners_excl": {
        "text": "Standard homeowners insurance does not cover flood damage; flood insurance is bought separately, through the "
                "federal NFIP or a private insurer.",
        "sources": [(FS + "/flood-insurance-basics", "most homeowners insurance does not cover flood damage", "curl")]},
    "wait_30": {
        "text": "Most NFIP policies take effect <b>30 days after you buy</b>, so a policy bought today will not cover a "
                "flood this week.",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl")]},
    "wait_exceptions": {
        "text": "Exceptions in FEMA's flood insurance manual: with a loan secured by the insured property (making, increasing, extending or renewing it), coverage "
                "you apply for on or before closing can start at the time of the loan closing if the "
                "insurer gets the form and full amount due in time; the wait is one day when a FEMA map revision newly shows the building in a high-risk zone "
                "and the insurer gets them within 13 months of the revision's effective date.",
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
        "text": "With the map exception the same receipt rules apply, but the start is the next calendar day instead of the 30th; if the insurer receives the form "
                "and full amount due more than 13 months after the map revision's effective date, the 30-day wait applies.",
        "sources": [(FIM, "after 13 months from the effective date of the map revision, the 30-day waiting period applies", "manual"),
                    (FIM, "on the next calendar day after the application date", "manual"),
                    (FIM, "on the next calendar day after the insurer", "manual")]},
    "start_loan": {   # FIM Table 10
        "text": "With the loan exception, coverage starts at the time of the loan closing if the insurer receives the form and full amount due within 30 calendar "
                "days of closing when the lender, title company or settlement attorney pays, or within 10 calendar days when you or anyone else pays; otherwise "
                "the earliest start is the 30th calendar day after the insurer receives them. Contents-only coverage qualifies only if the contents are part of "
                "the security for the loan.",
        "sources": [(FIM, "Contents-only policies and endorsements can only be eligible for the loan exception if the contents are part of the security for a loan", "manual"),
                    (FIM, "If the lender, title company, or settlement attorney pays the premium", "manual"),
                    (FIM, "within 30 calendar days from the closing", "manual"),
                    (FIM, "within 10 calendar days from the loan transaction closing", "manual"),
                    (FIM, "The effective date will be the date and time of the loan closing", "manual")]},
    "howto_answer": {
        "text": "Most policies start <b>30 days</b> after you buy, but there is no wait if you buy it with a new "
                "or refinanced mortgage.",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl"),
                    (FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making", "curl")]},
    "howto_tiles": {
        "text": "<ul class='kv'><li><b>Waiting period</b><span>30 days</span></li>"
                "<li><b>Bought with a new or refinanced mortgage</b><span>No wait</span></li>"
                "<li><b>NFIP building limit</b><span>$250,000</span></li>"
                "<li><b>NFIP contents limit</b><span>$100,000</span></li></ul>",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl"),
                    (FS + "/get-insured/buy-a-policy", "There is no wait if you buy flood insurance while making", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl")]},
    "limits": {
        "text": "NFIP covers up to <b>$250,000</b> on the building and <b>$100,000</b> on contents, which you choose separately "
                "on the same policy.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl"),
                    (FS + "/get-insured/buy-a-policy", "contents policies cover up to $100,000", "curl")]},
    "building_cap": {
        "text": "the NFIP's <b>$250,000</b> building limit.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl")]},
    "how_to_buy": {
        "text": "To buy: call the NFIP at <a href='tel:+18773362627'><b>(877) 336-2627</b></a>, go to <a href='https://www.floodsmart.gov' rel='nofollow "
                "noopener' target='_blank'>FloodSmart.gov</a>, or ask any licensed insurance agent. Every NFIP insurer "
                "offers the same rates.",
        "sources": [(FS + "/contact", "Call the NFIP at (877) 336-2627", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Each one offers the same rates.", "curl")]},
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
    "fl_citizens_short": {   # must not contradict fl_citizens: same two tracks, no "now" that goes stale
        "text": "In Florida, Citizens homes with wind cover need it in a high-risk zone since 2023; outside one, since January 2026 "
                "if they cost $400,000 or more to rebuild, and from January 2027 for all others.",
        "sources": [("https://www.flsenate.gov/Laws/Statutes/2025/627.351",
                     "located within the special flood hazard area defined by the Federal Emergency Management Agency must have flood coverage in place", "curl"),
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
                "coastal high-risk with waves; B and shaded X are moderate risk; C and unshaded X are minimal risk; D is not yet studied.",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "B, X Areas of moderate flood hazards", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "C, X Area of minimal hazards", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "D Area of undetermined but possible, flood hazards", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=64", "A99 Area of special flood hazard where enough progress has been made on a protective system", "curl")]},
    "private_accept": {   # backlog 2: lenders must take a qualifying private policy (FDIC rule; OCC, Fed, NCUA, FCA rules match)
        "text": "A private flood policy can meet a lender's flood requirement: federally regulated lenders must accept a private "
                "policy that meets the federal definition of private flood insurance and covers at least what the loan requires "
                "(12 CFR §339.3(c)). Its price is not in FEMA's records.",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-12.xml?part=339&section=339.3",
                     "must accept private flood insurance, as defined in § 339.2, in satisfaction of the flood insurance purchase requirement", "curl")]},
    "rcv_80": {   # hater r6: the real answer to "would it pay to rebuild" (SFIP Dwelling Form, 44 CFR 61 App. A(1), Art. VII)
        "text": "The NFIP pays the cost to rebuild (not a depreciated value) only for a single-family home that is your "
                "principal residence and is insured for at least 80% of its full rebuilding cost, or for the $250,000 maximum.",
        "sources": [("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "the amount of insurance in this policy that applies to the dwelling is 80 percent or more of its full replacement cost immediately before the loss, or is the maximum amount of insurance available under the NFIP", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "It is your principal residence", "curl")]},
    "save_ways": {   # hater r5: every top result answers "how do I pay less"; FEMA's own list
        "text": "FEMA's ways to lower an NFIP bill: a higher deductible (you pay more of any loss), work that lowers "
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
                "building help; a lender or insurer can require it anywhere.",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "regulated lending institutions", "curl")]},
    "howto_short": {
        "text": "Usually 30 days after you buy; no wait with a new or refinanced mortgage.",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl")]},
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
        "text": "Outside them, a lender can still require it.",
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
        "text": "Except for the Emergency Program discount, statutory discounts gradually phase out through an annual increase cap discount at each renewal date until the policy reaches its full-risk premium.",
        "sources": [(FS + "/premiumcosts", "Limits annual premium increases to a set percentage.", "curl"),
                    (FIM, "gradually phase out through a statutory annual increase cap discount", "manual")]},
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
        "text": "FEMA's claim records give a reason when a building claim closes without payment, such as damage less than the deductible, not an actual flood, "
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
        "text": "Zone VE is a coastal high-risk area: land with a 1 percent or greater chance of flooding in any given year, hit by "
                "tidal floods with fast-moving water, where FEMA has worked out how high the water would reach (44 CFR §59.1, §64.3).",
        "sources": [(CFR64, "with water surface elevations determined and with velocity, that is inundated by tidal floods", "curl"),
                    (CFR59, "subject to a 1 percent or greater chance of flooding in any given year", "curl")]},
    "zone_x": {
        "text": "Zone X is outside the high-risk zones. Federal rules use it for two kinds of land: areas of moderate flood hazard, and "
                "areas of minimal hazard (44 CFR §64.3). FEMA's map shows the moderate kind shaded and the minimal kind unshaded.",
        "sources": [(CFR64, "B, X Areas of moderate flood hazards", "curl"),
                    (CFR64, "C, X Area of minimal hazards", "curl")]},
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
    "odds_30": {
        "text": "A 1 percent chance a year works out to about a 26% chance of at least one such flood over 30 years.",
        # arithmetic, tested in test_calc.py: 1 - 0.99**30 = 0.2603; the 1 percent is the regulation's
        "sources": [(CFR59, "subject to a 1 percent or greater chance of flooding in any given year", "curl")]},
    "flood_def": {
        "text": "The policy generally counts a flood only when water covers two or more acres of normally dry land or two or more properties, "
                "one of them yours.",
        "sources": [(CFR61, "two or more acres of normally dry land area or of two or more properties", "curl")]},
    "not_covered": {
        "text": "A standard NFIP home policy does not pay for a hotel or other living costs while you are out of the home, or for belongings outside the "
                "building, and it limits what it pays for in a basement. Belongings are paid at actual cash value (their used value), not the cost of new ones.",
        "sources": [(CFR61, "Any additional living expenses incurred while the insured building is being repaired", "curl"),
                    (CFR61, "Personal property not inside", "curl"),
                    ("https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61", "in a basement regardless of the zone", "curl"),
                    ("https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61", "subject to actual cash value", "curl")]},
    "claim_appeal": {
        "text": "NFIP claim denied? You can appeal to FEMA within 60 days of the date on the denial letter, and you can sue within one year of the denial. "
                "An appeal does not extend that year.",
        "sources": [(FS + "/recover/appeal-a-claim", "within 60 days of the date written on your denial letter", "curl"),
                    (FS + "/recover/appeal-a-claim", "does not extend the one-year period", "curl")]},
    "substantial_damage": {
        "text": "If repairs would cost 50 percent or more of the building's market value before the flood, it counts as substantially damaged under federal rules, and "
                "local floodplain rules can require elevating or other work. On an NFIP policy with building coverage, Increased Cost of Compliance pays up to $30,000 toward "
                "that; the local official's letter has to come before the work starts.",
        "sources": [(CFR59, "would equal or exceed 50 percent of the market value of the structure before the damage occurred", "curl"),
                    (CFR61, "We will pay you up to $30,000 under this Coverage D", "curl"),
                    ("https://www.floodsmart.gov/sites/default/files/media/document/2022-12/B17_Increased%20Cost%20of%20Compliance%20Benefits_Decision%20Upheld.pdf",
                     "before the initiation of mitigation activities", "manual")]},
    "lapse_discount": {
        "text": "Paying a renewal 30 days or more after the policy expires causes a lapse in coverage. You then need a new application, and the lapse may cost you "
                "statutory discounts (what keeps a bill below full risk), including the yearly cap.",
        "sources": [(FIM, "causes a lapse in coverage that may result in the loss of Statutory Discounts including the Annual Increase Cap", "manual"),
                    (FIM, "A new application is required", "manual")]},
    "surcharge": {
        "text": "Property that is not your primary residence, such as a second home, a rental you own or a non-residential building, pays a higher federal surcharge: $250 a year, against $25 for a primary home.",
        "sources": [("https://www.law.cornell.edu/uscode/text/42/4015a", "(1) $25, except as provided in paragraph (2); and (2) $250, in the case of a policy for any property that is", "curl"),
                    ("https://www.law.cornell.edu/uscode/text/42/4015a", "a residential property that is not the primar", "curl")]},
    "tx_twia": {   # Texas only
        "text": "In Texas, a TWIA windstorm policy requires flood insurance when any part of the property is in a V, VE or V1-V30 zone, NFIP cover "
                "is available for it, and the structure was built, altered, remodeled or enlarged after September 1, 2009.",
        "sources": [("https://www.twia.org/flood-requirement", "Flood insurance is required when all three of the following conditions are met", "curl"),
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
}


def rule(key):
    """The one way the page prints a rule: the registry text inside an element the gate can check
    (a div when the rule is a block such as a tile list, otherwise a span)."""
    tag = "div" if RULES[key]["text"].startswith("<ul") else "span"
    return f'<{tag} data-rule="{key}">{RULES[key]["text"]}</{tag}>'
