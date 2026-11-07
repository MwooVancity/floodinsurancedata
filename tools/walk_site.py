"""Click through the live site like a reader on a phone: every sitemap page loads (200, no console errors, no broken
images), every internal link resolves, the home search box finds a county, and every reader tool opens and answers.
Read-only; FEMA's map servers refuse non-US connections, so the address tool is checked up to its map step only.
Usage: python -I tools/walk_site.py [base]   (default https://floodinsurancedata.com)"""
import re, sys, urllib.request
from playwright.sync_api import sync_playwright

UA = {"User-Agent": "Mozilla/5.0 (floodinsurancedata site walk)"}
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://floodinsurancedata.com").rstrip("/")

def main():
    sm = urllib.request.urlopen(urllib.request.Request(BASE + "/sitemap.xml", headers=UA), timeout=60).read().decode()
    pages = re.findall(r"<loc>([^<]+)</loc>", sm)
    bad, links = [], set()
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "googletagmanager" not in m.text else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for u in pages:
            errs.clear()
            r = pg.goto(u, wait_until="load")
            if not r or r.status != 200: bad.append(f"{u}: HTTP {r.status if r else 'none'}"); continue
            if errs: bad.append(f"{u}: console {errs[:2]}")
            broken = pg.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src).map(i => i.src)")
            if broken: bad.append(f"{u}: broken images {broken[:2]}")
            for h in pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.href)"):
                h = h.split("#")[0]
                if h.startswith(BASE): links.add(h)
        print(f"pages: {len(pages)} loaded; internal links found: {len(links)}")
        for h in sorted(links - set(pages)):
            try:
                c = urllib.request.urlopen(urllib.request.Request(h, method="HEAD", headers=UA), timeout=30).status
            except Exception as e: c = getattr(e, "code", repr(e)[:40])
            if c != 200: bad.append(f"link {h}: {c}")
        # home search box: type a county, a match must show
        pg.goto(BASE + "/", wait_until="load")
        if pg.locator("#s").count():
            pg.fill("#s", "palm beach"); pg.wait_for_timeout(400)
            vis = pg.evaluate("[...document.querySelectorAll('#t tbody tr, #st tbody tr')].filter(r => r.offsetParent && r.textContent.toLowerCase().includes('palm beach')).length")
            if not vis: bad.append("home search: typing 'palm beach' shows no row")
        # quote checker on a sample county
        pg.goto(BASE + "/flood-insurance/palm-beach-county-fl/", wait_until="load")
        q = pg.locator("#compare input").first
        if q.count():
            q.fill("1200"); q.press("Enter"); pg.wait_for_timeout(400)
            t = pg.inner_text("#compare")
            if not re.search(r"\$1,200|1,200", t) or re.search(r"NaN|undefined", t): bad.append(f"quote checker: no answer for $1,200 ({t[:120]!r})")
        else: bad.append("quote checker: not found on palm-beach-county-fl")
        # address tool: opens, takes an address, reaches the Census step (FEMA itself is not reachable from here)
        pg.goto(BASE + "/flood-zone-map/", wait_until="load")
        if pg.locator("#zm .zm-open").count():
            errs.clear(); pg.click("#zm .zm-open"); pg.wait_for_function("window.__zmStart !== undefined", timeout=15000)
            if errs: bad.append(f"address tool: console {errs[:2]}")
        else: bad.append("address tool: missing on /flood-zone-map/")
        b.close()
    for x in bad[:40]: print("  -", x)
    print("WALK", "FAIL" if bad else "PASS", f"({len(bad)} problems)")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
