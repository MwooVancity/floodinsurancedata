"""What every printed figure MEANS. One entry per figure: dataset, the FEMA fields it is computed from, its unit,
what one counted item is, and the basis phrase a sentence must name when a same-topic figure on another basis is
nearby. build_page prints figures through m(), compares through compare(), and builds source lines through
sources_for(); gate.py re-checks all three on the rendered page. FEMA field definitions are hashed in
metric_defs.json (refresh: python -I tools/metrics.py --refresh); recheck.py fails when FEMA changes one.

Born 2026-10-25: policyCost (premium + fees) was compared with fullRiskPremium (premium only) on every page and
the 29-check gate passed it, because nothing said what either number meant."""
import hashlib, json, os, re, sys, urllib.parse, urllib.request

OPENFEMA = "openfema"
DATASETS = {   # display name, citation URL, whether the OpenFEMA attribution applies
    "NfipPolicies": ("FEMA OpenFEMA — NFIP Policies", "https://www.fema.gov/openfema-data-page/fima-nfip-redacted-policies-v2", OPENFEMA),
    "NfipClaims": ("FEMA OpenFEMA — NFIP Claims", "https://www.fema.gov/openfema-data-page/fima-nfip-redacted-claims-v2", OPENFEMA),
    "NRI": ("FEMA — National Risk Index (flood)", "https://www.fema.gov/flood-maps/products-tools/national-risk-index", "fema"),
    "NfipCommunityStatusBook": ("FEMA OpenFEMA — NFIP Community Status Book (CRS)", "https://www.fema.gov/openfema-data-page/nfip-community-status-book-v1", OPENFEMA),
    "DisasterDeclarationsSummaries": ("FEMA OpenFEMA — Disaster Declarations Summaries", "https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2", OPENFEMA),
    "HousingAssistanceOwners": ("FEMA OpenFEMA — Housing Assistance (Owners)", "https://www.fema.gov/openfema-data-page/housing-assistance-program-data-owners-v2", OPENFEMA),
    "IndividualAssistanceMultipleLossFloodProperties": ("FEMA OpenFEMA — Repetitive-Loss Flood Properties", "https://www.fema.gov/openfema-data-page/individual-assistance-multiple-loss-flood-properties-v1", OPENFEMA),
    "NfipResidentialPenetrationRates": ("FEMA OpenFEMA — NFIP Residential Penetration Rates", "https://www.fema.gov/openfema-data-page/nfip-residential-penetration-rates-v1", OPENFEMA),
    "StormEvents": ("NOAA NCEI — Storm Events Database", "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/", "noaa"),
    "CensusACS": ("U.S. Census Bureau — ACS 5-year B25001 (housing units)", "https://data.census.gov/table/ACSDT5Y2023.B25001", "census"),
}
API_VERSION = {"NfipPolicies": 3, "NfipClaims": 3, "NfipCommunityStatusBook": 1, "DisasterDeclarationsSummaries": 2,
               "HousingAssistanceOwners": 2, "IndividualAssistanceMultipleLossFloodProperties": 1,
               "NfipResidentialPenetrationRates": 1}

# unit: closed set — compare() only allows equal units. counts: what ONE counted item is; NOUN_REQUIRED is the noun
# that must name it in the words right after the number (or in its tile label). A FEMA IA row is one property PER
# disaster, so "1,133 homes" fails and "1,133 flood-damage applications" passes. (A positive rule, not a ban list.)
UNITS = {"usd_cost_with_fees", "usd_premium_only", "usd_claim_paid", "usd_aid_paid", "usd_coverage", "usd_modeled_loss",
         "usd_reported_damage", "pct", "count", "rating"}
NOUN_REQUIRED = {"ia_damage_record": r"records?|applications?", "policy_record": r"polic(y|ies)|records?",
                 "claim_record": r"claims?|NFIP flood claims",
                 "noaa_event": r"flood|events?"}

def _m(dataset, fields, unit, counts=None, basis=None, of=None):
    assert unit in UNITS, unit
    return {"dataset": dataset, "fields": fields, "unit": unit, "counts": counts, "basis": basis, "of": of}

