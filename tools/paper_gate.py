"""Research paper gate, machine half (docs/PAPER-GATE-PROMPT.md, owner 11-12 "strictest, PubMed level"). For every paper page built:
M2.1 sections present in order; M2.3 banned words; M1.3 every table share has a 90% range; M1.1/M2.2 every row and every CSV line
recomputed from data/all-counties with this file's own code (never imports papers.py or build_site.py: PLAN E22); county cards
match; M2.6 FEMA attribution; M3.1 papers share under 30% of sentences. Usage: python -I tools/paper_gate.py [--test]"""
import csv, glob, io, json, math, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "dist")
# a second, independent copy of each paper's base: (numerator path, denominator path, minimum). A drift from papers.py fails.
BASES = {"underinsured": (("extras", "claims", "underinsured", "over"), ("extras", "claims", "underinsured", "n"), 100),
         "outside-the-zone": (("extras", "claims", "zone_split", "out_paid_n"), ("extras", "claims", "zone_split", "known_paid_n"), 100)}
SECTIONS = ["abstract", "question", "data", "methods", "results", "prior", "table", "limitations", "reproduce", "cite", "versions", "corrections"]
BANNED = re.compile(r"\b(best|worst|safest|most dangerous|peer[- ]reviewed|significant(ly)?|only published here|denied|forecast|will rise|because|due to|caused by|driven by)\b", re.I)

def g(r, p):
    for k in p: r = r.get(k) if isinstance(r, dict) else None
    return r

def ci(k, n):   # 90% Wilson, written out on its own (not papers.wilson)
    z = 1.6448536269514722; ph = k / n; den = 1 + z * z / n
    mid = (ph + z * z / (2 * n)) / den; half = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return round(100 * (mid - half), 1), round(100 * (mid + half), 1)

