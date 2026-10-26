"""THE gate for one built page ("is it true and readable?"). Exit 1 blocks ship.
Usage: python -I tools/gate.py <agg.json> <page.html> [official_count]
Seven questions; the phone (phone_check.py) and the live site (gate_live.py) are the other two. Every check id
below is proven by a mutation in tools/test_gate.py that reintroduces a real shipped defect and must fail here.
  1 INPUTS    is the data complete and on the right basis?
  2 NUMBERS   is every number on the page tagged, and equal to the data it names?        (V1, V2: the core)
  3 MEANING   does each number carry the right noun and basis, and do panels agree?
  4 WORDS     do words that carry direction or size agree with the numbers?
  5 SOURCES   is every source line, dataset list and rule text generated and current?
  6 READER    names not codes, no jargon or dead pointers, storms dated, caveats present
  7 ANSWER    does every card open with a short answer?"""
import datetime, html as H, json, os, re, sys
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as MX
from rules_registry import RULES

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # a failure quoting "→" must print, not crash the gate
agg_path, html_path = sys.argv[1], sys.argv[2]
official = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.dirname(os.path.abspath(agg_path))
agg = json.load(open(agg_path))
data = json.load(open(os.path.join(DIR, "data.json"))) if os.path.exists(os.path.join(DIR, "data.json")) else {}
EXTRAS = json.load(open(os.path.join(DIR, "extras.json"))) if os.path.exists(os.path.join(DIR, "extras.json")) else {}
if not EXTRAS:   # county pages: extras live in data/all-counties/<geoid>.json
    try:
        _g = next(p["geoid"] for p in json.load(open(os.path.join(ROOT, "places.json"))) if p["slug"] == os.path.basename(DIR))
        EXTRAS = json.load(open(os.path.join(ROOT, "data", "all-counties", _g + ".json"))).get("extras") or {}
    except Exception: EXTRAS = {}
page = open(html_path, encoding="utf-8").read()
P, C = agg.get("policies", {}), agg.get("claims", {})
VALS = MX.values(agg, data)
fails = []
def fail(cid, msg): fails.append(f"[{cid}] {msg}")
def money(n): return "$" + format(int(round(n)), ",")
def norm(s): return re.sub(r"\s+", " ", H.unescape(s)).strip()

class Visible(HTMLParser):
    """Visible body text, optionally skipping elements carrying the given attributes."""
    SKIP = {"script", "style", "svg", "head"}
    VOID = ("br", "img", "input", "meta", "link")
    def __init__(self, skip_attrs=()):
        super().__init__(convert_charrefs=True); self.skip_attrs, self.stack, self.out = skip_attrs, [], []
    def handle_starttag(self, tag, attrs):
        if tag in self.VOID: return
        self.stack.append(tag in self.SKIP or any(a in dict(attrs) for a in self.skip_attrs) or (self.stack[-1] if self.stack else False))
    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack: self.stack.pop()
    def handle_data(self, d):
        if not (self.stack and self.stack[-1]): self.out.append(d)
def visible(skip_attrs=()):
    v = Visible(skip_attrs); v.feed(page); return norm(" ".join(v.out))
TEXT = visible()
READ = norm(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.S)))   # chart labels included
SPANS3 = re.findall(r'<span data-m="(\w+)"((?: data-[qp]="[^"]*")*)>(.*?)</span>', page)
units = P.get("units") or 0

# ---------------- 1 INPUTS ----------------
mani = agg.get("manifest", {})
if not mani: fail("L1", "no manifest")
for k, v in mani.items():
    if not v.get("complete"): fail("L1", f"{k} incomplete: {v.get('unique_fetched')}/{v.get('reported_total')} (missing {v.get('missing')})")
for k in ("units", "p25", "p50", "p75", "frp_median", "share_below", "zone_units", "sfha_share_units"):
    if P.get(k) in (None, "", {}): fail("L2", f"policies.{k} missing")
for k in ("rows", "total_paid", "by_year", "year_min", "year_max"):
    if C.get(k) in (None, "", {}): fail("L2", f"claims.{k} missing")
pv = [P.get(k) for k in ("p25", "p50", "p75", "p90") if P.get(k) is not None]
if pv != sorted(pv): fail("L3", f"percentiles not monotonic: {pv}")
if official and units and abs(units - official) / official * 100 > 5:
    fail("L4", f"reconciliation {abs(units - official) / official * 100:.1f}% > 5% (units {units} vs official {official})")
if P.get("frp_median") and P.get("gap_basis") != "premium":
    fail("L17", "full-risk gap not on the premium basis (run tools/collect_premium_gap.py)")

