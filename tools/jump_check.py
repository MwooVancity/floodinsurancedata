"""Monthly refresh guard (PLAN.md calendar): a typical cost that moves more than 25% in one refresh is held for a look.
Compares each state and county agg.json in the working tree with the last committed copy (git HEAD). Exit 1 stops the
refresh job before it commits, so the site keeps last month's data. Usage: python -I tools/jump_check.py [--limit 0.25] [--test]
2026-11-03 review: a median that vanished passed (skipped as "too small"), and a month of missing renewals (~8% of policies)
passed under 25%; now a vanished figure is held, and a state's policy units may move at most 5% (FEMA files vary ~1-2%)."""
import glob, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = float(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0.25
STATE_UNITS = max(0.05, LIMIT) if LIMIT > 0.25 else 0.05   # a person who raised the limit after a look raises this too
MIN_N = 100   # small samples swing; only medians from 100+ priced policies are judged

def judge(rel, a, b, state):   # a = last month's policies block, b = this month's; returns the reasons to hold
    out = []
    if a.get("p50") and (a.get("cost_n") or 0) >= MIN_N:
        if not b.get("p50") or (b.get("cost_n") or 0) < MIN_N:
            out.append(f"{rel}: median ${a['p50']:,} from {a['cost_n']:,} policies is gone or under {MIN_N} (now {b.get('cost_n')})")
        elif abs(b["p50"] / a["p50"] - 1) > LIMIT:
            out.append(f"{rel}: median ${a['p50']:,} -> ${b['p50']:,} ({b['p50'] / a['p50'] - 1:+.0%})")
    lim = STATE_UNITS if state else LIMIT
    if a.get("units") and (not b.get("units") or abs(b["units"] / a["units"] - 1) > lim):
        out.append(f"{rel}: policy units {a['units']:,} -> {b.get('units') or 0:,} (limit {lim:.0%})")
    return out

if "--test" in sys.argv:
    assert judge("x", {"p50": 1000, "cost_n": 500}, {"p50": None, "cost_n": 0}, False)            # vanished median is held
    assert judge("x", {"p50": 1000, "cost_n": 500}, {"p50": 1300, "cost_n": 500}, False)          # +30% held
    assert not judge("x", {"p50": 1000, "cost_n": 500}, {"p50": 1100, "cost_n": 500}, False)      # +10% passes
    assert not judge("x", {"p50": 1000, "cost_n": 50}, {"p50": None, "cost_n": 0}, False)         # too small to judge last month
    assert judge("x", {"units": 100000}, {"units": 93000}, True)                                   # a state losing 7% (a missing month) is held
    assert not judge("x", {"units": 100000}, {"units": 98500}, True)                              # normal monthly drift passes
    assert not judge("x", {"units": 1000}, {"units": 930}, False)                                 # counties keep the 25% limit
    assert judge("x", {"units": 1000}, {}, False)                                                  # vanished units held
    print("jump_check tests pass"); sys.exit(0)

held = []
PUB = {c["geoid"] for c in json.load(open(os.path.join(ROOT, "tools", "counties.json")))}   # only published pages can stop a refresh
for g in sorted(PUB):
    if not os.path.exists(os.path.join(ROOT, "data", "all-counties", g + ".json")): held.append(f"data/all-counties/{g}.json: published county gone from the download")
for f in sorted(glob.glob(os.path.join(ROOT, "data", "states", "*", "agg.json")) + glob.glob(os.path.join(ROOT, "data", "all-counties", "*.json"))):   # the refresh writes all-counties, never data/c
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    if "all-counties" in rel and os.path.basename(f)[:5] not in PUB: continue
    old = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    if not old: continue   # a new page has nothing to compare with
    held += judge(rel, json.loads(old).get("policies") or {}, json.load(open(f, encoding="utf-8")).get("policies") or {}, "/states/" in rel)
print("\n".join(held) or f"JUMP CHECK PASS: no median moved more than {LIMIT:.0%}, no state's policies more than {STATE_UNITS:.0%}")
sys.exit(1 if held else 0)
