"""The hater gate's mechanical half. The judging half is a fresh agent running docs/HATER-PROMPT.md.
  python -I tools/hater.py prep <round> <slug> [<slug> ...] [--local]   phone screenshots of the LIVE pages (or of dist/) + the filled brief
  python -I tools/hater.py record <round>                     read the review, write state/reviews/<slug>.json
A slug is "home", a state slug or a county slug. record writes PASS only for a section ending "Verdict: PASS" with
no BLOCKER or MAJOR in it; google_gate.py S12 refuses any indexable page without a current PASS (tools/review.py)."""
import json, os, re, shutil, sys
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
sys.path.insert(0, T); import review as RV
BASE = "https://floodinsurancedata.com"
DIR = os.path.join(ROOT, "state", "reviews")

LOCAL = "--local" in sys.argv   # review the new build in dist/ before it ships (the live site still has the old pages)
def url(slug):
    if LOCAL: return "file:///" + html_path(slug).replace("\\", "/")
    return BASE + "/" if slug == "home" else f"{BASE}/flood-insurance/{slug}/"
def html_path(slug):
    if slug == "home": return os.path.join(ROOT, "dist", "index.html")
    p = os.path.join(ROOT, "dist", "flood-insurance", slug, "index.html")
    # a queued county held for its own review exists only in the review build (build_counties.py --all) until it ships
    q = os.path.join(ROOT, "review", "flood-insurance", slug, "index.html")
    return q if not os.path.exists(p) and os.path.exists(q) else p
def data_dir(slug):
    for d in (os.path.join(ROOT, "data", "states", slug), os.path.join(ROOT, "data", "c", slug)):
        if os.path.isdir(d): return d
    return ""
def query(slug):   # the query a real reader types for this page
    if slug == "home": return "flood insurance cost"
    if not data_dir(slug): return "flood insurance " + slug.replace("-", " ")   # a national page (renters): its own words
    a = json.load(open(os.path.join(data_dir(slug), "agg.json")))
    return f"flood insurance cost {a.get('name') or slug.replace('-', ' ')}" if a.get("level") == "state" else \
           f"flood insurance cost {slug.rsplit('-', 1)[0].replace('-', ' ')} {a.get('state', '')}"

SNAP = os.path.join(DIR, "snap")   # visible text the reviewer saw (prep) and the last text that PASSed (record)
def vis_text(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S)   # CSS is not text a reader sees
    # 11-08: the county index grows every day by design (each row is gated on its own page); its rows and "N counties"
    # count are data, not template wording, so a carry compares everything else word for word
    h = re.sub(r'<tr data-k="[^"]*">.*?</tr>', " ", h, flags=re.S)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
    t = re.sub(r"\bretrieved \d{4}-\d{2}-\d{2}\b", "retrieved DATE", t)   # a fetch date is data, not wording
    return re.sub(r"\b[\d,]+ (count(?:y|ies)|parish(?:es)?|places)\b", r"N \1", t)
def snap(rnd, slugs):
    d = os.path.join(SNAP, f"round{rnd}"); os.makedirs(d, exist_ok=True)
    old = sorted((x for x in os.listdir(SNAP) if x.startswith("round")), key=lambda x: int(x[5:]))[:-3]   # cap: last 3 rounds + passed
    for x in old: shutil.rmtree(os.path.join(SNAP, x), ignore_errors=True)
    for s in slugs: open(os.path.join(d, s + ".txt"), "w", encoding="utf-8").write(vis_text(open(html_path(s), encoding="utf-8").read()))

