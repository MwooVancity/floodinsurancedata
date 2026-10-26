"""Gate 2 ("it is true") for one built county page. Exit 1 blocks ship.
Usage: python -I tools/gate.py <agg.json> <page.html> [official_count]
Every failure is tagged [id]. tools/test_gate.py reintroduces each known bug and proves its id fails.
Layers (docs/GATE-PROMPT.md): A metric registry (sources, labels, repeats, bases), B claims (direction and
majority words), C invariants (panels agree with each other), E rules registry (law and program text).
The legacy checks (L*) are kept only where the mutation suite shows they guard something A-E does not."""
import datetime, html as H, json, os, re, sys
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as MX
from rules_registry import RULES

agg_path, html_path = sys.argv[1], sys.argv[2]
official = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 0
agg = json.load(open(agg_path))
_dp = os.path.join(os.path.dirname(os.path.abspath(agg_path)), "data.json")
data = json.load(open(_dp)) if os.path.exists(_dp) else {}
page = open(html_path, encoding="utf-8").read()
P, C = agg.get("policies", {}), agg.get("claims", {})
VALS = MX.values(agg, data)
fails = []
def fail(cid, msg): fails.append(f"[{cid}] {msg}")
def money(n): return "$" + format(int(round(n)), ",")
def norm(s): return re.sub(r"\s+", " ", H.unescape(s)).strip()


class Visible(HTMLParser):
    """Visible body text; optionally skipping everything inside elements carrying the given attributes."""
    SKIP_TAGS = {"script", "style", "svg", "head"}
    def __init__(self, skip_attrs=()):
        super().__init__(convert_charrefs=True); self.skip_attrs, self.stack, self.out = skip_attrs, [], []
    def handle_starttag(self, tag, attrs):
        hide = tag in self.SKIP_TAGS or any(a in dict(attrs) for a in self.skip_attrs)
        if tag in ("br", "img", "input", "meta", "link"): return
        self.stack.append(hide or (self.stack[-1] if self.stack else False))
    def handle_endtag(self, tag):
        if tag in ("br", "img", "input", "meta", "link"): return
        if self.stack: self.stack.pop()
    def handle_data(self, d):
        if not (self.stack and self.stack[-1]): self.out.append(d)
def visible(skip_attrs=()):
    v = Visible(skip_attrs); v.feed(page); return norm(" ".join(v.out))
TEXT = visible()

# ---------------- legacy checks (L) ----------------
mani = agg.get("manifest", {})
if not mani: fail("L1", "no manifest")
for k, v in mani.items():
    if not v.get("complete"):
        fail("L1", f"{k} incomplete: {v.get('unique_fetched')}/{v.get('reported_total')} (missing {v.get('missing')})")
for k in ("units", "p25", "p50", "p75", "frp_median", "share_below", "zone_units", "sfha_share_units"):
    if P.get(k) in (None, "", {}): fail("L2", f"policies.{k} missing")
for k in ("rows", "total_paid", "by_year", "year_min", "year_max"):
    if C.get(k) in (None, "", {}): fail("L2", f"claims.{k} missing")
pv = [P.get(k) for k in ("p25", "p50", "p75", "p90") if P.get(k) is not None]
if pv != sorted(pv): fail("L3", f"percentiles not monotonic: {pv}")
if official and P.get("units"):
    diff = abs(P["units"] - official) / official * 100
    if diff > 5: fail("L4", f"reconciliation {diff:.1f}% > 5% (units {P['units']} vs official {official})")
if P.get("p50") and money(P["p50"]) not in page: fail("L5", f"median {money(P['p50'])} not on page")
# (L6 "OpenFEMA appears somewhere" deleted 2026-10-25: A1 checks each panel's attribution; mutation proves it.)
if re.search(r">\s*(None|nan|NaN|undefined)\s*<", page) or "$None" in page or "None%" in page:
    fail("L7", "None/nan leaked into the page")
if not agg.get("nri") and "Gap:" not in page: fail("L8", "NRI missing without a gap line")
cn = P.get("cost_n") or 0
spread_ok = P.get("spread_ok", cn >= 100); has_spread = "Annual NFIP cost spread" in page
if spread_ok != has_spread: fail("L9", f"spread chart shown={has_spread} but spread_ok={spread_ok} (cost_n {cn})")
for y in re.findall(r"<li>(\d{4}) — ", page):
    if int(y) > datetime.date.today().year: fail("L10", f"declaration shows future year {y}")
