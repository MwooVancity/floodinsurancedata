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
import collections, datetime, html as H, json, os, re, sys
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
from agg_raw import NAMES as _SN, slug as _sslug
_SD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "states", _sslug(agg["state"])) \
    if agg.get("level") == "county" and agg.get("state") in _SN else ""
if _SD and os.path.exists(os.path.join(_SD, "agg.json")):   # county pages print the state's figure beside their own (q='state')
    ROOT_DATA["state"] = {f: json.load(open(os.path.join(_SD, f + ".json"))) for f in ("agg", "data", "extras") if os.path.exists(os.path.join(_SD, f + ".json"))}
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
_rest = re.sub(r'<span data-m="\w+"[^>]*>.*?</span>|<span data-name>.*?</span>|<(span|div) data-rule="\w+">.*?</\1>', " ", _rest, flags=re.S)
_rest = norm(re.sub(r"<[^>]+>", " ", _rest))
_rest = re.sub(r"\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(, \d{4})?\b", " ", _rest)
_free = [mm for mm in re.finditer(r"(?<![\w.])\$?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![\w])", _rest)
         if not re.fullmatch(r"(19[5-9]\d|20[0-3]\d)", mm.group(0))]          # a year is a label, not a figure
for mm in _free: fail("V1", f"untagged number '{mm.group(0)}' in: {_rest[max(0, mm.start() - 40):mm.end() + 20]}")
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
    if got is None or not isinstance(want, (int, float)) or abs(got - float(want)) > tol * (1 + 1e-9) + 1e-9:   # exactly half a unit rounds either way
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
for mm in re.finditer(r'<span data-m="(\w+)"', page):   # A6 words naming new policies sit only on a new-policy figure (hater r5:
    seg = re.split(r"[.!?]\s", norm(re.sub(r"<[^>]+>", " ", page[max(0, mm.start() - 200):mm.start()])))[-1]   # "a new one ... $1,466" was existing stock)
    if re.search(r"\bnew (?:single-family )?(?:policy|policies|one|buyers?)\b|\bbrand-new\b|\bfirst bought\b", seg, re.I) \
            and "past year" not in (MX.METRICS.get(mm.group(1), {}).get("basis") or ""):
        fail("A6", f"{mm.group(1)} is not a new-policy figure, but its sentence says: …{seg[-80:]}")
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
OUTSIDE = visible(skip_attrs=("data-claim", "data-rule", "data-name"))   # a place name ("Rising Sun") is not a claim
for w in MX.QUANT:
    hit = re.search(rf"\b{re.escape(w)}\b", OUTSIDE, re.I)
    if hit: fail("B2", f"'{w}' used without a checked claim: …{OUTSIDE[max(0, hit.start()-50):hit.end()+40]}…")
for _mm in re.finditer(r"\b(None|nan|NaN|undefined)\b(?!\s+(of|were|was|have|has|is|are)\b)", page):   # B3 a missing value printed as text
    fail("B3", f"missing value printed as '{_mm.group(1)}': …{page[max(0, _mm.start()-50):_mm.end()+20]}…")
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
        if "OpenFEMA API" in body: fail("A1", f"OpenFEMA credit repeated under the panel citing {keys} (it belongs once, in the footer)")
        if MX.needs_openfema_attr(ks): _needs_attr = True
    if not body.startswith(want): fail("A1", f"source line for [{keys}] reads '{body[:70]}', registry says '{want[:70]}'")
# C5 a chart draws the measure its caption names: claims-per-year bar heights are proportional to dollars paid
_bars = [(float(h), float(d.replace(",", ""))) for h, d in re.findall(r'height="([\d.]+)"[^>]*><title>\d{4}: [\d,]+ claims, \$([\d,]+)</title>', page)]
if _bars and max(d for _, d in _bars) > 0:
    _k = max(h for h, _ in _bars) / max(d for _, d in _bars)
    for h, d in _bars:
        if abs(h - d * _k) > 1.0: fail("C5", f"claims chart bar height {h} is not dollars ({d:,.0f}); the caption says bars are dollars"); break
# C7 the zone table's high-risk rows add to the high-risk share the card states (hater r1: VE/AH hid in "other")
_zt = re.search(r"<th>Flood zone</th><th>Policy units</th><th>Share</th></tr></thead><tbody>(.*?)</tbody>", page, re.S)
if _zt and P.get("sfha_share_units") is not None:
    _hr = sum(float(s) for lab, s in re.findall(r"<tr><td>([^<]*)</td><td>.*?</td><td><span[^>]*>([\d.]+)%</span></td></tr>", _zt.group(1))
              if "high-risk" in lab)
    if abs(_hr - P["sfha_share_units"]) > 0.3: fail("C7", f"zone table high-risk rows add to {_hr:.1f}%, page states {P['sfha_share_units']}%")
