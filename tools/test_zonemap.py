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

ZONES = re.compile(r"(A|A99|AE|AH|AO|AR|V|VE|X|D|B|C|A\d{1,2}|V\d{1,2})")   # FEMA zone letters; anything else is quoted, never "Zone ..."
def name(a):
    z, s = str(a.get("FLD_ZONE") or "").strip(), str(a.get("ZONE_SUBTY") or "").strip()
    return ("Zone " + z + (f" ({s.lower()})" if s else "")) if ZONES.fullmatch(z) else None

def _num(v, lo, hi):   # a FEMA number usable as printed: a real int/float inside the range (bool, NaN, text are not)
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and lo < v < hi

def _js(v):   # how JavaScript prints a number: 9.0 -> "9", 9.5 -> "9.5"
    return str(int(v)) if float(v).is_integer() else repr(float(v))

def oracle(point, box, panel, lomr=None, loma=None):   # written from the rule text in CLAUDE.md, not from the JS
    if point is None or box is None or "error" in point or "error" in box:
        return ["FEMA's map service did not answer. Check this spot on FEMA's map."]
    here = [f.get("attributes") or {} for f in point.get("features") or []]
    raw = next((str(a.get("FLD_ZONE") or "").strip() for a in here if str(a.get("FLD_ZONE") or "").strip() and not name(a)), "")
    here = [a for a in here if name(a)]
    if not here and raw: return [f"FEMA's map labels this spot “{raw}” instead of a flood zone. That label says nothing about whether your property can flood. Check this spot on FEMA's map."]
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
    # owner 11-08: elevation / depth as FEMA returns them, in feet only, only when the pin sits in one zone
    h = here[0]; feet = str(h.get("LEN_UNIT") or "").strip().lower() == "feet"
    if len(near) == 1 and feet and _num(h.get("STATIC_BFE"), -9000, 30000):
        dat = str(h.get("V_DATUM") or "").strip()
        out.append(f"FEMA's map lists a base flood elevation of {_js(h['STATIC_BFE'])} feet" + (f" ({dat})" if re.fullmatch(r"[A-Za-z0-9 ]{2,20}", dat) else "") + " for this zone at this pin.")
    if len(near) == 1 and feet and _num(h.get("DEPTH"), 0, 100):
        out.append(f"FEMA's map lists a flood depth of {_js(h['DEPTH'])} feet for this zone at this pin.")
    def date(e):
        if isinstance(e, (int, float)) and not isinstance(e, bool) and abs(e) < 8.64e15:
            t = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=e); return f"{M[t.month - 1]} {t.day}, {t.year}"
        return None
    p = (panel or {}).get("features") if panel and "error" not in panel else None
    p = (p[0].get("attributes") or {}) if p else None
    if p and p.get("FIRM_PAN"):
        d = date(p.get("EFF_DATE"))
        out.append(f"FEMA map panel {str(p['FIRM_PAN']).strip()}" + (f", in effect since {d}" if d else "") + ".")
    # map changes near the pin: a failed lookup says nothing; letters are counted, never named
    if isinstance(lomr, dict) and "error" not in lomr and isinstance(lomr.get("features"), list):
        ds = [((f.get("attributes") or {}) if isinstance(f, dict) else {}).get("EFF_DATE") for f in lomr["features"]]
        ds = sorted((e for e in ds if isinstance(e, (int, float)) and not isinstance(e, bool) and e > 0 and date(e)), reverse=True)   # 0 = no date
        if ds: out.append(f"FEMA revised the map at this spot by a Letter of Map Revision in effect since {date(ds[0])}.")
    if isinstance(loma, dict) and "error" not in loma and isinstance(loma.get("features"), list):
        g = {"out": 0, "as": 0, "den": 0, "oth": 0}
        for f in loma["features"]:
            o = str(((f.get("attributes") or {}) if isinstance(f, dict) else {}).get("OUTCOME") or "").lower()
            g["den" if "denied" in o else "as" if "out as shown" in o else "out" if re.match(r"(structure|property|portion of property) removed", o) else "oth"] += 1
        n = len(loma["features"])
        if not n: out.append("FEMA's map service lists no Letters of Map Amendment within 150 meters (about 500 feet) of this pin.")
        else:
            parts = [f"{g['out']} took a building or lot out of the high-risk zone", f"{g['as']} found it already outside the zone as mapped", f"{g['den']} denied"] + ([f"{g['oth']} other"] if g["oth"] else [])
            out.append(f"FEMA's map service lists {n} Letter{'' if n == 1 else 's'} of Map Amendment for properties within 150 meters (about 500 feet) of this pin: "
                       + ", ".join(parts) + ". Each letter covers only the property it names; it does not change this spot's zone.")
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
    "open water": (F({"FLD_ZONE": "OPEN WATER", "SFHA_TF": "F"}), F({"FLD_ZONE": "OPEN WATER"}, {"FLD_ZONE": "AE"}), F()),
    "open water beside AE": (F({"FLD_ZONE": "AE", "SFHA_TF": "T"}), F({"FLD_ZONE": "OPEN WATER"}), F()),
    "area not included": (F({"FLD_ZONE": "AREA NOT INCLUDED"}), F(), F()),
    "panel no date": (F({"FLD_ZONE": "A", "SFHA_TF": "T"}), F(), F({"FIRM_PAN": "22071C0115E", "EFF_DATE": None})),
    # owner 11-08: elevation, depth and map letters near the pin
    "AE with BFE + letters": (F({"FLD_ZONE": "AE", "SFHA_TF": "T", "STATIC_BFE": 9, "V_DATUM": "NAVD88", "LEN_UNIT": "Feet"}), F({"FLD_ZONE": "AE"}),
                              F({"FIRM_PAN": "12099C0587F", "EFF_DATE": 1734652800000}), F({"EFF_DATE": 1500000000000}, {"EFF_DATE": 1600000000000}),
                              F({"OUTCOME": "Structure removed"}, {"OUTCOME": "Denied"}, {"OUTCOME": "Structure out as shown"}, {"OUTCOME": "Property removed"}, {"OUTCOME": "Something new"})),
    "BFE sentinel, no letters": (F({"FLD_ZONE": "AE", "SFHA_TF": "T", "STATIC_BFE": -9999, "LEN_UNIT": "Feet"}), F(), F(), F(), F()),
    "BFE half foot below sea level": (F({"FLD_ZONE": "AE", "SFHA_TF": "T", "STATIC_BFE": -2.5, "V_DATUM": "NAVD88", "LEN_UNIT": "Feet"}), F(), F(), None, None),
    "AO depth": (F({"FLD_ZONE": "AO", "SFHA_TF": "T", "DEPTH": 2, "LEN_UNIT": "Feet"}), F(), F(), F(), F({"OUTCOME": "Denied"})),
    "BFE in meters is not shown": (F({"FLD_ZONE": "AE", "SFHA_TF": "T", "STATIC_BFE": 3, "LEN_UNIT": "Meters"}), F(), F(), {"error": {}}, {"error": {}}),
    "BFE no unit is not shown": (F({"FLD_ZONE": "AE", "SFHA_TF": "T", "STATIC_BFE": 7}), F(), F(), F(), None),
    "BFE at a zone line is not shown": (F({"FLD_ZONE": "AE", "SFHA_TF": "T", "STATIC_BFE": 9, "LEN_UNIT": "Feet"}), F({"FLD_ZONE": "X"}), F(), F(), F()),
    "odd datum text": (F({"FLD_ZONE": "VE", "SFHA_TF": "T", "STATIC_BFE": 12, "V_DATUM": "<b>x</b>", "LEN_UNIT": "FEET"}), F(), F(), F(), F()),
}

