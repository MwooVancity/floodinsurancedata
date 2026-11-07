"""/flood-insurance/claims/: every figure recomputed from the data files by code that shares nothing with build_site.py.
Fails on: C1 lede total, share or county range differs; C2 a table row (claims, share) differs, a county with 500+
claims is missing or one under is listed; C3 the CSV differs from the table; C4 the word "denied" anywhere outside FEMA's
own reason labels. Usage: python -I tools/claims_check.py [--test]   (--test: each mutation must fail the check)"""
import csv, glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
ERR = {"98", "99"}

def expect():
    rows = {}
    for p in glob.glob(os.path.join(D, "all-counties", "*.json")):
        rc = ((json.load(open(p)).get("extras") or {}).get("claims") or {}).get("recent")
        if not rc: continue
        n = rc["n"] - sum(v for k, v in rc["unpaid_reasons"].items() if k in ERR)
        if n >= 500: rows[os.path.basename(p)[:-5]] = (n, round(100 * rc["paid_n"] / n, 1))
    us = [json.load(open(p))["claims"]["recent"] for p in glob.glob(os.path.join(D, "states", "*", "extras.json"))]
    n = sum(r["n"] - sum(v for k, v in r["unpaid_reasons"].items() if k in ERR) for r in us)
    e = sum(sum(v for k, v in r["unpaid_reasons"].items() if k in ERR) for r in us)
    return rows, n, round(100 * sum(r["paid_n"] for r in us) / n, 1), round(100 * sum(r["paid_n"] for r in us) / (n + e), 1)

def check(page, csvtext):
    bad = []; rows, n, pct, alt = expect()
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page))
    m = re.search(r"Of ([\d,]+) NFIP flood claims for losses from 2020 on, ([\d.]+)% had a recorded payment\. In the (\d+) counties .*? from ([\d.]+)% in .*? to ([\d.]+)% in", text)
    if not m: return ["C1 lede not found"]
    if int(m[1].replace(",", "")) != n or float(m[2]) != pct: bad.append(f"C1 lede {m[1]}/{m[2]}% vs {n:,}/{pct}%")
    if int(m[3]) != len(rows): bad.append(f"C1 county count {m[3]} vs {len(rows)}")
    if rows and (float(m[4]) != min(v[1] for v in rows.values()) or float(m[5]) != max(v[1] for v in rows.values())): bad.append("C1 range differs")
    got = {}
    for r in csv.DictReader(csvtext.splitlines()):
        got[r["county_fips"]] = (int(r["claims_loss_year_2020_on"]), float(r["share_with_payment_pct"]))
    if got != rows: bad.append(f"C2/C3 CSV rows differ: {len(got)} vs {len(rows)} expected; first diff {next(((k, got.get(k), rows.get(k)) for k in set(got) | set(rows) if got.get(k) != rows.get(k)), None)}")
    sec = page[page.find('id="counties"'):]
    tbl = re.findall(r"<tr><td>(?:<a [^>]*>)?[^<]*(?:</a>)?</td><td>([\d,]+)</td><td>([\d.]+)%</td>", sec)
    if sorted((int(a.replace(",", "")), float(b)) for a, b in tbl) != sorted(rows.values()): bad.append("C2 page table differs from data")
    ma = re.search(r"the U\.S\. share would be ([\d.]+)%", text)
    if not ma or float(ma[1]) != alt: bad.append(f"C5 share counting error-coded records: page {ma and ma[1]} vs {alt}")
    if re.search(r"\bdenied\b", text.replace("does not mean a claim was denied", ""), re.I): bad.append("C4 'denied' printed")
    return bad

def check_nfip(page):   # /nfip/: lede and tiles recomputed from built.json + cost_hist.json, sharing no code with build_site
    st = json.load(open(os.path.join(D, "states", "built.json")))
    units, claims, paid = sum(s["units"] for s in st), sum(s["claims"] for s in st), sum(s["paid"] for s in st)
    h = json.load(open(os.path.join(D, "us", "cost_hist.json")))
    vs = sorted((int(k), c) for v in h.values() for k, c in v.items()); tot = sum(c for _, c in vs); run = 0
    for med, c in vs:
        run += c
        if run >= tot / 2: break
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)); bad = []
    for want, label in ((f"had {units:,} policy units", "N1 units"), (f"median of ${med:,} a year", "N2 median"),
                        (f"list {claims:,} NFIP claims, paid or not, and ${paid:,} paid in total", "N3 claims"), (f"${paid / 1e9:.1f}B", "N4 paid tile")):
        if want not in text: bad.append(f"{label}: '{want}' not on the page")
    return bad

if __name__ == "__main__":
    if "--nfip" in sys.argv:
        pg = open(os.path.join(ROOT, "dist", "nfip", "index.html"), encoding="utf-8").read()
        bad = check_nfip(pg)
        if "--test" in sys.argv:
            assert not bad, bad
            assert check_nfip(pg.replace(" policy units in force on", "9 policy units in force on", 1)), "mutation not caught: units"
            assert check_nfip(re.sub(r"\$[\d.]+B", "$1.0B", pg, count=1)), "mutation not caught: paid tile"
            print("nfip check mutations: 2 caught"); sys.exit()
        for b in bad: print("  -", b)
        print("NFIP CHECK", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
    pg = open(os.path.join(ROOT, "dist", "flood-insurance", "claims", "index.html"), encoding="utf-8").read()
    cv = open(os.path.join(ROOT, "dist", "data", "claims-2020-counties.csv"), encoding="utf-8").read()
    if "--test" in sys.argv:
        assert not check(pg, cv), check(pg, cv)
        muts = {"lede": re.sub(r"(had a recorded payment)", r"\1", re.sub(r"([\d.]+)% had a recorded", "12.3% had a recorded", pg, count=1)),
                "row": re.sub(r"(</a></td><td>[\d,]+</td><td>)([\d.]+)%", r"\g<1>1.0%", pg, count=1) if "</a></td><td>" in pg else pg.replace("%</td>", "1%</td>", 1),
                "denied": pg + "<p>Claims denied.</p>"}
        for k, m in muts.items(): assert check(m, cv), f"mutation not caught: {k}"
        cv2 = cv.splitlines(); cv2.pop(1)
        assert check(pg, "\n".join(cv2)), "mutation not caught: csv row dropped"
        print("claims_check mutations: 4 caught"); sys.exit()
    bad = check(pg, cv)
    for b in bad: print("  -", b)
    print("CLAIMS CHECK", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
