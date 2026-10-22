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
BASE = os.environ.get("FF_BASEURL", "https://example.com")
FORCE = os.environ.get("FF_FORCE") == "1"
counties = json.load(open(os.path.join(TOOLS, "counties.json")))

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
    if FORCE or not os.path.exists(agg):
        if run("collect_small.py", env): blocked.append(slug); continue
        if run("collect.py", env): blocked.append(slug + " (policies/claims 503 — rerun when API calm)"); continue
        run("nri.py", env, args=[c["geoid"], agg])
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
        "reconciliation": {"pct": recon, "pass": recon is not None and recon <= 5},
        "distinct_from_parent": "N/A — county is the base geography (no parent to dedupe against); "
                                "the 3-part test applies to sub-county ZIP pages, none published",
        "distinct_search_intent": "NOT measurable offline — requires Search Console/keyword data post-launch",
    }
    publish = crit["statistical_sufficiency"]["pass"] and crit["data_completeness"]["pass"] and crit["reconciliation"]["pass"]
    json.dump({
        "slug": slug, "label": c["label"], "geoid": c["geoid"],
        "sources": {"policies_asof": Pp.get("asof"), "retrieved": Pp.get("retrieved")},
        "policy_units": Pp.get("units"), "cohort_n": Pp.get("cohort_n"),
        "publish_criteria": crit, "publish": publish, "gate": "pass",
    }, open(os.path.join(d, "manifest.json"), "w"), indent=1)
    if not publish: blocked.append(slug + " (publish criteria not met)"); continue
    ok.append(slug)

run("build_site.py", {"FF_PLACES": PLACES, "FF_DIST": DIST, "FF_DATADIR": DATA, "FF_BASEURL": BASE})
print("\nBUILT:", ok)
if blocked: print("BLOCKED:", blocked)
