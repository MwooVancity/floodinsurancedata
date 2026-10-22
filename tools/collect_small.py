"""Pull the small, reliable Lee County FL (12071) datasets and save to data.json.
Also probe NfipClaims field names for the bulk collector."""
import json, urllib.parse, urllib.request

OUT = "data.json"
def get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ff"}), timeout=timeout) as r:
        return json.load(r)
def ofm(ds, params, ver="v2"):
    return get(f"https://www.fema.gov/api/open/{ver}/{ds}?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))

d = {}

# NRI flood risk (county) --------------------------------------------------------
base = "https://services2.arcgis.com/EiGeaCDLpVDPqdJ5/ArcGIS/rest/services/NRI_Counties_EAL/FeatureServer/0/query"
sel = ("State_County_FIPS_Code,County,State,"
       "Coastal_Flooding___Expected_Annual_Loss___Total,Coastal_Flooding___Expected_Annual_Loss_Rating,"
       "Coastal_Flooding___Expected_Annual_Loss_Rate___National_Percentile,"
       "Inland_Flooding___Expected_Annual_Loss___Total,Inland_Flooding___Expected_Annual_Loss_Rating,"
       "Inland_Flooding___Expected_Annual_Loss_Rate___National_Percentile,"
       "Inland_Flooding___Number_of_Events,Coastal_Flooding___Number_of_Events")
for where in ("State_County_FIPS_Code=12071", "State_County_FIPS_Code='12071'"):
    try:
        r = get(base + "?" + urllib.parse.urlencode({"where": where, "outFields": sel, "f": "json", "returnGeometry": "false"}))
        if r.get("features"):
            d["nri"] = r["features"][0]["attributes"]
            print("NRI ok via", where)
            break
    except Exception as e:
        print("NRI err", repr(e)[:80])
else:
    print("NRI: no match")

# CRS discounts (communities in Lee County) --------------------------------------
r = ofm("NfipCommunityStatusBook", {"$filter": "state eq 'FL' and county eq 'LEE COUNTY'",
        "$select": "communityName,classRating,sfhaDiscount,nonSfhaDiscount,participatingInNFIP",
        "$top": 50, "$inlinecount": "allpages"}, ver="v1")
d["crs"] = r["NfipCommunityStatusBook"]
print("CRS communities:", len(d["crs"]))

# Disaster declarations (Lee County, all incident types for context) -------------
r = ofm("DisasterDeclarationsSummaries", {"$filter": "state eq 'FL' and fipsCountyCode eq '071'",
        "$select": "disasterNumber,declarationType,incidentType,declarationTitle,fyDeclared,declarationDate",
        "$top": 200, "$inlinecount": "allpages", "$orderby": "declarationDate desc"})
d["declarations"] = r["DisasterDeclarationsSummaries"]
print("declarations (all types):", r["metadata"]["count"])

# Housing assistance (Lee County owners, aggregate across disasters) -------------
r = ofm("HousingAssistanceOwners", {"$filter": "state eq 'FL' and county eq 'Lee (County)'",
        "$select": "disasterNumber,zipCode,city,validRegistrations,totalApprovedIhpAmount,repairReplaceAmount,averageFemaInspectedDamage",
        "$top": 1000, "$inlinecount": "allpages"})
d["housing"] = r["HousingAssistanceOwners"]
print("housing rows:", r["metadata"]["count"])

# Probe NfipClaims fields for the bulk collector ---------------------------------
try:
    r = get("https://www.fema.gov/api/open/v2/NfipClaims?$top=1")
    row = r["NfipClaims"][0]
    print("CLAIMS fields:", sorted(row.keys()))
    d["_claims_fields"] = sorted(row.keys())
except Exception as e:
    print("claims probe err", repr(e)[:100])

json.dump(d, open(OUT, "w"))
print("saved", OUT)
