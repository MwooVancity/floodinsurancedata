"""Build one county's flood page from data.json (small datasets) + agg.json (bulk); parameterized by env.
River-style: white cards, every number has a unit, one line of context, source + as-of once.
No verdict, no advice prose. Writes directly to the repo dist path. -> OUT_HTML."""
import json, html, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops script dir; restore for ffcalc
import ffcalc
import metrics as MX
from metrics import m
from rules_registry import RULES, rule

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.environ.get("FF_DIR", HERE)
OUT_HTML = os.environ.get("OUT_HTML", os.path.join(HERE, "lee.html"))
data = json.load(open(os.path.join(DIR, "data.json")))
agg = json.load(open(os.path.join(DIR, "agg.json")))
P = agg["policies"]; C = agg["claims"]; NRI = agg.get("nri")
CL = os.environ.get("FF_COUNTYLABEL", "Lee County, Florida")   # full label
CS = os.environ.get("FF_COUNTYSHORT", "Lee County")            # short label
IS_STATE = os.environ.get("FF_LEVEL", "county") == "state"     # state hub page: same template, state data, county table
EXTRAS = json.load(open(os.path.join(DIR, "extras.json"))) if os.path.exists(os.path.join(DIR, "extras.json")) else {}
if not EXTRAS:   # county pages: the raw-pull extras live in data/all-counties/<geoid>.json
    _xp = os.path.join(os.path.dirname(HERE), "data", "all-counties", os.environ.get("FF_GEOID", "") + ".json")
    if os.path.exists(_xp): EXTRAS = json.load(open(_xp)).get("extras") or {}
OFFICIAL = int(os.environ.get("FF_OFFICIAL", "0"))        # FEMA official PIF count (0 = unknown)
POL_ASOF = "July 31, 2026"; RETR = "October 22, 2026"
ATTR = ("This product uses the Federal Emergency Management Agency's OpenFEMA API, "
        "but is not endorsed by FEMA.")

def money(n): return "$" + format(int(round(n)), ",") if n is not None else "—"
def big(n):
    """Readable large amounts for sentences: $68.9 million / $1.2 billion (exact figures stay in the details)."""
    if n is None: return "—"
    if n >= 1e9: return f"${n / 1e9:.1f} billion"
    if n >= 1e6: return f"${n / 1e6:.1f} million"
    return money(n)
def and_list(xs): xs = [str(x) for x in xs]; return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
def num(n): return format(int(n), ",") if n is not None else "—"
def _retr():
    try: _p = (json.load(open(os.path.join(DIR, "agg.json"))).get("manifest") or {}).get("policies", {}).get("pulled")
    except Exception: _p = None
    return pretty_date(_p) if _p else RETR
def pretty_date(s):
    """'2026-10-25' -> 'October 25, 2026' so every block shows one date format; other text passes through."""
    import datetime
    try: d = datetime.date.fromisoformat(str(s)[:10]); return f"{d:%B} {d.day}, {d.year}"
    except ValueError: return s
_SF = os.environ.get("FF_GEOID", "12071")[:2]
UNIT, UNITS = {"22": ("parish", "parishes"), "02": ("borough", "boroughs")}.get(_SF, ("county", "counties"))
RETR = _retr()
POL_ASOF = pretty_date(P.get("asof")) if P.get("asof") else POL_ASOF   # the snapshot date in the data, not a typed one   # the day this place's records were downloaded (state pages); the county collect date otherwise
USED = []   # metric keys every panel's source line cited -> the page's sources block (no hand-kept list)
def src(keys, effective, retrieved):
    """A panel's source line, built from the metrics it shows (metrics.py), never typed by hand."""
    USED.extend(keys)
    effective, retrieved = pretty_date(effective), pretty_date(retrieved)
    attr = (" " + ATTR) if MX.needs_openfema_attr(keys) else ""
    return (f'<p class="src" data-src="{",".join(keys)}">Source: {"; ".join(MX.sources_for(keys))}. '
            f'Data effective {effective}; retrieved {retrieved}.{attr}</p>')
def src_rules(keys):
    """Source line for a panel of program/legal rules: the official hosts behind each rule (rules_registry.py)."""
    hosts = []
    for k in keys:
        for u, _, _ in RULES[k]["sources"]:
            h = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
            if h not in hosts: hosts.append(h)
    return (f'<p class="src" data-src="rule:{",".join(keys)}">Source: {", ".join(hosts)} (official pages, checked '
            f'{pretty_date(__import__("rules_registry").CHECKED)}). Not endorsed by FEMA.</p>')
VALS = MX.values(agg, data)
def claim(text, word, cond): return MX.claim(text, word, cond, VALS)

# ---- housing assistance: aggregate Lee rows ----
h_rows = data.get("housing", [])
h_regs = sum(int(r.get("validRegistrations") or 0) for r in h_rows)
h_ihp = sum(float(r.get("totalApprovedIhpAmount") or 0) for r in h_rows)
h_disasters = len(set(r.get("disasterNumber") for r in h_rows))

# ---- declarations: distinct flood/storm events (by disasterNumber), not records ----
decl = data.get("declarations", [])
fh = [d for d in decl if d.get("incidentType") in ("Flood", "Hurricane", "Tropical Storm", "Tropical Depression", "Coastal Storm", "Severe Storm")]
def cal_year(d):
    # CALENDAR year from declarationDate — NOT fyDeclared (FEMA's federal fiscal year, which rolls to
    # the next year on Oct 1 and would mislabel an Oct 2026 event as "2027").
    s = d.get("declarationDate") or ""
    return s[:4] if len(s) >= 4 and s[:4].isdigit() else (str(d.get("fyDeclared")) if d.get("fyDeclared") else "")
def event_key(d):
    # one real event = one storm in one year. FEMA issues BOTH an emergency (EM, 3000-series) and a
    # major-disaster (DR, 4000-series) number for the same storm, sometimes with different type labels
    # ("Hurricane Helene" vs "Tropical Storm Helene"); dedup by storm name + calendar year, not number.
    t = (d.get("declarationTitle") or "").upper().strip()
    m = re.match(r"(?:HURRICANE|TROPICAL STORM|TROPICAL DEPRESSION)\s+(.+)", t)
    return (cal_year(d), (m.group(1).strip() if m else t))
fh_events = {event_key(d) for d in fh}
recent, seen = [], set()
for d in sorted(fh, key=lambda x: x.get("declarationDate") or "", reverse=True):
    k = event_key(d)
    if k in seen: continue
    seen.add(k); recent.append(d)
    if len(recent) >= 6: break

crs = sorted(data.get("crs", []), key=lambda x: -(int((x.get("sfhaDiscount") or "0%").rstrip("%") or 0)))

# ---- claims by year chart ----
by = C["by_year"]
years = sorted(int(y) for y in by)
maxc = max((by[str(y)][0] for y in years), default=1)
top_paid = sorted(((y, by[str(y)][1]) for y in years), key=lambda x: -x[1])[:3]

