"""ZIP -> the town a reader knows it by: U.S. Census 2020 ZCTA-to-place relationship file (public, no key).
Each ZIP gets the Census place (city, town, CDP) covering the most of its land; ZIPs with no place get none.
Writes data/us/zip_places.json {"33480": "Palm Beach", ...}.  Usage: python -I tools/fetch_zip_places.py"""
import csv, json, os, re, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_place20_natl.txt"
raw = os.path.join(ROOT, ".cache", "census", "zcta_place.txt")
if not os.path.exists(raw):
    os.makedirs(os.path.dirname(raw), exist_ok=True); urllib.request.urlretrieve(URL, raw)
best = {}
for r in csv.DictReader(open(raw, encoding="utf-8-sig"), delimiter="|"):
    z, name, part = r["GEOID_ZCTA5_20"], r["NAMELSAD_PLACE_20"], int(r["AREALAND_PART"] or 0)
    if not z or not name: continue
    # 2026-10-28 backlog: a place must cover at least a quarter of the ZIP's land, or the ZIP gets no name. 77386 is
    # mostly unincorporated: Houston's 6% sliver made it "Houston" (USPS: Spring); Little River covers 32% of 29566.
    if 4 * part < int(r["AREALAND_ZCTA5_20"] or 0): continue
    if part > best.get(z, ("", -1))[1]: best[z] = (name, part)
# "Boca Raton city" -> "Boca Raton"; "Jupiter Farms CDP" -> "Jupiter Farms"
strip = r"\s+(city|town|village|borough|CDP|municipality|city and borough|urban county|consolidated government.*|metro government.*|unified government.*|\(balance\))$"
out = {z: re.sub(strip, "", n, flags=re.I) for z, (n, _) in best.items()}
json.dump(out, open(os.path.join(ROOT, "data", "us", "zip_places.json"), "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
print(f"zip_places: {len(out)} ZIPs; sample", {z: out[z] for z in ("33480", "33484", "33470", "70112") if z in out})
