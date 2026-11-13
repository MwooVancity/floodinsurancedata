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
    sec = page[page.find('id="counties"'):]; sec = sec[:sec.find("</div>")]
    st_of = {g: json.load(open(os.path.join(D, "all-counties", g + ".json"))).get("state", "") for g in rows}   # audit 11-10: names checked, not skipped
    tbl = sorted((c[0], int(c[1].replace(",", "")), _num(c[2])) for c in _cells(sec))
    if tbl != sorted((cname(g, st_of[g]), *v) for g, v in rows.items()): bad.append("C2 page table (county name + numbers) differs from data")
    ma = re.search(r"the U\.S\. share would be ([\d.]+)%", text)
    if not ma or float(ma[1]) != alt: bad.append(f"C5 share counting error-coded records: page {ma and ma[1]} vs {alt}")
    yb = {}   # C6 (11-09): the ten costliest loss years, summed from every state's agg.json
    for p in glob.glob(os.path.join(D, "states", "*", "agg.json")):
        for y, (cn, cp) in json.load(open(p))["claims"]["by_year"].items():
            yb.setdefault(int(y), [0, 0]); yb[int(y)][0] += cn; yb[int(y)][1] += cp
    want = [(y, v[0], v[1]) for y, v in sorted(yb.items(), key=lambda kv: -kv[1][1])[:10]]
    ys = page[page.find('id="years"'):page.find('id="counties"')]
    gy = [(int(a), int(b.replace(",", "")), int(c.replace(",", ""))) for a, b, c in re.findall(r"<tr><td>(\d{4})</td><td>([\d,]+)</td><td>\$([\d,]+)</td></tr>", ys)]
    if gy != want: bad.append(f"C6 costliest years differ: page {gy[:2]} vs data {want[:2]}")
    sz = sorted(c["paid_building_median"] for p in glob.glob(os.path.join(D, "states", "*", "extras.json"))   # C7: claim-size range
                for c in [json.load(open(p))["claims"]] if c.get("paid_building_median") and (c.get("damage_n") or 0) >= 500)
    csf = os.path.join(D, "us", "claim_size.json"); cs = json.load(open(csf)) if os.path.exists(csf) else {}   # C7b: the U.S. median, same as-of only
    if cs.get("p50") and cs.get("asof") == json.load(open(os.path.join(D, "us", "asof.json")))["asof"] and \
            f"the median paid building claim is ${cs['p50']:,}, on {cs['n']:,} claims" not in text: bad.append("C7b U.S. median paid building claim missing or differs")
    ms = re.search(r"median paid building claim runs from \$([\d,]+) in .*? to \$([\d,]+) in .*?, among the (\d+) states with", text)
    if len(sz) >= 2 and (not ms or (int(ms[1].replace(",", "")), int(ms[2].replace(",", "")), int(ms[3])) != (sz[0], sz[-1], len(sz))):
        bad.append(f"C7 claim-size range: page {ms and ms.groups()} vs ${sz[0]:,}-${sz[-1]:,} in {len(sz)}")
    for f in glob.glob(os.path.join(ROOT, "dist", "**", "*.html"), recursive=True):   # C8 (hater r124): codes 98/99 are out of every count, so
        for m in re.finditer(r"every claim record, paid or not(?!, except records FEMA coded)", open(f, encoding="utf-8").read()):   # "every record" must say so
            bad.append(f"C8 {os.path.relpath(f, ROOT)}: 'every claim record' without the error-code exclusion"); break
    for f in glob.glob(os.path.join(ROOT, "dist", "**", "*.html"), recursive=True):   # C8b (audit 11-10): records coded 98/99 are left out of every count (agg_raw)
        if re.search(r"includ\w*[^.<]{0,40}(?:coded|entered)[^.<]{0,30}in error", open(f, encoding="utf-8").read()):
            bad.append(f"C8b {os.path.relpath(f, ROOT)}: says error-coded records are included; every count leaves them out"); break
    if re.search(r"\bdenied\b", text.replace("does not mean a claim was denied", ""), re.I): bad.append("C4 'denied' printed")
    return bad + check_stories(page) + check_bycounty(page)

