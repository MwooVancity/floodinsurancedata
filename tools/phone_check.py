"""Gate 3 ("live and usable"): the reader on a phone, measured. Playwright at 390x844 on three counties (the
largest, a Louisiana parish, the smallest). Fails when a reader would be hurt:
  P1 anything wider than the screen (outside its own scroll box)   P2 any rendered text, SVG included, under 11px
  P3 screen 1 lacks the median, the FEMA map button or the jump menu   P4 the quote checker is below screen 2
  P8 the last of the six reader answers (data-ans) starts below screen 1
  P5 data hidden inside a collapsed <details>   P6 chart labels overlap   P7 text contrast under WCAG AA (owner 11-04: "blurry")
Usage: python -I tools/phone_check.py [--base file:///.../dist | https://floodinsurancedata.com] [slug ...]"""
import json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, MIN_PX = 390, 844, 11
args = sys.argv[1:]
base = "file:///" + os.path.join(ROOT, "dist").replace("\\", "/")
if "--base" in args:
    i = args.index("--base"); base = args[i + 1]; del args[i:i + 2]
slugs = args
TEST = "--test" in args
if TEST:   # P8 mutation: answers pushed below screen 1 must fail; a real county page copied into a temp dist
    import shutil, tempfile
    _cs = json.load(open(os.path.join(ROOT, "tools", "counties.json")))[0]["slug"]
    _tmp = tempfile.mkdtemp(); _d = os.path.join(_tmp, "flood-insurance", _cs); os.makedirs(_d)
    _h = open(os.path.join(ROOT, "dist", "flood-insurance", _cs, "index.html"), encoding="utf-8").read()
    open(os.path.join(_d, "index.html"), "w", encoding="utf-8").write(_h.replace('<nav class="jump qa">', '<div style="height:700px"></div><nav class="jump qa">', 1))
    base = "file:///" + _tmp.replace("\\", "/"); slugs = [_cs]
if not slugs:
    cs = json.load(open(os.path.join(ROOT, "tools", "counties.json")))
    u = {c["slug"]: json.load(open(os.path.join(ROOT, "data", "c", c["slug"], "agg.json")))["policies"]["units"] for c in cs}
    big, small = max(u, key=u.get), min(u, key=u.get)
    parish = next((s for s in sorted(u, key=u.get, reverse=True) if "parish" in s), big)
    slugs = list(dict.fromkeys([big, parish, small]))
    import datetime, random   # P8 (11-12): 5 random counties a day as well, seeded by the date so a rerun checks the same ones
    slugs += random.Random(datetime.date.today().isoformat()).sample(sorted(set(u) - set(slugs)), min(5, max(0, len(u) - len(slugs))))
    _bp = os.path.join(ROOT, "data", "states", "built.json")   # plus the largest and smallest state page
    st = sorted(json.load(open(_bp)), key=lambda s: s["units"]) if os.path.exists(_bp) else []
    slugs += list(dict.fromkeys(s["slug"] for s in st[-1:] + st[:1]))
    slugs += ["/", "/flood-zones/x/", "/flood-zone-map/"]   # 11-12 hater r153: the home page scrolled sideways and was never phone-checked   # 11-06: zone pages shipped a blue-on-blue button for days; P1/P2/P7 only (no county blocks)

