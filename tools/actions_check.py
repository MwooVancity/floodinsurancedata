"""Session-start check that does not run on GitHub Actions (11-14 audit: a billing/minutes block runs zero steps, so no
job's own alert fires and watch.yml is blocked too). Prints this month's Actions minutes (private repo: 2,000 free) and
any recent run GitHub refused to start. Exit 1 when blocked or above WARN minutes.
Usage: python -I tools/actions_check.py [--test]"""
import datetime, json, subprocess, sys

FREE, WARN = 2000, 1500

def minutes(runs):   # wall-clock minutes per run, rounded up per run (GitHub bills per job-minute, rounded up)
    f = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return sum(-(-int((f(r["updatedAt"]) - f(r["createdAt"])).total_seconds()) // 60) for r in runs)

def refused(run):   # failed with every job at zero steps = GitHub never started it
    jobs = run.get("jobs") or []
    return run.get("conclusion") == "failure" and bool(jobs) and not any(j.get("steps") for j in jobs)

def gh(*a): return json.loads(subprocess.run(["gh", *a], capture_output=True, text=True, check=True).stdout or "[]")

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        assert minutes([{"createdAt": "2026-11-14T00:00:00Z", "updatedAt": "2026-11-14T00:00:01Z"}]) == 1
        assert minutes([{"createdAt": "2026-11-14T00:00:00Z", "updatedAt": "2026-11-14T01:00:00Z"}]) == 60
        assert refused({"conclusion": "failure", "jobs": [{"steps": []}]})
        assert not refused({"conclusion": "failure", "jobs": [{"steps": [{"n": 1}]}]})   # a real failure is not a block
        assert not refused({"conclusion": "success", "jobs": [{"steps": []}]})
        sys.exit(print("actions_check --test ok"))
    today = datetime.date.today()
    runs = gh("run", "list", "--limit", "500", "--created", f">={today.replace(day=1)}", "--json", "databaseId,workflowName,conclusion,createdAt,updatedAt")
    used = minutes(runs)
    bad = [r for r in runs[:10] if r.get("conclusion") == "failure"
           and refused(gh("run", "view", str(r["databaseId"]), "--json", "conclusion,jobs"))]
    print(f"Actions minutes {today:%Y-%m}: ~{used} of {FREE} free ({len(runs)} runs)")
    for r in bad: print(f"BLOCKED: GitHub refused to start {r['workflowName']} run {r['databaseId']} ({r['createdAt'][:10]}); cloud jobs are off, release.py deploys locally")
    if used > WARN: print(f"WARN: over {WARN} minutes; no forced refresh until the 1st")
    sys.exit(1 if bad or used > WARN else 0)
