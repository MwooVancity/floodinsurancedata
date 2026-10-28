"""One command for a release, in order; stops at the first failure.
  python -I tools/release.py          build all pages + gate 2 on each, unit tests, mutation suite, phone check (dist)
  python -I tools/release.py --live   after deploy: phone check + every live page byte-equal to the built page
recheck.py (network, minutes) runs separately as its own background job before a release is called verified."""
import os, re, subprocess, sys

T = os.path.dirname(os.path.abspath(__file__))
def step(name, *cmd):
    print(f"== {name}", flush=True)
    r = subprocess.run([sys.executable, "-I", *cmd], cwd=os.path.dirname(T))
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
    step("unit tests", os.path.join(T, "test_calc.py"))
    step("mutation suite", os.path.join(T, "test_gate.py"))
    step("hater verdict parser", os.path.join(T, "test_hater.py"))
    step("phone check (dist)", os.path.join(T, "phone_check.py"))
    # Google gate; S12 (hater review) is skipped only by --hotfix "<reason>", for a fix that removes wrong text from live pages
    hot = sys.argv[sys.argv.index("--hotfix") + 1] if "--hotfix" in sys.argv else ""
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
