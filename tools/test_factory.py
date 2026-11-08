"""Factory stress test (owner 11-08: "stress test the factory now with the edge cases of all possibilities").
Takes one real county's data, bends it into every edge case a future county could bring (no claims, one zone, a
decade-only history, New Year as-of dates, a billion-dollar flood, zero units...), builds each with the shipping
build_page.py and runs the shipping gate. A page may pass or be held; what fails here is a CRASH (builder or gate),
because a crash at 2,000 counties stops the daily run for everyone. Prints which gate ids each case fired, so a
case that ships with a wrong label shows up as PASS beside its expected id. Run: python -I tools/test_factory.py"""
import copy, json, os, re, shutil, subprocess, sys, tempfile
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
# owner 11-08 "don't miss a type": every page type built from per-place data runs every case (counties and states share
# build_page.py; site-wide pages have their own recompute + mutation checks in release.py)
TARGETS = [  # (slug, data dir, label, geoid, level)
    ("brevard-county-fl", os.path.join(ROOT, "data", "c", "brevard-county-fl"), "Brevard County, Florida", "12009", "county"),
    ("delaware", os.path.join(ROOT, "data", "states", "delaware"), "Delaware", "10", "state"),          # small state
    ("louisiana", os.path.join(ROOT, "data", "states", "louisiana"), "Louisiana", "22", "state")]       # big claims state
TARGETS = [t for t in TARGETS if os.path.exists(os.path.join(t[1], "agg.json"))]
if not TARGETS: print("test_factory: skipped (no data)"); sys.exit(0)

def case(fn, base):
    b = copy.deepcopy(base); fn(b["agg"], b["data"], b["extras"]); return b

def no_claims(a, d, x):
    a["claims"].update(rows=0, total_paid=0, by_year={}, year_min=None, year_max=None)
    d["claims_extra"] = None; x["claims"] = {}
def one_claim(a, d, x):
    y = a["claims"]["year_max"]; a["claims"].update(rows=1, total_paid=5000, by_year={str(y): [1, 5000]}, year_min=y)
    d["claims_extra"] = dict(d["claims_extra"], claims=1, paid_n=1, cwop_share=0.0, avg_paid=5000)
    x["claims"].update(events=[], by_decade={f"{str(y)[:3]}0s": {"n": 1, "paid_pct": 100.0}}, unpaid_n=0, unpaid_reasons=[], paid_n=1)
def one_zone(a, d, x):
    u = a["policies"]["units"]; a["policies"]["zone_units"] = {"X": u}; a["policies"]["sfha_units"] = 0; a["policies"]["sfha_share_units"] = 0.0
    a["policies"]["cost_by_zone"] = {"X": {"median": a["policies"]["p50"], "n": a["policies"]["cost_n"]}}
def big_unpriced_zone(a, d, x):   # the r103 Levy shape: a zone with 40% of units and no median
    P = a["policies"]; cz = dict(list(P["cost_by_zone"].items())[:1]); P["cost_by_zone"] = cz
def no_priced_zone(a, d, x): a["policies"]["cost_by_zone"] = {}
def under_floor(a, d, x): a["policies"].update(cost_n=29, cohort_n=29, spread_ok=False)
def all_decades_small(a, d, x):
    x["claims"]["by_decade"] = {k: {"n": 5, "paid_pct": 60.0} for k in x["claims"].get("by_decade") or {"2020s": 0}}
def only_catch_all(a, d, x):
    x["claims"]["events"] = [{"name": "Flooding", "years": ["1979", "2024"], "claims": 400, "paid": 9e7, "avg": 225000}]
def billion_flood(a, d, x):
    ev = x["claims"]["events"]; ev[0] = dict(ev[0], paid=1.2e9, avg=1.2e9 / max(1, ev[0]["claims"]))
def asof_jan1(a, d, x): a["policies"]["asof"] = "2027-01-01"
def asof_dec31(a, d, x): a["policies"]["asof"] = "2026-12-31"
def claims_old(a, d, x):   # history ends years before the as-of (r103 Dixie)
    by = {k: v for k, v in a["claims"]["by_year"].items() if int(k) <= 2019}; a["claims"].update(by_year=by, year_max=max(map(int, by)))
