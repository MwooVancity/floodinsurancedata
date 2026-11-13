"""Pull every in-force NFIP policy and every NFIP claim for the 50 states + DC ONCE, to compact gzip CSVs in
.cache/raw/, so state, county and ZIP figures (and any new metric) are computed offline without touching FEMA again.
- Policies in force on ASOF, sliced by policyEffectiveDate month; claims sliced by yearOfLoss. Each slice's unique
  ids must equal FEMA's count for that slice; the slices must sum to the state total, or the state is not marked done.
- Resumable: finished slices are skipped. 3 worker threads (OpenFEMA tolerates it; the shrink-on-503 retry handles bursts).
Usage: python -I tools/pull_raw.py [ST ...]       Log: .cache/raw/pull.log"""
import csv, datetime, gzip, io, json, os, sys, threading, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, ".cache", "raw")
API = "https://www.fema.gov/api/open/v3/"
def _asof():   # end of the month 3 months back (FEMA updates monthly, with a lag); a resumed pull keeps the date it started with
    p = os.path.join(RAW, "asof.txt")
    if os.path.exists(p): return open(p).read().strip()
    t = datetime.date.today().replace(day=1)
    for _ in range(2): t = (t - datetime.timedelta(days=1)).replace(day=1)
    d = str(t - datetime.timedelta(days=1)); os.makedirs(RAW, exist_ok=True); open(p, "w").write(d); return d
ASOF_DATE = datetime.date.fromisoformat(_asof())
ASOF = f"{ASOF_DATE}T00:00:00.000z"
STATES = ("DC HI WY SD AK MT VT ND NH NE UT ID NM KS NV IA ME WV OK OR CO KY AR RI MN WI TN IN MO MI AZ WA MS DE CT "
          "OH IL AL MD PA GA MA VA NC SC NY NJ CA LA TX FL").split()          # smallest first
POL_FIELDS = ("id propertyState censusGeoid reportedZipCode reportedCity nfipCommunityNumberCurrent ratedFloodZone floodZoneCurrent "
              "occupancyType primaryResidenceIndicator policyCount policyCost totalInsurancePremiumOfThePolicy fullRiskPremium "
              "federalPolicyFee hfiaaSurcharge reserveFundAssessment iccPremium crsClassCode buildingDeductibleCode contentsDeductibleCode "
              "totalBuildingInsuranceCoverage totalContentsInsuranceCoverage buildingReplacementCost elevatedBuildingIndicator "
              "elevationCertificateIndicator postFIRMConstructionIndicator preFIRMConstructionIndicator grandfatheringTypeCode "
              "mandatoryPurchaseFlag rateMethod originalNBDate policyEffectiveDate originalConstructionDate propertyPurchaseDate "
              "rentalPropertyIndicator tenantIndicator condominiumCoverageTypeCode numberOfFloorsInInsuredBuilding foundationType "
              "waitingPeriodType subsidizedRateType obstructionType basementEnclosureCrawlspaceType floodproofedIndicator").split()   # 11-12 cloud field batch (PLAN)
CLM_FIELDS = ("id state countyCode censusGeoid reportedZipCode yearOfLoss dateOfLoss floodEvent eventDesignationNumber causeOfDamage "
              "ratedFloodZone floodZoneCurrent occupancyType primaryResidenceIndicator policyCount netBuildingPaymentAmount "
              "netContentsPaymentAmount netIccPaymentAmount buildingDamageAmount contentsDamageAmount buildingPropertyValue "
              "totalBuildingInsuranceCoverage totalContentsInsuranceCoverage buildingDeductibleCode nonPaymentReasonBuilding "
              "nonPaymentReasonContents waterDepth floodWaterDuration elevatedBuildingIndicator postFIRMConstructionIndicator "
              "rateMethod originalNBDate crsClassCode nfipCommunityNumberCurrent").split()
LOCK = threading.Lock()
def log(msg):
    line = f"{datetime.datetime.now():%H:%M:%S} {msg}"
    with LOCK:
        print(line, flush=True); open(os.path.join(RAW, "pull.log"), "a").write(line + "\n")

def get(url, tries=8):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "floodinsurancedata-pull"}), timeout=300) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(min(60, 4 * (i + 1)))
    raise RuntimeError("exhausted: " + repr(last)[:100])

def q(ds, params): return API + ds + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
def count(ds, filt): return get(q(ds, {"$filter": filt, "$select": "id", "$top": 1, "$inlinecount": "allpages"}))["metadata"]["count"]

