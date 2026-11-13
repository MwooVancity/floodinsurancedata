"""Research papers (owner 11-12: national data, "PubMed worthy"; docs/PAPER-GATE-PROMPT.md). One spec per paper; every U.S. county
in data/all-counties whose count base meets the minimum is ranked. Shares are numerator / denominator on ONE base (methods review 162
M1.1), each with a 90% Wilson interval (M1.3); readers see fifths (bands), never a bare rank. build_site.py writes each paper page +
CSV; build_counties.py writes .cache/papers.json once per build (PLAN E13). tools/paper_gate.py recomputes
every row from the raw county files with its own code (PLAN E22)."""
import json, math, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL = os.path.join(ROOT, "data", "all-counties")
CACHE = os.path.join(ROOT, ".cache", "papers.json")
Z90 = 1.6448536269514722   # two-sided 90% normal quantile

SPECS = [
    {"key": "underinsured", "ready": False, "indexable": False, "title": "Underinsured: flood claims where damage passed the building coverage",
     "num": ("extras", "claims", "underinsured", "over"), "den": ("extras", "claims", "underinsured", "n"), "min": 100,
     "window": ("extras", "claims", "underinsured"),
     "question": "In which U.S. counties did FEMA's recorded building damage on paid flood claims most often exceed the policy's building coverage?",
     "unit": "single-family primary-home claims with a building payment",
     "measure": "share of paid single-family primary-home NFIP claims whose recorded building damage (actual cash value) was more than the policy's building coverage",
     "short": "damage above building coverage", "meets": "had recorded building damage above the building coverage",
     "fields": "buildingDamageAmount, totalBuildingInsuranceCoverage, netBuildingPaymentAmount, yearOfLoss, occupancyType, primaryResidenceIndicator, nonPaymentReasonBuilding",
     "defs": ['FEMA defines buildingDamageAmount as "The actual cash value amount of damage to a main property in whole dollars."',
              'FEMA defines totalBuildingInsuranceCoverage as "Total Insurance Amount in whole dollars on the Building".'],
     "dataset": "FEMA OpenFEMA NFIP Claims v3", "api": "https://www.fema.gov/api/open/v3/NfipClaims",
     "base": "claims on single-family primary homes with a loss in the window, a building payment above $0, recorded building damage above $0 and building coverage above $0; records FEMA coded deleted or assigned in error left out",
     "limits": ["Damage above coverage is FEMA's recorded actual cash value against the building coverage on the policy; it is not the owner's uninsured loss, which also depends on contents, deductibles, other insurance and aid.",
                "Only insured, paid claims are in the base: homes without flood insurance are not.",
                "Counties are those FEMA codes on the claim, which can differ from the property's county."],
     "prior": "No published ranking of this measure by county was found in searches on 2026-11-12 (WebSearch: NFIP claims damage exceeded coverage by county).",
     "prior_links": [], "prior_rules": [], "policy_col": False, "published": None,
     "rules": []},
    {"key": "outside-the-zone", "ready": True, "indexable": False, "title": "Outside the zone: paid flood claims rated outside high-risk zones",
     "num": ("extras", "claims", "zone_split", "out_paid_n"), "den": ("extras", "claims", "zone_split", "known_paid_n"), "min": 100,
     "window": ("extras", "claims", "zone_split"),
     "question": "In which U.S. counties are the most paid NFIP flood claims rated outside FEMA's high-risk zones (A and V)?",
     "unit": "claims with a payment and a rated zone",
     "measure": "share of paid NFIP claims with a rated flood zone whose zone is outside zones A and V (zones X, B, C and D)",
     "short": "paid claims outside zones A and V", "meets": "were rated outside zones A and V",
     "fields": "ratedFloodZone, netBuildingPaymentAmount, netContentsPaymentAmount, netIccPaymentAmount, yearOfLoss, nonPaymentReasonBuilding",
     "defs": [],
     "dataset": "FEMA OpenFEMA NFIP Claims v3", "api": "https://www.fema.gov/api/open/v3/NfipClaims",
     "base": "NFIP claims on every building type with a loss in the window, a payment above $0 and a rated flood zone; zone D (possible but undetermined hazard) counts as outside A and V; records FEMA coded deleted or assigned in error left out",
     "limits": ["This is a share of claims, not of homes, and not the chance that any home floods.",
                "The zone is the zone FEMA rated on the claim, which can differ from today's map.",
                "Claims with no rated zone are not in the base."],
     "prior": "No national ranking of counties on this base was found in searches on 2026-11-12.",
     "prior_links": [("Penn State's PSIRC mapped Pennsylvania NFIP claims, including claims outside the Special Flood Hazard Area, from FEMA's 2019 claims release",
                      "https://www.psirc.psu.edu/assets/NFIP_Insights_for_PA.one-pager.2022-09-05.pdf")],
     "prior_rules": ["fema_outside_third"], "policy_col": True, "published": "2026-11-13",
     # review outside-zone-4 M1: say only what FloodSmart states (current high-risk areas, 2014-2024); it does not say paid-only or all claims
     "prior_note": "FEMA's figure uses current high-risk areas and the years 2014 to 2024, and does not say whether it counts only paid claims; this page counts paid claims by the zone rated on each claim.",
     "policy_note": "Policy units outside A and V: the share of NFIP policy units in force in the county, every policy type, rated outside zones A and V.",
     "rules": []},
]
READY = [s for s in SPECS if s.get("ready")]   # a paper ships only after tools/paper_gate.py and both reviews pass (PAPER-GATE-PROMPT)

