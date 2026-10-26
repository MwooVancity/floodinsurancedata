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
        "text": "Most homeowners insurance does not cover flood damage; flood insurance is bought separately, through the "
                "federal NFIP or a private insurer.",
        "sources": [(FS + "/flood-insurance-basics", "most homeowners insurance does not cover flood damage", "curl")]},
    "wait_30": {
        "text": "Most NFIP policies take effect <b>30 days after you buy</b>, so a policy bought today will not cover a "
                "flood this week.",
        "sources": [(FS + "/get-insured/buy-a-policy", "will go into effect 30 days after your date of purchase", "curl")]},
    "wait_exceptions": {
        "text": "Exceptions: no wait if you buy while making, increasing, extending or renewing a mortgage, or change "
                "coverage at renewal; a one-day wait if a map revision puts the property in a high-risk zone and you buy "
                "within 13 months of the revision (44 CFR §61.11).",
        # FloodSmart's consumer page rounds this to "12 months"; the regulation says 13 — the regulation is cited.
        "sources": [(FS + "/get-insured/buy-a-policy", "while making, increasing, extending or renewing a mortgage", "curl"),
                    ("https://www.govinfo.gov/content/pkg/CFR-2024-title44-vol1/xml/CFR-2024-title44-vol1-sec61-11.xml",
                     "During the 13-month period beginning on the effective date of a revised", "curl")]},
    "howto_answer": {
        "text": "Buy it now: most policies start <b>30 days</b> after you buy, but there's no wait if you buy it with a new "
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
        "text": "NFIP covers up to <b>$250,000</b> on the building and <b>$100,000</b> on contents, which is a separate "
                "policy.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl"),
                    (FS + "/get-insured/buy-a-policy", "contents policies cover up to $100,000", "curl")]},
    "building_cap": {
        "text": "the NFIP's <b>$250,000</b> building limit.",
        "sources": [(FS + "/get-insured/buy-a-policy", "Building policies cover up to $250,000", "curl")]},
    "how_to_buy": {
        "text": "To buy: call the NFIP at <b>(877) 336-2627</b>, go to <a href='https://www.floodsmart.gov' rel='nofollow "
                "noopener' target='_blank'>FloodSmart.gov</a>, or ask any licensed insurance agent. Every NFIP insurer "
                "offers the same rates.",
        "sources": [(FS + "/contact", "Call the NFIP at (877) 336-2627", "curl"),
                    (FS + "/get-insured/buy-a-policy", "Each one offers the same rates.", "curl")]},
    "already_flooded": {
        "text": "<b>Already flooded?</b> Insured: report the loss to your insurance agent or company now (FEMA's steps: "
                "<a href='https://www.floodsmart.gov/recover/start-a-claim' rel='nofollow noopener' target='_blank'>how "
                "to start a flood claim</a>). Not insured: a policy bought today will not cover a flood that already "
                "happened, and FEMA disaster aid is open to people in counties designated in a federally declared "
                "disaster.",
        "sources": [(FS + "/contact", "Report your loss immediately to your insurance agent or carrier.", "curl"),
                    (IA_META, "in designated counties who sustained damage", "curl"),
                    (IA_META, "resulting from a federally declared disaster may apply", "curl")]},
    "purchase_answer": {
        "text": "Only if your home is in a high-risk zone (A or V) and your mortgage is from a federally regulated lender, or federal "
                "help to buy or build (42 U.S.C. §4012a).",
        "sources": [("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "regulated lending institutions", "curl"),
                    ("https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm",
                     "financial assistance for acquisition or construction purposes", "curl")]},
    "lender_any_zone": {
        "text": "Outside those zones the federal requirement drops, but a lender can still require coverage.",
        "sources": [("https://www.federalreserve.gov/frrs/regulations/interagency-questions-and-answers-regarding-flood-insurance.htm",
                     "a lender may require flood insurance as a condition of making the loan, as a matter of safety and soundness", "curl")]},
    "cap": {
        "text": "By law most premiums cannot rise more than 18% a year (FloodSmart puts it at 18&ndash;25% for most "
                "policyholders); the cap usually does not apply to new policies, and fees and surcharges sit outside it.",
        "sources": [(FS + "/premiumcosts", "per year for most policyholders. This usually does not apply to new policies.", "curl"),
                    ("https://www.fema.gov/flood-insurance/risk-rating", "most rates not increase more than 18% per year", "manual")]},
    "rr2_zone": {
        "text": "Since FEMA's <a href='https://www.fema.gov/flood-insurance/risk-rating' rel='nofollow noopener' "
                "target='_blank'>Risk Rating 2.0</a>, price is set from each building's own flood risk, not its zone, and "
                "these are existing policies whose buildings differ. The reason for any one zone is not in this data.",
        "sources": [(FS + "/premiumcosts", "The premium amount is based on the flood risk of the building.", "curl"),
                    ("https://www.fema.gov/flood-insurance/risk-rating", "does not use flood zones to determine flood risk", "manual")]},
    "glide": {
        "text": "Those prices step up toward full-risk each year, limited by the yearly cap.",
        "sources": [(FS + "/premiumcosts", "Limits annual premium increases to a set percentage.", "curl"),
                    ("https://www.fema.gov/flood-insurance/risk-rating", "most rates not increase more than 18% per year", "manual")]},
    "crs_auto": {
        "text": "It applies to every eligible policy there.",
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