# C8 the unpaid-reasons table accounts for every unpaid claim (hater r1: 3 rows covered 45%)
_ut = re.search(r"<th>Reason recorded</th><th>Claims</th></tr></thead><tbody>(.*?)</tbody>", page, re.S)
if _ut and (EXTRAS.get("claims") or {}).get("unpaid_n"):
    _us = sum(int(x.replace(",", "")) for x in re.findall(r"<td><span[^>]*>([\d,]+)</span></td></tr>", _ut.group(1)))
    if _us != EXTRAS["claims"]["unpaid_n"]: fail("C8", f"unpaid-reasons rows add to {_us}, not the {EXTRAS['claims']['unpaid_n']} unpaid claims")
# E2 no sentence of 12+ words printed twice on one page (hater r1: rules repeated verbatim)
# keyed on each sentence's last 12 words: a tile value glued in front ("$100,000 Most homeowners...") must not hide a copy
_sent = collections.Counter(" ".join(s.split()[-12:]) for s in re.split(r"(?<=[.!?])\s+", TEXT) if len(s.split()) >= 12)
for _s, _c in _sent.items():
    if _c > 1: fail("E2", f"sentence printed {_c} times: {_s[:80]}"); break
# C9 every flood event the data holds (20+ paid claims) has its row: hater r6 found FEMA's catch-all "Flooding" and
# Louisiana's 1995 dropped without a word (mined from the reviews, 2026-10-28)
_et = re.search(r"<th>Flood \(FEMA's name\)</th>.*?<tbody>(.*?)</tbody>", page, re.S)
if _et:
    _shown = set(re.findall(r'data-p="extras\.claims\.events\.(\d+)\.claims"', _et.group(1)))
    for _i, _e in enumerate((EXTRAS.get("claims") or {}).get("events") or []):
        if (_e.get("claims") or 0) >= 20 and _e.get("years") and str(_i) not in _shown:
            fail("C9", f"flood event '{_e['name']}' ({_e['claims']} paid claims) is in the data but not in the events table")
# C6 CRS discounts under Risk Rating 2.0 are one rate for every zone: no separate "other areas" rate
if re.search(r"<th>Other areas</th>", page): fail("C6", "CRS table shows a separate non-high-risk discount (pre-2021 rule; Risk Rating 2.0 is one rate in every zone)")
_foot = re.search(r"<footer>(.*?)</footer>", page, re.S)
if globals().get("_needs_attr") and not (_foot and "OpenFEMA API, but is not endorsed by FEMA" in _foot.group(1)):
    fail("A1", "page shows OpenFEMA data but its footer lacks FEMA's required credit")
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
_sv = re.search(r"costliest flood FEMA named here was (.*?):", READ)
if _sv and not re.search(r"\(\d{4}(–\d{4})?\)", _sv.group(1)): fail("H5", f"storm named without its year: {_sv.group(1)[:50]}")
for y in re.findall(r"<li>(\d{4}) — ", page):
    if int(y) > datetime.date.today().year: fail("L10", f"declaration shows future year {y}")
# H8 a list a reader scans for their place is A to Z ignoring case (hater r6: "Jefferson Davis" before "Jefferson")
_lists = [re.findall(r"<tr><td>(?:<a [^>]*>)?([^<]+)", _ct.group(1))] if _ct else []
for _nd in re.finditer(r"<b>No CRS discount \([^)]*\):</b>(.*?)</p>", page, re.S):
    _lists.append(norm(re.sub(r"<[^>]+>", "", _nd.group(1))).rstrip(". ").split(";"))   # unescape first: "Hunter&#x27;s" holds a ";"
for _l in _lists:
    _l = [norm(x) for x in _l if norm(x)]
    _bad = next(((a, b) for a, b in zip(_l, _l[1:]) if a.casefold() > b.casefold()), None)
    if _bad: fail("H8", f"list not A to Z: '{_bad[0]}' before '{_bad[1]}'")
