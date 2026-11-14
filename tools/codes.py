"""FEMA's legal values for coded NFIP fields, copied from the OpenFEMA data dictionary (OpenFemaDataSetFields,
fetched 2026-10-25). The page labels a code ONLY from here, so a label always matches FEMA's own definition."""

NONPAY_REASON = {   # NfipClaims.nonPaymentReasonBuilding
    "01": "Damage less than the deductible", "02": "Seepage", "03": "Backed-up drains", "04": "Shrubs (not covered)",
    "05": "Sea wall", "06": "Not an actual flood", "07": "Loss already in progress", "08": "Claim not pursued",
    "09": "Debris removal only", "10": "Fire", "11": "Fence damage", "12": "Hydrostatic pressure",
    "13": "Clogged drainage", "14": "Boat piers", "15": "Damage before the policy started", "16": "Wind damage (not flood)",
    "17": "Erosion not covered", "18": "Landslide", "19": "Mudflow not covered", "20": "No demonstrable damage",
    "97": "Other", "98": "Claim deleted in error", "99": "Assigned in error"}
CAUSE = {           # NfipClaims.causeOfDamage (more than one code can be present)
    "0": "Other causes", "1": "Tidal water (storm surge)", "2": "River, stream or lake overflow", "3": "Alluvial fan overflow",
    "4": "Heavy rain or snowmelt", "7": "Erosion (demolition)", "8": "Erosion (removal)", "9": "Earth movement",
    "A": "Closed basin lake"}       # B/C/D are claim-handling methods, not causes, so they are not labelled as causes
DEDUCTIBLE = {"0": 500, "1": 1000, "2": 2000, "3": 3000, "4": 4000, "5": 5000, "9": 750, "A": 10000, "B": 15000,
              "C": 20000, "D": 25000, "E": 50000, "F": 1250, "G": 1500}
CONDO = {"N": "Not a condominium", "U": "Condo unit", "A": "Condo association", "H": "Condo master policy (high-rise)",
         "L": "Condo master policy (low-rise)"}
GRANDFATHER = {"1": "No grandfathering", "2": "Grandfathered: built to code", "3": "Grandfathered: continuous coverage"}
SOURCE = "https://www.fema.gov/api/open/v1/OpenFemaDataSetFields (NfipPolicies v3, NfipClaims v3)"

def truthy(v): return str(v).strip().lower() in ("true", "1", "t", "y", "yes")
def loma_group(outcome):   # FEMA NFHL LOMA layer OUTCOME wording -> the groups county pages and the LOMA guide print (round 74; one rule, two pages)
    o = str(outcome).split("|")[0].lower()   # "removed" = out of the high-risk zone, never demolished
    return ("denied" if "denied" in o else "bldg" if o.startswith("structure removed") else "part" if o.startswith("portion of property removed")
            else "whole" if o.startswith("property removed") else "bldg_out" if o.startswith("structure out as shown")
            else "out" if "out as shown" in o else "other")
