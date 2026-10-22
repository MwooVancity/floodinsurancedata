"""Pull FEMA National Risk Index flood fields for a county and merge into agg.json.
Authoritative keyless source: FEMA_NationalRiskIndex ArcGIS org. Usage: nri.py <STCOFIPS> [agg.json]"""
import json, sys, urllib.parse, urllib.request

FIPS = sys.argv[1] if len(sys.argv) > 1 else "12071"
AGG = sys.argv[2] if len(sys.argv) > 2 else "agg.json"
BASE = ("https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/"
        "National_Risk_Index_Counties/FeatureServer/0/query")

def get(u, t=60):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "ff"}), timeout=t) as r:
        return json.load(r)

r = get(BASE + "?" + urllib.parse.urlencode(
    {"where": f"STCOFIPS='{FIPS}'", "outFields": "*", "f": "json", "returnGeometry": "false", "resultRecordCount": 1}))
feats = r.get("features", [])
agg = json.load(open(AGG))
if not feats:
    agg["nri"] = None
    print("NRI: no row for", FIPS)
else:
    a = feats[0]["attributes"]
    def g(k): return a.get(k)
    # CFLD = coastal flooding, RFLD = riverine/inland flooding. Keep rating, score, national percentile, EAL$.
    agg["nri"] = {
        "county": a.get("COUNTY"), "state": a.get("STATEABBRV"),
        "coastal": {"risk_rating": g("CFLD_RISKR"), "risk_score": g("CFLD_RISKS"),
                    "eal_rating": g("CFLD_EALR"), "eal_national_pctl": g("CFLD_ALR_NPCTL"),
                    "eal_total_usd": g("CFLD_EALT")},
        "riverine": {"risk_rating": g("RFLD_RISKR"), "risk_score": g("RFLD_RISKS"),
                     "eal_rating": g("RFLD_EALR"), "eal_national_pctl": g("RFLD_ALR_NPCTL"),
                     "eal_total_usd": g("RFLD_EALT")},
        "source": "FEMA National Risk Index (county), FEMA_NationalRiskIndex ArcGIS, keyless",
    }
    print("NRI ok:", a.get("COUNTY"), "coastal", g("CFLD_RISKR"), "pctl", g("CFLD_ALR_NPCTL"),
          "| riverine", g("RFLD_RISKR"), "pctl", g("RFLD_ALR_NPCTL"))
json.dump(agg, open(AGG, "w"))
