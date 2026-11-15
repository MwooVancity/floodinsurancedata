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

# Template text at most once a day (CLAUDE.md Site; 11-14: 6 site-wide releases in a day, one dropped 312 state links).
# A template ship = the review template hash (review.TEMPLATE files) differs from the last ship's AND some county/state
# page's visible text, digits and month names masked, differs from HEAD's copy. Ledger: state/template-ships.json.
# Edge cases: a data refresh changes numbers and the as-of month only (masked; template code unchanged = not a batch);
# code-only change with identical text = not a batch; a new county has no HEAD copy (skipped); first run, no ledger =
# text decides alone; the UTC day (cloud publish and CLAUDE.md count UTC); --hotfix ships and is still recorded; ledger
# capped at 60 entries. Ceiling: a data refresh that moves a size word (claim()) on the same day as a template edit counts.
TSHIPS = os.path.join(os.path.dirname(T), "state", "template-ships.json")

def template_refusal(changed, cur_hash, ledger, today, hot):   # '' to go, else why
    if not changed or (ledger.get("hash") and ledger["hash"] == cur_hash): return ""
    done = [s for s in ledger.get("ships", []) if s.get("date") == today and s.get("template")]
    if done and not hot: return (f"a template batch already shipped today ({today} UTC, commit {done[0].get('commit_before', '?')[:9]}); "
                                 f"this release changes county/state text on {len(changed)} pages, e.g. {changed[:3]}; ship it tomorrow, or --hotfix only for wrong live text")
    return ""

def template_pages_changed(R):   # county/state pages whose masked visible text differs from HEAD's copy
    sys.path.insert(0, T); import hater
    states = {s["slug"] for s in json.load(open(os.path.join(R, "data", "states", "built.json")))}
    rels = [f"dist/flood-insurance/{s}/index.html" for s in sorted(os.listdir(os.path.join(R, "dist", "flood-insurance")))
            if (s in states or os.path.isdir(os.path.join(R, "data", "c", s))) and os.path.exists(os.path.join(R, "dist", "flood-insurance", s, "index.html"))]
    out = subprocess.run(["git", "cat-file", "--batch"], cwd=R, input="".join(f"HEAD:{r}\n" for r in rels).encode(), capture_output=True).stdout
    mask = lambda h: hater.masked(hater.vis_text(h))   # digits and month names masked (hater.masked)
    changed, i = [], 0
    for r in rels:   # cat-file --batch: "<sha> blob <size>\n<bytes>\n" or "<name> missing\n"
        j = out.index(b"\n", i); head = out[i:j].split(); i = j + 1
        if head[-1] == b"missing": continue
        n = int(head[2]); old = out[i:i + n].decode("utf-8", "replace"); i += n + 1
        if mask(old) != mask(open(os.path.join(R, r), encoding="utf-8").read()): changed.append(r.split("/")[2])
    return changed

