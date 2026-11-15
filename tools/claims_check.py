"""/flood-insurance/claims/: every figure recomputed from the data files by code that shares nothing with build_site.py.
Fails on: C1 lede total, share or county range differs; C2 a table row (claims, share) differs, a county with 500+
claims is missing or one under is listed; C3 the CSV differs from the table; C4 the word "denied" anywhere outside FEMA's
own reason labels. Usage: python -I tools/claims_check.py [--test]   (--test: each mutation must fail the check)"""
import collections, csv, glob, json, os, re, sys
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
    return bad + check_stories(page) + check_bycounty(page) + check_icc(text)

def check_icc(text):   # C13 (11-13, claim guide folded in): paid claims with an ICC payment, summed from every state's extras.json
    ex = [json.load(open(p))["claims"] for p in glob.glob(os.path.join(D, "states", "*", "extras.json"))]
    m = re.search(r"Of the ([\d,]+) NFIP claims with a recorded payment for losses from \d{4} to \d{4}, all 50 states and DC, ([\d,]+) \(([\d.]+)%\) include an Increased Cost of Compliance payment", text)
    if len(ex) != 51 or any(c.get("icc_claims") is None for c in ex):
        return ["C13 ICC sentence printed with states missing"] if m else []
    i, n = sum(c["icc_claims"] for c in ex), sum(c["paid_n"] for c in ex)
    if not m: return ["C13 ICC sentence missing"] if i else []
    return [] if (int(m[1].replace(",", "")), int(m[2].replace(",", "")), float(m[3])) == (n, i, round(100 * i / n, 1)) else [f"C13 ICC {m.groups()} vs {n:,}/{i:,}"]

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
    hi = {z: round(100 * sum(c for d, c in dz[z].items() if float(d) >= 5000) / n[z], 1) for z in ("AE", "X")}   # lede, from counts
    if f"{hi['AE']}% of zone AE policies carry one of $5,000 or more, against {hi['X']}%" not in page: bad.append(f"D4 lede $5,000+ shares, recomputed {hi}")
    return bad