def claims_svg():
    if not years: return "<p>No claims recorded.</p>"
    # drawn at phone scale (360 wide) so 13px labels stay readable when the svg fills a ~300px card
    y0, y1 = years[0], years[-1]; W, H, pad = 360, 170, 18; span = max(1, y1 - y0)
    bw = max(2.0, (W - 2 * pad) / (span + 1) * 0.7)
    bars = []
    for y in years:
        c = by[str(y)][0]; x = pad + (y - y0) / span * (W - 2 * pad - bw); bh = (c / maxc) * (H - 2 * pad - 8)
        col = "var(--accent)" if any(y == ty for ty, _ in top_paid) else "var(--bar)"
        bars.append(f'<rect x="{x:.1f}" y="{H-pad-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"><title>{y}: {num(c)} claims, {money(by[str(y)][1])}</title></rect>')
    labs = "".join(f'<text x="{pad+(y-y0)/span*(W-2*pad-bw):.1f}" y="{H-2}" class="ax">{y}</text>' for y in range(((y0+9)//10)*10, y1+1, 10))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="NFIP claims per year">'
            f'{"".join(bars)}<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="var(--line)"/>{labs}</svg>')

def spread_svg():
    # cost-with-fees only: the full-risk line is NOT drawn here (it is a premium-only figure, a different scale)
    p25, p50, p75, p90, frp = P["p25"], P["p50"], P["p75"], P["p90"], None
    if not p50: return ""
    hi = (p90 or p75 or p50) * 1.08; W, H, pad = 360, 84, 26
    def x(v): return pad + (v / hi) * (W - 2 * pad)
    marks = ""
    # ticks only: close values made their text labels overprint ("$1,0$8,17$1,376"); the values sit in one line below
    for v in (p25, p50, p75, p90):
        if v: marks += f'<line x1="{x(v):.1f}" y1="30" x2="{x(v):.1f}" y2="62" stroke="var(--ink)" stroke-width="{3 if v == p50 else 1}"/>' 
    rng = f'<rect x="{x(p25):.1f}" y="40" width="{x(p75)-x(p25):.1f}" height="12" rx="3" fill="var(--bar)"/>' if p25 and p75 else ""
    frpline = (f'<line x1="{x(frp):.1f}" y1="34" x2="{x(frp):.1f}" y2="58" stroke="var(--accent)" stroke-width="2"/>'
               f'<text x="{x(frp):.1f}" y="96" class="ax2" text-anchor="middle" fill="var(--accent)">full-risk {money(frp)}</text>') if frp else ""
    vals = " · ".join(f"<b>{lab}</b> {tp(key, 'policies.' + k, money)}" for k, key, lab in
                      [("p25", "cost_p25", "Low end"), ("p50", "cost_p50", "Typical"), ("p75", "cost_p75", "High end"), ("p90", "cost_p90", "Highest tenth pay")] if P.get(k))
    return (f'<svg viewBox="0 0 {W} {H - 20}" width="100%" role="img" aria-label="Annual NFIP cost spread">'
            f'<line x1="{pad}" y1="46" x2="{W-pad}" y2="46" stroke="var(--line)"/>{rng}{marks}{frpline}</svg>'
            f'<p class="note" style="margin-top:0">{vals}{" or more" if p90 else ""}</p>')

ROOT_DATA = dict(agg, data=data, extras=EXTRAS, const=MX.CONST)   # what tp() reads and the gate re-reads
def _get(path):
    v = ROOT_DATA
    for seg in path.split("."):
        v = v[int(seg)] if isinstance(v, list) else v[seg]
    return v
def pct(v): return f"{v}%"
def tp(key, path, fmt=num, q=None):
    """The one way to print a figure read from the data: the gate re-reads the same path (V2)."""
    return m(key, fmt(_get(path)), path, q)

def card(title, standfirst, body, source="", id=""):
    _id = f' id="{id}"' if id else ""
    return f'<section class="card"{_id}><h2>{title}</h2><p class="stand">{standfirst}</p>{body}{source}</section>'

# ---- risk card (NRI or honest gap) ----
ABSENT = {None, "", "Not Applicable", "Insufficient Data", "No Rating", "No Expected Annual Losses"}
def _present(v): return v not in ABSENT and str(v).strip() not in ABSENT
cf = (NRI or {}).get("coastal", {}); inl = (NRI or {}).get("inland", {})
have_risk = NRI and (_present(cf.get("risk_rating")) or _present(inl.get("risk_rating")))
if have_risk:
    # headline = the plain rating word; the modeled-loss dollars + percentile are demoted into a plain note
    # (kept, not hidden — just not near-top jargon noise).
    def rating_row(block, label):
        rr = block.get("risk_rating")
        return f"<li><b>{label} flood risk</b><span>{html.escape(str(rr))}</span></li>" if _present(rr) else ""
    def _detail(block, label):
        pctl, eald = block.get("eal_national_pctl"), block.get("eal_total_usd")
        if not _present(block.get("risk_rating")): return ""
        bits = []
        if isinstance(pctl, (int, float)): bits.append(f"expected annual flood loss above about {m('nri_eal_pctl_' + label.lower(), str(round(pctl)) + '%')} of U.S. counties")
        if isinstance(eald, (int, float)) and eald > 0: bits.append(f"FEMA models roughly {tp('nri_eal_usd', 'nri.' + label.lower() + '.eal_total_usd', money, q=label.lower())} of flood loss a year across all its buildings")
        return (f" {label}: " + "; ".join(bits) + ".") if bits else ""
    risk_body = ("<ul class='kv'>" + rating_row(cf, "Coastal") + rating_row(inl, "Inland") + "</ul>"
                 "<p class='note'>This is FEMA's plain risk rating for the " + UNIT + ", a comparison — not a prediction "
                 "for your home. The rating multiplies expected flood loss by a community factor for social "
                 "vulnerability and resilience; the percentile below is expected loss alone, so the two can differ."
                 + _detail(cf, "Coastal") + _detail(inl, "Inland") +
                 " Any loss figure is a whole-" + UNIT + " estimate across all buildings, never one home's expected loss or premium.</p>")
    parts = []
    if _present(inl.get("risk_rating")): parts.append(f"{html.escape(str(inl['risk_rating']))} for rivers and heavy rain")
    if _present(cf.get("risk_rating")): parts.append(f"{html.escape(str(cf['risk_rating']))} for coastal flooding")
    risk = card("How much flood risk is here?",
                " and ".join(parts) + f", by FEMA's {UNIT} rating. That compares this {UNIT} with others; it is not a forecast for your address.",
                risk_body, src(["nri_rating", "nri_eal_usd"], "NRI 2023 release", RETR))
else:
    risk = card("How much flood risk is here?",
                f"FEMA's National Risk Index has no usable flood rating for this {UNIT}.",
                f"<p class='gap'>Gap: NRI flood expected-annual-loss and national percentile for {CS}. "
                "Next source to pull (reachable host): FEMA NRI county table from gis.fema.gov or the "
                "NRI_Table_Counties.csv download. The public third-party ArcGIS copy was a non-national sample.</p>")
if IS_STATE: risk = ""   # FEMA's NRI rates counties; the state page shows every county's rating in the tile map instead

# ---- zone card (policy UNITS) ----
zu = P["zone_units"]
# compact table: zones holding >=1% of units; the rest fold into one disclosed "other" row (phone-friendly)
_zshown = [(z, v) for z, v in list(zu.items())[:8] if v >= 0.01 * P["units"]]
_zrest = P["units"] - sum(v for _, v in _zshown)   # units in zones not shown (lower-ranked) + other/unclassified
def _zrow(label, v, z):
    _u = tp("zone_units", "policies.zone_units." + z, num, q=z) if z != "other" else m("zone_units", num(v), q="other")
    return f"<tr><td>{label}</td><td>{_u}</td><td>{m('zone_share', str(round(100 * v / P['units'], 1)) + '%', q=z)}</td></tr>"
zone_body = ("<table><thead><tr><th>Flood zone</th><th>Policies</th><th>Share</th></tr></thead><tbody>"
    + "".join(_zrow(f"Zone {html.escape(z)}" + (" (high-risk)" if z[:1] in "AV" else ""), v, z) for z, v in _zshown)
    + (_zrow("Other or unclassified zones", _zrest, "other") if _zrest > 0 else "")
    + "</tbody></table>")

# suppress on VALID COST observations (cost_n), not raw cohort — a cohort full of null/refund costs
# must not get a spread. agg carries spread_ok = cost_n >= 100.
SMALL_COHORT = not P.get("spread_ok", (P.get("cost_n") or 0) >= 100)
if SMALL_COHORT:
    cost_lead = (f"Only {tp('cost_n', 'policies.cost_n')} single-family primary-residence NFIP policies in {CS} have a valid "
                 f"recorded cost — too few for a reliable spread, so we show the count and median only. "
                 f"Median annual cost {m('cost_p50', money(P['p50']))}.")
    cost_body = (f"<ul class='kv'><li><b>Policies with a valid cost</b><span>{tp('cost_n', 'policies.cost_n')}</span></li>"
                 f"<li><b>Median annual cost</b><span>{m('cost_p50', money(P['p50']))}</span></li></ul>"
                 f"<p class='note'>Suppressed percentile spread: fewer than {tp('threshold', 'const.spread_min', q='spread_min')} policies with a valid recorded cost.</p>")
else:
    cost_lead = (f"Typically about {m('cost_p50', money(P['p50']))} a year ({m('cost_mo', money(round(P['p50'] / 12)))} a month), "
                 f"fees included. Half of homeowners here pay between {m('cost_p25', money(P['p25']))} and "
                 f"{m('cost_p75', money(P['p75']))}. To check a quote, use the checker at the top.")
    cost_body = (spread_svg() + "<p class='note'>Each policy's annual cost (premium plus the federal policy fee, "
                 "reserve fund assessment and HFIAA surcharge), single-family primary residences. The bar is the middle "
                 "half of policies, from " + tp('cost_n', 'policies.cost_n') + " single-family primary-home policies.</p>")
PREM_MED = P.get("prem_median")        # premium charged, before fees: the like-for-like comparator for full-risk
if P.get("coverage_building"):
    cost_body += (f"<p class='note'><b>Coverage in force:</b> {tp('coverage', 'policies.coverage_building', big, q='building')} of building and "
                  f"{tp('coverage', 'policies.coverage_contents', big, q='contents')} of contents coverage across all {CS} policies.</p>")
# monthly framing for the median
median_mo = money(round(P['p50'] / 12)) if P.get("p50") else None

# ---- cost by flood zone (median per zone) ----
czone = P.get("cost_by_zone") or {}
zone_cost_card = ""
if czone:
    rows_ = "".join(f"<tr><td>Zone {html.escape(z)}</td><td>{tp('zone_cost', f'policies.cost_by_zone.{z}.median', money, q=z)}</td>"
                    f"<td>{tp('zone_cost_n', f'policies.cost_by_zone.{z}.n', num, q=z)}</td></tr>" for z, d in czone.items())
    _zlo = min(czone.items(), key=lambda kv: kv[1]["median"]); _zhi = max(czone.items(), key=lambda kv: kv[1]["median"])
    zone_cost_card = card("What does it cost in my flood zone?",
        (f"From about {tp('zone_cost', f'policies.cost_by_zone.{_zlo[0]}.median', money, q=_zlo[0])} a year (Zone {html.escape(_zlo[0])}) to {tp('zone_cost', f'policies.cost_by_zone.{_zhi[0]}.median', money, q=_zhi[0])} "
         f"(Zone {html.escape(_zhi[0])}) here. " if len(czone) > 1 else "")
        + "Your zone is on your lender's flood determination or FEMA's map; find its row below.",
        f"<table><thead><tr><th>Flood zone</th><th>Median / yr</th><th>Policies</th></tr></thead><tbody>{rows_}</tbody></table>"
        + (("<p class='note'><b>" + claim("Why can a high-risk zone cost less than Zone X here?", "cost less than",
                                           ("zone_inversion", "==", 1)) + "</b> " + rule("rr2_zone") + "</p>")
           if VALS["zone_inversion"] else "")
        + f"<p class='note'>Zones with fewer than {tp('threshold', 'const.zone_min', q='zone_min')} priced single-family policies are omitted. Your own premium still depends on elevation and coverage.</p>",
        src(["zone_cost"], POL_ASOF, RETR), id="zone-cost")

# ---- premium trend: REMOVED. An in-force annual-policy snapshot holds only current-term policies, so
# there are never enough distinct effective-years for an honest like-for-like trend — and showing one
# would contradict the page's own "what this data cannot tell you" note. The glide-path below is the
# sourced, rule-based answer to "is it going up?" instead. (No trend card is rendered.)

MX.compare("prem_median", "frp_median")   # like-for-like or it raises
gap_lead = ((m('share_below', str(P['share_below']) + '%') + " of bills here "
             + claim("can keep rising", "rising", ("share_below", ">", 0)) + ": they pay less than FEMA's full-risk price. "
             + rule("glide") if P.get("share_below") else
             "No policy here pays less than FEMA's full-risk price.")
            + f" Median premium {m('prem_median', money(PREM_MED))}, full-risk {m('frp_median', money(P['frp_median']))} (premiums only, before fees).")
# Years-to-full-risk glide path — derived from data we already hold + the statutory annual cap (a RULE,
# not a model). Honest, sourced counter to competitors' black-box projections.
glide_note = ""
_yrs = ffcalc.years_to_full_risk(PREM_MED, P.get("frp_median"))
if _yrs is None:
    glide_note = (f"<p class='note'><b>Yearly cap:</b> {rule('cap')} "
                  + claim("Here the median premium is already at or above the median full-risk premium, so the median "
                          "policy has no gap left to close; any one policy can still sit below its own full-risk price.",
                          "at or above", ("prem_median", ">=", "frp_median")) + "</p>")
else:
    glide_note = (f"<p class='note'><b>Years to the full-risk price:</b> {rule('cap')} At the "
                  f"{m('cap_pct', str(int(ffcalc.HFIAA_CAP*100)) + '%')} cap, a policy at today's median premium ({m('prem_median', money(PREM_MED))}) would take at "
                  f"least about {m('glide_years', str(_yrs))} annual renewal{'s' if _yrs != 1 else ''} to reach the median full-risk premium "
                  f"({m('frp_median', money(P['frp_median']))}). "
                  + claim("This is the limit on how fast a bill can climb, not a forecast of any one policy.", "climb",
                          ("frp_median", ">", "prem_median")) + "</p>")
claims_lead = (f"Floods here have led to {m('claims_filed', num(C['rows']))} NFIP flood claims and "
               f"{m('claims_total', big(C['total_paid']))} in payouts since {C['year_min']}"
               + (f"; the worst years were {and_list(y for y, _ in top_paid)}." if top_paid else "."))
# the ratio reads like a risk score, so it is demoted to a note with both numbers shown, never the headline.
claims_ratio_note = (f"<p class='note'>That is {m('claims_filed', num(C['rows']))} claims since {C['year_min']} against "
                     f"{m('units', num(P['units']))} policies in force today — a cumulative tally spanning ~{m('claims_span_years', str(C['year_max']-C['year_min']+1))} "
                     f"years over a present-day snapshot, not an annual claim rate or a flood probability.</p>")

def _pct(v):
    if v in ABSENT or str(v).strip() in ABSENT: return None
    s = str(v).strip().rstrip("%")
    try: n = int(float(s))
    except ValueError: return None
    return None if n == 0 else f"{n}%"
def _cls(v): return html.escape(str(v)) if (v not in ABSENT and str(v).strip() not in ABSENT) else "—"
def _disc(v): return _pct(v) or "No discount"
try: _PL_ALL = json.load(open(os.environ.get("FF_PLACES", "")))
except Exception: _PL_ALL = []
HAS_CPAGES = any(str(p.get("geoid") or "")[:2] == os.environ.get("FF_GEOID", "12071")[:2] and p.get("slug") != os.environ.get("FF_SLUG")
                 for p in _PL_ALL)
MIN_PRICED = 30   # a county median is shown from 30 priced policies (with its count); never a dash for a real number
_LEGAL = r",\s*(city|town|village|borough|township|county|parish)\s+of\s*$"
def _short(c):   # FEMA admin notes ("HOUMA, CITY OF-USE CID 225206": file under another community number) are not part of the name
    n = re.sub(r"\s*-\s*USE\s+CID\s*\d+.*$", "", c['communityName'].replace('*', '').strip(), flags=re.I)
    return re.sub(_LEGAL, "", n, flags=re.I).title()
def _cname(c):
    """FEMA's 'CAPE CANAVERAL, CITY OF' -> 'Cape Canaveral' (the reader looks for their town's name, not the legal form);
    two communities with one name keep their form: 'Stonington (town)', 'Stonington (borough)'."""
    n = _short(c)
    if sum(1 for o in crs if _short(o) == n) > 1:
        f = re.search(_LEGAL, c['communityName'].strip(), flags=re.I)
        if f: n += f" ({f.group(1).lower()})"
    return html.escape(n)
# table only for communities with a discount; the rest fold into one named line (a screen of "No discount" rows helps no one)
_has_disc = [c for c in crs if _pct(c.get("sfhaDiscount")) or _pct(c.get("nonSfhaDiscount"))]
_no_disc = [c for c in crs if c not in _has_disc]
def _tagd(key, shown, q):   # a table cell: tag it when it is a figure (not "No discount" / a dash)
    return m(key, shown, q=html.unescape(q).replace('"', "")) if re.search(r"\d", shown) else shown
def _dnum(c): return int((_pct(c.get("sfhaDiscount")) or "0%").rstrip("%"))
_shown_disc = sorted(_has_disc, key=lambda c: -_dnum(c))[:15] if IS_STATE else _has_disc   # a state can have hundreds
crs_rows = "".join(f"<tr><td>{_cname(c)}" + (f" ({html.escape(str(c.get('county') or '').title())})" if IS_STATE and c.get('county') else "") + "</td>"
                   f"<td>{_tagd('crs_discount', _disc(c.get('sfhaDiscount')), _cname(c) + ':sfha')}</td><td>{_tagd('crs_discount', _disc(c.get('nonSfhaDiscount')), _cname(c) + ':other')}</td>"
                   f"<td>{_tagd('crs_class', _cls(c.get('classRating')), _cname(c))}</td></tr>" for c in _shown_disc)
crs_none_note = ((f"<p class='note'>The {m('crs_count', str(len(_shown_disc)), q='shown')} largest discounts of {m('crs_count', str(len(_has_disc)), q='discounted')} discounted communities are shown; "
                  f"{m('crs_count', str(len(_no_disc)), q='none')} communities here have no CRS discount." + (f" Each {UNIT} page lists its own towns." if HAS_CPAGES else "") + "</p>")
                 if IS_STATE else
                 (f"<p class='note'><b>No CRS discount ({m('crs_count', str(len(_no_disc)), q='none')}):</b> " + "; ".join(_cname(c) for c in _no_disc) + ".</p>") if _no_disc else "")
_disc_communities = [c for c in crs if _pct(c.get("sfhaDiscount"))]
if _disc_communities:
    top = max(_disc_communities, key=lambda c: int(_pct(c["sfhaDiscount"]).rstrip("%")))
    crs_lead = (claim("Yes", "yes", ("crs_discount_communities", ">", 0))
                + f", in {m('crs_count', str(len(_disc_communities)), q='sfha_discounted')} of the {m('crs_count', str(len(crs)), q='all')} towns here: up to "
                f"{m('crs_discount', _pct(top['sfhaDiscount']), q=html.unescape(_cname(top)) + ':sfha')} off in {_cname(top)}. "
                + rule("crs_auto") + " Find your town below.")
else:
    crs_lead = ("Not through a community discount: " +
                (f"none of {CS}'s {m('crs_count', str(len(crs)), q='all')} NFIP communities has one." if len(crs) != 1 else f"{CS}'s only NFIP community has none."))

# ---- how to get covered (factual public NFIP rules — the reader's "what do I do next" + the 30-day catch) ----
_HOWTO = ["howto_answer", "homeowners_excl", "howto_tiles", "wait_exceptions", "limits", "how_to_buy", "already_flooded"]
howto_card = card("How do I actually get covered — and how fast?",
    rule("howto_answer"),
    rule("howto_tiles")
    + f"<p class='note'>{rule('homeowners_excl')} {rule('wait_exceptions')} {rule('limits')} {rule('how_to_buy')}</p>"
    + f"<p class='note'>{rule('already_flooded')} Past aid paid here is in &ldquo;Did the government pay homeowners "
      "after floods?&rdquo; below.</p>",
    src_rules(_HOWTO), id="covered")

recent_li = "".join(
    f"<li>{html.escape(cal_year(d))} — {html.escape((d.get('declarationTitle') or d.get('incidentType') or '').title())}</li>" for d in recent)

# ---- take-up: how common NFIP coverage is here (policy units vs Census housing units) ----
hu = data.get("housing_units")
hu_yr = data.get("housing_units_year", "2023")
takeup_card = ""
if hu and P.get("units") and (data.get("penetration") or {}).get("overall_pct") is None:   # Census proxy only when FEMA's rate is missing
    tu = round(100 * P["units"] / hu, 1)
    takeup_card = card("How common is flood insurance here?",
        f"{CS} has about {m('takeup_per_100', str(tu))} NFIP flood policies for every hundred homes ({tp('units', 'policies.units')} policy units vs "
        f"{tp('housing_units', 'data.housing_units')} housing units).",
        f"<ul class='kv'><li><b>NFIP policy units</b><span>{tp('units', 'policies.units')}</span></li>"
        f"<li><b>Housing units</b><span>{tp('housing_units', 'data.housing_units')}</span></li>"
        f"<li><b>Policies per hundred homes</b><span>{m('takeup_per_100', str(tu))}</span></li></ul>"
        "<p class='note'>A coverage-commonness proxy: policy units include some multi-unit and "
        "non-residential policies and exclude private flood insurance, so read it as how widespread NFIP "
        "coverage is here, not an exact share of households.</p>",
        src(["units", "housing_units"], f"ACS 5-year {hu_yr}", RETR))
else:
    takeup_card = card("How common is flood insurance here?",
        f"Not shown — Census housing-unit data was not available for this {UNIT}.",
        "<p class='gap'>Gap: U.S. Census ACS 5-year B25001 housing units, to divide into NFIP policy units.</p>")

# ---- state flood-risk table (every county in the state by FEMA rating, this one in bold) ----
GEOID_SELF = os.environ.get("FF_GEOID", "12071")
state_risk = agg.get("state_risk") or []
RISK_ORD = {"Very High": 4, "Relatively High": 3, "Relatively Moderate": 2, "Relatively Low": 1, "Very Low": 0}
def _ord(r): return RISK_ORD.get(r, -1)
tilemap_card = ""
if len(state_risk) >= 4:
    # a labelled table, not a mosaic: unlabelled squares told a phone reader nothing (Vermont read, 2026-10-26)
    try: _CNM = json.load(open(os.path.join(os.path.dirname(HERE), "data", "us", "county_names.json")))
    except Exception: _CNM = {}
    def _rn(c): return html.escape(_CNM.get(c.get("fips")) or c.get("county") or "")
    _by = {}
    for c in state_risk: _by.setdefault(_ord(c.get("rating")), []).append(c)
    _rt = "".join(f"<tr><td>{lab}</td><td>{m('county_count', str(len(_by.get(o, []))), q=lab)}</td><td>"
                  + (", ".join(("<b>" + _rn(c) + "</b>") if c.get("fips") == GEOID_SELF else _rn(c) for c in _by.get(o, [])[:12])
                     + (f" and {m('county_count', str(len(_by[o]) - 12), q=lab + ':more')} more" if len(_by.get(o, [])) > 12 else "") if o >= 3 or any(c.get("fips") == GEOID_SELF for c in _by.get(o, [])) else "")
                  + "</td></tr>" for lab, o in [("Very High", 4), ("Relatively High", 3), ("Relatively Moderate", 2), ("Relatively Low", 1), ("Very Low", 0)])
    tiles_body = (f"<table><thead><tr><th>FEMA flood-risk rating</th><th>{UNITS.title()}</th><th>Which</th></tr></thead><tbody>{_rt}</tbody></table>"
                  "<p class='note'>FEMA's National Risk Index rating (coastal and inland flooding, the worse of the two), a model of expected loss. "
                  "Names are listed for the two highest ratings" + ("" if IS_STATE else f" and for this {UNIT}, in bold") + ".</p>")
    _high = sum(1 for c in state_risk if _ord(c.get("rating")) >= 3)
    tilemap_card = card(f"How {CS} {UNITS} compare" if IS_STATE else f"How {CS} compares across the state",
        ((f"{m('county_count', str(_high), q='high')} of" if _high else "None of") + f" {CS}'s {m('county_count', str(len(state_risk)), q='all')} {UNITS} "
         + ("is" if not _high else "are") + " rated Relatively High or Very High for flooding by FEMA's National Risk Index, a model of expected loss; "
         "the payouts above show what has actually flooded." if IS_STATE else
         (lambda own: f"{CS} is rated {html.escape(str(own.get('rating')))}: {m('county_count', str(sum(1 for c in state_risk if _ord(c.get('rating')) >= _ord(own.get('rating')))), q='same_or_higher')} "
                      f"of the state's {m('county_count', str(len(state_risk)), q='all')} {UNITS} are rated the same or higher.")
         (next((c for c in state_risk if c.get("fips") == GEOID_SELF), None) or {"rating": "unrated"})),
        tiles_body,
        src(["nri_rating"], "NRI 2023 release", RETR))

# ---- ZIP lookup inside the county (your-place flow) ----
bz = [z for z in (agg["policies"].get("by_zip") or []) if z.get("units")]
zip_card = ""
if bz:
    data_js = json.dumps({z["zip"]: {"u": z["units"], "m": z["median"], "n": z["cost_n"]} for z in bz})
    _zi = {z["zip"]: i for i, z in enumerate(agg["policies"].get("by_zip") or [])}
    toprows = "".join(
        f"<tr><td>{m('zip', html.escape(z['zip']), q=z['zip'])}</td><td>{tp('zip_cost', f'policies.by_zip.{_zi[z[chr(122)+chr(105)+chr(112)]]}.median', money, q=z['zip']) if z.get('median') else '—'}</td>"
        f"<td>{tp('zip_units', f'policies.by_zip.{_zi[z[chr(122)+chr(105)+chr(112)]]}.units', num, q=z['zip'])}</td></tr>" for z in bz[:8])
    zip_card = card(f"Find your ZIP in this {UNIT}",
        ((lambda zs: f"Costs vary by ZIP here, from about {tp('zip_cost', f'policies.by_zip.{_zi[min(zs, key=lambda z: z[1])[0]]}.median', money, q=min(zs, key=lambda z: z[1])[0])} to "
                     f"{tp('zip_cost', f'policies.by_zip.{_zi[max(zs, key=lambda z: z[1])[0]]}.median', money, q=max(zs, key=lambda z: z[1])[0])} a year among the largest. " if len(zs) > 1 else "")
         ([(z["zip"], z["median"]) for z in bz if z.get("median")])) + "Type yours to see its own figures.",
        f'<input id="zq" inputmode="numeric" maxlength="5" placeholder="e.g. {bz[0]["zip"]}" aria-label="Your ZIP code" '
        f'style="font-size:18px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;width:160px">'
        f'<p id="zout" class="note" style="margin-top:10px">Enter a five-digit ZIP above.</p>'
        f'<table style="margin-top:12px"><thead><tr><th>ZIP</th><th>Median annual cost</th><th>Policy units</th></tr></thead>'
        f'<tbody>{toprows}</tbody></table>'
        f'<p class="note">Median shown only for ZIPs with {tp("threshold", "const.zip_min", q="zip_min")} or more priced single-family policies; smaller ZIPs show count only.</p>'
        f'<script>var ZD={data_js};var zi=document.getElementById("zq"),zo=document.getElementById("zout");'
        'zi.addEventListener("input",function(){var z=zi.value.trim();var d=ZD[z];'
        'if(!d){zo.textContent=z.length>=5?"No NFIP data for ZIP "+z+" in this ' + UNIT + '.":"Enter a five-digit ZIP above.";return;}'
        'zo.innerHTML="<b>"+z+"</b>: "+d.u.toLocaleString()+" policy units"+(d.m?("; median $"+d.m.toLocaleString()+" / yr ("+d.n.toLocaleString()+" priced policies)"):" (too few priced policies for a median).");});'
        '</script>',
        src(["zip_cost", "units"], POL_ASOF, RETR))

# ---- STATE-ONLY blocks: cost by county (the hub), why published averages differ, policies-in-force trend ----
averages_card = state_trend_card = ""
if IS_STATE:
    _nm = {c["fips"]: c["county"] for c in (data.get("nri_counties") or [])}
    try: _pl = {p.get("geoid"): p["slug"] for p in json.load(open(os.environ.get("FF_PLACES", "")))}
    except Exception: _pl = {}
    try: _CN = json.load(open(os.path.join(os.path.dirname(HERE), "data", "us", "county_names.json")))
    except Exception: _CN = {}
    def _cn(g): return html.escape(_CN.get(g) or _nm.get(g) or g)   # Census name ("Washington County"), NRI as fallback
    def _clink(g): return f'<a href="../{_pl[g]}/">{_cn(g)}</a>' if g in _pl else _cn(g)
    # only this state's counties: a few records carry another state's county code (e.g. 20015 on a Vermont policy)
    _cty = sorted(((g, r) for g, r in (agg.get("counties") or {}).items() if r.get("units") and g[:2] == GEOID_SELF[:2]),
                  key=lambda kv: -kv[1]["units"])
    _priced = [(g, r) for g, r in _cty if (r.get("cost_n") or 0) >= MIN_PRICED and r.get("p50")]
    _ok = lambda r: (r.get("cost_n") or 0) >= MIN_PRICED
    _rows = "".join(f"<tr><td>{_clink(g)}</td><td>{tp('county_units', f'counties.{g}.units', num, q=g)}</td>"
                    f"<td>{tp('county_cost', f'counties.{g}.p50', money, q=g) if _ok(r) else '—'}</td>"
                    f"<td>{tp('county_share_below', f'counties.{g}.share_below', pct, q=g) if _ok(r) and r.get('share_below') is not None else '—'}</td>"
                    f"<td>{tp('county_claims', f'counties.{g}.claims', num, q=g)}</td></tr>" for g, r in _cty[:30])
    _cheap = sorted(_priced, key=lambda kv: kv[1]["p50"])[:5]; _dear = sorted(_priced, key=lambda kv: -kv[1]["p50"])[:5]
    zip_card = "" if len(_cty) < 2 else card(f"What does it cost in my {UNIT}?",
        (f"From about {tp('county_cost', f'counties.{_cheap[0][0]}.p50', money, q=_cheap[0][0])} a year in {_cn(_cheap[0][0])} to "
         f"{tp('county_cost', f'counties.{_dear[0][0]}.p50', money, q=_dear[0][0])} in {_cn(_dear[0][0])}, "
         f"among {UNITS} with {tp('threshold', 'const.min_priced', q='min_priced')} or more priced policies. Find yours below." if len(_priced) > 1 else f"Find your {UNIT} below."),
        f"<table><thead><tr><th>{UNIT.title()}</th><th>Policies</th><th>Median / yr</th><th>Below full-risk</th><th>Claims since 1978</th></tr></thead>"
        f"<tbody>{_rows}</tbody></table>"
        + (f"<p class='note'>{m('units_listed', str(len(_cty) - 30), q='not_listed')} smaller {UNITS} are not listed. </p>" if len(_cty) > 30 else "")
        + (f"<p class='note'><b>Lowest typical cost:</b> {and_list(_cn(g) + ' (' + tp('county_cost', f'counties.{g}.p50', money, q=g) + ')' for g, r in _cheap)}. "
           f"<b>Highest:</b> {and_list(_cn(g) + ' (' + tp('county_cost', f'counties.{g}.p50', money, q=g) + ')' for g, r in _dear)}. "
           "Median annual cost of single-family primary-home policies.</p>" if len(_priced) >= 10 else "")
        + f"<p class='note'>{UNITS.title()} with fewer than {tp('threshold', 'const.min_priced', q='min_priced')} priced single-family policies show a dash; medians from under {tp('threshold', 'const.spread_min', q='spread_min')} policies move more from year to year.</p>",
        src(["county_units", "cost_p50", "share_below", "claims_filed"], POL_ASOF, RETR), id="counties")
    _av = (EXTRAS.get("policies") or {}).get("averages") or {}
    if _av.get("sf_cost_mean"):
        _avrows = [("Median cost, single-family homes", m("cost_p50", money(P["p50"])), "premium plus fees; the middle policy"),
                   ("Average (mean) cost, single-family homes", tp("cost_mean", "extras.policies.averages.sf_cost_mean", money), "pulled up by a few expensive policies"),
                   ("Median premium only, single-family homes", tp("prem_sf_median", "extras.policies.averages.sf_prem_median", money), "before the federal fee, reserve fund and surcharge"),
                   ("Average premium only, single-family homes", tp("prem_mean", "extras.policies.averages.sf_prem_mean", money), "the figure many sites quote"),
                   ("Median cost, every policy type", tp("cost_all_median", "extras.policies.averages.all_cost_median", money), "adds condos, rentals and businesses"),
                   ("Average cost, every policy type", tp("cost_all_mean", "extras.policies.averages.all_cost_mean", money), "")]
        averages_card = card(f"Why do sites quote different averages for {CS}?",
            f"Because they measure different things. From the same FEMA records, the typical single-family home pays "
            f"{m('cost_p50', money(P['p50']))} a year, but the average across every policy type is {tp('cost_all_mean', 'extras.policies.averages.all_cost_mean', money)}.",
            "<table><thead><tr><th>Measure</th><th>Amount</th><th>What it counts</th></tr></thead><tbody>"
            + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in _avrows) + "</tbody></table>"
            "<p class='note'>Published averages rarely say which of these they are, or which year. All six here come from the "
            f"NFIP policies in force on {POL_ASOF}.</p>",
            src(["cost_p50", "cost_mean", "prem_mean", "cost_all_median", "cost_all_mean"], POL_ASOF, RETR))
    _h = (data.get("inforce_history") or {}).get("by_year") or {}
    _ch = VALS.get("inforce_change_pct")
    if _h and _ch is not None:
        _c = ("inforce_change_pct", "<", 0) if _ch < 0 else ("inforce_change_pct", ">", 0)
        _txt = (claim("Yes", "yes", _c) + ": " + claim(f"policies in force fell {m('inforce_change_pct', str(abs(_ch)) + '%')} from 2022 to 2026", "fell", _c)
                if _ch < 0 else "No: " + claim(f"policies in force grew {m('inforce_change_pct', str(_ch) + '%')} from 2022 to 2026", "grew", _c)
                if _ch > 0 else "No: policies in force were unchanged from 2022 to 2026")
        state_trend_card = card(f"Are people dropping flood insurance in {CS}?",
            _txt + f", from {tp('inforce', 'data.inforce_history.by_year.2022', q='2022')} to {tp('inforce', 'data.inforce_history.by_year.2026', q='2026')} NFIP policy records.",
            "<table><thead><tr><th>July 31</th><th>Policies in force</th></tr></thead><tbody>"
            + "".join(f"<tr><td>{y}</td><td>{tp('inforce', f'data.inforce_history.by_year.{y}', q=y)}</td></tr>" for y, v in sorted(_h.items())) + "</tbody></table>"
            "<p class='note'>Policy records in force on July 31 of each year (a condo-building policy counts once). "
            "Private flood policies are not in this data.</p>",
            src(["inforce"], "2019–2026", RETR))

# ---- raw-pull extras: would a policy rebuild the home, why claims went unpaid, which storms paid most ----
_xp, _xc = EXTRAS.get("policies") or {}, EXTRAS.get("claims") or {}
rebuild_card = unpaid_card = events_card = ""
if (_xp.get("replacement_n") or 0) >= 30 and _xp.get("replacement_over_250k_pct") is not None:
    _ro = _xp["replacement_over_250k_pct"]
    rebuild_card = card("Would a policy here pay to rebuild my home?",
        f"Not in full for {tp('rebuild_over_cap_pct', 'extras.policies.replacement_over_250k_pct', pct)} of insured single-family homes here: FEMA's records put their "
        f"rebuilding cost above {rule('building_cap')}",
        f"<ul class='kv'><li><b>Rebuilding cost above the building limit (of {tp('rebuild_n', 'extras.policies.replacement_n')} policies reporting one)</b><span>{tp('rebuild_over_cap_pct', 'extras.policies.replacement_over_250k_pct', pct)}</span></li>"
        + (f"<li><b>Carry the maximum building coverage</b><span>{tp('at_cap_pct', 'extras.policies.at_building_max_pct', pct)}</span></li>" if _xp.get("at_building_max_pct") is not None else "")
        + (f"<li><b>Damage was more than the coverage (of {tp('damage_n', 'extras.claims.damage_n')} claims paid with a damage figure)</b><span>{tp('damage_over_cov_pct', 'extras.claims.damage_over_coverage_pct', pct)}</span></li>"
           if _xc.get("damage_over_coverage_pct") is not None and (_xc.get("damage_n") or 0) >= 30 else "")
        + f"</ul><p class='note'>{rule('limits')} Rebuilding cost is the replacement-cost figure on each single-family primary-home policy record.</p>",
        src(["rebuild_over_cap_pct", "at_cap_pct", "damage_over_cov_pct"], POL_ASOF, RETR) + src_rules(["building_cap", "limits"]))
_why = [dict(r, i=i) for i, r in enumerate(_xc.get("unpaid_reasons") or []) if r["code"] not in ("97", "98", "99")]   # 97 other, 98/99 recorded in error: not a reason
if _why and (_xc.get("unpaid_n") or 0) >= 10:
    unpaid_card = card("Why do flood claims here go unpaid?",
        f"Of the {tp('unpaid_n', 'extras.claims.unpaid_n')} claims here closed without payment, the top reason FEMA recorded was "
        f"“{html.escape(_why[0]['label']).lower()}” ({tp('unpaid_reason_n', f'extras.claims.unpaid_reasons.{_why[0][chr(105)]}.n', q=_why[0]['code'])} claims).",
        "<table><thead><tr><th>Reason recorded</th><th>Claims</th></tr></thead><tbody>"
        + "".join(f"<tr><td>{html.escape(r['label'])}</td><td>{tp('unpaid_reason_n', f'extras.claims.unpaid_reasons.{r[chr(105)]}.n', q=r['code'])}</td></tr>" for r in _why) + "</tbody></table>"
        "<p class='note'>The building non-payment reason on each NFIP claim closed with nothing paid. Records marked "
        "“other” or entered in error are left out.</p>",
        src(["unpaid_n", "unpaid_reason_n"], f"{C['year_min']}–{C['year_max']}", RETR))
def _evname(e):   # FEMA's event name plus its year(s) of loss: "Vermont/New York Flooding (2023)"
    y = e.get("years") or []
    n = re.sub(r"^\d{4}-\d{2}-", "", e["name"])                       # FEMA codes like "2026-03-KonaStorm"
    n = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", n.replace("-", " ")).strip()   # -> "Kona Storm"
    return html.escape(n) +(f" ({y[0]})" if len(y) == 1 else f" ({y[0]}–{y[-1]})" if y else "")
_GENERIC = {"flood", "flooding", "floods", "heavy", "rain", "rains", "rainfall", "severe", "storm", "storms", "and", "flash", "spring", "event"}
_ev = [dict(e, i=i) for i, e in enumerate(_xc.get("events") or []) if set(e["name"].lower().replace("/", " ").split()) - _GENERIC]
if len(_ev) >= 2:
    events_card = card("Which named storms paid out the biggest totals here?",
        f"Among named storms, {_evname(_ev[0])} paid out the largest total: {tp('event_paid', f'extras.claims.events.{_ev[0][chr(105)]}.paid', big, q=_ev[0]['name'])} across "
        f"{tp('event_claims', f'extras.claims.events.{_ev[0][chr(105)]}.claims', q=_ev[0]['name'])} NFIP flood claims.",
        "<table><thead><tr><th>Storm (FEMA's name)</th><th>Claims</th><th>Total paid</th><th>Average</th></tr></thead><tbody>"
        + "".join(f"<tr><td>{_evname(e)}</td><td>{tp('event_claims', f'extras.claims.events.{e[chr(105)]}.claims', q=e['name'])}</td>"
                  f"<td>{tp('event_paid', f'extras.claims.events.{e[chr(105)]}.paid', big, q=e['name'])}</td>"
                  f"<td>{tp('event_avg', f'extras.claims.events.{e[chr(105)]}.avg', money, q=e['name'])}</td></tr>" for e in _ev)
        + "</tbody></table><p class='note'>NFIP claims that were paid, grouped by the flood event FEMA assigned; claims with no event "
        "name, or a generic one like “flooding”, are left out.</p>",
        src(["event_paid", "event_claims"], f"{C['year_min']}–{C['year_max']}", RETR))

# ---- repetitive-loss properties (FEMA IA multiple-loss; a chronic repeat-flood signal, distinct from
# the annual NFIP claims) ----
ml = data.get("multiloss") or {}
multiloss_card = ""
if ml.get("total") is not None:   # 0 is a real, reassuring finding (no chronic repeat-flood homes), not "no data"
    _srl = ml.get("srl") or 0
    _mldate = ml.get("retrieved", RETR)
    # FEMA: one row per property PER declared disaster, and "there is not a way to aggregate by property" —
    # so the count is damage records on repeat-flooded homes, never a count of distinct homes.
    _ml_lead = (f"Some homes here flood again and again: {m('ml_total', num(ml['total']))} flood-damage applications in FEMA's "
                f"disaster-aid records came from homes that flooded more than once"
                + (f"; {m('ml_srl', num(_srl))} of those records came from homes hit in four or more" if _srl else "") + "."
                if ml["total"] else
                f"Not in FEMA's records: no disaster-aid applications here came from homes that flooded more than once.")
    multiloss_card = card("How often do the same homes flood here?", _ml_lead,
        f"<ul class='kv'><li><b>Repeat-flood damage records</b><span>{tp('ml_total', 'data.multiloss.total')}</span></li>"
        + (f"<li><b>Records from homes hit four or more times</b><span>{tp('ml_srl', 'data.multiloss.srl')}</span></li>" if _srl else "")
        + "</ul><p class='note'>One home appears once for each declared disaster that damaged it, so this counts "
        "damage events on repeat-flooded homes, not distinct homes (FEMA says these records cannot be totaled by "
        "property). Disaster-aid applications since 2002, separate from NFIP insurance claims.</p>",
        src(["ml_total"], "FEMA's current list", _mldate))

# ---- payout reality (avg paid + closed-without-payment share) ----
cx = data.get("claims_extra") or {}
payout_card = ""
if cx.get("claims"):
    _paid_pct = round(100 - cx["cwop_share"], 1)
    _ans = (claim("Most do", "most", ("cwop_share", "<", 50)) + f": {m('paid_share', str(_paid_pct) + '%')} of claims here paid something"
            if cx["cwop_share"] < 50 else
            claim("Most don't", "most", ("cwop_share", ">", 50)) + f": {m('cwop_share', str(cx['cwop_share']) + '%')} of claims here closed with no payment"
            if cx["cwop_share"] > 50 else f"About half: {m('cwop_share', str(cx['cwop_share']) + '%')} of claims here closed with no payment")
    payout_card = card("Do flood claims here actually pay out?",
        f"{_ans}. The average paid claim was {tp('avg_paid', 'data.claims_extra.avg_paid', money)}.",
        f"<ul class='kv'><li><b>Average paid claim</b><span>{tp('avg_paid', 'data.claims_extra.avg_paid', money)}</span></li>"
        f"<li><b>Closed with no payment</b><span>{tp('cwop_share', 'data.claims_extra.cwop_share', pct)}</span></li>"
        f"<li><b>Claims that paid</b><span>{tp('claims_paid_n', 'data.claims_extra.paid_n')}</span></li></ul>"
        f"<p class='note'>{rule('cwop')} The average is over claims that paid something; a single home can file "
        "across several floods over the years.</p>",
        src(["claims_filed", "avg_paid", "cwop_share"], f"{C['year_min']}–{C['year_max']}", cx.get("retrieved", RETR)))

# ---- claims OUTSIDE the high-risk zone (the "I'm not in the flood zone" rebuttal) ----
outside_note = ""
if cx.get("outside_sfha_pct") is not None and P.get("sfha_share_units") is not None:
    _out_pol = round(100 - P["sfha_share_units"], 1)          # share of policy units outside A/V zones
    MX.compare("outside_sfha_dollars", "outside_sfha_policies")
    _per = (claim("less per policy than inside the high-risk zone, but not zero", "less per policy",
                  ("outside_sfha_dollars", "<", "outside_sfha_policies")) if cx["outside_sfha_pct"] < _out_pol
            else claim("at least as much per policy as inside the high-risk zone", "as much per policy",
                       ("outside_sfha_dollars", ">=", "outside_sfha_policies")))
    _xmed = (czone.get("X") or {}).get("median")
    outside_note = card("I'm outside the high-risk zone. Do floods happen there?",
        claim("Yes", "yes", ("outside_sfha_dollars", ">", 0))
        + f". {m('outside_sfha_dollars', str(cx['outside_sfha_pct']) + '%')} of the flood-insurance claim money paid in {CS} went to homes "
        f"outside the high-risk zones, which hold {m('outside_sfha_policies', str(_out_pol) + '%')} of policies here: {_per}.",
        f"<ul class='kv'><li><b>Claim dollars paid outside A/V zones</b><span>{m('outside_sfha_dollars', str(cx['outside_sfha_pct']) + '%')}</span></li>"
        f"<li><b>Policies outside A/V zones</b><span>{m('outside_sfha_policies', str(_out_pol) + '%')}</span></li>"
        + (f"<li><b>Zone X median cost</b><span>{tp('zone_cost', 'policies.cost_by_zone.X.median', money, q='X')}</span></li>" if _xmed else "")
        + f"</ul><p class='note'>{rule('lender_any_zone')} Insured claims only, by each policy's rated zone.</p>",
        src(["outside_sfha_dollars", "outside_sfha_policies", "zone_cost"], f"claims {C['year_min']}–{C['year_max']}; policies {POL_ASOF}", cx.get("retrieved", RETR)))

# ---- how common flood insurance is: prefer NFIP penetration (overall + inside-SFHA) over the Census proxy ----
pen = data.get("penetration") or {}
def _share_words(p):   # the words must match the number: 64.9% is "about 6 in 10", never "1 in 2"
    return "Almost every home" if p >= 95 else f"About {round(p / 10)} in 10 homes" if p >= 15 else f"About 1 in {round(100 / p)} homes"
if pen.get("overall_pct") is not None:
    takeup_card = card("How many homes here carry flood insurance?",
        (f"{m('pen_words', _share_words(pen['overall_pct']))} here {'has' if pen['overall_pct'] < 20 else 'have'} flood insurance ({m('pen_overall', str(pen['overall_pct']) + '%')}). "
         if pen["overall_pct"] else f"Almost no homes here have NFIP flood insurance ({m('pen_overall', str(pen['overall_pct']) + '%')}). ")
        + ((f"Inside the high-risk zone it's {m('pen_sfha', str(pen['sfha_pct']) + '%')}." if pen["sfha_pct"] <= 100 else
            f"Inside the high-risk zone FEMA's rate is {m('pen_sfha', str(pen['sfha_pct']) + '%')}: it counts more policies there than its own "
            "estimate of high-risk buildings, so the exact share is unknown.") if pen.get("sfha_pct") is not None else ""),
        f"<ul class='kv'><li><b>All homes insured</b><span>{m('pen_overall', str(pen['overall_pct']) + '%')}</span></li>"
        + (f"<li><b>High-risk-zone homes insured</b><span>{m('pen_sfha', str(pen['sfha_pct']) + '%')}</span></li>"
           if pen.get("sfha_pct") is not None and pen["sfha_pct"] <= 100 else "")   # over 100%: explained in the lead, never a bare tile
        + f""
        f"<li><b>Residential policies in force</b><span>{tp('pen_contracts', 'data.penetration.contracts')}</span></li></ul>"
        "<p class='note'>FEMA's NFIP residential take-up rate — share of residential structures with an NFIP "
        "policy, overall and inside the Special Flood Hazard Area. NFIP only (excludes private flood insurance); "
        "the structure count is a FEMA estimate.</p>",
        src(["pen_overall", "pen_sfha"], pretty_date(pen.get("asof", RETR)), RETR))
# (else: the Census-based takeup_card defined earlier stands)

# ---- physical flood history (NOAA Storm Events) — distinct from insured claims ----
se = data.get("storm_events") or {}
storm_card = ""
if se.get("events"):
    storm_card = card("How often has it actually flooded here?",
        f"{m('storm_events', num(se['events']))} flood events here since {se.get('period', '1996-2025')[:4]}, by the weather service's count"
        + (f", with about {m('storm_damage', big(se['damage']))} in reported property damage" if se.get("damage") else "") + ".",
        f"<ul class='kv'><li><b>Flood events logged</b><span>{m('storm_events', num(se['events']))}</span></li>"
        + (f"<li><b>Reported property damage</b><span>{m('storm_damage', big(se['damage']))}</span></li>" if se.get("damage") else "")
        + "</ul><p class='note'>Physical flood events recorded by the National Weather Service for this " + UNIT + " "
        "(1996 on), separate from insured NFIP claims — it counts floods that happened, insured or not. Damage "
        "figures are NWS field estimates, not audited, and undercount in early years.</p>",
        src(["storm_events", "storm_damage"], se.get("period", "1996-2025"), se.get("retrieved", RETR)))

# ---- premium trend: median cost by the YEAR a policy was written (cohort-mix caveat, not a like-for-like index) ----
cyear = agg["policies"].get("cost_by_year") or {}
trend_card = ""
if len(cyear) >= 3:
    yrs = sorted(cyear.items())[-8:]
    rows_ = "".join(f"<tr><td>{y}</td><td>{tp('cost_by_year', f'policies.cost_by_year.{y}.median', money, q=y)}</td>"
                    f"<td>{tp('cost_by_year_n', f'policies.cost_by_year.{y}.n', num, q=y)}</td></tr>" for y, d in yrs)
    trend_card = card("What have premiums done over time here?",
        f"Median annual cost of {CS} single-family policies by the year each policy was written, "
        f"{yrs[0][0]} to {yrs[-1][0]}.",
        f"<table><thead><tr><th>Policy written</th><th>Median annual cost</th><th>Policies</th></tr></thead><tbody>{rows_}</tbody></table>"
        "<p class='note'>This is what policies <i>written in each year</i> cost — NOT the same homes tracked over "
        "time, so it reflects which properties bought each year and FEMA's Risk Rating 2.0 phase-in, not a "
        "like-for-like price index. For how a single bill can rise, see the full-risk glide-path above. Years with "
        f"under {tp('threshold', 'const.year_min', q='year_min')} priced policies are omitted.</p>",
        src(["cost_p50"], POL_ASOF, RETR))

mani = agg.get("manifest", {})
mani_ok = all(v.get("complete") for v in mani.values()) if mani else False
mani_line = "; ".join(f"{k}: {tp('records_total', f'manifest.{k}.unique_fetched', q=k + ':fetched')} of {tp('records_total', f'manifest.{k}.reported_total', q=k + ':reported')} fetched"
                      + ("" if v["complete"] else f" (MISSING {v['missing']})") for k, v in mani.items()) or "n/a"

# ---- SEO / GEO + place registry ----
SLUG = os.environ.get("FF_SLUG", "lee-county-fl")
BASE_URL = os.environ.get("FF_BASEURL", "https://example.com").rstrip("/")
CANON = f"{BASE_URL}/flood-insurance/{SLUG}/"
GEOID = os.environ.get("FF_GEOID", "12071")
META_DESC = (f"Median NFIP flood insurance cost in {CS} is {money(P['p50'])} a year "
             f"(middle half {money(P['p25'])}–{money(P['p75'])}); {P['share_below']}% pay below FEMA's "
             f"full-risk price. {num(P['rows'])} policies, claims, flood risk and CRS discounts, from FEMA data.")
# register this place so home/lookup/sitemap/siblings know it exists
PLACES = os.environ.get("FF_PLACES", os.path.join(HERE, "places.json"))
try: places = json.load(open(PLACES))
except Exception: places = []
if not IS_STATE:   # places.json lists county pages; state pages are listed by build_states.py
    places = [p for p in places if p.get("slug") != SLUG]
    places.append({"slug": SLUG, "label": CL, "short": CS, "geoid": GEOID,
                   "units": P["units"], "median": P["p50"], "state": agg.get("nri", {}).get("state") if agg.get("nri") else None})
    places.sort(key=lambda p: -(p.get("units") or 0))
    json.dump(places, open(PLACES, "w"), indent=1)
from agg_raw import NAMES as STATE_NAMES, slug as state_slug
# siblings must be ACTUAL neighbours: same-state BUILT pages (never the global top-5 by policy count,
# which just funnelled every page to the same mega-counties and orphaned the tail). No same-state page
# built yet -> link to the full directory, not a false "nearby".
_state = agg.get("nri", {}).get("state") if agg.get("nri") else None
_others = [p for p in places if p.get("slug") != SLUG]
_same = [p for p in _others if _state and p.get("state") == _state]
# guarantee >=3 links: same-state first; if fewer than 3, fill with the nearest-by-size other counties
# (places.json is sorted by units desc). Never leave a page with 0 lateral links.
_fill = [p for p in _others if p not in _same]
siblings = _same[:6] if len(_same) >= 3 else (_same + _fill)[:5]
try: _built_states = {s["abbr"] for s in json.load(open(os.path.join(os.path.dirname(HERE), "data", "states", "built.json")))}
except Exception: _built_states = set()
_state_link = (f'<a href="../{state_slug(_state)}/">{html.escape(STATE_NAMES[_state])} overview</a> · '
               if _state in _built_states else "")   # only link a state page that was actually built and gated

# "is $865 high?": the place beside its state and the U.S., same cohort (single-family primary-home policyCost),
# same snapshot. U.S. only when all 51 states are in the histogram; never a partial total called national.
_DD = os.path.join(os.path.dirname(HERE), "data")
def _hist_median(hist):
    a = sorted((int(v), c) for v, c in hist.items()); n, acc = sum(c for _, c in a), 0
    for v, c in a:
        acc += c
        if acc >= n / 2: return v
try: _uh = json.load(open(os.path.join(_DD, "us", "cost_hist.json")))
except Exception: _uh = {}
US_P50 = None
if len(_uh) == 51:
    _all = defaultdict(int)
    for _st in _uh.values():
        for v, c in _st.items(): _all[int(v)] += c
    US_P50 = _hist_median(_all)
def ordinal(n): return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
_ab = agg.get("state") if IS_STATE else _state
_sp = os.path.join(_DD, "states", state_slug(_ab), "agg.json") if _ab in STATE_NAMES else ""
_sagg = json.load(open(_sp)) if _sp and os.path.exists(_sp) else None
def _rank(r, n): return f"{ordinal(r)} highest" if r <= (n + 1) // 2 else f"{ordinal(n - r + 1)} lowest"   # say the short end
def _pct_vs(a, b, q):
    d = round(100 * (a - b) / b)
    return "the same as" if d == 0 else f"{m('pct_vs', str(abs(d)) + '%', q=q)} {'above' if d > 0 else 'below'}"
cmp_line = ""
if IS_STATE and US_P50:
    _ranked = []
    for _a in STATE_NAMES:
        _q = os.path.join(_DD, "states", state_slug(_a), "agg.json")
        if os.path.exists(_q):
            _pp = json.load(open(_q))["policies"]
            if (_pp.get("cost_n") or 0) >= 100: _ranked.append((_pp["p50"], _a))
    _ranked.sort(reverse=True)
    _r = next((i + 1 for i, (_, a) in enumerate(_ranked) if a == _ab), None)
    cmp_line = (f'<p class="cmp">That is {_pct_vs(P["p50"], US_P50, "us")} the U.S. median of {m("us_p50", money(US_P50))}'
                + (f'; {m("cost_rank", _rank(_r, len(_ranked)))} of {m("rank_n", str(len(_ranked)))} states' if _r else "") + ".</p>")
elif _sagg and not IS_STATE:
    _sc = [(r["p50"], g) for g, r in (_sagg.get("counties") or {}).items() if (r.get("cost_n") or 0) >= 100 and r.get("p50") and g[:2] == GEOID_SELF[:2]]
    _sc.sort(reverse=True)
    _r = next((i + 1 for i, (_, g) in enumerate(_sc) if g == GEOID_SELF), None)
    _sn = html.escape(STATE_NAMES[_ab])
    cmp_line = (f'<p class="cmp">That is {_pct_vs(P["p50"], _sagg["policies"]["p50"], "state")} the {_sn} median of {m("state_p50", money(_sagg["policies"]["p50"]))}'
                + (f' and {_pct_vs(P["p50"], US_P50, "us")} the U.S. median of {m("us_p50", money(US_P50))}' if US_P50 else "")
                + (f'; {m("cost_rank", _rank(_r, len(_sc)))} of {m("rank_n", str(len(_sc)))} {_sn} {UNITS}' if _r else "") + ".</p>")
if IS_STATE:
    _st_all = sorted(STATE_NAMES.items(), key=lambda kv: kv[1])
    _i = next((i for i, (a, n) in enumerate(_st_all) if n == CS), 0)
    _nb = [_st_all[(_i + d) % len(_st_all)] for d in (-3, -2, -1, 1, 2, 3)]
    sib_html = ("<nav class='sib'><b>Other states:</b> " + " · ".join(f'<a href="../{state_slug(a)}/">{html.escape(n)}</a>' for a, n in _nb)
                + ' · <a href="../../">all states</a></nav>')
elif siblings:
    _lbl = f"Other {html.escape(_state)} counties" if len(_same) >= 3 else "Compare other counties"
    sib_html = (f"<nav class='sib'>{_state_link}<b>{_lbl}:</b> " +
                " · ".join(f'<a href="../{p["slug"]}/">{html.escape(p["short"])}</a>' for p in siblings) +
                ' · <a href="../../">all places</a></nav>')
else:
    sib_html = f'<nav class="sib">{_state_link}<a href="../../">Browse all places by state →</a></nav>'
# Federal source catalog — single source of truth for the citation schema AND the visible sources block.
ISO_DATE = (P.get("retrieved") or "2026-10-22")   # ISO date the federal data was last pulled
_pulls = [ISO_DATE] + [str((data.get(k) or {}).get("retrieved") or "") for k in ("claims_extra", "storm_events", "multiloss")]
LATEST_PULL = pretty_date(max(d for d in _pulls if d[:4].isdigit()))
# The page's dataset list is DERIVED from what its panels cite (src() records USED). The inline cards in the
# template below build their source lines while the f-string renders, so the list, its count and the JSON-LD
# citation are placeholders filled after HTML exists. A dataset no panel cites can no longer be listed.
def page_sources():
    seen = []
    for k in USED:
        ds = MX.METRICS[k]["dataset"]
        if ds not in seen: seen.append(ds)
    return [MX.DATASETS[d][:2] for d in MX.DATASETS if d in seen]
sources_li = "@@SOURCES_LI@@"
# JSON-LD: Dataset + Place + FAQPage + Breadcrumb
_faq = [
    (f"How much is flood insurance in {CS}?",
     f"Existing single-family NFIP policyholders pay a median {money(P['p50'])} a year, with the middle "
     f"half between {money(P['p25'])} and {money(P['p75'])}. This is what current policies cost, not a quote."),
    (f"Is {CS} flood insurance below FEMA's full-risk price?",
     f"{P['share_below']}% of single-family policies pay a premium below FEMA's full-risk premium "
     f"(median full-risk {money(P['frp_median'])} vs median premium {money(PREM_MED)}, premiums only)."),
    (f"How many flood claims has {CS} had?",
     f"{num(C['rows'])} NFIP flood claims between {C['year_min']} and {C['year_max']}, which paid {money(C['total_paid'])} in total."),
]
# provenance: we download every record FEMA publishes for the place and recompute; say so, with the counts
_man = agg.get("manifest") or {}
_mp, _mc = _man.get("policies") or {}, _man.get("claims") or {}
_pulled = pretty_date(_mp["pulled"]) if _mp.get("pulled") else RETR
PROV_OK = bool(_mp.get("complete") and _mc.get("complete") and not _mp.get("missing") and not _mc.get("missing"))
prov_line = (f'<p class="prov">Built from all {tp("records_policies", "manifest.policies.unique_fetched")} in-force NFIP policy records and '
             f'{tp("records_claims", "manifest.claims.unique_fetched")} claim records FEMA publishes for {CS}, downloaded {_pulled} and '
             f'matched to FEMA\'s own count, none missing. <a href="data.csv">Download the figures on this page (CSV)</a> · '
             f'<a href="../../methodology/">How we check them</a></p>') if PROV_OK else ""
jsonld = json.dumps([
    {"@context": "https://schema.org", "@type": "Dataset",
     "name": f"NFIP flood insurance data for {CL}", "url": CANON,
     "description": META_DESC + (f" Computed from a full download of {_mp['unique_fetched']:,} in-force NFIP policy records and "
                                 f"{_mc['unique_fetched']:,} NFIP claim records (OpenFEMA NfipPolicies v3 and NfipClaims v3), "
                                 "reconciled to FEMA's published record count." if PROV_OK else ""),
     "measurementTechnique": "Full record-level download of OpenFEMA NfipPolicies v3 and NfipClaims v3, deduplicated by record id, reconciled to the API's record count, recomputed offline",
     "variableMeasured": ["annual policy cost (premium plus fees)", "full-risk premium", "flood zone", "NFIP claims paid", "claim non-payment reason", "building replacement cost"],
     "temporalCoverage": f"{C['year_min']}/{C['year_max']}",
     "spatialCoverage": {"@type": "Place", "name": CL},
     "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": CANON + "data.csv"}],
     "keywords": ["flood insurance", "NFIP", "FEMA", CS],
     "creator": {"@type": "Organization", "name": "FEMA OpenFEMA"},
     "publisher": {"@type": "Organization", "name": "Flood Insurance Data", "url": BASE_URL},
     "dateModified": ISO_DATE, "datePublished": ISO_DATE,
     "citation": "@@CITATION@@",
     "isBasedOn": "https://www.fema.gov/about/openfema/data-sets", "license": "https://www.fema.gov/about/openfema/terms-conditions"},
    {"@context": "https://schema.org", "@type": "Place", "name": CL,
     "address": {"@type": "PostalAddress", "addressRegion": agg.get("nri", {}).get("state") if agg.get("nri") else None, "addressCountry": "US"}},
    {"@context": "https://schema.org", "@type": "FAQPage",
     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in _faq]},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Flood insurance", "item": f"{BASE_URL}/flood-insurance/"},
        {"@type": "ListItem", "position": 2, "name": CS, "item": CANON}]},
])
# quote-compare widget (client-side; a position in the distribution, never a quote)
quote_widget = f"""<section class="card" id="compare"><h2>Is my quote or renewal normal here?</h2>
<p class="stand">Type your yearly flood cost (premium plus fees, as on your bill) to see where it sits among {CS}'s existing single-family policies. This is a comparison, not a quote.</p>
<input id="q" type="number" inputmode="numeric" placeholder="e.g. 1800" aria-label="Your annual premium in dollars"
 style="font-size:18px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;width:160px">
<p id="qout" class="note" style="margin-top:10px">Enter an amount above.</p>
<script>
var P={{p25:{P['p25']},p50:{P['p50']},p75:{P['p75']},p90:{P['p90']}}};
var el=document.getElementById('q'),out=document.getElementById('qout');
el.addEventListener('input',function(){{
  var v=parseFloat(el.value);
  if(!v||v<=0){{out.textContent='Enter an amount above.';return;}}
  var msg;
  if(v< P.p25) msg='below the lowest quarter — cheaper than about 75% of existing policies here.';
  else if(v< P.p50) msg='in the lower-middle — cheaper than about half of existing policies here.';
  else if(v< P.p75) msg='in the upper-middle — more than about half of existing policies here.';
  else if(v< P.p90) msg='in the top quarter — more than about 75% of existing policies here.';
  else msg='above the 90th percentile — among the highest here.';
  out.textContent='$'+v.toLocaleString()+' is '+msg+' (middle half $'+P.p25.toLocaleString()+' to $'+P.p75.toLocaleString()+', typical $'+P.p50.toLocaleString()+').';
}});
</script></section>"""

