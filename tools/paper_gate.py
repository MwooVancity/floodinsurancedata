"""Research paper gate, machine half (docs/PAPER-GATE-PROMPT.md, owner 11-12 "strictest, PubMed level"). For every paper page built:
M2.1 sections present in order; M2.3 banned words; M1.3 every table share has a 90% range; M1.1/M2.2 every row and every CSV line
recomputed from data/all-counties with this file's own code (never imports papers.py or build_site.py: PLAN E22); county cards
match; M2.6 FEMA attribution; M3.1 papers share under 30% of sentences. Usage: python -I tools/paper_gate.py [--test]"""
import csv, glob, io, json, math, os, re, statistics, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "dist")
# a second, independent copy of each paper's base: (numerator path, denominator path, minimum). A drift from papers.py fails.
BASES = {"damage-over-coverage": (("extras", "claims", "underinsured", "over"), ("extras", "claims", "underinsured", "n"), 100),
         "outside-the-zone": (("extras", "claims", "zone_split", "out_paid_n"), ("extras", "claims", "zone_split", "known_paid_n"), 100)}
def ded_at(r, lo):   # Deductible Choice, own copy: SF primary policy units with a building deductible of lo dollars or more
    d = g(r, ("extras", "policies", "deductible_units"))
    return sum(v for k, v in d.items() if k.isdigit() and int(k) >= lo and isinstance(v, int)) if isinstance(d, dict) and d else None
BASES["deductible-choice"] = (lambda r: ded_at(r, 5000), lambda r: ded_at(r, 0), 30)
MO = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def mon(r):   # Flood Calendar, own copy: claims by calendar month, valid month keys and int counts only
    b = g(r, ("extras", "claims", "loss_month_n", "by_month"))
    b = {k: v for k, v in b.items() if k.isdigit() and 1 <= int(k) <= 12 and len(k) == 2 and isinstance(v, int)} if isinstance(b, dict) else {}
    return b if sum(b.values()) > 0 else None
BASES["flood-calendar"] = (lambda r: max(mon(r).values()) if mon(r) else None, lambda r: sum(mon(r).values()) if mon(r) else None, 100)
_CH = {}
def chance(n):   # own copy: expected largest-month share (%) of n claims thrown at random into 12 equal months, 4,000 draws seeded by n
    if n not in _CH:
        import numpy
        draws = numpy.random.default_rng(n).multinomial(n, [1 / 12] * 12, size=4000)
        _CH[n] = round(100 * int(draws.max(axis=1).sum()) / (4000 * n), 1)
    return _CH[n]
# Price Gap, own copy: SF primary-home policies priced both ways (agg), $100+ below full-risk; any-amount share and median gap (30+ below)
BASES["price-gap"] = (("policies", "below100_k"), ("policies", "below_n"), 30)
def gapcols(r):
    p = r.get("policies") or {}; k, n, md = p.get("below_k"), p["below_n"], p.get("below_gap_median")
    crs = g(r, ("extras", "policies", "below_by_crs"))   # bug review 11-14: Results' $10 line and CRS split recomputed too
    return (round(100 * k / n, 1), md if k >= 30 and isinstance(md, (int, float)) else None, k, p.get("below10_k"), crs if isinstance(crs, dict) else {})
def gap_results(T):   # own copy of the price-gap Results words: pooled shares at any amount / $10 / $100, CRS classes with 1,000+ policies
    n = sum(t["n"] for t in T); r = lambda a: round(100 * a / n, 1)
    pooled = (f"pooled over the {len(T):,} counties, {r(sum(t['gap'][2] for t in T))}% of {n:,} ",
              f" by any amount, {r(sum(t['gap'][3] or 0 for t in T))}% by $10 or more and {r(sum(t['k'] for t in T))}% by $100 or more.</li>")
    tot = {}
    for t in T:
        for c, (a, b) in t["gap"][4].items(): tot[c] = [tot.get(c, [0, 0])[0] + a, tot.get(c, [0, 0])[1] + b]
    cl = sorted((c for c in tot if tot[c][0] >= 1000), key=lambda c: (c == "blank", int(c) if c.isdigit() else 99))
    crs = "".join(f'<tr><td>{"No class code" if c == "blank" else "Class " + c}</td><td>{tot[c][0]:,}</td><td>{round(100 * tot[c][1] / tot[c][0], 1)}%</td></tr>' for c in cl)   # owner 11-15: a small table
    return pooled, (f"<tbody>{crs}</tbody></table>" if cl else None)
