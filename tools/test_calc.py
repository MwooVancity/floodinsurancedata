"""Fixture tests that exercise the PRODUCTION calculations in ffcalc.py (not a re-implementation),
with known answers: duplicate exclusion, refunds, nulls, multi-unit condo rows, non-SFH, percentiles,
full-risk gap, claims aggregation, and the cost-sample suppression rule. Run: python -I tools/test_calc.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops script dir
import ffcalc

POL = [
    {"id": 1, "policyCost": 1000, "fullRiskPremium": 3000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 2, "policyCost": 2000, "fullRiskPremium": 1500, "ratedFloodZone": "AE", "occupancyType": 11, "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 3, "policyCost": 3000, "fullRiskPremium": 5000, "ratedFloodZone": "X",  "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 4, "policyCost": -50,  "fullRiskPremium": 2000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},  # refund excluded
    {"id": 5, "policyCost": None, "fullRiskPremium": 2000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},  # null cost excluded
    {"id": 6, "policyCost": 9999, "fullRiskPremium": 9999, "ratedFloodZone": "VE", "occupancyType": 2,  "primaryResidenceIndicator": True,  "policyCount": 4},  # non-SFH condo, 4 units
]
P = ffcalc.aggregate_policies(POL)
assert P["units"] == 9, P["units"]                                  # 1*5 + 4
assert P["cohort_n"] == 5, P["cohort_n"]                            # ids 1-5 (SFH primary); id6 non-SFH
assert P["cost_n"] == 3, P["cost_n"]                                # ids 1,2,3 (−50 and null dropped)
assert P["cost_excluded"] == 2, P["cost_excluded"]
assert P["p50"] == 2000, P["p50"]
assert P["zone_units"] == {"AE": 4, "VE": 4, "X": 1}, P["zone_units"]   # zone mix counts all policies, not just valid-cost ones
assert P["sfha_units"] == 8 and P["sfha_share_units"] == round(100 * 8 / 9, 1), (P["sfha_units"], P["sfha_share_units"])
assert P["share_below"] == 66.7 and P["below_n"] == 3, (P["share_below"], P["below_n"])  # id1,id3 below; id2 not
assert P["spread_ok"] is False, P["spread_ok"]                      # only 3 valid costs < 100 -> suppress

CLM = [
    {"yearOfLoss": 2017, "netBuildingPaymentAmount": 100, "netContentsPaymentAmount": 50},
    {"yearOfLoss": 2017, "netBuildingPaymentAmount": 200, "netContentsPaymentAmount": 0},
    {"yearOfLoss": 1999, "netBuildingPaymentAmount": 10,  "netContentsPaymentAmount": 5},
]
C = ffcalc.aggregate_claims(CLM, P["units"])
assert C["total_paid"] == 365, C["total_paid"]
assert C["by_year"]["2017"] == [2, 350], C["by_year"]["2017"]
assert C["year_min"] == 1999 and C["year_max"] == 2017
assert C["cumulative_per_100_current_units"] == round(100 * 3 / 9, 1)

# small fixture: per-zone/per-year medians need enough obs, so they stay empty here
assert P["cost_by_zone"] == {}, P["cost_by_zone"]
assert P["cost_by_year"] == {}, P["cost_by_year"]
assert P["coverage_building"] == 0 and P["coverage_contents"] == 0

# spread_ok + cost_by_zone populate once enough valid costs exist
big = [{"id": i, "policyCost": 1000 + i, "fullRiskPremium": 2000, "ratedFloodZone": "AE",
        "occupancyType": 1, "primaryResidenceIndicator": True, "policyCount": 1,
        "policyEffectiveDate": "2026-03-01", "totalBuildingInsuranceCoverage": 250000} for i in range(120)]
B = ffcalc.aggregate_policies(big, asof="2026-07-31")
assert B["spread_ok"] is True
assert B["cost_by_zone"]["AE"]["n"] == 120, B["cost_by_zone"]
assert B["cost_by_year"]["2026"]["n"] == 120, B["cost_by_year"]
assert B["recent_median"] is not None and B["recent_n"] == 120   # all written within 12mo of asof
assert B["coverage_building"] == 120 * 250000

# percentile convention edge cases (inclusive method), per review request
assert ffcalc.pctl([], 50) is None                       # empty
assert ffcalc.pctl([1200], 50) == 1200                   # single observation -> the value
assert ffcalc.pctl([1200], 25) == 1200
assert ffcalc.pctl([10, 20, 30, 40], 50) == 25           # even-sized -> interpolated midpoint
assert ffcalc.pctl([5, 5, 5, 5], 50) == 5                # repeated values
assert ffcalc.pctl([5, 5, 5, 5], 90) == 5
assert ffcalc.pctl([1, 2, 3, 4, 5], 50) == 3             # odd-sized -> middle

print("test_calc: all assertions passed (exercising ffcalc production functions)")
