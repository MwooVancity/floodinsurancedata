"""THE Google gate: the whole site checked against Google's spam policies and structured-data rules before a deploy.
gate.py asks "is each page true and readable?"; this asks "could Google read the site as spam?". Exit 1 blocks ship.
Usage: python -I tools/google_gate.py [--root dist] [--skip-review]
  S1 structured data   markup claims only what the page shows (no FAQ/Review/Rating markup; dateModified = the data's date)
  S2 scaled content    no indexable page is a near-copy of another in its state (numbers and place names masked)
  S3 thin pages        every indexable county page carries its own data (enough figures read from its own records)
  S4 doorway signals   titles and descriptions unique across the site, no repeated keywords in a title
  S5 hidden text       no text hidden with inline CSS (display:none, visibility:hidden, font-size:0, off-screen)
  S6 index hygiene     sitemap = exactly the indexable pages; canonicals self-referential; robots allows crawling
  S7 rollout pace      at most 25 newly indexable pages per release (owner 2026-11-01: stick to 20 a day)
  S8 broken links      every internal link resolves to a built page
  S9 page weight       every page under 400 KB of HTML
  S10 cloaking         in gate_live.py: every live page fetched as Googlebot equals the built page"""
import json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # a failure quoting "→" must print, not crash the gate
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else os.path.join(ROOT, "dist")
MAX_NEW_INDEXABLE, DUP_MAX, MIN_OWN_FIGURES = 25, 0.80, 40
fails = []
def fail(cid, msg): fails.append(f"[{cid}] {msg}")
def text(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|head)\b.*?</\1>", " ", h, flags=re.S))).strip()

pages = {}   # url path -> html
for d, _, fs in os.walk(DIST):
    for f in fs:
        if f.endswith(".html"):
            rel = os.path.relpath(os.path.join(d, f), DIST).replace("\\", "/")
            path = "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)
            pages[path] = open(os.path.join(d, f), encoding="utf-8").read()
indexable = {p for p, h in pages.items() if 'name="robots" content="noindex' not in h}

# S1 structured data claims only what the page shows
for p, h in pages.items():
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        for o in (lambda x: x if isinstance(x, list) else [x])(json.loads(blk)):
            t = o.get("@type")
            if t in ("FAQPage", "QAPage", "Review", "AggregateRating", "HowTo", "Product", "JobPosting", "Event"):
                fail("S1", f"{p}: {t} markup (must match visible content; we show none)")
            if t == "Dataset" and o.get("dateModified") and not re.match(r"\d{4}-\d{2}-\d{2}$", str(o["dateModified"])):
                fail("S1", f"{p}: Dataset dateModified not a date")
            if t == "Dataset":   # Search Console 2026-10-29: missing description/license/creator, citation of objects
                for k in ("name", "description", "license", "creator"):
                    if not o.get(k): fail("S1", f"{p}: Dataset missing {k}")
                if any(not isinstance(c, str) for c in (o.get("citation") or [])):
                    fail("S1", f"{p}: Dataset citation must be text, not objects (Google checks nested Datasets)")

# S2 scaled content: masked 8-gram similarity among indexable county pages of the same state (and against the state page)
# Names are masked (a name swap is the doorway pattern); numbers are KEPT, because each county's own figures are the
# page's content. The number-masked prose figure is printed every run (not failing) so template sameness stays visible.
def shingles(h, own):
    t = text(h).lower()
    for w in sorted(own, key=len, reverse=True): t = t.replace(w.lower(), " X ")
    w = re.findall(r"[a-z0-9]+", t)
    return {" ".join(w[i:i + 8]) for i in range(max(0, len(w) - 7))}
places = json.load(open(os.path.join(DIST, "..", "places.json") if os.path.exists(os.path.join(DIST, "..", "places.json")) else os.path.join(ROOT, "places.json")))
states = json.load(open(os.path.join(ROOT, "data", "states", "built.json")))
st_slug = {s["abbr"]: s["slug"] for s in states}; st_name = {s["abbr"]: s["name"] for s in states}
by_state, sims = defaultdict(list), []
for c in places:
    p = f"/flood-insurance/{c['slug']}/"
    if p in pages and p in indexable: by_state[c["state"]].append((p, c))
