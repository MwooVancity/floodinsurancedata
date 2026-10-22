"""Pull the small, reliable per-county datasets (CRS, declarations, housing) to data.json.
Parameterized by env: FF_STATE, FF_GEOID (5-digit), FF_COUNTY (e.g. LEE), FF_COUNTYTITLE (e.g. Lee)."""
import json, os, urllib.parse, urllib.request

ST = os.environ.get("FF_STATE", "FL")
GEO = os.environ.get("FF_GEOID", "12071")
CO = os.environ.get("FF_COUNTY", "LEE").upper()          # CRS: "LEE COUNTY"
COT = os.environ.get("FF_COUNTYTITLE", "Lee")            # housing: "Lee (County)"
CO3 = GEO[2:]                                             # declarations fipsCountyCode
OUT = os.path.join(os.environ.get("FF_DIR", "."), "data.json")

def get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ff"}), timeout=timeout) as r:
        return json.load(r)
def ofm(ds, params, ver="v2"):
    return get(f"https://www.fema.gov/api/open/{ver}/{ds}?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))

d = {}
r = ofm("NfipCommunityStatusBook", {"$filter": f"state eq '{ST}' and county eq '{CO} COUNTY'",
        "$select": "communityName,classRating,sfhaDiscount,nonSfhaDiscount,participatingInNFIP",
        "$top": 80, "$inlinecount": "allpages"}, ver="v1")
d["crs"] = r["NfipCommunityStatusBook"]
print("CRS communities:", len(d["crs"]))

r = ofm("DisasterDeclarationsSummaries", {"$filter": f"state eq '{ST}' and fipsCountyCode eq '{CO3}'",
        "$select": "disasterNumber,declarationType,incidentType,declarationTitle,fyDeclared,declarationDate",
        "$top": 300, "$inlinecount": "allpages", "$orderby": "declarationDate desc"})
d["declarations"] = r["DisasterDeclarationsSummaries"]
print("declarations (all types):", r["metadata"]["count"])

r = ofm("HousingAssistanceOwners", {"$filter": f"state eq '{ST}' and county eq '{COT} (County)'",
        "$select": "disasterNumber,zipCode,city,validRegistrations,totalApprovedIhpAmount,repairReplaceAmount,averageFemaInspectedDamage",
        "$top": 2000, "$inlinecount": "allpages"})
d["housing"] = r["HousingAssistanceOwners"]
print("housing rows:", r["metadata"]["count"])

json.dump(d, open(OUT, "w"))
print("saved", OUT, "for", COT, "County", ST)