def prep(rnd, slugs):
    if "--light" in sys.argv:   # CLAUDE.md budget: changed cards only, page text, no screenshots, no random pages
        open(os.path.join(DIR, f"round{rnd}-template.txt"), "w").write(RV.template_hash()); snap(rnd, slugs)
        return print("light round: template", RV.template_hash(), "pages:", " ".join(html_path(s) for s in slugs))
    # 2 random pages each round beside the samples: findings came only from the same 3-4 pages (2026-10-28)
    import random
    pool = [p["slug"] for p in json.load(open(os.path.join(ROOT, "places.json")))] + \
           [s["slug"] for s in json.load(open(os.path.join(ROOT, "data", "states", "built.json")))]
    slugs = list(slugs) + random.Random(int(rnd)).sample(sorted(set(pool) - set(slugs)), 2)
    from playwright.sync_api import sync_playwright
    for x in os.listdir(DIR):   # cap: only this round's screenshots stay on disk (72 MB had piled up by 11-04)
        if re.fullmatch(r"round\d+", x) and x != f"round{rnd}": shutil.rmtree(os.path.join(DIR, x), ignore_errors=True)
    shots = os.path.join(DIR, f"round{rnd}"); os.makedirs(shots, exist_ok=True)
    listing = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True,
                        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148")
        for s in slugs:
            pg.goto(url(s) + ("" if LOCAL else "?hater=" + str(rnd)), wait_until="networkidle")   # the live page, past any cache
            n = -(-pg.evaluate("document.documentElement.scrollHeight") // 844)
            for i in range(n):
                pg.evaluate(f"window.scrollTo(0,{i * 844})"); pg.screenshot(path=os.path.join(shots, f"{s}-{i:02d}.png"))
            listing.append(f"{s}-00..{s}-{n - 1:02d}.png")
        b.close()
    prev = os.path.join(DIR, f"hater-round{int(rnd) - 1}.md")
    fill = {"pages": ", ".join(url(s) for s in slugs), "slugs": ", ".join(slugs),
            "queries": "; ".join(f'{s}: "{query(s)}"' for s in slugs),
            "screens": f"{shots}\\ ({'; '.join(listing)})",
            "html": "; ".join(html_path(s) for s in slugs),
            "data": "; ".join(data_dir(s) + "\\{agg,data,extras}.json" for s in slugs if data_dir(s)) or "n/a",
            "previous": prev if os.path.exists(prev) else "none",
            "out": os.path.join(DIR, f"hater-round{rnd}.md")}
    body = open(os.path.join(ROOT, "docs", "HATER-PROMPT.md"), encoding="utf-8").read().split("\n---\n", 1)[1]
    brief = re.sub(r"\{(\w+)\}", lambda mm: fill.get(mm.group(1), mm.group(0)), body)
    path = os.path.join(DIR, f"round{rnd}-brief.md"); open(path, "w", encoding="utf-8").write(brief)
    open(os.path.join(DIR, f"round{rnd}-template.txt"), "w").write(RV.template_hash())   # the template this round reviews
    print("brief:", path)

def record(rnd):
    _raw = open(os.path.join(DIR, f"hater-round{rnd}.md"), "rb").read()
    try: txt = _raw.decode("utf-8")
    except UnicodeDecodeError: txt = _raw.decode("cp1252")   # 11-13 r169: a reviewer saved Windows-1252 dashes; read it, never crash
    tf = os.path.join(DIR, f"round{rnd}-template.txt")
    if not os.path.exists(tf): sys.exit(f"no {tf}: run prep {rnd} first (a PASS covers only the template the reviewer saw)")
    th = open(tf).read().strip()
    if th and th != RV.template_hash(): print(f"template changed since round {rnd} prep: its PASS will not cover the current build")
    for slug, sec in re.findall(r"^## (\S+)[^\n]*\n(.*?)(?=^## |\Z)", txt, re.S | re.M):
        slug = slug.strip("`/").split("/")[-1] or "home"
        if not (slug == "home" or data_dir(slug)): continue   # "Classes", "Previous items"
        v = re.search(r"Verdict:\s*\**\s*(PASS|FAIL)", sec)
        bad = re.findall(r"\*\*(BLOCKER|MAJOR)\*\*[^\n]*", sec)
        verdict = "PASS" if v and v.group(1) == "PASS" and not bad else "FAIL"
        RV.record(slug, verdict, [b[:160] for b in re.findall(r"\*\*(?:BLOCKER|MAJOR)\*\*[^\n]*", sec)][:60],
                  reviewer=f"hater round {rnd} (fresh agent, docs/HATER-PROMPT.md)", template=th)
        gaps = re.findall(r"\*\*GAP[^*]*\*\*[^\n]*", sec)   # owner 2026-10-28: gaps never block; they go to the to-do list
        if gaps:
            with open(os.path.join(DIR, "backlog.md"), "a", encoding="utf-8") as f:
                f.write(f"\n## {slug} (round {rnd})\n" + "".join(f"- {re.sub(r'^[*]{2}GAP[^*]*[*]{2}', '', g).strip()}\n" for g in gaps))
        sp = os.path.join(SNAP, f"round{rnd}", slug + ".txt")
        if verdict == "PASS" and os.path.exists(sp):
            os.makedirs(os.path.join(SNAP, "passed"), exist_ok=True); shutil.copy(sp, os.path.join(SNAP, "passed", slug + ".txt"))
        print(f"{slug}: {verdict} ({len(bad)} blocker/major, {len(gaps)} gaps to backlog.md)")

def stamped_slugs():
    """Every page with its own PASS on the samples' last approved template: all of them must move together, or a flagged
    page loses its example (analytics, 2026-10-30: two were missed and the ship stopped at S12). Older stamps stay old."""
    home = RV.get("home") or sys.exit("carry: no review stamp for home; name the pages")
    out = sorted(p[:-5] for p in os.listdir(DIR) if p.endswith(".json") and RV.own_pass(p[:-5], home["template"]))
    return out or sys.exit("carry: no page holds a PASS on the samples' template; run a review")

def carry(rnd, prev, slugs):
    """CLAUDE.md budget "None": a template change no reader can see (markup, scripts) keeps its PASS only if every
    slug's visible text equals the release `prev`, which passed review. Any difference stops it: a real review is due."""
    import subprocess
    if os.path.exists(os.path.join(DIR, f"hater-round{rnd}.md")):   # 11-10: carry overwrote a reviewer's round file; a carry takes its own round
        sys.exit(f"carry refused: hater-round{rnd}.md exists (a review's record); carry into a new round number")
    def vis(h):
        h = re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S)   # CSS is not text a reader sees
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
    lines = []
    for s in slugs:
        rel = os.path.relpath(html_path(s), ROOT).replace("\\", "/")
        if prev == "passed":
            sp = os.path.join(SNAP, "passed", s + ".txt")
            same = os.path.exists(sp) and open(sp, encoding="utf-8").read() == vis_text(open(html_path(s), encoding="utf-8").read())
        else:
            old = subprocess.run(["git", "show", f"{prev}:{rel}"], capture_output=True, text=True, encoding="utf-8").stdout
            same = bool(old) and vis(old) == vis(open(html_path(s), encoding="utf-8").read())
        if not same:
            sys.exit(f"carry refused: {s} visible text differs from {prev} (or no copy there); run a light review")
        lines.append(f"## {s}\nVisible text identical to release {prev} (scripts and tags stripped); no reader-visible change.\nVerdict: PASS\n")
    open(os.path.join(DIR, f"hater-round{rnd}.md"), "w", encoding="utf-8").write(f"# Round {rnd}: carried PASS (machine check)\n\n" + "\n".join(lines))
    open(os.path.join(DIR, f"round{rnd}-template.txt"), "w").write(RV.template_hash())
    record(rnd)

if __name__ == "__main__":
    if sys.argv[1:2] == ["carry"]: carry(sys.argv[2], sys.argv[3], sys.argv[4:] or stamped_slugs()); sys.exit()
    if sys.argv[1:2] == ["prep"]: prep(sys.argv[2], [a for a in sys.argv[3:] if a not in ("--local", "--light")])
    elif sys.argv[1:2] == ["record"]: record(sys.argv[2])
    else: print(__doc__)
