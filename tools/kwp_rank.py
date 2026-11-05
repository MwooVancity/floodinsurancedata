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

def low(v):  # "100 – 1K" -> 100; "1K – 10K" -> 1000; "0 – 10" -> 0
    m = re.match(r"\s*([\d.]+)(K?)", v or "")
    return int(float(m[1]) * (1000 if m[2] else 1)) if m else 0

def kind(k):
    if re.search(r"\bzone (a|ae|ah|ao|v|ve|x|shaded x|d|b|c)\b", k): return "zone"
    if " county " in f" {k} " or " parish " in f" {k} " or " borough " in f" {k} ": return "county"
    tail = re.sub(r"^(flood insurance cost|flood insurance|flood zone map) ", "", k)
    if tail != k and tail in STATES: return "state"
    if k.startswith("flood insurance ") and tail in TOWNS: return "town"
    return "generic"

by = collections.defaultdict(list)
for r in rows:
    by[kind(r["Keyword"])].append((low(r["Avg. monthly searches"]), r["Avg. monthly searches"], r["Keyword"]))
for k, v in sorted(by.items(), key=lambda kv: -sum(x[0] for x in kv[1])):
    v.sort(reverse=True)
    with_vol = sum(1 for x in v if x[0] >= 10)
    print(f"\n== {k}: {len(v)} keywords, {with_vol} with 10+/mo, floor total {sum(x[0] for x in v):,}/mo")
    for x in v[:12]: print(f"  {x[1]:>12}  {x[2]}")
