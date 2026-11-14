"""One command for a release, in order; stops at the first failure.
  python -I tools/release.py          build all pages + gate 2 on each, unit tests, mutation suite, phone check (dist)
  python -I tools/release.py --live   after deploy: phone check + every live page byte-equal to the built page
recheck.py (network, minutes) runs separately as its own background job before a release is called verified."""
import json, os, re, subprocess, sys

T = os.path.dirname(os.path.abspath(__file__))

def started_jobs(run):   # 11-14 audit: a billing-blocked run lists its job with 0 steps (run 43561612814), so count jobs that ran a step
    return sum(1 for j in run.get("jobs") or [] if j.get("steps"))

def wait_deploy(poll, now, sleep, stuck=900, limit=1800, every=15):
    """'' when the deploy run succeeds, else why it stopped. 11-11: run 43097109682 sat queued with no job for 4 h and the
    release waited on it; a run queued with no job for 15 min (GitHub stuck, or Actions minutes used up) stops the release."""
    t0 = now()
    while True:
        status, concl, jobs = poll()
        if status == "completed" and concl != "success" and not jobs: return "not started (GitHub refused the job: Actions minutes or billing)"
        if status == "completed": return "" if concl == "success" else f"finished {concl}"
        if status == "queued" and not jobs and now() - t0 > stuck: return "not started: queued with no job for 15 min (GitHub stuck or Actions minutes used up)"
        if now() - t0 > limit: return f"still {status} after 30 min"
        sleep(every)

if "--test-deploy-wait" in sys.argv:   # fake GitHub and clock: every path of wait_deploy
    def run(states):
        t = [0]; it = iter(states)
        def poll(): return next(it, states[-1])
        return wait_deploy(poll, lambda: t[0], lambda s: t.__setitem__(0, t[0] + s))
    assert run([("queued", None, 0), ("in_progress", None, 1), ("completed", "success", 1)]) == ""
    assert "queued with no job" in run([("queued", None, 0)])
    assert "finished failure" in run([("in_progress", None, 1), ("completed", "failure", 1)])
    assert run([("completed", "failure", 0)]).startswith("not started")   # 11-14: billing block, the job never ran
    blocked = {"status": "completed", "conclusion": "failure", "jobs": [{"name": "deploy", "conclusion": "failure", "steps": []}]}   # real shape, run 43561612814
    assert run([("completed", "failure", started_jobs(blocked))]).startswith("not started")
    assert started_jobs({"jobs": [{"steps": [{"name": "x"}]}]}) == 1
    assert "after 30 min" in run([("in_progress", None, 1)])
    print("deploy wait: 7 cases PASS"); sys.exit()
def step(name, *cmd):   # every step is timed (PLAN: measure every recurring job; what grows with pages gets fingerprinted)
    print(f"== {name}", flush=True); t0 = __import__("time").time()
    r = subprocess.run([sys.executable, "-I", *cmd], cwd=os.path.dirname(T))
    print(f"   [{__import__('time').time() - t0:.0f} s] {name}", flush=True)
    if r.returncode: sys.exit(f"RELEASE STOPPED at: {name}")

if "--live" in sys.argv:
    base = "https://floodinsurancedata.com"
    step("phone check (live)", os.path.join(T, "phone_check.py"), "--base", base)
    step("every live page = the built page that passed (as Googlebot)", os.path.join(T, "gate_live.py"))
    print("LIVE OK")
