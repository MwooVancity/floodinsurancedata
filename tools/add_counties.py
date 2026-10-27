"""Publish the next N counties: the largest (by policy units) that passed the review build and are not yet in counties.json.
Usage: python -I tools/add_counties.py [N]   (default 10). Reads state/county-queue.json (committed, so the daily GitHub job
can use it); `--refresh` rewrites that queue from review/places.json after a local `build_counties.py --all`.
Owner 2026-10-26: a few at a time, never hundreds at once; google_gate S7 caps a release at 25 new indexable pages."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "state", "county-queue.json")
if "--refresh" in sys.argv:   # only counties whose review page passed the gate, largest first
    q = [{k: p[k] for k in ("slug", "state", "geoid", "label", "short", "units")} for p in json.load(open(os.path.join(ROOT, "review", "places.json")))]
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), indent=0, ensure_ascii=False); print(f"queue: {len(q)} counties"); sys.exit()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
path = os.path.join(ROOT, "tools", "counties.json")
cur = json.load(open(path, encoding="utf-8"))
have = {c["geoid"] for c in cur}
passed = json.load(open(QUEUE, encoding="utf-8"))
sys.path.insert(0, os.path.join(ROOT, "tools")); import review as RV
new = [p for p in passed if p["geoid"] not in have and RV.ok(p["slug"])][:N]   # only pages a hater review passed
for p in new:
    t = p["short"].rsplit(" ", 1)[0] if p["short"].split(" ")[-1] in ("County", "Parish", "Borough") else p["short"]
    cur.append({"slug": p["slug"], "state": p["state"], "geoid": p["geoid"], "county": t.upper(), "countytitle": t,
                "label": p["label"], "short": p["short"], "official": 0})   # 0 = FEMA's official count not on file
json.dump(cur, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"added {len(new)}: " + ", ".join(p["slug"] for p in new))
