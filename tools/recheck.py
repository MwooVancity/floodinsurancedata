"""Independent recompute (docs/GATE-PROMPT.md layer D) + source drift. Release-level, network, run as ONE job.
1. Picks 2 random counties under 25,000 policy units, pulls policies + claims straight from OpenFEMA and recomputes
   the hero figures with code that deliberately shares nothing with ffcalc.py (statistics.median, plain loops),
   then compares with the figures tagged on the built page. A shared bug can't hide in both.
2. Re-fetches FEMA's field definitions; a changed hash means FEMA changed what a field means -> re-read it.
3. Re-fetches every rules_registry source marked "curl" and checks its excerpt is still on the page.
4. Hashes the text around each law excerpt; any change there (a new exception) fails until a person re-reads it and runs --accept-law.
Usage: python -I tools/recheck.py [--base https://floodinsurancedata.com] [--accept-law] [slug ...]
Exit 1 on any mismatch."""
import datetime, hashlib, html, json, os, random, re, statistics, subprocess, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as MX                    # registry metadata only (field defs); no calculation is shared
from rules_registry import RULES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.fema.gov/api/open/v3/"
from agg_raw import asof as _asof
ASOF = _asof() + "T00:00:00.000z"
args = sys.argv[1:]
base = None
RULES_ONLY = "--rules-only" in args   # release.py step: every rule's official wording is still on its source (seconds, not minutes)
if RULES_ONLY: args.remove("--rules-only")
ACCEPT_LAW = "--accept-law" in args   # after a person re-read the changed text
if ACCEPT_LAW: args.remove("--accept-law"); RULES_ONLY = True
if "--base" in args:
    i = args.index("--base"); base = args[i + 1]; del args[i:i + 2]
counties = {c["slug"]: c for c in json.load(open(os.path.join(ROOT, "tools", "counties.json")))}