POL, CLM = "NfipPolicies", "NfipClaims"
METRICS = {
    "cost_p25": _m(POL, ["policyCost"], "usd_cost_with_fees"),
    "cost_p50": _m(POL, ["policyCost"], "usd_cost_with_fees"),
    "cost_p75": _m(POL, ["policyCost"], "usd_cost_with_fees"),
    "cost_p90": _m(POL, ["policyCost"], "usd_cost_with_fees"),
    "cost_mo": _m(POL, ["policyCost"], "usd_cost_with_fees"),
    "zone_cost": _m(POL, ["policyCost", "ratedFloodZone"], "usd_cost_with_fees"),
    "zip_cost": _m(POL, ["policyCost", "reportedZipCode"], "usd_cost_with_fees"),
    "prem_median": _m(POL, ["totalInsurancePremiumOfThePolicy"], "usd_premium_only"),
    "frp_median": _m(POL, ["fullRiskPremium"], "usd_premium_only"),
    "share_below": _m(POL, ["totalInsurancePremiumOfThePolicy", "fullRiskPremium"], "pct", basis="full-risk",
                      of="single-family primary-residence policies with both premiums"),
    "units": _m(POL, ["policyCount"], "count", counts="policy_unit"),
    "sfha_share": _m(POL, ["policyCount", "ratedFloodZone"], "pct", of="policy units"),
    "coverage": _m(POL, ["totalBuildingInsuranceCoverage", "totalContentsInsuranceCoverage"], "usd_coverage"),
    "claims_filed": _m(CLM, ["id"], "count", counts="claim_record"),
    "claims_paid_n": _m(CLM, ["netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"], "count", counts="claim_record"),
    "claims_total": _m(CLM, ["netBuildingPaymentAmount", "netContentsPaymentAmount"], "usd_claim_paid"),
    "avg_paid": _m(CLM, ["netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"], "usd_claim_paid"),
    "cwop_share": _m(CLM, ["netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"], "pct", of="claims filed"),
    "outside_sfha_dollars": _m(CLM, ["ratedFloodZone", "netBuildingPaymentAmount"], "pct", of="paid claim dollars"),
    "outside_sfha_policies": _m(POL, ["ratedFloodZone", "policyCount"], "pct", of="policy units"),
    "nri_rating": _m("NRI", ["RISK_RATNG"], "rating", basis="rating"),
    "nri_eal_pctl_coastal": _m("NRI", ["CFLD_EALP"], "pct", basis="expected annual flood loss"),
    "nri_eal_pctl_inland": _m("NRI", ["IFLD_EALP"], "pct", basis="expected annual flood loss"),
    "nri_eal_usd": _m("NRI", ["EAL_VALT"], "usd_modeled_loss"),
    "crs_discount": _m("NfipCommunityStatusBook", ["sfhaDiscount", "nonSfhaDiscount", "classRating"], "pct"),
    "declarations": _m("DisasterDeclarationsSummaries", ["disasterNumber", "incidentType", "declarationDate"], "count", counts="declaration_event"),
    "ia_paid": _m("HousingAssistanceOwners", ["totalApprovedIhpAmount"], "usd_aid_paid"),
    "ia_regs": _m("HousingAssistanceOwners", ["validRegistrations"], "count", counts="registration"),
    "ml_total": _m("IndividualAssistanceMultipleLossFloodProperties", ["highRiskPropertyType"], "count", counts="ia_damage_record"),
    "ml_srl": _m("IndividualAssistanceMultipleLossFloodProperties", ["highRiskPropertyType"], "count", counts="ia_damage_record"),
    "pen_overall": _m("NfipResidentialPenetrationRates", ["resPenetrationRate"], "pct", of="residential structures"),
    "pen_sfha": _m("NfipResidentialPenetrationRates", ["resPenetrationRateSfha"], "pct", of="residential structures in the SFHA"),
    "storm_events": _m("StormEvents", ["EVENT_TYPE", "CZ_FIPS"], "count", counts="noaa_event"),
    "storm_damage": _m("StormEvents", ["DAMAGE_PROPERTY"], "usd_reported_damage"),
    "housing_units": _m("CensusACS", ["B25001_001E"], "count", counts="housing_unit"),
    # state-page "why the averages differ" figures: all from the same NfipPolicies records, different cuts
    "cost_mean": _m(POL, ["policyCost"], "usd_cost_with_fees"),
    "cost_all_median": _m(POL, ["policyCost", "occupancyType"], "usd_cost_with_fees"),
    "cost_all_mean": _m(POL, ["policyCost", "occupancyType"], "usd_cost_with_fees"),
    "prem_mean": _m(POL, ["totalInsurancePremiumOfThePolicy"], "usd_premium_only"),
    "inforce": _m(POL, ["policyEffectiveDate", "policyTerminationDate"], "count", counts="policy_record"),
    "inforce_change_pct": _m(POL, ["policyEffectiveDate", "policyTerminationDate"], "pct", of="in-force policy records, 2022 to 2026"),
    "county_units": _m(POL, ["policyCount", "censusGeoid"], "count", counts="policy_unit"),
    "zone_inversion": _m(POL, ["policyCost", "ratedFloodZone"], "count"),   # 1 if any A/V zone median < Zone X median
    # extras (raw pull, tools/extras_raw.py): single-family primary-home policy rows; claims by building non-payment code
    "rebuild_over_cap_pct": _m(POL, ["buildingReplacementCost"], "pct", of="single-family home policies reporting a rebuilding cost"),
    "rebuild_n": _m(POL, ["buildingReplacementCost"], "count", counts="policy_record"),
    "at_cap_pct": _m(POL, ["totalBuildingInsuranceCoverage"], "pct", of="single-family home policies"),
    "damage_over_cov_pct": _m(CLM, ["buildingDamageAmount", "totalBuildingInsuranceCoverage"], "pct", of="paid claims with a damage figure"),
    "unpaid_n": _m(CLM, ["netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"], "count", counts="claim_record"),
    "unpaid_reason_n": _m(CLM, ["nonPaymentReasonBuilding"], "count", counts="claim_record"),
    "event_paid": _m(CLM, ["floodEvent", "netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"], "usd_claim_paid"),
    "event_claims": _m(CLM, ["floodEvent"], "count", counts="claim_record"),
}