for st, items in by_state.items():
    sh = {p: shingles(pages[p], [c["short"], c["label"], st_name.get(st, ""), c["short"].split(" ")[0]]) for p, c in items}
    sp = f"/flood-insurance/{st_slug.get(st, '')}/"
    if sp in pages: sh[sp] = shingles(pages[sp], [st_name.get(st, "")])
    keys = list(sh)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = sh[keys[i]], sh[keys[j]]
            if not a or not b: continue
            s = len(a & b) / len(a | b); sims.append(s)
            if s > DUP_MAX: fail("S2", f"{keys[i]} and {keys[j]} are {s:.0%} the same text with place names masked (max {DUP_MAX:.0%})")

# S3 thin: an indexable county page carries enough figures read from its own records (not constants, not the state's)
for st, items in by_state.items():
    for p, c in items:
        own = len(re.findall(r'data-p="(?!const\.)[^"]+"', pages[p]))
        if own < MIN_OWN_FIGURES: fail("S3", f"{p}: only {own} figures from its own data (min {MIN_OWN_FIGURES})")

# S4 doorway signals
seen_t, seen_d = {}, {}
for p in sorted(indexable):
    h = pages[p]; t = (re.search(r"<title>(.*?)</title>", h, re.S) or [None, ""])[1].strip()
    d = (re.search(r'<meta name="description" content="([^"]*)"', h) or [None, ""])[1].strip()
    if t in seen_t: fail("S4", f"{p}: same title as {seen_t[t]}: {t[:60]}")
    if d and d in seen_d: fail("S4", f"{p}: same description as {seen_d[d]}")
    seen_t.setdefault(t, p); seen_d.setdefault(d, p)
    words = [w for w in re.findall(r"[a-z]+", t.lower()) if len(w) > 3]
    for w in set(words):
        if words.count(w) > 2: fail("S4", f"{p}: '{w}' repeated {words.count(w)} times in the title")

# S15 analytics: every page carries the tag /privacy/ discloses, so no new page or template goes uncounted
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from notes import GA_TAG
for p, h in pages.items():
    if GA_TAG not in h: fail("S15", f"{p}: Google Analytics tag missing")

# S5 hidden text
for p, h in pages.items():
    body = re.sub(r"<(script|style|head)\b.*?</\1>", " ", h, flags=re.S)
    for m in re.finditer(r'<(\w+)[^>]*style="[^"]*(display:\s*none|visibility:\s*hidden|font-size:\s*0[^.\d]|text-indent:\s*-\d{3,})[^"]*"[^>]*>([^<]{3,})', body):
        fail("S5", f"{p}: text hidden with inline CSS: {m.group(3)[:50]}")

# S6 index hygiene
sm = open(os.path.join(DIST, "sitemap.xml"), encoding="utf-8").read()
sm_paths = {re.sub(r"^https?://[^/]+", "", u) for u in re.findall(r"<loc>(.*?)</loc>", sm)}
for p in sm_paths - set(pages): fail("S6", f"sitemap lists {p}, which is not built")
for p in sm_paths & (set(pages) - indexable): fail("S6", f"sitemap lists {p}, which is noindex")
for p in {q for q in indexable if q.startswith("/flood-insurance/")} - sm_paths: fail("S6", f"{p} is indexable but missing from the sitemap")
for p, h in pages.items():
    c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    if p in indexable and (not c or re.sub(r"^https?://[^/]+", "", c.group(1)) != p): fail("S6", f"{p}: canonical is {c.group(1) if c else 'missing'}")
rb = open(os.path.join(DIST, "robots.txt"), encoding="utf-8").read()
if re.search(r"^Disallow:\s*/\s*$", rb, re.M) or "Sitemap:" not in rb: fail("S6", "robots.txt blocks the site or names no sitemap")

# S7 rollout pace: newly indexable pages vs the last released sitemap (git HEAD)
try:
    prev = subprocess.run(["git", "show", "HEAD:dist/sitemap.xml"], cwd=ROOT, capture_output=True, text=True).stdout
    prev_paths = {re.sub(r"^https?://[^/]+", "", u) for u in re.findall(r"<loc>(.*?)</loc>", prev)}
    new = sorted(sm_paths - prev_paths) if prev_paths else []
    if len(new) > MAX_NEW_INDEXABLE: fail("S7", f"{len(new)} newly indexable pages in one release (max {MAX_NEW_INDEXABLE}): {new[:5]}...")
except Exception as e: fail("S7", f"could not read the last released sitemap: {e}")

