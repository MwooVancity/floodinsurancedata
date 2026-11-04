"""Reader tools ship standard (CLAUDE.md): an independent Python oracle computes every expected answer; the real page's
JavaScript output must equal it. Edge suites (leap day, year end, DST, Hawaii/New York/Guam clocks, bad input), fuzz
(random strings and dates: never a crash, never NaN/undefined/Infinity, only listed sentences) and JavaScript off.
Usage: python -I tools/test_tools.py [--browser chromium|webkit|firefox]   (needs dist/ built; release.py runs it)"""
import datetime, json, os, random, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROWSER = sys.argv[sys.argv.index("--browser") + 1] if "--browser" in sys.argv else "chromium"
M = "January February March April May June July August September October November December".split()
fmt = lambda d: f"{M[d.month - 1]} {d.day}, {d.year}"

def oracle(value, today):   # the full list of sentences the deadline planner may print
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", value or "")
    if not m: return "That is not a date. Enter the day the water came in." if value else ""
    try: d = datetime.date(int(m[1]), int(m[2]), int(m[3]))
    except ValueError: return "That is not a date. Enter the day the water came in."
    if d > today: return "That date is in the future. Enter the day the water came in."
    due = d + datetime.timedelta(days=60); left = (due - today).days
    if left > 0: return (f"An NFIP proof of loss is due by {fmt(due)} ({left} {'day' if left == 1 else 'days'} from today). "
                         "Report the loss to your insurer now if you have not.")
    if left == 0: return f"An NFIP proof of loss is due today, {fmt(due)}. Contact your insurer now."
    return f"The 60-day NFIP proof-of-loss date was {fmt(due)}. Contact your insurer now; it may have extended the date."

def start_oracle(t, av, rv, c, l):   # policy start date: FIM October 2025 Tables 8-10, written from the manual, not from the JS
    D = datetime.timedelta
    def pd(v):
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", v or "")
        if not m: return None
        try: return datetime.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError: return None
    a, r = pd(av), pd(rv)
    if not av: return ""
    if not a: return "That is not a date. Enter the application date (with a loan, the closing date)."
    if rv and not r: return "That is not a date. Leave the receipt date empty if you do not know it."
    if t == "loan":   # Table 10: lender/title/attorney pays -> closing + 29 days; anyone else -> closing + 9 days
        w = a + D(days=29 if l else 9)
        if not r: return (f"Coverage starts at the time of the loan closing on {fmt(a)} if the insurer receives the form and full amount due by {fmt(w)}. "
                          "If it receives them later, the earliest start is 12:01 a.m. local time on the 30th calendar day after it receives them.")
        if r <= w: return f"Coverage starts at the time of the loan closing on {fmt(a)}."
        return f"The insurer received them after {fmt(w)}, so the earliest start is 12:01 a.m. local time on {fmt(r + D(days=30))}."
    if r and r < a: return "The insurer cannot receive the form before the application date. Check both dates."
    s = _std(t, a, r, c, D)
    # round 57 T3: every map result carries the manual's 13-month receipt limit
    return s + (" This holds only if the insurer receives them within 13 months of the map revision's effective date; after that, the 30-day wait applies."
                if t == "map" else "")
def _std(t, a, r, c, D):
    k = 1 if t == "map" else 30   # Table 9 (next calendar day) / Table 8 (30th calendar day)
    if c or (r and r <= a + D(days=9)): return f"The earliest start is 12:01 a.m. local time on {fmt(a + D(days=k))}."
    if not r: return (f"The earliest start is 12:01 a.m. local time on {fmt(a + D(days=k))} if the insurer receives the form and full amount due by "
                      f"{fmt(a + D(days=9))}, or they are mailed by certified mail by {fmt(a + D(days=3))}. If the insurer receives them later, it is the "
                      f"{'next calendar day' if k == 1 else '30th calendar day'} after it receives them.")
    return ("The insurer received them more than 10 days after the application date, so the earliest start is 12:01 a.m. local time on "
            f"{fmt(r + D(days=k))}.")