def crs_adds_up(recs):   # M3 split (extras_raw, its own pass) must hold exactly the agg base: same policies, same count below
    bad = []
    for c, r in recs.items():
        b = g(r, ("extras", "policies", "below_by_crs")); p = r.get("policies") or {}
        if isinstance(b, dict) and b and isinstance(p.get("below_n"), int) and (sum(v[0] for v in b.values()), sum(v[1] for v in b.values())) != (p["below_n"], p.get("below_k")):
            bad.append(f"price-gap: county {c} CRS split does not hold the same policies as the base")
    return bad[:5]
NULL = {"flood-calendar": chance}   # papers ranked on share minus a chance expectation (statistician round 2)
def cal(r):   # (peak months, year-months holding over half of a peak month with 10+ claims), both as page words
    b = mon(r); ym = g(r, ("extras", "claims", "loss_month_n", "by_year_month")) or {}; top = max(b.values())
    pk = [k for k in sorted(b) if b[k] == top]; st = []
    for k in pk:
        ys = sorted(((v, y) for y, v in ym.items() if y.endswith("-" + k)), reverse=True)
        if top >= 10 and ys and 2 * ys[0][0] > top: st.append(ys[0][1])
    yrs = [len({y[:4] for y, v in ym.items() if y.endswith("-" + k) and isinstance(v, int) and v > 0}) for k in pk]   # distinct loss years
    y10 = [len({y[:4] for y, v in ym.items() if y.endswith("-" + k) and isinstance(v, int) and v >= 10}) for k in pk]   # round 3: 10+ claim years
    tsh = [round(100 * max([v for y, v in ym.items() if y.endswith("-" + k) and isinstance(v, int)] or [0]) / top, 1) for k in pk]   # largest year's share
    return " and ".join(MO[int(k) - 1] for k in pk), " and ".join(f"{MO[int(y[5:]) - 1]} {y[:4]}" for y in st), ";".join(pk), ";".join(st), yrs, y10, tsh
def months_add_up(recs):   # each month's year-months must sum to that month (the flag's base = the share's base)
    bad = []
    for c, r in recs.items():
        lm = g(r, ("extras", "claims", "loss_month_n"))
        if isinstance(lm, dict) and lm.get("by_month"):
            ym = lm.get("by_year_month") or {}
            if any(sum(v for y, v in ym.items() if y.endswith("-" + k)) != v for k, v in lm["by_month"].items()): bad.append(f"flood-calendar: county {c} year-months do not add up to months")
    return bad[:5]

def units_are_records(recs):   # M1.7: Wilson counts units as records; a county whose SF records hold more units than records fails
    bad = []
    for c, r in recs.items():
        p = g(r, ("extras", "policies")) or {}
        if isinstance(p.get("deductible_units"), dict) and p["deductible_units"] and p.get("sf_n") != sum(p["deductible_units"].values()) + (p.get("deductible_units_blank") or 0):
            bad.append(f"deductible-choice: county {c} single-family records {p.get('sf_n')} differ from policy units (M1.7)")
    return bad[:5]

# M1.4/M1.8 second copy: (median excess path, over-by-year path) for papers with an excess column
EXTRA = {"damage-over-coverage": (("extras", "claims", "underinsured", "excess_median"), ("extras", "claims", "underinsured", "over_by_year"))}
# label-vs-data (statistician review, deductible paper): FEMA records a value on the policy, not an owner's choice, so these words
# never appear in a label (title, description, h1, lede, Abstract, Question, Results); a cited study's own title in Prior work is not a label
LABEL = {"deductible-choice": re.compile(r"\b(choice|choices|choose|chooses|chose|chosen|opt|opts|opted|elect|elects|elected)\b", re.I),
         # statistician round 2: 404 of 416 peak months are mostly one year, so no season or calendar word in a label
         "flood-calendar": re.compile(r"\b(calendar|seasons?|seasonal|seasonality)\b", re.I),
         # FEMA records a full-risk premium, not a subsidy: the word is Neptune's reading, never this paper's label
         "price-gap": re.compile(r"\bsubsid(y|ies|ized|ised|ize|ise)\b", re.I)}
# round 3 (statistician): the over-half flag says nothing about other years, so no sentence anywhere claims the month does not recur
OVERCLAIM = {"flood-calendar": re.compile(r"repeats? each year|not a pattern|mostly one year's flood|\brecur(s|ring)?\b", re.I)}
LABEL_MUT = {"deductible-choice": " choice", "flood-calendar": " calendar", "price-gap": " subsidy"}
STAGED, SITEMAP = set(), ""   # papers with no published date: must be noindex and out of the sitemap (M3.5); filled in main
SECTIONS = ["abstract", "question", "data", "methods", "results", "prior", "table", "limitations", "reproduce", "cite", "versions", "corrections"]
BANNED = re.compile(r"\b(best|worst|safest|most dangerous|peer[- ]reviewed|significant(ly)?|only published here|denied|forecast|will rise|because|due to|caused by|driven by)\b", re.I)

