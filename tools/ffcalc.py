"""Shared production calculations. Imported by collect.py (real pipeline) AND test_calc.py
(fixtures), so the tests exercise the exact code that ships. Pure functions, no I/O."""
import statistics
from collections import defaultdict

SFHA_PREFIXES = ("A", "V")
SMALL_COHORT = 100  # min VALID COST observations to publish a percentile spread

def isone(v): return v in (1, 11, "1", "11")          # single-family occupancy types
def istrue(v): return v in (True, "true", "True", 1, "1")

def pctl(values, p):
    a = sorted(values)
    if not a: return None
    if len(a) == 1: return round(a[0])
    return round(statistics.quantiles(a, n=100, method="inclusive")[p - 1])

def aggregate_policies(rows):
    units = sum(int(r.get("policyCount") or 0) for r in rows)
    coh = [r for r in rows if isone(r.get("occupancyType")) and istrue(r.get("primaryResidenceIndicator"))]
    cost = [r["policyCost"] for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0]
    both = [r for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0
            and isinstance(r.get("fullRiskPremium"), (int, float)) and r["fullRiskPremium"] > 0]
    frp = [r["fullRiskPremium"] for r in both]
    below = sum(1 for r in both if r["policyCost"] < r["fullRiskPremium"])
    zu = defaultdict(int)
    for r in rows:
        zu[(r.get("ratedFloodZone") or "Unknown").strip()] += int(r.get("policyCount") or 0)
    sfha = sum(u for z, u in zu.items() if z[:1] in SFHA_PREFIXES)
    return {
        "rows": len(rows), "units": units,
        "cohort_n": len(coh), "cost_n": len(cost),
        "cost_excluded": len(coh) - len(cost),          # cohort records dropped for null/non-positive cost
        "p25": pctl(cost, 25), "p50": pctl(cost, 50), "p75": pctl(cost, 75), "p90": pctl(cost, 90),
        "frp_median": pctl(frp, 50), "frp_n": len(frp),
        "share_below": round(100 * below / len(both), 1) if both else None, "below_n": len(both),
        "zone_units": dict(sorted(zu.items(), key=lambda x: -x[1])[:12]),
        "sfha_units": sfha, "sfha_share_units": round(100 * sfha / units, 1) if units else None,
        "spread_ok": len(cost) >= SMALL_COHORT,         # publish the spread only on enough VALID cost obs
    }

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
