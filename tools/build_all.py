"""Build the whole site from the downloaded data, offline: every county (build_counties.py, one pipeline from the
raw pull), every state (build_states.py), then home, hub, sitemap and CSV (build_site.py). Every page is gated as
it is built; a failing page is removed. Stale page folders are pruned, so nothing unverified is ever served.
Usage: python -I tools/build_all.py"""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS, DATA, DIST = os.path.join(ROOT, "tools"), os.path.join(ROOT, "data"), os.path.join(ROOT, "dist")
BASE = os.environ.get("FF_BASEURL", "https://floodinsurancedata.com")

def run(script):
    env = dict(os.environ, FF_BASEURL=BASE, FF_PLACES=os.path.join(ROOT, "places.json"), FF_DIST=DIST, FF_DATADIR=DATA)
    r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, script)], env=env,
                       cwd=TOOLS, capture_output=True, text=True)
    print(r.stdout.rstrip())
    if r.returncode: print(f"[{script}] FAILED", r.stderr[-600:])
    return r.returncode

codes = [run("build_counties.py")]
places = {p["slug"] for p in json.load(open(os.path.join(ROOT, "places.json")))}
fdir = os.path.join(DIST, "flood-insurance")
sys.path.insert(0, TOOLS); from agg_raw import NAMES, slug as _sslug
_states = {_sslug(st) for st in NAMES}   # state folders stay: build_states rebuilds only the ones whose inputs changed
from papers import SPECS as _PS; _papers = {s["key"] for s in _PS}   # every paper, ready or not: switching one off must not delete its dated versions (bug review 11-14)   # paper folders hold dated versions (PAPER-GATE M2.5): never pruned
for name in os.listdir(fdir):   # prune any page folder that is neither a county that passed this run nor a state
    if os.path.isdir(os.path.join(fdir, name)) and name not in places and name not in _states and name not in _papers:
        shutil.rmtree(os.path.join(fdir, name), ignore_errors=True)
_bj = os.path.join(ROOT, "data", "states", "built.json"); _rd = lambda: open(_bj, "rb").read() if os.path.exists(_bj) else b""
_before = _rd()
codes += [run("build_states.py")]
# 11-14: county pages link only the states in built.json, which build_states writes AFTER them; when that list changed this run
# (a state blocked last run, passing now), the county pages were built from the old list and lost their state link (312 shipped
# that way). Rebuild them from the new list; the fingerprint skips every county whose inputs did not change.
if _rd() != _before: codes += [run("build_counties.py")]
codes += [run("build_site.py")]
sys.exit(1 if any(codes) else 0)   # a blocked page fails the build, so nothing downstream can ship around it
