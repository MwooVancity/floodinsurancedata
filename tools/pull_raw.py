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
ASOF = "2026-07-31T00:00:00.000z"
STATES = ("DC WY SD AK MT VT ND NH NE UT ID NM KS NV IA ME WV OK OR CO KY AR RI MN WI TN IN MO MI AZ WA MS DE CT "
          "OH IL AL MD PA GA MA VA NC SC NY NJ CA LA TX FL").split()          # smallest first
POL_FIELDS = ("id propertyState censusGeoid reportedZipCode reportedCity nfipCommunityNumberCurrent ratedFloodZone floodZoneCurrent "
              "occupancyType primaryResidenceIndicator policyCount policyCost totalInsurancePremiumOfThePolicy fullRiskPremium "
              "federalPolicyFee hfiaaSurcharge reserveFundAssessment iccPremium crsClassCode buildingDeductibleCode contentsDeductibleCode "
              "totalBuildingInsuranceCoverage totalContentsInsuranceCoverage buildingReplacementCost elevatedBuildingIndicator "
              "elevationCertificateIndicator postFIRMConstructionIndicator preFIRMConstructionIndicator grandfatheringTypeCode "
              "mandatoryPurchaseFlag rateMethod originalNBDate policyEffectiveDate originalConstructionDate propertyPurchaseDate "
              "rentalPropertyIndicator tenantIndicator condominiumCoverageTypeCode numberOfFloorsInInsuredBuilding foundationType "
              "waitingPeriodType subsidizedRateType").split()
CLM_FIELDS = ("id state countyCode censusGeoid reportedZipCode yearOfLoss dateOfLoss floodEvent eventDesignationNumber causeOfDamage "
              "ratedFloodZone floodZoneCurrent occupancyType primaryResidenceIndicator policyCount netBuildingPaymentAmount "
              "netContentsPaymentAmount netIccPaymentAmount buildingDamageAmount contentsDamageAmount buildingPropertyValue "
              "totalBuildingInsuranceCoverage totalContentsInsuranceCoverage buildingDeductibleCode nonPaymentReasonBuilding "
              "nonPaymentReasonContents waterDepth floodWaterDuration elevatedBuildingIndicator postFIRMConstructionIndicator "
              "rateMethod originalNBDate crsClassCode nfipCommunityNumberCurrent").split()
LOCK = threading.Lock()
os.makedirs(RAW, exist_ok=True)
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
        base = f"propertyState eq '{st}' and policyEffectiveDate le '{ASOF}' and policyTerminationDate ge '{ASOF}'"
        out = [("pre2020", base + " and policyEffectiveDate lt '2020-01-01T00:00:00.000z'")]
        d = datetime.date(2020, 1, 1)
        while d <= datetime.date(2026, 7, 1):
            n = (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
            out.append((f"{d:%Y%m}", base + f" and policyEffectiveDate ge '{d}T00:00:00.000z' and policyEffectiveDate lt '{n}T00:00:00.000z'"))
            d = n
        return base, out
    base = f"state eq '{st}'"
    return base, [("noyear", base + " and yearOfLoss eq null")] + [(str(y), base + f" and yearOfLoss eq {y}") for y in range(1970, 2027)]

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

def pull_state(ds, st, fields):
    marker = os.path.join(RAW, ds, st + ".done")
    if os.path.exists(marker): log(f"{ds} {st} already done"); return
    base, parts = slices(ds, st)
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
        log(f"MISMATCH {ds} {st}: slices sum {got} != state total {total} — not marked done"); return
    json.dump({"n": total, "at": str(datetime.datetime.now()), "secs": round(time.time() - t0)}, open(marker, "w"))
    log(f"DONE {ds} {st}: {total} records in {round(time.time() - t0)}s")

states = sys.argv[1:] or STATES
jobs = [("NfipPolicies", s, POL_FIELDS) for s in states] + [("NfipClaims", s, CLM_FIELDS) for s in states]
log(f"start: {len(states)} states, {len(jobs)} state-datasets")
with ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(lambda j: pull_state(*j), jobs))
left = [f"{ds} {s}" for ds, s, _ in jobs if not os.path.exists(os.path.join(RAW, ds, s + ".done"))]
log("ALL DONE" if not left else f"FINISHED WITH {len(left)} UNFINISHED: {left}")
