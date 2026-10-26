"""Generator: build every county in tools/counties.json, then the shared site.
Per county: collect_small -> collect -> nri -> build_page -> gate. Resumable (skips a county whose
agg.json already exists unless FF_FORCE=1). Then build_site. One command builds the whole site.
Usage: python -I tools/build_all.py"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
DIST = os.path.join(ROOT, "dist")
PLACES = os.path.join(ROOT, "places.json")
PUBLISHED = os.path.join(ROOT, "published.json")   # authoritative list of counties that passed THIS run
BASE = os.environ.get("FF_BASEURL", "https://floodinsurancedata.com")
FORCE = os.environ.get("FF_FORCE") == "1"
counties = json.load(open(os.path.join(TOOLS, "counties.json")))

# fail-closed: rebuild the published list from scratch each run so a county that now fails can never
# linger on the home page / sitemap / CSV from an earlier success.
for f in (PLACES, PUBLISHED):
    try: os.remove(f)
    except FileNotFoundError: pass

def agg_complete(path):
    try: return json.load(open(path)).get("complete") is True
    except Exception: return False

# Pre-populate places.json from every complete agg.json BEFORE rendering, so each page's sibling links see
# the FULL county set — not just the ones built earlier in this run (which left the first/biggest page in
# each state with 0 links). build_page reads this, keeps it whole (removes+re-adds only itself).
_pre = []
for _c in counties:
    _ap = os.path.join(DATA, _c["slug"], "agg.json")
    if agg_complete(_ap):
        _a = json.load(open(_ap)); _P = _a["policies"]
        _pre.append({"slug": _c["slug"], "label": _c["label"], "short": _c["short"], "geoid": _c["geoid"],
                     "units": _P.get("units"), "median": _P.get("p50"),
                     "state": (_a.get("nri") or {}).get("state")})
_pre.sort(key=lambda p: -(p.get("units") or 0))
if _pre:
    json.dump(_pre, open(PLACES, "w"), indent=1)

def run(script, env, args=()):
    e = dict(os.environ, **env)
    r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, script), *args],
                       env=e, cwd=TOOLS, capture_output=True, text=True)
    tag = f"[{script} {env.get('FF_GEOID','')}]"
    if r.stdout.strip(): print(tag, r.stdout.strip().splitlines()[-1])
    if r.returncode != 0:
        print(tag, "FAILED\n", r.stdout[-400:], r.stderr[-400:])
    return r.returncode

ok, blocked = [], []
for c in counties:
    slug = c["slug"]
    d = os.path.join(DATA, slug)
    os.makedirs(d, exist_ok=True)
    env = {"FF_STATE": c["state"], "FF_GEOID": c["geoid"], "FF_COUNTY": c["county"],
           "FF_COUNTYTITLE": c["countytitle"], "FF_COUNTYLABEL": c["label"], "FF_COUNTYSHORT": c["short"],
           "FF_SLUG": slug, "FF_OFFICIAL": str(c.get("official", 0)), "FF_DIR": d,
           "FF_PLACES": PLACES, "FF_BASEURL": BASE}
    agg = os.path.join(d, "agg.json")
    # resume from the first INCOMPLETE stage: a partial/absent agg.json (claims failed, etc.) re-collects.
    if FORCE or not agg_complete(agg):
        if run("collect_small.py", env): blocked.append(slug + " (small datasets)"); continue
        if run("collect.py", env): blocked.append(slug + " (policies/claims 503 — rerun when API calm)"); continue
        run("nri.py", env, args=[c["geoid"], agg])
        if not agg_complete(agg): blocked.append(slug + " (agg incomplete after collect)"); continue
    out = os.path.join(DIST, "flood-insurance", slug, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    env["OUT_HTML"] = out
    if run("build_page.py", env): blocked.append(slug + " (build)"); continue
    if run("gate.py", env, args=[agg, out, str(c.get("official", 0))]): blocked.append(slug + " (gate)"); continue
    # verified decision record: why this page exists + its evidence (ChatGPT review #5/#7)
    a = json.load(open(agg)); Pp = a["policies"]
    official = c.get("official", 0)
    recon = round(abs(Pp["units"] - official) / official * 100, 2) if official else None
    crit = {
        "statistical_sufficiency": {"valid_cost_obs": Pp.get("cost_n"), "spread_published": bool(Pp.get("spread_ok")),
                                     "pass": (Pp.get("cost_n") or 0) >= 100},
        "data_completeness": {"manifest": a.get("manifest"),
                              "pass": all((v.get("complete") and not v.get("provisional")) for v in a.get("manifest", {}).values())},
        # Reconciliation to FEMA's official PIF count is a SECONDARY cross-check, not a correctness
        # requirement: the API numbers are valid without it. Enforce <=5% ONLY where an official count is
        # known; where it isn't, ship with "reconciliation pending" (completeness + the recheck already
        # prove the pull is whole). Blocking a valid page merely for lacking the benchmark would hide
        # available public evidence.
        "reconciliation": {"pct": recon, "official_known": bool(official), "pass": (recon is None) or (recon <= 5)},
        "distinct_from_parent": "N/A — county is the base geography (no parent to dedupe against); "
                                "the 3-part test applies to sub-county ZIP pages, none published",
        "distinct_search_intent": "NOT measurable offline — requires Search Console/keyword data post-launch",
    }
    # data_ok = technical/data approval only. indexing_approved is a SEPARATE editorial/SEO decision
    # (needs search-demand evidence) and stays false until a human approves it.
    data_ok = crit["statistical_sufficiency"]["pass"] and crit["data_completeness"]["pass"] and crit["reconciliation"]["pass"]
    json.dump({
        "slug": slug, "label": c["label"], "geoid": c["geoid"],
        "sources": {"policies_asof": Pp.get("asof"), "retrieved": Pp.get("retrieved")},
        "policy_units": Pp.get("units"), "cohort_n": Pp.get("cohort_n"),
        "publish_criteria": crit, "data_ok": data_ok, "indexing_approved": False, "gate": "pass",
    }, open(os.path.join(d, "manifest.json"), "w"), indent=1)
    if not data_ok: blocked.append(slug + " (data criteria not met)"); continue
    ok.append(slug)

# C1: DUPLICATION GUARD — no two published pages may share more than DUP_THRESH of their FULL visible
# text, numbers and place names INCLUDED. On a data page the numbers ARE the content that makes each
# county distinct, so they must count: an earlier version masked numbers+names and then measured overlap,
# which deleted the real differentiation and wrongly flagged genuinely distinct counties (different median,
# claims, zones, CRS) as duplicates. This 8-gram check on full text still catches a true mad-lib/doorway
# page (same prose, one number swapped ~ >0.9 overlap) but passes pages that share only structure. Of any
# over-threshold pair the page with FEWER policies (less unique data) is dropped; the richest survives.
import re as _re
DUP_THRESH = 0.85
def _page_shingles(slug, k=8):
    t = open(os.path.join(DIST, "flood-insurance", slug, "index.html"), encoding="utf-8").read()
    t = _re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=_re.S | _re.I)
    t = _re.sub(r"<[^>]+>", " ", t).lower()
    w = _re.findall(r"[a-z0-9]+", t)
    return set(tuple(w[i:i+k]) for i in range(max(0, len(w) - k + 1)))
def _units(slug):
    try: return json.load(open(os.path.join(DATA, slug, "agg.json")))["policies"]["units"] or 0
    except Exception: return 0
_kept, _sh = [], {}
for slug in sorted(ok, key=lambda s: -_units(s)):   # richest first; it wins any duplicate pair
    _sh[slug] = _page_shingles(slug)
    hit = None
    for ks in _kept:
        inter = len(_sh[slug] & _sh[ks]); uni = len(_sh[slug] | _sh[ks]) or 1
        if inter / uni > DUP_THRESH: hit = (ks, inter / uni); break
    if hit:
        blocked.append(f"{slug} (near-duplicate {hit[1]:.0%} of {hit[0]})")
        print(f"DUP BLOCK {slug} ~ {hit[0]} ({hit[1]:.0%} masked overlap)")
    else:
        _kept.append(slug)
ok = _kept

# fail-closed: prune any county dir in dist that did NOT pass this run (stale output never served).
fdir = os.path.join(DIST, "flood-insurance")
if os.path.isdir(fdir):
    for name in os.listdir(fdir):
        if name not in ok and os.path.isdir(os.path.join(fdir, name)):   # only county dirs; never the hub index.html
            import shutil; shutil.rmtree(os.path.join(fdir, name), ignore_errors=True)
            print("pruned stale dist/flood-insurance/" + name)
# state pages: rebuilt and gated every run (the prune above removed them); a failing state is removed and left out of built.json
run("build_states.py", {"FF_BASEURL": BASE})
# the site (home search, sitemap, CSV) is built ONLY from counties that passed this run.
json.dump(ok, open(PUBLISHED, "w"))
run("build_site.py", {"FF_PLACES": PLACES, "FF_DIST": DIST, "FF_DATADIR": DATA,
                      "FF_BASEURL": BASE, "FF_PUBLISHED": PUBLISHED})
print("\nBUILT:", ok)
if blocked: print("BLOCKED:", blocked)
