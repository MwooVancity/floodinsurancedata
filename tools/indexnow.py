"""IndexNow (Bing, Yandex, others): tell search engines which pages changed in a release. Agreed plan 11-06 step 1.
A notice only: it proves nothing about indexing, and a failure here never fails a release (the pages are already live).
Only URLs whose built HTML changed between <base> and HEAD are sent (Bing: notify changed URLs, not the whole site).
The key file dist/<KEY>.txt is written by build_site.py; IndexNow keys are public by design.
Usage: python -I tools/indexnow.py <base-commit>   |   --test (URL mapping self-check, sends nothing)"""
import json, os, subprocess, sys, urllib.request

KEY = "6f1c2a9e4b7d40c8a3e5f9b2d1c07e64"
HOST = "floodinsurancedata.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def urls(paths):   # dist/flood-insurance/florida/index.html -> https://floodinsurancedata.com/flood-insurance/florida/
    out = []
    for p in paths:
        p = p.replace("\\", "/")
        if not (p.startswith("dist/") and p.endswith("index.html")): continue
        out.append(f"https://{HOST}/" + p[len("dist/"):-len("index.html")])
    return sorted(set(out))

def changed(base):
    r = subprocess.run(["git", "diff", "--name-only", base, "HEAD", "--", "dist"], cwd=ROOT, capture_output=True, text=True, check=True)
    return urls(r.stdout.split())

def send(us):
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": us[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp: return resp.status
    except Exception as e: return repr(e)[:120]

if __name__ == "__main__":
    if "--test" in sys.argv:
        assert urls(["dist/index.html", "dist/flood-zones/x/index.html", "dist/sitemap.xml", "data/x/index.html"]) == \
            [f"https://{HOST}/", f"https://{HOST}/flood-zones/x/"]
        print("indexnow mapping OK"); sys.exit()
    us = changed(sys.argv[1] if len(sys.argv) > 1 else "HEAD~1")
    if not us: print("indexnow: no changed pages"); sys.exit()
    print(f"indexnow: {len(us)} changed pages, response {send(us)} (200/202 = received, not indexed)")
