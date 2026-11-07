"""Address tool (zonemap.js) ship standard: an independent Python oracle of what the tool may say for every kind of
FEMA answer, the page's own describe() must equal it; the full click path runs in a real browser with FEMA and the
Census geocoder answered by fixtures (FEMA refuses non-US connections, so local runs never touch the network);
fuzz (random FEMA answers: no crash, no NaN/undefined/null/Infinity, only oracle sentences); JS off = FEMA link.
Usage: python -I tools/test_zonemap.py [--browser chromium|webkit]   (needs dist/ built with the zonemap flag on)"""
import datetime, functools, http.server, json, os, random, re, sys, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROWSER = sys.argv[sys.argv.index("--browser") + 1] if "--browser" in sys.argv else "chromium"
M = "January February March April May June July August September October November December".split()

def name(a):
    z, s = str(a.get("FLD_ZONE") or "").strip(), str(a.get("ZONE_SUBTY") or "").strip()
    return ("Zone " + z + (f" ({s.lower()})" if s else "")) if z else None

def oracle(point, box, panel):   # written from the rule text in CLAUDE.md, not from the JS
    if point is None or box is None or "error" in point or "error" in box:
        return ["FEMA's map service did not answer. Check this spot on FEMA's map."]
    here = [f.get("attributes") or {} for f in point.get("features") or []]
    here = [a for a in here if name(a)]
    if not here:
        return ["FEMA's digital flood map shows no flood zone at this pin. That is not a finding of no flood risk: FEMA's digital map does not cover every place. Check this spot on FEMA's map."]
    near = []
    for a in here + [f.get("attributes") or {} for f in box.get("features") or []]:
        n = name(a)
        if n and n not in near: near.append(n)
    out = [f"A zone line is within 15 meters (about 50 feet) of this pin. FEMA's map shows: {'; '.join(near)}." if len(near) > 1
           else f"FEMA's map shows {name(here[0])} at this pin."]
    sf = str(here[0].get("SFHA_TF") or "").upper()
    if sf == "T": out.append("FEMA marks this spot as a Special Flood Hazard Area (high-risk).")
    elif sf == "F" and len(near) == 1 and str(here[0].get("FLD_ZONE")).strip() == "X": out.append("FEMA does not mark this spot as a Special Flood Hazard Area.")
    p = (panel or {}).get("features") if panel and "error" not in panel else None
    p = (p[0].get("attributes") or {}) if p else None
    if p and p.get("FIRM_PAN"):
        e = p.get("EFF_DATE"); d = None
        if isinstance(e, (int, float)) and not isinstance(e, bool) and abs(e) < 8.64e15:
            t = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=e); d = f"{M[t.month - 1]} {t.day}, {t.year}"
        out.append(f"FEMA map panel {str(p['FIRM_PAN']).strip()}" + (f", in effect since {d}" if d else "") + ".")
    return out

F = lambda *rows: {"features": [{"attributes": r} for r in rows]}
CASES = {   # every branch: one zone, zone line nearby, nothing, FEMA error, FEMA silent, panel missing, odd fields
    "AE high-risk": (F({"FLD_ZONE": "AE", "ZONE_SUBTY": None, "SFHA_TF": "T"}), F({"FLD_ZONE": "AE"}), F({"FIRM_PAN": "12099C0587F", "EFF_DATE": 1734652800000})),
    "X shaded": (F({"FLD_ZONE": "X", "ZONE_SUBTY": "0.2 PCT ANNUAL CHANCE FLOOD HAZARD", "SFHA_TF": "F"}), F({"FLD_ZONE": "X", "ZONE_SUBTY": "0.2 PCT ANNUAL CHANCE FLOOD HAZARD"}), F({"FIRM_PAN": "12103C0109H", "EFF_DATE": 1507161600000})),
    "zone line": (F({"FLD_ZONE": "X", "ZONE_SUBTY": "AREA OF MINIMAL FLOOD HAZARD", "SFHA_TF": "F"}), F({"FLD_ZONE": "X", "ZONE_SUBTY": "AREA OF MINIMAL FLOOD HAZARD"}, {"FLD_ZONE": "AE"}), F({"FIRM_PAN": "48201C0880M", "EFF_DATE": 1573776000000})),
    "floodway": (F({"FLD_ZONE": "AE", "ZONE_SUBTY": "FLOODWAY", "SFHA_TF": "T"}), F(), None),
    "nothing": (F(), F(), F()),
    "blank zone": (F({"FLD_ZONE": "  ", "SFHA_TF": "F"}), F(), F()),
    "fema error": ({"error": {"code": 500}}, F(), F()),
    "fema silent": (None, None, None),
    "box silent": (F({"FLD_ZONE": "VE", "SFHA_TF": "T"}), None, F()),
    "panel error": (F({"FLD_ZONE": "D", "SFHA_TF": "F"}), F({"FLD_ZONE": "D"}), {"error": {}}),
    "panel no date": (F({"FLD_ZONE": "A", "SFHA_TF": "T"}), F(), F({"FIRM_PAN": "22071C0115E", "EFF_DATE": None})),
}

