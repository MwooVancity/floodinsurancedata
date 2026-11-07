"""Hater review records. Owner 2026-10-27: "no pages live unless scrutinized like the worst hater in the world", then
(same day, Musk's five steps): review the TEMPLATE deeply, not every page again.
A page may ship when either:
  1. it has its own current PASS (state/reviews/<slug>.json, verdict PASS, this template hash), or
  2. the template is approved (the SAMPLES home, one state and one county all have a current PASS) AND the page is
     not flagged by flags(): the code check for what varies page to page (numbers far from the state, small samples).
     A flagged page needs its own PASS (a quick look at what is unusual, not a full review).
The hash covers the template and its rule/metric modules: any template change makes every PASS stale, so only the
3 samples are reviewed again. google_gate.py S12 and add_counties.py both use ok().
Usage: python -I tools/review.py status"""
import hashlib, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "state", "reviews")
TEMPLATE = [os.path.join(ROOT, "tools", f) for f in ("build_page.py", "build_site.py", "metrics.py", "rules_registry.py", "notes.py", "codes.py", "zonemap_block.py", "static/zonemap.js")]
SAMPLES = ("home", "louisiana", "palm-beach-county-fl")   # one page per template, the ones the hater reads in depth

def template_hash():
    h = hashlib.sha256()
    for f in TEMPLATE: h.update(open(f, "rb").read().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:16]

def get(slug):
    p = os.path.join(DIR, slug + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

def own_pass(slug, th=None):
    r = get(slug)
    return bool(r) and r.get("verdict") == "PASS" and r.get("template") == (th or template_hash()) and not r.get("defects")

def template_ok(th=None):
    th = th or template_hash()
    return all(own_pass(s, th) for s in SAMPLES)

def _load(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}

def flags(slug):
    """What varies page to page, checked by code: a county whose figures sit far from its state's, or rest on few
    records, gets a reason here (state dollar shares are left out: one disaster county dominates them) and needs its own review. Thresholds are wide on purpose: they catch Palm Beach's
    56.5% unpaid vs Florida's 30.1%, not ordinary local variation."""
    d = os.path.join(ROOT, "data", "c", slug)
    agg, data = _load(os.path.join(d, "agg.json")), _load(os.path.join(d, "data.json"))
    if not agg:   # a queued county not built here yet: its raw file
        q = {c["slug"]: c for c in (_load(os.path.join(ROOT, "state", "county-queue.json")) or [])}
        if slug not in q: return []   # home or a state page: nothing to compare against
        raw = _load(os.path.join(ROOT, "data", "all-counties", q[slug]["geoid"] + ".json"))
        agg, data = {"policies": raw.get("policies", {}), "claims": raw.get("claims", {}), "state": raw.get("state")}, {"claims_extra": raw.get("claims_extra") or {}}
    if agg.get("level") == "state" or not agg.get("state"): return []
    sys.path.insert(0, os.path.join(ROOT, "tools")); from agg_raw import NAMES, slug as sslug
    sa = _load(os.path.join(ROOT, "data", "states", sslug(agg["state"]), "agg.json"))
    sx = _load(os.path.join(ROOT, "data", "states", sslug(agg["state"]), "data.json")).get("claims_extra") or sa.get("claims_extra") or {}
    P, C, cx = agg.get("policies", {}), agg.get("claims", {}), data.get("claims_extra") or {}
    out = []
    if cx.get("cwop_share") is not None and sx.get("cwop_share") is not None and abs(cx["cwop_share"] - sx["cwop_share"]) > 20:
        out.append(f"unpaid {cx['cwop_share']}% vs state {sx['cwop_share']}%")
    sc, su = (sa.get("claims") or {}).get("rows"), (sa.get("policies") or {}).get("units")
    if C.get("rows") and P.get("units") and sc and su:
        r = (C["rows"] / P["units"]) / (sc / su)
        if r < 0.2 or r > 5: out.append(f"claims per policy {r:.2f}x the state's")
    return out

def flag_kind(f):   # the kind of oddity, and how far out it is (for the extreme guard)
    import re as _re
    if f.startswith("unpaid"):
        a, b = [float(x) for x in _re.findall(r"[\d.]+", f)[:2]]; return "unpaid", abs(a - b)
    r = float(_re.findall(r"[\d.]+", f)[0]); return ("claims_low", 1 / max(r, 1e-6)) if r < 1 else ("claims_high", r)

def kind_approved(fl, th):
    """PLAN scale problem 3: a flagged page may ship when a page with the same kind of flag passed its own review under
    this template, and this page is not more than twice as far out as that example (more extreme = its own review)."""
    ex = {}
    for p in os.listdir(DIR):
        if p.endswith(".json") and own_pass(p[:-5], th):
            for k, v in (flag_kind(f) for f in flags(p[:-5])): ex[k] = max(ex.get(k, 0), v)
    return all(k in ex and v <= 2 * ex[k] for k, v in (flag_kind(f) for f in fl))

def ok(slug, th=None):
    th = th or template_hash()
    if own_pass(slug, th): return True
    fl = flags(slug)
    # round 32 passed the round-31 fixes on flagged examples (Manhattan, Broward), so kind approval is back on
    return template_ok(th) and (not fl or kind_approved(fl, th))

def record(slug, verdict, defects, reviewer, notes="", template=None):
    """template = the hash the reviewer saw (saved at prep); an edit made after the review must not inherit its PASS."""
    os.makedirs(DIR, exist_ok=True)
    json.dump({"slug": slug, "verdict": verdict, "template": template or template_hash(), "defects": defects, "reviewer": reviewer,
               "notes": notes}, open(os.path.join(DIR, slug + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

if __name__ == "__main__" and sys.argv[1:2] == ["status"]:
    th = template_hash(); places = json.load(open(os.path.join(ROOT, "places.json")))
    states = json.load(open(os.path.join(ROOT, "data", "states", "built.json")))
    slugs = ["home"] + [s["slug"] for s in states] + [p["slug"] for p in places]
    print(f"template {th}: samples {'APPROVED' if template_ok(th) else 'not approved'} ({', '.join(s + ('=PASS' if own_pass(s, th) else '') for s in SAMPLES)})")
    fl = {s: flags(s) for s in slugs}
    print(f"{sum(1 for s in slugs if ok(s, th))} of {len(slugs)} pages may ship; {sum(1 for v in fl.values() if v)} flagged for their own look")
    for s, v in fl.items():
        if v: print("  flagged:", s, "|", "; ".join(v))
