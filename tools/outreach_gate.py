"""Outreach gate (owner 11-14: "I don't outreach shit pages; read it like a human Forbes editor; screenshot every page").
One review system, not two: the page needs a PASS from a `hater.py prep <round> <pages> --editor` round (phone, desktop, dark,
JavaScript-off screenshots + the six reviewers + the editor in docs/HATER-PROMPT.md), recorded by hater.py record, and the
LIVE page's exact visible text must still be the text that round hashed. Any later change = re-review before sending.
Usage: python -I tools/outreach_gate.py <url> [<url> ...]   exit 1 if any page may not be pitched | --test
Edge cases (each a --test case): no review; FAIL or a BLOCKER/MAJOR left; a light or carried PASS (no screenshots, no
editor_sha); live text changed after the review (a figure refreshed); page noindex or not live; a URL off this site."""
import hashlib, os, sys, urllib.request
from urllib.parse import urlparse
T = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, T)
import hater, review as RV

def slug_of(u):
    p = urlparse(u)
    if p.netloc not in ("floodinsurancedata.com", "www.floodinsurancedata.com"): return None
    path = p.path.strip("/")
    if not path: return "home"
    parts = path.split("/")
    if len(parts) == 2 and parts[0] == "flood-insurance" and hater.data_dir(parts[1]): return parts[1]   # state or county page
    return path

def why_not(u, fetch, get=RV.get):
    s = slug_of(u)
    if not s: return "not a floodinsurancedata.com page"
    r = get(s)
    if not r: return "no review"
    if r.get("verdict") != "PASS" or r.get("defects"): return f"review is {r.get('verdict')} with {len(r.get('defects') or [])} BLOCKER/MAJOR"
    if not r.get("editor_sha"): return "PASS has no editor round (screenshots + editor read): run hater.py prep <round> <page> --editor"
    h = fetch(u)
    if h is None: return "not live"
    if 'name="robots" content="noindex' in h: return "page is noindex"
    if hashlib.sha256(hater.exact_text(h).encode()).hexdigest() != r["editor_sha"]: return "live text changed since the editor review: re-review"
    return ""

def live(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "floodinsurancedata-outreach-gate/1"}), timeout=30).read().decode("utf-8")
    except Exception: return None

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        page = "<html><head><title>t</title></head><body><h1>Zone AE</h1><p>1,234 claims</p></body></html>"
        sha = hashlib.sha256(hater.exact_text(page).encode()).hexdigest(); U = "https://floodinsurancedata.com/guides/loma-lomr/"
        ok = {"verdict": "PASS", "defects": [], "editor_sha": sha}
        f = lambda h: (lambda u: h)
        assert why_not(U, f(page), lambda s: ok) == ""
        assert why_not(U, f(page), lambda s: None) == "no review"
        assert "FAIL" in why_not(U, f(page), lambda s: {**ok, "verdict": "FAIL"})
        assert "BLOCKER" in why_not(U, f(page), lambda s: {**ok, "defects": ["**MAJOR** x"]})
        assert "editor round" in why_not(U, f(page), lambda s: {"verdict": "PASS", "defects": []})   # light or carried PASS
        assert "changed" in why_not(U, f(page.replace("1,234", "1,235")), lambda s: ok)   # one figure refreshed
        assert why_not(U, f(None), lambda s: ok) == "not live"
        assert why_not(U, f(page.replace("<title>", '<meta name="robots" content="noindex,follow"><title>')), lambda s: ok) == "page is noindex"
        assert why_not("https://example.com/x/", f(page), lambda s: ok) == "not a floodinsurancedata.com page"
        assert slug_of("https://floodinsurancedata.com/") == "home" and slug_of(U) == "guides/loma-lomr"
        sys.exit(print("outreach_gate --test: 10 cases PASS"))
    bad = [(u, w) for u in sys.argv[1:] if (w := why_not(u, live))]
    for u, w in bad: print("OUTREACH BLOCKED", u, "-", w)
    print("OUTREACH GATE FAIL" if bad or not sys.argv[1:] else f"OUTREACH GATE PASS ({len(sys.argv) - 1} pages)"); sys.exit(1 if bad or not sys.argv[1:] else 0)
