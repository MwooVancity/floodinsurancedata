"""Small per-state datasets for the state pages (and per-county breakdowns kept for the county rollout).
Writes data/states/<slug>/data.json in the county-page schema, plus extras:
  crs, declarations, housing, multiloss {total, srl, by_county}, penetration {overall_pct, sfha_pct, contracts, by_county},
  nri_counties [{fips, county, coastal, inland, rating}], inforce_history {YYYY: in-force policy records on Jul 31}
Run AFTER tools/pull_raw.py finishes (one network job at a time). Usage: python -I tools/collect_state_small.py [ST ...]"""
import json, os, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES, slug, FIPS, assemble
import ffcalc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NRI = "https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0/query"

def get(url, tries=6):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "floodinsurancedata"}), timeout=180) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(4 * (i + 1))
    raise RuntimeError(repr(last)[:100])

def fema(ver, ds, filt, select):
    rows, skip, total = [], 0, None
    while True:
        r = get(f"https://www.fema.gov/api/open/{ver}/{ds}?" + urllib.parse.urlencode(
            {"$filter": filt, "$select": select, "$top": 1000, "$skip": skip, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote))
        total = r["metadata"]["count"]; got = r[ds]; rows += got
        if not got or len(rows) >= total: break
        skip += 1000
    if len(rows) != total: raise RuntimeError(f"{ds}: {len(rows)}/{total}")
    return rows

def count(filt, tries=6):
    return get("https://www.fema.gov/api/open/v3/NfipPolicies?" + urllib.parse.urlencode(
        {"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}, quote_via=urllib.parse.quote), tries)["metadata"]["count"]

def run(st):
    d = os.path.join(ROOT, "data", "states", slug(st)); os.makedirs(d, exist_ok=True)
    out = {}
    out["crs"] = fema("v1", "NfipCommunityStatusBook", f"state eq '{st}'",
                      "communityName,county,classRating,sfhaDiscount,nonSfhaDiscount,participatingInNFIP,currentlyEffectiveMapDate")   # map date: PLAN 3e
    out["declarations"] = fema("v2", "DisasterDeclarationsSummaries", f"state eq '{st}'",
                               "disasterNumber,declarationType,incidentType,declarationTitle,fyDeclared,declarationDate,fipsCountyCode")
    out["housing"] = fema("v2", "HousingAssistanceOwners", f"state eq '{st}'",
                          "disasterNumber,county,validRegistrations,totalApprovedIhpAmount")
    ml = fema("v1", "IndividualAssistanceMultipleLossFloodProperties", f"fipsStateCode eq '{FIPS[st]}'",
              "fipsCountyCode,highRiskPropertyType")
    byc = {}
    for r in ml:
        g = FIPS[st] + (r.get("fipsCountyCode") or "")
        b = byc.setdefault(g, {"total": 0, "srl": 0}); b["total"] += 1; b["srl"] += r.get("highRiskPropertyType") == "SRL"
    out["multiloss"] = {"total": len(ml), "srl": sum(b["srl"] for b in byc.values()), "by_county": byc,
                        "retrieved": time.strftime("%Y-%m-%d"), "source": "OpenFEMA IndividualAssistanceMultipleLossFloodProperties v1"}
    pen = fema("v1", "NfipResidentialPenetrationRates", f"state eq '{NAMES[st]}'",
               "fipsCode,county,resContractsInForce,resContractsInForceSfha,totalResStructures,totalResStructuresSfha,asOfDate")
    c, cs, s, ss = (sum(int(r.get(k) or 0) for r in pen) for k in
                    ("resContractsInForce", "resContractsInForceSfha", "totalResStructures", "totalResStructuresSfha"))
    out["penetration"] = {"overall_pct": round(100 * c / s, 1) if s else None, "sfha_pct": round(100 * cs / ss, 1) if ss else None,
                          "contracts": c, "sfha_contracts": cs, "asof": (pen[0]["asOfDate"][:10] if pen else None),
                          "by_county": {r["fipsCode"]: {"overall_pct": round(100 * int(r["resContractsInForce"] or 0) / int(r["totalResStructures"]), 1)
                                                       if r.get("totalResStructures") else None} for r in pen},
                          "source": "OpenFEMA NfipResidentialPenetrationRates v1 (summed over the state's counties)"}
    nri = get(NRI + "?" + urllib.parse.urlencode({"where": f"STATEABBRV='{st}'", "outFields": "STCOFIPS,COUNTY,CFLD_RISKR,IFLD_RISKR",
                                                  "f": "json", "returnGeometry": "false", "resultRecordCount": 1000}))
    out["nri_counties"] = [{"fips": f["attributes"]["STCOFIPS"], "county": f["attributes"]["COUNTY"],
                            "coastal": f["attributes"]["CFLD_RISKR"], "inland": f["attributes"]["IFLD_RISKR"],
                            "rating": ffcalc.worst_flood_rating(f["attributes"]["CFLD_RISKR"], f["attributes"]["IFLD_RISKR"])}
                           for f in nri.get("features", [])]
    # FEMA's API times out (503 after ~147 s) on this count for the biggest states, sliced or not; then the
    # page simply has no trend card and says nothing about a trend (gap recorded here, never guessed)
    hist = {}
    try:
        for y in range(2019, 2027):
            a = f"{y}-07-31T00:00:00.000z"
            hist[str(y)] = count(f"propertyState eq '{st}' and policyEffectiveDate le '{a}' and policyTerminationDate ge '{a}'", tries=2)
        out["inforce_history"] = {"by_year": hist, "note": "in-force NFIP policy records on July 31 of each year", "source": "OpenFEMA NfipPolicies v3"}
    except RuntimeError as e:
        hist = None
        out["inforce_history"] = {"by_year": None, "unavailable": f"OpenFEMA count query timed out: {e}"}
    old = json.load(open(os.path.join(d, "data.json"))) if os.path.exists(os.path.join(d, "data.json")) else {}
    for k in ("crs", "declarations", "housing"):
        if len(out[k]) < 0.8 * len(old.get(k) or []): raise RuntimeError(f"{k} shrank {len(old[k])} -> {len(out[k])}")   # keep last month's file
    json.dump(out, open(os.path.join(d, "data.json"), "w"))
    assemble(d)
    print(f"{st}: crs {len(out['crs'])}, decl {len(out['declarations'])}, housing {len(out['housing'])}, multiloss {len(ml)}, "
          f"pen {out['penetration']['overall_pct']}%, nri counties {len(out['nri_counties'])}, in-force {hist}", flush=True)

if __name__ == "__main__":
    failed = []
    for st in (sys.argv[1:] or sorted(NAMES)):
        for attempt in (1, 2):
            try: run(st); break
            except Exception as e:
                print(st, "FAILED", repr(e)[:150], flush=True)
                if attempt == 2: failed.append(st)
    if failed: sys.exit(f"STOP: {failed} not refreshed; a fresh date must not sit on last month's figures")
