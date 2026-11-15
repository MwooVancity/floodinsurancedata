"""Rank the Keyword Planner export by kind (generic, zone, state, county, town). Input: newest data/kwp/*.csv (UTF-16, tab).
Run: python -I tools/kwp_rank.py. Volumes are Google's ranges; 'low' is the range floor, so totals are floors, not estimates."""
import collections, csv, glob, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sorted(glob.glob(os.path.join(ROOT, "data", "kwp", "us-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv")))[-1]   # 11-15: the Planner export only, never the hand-made -topics/-grow lists (UTF-8, other columns)
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

def owner(k, kd):   # owner 11-15 "all the keywords": the built page that answers each keyword, or why none ("" = none)
    D = os.path.join(ROOT, "dist")
    ok = lambda u: u if os.path.exists(os.path.join(D, u.strip("/"), "index.html")) else ""
    if kd == "zone":
        z = re.search(r"\bzone (shaded x|ae|ah|ao|ve|a|v|x|d|b|c)\b", k)[1]
        return ok("/flood-zones/" + {"shaded x": "x", "v": "ve", "b": "x", "c": "x"}.get(z, z) + "/")
    if kd == "state":
        return ok("/flood-insurance/" + re.sub(r"^(flood insurance cost|flood insurance|flood zone map) ", "", k).replace(" ", "-") + "/")
    if kd == "county":
        m = re.match(r"(.+? (?:county|parish|borough))\b", k)
        hits = [p["slug"] for p in PLACES if m and p["slug"].rsplit("-", 1)[0].replace("-", " ") == m[1].replace(".", "").replace("'", "")]
        return ok(f"/flood-insurance/{hits[0]}/") if hits else ok("/flood-insurance/miami-dade-county-fl/") if m and m[1] == "dade county" else ""   # a shared name: the built page answers it
    if kd == "town": return ""   # city pages: PLAN growth move 6
    for pat, u in ((r"map|by address|what flood zone|my flood zone", "/flood-zone-map/"), (r"renter", "/flood-insurance/renters/"),
                   (r"\bnfip\b|national flood|fema flood insurance", "/nfip/"), (r"required|mandatory|need flood insurance", "/"), (r"claim", "/flood-insurance/claims/"),
                   (r"private", "/guides/private-flood-insurance/"), (r"condo", "/guides/condo-flood-insurance/"),
                   (r"risk rating", "/guides/risk-rating-2/"), (r"homeowners", "/guides/homeowners-insurance-flooding/"),
                   (r"loma|lomr|letter of map", "/guides/loma-lomr/"), (r"deductible", "/guides/flood-insurance-deductible/"),
                   (r"contents", "/guides/flood-insurance-contents-coverage/"), (r"buying|buy a house", "/guides/buying-a-house-in-a-flood-zone/"),
                   (r"zip", "/flood-insurance/zip/"), (r"cost|how much|price|average|flood insurance$", "/")):
        if re.search(pat, k): return ok(u)
    return ""

if "--map" in sys.argv:   # state/keyword-map.csv: every keyword, its floor, kind and owning page; the unowned volume is the build queue
    PLACES = json.load(open(os.path.join(ROOT, "places.json"), encoding="utf-8"))
    out = sorted(((low(r["Avg. monthly searches"]), r["Keyword"], kind(r["Keyword"])) for r in rows), reverse=True)
    out = [(v, k, kd, owner(k, kd)) for v, k, kd in out]
    with open(os.path.join(ROOT, "state", "keyword-map.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["floor_per_month", "keyword", "kind", "page"]); w.writerows(out)
    tot = collections.defaultdict(lambda: [0, 0, 0, 0])
    for v, k, kd, u in out: t = tot[kd]; t[0 if u else 2] += v; t[1 if u else 3] += 1
    for kd, (vo, no, vn, nn) in sorted(tot.items(), key=lambda x: -(x[1][0] + x[1][2])):
        print(f"{kd:8} owned {vo:>7,}/mo ({no:,} kw) | no page {vn:>7,}/mo ({nn:,} kw)")
    print("top unowned:", [(v, k) for v, k, kd, u in out if not u][:15]); sys.exit()

by = collections.defaultdict(list)
for r in rows:
    by[kind(r["Keyword"])].append((low(r["Avg. monthly searches"]), r["Avg. monthly searches"], r["Keyword"]))
for k, v in sorted(by.items(), key=lambda kv: -sum(x[0] for x in kv[1])):
    v.sort(reverse=True)
    with_vol = sum(1 for x in v if x[0] >= 10)
    print(f"\n== {k}: {len(v)} keywords, {with_vol} with 10+/mo, floor total {sum(x[0] for x in v):,}/mo")
    for x in v[:12]: print(f"  {x[1]:>12}  {x[2]}")
