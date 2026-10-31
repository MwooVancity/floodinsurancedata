"""Build + gate every state hub page whose data is complete, with the SAME template (build_page.py, FF_LEVEL=state)
and the SAME gate as the county pages. A state is built only when agg_raw.py, extras_raw.py and
collect_state_small.py have all produced its files. Writes dist/flood-insurance/<state-slug>/ and
data/states/built.json (the list build_site and the county pages use, so nothing links to a page that isn't there).
Usage: python -I tools/build_states.py"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES, slug, assemble
from collect_state_small import FIPS
import fingerprint as FP   # build only what changed (PLAN scale guard)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
SD = os.path.join(ROOT, "data", "states")
DIST = os.path.join(ROOT, "dist", "flood-insurance")
PLACES = os.path.join(ROOT, "places.json")
BASE = os.environ.get("FF_BASEURL", "https://floodinsurancedata.com")

built, blocked = [], []
for st, name in sorted(NAMES.items(), key=lambda kv: kv[1]):
    d = os.path.join(SD, slug(st))
    need = [os.path.join(d, f) for f in ("agg.json", "data.json", "extras.json")]
    if not all(os.path.exists(p) for p in need):
        continue
    assemble(d)   # the template reads the county schema (agg.state_risk for the tile map, data.claims_extra for payouts)
    agg = json.load(open(need[0]))
    out = os.path.join(DIST, slug(st), "index.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
    label = "the District of Columbia" if st == "DC" else name    # reads right in "in ...", "...'s"
    env = dict(os.environ, FF_LEVEL="state", FF_DIR=d, OUT_HTML=out, FF_COUNTYLABEL=label, FF_COUNTYSHORT=label,
               FF_SLUG=slug(st), FF_GEOID=FIPS[st], FF_OFFICIAL="0", FF_BASEURL=BASE, FF_PLACES=PLACES)
    fp = FP.page_fp(need, {"st": st, "label": label, "base": BASE,
                            "places": sorted((p["slug"], p["units"], p["median"]) for p in (json.load(open(PLACES)) if os.path.exists(PLACES) else []) if p.get("state") == st)})
    if not FP.unchanged(out, fp):
        r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "build_page.py")], env=env, cwd=TOOLS, capture_output=True, text=True)
    else: r = None
    if r is not None and r.returncode:
        blocked.append(f"{st} (build): {r.stderr.strip().splitlines()[-1][:160] if r.stderr.strip() else '?'}"); continue
    g = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "gate.py"), need[0], out, "0"], capture_output=True, text=True) if r is not None else None
    if g is not None and g.returncode:
        os.remove(out)   # a failing page is never left where deploy would ship it
        blocked.append(f"{st} (gate): " + " | ".join(l.strip() for l in g.stdout.splitlines() if "[" in l)[:300]); continue
    if r is not None: FP.stamp(out, fp)
    built.append({"abbr": st, "slug": slug(st), "name": name, "units": agg["policies"]["units"], "median": agg["policies"]["p50"],
                  "share_below": agg["policies"].get("share_below"), "claims": agg["claims"]["rows"], "paid": agg["claims"]["total_paid"]})
    print(f"STATE PASS {st} {name}: units {agg['policies']['units']}, median ${agg['policies']['p50']}")
json.dump(built, open(os.path.join(SD, "built.json"), "w"), indent=1)
for b in blocked: print("STATE BLOCKED", b)
print(f"states built: {len(built)}, blocked: {len(blocked)}")
sys.exit(1 if blocked else 0)