if "--test-template" in sys.argv:
    L = {"hash": "h1", "ships": [{"date": "2026-11-14", "template": True, "commit_before": "abc"}]}
    assert template_refusal(["a"], "h2", L, "2026-11-14", "").startswith("a template batch already shipped"), "second batch same day"
    assert template_refusal(["a"], "h2", L, "2026-11-14", "wrong figure live") == "", "--hotfix ships"
    assert template_refusal(["a"], "h2", L, "2026-11-15", "") == "", "next UTC day"
    assert template_refusal([], "h2", L, "2026-11-14", "") == "", "no visible county/state change"
    assert template_refusal(["a"], "h1", L, "2026-11-14", "") == "", "template code unchanged since last ship: a data refresh"
    assert template_refusal(["a"], "h2", {}, "2026-11-14", "") == "", "first run, no ledger"
    assert template_refusal(["a"], "h2", {"hash": "h1", "ships": [{"date": "2026-11-14", "template": False}]}, "2026-11-14", "") == "", "a data-only ship today"
    sys.path.insert(0, T); import hater
    m = lambda h: hater.masked(hater.vis_text(h))
    assert m("<p>As of August 31, 2026: $1,015</p>") == m("<p>As of September 30, 2026: $1,240</p>"), "data refresh masked"
    assert m("<p>As of August 31: the median</p>") != m("<p>As of August 31: the typical</p>"), "wording change seen"
    print("template once a day: 9 cases PASS"); sys.exit()

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
    # owner 11-14 "I don't want to ship nonperfect pages": the code that writes pages must be bug-reviewed before it ships
    # (a --hotfix for wrong live text may skip it, like the hater review). Checked first so a long gate run never ends in a refusal.
    # bug review 11-14: the cloud's daily publish runs release.py without --ship and then deploys, so it must stop too
    _need_cr = ("--ship" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true") and "--hotfix" not in sys.argv
    if _need_cr:
        sys.path.insert(0, T); import code_stamp
        _cr = code_stamp.check()
        if _cr: sys.exit(f"RELEASE STOPPED at: code bug review ({_cr}): run /code-review medium on the changed tools, fix every finding, then code_stamp.py --stamp")
    out = subprocess.run([sys.executable, "-I", os.path.join(T, "build_all.py")], cwd=os.path.dirname(T),
                         capture_output=True, text=True).stdout
    n_pass, bad = len(re.findall(r"GATE PASS", out)), re.findall(r".*(?:GATE FAIL|FAILED|\[\w+\]).*", out)
    print(f"== build + gate: {n_pass} pages pass"); [print("  ", b) for b in bad[:30]]
    if bad or not n_pass: sys.exit("RELEASE STOPPED at: build + gate")
    if "--ship" in sys.argv:   # template text at most once a UTC day; checked before the long steps
        import datetime; sys.path.insert(0, T); import review as _RV
        try: _tl = json.load(open(TSHIPS, encoding="utf-8"))
        except (OSError, ValueError): _tl = {}
        _tday, _th = str(datetime.datetime.now(datetime.timezone.utc).date()), _RV.template_hash()
        _tchanged = template_pages_changed(os.path.dirname(T))
        _twhy = template_refusal(_tchanged, _th, _tl, _tday, "--hotfix" in sys.argv)
        if _twhy: sys.exit(f"RELEASE STOPPED at: template text once a day ({_twhy})")
        print(f"== template once a day: {len(_tchanged)} county/state pages with changed wording; " + ("a template batch" if _tchanged and _tl.get("hash") != _th else "not a template batch"))
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
    step("25-a-day cap cases", os.path.join(T, "new_pages_cap.py"), "--test")
    step("cloud aggregation on a synthetic FEMA download", os.path.join(T, "test_raw.py"))
    step("mutation suite", os.path.join(T, "test_gate.py"))
    step("factory stress (edge-case data, no crash)", os.path.join(T, "test_factory.py"))
    step("site factory stress (national edge cases: no crash, garbage, dead link)", os.path.join(T, "test_site_factory.py"))
    step("hater verdict parser", os.path.join(T, "test_hater.py"))
    step("proofread flag + S12 notice cases (owner 11-15)", os.path.join(T, "hater.py"), "--test")
    step("writing gate mutations (owner 11-15)", os.path.join(T, "prose_check.py"), "--test")
    step("writing gate: repeats, 45-word sentences, doubled words; ratchet on state/prose-baseline.json", os.path.join(T, "prose_check.py"))
    step("template text once a day cases", os.path.join(T, "release.py"), "--test-template")
    step("cloud job budget cases (tools/cloud_run.py)", os.path.join(T, "cloud_run.py"), "--test")
    step("refresh plan cases (one forced refresh a month)", os.path.join(T, "refresh_plan.py"), "--test")
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
    step("outreach gate cases (editor round PASS on the exact live text)", os.path.join(T, "outreach_gate.py"), "--test")
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
    # owner 11-14: at most 25 new pages a day, all kinds; the ledger is written only by a run that ships (here or the cloud publish)
    _cap = [sys.executable, "-I", os.path.join(T, "new_pages_cap.py")] + (["--record"] if "--ship" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true" else [])
    if subprocess.run(_cap).returncode: sys.exit("RELEASE STOPPED at: 25 new pages a day (tools/new_pages_cap.py)")
    if "--ship" not in sys.argv: sys.exit(print("READY TO SHIP: release.py --ship [--hotfix \"reason\"]"))
    # deploy.yml deploys the COMMITTED dist on any push that changes it, so commit the built pages before anything ships
    R = os.path.dirname(T); g = lambda *a: subprocess.run(["git", *a], cwd=R, check=True)
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=R, capture_output=True, text=True).stdout.strip()   # IndexNow: pages changed since here
    subprocess.run([sys.executable, "-I", os.path.join(T, "sameness.py"), "--record"], cwd=R)   # the shipped share becomes the new ceiling
    if _need_cr and code_stamp.check(): sys.exit(f"RELEASE STOPPED at: code bug review (tools changed during the gate run: {code_stamp.check()})")   # bug review 11-14
    subprocess.run([sys.executable, "-I", os.path.join(T, "prose_check.py"), "--record"], cwd=R)   # the shipped faults become the new ceiling (lower only)
    if _tchanged and _tl.get("hash") != _th:   # record the template ship (committed with the release below)
        _tl.setdefault("ships", []).append({"date": _tday, "template": True, "commit_before": base, "pages": len(_tchanged)})
    _tl["hash"] = _th; _tl["ships"] = _tl.get("ships", [])[-60:]
    json.dump(_tl, open(TSHIPS, "w", encoding="utf-8"), indent=1)
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
