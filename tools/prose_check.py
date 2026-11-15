"""Site-wide writing gate (owner 11-15: "write for a person, not a machine reading to a machine"), run on every built page.
A page fails for: a prose paragraph printed twice; the same 8-word run more than 3 times in its prose; a prose sentence over
45 words; a doubled word ("the the"); "on <date> on". Prose = <p> text outside tables, lists, forms, nav, quotes and rule()
text (data-rule), source lines (p.src/.prov); quoted words inside a sentence do not count toward its length.
Ratchet: today's failures are state/prose-baseline.json; a page fails only when its count grows past its baseline, or (a
page not in the baseline) past the largest count of a baseline page of its type, so the daily county publish is not
stopped by text every county already has. --record lowers the baseline (never raises an old page); release.py --ship runs it.
Usage: python -I tools/prose_check.py [--record] [--root dist] | --test
Edge cases:
- Table cells or list items joined into one "sentence" (sameness.py 11-11): block tags end a block; only <p> is prose. Test: long_li.
- A rule() quote or FEMA quote over 45 words: data-rule/blockquote/q/code text is skipped, "..." inside a sentence not counted. Test: quoted.
- One repeated sentence makes many overlapping 8-word runs: reported once per run. Test: run4 counts 1.
- Abbreviations (U.S., e.g.) split a sentence: an undercount (a miss), never a false fail.
- First run, no baseline: every failing page is new and its type has no ceiling, so it fails: --record writes it first. Test: ratchet.
- A new county inheriting template text: allowed up to its type's largest baseline count. Test: ratchet new_ok.
- Scale: 2,000 pages x ~110 KB through html.parser, one pass each (~0.03 s a page)."""
import json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "state", "prose-baseline.json")
MAXW, RUN, RUNMAX = 45, 8, 3
BLOCK = {"p", "div", "li", "td", "th", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "main", "header",
         "footer", "aside", "nav", "ul", "ol", "dl", "dt", "dd", "table", "thead", "tbody", "form", "label", "option",
         "select", "figure", "figcaption", "details", "summary", "blockquote", "pre", "body", "caption"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "area", "col", "embed", "param", "track"}
SKIP = {"script", "style", "head", "svg", "template", "noscript", "title"}
QUOTE = {"blockquote", "q", "code", "pre", "cite"}            # raw source text: no check at all
STRUCT = {"table", "ul", "ol", "dl", "form", "nav", "select", "figcaption", "caption"}   # not prose; doubled words still checked
QCLASS = {"src", "prov", "srclist"}                           # source lines: names and dates, not sentences
MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?"
DATE_ON = re.compile(r"\bon\s+(?:" + MONTH + r"\s+\d{1,2},?\s+\d{4}|" + MONTH + r"\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\s+on\b", re.I)
DOUBLE = re.compile(r"\b([A-Za-z]+)\s+\1\b", re.I)
INQUOTE = re.compile(r"\u201c[^\u201d]*\u201d|\"[^\"]*\"")

