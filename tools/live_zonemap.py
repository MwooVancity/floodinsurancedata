"""Batch E gate (PLAN): the LIVE address tool against REAL FEMA and Census, from a US machine (FEMA refuses others).
For each address: Python asks the Census geocoder and FEMA's NFHL directly (same point, same 15 m box), the oracle from
test_zonemap.py turns FEMA's answer into the sentences the page must print, and the live page, driven like a reader
(open, type, find, confirm pin), must print every one of them plus the label and the FEMA link.
Usage (US runner): python -I tools/live_zonemap.py [--browser chromium|webkit]"""
import json, math, os, sys, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_zonemap import oracle   # Python mirror of describe(), written from the CLAUDE.md rule
from playwright.sync_api import sync_playwright
BROWSER = sys.argv[sys.argv.index("--browser") + 1] if "--browser" in sys.argv else "chromium"
PAGE = "https://floodinsurancedata.com/flood-zone-map/"
NFHL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer"
ADDRS = ["301 N Olive Ave, West Palm Beach, FL", "1700 Convention Center Dr, Miami Beach, FL",
         "1001 Preston St, Houston, TX", "1300 Perdido St, New Orleans, LA", "100 Ocean Blvd, Long Beach, NY"]

def get(url, p):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(p), headers={"User-Agent": "Mozilla/5.0"})
    try: return json.load(urllib.request.urlopen(req, timeout=20))
    except Exception: return None

def fema(addr):
    g = get("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress", {"address": addr, "benchmark": "Public_AR_Current", "format": "json"})
    mt = (g or {}).get("result", {}).get("addressMatches") or []
    if not mt: return None
    lon, lat = mt[0]["coordinates"]["x"], mt[0]["coordinates"]["y"]
    base = {"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326, "returnGeometry": "false", "f": "json"}
    pt = get(NFHL + "/28/query", dict(base, outFields="FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE,V_DATUM,DEPTH,LEN_UNIT"))
    bx = get(NFHL + "/28/query", dict(base, distance=15, units="esriSRUnit_Meter", outFields="FLD_ZONE,ZONE_SUBTY"))   # D5: true 15 m circle
    pn = get(NFHL + "/3/query", dict(base, outFields="FIRM_PAN,EFF_DATE"))
    lr = get(NFHL + "/1/query", dict(base, outFields="EFF_DATE"))   # owner 11-08: map letters near the pin, as the page asks
    la = get(NFHL + "/34/query", dict(base, distance=150, units="esriSRUnit_Meter", outFields="OUTCOME"))
    return mt[0]["matchedAddress"], pt, bx, pn, lr, la

bad, zones = [], []
with sync_playwright() as p:
    b = getattr(p, BROWSER).launch()
    for a in ADDRS:
        r = fema(a)
        if not r: bad.append(f"{a}: Census did not match (test address needs fixing)"); continue
        matched, pt, bx, pn, lr, la = r
        want = oracle(pt, bx, pn, lr, la); zones.append((a, (pt or {}).get("features", [{}])[0].get("attributes", {}).get("FLD_ZONE") if (pt or {}).get("features") else None))
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page(); pg.goto(PAGE)
        pg.click("#zm .zm-open"); pg.fill("#zm .zm-addr", a)
        pg.wait_for_function("window.__zmStart !== undefined", timeout=20000)
        pg.click("#zm .zm-go"); pg.wait_for_selector("#zm .zm-ok", timeout=20000)
        if matched not in pg.inner_text("#zm .zm-out"): bad.append(f"{a}: page did not show Census's match {matched!r}")
        pg.click("#zm .zm-ok")
        pg.wait_for_function("!document.querySelector('#zm .zm-out').innerText.includes('Asking FEMA')", timeout=20000)
        out = pg.inner_text("#zm .zm-out")
        for s in want + ["FEMA's map, not an official determination.", "Check it on FEMA's map"]:
            if s not in out: bad.append(f"{a}: missing {s!r}; page said {out[:300]!r}")
        pg.context.close()
    b.close()
for a, z in zones: print(f"  {a}: FEMA zone {z}")
# fresh audit 11-08 D4: page == oracle also holds when FEMA is down (both say "did not answer"), so that alone proves nothing.
# The tool is only working when FEMA named a zone for at least 4 of the 5 real addresses.
named = sum(1 for _, z in zones if z)
if named < 4: bad.append(f"only {named} of {len(ADDRS)} real addresses got a zone from FEMA: FEMA down, blocked or changed")
for x in bad: print("  -", x)
print(f"LIVE ZONEMAP {'FAIL' if bad else 'PASS'} ({BROWSER}): {len(zones)} real addresses, page == FEMA via oracle")
sys.exit(1 if bad else 0)
