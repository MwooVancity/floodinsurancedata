"""Each community's current FEMA flood-map date (OpenFEMA NfipCommunityStatusBook currentlyEffectiveMapDate), merged
into the crs list of every built state and county data.json (PLAN 3e). Small: one call per state, a few thousand rows.
The monthly refresh collects it too (collect_state_small); this fills the pages now. Usage: python -I tools/fetch_map_dates.py"""
import glob, json, os, time, urllib.parse, urllib.request
def _dump(obj, path, **kw):   # 11-09: a killed step must never leave half a file to commit; write aside, then swap in one step
    with open(path + ".tmp", "w", encoding="utf-8") as fh: json.dump(obj, fh, **kw)
    os.replace(path + ".tmp", path)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.fema.gov/api/open/v1/NfipCommunityStatusBook"
def pull(st):
    rows, skip = [], 0
    while True:
        q = urllib.parse.urlencode({"$filter": f"state eq '{st}'", "$select": "communityName,county,currentlyEffectiveMapDate",
                                    "$top": 1000, "$skip": skip}, quote_via=urllib.parse.quote)
        for t in range(5):
            try: got = json.load(urllib.request.urlopen(f"{API}?{q}", timeout=60))["NfipCommunityStatusBook"]; break
            except Exception: time.sleep(5 * (t + 1))
        else: raise SystemExit(f"FEMA did not answer for {st}")
        rows += got; skip += 1000
        if len(got) < 1000: return rows
files = glob.glob(os.path.join(ROOT, "data", "states", "*", "data.json")) + glob.glob(os.path.join(ROOT, "data", "c", "*", "data.json"))
by_state, n_set, n_files = {}, 0, 0
for f in files:
    d = json.load(open(f, encoding="utf-8"))
    st = (d.get("state") or (json.load(open(os.path.join(os.path.dirname(f), "agg.json"))).get("state")) or "")
    if not st or not d.get("crs"): continue
    if st not in by_state: by_state[st] = {(r["communityName"], r.get("county")): r.get("currentlyEffectiveMapDate") for r in pull(st)}
    m = by_state[st]
    for c in d["crs"]:
        k = (c.get("communityName"), c.get("county"))
        if k in m: c["currentlyEffectiveMapDate"] = m[k]; n_set += 1
    _dump(d, f); n_files += 1
print(f"map dates set on {n_set} communities in {n_files} pages ({len(by_state)} states pulled)")