def fuzz(r):
    pick = lambda xs: r.choice(xs)
    zone = lambda: {"FLD_ZONE": pick(["AE", "X", "VE", "A", "AO", "AH", "D", "", None, 7, "OPEN WATER"]),
                    "ZONE_SUBTY": pick([None, "", "FLOODWAY", "0.2 PCT ANNUAL CHANCE FLOOD HAZARD", 3]), "SFHA_TF": pick(["T", "F", "t", None, ""])}
    resp = lambda mk: pick([None, {"error": {}}, {}, {"features": None}, F(*[mk() for _ in range(r.randint(0, 3))])])
    pan = lambda: {"FIRM_PAN": pick(["12099C0587F", None, "", 5]), "EFF_DATE": pick([1734652800000, None, "x", -1, 0, 1e300])}
    return resp(zone), resp(zone), resp(pan)

def main():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=os.path.join(ROOT, "dist")))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    host = f"http://127.0.0.1:{srv.server_address[1]}"
    page_url = host + "/flood-insurance/palm-beach-county-fl/"
    bad = []
    with sync_playwright() as p:
        b = getattr(p, BROWSER).launch()
        # 1. the page's describe() equals the oracle, fixtures + fuzz
        pg = b.new_page()
        pg.goto("file:///" + os.path.join(ROOT, "dist", "index.html").replace("\\", "/"))
        pg.add_script_tag(path=os.path.join(ROOT, "dist", "zonemap.js"))
        cases = list(CASES.items()) + [(f"fuzz {i}", fuzz(random.Random(i))) for i in range(3000)]
        got = pg.evaluate("cs => cs.map(c => window.__zmDescribe(c[0], c[1], c[2]).lines)", [list(c) for _, c in cases])
        for (k, c), g in zip(cases, got):
            want = oracle(*c)
            if g != want: bad.append(f"{k}: page {g} != oracle {want}")
            if any(re.search(r"NaN|undefined|null|Infinity|\[object", s) for s in g): bad.append(f"{k}: bad token in {g}")
        # 2. full click path on a real page, network answered by fixtures
        ctx = b.new_context(viewport={"width": 390, "height": 844}, geolocation={"latitude": 26.7, "longitude": -80.1}, permissions=["geolocation"])
        pt, bx, pn = CASES["zone line"]
        def route(r):
            u = r.request.url
            if "geocoding.geo.census.gov" in u:
                cb = re.search(r"callback=([\w$]+)", u)[1]
                body = cb + '({"result":{"addressMatches":[{"matchedAddress":"301 N OLIVE AVE, WEST PALM BEACH, FL, 33401","coordinates":{"x":-80.0533,"y":26.7153}}]}})'
                return r.fulfill(status=200, content_type="application/javascript", body=body)
            if "/MapServer/28/query" in u: return r.fulfill(status=200, content_type="application/json", body=json.dumps(bx if "Envelope" in u else pt))
            if "/MapServer/3/query" in u: return r.fulfill(status=200, content_type="application/json", body=json.dumps(pn))
            if "/export?" in u or "basemap.nationalmap.gov" in u: return r.fulfill(status=200, content_type="image/png", body=b"")
            if u.startswith(host): return r.continue_()
            return r.abort()
        pg = ctx.new_page(); pg.route("**/*", route); pg.goto(page_url)
        if pg.locator("#zm .zm-open").count() != 1: bad.append("click path: no tool on the sample page")
        else:
            pg.click("#zm .zm-open"); pg.fill("#zm .zm-addr", "301 N Olive Ave, West Palm Beach, FL")
            pg.wait_for_function("window.__zmStart !== undefined", timeout=15000)
            pg.click("#zm .zm-go"); pg.wait_for_selector("#zm .zm-ok", timeout=15000)
            pre = pg.inner_text("#zm .zm-out")
            if "FEMA's map shows" in pre: bad.append("click path: a zone was named before the reader confirmed the pin")
            if "Matched address: 301 N OLIVE AVE" not in pre: bad.append("click path: matched address not shown")
            pg.click("#zm .zm-ok"); pg.wait_for_function("document.querySelector('#zm .zm-out').innerText.includes('FEMA')", timeout=15000)
            pg.wait_for_timeout(300)
            out = pg.inner_text("#zm .zm-out")
            for s in oracle(pt, bx, pn) + ["FEMA's map, not an official determination."]:
                if s not in out: bad.append(f"click path: missing {s!r}")
            if "Check it on FEMA's map" not in out: bad.append("click path: no FEMA link after the answer")
        # 3. JS off: a plain link to FEMA's map, no form
        nj = b.new_context(java_script_enabled=False).new_page(); nj.goto(page_url)
        a = nj.locator("#zm a.zm-open")
        if a.count() != 1 or "msc.fema.gov" not in (a.get_attribute("href") or "") or not a.is_visible(): bad.append("JS off: FEMA link missing or hidden")
        b.close()
    srv.shutdown()
    for x in bad[:20]: print("  -", x)
    print(f"ZONEMAP TOOL {'FAIL' if bad else 'PASS'} ({BROWSER}): {len(cases)} answers vs oracle, click path, JS off")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