def slices(ds, st):
    if ds == "NfipPolicies":
        base = f"propertyState eq '{st}' and policyEffectiveDate le '{ASOF}' and policyTerminationDate gt '{ASOF}'"
        # NFIP terms are at most 3 years, so nothing older is in force (FL, TX 2026-11-03: 0 rows); one guard slice keeps
        # the sum exact if FEMA ever has such a row. Cut ~45 empty slices per state, the ones that drew most 503s.
        d = ASOF_DATE.replace(year=ASOF_DATE.year - 3, day=1)
        out = [("older", base + f" and policyEffectiveDate lt '{d}T00:00:00.000z'")]
        while d <= ASOF_DATE.replace(day=1):
            n = (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
            out.append((f"{d:%Y%m}", base + f" and policyEffectiveDate ge '{d}T00:00:00.000z' and policyEffectiveDate lt '{n}T00:00:00.000z'"))
            d = n
        return base, out
    base = f"state eq '{st}'"
    return base, [("noyear", base + " and yearOfLoss eq null")] + [(str(y), base + f" and yearOfLoss eq {y}") for y in range(1970, datetime.date.today().year + 1)]

def pull_slice(ds, st, name, filt, fields):
    d = os.path.join(RAW, ds, st); os.makedirs(d, exist_ok=True)
    done = os.path.join(d, name + ".done")
    if os.path.exists(done): return json.load(open(done))["n"]
    total = count(ds, filt)
    rows, skip, top = {}, 0, 1000
    while len(rows) < total:
        try:
            page = get(q(ds, {"$filter": filt, "$select": ",".join(fields), "$top": top, "$skip": skip}))
        except RuntimeError:
            if top > 125: top //= 2; continue
            raise
        got = page[[k for k in page if k != "metadata"][0]]
        if not got: break
        for r in got: rows[r["id"]] = r
        skip += top
    if len(rows) != total:
        raise RuntimeError(f"{ds} {st} {name}: {len(rows)}/{total} unique")
    buf = io.StringIO(); w = csv.writer(buf); w.writerow(fields)
    for r in rows.values(): w.writerow(["" if r.get(f) is None else r.get(f) for f in fields])
    with gzip.open(os.path.join(d, name + ".csv.gz"), "wt", encoding="utf-8", newline="") as f: f.write(buf.getvalue())
    json.dump({"n": total, "at": str(datetime.datetime.now())}, open(done, "w"))
    return total

RECENT = ASOF_DATE.year - 2   # claims for losses before this year are kept from last month's pull (owner 2026-10-29)
def _clear(ds, st, keep_old):
    d = os.path.join(RAW, ds, st)
    for f in (os.listdir(d) if os.path.isdir(d) else []):
        y = f.split(".")[0]
        if f.endswith(".done") and not (keep_old and y.isdigit() and int(y) < RECENT): os.remove(os.path.join(d, f))

def pull_state(ds, st, fields, full=False):
    marker = os.path.join(RAW, ds, st + ".done")
    if os.path.exists(marker):
        if json.load(open(marker)).get("asof") == str(ASOF_DATE): log(f"{ds} {st} already done"); return
        os.remove(marker); _clear(ds, st, keep_old=True)   # last month's claims: re-pull recent years and "no year" only
    if full: _clear(ds, st, keep_old=False)
    base, parts = slices(ds, st)
    d = os.path.join(RAW, ds, st); names = {n for n, _ in parts}   # agg_raw reads every *.csv.gz here: a file from an
    for f in (os.listdir(d) if os.path.isdir(d) else []):           # old slice scheme would be counted twice (2026-11-03)
        if f.split(".")[0] not in names: os.remove(os.path.join(d, f))
    total = count(ds, base); t0 = time.time()
    got = 0
    for name, filt in parts:
        for attempt in range(3):
            try: got += pull_slice(ds, st, name, filt, fields); break
            except Exception as e:
                log(f"  retry {ds} {st} {name}: {repr(e)[:120]}"); time.sleep(30)
        else:
            log(f"FAILED {ds} {st} slice {name} — state left unfinished"); return
    if got != total:
        if not full:   # FEMA revised an old year we kept: pull this state's claims in full once
            log(f"MISMATCH {ds} {st}: {got} != {total}; re-pulling every slice"); return pull_state(ds, st, fields, full=True)
        log(f"MISMATCH {ds} {st}: slices sum {got} != state total {total} — not marked done"); return
    json.dump({"n": total, "asof": str(ASOF_DATE), "at": str(datetime.datetime.now()), "secs": round(time.time() - t0)}, open(marker, "w"))
    log(f"DONE {ds} {st}: {total} records in {round(time.time() - t0)}s")

if __name__ == "__main__":   # pull_bulk.py imports the field lists, the as-of rule and the API helpers
    os.makedirs(RAW, exist_ok=True); states = sys.argv[1:] or STATES
    jobs =[("NfipPolicies", s, POL_FIELDS) for s in states] + [("NfipClaims", s, CLM_FIELDS) for s in states]
    log(f"start: {len(states)} states, {len(jobs)} state-datasets")
    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(lambda j: pull_state(*j), jobs))
    left = [f"{ds} {s}" for ds, s, _ in jobs if not os.path.exists(os.path.join(RAW, ds, s + ".done"))]
    log("ALL DONE" if not left else f"FINISHED WITH {len(left)} UNFINISHED: {left}")
    sys.exit(1 if left else 0)   # a partial pull must stop the refresh job before agg_raw writes half a country
