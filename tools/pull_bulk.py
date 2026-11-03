"""FEMA's bulk files instead of ~4,000 API pages (owner 2026-11-03; today's 3 failed refreshes were API 503s).
Downloads NfipPoliciesV3.parquet (3.7 GB) and NfipClaimsV3.parquet (164 MB) with curl (FEMA's file server refuses Python's
HTTP client), keeps policies in force on the as-of date, and writes the same .cache/raw/<ds>/<ST>/ files and .done markers
pull_raw.py writes, so agg_raw and extras_raw are unchanged. Fails closed (exit 1, nothing marked done) unless:
  1. each file's Last-Modified day equals the dataset's lastDataSetRefresh (file and API are the same snapshot);
  2. the bytes on disk equal the server's size, and a resumed download kept the same ETag (never two versions spliced);
  3. every required column exists and geoid/ZIP columns are text (numbers would drop the leading zero of states 01-09);
  4. ids are unique, and each state's row count equals FEMA's own API count for the same filter;
  5. oracle: DC pulled through the API matches the bulk rows field by field.
Usage: python -I tools/pull_bulk.py [--keep]   (--keep leaves the parquet files; default deletes them, nothing piles up)"""
import csv, datetime, decimal, gzip, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pull_raw as PR   # field lists, as-of, API count/get, log
import pyarrow.dataset as pds, pyarrow.compute as pc, pyarrow as pa

BULK = os.path.join(PR.ROOT, ".cache", "bulk"); os.makedirs(BULK, exist_ok=True)
SRC = {"NfipPolicies": ("NfipPoliciesV3.parquet", "propertyState", PR.POL_FIELDS),
       "NfipClaims": ("NfipClaimsV3.parquet", "state", PR.CLM_FIELDS)}
TEXT = ("censusGeoid", "reportedZipCode", "countyCode", "nfipCommunityNumberCurrent")
URL = "https://www.fema.gov/about/reports-and-data/openfema/v3/"

def fmt(v):   # the text pull_raw's csv gets from the API's JSON for the same value
    if v is None: return ""
    if isinstance(v, bool): return "True" if v else "False"
    if isinstance(v, datetime.date): return f"{v}T00:00:00.000Z"
    if isinstance(v, decimal.Decimal): return str(int(v)) if v == v.to_integral_value() else repr(float(v))
    return str(v)

def head(url):
    h = subprocess.run(["curl", "-s", "-r", "0-0", "-D", "-", "-o", os.devnull, url], capture_output=True, text=True, check=True).stdout
    g = {l.split(":", 1)[0].strip().lower(): l.split(":", 1)[1].strip() for l in h.splitlines() if ":" in l}
    lm = datetime.datetime.strptime(g["last-modified"], "%a, %d %b %Y %H:%M:%S GMT").date()
    return int(g["content-range"].split("/")[1]), g.get("etag", ""), lm

def fema_refresh(name):
    r = PR.get("https://www.fema.gov/api/open/v1/DataSets?$select=name,lastDataSetRefresh&$filter=name%20eq%20%27" + name + "%27")
    return datetime.date.fromisoformat(r["DataSets"][0]["lastDataSetRefresh"][:10])

def download(ds):
    fn = SRC[ds][0]; url = URL + fn; path = os.path.join(BULK, fn); tag = path + ".etag"
    size, etag, lm = head(url)
    if lm != fema_refresh(ds): sys.exit(f"STOP {ds}: file dated {lm}, API dataset refreshed {fema_refresh(ds)}: not the same snapshot")
    if os.path.exists(path) and (not os.path.exists(tag) or open(tag).read() != etag): os.remove(path)   # never splice two versions
    open(tag, "w").write(etag)
    for i in range(4):
        subprocess.run(["curl", "-s", "-f", "-C", "-", "--retry", "5", "--retry-all-errors", "-o", path, url])
        if os.path.exists(path) and os.path.getsize(path) == size: break
        time.sleep(60 * (i + 1))
    if not os.path.exists(path) or os.path.getsize(path) != size or head(url)[1] != etag:
        sys.exit(f"STOP {ds}: {os.path.getsize(path) if os.path.exists(path) else 0} of {size} bytes, or FEMA replaced the file mid-download")
    PR.log(f"{fn}: {size:,} bytes, file {lm}"); return path

