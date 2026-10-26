"""Mutation suite: every gate check is proven by reintroducing the bug it exists for (docs/GATE-PROMPT.md).
Builds a real county page with the shipping build_page.py, confirms the clean page passes gate 2 (and gate 3 when
Playwright is installed), then applies each mutation and asserts the intended check id fires. Prints which ids
caught which mutation, so a check that never fires can be deleted. Run: python -I tools/test_gate.py"""
import io, json, os, re, shutil, subprocess, sys, tempfile, tokenize
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
sys.path.insert(0, T)
import metrics as MX

SLUG = "brevard-county-fl"
src_dir = os.path.join(ROOT, "data", SLUG)
if not os.path.exists(os.path.join(src_dir, "agg.json")):
    print("test_gate: skipped (no data for", SLUG + ")"); sys.exit(0)
tmp = tempfile.mkdtemp(); d = os.path.join(tmp, "d"); shutil.copytree(src_dir, d)
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
     sub("of policyholders here pay", "of policyholders here pay <span data-claim='{\"word\": \"most\", \"cond\": [\"share_below\", \">\", 50]}'>most</span>"), None),
    ("2 prose vs numbers", "free-typed 'climb toward'", "B2", sub("Both are premiums only;", "Bills climb toward it. Both are premiums only;"), None),
    ("3 rows called homes", "IA records labelled homes", "A2", sub("</span> flood-damage applications", "</span> homes"), None),
    ("4 cross-panel", "filed count called 'paid'", "C3", sub("</span> NFIP flood claims, which paid", "</span> paid NFIP flood claims, which paid"), None),
    ("5 rating vs percentile", "percentile without its basis", "A4", PAGE.replace("expected annual flood loss above about", "higher flood risk than about"), None),
    ("6 attribution", "NOAA panel credited to FEMA", "A1", sub(STORM, '<p class="src" data-src="storm_events,storm_damage">Source: FEMA OpenFEMA.'), None),
    ("6 attribution", "hand-typed source line", "A1", re.sub(r'<p class="src" data-src="ml_total">', '<p class="src">', PAGE, count=1), None),
    ("8 law wording", "purchase rule narrowed", "E1", sub("federally regulated lender, or", "federally backed lender, or"), None),
    ("sources", "dataset listed that no panel shows", "A5", sub('<ul class="srclist">', '<ul class="srclist"><li><a href="x">FEMA OpenFEMA — Made Up</a></li>'), None),
    ("one figure", "same metric shows two values", "A3", sub('<span data-m="cost_p50">$865</span>', '<span data-m="cost_p50">$856</span>'), None),
    # these two proved legacy L6 / L12b redundant (deleted 2026-10-25); kept as regression tests of A1 / C4
    ("legacy L6", "all OpenFEMA attribution removed", "A1", PAGE.replace("This product uses the Federal Emergency Management Agency's OpenFEMA API, but is not endorsed by FEMA.", ""), None),
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
        ("9 reader", "page wider than the phone", "P1", PAGE.replace("</main>", '<div style="width:900px">x</div></main>'))]:
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