# ---------------- 2 NUMBERS: every number tagged (V1) and equal to the data it names (V2) ----------------
ROOT_DATA = dict(agg, data=data, extras=EXTRAS, const=MX.CONST)
def _resolve(path):
    v = ROOT_DATA
    for seg in path.split("."):
        v = v[int(seg)] if isinstance(v, list) else v[seg]
    return v
def _parse(shown):
    t = norm(re.sub(r"<[^>]+>", "", shown)).replace("$", "").replace(",", "").replace("%", "")
    mm = re.match(r"(-?\d+(?:\.(\d+))?)\s*(million|billion)?", t)
    if not mm: return None, None
    mult = {"million": 1e6, "billion": 1e9}.get(mm.group(3), 1)
    return float(mm.group(1)) * mult, 0.5 * 10 ** -len(mm.group(2) or "") * mult
_rest = re.sub(r"<(script|style|head|title)\b.*?</\1>", " ", page, flags=re.S)
_rest = re.sub(r'<p class="src".*?</p>|<ul class="srclist">.*?</ul>|<footer.*?</footer>', " ", _rest, flags=re.S)
_rest = re.sub(r'<span data-m="\w+"[^>]*>.*?</span>|<(span|div) data-rule="\w+">.*?</\1>', " ", _rest, flags=re.S)
_rest = norm(re.sub(r"<[^>]+>", " ", _rest))
_rest = re.sub(r"\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(, \d{4})?\b", " ", _rest)
_free = [mm for mm in re.finditer(r"(?<![\w.])\$?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![\w])", _rest)
         if not re.fullmatch(r"(19[5-9]\d|20[0-3]\d)", mm.group(0))]          # a year is a label, not a figure
_show = len(_free) if os.environ.get("GATE_ALL") else 8
for mm in _free[:_show]: fail("V1", f"untagged number '{mm.group(0)}' in: {_rest[max(0, mm.start() - 40):mm.end() + 20]}")
if len(_free) > _show: fail("V1", f"... and {len(_free) - _show} more untagged numbers")
seen = {}
for k, attrs, shown in SPANS3:
    if k not in MX.METRICS: fail("A0", f"figure tagged with unknown metric {k}")
    q = re.search(r'data-q="([^"]*)"', attrs); kk = (k, q.group(1) if q else None); s_ = norm(re.sub(r"<[^>]+>", "", shown))
    if kk in seen and seen[kk] != s_: fail("A3", f"{k}{'[' + kk[1] + ']' if kk[1] else ''} shown as both '{seen[kk]}' and '{s_}'")
    seen.setdefault(kk, s_)
    pm = re.search(r'data-p="([^"]+)"', attrs)
    if not pm: continue
    try: want = _resolve(pm.group(1))
    except (KeyError, IndexError, TypeError, ValueError): fail("V2", f"{k}: path {pm.group(1)} not in the data"); continue
    got, tol = _parse(shown)
    if isinstance(want, str): want = _parse(want)[0]   # FEMA stores some rates as text ("20%")
    if got is None or not isinstance(want, (int, float)) or abs(got - float(want)) > tol + 1e-9:
        fail("V2", f"{k} shows '{s_}' but {pm.group(1)} = {want}")
for _k, _ds in (("records_policies", "policies"), ("records_claims", "claims")):   # the full download is stated
    _mm = mani.get(_ds) or {}
    if _mm.get("complete") and not _mm.get("missing") and f'data-m="{_k}"' not in page: fail("G1", f"complete {_ds} download not stated on the page")

# ---------------- 3 MEANING ----------------
tiles = dict((k, lab) for lab, k in re.findall(r'<li><b>([^<]*)</b><span><span data-m="(\w+)"[^>]*>', page))
for mm in re.finditer(r'<span data-m="(\w+)"([^>]*)>([^<]*)</span>([^<]{0,60})', page):   # A2 a count is named by its noun
    k, attrs, shown, after = mm.groups()
    need = MX.NOUN_REQUIRED.get(MX.METRICS.get(k, {}).get("counts"))
    if not need or "data-q=" in attrs: continue    # a table cell: its column header names the noun
    in_tile = page[max(0, mm.start() - 12): mm.start()].endswith("<span>") and k in tiles
    words = tiles[k] if in_tile else " ".join(after.split()[:3])
    if not re.search(rf"\b({need})\b", words, re.I): fail("A2", f"{k} ({shown}) named '{words.strip()[:40]}', needs {need}")
for mm in re.finditer(r'<span data-m="(\w+)"[^>]*>', page):   # A4 a figure with a named basis sits next to that basis
    basis = MX.METRICS.get(mm.group(1), {}).get("basis")
    if not basis or basis == "rating": continue
    if basis not in norm(re.sub(r"<[^>]+>", " ", page[max(0, mm.start() - 260): mm.end() + 260])).lower():
        fail("A4", f"{mm.group(1)} shown without naming its basis '{basis}'")
