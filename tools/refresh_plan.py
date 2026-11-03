"""Does this month's refresh need the big FEMA download (owner 2026-11-03: "downloading over and over seems wasteful")?
Pull only when the new as-of date is (a) newer than the one in data/ and (b) before FEMA's last policy-file update, so a
rerun, the backup cron or a month FEMA did not update re-downloads nothing, and the as-of never runs past FEMA's data
(policies renewing in a month the file does not cover would vanish: about 1/12 of all homes per month, under the jump check).
Writes pull=true|false to $GITHUB_OUTPUT. FEMA unreachable = exit 1 (the job fails and alerts; a silent skip would never alert).
Usage: python -I tools/refresh_plan.py [--test]"""
import datetime, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def target_asof(today):   # end of the month 3 months back (FEMA updates monthly, with a lag); pull_raw uses the same rule
    t = today.replace(day=1)
    for _ in range(2): t = (t - datetime.timedelta(days=1)).replace(day=1)
    return t - datetime.timedelta(days=1)

def decide(target, have, fema):
    if have and target <= have: return False, f"data already as of {have}"
    if target >= fema: return False, f"FEMA's policy file (updated {fema}) does not cover {target} yet; last month's figures stay"
    return True, f"new as-of {target} (data {have}, FEMA file {fema})"

def fema_updated():
    url = "https://www.fema.gov/api/open/v1/DataSets?$select=name,lastDataSetRefresh&$filter=name%20eq%20%27NfipPolicies%27"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "floodinsurancedata-pull"}), timeout=60) as r:
        return datetime.date.fromisoformat(json.load(r)["DataSets"][0]["lastDataSetRefresh"][:10])

if "--test" in sys.argv:
    d = datetime.date
    assert target_asof(d(2026, 11, 3)) == d(2026, 8, 31) and target_asof(d(2027, 1, 6)) == d(2026, 10, 31)
    assert target_asof(d(2026, 3, 3)) == d(2025, 12, 31)
    assert decide(d(2026, 8, 31), d(2026, 7, 31), d(2026, 9, 9))[0]          # normal month
    assert not decide(d(2026, 8, 31), d(2026, 8, 31), d(2026, 9, 9))[0]      # rerun / backup cron: nothing new
    assert not decide(d(2026, 9, 30), d(2026, 8, 31), d(2026, 9, 9))[0]      # FEMA has not updated: never pull past its file
    assert decide(d(2026, 8, 31), None, d(2026, 9, 9))[0]                    # first run, no data yet
    print("refresh_plan tests pass"); sys.exit(0)

p = os.path.join(ROOT, "data", "us", "asof.json")
have = datetime.date.fromisoformat(json.load(open(p))["asof"]) if os.path.exists(p) else None
pull, why = decide(target_asof(datetime.date.today()), have, fema_updated())
print(("PULL: " if pull else "SKIP download: ") + why)
if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"pull={str(pull).lower()}\n")