else:
    out = subprocess.run([sys.executable, "-I", os.path.join(T, "build_all.py")], cwd=os.path.dirname(T),
                         capture_output=True, text=True).stdout
    n_pass, bad = len(re.findall(r"GATE PASS", out)), re.findall(r".*(?:GATE FAIL|FAILED|\[\w+\]).*", out)
    print(f"== build + gate: {n_pass} pages pass"); [print("  ", b) for b in bad[:30]]
    if bad or not n_pass: sys.exit("RELEASE STOPPED at: build + gate")
    step("truth proof: every fixed defect is fixed on the built pages", os.path.join(T, "test_truth.py"))
    step("reader tools: oracle, edge cases, fuzz, JS off (CLAUDE.md ship standard)", os.path.join(T, "test_tools.py"))
    step("rule sources: every rule's quoted wording is still on its official page", os.path.join(T, "recheck.py"), "--rules-only")
    step("address tool: oracle, fuzz, click path with FEMA fixtures, JS off", os.path.join(T, "test_zonemap.py"))
    step("ZIP tool: oracle on every ZIP, form edges, JS off", os.path.join(T, "test_ziptool.py"))
    step("nfip page: figures recomputed", os.path.join(T, "claims_check.py"), "--nfip")
    step("nfip check mutations", os.path.join(T, "claims_check.py"), "--nfip", "--test")
    step("guides: figures recomputed, zone pages agree (owner 11-12)", os.path.join(T, "claims_check.py"), "--guides")
    step("guides check mutations", os.path.join(T, "claims_check.py"), "--guides", "--test")
    step("renters page: figures recomputed", os.path.join(T, "claims_check.py"), "--renters")
    step("renters check mutations", os.path.join(T, "claims_check.py"), "--renters", "--test")
    step("claims page: every figure recomputed", os.path.join(T, "claims_check.py"))
    step("claims check mutations", os.path.join(T, "claims_check.py"), "--test")
    step("zone pages: every figure recomputed", os.path.join(T, "zone_check.py"))
    step("zone check mutations", os.path.join(T, "zone_check.py"), "--test")
    step("county towns: Census place and ZIP in this county", os.path.join(T, "town_check.py"))
    step("town check mutations", os.path.join(T, "town_check.py"), "--test")
    step("unit tests", os.path.join(T, "test_calc.py"))
    step("cloud aggregation on a synthetic FEMA download", os.path.join(T, "test_raw.py"))
    step("mutation suite", os.path.join(T, "test_gate.py"))
    step("factory stress (edge-case data, no crash)", os.path.join(T, "test_factory.py"))
    step("site factory stress (national edge cases: no crash, garbage, dead link)", os.path.join(T, "test_site_factory.py"))
    step("hater verdict parser", os.path.join(T, "test_hater.py"))
    step("sitemap lastmod rule", os.path.join(T, "lastmod.py"), "--test")
    step("deploy wait: stuck or failed deploy run stops the release", os.path.join(T, "release.py"), "--test-deploy-wait")
    step("national rules live once on /nfip/ (owner 11-11)", os.path.join(T, "rules_home.py"))
    step("national rules guard mutations", os.path.join(T, "rules_home.py"), "--test")
    step("identical text across place pages: warning only (owner 11-08, 11-11)", os.path.join(T, "sameness.py"))
    step("sameness ratchet mutation", os.path.join(T, "sameness.py"), "--test")
    step("research paper gate: sections, banned words, 90% ranges, every row + CSV + county card recomputed (PAPER-GATE-PROMPT)", os.path.join(T, "paper_gate.py"))
    step("research paper gate mutations", os.path.join(T, "paper_gate.py"), "--test")
    step("AdSense verification tag + ads.txt (owner 11-12)", os.path.join(T, "adsense_check.py"))
    step("AdSense check mutations", os.path.join(T, "adsense_check.py"), "--test")
    step("hub page word rules mutations", os.path.join(T, "hub_words.py"), "--test")
    step("hub page word rules (pages gate.py never sees)", os.path.join(T, "hub_words.py"))
    step("phone check (dist)", os.path.join(T, "phone_check.py"))
    step("phone check P8 mutation (answers below screen 1 must fail)", os.path.join(T, "phone_check.py"), "--test")
    # Google gate; S12 (hater review) is skipped only by --hotfix "<reason>", for a fix that removes wrong text from live pages
    hot = sys.argv[sys.argv.index("--hotfix") + 1] if "--hotfix" in sys.argv else ""
    step("google gate mutations (S6 sitemap)", os.path.join(T, "test_google_gate.py"))
    step("google gate", os.path.join(T, "google_gate.py"), *(["--skip-review"] if hot else []))
    if hot:   # a hotfix only removes or corrects text: no page may gain a figure it did not have in the last release
        R_ = os.path.dirname(T); grew = []
        for d, _, fs in os.walk(os.path.join(R_, "dist")):
            for f in (x for x in fs if x.endswith(".html")):
                rel = os.path.relpath(os.path.join(d, f), R_).replace("\\", "/")
                old = subprocess.run(["git", "show", "HEAD:" + rel], cwd=R_, capture_output=True, text=True, encoding="utf-8").stdout
                new_keys = set(re.findall(r'data-m="(\w+)"', open(os.path.join(d, f), encoding="utf-8").read())) - set(re.findall(r'data-m="(\w+)"', old))
                if old and new_keys: grew.append(f"{rel}: {sorted(new_keys)}")
        if grew: sys.exit("RELEASE STOPPED at: hotfix adds figures (needs a hater review): " + "; ".join(grew[:5]))
    if "--ship" not in sys.argv: sys.exit(print("READY TO SHIP: release.py --ship [--hotfix \"reason\"]"))
    # deploy.yml deploys the COMMITTED dist on any push that changes it, so commit the built pages before anything ships
    R = os.path.dirname(T); g = lambda *a: subprocess.run(["git", *a], cwd=R, check=True)
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=R, capture_output=True, text=True).stdout.strip()   # IndexNow: pages changed since here
    subprocess.run([sys.executable, "-I", os.path.join(T, "sameness.py"), "--record"], cwd=R)   # the shipped share becomes the new ceiling
    g("add", "-A", "dist", "data/c", "data/states", "places.json", "tools", "state")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=R).returncode:
        g("commit", "-q", "-m", "release: built site" + (f" (hotfix, hater review skipped: {hot})" if hot else "")
          + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    g("push", "-q")
    # audit 11-10: deploy.yml (site-deploy concurrency group) is the ONE deployer; a local wrangler deploy beside it was a
    # second writer that could land out of order. Wait for the deploy run of the pushed commit, then gate live.
    import time
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=R, capture_output=True, text=True).stdout.strip()
    if subprocess.run(["git", "diff", "--quiet", base, "HEAD", "--", "dist"], cwd=R).returncode:   # no dist change = deploy.yml does not run, nothing new to deploy
        rid = ""
        for _ in range(40):   # the run appears a few seconds after the push
            rid = subprocess.run(["gh", "run", "list", "--workflow", "deploy.yml", "--commit", head, "--json", "databaseId", "-q", ".[0].databaseId"],
                                 cwd=R, capture_output=True, text=True).stdout.strip()
            if rid: break
            time.sleep(6)
        def poll():
            j = json.loads(subprocess.run(["gh", "run", "view", rid, "--json", "status,conclusion,jobs"], cwd=R, capture_output=True, text=True).stdout or "{}")
            return j.get("status"), j.get("conclusion"), started_jobs(j)
        why = wait_deploy(poll, time.monotonic, time.sleep) if rid else "not started: no deploy.yml run appeared (Actions off or push event lost)"
        if why.startswith("not started"):   # 11-14: GitHub never ran the job, so there is no second writer: deploy the same committed dist here
            # wrangler uploads ./dist as it is on disk: only the committed release may go live (11-14 audit: a build running beside it would ship unchecked pages)
            dirty = subprocess.run(["git", "status", "--porcelain", "--", "dist"], cwd=R, capture_output=True, text=True).stdout.strip()
            now_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=R, capture_output=True, text=True).stdout.strip()
            if dirty or now_head != head: sys.exit(f"RELEASE STOPPED at: deploy (deploy.yml {why}; dist differs from committed {head[:9]}, local deploy refused)")
            print(f"deploy.yml run {rid} {why}; deploying committed {head[:9]} from this machine", flush=True)
            subprocess.run(["npx", "--yes", "wrangler@4.86.0", "deploy"], cwd=R, check=True, shell=os.name == "nt")
        elif why: sys.exit(f"RELEASE STOPPED at: deploy (deploy.yml run {rid} for {head[:9]}: {why})")
    time.sleep(20)   # Cloudflare edge caches
    step("live", os.path.join(T, "release.py"), "--live")
    subprocess.run([sys.executable, "-I", os.path.join(T, "indexnow.py"), base], cwd=R)   # notice only; never stops a release
    print("SHIPPED")
