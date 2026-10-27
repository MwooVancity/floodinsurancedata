"""One command for a release, in order; stops at the first failure.
  python -I tools/release.py          build all pages + gate 2 on each, unit tests, mutation suite, phone check (dist)
  python -I tools/release.py --live   after deploy: phone check + body check on the live site
recheck.py (network, minutes) runs separately as its own background job before a release is called verified."""
import os, re, subprocess, sys, urllib.request

T = os.path.dirname(os.path.abspath(__file__))
def step(name, *cmd):
    print(f"== {name}", flush=True)
    r = subprocess.run([sys.executable, "-I", *cmd], cwd=os.path.dirname(T))
    if r.returncode: sys.exit(f"RELEASE STOPPED at: {name}")

if "--live" in sys.argv:
    base = "https://floodinsurancedata.com"
    step("phone check (live)", os.path.join(T, "phone_check.py"), "--base", base)
    import json   # every state the home page links to must be live, not just three counties
    states = [s["slug"] for s in json.load(open(os.path.join(os.path.dirname(T), "data", "states", "built.json")))]
    for s in ("brevard-county-fl", "jefferson-parish-la", "kanawha-county-wv", *states):
        req = urllib.request.Request(f"{base}/flood-insurance/{s}/", headers={"User-Agent": "Mozilla/5.0 (release-check)"})
        body = urllib.request.urlopen(req, timeout=60).read().decode()   # Cloudflare 403s Python's default UA
        ok = 'data-m="cost_p50"' in body and "srclist" in body and len(body) > 30000
        print(f"live body {s}: {'ok' if ok else 'BAD'} ({len(body)} bytes)")
        if not ok: sys.exit("RELEASE STOPPED at: live body")
    step("gate on every live page", os.path.join(T, "gate_live.py"))
    print("LIVE OK")
else:
    out = subprocess.run([sys.executable, "-I", os.path.join(T, "build_all.py")], cwd=os.path.dirname(T),
                         capture_output=True, text=True).stdout
    n_pass, bad = len(re.findall(r"GATE PASS", out)), re.findall(r".*(?:GATE FAIL|FAILED|\[\w+\]).*", out)
    print(f"== build + gate: {n_pass} pages pass"); [print("  ", b) for b in bad[:30]]
    if bad or not n_pass: sys.exit("RELEASE STOPPED at: build + gate")
    step("unit tests", os.path.join(T, "test_calc.py"))
    step("mutation suite", os.path.join(T, "test_gate.py"))
    step("hater verdict parser", os.path.join(T, "test_hater.py"))
    step("phone check (dist)", os.path.join(T, "phone_check.py"))
    # Google gate; S12 (hater review) is skipped only by --hotfix "<reason>", for a fix that removes wrong text from live pages
    hot = sys.argv[sys.argv.index("--hotfix") + 1] if "--hotfix" in sys.argv else ""
    step("google gate", os.path.join(T, "google_gate.py"), *(["--skip-review"] if hot else []))
    if "--ship" not in sys.argv: sys.exit(print("READY TO SHIP: release.py --ship [--hotfix \"reason\"]"))
    # every push to master redeploys the COMMITTED dist (deploy.yml), so commit the built pages before anything ships
    R = os.path.dirname(T); g = lambda *a: subprocess.run(["git", *a], cwd=R, check=True)
    g("add", "-A", "dist", "data/c", "places.json", "tools", "state")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=R).returncode:
        g("commit", "-q", "-m", "release: built site" + (f" (hotfix, hater review skipped: {hot})" if hot else "")
          + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    g("push", "-q")
    if subprocess.run("npx wrangler deploy", cwd=R, shell=True).returncode: sys.exit("RELEASE STOPPED at: deploy")
    import time; time.sleep(45)
    step("live", os.path.join(T, "release.py"), "--live")
    print("SHIPPED")