def fuzz(r):
    pick = lambda xs: r.choice(xs)
    zone = lambda: {"FLD_ZONE": pick(["AE", "X", "VE", "A", "AO", "AH", "D", "", None, 7, "OPEN WATER", "AREA NOT INCLUDED", "A12", "ae"]),
                    "ZONE_SUBTY": pick([None, "", "FLOODWAY", "0.2 PCT ANNUAL CHANCE FLOOD HAZARD", 3]), "SFHA_TF": pick(["T", "F", "t", None, ""]),
                    "STATIC_BFE": pick([None, -9999, 9, 9.5, -2, 0, 1e9, "9", True, 29999.9]), "DEPTH": pick([None, -9999, 0, 1, 2.5, 150, "2"]),
                    "LEN_UNIT": pick(["Feet", "FEET", "Meters", "", None, 1]), "V_DATUM": pick(["NAVD88", "NGVD29", "", None, "<i>", 4])}
    resp = lambda mk: pick([None, {"error": {}}, {}, {"features": None}, F(*[mk() for _ in range(r.randint(0, 3))])])
    pan = lambda: {"FIRM_PAN": pick(["12099C0587F", None, "", 5]), "EFF_DATE": pick([1734652800000, None, "x", -1, 0, 1e300])}
    lomr = lambda: {"EFF_DATE": pick([1600000000000, None, "x", 1e300, 0])}
    loma = lambda: {"OUTCOME": pick(["Structure removed", "Denied", "Structure out as shown", "Portion of property removed", None, "", 7, "Property denied"])}
    return resp(zone), resp(zone), resp(pan), resp(lomr), resp(loma)

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
        got = pg.evaluate("cs => cs.map(c => window.__zmDescribe(c[0], c[1], c[2], c[3], c[4]).lines)", [list(c) for _, c in cases])
        for (k, c), g in zip(cases, got):
            want = oracle(*c)
            if g != want: bad.append(f"{k}: page {g} != oracle {want}")
            if any(re.search(r"NaN|undefined|null|Infinity|\[object", s) for s in g): bad.append(f"{k}: bad token in {g}")
        # 2. full click path on a real page, network answered by fixtures
        ctx = b.new_context(viewport={"width": 390, "height": 844}, geolocation={"latitude": 26.7, "longitude": -80.1}, permissions=["geolocation"])
        pt, bx, pn = CASES["zone line"]
        lr, la = CASES["AE with BFE + letters"][3:]   # 11-08: the two map-letter lookups answered by fixtures
        def route(r):
            u = r.request.url
            if "geocoding.geo.census.gov" in u:
                cb = re.search(r"callback=([\w$]+)", u)[1]
                body = cb + '({"result":{"addressMatches":[{"matchedAddress":"301 N OLIVE AVE, WEST PALM BEACH, FL, 33401","coordinates":{"x":-80.0533,"y":26.7153}}]}})'
                return r.fulfill(status=200, content_type="application/javascript", body=body)
            if "/MapServer/28/query" in u: return r.fulfill(status=200, content_type="application/json", body=json.dumps(bx if "distance=15" in u and "esriSRUnit_Meter" in u else pt))   # D5: the nearby query must be a 15 m circle
            if "/MapServer/3/query" in u: return r.fulfill(status=200, content_type="application/json", body=json.dumps(pn))
            if "/MapServer/1/query" in u: return r.fulfill(status=200, content_type="application/json", body=json.dumps(lr))
            if "/MapServer/2/query" in u: return r.fulfill(status=200, content_type="application/json", body=json.dumps(la if "distance=150" in u and "esriSRUnit_Meter" in u else F()))   # a 150 m circle
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
            for s in oracle(pt, bx, pn, lr, la) + ["FEMA's map, not an official determination."]:
                if s not in out: bad.append(f"click path: missing {s!r}")
            if "Check it on FEMA's map" not in out: bad.append("click path: no FEMA link after the answer")
            # D1 (fresh audit 11-08): FEMA answers slowly, the reader drags the pin meanwhile; the old answer must not appear
            pg.evaluate("() => { const f = window.fetch; window.fetch = (...a) => new Promise(r => setTimeout(() => r(f(...a)), 2000)); }")
            def drag(dx):
                mk = pg.locator("#zm .leaflet-marker-icon").bounding_box()
                if not mk: return False
                pg.mouse.move(mk["x"] + mk["width"] / 2, mk["y"] + mk["height"] - 4); pg.mouse.down()
                pg.mouse.move(mk["x"] + dx, mk["y"] + 40, steps=8); pg.mouse.up(); return True
            if not drag(60): bad.append("D1 test: no pin to drag")
            elif pg.locator("#zm .zm-ok").count() != 1: bad.append("D1 test: drag did not ask to confirm")
            else:
                pg.click("#zm .zm-ok")   # FEMA now answering (2 s), and the reader moves the pin again
                drag(-60)
                pg.wait_for_timeout(2800)
                late = pg.inner_text("#zm .zm-out")
                if "FEMA's map shows" in late or "zone line" in late: bad.append("D1: an answer for the old pin appeared after the pin moved")
                if pg.locator("#zm .zm-ok").count() != 1: bad.append("D1: after the drag the reader is not asked to confirm the new pin")
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