# ---- OG social/citation card (PIL): branded 1200x630 PNG so shares + AI cards aren't blank ----
def write_og(dirpath):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return None
    def font(sz, bold=True):
        for p in (("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
        return ImageFont.load_default()
    img = Image.new("RGB", (1200, 630), (14, 74, 97)); d = ImageDraw.Draw(img)
    d.text((70, 66), "FLOOD INSURANCE DATA", font=font(30), fill=(188, 212, 223))
    d.text((70, 140), CL, font=font(60), fill=(255, 255, 255))
    d.text((70, 250), f"Median NFIP cost  {money(P['p50'])}/yr", font=font(50), fill=(255, 255, 255))
    if P.get("share_below") is not None:
        d.text((70, 330), f"{P['share_below']}% pay below FEMA's full-risk price", font=font(34), fill=(194, 89, 31))
    d.text((70, 520), "Public federal data · sourced & dated · not a quote", font=font(26, False), fill=(159, 192, 210))
    try: img.save(os.path.join(dirpath, "og.png")); return "og.png"
    except Exception: return None
OG = write_og(os.path.dirname(os.path.abspath(OUT_HTML)))
_og_meta = (f'<meta property="og:image" content="{CANON}og.png">'
            '<meta name="twitter:card" content="summary_large_image">') if OG else '<meta name="twitter:card" content="summary">'

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flood insurance cost in {CL}: {money(P['p50'])} median a year (FEMA data)</title>
<meta name="description" content="{html.escape(META_DESC)}">
<link rel="canonical" href="{CANON}">
<meta property="og:type" content="website"><meta property="og:title" content="Flood insurance in {html.escape(CL)}">
<meta property="og:description" content="{html.escape(META_DESC)}"><meta property="og:url" content="{CANON}">
{_og_meta}
<script type="application/ld+json">{jsonld}</script>
<style>
:root{{--bg:#f4f7f8;--surface:#fff;--ink:#132029;--mut:#55656f;--faint:#7d8c96;--line:#dbe3e7;
 --serif:"Iowan Old Style","Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;
 --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
 --brand:#15617f;--brand-d:#0e4a61;--accent:#c2591f;--bar:#9fc0d2;--r:14px;--gut:20px;
 --shadow:0 1px 2px rgba(16,32,43,.05),0 6px 20px rgba(16,32,43,.06)}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.62 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:740px;margin:0 auto;padding:0 var(--gut)}}
a{{color:var(--brand)}}
.topbar{{background:var(--brand-d)}}.topbar .wrap{{display:flex;gap:12px;align-items:baseline;padding:11px var(--gut)}}
.topbar .brand{{color:#fff;font-weight:800;text-decoration:none;letter-spacing:.2px}}
.topbar .crumb{{color:#bcd4df;font-size:13px}}
.hero{{padding:30px 0 6px}}
.hero h1{{font-family:var(--serif);font-weight:600;font-size:36px;line-height:1.1;margin:.1em 0 .3em;letter-spacing:-.01em}}
.cmp{{font-size:15px;margin:2px 0 10px;color:var(--ink)}}
.prov{{font-size:13.5px;color:var(--mut);border-left:3px solid var(--brand);padding:2px 0 2px 10px;margin:10px 0}}
.kicker{{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin:0}}
.lede{{color:var(--mut);font-size:16.5px;margin:.2em 0 1.1em;max-width:62ch}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:0 0 14px}}
.stat{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.stat .n{{font-family:var(--serif);font-size:27px;font-weight:600;letter-spacing:-.01em;font-variant-numeric:tabular-nums;line-height:1.15}}
.stat .l{{font-size:11.5px;color:var(--faint);margin-top:3px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}}
.chips{{margin:2px 0 10px}}
.chip{{display:inline-block;background:#dde8ee;color:var(--brand-d);border-radius:999px;padding:4px 12px;font-size:12.5px;margin:0 6px 6px 0;font-weight:600}}
.caveat{{color:var(--mut);font-size:14px;margin:.2em 0 1.1em;max-width:62ch}}
.btn{{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:10px;box-shadow:var(--shadow)}}
.btn:hover{{filter:brightness(.96)}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin:18px 0}}
.card h2{{font-family:var(--serif);font-size:24px;font-weight:600;line-height:1.2;margin:0 0 6px;letter-spacing:-.005em}}
.stand{{margin:0 0 14px}}
.src{{color:var(--faint);font-size:12px;margin:14px 0 0;border-top:1px solid var(--line);padding-top:9px}}
.gap{{color:#9a3d12;font-size:14px;background:#fbf0e9;border:1px solid #f0d9c9;border-radius:9px;padding:10px 13px}}
.note{{color:var(--mut);font-size:13.5px;margin:.6em 0 0}}
ul.kv{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}}
ul.kv li{{display:flex;flex-direction:column;background:#f5f8fb;border:1px solid var(--line);border-radius:10px;padding:11px 13px}}
ul.kv b{{order:2;font-weight:600;color:var(--faint);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;margin-top:3px}}
ul.kv span{{order:1;font-family:var(--serif);font-size:22px;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:4px}}
th,td{{padding:9px 10px;text-align:left}}
thead th{{color:var(--faint);font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--line)}}
tbody tr:nth-child(odd){{background:#f5f8fb}}
td:nth-child(n+2),thead th:nth-child(n+2){{text-align:right;font-variant-numeric:tabular-nums}}
svg{{display:block;margin:6px 0}}
.ax{{fill:var(--mut);font-size:13px;text-anchor:middle}}.ax2{{fill:var(--faint);font-size:13px}}
nav.jump{{font-size:14px;margin:0 0 12px;display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center}}
nav.jump a{{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:5px 11px;text-decoration:none;font-weight:600}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
nav.sib{{font-size:14px;color:var(--mut);margin:16px 0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px}}
nav.sib a{{color:var(--brand);font-weight:600}}
footer{{color:var(--faint);font-size:12.5px;margin:28px 0;border-top:1px solid var(--line);padding-top:14px}}
footer a{{color:var(--mut)}}
details.more{{margin:16px 0}}details.more>summary{{cursor:pointer;font-weight:700;color:var(--brand);padding:12px 0;list-style:none}}
details.more>summary::-webkit-details-marker{{display:none}}details.more>summary:before{{content:"▸ "}}details.more[open]>summary:before{{content:"▾ "}}
@media(max-width:620px){{.stats{{grid-template-columns:repeat(2,1fr)}}.two{{grid-template-columns:1fr}}.hero h1{{font-size:30px}}
.card{{padding:18px 15px}}.card h2{{font-size:21px}}.stat .n{{font-size:23px}}ul.kv span{{font-size:19px}}ul.kv b{{font-size:11px}}
table{{font-size:13.5px}}th,td{{padding:7px 6px}}thead th{{font-size:11px;white-space:normal}}
table{{width:100%}}}}
</style></head><body>
<header class="topbar"><div class="wrap"><a class="brand" href="../../">Flood Insurance Data</a><span class="crumb">Flood insurance › {(f'<a href="../{state_slug(_state)}/" style="color:inherit">{html.escape(STATE_NAMES[_state])}</a> › ' if (not IS_STATE and _state in _built_states) else '')}{CS}</span></div></header>
<main class="wrap">
<section class="hero">
<p class="kicker">NFIP records · {CS} · policies as of {POL_ASOF}</p>
<h1>Flood insurance in {CL}</h1>
<p class="lede">What policyholders here actually pay, what floods have paid out, and how to pay less, from public federal records.</p>
<div class="stats">
<div class="stat"><div class="n">{m('cost_p50', money(P['p50']))}</div><div class="l">Median / yr</div></div>
<div class="stat"><div class="n">{m('cost_mo', median_mo)}</div><div class="l">Per month</div></div>
<div class="stat"><div class="n">{m('cost_p25', money(P['p25']))}–{m('cost_p75', money(P['p75']))}</div><div class="l">Middle half</div></div>
<div class="stat"><div class="n">{m('share_below', str(P['share_below']) + '%')}</div><div class="l">Pay under FEMA's full-risk price</div></div>
</div>
<nav class="jump"><b>Jump to:</b> <a href="#required">Am I required?</a> <a href="#zone-cost">Cost in my zone</a> <a href="#compare">Is my quote normal?</a> <a href="#covered">How to buy / already flooded</a></nav>
{cmp_line}
<p class="caveat">This is what existing single-family policies cost — not a quote. Your own premium depends on your building, coverage and elevation.</p>
<a class="btn" href="https://msc.fema.gov/portal/home" rel="nofollow noopener" target="_blank">Check your address on FEMA's flood map →</a>
<p class="note">Your flood zone is set at your exact address and drives your price and whether coverage is required. Look it up first, then read your zone's row in "What does it cost in my flood zone?" below.</p>
{prov_line}
</section>

{quote_widget}

{card("Am I required to carry it?",
  rule("purchase_answer") + " Check your zone on <a href=\"https://msc.fema.gov/portal/home\" rel=\"nofollow noopener\" target=\"_blank\">FEMA's flood map</a>.",
  f"<p class='note'>{m('sfha_share', str(P['sfha_share_units']) + '%')} of {CS}'s NFIP policies are in high-risk zones (not {tp('sfha_share', 'policies.sfha_share_units', pct)} of all buildings, and not an answer about your own home).</p>"
  f"{zone_body}<p class='note'>Insured units by the flood zone each policy is rated in (a condo-building policy counts each unit). {rule('lender_any_zone')}</p>",
  src(["units", "sfha_share"], POL_ASOF, RETR) + src_rules(["purchase_answer", "lender_any_zone"]), id="required")}

{outside_note}

{card("How much does it cost here?", cost_lead, cost_body, src(["cost_p50", "prem_median", "frp_median", "coverage"], POL_ASOF, RETR))}

{howto_card}

{card("What do floods actually pay out here?", claims_lead, claims_svg() +
  f"<p class='note'>Orange bars are the three costliest years: " + ", ".join(f"{y} ({tp('claims_year_paid', f'claims.by_year.{y}.1', money, q=str(y))})" for y, p in top_paid) +
  f". Total paid {tp('claims_total', 'claims.total_paid', money, q='exact')}: net building + contents payments by year of loss. Claims are matched by the claims dataset's county code, which may not exactly match a policy's property county.</p>" + claims_ratio_note,
  src(["claims_filed", "claims_total"], f"{C['year_min']}–{C['year_max']}", RETR))}

{payout_card}

{unpaid_card}

{events_card}

{rebuild_card}

{zone_cost_card}

{zip_card}

{averages_card}

{card("How do current premiums compare with FEMA's full-risk price?", gap_lead,
  f"<ul class='kv'><li><b>Median premium charged (before fees)</b><span>{m('prem_median', money(PREM_MED))}</span></li>"
  f"<li><b>Median full-risk premium</b><span>{m('frp_median', money(P['frp_median']))}</span></li>"
  f"<li><b>Pay below full-risk</b><span>{m('share_below', str(P['share_below']) + '%')} of {tp('units_listed', 'policies.below_n', q='below_n')}</span></li></ul>" + glide_note,
  src(["prem_median", "frp_median", "share_below"], POL_ASOF, RETR))}

{trend_card}

{state_trend_card}

{card("Can I pay less than the sticker price?", crs_lead,
  (f"<table><thead><tr><th>Community</th><th>High-risk zone</th><th>Other areas</th><th>CRS class</th></tr></thead><tbody>{crs_rows}</tbody></table>" if crs_rows else "")
  + crs_none_note +
  "<p class='note'>The Community Rating System cuts NFIP premiums for every eligible policy in a community that does extra flood work. The discount shown is the community's rate; what share of its policies currently receive it is not in this data. Confirm with your agent.</p>",
  src(["crs_discount"], "current Community Status Book", RETR))}

{risk}


{storm_card}

{multiloss_card}

{tilemap_card}

{takeup_card}

{card(f"How often is {CS} a flood disaster?" if IS_STATE else f"How often is this {UNIT} a flood disaster?",
  f"{m('declarations', str(len(fh_events)))} federal disasters for floods or storms here"
  + (f"; the latest was {html.escape((recent[0].get('declarationTitle') or '').title())} ({html.escape(cal_year(recent[0]))})." if recent else "."),
  f"<ul>{recent_li}</ul><p class='note'>Distinct storms by calendar year (one storm's emergency and major-disaster declarations are counted once), not individual declaration records.</p>",
  src(["declarations"], "declarations through 2026", RETR))}

{card("Did the government pay homeowners after floods?",
  ((claim("Yes", "yes", ("ia_paid", ">", 0)) + f", but not much per household: FEMA approved {m('ia_paid', big(h_ihp))} for homeowners here, "
    f"about {m('ia_per_reg', money(h_ihp / h_regs))} per registration"
    + (f", against an average paid flood claim of {m('avg_paid', money((data.get('claims_extra') or {})['avg_paid']))}"
       if (data.get('claims_extra') or {}).get('avg_paid') else "") + ".")
   if h_ihp and h_regs else "No FEMA housing aid to homeowners here is on record."),
  f"<p class='note'>{rule('ia_partial')}</p>",
  src(["ia_paid", "ia_regs"] + (["avg_paid"] if (data.get('claims_extra') or {}).get('avg_paid') and h_ihp and h_regs else []),
      "owner registrations by disaster", RETR))}

{card("Reconciliation &amp; data completeness", ("Our counts are checked against FEMA's official figure and the API's own totals." if OFFICIAL
  else "Our record counts match the API's own totals; FEMA's official policy count is not yet joined for " + CS + "."),
  f"<p class='note'>In-force count: {tp('units', 'policies.units')} policy units (from {tp('records_total', 'policies.rows', q='rows')} API records; condo-association records carry more than one unit). " +
  (f"FEMA's official count for July 31, 2026 was {m('official_count', num(OFFICIAL))}: a {m('official_diff', str(round(abs(P['units']-OFFICIAL)/OFFICIAL*100,1)) + '%')} difference. " if OFFICIAL else "") +
  f"Count reconciliation (not a snapshot proof): {mani_line}.</p>")}

<section class="card"><h2>What this data cannot tell you</h2>
<ul class="note">
<li>Your own premium — it depends on elevation, coverage and deductible. We show where existing policies fall.</li>
<li>Private (non-NFIP) flood insurance prices.</li>
<li>Your address's exact flood zone — use FEMA's Flood Map Service Center.</li>
<li>Why any one premium changes — we show the gap to full-risk, not the cause.</li>
<li>A year-over-year premium trend — the in-force snapshot holds only current-term policies, so a like-for-like multi-year index isn't possible from this data. A per-effective-year median is shown only where several years of policies exist.</li>
</ul></section>

<section class="card"><h2>The federal datasets behind this page</h2>
<p class="stand">Every figure comes from a public U.S. federal dataset; estimates are labeled where they appear. This page joins <span data-m="n_sources">@@N_SOURCES@@</span> of them for {CS}. Last pulled {LATEST_PULL}.</p>
<ul class="srclist">{sources_li}</ul></section>

{sib_html}

<footer>{ATTR} Place names via GeoNames (CC BY 4.0). Figures are aggregates, never individual quotes or records.
<a href="../../about/">About</a> · <a href="../../methodology/">Methodology</a> · <a href="../../data/">Download the data</a> · <a href="../../privacy/">Privacy</a> · <a href="../../terms/">Terms</a></footer>
</main></body></html>"""

SOURCES = page_sources()
HTML = (HTML.replace("@@SOURCES_LI@@", "".join(f'<li><a href="{u}">{html.escape(n)}</a></li>' for n, u in SOURCES))
            .replace("@@N_SOURCES@@", str(len(SOURCES)))
            .replace('"@@CITATION@@"', json.dumps([{"@type": "Dataset", "name": n, "url": u} for n, u in SOURCES])))
open(OUT_HTML, "w", encoding="utf-8").write(HTML)
# data.csv next to the page: exactly the tagged figures the page shows, each with its dataset and FEMA fields
import csv
with open(os.path.join(os.path.dirname(OUT_HTML), "data.csv"), "w", newline="", encoding="utf-8") as _f:
    _w = csv.writer(_f); _w.writerow(["place", "metric", "value", "unit", "dataset", "fields", "policies_as_of"]); _seen = set()
    for _k, _v in re.findall(r'<span data-m="(\w+)"[^>]*>(.*?)</span>', HTML):
        if _k in _seen: continue
        _seen.add(_k); _d = MX.METRICS[_k]
        _w.writerow([CL, _k, html.unescape(re.sub("<[^>]+>", "", _v)), _d["unit"], MX.DATASETS[_d["dataset"]][0], " + ".join(_d["fields"]), POL_ASOF])
print("wrote", OUT_HTML, len(HTML), "bytes; NRI:", "yes" if NRI else "GAP",
      "; zones=policyUnits; completeness", mani_ok)
