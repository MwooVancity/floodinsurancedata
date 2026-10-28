"""Turn review findings into gates: group every BLOCKER/MAJOR/MINOR line in state/reviews/hater-round*.md by defect
type, say which check covers each type, and list the types no check covers (the missing-gates list).
  python -I tools/mine_reviews.py
A type is a regex over the finding's text; 'covered' names the check id (gate.py, google_gate.py, test_truth.py,
phone_check.py) that fails on it. Unmatched findings are printed so a new type can be added."""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPES = [   # (type, pattern over the finding, covering check or None)
    ("figure differs from its data",        r"\bshows? .* but\b|does not match|mismatch|recomput", "V2"),
    ("untagged or unsourced number",         r"untagged|no source|unsourced|without a source", "V1/A1"),
    ("rule wrong or out of date",            r"\brule\b|statute|regulation|CFR|§|U\.S\.C|law\b|Citizens", "E1 + recheck (wording only)"),
    ("wrong basis or noun on a figure",      r"basis|new polic|existing polic|premium only|fees included|per policy|units?\b vs", "A2/A4/A6"),
    ("number words disagree with figures",   r"\bmost\b|majority|rising|\bfell\b|\bgrew\b|reassur", "B1/B2"),
    ("same text on many pages",              r"word for word|templated|boilerplate|shared (text|paragraph)|scaled", "S13"),
    ("dates disagree or stale",              r"\bdates? (disagree|mismatch)|downloaded .* vs|stale|tense|out of date|2025/2026|mixed", None),
    ("data held but not shown (dropped rows)", r"silently drops?|dropp|left out|hid(es|den)?\b|missing from|not in the (table|parish)", None),
    ("label disagrees with its column",      r"header|column|label (says|is)|labell?ed", None),
    ("sort order",                           r"\bsort|alphabetical|before .* \(case", None),
    ("grammar or number agreement",          r"grammar|ungrammatical|hyphen|\bhas\b.*should|agreement", None),
    ("constant shown as a local example",    r"placeholder|constant|e\.g\. \d", "test_truth (one phrase)"),
    ("jargon on screen",                     r"jargon|unexplained (term|code)|\bcode\b shown", "H3 (FEMA field names only)"),
    ("version or link mismatch in markup",   r"JSON-LD|v3|v2|breadcrumb|citation url", None),
    ("figure near a different-meaning figure", r"near-identical|merges? them|two .* totals|beside .* (smaller|larger)", None),
    ("checker or tool output wrong",         r"checker|lookup|search box|prints", None),
    ("chart reads wrong",                    r"chart|bar|footnote|axis", "C5/P2/P6"),
    ("competitor gap",                       r"gap vs|top result|NerdWallet|Insurify|Policygenius|MoneyGeek|Bankrate", "GAP (backlog)"),
]

rows = []
for f in sorted(glob.glob(os.path.join(ROOT, "state", "reviews", "hater-round*.md")), key=lambda p: int(re.search(r"(\d+)", os.path.basename(p)).group(1))):
    rnd = re.search(r"(\d+)", os.path.basename(f)).group(1)
    for line in open(f, encoding="utf-8"):
        m = re.match(r"\s*-\s*\*\*(BLOCKER|MAJOR|MINOR|GAP)[^*]*\*\*(.*)", line)
        if m: rows.append((rnd, m.group(1), m.group(2).strip()))

hits = {t: [] for t, _, _ in TYPES}; none = []
for rnd, sev, txt in rows:
    t = next((t for t, rx, _ in TYPES if re.search(rx, txt, re.I)), None)
    (hits[t] if t else none).append((rnd, sev, txt))
cover = {t: c for t, _, c in TYPES}
print(f"{len(rows)} findings in {len({r for r, _, _ in rows})} rounds\n")
print("UNCOVERED (no check fails on this type):")
for t, h in sorted(hits.items(), key=lambda kv: -len(kv[1])):
    if h and cover[t] is None:
        sev = {s: sum(1 for _, x, _ in h if x == s) for s in ("BLOCKER", "MAJOR", "MINOR")}
        print(f"  {len(h):3}  {t}  ({sev['BLOCKER']}B/{sev['MAJOR']}M/{sev['MINOR']}m; rounds {sorted({int(r) for r, _, _ in h})})")
        for r, s, x in h[:2]: print(f"         r{r} {s}: {x[:110]}")
print("\ncovered:")
for t, h in sorted(hits.items(), key=lambda kv: -len(kv[1])):
    if h and cover[t]: print(f"  {len(h):3}  {t}  -> {cover[t]}")
print(f"\nunmatched: {len(none)}")
for r, s, x in none[:15]: print(f"  r{r} {s}: {x[:120]}")