# H9 the structured data names the same dataset versions its citation links point to (hater r5-r9: "v3" text, "-v2" URLs)
for _ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
    _tv, _uv = set(re.findall(r"\b(?:NfipPolicies|NfipClaims) v(\d)\b", _ld)), set(re.findall(r"(?:policies|claims)-v(\d)\b", _ld))
    if _tv and _uv and _tv != _uv: fail("H9", f"structured data says dataset version v{'/v'.join(sorted(_tv))} but links v{'/v'.join(sorted(_uv))}")
# H11 "N in 10 homes" takes a plural verb (hater r9: "About 2 in 10 homes here has")
for _mm in re.finditer(r"\b(?:[2-9]|\d{2,}) in \d+ homes(?: here)? has\b", READ): fail("H11", f"plural count with 'has': {_mm.group(0)}")
if not agg.get("nri") and agg.get("level") != "state" and "Gap:" not in page: fail("L8", "NRI missing without a gap line")
if P.get("spread_ok", (P.get("cost_n") or 0) >= 100) != ("Annual NFIP cost spread" in page): fail("L9", "cost spread shown for a small cohort (or hidden for a large one)")
if P.get("sfha_units") is not None and units and "of all buildings" not in page: fail("L12", "SFHA share shown without its denominator disclosure")
if re.search(r"per 100\b", page, re.I) and not re.search(r"cumulative|not an annual rate", page, re.I): fail("L14", "a per-100 ratio without its caveat")
if P.get("frp_median") and money(P["frp_median"]) in page and not re.search(r"not a quote", page, re.I): fail("L16", "full-risk shown without a 'not a quote' caveat")

# H12/H13 every card states its limits and never claims past its data; a card whose data exists is on the page
# (tools/card_spec.py; hater r10: NOAA "all buildings" with coastal floods missing, a silently dropped storm)
from card_spec import CARDS as _CS
_secs = [(norm(re.sub(r"<[^>]+>", " ", t)), norm(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", b, flags=re.S))))
         for t, b in re.findall(r'<section class="card"[^>]*><h2>(.*?)</h2>(.*?)</section>', page, re.S)]
for _c in _CS:
    _hit = [b for t, b in _secs if re.search(_c["title"], t)]
    for _b in _hit:
        for _p in _c["must"]:
            if _p not in _b: fail("H12", f"card '{_c['title']}' does not state its limit: '{_p}'")
        for _p in _c["never"]:
            if _p.lower() in _b.lower(): fail("H12", f"card '{_c['title']}' claims past its data: '{_p}'")
    try: _want = _c["shown_when"](agg, data, EXTRAS)
    except Exception as _e: fail("H13", f"card '{_c['title']}' spec cannot read this page's data: {_e!r}"); continue
    if _want and not _hit: fail("H13", f"card '{_c['title']}' has data here but is not on the page")

# round 31: an average dragged up by one flood is true but misleading; when one event paid over half the money,
# the payout card must show the typical (median) claim and name that flood
_evp = [e.get("paid") or 0 for e in ((EXTRAS.get("claims") or {}).get("events") or [])]
_tot = (agg.get("claims") or {}).get("total_paid") or 0
if _evp and _tot and max(_evp) > 0.5 * _tot and (EXTRAS.get("claims") or {}).get("paid_building_median") \
        and 'data-m="avg_paid"' in page and "<b>Typical claim:</b>" not in page:
    fail("H17", "one flood paid over half of all claim dollars, but the average is shown without the typical claim (round 31: Sandy)")

# rounds 16-19 defect classes made checks (CLAUDE.md: every defect class becomes a check with a mutation)
if re.search(r"<td>Zone (B|C|X|D|A99|AH|AO|AR)\b", page) and 'data-rule="zone_codes"' not in page:
    fail("H14", "zone codes shown without the plain-words rule (round 16: B, C, A99, AH unexplained)")
for _ul in re.findall(r"<ul>(.*?)</ul>", page, re.S):
    _li = [norm(re.sub(r"<[^>]+>", " ", x)) for x in re.findall(r"<li>(.*?)</li>", _ul, re.S)]
    _dup = next((a for a, b in zip(_li, _li[1:]) if a and a == b), None)
    if _dup: fail("H15", f"the same list line twice in a row: '{_dup[:60]}' (round 16: identical disaster lines)")
_nn = re.search(r"Not in the NFIP \(.*?</b>", page, re.S)
if _nn:
    for _nm in re.findall(r"<span data-name>([^<]*(?:County|Parish|Borough))</span>(?! \(unincorporated area only\))", _nn.group(0)):
        fail("H16", f"'{_nm}' in the not-in-NFIP list without 'unincorporated area only' (round 16: Box Butte)")

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