units = P.get("units") or 0; sfha = P.get("sfha_units")
if units and sfha is not None:
    if P.get("sfha_share_units") != round(100 * sfha / units, 1): fail("L11", "sfha_share_units != sfha_units/units")
    if f"{P.get('sfha_share_units')}%" not in page: fail("L11", "SFHA share not shown on page")
    if "of all buildings" not in page: fail("L12", "SFHA share shown without its denominator disclosure")
    # (truncated-zone-list check deleted 2026-10-25: C4 sums the rendered zone table to the unit total.)
blk = re.search(r'srclist">(.*?)</ul>', page, re.S)
if not blk: fail("L13", "no visible federal-sources block on page")
else:
    n_listed = len(re.findall(r"<li>", blk.group(1)))
    mj = re.search(r"joins\s+(\d+)\s+of them", page)
    if mj and int(mj.group(1)) != n_listed: fail("L13", f"stated dataset count {mj.group(1)} != {n_listed} listed")
if re.search(r"per 100", page, re.I) and not re.search(r"cumulative|not an annual rate", page, re.I):
    fail("L14", "a per-100 ratio without its 'cumulative, not an annual rate' caveat")
tp = C.get("total_paid")
if tp and money(tp) not in page: fail("L15", f"claims total {money(tp)} not on page")
by = C.get("by_year") or {}
if by:
    ty, (tc, typaid) = max(by.items(), key=lambda kv: kv[1][1])
    if money(typaid) not in page: fail("L15", f"largest loss year {ty} not reconciled on page")
if P.get("frp_median") and money(P["frp_median"]) in page and not re.search(r"not a quote", page, re.I):
    fail("L16", "full-risk shown without a 'not a quote' caveat")
if P.get("frp_median") and P.get("gap_basis") != "premium":
    fail("L17", "full-risk gap not on the premium basis (run tools/collect_premium_gap.py)")
if '"dateModified"' not in page: fail("L18", "no dateModified in schema")

# ---------------- A. metric registry ----------------
SPANS = re.findall(r'<span data-m="(\w+)">(.*?)</span>', page)
for k, _ in SPANS:
    if k not in MX.METRICS: fail("A0", f"figure tagged with unknown metric {k}")
# A1 every source line is generated from the metrics it shows; never hand-typed, never mis-attributed
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
        ks = keys.split(",")
        want = "Source: " + "; ".join(MX.sources_for(ks))
        if MX.needs_openfema_attr(ks) != ("OpenFEMA API" in body):
            fail("A1", f"OpenFEMA attribution wrong for a panel citing {keys}")
    if not body.startswith(want):
        fail("A1", f"source line for [{keys}] reads '{body[:70]}', registry says '{want[:70]}'")
# A2 a count is named by the noun for what it counts (an IA damage record is a record, never "homes"):
# inline, within the 3 words after the number; in a tile, in its label.
tiles = dict((k, lab) for lab, k in re.findall(r'<li><b>([^<]*)</b><span><span data-m="(\w+)">', page))
for mm in re.finditer(r'<span data-m="(\w+)">([^<]*)</span>([^<]{0,60})', page):
    k, shown, after = mm.groups()
    need = MX.NOUN_REQUIRED.get(MX.METRICS.get(k, {}).get("counts"))
    if not need: continue
    in_tile = page[max(0, mm.start() - 12): mm.start()].endswith("<span>") and k in tiles
    words = tiles[k] if in_tile else " ".join(after.split()[:3])
    if not re.search(rf"\b({need})\b", words, re.I): fail("A2", f"{k} ({shown}) named '{words.strip()[:40]}', needs {need}")
# A3 one figure, one value: every appearance of a metric shows the same number
seen = {}
for k, shown in SPANS:
    s = norm(re.sub(r"<[^>]+>", "", shown))
    if k in seen and seen[k] != s: fail("A3", f"{k} shown as both '{seen[k]}' and '{s}'")
    seen.setdefault(k, s)
# A4 a figure with a named basis sits next to that basis (rating vs expected-loss percentile)
for mm in re.finditer(r'<span data-m="(\w+)">', page):
    basis = MX.METRICS.get(mm.group(1), {}).get("basis")
    if not basis or basis == "rating": continue
    around = norm(re.sub(r"<[^>]+>", " ", page[max(0, mm.start() - 260): mm.end() + 260])).lower()
    if basis not in around: fail("A4", f"{mm.group(1)} shown without naming its basis '{basis}'")
