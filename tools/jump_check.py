"""Monthly refresh guard (PLAN.md calendar): a typical cost that moves more than 25% in one refresh is held for a look.
Compares each state and county agg.json in the working tree with the last committed copy (git HEAD). Exit 1 stops the
refresh job before it commits, so the site keeps last month's data. Usage: python -I tools/jump_check.py [--limit 0.25]"""
import glob, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = float(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0.25
MIN_N = 100   # small samples swing; only medians from 100+ priced policies are judged
held = []
for f in sorted(glob.glob(os.path.join(ROOT, "data", "states", "*", "agg.json")) + glob.glob(os.path.join(ROOT, "data", "c", "*", "agg.json"))):
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    old = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    if not old: continue   # a new page has nothing to compare with
    a, b = json.loads(old).get("policies") or {}, json.load(open(f, encoding="utf-8")).get("policies") or {}
    if not (a.get("p50") and b.get("p50")) or min(a.get("cost_n") or 0, b.get("cost_n") or 0) < MIN_N: continue
    ch = b["p50"] / a["p50"] - 1
    if abs(ch) > LIMIT: held.append(f"{rel}: median ${a['p50']:,} -> ${b['p50']:,} ({ch:+.0%})")
print("\n".join(held) or f"JUMP CHECK PASS: no median moved more than {LIMIT:.0%}")
sys.exit(1 if held else 0)
