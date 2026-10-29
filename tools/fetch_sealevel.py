"""NOAA sea-level trends (Tides & Currents sealvltrends, NOAA's own published trend per tide station) -> data/us/sealevel.json
{county geoid: [{station, name, trend (inches/decade), error, start, end}]}. Each station's county comes from the Census
geocoder (its point). PLAN 3e: only NOAA's published trend and period are used, never our own fit.
Usage: python -I tools/fetch_sealevel.py"""
import json, os, time, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOAA = "https://api.tidesandcurrents.noaa.gov/dpapi/prod/webapi/product/sealvltrends.json"
GEO = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
def get(url):
    for t in range(5):
        try: return json.load(urllib.request.urlopen(url, timeout=60))
        except Exception: time.sleep(5 * (t + 1))
    raise SystemExit(f"no answer: {url[:80]}")
out, skipped = {}, []
for s in get(NOAA)["SeaLvlTrends"]:
    if s.get("affil") != "US" or s.get("trendUnits") != "inches/decade" or s.get("trend") is None: skipped.append(s.get("stationId")); continue
    q = urllib.parse.urlencode({"x": s["longitude"], "y": s["latitude"], "benchmark": "Public_AR_Current", "vintage": "Current_Current",
                                "layers": "Counties", "format": "json"})
    c = (get(f"{GEO}?{q}").get("result", {}).get("geographies", {}).get("Counties") or [])
    if not c: skipped.append(s["stationId"]); continue   # a station offshore of every county polygon
    out.setdefault(c[0]["GEOID"], []).append({"station": s["stationId"], "name": s["stationName"], "trend": s["trend"],
                                             "error": s["trendError"], "start": s["startDate"], "end": s["endDate"]})
json.dump(out, open(os.path.join(ROOT, "data", "us", "sealevel.json"), "w", encoding="utf-8"), indent=0)
print(f"{sum(len(v) for v in out.values())} stations in {len(out)} counties; skipped {len(skipped)}: {skipped[:10]}")
