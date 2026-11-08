"""State insurance regulators, for the "who to call" line on state and county pages (hcu-critique 11-07, checklist F).
Candidate official URLs are fetched one by one; a state is kept only if its own page title names insurance (evidence
saved beside it). No phone numbers: each would need its own read. Writes data/us/insurance_depts.json
{"TX": {"name": "...", "url": "...", "title": "<page title as fetched>", "read": "YYYY-MM-DD"}}.
Usage: python -I tools/fetch_insurance_depts.py   (re-run any time; states that fail keep their last good entry)"""
import datetime, html, json, os, re, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "us", "insurance_depts.json")
C = {"AL": "https://www.aldoi.gov/", "AK": "https://www.commerce.alaska.gov/web/ins/", "AZ": "https://difi.az.gov/",
     "AR": "https://insurance.arkansas.gov/", "CA": "https://www.insurance.ca.gov/", "CO": "https://doi.colorado.gov/",
     "CT": "https://portal.ct.gov/cid", "DE": "https://insurance.delaware.gov/", "DC": "https://disb.dc.gov/",
     "FL": "https://www.myfloridacfo.com/division/consumers", "GA": "https://oci.georgia.gov/", "HI": "https://cca.hawaii.gov/ins/",
     "ID": "https://doi.idaho.gov/", "IL": "https://idoi.illinois.gov/", "IN": "https://www.in.gov/idoi/", "IA": "https://iid.iowa.gov/",
     "KS": "https://insurance.kansas.gov/", "KY": "https://insurance.ky.gov/", "LA": "https://www.ldi.la.gov/", "ME": "https://www.maine.gov/pfr/insurance/",
     "MD": "https://insurance.maryland.gov/", "MA": "https://www.mass.gov/orgs/division-of-insurance", "MI": "https://www.michigan.gov/difs",
     "MN": "https://mn.gov/commerce/insurance/", "MS": "https://www.mid.ms.gov/", "MO": "https://insurance.mo.gov/", "MT": "https://csimt.gov/",
     "NE": "https://doi.nebraska.gov/", "NV": "https://doi.nv.gov/", "NH": "https://www.insurance.nh.gov/", "NJ": "https://www.nj.gov/dobi/index.shtml",
     "NM": "https://www.osi.state.nm.us/", "NY": "https://www.dfs.ny.gov/", "NC": "https://www.ncdoi.gov/", "ND": "https://www.insurance.nd.gov/",
     "OH": "https://insurance.ohio.gov/", "OK": "https://www.oid.ok.gov/", "OR": "https://dfr.oregon.gov/", "PA": "https://www.pa.gov/agencies/insurance",
     "RI": "https://dbr.ri.gov/insurance", "SC": "https://doi.sc.gov/", "SD": "https://dlr.sd.gov/insurance/", "TN": "https://www.tn.gov/commerce/insurance.html",
     "TX": "https://www.tdi.texas.gov/", "UT": "https://insurance.utah.gov/", "VT": "https://dfr.vermont.gov/", "VA": "https://www.scc.virginia.gov/pages/Bureau-of-Insurance",
     "WA": "https://www.insurance.wa.gov/", "WV": "https://www.wvinsurance.gov/", "WI": "https://oci.wi.gov/", "WY": "https://doi.wyo.gov/"}

NAME = {"AL": "Alabama Department of Insurance", "AK": "Alaska Division of Insurance", "AZ": "Arizona Department of Insurance and Financial Institutions",
 "AR": "Arkansas Insurance Department", "CA": "California Department of Insurance", "CO": "Colorado Division of Insurance", "CT": "Connecticut Insurance Department",
 "DE": "Delaware Department of Insurance", "DC": "DC Department of Insurance, Securities and Banking", "FL": "Florida Department of Financial Services (consumer help)",
 "GA": "Georgia Office of the Commissioner of Insurance and Safety Fire", "HI": "Hawaii Insurance Division", "ID": "Idaho Department of Insurance",
 "IL": "Illinois Department of Insurance", "IN": "Indiana Department of Insurance", "IA": "Iowa Insurance Division", "KS": "Kansas Insurance Department",
 "KY": "Kentucky Department of Insurance", "LA": "Louisiana Department of Insurance", "ME": "Maine Bureau of Insurance", "MD": "Maryland Insurance Administration",
 "MA": "Massachusetts Division of Insurance", "MI": "Michigan Department of Insurance and Financial Services", "MN": "Minnesota Department of Commerce, Insurance",
 "MS": "Mississippi Insurance Department", "MO": "Missouri Department of Insurance", "MT": "Montana Commissioner of Securities and Insurance",
 "NE": "Nebraska Department of Insurance", "NV": "Nevada Division of Insurance", "NH": "New Hampshire Insurance Department", "NJ": "New Jersey Department of Banking and Insurance",
 "NM": "New Mexico Office of the Superintendent of Insurance", "NY": "New York Department of Financial Services", "NC": "North Carolina Department of Insurance",
 "ND": "North Dakota Insurance Department", "OH": "Ohio Department of Insurance", "OK": "Oklahoma Insurance Department", "OR": "Oregon Division of Financial Regulation",
 "PA": "Pennsylvania Insurance Department", "RI": "Rhode Island Department of Business Regulation, Insurance", "SC": "South Carolina Department of Insurance",
 "SD": "South Dakota Division of Insurance", "TN": "Tennessee Department of Commerce and Insurance", "TX": "Texas Department of Insurance", "UT": "Utah Insurance Department",
 "VT": "Vermont Department of Financial Regulation", "VA": "Virginia Bureau of Insurance (State Corporation Commission)", "WA": "Washington Office of the Insurance Commissioner",
 "WV": "West Virginia Offices of the Insurance Commissioner", "WI": "Wisconsin Office of the Commissioner of Insurance", "WY": "Wyoming Department of Insurance"}
assert set(NAME) == set(C)

def title(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    t = urllib.request.urlopen(req, timeout=30).read(400_000).decode("utf-8", "ignore")
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", t)
    return re.sub(r"\s+", " ", html.unescape(m[1])).strip() if m else ""

if __name__ == "__main__":
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    out, miss = dict(old), []
    for st, u in C.items():
        try: t = title(u)
        except Exception as e: t = ""; err = repr(e)[:60]
        # the page's own title must name insurance (or the regulator's known acronym in it); else not shown
        if re.search(r"insurance|\bDIFS\b|\bDFS\b|\bDISB\b|\bOCI\b|\bCSI\b|Financial Services|Financial Regulation|Securities|\bIDOI\b|\bNC DOI\b", t, re.I):
            name = NAME[st]
            out[st] = {"url": u, "title": t, "name": name, "read": datetime.date.today().isoformat()}
        else: miss.append(f"{st} ({t[:50] or err})")
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"insurance depts: {len(out)} of {len(C)} kept; not confirmed: {', '.join(miss) or 'none'}")