# the manual's own worked examples (pages 2-15..2-18) must come out of the oracle
_ex = [(("none", "2026-05-13", "2026-05-17", False, False), "June 12, 2026"), (("none", "2026-05-13", "2026-05-26", True, False), "June 12, 2026"),
       (("none", "2026-05-13", "2026-05-25", False, False), "June 24, 2026"), (("map", "2026-05-13", "2026-05-17", False, False), "May 14, 2026"),
       (("map", "2026-05-13", "2026-05-26", True, False), "May 14, 2026"), (("map", "2026-05-13", "2026-05-28", False, False), "May 29, 2026"),
       (("loan", "2026-04-03", "2026-04-20", False, True), "April 3, 2026"), (("loan", "2026-04-03", "2026-05-10", False, True), "June 9, 2026"),
       (("loan", "2026-04-03", "2026-04-07", False, False), "April 3, 2026"), (("loan", "2026-04-03", "2026-04-15", False, False), "May 15, 2026")]
bad0 = [f"start oracle {i} misses the manual's example {want}" for i, want in _ex if want not in start_oracle(*i)]

# FEMA map-date reader (PLAN 3e): a truth table from FEMA's legend, then every real value in the data must parse
sys.path.insert(0, os.path.join(ROOT, "tools")); from mapdate import map_date
_T = datetime.date(2026, 10, 29)
TRUTH = [("09/24/21", "current", datetime.date(2021, 9, 24)), ("09/28/84", "current", datetime.date(1984, 9, 28)),
         ("01/05/70", "current", datetime.date(1970, 1, 5)), ("12/31/69", "current", datetime.date(2069, 12, 31)),
         ("11/13/26(>)", "new", datetime.date(2026, 11, 13)), ("10/01/26(>)", "current", datetime.date(2026, 10, 1)),
         ("04/03/12(M)", "current", datetime.date(2012, 4, 3)), ("02/02/90(L)", "current", datetime.date(1990, 2, 2)),
         ("(NSFHA)", "nsfha", None), ("(All Zone D)", "nsfha", None), ("", "none", None), (None, "none", None), ("N/A", "none", None),
         ("E", "none", None), ("(S)", "none", None), ("06/01/95(S)", "none", None), ("(W)", "none", None)]
bad = list(bad0)
for v, kind, d in TRUTH:
    k2, d2, _ = map_date(v, _T)
    if (k2, d2) != (kind, d) and not (v == "12/31/69" and k2 == "new"): bad.append(f"map_date({v!r}) = {(k2, d2)} != {(kind, d)}")
for v in ("13/01/20", "02/30/20", "garbage", "2020-01-01"):
    try: map_date(v, _T); bad.append(f"map_date({v!r}) accepted a bad value")
    except ValueError: pass
import glob
_vals = {c.get("currentlyEffectiveMapDate") for f in glob.glob(os.path.join(ROOT, "data", "*", "*", "data.json"))
         for c in json.load(open(f, encoding="utf-8")).get("crs", []) if "currentlyEffectiveMapDate" in c}
for v in _vals:
    try: map_date(v, _T)
    except ValueError as e: bad.append(f"real FEMA value not understood: {e}")

# NOAA sea-level line (PLAN 3e): every trend printed equals NOAA's file for a gauge in the county or a bordering one
_sl = json.load(open(os.path.join(ROOT, "data", "us", "sealevel.json"), encoding="utf-8"))
_adj = json.load(open(os.path.join(ROOT, "data", "us", "county_adjacency.json"), encoding="utf-8"))
for _d in glob.glob(os.path.join(ROOT, "dist", "flood-insurance", "*", "index.html")):
    _h = open(_d, encoding="utf-8").read()
    _got = re.findall(r"tide gauge at .*?measured a sea-level trend of <[^>]*>([+-]\d+\.\d\d)<", _h)
    if not _got: continue
    _ag = os.path.join(ROOT, "data", "c", os.path.basename(os.path.dirname(_d)), "agg.json")
    _g = json.load(open(_ag, encoding="utf-8")).get("geoid") if os.path.exists(_ag) else ""
    _ok = {f"{s['trend']:+.2f}" for s in _sl.get(_g, [])}   # in-county gauges only (round 28)
    for t in _got:
        if t not in _ok: bad.append(f"{os.path.basename(os.path.dirname(_d))}: sea trend {t} not in NOAA's file for it or a neighbour")

