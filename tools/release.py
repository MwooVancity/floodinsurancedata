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
    print("LIVE OK")
else:
    out = subprocess.run([sys.executable, "-I", os.path.join(T, "build_all.py")], cwd=os.path.dirname(T),
                         capture_output=True, text=True).stdout
    n_pass, bad = len(re.findall(r"GATE PASS", out)), re.findall(r".*(?:GATE FAIL|FAILED|\[\w+\]).*", out)
    print(f"== build + gate: {n_pass} pages pass"); [print("  ", b) for b in bad[:30]]
    if bad or not n_pass: sys.exit("RELEASE STOPPED at: build + gate")
    step("unit tests", os.path.join(T, "test_calc.py"))
    step("mutation suite", os.path.join(T, "test_gate.py"))
    step("phone check (dist)", os.path.join(T, "phone_check.py"))
    print("READY TO DEPLOY (then: release.py --live, and run recheck.py)")