def values(agg, data):
    """Numeric value of each claim-able metric, straight from the county's JSON (what gate re-checks claims on)."""
    P, C = agg.get("policies", {}), agg.get("claims", {})
    cx, ml = data.get("claims_extra") or {}, data.get("multiloss") or {}
    cz = P.get("cost_by_zone") or {}
    xm = (cz.get("X") or {}).get("median")
    v = {"share_below": P.get("share_below"), "prem_median": P.get("prem_median"), "frp_median": P.get("frp_median"),
         "cost_p50": P.get("p50"), "units": P.get("units"), "sfha_share": P.get("sfha_share_units"),
         "claims_filed": C.get("rows"), "claims_paid_n": cx.get("paid_n"), "cwop_share": cx.get("cwop_share"),
         "outside_sfha_dollars": cx.get("outside_sfha_pct"), "ml_total": ml.get("total"), "ml_srl": ml.get("srl"),
         "outside_sfha_policies": round(100 - P["sfha_share_units"], 1) if P.get("sfha_share_units") is not None else None,
         "zone_inversion": int(bool(xm) and any(z[:1] in "AV" and d["median"] < xm for z, d in cz.items()))}
    v["ia_paid"] = sum(float(r.get("totalApprovedIhpAmount") or 0) for r in data.get("housing", []))
    def _disc(x):
        try: return float(str(x).rstrip("%") or 0) > 0
        except ValueError: return False
    h = (data.get("inforce_history") or {}).get("by_year") or {}
    v["inforce_change_pct"] = (round(100 * (h["2026"] - h["2022"]) / h["2022"], 1)
                               if h.get("2022") and h.get("2026") is not None else None)
    v["crs_discount_communities"] = sum(1 for c in data.get("crs", []) if _disc(c.get("sfhaDiscount")) or _disc(c.get("nonSfhaDiscount")))
    return v

