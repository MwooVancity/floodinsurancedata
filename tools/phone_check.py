"""Gate 3 ("live and usable"): the reader on a phone, measured. Playwright at 390x844 on three counties (the
largest, a Louisiana parish, the smallest). Fails when a reader would be hurt:
  P1 anything wider than the screen (outside its own scroll box)   P2 any rendered text, SVG included, under 11px
  P3 screen 1 lacks the median, the FEMA map button or the jump menu   P4 the quote checker is below screen 2
  P5 data hidden inside a collapsed <details>
Usage: python -I tools/phone_check.py [--base file:///.../dist | https://floodinsurancedata.com] [slug ...]
Appends one line per page to state/phone-check.jsonl (page height is recorded so growth is visible)."""
import datetime, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, MIN_PX = 390, 844, 11
args = sys.argv[1:]
base = "file:///" + os.path.join(ROOT, "dist").replace("\\", "/")
if "--base" in args:
    i = args.index("--base"); base = args[i + 1]; del args[i:i + 2]
slugs = args
if not slugs:
    cs = json.load(open(os.path.join(ROOT, "tools", "counties.json")))
    u = {c["slug"]: json.load(open(os.path.join(ROOT, "data", c["slug"], "agg.json")))["policies"]["units"] for c in cs}
    big, small = max(u, key=u.get), min(u, key=u.get)
    parish = next((s for s in sorted(u, key=u.get, reverse=True) if "parish" in s), big)
    slugs = list(dict.fromkeys([big, parish, small]))

# vw is the DEVICE width, not innerWidth: given wide content a phone widens the layout viewport and zooms the whole
# page out, so measuring against innerWidth would hide exactly the overflow a reader suffers.
JS = """() => {
  const vw = %W%, out = {height: document.documentElement.scrollHeight, wide: [], small: [], hidden: 0};
  if (document.documentElement.scrollWidth > vw + 1 || innerWidth > vw + 1)
    out.wide.push('page is ' + Math.max(document.documentElement.scrollWidth, innerWidth) + 'px wide');
  const scrollBox = e => { for (let p = e.parentElement; p; p = p.parentElement) {
      const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll') return p; } return null; };
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect(); if (!r.width) continue;
    if (r.right > vw + 1) { const b = scrollBox(e); if (!b || b.getBoundingClientRect().right > vw + 1)
        out.wide.push(e.tagName + '.' + (e.className.baseVal ?? e.className)); }
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    let px = parseFloat(getComputedStyle(e).fontSize);
    const svg = e.closest('svg');
    if (svg && svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width)
      px = px * svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    if (px < %MIN%) out.small.push(e.tagName + ' ' + px.toFixed(1) + 'px "' + e.textContent.trim().slice(0, 30) + '"');
  }
  const top = s => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().top + scrollY : null; };
  out.median = top('[data-m="cost_p50"]'); out.map = top('a.btn'); out.jump = top('nav.jump'); out.compare = top('#compare');
  out.hidden = [...document.querySelectorAll('details:not([open])')].filter(d => d.querySelector('.card, table, [data-m]')).length;
  return out; }""".replace("%MIN%", str(MIN_PX)).replace("%W%", str(W))

failed = False
os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_context(viewport={"width": W, "height": H}, is_mobile=True, has_touch=True).new_page()
    for s in slugs:
        url = f"{base}/flood-insurance/{s}/" + ("index.html" if base.startswith("file:") else "")
        pg.goto(url, wait_until="networkidle")
        r = pg.evaluate(JS)
        bad = []
        if r["wide"]: bad.append(f"P1 wider than screen: {r['wide'][:4]}")
        if r["small"]: bad.append(f"P2 text under {MIN_PX}px: {r['small'][:4]}")
        for k in ("median", "map", "jump"):
            if r[k] is None or r[k] > H: bad.append(f"P3 {k} not on screen 1 (top {r[k]})")
        if r["compare"] is None or r["compare"] > 2 * H: bad.append(f"P4 quote checker not within screen 2 (top {r['compare']})")
        if r["hidden"]: bad.append(f"P5 {r['hidden']} collapsed <details> hide data")
        print(("PHONE FAIL " if bad else "PHONE PASS ") + f"{s} (height {r['height']}px = {r['height'] / H:.1f} screens)")
        for b in bad: print("  -", b)
        failed |= bool(bad)
        with open(os.path.join(ROOT, "state", "phone-check.jsonl"), "a") as f:
            f.write(json.dumps({"date": str(datetime.date.today()), "base": base, "slug": s, "height": r["height"],
                                "pass": not bad, "fails": bad}) + "\n")
    br.close()
sys.exit(1 if failed else 0)
