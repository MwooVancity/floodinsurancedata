"""Mutation suite: every gate check is proven by reintroducing the bug it exists for (ids listed in gate.py).
Builds a real county page with the shipping build_page.py, confirms the clean page passes gate 2 (and gate 3 when
Playwright is installed), then applies each mutation and asserts the intended check id fires. Prints which ids
caught which mutation, so a check that never fires can be deleted. Run: python -I tools/test_gate.py
Edge-case DATA (not a broken page) lives in test_factory.py; both run in release.py."""
import io, json, os, re, shutil, subprocess, sys, tempfile, tokenize
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
sys.path.insert(0, T)
import metrics as MX

SLUG = "brevard-county-fl"
src_dir = os.path.join(ROOT, "data", "c", SLUG) if os.path.isdir(os.path.join(ROOT, "data", "c", SLUG)) else os.path.join(ROOT, "data", SLUG)
if not os.path.exists(os.path.join(src_dir, "agg.json")):
    print("test_gate: skipped (no data for", SLUG + ")"); sys.exit(0)
tmp = tempfile.mkdtemp(); d = os.path.join(tmp, SLUG); shutil.copytree(src_dir, d)   # named like data/<slug>, so the gate finds its extras
site = os.path.join(tmp, "site", "flood-insurance", SLUG); os.makedirs(site)
good = os.path.join(site, "index.html")
env = dict(os.environ, FF_DIR=d, OUT_HTML=good, FF_COUNTYLABEL="Brevard County, Florida", FF_COUNTYSHORT="Brevard County",
           FF_OFFICIAL="0", FF_SLUG=SLUG, FF_GEOID="12009", FF_BASEURL="https://floodinsurancedata.com",
           FF_PLACES=os.path.join(tmp, "places.json"))
r = subprocess.run([sys.executable, "-I", os.path.join(T, "build_page.py")], env=env, cwd=T, capture_output=True, text=True)
assert r.returncode == 0, "build_page failed: " + r.stderr[-600:]
PAGE = open(good, encoding="utf-8").read()
AGG = json.load(open(os.path.join(d, "agg.json")))
_P50 = re.search(r'<span data-m="cost_p50">([^<]+)</span>', PAGE).group(1)   # read from the page: a refresh moves it

def gate(html=None, agg=None):
    hp, ap = os.path.join(tmp, "m.html"), os.path.join(d, "agg.json")
    open(hp, "w", encoding="utf-8").write(PAGE if html is None else html)
    json.dump(AGG if agg is None else agg, open(ap, "w"))
    out = subprocess.run([sys.executable, "-I", os.path.join(T, "gate.py"), ap, hp, "0"], capture_output=True, text=True)
    json.dump(AGG, open(ap, "w"))
    return set(re.findall(r"\[(\w+)\]", out.stdout)), out.stdout

# every OpenFEMA field a metric uses has a recorded definition hash (else recheck cannot see FEMA change it)
_defs = json.load(open(os.path.join(T, "metric_defs.json")))
_unrec = sorted({f"{d['dataset']}.{f}" for d in MX.METRICS.values() if d["dataset"] in MX.API_VERSION
                 for f in d["fields"] if f not in (_defs.get(d["dataset"]) or {})})
assert not _unrec, f"metric fields with no recorded FEMA definition (run: python -I tools/metrics.py --refresh): {_unrec}"

# inputs: the national pull covers exactly the 51 states (Hawaii was once missing), and no module another tool
# imports runs code on import (importing collect_small once ran a Lee County collection)
import ast
from agg_raw import NAMES as _NAMES
_pull = ast.parse(open(os.path.join(T, "pull_raw.py"), encoding="utf-8").read())
_st = next(n.value for n in _pull.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "STATES")
_pulled = set(ast.literal_eval(_st.func.value).split()) if isinstance(_st, ast.Call) else set()
assert _pulled == set(_NAMES), f"pull_raw.STATES differs from the 51 names: missing {set(_NAMES) - _pulled}, extra {_pulled - set(_NAMES)}"
import datetime as _dt, extras_raw as _XR   # "last 12 months" means 12 months to the pull's as-of date, not a stale constant
from agg_raw import asof as _asof_fn   # one as-of date (data/us/asof.json, set by the pull): no script may type its own
_asof = _dt.date.fromisoformat(_asof_fn())
for _f in ("agg_raw.py", "recheck.py", "extras_raw.py", "build_counties.py", "build_site.py", "pull_raw.py"):
    assert not re.search(r"asof=\"20\d\d|ASOF = \"20\d\d|NB_FROM = \"20\d\d", open(os.path.join(T, _f), encoding="utf-8").read()), f"{_f} types an as-of date"