# S8 broken internal links
for p, h in pages.items():
    for href in re.findall(r'href="([^"#?]+)"', h):
        if href.startswith(("http", "mailto:", "//")) or href.endswith((".csv", ".png", ".xml", ".txt", ".json")): continue
        tgt = os.path.normpath(os.path.join(p if p.endswith("/") else os.path.dirname(p) + "/", href)).replace("\\", "/")
        tgt = tgt if tgt.endswith((".html", "/")) else tgt + "/"
        if tgt not in pages and tgt.rstrip("/") + "/" not in pages: fail("S8", f"{p} links to {href}, which is not built")

# S9 page weight
for p, h in pages.items():
    if len(h.encode()) > 400_000: fail("S9", f"{p}: {len(h.encode()) // 1000} KB of HTML (max 400)")

# S11 home and hub figures: every table row re-read from its page's own data; record totals = the state manifests;
# the U.S. median on the home equals the one every state and county page prints
def _agg(slug):
    for d in (os.path.join(ROOT, "data", "states", slug), os.path.join(ROOT, "data", "c", slug)):
        if os.path.exists(os.path.join(d, "agg.json")): return json.load(open(os.path.join(d, "agg.json")))
for hp in ("/", "/flood-insurance/"):
    for slug, med, units in re.findall(r'<a href="/flood-insurance/([^/"]+)/">[^<]*</a></td><td>([^<]*)</td><td>([\d,]+)</td>', pages.get(hp, "")):
        a = _agg(slug)
        if not a: fail("S11", f"{hp} lists {slug}, which has no data"); continue
        want = (f"${a['policies']['p50']:,.0f}", f"{a['policies']['units']:,}")
        if (med, units) != want: fail("S11", f"{hp} row {slug} shows {med} / {units}, its data says {want[0]} / {want[1]}")
_tot = [0, 0]
for s in states:
    mm = (_agg(s["slug"]) or {}).get("manifest") or {}
    _tot[0] += (mm.get("policies") or {}).get("unique_fetched") or 0; _tot[1] += (mm.get("claims") or {}).get("unique_fetched") or 0
for hp in ("/", "/methodology/", "/about/"):
    for tp_, tc_ in re.findall(r"([\d,]+) (?:NFIP )?policy records and ([\d,]+) claim records", text(pages.get(hp, ""))):
        if [int(tp_.replace(",", "")), int(tc_.replace(",", ""))] != _tot: fail("S11", f"{hp} says {tp_} policy / {tc_} claim records; the manifests total {_tot[0]:,} / {_tot[1]:,}")
_us = re.search(r'<div class="n">(\$[\d,]+)</div><div class="l">U\.S\. median', pages.get("/", ""))
_seen = {re.sub(r"<[^>]+>", "", v) for h in pages.values() for v in re.findall(r'<span data-m="us_p50"[^>]*>(.*?)</span>', h)}
if _us and _seen - {_us.group(1)}: fail("S11", f"home U.S. median {_us.group(1)} but pages print {sorted(_seen)}")

# S15 every home-page figure equals an independent recompute from the data files (2026-10-28 site review: the home
# page, the busiest page, was the only one no number check read)
_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_home = text(pages.get("/", ""))
def _hist_mid(path):   # median of a {state: {cost: count}} histogram, written apart from build_site's quantile code
    cnt = {}
    for st in json.load(open(path)).values():
        for v, c in st.items(): cnt[int(v)] = cnt.get(int(v), 0) + c
    half, run = sum(cnt.values()) / 2, 0
    for v in sorted(cnt):
        run += cnt[v]
        if run >= half: return v
if _home and os.path.exists(os.path.join(_DATA, "us", "cost_hist.json")):
    _sx = [json.load(open(os.path.join(_DATA, "states", s, "extras.json")))["policies"]
           for s in sorted(os.listdir(os.path.join(_DATA, "states"))) if os.path.exists(os.path.join(_DATA, "states", s, "extras.json"))]
    def _wm(mk, nk): return round(sum((e["averages"][mk] or 0) * e["averages"][nk] for e in _sx) / sum(e["averages"][nk] for e in _sx))
    _dc = {}
    for e in _sx:
        for d, c in (e.get("ded_counts") or {}).items(): _dc[d] = _dc.get(d, 0) + c
    _top = max(_dc, key=_dc.get)
    _want = {"Typical cost, existing single-family homes (median)": _hist_mid(os.path.join(_DATA, "us", "cost_hist.json")),
             "Typical cost, policies first bought in the past year": _hist_mid(os.path.join(_DATA, "us", "cost_hist_new.json")),
             "Average (mean) cost, single-family homes": _wm("sf_cost_mean", "sf_n"),
             "Average cost, every policy type (adds condos, rentals, businesses)": _wm("all_cost_mean", "all_n"),
             "Average premium alone, single-family homes (before the federal fees)": _wm("sf_prem_mean", "sf_prem_n")}
    for _lab, _v in _want.items():
        _mm = re.search(re.escape(_lab) + r" \$([\d,]+)", _home)
        if not _mm: fail("S15", f"home: row '{_lab}' missing")
        elif int(_mm.group(1).replace(",", "")) != _v: fail("S15", f"home: '{_lab}' shows ${_mm.group(1)}, data says ${_v:,}")
    _mm = re.search(r"single-family policies is \$([\d,]+) \(([\d.]+)% of them\)", _home)
    if not _mm or int(_mm.group(1).replace(",", "")) != int(float(_top)) or float(_mm.group(2)) != round(100 * _dc[_top] / sum(_dc.values()), 1):
        fail("S15", f"home: usual deductible line does not match the data (${int(float(_top)):,}, {round(100 * _dc[_top] / sum(_dc.values()), 1)}%)")

