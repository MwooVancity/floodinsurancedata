"""Site-wide factory stress test (owner 11-08 "don't miss a type"): the home, /nfip/, claims, renters, ZIP, zone pages,
/flood-zone-map/ and methodology are built by build_site.py from national files, so test_factory.py (per-place pages)
never bends their data. Each case copies data/ to a temp folder, bends one national input (a state missing, a zone
gone, empty renters, a refund or a $1 billion cost bucket, New Year as-of dates, no ZIP places...), runs the shipping
build_site.py into a temp dist, then scans every site-level page it wrote. FAIL = a crash, garbage a reader would see
(None, nan, Infinity, undefined, "$-"), or an internal link to a page the build did not write. A page the build
deliberately skips (national totals need all 51 states) is a hold, not a failure. Run: python -I tools/test_site_factory.py"""
import json, os, re, shutil, subprocess, sys, tempfile, html as H
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
if not os.path.exists(os.path.join(ROOT, "data", "us", "cost_hist.json")): print("test_site_factory: skipped (no data)"); sys.exit(0)
tmp = tempfile.mkdtemp()
DATA = os.path.join(tmp, "data"); shutil.copytree(os.path.join(ROOT, "data"), DATA)
SITE_DIRS = {"claims", "renters", "zip"}   # site-level pages under /flood-insurance/; the rest there are states/counties
def jl(*p): return json.load(open(os.path.join(DATA, *p), encoding="utf-8"))
def jd(v, *p): json.dump(v, open(os.path.join(DATA, *p), "w", encoding="utf-8"))

def bend(path, fn):   # returns (apply, restore) for one file
    full = os.path.join(DATA, *path); bak = full + ".bak"
    def apply():
        shutil.copy(full, bak); v = json.load(open(full, encoding="utf-8")); v = fn(v)
        if v is None: os.remove(full)
        else: json.dump(v, open(full, "w", encoding="utf-8"))
    def restore(): shutil.move(bak, full)
    return apply, restore

def multi(*bs): return (lambda: [a() for a, _ in bs], lambda: [r() for _, r in bs])
def story(cause, moved):   # 11-10 claims-page story fields on one county file (cloud refresh writes them)
    def f(v):
        c = v.setdefault("extras", {}).setdefault("claims", {})
        c["cause10"] = dict({"from": "2016", "to": "2025", "paid_n": cause[0]}, with_cause=cause[0], by_code=cause[1])
        c["moved"] = dict({"from": "2016", "to": "2025"}, rated_out_known=moved[0], now_av=moved[1], current_blank=moved[2]); return v
    return f
def each_state(f): return lambda d: {s: f(v) for s, v in d.items()}
def add_bucket(st, k, n): return lambda d: dict(d, **{st: dict(d[st], **{k: n})})
CASES = {
    "missing_state": bend(("states", "wyoming", "agg.json"), lambda v: None),
    "state_not_built": bend(("states", "built.json"), lambda v: [x for x in v if x.get("slug") != "wyoming"]),
    "no_exact_zone_file": bend(("us", "cost_hist_zone_exact.json"), lambda v: None),
    "zone_ao_vanishes": bend(("us", "cost_hist_zone_exact.json"), each_state(lambda h: {z: x for z, x in h.items() if z != "AO"})),
    "renters_empty": bend(("us", "renter_hist.json"), each_state(lambda h: {})),
    "claims_by_zone_empty": bend(("us", "claims_zone.json"), each_state(lambda c: dict(c, by_zone={}))),
    "asof_jan1": bend(("us", "asof.json"), lambda v: {"asof": "2027-01-01"}),
    "asof_dec31": bend(("us", "asof.json"), lambda v: {"asof": "2026-12-31"}),
    "zip_places_empty": bend(("us", "zip_places.json"), lambda v: {}),
    "map_status_empty": bend(("us", "map_status.json"), lambda v: {}),
    "refund_bucket": bend(("us", "cost_hist.json"), add_bucket("TX", "-250", 40)),
    "billion_bucket": bend(("us", "cost_hist.json"), add_bucket("CA", "1000000000", 1)),
    "one_policy_state": bend(("us", "cost_hist.json"), lambda d: dict(d, WY={"500": 1})),
    # 11-10 story tables: exactly the 500 floor with no cause codes (0%), every claim two causes (rows over 100%), 499 left out,
    # all now in A/V, none known (blank only); one county alone prints no card
    "story_edges": multi(bend(("all-counties", "48061.json"), story((500, {}), (500, 0, 0))),
                         bend(("all-counties", "48071.json"), story((600, {"4": 600, "2": 600, "1": 1}), (900, 900, 0))),
                         bend(("all-counties", "06037.json"), story((499, {"4": 499}), (0, 0, 40)))),
    "story_one_county": bend(("all-counties", "48061.json"), story((800, {"4": 8}), (800, 8, 0))),
    "sealevel_empty":bend(("us", "sealevel.json"), lambda v: {} if isinstance(v, dict) else []),
}
GARBAGE = re.compile(r"\bNone\b|\bnan\b|\bNaN\b|Infinity|undefined|\$-\d|\$—\d|\{[a-z_]+\}")