assert _XR.NB_FROM ==str(_asof.replace(year=_asof.year - 1) + _dt.timedelta(days=1)), \
    f"extras_raw.NB_FROM {_XR.NB_FROM} is not 12 months before pull_raw.ASOF {_asof}"
from rules_registry import RULES as _RULES   # a date a rule's source states must appear in the rule text (Citizens 2023 was left out)
for _k, _r in _RULES.items():
    for _u, _ex, _ in _r["sources"]:
        for _y in re.findall(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, (\d{4})", _ex):
            assert _y in _r["text"], f"rule {_k}: its source says {_y} ({_ex[:60]}...) but the rule text never mentions {_y}"
_imported = {a.name.split(".")[0] for f in os.listdir(T) if f.endswith(".py")
             for n in ast.walk(ast.parse(open(os.path.join(T, f), encoding="utf-8").read()))
             if isinstance(n, (ast.Import, ast.ImportFrom)) for a in (n.names if isinstance(n, ast.Import) else [ast.alias(n.module or "")])}
from agg_raw import FIPS as _FIPS   # every county file belongs to its own state (a stray LA record once overwrote Broward)
_acd = os.path.join(ROOT, "data", "all-counties")
_wrong = [f for f in (os.listdir(_acd) if os.path.isdir(_acd) else [])
          if _FIPS.get(json.load(open(os.path.join(_acd, f))).get("state")) != f[:2]]
assert not _wrong, f"{len(_wrong)} county files hold another state's records, e.g. {_wrong[:5]} (rerun agg_raw.py + extras_raw.py)"
_IO = {"print", "urlopen", "dump", "write", "makedirs", "run", "remove", "rmtree", "copytree", "system"}   # a side effect
for _mod in sorted(_imported):
    _fp = os.path.join(T, _mod + ".py")
    if not os.path.exists(_fp): continue
    for _n in ast.parse(open(_fp, encoding="utf-8").read()).body:
        if isinstance(_n, (ast.FunctionDef, ast.ClassDef)) or (isinstance(_n, ast.If) and "__main__" in ast.unparse(_n.test)): continue
        _io = [c for c in ast.walk(_n) if isinstance(c, ast.Call) and getattr(c.func, "attr", getattr(c.func, "id", "")) in _IO]
        assert not _io, f"{_mod}.py does I/O on import (line {_n.lineno}: {ast.unparse(_n)[:60]}); put it under if __name__ == '__main__'"

ids, out = gate()
assert not ids, "clean page must pass gate 2:\n" + out

def sub(old, new, count=1):
    assert old in PAGE, f"mutation anchor missing: {old[:60]}"
    return PAGE.replace(old, new, count)
def rsub(pat, rep):   # 11-08: a regex mutation that matches nothing silently tests nothing; it must change the page
    out = re.sub(pat, rep, PAGE, count=1, flags=re.S)
    assert out != PAGE, f"mutation pattern matched nothing: {pat[:60]}"
    return out
def agg_with(**kw):
    a = json.loads(json.dumps(AGG)); a["policies"].update(kw); return a
_EV = json.load(open(os.path.join(d, "extras.json")))["claims"]["events"]   # C12 mutation points the lead at the smallest row
STORM = re.search(r'<p class="src" data-src="ml_total">Source: [^.]*\.', PAGE).group()   # weather card cut 2026-10-28: the repeat-flood line carries the test
MUTATIONS = [   # (defect class from THE EVIDENCE table, what we reintroduce, expected id, page or agg)
    ("1 fee-vs-premium basis", "gap computed on policyCost", "L17", None, agg_with(gap_basis="cost")),
    ("2 prose vs numbers", "'most' asserted at 46.1%", "B1",
     sub("Both are premiums only", '<span data-claim="{&quot;word&quot;: &quot;most&quot;, &quot;cond&quot;: [&quot;share_below&quot;, &quot;&gt;&quot;, 50]}">Most</span> pay below. Both are premiums only')
     if "Both are premiums only" in PAGE else sub("(premiums only, before fees)", '(premiums only, before fees) <span data-claim="{&quot;word&quot;: &quot;most&quot;, &quot;cond&quot;: [&quot;share_below&quot;, &quot;&gt;&quot;, 50]}">Most</span> pay below.'), None),
    ("2 prose vs numbers", "free-typed 'climb toward'", "B2", sub("(premiums only, before fees)", "(premiums only, before fees). Bills climb toward it"), None),
    ("3 rows called homes", "IA records labelled homes", "A2", sub("</span> records from homes", "</span> homes"), None),
    ("4 cross-panel", "filed count called 'paid'", "C3", sub("</span> NFIP flood claims and", "</span> paid NFIP flood claims and"), None),
    ("5 rating vs percentile", "percentile without its basis", "A4", PAGE.replace("loss per dollar of building value: inland flood loss here is higher than in about", "inland flood risk is higher than in about"), None),
    ("6 attribution", "FEMA panel credited to NOAA", "A1", sub(STORM, '<p class="src" data-src="ml_total">Source: NOAA NCEI.'), None),
    ("6 attribution", "hand-typed source line", "A1", re.sub(r'<p class="src" data-src="ml_total">', '<p class="src">', PAGE, count=1), None),
    ("8 law wording", "purchase rule narrowed", "E1", sub("federally regulated or backed mortgage", "federally backed mortgage"), None),
    ("sources", "dataset listed that no panel shows", "A5", sub('<ul class="srclist">', '<ul class="srclist"><li><a href="x">FEMA OpenFEMA — Made Up</a></li>'), None),
    ("reader first", "card opens with a data dump", "F1",
     PAGE.replace('<p class="stand">', '<p class="stand">' + "This block lists every figure in the dataset before any answer is given to the reader at all. " * 2, 1), None),
    ("one figure", "same metric shows two values", "A3", sub(f'<span data-m="cost_p50">{_P50}</span>', '<span data-m="cost_p50">$1</span>'), None),
    ("meaning", "ZIP range count wrong (hater r147)", "C18", re.sub(r'(By ZIP \(the <span data-m="zip_count"[^>]*>)\d+', r"\g<1>999", PAGE, count=1), None),
    ("provenance", "record count inflated", "V2", re.sub(r'(<span data-m="records_policies"[^>]*>)[\d,]+', r"\g<1>99,999", PAGE, count=1), None),
    ("provenance", "complete download not stated", "G1", re.sub(r'<p class="prov">.*?</p>', "", PAGE, count=1, flags=re.S), None),
    ("reader text", "county shown as its code", "H1", sub("</main>", '<div id="counties"><table><tbody><tr><td>12009</td></tr></tbody></table></div></main>'), None),
    ("reader text", "points to county pages it does not link", "H2", sub('<p class="stand">', '<p class="stand">Open a county below for its own figures. '), None),
    ("reader text", "percentile code in a chart label", "H3", sub("<b>Typical</b>", "<b>p25 median</b>"), None),
    ("reader text", "effective date is the download day", "H4", re.sub(r"Data effective [A-Z][a-z]+ \d{1,2}, \d{4}; retrieved ([A-Z][a-z]+ \d{1,2}, \d{4})", r"Data effective \1; retrieved \1", PAGE, count=1), None),
    ("numbers", "hand-typed figure in a lead", "V1", sub('<p class="stand">', '<p class="stand">About 4,200 homes flooded here. '), None),
    ("numbers", "table cell differs from its data", "V2",
     re.sub(r'(<span data-m="zone_cost" data-q="X" data-p="[^"]+">)\$[\d,]+', r"\g<1>$999", PAGE), None),
    ("reader text", "share over 100%", "H6", sub('<p class="stand">', '<p class="stand">Inside the zone it is 113.1% insured. '), None),
    ("reader text", "'1 in N' disagrees with its percent", "H7", sub('<p class="stand">', '<p class="stand">About 1 in 2 homes here have flood insurance (64.9%). '), None),
    ("reader text", "storm without its year", "H5", re.sub(r"(costliest flood FEMA named here was [^<(]*?) \(\d{4}[^)]*\)", r"\1", PAGE, count=1), None),
    # these two proved legacy L6 / L12b redundant (deleted 2026-10-25); kept as regression tests of A1 / C4
    ("legacy L6", "all OpenFEMA attribution removed", "A1", PAGE.replace("This product uses the Federal Emergency Management Agency's OpenFEMA API, but is not endorsed by FEMA.", ""), None),
    ("2 numbers", "state figure beside a county tile is wrong", "V2",
     re.sub(r'(data-p="state\.data\.claims_extra\.avg_paid">)\$[\d,]+', r"\g<1>$1", PAGE, count=1) if 'data-p="state.data.claims_extra.avg_paid"' in PAGE else "anchor missing", None),
    # hater round 1 (2026-10-27) BLOCKERs, each now a check
    ("hater r1", "claims chart drawn as claim counts", "C5",
     re.sub(r'height="([\d.]+)"(?=[^>]*><title>\d{4}: [\d,]+ claims, \$[\d,]+</title>)', lambda mm: f'height="{float(mm.group(1)) * 0.5 + 3:.1f}"', PAGE, count=3), None),
    ("hater r1", "pre-2021 'other areas' CRS discount column", "C6", sub("<th>Discount</th>", "<th>Discount</th><th>Other areas</th>"), None),
    ("hater r1", "high-risk zone hidden in 'other'", "C7", re.sub(r"(<tr><td>(?:<a [^>]*>)?Zone A[^<]*?(?:</a>)?) \(high-risk\)", r"\1", PAGE, count=1), None),
    ("hater r1", "unpaid table shows only some reasons", "C8",
     re.sub(r"(<th>Reason recorded</th><th>Claims</th></tr></thead><tbody>)<tr>.*?</tr>", r"\1", PAGE, count=1, flags=re.S), None),
    ("hater r1", "a rule printed twice on the page", "E2",
     PAGE.replace("<p class='note'>Policy records keep", "<p class='note'>" + _RULES["purchase_short"]["text"] + " Policy records keep", 1), None),   # read from the registry: typed text went stale when the rule changed (11-04)
    ("edge 11-02", "count with a plural noun", "T2", sub("; other sites count other policies", "; 1 federal disasters; other sites count other policies"), None),
    ("edge 11-02", "builder note on the page", "T2", sub("; other sites count other policies", "; Next source to pull; other sites count other policies"), None),
    ("truth 11-02", "duty typed outside a sourced rule", "T1", sub("; other sites count other policies", "; your lender may limit this; other sites count other policies"), None),
    ("L19", "outside-zone claim line dropped", "L19", PAGE.replace("Of the NFIP claim dollars paid here", "Of paid dollars"), None),
    ("legacy L12b", "'other zones' row dropped", "C4", re.sub(r"<tr><td>Other[^<]*</td>.*?</tr>", "", PAGE, count=1), None),
    # hater round 5 (2026-10-27): existing stock's full-risk price sold as what a new policy costs
    ("hater r5", "existing-policy figure called a new policy's price", "A6",
     sub("; other sites count other policies", ", but a new one is priced at full risk: about "
         + re.search(r'<span data-m="frp_plus_fees">[^<]*</span>', PAGE).group() + " with fees; other sites count other policies"), None),
    # mined from hater rounds 5-9 (tools/mine_reviews.py, 2026-10-28): types no check covered
    ("mined", "flood event in the data dropped from the table", "C9",
     re.sub(r"(<th>Flood \(FEMA's name\)</th>.*?<tbody>)<tr>.*?</tr>", r"\1", PAGE, count=1, flags=re.S) if "<th>Flood (FEMA's name)</th>" in PAGE else "anchor missing", None),
    ("mined", "list not A to Z (case-sensitive sort)", "H8", sub("</main>", "<p class='note'><b>No CRS discount (2):</b> Westlake; Atlantis.</p></main>"), None),
    ("mined", "structured data names v3, links v2", "H9",
     sub("</main>", '<script type="application/ld+json">{"d": "OpenFEMA NfipPolicies v3", "u": "https://x/fima-nfip-redacted-policies-v2"}</script></main>'), None),
    ("mined", "'2 in 10 homes has'", "H11", sub('<p class="stand">', '<p class="stand">About 2 in 10 homes here has flood insurance (20.0%). '), None),
    ("round 31", "one-storm average without the typical claim", "H17",   # data where one flood paid most of the money
     re.sub(r"<p class='note'><b>Typical claim:</b>.*?</p>", "", PAGE, count=1, flags=re.S),
     dict(AGG, claims=dict(AGG["claims"], total_paid=int(1.2 * max(e.get("paid") or 0 for e in json.load(open(os.path.join(d, "extras.json")))["claims"]["events"]))))),
    ("round 16", "zone codes without plain words", "H14",
     re.sub(r'<span data-rule="zone_codes">.*?</span>', "", sub("</main>", "<table><tr><td>Zone B</td></tr></table></main>"), flags=re.S), None),
    ("round 16", "identical disaster lines", "H15", sub("</main>", "<ul><li>May 2023 — Flooding</li><li>May 2023 — Flooding</li></ul></main>"), None),
    ("round 16", "county in not-in-NFIP list without its scope", "H16",
     sub("</main>", "<p class='note'><b>Not in the NFIP (1 communities here): <span data-name>Box Butte County</span>.</b></p></main>"), None),
    # 11-08 silent drops and broken label promises (hater r97, r103)
    ("round 103", "decade dropped from the table without a word", "C10",
     re.sub(r'<tr><td><span data-m="decade"[^>]*>.*?</tr>', "", PAGE, count=1, flags=re.S), None),
    ("round 97/103", "big zone missing from the cost answer", "C11",
     rsub(r'(<a href="#zone-cost"[^>]*>.*?</span>)(?:, [^<]+<span data-m="zone_cost"[^>]*>[^<]*</span>)+', r"\1"), None),
    ("11-08 own slip", "priced zone called too few to price", "C11",
     rsub(r'(<a href="#zone-cost"[^>]*>.*?) a year \(median, single-family homes\)', r"\1 a year (median, single-family homes); Zone X, 1.0% of policy units, has too few single-family homes to price"), None),
    ("round 103", "'costliest flood' beaten by its own table", "C12",
     (lambda i, js: re.sub(rf"(costliest flood FEMA named here was.*?)extras\.claims\.events\.{i}\.paid", rf"\g<1>extras.claims.events.{min(js, key=lambda j: _EV[int(j)].get('paid') or 0)}.paid", PAGE, count=1, flags=re.S))(
         re.search(r'costliest flood FEMA named here was.*?events\.(\d+)\.paid', PAGE, re.S).group(1),
         re.findall(r'<td><span data-m="event_paid"[^>]*data-p="extras\.claims\.events\.(\d+)\.paid"', PAGE)), None),
    ("factory 11-08", "'Largest zones' not the largest (file order)", "C11", None,
     agg_with(cost_by_zone={z: dict(d, n=(1 if i < 2 else 10 ** 6)) for i, (z, d) in enumerate(AGG["policies"]["cost_by_zone"].items())})),
    ("11-08 A4 header", "table figure whose column header lacks its basis", "A4",
     sub("</main>", "<p>x</p>" * 60 + '<table><thead><tr><th>ZIP</th><th>Share</th></tr></thead><tbody><tr><td>z</td><td><span data-m="zip_share_below">5%</span></td></tr></tbody></table></main>'), None),
    ("round 109", "'no flood in the table' for a year the table lists", "C15",
     sub("</main>", "<p class='note'>Among the five costliest years, these have no flood of their own in the table above: "
         + re.search(r"\((\d{4})\)</td>", PAGE[PAGE.index("<th>Flood (FEMA"):]).group(1) + " (their totals are in the yearly chart above).</p></main>"), None),
    ("round 107", "multi-year catch-all row reads as one flood", "C12",
     sub(": many floods; FEMA's records use this name for claims in several years", ""), None),
    ("round 106", "events table not biggest first", "C12",
     re.sub(r"(<th>Flood \(FEMA's name\)</th>.*?<tbody>)(.*?)(</tbody>)", lambda mm: mm.group(1) + "".join(reversed(re.findall(r"<tr>.*?</tr>", mm.group(2), re.S))) + mm.group(3), PAGE, count=1, flags=re.S), None),
    ("round 106", "bigger catch-all labelled but not in the lead", "C12",
     (lambda h: re.sub(r"(<th>Flood \(FEMA's name\)</th>.*?<tbody>)(.*?)(</tbody>)", lambda mm: mm.group(1) + mm.group(2).replace('</td><td><span data-m="event_claims"', ' (many floods)</td><td><span data-m="event_claims"') + mm.group(3), h, count=1, flags=re.S))(
         (lambda i, js: re.sub(rf"(costliest flood FEMA named here was.*?)extras\.claims\.events\.{i}\.paid", rf"\g<1>extras.claims.events.{min(js, key=lambda j: _EV[int(j)].get('paid') or 0)}.paid", PAGE, count=1, flags=re.S))(
             re.search(r'costliest flood FEMA named here was.*?events\.(\d+)\.paid', PAGE, re.S).group(1),
             re.findall(r'<td><span data-m="event_paid"[^>]*data-p="extras\.claims\.events\.(\d+)\.paid"', PAGE))), None),
    ("round 103", "'not final' on long-settled years", "C13", re.sub(r"Totals for [^.]* are not final", "Totals for the latest two years are not final", PAGE, count=1), None),
]
table, ok = [], True
for cls, what, want, html, agg in MUTATIONS:
    assert html is None or html != PAGE, f"mutation '{what}' left the page unchanged: its pattern no longer matches the template"
    got, out = gate(html, agg)
    hit = want in got; ok &= hit
    table.append((cls, what, want, "PASS" if hit else "MISSED", ",".join(sorted(got)) or "-"))
    if not hit: print(f"MISSED {want} for '{what}':\n{out}")

# A4 positive control (11-08): the same cell under a header that names its basis must NOT fire A4
_a4ok, _ = gate(sub("</main>", "<p>x</p>" * 60 + '<table><thead><tr><th>ZIP</th><th>Premium below full-risk</th></tr></thead><tbody><tr><td>z</td><td><span data-m="zip_share_below">5%</span></td></tr></tbody></table></main>'))
table.append(("11-08 A4 header", "basis named in the column header", "no A4", "PASS" if "A4" not in _a4ok else "MISSED", ",".join(sorted(_a4ok)) or "-"))
ok &= "A4" not in _a4ok

# state-page mutations (11-08 C16): build Louisiana with the shipping template, prove the clean page passes, then break it
_LA = os.path.join(ROOT, "data", "states", "louisiana")
if os.path.exists(os.path.join(_LA, "agg.json")):
    _lo = os.path.join(tmp, "site", "flood-insurance", "louisiana", "index.html"); os.makedirs(os.path.dirname(_lo), exist_ok=True)
    _r = subprocess.run([sys.executable, "-I", os.path.join(T, "build_page.py")], cwd=T, capture_output=True, text=True,
                        env=dict(os.environ, FF_LEVEL="state", FF_DIR=_LA, OUT_HTML=_lo, FF_COUNTYLABEL="Louisiana", FF_COUNTYSHORT="Louisiana",
                                 FF_SLUG="louisiana", FF_GEOID="22", FF_OFFICIAL="0", FF_BASEURL="https://floodinsurancedata.com", FF_PLACES=os.path.join(ROOT, "places.json")))
    assert _r.returncode == 0, "state build failed: " + _r.stderr[-400:]
    _LP = open(_lo, encoding="utf-8").read()
    def _sgate(h):
        hp = os.path.join(tmp, "s.html"); open(hp, "w", encoding="utf-8").write(h)
        o = subprocess.run([sys.executable, "-I", os.path.join(T, "gate.py"), os.path.join(_LA, "agg.json"), hp, "0"], capture_output=True, text=True).stdout
        return set(re.findall(r"\[(\w+)\]", o))
    assert not _sgate(_LP), "clean Louisiana page must pass the gate"
    _got = _sgate(re.sub(r"<tr><td>No rating for this kind of flooding</td>.*?</tr>", "", _LP, count=1, flags=re.S))
    table.append(("11-08 state card", "unrated counties dropped from the risk table", "C16", "PASS" if "C16" in _got else "MISSED", ",".join(sorted(_got)) or "-"))
    ok &= "C16" in _got

# 7 chart overlay / any comparison across units raises at build time
try: MX.compare("cost_p50", "frp_median"); table.append(("7 chart overlay", "cost vs full-risk compare", "compare()", "MISSED", "-")); ok = False
except MX.UnitMismatch: table.append(("7 chart overlay", "cost vs full-risk compare", "compare()", "PASS", "UnitMismatch"))

# rule facts may only enter build_page.py through rules_registry (source lint on string literals)
RULE_FACTS = ("$250,000", "$100,000", "336-2627", "4012a", "30 days", "13 months", "61.11", "18&ndash;25")
lits = [t.string for t in tokenize.generate_tokens(io.StringIO(open(os.path.join(T, "build_page.py"), encoding="utf-8").read()).readline)
        if t.type == tokenize.STRING or getattr(tokenize, "FSTRING_MIDDLE", -1) == t.type]
leaked = [f for f in RULE_FACTS if any(f in s for s in lits)]
table.append(("8 law wording", "rule fact typed in build_page", "lint", "PASS" if not leaked else "MISSED", ",".join(leaked) or "-"))
ok &= not leaked

# 11-08, found twice: a heredoc turned "\1" and "\b" into invisible control characters inside source regexes (C11 mutation
# and the CRS label silently stopped matching). No tool file may hold a control character other than tab/newline.
_ctrl = [f for f in os.listdir(T) if f.endswith((".py", ".mjs", ".js", ".sh")) and re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", open(os.path.join(T, f), encoding="utf-8", errors="replace").read())]
assert re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "re.sub(r'(x)', r'" + chr(1) + "')") and re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", chr(8) + "(COUNTY)")   # the lint fires on both real slips
table.append(("11-08 lint", "control character in a tool file", "lint", "PASS" if not _ctrl else "MISSED", ",".join(_ctrl) or "-"))
ok &= not _ctrl
# 11-08: an unquoted ": " in a step name made refresh-data.yml unreadable to GitHub (no trigger at all); parse every workflow
try:
    import yaml
    _wd = os.path.join(ROOT, ".github", "workflows"); _yb = []
    for _f in sorted(os.listdir(_wd)) if os.path.isdir(_wd) else []:
        try: yaml.safe_load(open(os.path.join(_wd, _f), encoding="utf-8"))
        except yaml.YAMLError: _yb.append(_f)
    table.append(("11-08 lint", "workflow file GitHub cannot read", "yaml", "PASS" if not _yb else "MISSED", ",".join(_yb) or "-")); ok &= not _yb
except ImportError: table.append(("11-08 lint", "workflow file GitHub cannot read", "yaml", "SKIPPED", "pyyaml not installed"))

# gate 3 (reader on a phone) needs Playwright; CI without it skips these and says so
try:
    import playwright  # noqa: F401
    def phone(html):
        open(good, "w", encoding="utf-8").write(html)
        o = subprocess.run([sys.executable, "-I", os.path.join(T, "phone_check.py"), "--base",
                            "file:///" + os.path.join(tmp, "site").replace("\\", "/"), SLUG], capture_output=True, text=True).stdout
        return set(re.findall(r"- (P\d)", o)), o
    got, o = phone(PAGE)
    assert not got, "clean page must pass gate 3:\n" + o
    QW = re.search(r'<section class="card" id="compare">.*?</section>', PAGE, re.S).group()
    for cls, what, want, html in [
        ("9 reader", "data collapsed in <details>", "P5", re.sub(r'(<section class="card" id="required">.*?</section>)', r"<details>\1</details>", PAGE, count=1, flags=re.S)),
        ("9 reader", "quote checker moved to the end", "P4", PAGE.replace(QW, "").replace("</main>", QW + "</main>")),
        ("9 reader", "4px chart labels", "P2", PAGE.replace(".ax{fill:var(--mut);font-size:13px", ".ax{fill:var(--mut);font-size:4px")),
        ("9 reader", "faint grey text", "P7", PAGE.replace("</style></head>", "</style><style>.src{color:#b4bcc2}</style></head>", 1)),
        ("9 reader", "page wider than the phone", "P1", PAGE.replace("</main>", '<div style="width:900px">x</div></main>')),
        ("9 reader", "chart labels print over each other", "P6", PAGE.replace("</main>",
         '<svg viewBox="0 0 360 40" width="100%"><text x="100" y="20" class="ax">$1,008</text><text x="110" y="20" class="ax">$1,172</text></svg></main>'))]:
        got, o = phone(html); hit = want in got; ok &= hit
        table.append((cls, what, want, "PASS" if hit else "MISSED", ",".join(sorted(got)) or "-"))
    open(good, "w", encoding="utf-8").write(PAGE)
except ImportError:   # in the cloud a missing browser fails (the 2026-10-28 daily run passed with phone checks skipped)
    ok &= not os.environ.get("CI")
    table.append(("9 reader", "phone checks", "P1-P5", "SKIPPED" if ok else "MISSING", "playwright not installed"))

w = max(len(x[1]) for x in table)
print(f"{'defect class':<22} {'mutation':<{w}} {'expect':<9} {'result':<8} ids fired")
for cls, what, want, res, got in table: print(f"{cls:<22} {what:<{w}} {want:<9} {res:<8} {got}")
shutil.rmtree(tmp, ignore_errors=True)
assert ok, "a mutation was not caught"
print("test_gate: every mutation caught")