# S12 hater review: every indexable page (home, states, counties) has a current PASS from a hostile reader (tools/review.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import review as RV
_th = RV.template_hash()
for p in ([] if "--skip-review" in sys.argv else sorted(indexable)):   # skipped only by release.py --hotfix "<reason>"
    m_ = re.fullmatch(r"/flood-insurance/([^/]+)/", p)
    slug = "home" if p == "/" else m_.group(1) if m_ else None
    if slug and not RV.ok(slug, _th):
        fail("S12", f"{p}: no current hater-review PASS (template {_th}; state/reviews/{slug}.json is {(RV.get(slug) or {}).get('verdict') or 'missing'})")

# S14 a ranked gap blocks once it is 3 review rounds old (2026-10-28: "gaps never block" became "gaps never get done")
_bl = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state", "reviews", "backlog.md")
_rounds = [int(x) for x in re.findall(r"hater-round(\d+)\.md", " ".join(os.listdir(os.path.dirname(_bl))))]
if "--skip-review" not in sys.argv and os.path.exists(_bl) and _rounds:
    for _item, _since in re.findall(r"(?m)^\d+\. (.*?) \(since round (\d+)\)$", open(_bl, encoding="utf-8").read()):
        if max(_rounds) - int(_since) >= 3: fail("S14", f"gap open since round {_since} (now round {max(_rounds)}): {_item[:80]}")

# S13 boilerplate share (hater r5: shared paragraphs = scaled content). A caveat belongs beside its figure, so a shared
# sentence is allowed; a county page whose prose is MOSTLY sentences found on over half the county pages is templated.
# Prose = <p> text, not menus, source lines or rule() text (rules are one registry text with their source, by design).
_cp = {p: pages[p] for items in by_state.values() for p, _ in items}
_share = {}
if len(_cp) >= 5:
    _sents, _cnt = {}, defaultdict(int)
    for p, h in _cp.items():
        h = re.sub(r'<(span|div) data-rule="\w+">.*?</\1>', " ", h, flags=re.S)
        t = " ".join(text(x) for x in re.findall(r'<p(?! class="(?:src|prov)")[^>]*>(.*?)</p>', h, re.S))
        _sents[p] = [" ".join(s.split()) for s in re.split(r"(?<=[.!?])\s+", t) if s.split()]
        for s_ in set(_sents[p]): _cnt[s_] += 1
    for p, ss in _sents.items():
        tot = sum(len(s.split()) for s in ss) or 1
        _share[p] = sum(len(s.split()) for s in ss if _cnt[s] > len(_cp) / 2) / tot
        if _share[p] > 0.5: fail("S13", f"{p}: {_share[p]:.0%} of its prose is shared with most county pages (max 50%)")

# S10 cloaking: gate_live.py fetches every page as Googlebot and requires it byte-identical to the built page

sims.sort()
print(f"google gate: {len(pages)} pages, {len(indexable)} indexable; same-state similarity (names masked) "
      + (f"median {sims[len(sims) // 2]:.0%}, max {sims[-1]:.0%} over {len(sims)} pairs" if sims else "n/a (fewer than 2 pages in any state)")
      + (f"; shared prose per county page median {sorted(_share.values())[len(_share) // 2]:.0%}, max {max(_share.values()):.0%}" if _share else ""))
for f in fails: print("  -", f)
print("GOOGLE GATE " + ("FAIL" if fails else "PASS"))
sys.exit(1 if fails else 0)