def truth(recs, key):
    nump, denp, mn = BASES[key]
    rows = [(c, g(r, nump), g(r, denp)) for c, r in recs.items()]
    rows = sorted([(c, k, n) for c, k, n in rows if isinstance(k, int) and isinstance(n, int) and n >= mn and 0 <= k <= n], key=lambda t: (-t[1] / t[2], t[0]))
    N = len(rows)
    def pol(c):   # policy units outside A and V today, from the county's own inside share (review outside-zone-2 M1)
        s_ = g(recs[c], ("policies", "sfha_share_units"))
        return round(100 - s_, 1) if isinstance(s_, (int, float)) else None
    return [{"c": c, "k": k, "n": n, "v": round(100 * k / n, 1), "ci": ci(k, n), "fifth": 1 + 5 * i // N, "pol": pol(c)} for i, (c, k, n) in enumerate(rows)]

def text(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style|head)\b.*?</\1>", " ", h)))

def check(key, page, csv_text, cards, T):
    bad = []
    pos = [page.find(f'id="{s}"') for s in SECTIONS]
    if -1 in pos: bad.append(f"{key}: missing sections {[s for s, p in zip(SECTIONS, pos) if p < 0]}")
    elif pos != sorted(pos): bad.append(f"{key}: sections out of order")
    for m in BANNED.finditer(text(page)): bad.append(f"{key}: banned word '{m[0]}'")
    if "not endorsed by FEMA" not in page: bad.append(f"{key}: no FEMA attribution")
    rows = re.findall(r"<tr><td>(\w+) fifth</td><td>.*?</td><td>([\d.]+)%</td><td>([\d.]+)–([\d.]+)%</td><td>([\d,]+) of ([\d,]+)</td>(?:<td>[^<]*</td>)*</tr>", page)
    if not rows: bad.append(f"{key}: no table rows with a 90% range")
    want = T if len(T) <= 500 else T[:100] + T[-100:]
    if len(rows) != len(want): bad.append(f"{key}: table {len(rows)} rows, recompute {len(want)}")
    for (fw, v, lo, hi, k, n), t in zip(rows, want):
        if (float(v), (float(lo), float(hi)), int(k.replace(",", "")), int(n.replace(",", ""))) != (t["v"], t["ci"], t["k"], t["n"]):
            bad.append(f"{key}: row {t['c']} page {v}% {lo}-{hi} {k}/{n} vs {t['v']}% {t['ci']} {t['k']}/{t['n']}"); break
    if "Policy units outside A and V" in page:   # every printed policy share = recompute (or a dash where FEMA has none)
        pcol = re.findall(r"</td><td>[\d,]+ of [\d,]+</td><td>([\d.]+%|—)</td>", page)
        if len(pcol) != len(want) or any((p_ == "—") != (t["pol"] is None) or (p_ != "—" and float(p_[:-1]) != t["pol"]) for p_, t in zip(pcol, want)):
            bad.append(f"{key}: policy share column disagrees with recompute")
    cr = list(csv.DictReader(io.StringIO(csv_text or "")))
    if len(cr) != len(T): bad.append(f"{key}: CSV {len(cr)} rows, recompute {len(T)}")
    tc = {t["c"]: t for t in T}
    for r in cr:
        t = tc.get(r["county_fips"])
        if not t or (int(r["numerator"]), int(r["denominator"]), float(r["share_pct"]), (float(r["ci90_low_pct"]), float(r["ci90_high_pct"])), int(r["fifth"])) != (t["k"], t["n"], t["v"], t["ci"], t["fifth"]):
            bad.append(f"{key}: CSV row {r.get('county_fips')} disagrees with recompute"); break
    for c, h in cards.items():   # every county page: the card's share and fifth = recompute, or "not listed" when not in T
        m = re.search(rf'data-paper="{key}" data-fifth="(\d)"', h)
        if not m: bad.append(f"{c}: no {key} line"); continue
        if int(m[1]) != (tc[c]["fifth"] if c in tc else 0): bad.append(f"{c}: {key} fifth {m[1]} vs {tc[c]['fifth'] if c in tc else 0}")
    return bad

def sameness(pages):   # M3.1 (our threshold): any two papers share under 30% of sentences (numbers masked)
    sets = {k: {re.sub(r"[\d.,%$]+", "#", s) for s in re.split(r"(?<=[.!?])\s+", text(h)) if len(s.split()) >= 6} for k, h in pages.items()}
    ks = sorted(sets); bad = []
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            sh = len(sets[a] & sets[b]) / max(1, min(len(sets[a]), len(sets[b])))
            if sh >= 0.30: bad.append(f"{a} vs {b}: {round(100 * sh)}% shared sentences (limit 30%)")
    return bad

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I drops the script dir
    import papers   # only to learn which papers are switched on, never for figures
    ready = [s["key"] for s in papers.READY]
    if set(ready) - set(BASES): sys.exit(f"PAPER GATE FAIL: no independent base for {sorted(set(ready) - set(BASES))}")
    if not ready: print("PAPER GATE: no paper switched on"); sys.exit(0)
    recs = {os.path.basename(f)[:5]: json.load(open(f)) for f in glob.glob(os.path.join(ROOT, "data", "all-counties", "*.json"))}
    live = {p["geoid"]: p["slug"] for p in json.load(open(os.path.join(ROOT, "places.json")))}
    cards = {c: open(os.path.join(D, "flood-insurance", s, "index.html"), encoding="utf-8").read() for c, s in live.items()
             if os.path.exists(os.path.join(D, "flood-insurance", s, "index.html"))}
    pages, bad = {}, []
    for key in ready:
        pp, cv = os.path.join(D, "flood-insurance", key, "index.html"), os.path.join(D, "data", f"{key}.csv")
        page = open(pp, encoding="utf-8").read() if os.path.exists(pp) else ""; csv_text = open(cv, encoding="utf-8").read() if os.path.exists(cv) else ""
        T = truth(recs, key); pages[key] = page
        if "--test" in sys.argv:
            muts = {"section dropped": (page.replace('id="limitations"', 'id="x"'), csv_text, cards),
                    "banned word": (page.replace("</h1>", " the worst counties</h1>", 1), csv_text, cards),
                    "share changed": (re.sub(r"(<td>\w+ fifth</td><td>.*?</td><td>)([\d.]+)%", lambda m: m[1] + "0.1%", page, count=1), csv_text, cards),
                    "range dropped": (re.sub(r"<td>[\d.]+–[\d.]+%</td>", "<td></td>", page, count=1), csv_text, cards),
                    "csv row dropped": (page, "\n".join(csv_text.splitlines()[:-1]) + "\n", cards),
                    "policy share wrong": (re.sub(r"(</td><td>[\d,]+ of [\d,]+</td><td>)([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1) if "Policy units outside" in page else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "card fifth wrong": (page, csv_text, {c: re.sub(rf'data-paper="{key}" data-fifth="(\d)"', lambda m: f'data-paper="{key}" data-fifth="{(int(m[1]) % 5) + 1}"', h, count=1) for c, h in cards.items()})}
            for k, (pg, cs, cd) in muts.items(): assert check(key, pg, cs, cd, T), f"{key}: missed {k}"
            assert not check(key, page, csv_text, cards, T), check(key, page, csv_text, cards, T)[:3]
            print(f"{key}: {len(muts)} mutations caught"); continue
        bad += check(key, page, csv_text, cards, T)
        print(f"{key}: {len(T)} counties recomputed")
    if "--test" not in sys.argv: bad += sameness(pages)
    for b in bad[:15]: print("PAPER GATE FAIL", b)
    print("PAPER GATE", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
