"""County flood-map status from FEMA's own map service (NFHL MapServer), for each live county page. Runs only in the US
cloud (FEMA's map servers refuse non-US connections; verified 11-06). Map debate 11-06: map age, map revisions,
individual exemptions are the facts no competitor prints beside the map.
Per county (geoid):
  panels  FIRM Panels (layer 3) of the countywide FEMA map DFIRM_ID=<geoid>C: count, oldest and newest EFF_DATE
          (none = no countywide digital map; the page then prints nothing)
  lomr    LOMRs (layer 1) on that map: total, and how many took effect in the last 5 whole years
  loma    LOMAs (layer 34) for the county's NFIP communities (CIDs from OpenFEMA NfipCommunityStatusBook, county field):
          counts by OUTCOME and DETERMINATIONTYPE exactly as FEMA codes them; wording waits for FEMA's code meanings
Writes data/us/map_status.json. A county whose query fails is left out (never a zero), and the job fails when more
than 5% fail, so a FEMA outage never ships empty facts.
Usage: python -I tools/pull_mapstatus.py [geoid ...]"""
import datetime, json, os, sys, time, urllib.parse, urllib.request
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer"
CSB = "https://www.fema.gov/api/open/v1/NfipCommunityStatusBook"
TODAY = datetime.date.today()
SINCE = datetime.date(TODAY.year - 5, 1, 1)

def get(url, params, tries=4):
    u = url + "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "floodinsurancedata-mapstatus/1"}), timeout=60))
            if "error" in d: raise RuntimeError(str(d["error"])[:200])
            return d
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(10 * (i + 1))

def stats(layer, where, stats_, group=None):
    p = {"where": where, "outStatistics": json.dumps(stats_), "f": "json"}
    if group: p["groupByFieldsForStatistics"] = group
    return [f["attributes"] for f in get(f"{B}/{layer}/query", p).get("features", [])]

def day(ms): return str(datetime.date(1970, 1, 1) + datetime.timedelta(milliseconds=ms)) if ms is not None else None

def cids_by_county(states):
    out = defaultdict(list)
    for st in sorted(states):
        skip = 0
        while True:
            d = get(CSB, {"$filter": f"state eq '{st}'", "$select": "communityIdNumber,county,participatingInNFIP", "$top": 1000, "$skip": skip})
            rows = d["NfipCommunityStatusBook"]
            for r in rows:
                if r.get("communityIdNumber") and r.get("county"): out[(st, r["county"].strip().upper())].append(r["communityIdNumber"])
            if len(rows) < 1000: break
            skip += 1000
    return out

def county(c, cids):
    g = c["geoid"]; dfirm = g + "C"
    cnt = lambda f, n: {"statisticType": "count", "onStatisticField": f, "outStatisticFieldName": n}
    pan = stats(3, f"DFIRM_ID='{dfirm}'", [cnt("OBJECTID", "n"),
          {"statisticType": "min", "onStatisticField": "EFF_DATE", "outStatisticFieldName": "oldest"},
          {"statisticType": "max", "onStatisticField": "EFF_DATE", "outStatisticFieldName": "newest"}])[0]
    o = {"dfirm": dfirm, "panels": pan["n"] or 0, "oldest": day(pan["oldest"]), "newest": day(pan["newest"])}
    for k in ("oldest", "newest"):   # FEMA placeholder dates (9999-09-09, 1899) are not dates: stored as None (hater r133)
        if o[k] and not ("1968-01-01" <= o[k] <= datetime.date.today().isoformat()): o[k] = None
    if o["panels"]:
        o["lomr"] = stats(1, f"DFIRM_ID='{dfirm}'", [cnt("OBJECTID", "n")])[0]["n"] or 0
        o["lomr_recent"] = stats(1, f"DFIRM_ID='{dfirm}' AND EFF_DATE >= DATE '{SINCE}'", [cnt("OBJECTID", "n")])[0]["n"] or 0
        o["lomr_since"] = str(SINCE)
    if cids:
        rows = stats(34, "CID IN (" + ",".join(f"'{x}'" for x in sorted(set(cids))) + ")", [cnt("OBJECTID", "n")], "OUTCOME,DETERMINATIONTYPE")
        o["loma"] = {f'{r.get("OUTCOME")}|{r.get("DETERMINATIONTYPE")}': r["n"] for r in rows}
        o["cids"] = sorted(set(cids))
    return o

