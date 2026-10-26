"""Independent recompute (docs/GATE-PROMPT.md layer D) + source drift. Release-level, network, run as ONE job.
1. Picks 2 random counties under 25,000 policy units, pulls policies + claims straight from OpenFEMA and recomputes
   the hero figures with code that deliberately shares nothing with ffcalc.py (statistics.median, plain loops),
   then compares with the figures tagged on the built page. A shared bug can't hide in both.
2. Re-fetches FEMA's field definitions; a changed hash means FEMA changed what a field means -> re-read it.
3. Re-fetches every rules_registry source marked "curl" and checks its excerpt is still on the page.
Usage: python -I tools/recheck.py [--base https://floodinsurancedata.com] [slug ...]   -> state/recheck.jsonl
Exit 1 on any mismatch."""
import datetime, html, json, os, random, re, statistics, subprocess, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as MX                    # registry metadata only (field defs); no calculation is shared
from rules_registry import RULES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.fema.gov/api/open/v3/"
ASOF = "2026-07-31T00:00:00.000z"
args = sys.argv[1:]
base = None
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
    for k, v in re.findall(r'<span data-m="(\w+)"[^>]*>([^<]*)</span>', src):
        try: out.setdefault(k, float(v.replace("$", "").replace(",", "").replace("%", "")))
        except ValueError: pass   # a text figure ("16th highest" rank); recheck compares numbers only
    return out

def recompute(c):
    sfh = lambda r: str(r.get("occupancyType")) in ("1", "11") and str(r.get("primaryResidenceIndicator")) in ("True", "true", "1")
    pol = pull("NfipPolicies", f"propertyState eq '{c['state']}' and startswith(censusGeoid,'{c['geoid']}') and "
               f"policyEffectiveDate le '{ASOF}' and policyTerminationDate ge '{ASOF}'",
               "id,policyCost,totalInsurancePremiumOfThePolicy,fullRiskPremium,occupancyType,primaryResidenceIndicator,policyCount,ratedFloodZone")
    units = sum(int(r.get("policyCount") or 0) for r in pol)
    hi = sum(int(r.get("policyCount") or 0) for r in pol if (r.get("ratedFloodZone") or "")[:1] in ("A", "V"))
    coh = [r for r in pol if sfh(r)]
    costs = [r["policyCost"] for r in coh if isinstance(r.get("policyCost"), (int, float)) and r["policyCost"] > 0]
    pairs = [(r["totalInsurancePremiumOfThePolicy"], r["fullRiskPremium"]) for r in coh
             if all(isinstance(r.get(f), (int, float)) and r[f] > 0 for f in ("totalInsurancePremiumOfThePolicy", "fullRiskPremium"))]
    clm = pull("NfipClaims", f"state eq '{c['state']}' and countyCode eq '{c['geoid']}'",
               "id,netBuildingPaymentAmount,netContentsPaymentAmount,netIccPaymentAmount")
    paid = sum(1 for r in clm if sum((r.get(f) or 0) for f in ("netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount")) > 0)
    return {"units": units, "cost_p50": round(statistics.median(costs)), "sfha_share": round(100 * hi / units, 1),
            "share_below": round(100 * sum(1 for a, b in pairs if a < b) / len(pairs), 1),
            "prem_median": round(statistics.median(a for a, _ in pairs)), "frp_median": round(statistics.median(b for _, b in pairs)),
            "claims_filed": len(clm), "claims_paid_n": paid}

# tolerance: the API keeps receiving late records, so counts may drift ~1% between the pull and the check
TOL = {"units": 0.01, "claims_filed": 0.01, "claims_paid_n": 0.01, "cost_p50": 0.01, "prem_median": 0.01,
       "frp_median": 0.01, "share_below": 1.0, "sfha_share": 1.0}   # pct metrics: points; others: relative
problems, log = [], {"date": str(datetime.date.today()), "base": base or "dist"}

slugs = args or random.sample([s for s in counties if json.load(open(os.path.join(ROOT, "data", s, "agg.json")))["policies"]["units"] < 25000], 2)
log["counties"] = {}
for s in slugs:
    mine, shown = recompute(counties[s]), page_figures(s)
    rows = {}
    for k, v in mine.items():
        p = shown.get(k)
        ok = p is not None and (abs(v - p) <= TOL[k] if TOL[k] >= 1 else abs(v - p) <= TOL[k] * max(abs(v), 1))
        rows[k] = {"recomputed": v, "page": p, "ok": ok}
        if not ok: problems.append(f"{s} {k}: recomputed {v}, page shows {p}")
    log["counties"][s] = rows
    print(f"{s}: " + ", ".join(f"{k} {'ok' if r['ok'] else 'MISMATCH'} ({r['recomputed']} vs {r['page']})" for k, r in rows.items()))

stored = json.load(open(MX.DEFS))
now = MX.fetch_defs()
for ds, fields in now.items():
    for f, v in fields.items():
        old = (stored.get(ds) or {}).get(f)
        if not v or not old or v["sha256"] != old["sha256"]:
            problems.append(f"FEMA definition changed or vanished: {ds}.{f} — re-read it, update metrics.py, then --refresh")
print("field definitions:", "unchanged" if not any("definition" in p for p in problems) else "CHANGED")

cache = {}
for k, r in RULES.items():
    for url, ex, method in r["sources"]:
        if method != "curl": continue
        if url not in cache:
            raw = subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "--max-time", "60", url], capture_output=True).stdout.decode("utf-8", "replace")
            raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
            cache[url] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
        if ex not in cache[url]: problems.append(f"rule {k}: excerpt no longer on {url}: {ex!r}")
manual = sorted({k for k, r in RULES.items() for _, _, m_ in r["sources"] if m_ == "manual"})
print("rules: curl sources", "all present" if not any(p.startswith("rule ") for p in problems) else "MISSING",
      f"| manual (human re-read due): {manual}")

log["problems"], log["pass"] = problems, not problems
os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
open(os.path.join(ROOT, "state", "recheck.jsonl"), "a").write(json.dumps(log) + "\n")
print("RECHECK", "PASS" if not problems else "FAIL")
for p in problems: print("  -", p)
sys.exit(1 if problems else 0)
