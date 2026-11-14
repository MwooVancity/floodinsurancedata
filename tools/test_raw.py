"""Local run of the cloud-only aggregation (extras_raw.py) on a tiny synthetic FEMA download (11-08: a comment pasted
inside a dict literal deleted two keys and the 63-minute cloud refresh died with KeyError 'icc_n'; nothing ran this
code locally). Builds gzipped CSVs with every column the code reads, points extras_raw at them, runs policies() and
claims() for Delaware, and checks the 11-08 figures against hand-counted answers. Writes nothing under data/.
Run: python -I tools/test_raw.py"""
import csv, gzip, os, re, shutil, sys, tempfile
T = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, T)
import extras_raw as X, agg_raw as A, ffcalc

src = open(os.path.join(T, "extras_raw.py"), encoding="utf-8").read()
COLS = sorted(set(re.findall(r'"([a-z]+[A-Z]\w*)"', src))   # every FEMA-style field name in the source (some are read via a loop variable) | set(A.POL_NUM) | set(A.POL_STR) | set(A.CLM_NUM) | set(A.CLM_STR)
              | {ffcalc.PREM, "primaryResidenceIndicator", "netContentsPaymentAmount", "dateOfLoss", "elevatedBuildingIndicator"})
tmp = tempfile.mkdtemp()
def write(ds, recs):
    d = os.path.join(tmp, ds, "DE"); os.makedirs(d)
    with gzip.open(os.path.join(d, "x.csv.gz"), "wt", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, COLS); w.writeheader()
        for r in recs: w.writerow({c: r.get(c, "") for c in COLS})
    open(os.path.join(tmp, ds, "DE.done"), "w").write('{"n": 1, "at": "2026-11-08"}')

base = {"policyCount": 1, "censusGeoid": "10001040100", "occupancyType": 1, "primaryResidenceIndicator": "True", "ratedFloodZone": "AE",
        "reportedZipCode": "19901", "policyEffectiveDate": "2026-01-01", "totalBuildingInsuranceCoverage": 200000, "totalContentsInsuranceCoverage": 0}
pol = ([dict(base, policyCost=1000, **{ffcalc.PREM: 800, "fullRiskPremium": 1200 if i < 30 else 600}) for i in range(40)]      # ZIP 19901: 30 of 40 below full-risk
       + [dict(base, condominiumCoverageTypeCode="U", policyCost=500 + i, **{ffcalc.PREM: 400, "fullRiskPremium": 400}) for i in range(31)]   # 31 condo units: median 515
       # Deductible Choice, county 10005 (unpriced): $1,000 x1 unit, $5,000 on a 2-unit record, blank code 1 unit; condo unit and rental out of the base
       + [dict(base, censusGeoid="10005000100", buildingDeductibleCode=c, policyCount=n, **x) for c, n, x in (
          ("1", 1, {}), ("5", 2, {}), ("", 1, {}), ("1", 1, {"condominiumCoverageTypeCode": "U"}), ("1", 1, {"primaryResidenceIndicator": "False"}))])