def llms_problems(path):   # 11-08: AI assistants quote llms.txt; a figure without its base or a county without its state misleads
    if not os.path.exists(path): return ["llms.txt missing"]
    t = open(path, encoding="utf-8").read(); out = []
    if "single-family primary homes" not in t or "premium plus fees" not in t: out.append("llms.txt: medians lack their base")
    for l in t.splitlines():
        if "median $" in l and not l.rstrip().endswith("a year"): out.append(f"llms.txt: figure without 'a year': {l[:80]}")
        if "/flood-insurance/" in l and re.search(r"-(county|parish|borough|city|census-area|municipality)-[a-z]{2}/\)", l) and not re.search(r", [A-Z]{2}\]", l):
            out.append(f"llms.txt: county without its state: {l[:80]}")
        if "/flood-zones/d/" in l and "costs" in l: out.append("llms.txt: zone D has no cost figure")
    if GARBAGE.search(t): out.append("llms.txt: garbage text")
    return out
# the llms check must be able to fail: a bare county line and a bare figure are caught, a good line is not
_lt = os.path.join(tmp, "llms_selftest.txt")
open(_lt, "w", encoding="utf-8").write("single-family primary homes, premium plus fees\n- [Jefferson County](https://x/flood-insurance/jefferson-county-tx/): median $1,147\n")
assert len(llms_problems(_lt)) == 2, llms_problems(_lt)
open(_lt, "w", encoding="utf-8").write("single-family primary homes, premium plus fees\n- [Jefferson County, TX](https://x/flood-insurance/jefferson-county-tx/): median $1,147 a year\n")
assert not llms_problems(_lt), llms_problems(_lt)
def visible(page):
    page = re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.S)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", page)))

def run(name):
    dist = os.path.join(tmp, "dist_" + name)
    try: return _run(name, dist)
    finally: shutil.rmtree(dist, ignore_errors=True)   # one 52 MB copy at a time, never 15 (nothing piles up)

def _run(name, dist):
    # start from the last release, as the real pipeline does: a page this build holds keeps its previous version live
    shutil.copytree(os.path.join(ROOT, "dist"), dist)
    r = subprocess.run([sys.executable, "-I", os.path.join(T, "build_site.py")], cwd=ROOT, capture_output=True, text=True,
                       env=dict(os.environ, FF_DIST=dist, FF_DATADIR=DATA))
    if r.returncode != 0:
        return ("CRASH" if "Traceback" in r.stderr else "HELD"), (r.stderr.strip().splitlines() or ["?"])[-1][:100]
    bad, pages = [], []
    for dp, _, fs in os.walk(dist):
        rel = os.path.relpath(dp, dist).replace("\\", "/")
        top = rel.split("/")
        if top[0] == "flood-insurance" and (len(top) == 1 or top[1] not in SITE_DIRS): continue   # not built here
        for f in fs:
            if not f.endswith(".html"): continue
            pg = open(os.path.join(dp, f), encoding="utf-8").read(); pages.append(rel)
            g = GARBAGE.search(visible(pg))
            if g: bad.append(f"{rel}: '{visible(pg)[max(0, g.start() - 50):g.end() + 30]}'")
            for href in set(re.findall(r'href="(/[^"#?]*)"', pg)):   # (llms.txt is checked once per case below)
                tgt = os.path.join(dist, href.lstrip("/"))
                if not (os.path.exists(tgt) or os.path.exists(os.path.join(tgt, "index.html"))):
                    bad.append(f"{rel}: link to {href} that this build did not write")
    bad += llms_problems(os.path.join(dist, "llms.txt"))
    return ("FAIL" if bad else "PASS"), (bad[0][:160] + (f" (+{len(bad) - 1} more)" if len(bad) > 1 else "")) if bad else f"{len(pages)} pages"

# the scan must be able to fail: each of these reader-visible slips is caught, and a normal sentence is not
for _bad in ("<p>Median None a year</p>", "<p>$-250 a year</p>", "<p>nan%</p>", "<p>Infinity</p>", "<p>{median} a year</p>"):
    assert GARBAGE.search(visible(_bad)), _bad
assert not GARBAGE.search(visible("<p>Zone X $928 a year; Monday — 1,018,718 policies.</p><script>var x=undefined</script>"))
rows, failed = [], []
res = run("baseline"); rows.append(("baseline", *res))
if res[0] != "PASS": failed.append("baseline")
for name, (apply, restore) in CASES.items():
    try:
        apply(); res = run(name)
    except Exception as e: res = ("CASE-ERR", repr(e)[:100])
    finally:
        try: restore()
        except FileNotFoundError: pass
    rows.append((name, *res))
    if res[0] in ("CRASH", "FAIL", "CASE-ERR"): failed.append(name)
shutil.rmtree(tmp, ignore_errors=True)
w = max(len(r[0]) for r in rows)
for n, s, i in rows: print(f"{n:<{w}} {s:<9} {i}")
assert not failed, f"site factory failed on: {failed}"
print("test_site_factory: no crash, garbage or dead link on", len(CASES), "national edge cases")
