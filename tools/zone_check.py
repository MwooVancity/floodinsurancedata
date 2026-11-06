"""Zone pages (/flood-zones/<z>/): every figure recomputed from the data files by code that shares nothing with
build_site.py, then compared with the built page. No gate covered these pages before 11-06 (a top-12 cut there
undercounted VE/AO/AH/D units for days). Fails on:
  Z1 state table: a state's median or policy count differs from its agg.json, a state with a median is missing or doubled,
     or a state without one is listed
  Z2 the "N more states ... too few" count is wrong
  Z3 the headline median differs from a fresh recompute (exact zone once all 51 states carry it, else the zone group
     on AE/X/VE only, else no tile at all)
  Z4 the title's number differs from the headline tile
  Z5 the threshold printed differs from ffcalc.ZONE_MIN
  Z6 claims card: counts or dollars differ from claims_zone.json summed over 51 states; any claims figure with fewer
     than 51 states or under 10 paid claims
  Z7 a "Full-risk" tile without its "before fees" label
Usage: python -I tools/zone_check.py [dist dir]   |   --test runs the mutations (each must make the check fail)."""
import glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffcalc import ZONE_MIN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CODES = {"ae": "AE", "x": "X", "ve": "VE", "a": "A", "ao": "AO", "ah": "AH", "d": "D"}
GROUP = {"AE": "A", "X": "X", "VE": "V"}

def load(p, default=None):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default

def us(name):
    d = load(os.path.join(DATA, "us", name), {})
    return d if len(d) == 51 else {}

def quantile(hists, q):   # independent of build_site._hq: one flat sorted walk
    pairs = sorted((int(k), c) for h in hists for k, c in h.items())
    total = sum(c for _, c in pairs)
    if not total: return None
    need, run = total * q, 0
    for v, c in pairs:
        run += c
        if run >= need: return v

def dollars(s): return int(s.replace("$", "").replace(",", ""))

def expected(code, states, agg):
    zx, zh = us("cost_hist_zone_exact.json"), us("cost_hist_zone.json")
    ex = [h.get(code) or {} for h in zx.values()]
    if zx and sum(sum(h.values()) for h in ex) >= ZONE_MIN: return quantile(ex, 0.5)
    if code in GROUP and len(zh) == 51: return quantile([h.get(GROUP[code]) or {} for h in zh.values()], 0.5)
    return None

def check_page(code, page, states, agg):
    bad = []
    text = html.unescape(re.sub(r"<[^>]+>", " ", page))
    # Z1/Z2: the state cost table
    m = re.search(r'id="states".*?<tbody>(.*?)</tbody>', page, re.S)
    rows = re.findall(r'<tr><td><a href="/flood-insurance/([^/]+)/">[^<]*</a></td><td>(\$[\d,]+)</td><td>([\d,]+)</td>', m[1]) if m else []
    seen = [r[0] for r in rows]
    want = {s["slug"]: agg[s["slug"]].get("cost_by_zone", {}).get(code) for s in states}
    for slug, med, n in rows:
        w = want.get(slug)
        if not w: bad.append(f"Z1 {code}: {slug} listed with no median in its data")
        elif dollars(med) != w["median"] or int(n.replace(",", "")) != w["n"]: bad.append(f"Z1 {code}: {slug} shows {med}/{n}, data {w['median']}/{w['n']}")
    for slug, w in want.items():
        if w and seen.count(slug) != 1: bad.append(f"Z1 {code}: {slug} has a median but appears {seen.count(slug)} times")
    def units(p):   # None when the old top-12 field may have cut the zone off
        if p.get("zone_units_all") is not None: return p["zone_units_all"].get(code, 0)
        t = p.get("zone_units") or {}
        return t.get(code, 0) if code in t or len(t) < 12 else None
    few = sum(1 for s in states if not want[s["slug"]] and units(agg[s["slug"]]))
    mf = re.search(r"(\d+) more (?:states have|state has) zone \w+ policies", text)
    if (int(mf[1]) if mf else 0) != few: bad.append(f"Z2 {code}: page says {mf[1] if mf else 0} more states, data {few}")
    # Z3/Z4: headline tile and title
    tile = re.search(r'<div class="stat"><div class="n">(\$[\d,]+)</div>', page)
    exp = expected(code, states, agg)
    got = dollars(tile[1]) if tile else None
    if got != exp: bad.append(f"Z3 {code}: headline {got}, recomputed {exp}")
    tt = re.search(r"<title>[^<]*?\((\$[\d,]+) median", page)
    if tt and (not tile or tt[1] != tile[1]): bad.append(f"Z4 {code}: title {tt[1]} vs tile {tile[1] if tile else None}")
    # Z5: the threshold wording
    for t in re.findall(r"(\d+) or more priced policies|under (\d+) priced", text):
        v = int(t[0] or t[1])
        if v != ZONE_MIN: bad.append(f"Z5 {code}: threshold printed {v}, ZONE_MIN {ZONE_MIN}")
    # Z6: claims by zone
    mc = re.search(r"NFIP claims rated (\w+), losses in (\d{4})–(\d{4}): ([\d,]+) claims, ([\d,]+) paid, (\$[\d,]+) paid in total, (\$[\d,]+) on average", text)
    cz = us("claims_zone.json")
    if mc:
        if not cz: bad.append(f"Z6 {code}: claims shown without all 51 states")
        else:
            t = [0, 0, 0]
            for v in cz.values():
                c = v["by_zone"].get(code) or {}
                t[0] += c.get("n", 0); t[1] += c.get("paid_n", 0); t[2] += c.get("paid", 0)
            shown = [int(mc[4].replace(",", "")), int(mc[5].replace(",", "")), dollars(mc[6])]
            if shown != t: bad.append(f"Z6 {code}: claims {shown}, data {t}")
            if t[1] < 10: bad.append(f"Z6 {code}: claims shown on {t[1]} paid claims")
            elif dollars(mc[7]) != round(t[2] / t[1]): bad.append(f"Z6 {code}: average {mc[7]}, data {round(t[2] / t[1])}")
    # Z7: full-risk label
    for lab in re.findall(r'<div class="l">([^<]*Full-risk[^<]*)</div>', page):
        if "before fees" not in lab: bad.append(f"Z7 {code}: full-risk tile without 'before fees': {lab}")
    return bad