def names():
    return json.load(open(os.path.join(ROOT, "data", "us", "county_names.json"), encoding="utf-8"))

def _get(rec, path):
    v = rec
    for k in path: v = v.get(k) if isinstance(v, dict) else None
    return v

def wilson(k, n, z=Z90):
    """90% Wilson score interval for k of n, in percent, one decimal."""
    if not n: return None, None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return round(100 * (c - h) / d, 1), round(100 * (c + h) / d, 1)

def rows(spec, recs=None):
    """Every county whose count base meets the minimum: share = num/den on one base, 90% interval, fifth (1 = highest share)."""
    recs = recs if recs is not None else load()
    out = []
    for g, r in recs.items():
        k, n = _get(r, spec["num"]), _get(r, spec["den"])
        if isinstance(k, int) and isinstance(n, int) and n >= spec["min"] and 0 <= k <= n:
            lo, hi = wilson(k, n)
            out.append({"geoid": g, "state": r.get("state", ""), "k": k, "n": n, "value": round(100 * k / n, 1), "lo": lo, "hi": hi})
    out.sort(key=lambda x: (-x["k"] / x["n"], x["geoid"]))
    N = len(out)
    first = {}   # review 11-13: an equal printed share always gets the same fifth (the fifth of its first, highest-placed row)
    for i, x in enumerate(out): x["fifth"] = first.setdefault(x["value"], 1 + (5 * i) // N)
    return out

def context(spec, rec, w0, w1):
    """Per-row context the statistics review asked for (methods review outside-zone-2, M1): the county's policy units outside
    zones A and V today (policies.sfha_share_units is the share inside A and V). None where FEMA's record has no value."""
    sf = _get(rec, ("policies", "sfha_share_units"))
    return {"pol_out": round(100 - sf, 1) if isinstance(sf, (int, float)) else None}

def pooled_boot(rows_, B=2000, seed=20261113):
    """90% range of the pooled share, resampling whole counties (review M2: claims in one county are not independent)."""
    import random
    rnd = random.Random(seed); n = len(rows_); vals = []
    for _ in range(B):
        s = [rows_[rnd.randrange(n)] for _ in range(n)]
        vals.append(100 * sum(x["k"] for x in s) / sum(x["n"] for x in s))
    vals.sort()
    return round(vals[int(0.05 * B)], 1), round(vals[int(0.95 * B) - 1], 1)

def all_pooled(spec, recs):
    """Pooled share over EVERY county with at least one record in the base (review outside-zone-3 M2): the figure to set beside FEMA's."""
    ks = [(_get(r, spec["num"]), _get(r, spec["den"])) for r in recs.values()]
    ks = [(k, n) for k, n in ks if isinstance(k, int) and isinstance(n, int) and n > 0 and 0 <= k <= n]
    return round(100 * sum(k for k, _ in ks) / sum(n for _, n in ks), 1), sum(n for _, n in ks)

def corr(pairs):
    """Pearson correlation of (x, y) pairs, two decimals (descriptive only; no test). None with fewer than 3 pairs."""
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    if len(pairs) < 3: return None
    n = len(pairs); mx = sum(x for x, _ in pairs) / n; my = sum(y for _, y in pairs) / n
    sxy = sum((x - mx) * (y - my) for x, y in pairs); sx = sum((x - mx) ** 2 for x, _ in pairs) ** 0.5; sy = sum((y - my) ** 2 for _, y in pairs) ** 0.5
    return round(sxy / (sx * sy), 2) if sx and sy else None

def excluded(spec, recs):
    """Counties with 1..min-1 records in the base (review M3: selection): count, median share, pooled share."""
    ex = [(_get(r, spec["num"]), _get(r, spec["den"])) for r in recs.values()]
    ex = [(k, n) for k, n in ex if isinstance(k, int) and isinstance(n, int) and 0 < n < spec["min"] and 0 <= k <= n]
    if not ex: return 0, None, None
    import statistics
    return len(ex), round(statistics.median(100 * k / n for k, n in ex), 1), round(100 * sum(k for k, _ in ex) / sum(n for _, n in ex), 1)

def skipped(spec, recs):
    nul = sum(1 for r in recs.values() if not isinstance(_get(r, spec["den"]), int) or _get(r, spec["den"]) == 0)
    small = sum(1 for r in recs.values() if isinstance(_get(r, spec["den"]), int) and 0 < _get(r, spec["den"]) < spec["min"])
    return nul, small

def window(spec, recs):
    for r in recs.values():
        w = _get(r, spec["window"])
        if isinstance(w, dict) and w.get("from"): return w["from"], w["to"]
    return None, None

def load():
    return {f[:5]: json.load(open(os.path.join(ALL, f))) for f in sorted(os.listdir(ALL)) if f.endswith(".json")}

def write_cache():
    recs = load(); out = {}
    for s in READY:
        rs = rows(s, recs)
        out[s["key"]] = {"pool": len(rs), "rows": {x["geoid"]: [x["fifth"], x["value"], x["lo"], x["hi"], x["n"]] for x in rs}}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(out, open(CACHE, "w"))
    return out

def read_cache():
    try: return json.load(open(CACHE))
    except Exception: return {}

if __name__ == "__main__":   # self-check: interval, base, fifths
    lo, hi = wilson(10, 100); assert (lo, hi) == (6.1, 16.0), (lo, hi)   # hand-checked: z=1.6449, (0.1135 -+ 0.0512) / 1.0271
    S = {"num": ("a",), "den": ("b",), "min": 2}
    r = rows(S, {"1": {"a": 1, "b": 2}, "2": {"a": 3, "b": 1}, "3": {"a": 0, "b": 1}, "4": {"a": 2, "b": 2}, "5": {"a": None, "b": 5}})
    assert [(x["geoid"], x["value"]) for x in r] == [("4", 100.0), ("1", 50.0)], r   # k > n and n < min left out
    assert [x["fifth"] for x in r] == [1, 3]
    r = rows(S, {str(i): {"a": a, "b": 2} for i, a in enumerate([2, 1, 1, 1, 0])})   # three tied 50% rows span fifths 2-4
    assert [x["fifth"] for x in r] == [1, 2, 2, 2, 5], [x["fifth"] for x in r]
    print("papers self-test OK")