OPS = {">": lambda a, b: a > b, ">=": lambda a, b: a >= b, "<": lambda a, b: a < b, "<=": lambda a, b: a <= b,
       "==": lambda a, b: a == b}
# words that carry a numeric direction or majority: on a rendered page they may appear only inside a claim()
# span whose condition holds, or inside a rule() span (registry text). Matching is on whole words/phrases.
QUANT = ("most", "majority", "climb", "climbing", "climbs", "rise", "rises", "rising", "less per policy",
         "as much per policy", "cost less than", "at or above", "yes", "fell", "grew")   # "yes" = a yes/no heading's answer

def holds(cond, vals):
    a, op, b = cond
    va = vals.get(a); vb = vals.get(b) if isinstance(b, str) else b
    return va is not None and vb is not None and OPS[op](va, vb)

def claim(text, word, cond, vals):
    """A sentence carrying a direction/majority word, tagged with the condition that makes the word true.
    cond = (metric, op, metric_or_number). Raises at build time if the word is absent or the condition false."""
    assert word in QUANT and re.search(rf"\b{re.escape(word)}\b", text, re.I), (word, text)
    if not holds(cond, vals):
        raise ValueError(f"claim '{word}' false: {cond} with {vals.get(cond[0])} vs {cond[2]}")
    # attribute is HTML-escaped: the condition contains ">"/"<", which must never end the tag early
    attr = json.dumps({"word": word, "cond": list(cond)}).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<span data-claim="{attr}">{text}</span>'


class UnitMismatch(ValueError):
    pass

def compare(a, b):
    """Gatekeeper for every comparison or overlay between two figures: same unit, or it raises."""
    ua, ub = METRICS[a]["unit"], METRICS[b]["unit"]
    if ua != ub:
        raise UnitMismatch(f"cannot compare {a} ({ua}) with {b} ({ub})")
    return True

def m(key, shown):
    """Print a figure tagged with its metric key so the gate can check labels, bases and repeats."""
    assert key in METRICS, key
    return f'<span data-m="{key}">{shown}</span>'

def sources_for(keys):
    """Dataset display names for the figures a panel shows, in first-seen order (the panel's source line)."""
    out = []
    for k in keys:
        ds = DATASETS[METRICS[k]["dataset"]][0]
        if ds not in out: out.append(ds)
    return out

def needs_openfema_attr(keys):
    return any(DATASETS[METRICS[k]["dataset"]][2] == OPENFEMA for k in keys)


DEFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metric_defs.json")

def fetch_defs():
    """Current FEMA definition text + sha256 for every OpenFEMA field the registry uses."""
    want = {}
    for k in METRICS.values():
        if k["dataset"] in API_VERSION: want.setdefault(k["dataset"], set()).update(k["fields"])
    out = {}
    for ds, fields in sorted(want.items()):
        q = urllib.parse.urlencode({"$filter": f"openFemaDataSet eq '{ds}' and datasetVersion eq {API_VERSION[ds]}",
                                    "$select": "name,description", "$top": 500}, quote_via=urllib.parse.quote)
        rows = json.load(urllib.request.urlopen(urllib.request.Request(
            "https://www.fema.gov/api/open/v1/OpenFemaDataSetFields?" + q, headers={"User-Agent": "ff"}), timeout=120))["OpenFemaDataSetFields"]
        have = {r["name"]: r["description"] for r in rows}
        out[ds] = {f: ({"def": have[f], "sha256": hashlib.sha256(have[f].encode()).hexdigest()} if f in have else None)
                   for f in sorted(fields)}
    return out

if __name__ == "__main__" and "--refresh" in sys.argv:
    d = fetch_defs()
    missing = [f"{ds}.{f}" for ds, fs in d.items() for f, v in fs.items() if v is None]
    json.dump(d, open(DEFS, "w"), indent=1)
    print("wrote", DEFS, "| fields not in FEMA's dictionary:", missing or "none")