def check_bycounty(page, bcv=None):   # C12 (audit 11-10, "nfip claims by county"): top 25 by dollars paid, the county count, title, CSV of every county
    want = {}
    for p in glob.glob(os.path.join(D, "all-counties", "*.json")):
        c = json.load(open(p)).get("claims") or {}
        if c.get("rows"): want[os.path.basename(p)[:-5]] = (c["rows"], c["total_paid"])
    bad = []
    if "NFIP claims by county" not in (re.search(r"<title>(.*?)</title>", page) or [None, ""])[1]: bad.append("C12 title lacks 'NFIP claims by county'")
    i = page.find('id="bycounty"')
    if i < 0: return bad + [f"C12 card missing ({len(want)} counties in the data)"]
    sec = page[i:page.find("</div>", i)]; txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sec))
    top = sorted(want.values(), key=lambda v: -v[1])[:25]
    got = [(int(a.replace(",", "")), int(b.replace(",", ""))) for a, b in re.findall(r"<tr><td>(?:<a [^>]*>)?[^<]*(?:</a>)?</td><td>([\d,]+)</td><td>\$([\d,]+)</td></tr>", sec)]
    if got != top: bad.append(f"C12 top-25 rows differ from data or order: page {got[:2]} vs {top[:2]}")
    if f"of the {len(want):,} counties with at least one NFIP claim on record" not in txt: bad.append(f"C12 county count not {len(want):,}")
    bp = os.path.join(ROOT, "dist", "data", "claims-by-county.csv")
    if bcv is None: bcv = open(bp, encoding="utf-8").read() if os.path.exists(bp) else ""
    gc = {r["county_fips"]: (int(r["claims_on_record"]), int(r["paid_usd"])) for r in csv.DictReader(bcv.splitlines())}
    if gc != want: bad.append(f"C12 CSV differs: {len(gc)} rows vs {len(want)}")
    return bad

HEADS = {   # label = definition (audit 11-10: swapped headers passed); a new wording is a deliberate change made here too
    "outside": ("Flood claims rated outside the high-risk zones, county by county",
                ["County", "Claims with a zone", "Rated outside A and V", "Claims rated outside A and V: share of dollars paid on claims with a zone"]),
    "cause": ("Rain, river or tide: what FEMA records as the cause of paid flood claims, county by county",
              ["County", "Paid claims with a cause", "Rain or snowmelt", "River, stream or lake overflow", "Tidal water overflow"]),
    "moved": ("Zone on the claim vs the zone FEMA lists now: claims rated outside zones A and V",
              ["County", "Claims rated outside A and V, current zone listed", "Current zone A or V"])}
_NAMES = None
def cname(g, st):   # "Harris County, TX" from the Census name file and the county file's own state
    global _NAMES
    if _NAMES is None: _NAMES = json.load(open(os.path.join(D, "us", "county_names.json"), encoding="utf-8"))
    return f"{_NAMES.get(g, g)}, {st}"