clm = ([{"countyCode": "10001", "yearOfLoss": "2023", "floodEvent": "Storm A", "netBuildingPaymentAmount": 5000, "ratedFloodZone": "AE", "dateOfLoss": "2023-09-01"} for _ in range(6)]
       + [{"countyCode": "10001", "yearOfLoss": "2023", "floodEvent": "Storm A", "netBuildingPaymentAmount": 0, "nonPaymentReasonBuilding": "01"} for _ in range(2)]
       + [{"countyCode": "10001", "yearOfLoss": "2023", "floodEvent": "Storm A", "netBuildingPaymentAmount": 0, "nonPaymentReasonBuilding": "98"}]   # deleted in error: not a claim
       + [{"countyCode": "10001", "yearOfLoss": "2024", "floodEvent": "Storm B", "netBuildingPaymentAmount": 0, "nonPaymentReasonBuilding": "01"}]   # unpaid only: no events row
       + [{"countyCode": "10001", "yearOfLoss": "2024", "netBuildingPaymentAmount": 3000, "ratedFloodZone": " x "},   # 11-09 zone_split: outside A/V, lower case
          {"countyCode": "10001", "yearOfLoss": "2024", "netBuildingPaymentAmount": 0, "ratedFloodZone": "X", "nonPaymentReasonBuilding": "01", "floodZoneCurrent": "X"},
          {"countyCode": "10001", "yearOfLoss": "2005", "netBuildingPaymentAmount": 9000, "ratedFloodZone": "X"}]   # before the ten-year window: out of zone_split
       # 11-10 moved/cause10, county 10003: rated X now in " ae " (lower case, spaces) with rain + a handling code; river; handling codes only
       + [{"countyCode": "10003", "yearOfLoss": "2024", "netBuildingPaymentAmount": 2000, "ratedFloodZone": "X", "floodZoneCurrent": " ae ", "causeOfDamage": "4B"},
          {"countyCode": "10003", "yearOfLoss": "2024", "netBuildingPaymentAmount": 1000, "ratedFloodZone": "AE", "causeOfDamage": "2"},
          {"countyCode": "10003", "yearOfLoss": "2024", "netBuildingPaymentAmount": 1000, "ratedFloodZone": "AE", "causeOfDamage": "BD"}]
       # 11-13 damage over coverage, county 10009: 3 in the base (2 over, excess 50,000 and 20,000), 5 left out (condo, rental, 2010, no coverage, no damage)
       + [dict({"countyCode": "10009", "occupancyType": "1", "primaryResidenceIndicator": "1"}, **x) for x in (
          {"yearOfLoss": "2023", "buildingDamageAmount": 300000, "totalBuildingInsuranceCoverage": 250000, "netBuildingPaymentAmount": 240000},
          {"yearOfLoss": "2023", "buildingDamageAmount": 120000, "totalBuildingInsuranceCoverage": 100000, "netBuildingPaymentAmount": 99000},
          {"yearOfLoss": "2024", "buildingDamageAmount": 50000, "totalBuildingInsuranceCoverage": 250000, "netBuildingPaymentAmount": 45000},
          {"yearOfLoss": "2023", "buildingDamageAmount": 300000, "totalBuildingInsuranceCoverage": 100000, "netBuildingPaymentAmount": 99000, "condominiumCoverageTypeCode": "A"},
          {"yearOfLoss": "2023", "buildingDamageAmount": 300000, "totalBuildingInsuranceCoverage": 100000, "netBuildingPaymentAmount": 99000, "primaryResidenceIndicator": "0"},
          {"yearOfLoss": "2010", "buildingDamageAmount": 300000, "totalBuildingInsuranceCoverage": 100000, "netBuildingPaymentAmount": 99000},
          {"yearOfLoss": "2023", "buildingDamageAmount": 300000, "totalBuildingInsuranceCoverage": 0, "netBuildingPaymentAmount": 99000},
          {"yearOfLoss": "2023", "buildingDamageAmount": 0, "totalBuildingInsuranceCoverage": 100000, "netBuildingPaymentAmount": 99000})]
       # Flood Calendar, county 10007: 2 March claims (one unpaid) in the window; bad date; 2010 outside the window; code 98 out
       + [dict({"countyCode": "10007"}, **x) for x in (
          {"yearOfLoss": "2024", "dateOfLoss": "2024-03-15", "netBuildingPaymentAmount": 1000}, {"yearOfLoss": "2024", "dateOfLoss": "2024-03-02T00:00:00.000Z", "nonPaymentReasonBuilding": "01"},
          {"yearOfLoss": "2024", "dateOfLoss": "2024-3-5", "netBuildingPaymentAmount": 1000}, {"yearOfLoss": "2010", "dateOfLoss": "2010-03-01", "netBuildingPaymentAmount": 1000},
          {"yearOfLoss": "2024", "dateOfLoss": "2024-03-01", "nonPaymentReasonBuilding": "98"})])
write("NfipPolicies", pol); write("NfipClaims", clm)
# 11-09 cost trend (pull_bulk.trend's columns): 2022 all priced; 2023 under 30 priced; 2024 95 of 100 priced; 2025 35 of 40 (< 90%)
_t = lambda y, n, cost, **k: [dict({"year": y, "propertyState": "DE", "censusGeoid": "10001040100", "occupancyType": "1",
                                    "primaryResidenceIndicator": "True", "condominiumCoverageTypeCode": "N", "policyCost": cost}, **k) for _ in range(n)]
