"""NOAA sea-level trends (Tides & Currents sealvltrends, NOAA's own published trend per tide station) -> data/us/sealevel.json
{county geoid: [{station, name, trend (inches/decade), error, start, end}]}. Each station's county comes from the Census
geocoder (its point). PLAN 3e: only NOAA's published trend and period are used, never our own fit.
Usage: python -I tools/fetch_sealevel.py"""
import json, os, time, urllib.parse, urllib.request
def _dump(obj, path, **kw):   # 11-09: a killed step must never leave half a file to commit; write aside, then swap in one step
    with open(path + ".tmp", "w", encoding="utf-8") as fh: json.dump(obj, fh, **kw)
    os.replace(path + ".tmp", path)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOAA = "https://api.tidesandcurrents.noaa.gov/dpapi/prod/webapi/product/sealvltrends.json"
GEO = os.environ.get("FF_GEO", "https://geocoding.geo.census.gov/geocoder/geographies/coordinates")
OUT = os.path.join(ROOT, "data", "us", "sealevel.json")
# A tide station does not change county: reuse the last file's answer, so the geocoder is asked only about a new station.
# 2026-10-30: one geocoder timeout on the 139th call stopped the whole 2.5-hour refresh.
known = {r["station"]: g for g, v in (json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}).items() for r in v}
def get(url):
    for t in range(5):
        try: return json.load(urllib.request.urlopen(url, timeout=60))
        except Exception: time.sleep(5 * (t + 1))
    raise SystemExit(f"no answer: {url[:80]}")
out, skipped = {}, []
for s in get(NOAA)["SeaLvlTrends"]:
    if s.get("affil") != "US" or s.get("trendUnits") != "inches/decade" or s.get("trend") is None: skipped.append(s.get("stationId")); continue
    geoid = known.get(s["stationId"])
    if not geoid:
        q = urllib.parse.urlencode({"x": s["longitude"], "y": s["latitude"], "benchmark": "Public_AR_Current", "vintage": "Current_Current",
                                    "layers": "Counties", "format": "json"})
        try: c = (get(f"{GEO}?{q}").get("result", {}).get("geographies", {}).get("Counties") or [])
        except SystemExit as e: print(f"::warning::{s['stationId']} left out this month: {e}"); skipped.append(s["stationId"]); continue   # a gap, not a guess
        if not c: skipped.append(s["stationId"]); continue   # a station offshore of every county polygon
        geoid = c[0]["GEOID"]
    out.setdefault(geoid, []).append({"station": s["stationId"], "name": s["stationName"], "trend": s["trend"],
                                      "error": s["trendError"], "start": s["startDate"], "end": s["endDate"]})
n = sum(len(v) for v in out.values())
# a short answer never replaces good data (2026-10-30: NOAA returned 1 station and the file was emptied in a test)
if n < 0.9 * len(known): raise SystemExit(f"only {n} stations against {len(known)} last time: file kept")
_dump(out, OUT, indent=0)
print(f"{sum(len(v) for v in out.values())} stations in {len(out)} counties; skipped {len(skipped)}: {skipped[:10]}")
