"""The only way to start a cloud job (owner 11-15 "don't let this happen again": forced reruns used up the month's Actions
minutes). Prints the workflow's median minutes from its own run history and the month's used/remaining minutes
(actions_check.py), then refuses when used + that median would pass 50% of the free minutes before the 15th, or 90% from
the 15th; a second forced refresh-data run in a month is refused too (refresh_plan.forced_runs, the one copy of that rule).
Usage: python -I tools/cloud_run.py <workflow.yml> [-f key=value ...] | --test
Edge cases:
- First run of a workflow, no history: median unknown, decided on used minutes alone, printed "no history". Test: no_hist.
- Billing-blocked runs (0 steps, ~0 min) drag the median down: only successful runs count. Test: median_success.
- gh not logged in or offline: nothing measured = nothing started (exit 1).
- Month and day are UTC (GitHub bills by UTC month): the 14th 23:00 in New York is already the 15th. Test: day15.
- A name without .yml: added. A job that only takes 30 s still counts as 1 minute (rounded up per run, actions_check)."""
import datetime, json, statistics, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import actions_check as AC

def median_minutes(runs):   # None when the workflow never succeeded
    ok = [r for r in runs if r.get("conclusion") == "success"]
    return statistics.median(AC.minutes([r]) for r in ok) if ok else None

def refuse(used, med, day, free=AC.FREE):   # '' to go, else why
    cap = 0.5 if day < 15 else 0.9
    proj = used + (med or 0)
    if proj > cap * free:
        return f"would reach ~{proj:.0f} of {free} minutes (cap {cap:.0%} {'before' if day < 15 else 'from'} the 15th)"
    return ""

def test():
    r = lambda m, c="success": {"conclusion": c, "createdAt": "2026-11-14T00:00:00Z", "updatedAt": f"2026-11-14T00:{m:02d}:00Z"}
    assert median_minutes([r(10), r(20), r(30)]) == 20
    assert median_minutes([r(10), r(0, "failure"), r(0, "failure")]) == 10, "median_success: blocked runs left out"
    assert median_minutes([]) is None
    assert refuse(900, 90, 14) == "" and refuse(950, 90, 14), "50% before the 15th"
    assert refuse(950, 90, 15) == "" and refuse(1750, 90, 15), "day15: 90% from the 15th"
    assert refuse(1001, None, 3), "no_hist: decided on used alone"
    assert refuse(999, None, 3) == ""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import refresh_plan as RP
    runs = [{"displayTitle": "refresh-data (forced)", "databaseId": 1}, {"displayTitle": "refresh-data", "databaseId": 2}]
    assert RP.forced_runs(runs) == [1] and RP.forced_runs(runs, own=1) == [] and RP.forced_runs(runs[1:]) == []
    print("cloud_run --test: 10 cases PASS")

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]: test(); sys.exit()
    if len(sys.argv) < 2: sys.exit(__doc__)
    wf = sys.argv[1] if sys.argv[1].endswith((".yml", ".yaml")) else sys.argv[1] + ".yml"
    inputs = sys.argv[2:]
    now = datetime.datetime.now(datetime.timezone.utc); first = now.date().replace(day=1)
    try:
        hist = AC.gh("run", "list", "--workflow", wf, "--limit", "20", "--json", "conclusion,createdAt,updatedAt")
        month = AC.gh("run", "list", "--limit", "500", "--created", f">={first}", "--json", "conclusion,createdAt,updatedAt")
    except (subprocess.CalledProcessError, OSError, ValueError) as e:
        sys.exit(f"CLOUD RUN REFUSED: could not read GitHub run history ({e}); nothing started")
    med, used = median_minutes(hist), AC.minutes(month)
    print(f"{wf}: median {'~%.0f min' % med if med is not None else 'unknown (no history)'} per run; "
          f"{now:%Y-%m}: ~{used} of {AC.FREE} minutes used, ~{AC.FREE - used} left")
    why = refuse(used, med, now.day)
    if wf == "refresh-data.yml" and "force=true" in inputs:
        import refresh_plan as RP
        done = RP.forced_runs(AC.gh("run", "list", "--workflow", wf, "--created", f">={first}", "--json", "displayTitle,databaseId"))
        if done: why = why or f"a forced refresh already ran this month (run {done[0]}); new fields wait for the next monthly refresh"
    if why: sys.exit(f"CLOUD RUN REFUSED: {why}")
    cmd = ["gh", "workflow", "run", wf] + [x for kv in inputs if kv != "-f" for x in ("-f", kv)]
    subprocess.run(cmd, check=True)
    print("started:", " ".join(cmd))