def get(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ff-recheck"}), timeout=240) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(min(20, 3 * (i + 1)))
    raise RuntimeError(repr(last)[:90])

def pull(ds, filt, select):
    q = lambda p: API + ds + "?" + urllib.parse.urlencode(p, quote_via=urllib.parse.quote)
    total = get(q({"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}))["metadata"]["count"]
    rows, skip = {}, 0
    while len(rows) < total:
        page = get(q({"$filter": filt, "$select": select, "$top": 1000, "$skip": skip}))
        got = page[[k for k in page if k != "metadata"][0]]
        if not got: break
        for r in got: rows[r["id"]] = r
        skip += 1000
    if len(rows) != total: raise RuntimeError(f"{ds}: got {len(rows)}/{total}")
    return list(rows.values())

def page_figures(slug):
    path = os.path.join(ROOT, "dist", "flood-insurance", slug, "index.html")
    src = (urllib.request.urlopen(urllib.request.Request(f"{base}/flood-insurance/{slug}/",
                                  headers={"User-Agent": "Mozilla/5.0 (recheck)"}), timeout=60).read().decode() if base
           else open(path, encoding="utf-8").read())
    out = {}
    for k, v in re.findall(r'<span data-m="(\w+)"(?![^>]*data-q=)[^>]*>([^<]*)</span>', src):
        try: out.setdefault(k, float(v.replace("$", "").replace(",", "").replace("%", "")))
        except ValueError: pass   # a text figure ("16th highest" rank); recheck compares numbers only
    return out

def recompute(c):
    sfh = lambda r: str(r.get("occupancyType")) in ("1", "11") and str(r.get("primaryResidenceIndicator")) in ("True", "true", "1") \
        and str(r.get("condominiumCoverageTypeCode") or "N").strip().upper() in ("N", "")   # hcu 11-07: condo units out
    pol = pull("NfipPolicies", f"propertyState eq '{c['state']}' and startswith(censusGeoid,'{c['geoid']}') and "
               f"policyEffectiveDate le '{ASOF}' and policyTerminationDate gt '{ASOF}'",
               "id,policyCost,totalInsurancePremiumOfThePolicy,fullRiskPremium,occupancyType,primaryResidenceIndicator,policyCount,ratedFloodZone,originalNBDate,condominiumCoverageTypeCode")
    units = sum(int(r.get("policyCount") or 0) for r in pol)
    hi = sum(int(r.get("policyCount") or 0) for r in pol if (r.get("ratedFloodZone") or "")[:1] in ("A", "V"))
    coh = [r for r in pol if sfh(r)]
    costs = [r["policyCost"] for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0]
    pairs = [(r["totalInsurancePremiumOfThePolicy"], r["fullRiskPremium"]) for r in coh
             if all(isinstance(r.get(f), (int, float)) and r[f] > 0 for f in ("totalInsurancePremiumOfThePolicy", "fullRiskPremium"))]
    clm = pull("NfipClaims", f"state eq '{c['state']}' and countyCode eq '{c['geoid']}'",
               "id,netBuildingPaymentAmount,netContentsPaymentAmount,netIccPaymentAmount,yearOfLoss,nonPaymentReasonBuilding")
    clm = [r for r in clm if str(r.get("nonPaymentReasonBuilding") or "") not in ("98", "99")]   # bookkeeping, not claims (same rule as agg_raw)
    ispaid = lambda r: sum((r.get(f) or 0) for f in ("netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount")) > 0
    paid = sum(1 for r in clm if ispaid(r))
    # extras_raw figures (code review 2026-10-28: nothing recomputed them): past-year buyers' cost, latest decade's paid share
    nb = str(datetime.date.fromisoformat(ASOF[:10]).replace(year=int(ASOF[:4]) - 1) + datetime.timedelta(days=1))
    new = [r["policyCost"] for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0 and (r.get("originalNBDate") or "")[:10] >= nb]
    dec = [r for r in clm if str(r.get("yearOfLoss") or "")[:3] == "202"]
    return {"units": units, "cost_p50": round(statistics.median(costs)), "sfha_share": round(100 * hi / units, 1),
            "share_below": round(100 * sum(1 for a, b in pairs if a < b) / len(pairs), 1),
            "prem_median": round(statistics.median(a for a, _ in pairs)), "frp_median": round(statistics.median(b for _, b in pairs)),
            "claims_filed": len(clm), "claims_paid_n": paid,
            "x_cost_new": round(statistics.median(new)) if new else None,
            "x_paid_2020s": round(100 * sum(1 for r in dec if ispaid(r)) / len(dec), 1) if dec else None}

def extras_figures(c):   # what extras_raw wrote for this county (the page prints these; gate V2 ties page to file)
    x = json.load(open(os.path.join(ROOT, "data", "all-counties", c["geoid"] + ".json"))).get("extras") or {}
    return {"x_cost_new": (x.get("policies") or {}).get("cost_new_median"),
            "x_paid_2020s": (((x.get("claims") or {}).get("by_decade") or {}).get("2020s") or {}).get("paid_pct")}

# tolerance: the API keeps receiving late records, so counts may drift ~1% between the pull and the check
TOL = {"units": 0.01, "claims_filed": 0.01, "claims_paid_n": 0.01, "cost_p50": 0.01, "prem_median": 0.01,
       "frp_median": 0.01, "share_below": 1.0, "sfha_share": 1.0, "x_cost_new": 0.01, "x_paid_2020s": 1.0}   # pct metrics: points; others: relative
problems = []

_built = [s for s in counties if os.path.exists(os.path.join(ROOT, "data", "c", s, "agg.json"))]
slugs = [] if RULES_ONLY else args or random.sample([s for s in _built if json.load(open(os.path.join(ROOT, "data", "c", s, "agg.json")))["policies"]["units"] < 25000], 2)
for s in slugs:
    mine, shown = recompute(counties[s]), dict(page_figures(s), **extras_figures(counties[s]))
    rows = {}
    for k, v in mine.items():
        p = shown.get(k)
        ok = (v is None and p is None) or v is not None and p is not None and (abs(v - p) <= TOL[k] if TOL[k] >= 1 else abs(v - p) <= TOL[k] * max(abs(v), 1))
        rows[k] = {"recomputed": v, "page": p, "ok": ok}
        if not ok: problems.append(f"{s} {k}: recomputed {v}, page shows {p}")
    print(f"{s}: " + ", ".join(f"{k} {'ok' if r['ok'] else 'MISMATCH'} ({r['recomputed']} vs {r['page']})" for k, r in rows.items()))

stored = json.load(open(MX.DEFS))
now = {} if RULES_ONLY else MX.fetch_defs()
for ds, fields in now.items():
    for f, v in fields.items():
        old = (stored.get(ds) or {}).get(f)
        if not v or not old or v["sha256"] != old["sha256"]:
            problems.append(f"FEMA definition changed or vanished: {ds}.{f} — re-read it, update metrics.py, then --refresh")
print("field definitions:", "unchanged" if not any("definition" in p for p in problems) else "CHANGED")

def fetch_page(url):   # (text, ok): ok only on HTTP 200; 3 tries
    for _ in range(3):
        p = subprocess.run(["curl", "-sL", "--compressed", "-A", "Mozilla/5.0", "--max-time", "60", "-w", "\n%{http_code}", url], capture_output=True)
        raw, _, code = p.stdout.decode("utf-8", "replace").rpartition("\n")
        if code == "200": break
        time.sleep(10)
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))), code == "200"

# 2026-10-29 the daily release stopped because flsenate.gov did not answer GitHub's servers and that was reported as
# "excerpt gone". Unreachable is not changed: it warns, and fails only when the page has not loaded for 14 days.
# 2026-11-02: registry links are dated snapshots, so re-fetching them could never show a change in the law. Always read the current text.
LIVE = {"https://www.govinfo.gov/content/pkg/CFR-2024-title44-vol1/xml/CFR-2024-title44-vol1-sec61-11.xml": "https://www.law.cornell.edu/cfr/text/44/61.11",
        "https://www.govinfo.gov/content/pkg/USCODE-2023-title42/html/USCODE-2023-title42-chap50-subchapI-sec4012a.htm": "https://www.law.cornell.edu/uscode/text/42/4012a",
        "https://www.flsenate.gov/Laws/Statutes/2025/627.351": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/0627/Sections/0627.351.html",
        "https://www.flsenate.gov/Laws/Statutes/2025/689.302": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/0689/Sections/0689.302.html"}
SNAPSHOT = re.compile(r"govinfo\.gov/content/pkg/(CFR|USCODE)-|flsenate\.gov/Laws/Statutes/\d{4}/")
def _ecfr_dates():
    try: return {str(t["number"]): t["up_to_date_as_of"] for t in json.loads(fetch_page_raw("https://www.ecfr.gov/api/versioner/v1/titles.json"))["titles"]}
    except Exception as e: problems.append(f"eCFR latest date unavailable: {e}"); return {}
def fetch_page_raw(url):
    return subprocess.run(["curl", "-sL", "--compressed", "--max-time", "60", url], capture_output=True).stdout.decode("utf-8", "replace")
ECFR = _ecfr_dates()
def live(url):
    m = re.search(r"ecfr\.gov/api/versioner/v1/full/[\d-]+/title-(\d+)\.xml", url)
    if m and m[1] in ECFR: return re.sub(r"/full/[\d-]+/", f"/full/{ECFR[m[1]]}/", url)
    return LIVE.get(url, url)
assert live("https://www.flsenate.gov/Laws/Statutes/2025/689.302") != "https://www.flsenate.gov/Laws/Statutes/2025/689.302"
OKF = os.path.join(ROOT, "state", "rule-fetch-ok.json")
last_ok = json.load(open(OKF)) if os.path.exists(OKF) else {}
today = datetime.date.today()
cache = {}
LAWF = os.path.join(ROOT, "state", "law-sections.json")
law = json.load(open(LAWF)) if os.path.exists(LAWF) else {}
LAWHOST = re.compile(r"ecfr\.gov|law\.cornell\.edu|leg\.state\.fl\.us")
for k, r in RULES.items():
    for url, ex, method in r["sources"]:
        if method != "curl": continue
        if SNAPSHOT.search(url) and url not in LIVE: problems.append(f"rule {k}: dated snapshot with no live page in recheck.LIVE: {url}")
        url = live(url)
        if url not in cache:
            cache[url] = fetch_page(url)
            if cache[url][1]: last_ok[url] = today.isoformat()
        text, ok = cache[url]
        if ok and ex not in text: problems.append(f"rule {k}: excerpt no longer on {url}: {ex!r}")
        elif ok and LAWHOST.search(url):   # the excerpt can survive while a new exception lands beside it
            i = text.index(ex); h = hashlib.sha256(text[max(0, i - 1500):i + len(ex) + 1500].encode()).hexdigest()[:16]
            lk = f"{k}|{ex[:50]}"
            if lk in law and law[lk] != h and not ACCEPT_LAW: problems.append(f"rule {k}: law text changed near {ex[:50]!r} on {url}; re-read it, fix the rule if needed, then --accept-law")
            elif law.get(lk) != h: law[lk] = h
        elif not ok:
            age = (today - datetime.date.fromisoformat(last_ok[url])).days if url in last_ok else 999
            if age > 14: problems.append(f"rule {k}: {url} has not loaded for {age} days; re-read it by hand")
            else: print(f"warning: rule {k}: {url} did not load this run (last loaded {age} days ago)")
json.dump(last_ok, open(OKF, "w"), indent=1, sort_keys=True)
json.dump(law, open(LAWF, "w"), indent=1, sort_keys=True)
manual = sorted({k for k, r in RULES.items() for _, _, m_ in r["sources"] if m_ == "manual"})
MRF = os.path.join(ROOT, "state", "manual-rule-read.json")   # {rule: date a person or Claude last read its source in raw text}
read = json.load(open(MRF))
for k in manual:   # no script can reach these sources, so an old reading stops the release: re-read, then update the date
    age = (today - datetime.date.fromisoformat(read[k])).days if k in read else 999
    if age > 183: problems.append(f"rule {k}: source last read {age} days ago; re-read it in raw text and update state/manual-rule-read.json")
print("rules: curl sources", "all present" if not any(p.startswith("rule ") for p in problems) else "MISSING",
      f"| manual (human re-read due): {manual}")

print("RECHECK", "PASS" if not problems else "FAIL")
for p in problems: print("  -", p)
sys.exit(1 if problems else 0)