def run(dist):
    states = load(os.path.join(DATA, "states", "built.json"), [])
    agg = {s["slug"]: load(os.path.join(DATA, "states", s["slug"], "agg.json"))["policies"] for s in states}
    pages = {z: open(p, encoding="utf-8").read() for z in CODES for p in [os.path.join(dist, "flood-zones", z, "index.html")] if os.path.exists(p)}
    if len(states) == 51 and len(pages) != len(CODES): return [f"Z0 zone pages built: {sorted(pages)}"]
    return [b for z, pg in pages.items() for b in check_page(CODES[z], pg, states, agg)]

def test(dist):
    states = load(os.path.join(DATA, "states", "built.json"), [])
    agg = {s["slug"]: load(os.path.join(DATA, "states", s["slug"], "agg.json"))["policies"] for s in states}
    ae = open(os.path.join(dist, "flood-zones", "ae", "index.html"), encoding="utf-8").read()
    assert not check_page("AE", ae, states, agg), check_page("AE", ae, states, agg)
    row = re.search(r'(<tr><td><a href="/flood-insurance/[^/]+/">[^<]*</a></td><td>)(\$[\d,]+)', ae)
    tile = re.search(r'<div class="stat"><div class="n">(\$[\d,]+)', ae)
    muts = {
        "Z1 median": ae.replace(row[0], row[1] + "$1", 1),
        "Z1 missing state": ae.replace(re.search(r'<tr><td><a href="/flood-insurance/[^"]+">.*?</tr>', ae[ae.index('id="states"'):])[0], "", 1),
        "Z2 few": ae.replace("<tbody>", "<tbody>", 1).replace("in force on", "in force on", 1) + " 99 more states have zone AE policies",
        "Z3 headline": ae.replace(tile[0], '<div class="stat"><div class="n">$1', 1),
        "Z5 threshold": ae + " under 30 priced policies",
        "Z7 label": ae + '<div class="l">Full-risk premium median</div>',
    }
    for name, m in muts.items():
        assert check_page("AE", m, states, agg), f"mutation not caught: {name}"
    print(f"zone_check mutations: {len(muts)} caught")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    dist = a[0] if a else os.path.join(ROOT, "dist")
    if "--test" in sys.argv: test(dist); sys.exit()
    bad = run(dist)
    for b in bad[:40]: print("  -", b)
    print("ZONE CHECK", "FAIL" if bad else "PASS", f"({len(bad)} problems)")
    sys.exit(1 if bad else 0)
