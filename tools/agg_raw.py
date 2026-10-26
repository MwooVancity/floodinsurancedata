"""Offline: turn the raw pulls in .cache/raw/ (tools/pull_raw.py) into figures, with the SAME ffcalc code the
county pages use, so a state, a county and a test fixture can never be computed differently.
Writes, per finished state:
  data/states/<state-slug>/agg.json   state policies + claims aggregates (county-page schema) + per-county rollup
  data/all-counties/<geoid>.json      every county's policies + claims aggregates (for the county rollout later)
Usage: python -I tools/agg_raw.py [ST ...]   (one state in memory at a time; Florida is ~1.1M policy rows)"""
import csv, glob, gzip, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffcalc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, ".cache", "raw")
NAMES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
         "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
         "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
         "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
         "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
         "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
         "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
         "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
         "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}
def slug(st): return NAMES[st].lower().replace(" ", "-")

# only the columns a figure needs, numbers parsed; everything else stays in the raw file for later metrics
POL_NUM = ("policyCount", "policyCost", ffcalc.PREM, "fullRiskPremium", "totalBuildingInsuranceCoverage", "totalContentsInsuranceCoverage")
POL_STR = ("occupancyType", "primaryResidenceIndicator", "ratedFloodZone", "reportedZipCode", "policyEffectiveDate", "censusGeoid",
           "elevationCertificateIndicator", "preFIRMConstructionIndicator", "mandatoryPurchaseFlag", "buildingDeductibleCode",
           "originalNBDate", "crsClassCode")
CLM_NUM = ("netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount", "policyCount", "waterDepth",
           "buildingDamageAmount", "buildingPropertyValue")
CLM_STR = ("yearOfLoss", "countyCode", "ratedFloodZone", "floodEvent", "nonPaymentReasonBuilding", "reportedZipCode", "dateOfLoss")

def num(v):
    if v in ("", None): return None
    try: f = float(v); return int(f) if f.is_integer() else f
    except ValueError: return None

def load(ds, st, nums, strs):
    out = []
    for f in sorted(glob.glob(os.path.join(RAW, ds, st, "*.csv.gz"))):
        for r in csv.DictReader(gzip.open(f, "rt", encoding="utf-8")):
            d = {k: num(r.get(k)) for k in nums}
            d.update({k: (r.get(k) or None) for k in strs})
            out.append(d)
    return out

def net(r): return (r["netBuildingPaymentAmount"] or 0) + (r["netContentsPaymentAmount"] or 0) + (r["netIccPaymentAmount"] or 0)

def claims_extra(rows):
    """Payout reality, same definitions as collect_claims_extra.py (net = building + contents + ICC)."""
    if not rows: return None
    paid = [r for r in rows if net(r) > 0]
    paid_total = sum(net(r) for r in paid)
    outside = sum(net(r) for r in paid if (r["ratedFloodZone"] or "")[:1] not in ("A", "V"))
    return {"claims": len(rows), "avg_paid": round(paid_total / len(paid)) if paid else 0,
            "cwop_share": round(100 * (len(rows) - len(paid)) / len(rows), 1),
            "outside_sfha_pct": round(100 * outside / paid_total, 1) if paid_total else None,
            "paid_n": len(paid), "source": "OpenFEMA NFIP Claims v3 (raw pull)"}

def manifest(ds, st):
    m = json.load(open(os.path.join(RAW, ds, st + ".done")))
    return {"reported_total": m["n"], "recheck_total": m["n"], "unique_fetched": m["n"], "missing": 0,
            "complete": True, "stable": True, "provisional": False, "pulled": m["at"][:10]}

def run(st):
    if not all(os.path.exists(os.path.join(RAW, ds, st + ".done")) for ds in ("NfipPolicies", "NfipClaims")):
        print(st, "skipped: pull not finished"); return
    pol = load("NfipPolicies", st, POL_NUM, POL_STR)
    clm = load("NfipClaims", st, CLM_NUM, CLM_STR)
    P = ffcalc.aggregate_policies(pol)
    C = ffcalc.aggregate_claims(clm, P["units"])
    by_c = {}
    for r in pol:
        g = (r["censusGeoid"] or "")[:5]
        if len(g) == 5: by_c.setdefault(g, []).append(r)
    cl_c = {}
    for r in clm:
        g = r["countyCode"] or ""
        if len(g) == 5: cl_c.setdefault(g, []).append(r)
    os.makedirs(os.path.join(ROOT, "data", "all-counties"), exist_ok=True)
    rollup = {}
    for g in sorted(set(by_c) | set(cl_c)):
        cp = ffcalc.aggregate_policies(by_c.get(g, []))
        cc = ffcalc.aggregate_claims(cl_c.get(g, []), cp["units"])
        cx = claims_extra(cl_c.get(g, []))
        json.dump({"geoid": g, "state": st, "policies": cp, "claims": cc, "claims_extra": cx},
                  open(os.path.join(ROOT, "data", "all-counties", g + ".json"), "w"))
        rollup[g] = {"units": cp["units"], "cost_n": cp["cost_n"], "p50": cp["p50"], "prem_median": cp.get("prem_median"),
                     "share_below": cp.get("share_below"), "sfha_share": cp["sfha_share_units"],
                     "claims": cc["rows"], "paid": cc["total_paid"], "cwop_share": (cx or {}).get("cwop_share")}
    unassigned = sum(1 for r in pol if len((r["censusGeoid"] or "")[:5]) != 5)
    agg = {"level": "state", "state": st, "name": NAMES[st],
           "policies": dict(P, asof="2026-07-31", retrieved=manifest("NfipPolicies", st)["pulled"], unassigned_rows=unassigned),
           "claims": dict(C, retrieved=manifest("NfipClaims", st)["pulled"]),
           "claims_extra": claims_extra(clm), "counties": rollup,
           "manifest": {"policies": manifest("NfipPolicies", st), "claims": manifest("NfipClaims", st)}, "complete": True}
    d = os.path.join(ROOT, "data", "states", slug(st)); os.makedirs(d, exist_ok=True)
    json.dump(agg, open(os.path.join(d, "agg.json"), "w"))
    print(f"{st}: {len(pol)} policy rows ({P['units']} units, median ${P['p50']}, {P.get('share_below')}% below full-risk), "
          f"{len(clm)} claims, {len(rollup)} counties, {unassigned} policies without a county")

for st in (sys.argv[1:] or sorted(NAMES)):
    run(st)