def panels_rows(rows):   # grouped FIRM Panels stats -> {county geoid: panels, oldest, newest}; countywide maps only (<geoid>C)
    out = {}
    for r in rows:
        d = str(r.get("DFIRM_ID") or "")
        if len(d) != 6 or not d[:5].isdigit() or d[5] != "C": continue   # community-based maps are not a county's map
        o = {"panels": r.get("n") or 0, "oldest": day(r.get("oldest")), "newest": day(r.get("newest"))}
        for k in ("oldest", "newest"):   # same placeholder-date rule as county()
            if o[k] and not ("1968-01-01" <= o[k] <= str(TODAY)): o[k] = None
        out[d[:5]] = o
    return out

def panels_all(state_fips):   # Flood Map Age paper (11-13): every U.S. county, one grouped query per state, not ~3,000 county queries
    st = [{"statisticType": "count", "onStatisticField": "OBJECTID", "outStatisticFieldName": "n"},
          {"statisticType": "min", "onStatisticField": "EFF_DATE", "outStatisticFieldName": "oldest"},
          {"statisticType": "max", "onStatisticField": "EFF_DATE", "outStatisticFieldName": "newest"}]
    out, bad = {}, []
    for sf in sorted(state_fips):
        try:
            d = get(f"{B}/3/query", {"where": f"DFIRM_ID LIKE '{sf}___C'", "outStatistics": json.dumps(st), "groupByFieldsForStatistics": "DFIRM_ID", "f": "json"})
            if d.get("exceededTransferLimit"): raise RuntimeError("group limit hit")   # a cut-off list would drop counties silently
            out.update(panels_rows([f_["attributes"] for f_ in d.get("features", [])]))
        except Exception as e: bad.append(sf); print("FAILED state", sf, repr(e)[:150], flush=True)
    if bad: sys.exit(f"STOP: panel dates failed for states {bad}; map_panels.json left as it was")   # never a partial national file
    out["_retrieved"] = str(TODAY)
    json.dump(out, open(os.path.join(ROOT, "data", "us", "map_panels.json"), "w"), indent=0, sort_keys=True)
    print(f"map panels: {len(out) - 1} counties with a countywide digital map, {len(state_fips)} states")

def main(only):
    cs = json.load(open(os.path.join(ROOT, "tools", "counties.json"), encoding="utf-8"))
    if only: cs = [c for c in cs if c["geoid"] in only]
    cid = cids_by_county({c["state"] for c in cs})
    out, bad = {}, []
    for c in cs:
        key = (c["state"], c["short"].strip().upper())
        try: out[c["geoid"]] = county(c, cid.get(key, []))
        except Exception as e: bad.append(c["geoid"]); print("FAILED", c["slug"], repr(e)[:150], flush=True)
    print(f"map status: {len(out)} counties, {len(bad)} failed; sample {json.dumps(next(iter(out.values()), {}))[:400]}")
    if len(bad) > 0.05 * len(cs): sys.exit(f"STOP: {len(bad)} of {len(cs)} counties failed; FEMA's map service is not answering")
    p = os.path.join(ROOT, "data", "us", "map_status.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    if not only: old = {}
    old.update(out); old["_retrieved"] = str(TODAY)
    json.dump(old, open(p, "w"), indent=0, sort_keys=True)

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        r = panels_rows([{"DFIRM_ID": "12071C", "n": 5, "oldest": 0, "newest": 1700000000000}, {"DFIRM_ID": "125128", "n": 3},
                         {"DFIRM_ID": "48201C", "n": 2, "oldest": -2208988800000, "newest": None}])
        assert set(r) == {"12071", "48201"}, r   # community map 125128 is not a county row
        assert r["12071"] == {"panels": 5, "oldest": "1970-01-01", "newest": "2023-11-14"}, r
        assert r["48201"]["oldest"] is None and r["48201"]["newest"] is None, r   # 1800s placeholder dropped, missing date stays None
        print("pull_mapstatus --test ok")
    elif sys.argv[1:] == ["--panels"]:
        panels_all({f[:2] for f in os.listdir(os.path.join(ROOT, "data", "all-counties")) if f[:5].isdigit()})
    else: main(set(sys.argv[1:]))