def flat(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

def expect_stories():   # 11-10 story tables, from the county files alone: {story: {fips: (name, n, shares...)}}, left-out counts, loss years
    want, left, yrs = {"outside": {}, "cause": {}, "moved": {}}, {"outside": 0, "cause": 0, "moved": 0}, {"outside": set(), "cause": set(), "moved": set()}
    r1 = lambda a, b: round(100 * a / b, 1) if b else None   # audit 11-10: a 500+ county with $0 paid stays in the table (share "—"), never in "1 to 499"
    for p in glob.glob(os.path.join(D, "all-counties", "*.json")):
        g = os.path.basename(p)[:-5]; j = json.load(open(p)); c = (j.get("extras") or {}).get("claims") or {}; nm = cname(g, j.get("state", ""))
        z, k, m = c.get("zone_split") or {}, c.get("cause10") or {}, c.get("moved") or {}
        if z.get("known_n"):
            if z["known_n"] >= 500: want["outside"][g] = (nm, z["known_n"], r1(z["out_n"], z["known_n"]), r1(z.get("out_paid", 0), z.get("known_paid", 0))); yrs["outside"].add((z["from"], z["to"]))
            else: left["outside"] += 1
        if k.get("with_cause"):
            n = k["with_cause"]; b = k["by_code"]
            if n >= 500: want["cause"][g] = (nm, n, r1(b.get("4", 0), n), r1(b.get("2", 0), n), r1(b.get("1", 0), n)); yrs["cause"].add((k["from"], k["to"]))
            else: left["cause"] += 1
        if m.get("rated_out_known"):
            if m["rated_out_known"] >= 500: want["moved"][g] = (nm, m["rated_out_known"], r1(m["now_av"], m["rated_out_known"])); yrs["moved"].add((m["from"], m["to"]))
            else: left["moved"] += 1
    return want, left, yrs

def _cells(sec):   # every body row as its flat cell texts
    return [[flat(c) for c in re.findall(r"<td>(.*?)</td>", r, re.S)] for r in re.findall(r"<tr><td>.*?</tr>", sec, re.S)]
def _num(x): return None if x in ("—", "") else float(x.rstrip("%").replace(",", "").lstrip("$"))

def check_stories(page, scv=None):   # C9 outside zones, C10 cause, C11 moved: rows (name + numbers), rank, headers, years, lede, left-out label, CSV
    bad = []; want, left, yrs = expect_stories()
    sp = os.path.join(ROOT, "dist", "data", "claims-stories-counties.csv")
    if scv is None: scv = open(sp, encoding="utf-8").read() if os.path.exists(sp) else ""
    story = {"outside_zones_a_v": "outside", "cause_rain_river_tide": "cause", "rated_outside_now_a_v": "moved"}
    got = {"outside": {}, "cause": {}, "moved": {}}
    for r in csv.DictReader(scv.splitlines()):
        v = [_num(r[c]) for c in ("share_pct", "second_share_pct", "third_share_pct")][:len(HEADS[story[r["story"]]][1]) - 2]
        got[story[r["story"]]][r["county_fips"]] = (f'{r["county"]}, {r["state"]}', int(r["claims_in_base"]), *v)
    for code, s in (("C9", "outside"), ("C10", "cause"), ("C11", "moved")):
        w = want[s]
        i = page.find(f'id="{s}"')
        if len(w) < 2:
            if i >= 0: bad.append(f"{code} card printed with fewer than 2 counties")
            continue
        if i < 0: bad.append(f"{code} card missing ({len(w)} counties in the data)"); continue
        sec = page[i:page.find("</div>", i)]; txt = flat(sec)
        h2, ths = HEADS[s]
        if flat((re.search(r"<h2>(.*?)</h2>", sec, re.S) or [None, ""])[1]) != h2: bad.append(f"{code} heading differs from its definition")
        if [flat(x) for x in re.findall(r"<th>(.*?)</th>", sec, re.S)] != ths: bad.append(f"{code} column headers differ from their definitions")
        if len(yrs[s]) != 1: bad.append(f"{code} counties have different loss-year spans {sorted(yrs[s])}: one label cannot cover them")
        else:
            y0, y1 = next(iter(yrs[s]))
            if not txt.count(f"Losses {y0}–{y1}:") == 1 or re.search(r"Losses \d{4}–\d{4}", txt.replace(f"Losses {y0}–{y1}", "")): bad.append(f"{code} loss years not 'Losses {y0}–{y1}'")
        tup = [(c[0], int(c[1].replace(",", "")), *map(_num, c[2:])) for c in _cells(sec)]
        if sorted(tup, key=str) != sorted(w.values(), key=str): bad.append(f"{code} table rows (county name + numbers) differ from data: {len(tup)} rows vs {len(w)}")
        if [t[2] for t in tup] != sorted((t[2] for t in tup), reverse=True): bad.append(f"{code} not ranked by value")
        if got[s] != w: bad.append(f"{code} CSV (names or numbers) differs from data")
        lo = min(w.values(), key=lambda t: (t[2], t[0])); hi = max(w.values(), key=lambda t: (t[2], [-ord(ch) for ch in t[0]]))
        mr = re.search(r"runs from ([\d.]+)% in (.*?) to ([\d.]+)% in (.*?), (?:among|in) the (\d+) counties", txt)
        if not mr or (float(mr[1]), float(mr[3]), int(mr[5])) != (lo[2], hi[2], len(w)) or \
                mr[2].strip() not in [t[0] for t in w.values() if t[2] == lo[2]] or mr[4].strip() not in [t[0] for t in w.values() if t[2] == hi[2]]:
            bad.append(f"{code} lede range or its counties {mr and mr.groups()} vs {lo[2]}% {lo[0]} to {hi[2]}% {hi[0]} in {len(w)}")
        if f"Left out: counties with 1 to 499 such claims ({left[s]:,} counties)" not in txt: bad.append(f"{code} left-out label missing or not '1 to 499 ... ({left[s]:,} counties)'")
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
    if 'except records FEMA coded "deleted in error" or "assigned in error"' not in text: bad.append("N5 claims count lacks the error-code exclusion (audit 11-10)")
    for want, label in ((f"had {units:,} policy units", "N1 units"), (f"median of ${med:,} a year", "N2 median"),
                        (f"list {claims:,} NFIP claims, paid or not, and ${paid:,} paid in total", "N3 claims"), (f"${paid / 1e9:.1f}B", "N4 paid tile")):
        if want not in text: bad.append(f"{label}: '{want}' not on the page")
    return bad

def check_renters(page):   # /flood-insurance/renters/: lede, tiles and state rows recomputed from renter_hist.json alone
    h = json.load(open(os.path.join(D, "us", "renter_hist.json")))
    def q(hs, p):
        vs = sorted((int(k), c) for v in hs for k, c in v.items()); tot = sum(c for _, c in vs); run = 0
        for v, c in vs:
            run += c
            if run >= tot * p: return v
    n = sum(sum(v.values()) for v in h.values()); lo, md, hi = (q(h.values(), p) for p in (0.25, 0.5, 0.75))
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)); bad = []
    if f"paid a median of ${md:,} a year, premium plus fees, across {n:,} priced renter policies" not in text: bad.append(f"R1 lede: ${md:,} on {n:,}")
    if f"The middle half paid ${lo:,} to ${hi:,}." not in text: bad.append(f"R2 middle half ${lo:,}-${hi:,}")
    want = sorted((sum(v.values()), q([v], 0.5)) for v in h.values() if sum(v.values()) >= 30)
    got = sorted((int(b.replace(",", "")), int(a.replace(",", ""))) for a, b in re.findall(r"<tr><td>(?:<a [^>]*>)?[^<]*(?:</a>)?</td><td>\$([\d,]+)</td><td>([\d,]+)</td></tr>", page))
    if got != want: bad.append(f"R3 state rows {len(got)} vs {len(want)}")
    return bad

