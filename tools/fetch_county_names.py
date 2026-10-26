"""County names by 5-digit FIPS from the Census API (key from .env), for any county code FEMA's NRI does not name
(Connecticut's 8 old counties, which NFIP records still carry, sit beside its 9 new planning regions).
Writes data/us/county_names.json. Usage: python -I tools/fetch_county_names.py"""
import json, os, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def census_key():   # same reader as collect_small.py (importing that module runs its collection)
    for l in open(os.path.join(ROOT, ".env")):
        if l.startswith("CENSUS_KEY="): return l.split("=", 1)[1].strip()
names = {}
for url in ("https://api.census.gov/data/2020/dec/pl?get=NAME&for=county:*",       # pre-2022 counties (old CT)
            "https://api.census.gov/data/2023/acs/acs5?get=NAME&for=county:*"):    # current (CT planning regions)
    rows = json.load(urllib.request.urlopen(urllib.request.Request(url + "&key=" + census_key(), headers={"User-Agent": "floodinsurancedata"}), timeout=120))
    for name, st, co in rows[1:]:
        names[st + co] = name.split(",")[0]          # "Fairfield County, Connecticut" -> "Fairfield County"
json.dump(dict(sorted(names.items())), open(os.path.join(ROOT, "data", "us", "county_names.json"), "w"), indent=0)
print(len(names), "county names;", {k: names[k] for k in ("09001", "09110", "50023") if k in names})
