"""Research papers (owner 11-12, PLAN "Paper standard"): every paper page, its CSV and every county page's rank line are
recomputed from data/all-counties/*.json with this file's own code (never imports papers.py or build_site.py: PLAN E22).
Also fails a paper page missing a required section. Usage: python -I tools/index_check.py [--test]"""
import csv, glob, io, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "dist")
# key: (value path, n path, minimum) -- typed here on purpose, a second copy of the spec (a drift fails the check)
PAPERS = {"price-gap": (("policies", "share_below"), ("policies", "below_n"), 100),
          "outside-the-zone": (("claims_extra", "outside_sfha_pct"), ("claims_extra", "paid_n"), 100)}
READY = set()   # mirrors papers.READY on purpose (own copy): both off after methods review 162
PAPERS = {k: v for k, v in PAPERS.items() if k in READY}
SECTIONS = ["abstract", "data", "methods", "results", "table", "limitations", "reproduce", "cite"]

def truth(recs, key):
    vp, np_, mn = PAPERS[key]
    def g(r, p):
        for k in p: r = r.get(k) if isinstance(r, dict) else None
        return r
    rows = {c: (g(r, vp), g(r, np_)) for c, r in recs.items()}
    rows = {c: (v, n) for c, (v, n) in rows.items() if isinstance(v, (int, float)) and isinstance(n, int) and n >= mn and 0 <= v <= 100}
    vals = [v for v, _ in rows.values()]
    return {c: (v, n, 1 + sum(x > v for x in vals), vals.count(v) > 1) for c, (v, n) in rows.items()}

def check(key, page, csv_text, county_pages, T, live):
    bad = [f"{key}: section '{s}' missing" for s in SECTIONS if f'id="{s}"' not in page]
    got = re.findall(r'<tr><td>(\d+)( \(tied\))?</td><td>(?:<a href="/flood-insurance/([a-z0-9-]+)/">)?([^<]+)(?:</a>)?</td><td>([\d.]+)%</td>(?:<td>[^<]*</td>)*?<td>([\d,]+)</td></tr>', page)
    if len(got) != len(T): bad.append(f"{key}: page has {len(got)} rows, data has {len(T)}")
    rd = list(csv.DictReader(io.StringIO(csv_text or "")))
    if len(rd) != len(T): bad.append(f"{key}: CSV has {len(rd)} rows, data has {len(T)}")
    for r in rd:
        t = T.get(r.get("county_fips"))
        if not t: bad.append(f"{key}: CSV row {r.get('county_fips')} not in data"); continue
        if (float(r[[k for k in r if k.endswith("_pct")][0]]), int(r["n"]), int(r["rank"]), r["tied"] == "True") != (t[0], t[1], t[2], t[3]):
            bad.append(f"{key}: CSV {r['county_fips']} {dict(r)} vs data {t}")
    want = sorted(T.values(), key=lambda t: (t[2]))
    for (rk, tied, slug, nm, sh, n), t in zip(got, want):
        if (int(rk), bool(tied), float(sh)) != (t[2], t[3], t[0]): bad.append(f"{key}: page row {nm} #{rk}{tied} {sh}% vs data #{t[2]} {t[0]}%")
    if [int(g[0]) for g in got] != sorted(int(g[0]) for g in got): bad.append(f"{key}: page not in rank order")
    for c, slug in live.items():
        h = county_pages.get(slug)
        if h is None: continue
        mm = re.search(rf'data-paper="{key}" data-rank="(\d+)"(?: data-of="(\d+)")?', h)
        if not mm: bad.append(f"{slug}: no {key} line"); continue
        exp = (T[c][2], len(T)) if c in T else (0, None)
        if (int(mm[1]), int(mm[2]) if mm[2] else None) != exp: bad.append(f"{slug}: {key} says #{mm[1]} of {mm[2]}, data #{exp[0]} of {exp[1]}")
    return bad

if __name__ == "__main__":
    recs = {os.path.basename(f)[:5]: json.load(open(f)) for f in glob.glob(os.path.join(ROOT, "data", "all-counties", "*.json"))}
    live = {p["geoid"]: p["slug"] for p in json.load(open(os.path.join(ROOT, "places.json")))}
    cp = {s: open(os.path.join(D, "flood-insurance", s, "index.html"), encoding="utf-8").read() for s in live.values()
          if os.path.exists(os.path.join(D, "flood-insurance", s, "index.html"))}
    allbad = []
    for key in PAPERS:
        T = truth(recs, key)
        pp, cv = os.path.join(D, "flood-insurance", key, "index.html"), os.path.join(D, "data", f"{key}.csv")
        page = open(pp, encoding="utf-8").read() if os.path.exists(pp) else ""
        csv_text = open(cv, encoding="utf-8").read() if os.path.exists(cv) else ""
        if "--test" in sys.argv:
            c0 = next(iter(T)); v0 = T[c0][0]
            muts = {"section dropped": (page.replace('id="limitations"', 'id="x"'), csv_text, cp),
                    "row dropped": (re.sub(r"<tr><td>\d+.*?</tr>", "", page, count=1), csv_text, cp),
                    "share changed": (re.sub(r"(<tr><td>1(?: \(tied\))?</td><td>.*?</td><td>)([\d.]+)%", lambda m: m[1] + "0.1%", page, count=1), csv_text, cp),
                    "csv row dropped": (page, "\n".join(csv_text.splitlines()[:-1]) + "\n", cp),
                    "county rank wrong": (page, csv_text, {s: re.sub(rf'data-paper="{key}" data-rank="(\d+)"', lambda m: f'data-paper="{key}" data-rank="{int(m[1]) + 3}"', h, count=1) for s, h in cp.items()})}
            for k, (pg, cs, cps) in muts.items(): assert check(key, pg, cs, cps, T, live), f"{key}: missed {k}"
            assert not check(key, page, csv_text, cp, T, live), f"{key}: clean build flagged: {check(key, page, csv_text, cp, T, live)[:3]}"
            print(f"{key}: {len(muts)} mutations caught"); continue
        bad = check(key, page, csv_text, cp, T, live)
        allbad += bad
        print(f"{key}: {'FAIL' if bad else 'PASS'} ({len(T)} counties, {len(cp)} county pages)")
    for b in allbad[:12]: print("INDEX FAIL", b)
    sys.exit(1 if allbad else 0)