def check_guides(page, zone_x):   # /guides/homeowners-insurance-flooding/: claims shares recomputed from claims_zone.json, no build_site code
    z = json.load(open(os.path.join(D, "us", "claims_zone.json")))
    rows = [(k, c) for v in z.values() for k, c in v["by_zone"].items() if k and k != "blank"]   # 11-12: blank = no zone, never "outside"
    alld = sum(c["paid"] for _, c in rows); out = sum(c["paid"] for k, c in rows if k.strip().upper()[:1] not in ("A", "V"))
    n, pn = sum(c["n"] for _, c in rows), sum(c["paid_n"] for _, c in rows); pc = round(100 * out / alld)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)); bad = []
    if f"{pn:,} of the {n:,} claims with a rated zone had a payment, and {pc}% of the dollars" not in text: bad.append(f"G1 claims line: {pn:,} of {n:,}, {pc}%")
    if f">{pc}%<" not in page: bad.append(f"G2 tile {pc}%")
    zx = re.search(r"Of all paid claim dollars with a zone on the claim, (\d+)%", re.sub(r"<[^>]+>", "", zone_x or ""))
    if not zx or int(zx[1]) != pc: bad.append(f"G3 zone X page says {zx[1] if zx else 'nothing'}%, guide {pc}%: one measure, two numbers")
    return bad

