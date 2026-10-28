"""Live = what passed. Every built page in dist/ is fetched from the live site with Googlebot's user agent and must
be byte-identical to the file that passed the gates (proves the deploy, and that crawlers get what readers get).
Replaces re-gating 93 live pages and the hand-picked "live body" loop (ponytail audit 2026-10-27).
Usage: python -I tools/gate_live.py"""
import hashlib, os, re, sys, time, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST, BASE = os.path.join(ROOT, "dist"), "https://floodinsurancedata.com"
UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

def fetch(url):
    for i in range(4):   # a slow edge read once stopped a release that had already deployed
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e: last = e; time.sleep(5 * (i + 1))
    raise RuntimeError(f"{url}: {last!r}"[:160])

bad, n = [], 0
for d, _, fs in os.walk(DIST):
    for f in fs:
        if not f.endswith(".html"): continue
        rel = os.path.relpath(os.path.join(d, f), DIST).replace("\\", "/")
        url = BASE + "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)
        built = open(os.path.join(d, f), "rb").read().replace(b"\r\n", b"\n"); n += 1   # Windows writes CRLF; git deploys LF
        try: live = fetch(url + "?v=" + hashlib.sha256(built).hexdigest()[:8])   # past any edge cache
        except RuntimeError as e: bad.append(str(e)); continue
        live = re.sub(rb'<script type="module" src="https://static\.cloudflareinsights\.com/[^>]*></script>\n?', b"", live)   # Cloudflare Web Analytics, injected at the edge
        if live.replace(b"\r\n", b"\n") != built: bad.append(f"{url}: live differs from dist ({len(live)} vs {len(built)} bytes)")
print(f"live pages checked: {n}, differing: {len(bad)}")
for b in bad: print("  ", b)
sys.exit(1 if bad else 0)