def g(r, p):
    if callable(p): return p(r)
    for k in p: r = r.get(k) if isinstance(r, dict) else None
    return r

def ci(k, n):   # 90% Wilson, written out on its own (not papers.wilson)
    z = 1.6448536269514722; ph = k / n; den = 1 + z * z / n
    mid = (ph + z * z / (2 * n)) / den; half = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return max(0.0, round(100 * (mid - half), 1)) + 0.0, min(100.0, round(100 * (mid + half), 1)) + 0.0

def truth(recs, key):
    nump, denp, mn = BASES[key]
    rows = [(c, g(r, nump), g(r, denp)) for c, r in recs.items()]
    nf = NULL.get(key)
    rows = sorted([(c, k, n) for c, k, n in rows if isinstance(k, int) and isinstance(n, int) and n >= mn and 0 <= k <= n],
                  key=lambda t: (-(t[1] / t[2] - (nf(t[2]) / 100 if nf else 0)), t[0]))
    N = len(rows)
    def pol(c):   # policy units outside A and V today, from the county's own inside share (review outside-zone-2 M1)
        s_ = g(recs[c], ("policies", "sfha_share_units"))
        return round(100 - s_, 1) if isinstance(s_, (int, float)) else None
    out, band = [], {}   # an equal printed share gets one fifth: the fifth where that share first appears
    for i, (c, k, n) in enumerate(rows):
        v = round(100 * k / n, 1)
        ex = by = None
        if key in EXTRA:
            ex, by = g(recs[c], EXTRA[key][0]), g(recs[c], EXTRA[key][1]) or {}
            by = next((y for y, m in by.items() if 2 * m > sum(by.values()) >= 10), None)   # at most one year holds over half; 10+ claims only (review underinsured-2 N1)
        e = nf(n) if nf else None; x = None if e is None else round(v - e, 1)   # printed share minus printed expected
        out.append({"c": c, "k": k, "n": n, "v": v, "ci": ci(k, n), "fifth": band.setdefault(v if x is None else x, 1 + 5 * i // N), "pol": pol(c), "ex": ex, "yr": by, "e": e, "x": x,
                    "cal": cal(recs[c]) if key == "flood-calendar" else None, "gap": gapcols(recs[c]) if key == "price-gap" else None})
    return out

def text(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style|head)\b.*?</\1>", " ", h)))

def check(key, page, csv_text, cards, T, sm=None):
    bad = []; sm = SITEMAP if sm is None else sm
    if key in LABEL:
        lab = page[:max(0, page.find('id="data"'))] + page[page.find('id="results"'):page.find('id="prior"')]
        for m in LABEL[key].finditer(text(lab)): bad.append(f"{key}: label word '{m[0]}' (a claim the data does not make)")
    if key in STAGED and ('content="noindex' not in page or f"/flood-insurance/{key}/<" in sm):
        bad.append(f"{key}: not yet opened by the owner, must be noindex and out of the sitemap (M3.5)")
    # owner 11-14: the plain-words answer and the county lookup come first; its median is the recomputed median
    pl = page[page.find('id="plain"'):page.find('class="lede"')] if 'id="plain"' in page else ""
    _pm = re.search(r"(?:median listed county (?:it (?:is|was)|the (?:busiest|peak) month held)) ([\d.]+)%", text(pl))
    if not pl or 'id="ps"' not in pl or not _pm or float(_pm[1]) != round(statistics.median(t["v"] for t in T), 1) if T else False:
        bad.append(f"{key}: plain-words answer, its median ({_pm and _pm[1]}) or the county lookup missing or wrong")
    asof = next(csv.DictReader(io.StringIO(csv_text or "")), {}).get("as_of", "")   # M2.5: the current dated address, listed and built
    vc = page[page.find('id="versions"'):page.find('id="corrections"')]
    vdir = os.path.join(D, "flood-insurance", key)
    olds = [x for x in (os.listdir(vdir) if os.path.isdir(vdir) else []) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)]
    if not asof or f'href="/flood-insurance/{key}/{asof}/"' not in vc or not os.path.exists(os.path.join(vdir, asof, "index.html"))             or any(f'/flood-insurance/{key}/{x}/' not in vc for x in olds) or re.search(r"replaces? (the|every)", vc):
        bad.append(f"{key}: Versions card does not link every dated version (M2.5)")
    if len(T) > 500 and (f"fetch('/data/{key}.csv')" not in page or 'id="ps"' not in page):
        bad.append(f"{key}: over 500 counties and no state lookup on the CSV (rater Needs Met)")
    pos = [page.find(f'id="{s}"') for s in SECTIONS]
    if -1 in pos: bad.append(f"{key}: missing sections {[s for s, p in zip(SECTIONS, pos) if p < 0]}")
    elif pos != sorted(pos): bad.append(f"{key}: sections out of order")
    own = re.sub(r'(?s)<(span|div) data-rule="[^"]+">.*?</\1>', " ", page)   # FEMA's quoted rule text is exact and never reworded
    for m in BANNED.finditer(text(own)): bad.append(f"{key}: banned word '{m[0]}'")
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
    if key in EXTRA:   # M1.4 + M1.8 columns = recompute, on the page and in the CSV
        xcol = re.findall(r"</td><td>[\d,]+ of [\d,]+</td><td>(\$[\d,]+|—)</td><td>(\d{4}|)</td></tr>", page)
        if len(xcol) != len(want) or any((e_ == "—") != (t["ex"] is None) or (e_ != "—" and int(e_[1:].replace(",", "")) != round(t["ex"])) or (y_ or None) != t["yr"] for (e_, y_), t in zip(xcol, want)):
            bad.append(f"{key}: excess or one-year column disagrees with recompute")
        m = re.search(r"from one loss year, (\d{4}), which may hold one flood or several \(([\d,]+) of the [\d,]+ counties", page)   # the Abstract's one-flood flag on the top county
        want_ab = (T[0]["yr"], sum(1 for t in T if t["yr"])) if T and T[0]["yr"] else None
        if (m and (m[1], int(m[2].replace(",", "")))) != (want_ab or None): bad.append(f"{key}: Abstract one-year flag {m and m.groups()} vs {want_ab}")
    if key == "price-gap":   # M2 columns = recompute, page and CSV; M9 prior work cites GAO
        gcol = re.findall(r"</td><td>[\d,]+ of [\d,]+</td><td>([\d.]+)%</td><td>(\$[\d,]+|—)</td></tr>", page)
        if len(gcol) != len(want) or any((float(a_), None if b_ == "—" else int(b_[1:].replace(",", ""))) != (t["gap"][0], None if t["gap"][1] is None else round(t["gap"][1])) for (a_, b_), t in zip(gcol, want)):
            bad.append(f"{key}: any-amount share or median gap column disagrees with recompute")
        tg = {x["c"]: x for x in T}
        for r in csv.DictReader(io.StringIO(csv_text or "")):
            t = tg.get(r["county_fips"])
            if t and (int(r["below_any_amount_n"]), float(r["below_any_amount_pct"]), r["median_gap_usd_below_any_amount"] or None) != (t["gap"][2], t["gap"][0], None if t["gap"][1] is None else str(t["gap"][1])):
                bad.append(f"{key}: CSV row {r['county_fips']} any-amount/median gap disagrees with recompute"); break
        rs = page[page.find('id="results"'):page.find('id="prior"')]; (p0, p1), crs = gap_results(T)
        if p0 not in rs or p1 not in rs: bad.append(f"{key}: Results pooled any/$10/$100 shares disagree with recompute")
        if (crs is None) != ("By the CRS class code" not in rs) or (crs and crs not in rs): bad.append(f"{key}: Results CRS split disagrees with recompute")
        t0 = next((t for t in T if t["c"] == "12021"), None)   # M9 reconcile: Collier County, FL, beside GAO's own figure
        if t0 and f"here {t0['gap'][0]}% of {t0['n']:,} " not in page or t0 and f"by any amount and {t0['v']}% by $100 or more, as of" not in page:
            bad.append(f"{key}: Prior work Collier County figures disagree with recompute")
        if "GAO-27-108012" not in page[page.find('id="prior"'):page.find('id="table"')]: bad.append(f"{key}: Prior work does not cite GAO-27-108012 (M9)")
    if key in OVERCLAIM:
        for m in OVERCLAIM[key].finditer(text(page)): bad.append(f"{key}: '{m[0]}' claims more than the one-year flag measures (round 3 M1)")
    if key == "flood-calendar":   # peak month + one-year flag columns, the Abstract flag count and top-county flag = recompute
        mcol = re.findall(r"</td><td>[\d,]+ of [\d,]+</td><td>([\d.]+)%</td><td>([+-][\d.]+)</td><td>([A-Z][a-z]+(?: and [A-Z][a-z]+)*)</td><td>([\d.]+%(?: and [\d.]+%)*)</td><td>([\d,]+(?: and [\d,]+)*)</td><td>([\d,]+(?: and [\d,]+)*)</td><td>([^<]*)</td></tr>", page)
        ints = lambda s_: [int(y.replace(",", "")) for y in s_.split(" and ")]
        if len(mcol) != len(want) or any((float(e_), float(x_), a_, [float(y[:-1]) for y in s_.split(" and ")], ints(y_), ints(z_), b_) != (t["e"], t["x"], t["cal"][0], t["cal"][6], t["cal"][4], t["cal"][5], t["cal"][1])
                                         for (e_, x_, a_, s_, y_, z_, b_), t in zip(mcol, want)): bad.append(f"{key}: expected, excess, peak month, largest-year share, loss years or one-year column disagrees with recompute")
        if "<th>Loss years with at least one claim in the peak month</th>" not in page or "<th>Loss years with 10 or more claims in the peak month</th>" not in page:
            bad.append(f"{key}: loss-years column not labelled 'at least one claim', or no 10-or-more column (round 3 M2)")
        m = re.search(r"In the median county, the largest loss year holds ([\d.]+)% of the peak month's claims .*?peak month had 10 or more claims in ([\d.]+) of the ", text(page))
        want_g = (round(statistics.median(t["cal"][6][0] for t in T), 1), float(statistics.median(t["cal"][5][0] for t in T)))
        if not m or (float(m[1]), float(m[2])) != want_g: bad.append(f"{key}: Abstract graded figures {m and m.groups()} vs {want_g} (round 3 M1)")
        # label-vs-data (round 2): Wilson ranges assume independent claims and ignore the peak pick; the table must say both
        # owner 11-15: the two reasons are explained once, in Limitations; the table labels its ranges and points there
        tb = page[page.find('id="table"'):page.find('id="limitations"')]; lim = page[page.find('id="limitations"'):page.find('id="reproduce"')]
        if "<th>90% range if claims were independent</th>" not in tb or "if claims were independent" not in tb.split("<table>")[0] or "picked from the same claims" not in lim or "not independent" not in lim or "<th>Fifth by excess over chance</th>" not in tb:
            bad.append(f"{key}: table does not say its ranges assume independent claims, Limitations does not give the peak pick, or fifths are not by excess (round 2)")
        rs = page[page.find('id="results"'):page.find('id="prior"')]
        if "(90% range if claims were independent " not in rs or "Highest:" in rs: bad.append(f"{key}: Results range not labelled 'if claims were independent'")
        ab = page[page.find('id="abstract"'):page.find('id="question"')]
        if "Main finding:</b> In " not in ab.split("<b>Data:</b>")[0]: bad.append(f"{key}: Abstract does not lead with the one-year finding (round 2)")
        m = re.search(r"[Tt]he median county's share is ([\d.]+)%, against a median expected share at random of ([\d.]+)%", ab)
        want_m = (round(statistics.median(t["v"] for t in T), 1), round(statistics.median(t["e"] for t in T), 1))
        if not m or (float(m[1]), float(m[2])) != want_m: bad.append(f"{key}: Abstract median vs chance {m and m.groups()} vs {want_m}")
        m = re.search(r"the largest excess is .*?: ([\d.]+)% against ([\d.]+)% expected at random \(([\d,]+) of ([\d,]+)\)", text(ab))
        if not m or (float(m[1]), float(m[2]), int(m[3].replace(",", "")), int(m[4].replace(",", ""))) != (T[0]["v"], T[0]["e"], T[0]["k"], T[0]["n"]): bad.append(f"{key}: Abstract largest excess {m and m.groups()} vs row 1")
        m = re.search(r"In ([\d,]+) of the [\d,]+ counties the peak month has at least 10 claims", page)
        if not m or int(m[1].replace(",", "")) != sum(1 for t in T if t["cal"][3]): bad.append(f"{key}: Abstract flag count {m and m[1]} vs {sum(1 for t in T if t['cal'][3])}")
        m = re.search(r"over half of those claims are from ([A-Z][a-z]+ \d{4}(?: and [A-Z][a-z]+ \d{4})*) alone", page)
        if (m and m[1]) != (T[0]["cal"][1] or None): bad.append(f"{key}: Abstract top-county flag {m and m[1]} vs {T[0]['cal'][1]}")
    cr = list(csv.DictReader(io.StringIO(csv_text or "")))
    hdr = next(csv.reader(io.StringIO(csv_text or "")), [])   # label vs data (stat review): the download line names every CSV column, in order
    m = re.search(r'\.csv">Download all [\d,]+ rows as CSV</a> \((\d+) columns: <code>([^<]*)</code>\)', page)
    if not m or int(m[1]) != len(hdr) or m[2].split(", ") != hdr: bad.append(f"{key}: CSV column list on the page {m and m.groups()} vs header {hdr}")
    if "below_any_amount_n" in hdr and not re.search(r"share_pct, ci90_low_pct, ci90_high_pct and numerator count policies at least \$\d+ a year below full-risk; below_any_amount_n, below_any_amount_pct and median_gap_usd_below_any_amount count policies below by any amount", page):
        bad.append(f"{key}: CSV note does not say which columns use the $ line and which the any-amount base")
    if len(cr) != len(T): bad.append(f"{key}: CSV {len(cr)} rows, recompute {len(T)}")
    tc = {t["c"]: t for t in T}
    for r in cr:
        t = tc.get(r["county_fips"])
        if not t or (int(r["numerator"]), int(r["denominator"]), float(r["share_pct"]), (float(r["ci90_low_pct"]), float(r["ci90_high_pct"])), int(r["fifth"])) != (t["k"], t["n"], t["v"], t["ci"], t["fifth"]):
            bad.append(f"{key}: CSV row {r.get('county_fips')} disagrees with recompute"); break
        if key in EXTRA and ((r["median_excess_usd"] or None) != (None if t["ex"] is None else str(t["ex"])) or (r["loss_year_over_half"] or None) != t["yr"]):
            bad.append(f"{key}: CSV row {r['county_fips']} excess/year disagrees with recompute"); break
        if key == "flood-calendar" and (r["peak_months"], r["year_month_over_half"], float(r["expected_share_at_random_pct"]), float(r["excess_points"]), r["peak_month_loss_years_any"], r["largest_year_share_of_peak_pct"], r["peak_month_loss_years_10plus"]) != (*t["cal"][2:4], t["e"], t["x"], *(";".join(map(str, t["cal"][i])) for i in (4, 6, 5))):
            bad.append(f"{key}: CSV row {r['county_fips']} peak month/flag disagrees with recompute"); break
    for c, h in cards.items():   # every county page: the card's share and fifth = recompute, or "not listed" when not in T
        m = re.search(rf'data-paper="{key}" data-fifth="(\d)"', h)
        if not m: bad.append(f"{c}: no {key} line"); continue
        if int(m[1]) != (tc[c]["fifth"] if c in tc else 0): bad.append(f"{c}: {key} fifth {m[1]} vs {tc[c]['fifth'] if c in tc else 0}")
        if key in NULL and int(m[1]) and ("90%</span> range" not in h[m.end():h.find("</li>", m.end())] or "At random, " not in h[m.end():h.find("</li>", m.end())]):
            bad.append(f"{c}: {key} card has no 90% range or no chance expectation (round 2; reviewer 11-15: the independence caveat lives on the paper page)")
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
    STAGED.update(s["key"] for s in papers.READY if not s.get("published"))
    SITEMAP = open(os.path.join(D, "sitemap.xml"), encoding="utf-8").read() if os.path.exists(os.path.join(D, "sitemap.xml")) else ""
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
                    "plain median wrong": (re.sub(r"(median listed county (?:it (?:is|was)|the (?:busiest|peak) month held) )([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1), csv_text, cards),
                    "lookup not first": (page.replace('id="plain"', 'id="x"', 1), csv_text, cards),
                    "banned word": (page.replace("</h1>", " the worst counties</h1>", 1), csv_text, cards),
                    "share changed": (re.sub(r"(<td>\w+ fifth</td><td>.*?</td><td>)([\d.]+)%", lambda m: m[1] + "0.1%", page, count=1), csv_text, cards),
                    "range dropped": (re.sub(r"<td>[\d.]+–[\d.]+%</td>", "<td></td>", page, count=1), csv_text, cards),
                    "csv row dropped": (page, "\n".join(csv_text.splitlines()[:-1]) + "\n", cards),
                    "policy share wrong": (re.sub(r"(</td><td>[\d,]+ of [\d,]+</td><td>)([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1) if "Policy units outside" in page else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "excess wrong": (re.sub(r"( of [\d,]+</td><td>\$)([\d,]+)", lambda m: m[1] + "1", page, count=1) if key in EXTRA else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "abstract flag wrong": (re.sub(r"(from one loss year, \d{4}, which may hold one flood or several \()([\d,]+)", lambda m: m[1] + "9999", page, count=1) if key in EXTRA else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "label word": (page.replace("</h1>", LABEL_MUT[key] + "</h1>", 1) if key in LABEL else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "version link dropped": (re.sub(rf'href="/flood-insurance/{key}/\d{{4}}-\d{{2}}-\d{{2}}/"', 'href="/"', page), csv_text, cards),
                    "lookup dropped": (page.replace('id="ps"', 'id="x"') if len(T) > 500 else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "peak month wrong": (re.sub(r"( of [\d,]+</td><td>[\d.]+%</td><td>[+-][\d.]+</td><td>)([A-Z][a-z]+)(</td>)", lambda m: m[1] + ("May" if m[2] != "May" else "June") + m[3], page, count=1) if key == "flood-calendar" else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "one-year flag dropped": (re.sub(r"(%</td><td>[\d,]+</td><td>[\d,]+</td><td>)[A-Z][a-z]+ \d{4}(</td>)", lambda m: m[1] + m[2], page, count=1) if key == "flood-calendar" else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    "flag count wrong": (re.sub(r"In ([\d,]+) of the ([\d,]+) counties the peak month", r"In 1 of the \2 counties the peak month", page, count=1) if key == "flood-calendar" else page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    **({"expected wrong": (re.sub(r"( of [\d,]+</td><td>)([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1), csv_text, cards),
                        "excess wrong": (re.sub(r"( of [\d,]+</td><td>[\d.]+%</td><td>)([+-])", lambda m: m[1] + ("-" if m[2] == "+" else "+"), page, count=1), csv_text, cards),
                        "loss years wrong": (re.sub(r"(</td><td>[A-Z][a-z]+</td><td>[\d.]+%</td><td>)(\d+)(</td>)", lambda m: f"{m[1]}{int(m[2]) + 1}{m[3]}", page, count=1), csv_text, cards),
                        "largest-year share wrong": (re.sub(r"(</td><td>[A-Z][a-z]+</td><td>)([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) / 2}%", page, count=1), csv_text, cards),
                        "10+ years wrong": (re.sub(r"(</td><td>[A-Z][a-z]+</td><td>[\d.]+%</td><td>\d+</td><td>)(\d+)(</td>)", lambda m: f"{m[1]}{int(m[2]) + 1}{m[3]}", page, count=1), csv_text, cards),
                        "overclaim back": (page.replace("This does not say whether the month", "So the peak month is not a pattern that repeats each year. This does not say whether the month", 1), csv_text, cards),
                        "loss years unlabelled": (page.replace("<th>Loss years with at least one claim in the peak month</th>", "<th>Loss years with claims in the peak month</th>"), csv_text, cards),
                        "graded median wrong": (re.sub(r"(largest loss year holds )([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1), csv_text, cards),
                        "csv 10+ years wrong": (page, re.sub(r"(?m)^(.*),(\d+)\r?$", lambda m: f"{m[1]},{int(m[2]) + 1}", csv_text, count=1), cards),
                        "independence label dropped": (page.replace("<th>90% range if claims were independent</th>", "<th>90% range</th>"), csv_text, cards),
                        "results range unlabelled": (page.replace("(90% range if claims were independent ", "(90% range ", 1).replace("Largest excess over chance:", "Highest:", 1), csv_text, cards),
                        "peak-pick cause dropped": (page.replace("picked from the same claims", "chosen", 1), csv_text, cards),
                        "table range note dropped": (page.replace("Each 90% range is the one that would hold if claims were independent; ", "", 1), csv_text, cards),
                        "fifths by share": (page.replace("<th>Fifth by excess over chance</th>", "<th>Fifth by share</th>"), csv_text, cards),
                        "finding not first": (re.sub(r'(<p class="stand"><b>Main finding:</b>.*?</p>)(\s*<p class="stand"><b>Data:</b>.*?</p>)', r"\2\1", page, count=1, flags=re.S), csv_text, cards),
                        "median chance wrong": (re.sub(r"(a median expected share at random of )([\d.]+)", lambda m: f"{m[1]}{float(m[2]) + 1}", page, count=1), csv_text, cards),
                        "largest excess wrong": (re.sub(r"(the largest excess is .*?: )([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1, flags=re.S), csv_text, cards),
                        "csv expected wrong": (page, re.sub(r"(?m)^((?:[^,\n]*,){13})([\d.]+)", lambda m: f"{m[1]}{float(m[2]) + 1}", csv_text, count=1), cards)} if key == "flood-calendar" else {}),
                    "card range unlabelled": (page, csv_text, {c: h.replace("At random, ", "So, ") for c, h in cards.items()}) if key in NULL else (page.replace('id="prior"', 'id="x"'), csv_text, cards),
                    **({"any share wrong": (re.sub(r"( of [\d,]+</td><td>)([\d.]+)%(</td><td>(?:\$[\d,]+|—)</td></tr>)", lambda m: f"{m[1]}{float(m[2]) + 1}%{m[3]}", page, count=1), csv_text, cards),
                        "median gap wrong": (re.sub(r"(%</td><td>\$)([\d,]+)(</td></tr>)", lambda m: m[1] + "1" + m[3], page, count=1), csv_text, cards),
                        "csv any wrong": (page, re.sub(r"(?m)^((?:[^,\n]*,){12})([\d.]+)", lambda m: f"{m[1]}{float(m[2]) + 1}", csv_text, count=1), cards),
                        "gao dropped": (page.replace("GAO-27-108012", "GAO"), csv_text, cards),
                        "pooled $10 wrong": (re.sub(r"([\d.]+)(% by \$10 or more)", lambda m: f"{float(m[1]) + 1}{m[2]}", page, count=1), csv_text, cards),
                        "crs share wrong": (re.sub(r"(<tr><td>Class \d+</td><td>[\d,]+</td><td>)([\d.]+)", lambda m: f"{m[1]}{float(m[2]) + 1}", page, count=1), csv_text, cards),
                        "crs line dropped": (re.sub(r"<li>By the CRS class code.*?</li>", "", page, count=1, flags=re.S), csv_text, cards),
                        "reconcile wrong": (re.sub(r"(: here )([\d.]+)%", lambda m: f"{m[1]}{float(m[2]) + 1}%", page, count=1), csv_text, cards)} if key == "price-gap" else {}),
                    "csv column unlisted": (re.sub(r"(rows as CSV</a> \(\d+ columns: <code>)[^,]+, ", r"\1", page, count=1), csv_text, cards),
                    "csv column added": (page, csv_text.replace(csv_text.splitlines()[0], csv_text.splitlines()[0] + ",extra", 1), cards),
                    **({"csv base note dropped": (page.replace(" count policies below by any amount", " are extra", 1), csv_text, cards)} if key == "price-gap" else {}),
                    "card fifth wrong": (page, csv_text, {c: re.sub(rf'data-paper="{key}" data-fifth="(\d)"', lambda m: f'data-paper="{key}" data-fifth="{(int(m[1]) % 5) + 1}"', h, count=1) for c, h in cards.items()})}
            for k, (pg, cs, cd) in muts.items(): assert check(key, pg, cs, cd, T), f"{key}: missed {k}"
            if key in STAGED:   # M3.5 mutations: noindex dropped; URL put in the sitemap
                assert check(key, page.replace('content="noindex', 'content="index'), csv_text, cards, T), f"{key}: missed noindex dropped"
                assert check(key, page, csv_text, cards, T, sm=SITEMAP + f"<loc>https://x/flood-insurance/{key}/</loc>"), f"{key}: missed sitemap entry"
            if key == "flood-calendar":   # oracle: the statistician's own no-seasonality simulation (round 2), then year-months vs months
                assert [chance(n) for n in (100, 473, 2000)] == [13.3, 10.6, 9.4], [chance(n) for n in (100, 473, 2000)]
                c0 = next(c for c, r in recs.items() if mon(r)); m8 = dict(recs); m8[c0] = json.loads(json.dumps(recs[c0]))
                m8[c0]["extras"]["claims"]["loss_month_n"]["by_year_month"] = {}
                assert months_add_up(m8) and not months_add_up(recs), "flood-calendar: missed year-months vs months"
            if key == "price-gap":   # M3 mutation: the CRS split gains a policy the base does not hold
                c0 = next(c for c, r in recs.items() if g(r, ("extras", "policies", "below_by_crs")))
                m9 = dict(recs); m9[c0] = json.loads(json.dumps(recs[c0])); k0 = next(iter(m9[c0]["extras"]["policies"]["below_by_crs"]))
                m9[c0]["extras"]["policies"]["below_by_crs"][k0][0] += 1
                assert crs_adds_up(m9) and not crs_adds_up(recs), "price-gap: missed CRS split vs base"
            if key == "deductible-choice":   # M1.7 mutation: one county's records hold two units each
                c0 = next(c for c, r in recs.items() if g(r, ("extras", "policies", "deductible_units")))
                m7 = dict(recs); m7[c0] = json.loads(json.dumps(recs[c0])); m7[c0]["extras"]["policies"]["sf_n"] //= 2
                assert units_are_records(m7) and not units_are_records(recs), "deductible-choice: missed units vs records"
            if re.search(r"\bNone\b", text(page)): assert False, f"{key}: 'None' printed on the page"
            assert not check(key, page, csv_text, cards, T), check(key, page, csv_text, cards, T)[:3]
            print(f"{key}: {len(muts)} mutations caught"); continue
        bad += check(key, page, csv_text, cards, T) + (units_are_records(recs) if key == "deductible-choice" else []) + (months_add_up(recs) if key == "flood-calendar" else []) + (crs_adds_up(recs) + units_are_records(recs) if key == "price-gap" else []) + ([f"{key}: 'None' printed"] if re.search(r"\bNone\b", text(page)) else [])
        print(f"{key}: {len(T)} counties recomputed")
    if "--test" not in sys.argv: bad += sameness(pages)
    for b in bad[:15]: print("PAPER GATE FAIL", b)
    print("PAPER GATE", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
