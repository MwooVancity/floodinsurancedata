"""Crawl the live site the way Googlebot does and report what Google would see: status, redirects, canonical, robots meta,
title / description / H1 duplicates, thin text, orphans (sitemap URL nobody links to), broken or redirecting internal links.
Read-only, 4 requests a second, stdlib only. Complements walk_site.py (reader click-through) and gate_live.py (byte match).
Usage: python -I tools/crawl_like_google.py [base] [--limit N]   Writes state/crawl-report.json; exit 1 if any ERROR."""
import json, os, re, sys, time, urllib.request, urllib.error, urllib.parse
from collections import defaultdict
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
args = [a for i, a in enumerate(sys.argv[1:]) if a.startswith("http")]
BASE = (args[0] if args else "https://floodinsurancedata.com").rstrip("/")
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 10**9

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
OPENER = urllib.request.build_opener(NoRedirect)

def get(url):
    """(status, location, body) without following redirects, so a redirect chain shows as one."""
    for i in range(3):
        try:
            r = OPENER.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60)
            return r.status, "", r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Location", ""), ""
        except Exception as e:
            err = repr(e); time.sleep(2 * (i + 1))
    print('FETCH FAIL', url, err)
    return 0, "", ""

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.title = s.h1 = s.desc = s.canon = s.robots = ""; s.links = []; s.text = []; s.h1n = 0
        s._t = s._h = s._done = False; s._skip = 0; s.ld = 0
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == "title" and not s._done: s._t = True
        elif tag == "h1": s._h = True; s.h1n += 1
        elif tag in ("script", "style", "noscript"): s._skip += 1; s.ld += tag == "script" and a.get("type") == "application/ld+json"
        elif tag == "meta" and a.get("name") == "description": s.desc = a.get("content", "")
        elif tag == "meta" and a.get("name") == "robots": s.robots = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical": s.canon = a.get("href", "")
        elif tag == "a" and a.get("href"): s.links.append(a["href"])
    def handle_endtag(s, tag):
        if tag == "title": s._t = False; s._done = bool(s.title)
        elif tag == "h1": s._h = False
        elif tag in ("script", "style", "noscript"): s._skip = max(0, s._skip - 1)
    def handle_data(s, d):
        if s._t and not s._done: s.title += d
        if s._h: s.h1 += d
        if not s._skip: s.text.append(d)

def main():
    st, _, robots = get(BASE + "/robots.txt")
    print("robots.txt", st, "Disallow lines:", len(re.findall(r"(?im)^disallow:\s*\S", robots)))
    st, _, sm = get(BASE + "/sitemap.xml")
    allu = re.findall(r"<loc>([^<]+)</loc>", sm); urls = allu[:LIMIT]
    print("sitemap", st, len(allu), "URLs")
    if st != 200 or not allu: print("ERROR sitemap unreadable or empty: crawl not trusted"); sys.exit(1)
    pages, errors, warns = {}, [], []
    for n, u in enumerate(urls):
        st, loc, body = get(u)
        if st != 200: errors.append(f"{u}: HTTP {st} {loc}"); time.sleep(0.25); continue
        p = P(); p.feed(body); words = len(" ".join(p.text).split())
        pages[u] = dict(title=p.title.strip(), desc=p.desc.strip(), h1=p.h1.strip(), canon=p.canon, robots=p.robots, words=words,
                        links=sorted({urllib.parse.urljoin(u, l).split("#")[0] for l in p.links}), h1n=p.h1n, ld=p.ld)
        time.sleep(0.25)
    inbound, bad_links, seen = defaultdict(set), [], {}
    site = set(allu); norm = {x.rstrip("/") + "/" for x in site}
    for u, d in pages.items():
        if d["canon"].rstrip("/") != u.rstrip("/"): errors.append(f"{u}: canonical {d['canon']!r} is not itself")
        if "noindex" in d["robots"].lower(): errors.append(f"{u}: noindex in a sitemap page")
        if d["h1n"] != 1: warns.append(f"{u}: {d['h1n']} H1 tags")
        if not d["title"] or len(d["title"]) > 70: warns.append(f"{u}: title length {len(d['title'])}")
        if not d["desc"]: warns.append(f"{u}: no meta description")
        if d["words"] < 250: warns.append(f"{u}: only {d['words']} words of body text")
        for l in d["links"]:
            if l.startswith(BASE) and l.rstrip("/") + "/" in norm:
                if l not in site: warns.append(f"{u}: internal link {l} is not the sitemap form (would redirect)")
                if l.rstrip("/") + "/" != u.rstrip("/") + "/": inbound[l.rstrip("/") + "/"].add(u)   # a self-link is not an inbound link
            elif l.startswith(BASE) and "/data/" not in l and "." not in l.rsplit("/", 1)[-1]: bad_links.append((u, l))
    for kind in ("title", "desc", "h1"):
        g = defaultdict(list)
        for u, d in pages.items():
            if d[kind]: g[d[kind]].append(u)
        for t, us in g.items():
            if len(us) > 1: warns.append(f"duplicate {kind} on {len(us)} pages: {t[:70]!r} e.g. {us[0]}")
    orph = [u for u in pages if u.rstrip("/") + "/" not in inbound and u.rstrip("/") != BASE]
    if LIMIT < len(allu): orph = []; print("note: --limit crawl, orphan check skipped (a partial crawl cannot see all inbound links)")
    for u in orph: errors.append(f"{u}: orphan (no internal link to it)")
    targets = defaultdict(list)
    for u, l in bad_links: targets[l].append(u)
    for l, us in targets.items():   # a link to a page outside the sitemap is fine only if that page is noindex
        st, loc, body = get(l); time.sleep(0.25)
        if st != 200: errors.append(f"{l}: linked from {len(us)} pages (e.g. {us[0]}) but HTTP {st} {loc}")
        elif "noindex" not in body[:6000].lower(): errors.append(f"{l}: indexable page missing from the sitemap, linked from {len(us)} pages")
        else: warns.append(f"{l}: noindex page linked from {len(us)} pages (intended?)")
    json.dump(dict(base=BASE, pages=len(pages), errors=errors, warnings=warns), open(os.path.join(ROOT, "state", "crawl-report.json"), "w"), indent=1)
    print(f"crawled {len(pages)} pages; ERRORS {len(errors)}; warnings {len(warns)}")
    for e in errors[:40]: print("ERROR", e)
    for w in warns[:40]: print("warn", w)
    sys.exit(1 if errors else 0)

main()