trd = (_t(2022, 35, 900) + _t(2022, 2, 50, condominiumCoverageTypeCode="U") + _t(2022, 1, 50, primaryResidenceIndicator="False")
       + _t(2023, 20, 700) + _t(2023, 10, "") + _t(2024, 57, 800) + _t(2024, 3, 0) + _t(2025, 35, 850) + _t(2025, 5, "")
       + _t(2021, 81, 600))   # 81 records vs 40 today: over twice, so the records may place homes differently; left out
os.makedirs(os.path.join(tmp, "NfipPoliciesTrend", "DE"))
with gzip.open(os.path.join(tmp, "NfipPoliciesTrend", "DE", "bulk.csv.gz"), "wt", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, list(trd[0])); w.writeheader(); w.writerows(trd)
X.RAW = tmp
try:
    P, C = X.policies("DE"), X.claims("DE")
    p = P["10001"]
    assert p["condo_unit_cost_n"] == 31 and p["condo_unit_cost_median"] == 515, (p["condo_unit_cost_n"], p["condo_unit_cost_median"])
    # 11-12 cloud field batch: the new keys exist, counts are whole numbers, every within-zone cell names its zone and n
    assert {"prem_zone_elev", "obstruction_counts", "basement_counts", "floodproofed_n", "deductibles_by_zone"} <= set(p), sorted(p)
    assert all(k.split("|")[0] in ("AE", "X") and k.split("|")[1] in ("elevated", "not") and v["n"] >= 1 for k, v in p["prem_zone_elev"].items()), p["prem_zone_elev"]
    assert sum(p["basement_counts"].values()) == p["sf_n"], (p["basement_counts"], p["sf_n"])   # every single-family record lands in one bucket
    p5 = P["10005"]; assert (p5["deductible_units"], p5["deductible_units_blank"]) == ({"1000": 1, "5000": 2}, 1), p5   # SUM policyCount, base only
    lm = C["10007"]["loss_month_n"]; assert (lm["by_month"], lm["no_month"], lm["from"] <= "2024" <= lm["to"]) == ({"03": 2}, 1, True), lm
    assert C["10001"]["loss_month_n"]["by_month"] == {"09": 6}, C["10001"]["loss_month_n"]   # every window claim lands in a month or no_month
    assert C["10001"]["loss_month_n"]["by_year_month"] == {"2023-09": 6}, C["10001"]["loss_month_n"]   # Flood Calendar one-storm flag base
    assert sum(lm["by_year_month"].values()) == sum(lm["by_month"].values()), lm   # same claims, split by year too
    assert p["below_by_crs"] == {"blank": [40, 30]}, p["below_by_crs"]   # Price Gap M3: condo units out, 30 of 40 below, CRS blank kept as its own bucket
    uw = C["10001"]["underinsured"]   # 11-13 Underinsured paper: one base (window, single-family primary, damage+payment+coverage > 0)
    assert set(uw) == {"n", "over", "from", "to", "excess_median", "over_by_year"} and 0 <= uw["over"] <= uw["n"] <= C["10001"]["damage_n"], uw
    u9 = C["10009"]["underinsured"]; assert (u9["n"], u9["over"], u9["excess_median"], u9["over_by_year"]) == (3, 2, 35000, {"2023": 2}), u9   # base rules + M1.4/M1.8 fields
    assert sum(uw["over_by_year"].values()) == uw["over"] and (uw["excess_median"] is None) == (uw["over"] == 0), uw   # every over-claim in one year bucket
    ev = {e["name"]: e for e in C["10001"]["events"]}
    assert set(ev) == {"Storm A"}, ev                                    # an event with no paid claim is not a row
    a = ev["Storm A"]
    assert (a["claims"], a["filed"], a["paid_pct"]) == (6, 8, 75.0), a    # 6 paid of 8 filed; the code-98 record is out
    z = {d["zip"]: d for d in ffcalc.aggregate_policies([dict(r, **{k: (float(v) if isinstance(v, (int, float)) else v) for k, v in r.items()}) for r in pol])["by_zip"]}
    assert (z["19901"]["below_n"], z["19901"]["share_below"]) == (40, 75.0), z["19901"]   # 30 of 40 single-family; the 31 condo units are outside the base
    zs = C["10001"]["zone_split"]   # 6 AE paid $30,000; 2 X (1 paid $3,000); 3 with no zone; the 2005 claim outside the window
    assert (zs["known_n"], zs["known_paid_n"], zs["known_paid"], zs["out_n"], zs["out_paid_n"], zs["out_paid"], zs["blank_n"]) == (8, 7, 33000, 2, 1, 3000, 3), zs
    assert (zs["out_pct"], zs["out_paid_pct"]) == (25.0, 9.1), zs   # 2 of 8 claims; $3,000 of $33,000
    assert "zone_split" not in C["ST"] and "_pb" in C["ST"]
    mv, mv3, c1, c3 = C["10001"]["moved"], C["10003"]["moved"], C["10001"]["cause10"], C["10003"]["cause10"]
    assert (mv["rated_out_known"], mv["now_av"], mv["current_blank"]) == (1, 0, 1), mv     # unpaid X now X; paid " x " has no current zone
    assert (mv3["rated_out_known"], mv3["now_av"], mv3["current_blank"]) == (1, 1, 0), mv3  # X now " ae "
    assert (c1["paid_n"], c1["with_cause"], c1["by_code"]) == (7, 0, {}), c1             # 6 AE + 1 X paid in the window, no cause codes
    assert (c3["paid_n"], c3["with_cause"], c3["by_code"]) == (3, 2, {"4": 1, "2": 1}), c3  # "BD" is handling only: no cause
    X.ROOT = tmp; os.makedirs(os.path.join(tmp, "data", "us")); cs = os.path.join(tmp, "data", "us", "claim_size.json")
    X.NAT_PB.clear(); X.NAT_PB["DE"] = [1000] * 40; X.write_claim_size()
    assert not os.path.exists(cs)   # one state ran: no national figure
    X.NAT_PB.update({s: [] for s in A.NAMES}); X.NAT_PB["DE"] = [1000] * 20 + [3000] * 21; X.write_claim_size()
    assert __import__("json").load(open(cs))["p50"] == 3000 and __import__("json").load(open(cs))["n"] == 41
    tr = [(t["year"], t["median"], t["n"], t["sf_n"]) for t in p["cost_trend"]]
    assert tr == [(2021, None, 81, 81), (2022, 900, 35, 35), (2023, None, 20, 30), (2024, 800, 57, 60), (2025, None, 35, 40), (X._A.year, 1000, 40, 40)], tr
    # 11-09 feed sweep: county_detail.json is written by the monthly state job again (collector deleted 10-29)
    import collect_state_small as CSS
    CSS.write_detail("DE", tmp, [{"attributes": {"STCOFIPS": "10001", "COUNTY": "Kent", "NRI_VER": "December 2025", "CFLD_RISKR": "Relatively Low", "IFLD_RISKR": "Relatively High"}},
                                 {"attributes": {"STCOFIPS": "10003", "COUNTY": "New Castle", "NRI_VER": "December 2025"}}],
                     [{"fipsCode": "10001", "resContractsInForce": "50", "resContractsInForceSfha": "10", "totalResStructures": "1000", "totalResStructuresSfha": "20", "asOfDate": "2026-08-03T00:00:00.000Z"},
                      {"fipsCode": "10003", "resContractsInForce": "5", "totalResStructures": "0", "asOfDate": ""}])
    det = __import__("json").load(open(os.path.join(tmp, "county_detail.json")))
    assert det["_nri"]["version"] == "December 2025" and det["10001"]["nri"]["inland"]["risk_rating"] == "Relatively High", det
    assert det["10001"]["penetration"]["overall_pct"] == 5.0 and det["10001"]["penetration"]["sfha_pct"] == 50.0 and det["10001"]["penetration"]["asof"] == "2026-08-03"
    assert det["10003"]["penetration"]["overall_pct"] is None and det["10003"]["penetration"]["asof"] is None   # no homes, no date: no card
    CSS.write_detail("DE", tmp, [{"attributes": {"STCOFIPS": "10001", "NRI_VER": "a"}}, {"attributes": {"STCOFIPS": "10003", "NRI_VER": "b"}}], [])
    assert __import__("json").load(open(os.path.join(tmp, "county_detail.json")))["_nri"]["version"] is None   # two versions: none printed
    print("test_raw: extras_raw policies()+claims() run on a synthetic download; condo cost, event paid share, cost trend, county detail OK")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