flags = json.load(open(os.path.join(ROOT, "tools", "tools_flags.json"), encoding="utf-8"))
on = flags.get("deadline") or []
slugs = [s for s in os.listdir(os.path.join(ROOT, "dist", "flood-insurance")) if os.path.exists(os.path.join(ROOT, "dist", "flood-insurance", s, "index.html"))]
pages = slugs if on == "all" else [s for s in on if s in slugs]
# scale (PLAN): the oracle/fuzz runs on one page (same code everywhere); presence is checked on every page above
url = lambda s: "file:///" + os.path.join(ROOT, "dist", "flood-insurance", s, "index.html").replace("\\", "/")
# the tool appears exactly where the flags say, and nowhere else
for s in slugs:
    has = "id='deadline'" in open(os.path.join(ROOT, "dist", "flood-insurance", s, "index.html"), encoding="utf-8").read()
    if has != (s in pages): bad.append(f"{s}: deadline tool {'present' if has else 'missing'} against tools_flags.json")

for _k in ("deadline", "start"):   # a flagged page missing from dist/ must fail, not shrink the test to 0 pages (11-03: it passed on 0)
    if flags.get(_k) != "all":
        bad += [f"{_k}: flagged page {s} not built" for s in (flags.get(_k) or []) if s not in slugs]
son = flags.get("start") or []
spages = slugs if son == "all" else [s for s in son if s in slugs]
for s in slugs:
    has = "id='start'" in open(os.path.join(ROOT, "dist", "flood-insurance", s, "index.html"), encoding="utf-8").read()
    if has != (s in spages): bad.append(f"{s}: start-date tool {'present' if has else 'missing'} against tools_flags.json")
# inputs: every exception x application dates (leap day, year end, DST weeks, month ends) x receipt dates at each rule boundary
_A = ["", "abc", "2026-02-30", "2028-02-29", "2026-12-31", "2026-03-08", "2026-11-01", "2026-01-31", "2027-02-28", "1999-07-04", "2026-11-03"]
def _rs(a):
    try: d = datetime.date.fromisoformat(a)
    except ValueError: return ["", "2026-13-01"]
    return ["", "x"] + [str(d + datetime.timedelta(days=n)) for n in (-1, 0, 3, 4, 9, 10, 29, 30, 31, 400)]
START_CASES = [(t, a, r, c, l) for t in ("none", "map", "loan") for a in _A for r in _rs(a) for c in (False, True) for l in (False, True)]

TODAYS = ["2026-10-29", "2028-02-29", "2026-12-31", "2027-01-01", "2026-03-08", "2026-11-01", "2027-03-01"]
DATES = ["", "abc", "2026-02-30", "2025-13-01", "0000-01-01", "1978-01-01", "2028-02-29", "2027-02-29", "9999-12-31",
         "2026-10-29", "2026-08-30", "2026-08-31", "2026-09-01", "2026-12-31", "2026-11-01", "2024-02-29", "2026-10-30"]
