"""County pages: every town named (ZIP card line and meta description) must be a Census place that, with at least one of
this county's NFIP ZIPs, lies in this county (data/us/zip_place_counties.json), listed in order of summed policy units.
Shares no code with build_page.py. Usage: python -I tools/town_check.py [--test]   (--test: each mutation must fail)"""
import glob, html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
US = os.path.join(ROOT, "data", "us")
ZP = json.load(open(os.path.join(US, "zip_places.json"), encoding="utf-8"))
ZC = json.load(open(os.path.join(US, "zip_place_counties.json"), encoding="utf-8"))

def expect(geoid):
    tot, cover = {}, [0, 0]   # cover: [units in ZIPs with a town here, units in all 5-digit ZIPs]
    for z in json.load(open(os.path.join(ROOT, "data", "all-counties", geoid + ".json")))["policies"].get("by_zip") or []:
        if not (re.fullmatch(r"\d{5}", str(z.get("zip"))) and z.get("units")): continue
        cover[1] += z["units"]
        if z["zip"] in ZP and geoid in ZC.get(z["zip"], []):
            tot[ZP[z["zip"]]] = tot.get(ZP[z["zip"]], 0) + z["units"]; cover[0] += z["units"]
    top = sorted(tot.items(), key=lambda kv: -kv[1])[:5]
    return [t for t, _ in top] if len(top) > 1 else [], tot, cover

def check(page, geoid):
    want, tot, cover = expect(geoid)
    wt = want   # title/description name the top town; the town line states what the ranking leaves out (T5)
    m = re.search(r"Towns here, ranked by NFIP policy units in their ZIPs: (.*?)\.</p>", page)
    got = [html.unescape(re.sub(r"<[^>]+>", "", t)) for t in m[1].split(", ")] if m else []
    bad = [f"T1 town line {got} vs {want}"] if got != want else []
    if any(tot.get(t, 0) < tot.get(u, 0) for t, u in zip(got, got[1:])): bad.append("T2 towns out of order")
    d = re.search(r'<meta name="description" content="[^"]*? primary home in [^"(]*?(?: \(([^)]*)\))? is \$', page)
    dw = ", ".join(wt[:3]) if wt else None
    if not d or (html.unescape(d[1]) if d[1] else None) != dw: bad.append(f"T3 description towns {d and d[1]} vs {dw}")
    t = re.search(r"<title>[^<(]*?(?: \(([^)]*)\))? flood zones", page)   # T4 title names the top town, or none
    # a New York City county is one borough (Census county subdivision, not a place): the title names the borough instead
    boro = {"36061": "Manhattan", "36047": "Brooklyn", "36081": "Queens", "36005": "the Bronx", "36085": "Staten Island"}.get(geoid)
    if not t or (html.unescape(t[1]) if t[1] else None) != (boro or (wt[0] if wt and wt[0].lower() not in page[t.start():t.end()].split(" (")[0].lower() else None)):
        bad.append(f"T4 title town {t and t[1]} vs {wt[:1]}")
    # T5 (r114 Sonoma): when the ranking leaves units out, the page says how many, with the right numbers
    lo = re.search(r"ZIPs where no single town covers at least a quarter of the land hold <span[^>]*>([\d,]+)</span> of the <span[^>]*>([\d,]+)</span>", page)
    need = want and cover[1] > cover[0]
    if need and not (lo and (int(lo[1].replace(",", "")), int(lo[2].replace(",", ""))) == (cover[1] - cover[0], cover[1])):
        bad.append(f"T5 left-out ZIP units {lo and lo.groups()} vs {(cover[1] - cover[0], cover[1])}")
    if lo and not need: bad.append("T5 left-out line where every ZIP has a town")
    return bad

def pages():
    for p in json.load(open(os.path.join(ROOT, "places.json"))):
        f = os.path.join(ROOT, "dist", "flood-insurance", p["slug"], "index.html")
        if os.path.isfile(f): yield p["slug"], p["geoid"], open(f, encoding="utf-8").read()

if __name__ == "__main__":
    if "--test" in sys.argv:
        sl, g, pg = next((s, g, p) for s, g, p in pages() if len(expect(g)[0]) > 2 and f" ({expect(g)[0][0]}) flood zones" in p)
        assert not check(pg, g), check(pg, g)
        w = expect(g)[0]
        muts = {"swap order": pg.replace(f"{w[0]}</span>, <span data-name>{w[1]}", f"{w[1]}</span>, <span data-name>{w[0]}", 1),
                "foreign town": pg.replace(f"their ZIPs: <span data-name>{w[0]}<", "their ZIPs: <span data-name>Houston<", 1),
                "description town": pg.replace(f" ({w[0]}, ", " (Atlantis, ", 1),
                "title town": pg.replace(f" ({w[0]}) flood zones", " (Atlantis) flood zones", 1)}
        for k, mp in muts.items(): assert mp != pg and check(mp, g), f"mutation not caught: {k}"
        # T5 (r114): a page whose ranking leaves ZIP units out must say so; drop that line and the check must fire
        s5 = next(((s, g5, p5) for s, g5, p5 in pages() if "ZIPs where no single town covers at least a quarter of the land" in p5), None)
        if s5:
            assert not check(s5[2], s5[1]), check(s5[2], s5[1])
            m5 = re.sub(r"<p class='note'>ZIPs where no single town covers at least a quarter of the land.*?</p>", "", s5[2], count=1, flags=re.S)
            assert m5 != s5[2] and any(b.startswith("T5") for b in check(m5, s5[1])), "mutation not caught: left-out ZIP line dropped"
        print(f"town check mutations: {len(muts) + bool(s5)} caught ({sl}{', ' + s5[0] if s5 else ''})"); sys.exit()
    bad, n = [], 0
    for sl, g, pg in pages():
        n += 1; bad += [f"{sl}: {b}" for b in check(pg, g)]
    for b in bad[:20]: print("  -", b)
    print(f"TOWN CHECK {'FAIL' if bad else 'PASS'}: {n} county pages"); sys.exit(1 if bad else 0)
