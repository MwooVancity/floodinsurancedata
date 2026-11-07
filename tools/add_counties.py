"""Publish the next N counties in queue order (largest by policy units; 11-03: 30 counties Search Console already shows us
for, town named with its state, moved to the front by hand) that passed the review build and are not yet in counties.json.
Usage: python -I tools/add_counties.py [N]   (default 10). Reads state/county-queue.json (committed, so the daily GitHub job
can use it); `--refresh` rewrites that queue from review/places.json after a local `build_counties.py --all`.
Owner 2026-11-01: 20 a day; google_gate S7 caps a release at 25 new indexable pages."""
import re, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "state", "county-queue.json")
if "--refresh" in sys.argv:   # only counties whose review page passed the gate, largest first
    q = [{k: p[k] for k in ("slug", "state", "geoid", "label", "short", "units")} for p in json.load(open(os.path.join(ROOT, "review", "places.json")))]
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), indent=0, ensure_ascii=False); print(f"queue: {len(q)} counties")
    import subprocess   # review 11-07: a rewritten queue has no "kw"; re-rank at once or every county reads as unsearched
    sys.exit(subprocess.run([sys.executable, "-I", os.path.join(ROOT, "tools", "kwp_rank.py"), "--queue"]).returncode)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
if N == 0: print("added 0: county publishing frozen (owner 11-06)"); sys.exit()   # freeze, not a stall: no alert
path = os.path.join(ROOT, "tools", "counties.json")
cur = json.load(open(path, encoding="utf-8"))
have = {c["geoid"] for c in cur}
passed = json.load(open(QUEUE, encoding="utf-8"))
sys.path.insert(0, os.path.join(ROOT, "tools")); import review as RV
new = [p for p in passed if p["geoid"] not in have and RV.ok(p["slug"]) and p.get("kw", 0) > 0 and not p.get("blocked")][:N]   # owner 11-06: only counties people search for (kwp_rank --queue)   # only pages a hater review passed
if not new and any(p["geoid"] not in have and not RV.flags(p["slug"]) and p.get("kw", 0) > 0 and not p.get("blocked") for p in passed):
    sys.exit("STALLED: unflagged counties remain but none has a current review (stale stamps?)")   # else the job logs "queue empty"
for p in new:
    t = p["short"].rsplit(" ", 1)[0] if p["short"].split(" ")[-1] in ("County", "Parish", "Borough") else p["short"]
    cur.append({"slug": p["slug"], "state": p["state"], "geoid": p["geoid"], "county": t.upper(), "countytitle": t,
                "label": p["label"], "short": p["short"], "official": 0})   # 0 = FEMA's official count not on file
json.dump(cur, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
if new:   # audit 11-07: a new county that fails a gate must not stop the whole day; set it aside, publish the rest
    import subprocess
    r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "tools", "build_counties.py"), "--only", ",".join(p["slug"] for p in new)],
                       capture_output=True, text=True)
    blocked = dict(re.findall(r"COUNTY BLOCKED (\S+) (.*)", r.stdout))
    if r.returncode and not blocked:   # a STOP (missing extras, unmatched rows) names no county: set the whole batch aside (review 11-07)
        blocked = {p["slug"]: "build stopped: " + (r.stderr or r.stdout).strip()[-150:] for p in new}
    env = [v for v in blocked.values() if "ModuleNotFoundError" in v or "ImportError" in v]
    if env: sys.exit("STOP: the build machine is missing a library, not a county fault; nothing set aside: " + env[0][:150])   # 11-07
    if blocked:
        cur = [c for c in cur if c["slug"] not in blocked]; json.dump(cur, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        for p in passed:
            if p["slug"] in blocked: p["blocked"] = blocked[p["slug"]][:200]
        json.dump(passed, open(QUEUE, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
        new = [p for p in new if p["slug"] not in blocked]
        print("set aside (gate):", "; ".join(f"{k}: {v[:80]}" for k, v in blocked.items()))
print(f"added {len(new)}: " + ", ".join(p["slug"] for p in new))