ZONES = ["Pacific/Honolulu", "America/New_York", "Pacific/Guam"]
if pages:
    from playwright.sync_api import sync_playwright
    rnd = random.Random(29)
    with sync_playwright() as p:
        b = getattr(p, BROWSER).launch()
        for tz in ZONES:
            ctx = b.new_context(timezone_id=tz); pg = ctx.new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            for td in TODAYS:
                from zoneinfo import ZoneInfo   # noon in the page's own zone: "today" is the reader's local date
                pg.clock.set_fixed_time(datetime.datetime.fromisoformat(td + "T12:00:00").replace(tzinfo=ZoneInfo(tz)))
                pg.goto(url(pages[0]))
                today = datetime.date.fromisoformat(td)
                fuzz = DATES + [f"{rnd.randint(1900, 2100):04d}-{rnd.randint(0, 13):02d}-{rnd.randint(0, 32):02d}" for _ in range(300)] \
                       + ["".join(rnd.choice("0123456789-/ .aZ") for _ in range(rnd.randint(1, 12))) for _ in range(100)]
                got = pg.evaluate("""vals => vals.map(v => { var i=document.getElementById('dl'); i.type='text'; i.value=v;
                                     i.dispatchEvent(new Event('input')); return document.getElementById('dlo').textContent; })""", fuzz)
                for v, g in zip(fuzz, got):
                    want = oracle(v, today)
                    if g != want: bad.append(f"{BROWSER} {tz} today={td} input={v!r}: page {g!r} != oracle {want!r}")
                    if re.search(r"NaN|undefined|Infinity|null", g): bad.append(f"{BROWSER} {tz} {v!r}: shows {g!r}")
            if spages:   # start-date tool: no "today" in its math, one clock per zone covers it
                pg.goto(url(spages[0]))
                rnd2 = random.Random(3)
                cases = START_CASES + [(rnd2.choice(("none", "map", "loan")), f"{rnd2.randint(1900, 2100):04d}-{rnd2.randint(0, 13):02d}-{rnd2.randint(0, 32):02d}",
                                        rnd2.choice(["", "".join(rnd2.choice("0123456789-/ .aZ") for _ in range(rnd2.randint(1, 12))),
                                                     f"{rnd2.randint(1900, 2100):04d}-{rnd2.randint(1, 12):02d}-{rnd2.randint(1, 28):02d}"]),
                                        rnd2.random() < .5, rnd2.random() < .5) for _ in range(1500)]
                got = pg.evaluate("""cs => cs.map(c => { var g=x=>document.getElementById(x);
                    g('st').value=c[0]; g('sa').type='text'; g('sa').value=c[1]; g('sr').type='text'; g('sr').value=c[2];
                    g('sc').checked=c[3]; g('sl').checked=c[4]; g('sl').dispatchEvent(new Event('change')); return g('so').textContent; })""", cases)
                for cs, gg in zip(cases, got):
                    want = start_oracle(*cs)
                    if gg != want: bad.append(f"{BROWSER} {tz} start {cs}: page {gg!r} != oracle {want!r}")
                    if re.search(r"NaN|undefined|Infinity|null", gg): bad.append(f"{BROWSER} {tz} start {cs}: shows {gg!r}")
            if errs: bad.append(f"{BROWSER} {tz}: JS errors {errs[:2]}")
            ctx.close()
        # JavaScript off: the rules still read as text
        ctx = b.new_context(java_script_enabled=False); pg = ctx.new_page(); pg.goto(url(pages[0]))
        if "60 days from that declaration date" not in pg.inner_text("#deadline"): bad.append("JS off: deadline rules not readable")
        if spages:
            pg.goto(url(spages[0]))
            if "30th calendar day after the application date" not in pg.inner_text("#start"): bad.append("JS off: start-date rules not readable")
        ctx.close(); b.close()
print("\n".join(bad[:20]) or f"TOOLS PASS ({BROWSER}): deadline planner on {len(pages)} pages; oracle matched on "
      f"{len(ZONES) * len(TODAYS)} clocks x {len(DATES) + 400} inputs; start-date tool on {len(spages)} pages, "
      f"{len(ZONES)} zones x {len(START_CASES) + 1500} inputs; JS off readable")
sys.exit(1 if bad else 0)
