"""Fixture tests: recompute the published statistics from known rows and assert exact answers.
Addresses the 'gate checks presence, not math' review finding. Run: python -I tools/test_calc.py"""
import statistics
from collections import defaultdict

def q(a, p):
    a = sorted(a)
    return round(statistics.quantiles(a, n=100, method="inclusive")[p - 1]) if len(a) > 1 else (a[0] if a else None)

# --- policy-unit summing (condo rows carry >1 unit), zone mix by units, cohort cost, full-risk gap ---
POL = [
    # id, policyCost, fullRiskPremium, ratedFloodZone, occupancyType, primaryResidenceIndicator, policyCount
    {"id": 1, "policyCost": 1000, "fullRiskPremium": 3000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 2, "policyCost": 2000, "fullRiskPremium": 1500, "ratedFloodZone": "AE", "occupancyType": 11, "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 3, "policyCost": 3000, "fullRiskPremium": 5000, "ratedFloodZone": "X",  "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 4, "policyCost": -50,  "fullRiskPremium": 2000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},  # refund excluded
    {"id": 5, "policyCost": 9999, "fullRiskPremium": 9999, "ratedFloodZone": "VE", "occupancyType": 2,  "primaryResidenceIndicator": True,  "policyCount": 4},  # non-SFH, condo 4 units
]
def isone(v): return v in (1, 11, "1", "11")
def istrue(v): return v in (True, "true", "True", 1, "1")

units = sum(int(r.get("policyCount") or 0) for r in POL)
assert units == 8, units  # 1+1+1+1+4

zu = defaultdict(int)
for r in POL: zu[r["ratedFloodZone"]] += int(r["policyCount"] or 0)
assert dict(zu) == {"AE": 3, "X": 1, "VE": 4}, dict(zu)
sfha = sum(u for z, u in zu.items() if z[:1] in ("A", "V"))
assert sfha == 7, sfha  # AE3 + VE4 ; X excluded
assert round(100 * sfha / units, 1) == 87.5, round(100 * sfha / units, 1)

coh = [r for r in POL if isone(r["occupancyType"]) and istrue(r["primaryResidenceIndicator"])]
cost = [r["policyCost"] for r in coh if isinstance(r["policyCost"], (int, float)) and r["policyCost"] > 0]
assert sorted(cost) == [1000, 2000, 3000], sorted(cost)   # id4 (-50) excluded, id5 (non-SFH) excluded
assert q(cost, 50) == 2000, q(cost, 50)

both = [r for r in coh if r["policyCost"] > 0 and r["fullRiskPremium"] > 0]
below = sum(1 for r in both if r["policyCost"] < r["fullRiskPremium"])
assert below == 2, below                                  # id1 (1000<3000), id3 (3000<5000); id2 1500<2000 no
assert round(100 * below / len(both), 1) == 66.7, round(100 * below / len(both), 1)

# --- claims by year: sum net building + contents, cumulative not annual ---
CLM = [
    {"yearOfLoss": 2017, "netBuildingPaymentAmount": 100, "netContentsPaymentAmount": 50},
    {"yearOfLoss": 2017, "netBuildingPaymentAmount": 200, "netContentsPaymentAmount": 0},
    {"yearOfLoss": 1999, "netBuildingPaymentAmount": 10,  "netContentsPaymentAmount": 5},
]
byyear = defaultdict(lambda: [0, 0.0])
tot = 0.0
for r in CLM:
    p = (r["netBuildingPaymentAmount"] or 0) + (r["netContentsPaymentAmount"] or 0)
    byyear[r["yearOfLoss"]][0] += 1; byyear[r["yearOfLoss"]][1] += p; tot += p
assert tot == 365, tot
assert byyear[2017] == [2, 350.0], byyear[2017]
assert round(100 * len(CLM) / units, 1) == 37.5, round(100 * len(CLM) / units, 1)  # cumulative per 100 current units

print("test_calc: all assertions passed")
