"""Run gate 2 against the LIVE html of every published page (all states + all counties), not the local build.
Proves what readers get is what passed. Usage: python -I tools/gate_live.py"""
import json, os, subprocess, sys, tempfile, urllib.request
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
BASE = "https://floodinsurancedata.com"
pages = [(s["slug"], os.path.join(ROOT, "data", "states", s["slug"], "agg.json"))
         for s in json.load(open(os.path.join(ROOT, "data", "states", "built.json")))]
pages += [(p["slug"], os.path.join(ROOT, "data", "c", p["slug"], "agg.json")) for p in json.load(open(os.path.join(ROOT, "places.json")))]
bad, tmp = [], tempfile.mkdtemp()
for slug, agg in pages:
    body = urllib.request.urlopen(urllib.request.Request(f"{BASE}/flood-insurance/{slug}/", headers={"User-Agent": "Mozilla/5.0 (gate-live)"}),
                                  timeout=60).read().decode()
    f = os.path.join(tmp, slug + ".html"); open(f, "w", encoding="utf-8").write(body)
    r = subprocess.run([sys.executable, "-I", os.path.join(T, "gate.py"), agg, f, "0"], capture_output=True, text=True)
    if r.returncode: bad.append(slug + ": " + " | ".join(l.strip() for l in r.stdout.splitlines() if l.strip().startswith("- "))[:300])
print(f"live pages gated: {len(pages)}, failing: {len(bad)}")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
