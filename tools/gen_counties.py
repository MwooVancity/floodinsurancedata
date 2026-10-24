"""Generate tools/counties.json from a curated (state, county-name) target list, resolving each to its
AUTHORITATIVE 5-digit FIPS via the FEMA NRI county endpoint (never hand-typed). Keeps any existing rows
(Lee, Kanawha). Prints every resolution so it can be sanity-checked before a build. official=0 (the page
shows 'reconciliation pending'; fill later from the FEMA PIF workbook). Usage: python -I tools/gen_counties.py"""
import json, os, re, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "counties.json")
NRI = ("https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/"
       "National_Risk_Index_Counties/FeatureServer/0/query")

ST = {"FL": ("12", "Florida"), "TX": ("48", "Texas"), "LA": ("22", "Louisiana"), "SC": ("45", "South Carolina"),
      "NC": ("37", "North Carolina"), "NJ": ("34", "New Jersey"), "NY": ("36", "New York"),
      "GA": ("13", "Georgia"), "AL": ("01", "Alabama"), "MS": ("28", "Mississippi"), "CA": ("06", "California"),
      "MO": ("29", "Missouri"), "WV": ("54", "West Virginia")}

# diverse, high-NFIP / high-flood set: coastal metros, barrier islands, LA parishes, plus inland variance.
TARGETS = [
    ("FL", "Miami-Dade"), ("FL", "Broward"), ("FL", "Pinellas"), ("FL", "Collier"), ("FL", "Monroe"),
    ("FL", "Duval"), ("FL", "Brevard"), ("FL", "Sarasota"),
    ("TX", "Harris"), ("TX", "Galveston"), ("TX", "Jefferson"), ("TX", "Nueces"),
    ("LA", "Orleans"), ("LA", "Jefferson"), ("LA", "St. Tammany"), ("LA", "Terrebonne"),
    ("SC", "Charleston"), ("SC", "Horry"), ("NC", "New Hanover"), ("NC", "Dare"),
    ("NJ", "Ocean"), ("NJ", "Monmouth"), ("NJ", "Atlantic"), ("NY", "Nassau"), ("NY", "Suffolk"),
    ("GA", "Chatham"), ("AL", "Baldwin"), ("MS", "Harrison"), ("CA", "Orange"), ("MO", "St. Louis"),
]

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ff"}), timeout=90) as r:
        return json.load(r)

def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("saint", "st"))

def state_counties(fips):
    r = get(NRI + "?" + urllib.parse.urlencode(
        {"where": f"STATEFIPS='{fips}'", "outFields": "STCOFIPS,COUNTY,COUNTYTYPE", "f": "json",
         "returnGeometry": "false", "resultRecordCount": 400}))
    return [f["attributes"] for f in r.get("features", [])]

def kebab(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

cache, rows, seen = {}, [], set()
# keep existing rows (Lee, Kanawha) first
try:
    for r in json.load(open(OUT)):
        rows.append(r); seen.add(r["geoid"])
except Exception:
    pass

for abbr, name in TARGETS:
    fips, state_name = ST[abbr]
    if abbr not in cache: cache[abbr] = state_counties(fips)
    match = next((a for a in cache[abbr] if norm(a.get("COUNTY")) == norm(name)), None)
    if not match:
        print(f"  NO MATCH {name}, {abbr} — skipped"); continue
    geoid = match["STCOFIPS"]; cty = match["COUNTY"]
    if geoid in seen:
        print(f"  dup {cty} {geoid} — skipped"); continue
    suffix = "Parish" if abbr == "LA" else "County"
    short = f"{cty} {suffix}"
    rows.append({"slug": f"{kebab(cty)}-{suffix.lower()}-{abbr.lower()}", "state": abbr, "geoid": geoid,
                 "county": cty.upper(), "countytitle": cty, "label": f"{cty} {suffix}, {state_name}",
                 "short": short, "official": 0})
    seen.add(geoid)
    print(f"  {short}, {abbr}  ->  {geoid}")

json.dump(rows, open(OUT, "w"), indent=1)
print(f"\nwrote {len(rows)} counties to {OUT}")