cx = data.get("claims_extra") or {}
if VALS["claims_paid_n"] is not None and VALS["claims_filed"] is not None and VALS["claims_paid_n"] > VALS["claims_filed"]:
    fail("C1", f"claims paid {VALS['claims_paid_n']} > claims filed {VALS['claims_filed']}")
if cx.get("claims") and cx.get("paid_n") is not None and cx.get("cwop_share") is not None \
        and abs(cx["paid_n"] - cx["claims"] * (100 - cx["cwop_share"]) / 100) > max(1, 0.002 * cx["claims"]):
    fail("C2", f"paid {cx['paid_n']} + closed-without-payment {cx['cwop_share']}% != {cx['claims']} filed")
for n in re.findall(r"([\d,]+) paid (?:NFIP )?(?:flood )?claims", TEXT, re.I):
    if VALS["claims_paid_n"] is None or int(n.replace(",", "")) != VALS["claims_paid_n"]:
        fail("C3", f"'{n} paid claims' on the page, but {VALS['claims_paid_n']} claims paid")
req = re.search(r'id="required".*?<tbody>(.*?)</tbody>', page, re.S)
if req and units:
    tot = sum(int(x.replace(",", "")) for x in re.findall(r"<tr><td>[^<]*</td><td>(?:<span[^>]*>)?([\d,]+)(?:</span>)?</td>", req.group(1)))
    if tot != units: fail("C4", f"zone table rows sum to {tot}, not the {units} units shown")

# ---------------- 4 WORDS agree with the numbers ----------------
for attr, body in re.findall(r'<span data-claim="([^"]*)">(.*?)</span>', page, re.S):
    c = json.loads(H.unescape(attr))
    if not re.search(rf"\b{re.escape(c['word'])}\b", norm(re.sub(r'<[^>]+>', '', body)), re.I): fail("B1", f"claim word '{c['word']}' not in its sentence")
    if not MX.holds(c["cond"], VALS): fail("B1", f"claim '{c['word']}' is false: {c['cond']} with {VALS.get(c['cond'][0])}")
OUTSIDE = visible(skip_attrs=("data-claim", "data-rule"))
for w in MX.QUANT:
    hit = re.search(rf"\b{re.escape(w)}\b", OUTSIDE, re.I)
    if hit: fail("B2", f"'{w}' used without a checked claim: …{OUTSIDE[max(0, hit.start()-50):hit.end()+40]}…")
for _mm in re.finditer(r"(\d+(?:\.\d+)?)%(.{0,40})", READ):   # H6 a share is never over 100% unless explained
    if float(_mm.group(1)) > 100 and not re.match(r"\s*(above|below|more|higher|lower|difference)", _mm.group(2)) \
            and "exact share is unknown" not in _mm.group(2) + READ[_mm.end():_mm.end() + 120]:
        fail("H6", f"share over 100%: {_mm.group(0)[:60]}")
for _a, _b, _p in re.findall(r"About (\d+) in (\d+) homes[^(]{0,40}\((\d+(?:\.\d+)?)%\)", READ):   # H7 "N in 10" matches its %
    _a, _b, _p = int(_a), int(_b), float(_p)
    ok = (abs(10 * _a - _p) <= 5) if _b == 10 else (_a == 1 and _p < 15 and round(100 / _p) == _b) if _p else False   # "1 in N" only under 15%
    if not ok: fail("H7", f"'{_a} in {_b}' beside {_p}%")

# ---------------- 5 SOURCES and RULES ----------------
for tag in re.findall(r'<p class="src"[^>]*>', page):
    if "data-src=" not in tag: fail("A1", "a source line was typed by hand (no data-src)")
for keys, body in re.findall(r'<p class="src" data-src="([^"]*)">(.*?)</p>', page, re.S):
    body = norm(re.sub(r"<[^>]+>", "", body))
    if keys.startswith("rule:"):
        hosts = []
        for rk in keys[5:].split(","):
            for u, _, _ in RULES.get(rk, {"sources": []})["sources"]:
                h = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
                if h not in hosts: hosts.append(h)
        want = "Source: " + ", ".join(hosts)
    else:
        ks = keys.split(","); want = "Source: " + "; ".join(MX.sources_for(ks))
        if MX.needs_openfema_attr(ks) != ("OpenFEMA API" in body): fail("A1", f"OpenFEMA attribution wrong for a panel citing {keys}")
    if not body.startswith(want): fail("A1", f"source line for [{keys}] reads '{body[:70]}', registry says '{want[:70]}'")
