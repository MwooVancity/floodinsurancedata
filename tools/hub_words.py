"""gate.py's word rules on the pages gate.py never sees (audit 11-10): home, zone pages, claims, /nfip/, renters, ZIP,
map, methodology, about, data. Per-place pages are gated by gate.py with their own data.
  W-B3 a missing value printed as text (None, nan, undefined)
  W-T1 a law or duty typed outside a sourced rule()
  W-T2 broken count wording or a builder note
  W-E2 a sentence of 12+ words printed twice on one page
Direction and size words (gate B2) are not checked here: hub pages rank by value in tables, where "most paid first" is
the sort label, not a claim. Usage: python -I tools/hub_words.py [--test]"""
import collections, glob, html as H, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def text(h, skip_rules):
    h = re.sub(r"<(script|style|svg|head)\b.*?</\1>", " ", h, flags=re.S)
    if skip_rules: h = re.sub(r"<(h[1-3]|title)\b.*?</\1>", " ", h, flags=re.S)   # a question heading ("Must I buy?") is not a stated duty
    if skip_rules: h = re.sub(r'<(span|div|p)[^>]*data-rule="\w+"[^>]*>.*?</\1>', " ", h, flags=re.S)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

def check(h):
    bad, t, out = [], text(h, False), text(h, True)
    for m in re.finditer(r"\b(None|nan|NaN|undefined)\b(?!\s+(of|were|was|have|has|is|are)\b)", t): bad.append(f"W-B3 '{m[1]}': …{t[max(0, m.start()-40):m.end()+20]}…")
    m = re.search(r"\b(must|by law|federal law|Congress|lenders? (?:may|can)|statut\w+|grace period)\b", out)
    if m: bad.append(f"W-T1 law or duty outside rule(): …{out[max(0, m.start()-60):m.end()+40]}…")
    m = re.search(r"(?<![\d,.$])1 (?:claims|NFIP flood claims|federal disasters|counties)\b|Next source to pull|TODO|\{[a-z_]+\}", t)
    if m: bad.append(f"W-T2 broken wording: …{t[max(0, m.start()-40):m.end()+40]}…")
    c = collections.Counter(" ".join(s.split()[-12:]) for s in re.split(r"(?<=[.!?])\s+", t) if len(s.split()) >= 12)
    for s, n in c.items():
        if n > 1: bad.append(f"W-E2 sentence printed {n} times: {s[:80]}"); break
    return bad

def hubs():
    places = {p["slug"] for p in json.load(open(os.path.join(ROOT, "places.json")))}
    states = {s["slug"] for s in json.load(open(os.path.join(ROOT, "data", "states", "built.json")))}
    for f in sorted(glob.glob(os.path.join(ROOT, "dist", "**", "index.html"), recursive=True)):
        slug = os.path.basename(os.path.dirname(f))
        if os.path.basename(os.path.dirname(os.path.dirname(f))) == "flood-insurance" and slug in places | states: continue
        yield f

if __name__ == "__main__":
    if "--test" in sys.argv:
        ok = "<p>Claims paid on time.</p><span data-rule='x'></span>"
        assert not check(ok), check(ok)
        for k, h in {"B3": "<p>Median None a year.</p>", "T1": "<p>Your lender may... lenders may require it.</p>", "T2": "<p>1 claims filed.</p>",
                     "E2": "<p>" + "This exact sentence has more than twelve words in it so it counts here. " * 2 + "</p>"}.items():
            assert any(b.startswith("W-" + k) for b in check(h)), f"mutation not caught: {k}"
        assert not check('<p data-rule="lender">Lenders may require it.</p>'), "a sourced rule is not typed law"
        print("hub_words mutations: 4 caught"); sys.exit()
    bad = [f"{os.path.relpath(f, ROOT)}: {b}" for f in hubs() for b in check(open(f, encoding="utf-8").read())]
    for b in bad: print("  -", b)
    print("HUB WORDS", "FAIL" if bad else "PASS", f"({sum(1 for _ in hubs())} pages)"); sys.exit(1 if bad else 0)