class Walk(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skip, self.cur, self.blocks = [], 0, [], []   # blocks: (prose text, all checkable text)
    def _flags(self):
        q = any(f == "q" for _, f in self.stack); s = q or any(f == "s" for _, f in self.stack)
        top = next((t for t, _ in reversed(self.stack) if t in BLOCK), "")
        return q, s, top
    def flush(self):
        if self.cur:
            prose = " ".join(t for t, p, _ in self.cur if p).split(); chk = " ".join(t for t, _, c in self.cur if c).split()
            if prose or chk: self.blocks.append((" ".join(prose), " ".join(chk)))
        self.cur = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if tag == "br": self.flush()
            return
        if self.skip or tag in SKIP:
            self.skip += 1; return
        a = dict(attrs); cls = set((a.get("class") or "").split())
        f = "q" if tag in QUOTE or "data-rule" in a or cls & QCLASS else "s" if tag in STRUCT else ""
        if tag in BLOCK: self.flush()
        self.stack.append((tag, f))
    def handle_endtag(self, tag):
        if tag in VOID: return   # <img/> calls this too: it must not end a skip
        if self.skip:
            self.skip -= 1; return
        if tag in VOID or not any(t == tag for t, _ in self.stack): return
        if tag in BLOCK: self.flush()
        while self.stack:
            t, _ = self.stack.pop()
            if t == tag: break
        if tag in BLOCK: self.flush()
    def handle_data(self, d):
        if self.skip or not d.strip(): return
        q, s, top = self._flags()
        self.cur.append((d, top == "p" and not s, not q))

def findings(html):
    w = Walk(); w.feed(html); w.close(); w.flush()
    out, prose = [], [p for p, _ in w.blocks if p]
    seen = {}
    for p in prose:
        k = re.sub(r"\W+", " ", p.lower()).strip()
        if len(k.split()) >= 4: seen[k] = seen.get(k, 0) + 1
    out += [f"paragraph x{n}: {k[:80]}" for k, n in seen.items() if n > 1]
    grams = {}
    blocks_w = [[re.sub(r"[^\w$%'-]", "", x.lower()) for x in p.split()] for p in prose]
    blocks_w = [[x for x in b if x] for b in blocks_w]
    for b in blocks_w:
        for i in range(len(b) - RUN + 1): g = " ".join(b[i:i + RUN]); grams[g] = grams.get(g, 0) + 1
    hot, rep = {g for g, n in grams.items() if n > RUNMAX}, set()
    for b in blocks_w:   # ponytail: one report per run (first hot gram of a stretch), not one per overlapping gram
        i = 0
        while i <= len(b) - RUN:
            g = " ".join(b[i:i + RUN])
            if g in hot:
                rep.add(g); i += RUN
                while i <= len(b) - RUN and " ".join(b[i - RUN + 1:i + 1]) in hot: i += 1
            else: i += 1
    out += [f"8-word run x{grams[g]}: {g}" for g in sorted(rep)]
    for p in prose:
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9$(\u201c\"])", p):
            n = len(INQUOTE.sub(" ", s).split())
            # 4+ semicolons = a list of names printed inline (communities), not a sentence
            if n > MAXW and s.count(";") < 4: out.append(f"sentence {n} words: {s[:80]}")
    for _, c in w.blocks:
        out += [f"doubled word: {m.group(0)}" for m in DOUBLE.finditer(c)]
        out += [f"date doubled: {m.group(0)}" for m in DATE_ON.finditer(c)]
    return out

def kind(rel, states):   # page type for a new page's ceiling
    parts = rel.split("/")
    if rel == "index.html": return "home"
    if parts[0] == "flood-insurance" and len(parts) == 3:
        return "state" if parts[1] in states else "county" if os.path.isdir(os.path.join(ROOT, "data", "c", parts[1])) else "flood-insurance/" + parts[1]
    return parts[0]

def judge(counts, base, kinds):   # list of page failures under the ratchet
    ceil = {}
    for p, n in base.items(): ceil[kinds.get(p, "")] = max(ceil.get(kinds.get(p, ""), 0), n)
    bad = []
    for p, n in counts.items():
        lim = base[p] if p in base else ceil.get(kinds.get(p), 0)
        if n > lim: bad.append(f"{p}: {n} writing faults, allowed {lim} ({'its baseline' if p in base else 'new page, largest of its type'})")
    return bad

def lower(counts, base):   # --record: an old page never rises; a page at 0 stays listed at 0 (else it would get its type's ceiling)
    return {p: (min(n, base[p]) if p in base else n) for p, n in counts.items()}

def scan(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(d, f), root).replace("\\", "/")
                out[rel] = findings(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())
    return out

def test():
    P = lambda *b: "<html><head><title>t t</title></head><body>" + "".join(b) + "</body></html>"
    s46 = " ".join(f"w{i}" for i in range(45)) + " end."
    assert findings(P("<p>" + s46 + "</p>"))[0].startswith("sentence 46"), "46-word sentence not caught"
    assert not findings(P("<p>" + " ".join(f"w{i}" for i in range(44)) + " end.</p>")), "45 words falsely caught"
    assert not [f for f in findings(P("<ul><li>" + s46 + "</li></ul>")) if f.startswith("sentence")], "long_li: a list item is not prose"
    assert not [f for f in findings(P("<table><tr><td>" + s46 + "</td></tr></table>")) if f.startswith("sentence")]
    assert not findings(P('<p>FEMA says <span data-rule="x">' + s46 + "</span></p>")), "rule() text counted"
    assert not [f for f in findings(P("<p>FEMA writes \u201c" + " ".join(f"q{i}" for i in range(50)) + "\u201d here.</p>")) if f.startswith("sentence")], "quoted: words in quotes counted"
    assert not findings(P('<noscript><img src="x"/><p>' + s46 + "</p></noscript>")), "a self-closed void tag ended the skip of noscript text"
    assert lower({"a": 0, "b": 3, "n": 2}, {"a": 1, "b": 2}) == {"a": 0, "b": 2, "n": 2}, "a page fixed to 0 keeps 0 as its ceiling"
    assert judge({"a": 1}, lower({"a": 0}, {"a": 1}) | {"z": 4}, {"a": "county", "z": "county"}), "zero ratchet holds"
    para = "<p>These claims were closed without any payment at all.</p>"
    assert any(f.startswith("paragraph x2") for f in findings(P(para, para))), "repeated paragraph not caught"
    assert not [f for f in findings(P(para)) if f.startswith("paragraph")]
    run = "the median premium for a home in this county is"
    r4 = findings(P(*[f"<p>Part {i}: {run} shown here.</p>" for i in range(4)]))
    assert len([f for f in r4 if f.startswith("8-word")]) == 1, f"run4: one run, one report {r4}"
    assert not [f for f in findings(P(*[f"<p>Part {i}: {run} shown here.</p>" for i in range(3)])) if f.startswith("8-word")], "3 repeats allowed"
    assert not [f for f in findings(P(*[f"<table><tr><td>{run} {i}</td></tr></table>" for i in range(5)])) if f.startswith("8-word")], "tables exempt"
    assert any(f.startswith("doubled word: the the") for f in findings(P("<p>Read the the page.</p>")))
    assert any(f.startswith("doubled word") for f in findings(P("<table><tr><td>flood flood</td></tr></table>"))), "typo in a table cell"
    assert not findings(P("<table><tr><td>AE</td><td>AE</td></tr></table>")), "two cells are not a doubled word"
    assert not findings(P("<blockquote>that that</blockquote>")), "a source quote stays verbatim"
    assert any(f.startswith("date doubled") for f in findings(P("<p>Updated on August 31, 2026 on FEMA's file.</p>")))
    assert not findings(P("<p>Updated on August 31, 2026 from FEMA's file.</p>"))
    assert findings("") == [] and findings("<p>unclosed") == []
    k = {"a": "county", "b": "county", "n": "county", "g": "guides"}
    assert judge({"a": 2, "b": 0}, {"a": 2, "b": 1}, k) == [], "shrink passes"
    assert judge({"a": 3}, {"a": 2}, k), "ratchet: a grown count fails"
    assert judge({"n": 2}, {"a": 2}, k) == [], "new_ok: a new county up to its type's largest"
    assert judge({"n": 3}, {"a": 2}, k), "new county over its type fails"
    assert judge({"g": 1}, {"a": 2}, k), "new type with no baseline: any fault fails"
    assert judge({"g": 0}, {}, k) == []
    print("prose_check --test: 27 cases PASS")

if __name__ == "__main__":
    if "--test" in sys.argv: test(); sys.exit()
    root = sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else os.path.join(ROOT, "dist")
    res = scan(root); counts = {p: len(v) for p, v in res.items()}
    try: base = json.load(open(BASE, encoding="utf-8"))
    except (OSError, ValueError): base = {}
    states = {s["slug"] for s in json.load(open(os.path.join(ROOT, "data", "states", "built.json")))}
    kinds = {p: kind(p, states) for p in set(counts) | set(base)}
    tot = sum(counts.values())
    print(f"prose check: {len(res)} pages, {tot} writing faults on {sum(1 for n in counts.values() if n)} pages (baseline {sum(base.values())})")
    for p in sorted(res, key=lambda p: -counts[p])[:5]:
        if counts[p]: print(f"  {p}: {counts[p]}; e.g. {res[p][0][:110]}")
    if "--record" in sys.argv:   # lower only: an old page never gets a higher allowance; a page gone from dist is dropped
        new = lower(counts, base)
        json.dump(dict(sorted(new.items())), open(BASE, "w", encoding="utf-8"), indent=0)
        sys.exit(print(f"baseline recorded: {sum(new.values())} faults on {len(new)} pages"))
    bad = judge(counts, base, kinds)
    for b in bad[:20]: print("  FAIL", b, "|", "; ".join(x[:70] for x in res[b.split(":")[0]][:3]))
    print("PROSE " + ("FAIL" if bad else "OK"))
    sys.exit(1 if bad else 0)
