"""Research papers (owner 11-12: national data, "PubMed worthy"). One spec per paper; every U.S. county in data/all-counties
that meets the paper's minimum is ranked. build_site.py writes each paper page + CSV; build_counties.py writes .cache/papers.json
once per build so each county page reads its own ranks (PLAN E13: never every county's file per page).
tools/index_check.py recomputes every row from the raw files with its own code (PLAN E22)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL = os.path.join(ROOT, "data", "all-counties")
CACHE = os.path.join(ROOT, ".cache", "papers.json")

SPECS = [
    {"key": "price-gap", "ready": False, "title": "Flood Insurance Price Gap Index",
     "value": ("policies", "share_below"), "n": ("policies", "below_n"), "min": 100,
     "unit": "single-family primary-home NFIP policies",
     "measure": "share of single-family primary-home NFIP policies whose premium is below FEMA's full-risk premium",
     "short": "share below full-risk", "here": "of single-family primary-home policies here have a premium below their full-risk premium", "first": "the largest share of policies below full-risk",
     "fields": "totalInsurancePremiumOfThePolicy, fullRiskPremium, occupancyType, primaryResidenceIndicator, condominiumCoverageTypeCode",
     "dataset": "FEMA OpenFEMA NFIP Policies v3", "api": "https://www.fema.gov/api/open/v3/NfipPolicies",
     "base": "single-family primary-home policies in force whose premium and full-risk premium are both above $0; premiums only, before fees and surcharges",
     "extra": [("Median premium", ("policies", "prem_median"), "usd"), ("Median full-risk premium", ("policies", "frp_median"), "usd")],
     "limits": ["A share below full-risk says nothing about how far below any one policy is, or how fast its bill will change; it is not a forecast.",
                "Condos, rentals, second homes and businesses are not in this base.",
                "The county is the county FEMA coded on the policy."],
     "rules": ["glide", "cap"], "metric": ("share_below", "policies.share_below"), "n_metric": ("below_n", "policies.below_n")},
    {"key": "outside-the-zone", "ready": False, "title": "Outside the Zone: Flood Claim Dollars Paid Outside High-Risk Areas",
     "value": ("claims_extra", "outside_sfha_pct"), "n": ("claims_extra", "paid_n"), "min": 100,
     "unit": "NFIP claims with a recorded payment",
     "measure": "share of NFIP claim dollars paid on claims rated outside FEMA's high-risk zones (zones not starting with A or V), among claims with a rated zone",
     "short": "share of dollars outside high-risk zones", "here": "of NFIP claim dollars paid here went to claims rated outside high-risk zones", "first": "the largest share of claim dollars paid outside high-risk zones",
     "fields": "ratedFloodZone, netBuildingPaymentAmount, netContentsPaymentAmount, netIccPaymentAmount, nonPaymentReasonBuilding",
     "dataset": "FEMA OpenFEMA NFIP Claims v3", "api": "https://www.fema.gov/api/open/v3/NfipClaims",
     "base": "NFIP claims since 1978 with a rated flood zone; building, contents and Increased Cost of Compliance payments as paid, not adjusted for inflation; records FEMA coded deleted or assigned in error left out",
     "extra": [("Claims with a payment", ("claims_extra", "paid_n"), "count")],
     "limits": ["This is a share of dollars paid on claims, not a share of homes, and not the chance that any home floods.",
                "The zone is the zone FEMA rated on the claim, which can differ from today's map.",
                "Claims with no rated zone are not in the base."],
     "rules": [], "metric": ("outside_sfha_dollars", "data.claims_extra.outside_sfha_pct"), "n_metric": ("claims_paid_n", "data.claims_extra.paid_n")},
]

READY = [s for s in SPECS if s.get("ready")]   # methods review 162: a paper ships only after originality search + statistics review pass

def names():
    return json.load(open(os.path.join(ROOT, "data", "us", "county_names.json"), encoding="utf-8"))

def _get(rec, path):
    v = rec
    for k in path: v = (v or {}).get(k) if isinstance(v, dict) else None
    return v

def rows(spec, recs=None):
    """Ranked rows: every county whose value is a number and whose n meets the minimum; ties share a rank (1, 2, 2, 4)."""
    recs = recs if recs is not None else load()
    out = []
    for g, r in recs.items():
        v, n = _get(r, spec["value"]), _get(r, spec["n"])
        if isinstance(v, (int, float)) and isinstance(n, int) and n >= spec["min"] and 0 <= v <= 100:
            out.append({"geoid": g, "state": r.get("state", ""), "value": v, "n": n,
                        "extra": [_get(r, p) for _, p, _ in spec["extra"]]})
    out.sort(key=lambda x: (-x["value"], x["geoid"]))
    for i, x in enumerate(out):
        x["rank"] = out[i - 1]["rank"] if i and out[i - 1]["value"] == x["value"] else i + 1
    cnt = {}
    for x in out: cnt[x["value"]] = cnt.get(x["value"], 0) + 1
    for x in out: x["tied"] = cnt[x["value"]] > 1
    return out

def skipped(spec, recs):
    """Counties left out, by reason (method line)."""
    nul = sum(1 for r in recs.values() if not isinstance(_get(r, spec["value"]), (int, float)))
    small = sum(1 for r in recs.values() if isinstance(_get(r, spec["value"]), (int, float)) and not (isinstance(_get(r, spec["n"]), int) and _get(r, spec["n"]) >= spec["min"]))
    return nul, small

def load():
    return {f[:5]: json.load(open(os.path.join(ALL, f))) for f in sorted(os.listdir(ALL)) if f.endswith(".json")}

def write_cache():
    recs = load(); out = {}
    for s in SPECS:
        rs = rows(s, recs)
        out[s["key"]] = {"pool": len(rs), "ranks": {x["geoid"]: [x["rank"], x["tied"]] for x in rs}}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(out, open(CACHE, "w"))
    return out

def read_cache():
    try: return json.load(open(CACHE))
    except Exception: return {}

if __name__ == "__main__":   # self-check: ties, minimum, range
    fake = {"1": {"policies": {"share_below": 50.0, "below_n": 40}}, "2": {"policies": {"share_below": 50.0, "below_n": 31}},
            "3": {"policies": {"share_below": 70.0, "below_n": 30}}, "4": {"policies": {"share_below": 90.0, "below_n": 29}},
            "5": {"policies": {"share_below": None, "below_n": 99}}, "6": {"policies": {"share_below": 140.0, "below_n": 99}}}
    S = dict(SPECS[0], min=30); r = rows(S, fake)
    assert [(x["geoid"], x["rank"], x["tied"]) for x in r] == [("3", 1, False), ("1", 2, True), ("2", 2, True)], r
    assert skipped(S, fake) == (1, 1)
    print("papers self-test OK")
