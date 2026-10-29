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

# FEMA map-date reader (PLAN 3e): a truth table from FEMA's legend, then every real value in the data must parse
sys.path.insert(0, os.path.join(ROOT, "tools")); from mapdate import map_date
_T = datetime.date(2026, 10, 29)
TRUTH = [("09/24/21", "current", datetime.date(2021, 9, 24)), ("09/28/84", "current", datetime.date(1984, 9, 28)),
         ("01/05/70", "current", datetime.date(1970, 1, 5)), ("12/31/69", "current", datetime.date(2069, 12, 31)),
         ("11/13/26(>)", "new", datetime.date(2026, 11, 13)), ("10/01/26(>)", "current", datetime.date(2026, 10, 1)),
         ("04/03/12(M)", "current", datetime.date(2012, 4, 3)), ("02/02/90(L)", "current", datetime.date(1990, 2, 2)),
         ("(NSFHA)", "nsfha", None), ("(All Zone D)", "nsfha", None), ("", "none", None), (None, "none", None), ("N/A", "none", None),
         ("E", "none", None), ("(S)", "none", None), ("06/01/95(S)", "none", None), ("(W)", "none", None)]
bad = []
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
url = lambda s: "file:///" + os.path.join(ROOT, "dist", "flood-insurance", s, "index.html").replace("\\", "/")
# the tool appears exactly where the flags say, and nowhere else
for s in slugs:
    has = "id='deadline'" in open(os.path.join(ROOT, "dist", "flood-insurance", s, "index.html"), encoding="utf-8").read()
    if has != (s in pages): bad.append(f"{s}: deadline tool {'present' if has else 'missing'} against tools_flags.json")

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
            if errs: bad.append(f"{BROWSER} {tz}: JS errors {errs[:2]}")
            ctx.close()
        # JavaScript off: the rules still read as text
        ctx = b.new_context(java_script_enabled=False); pg = ctx.new_page(); pg.goto(url(pages[0]))
        if "60 days from that declaration date" not in pg.inner_text("#deadline"): bad.append("JS off: deadline rules not readable")
        ctx.close(); b.close()
print("\n".join(bad[:20]) or f"TOOLS PASS ({BROWSER}): deadline planner on {len(pages)} pages; oracle matched on "
      f"{len(ZONES) * len(TODAYS)} clocks x {len(DATES) + 400} inputs; JS off readable")
sys.exit(1 if bad else 0)