def convert(ds, path):
    fn, stcol, fields = SRC[ds]
    d = pds.dataset(path, format="parquet"); names = set(d.schema.names)
    miss = [f for f in fields if f not in names]
    if miss: sys.exit(f"STOP {ds}: columns missing from the bulk file: {miss}")
    bad = [f for f in TEXT if f in fields and not pa.types.is_string(d.schema.field(f).type)]
    if bad: sys.exit(f"STOP {ds}: {bad} are not text in the bulk file (leading zeros would be lost)")
    filt = None
    if ds == "NfipPolicies":   # same filter as the API pull: effective on or before as-of, terminating after it
        a = pa.scalar(PR.ASOF_DATE, pa.date32())
        filt = (pc.field("policyEffectiveDate") <= a) & (pc.field("policyTerminationDate") > a)
    out, ids, n = {}, {}, {}
    for st in PR.STATES:
        sd = os.path.join(PR.RAW, ds, st); os.makedirs(sd, exist_ok=True)
        for f in os.listdir(sd): os.remove(os.path.join(sd, f))   # one file per state replaces the API's slices
        fh = gzip.open(os.path.join(sd, "bulk.csv.gz"), "wt", encoding="utf-8", newline="")
        out[st] = (fh, csv.writer(fh)); out[st][1].writerow(fields); ids[st] = set(); n[st] = 0
        if os.path.exists(os.path.join(PR.RAW, ds, st + ".done")): os.remove(os.path.join(PR.RAW, ds, st + ".done"))
    for b in d.to_batches(columns=fields, filter=filt, batch_size=200_000):
        for r in b.to_pylist():
            st = r[stcol]
            if st not in out: continue   # territories: not on the site
            if r["id"] in ids[st]: sys.exit(f"STOP {ds} {st}: id {r['id']} twice in the bulk file")
            ids[st].add(r["id"]); n[st] += 1
            out[st][1].writerow([fmt(r[f]) for f in fields])
    for st, (fh, _) in out.items(): fh.close()
    return n

def api_filter(ds, st): return PR.slices(ds, st)[0]

def oracle(ds, st="DC"):   # the API's own rows for one small state must equal the bulk rows, field by field
    fields = SRC[ds][2]; base = api_filter(ds, st); total = PR.count(ds, base)
    api, skip = {}, 0
    while len(api) < total:
        page = PR.get(PR.q(ds, {"$filter": base, "$select": ",".join(fields), "$top": 1000, "$skip": skip}))
        got = page[[k for k in page if k != "metadata"][0]]
        if not got: break
        for r in got: api[str(r["id"])] = r
        skip += 1000
    bulk = {r["id"]: r for r in csv.DictReader(gzip.open(os.path.join(PR.RAW, ds, st, "bulk.csv.gz"), "rt", encoding="utf-8"))}
    if set(api) != set(bulk): sys.exit(f"STOP oracle {ds} {st}: {len(set(api) - set(bulk))} API-only ids, {len(set(bulk) - set(api))} bulk-only ids")
    def same(a, b):
        a = "" if a is None else ("True" if a is True else "False" if a is False else str(a))
        if a == b: return True
        try: return float(a) == float(b)
        except ValueError: return False
    diff = [(i, f, api[i].get(f), bulk[i][f]) for i in api for f in fields if not same(api[i].get(f), bulk[i][f])]
    if diff: sys.exit(f"STOP oracle {ds} {st}: {len(diff)} fields differ, e.g. {diff[:3]}")
    PR.log(f"oracle {ds} {st}: {len(api)} rows identical to the API")

if __name__ == "__main__":
    t0 = time.time()
    for ds in SRC:
        path = download(ds); n = convert(ds, path)
        for st in PR.STATES:   # FEMA's count for the same filter; a short or long state never gets a .done marker
            want = PR.count(ds, api_filter(ds, st))
            if n[st] != want: sys.exit(f"STOP {ds} {st}: bulk rows {n[st]} != FEMA count {want}")
        oracle(ds)
        for st in PR.STATES:
            for nm in ("bulk",):
                json.dump({"n": n[st], "at": str(datetime.datetime.now())}, open(os.path.join(PR.RAW, ds, st, nm + ".done"), "w"))
            json.dump({"n": n[st], "asof": str(PR.ASOF_DATE), "at": str(datetime.datetime.now()), "secs": round(time.time() - t0), "source": "bulk"},
                      open(os.path.join(PR.RAW, ds, st + ".done"), "w"))
        PR.log(f"DONE {ds} bulk: {sum(n.values()):,} rows, 51 states match FEMA's counts")
        if "--keep" not in sys.argv: os.remove(path)
    PR.log(f"ALL DONE (bulk) in {round(time.time() - t0)}s")
