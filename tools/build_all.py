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
for name in os.listdir(fdir):   # prune any page folder that is not a county that passed this run (states are rebuilt next)
    if os.path.isdir(os.path.join(fdir, name)) and name not in places:
        shutil.rmtree(os.path.join(fdir, name), ignore_errors=True)
codes += [run("build_states.py"), run("build_site.py")]
sys.exit(1 if any(codes) else 0)   # a blocked page fails the build, so nothing downstream can ship around it
