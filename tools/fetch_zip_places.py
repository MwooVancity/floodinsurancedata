"""ZIP -> the town a reader knows it by: U.S. Census 2020 ZCTA-to-place relationship file (public, no key).
Each ZIP gets the Census place (city, town, CDP) covering the most of its land; ZIPs with no place get none.
Writes data/us/zip_places.json {"33480": "Palm Beach", ...} and data/us/zip_place_counties.json {"33480": ["12099"], ...}:
the counties both that ZIP and its place lie in (Census 2020 ZCTA-county and place-county lists), so a county page never names a town across the
line (11-07). Downloads go to .cache/census and are deleted after.  Usage: python -I tools/fetch_zip_places.py"""
import csv, io, json, os, re, shutil, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_place20_natl.txt"
PBC = "https://www2.census.gov/geo/docs/reference/codes2020/national_place_by_county2020.txt"
ZC = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt"
CACHE = os.path.join(ROOT, ".cache", "census"); os.makedirs(CACHE, exist_ok=True)
def get(url, fn):
    p = os.path.join(CACHE, fn)
    if not os.path.exists(p):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    return p
best = {}
for r in csv.DictReader(open(get(URL, "zcta_place.txt"), encoding="utf-8-sig"), delimiter="|"):
    z, name, part = r["GEOID_ZCTA5_20"], r["NAMELSAD_PLACE_20"], int(r["AREALAND_PART"] or 0)
    if not z or not name: continue
    # 2026-10-28 backlog: a place must cover at least a quarter of the ZIP's land, or the ZIP gets no name. 77386 is
    # mostly unincorporated: Houston's 6% sliver made it "Houston" (USPS: Spring); Little River covers 32% of 29566.
    if 4 * part < int(r["AREALAND_ZCTA5_20"] or 0): continue
    if part > best.get(z, ("", -1, ""))[1]: best[z] = (name, part, r["GEOID_PLACE_20"])
cty = {}
for r in csv.DictReader(open(get(PBC, "place_county.txt"), encoding="utf-8-sig"), delimiter="|"):
    cty.setdefault(r["STATEFP"] + r["PLACEFP"], []).append(r["STATEFP"] + r["COUNTYFP"])
# "Boca Raton city" -> "Boca Raton"; "Jupiter Farms CDP" -> "Jupiter Farms"
strip = r"\s+(city|town|village|borough|CDP|municipality|city and borough|urban county|consolidated government.*|metro government.*|unified government.*|\(balance\))$"
out = {z: re.sub(strip, "", n.split(",")[0], flags=re.I) for z, (n, _, _) in best.items()}   # "Islamorada, Village of Islands" read as two towns in a list (11-07)
zcty = {}   # the counties the ZIP itself lies in: a stray downtown-Houston ZIP on a Montgomery policy never names Houston there
for r in csv.DictReader(open(get(ZC, "zcta_county.txt"), encoding="utf-8-sig"), delimiter="|"):
    if r["GEOID_ZCTA5_20"] and int(r["AREALAND_PART"] or 0) > 0: zcty.setdefault(r["GEOID_ZCTA5_20"], set()).add(r["GEOID_COUNTY_20"])
zc = {z: sorted(set(cty[g]) & zcty.get(z, set())) for z, (_, _, g) in best.items() if g in cty}
miss = len(out) - len(zc)
assert miss < 0.01 * len(out), f"{miss} ZIP places have no county in the Census list"   # a broken join must not empty every town line
d = os.path.join(ROOT, "data", "us")
json.dump(out, open(os.path.join(d, "zip_places.json"), "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
json.dump(zc, open(os.path.join(d, "zip_place_counties.json"), "w", encoding="utf-8"), separators=(",", ":"))
shutil.rmtree(CACHE)
print(f"zip_places: {len(out)} ZIPs, {len(zc)} with counties ({miss} without); sample", {z: (out[z], zc.get(z)) for z in ("33480", "77386", "60601", "70112") if z in out})
