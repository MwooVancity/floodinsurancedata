"""County pages: every town named (ZIP card line and meta description) must be a Census place that, with at least one of
this county's NFIP ZIPs, lies in this county (data/us/zip_place_counties.json), listed in order of summed policy units.
Shares no code with build_page.py. Usage: python -I tools/town_check.py [--test]   (--test: each mutation must fail)"""
import glob, html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
US = os.path.join(ROOT, "data", "us")
ZP = json.load(open(os.path.join(US, "zip_places.json"), encoding="utf-8"))
ZC = json.load(open(os.path.join(US, "zip_place_counties.json"), encoding="utf-8"))

def expect(geoid):
    tot = {}
    for z in json.load(open(os.path.join(ROOT, "data", "all-counties", geoid + ".json")))["policies"].get("by_zip") or []:
        if re.fullmatch(r"\d{5}", str(z.get("zip"))) and z.get("units") and z["zip"] in ZP and geoid in ZC.get(z["zip"], []):
            tot[ZP[z["zip"]]] = tot.get(ZP[z["zip"]], 0) + z["units"]
    top = sorted(tot.items(), key=lambda kv: -kv[1])[:5]
    return [t for t, _ in top] if len(top) > 1 else [], tot

def check(page, geoid):
    want, tot = expect(geoid)
    m = re.search(r"Towns here, ranked by NFIP policy units in their ZIPs: (.*?)\.</p>", page)
    got = [html.unescape(re.sub(r"<[^>]+>", "", t)) for t in m[1].split(", ")] if m else []
    bad = [f"T1 town line {got} vs {want}"] if got != want else []
    if any(tot.get(t, 0) < tot.get(u, 0) for t, u in zip(got, got[1:])): bad.append("T2 towns out of order")
    d = re.search(r'<meta name="description" content="[^"]*? primary home in [^"(]*?(?: \(([^)]*)\))? is \$', page)
    dw = ", ".join(want[:3]) if want else None
    if not d or (html.unescape(d[1]) if d[1] else None) != dw: bad.append(f"T3 description towns {d and d[1]} vs {dw}")
    return bad

def pages():
    for p in json.load(open(os.path.join(ROOT, "places.json"))):
        f = os.path.join(ROOT, "dist", "flood-insurance", p["slug"], "index.html")
        if os.path.isfile(f): yield p["slug"], p["geoid"], open(f, encoding="utf-8").read()

if __name__ == "__main__":
    if "--test" in sys.argv:
        sl, g, pg = next((s, g, p) for s, g, p in pages() if len(expect(g)[0]) > 2)
        assert not check(pg, g), check(pg, g)
        w = expect(g)[0]
        muts = {"swap order": pg.replace(f"{w[0]}</span>, <span data-name>{w[1]}", f"{w[1]}</span>, <span data-name>{w[0]}", 1),
                "foreign town": pg.replace(f"their ZIPs: <span data-name>{w[0]}<", "their ZIPs: <span data-name>Houston<", 1),
                "description town": pg.replace(f" ({w[0]}, ", " (Atlantis, ", 1)}
        for k, mp in muts.items(): assert mp != pg and check(mp, g), f"mutation not caught: {k}"
        print(f"town check mutations: {len(muts)} caught ({sl})"); sys.exit()
    bad, n = [], 0
    for sl, g, pg in pages():
        n += 1; bad += [f"{sl}: {b}" for b in check(pg, g)]
    for b in bad[:20]: print("  -", b)
    print(f"TOWN CHECK {'FAIL' if bad else 'PASS'}: {n} county pages"); sys.exit(1 if bad else 0)
