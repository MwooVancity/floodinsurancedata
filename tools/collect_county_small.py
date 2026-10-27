"""The per-county pieces the raw pull does not carry, for EVERY county (one network job):
  data/states/<slug>/county_detail.json  {geoid: {nri: {coastal, inland}, penetration: {overall_pct, sfha_pct, contracts, sfha_contracts, asof}}}
  data/us/storm_events.json              {geoid: {events, damage}}  NOAA NCEI Storm Events, flood types, 1996-2025
NRI field names are the ones collect.py used for the first 32 counties. Usage: python -I tools/collect_county_small.py"""
import csv, gzip, io, json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES, slug, FIPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NRI = "https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query"
NOAA = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
FLOOD = {"Flood", "Flash Flood", "Coastal Flood"}

def fetch(url, tries=6, timeout=180):
    last = None
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "floodinsurancedata"}), timeout=timeout).read()
        except Exception as e:
            last = e; time.sleep(4 * (i + 1))
    raise RuntimeError(repr(last)[:100])

def fema(ds, filt, select):
    rows, skip = [], 0
    while True:
        r = json.loads(fetch(f"https://www.fema.gov/api/open/v1/{ds}?" + urllib.parse.urlencode(
            {"$filter": filt, "$select": select, "$top": 1000, "$skip": skip, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote)))
        rows += r[ds]
        if not r[ds] or len(rows) >= r["metadata"]["count"]: break
        skip += 1000
    if len(rows) != r["metadata"]["count"]: raise RuntimeError(f"{ds}: {len(rows)}/{r['metadata']['count']}")
    return rows

def nri_block(a, p):
    return {"risk_rating": a.get(p + "_RISKR"), "risk_score": a.get(p + "_RISKS"), "eal_rating": a.get(p + "_EALR"),
            "eal_national_pctl": a.get(p + "_ALR_NPCTL"), "eal_total_usd": a.get(p + "_EALT")}

def state_detail(st):
    out = {}
    fields = "STCOFIPS,COUNTY," + ",".join(f"{p}_{k}" for p in ("CFLD", "IFLD") for k in ("RISKR", "RISKS", "EALR", "ALR_NPCTL", "EALT"))
    nri = json.loads(fetch(NRI + "?" + urllib.parse.urlencode({"where": f"STATEABBRV='{st}'", "outFields": fields, "f": "json",
                                                              "returnGeometry": "false", "resultRecordCount": 2000})))
    for f in nri.get("features", []):
        a = f["attributes"]
        out.setdefault(a["STCOFIPS"], {})["nri"] = {"county": a["COUNTY"], "state": st, "coastal": nri_block(a, "CFLD"), "inland": nri_block(a, "IFLD")}
    for r in fema("NfipResidentialPenetrationRates", f"state eq '{NAMES[st]}'",
                  "fipsCode,resContractsInForce,resContractsInForceSfha,totalResStructures,totalResStructuresSfha,asOfDate"):
        c, cs, s, ss = (int(r.get(k) or 0) for k in ("resContractsInForce", "resContractsInForceSfha", "totalResStructures", "totalResStructuresSfha"))
        out.setdefault(r["fipsCode"], {})["penetration"] = {
            "overall_pct": round(100 * c / s, 1) if s else None, "sfha_pct": round(100 * cs / ss, 1) if ss else None,
            "contracts": c, "sfha_contracts": cs, "asof": (r.get("asOfDate") or "")[:10] or None,
            "source": "OpenFEMA NfipResidentialPenetrationRates v1"}
    json.dump(out, open(os.path.join(ROOT, "data", "states", slug(st), "county_detail.json"), "w"))
    print(f"{st}: NRI {sum(1 for v in out.values() if 'nri' in v)} counties, penetration {sum(1 for v in out.values() if 'penetration' in v)}", flush=True)

def dmg(s):   # "10.00K" / "1.5M" / "" -> dollars
    m = re.match(r"([\d.]+)\s*([KMBkmb]?)", (s or "").strip())
    return float(m.group(1)) * {"K": 1e3, "M": 1e6, "B": 1e9, "": 1}[m.group(2).upper()] if m else 0.0

def storm_events():
    listing = fetch(NOAA).decode("latin-1"); files = {}
    for mm in re.finditer(r"(StormEvents_details-ftp_v1\.0_d(\d{4})_c\d+\.csv\.gz)", listing):
        if 1996 <= int(mm.group(2)) <= 2025: files[int(mm.group(2))] = mm.group(1)   # newest c-date wins
    acc = {}
    for y in range(1996, 2026):
        if y not in files: raise RuntimeError(f"NOAA {y}: no file")   # a missing year would undercount every county
        for row in csv.DictReader(io.StringIO(gzip.decompress(fetch(NOAA + files[y], timeout=300)).decode("latin-1"))):
            if row.get("CZ_TYPE") != "C" or row.get("EVENT_TYPE") not in FLOOD: continue
            try: g = f"{int(row['STATE_FIPS']):02d}{int(row['CZ_FIPS']):03d}"
            except (ValueError, KeyError): continue
            a = acc.setdefault(g, {"events": 0, "damage": 0.0}); a["events"] += 1; a["damage"] += dmg(row.get("DAMAGE_PROPERTY"))
        print(f"NOAA {y}: {len(acc)} counties so far", flush=True)
    json.dump({"period": "1996-2025", "retrieved": time.strftime("%Y-%m-%d"), "source": "NOAA NCEI Storm Events Database",
               "by_county": {g: {"events": v["events"], "damage": round(v["damage"])} for g, v in acc.items()}},
              open(os.path.join(ROOT, "data", "us", "storm_events.json"), "w"))

if __name__ == "__main__":
    for st in sorted(NAMES):
        try: state_detail(st)
        except Exception as e: print(st, "FAILED", repr(e)[:120], flush=True)
    storm_events()
    print("done")
