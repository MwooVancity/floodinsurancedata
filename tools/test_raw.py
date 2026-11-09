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
       + [dict(base, condominiumCoverageTypeCode="U", policyCost=500 + i, **{ffcalc.PREM: 400, "fullRiskPremium": 400}) for i in range(31)])   # 31 condo units: median 515
clm = ([{"countyCode": "10001", "yearOfLoss": "2023", "floodEvent": "Storm A", "netBuildingPaymentAmount": 5000, "ratedFloodZone": "AE", "dateOfLoss": "2023-09-01"} for _ in range(6)]
       + [{"countyCode": "10001", "yearOfLoss": "2023", "floodEvent": "Storm A", "netBuildingPaymentAmount": 0, "nonPaymentReasonBuilding": "01"} for _ in range(2)]
       + [{"countyCode": "10001", "yearOfLoss": "2023", "floodEvent": "Storm A", "netBuildingPaymentAmount": 0, "nonPaymentReasonBuilding": "98"}]   # deleted in error: not a claim
       + [{"countyCode": "10001", "yearOfLoss": "2024", "floodEvent": "Storm B", "netBuildingPaymentAmount": 0, "nonPaymentReasonBuilding": "01"}])   # unpaid only: no events row
write("NfipPolicies", pol); write("NfipClaims", clm)
X.RAW = tmp
try:
    P, C = X.policies("DE"), X.claims("DE")
    p = P["10001"]
    assert p["condo_unit_cost_n"] == 31 and p["condo_unit_cost_median"] == 515, (p["condo_unit_cost_n"], p["condo_unit_cost_median"])
    ev = {e["name"]: e for e in C["10001"]["events"]}
    assert set(ev) == {"Storm A"}, ev                                    # an event with no paid claim is not a row
    a = ev["Storm A"]
    assert (a["claims"], a["filed"], a["paid_pct"]) == (6, 8, 75.0), a    # 6 paid of 8 filed; the code-98 record is out
    z = {d["zip"]: d for d in ffcalc.aggregate_policies([dict(r, **{k: (float(v) if isinstance(v, (int, float)) else v) for k, v in r.items()}) for r in pol])["by_zip"]}
    assert (z["19901"]["below_n"], z["19901"]["share_below"]) == (40, 75.0), z["19901"]   # 30 of 40 single-family; the 31 condo units are outside the base
    print("test_raw: extras_raw policies()+claims() run on a synthetic download; condo cost, event paid share OK")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