for _e, _r in re.findall(r"Data effective ([A-Z][a-z]+ \d{1,2}, \d{4}); retrieved ([A-Z][a-z]+ \d{1,2}, \d{4})", READ):
    if _e == _r: fail("H4", f"data effective date is only the retrieval day ({_e})")
blk = re.search(r'srclist">(.*?)</ul>', page, re.S)
if not blk: fail("L13", "no visible federal-sources block on page")
else:
    n_listed = len(re.findall(r"<li>", blk.group(1)))
    mj = re.search(r'joins\s+(?:<span[^>]*>)?(\d+)', page)
    if mj and int(mj.group(1)) != n_listed: fail("L13", f"stated dataset count {mj.group(1)} != {n_listed} listed")
    cited = []
    for keys in re.findall(r'data-src="([^"]*)"', page):
        if not keys.startswith("rule:"):
            for d in MX.sources_for(keys.split(",")):
                if d not in cited: cited.append(d)
    listed = [norm(x) for x in re.findall(r"<li><a [^>]*>(.*?)</a></li>", blk.group(1))]
    if sorted(listed) != sorted(cited): fail("A5", f"sources block lists {sorted(set(listed) ^ set(cited))} that no panel cites (or misses one)")
RULE_RE = r'<(span|div) data-rule="(\w+)">(.*?)</\1>(?=\s|<|$)'
for tag, key, body in re.findall(RULE_RE, page, re.S):
    if key not in RULES: fail("E1", f"unknown rule {key}")
    elif norm(body) != norm(RULES[key]["text"]): fail("E1", f"rule {key} text differs from the registry")
if len(re.findall(r"data-rule=", page)) != len(re.findall(RULE_RE, page, re.S)): fail("E1", "a data-rule element could not be matched to its closing tag")

# ---------------- 6 READER words ----------------
_ct = re.search(r'id="counties".*?<tbody>(.*?)</tbody>', page, re.S)
for _c in (re.findall(r"<tr><td>(.*?)</td>", _ct.group(1)) if _ct else []):
    if re.fullmatch(r"\d{5}", re.sub(r"<[^>]+>", "", _c).strip()): fail("H1", f"county shown as a code: {_c}")
if re.search(r"Each (county|parish|borough) page lists|Open a county below", READ) \
        and not re.search(r'<a href="\.\./[a-z0-9-]+-(county|parish|borough|city)-[a-z]{2}/"', page):
    fail("H2", "points the reader to county pages, but links none")
for _j in re.findall(r"\b(p25|p75|p90|policyCount|policyCost|censusGeoid|ratedFloodZone|fullRiskPremium)\b", READ): fail("H3", f"jargon '{_j}' in reader text")
_sv = re.search(r"costliest single flood here was (.*?):", READ)
if _sv and not re.search(r"\(\d{4}(–\d{4})?\)", _sv.group(1)): fail("H5", f"storm named without its year: {_sv.group(1)[:50]}")
if re.search(r">\s*(None|nan|NaN|undefined)\s*<", page) or "$None" in page or "None%" in page: fail("L7", "None/nan leaked into the page")
for y in re.findall(r"<li>(\d{4}) — ", page):
    if int(y) > datetime.date.today().year: fail("L10", f"declaration shows future year {y}")
if not agg.get("nri") and agg.get("level") != "state" and "Gap:" not in page: fail("L8", "NRI missing without a gap line")
if P.get("spread_ok", (P.get("cost_n") or 0) >= 100) != ("Annual NFIP cost spread" in page): fail("L9", "cost spread shown for a small cohort (or hidden for a large one)")
if P.get("sfha_units") is not None and units and "of all buildings" not in page: fail("L12", "SFHA share shown without its denominator disclosure")
if re.search(r"per 100\b", page, re.I) and not re.search(r"cumulative|not an annual rate", page, re.I): fail("L14", "a per-100 ratio without its caveat")
if P.get("frp_median") and money(P["frp_median"]) in page and not re.search(r"not a quote", page, re.I): fail("L16", "full-risk shown without a 'not a quote' caveat")

# ---------------- 7 ANSWER first ----------------
for stand in re.findall(r'<p class="stand">(.*?)</p>', page, re.S):
    words = norm(re.sub(r"<[^>]+>", " ", stand)).split()
    if len(words) > 40: fail("F1", f"card opening is {len(words)} words (max 40): '{' '.join(words[:12])}…'")

if fails:
    print("GATE FAIL:")
    for f in fails: print("  -", f)
    sys.exit(1)
print("GATE PASS:", html_path, f"(units {units}, median {money(P['p50'])}, reconc "
      + (f"{abs(units - official) / official * 100:.1f}%" if official else "n/a") + ")")