def check_vents(page):   # vents guide: obstruction shares and state rows recomputed from every state's obstruction_counts (11-13)
    tot, rows = {}, []
    for p in glob.glob(os.path.join(D, "states", "*", "extras.json")):
        oc = json.load(open(p))["policies"].get("obstruction_counts") or {}
        for k, v in oc.items(): tot[k] = tot.get(k, 0) + v
        kn = sum(v for k, v in oc.items() if k != "blank")
        if kn >= 100: rows.append((kn, round(100 * oc.get("15", 0) / kn, 1)))
    kn = sum(v for k, v in tot.items() if k != "blank"); bad = []
    if f"{round(100 * tot.get('15', 0) / kn, 1)}%" not in page or f"{kn:,}" not in page: bad.append(f"V1 tile: code 15 {round(100 * tot.get('15', 0) / kn, 1)}% of {kn:,}")
    got = sorted((int(n.replace(",", "")), float(sh)) for sh, n in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>([\d.]+)%</td><td>([\d,]+)</td></tr>', page))
    if got != sorted(rows): bad.append(f"V2 state rows {len(got)} vs {len(rows)}")
    return bad

def check_private(page):   # private flood guide (11-13): U.S. share from state shares with rounding bounds, state rows, no brand words (G4)
    rows = [json.load(open(p))["policies"] for p in glob.glob(os.path.join(D, "states", "*", "extras.json"))]
    rows = [x for x in rows if x.get("replacement_over_250k_pct") is not None and (x.get("replacement_n") or 0) >= 30]
    n = sum(x["replacement_n"] for x in rows)
    lo = sum((x["replacement_over_250k_pct"] - 0.05) * x["replacement_n"] for x in rows) / n
    hi = sum((x["replacement_over_250k_pct"] + 0.05) * x["replacement_n"] for x in rows) / n
    t = re.sub(r"<[^>]+>", "", page); bad = []
    m_ = re.search(r"(\d+)% of the ([\d,]+) single-family primary-home NFIP policies that report a rebuilding cost report one above \$250,000", t)
    if not m_ or not (lo <= int(m_[1]) + 0.5 and int(m_[1]) - 0.5 <= hi) or int(m_[2].replace(",", "")) != n or round(lo) != round(hi):
        bad.append(f"P1 U.S. share: page {m_[0][:12] if m_ else 'none'}, recomputed {lo:.2f}-{hi:.2f}% of {n:,}")
    if f'<div class="n">{m_[1] if m_ else "?"}%</div>' not in page: bad.append("P1 tile differs from the sentence")
    got = sorted((int(b.replace(",", "")), float(a)) for a, b in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>([\d.]+)%</td><td>([\d,]+)</td></tr>', page))
    if got != sorted((x["replacement_n"], x["replacement_over_250k_pct"]) for x in rows): bad.append(f"P2 state rows {len(got)} vs {len(rows)}")
    bad += [f"P3 G4 word '{w}'" for w in re.findall(r"\b(?:best|cheapest|top-rated|recommended insurers?)\b", t, re.I)]
    bad += cap_tile(page, "P4")
    # P5 (r-private2 MAJOR: the lede opened on a legal fragment): the answer sentence comes before the lender rule
    a, r = t.find("single-family primary-home NFIP policies that report a rebuilding cost report one above"), t.find(re.sub(r"<[^>]+>", "", RULE_TEXT("private_accept"))[:40])
    if a < 0 or r < 0 or a > r: bad.append("P5 the 37%-style answer does not come before the private_accept rule")
    return bad

def check_rr2(page):   # Risk Rating 2.0 guide (11-13): U.S. share below full risk with rounding bounds, base count, state rows, gap
    rows = [json.load(open(p))["policies"] for p in glob.glob(os.path.join(D, "states", "*", "agg.json"))]
    rows = [x for x in rows if x.get("gap_basis") == "premium" and x.get("share_below") is not None and (x.get("below_n") or 0) >= 30]
    n = sum(x["below_n"] for x in rows)
    lo, hi = (sum((x["share_below"] + d) * x["below_n"] for x in rows) / n for d in (-0.05, 0.05))
    t = re.sub(r"<[^>]+>", "", page); bad = []
    m_ = re.search(r"(\d+)% of the ([\d,]+) U\.S\. single-family primary-home NFIP policies with both premiums recorded pay a premium below", t)
    if not m_ or int(m_[2].replace(",", "")) != n or not (lo <= int(m_[1]) + 0.5 and int(m_[1]) - 0.5 <= hi) or round(lo) != round(hi):
        bad.append(f"R1 U.S. share: page {m_[0][:12] if m_ else 'none'}, recomputed {lo:.2f}-{hi:.2f}% of {n:,}")
    if f'<div class="n">{m_[1] if m_ else "?"}%</div>' not in page: bad.append("R1 tile differs from the sentence")
    got = sorted((int(c.replace(",", "")), float(a), int(b.replace(",", ""))) for a, b, c in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>([\d.]+)%</td><td>\$([\d,]+)</td><td>([\d,]+)</td></tr>', page))
    if got != sorted((x["below_n"], x["share_below"], x["below_gap_median"]) for x in rows): bad.append(f"R2 state rows {len(got)} vs {len(rows)}")
    return bad

def cap_tile(page, code):   # P4 (r-private MAJOR: 77% printed with no base): the coverage tile names its base (all sf_n) and its test (>= $250,000,
    # as extras_raw counts); one copy for the private and coverage guides (11-15)
    mx = [x for x in (json.load(open(p))["policies"] for p in glob.glob(os.path.join(D, "states", "*", "extras.json"))) if x.get("at_building_max_pct") is not None and x.get("sf_n")]
    mn = sum(x["sf_n"] for x in mx)
    if not mn: return [f"{code} building tile printed with no extras data"] if "building coverage of $250,000 or more</div>" in page else []
    ml, mh = (sum((x["at_building_max_pct"] + d) * x["sf_n"] for x in mx) / mn for d in (-0.05, 0.05))
    m4 = re.search(r'<div class="n">(\d+)%</div><div class="l">of all ([\d,]+) U\.S\. NFIP single-family primary-home policies: building coverage of \$250,000 or more</div>', page)
    if not m4 and round(ml) == round(mh): return [f"{code} coverage tile missing, or its base or test unlabelled"]
    if m4 and (int(m4[2].replace(",", "")) != mn or not (ml <= int(m4[1]) + 0.5 and int(m4[1]) - 0.5 <= mh)): return [f"{code} coverage tile {m4[1]}% of {m4[2]}, recomputed {ml:.2f}-{mh:.2f}% of {mn:,}"]
    return []

def check_floodplain(page):   # floodplain guide (11-15): U.S. unit share from integer sums, base, state rows, range, zone disclosure; no build_site code
    rows = [x for x in (json.load(open(p))["policies"] for p in glob.glob(os.path.join(D, "states", "*", "agg.json")))
            if x.get("sfha_units") is not None and x.get("sfha_share_units") is not None and x.get("units")]
    n = sum(x["units"] for x in rows)
    if not n: return ["FP0 no state has sfha_units (first run or old data): guide must not be built"] if "100-year floodplain" in page else []
    pc = round(100 * sum(x["sfha_units"] for x in rows) / n, 1)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", page)); bad = []
    if not re.search(rf"In FEMA's records, {pc}% of the {n:,} NFIP policy units in force in \d+ states(?: and DC)? are rated in zones A or V", t):
        bad.append(f"FP1 U.S. share: want {pc}% of {n:,} policy units")
    if f'<div class="n">{pc}%</div><div class="l">of {n:,} NFIP policy units in force: rated in zones A or V</div>' not in page: bad.append("FP1 tile differs or loses its base")
    got = sorted((int(b.replace(",", "")), float(a)) for a, b in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>([\d.]+)%</td><td>([\d,]+)</td></tr>', page))
    if got != sorted((x["units"], x["sfha_share_units"]) for x in rows): bad.append(f"FP2 state rows {len(got)} vs {len(rows)}")
    sh = [x["sfha_share_units"] for x in rows]
    if not re.search(rf"The share runs from {min(sh)}% in (?:the )?[A-Z][^.]* to {max(sh)}% in ", t): bad.append(f"FP3 range sentence: want {min(sh)}% to {max(sh)}%")
    if "which can differ from the zone on today's map" not in t or "Buildings without NFIP flood insurance are not in these counts" not in t: bad.append("FP4 rated-zone / insured-only disclosure missing")
    return bad

def check_contents(page):   # contents guide (11-15): U.S. share with rounding bounds, base count, state rows, range sentence; no build_site code
    rows = [json.load(open(p))["policies"] for p in glob.glob(os.path.join(D, "states", "*", "agg.json"))]
    _min = __import__("metrics").CONST["min_priced"]   # code review 11-15: the page's own floor, one copy
    rows = [x for x in rows if x.get("contents_share") is not None and (x.get("cohort_n") or 0) >= _min]
    n = sum(x["cohort_n"] for x in rows)
    if not n: return ["T0 no state has contents_share (first run or old data): guide must not be built"] if "contents coverage" in page else []
    lo, hi = (sum((x["contents_share"] + d) * x["cohort_n"] for x in rows) / n for d in (-0.05, 0.05))
    t = re.sub(r"<[^>]+>", "", page); bad = []
    m_ = re.search(r"(\d+)% of the ([\d,]+) U\.S\. single-family primary-home NFIP policies carry some contents coverage", t)
    if not m_ or int(m_[2].replace(",", "")) != n or not (lo <= int(m_[1]) + 0.5 and int(m_[1]) - 0.5 <= hi) or round(lo) != round(hi):
        bad.append(f"T1 U.S. share: page {m_[0][:12] if m_ else 'none'}, recomputed {lo:.2f}-{hi:.2f}% of {n:,}")
    if f'<div class="n">{m_[1] if m_ else "?"}%</div><div class="l">of {n:,} U.S. NFIP single-family primary-home policies: some contents coverage</div>' not in page:
        bad.append("T1 tile differs from the sentence or loses its base")
    got = sorted((int(b.replace(",", "")), float(a)) for a, b in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>([\d.]+)%</td><td>([\d,]+)</td></tr>', page))
    if got != sorted((x["cohort_n"], x["contents_share"]) for x in rows): bad.append(f"T2 state rows {len(got)} vs {len(rows)}")
    sh = [x["contents_share"] for x in rows]
    if not re.search(rf"The share runs from {min(sh)}% in (?:the )?[A-Z][^.]* to {max(sh)}% in ", t): bad.append(f"T3 range sentence: want {min(sh)}% to {max(sh)}%")
    bad += cap_tile(page, "T4")   # 11-15 coverage retitle: the building tile, same test as the private guide's
    if 'data-rule="building_what"' not in page: bad.append("T5 'what does flood insurance cover' page without the building coverage rule")
    return bad

def check_loma(page, ms=None):   # LOMA/LOMR guide (11-14): outcomes regrouped from map_status.json with this file's own map (LL1-LL6), no build_site code
    ms = ms if ms is not None else json.load(open(os.path.join(D, "us", "map_status.json")))
    live = {p["geoid"]: p["state"] for p in json.load(open(os.path.join(ROOT, "places.json")))}
    cs = {g: v for g, v in ms.items() if g in live and isinstance(v, dict)}
    lo = {g: v["loma"] for g, v in cs.items() if v.get("loma") is not None}
    def grp(o):   # FEMA OUTCOME wording; checked first-match in this order: denied, removed, out as shown, everything else
        o = o.split("|")[0].lower()
        return "den" if "denied" in o else "rm" if o.startswith(("structure removed", "property removed", "portion of property removed")) else "as" if "out as shown" in o else "oth"
    g = collections.Counter(); bys = {}
    for k, d in lo.items():
        for o, n in d.items(): g[grp(o)] += n; bys.setdefault(live[k], collections.Counter())[grp(o)] += n
    t = sum(g.values()); pc = lambda n, d=None: f"{100 * n / (d or t):.1f}%"; bad = []
    tx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page))
    want = (f"FEMA's map service lists {t:,} rulings in its LOMA map layer for owners in {len(lo)} of the {len(live)} counties on this site who asked FEMA to take a building or lot out "
            f"of the high-risk flood zone. {pc(g['rm'])} of these rulings took the building or some or all of the lot out, and {pc(g['den'])} were denied.")   # owner 11-15: two sentences, same figures
    if want not in tx: bad.append(f"L1 lede: want {t:,} rulings, {len(lo)} counties, {pc(g['rm'])} out, {pc(g['den'])} denied")
    for lab, n in (("Denied", g["den"]), ("Already outside the zone as mapped", g["as"]), ("Other, mixed or no outcome recorded", g["oth"])):
        if f"<tr><td>{lab}</td><td>{pc(n)}</td><td>{n:,}</td></tr>" not in page: bad.append(f"L1 outcome row {lab}: {pc(n)} {n:,}")
    rs = [int(x.replace(",", "")) for x in re.findall(r"<tr><td>[A-Z][^<]*</td><td>[\d.]+%</td><td>([\d,]+)</td></tr>", page)]
    if rs != sorted(rs, reverse=True) or sum(rs) != t: bad.append(f"L1 outcome table not ranked by value or does not sum to {t:,}")
    seen = collections.Counter(c for k in lo for c in cs[k].get("cids", []))   # LL2: a community under two counties would be summed twice
    if any(n > 1 for n in seen.values()): bad.append(f"L2 {sum(n > 1 for n in seen.values())} communities listed under two counties")
    lede = tx[tx.find("FEMA's map service lists"):tx.find("were denied.")]
    if re.search(r"\bU\.S\.|\bnationwide\b|\bthe nation\b", lede): bad.append("L3 LOMA lede labelled national; the base is counties on this site")
    lr = [v for v in cs.values() if "lomr" in v]; sn = {v.get("lomr_since") for v in lr}
    if len(sn) > 1 or None in sn: bad.append(f"L4 {len(sn)} LOMR 'since' dates")
    elif not sn:   # no county with a LOMR count: the page prints no LOMR sentence (and still builds)
        if "Letters of Map Revision, " in tx: bad.append("L4 LOMR sentence with no LOMR counties")
    elif f"of {len(lr)} of the {len(live)} counties on this site with {sum(v['lomr'] for v in lr):,} Letters of Map Revision, {sum(v['lomr_recent'] for v in lr):,} of them" not in tx:
        bad.append("L4 LOMR sentence differs")
    got = sorted((int(b.replace(",", "")), c, d) for b, c, d in re.findall(r'<tr><td><a href="/flood-insurance/[a-z-]+/">[^<]+</a></td><td>\d+</td><td>([\d,]+)</td><td>([\d.]+%|—)</td><td>([\d.]+%|—)</td></tr>', page))
    for k, d in lo.items():
        if not d: bys.setdefault(live[k], collections.Counter())   # a state whose counties list zero rulings still prints its row, shares "—"
    sh = lambda n, d: pc(n, d) if d else "—"
    if got != sorted((sum(c.values()), sh(c["rm"], sum(c.values())), sh(c["den"], sum(c.values()))) for c in bys.values()): bad.append(f"L5 state rows {len(got)} vs {len(bys)}")
    return bad

def RULE_TEXT(k):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    return __import__("rules_registry").RULES[k]["text"]

def check_order(page, first, then, code):   # r-private2 MAJOR: an exception printed before the rule it is an exception to
    a, b = page.find(f'data-rule="{first}"'), page.find(f'data-rule="{then}"')
    return [] if b < 0 or 0 <= a < b else [f"{code} rule {then} printed without {first} before it"]

def check_rule_quotes(rules):   # r-private MAJOR: a rule shown in quotation marks must be the source's own words (its excerpts, read raw)
    bad = []
    for k, r in rules.items():
        ex = " ".join(e for _, e, _ in r["sources"])
        tx = re.sub(r"<[^>]+>", "", r["text"])
        if re.search(r'"\s+"|\bsubparagraph\b', tx): bad.append(f"Q2 rule {k}: back-to-back quotes or an undefined statute cross-reference")
        for q in re.findall(r'[“"]([^”"]{12,})[”"]', tx):
            bad += [f"Q1 rule {k}: quoted '{pc[:50]}' is not in its source excerpts" for pc in re.split(r"\s*(?:\.\.\.|…)\s*", q) if pc.strip().rstrip(".") and pc.strip().rstrip(".") not in ex]
    return bad

HOMES_WORDS = re.compile(r"\b(?:NFIP homes|elevated NFIP homes|zone AE homes|zone X homes|NFIP homeowners choose)\b", re.I)
def check_base_words(pages):   # r169 + r173 MAJOR twice: guides count POLICIES; "homes" as the base word is a mislabel
    bad = []
    for name, h in pages.items():
        t = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>", " ", h)) + " " + " ".join(re.findall(r'<meta name="description" content="([^"]*)"', h))   # r174: the description drifted from the base too
        bad += [f"B1 {name}: '{m_[0]}' names homes where the base is policies" for m_ in HOMES_WORDS.finditer(t)]
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
        lb = check_state_labels(gp) + check_base_words(gp)
        if "--test" in sys.argv:
            assert check_base_words({"x": "<p>26% of zone AE homes carry it</p>"}), "mutation not caught: homes as base"
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
        vg = open(os.path.join(ROOT, "dist", "guides", "flood-vents", "index.html"), encoding="utf-8").read()
        pv = open(os.path.join(ROOT, "dist", "guides", "private-flood-insurance", "index.html"), encoding="utf-8").read()
        bh = open(os.path.join(ROOT, "dist", "guides", "buying-a-house-in-a-flood-zone", "index.html"), encoding="utf-8").read()
        rr = open(os.path.join(ROOT, "dist", "guides", "risk-rating-2", "index.html"), encoding="utf-8").read()
        lg = open(os.path.join(ROOT, "dist", "guides", "loma-lomr", "index.html"), encoding="utf-8").read()
        _rd = lambda g: (lambda f: open(f, encoding="utf-8").read() if os.path.exists(f) else "")(os.path.join(ROOT, "dist", "guides", g, "index.html"))   # code review 11-15: a guide not built (n==0 / fewer than 10 states) is read as "", so its FP0/T guard runs instead of a crash
        tg, fg = _rd("flood-insurance-contents-coverage"), _rd("100-year-floodplain")
        bad = check_guides(pg, zx) + check_condo(cg) + check_deductible(dg) + check_vents(vg) + check_private(pv) + check_rr2(rr) + check_loma(lg) + check_contents(tg) + check_floodplain(fg) + check_order(bh, "wait_30", "start_loan_plain", "O1")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from rules_registry import RULES as _RQ
        bad += check_rule_quotes(_RQ)
        if "--test" in sys.argv:
            assert check_private(re.sub(r"(\d+)(% of the [\d,]+ single-family)", lambda m_: f"{int(m_[1]) + 1}{m_[2]}", pv, count=1)), "mutation not caught: private U.S. share"
            assert check_private(re.sub(r"</a></td><td>([\d.]+)%</td>", lambda m_: f"</a></td><td>{round(float(m_[1]) + 0.1, 1)}%</td>", pv, count=1)), "mutation not caught: private state row"
            assert check_private(pv.replace("<h1>Private flood insurance</h1>", "<h1>Best private flood insurance</h1>", 1)), "mutation not caught: G4 best"
            assert check_private(re.sub(r"(of all )([\d,]+)", lambda m_: m_[1] + f"{int(m_[2].replace(',', '')) + 1:,}", pv, count=1)), "mutation not caught: P4 base"
            assert check_private(pv.replace(": building coverage of $250,000 or more</div>", ": insured to the $250,000 building limit</div>", 1)), "mutation not caught: P4 label"
            assert check_rule_quotes({"x": {"text": 'The law says "lenders must accept any policy".', "sources": [("u", "lenders must accept a policy", "curl")]}}), "mutation not caught: Q1 paraphrase in quotes"
            assert check_rule_quotes({"x": {"text": 'Regulators direct "lenders" "to accept a policy" under subparagraph (A).', "sources": [("u", "lenders to accept a policy", "curl")]}}), "mutation not caught: Q2 garbled quote"
            assert check_private(pv.replace('<p class="lede">', '<p class="lede">' + __import__("rules_registry").rule("private_accept") + " ", 1)), "mutation not caught: P5 rule before answer"
            assert check_order(bh.replace('data-rule="wait_30"', 'data-rule="wait_x"'), "wait_30", "start_loan_plain", "O1"), "mutation not caught: O1 exception without rule"
            assert check_vents(re.sub(r"</a></td><td>([\d.]+)%</td>", lambda m_: f"</a></td><td>{float(m_[1]) + 1}%</td>", vg, count=1)), "mutation not caught: vents state row"
            assert check_rr2(re.sub(r"(\d+)(% of the [\d,]+ U\.S\. single-family)", lambda m_: f"{int(m_[1]) + 1}{m_[2]}", rr, count=1)), "mutation not caught: rr2 U.S. share"
            assert check_loma(re.sub(r"([\d.]+)(% of these rulings took the building)", lambda m_: f"{float(m_[1]) + 0.1:.1f}{m_[2]}", lg, count=1)), "mutation not caught: LOMA lede share"
            assert check_loma(re.sub(r"(<tr><td>Denied</td><td>[\d.]+%</td><td>)([\d,]+)", lambda m_: m_[1] + "1", lg, count=1)), "mutation not caught: LOMA outcome row"
            assert check_loma(lg.replace("counties on this site who asked", "U.S. counties on this site who asked", 1)), "mutation not caught: L3 U.S. label"
            assert check_loma(re.sub(r"(</a></td><td>\d+</td><td>[\d,]+</td><td>)([\d.]+)%", lambda m_: f"{m_[1]}{float(m_[2]) + 1:.1f}%", lg, count=1)), "mutation not caught: LOMA state row"
            _ms = json.load(open(os.path.join(D, "us", "map_status.json"))); _a, _b = [k for k, v in _ms.items() if isinstance(v, dict) and v.get("cids")][:2]
            _ms[_b] = dict(_ms[_b], cids=_ms[_b]["cids"] + _ms[_a]["cids"][:1])
            assert any(b.startswith("L2") for b in check_loma(lg, _ms)), "mutation not caught: L2 community in two counties"
            _ms = json.load(open(os.path.join(D, "us", "map_status.json")))   # 11-14 review: no LOMR counties = page without the sentence, not an L4 failure
            _nl = {k: ({a: b for a, b in v.items() if not a.startswith("lomr")} if isinstance(v, dict) else v) for k, v in _ms.items()}
            _lg0 = re.sub(r'<p class="stand">FEMA has revised the countywide.*?</p>', "", lg, count=1, flags=re.S)
            assert not any(b.startswith("L4") for b in check_loma(_lg0, _nl)), "false failure: L4 with no LOMR counties"
            assert any(b.startswith("L4") for b in check_loma(lg, _nl)), "mutation not caught: L4 LOMR sentence with no LOMR counties"
            _vt = [p["geoid"] for p in json.load(open(os.path.join(ROOT, "places.json"))) if p["state"] == "VT"]   # 11-14 review: a state with zero rulings prints "—"
            if _vt and isinstance(_ms.get(_vt[0]), dict) and _ms[_vt[0]].get("loma") is not None:
                _zv = dict(_ms, **{_vt[0]: dict(_ms[_vt[0]], loma={})})
                _lgv = re.sub(r'(<a href="/flood-insurance/vermont/">Vermont</a></td><td>\d+</td><td>)[^<]*</td><td>[^<]*</td><td>[^<]*', r"\g<1>0</td><td>—</td><td>—", lg, count=1)
                assert not any(b.startswith("L5") for b in check_loma(_lgv, _zv)), "false failure: L5 on a state with zero rulings"
            assert check_contents(re.sub(r"(\d+)(% of the [\d,]+ U\.S\. single-family)", lambda m_: f"{int(m_[1]) + 1}{m_[2]}", tg, count=1)), "mutation not caught: contents U.S. share"
            assert check_contents(re.sub(r"</a></td><td>([\d.]+)%</td>", lambda m_: f"</a></td><td>{round(float(m_[1]) + 0.1, 1)}%</td>", tg, count=1)), "mutation not caught: contents state row"
            assert check_contents(tg.replace("policies: some contents coverage</div>", "homes: some contents coverage</div>", 1)), "mutation not caught: contents tile base"
            assert check_contents(re.sub(r"(The share runs from )([\d.]+)%", lambda m_: f"{m_[1]}{round(float(m_[2]) + 1, 1)}%", tg, count=1)), "mutation not caught: contents range"
            assert check_contents(tg.replace(": building coverage of $250,000 or more</div>", ": insured to the building limit</div>", 1)), "mutation not caught: T4 building tile label"
            assert check_contents(re.sub(r'(<div class="n">)(\d+)(%</div><div class="l">of all [\d,]+ U\.S\. NFIP single-family primary-home policies: building)', lambda m_: f"{m_[1]}{int(m_[2]) + 1}{m_[3]}", tg, count=1)), "mutation not caught: T4 building share"
            assert check_contents(tg.replace('data-rule="building_what"', 'data-rule="x"')), "mutation not caught: T5 building rule"
            assert check_floodplain(re.sub(r"(In FEMA's records, )([\d.]+)%", lambda m_: f"{m_[1]}{round(float(m_[2]) + 0.1, 1)}%", fg, count=1)), "mutation not caught: FP1 U.S. share"
            assert check_floodplain(fg.replace("NFIP policy units in force: rated", "NFIP homes: rated", 1)), "mutation not caught: FP1 tile base"
            assert check_floodplain(re.sub(r"</a></td><td>([\d.]+)%</td>", lambda m_: f"</a></td><td>{round(float(m_[1]) + 0.1, 1)}%</td>", fg, count=1)), "mutation not caught: FP2 state row"
            assert check_floodplain(re.sub(r"<tr><td><a href=\"/flood-insurance/[a-z-]+/\">[^<]+</a></td><td>[\d.]+%</td><td>[\d,]+</td></tr>", "", fg, count=1)), "mutation not caught: FP2 state dropped"
            assert check_floodplain(re.sub(r"(The share runs from )([\d.]+)%", lambda m_: f"{m_[1]}{round(float(m_[2]) + 1, 1)}%", fg, count=1)), "mutation not caught: FP3 range"
            assert check_floodplain(fg.replace("which can differ from the zone on today's map", "as on today's map", 1)), "mutation not caught: FP4 disclosure"
            assert check_rr2(re.sub(r"</a></td><td>([\d.]+)%</td><td>\$([\d,]+)</td>", lambda m_: f"</a></td><td>{m_[1]}%</td><td>${int(m_[2].replace(',', '')) + 1:,}</td>", rr, count=1)), "mutation not caught: rr2 gap"
        if "--test" in sys.argv:
            assert check_deductible(re.sub(r"<td>([\d.]+)%</td><td>([\d.]+)%</td></tr>", lambda m_: f"<td>{float(m_[1]) + 1}%</td><td>{m_[2]}%</td></tr>", dg, count=1)), "mutation not caught: deductible share"
            assert check_deductible(dg.replace("zone AE vs zones X, B or C", "zone AE vs zone X", 1)), "mutation not caught: zone X label"
            assert check_deductible(re.sub(r"([\d.]+)(% of zone AE policies carry)", lambda m_: f"{round(float(m_[1]) + 0.3, 1)}{m_[2]}", dg, count=1)), "mutation not caught: $5,000+ lede"
        if "--test" in sys.argv:
            assert check_condo(re.sub(r"<td>\$([\d,]+)</td>", "<td>$1</td>", cg, count=1)), "mutation not caught: condo row"
            assert not bad, bad
            assert check_guides(re.sub(r">(\d+)%<", lambda m_: f">{int(m_[1]) + 1}%<", pg, count=1), zx), "mutation not caught: tile"
            assert check_guides(pg, re.sub(r"(zone on the claim, )(\d+)%", lambda m_: m_[1] + str(int(m_[2]) + 1) + "%", zx, count=1)), "mutation not caught: zone X disagrees"
            print("guides check mutations: 37 caught, 2 false failures ruled out"); sys.exit()
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
                "icc": re.sub(r"\(([\d.]+)%\) include an", lambda m_: f"({float(m_[1]) + 0.1:.1f}%) include an", pg, count=1),
                "icc gone": pg.replace("include an Increased Cost of Compliance payment", "", 1),
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