# vw is the DEVICE width, not innerWidth: given wide content a phone widens the layout viewport and zooms the whole
# page out, so measuring against innerWidth would hide exactly the overflow a reader suffers.
JS = """() => {
  const vw = %W%, out = {height: document.documentElement.scrollHeight, wide: [], small: [], faint: [], hidden: 0};
  const rgb = s => { const m = s.match(/[\\d.]+/g) || [0, 0, 0, 0]; return [+m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1]; };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; };
    return .2126 * f(c[0]) + .7152 * f(c[1]) + .0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
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
    if (!svg) { const cs = getComputedStyle(e), c = rgb(cs.color);
      let bg = null; for (let p = e; p && !bg; p = p.parentElement) { const b = rgb(getComputedStyle(p).backgroundColor); if (b[3]) bg = b; }
      const k = ratio(c, bg || [255, 255, 255, 1]), big = px >= 24 || (px >= 18.6 && +cs.fontWeight >= 700);
      if (k < (big ? 3 : 4.5)) out.faint.push(e.tagName + ' ' + k.toFixed(2) + ':1 "' + e.textContent.trim().slice(0, 30) + '"'); }
  }
  const top = s => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().top + scrollY : null; };
  out.median = top('[data-m="cost_p50"]'); out.map = top('a.btn'); out.jump = top('nav.jump'); out.compare = top('#compare');
  { const q = [...document.querySelectorAll('[data-ans]')]; out.qlast = q.length ? Math.max(...q.map(e => e.getBoundingClientRect().top + scrollY)) : null; out.qn = q.length; }
  out.hidden = [...document.querySelectorAll('details:not([open])')].filter(d => d.querySelector('.card, table, [data-m]')).length;
  out.overlap = [];   // P6 chart labels that print over each other ("$1,0$8,17$1,376")
  for (const svg of document.querySelectorAll('svg')) {
    const t = [...svg.querySelectorAll('text')].map(e => [e.textContent.trim(), e.getBoundingClientRect()]).filter(x => x[1].width);
    for (let i = 0; i < t.length; i++) for (let j = i + 1; j < t.length; j++) {
      const a = t[i][1], b = t[j][1];
      if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1)
        out.overlap.push('"' + t[i][0] + '" / "' + t[j][0] + '"'); } }
  return out; }""".replace("%MIN%", str(MIN_PX)).replace("%W%", str(W))

failed = False
os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_context(viewport={"width": W, "height": H}, is_mobile=True, has_touch=True).new_page()
    for s in slugs:
        site = s.startswith("/")
        if site and not os.path.exists(os.path.join(ROOT, "dist", s.strip("/"), "index.html")) and base.startswith("file:"): continue
        url = (f"{base}{s}" if site else f"{base}/flood-insurance/{s}/") + ("index.html" if base.startswith("file:") else "")
        pg.goto(url, wait_until="networkidle")
        r = pg.evaluate(JS)
        bad = []
        if r["wide"]: bad.append(f"P1 wider than screen: {r['wide'][:4]}")
        if r["small"]: bad.append(f"P2 text under {MIN_PX}px: {r['small'][:4]}")
        if r["faint"]: bad.append(f"P7 text too faint (contrast under 4.5:1, 3:1 if large): {r['faint'][:4]}")
        for k in (() if site else ("median", "map", "jump")):
            if r[k] is None or r[k] > H: bad.append(f"P3 {k} not on screen 1 (top {r[k]})")
        if not site and (r["compare"] is None or r["compare"] > 2 * H): bad.append(f"P4 quote checker not within screen 2 (top {r['compare']})")
        # P8 (audit 11-10, parent live check 11-12): the six reader answers (risk, required, cost, rising, pays, pay less) start on screen 1
        if not site and (r["qlast"] is None or r["qlast"] > H): bad.append(f"P8 last of the {r['qn']} screen-1 answers starts at {r['qlast']} (screen 1 ends {H})")
        if r["hidden"]: bad.append(f"P5 {r['hidden']} collapsed <details> hide data")
        if r["overlap"]: bad.append(f"P6 chart labels overlap: {r['overlap'][:3]}")
        print(("PHONE FAIL " if bad else "PHONE PASS ") + f"{s} (height {r['height']}px = {r['height'] / H:.1f} screens)")
        for b in bad: print("  -", b)
        failed |= bool(bad)
    br.close()
if TEST:
    assert failed, "P8 mutation not caught: answers pushed below screen 1 passed"
    print("phone_check P8 mutation: 1 caught"); sys.exit(0)
sys.exit(1 if failed else 0)
