"""Hater review records (owner 2026-10-27: "no pages live unless scrutinized like the worst hater in the world").
A page ships only with state/reviews/<slug>.json = {"verdict": "PASS", "template": <hash>, "defects": [], ...} written
after a hostile reviewer READ the rendered page. The hash covers the page template and its rule/metric modules, so any
template change makes every review stale. google_gate.py S12 and add_counties.py refuse a page without a current PASS.
Usage: python -I tools/review.py status        (which pages lack a current PASS)"""
import hashlib, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "state", "reviews")
TEMPLATE = [os.path.join(ROOT, "tools", f) for f in ("build_page.py", "build_site.py", "metrics.py", "rules_registry.py")]

def template_hash():
    h = hashlib.sha256()
    for f in TEMPLATE: h.update(open(f, "rb").read().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:16]

def get(slug):
    p = os.path.join(DIR, slug + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

def ok(slug, th=None):
    r = get(slug)
    return bool(r) and r.get("verdict") == "PASS" and r.get("template") == (th or template_hash()) and not r.get("defects")

def record(slug, verdict, defects, reviewer, notes=""):
    os.makedirs(DIR, exist_ok=True)
    json.dump({"slug": slug, "verdict": verdict, "template": template_hash(), "defects": defects, "reviewer": reviewer,
               "notes": notes}, open(os.path.join(DIR, slug + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

if __name__ == "__main__" and sys.argv[1:2] == ["status"]:
    th = template_hash(); places = json.load(open(os.path.join(ROOT, "places.json")))
    states = json.load(open(os.path.join(ROOT, "data", "states", "built.json")))
    slugs = ["home"] + [s["slug"] for s in states] + [p["slug"] for p in places]
    bad = [s for s in slugs if not ok(s, th)]
    print(f"template {th}: {len(slugs) - len(bad)} of {len(slugs)} pages have a current hater PASS")
    for s in bad[:20]: print("  needs review:", s, "(" + ((get(s) or {}).get("verdict") or "none") + ")")
