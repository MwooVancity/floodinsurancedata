"""ONE county pipeline: every county with 100+ priced single-family policies, built from the full raw pull
(data/all-counties) plus per-state files already on disk. Replaces the per-county API collectors.
For each county: write data/c/<slug>/{agg,data}.json, build with build_page.py, gate with gate.py; a failing
page is removed, never shipped. Counties already indexed (tools/counties.json) stay indexable; every new page
carries noindex; only counties in counties.json are published (see the rollout rule in __main__).
Writes places.json (what home, hub, sitemap and sibling links read). Usage: python -I tools/build_counties.py [--only slug,...]"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES, slug as state_slug, FIPS

T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
REVIEW = "--all" in sys.argv   # every eligible county, built into review/ (git-ignored, never deployed) to prove the gate at scale
DATA = os.path.join(ROOT, "data")
DIST = os.path.join(ROOT, "review" if REVIEW else "dist", "flood-insurance")
PLACES = os.path.join(ROOT, "review", "places.json") if REVIEW else os.path.join(ROOT, "places.json")
CDATA = os.path.join(ROOT, "review", "c") if REVIEW else os.path.join(DATA, "c")   # unpublished county data never enters git
BASE = os.environ.get("FF_BASEURL", "https://floodinsurancedata.com")
MIN_PRICED = 30   # a median from 30+ priced policies, with its small-sample caveat (no spread chart under 100); fewer = no honest median
ST_OF = {v: k for k, v in FIPS.items()}
INDEXED = {c["geoid"]: c for c in json.load(open(os.path.join(T, "counties.json")))}   # live and indexed before 2026-10-26
NAMES_CEN = json.load(open(os.path.join(DATA, "us", "county_names.json")))
STORM = json.load(open(os.path.join(DATA, "us", "storm_events.json")))

def page_slug(name, st): return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + "-" + st.lower()
def key(name):   # "Miami-Dade County" / "MIAMI-DADE COUNTY" / "Miami-Dade (County)" -> "miami-dade|county"
    n = name.lower().replace("(", "").replace(")", "").strip()
    m = re.match(r"(.*?)\s+(county|parish|borough|city and borough|census area|municipality|city)$", n)
    return (m.group(1).strip() + "|" + m.group(2)) if m else n

_states = {}
def state_files(st):
    if st not in _states:
        d = os.path.join(DATA, "states", state_slug(st))
        _states[st] = tuple(json.load(open(os.path.join(d, f))) for f in ("agg.json", "data.json", "county_detail.json"))
    return _states[st]

def assemble(g, raw):
    st = ST_OF[g[:2]]; name = NAMES_CEN[g]; sagg, sdata, sdet = state_files(st)
    det, k = sdet.get(g, {}), key(name)
    sm = sagg["manifest"]
    def man(ds, rows): return {"reported_total": rows, "unique_fetched": rows, "missing": 0, "complete": bool(sm[ds]["complete"]),
                               "provisional": False, "pulled": sm[ds]["pulled"], "scope": "state",
                               "state_total": sm[ds]["unique_fetched"]}   # every record of the state was downloaded and matched
    agg = {"level": "county", "geoid": g, "state": st, "complete": True,
           "policies": dict(raw["policies"], asof=sagg["policies"]["asof"], retrieved=sagg["policies"]["retrieved"]),
           "claims": dict(raw["claims"], retrieved=sagg["claims"]["retrieved"]),
           "nri": det.get("nri"), "state_risk": [{"fips": c["fips"], "county": c["county"], "rating": c["rating"]} for c in sdata.get("nri_counties", [])],
           "manifest": {"policies": man("policies", raw["policies"]["rows"]), "claims": man("claims", raw["claims"]["rows"])}}
    ml = (sdata.get("multiloss") or {}).get("by_county", {}).get(g)
    se = STORM["by_county"].get(g)
    data = {"claims_extra": dict(raw.get("claims_extra") or {}, retrieved=sm["claims"]["pulled"]),
            "crs": [c for c in sdata.get("crs", []) if key(c.get("county") or "") == k],
            "declarations": [d for d in sdata.get("declarations", []) if (d.get("fipsCountyCode") or "") == g[2:]],
            "housing": [h for h in sdata.get("housing", []) if key(h.get("county") or "") == k],
            "multiloss": {"total": ml["total"], "srl": ml["srl"], "retrieved": sdata["multiloss"]["retrieved"]} if ml else {"total": 0, "srl": 0, "retrieved": sdata["multiloss"]["retrieved"]},
            "penetration": det.get("penetration") or {},
            "storm_events": dict(se, period=STORM["period"], retrieved=STORM["retrieved"], source=STORM["source"]) if se else {}}
    return st, name, agg, data

import fingerprint as FP   # build only what changed (PLAN scale guard)
_ADJ = json.load(open(os.path.join(DATA, "us", "county_adjacency.json"))) if os.path.exists(os.path.join(DATA, "us", "county_adjacency.json")) else {}
def build_one(item):
    g, st, name, sl = item
    d = os.path.join(CDATA, sl); out = os.path.join(DIST, sl, "index.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
    off = str(INDEXED.get(g, {}).get("official", 0))
    sd = os.path.join(DATA, "states", state_slug(st))
    near = sorted((p["slug"], p["units"], p["median"]) for p in json.load(open(PLACES)) if p["state"] == st or p["geoid"] in _ADJ.get(g, []))
    fp = FP.page_fp([os.path.join(d, f) for f in ("agg.json", "data.json", "extras.json")] + [os.path.join(sd, f) for f in ("agg.json", "data.json", "extras.json")],
                    {"off": off, "idx": g in INDEXED, "label": f"{name}, {NAMES[st]}", "base": BASE, "near": near, "review": REVIEW})
    if FP.unchanged(out, fp): return sl, None   # same inputs, same page: it passed the gate when it was built
    env = dict(os.environ, FF_DIR=d, OUT_HTML=out, FF_GEOID=g, FF_SLUG=sl, FF_COUNTYLABEL=f"{name}, {NAMES[st]}", FF_COUNTYSHORT=name,
               FF_OFFICIAL=off, FF_BASEURL=BASE, FF_PLACES=PLACES, FF_PLACES_RO="1", FF_NOINDEX="0" if g in INDEXED else "1")
    r = subprocess.run([sys.executable, "-I", os.path.join(T, "build_page.py")], env=env, cwd=T, capture_output=True, text=True)
    if r.returncode: return sl, "build: " + (r.stderr.strip().splitlines() or ["?"])[-1][:200]
    r = subprocess.run([sys.executable, "-I", os.path.join(T, "gate.py"), os.path.join(d, "agg.json"), out, off], capture_output=True, text=True)
    if r.returncode:
        os.remove(out)   # a failing page never stays where deploy would ship it
        return sl, "gate: " + " | ".join(l.strip() for l in r.stdout.splitlines() if l.strip().startswith("- "))[:300]
    FP.stamp(out, fp)
    return sl, None

if __name__ == "__main__":
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    items, places = [], []
    for f in sorted(os.listdir(os.path.join(DATA, "all-counties"))):
        g = f[:5]; raw = json.load(open(os.path.join(DATA, "all-counties", f)))
        if g[:2] not in ST_OF or g not in NAMES_CEN or (raw["policies"].get("cost_n") or 0) < MIN_PRICED: continue
        if not raw.get("claims", {}).get("rows"): continue   # no NFIP claim ever filed: the claim-history half of the page would be empty
        if not raw.get("extras"):   # extras_raw.py not run since the last agg_raw: cards would vanish silently (2026-10-27)
            sys.exit(f"STOP: data/all-counties/{f} has no extras; run python -I tools/extras_raw.py first")
        if ST_OF[g[:2]] == "DC": continue   # one county = the state page; a second copy would be a duplicate
        # publish only the counties listed in counties.json (live and indexed). New counties are added there a few at a
        # time, each read as a reader first; publishing ~1,000 at once on a new domain risks a scaled-content verdict
        # (owner, 2026-10-26). --all builds every qualifying county locally for review; release never passes it.
        if g not in INDEXED and "--all" not in sys.argv: continue
        st, name, agg, data = assemble(g, raw)
        sl = page_slug(name, st)
        if only and sl not in only: continue
        d = os.path.join(CDATA, sl); os.makedirs(d, exist_ok=True)
        json.dump(agg, open(os.path.join(d, "agg.json"), "w")); json.dump(data, open(os.path.join(d, "data.json"), "w"))
        json.dump(raw.get("extras") or {}, open(os.path.join(d, "extras.json"), "w"))   # read by build_page and the gate from the page folder
        items.append((g, st, name, sl))
        places.append({"slug": sl, "label": f"{name}, {NAMES[st]}", "short": name, "geoid": g, "state": st,
                       "units": agg["policies"]["units"], "median": agg["policies"]["p50"], "indexable": g in INDEXED})
    places.sort(key=lambda p: -p["units"])
    if only and os.path.exists(PLACES):   # a partial build keeps every other published county in the list
        places = [p for p in json.load(open(PLACES)) if p["slug"] not in {q["slug"] for q in places}] + places
        places.sort(key=lambda p: -p["units"])
    json.dump(places, open(PLACES, "w"), indent=0)   # before the builds: sibling links and the gate read it
    with ThreadPoolExecutor(6) as ex: res = list(ex.map(build_one, items))
    bad = [(s, e) for s, e in res if e]
    built = {s for s, e in res if not e} | ({p["slug"] for p in places} - {it[3] for it in items} if only else set())
    json.dump([p for p in places if p["slug"] in built], open(PLACES, "w"), indent=0)   # only what passed
    for s in sorted(built): print("GATE PASS", s)
    for s, e in bad: print("COUNTY BLOCKED", s, e)
    print(f"counties built: {len(built)} ({sum(1 for p in places if p['slug'] in built and p['indexable'])} indexable), blocked: {len(bad)}")
    sys.exit(1 if bad else 0)
