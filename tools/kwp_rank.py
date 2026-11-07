"""Rank the Keyword Planner export by kind (generic, zone, state, county, town). Input: newest data/kwp/*.csv (UTF-16, tab).
Run: python -I tools/kwp_rank.py. Volumes are Google's ranges; 'low' is the range floor, so totals are floors, not estimates."""
import collections, csv, glob, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sorted(glob.glob(os.path.join(ROOT, "data", "kwp", "*.csv")))[-1]
rows = list(csv.DictReader(io.StringIO(open(path, encoding="utf-16").read().split("\n", 2)[2]), delimiter="\t"))
rows = [r for r in rows if r.get("Keyword", "").strip()]  # drop Google's blank total rows
STATES = {s.lower() for s in NAMES.values()}
import json
TOWNS = {t.lower() for t in json.load(open(os.path.join(ROOT, "data", "us", "zip_places.json"), encoding="utf-8")).values()}

BAND_FLOOR = {50: 10, 500: 100, 5000: 1000, 50000: 10000, 500000: 100000}   # the export writes each band (10-100, 100-1K...) as 50, 500...: read 5x high until 11-06

def low(v):  # band floor: "500.0" -> 100; "100 – 1K" -> 100; an exact figure stays as is
    m = re.match(r"\s*([\d.]+)(K?)", v or "")
    if not m: return 0
    n = int(float(m[1]) * (1000 if m[2] else 1))
    return BAND_FLOOR.get(n, n) if not m[2] else n

def kind(k):
    if re.search(r"\bzone (a|ae|ah|ao|v|ve|x|shaded x|d|b|c)\b", k): return "zone"
    if " county " in f" {k} " or " parish " in f" {k} " or " borough " in f" {k} ": return "county"
    tail = re.sub(r"^(flood insurance cost|flood insurance|flood zone map) ", "", k)
    if tail != k and tail in STATES: return "state"
    if k.startswith("flood insurance ") and tail in TOWNS: return "town"
    return "generic"

if "--queue" in sys.argv:   # reorder state/county-queue.json by Keyword Planner searches for the county name (owner 11-05)
    vol = collections.Counter()
    for r in rows:
        m = re.match(r"(.+? (?:county|parish|borough)) (?:flood insurance|flood zone map)$", r["Keyword"])
        if m: vol[m[1]] += low(r["Avg. monthly searches"])
    qp = os.path.join(ROOT, "state", "county-queue.json")
    q = json.load(open(qp, encoding="utf-8"))
    same = collections.Counter()   # "harris county" TX and GA share one search: split by insured units, so TX keeps nearly all
    for p in q: same[p["short"].lower()] += p.get("units") or 0
    key = lambda ip: (-(vol[ip[1]["short"].lower()] * (ip[1].get("units") or 0) / (same[ip[1]["short"].lower()] or 1)), ip[0])
    q2 = [p for _, p in sorted(enumerate(q), key=key)]
    for p in q2:   # band floor of searches for this county name, kept only by the county holding most of the name's insured units
        nm = p["short"].lower()   # (audit 11-07: Lee County AR, 71 homes, must not inherit Lee County FL's searches); add_counties publishes kw > 0
        p["kw"] = vol[nm] if 2 * (p.get("units") or 0) > (same[nm] or 0) else 0
    json.dump(q2, open(qp, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    print("queue reordered:", len(q2), "| first 10:", [p["slug"] for p in q2[:10]]); sys.exit()

by = collections.defaultdict(list)
for r in rows:
    by[kind(r["Keyword"])].append((low(r["Avg. monthly searches"]), r["Avg. monthly searches"], r["Keyword"]))
for k, v in sorted(by.items(), key=lambda kv: -sum(x[0] for x in kv[1])):
    v.sort(reverse=True)
    with_vol = sum(1 for x in v if x[0] >= 10)
    print(f"\n== {k}: {len(v)} keywords, {with_vol} with 10+/mo, floor total {sum(x[0] for x in v):,}/mo")
    for x in v[:12]: print(f"  {x[1]:>12}  {x[2]}")
