"""Physical flood history per county from NOAA NCEI Storm Events (keyless bulk CSV). ONE pass: download each
year's national gzip once (1996-2025, the complete era), stream-filter rows for our counties + flood event
types, accumulate {events, property damage $}. Merges into data.json as 'storm_events'. Answers "has it
actually flooded here, and how badly" — the physical-flood axis, distinct from insured NFIP claims.
Usage: python -I tools/collect_stormevents.py"""
import csv, gzip, io, json, os, re, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DIR = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
YEARS = range(1996, 2026)                       # 1996+ = the complete, consistently-coded era
FLOOD = {"Flood", "Flash Flood", "Coastal Flood"}
counties = json.load(open(os.path.join(HERE, "counties.json")))
WANT = {c["geoid"]: c["slug"] for c in counties}   # 5-digit FIPS -> slug
acc = {c["slug"]: {"events": 0, "damage": 0.0} for c in counties}

def fetch(u, tries=4, timeout=120):
    last = None
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ff"}), timeout=timeout).read()
        except Exception as e:
            last = e; time.sleep(4 * (i + 1))
    raise RuntimeError(repr(last)[:90])

def dmg(s):                                      # "10.00K" / "1.5M" / "" -> dollars
    s = (s or "").strip()
    if not s or s in ("0", "0.00"): return 0.0
    m = re.match(r"([\d.]+)\s*([KMBkmb]?)", s)
    if not m: return 0.0
    v = float(m.group(1)); return v * {"K": 1e3, "M": 1e6, "B": 1e9, "": 1}[m.group(2).upper()]

listing = fetch(DIR).decode("latin-1")
byyear = {}
for m in re.finditer(r"(StormEvents_details-ftp_v1\.0_d(\d{4})_c\d+\.csv\.gz)", listing):
    y = int(m.group(2))
    if y in YEARS: byyear[y] = m.group(1)        # dir is sorted; last (newest c-date) wins

for y in YEARS:
    fn = byyear.get(y)
    if not fn: print(f"  {y}: no file"); continue
    try:
        raw = fetch(DIR + fn)
        text = gzip.decompress(raw).decode("latin-1")
    except Exception as e:
        print(f"  {y}: FAIL {repr(e)[:60]}"); continue
    rd = csv.DictReader(io.StringIO(text))
    hit = 0
    for row in rd:
        if row.get("CZ_TYPE") != "C" or row.get("EVENT_TYPE") not in FLOOD:
            continue
        try:
            geoid = f"{int(row['STATE_FIPS']):02d}{int(row['CZ_FIPS']):03d}"
        except (ValueError, KeyError):
            continue
        slug = WANT.get(geoid)
        if not slug: continue
        acc[slug]["events"] += 1
        acc[slug]["damage"] += dmg(row.get("DAMAGE_PROPERTY"))
        hit += 1
    print(f"  {y}: {hit} county-flood rows")

for c in counties:
    a = acc[c["slug"]]
    rec = {"events": a["events"], "damage": round(a["damage"]), "period": "1996-2025",
           "retrieved": "2026-10-25", "source": "NOAA NCEI Storm Events Database"}
    dp = os.path.join(DATA, c["slug"], "data.json")
    try: dd = json.load(open(dp))
    except Exception: dd = {}
    dd["storm_events"] = rec; json.dump(dd, open(dp, "w"))
print("done:", {s: v["events"] for s, v in list(acc.items())[:6]})