def check_condo(page):   # condo guide: every state row recomputed from data/states/*/extras.json (11-12)
    rows = []
    for p in glob.glob(os.path.join(D, "states", "*", "extras.json")):
        x = json.load(open(p))["policies"]
        if x.get("condo_unit_cost_median"): rows.append((x["condo_unit_cost_n"], x["condo_unit_cost_median"]))
    want = sorted(rows)
    got = sorted((int(b.replace(",", "")), int(a.replace(",", ""))) for a, b in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>\$([\d,]+)</td><td>([\d,]+)</td></tr>', page))
    return [] if got == want else [f"C1 condo rows {len(got)} vs {len(want)} recomputed"]

def check_deductible(page):   # deductible guide: shares recomputed from every state's deductibles_by_zone counts (11-13)
    dz = {}
    for p in glob.glob(os.path.join(D, "states", "*", "extras.json")):
        for zg, cn in (json.load(open(p))["policies"].get("deductibles_by_zone") or {}).items():
            for d, c in cn.items(): dz.setdefault(zg, {}); dz[zg][d] = dz[zg].get(d, 0) + c
    n = {z: sum(dz.get(z, {}).values()) for z in ("AE", "X")}
    bad = [] if f"{n['AE']:,} rated zone AE, {n['X']:,} rated zone X" in re.sub(r"<[^>]+>", "", page) else [f"D1 base counts {n}"]
    # r169/r170: the X group is zones X, B and C; "zone X" alone in a title, lede or heading mislabels the base
    lab = re.sub(r"<[^>]+>", " ", re.sub(r'<table.*?</table>|<p class="(?:stand|mut)">Share of.*?</p>', " ", page, flags=re.S))
    bad += [f"D3 label '{m_[0]}' names zone X without B and C" for m_ in re.finditer(r"zones? (?:AE and )?X\b(?!, B or C)", lab)]
    for amt, ae, x in re.findall(r"<tr><td>\$([\d,]+)</td><td>([\d.]+)%</td><td>([\d.]+)%</td></tr>", page):
        k = str(int(amt.replace(",", "")))
        want = (round(100 * dz["AE"].get(k, 0) / n["AE"], 1), round(100 * dz["X"].get(k, 0) / n["X"], 1))
        if (float(ae), float(x)) != want: bad.append(f"D2 ${amt}: page {ae}%/{x}%, recomputed {want}")
    return bad

def check_state_labels(pages):   # review r167 MAJOR: "48 states" counted DC. Every "N states" / "N states and DC" label = the table's rows
    bad = []
    for name, h in pages.items():
        rows = re.findall(r'<tr><td><a href="/flood-insurance/([a-z-]+)/">', h)
        dc = "district-of-columbia" in rows; n = len(rows) - dc
        for lab in set(re.findall(r"(\d+) states( and DC)?", re.sub(r"<[^>]+>", "", h))):
            if (int(lab[0]), bool(lab[1])) != (n, dc): bad.append(f"L1 {name}: says '{lab[0]} states{lab[1]}', table has {n} states{' and DC' if dc else ''}")
    return bad

if __name__ == "__main__":
    if "--guides" in sys.argv:
        gp = {os.path.basename(os.path.dirname(p)): open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(ROOT, "dist", "guides", "*", "index.html"))}
        lb = check_state_labels(gp)
        if "--test" in sys.argv:
            assert not lb, lb
            k = next(k for k, h in gp.items() if " states and DC" in h)
            assert check_state_labels({k: re.sub(r"(\d+) states and DC", lambda m_: f"{int(m_[1]) + 1} states", gp[k], count=1)}), "mutation not caught: DC counted as a state"
        elif lb:
            for b in lb: print("  -", b)
            print("GUIDES CHECK FAIL"); sys.exit(1)
        pg = open(os.path.join(ROOT, "dist", "guides", "homeowners-insurance-flooding", "index.html"), encoding="utf-8").read()
        zx = open(os.path.join(ROOT, "dist", "flood-zones", "x", "index.html"), encoding="utf-8").read()
        cg = open(os.path.join(ROOT, "dist", "guides", "condo-flood-insurance", "index.html"), encoding="utf-8").read()
        dg = open(os.path.join(ROOT, "dist", "guides", "flood-insurance-deductible", "index.html"), encoding="utf-8").read()
        bad = check_guides(pg, zx) + check_condo(cg) + check_deductible(dg)
        if "--test" in sys.argv:
            assert check_deductible(re.sub(r"<td>([\d.]+)%</td><td>([\d.]+)%</td></tr>", lambda m_: f"<td>{float(m_[1]) + 1}%</td><td>{m_[2]}%</td></tr>", dg, count=1)), "mutation not caught: deductible share"
            assert check_deductible(dg.replace("zone AE vs zones X, B or C", "zone AE vs zone X", 1)), "mutation not caught: zone X label"
        if "--test" in sys.argv:
            assert check_condo(re.sub(r"<td>\$([\d,]+)</td>", "<td>$1</td>", cg, count=1)), "mutation not caught: condo row"
            assert not bad, bad
            assert check_guides(re.sub(r">(\d+)%<", lambda m_: f">{int(m_[1]) + 1}%<", pg, count=1), zx), "mutation not caught: tile"
            assert check_guides(pg, re.sub(r"(zone on the claim, )(\d+)%", lambda m_: m_[1] + str(int(m_[2]) + 1) + "%", zx, count=1)), "mutation not caught: zone X disagrees"
            print("guides check mutations: 6 caught"); sys.exit()
        for b in bad: print("  -", b)
        print("GUIDES CHECK", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
    if "--renters" in sys.argv:
        f = os.path.join(ROOT, "dist", "flood-insurance", "renters", "index.html")
        if not os.path.exists(f): print("RENTERS CHECK: no page (floor not met)"); sys.exit()
        pg = open(f, encoding="utf-8").read(); bad = check_renters(pg)
        if "--test" in sys.argv:
            assert not bad, bad
            assert check_renters(re.sub(r"paid a median of \$[\d,]+", "paid a median of $1", pg, count=1)), "mutation not caught: median"
            assert check_renters(re.sub(r"</td><td>([\d,]+)</td></tr>", "</td><td>9</td></tr>", pg, count=1)), "mutation not caught: row"
            print("renters check mutations: 2 caught"); sys.exit()
        for b in bad: print("  -", b)
        print("RENTERS CHECK", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
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
                "row": pg[:pg.find('id="counties"')] + re.sub(r"(</td><td>[\d,]+</td><td>)([\d.]+)%", r"\g<1>1.0%", pg[pg.find('id="counties"'):], count=1),   # audit 11-10: slice, or it hits #outside
                "denied": pg + "<p>Claims denied.</p>",
                "size": re.sub(r"(claim runs from \$)[\d,]+", r"\g<1>1", pg, count=1),
                "year": re.sub(r'(id="years".*?<tr><td>\d{4}</td><td>[\d,]+</td><td>\$)([\d,]+)', r"\g<1>1", pg, count=1, flags=re.S)}
        if "the median paid building claim is $" in pg: muts["us median"] = re.sub(r"(the median paid building claim is \$)[\d,]+", r"\g<1>1", pg, count=1)
        for k, m in muts.items(): assert check(m, cv), f"mutation not caught: {k}"
        cv2 = cv.splitlines(); cv2.pop(1)
        assert check(pg, "\n".join(cv2)), "mutation not caught: csv row dropped"
        tf = os.path.join(ROOT, "dist", "_c8_mutation.html")   # C8 reads every built page: plant one with the old label
        try:
            open(tf, "w", encoding="utf-8").write("<p>NFIP claims on record: every claim record, paid or not, for losses from 1978.</p>")
            assert any(b.startswith("C8") for b in check(pg, cv)), "mutation not caught: claim-record label"
            open(tf, "w", encoding="utf-8").write("<p>These shares count every FEMA claim record, including ones FEMA coded as entered in error.</p>")
            assert any(b.startswith("C8b") for b in check(pg, cv)), "mutation not caught: error-coded included label"
        finally:
            os.remove(tf)
        o = pg.find('id="outside"')   # C9-C11 (11-10): a changed share, a swapped rank, a dropped CSV row
        if o >= 0:
            m1 = pg[:o] + re.sub(r"(</td><td>[\d,]+</td><td>)([\d.]+)%", r"\g<1>0.1%", pg[o:], count=1)
            assert any(b.startswith("C9") for b in check_stories(m1)), "mutation not caught: story share"
            rs = re.findall(r"<tr><td>.*?</tr>", pg[o:pg.find("</div>", o)])
            m2 = pg.replace(rs[0], "@@").replace(rs[1], rs[0]).replace("@@", rs[1])
            assert any("ranked" in b for b in check_stories(m2)), "mutation not caught: rank order"
            sv = open(os.path.join(ROOT, "dist", "data", "claims-stories-counties.csv"), encoding="utf-8").read().splitlines(); sv.pop(1)
            assert any("CSV" in b for b in check_stories(pg, "\n".join(sv))), "mutation not caught: story CSV row"
        b = pg.find('id="bycounty"')   # C12: a changed dollar figure, a swapped rank, a dropped CSV row
        assert b >= 0, "C12 card missing"
        m3 = pg[:b] + re.sub(r"(</td><td>[\d,]+</td><td>\$)([\d,]+)", r"\g<1>1", pg[b:], count=1)
        assert any(x.startswith("C12") for x in check_bycounty(m3)), "mutation not caught: by-county paid"
        rs = re.findall(r"<tr><td>.*?</tr>", pg[b:pg.find("</div>", b)])
        assert any(x.startswith("C12") for x in check_bycounty(pg.replace(rs[0], "@@").replace(rs[1], rs[0]).replace("@@", rs[1]))), "mutation not caught: by-county rank"
        bv = open(os.path.join(ROOT, "dist", "data", "claims-by-county.csv"), encoding="utf-8").read().splitlines(); bv.pop(1)
        assert any("CSV" in x for x in check_bycounty(pg, "\n".join(bv))), "mutation not caught: by-county CSV row"
        # audit 11-10: the label mutations that passed before (names, headers, years, wording), on every story card
        def swap_names(p_, at):
            sec = p_[at:p_.find("</div>", at)]; nm = re.findall(r"<tr><td>(.*?)</td>", sec, re.S)[:2]
            s2 = sec.replace(nm[0], "@@", 1).replace(nm[1], nm[0], 1).replace("@@", nm[1], 1); return p_[:at] + s2 + p_[at + len(sec):]
        n_lab = 0
        for code, sid in (("C9", "outside"), ("C10", "cause"), ("C11", "moved")):
            at = pg.find(f'id="{sid}"')
            if at < 0: continue
            sec = pg[at:pg.find("</div>", at)]; ths = re.findall(r"<th>.*?</th>", sec)
            muts = {"names swapped": swap_names(pg, at),
                    "headers swapped": pg[:at] + sec.replace(ths[-1], "@@").replace(ths[-2], ths[-1]).replace("@@", ths[-2]) + pg[at + len(sec):],
                    "years shifted": pg[:at] + re.sub(r"Losses (\d{4})–(\d{4})", lambda q: f"Losses {int(q[1]) - 10}–{int(q[2]) - 10}", sec, count=1) + pg[at + len(sec):],
                    "heading word": pg[:at] + re.sub(r"<h2>(\w+)", "<h2>Inside", sec, count=1) + pg[at + len(sec):],
                    "left-out floor": pg[:at] + sec.replace("1 to 499", "1 to 99") + pg[at + len(sec):],
                    "lede county": pg[:at] + re.sub(r"(runs from [\d.]+% in )(<a [^>]*>)?[^<,]+", r"\1Nowhere County", sec, count=1) + pg[at + len(sec):]}
            for k_, m_ in muts.items():
                assert any(x.startswith(code) for x in check_stories(m_)), f"mutation not caught: {sid} {k_}"; n_lab += 1
        o2 = pg.find('id="outside"'); s2 = pg[o2:pg.find("</div>", o2)]
        assert any(x.startswith("C9") for x in check_stories(pg[:o2] + s2.replace("share of dollars", "share of claims") + pg[o2 + len(s2):])), "mutation not caught: dollars label"
        sv = open(os.path.join(ROOT, "dist", "data", "claims-stories-counties.csv"), encoding="utf-8").read().splitlines()
        f1 = next(csv.reader([sv[1]])); sv[1] = sv[1].replace(f1[2], "Wrong County", 1)
        assert any("CSV" in x for x in check_stories(pg, "\n".join(sv))), "mutation not caught: CSV county name"
        assert any(x.startswith("C2") for x in check(swap_names(pg, pg.find('id="counties"')), cv)), "mutation not caught: C2 names swapped"
        print(f"claims_check mutations: {16 + n_lab} caught"); sys.exit()
    bad = check(pg, cv)
    for b in bad: print("  -", b)
    print("CLAIMS CHECK", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
