"""Does this month's refresh need the big FEMA download (owner 2026-11-03: "downloading over and over seems wasteful")?
Pull only when the new as-of date is (a) newer than the one in data/ and (b) before FEMA's last policy-file update, so a
rerun, the daily 3rd-10th cron after a good run or a month FEMA did not update re-downloads nothing, and the as-of never runs past FEMA's data
(policies renewing in a month the file does not cover would vanish: about 1/12 of all homes per month, under the jump check).
Writes pull=true|false to $GITHUB_OUTPUT. FEMA unreachable = exit 1 (the job fails and alerts; a silent skip would never alert).
Usage: python -I tools/refresh_plan.py [--test]"""
import datetime, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def target_asof(today):   # end of the month 3 months back (FEMA updates monthly, with a lag); pull_raw uses the same rule
    t = today.replace(day=1)
    for _ in range(2): t = (t - datetime.timedelta(days=1)).replace(day=1)
    return t - datetime.timedelta(days=1)

def decide(target, have, fema):
    if have and target <= have: return False, f"data already as of {have}"
    if target >= fema: return False, f"FEMA's policy file (updated {fema}) does not cover {target} yet; last month's figures stay"
    return True, f"new as-of {target} (data {have}, FEMA file {fema})"

def stale(fema, today): return (today - fema).days > 90   # FEMA updates about monthly; 3 months without one needs a person
def old(have, today): return bool(have) and (today - have).days > 150   # as-of is ~95 days old by design; 150 = a missed month or two

def fema_updated(tries=3):   # FEMA 503s are common (2026-11-03); still down = fail, tomorrow's run retries (no email before the 10th)
    url = "https://www.fema.gov/api/open/v1/DataSets?$select=name,lastDataSetRefresh&$filter=name%20eq%20%27NfipPolicies%27"
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "floodinsurancedata-pull"}), timeout=60) as r:
                return datetime.date.fromisoformat(json.load(r)["DataSets"][0]["lastDataSetRefresh"][:10])
        except Exception:
            if i == tries - 1: raise
            time.sleep(60 * (i + 1))

def forced_runs(runs, own=None):   # ids of this month's forced runs (refresh-data.yml run-name says "(forced)"), not this one
    # owner 11-15: one forced refresh a month at most; a forced run that failed still spent its minutes, so it counts
    return [r["databaseId"] for r in runs if "(forced)" in (r.get("displayTitle") or "") and str(r["databaseId"]) != str(own)]

def force_allowed(today):   # '' when a forced pull may run now, else why not (no reading = refused: costs nothing)
    import subprocess
    try:
        runs = json.loads(subprocess.run(["gh", "run", "list", "--workflow", "refresh-data.yml", "--created", f">={today.replace(day=1)}",
                                          "--json", "displayTitle,databaseId"], capture_output=True, text=True, check=True).stdout or "[]")
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        return f"could not read this month's runs ({e})"
    done = forced_runs(runs, os.environ.get("GITHUB_RUN_ID"))
    return f"forced run {done[0]} already ran this month" if done else ""

if __name__ == "__main__" and "--test" in sys.argv:   # imported by cloud_run.py: only forced_runs is used there
    assert forced_runs([{"displayTitle": "refresh-data (forced)", "databaseId": 7}], own="7") == []   # this run itself
    assert forced_runs([{"displayTitle": "refresh-data (forced)", "databaseId": 6}], own="7") == [6]
    assert forced_runs([{"displayTitle": "refresh-data", "databaseId": 6}, {"databaseId": 5}]) == []
    d = datetime.date
    assert target_asof(d(2026, 11, 3)) == d(2026, 8, 31) and target_asof(d(2027, 1, 6)) == d(2026, 10, 31)
    assert target_asof(d(2026, 3, 3)) == d(2025, 12, 31)
    assert decide(d(2026, 8, 31), d(2026, 7, 31), d(2026, 9, 9))[0]          # normal month
    assert not decide(d(2026, 8, 31), d(2026, 8, 31), d(2026, 9, 9))[0]      # rerun / backup cron: nothing new
    assert not decide(d(2026, 9, 30), d(2026, 8, 31), d(2026, 9, 9))[0]      # FEMA has not updated: never pull past its file
    assert decide(d(2026, 8, 31), None, d(2026, 9, 9))[0]                    # first run, no data yet
    assert not stale(d(2026, 9, 9), d(2026, 11, 3)) and stale(d(2026, 9, 9), d(2026, 12, 9))
    assert not old(d(2026, 8, 31), d(2026, 12, 10)) and old(d(2026, 7, 31), d(2027, 1, 3)) and not old(None, d(2027, 1, 3))
    print("refresh_plan tests pass"); sys.exit(0)

if __name__ == "__main__":
    p = os.path.join(ROOT, "data", "us", "asof.json")
    have = datetime.date.fromisoformat(json.load(open(p))["asof"]) if os.path.exists(p) else None
    fema, today = fema_updated(), datetime.date.today()
    pull, why = decide(target_asof(today), have, fema)
    if os.environ.get("FORCE") == "true" and target_asof(today) < fema and not pull:   # hand run after a method fix (never past FEMA's file)
        no = force_allowed(today)
        if no: print(f"FORCE refused (one forced refresh a month, owner 11-15): {no}")
        else: pull, why = True, f"forced by hand: {why}"
    print(("PULL: " if pull else "SKIP download: ") + why)
    # side sources (community discounts, disasters, aid, repeat floods; ~73 min, 2026-10-31 log): with a new download, or once on the 3rd
    side = pull or today.day == 3
    if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"pull={str(pull).lower()}\nside={str(side).lower()}\n")
    if not pull and stale(fema, today):   # pages keep printing their as-of date, but someone must look (renamed dataset? stopped?)
        print(f"FEMA's policy file has not been updated since {fema} ({(today - fema).days} days)"); sys.exit(1)
    if not pull and old(have, today):   # skipped runs count as success, so the 34-day job check cannot see stale data
        print(f"site data is as of {have}, {(today - have).days} days old"); sys.exit(1)