def no_nri(a, d, x): a["nri"] = None
def no_disasters(a, d, x): d["declarations"] = []; d["housing"] = []; d["housing_unplaced"] = {}
def no_crs(a, d, x): d["crs"] = []
def no_multiloss(a, d, x): d["multiloss"] = {}
def shuffled_order(a, d, x):   # a source changing its row order must not change which row is called largest/costliest
    P = a["policies"]
    for k in ("zone_units", "cost_by_zone"): P[k] = dict(reversed(list((P.get(k) or {}).items())))
    x["claims"]["events"] = list(reversed(x["claims"].get("events") or []))
    a["claims"]["by_year"] = dict(reversed(list(a["claims"]["by_year"].items())))
def zero_units(a, d, x): a["policies"].update(units=0, rows=0, zone_units={}, sfha_units=0, sfha_share_units=None, cost_by_zone={}, cost_n=0)

CASES = [no_claims, one_claim, one_zone, big_unpriced_zone, no_priced_zone, under_floor, all_decades_small, only_catch_all,
         billion_flood, asof_jan1, asof_dec31, claims_old, no_nri, no_disasters, no_crs, no_multiloss, shuffled_order, zero_units]

tmp = tempfile.mkdtemp(); rows, crashed = [], []
for SLUG, SRC, LABEL, GEOID, LEVEL in TARGETS:
  BASE = {f: json.load(open(os.path.join(SRC, f + ".json"))) for f in ("agg", "data", "extras")}
  for fn in CASES:
    name = f"{SLUG}:{fn.__name__}"
    d = os.path.join(tmp, SLUG, fn.__name__, SLUG); shutil.copytree(SRC, d)   # side files too (state county_detail.json)
    try: b = case(fn, BASE)
    except Exception as e: rows.append((name, "CASE-ERR", repr(e)[:60])); crashed.append(name); continue
    for k, v in b.items(): json.dump(v, open(os.path.join(d, k + ".json"), "w"))
    out = os.path.join(tmp, SLUG, fn.__name__, "site", "flood-insurance", SLUG, "index.html"); os.makedirs(os.path.dirname(out))
    env = dict(os.environ, FF_DIR=d, OUT_HTML=out, FF_COUNTYLABEL=LABEL, FF_COUNTYSHORT=LABEL if LEVEL == "state" else LABEL.split(",")[0],
               FF_OFFICIAL="0", FF_SLUG=SLUG, FF_GEOID=GEOID, FF_BASEURL="https://floodinsurancedata.com",
               FF_PLACES=os.path.join(ROOT, "places.json") if LEVEL == "state" else os.path.join(tmp, "places.json"),
               **({"FF_LEVEL": "state"} if LEVEL == "state" else {}))
    r = subprocess.run([sys.executable, "-I", os.path.join(T, "build_page.py")], env=env, cwd=T, capture_output=True, text=True)
    if r.returncode != 0:
        msg = (r.stderr.strip().splitlines() or ["?"])[-1]
        held = "Traceback" not in r.stderr   # a deliberate refusal (sys.exit with a reason) is a hold, not a crash
        rows.append((name, "HELD" if held else "BUILD-CRASH", msg[:90]))
        if not held: crashed.append(name)
        continue
    g = subprocess.run([sys.executable, "-I", os.path.join(T, "gate.py"), os.path.join(d, "agg.json"), out, "0"], capture_output=True, text=True)
    if "Traceback" in g.stderr:
        rows.append((name, "GATE-CRASH", g.stderr.strip().splitlines()[-1][:90])); crashed.append(name); continue
    ids = sorted(set(re.findall(r"\[(\w+)\]", g.stdout)))
    rows.append((name, "BLOCKED" if g.returncode else "PASS", ",".join(ids) or "-"))
shutil.rmtree(tmp, ignore_errors=True)
w = max(len(r[0]) for r in rows)
for n, res, info in rows: print(f"{n:<{w}} {res:<11} {info}")
assert not crashed, f"factory crashed on: {crashed}"
print("test_factory: no crash on", len(CASES), "edge cases x", len(TARGETS), "page types/sizes")
