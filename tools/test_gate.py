"""Mutation suite: every gate check is proven by reintroducing the bug it exists for (docs/GATE-PROMPT.md).
Builds a real county page with the shipping build_page.py, confirms the clean page passes gate 2 (and gate 3 when
Playwright is installed), then applies each mutation and asserts the intended check id fires. Prints which ids
caught which mutation, so a check that never fires can be deleted. Run: python -I tools/test_gate.py"""
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
def agg_with(**kw):
    a = json.loads(json.dumps(AGG)); a["policies"].update(kw); return a
STORM = re.search(r'<p class="src" data-src="storm_events,storm_damage">Source: [^.]*\.', PAGE).group()
MUTATIONS = [   # (defect class from THE EVIDENCE table, what we reintroduce, expected id, page or agg)
    ("1 fee-vs-premium basis", "gap computed on policyCost", "L17", None, agg_with(gap_basis="cost")),
    ("2 prose vs numbers", "'most' asserted at 46.1%", "B1",
     sub("Both are premiums only", '<span data-claim="{&quot;word&quot;: &quot;most&quot;, &quot;cond&quot;: [&quot;share_below&quot;, &quot;&gt;&quot;, 50]}">Most</span> pay below. Both are premiums only')
     if "Both are premiums only" in PAGE else sub("(premiums only, before fees)", '(premiums only, before fees) <span data-claim="{&quot;word&quot;: &quot;most&quot;, &quot;cond&quot;: [&quot;share_below&quot;, &quot;&gt;&quot;, 50]}">Most</span> pay below.'), None),
    ("2 prose vs numbers", "free-typed 'climb toward'", "B2", sub("(premiums only, before fees)", "(premiums only, before fees). Bills climb toward it"), None),
    ("3 rows called homes", "IA records labelled homes", "A2", sub("</span> flood-damage applications", "</span> homes"), None),
    ("4 cross-panel", "filed count called 'paid'", "C3", sub("</span> NFIP flood claims and", "</span> paid NFIP flood claims and"), None),
    ("5 rating vs percentile", "percentile without its basis", "A4", PAGE.replace("expected annual flood loss above about", "higher flood risk than about"), None),
    ("6 attribution", "NOAA panel credited to FEMA", "A1", sub(STORM, '<p class="src" data-src="storm_events,storm_damage">Source: FEMA OpenFEMA.'), None),
    ("6 attribution", "hand-typed source line", "A1", re.sub(r'<p class="src" data-src="ml_total">', '<p class="src">', PAGE, count=1), None),
    ("8 law wording", "purchase rule narrowed", "E1", sub("federally regulated lender, or federal", "federally backed lender, or federal"), None),
    ("sources", "dataset listed that no panel shows", "A5", sub('<ul class="srclist">', '<ul class="srclist"><li><a href="x">FEMA OpenFEMA — Made Up</a></li>'), None),
    ("reader first", "card opens with a data dump", "F1",
     PAGE.replace('<p class="stand">', '<p class="stand">' + "This block lists every figure in the dataset before any answer is given to the reader at all. " * 2, 1), None),
    ("one figure", "same metric shows two values", "A3", sub('<span data-m="cost_p50">$865</span>', '<span data-m="cost_p50">$856</span>'), None),
    ("provenance", "record count inflated", "V2", re.sub(r'(<span data-m="records_policies"[^>]*>)[\d,]+', r"\g<1>99,999", PAGE, count=1), None),
    ("provenance", "complete download not stated", "G1", re.sub(r'<p class="prov">.*?</p>', "", PAGE, count=1, flags=re.S), None),
    ("reader text", "county shown as its code", "H1", sub("</main>", '<div id="counties"><table><tbody><tr><td>12009</td></tr></tbody></table></div></main>'), None),
    ("reader text", "points to county pages it does not link", "H2", sub('<p class="stand">', '<p class="stand">Open a county below for its own figures. '), None),
    ("reader text", "percentile code in a chart label", "H3", sub("<b>Typical</b>", "<b>p25 median</b>"), None),
    ("reader text", "effective date is the download day", "H4", re.sub(r"Data effective July 31, 2026; retrieved ([A-Z][a-z]+ \d{1,2}, \d{4})", r"Data effective \1; retrieved \1", PAGE, count=1), None),
    ("numbers", "hand-typed figure in a lead", "V1", sub('<p class="stand">', '<p class="stand">About 4,200 homes flooded here. '), None),
    ("numbers", "table cell differs from its data", "V2",
     re.sub(r'(<span data-m="zone_cost" data-q="X" data-p="[^"]+">)\$[\d,]+', r"\g<1>$999", PAGE), None),
    ("reader text", "share over 100%", "H6", sub('<p class="stand">', '<p class="stand">Inside the zone it is 113.1% insured. '), None),
    ("reader text", "'1 in N' disagrees with its percent", "H7", sub('<p class="stand">', '<p class="stand">About 1 in 2 homes here have flood insurance (64.9%). '), None),
    ("reader text", "storm without its year", "H5", re.sub(r"(costliest single flood here was [^<(]*?) \(\d{4}[^)]*\)", r"\1", PAGE, count=1), None),
    # these two proved legacy L6 / L12b redundant (deleted 2026-10-25); kept as regression tests of A1 / C4
    ("legacy L6", "all OpenFEMA attribution removed", "A1", PAGE.replace("This product uses the Federal Emergency Management Agency's OpenFEMA API, but is not endorsed by FEMA.", ""), None),
    ("2 numbers", "state figure beside a county tile is wrong", "V2",
     re.sub(r'(data-p="state\.data\.claims_extra\.avg_paid">)\$[\d,]+', r"\g<1>$1", PAGE, count=1) if 'data-p="state.data.claims_extra.avg_paid"' in PAGE else "anchor missing", None),
    ("legacy L12b", "'other zones' row dropped", "C4", re.sub(r"<tr><td>Other or unclassified zones</td>.*?</tr>", "", PAGE, count=1), None),
]
table, ok = [], True
for cls, what, want, html, agg in MUTATIONS:
    got, out = gate(html, agg)
    hit = want in got; ok &= hit
    table.append((cls, what, want, "PASS" if hit else "MISSED", ",".join(sorted(got)) or "-"))
    if not hit: print(f"MISSED {want} for '{what}':\n{out}")

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
        ("9 reader", "page wider than the phone", "P1", PAGE.replace("</main>", '<div style="width:900px">x</div></main>')),
        ("9 reader", "chart labels print over each other", "P6", PAGE.replace("</main>",
         '<svg viewBox="0 0 360 40" width="100%"><text x="100" y="20" class="ax">$1,008</text><text x="110" y="20" class="ax">$1,172</text></svg></main>'))]:
        got, o = phone(html); hit = want in got; ok &= hit
        table.append((cls, what, want, "PASS" if hit else "MISSED", ",".join(sorted(got)) or "-"))
    open(good, "w", encoding="utf-8").write(PAGE)
except ImportError:
    table.append(("9 reader", "phone checks", "P1-P5", "SKIPPED", "playwright not installed"))

w = max(len(x[1]) for x in table)
print(f"{'defect class':<22} {'mutation':<{w}} {'expect':<9} {'result':<8} ids fired")
for cls, what, want, res, got in table: print(f"{cls:<22} {what:<{w}} {want:<9} {res:<8} {got}")
shutil.rmtree(tmp, ignore_errors=True)
assert ok, "a mutation was not caught"
print("test_gate: every mutation caught")
