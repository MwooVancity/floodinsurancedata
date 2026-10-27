"""The hater gate's mechanical half. The judging half is a fresh agent running docs/HATER-PROMPT.md.
  python -I tools/hater.py prep <round> <slug> [<slug> ...]   phone screenshots of the LIVE pages + the filled brief
  python -I tools/hater.py record <round>                     read the review, write state/reviews/<slug>.json
A slug is "home", a state slug or a county slug. record writes PASS only for a section ending "Verdict: PASS" with
no BLOCKER or MAJOR in it; google_gate.py S12 refuses any indexable page without a current PASS (tools/review.py)."""
import json, os, re, sys
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
sys.path.insert(0, T); import review as RV
BASE = "https://floodinsurancedata.com"
DIR = os.path.join(ROOT, "state", "reviews")

def url(slug): return BASE + "/" if slug == "home" else f"{BASE}/flood-insurance/{slug}/"
def html_path(slug): return os.path.join(ROOT, "dist", "index.html") if slug == "home" else os.path.join(ROOT, "dist", "flood-insurance", slug, "index.html")
def data_dir(slug):
    for d in (os.path.join(ROOT, "data", "states", slug), os.path.join(ROOT, "data", "c", slug)):
        if os.path.isdir(d): return d
    return ""
def query(slug):   # the query a real reader types for this page
    if slug == "home": return "flood insurance cost"
    a = json.load(open(os.path.join(data_dir(slug), "agg.json")))
    return f"flood insurance cost {a.get('name') or slug.replace('-', ' ')}" if a.get("level") == "state" else \
           f"flood insurance cost {slug.rsplit('-', 1)[0].replace('-', ' ')} {a.get('state', '')}"

def prep(rnd, slugs):
    from playwright.sync_api import sync_playwright
    shots = os.path.join(DIR, f"round{rnd}"); os.makedirs(shots, exist_ok=True)
    listing = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True,
                        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148")
        for s in slugs:
            pg.goto(url(s) + "?hater=" + str(rnd), wait_until="networkidle")   # the live page, past any cache
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
    print("brief:", path)

def record(rnd):
    txt = open(os.path.join(DIR, f"hater-round{rnd}.md"), encoding="utf-8").read()
    for slug, sec in re.findall(r"^## (\S+)[^\n]*\n(.*?)(?=^## |\Z)", txt, re.S | re.M):
        slug = slug.strip("`/").split("/")[-1] or "home"
        if not (slug == "home" or data_dir(slug)): continue   # "Classes", "Previous items"
        v = re.search(r"Verdict:\s*\**\s*(PASS|FAIL)", sec)
        bad = re.findall(r"\*\*(BLOCKER|MAJOR)\*\*[^\n]*", sec)
        verdict = "PASS" if v and v.group(1) == "PASS" and not bad else "FAIL"
        RV.record(slug, verdict, [b[:160] for b in re.findall(r"\*\*(?:BLOCKER|MAJOR)\*\*[^\n]*", sec)][:60],
                  reviewer=f"hater round {rnd} (fresh agent, docs/HATER-PROMPT.md)")
        print(f"{slug}: {verdict} ({len(bad)} blocker/major)")

if __name__ == "__main__":
    if sys.argv[1:2] == ["prep"]: prep(sys.argv[2], sys.argv[3:])
    elif sys.argv[1:2] == ["record"]: record(sys.argv[2])
    else: print(__doc__)