# A5 the page's dataset list is exactly the datasets its panels cite
if blk:
    cited = []
    for keys in re.findall(r'data-src="([^"]*)"', page):
        if not keys.startswith("rule:"):
            for d in MX.sources_for(keys.split(",")):
                if d not in cited: cited.append(d)
    listed = [norm(x) for x in re.findall(r"<li><a [^>]*>(.*?)</a></li>", blk.group(1))]
    if sorted(listed) != sorted(cited):
        fail("A5", f"sources block lists {sorted(set(listed) ^ set(cited))} that no panel cites (or misses one)")

# ---------------- B. claims ----------------
for attr, body in re.findall(r'<span data-claim="([^"]*)">(.*?)</span>', page, re.S):
    c = json.loads(H.unescape(attr))
    if not re.search(rf"\b{re.escape(c['word'])}\b", norm(re.sub(r'<[^>]+>', '', body)), re.I):
        fail("B1", f"claim word '{c['word']}' not in its sentence")
    if not MX.holds(c["cond"], VALS):
        fail("B1", f"claim '{c['word']}' is false: {c['cond']} with {VALS.get(c['cond'][0])}")
OUTSIDE = visible(skip_attrs=("data-claim", "data-rule"))
for w in MX.QUANT:
    hit = re.search(rf"\b{re.escape(w)}\b", OUTSIDE, re.I)
    if hit: fail("B2", f"'{w}' used without a checked claim: …{OUTSIDE[max(0, hit.start()-50):hit.end()+40]}…")

# ---------------- C. invariants ----------------
cx = data.get("claims_extra") or {}
if VALS["claims_paid_n"] is not None and VALS["claims_filed"] is not None and VALS["claims_paid_n"] > VALS["claims_filed"]:
    fail("C1", f"claims paid {VALS['claims_paid_n']} > claims filed {VALS['claims_filed']}")
if cx.get("claims") and cx.get("paid_n") is not None and cx.get("cwop_share") is not None:
    expect_paid = cx["claims"] * (100 - cx["cwop_share"]) / 100
    if abs(cx["paid_n"] - expect_paid) > max(1, 0.002 * cx["claims"]):
        fail("C2", f"paid {cx['paid_n']} + closed-without-payment {cx['cwop_share']}% != {cx['claims']} filed")
for n in re.findall(r"([\d,]+) paid (?:NFIP )?(?:flood )?claims", TEXT, re.I):
    if VALS["claims_paid_n"] is None or int(n.replace(",", "")) != VALS["claims_paid_n"]:
        fail("C3", f"'{n} paid claims' on the page, but {VALS['claims_paid_n']} claims paid")
req = re.search(r'id="required".*?<tbody>(.*?)</tbody>', page, re.S)
if req and units:
    tot = sum(int(x.replace(",", "")) for x in re.findall(r"<tr><td>[^<]*</td><td>([\d,]+)</td>", req.group(1)))
    if tot != units: fail("C4", f"zone table rows sum to {tot}, not the {units} units shown")

# ---------------- F. reader first: every card opens with a short answer, not a data dump ----------------
for stand in re.findall(r'<p class="stand">(.*?)</p>', page, re.S):
    words = norm(re.sub(r"<[^>]+>", " ", stand)).split()
    if len(words) > 40: fail("F1", f"card opening is {len(words)} words (max 40): '{' '.join(words[:12])}…'")

# ---------------- E. rules registry ----------------
for tag, key, body in re.findall(r'<(span|div) data-rule="(\w+)">(.*?)</\1>(?=\s|<|$)', page, re.S):
    if key not in RULES: fail("E1", f"unknown rule {key}")
    elif norm(body) != norm(RULES[key]["text"]): fail("E1", f"rule {key} text differs from the registry")
if len(re.findall(r"data-rule=", page)) != len(re.findall(r'<(span|div) data-rule="(\w+)">(.*?)</\1>(?=\s|<|$)', page, re.S)):
    fail("E1", "a data-rule element could not be matched to its closing tag")

if fails:
    print("GATE FAIL:")
    for f in fails: print("  -", f)
    sys.exit(1)
print("GATE PASS:", html_path, f"(units {P.get('units')}, median {money(P['p50'])}, reconc "
      + (f"{abs(P['units']-official)/official*100:.1f}%" if official else "n/a") + ")")
