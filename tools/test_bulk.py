"""Run of pull_bulk.trend() on a tiny synthetic parquet (11-09: the cost-trend pass only runs in the cloud, after an 8-minute
download; a slip there would show up an hour in). Checks the snapshot filter (in force = effective on or before the day,
ending after it), the values the single-family rule reads (1 -> "1", True -> "True"), territories left out, and the
Feb 29 as-of day. Needs pyarrow (the refresh job installs it). Writes nothing under data/.
Run: python -I tools/test_bulk.py"""
import csv, datetime, gzip, os, shutil, sys, tempfile
T = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, T)
import pull_raw as PR, pull_bulk as B
import pyarrow as pa, pyarrow.parquet as pq

D = datetime.date
rows = [  # (state, effective, termination, cost)
    ("DE", D(2021, 9, 1), D(2022, 9, 1), 900.0),    # in force on 2022-08-31 only
    ("DE", D(2020, 8, 31), D(2021, 8, 31), 500.0),  # ends ON 2021-08-31: not in force that day
    ("DE", D(2025, 8, 31), D(2026, 8, 31), 850.0),  # starts on the day: in force on 2025-08-31
    ("PR", D(2021, 9, 1), D(2022, 9, 1), 700.0)]    # a territory: not on the site
t = pa.table({"propertyState": [r[0] for r in rows], "censusGeoid": ["10001040100"] * len(rows),
              "occupancyType": pa.array([1] * len(rows), pa.int64()), "primaryResidenceIndicator": [True] * len(rows),
              "condominiumCoverageTypeCode": ["N"] * len(rows), "policyCost": [r[3] for r in rows],
              "policyEffectiveDate": pa.array([r[1] for r in rows], pa.date32()), "policyTerminationDate": pa.array([r[2] for r in rows], pa.date32())})
tmp = tempfile.mkdtemp(); f = os.path.join(tmp, "p.parquet"); pq.write_table(t, f)
PR.RAW, PR.ASOF_DATE = tmp, D(2026, 8, 31)
try:
    B.trend(f)
    got = list(csv.DictReader(gzip.open(os.path.join(tmp, "NfipPoliciesTrend", "DE", "bulk.csv.gz"), "rt", encoding="utf-8")))
    assert [(r["year"], r["policyCost"]) for r in got] == [("2022", "900.0"), ("2025", "850.0")], got
    assert got[0]["occupancyType"] == "1" and got[0]["primaryResidenceIndicator"] == "True", got[0]
    assert not list(csv.DictReader(gzip.open(os.path.join(tmp, "NfipPoliciesTrend", "AK", "bulk.csv.gz"), "rt", encoding="utf-8")))
    PR.ASOF_DATE = D(2028, 2, 29); assert B.snap(2027) == D(2027, 2, 28) and B.snap(2024) == D(2024, 2, 29)
    print("test_bulk: trend snapshot filter, field text, territories, Feb 29 OK")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
