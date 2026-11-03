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

def fema_updated(tries=3):   # FEMA 503s are common (2026-11-03); still down = fail, tomorrow's run retries (no email before the 10th)
    url = "https://www.fema.gov/api/open/v1/DataSets?$select=name,lastDataSetRefresh&$filter=name%20eq%20%27NfipPolicies%27"
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "floodinsurancedata-pull"}), timeout=60) as r:
                return datetime.date.fromisoformat(json.load(r)["DataSets"][0]["lastDataSetRefresh"][:10])
        except Exception:
            if i == tries - 1: raise
            time.sleep(60 * (i + 1))

if "--test" in sys.argv:
    d = datetime.date
    assert target_asof(d(2026, 11, 3)) == d(2026, 8, 31) and target_asof(d(2027, 1, 6)) == d(2026, 10, 31)
    assert target_asof(d(2026, 3, 3)) == d(2025, 12, 31)
    assert decide(d(2026, 8, 31), d(2026, 7, 31), d(2026, 9, 9))[0]          # normal month
    assert not decide(d(2026, 8, 31), d(2026, 8, 31), d(2026, 9, 9))[0]      # rerun / backup cron: nothing new
    assert not decide(d(2026, 9, 30), d(2026, 8, 31), d(2026, 9, 9))[0]      # FEMA has not updated: never pull past its file
    assert decide(d(2026, 8, 31), None, d(2026, 9, 9))[0]                    # first run, no data yet
    assert not stale(d(2026, 9, 9), d(2026, 11, 3)) and stale(d(2026, 9, 9), d(2026, 12, 9))
    print("refresh_plan tests pass"); sys.exit(0)

p = os.path.join(ROOT, "data", "us", "asof.json")
have = datetime.date.fromisoformat(json.load(open(p))["asof"]) if os.path.exists(p) else None
fema, today = fema_updated(), datetime.date.today()
pull, why = decide(target_asof(today), have, fema)
print(("PULL: " if pull else "SKIP download: ") + why)
if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"pull={str(pull).lower()}\n")
if not pull and stale(fema, today):   # pages keep printing their as-of date, but someone must look (renamed dataset? stopped?)
    print(f"FEMA's policy file has not been updated since {fema} ({(today - fema).days} days)"); sys.exit(1)
