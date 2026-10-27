"""Shared production calculations. Imported by collect.py (real pipeline) AND test_calc.py
(fixtures), so the tests exercise the exact code that ships. Pure functions, no I/O."""
import math
import statistics
from collections import defaultdict

SFHA_PREFIXES = ("A", "V")
SMALL_COHORT = 100  # min VALID COST observations to publish a percentile spread
HFIAA_CAP = 0.18    # statutory max annual NFIP premium increase for most primary residences (HFIAA / Risk Rating 2.0)

def years_to_full_risk(current, full_risk, cap=HFIAA_CAP):
    """Minimum annual renewals for `current` to reach `full_risk` at the statutory max increase `cap`.
    A labeled legal RULE (the HFIAA cap), not a forecast. Returns None when there is no gap to close."""
    if not current or not full_risk or full_risk <= current:
        return None
    return math.ceil(math.log(full_risk / current) / math.log(1 + cap))

def isone(v): return v in (1, 11, "1", "11")          # single-family occupancy types
def istrue(v): return v in (True, "true", "True", 1, "1")

def pctl(values, p):
    a = sorted(values)
    if not a: return None
    if len(a) == 1: return round(a[0])
    return round(statistics.quantiles(a, n=100, method="inclusive")[p - 1])

ZONE_MIN = 50   # min valid-cost observations to publish a per-zone median
YEAR_MIN = 30   # min valid-cost observations to publish a per-year median (trend)
ZIP_MIN = 25    # min priced single-family policies to publish a per-ZIP median

def _valid_cost(r): return isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0

PREM = "totalInsurancePremiumOfThePolicy"

def premium_gap(coh):
    """Like-for-like gap to FEMA's full-risk price: premium charged vs fullRiskPremium, BOTH premium-only.
    policyCost adds the reserve fund assessment, federal policy fee and HFIAA surcharge (FEMA data
    dictionary), so comparing it to fullRiskPremium overstated bills and understated 'share below'."""
    both = [r for r in coh if isinstance(r.get(PREM), (int, float)) and r[PREM] > 0
            and isinstance(r.get("fullRiskPremium"), (int, float)) and r["fullRiskPremium"] > 0]
    below = sum(1 for r in both if r[PREM] < r["fullRiskPremium"])
    return {"prem_median": pctl([r[PREM] for r in both], 50),
            "frp_median": pctl([r["fullRiskPremium"] for r in both], 50), "frp_n": len(both),
            "share_below": round(100 * below / len(both), 1) if both else None, "below_n": len(both),
            "gap_basis": "premium"}

def aggregate_policies(rows):
    units = sum(int(r.get("policyCount") or 0) for r in rows)
    coh = [r for r in rows if isone(r.get("occupancyType")) and istrue(r.get("primaryResidenceIndicator"))]
    cost = [r["policyCost"] for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0]
    # cost by flood zone (median per zone, only where enough valid observations)
    zc = defaultdict(list)
    for r in coh:
        if _valid_cost(r): zc[(r.get("ratedFloodZone") or "Unknown").strip()].append(r["policyCost"])
    cost_by_zone = {z: {"median": pctl(v, 50), "n": len(v)} for z, v in zc.items() if len(v) >= ZONE_MIN}
    cost_by_zone = dict(sorted(cost_by_zone.items(), key=lambda kv: -kv[1]["n"]))
    # premium trend: median cost by policy effective YEAR (cohort-mix caveat printed on page)
    yc = defaultdict(list)
    for r in coh:
        d = r.get("policyEffectiveDate")
        if _valid_cost(r) and isinstance(d, str) and len(d) >= 4 and d[:4].isdigit():
            yc[d[:4]].append(r["policyCost"])
    cost_by_year = {y: {"median": pctl(v, 50), "n": len(v)} for y, v in sorted(yc.items()) if len(v) >= YEAR_MIN}
    cov_b = sum(r.get("totalBuildingInsuranceCoverage") or 0 for r in rows)
    cov_c = sum(r.get("totalContentsInsuranceCoverage") or 0 for r in rows)
    # per-ZIP: units (all policies) + cohort median cost where enough valid observations (>=25)
    zu_zip = defaultdict(int); zc_zip = defaultdict(list)
    for r in rows:
        z = (str(r.get("reportedZipCode") or "")).strip()
        if z: zu_zip[z] += int(r.get("policyCount") or 0)
    for r in coh:
        if _valid_cost(r):
            z = (str(r.get("reportedZipCode") or "")).strip()
            if z: zc_zip[z].append(r["policyCost"])
    by_zip = sorted(
        ({"zip": z, "units": zu_zip[z], "cost_n": len(zc_zip[z]),
          "median": pctl(zc_zip[z], 50) if len(zc_zip[z]) >= ZIP_MIN else None} for z in zu_zip),
        key=lambda d: -d["units"])   # every ZIP: a reader's ZIP must never read "no data" because it ranked 26th
    gap = premium_gap(coh)
    zu = defaultdict(int)
    for r in rows:
        zu[(r.get("ratedFloodZone") or "Unknown").strip()] += int(r.get("policyCount") or 0)
    sfha = sum(u for z, u in zu.items() if z[:1] in SFHA_PREFIXES)
    return {
        "rows": len(rows), "units": units,
        "cohort_n": len(coh), "cost_n": len(cost),
        "cost_excluded": len(coh) - len(cost),          # cohort records dropped for null/non-positive cost
        "p25": pctl(cost, 25), "p50": pctl(cost, 50), "p75": pctl(cost, 75), "p90": pctl(cost, 90),
        **gap,
        "zone_units": dict(sorted(zu.items(), key=lambda x: -x[1])[:12]),
        "sfha_units": sfha, "sfha_share_units": round(100 * sfha / units, 1) if units else None,
        "spread_ok": len(cost) >= SMALL_COHORT,         # publish the spread only on enough VALID cost obs
        "cost_by_zone": cost_by_zone, "cost_by_year": cost_by_year,
        "coverage_building": round(cov_b), "coverage_contents": round(cov_c),
        "by_zip": by_zip,
    }

# National Risk Index flood rating scale (worst of coastal/inland), for the state tile-map colour/order.
RISK_ORDER = {"Very Low": 0, "Relatively Low": 1, "Relatively Moderate": 2,
              "Relatively High": 3, "Very High": 4, "No Rating": -1, "Not Applicable": -1,
              "Insufficient Data": -1, None: -1}
def worst_flood_rating(coastal, inland):
    best = -1; label = None
    for r in (coastal, inland):
        o = RISK_ORDER.get(r, -1)
        if o > best: best, label = o, r
    return label

def aggregate_claims(rows, units):
    byyear = defaultdict(lambda: [0, 0.0])
    tot = 0.0
    for r in rows:
        y = r.get("yearOfLoss")
        paid = (r.get("netBuildingPaymentAmount") or 0) + (r.get("netContentsPaymentAmount") or 0)
        if y:
            byyear[int(y)][0] += 1
            byyear[int(y)][1] += paid
        tot += paid
    yrs = sorted(byyear)
    return {
        "rows": len(rows), "total_paid": round(tot),
        "by_year": {str(y): [c, round(p)] for y, (c, p) in sorted(byyear.items())},
        "cumulative_per_100_current_units": round(100 * len(rows) / units, 1) if units else None,
        "year_min": yrs[0] if yrs else None, "year_max": yrs[-1] if yrs else None,
    }
