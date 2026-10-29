"""Every legal / program fact the county page states, with the official page that says it.
The page prints rule text ONLY from here (build_page uses rule(key)); gate.py checks each data-rule span on a
page equals its registry text; recheck.py re-fetches each source and checks the excerpt is still there.
method: "curl" = machine-verifiable; "manual" = the host blocks scripts (fema.gov), excerpt verified by a human
read on `checked` (re-read it when it goes stale). Never add a rule without a source and an excerpt."""

FS = "https://www.floodsmart.gov"
CHECKED = "2026-10-25"
# FEMA's own dataset description (fema.gov pages block scripts; the OpenFEMA metadata API does not)
IA_META = "https://www.fema.gov/api/open/v1/OpenFemaDataSets?$filter=name%20eq%20'IndividualAssistanceHousingRegistrantsLargeDisasters'"

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
        "text": "Exceptions: no wait if you buy while making, increasing, extending or renewing a mortgage; a one-day wait if a map revision puts the property in a high-risk zone and you buy "
                "within 13 months of the revision (44 CFR §61.11).",
        # FloodSmart's consumer page rounds this to "12 months"; the regulation says 13 — the regulation is cited.
        "sources": [(FS + "/get-insured/buy-a-policy", "while making, increasing, extending or renewing a mortgage", "curl"),
                    ("https://www.govinfo.gov/content/pkg/CFR-2024-title44-vol1/xml/CFR-2024-title44-vol1-sec61-11.xml",
                     "During the 13-month period beginning on the effective date of a revised", "curl")]},
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
                "to start a flood claim</a>), and send a signed proof of loss within 60 days of the flood (44 CFR 61, "
                "App. A(1), Art. VII). Not insured: a policy bought today will not cover a flood that already "
                "happened, and FEMA disaster aid is open to people in counties designated in a federally declared "
                "disaster.",
        "sources": [(FS + "/contact", "Report your loss immediately to your insurance agent or carrier.", "curl"),
                    (IA_META, "in designated counties who sustained damage", "curl"),
                    (IA_META, "resulting from a federally declared disaster may apply", "curl"),
                    ("https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-44.xml?part=61",
                     "Within 60 days after the loss, send us a proof of loss", "curl")]},
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
        "text": "If FEMA aid pays to repair a home in a high-risk zone, you must buy and keep flood insurance on it, or "
                "you cannot get that aid again after a later flood.",
        "sources": [("https://www.fema.gov/press-release/20250121/flood-aid-recipients-get-insurance-stay-eligible-repeat-assistance",
                     "ineligible for IHP Assistance for flood-damaged real or personal property in future disasters", "manual")]},
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
        "text": "By law a primary home's premium cannot rise more than 18% a year; some policies, such as second homes "
                "and businesses, can rise up to 25%. The cap usually does not apply to new policies, and fees and "
                "surcharges sit outside it.",
        "sources": [(FS + "/premiumcosts", "per year for most policyholders. This usually does not apply to new policies.", "curl"),
                    ("https://www.fema.gov/flood-insurance/risk-rating", "most rates not increase more than 18% per year", "manual"),
                    ("https://www.govinfo.gov/link/uscode/42/4015?link-type=html", "may not be increased by more than 18 percent each year", "curl")]},
    "rr2_zone": {
        "text": "Since FEMA's <a href='https://www.fema.gov/flood-insurance/risk-rating' rel='noopener' "
                "target='_blank'>Risk Rating 2.0</a>, price is set from each building's own flood risk, not its zone, and "
                "these are existing policies whose buildings differ. The reason for any one zone is not in this data.",
        "sources": [(FS + "/premiumcosts", "The premium amount is based on the flood risk of the building.", "curl"),
                    ("https://www.fema.gov/flood-insurance/risk-rating", "does not use flood zones to determine flood risk", "manual")]},
    "glide": {
        "text": "Those prices step up toward full-risk each year, limited by the yearly cap.",
        "sources": [(FS + "/premiumcosts", "Limits annual premium increases to a set percentage.", "curl"),
                    ("https://www.fema.gov/flood-insurance/risk-rating", "most rates not increase more than 18% per year", "manual")]},
    "nfip_not_sold": {   # 2026-10-28 site review: 34 Louisiana, 137 Texas communities are not in the NFIP; the page called them "no discount"
        "text": "Federal flood insurance (NFIP) is sold only in communities that take part in the NFIP; in a community that "
                "has not joined, has withdrawn or is suspended, no one can buy an NFIP policy.",
        "sources": [("https://www.floodsmart.gov/get-insured/eligibility",
                     "You can get flood insurance from the National Flood Insurance Program if your city or town participates in the NFIP", "curl"),
                    ("https://www.fema.gov/about/glossary/participation-nfip",
                     "No resident will be able to purchase a flood insurance policy", "manual")]},
    "crs_auto": {
        "text": "It is automatic, already in these prices, and the same in every flood zone.",
        "sources": [(FS + "/premiumcosts", "Applies to all eligible policies within the community, regardless of flood zone.", "curl")]},
    "cwop": {
        "text": "FEMA lists reasons a claim closes without payment, such as damage below the deductible, no flood as "
                "the policy defines it, or seepage and drain backup the policy does not cover.",
        "sources": [("https://www.fema.gov/press-release/20250121/hurricane-irma-nfip-claim-closed-without-payment-heres-why",
                     "less than the deductible", "manual")]},
    "ia_partial": {
        "text": "FEMA disaster aid helps with uninsured and underinsured losses, and is separate from NFIP insurance.",
        "sources": [(IA_META, "uninsured and underinsured personal property losses", "curl")]},
}


def rule(key):
    """The one way the page prints a rule: the registry text inside an element the gate can check
    (a div when the rule is a block such as a tile list, otherwise a span)."""
    tag = "div" if RULES[key]["text"].startswith("<ul") else "span"
    return f'<{tag} data-rule="{key}">{RULES[key]["text"]}</{tag}>'
