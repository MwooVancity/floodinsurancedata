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

WATCH, WFILES = "MwooVancity/flood-lookup-watch", ("tools/live_zonemap.py", "tools/test_zonemap.py")
def watch_problems(last, today, local, remote):
    """11-15 public watch repo edge cases: W1 no run or not success (a run in progress counts as not passed);
    W2 last run older than 2 days (GitHub pauses schedules after 60 quiet days, silently); W3 a test file differs
    between this repo and the public copy (CRLF ignored), so the public run checks old answers; W4 repo unreachable."""
    if last is None: return ["W4 public watch repo unreachable (renamed, deleted or gh offline)"]
    out = []
    if not last or last[0].get("conclusion") != "success":
        out.append("W1 last live lookup run " + (f"{last[0].get('conclusion') or 'still running'} {last[0]['createdAt'][:10]}" if last else "missing"))
    if last and (today - datetime.date.fromisoformat(last[0]["createdAt"][:10])).days > 2:
        out.append(f"W2 last live lookup run is from {last[0]['createdAt'][:10]}: the nightly schedule may be paused")
    out += [f"W3 {f} differs from the public copy: push it to {WATCH}" for f in WFILES
            if (local.get(f) or "").replace("\r\n", "\n") != (remote.get(f) or "").replace("\r\n", "\n")]
    return out

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        assert minutes([{"createdAt": "2026-11-14T00:00:00Z", "updatedAt": "2026-11-14T00:00:01Z"}]) == 1
        assert minutes([{"createdAt": "2026-11-14T00:00:00Z", "updatedAt": "2026-11-14T01:00:00Z"}]) == 60
        assert refused({"conclusion": "failure", "jobs": [{"steps": []}]})
        assert not refused({"conclusion": "failure", "jobs": [{"steps": [{"n": 1}]}]})   # a real failure is not a block
        assert not refused({"conclusion": "success", "jobs": [{"steps": []}]})
        d, ok, fs = datetime.date(2026, 11, 15), [{"conclusion": "success", "createdAt": "2026-11-15T03:41:00Z"}], {f: "a\nb" for f in WFILES}
        assert watch_problems(ok, d, fs, fs) == [], "green, fresh, same files"
        assert watch_problems(ok, d, fs, {f: "a\r\nb" for f in WFILES}) == [], "CRLF only is not drift"
        assert watch_problems(None, d, fs, fs)[0].startswith("W4"), "unreachable"
        assert watch_problems([], d, fs, fs)[0].startswith("W1"), "no runs"
        assert watch_problems([{"conclusion": "", "createdAt": "2026-11-15T03:41:00Z"}], d, fs, fs)[0].startswith("W1"), "in progress"
        assert watch_problems([{"conclusion": "failure", "createdAt": "2026-11-15T03:41:00Z"}], d, fs, fs)[0].startswith("W1"), "red"
        assert any(p.startswith("W2") for p in watch_problems([{"conclusion": "success", "createdAt": "2026-11-11T03:41:00Z"}], d, fs, fs)), "stale"
        assert any(p.startswith("W3") for p in watch_problems(ok, d, fs, dict(fs, **{WFILES[1]: "a\nc"}))), "drift"
        sys.exit(print("actions_check --test ok (13 cases)"))
    today = datetime.date.today()
    runs = gh("run", "list", "--limit", "500", "--created", f">={today.replace(day=1)}", "--json", "databaseId,workflowName,conclusion,createdAt,updatedAt")
    used = minutes(runs)
    bad = [r for r in runs[:10] if r.get("conclusion") == "failure"
           and refused(gh("run", "view", str(r["databaseId"]), "--json", "conclusion,jobs"))]
    print(f"Actions minutes {today:%Y-%m}: ~{used} of {FREE} free ({len(runs)} runs)")
    for r in bad: print(f"BLOCKED: GitHub refused to start {r['workflowName']} run {r['databaseId']} ({r['createdAt'][:10]}); cloud jobs are off, release.py deploys locally")
    if used > WARN: print(f"WARN: over {WARN} minutes; no forced refresh until the 1st")
    # 11-15: the nightly live test of the address lookup runs in a public repo (free minutes); its last run is read here
    import base64, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        lw = gh("run", "list", "-R", WATCH, "--limit", "1", "--json", "conclusion,createdAt")
        remote = {f: base64.b64decode(gh("api", f"repos/{WATCH}/contents/{f}")["content"]).decode("utf-8") for f in WFILES}
    except (subprocess.CalledProcessError, KeyError, ValueError):
        lw, remote = None, {}
    local = {f: open(os.path.join(root, f), encoding="utf-8").read() for f in WFILES}
    wp = watch_problems(lw, today, local, remote)
    print(f"live lookup test ({WATCH}): " + ("; ".join(wp) if wp else f"success {lw[0]['createdAt'][:10]}, files in step"))
    sys.exit(1 if bad or used > WARN or wp else 0)
