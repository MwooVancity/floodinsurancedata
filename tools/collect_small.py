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

def fetch_all(ds, ver, filt, select, orderby=None):
    """Paginate through ALL matching rows; fail (raise) if the final count != API's reported total.
    Fail-closed: a truncated response must never be saved as if complete."""
    rows, skip, total = [], 0, None
    while True:
        p = {"$filter": filt, "$select": select, "$top": 1000, "$skip": skip, "$inlinecount": "allpages"}
        if orderby: p["$orderby"] = orderby
        r = get(f"https://www.fema.gov/api/open/{ver}/{ds}?" + urllib.parse.urlencode(p, quote_via=urllib.parse.quote))
        total = r["metadata"]["count"]
        got = r[ds]
        rows += got
        if not got or len(rows) >= total:
            break
        skip += 1000
    if len(rows) != total:
        raise SystemExit(f"{ds}: truncated {len(rows)}/{total} — not saving a partial dataset")
    return rows

d = {}
d["crs"] = fetch_all("NfipCommunityStatusBook", "v1", f"state eq '{ST}' and county eq '{CO} COUNTY'",
                     "communityName,classRating,sfhaDiscount,nonSfhaDiscount,participatingInNFIP")
print("CRS communities:", len(d["crs"]))
d["declarations"] = fetch_all("DisasterDeclarationsSummaries", "v2", f"state eq '{ST}' and fipsCountyCode eq '{CO3}'",
                              "disasterNumber,declarationType,incidentType,declarationTitle,fyDeclared,declarationDate",
                              orderby="declarationDate desc")
print("declarations (all types):", len(d["declarations"]))
d["housing"] = fetch_all("HousingAssistanceOwners", "v2", f"state eq '{ST}' and county eq '{COT} (County)'",
                         "disasterNumber,zipCode,city,validRegistrations,totalApprovedIhpAmount,repairReplaceAmount,averageFemaInspectedDamage")
print("housing rows:", len(d["housing"]))

json.dump(d, open(OUT, "w"))
print("saved", OUT, "for", COT, "County", ST)
