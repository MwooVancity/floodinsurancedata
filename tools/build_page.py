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
from notes import how

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
ATTR = ("This product uses the Federal Emergency Management Agency's OpenFEMA API, "
        "but is not endorsed by FEMA.")

def money(n): return "$" + format(int(n + 0.5) if n >= 0 else -int(-n + 0.5), ",") if n is not None else "—"   # half rounds up ($90.50 -> $91), not Python's half-to-even
def big(n):
    """Readable large amounts for sentences: $68.9 million / $1.2 billion (exact figures stay in the details)."""
    if n is None: return "—"
    if n >= 1e9: return f"${n / 1e9:.1f} billion"
    if n >= 1e6: return f"${n / 1e6:.1f} million"
    return money(n)
def and_list(xs): xs = [str(x) for x in xs]; return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
def num(n): return format(int(n), ",") if n is not None else "—"
def _retr():   # no typed fallback: a page without its download date fails here instead of printing a stale one
    return pretty_date(agg["manifest"]["policies"]["pulled"])
def pretty_date(s):
    """'2026-10-25' -> 'October 25, 2026' so every block shows one date format; other text passes through."""
    import datetime
    try: d = datetime.date.fromisoformat(str(s)[:10]); return f"{d:%B} {d.day}, {d.year}"
    except ValueError: return s
_SF = os.environ.get("FF_GEOID", "12071")[:2]
UNIT, UNITS = {"22": ("parish", "parishes"), "02": ("borough", "boroughs")}.get(_SF, ("county", "counties"))
RETR = _retr()
POL_ASOF = pretty_date(P["asof"])   # the snapshot date in the data, not a typed one   # the day this place's records were downloaded (state pages); the county collect date otherwise
def src(keys, effective, retrieved):
    """A panel's source line, built from the metrics it shows (metrics.py), never typed by hand."""
    effective, retrieved = pretty_date(effective), pretty_date(retrieved)
    # the OpenFEMA credit is printed once, in the footer, not under every card (it was ~9 identical copies per page)
    return (f'<p class="src" data-src="{",".join(keys)}">Source: {"; ".join(MX.sources_for(keys))}. '
            + (f'Data effective {effective}' if re.match(r"(\d|[A-Z][a-z]+ \d)", str(effective)) else f'Data: {effective}')
            + f'; retrieved {retrieved}.</p>')
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

# ---- declarations: distinct flood/storm events (by disasterNumber), not records ----
decl = data.get("declarations", [])
fh = [d for d in decl if MX.flood_decl(d)]
def _tc(t):   # title case that reads like a name: "St. John the Baptist Parish", "Severe Storms and Flooding", "Lafayette City-Parish"
    t = re.sub(r"\s*-\s*", "-", t.strip()).title()
    return re.sub(r"(?<=\S) (Of|The|And|At|In|On|For|To|A)\b", lambda mm: " " + mm.group(1).lower(), t)
def _dtitle(d):   # "KS-FLOODING 10/31/98" / "NY - SEVERE WX, SEPT 7, 1998" -> "Flooding" / "Severe Wx" (the year is shown beside it)
    t = re.sub(r"^[A-Z]{2}\s*-\s*", "", (d.get("declarationTitle") or d.get("incidentType") or "").strip())
    t = re.sub(r",?\s*\b\d{1,2}/\d{1,2}(/\d{2,4})?\b|,?\s*\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEPT?|OCT|NOV|DEC)[A-Z]*\.?\s+\d{1,2}(,\s*\d{4})?", "", t, flags=re.I)
    t = re.sub(r"\s*\b(of\s+)?'?\d{2,4}\b", "", t, flags=re.I)   # stray years ("1996", "Blizzard Of 96"); the year is shown beside it
    t = re.sub(r"\s+\d{1,2}$", "", t.strip(" ,-"))   # stress test: "AR SEVERE WEATHER 1" (FEMA's sequence number) left a stray figure
    return _tc(t.strip(" ,-"))
def cal_year(d):
    # CALENDAR year from declarationDate — NOT fyDeclared (FEMA's federal fiscal year, which rolls to
    # the next year on Oct 1 and would mislabel an Oct 2026 event as "2027").
    s = d.get("declarationDate") or ""
    return s[:4] if len(s) >= 4 and s[:4].isdigit() else (str(d.get("fyDeclared")) if d.get("fyDeclared") else "")
def event_key(d):
    # FEMA can issue an emergency (EM) and a major-disaster (DR) number for ONE named storm, sometimes with different
    # type labels ("Hurricane Helene" / "Tropical Storm Helene"): those merge. Every other declaration is its own
    # event by disaster number (round 11: generic titles a year apart merged eight separate Louisiana disasters).
    t = (d.get("declarationTitle") or "").upper().strip()
    mm = re.match(r"(?:HURRICANE|TROPICAL STORM|TROPICAL DEPRESSION)\s+([A-Z]+)\b", t)
    return ("storm", mm.group(1)) if mm else ("number", str(d.get("disasterNumber")))
# a named storm declared across a year boundary (Tropical Storm Zeta Oct 2020, Hurricane Zeta Jan 2021) is ONE event,
# shown under its first declaration's year
_ev_first = []
_seen_num = set()
for d in sorted(fh, key=lambda x: x.get("declarationDate") or ""):
    if d.get("disasterNumber") in _seen_num: continue   # one row per county per disaster: count the disaster once
    _seen_num.add(d.get("disasterNumber"))
    y, n = cal_year(d), event_key(d)
    hit = next((i for i, (y2, n2, _) in enumerate(_ev_first) if n[0] == "storm" and n == n2 and y.isdigit() and y2.isdigit() and abs(int(y) - int(y2)) <= 1), None)
    if hit is None: _ev_first.append((y, n, d))
    elif d.get("declarationType") == "DR" and _ev_first[hit][2].get("declarationType") != "DR":
        # the major-disaster title names the storm as it hit ("Hurricane Ida"); the earlier emergency title is pre-landfall
        _ev_first[hit] = (_ev_first[hit][0], n, dict(d, declarationDate=_ev_first[hit][2].get("declarationDate")))
fh_events = {(y, n) for y, n, _ in _ev_first}
# housing aid only from flood/storm disasters (not COVID, ice storms, fires, tornadoes)
_fh_nums = {d.get("disasterNumber") for d in fh}
h_rows = [r for r in h_rows if r.get("disasterNumber") in _fh_nums]
h_regs = sum(int(r.get("validRegistrations") or 0) for r in h_rows)
h_ihp = sum(float(r.get("totalApprovedIhpAmount") or 0) for r in h_rows)
h_disasters = len(set(r.get("disasterNumber") for r in h_rows))
recent = [d for _, _, d in reversed(_ev_first)][:6]

_crs_all = sorted(data.get("crs", []), key=lambda x: -(int((x.get("sfhaDiscount") or "0%").rstrip("%") or 0)))
crs = [c for c in _crs_all if c.get("participatingInNFIP") is not False]   # the discount lists: NFIP communities only
crs_out = [c for c in _crs_all if c.get("participatingInNFIP") is False]   # not in the NFIP: no policy can be bought there

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
    maxp = max(by[str(y)][1] for y in years) or 1   # bar height = dollars paid, the measure the caption and orange bars name
    for y in years:
        c = by[str(y)][0]; x = pad + (y - y0) / span * (W - 2 * pad - bw); bh = (by[str(y)][1] / maxp) * (H - 2 * pad - 8)
        col = "var(--accent)" if any(y == ty for ty, _ in top_paid) else "var(--bar)"
        bars.append(f'<rect x="{x:.1f}" y="{H-pad-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"><title>{y}: {num(c)} claims, {money(by[str(y)][1])}</title></rect>')
    labs = "".join(f'<text x="{pad+(y-y0)/span*(W-2*pad-bw):.1f}" y="{H-2}" class="ax">{y}</text>' for y in range(((y0+9)//10)*10, y1+1, 10))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="NFIP claim dollars paid per year">'
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
                      [("p25", "cost_p25", "A quarter pay under"), ("p50", "cost_p50", "Typical"), ("p75", "cost_p75", "A quarter pay over"), ("p90", "cost_p90", "A tenth pay")] if P.get(k))
    return (f'<svg viewBox="0 0 {W} {H - 20}" width="100%" role="img" aria-label="Annual NFIP cost spread">'
            f'<line x1="{pad}" y1="46" x2="{W-pad}" y2="46" stroke="var(--line)"/>{rng}{marks}{frpline}</svg>'
            f'<p class="note" style="margin-top:0">{vals}{" or more" if p90 else ""}</p>')

ROOT_DATA = dict(agg, data=data, extras=EXTRAS, const=MX.CONST)   # what tp() reads and the gate re-reads
from agg_raw import NAMES as STATE_NAMES, slug as state_slug
_SD = os.path.join(os.path.dirname(HERE), "data", "states", state_slug(agg["state"])) if agg.get("level") == "county" and agg.get("state") in STATE_NAMES else ""
if _SD and os.path.exists(os.path.join(_SD, "agg.json")):   # the county's state, so each figure can sit beside the state's own
    ROOT_DATA["state"] = {f: json.load(open(os.path.join(_SD, f + ".json"))) for f in ("agg", "data", "extras") if os.path.exists(os.path.join(_SD, f + ".json"))}
def _get(path):
    v = ROOT_DATA
    for seg in path.split("."):
        v = v[int(seg)] if isinstance(v, list) else v[seg]
    return v
def pct(v): return f"{v}%"
def tp(key, path, fmt=num, q=None):
    """The one way to print a figure read from the data: the gate re-reads the same path (V2)."""
    return m(key, fmt(_get(path)), path, q)
def vs_state(key, path, fmt=num):
    """County pages: the state's figure for the same measure, under the county's tile ("Hawaii: $41,200")."""
    try: v = _get("state." + path)
    except (KeyError, IndexError, TypeError): return ""
    if v is None: return ""
    return f"<small class='vs'>{html.escape(STATE_NAMES[agg['state']])}: {tp(key, 'state.' + path, fmt, q='state')}</small>"

def card(title, standfirst, body, source="", id=""):
    # every card is linkable (the "On this page" menu): a given id, else one made from the title
    id = id or "c-" + re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub("<[^>]+>", "", title)).lower()).strip("-")[:40]
    _id = f' id="{id}"'
    return f'<section class="card"{_id}><h2>{title}</h2><p class="stand">{standfirst}</p>{body}{source}</section>'

# ---- risk card (NRI or honest gap) ----
ABSENT = {None, "", "Not Applicable", "Insufficient Data", "No Rating", "No Expected Annual Losses"}
def _present(v): return v not in ABSENT and str(v).strip() not in ABSENT
def card_risk():
    cf = (NRI or {}).get("coastal", {}); inl = (NRI or {}).get("inland", {})
    have_risk = NRI and (_present(cf.get("risk_rating")) or _present(inl.get("risk_rating")))
    if have_risk:
        # headline = the plain rating word; the modeled-loss dollars + percentile are demoted into a plain note
        # (kept, not hidden — just not near-top jargon noise).
        def rating_row(block, label):
            rr = block.get("risk_rating")
            return f"<li><b>{label} flood risk rating (FEMA)</b><span>{html.escape(str(rr))}</span></li>" if _present(rr) else ""
        def _detail(block, label):
            pctl, eald = block.get("eal_national_pctl"), block.get("eal_total_usd")
            if not _present(block.get("risk_rating")): return ""
            bits = []
            # NRI's *_ALR_NPCTL is the loss RATE percentile (loss per dollar of building value), not total loss: say so
            if isinstance(eald, (int, float)) and eald > 0: bits.append(f"FEMA models roughly {tp('nri_eal_usd', 'nri.' + label.lower() + '.eal_total_usd', big, q=label.lower())} of flood loss a year (buildings, people and farmland valued in dollars, insured or not; a model, not insurance payouts)")
            if isinstance(pctl, (int, float)): bits.append(f"a separate FEMA measure, loss per dollar of building value: {label.lower()} flood loss here is higher than in about {m('nri_eal_pctl_' + label.lower(), str(round(pctl)) + '%')} of U.S. counties")   # stress test: equal coastal/inland percentiles printed one sentence twice
            return (f" {label}: " + "; ".join(bits) + ".") if bits else ""
        risk_body = ("<ul class='kv'>" + rating_row(cf, "Coastal") + rating_row(inl, "Inland") + "</ul>"
                     "<p class='note'>FEMA's rating weighs modeled loss with social vulnerability and community resilience; it is not a "
                     "prediction for your home, and it can differ from the loss percentile below."
                     + _detail(cf, "Coastal") + _detail(inl, "Inland") +
                     " Loss figures model all flood loss, insured or not, so they run far above insurance payouts." + how("nri") + "</p>")
        parts = []
        if _present(cf.get("risk_rating")): parts.append(f"{html.escape(str(cf['risk_rating']))} for coastal flooding")   # same order as the tiles
        if _present(inl.get("risk_rating")): parts.append(f"{html.escape(str(inl['risk_rating']))} for inland (river) flooding")
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
    elif _sea_line(): risk = risk.replace("</section>", _sea_line() + src(["sea_trend"], "NOAA's published trends", RETR) + "</section>", 1)
    return risk

def _sea_line():   # PLAN 3e: NOAA's published sea-level trend at a tide gauge in this county, else in a bordering one
    try:
        sl = json.load(open(os.path.join(os.path.dirname(HERE), "data", "us", "sealevel.json"), encoding="utf-8"))
        adj = json.load(open(os.path.join(os.path.dirname(HERE), "data", "us", "county_adjacency.json"), encoding="utf-8"))
    except Exception: return ""
    g = agg.get("geoid") or ""
    here = sl.get(g) or []
    st = here[:3]   # round 28: a gauge in the county only; a bordering county can be on the other coast (Broward/Collier)
    if not st: return ""   # no gauge in the county: nothing, never a far-away gauge
    def one(s, i):   # a signed figure, no direction word (gate B2); Alaska trends are negative (land rising)
        t = s["trend"]
        return (f"NOAA's tide gauge at {m('sea_trend', html.escape(s['name']), q=s['station'] + '_name')} measured a sea-level trend of "
                f"{m('sea_trend', f'{t:+.2f}', q=s['station'])} inches per decade (give or take {m('sea_trend', f'{s['error']:.2f}', q=s['station'] + '_err')} inches per decade) "
                f"from {m('sea_trend', s['start'][-4:], q=s['station'] + '_from')} to {m('sea_trend', s['end'][-4:], q=s['station'] + '_to')}")
    where = ""
    return (f"<p class='note'><b>Local sea level:</b> " + "; ".join(one(s, i) for i, s in enumerate(st)) + where
            + ". A plus sign means the water there got higher over that period. A tide gauge measures one spot on the coast; it is not your property's flood risk.</p>")

# ---- zone card (policy UNITS) ----
def _zone_body():
    zu = P["zone_units"]
    # compact table: zones holding >=1% of units; the rest fold into one disclosed "other" row (phone-friendly)
    _zshown = [(z, v) for z, v in list(zu.items())[:8] if v >= 0.01 * P["units"]]
    _zshown_k = {z for z, _ in _zshown}
    # VE, AH, AO, A01-A30...: still high-risk. From the full high-risk total, because zone_units keeps only the largest zones
    _zrest_hr = (P.get("sfha_units") or 0) - sum(v for z, v in _zshown if z[:1] in "AV")
    _zrest = P["units"] - sum(v for _, v in _zshown) - _zrest_hr   # units in other low-risk or unclassified zones
    def _zrow(label, v, z):
        _u = tp("zone_units", "policies.zone_units." + z, num, q=z) if z not in ("other", "other_hr") else m("zone_units", num(v), q=z)
        return f"<tr><td>{label}</td><td>{_u}</td><td>{m('zone_share', str(round(100 * v / P['units'], 1)) + '%', q=z)}</td></tr>"
    _hr_l = [z for z, v in sorted(zu.items(), key=lambda kv: -kv[1]) if z not in _zshown_k and z[:1] in "AV"]
    _hr_names = ", ".join(_hr_l[:4]) + (" and others" if len(_hr_l) > 4 else "")
    zone_body = ("<table><thead><tr><th>Flood zone</th><th>Policy units</th><th>Share</th></tr></thead><tbody>"
        + "".join(_zrow(f"Zone {html.escape(z)}" + (" (high-risk)" if z[:1] in "AV" else ""), v, z) for z, v in _zshown)
        + (_zrow(f"Other high-risk zones ({html.escape(_hr_names)})", _zrest_hr, "other_hr") if _zrest_hr > 0 else "")
        + (_zrow("Other low-risk or unclassified zones", _zrest, "other") if _zrest > 0 else "")
        + "</tbody></table><p class='note'>Every zone starting with A or V is high-risk, including older numbered labels "
          "such as A1 to A30 from older flood maps (newer maps use AE for the same kind of area). Policies keep the label "
          "they were rated with, so the old labels are counted on their own.</p>")
    return zone_body

# suppress on VALID COST observations (cost_n), not raw cohort — a cohort full of null/refund costs
# must not get a spread. agg carries spread_ok = cost_n >= 100.
PREM_MED = P.get("prem_median")        # premium charged, before fees: the like-for-like comparator for full-risk
median_mo = money(P['p50'] / 12) if P.get("p50") else None
def _cost_parts():
    SMALL_COHORT = not P.get("spread_ok", (P.get("cost_n") or 0) >= 100)
    if SMALL_COHORT:
        cost_lead = (f"Only {tp('cost_n', 'policies.cost_n')} single-family primary-residence NFIP policies in {CS} have a valid "
                     f"recorded cost — too few for a reliable spread, so we show the count and median only. "
                     f"Median annual cost {m('cost_p50', money(P['p50']))}.")
        cost_body = (f"<ul class='kv'><li><b>Policies with a valid cost</b><span>{tp('cost_n', 'policies.cost_n')}</span></li>"
                     f"<li><b>Median annual cost</b><span>{m('cost_p50', money(P['p50']))}</span></li></ul>"
                     f"<p class='note'>Suppressed percentile spread: fewer than {tp('threshold', 'const.spread_min', q='spread_min')} policies with a valid recorded cost.</p>")
    else:
        cost_lead = (f"Typically about {m('cost_p50', money(P['p50']))} a year ({m('cost_mo', money(P['p50'] / 12))} a month), "
                     f"fees included. Half of homeowners here pay between {m('cost_p25', money(P['p25']))} and "
                     f"{m('cost_p75', money(P['p75']))}. To check a quote, use the checker at the top.")
        cost_body = (spread_svg() + "<p class='note'>Each policy's annual cost (premium plus the federal policy fee, "
                     "reserve fund assessment and HFIAA surcharge), single-family primary residences. The bar is the middle "
                     "half of policies, from " + tp('cost_n', 'policies.cost_n') + " single-family primary-home policies. These are "
                     "existing policies, many still below FEMA's full-risk price.</p>")
    if P.get("coverage_building"):
        cost_body += (f"<p class='note'><b>Coverage in force:</b> {tp('coverage', 'policies.coverage_building', big, q='building')} of building and "
                      f"{tp('coverage', 'policies.coverage_contents', big, q='contents')} of contents coverage across all {CS} policies.</p>")
    # monthly framing for the median
    return cost_lead, cost_body

# ---- cost by flood zone (median per zone) ----
def card_zone_cost():
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
            f"<table><thead><tr><th>Flood zone</th><th>Median / yr</th><th>Priced policies</th></tr></thead><tbody>{rows_}</tbody></table>"
            + f"<p class='note'>{rule('zone_codes')}</p>"
            + ("<p class='note'>Some zones share the same median because many policies here are charged exactly the same amount, "
               "so the middle policy in several zones lands on that one price. Each median is computed from that zone's own policy records.</p>" if len({d['median'] for d in czone.values()}) < len(czone) else "")
            + (("<p class='note'><b>" + claim("Why can a high-risk zone cost less than Zone X here?", "cost less than",
                                               ("zone_inversion", "==", 1)) + "</b> " + rule("rr2_zone") + "</p>")
               if VALS["zone_inversion"] else "")
            + f"<p class='note'>Zones with fewer than {tp('threshold', 'const.zone_min', q='zone_min')} priced single-family policies are omitted. Your own premium still depends on elevation and coverage.</p>",
            src(["zone_cost"], POL_ASOF, RETR) + src_rules(["zone_codes"]), id="zone-cost")
    return zone_cost_card

# ---- premium trend: REMOVED. An in-force annual-policy snapshot holds only current-term policies, so
# there are never enough distinct effective-years for an honest like-for-like trend — and showing one
# would contradict the page's own "what this data cannot tell you" note. The glide-path below is the
# sourced, rule-based answer to "is it going up?" instead. (No trend card is rendered.)

def _gap_parts():
    MX.compare("prem_median", "frp_median")   # like-for-like or it raises
    gap_lead = ((m('share_below', str(P['share_below']) + '%') + " of policies here pay less than FEMA's full-risk price, so "
                 + claim("their bills are rising", "rising", ("share_below", ">", 0)) + " toward it." if P.get("share_below") else
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
    else:   # no "years to full risk": the two medians come from different policies, so their ratio describes no real bill
        glide_note = (f"<p class='note'><b>Yearly cap:</b> {rule('glide')} {rule('cap')} Bills already at full risk "
                      "still change with FEMA's yearly rate updates.</p>")
    return gap_lead, glide_note

def _claims_parts():
    claims_lead = (f"Floods here have led to {m('claims_filed', num(C['rows']))} NFIP flood claims and "
                   f"{m('claims_total', big(C['total_paid']))} in payouts since {C['year_min']}"
                   + (f"; the worst years were {and_list(y for y, _ in top_paid)}." if top_paid else "."))
    # the ratio reads like a risk score, so it is demoted to a note with both numbers shown, never the headline.
    claims_ratio_note = (f"<p class='note'>That is {m('claims_filed', num(C['rows']))} claims since {C['year_min']} against "
                         f"{m('units', num(P['units']))} policy units in force today — a cumulative tally spanning ~{m('claims_span_years', str(C['year_max']-C['year_min']+1))} "
                         f"years over a present-day snapshot, not an annual claim rate or a flood probability.</p>")
    return claims_lead, claims_ratio_note

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
    n = re.sub(r"\s*-\s*(USE\s+CID\s*)?\d{6}.*$", "", c['communityName'].replace('*', '').strip(), flags=re.I)
    prob = bool(re.search(r"\bON PROBATION\b", n, re.I))
    n = re.sub(r"\s+ON PROBATION\b.*$", "", n, flags=re.I)
    n = re.sub(r"\s+CONSOLIDATED GOVERNMENT$", "", n, flags=re.I)   # "Lafayette City-Parish Consolidated Government" -> the name a reader uses
    return _tc(re.sub(_LEGAL, "", n, flags=re.I)) + (" (on probation)" if prob else "")
def _cname(c): return f"<span data-name>{_cname_plain(c)}</span>"
def _cname_plain(c):
    """FEMA's 'CAPE CANAVERAL, CITY OF' -> 'Cape Canaveral' (the reader looks for their town's name, not the legal form);
    two communities with one name keep their form: 'Stonington (town)', 'Stonington (borough)'."""
    n = _short(c)
    if sum(1 for o in crs if _short(o) == n) > 1:
        f = re.search(_LEGAL, c['communityName'].strip(), flags=re.I)
        if f: n += f" ({f.group(1).lower()})"
    return html.escape(n)
# table only for communities with a discount; the rest fold into one named line (a screen of "No discount" rows helps no one)
from mapdate import map_date   # PLAN 3e: FEMA map-date legend reader (tested in test_tools.py)
def _mdate(d): return f"{_MONTHS[f'{d.month:02d}']} {d.day}, {d.year}"
def _map_line():   # PLAN 3e: when this place's FEMA map took effect, and which communities get a new one (FEMA's "(>)")
    rows = [(c, *map_date(c.get("currentlyEffectiveMapDate"))) for c in _crs_all if "currentlyEffectiveMapDate" in c]
    if not rows: return ""
    new = sorted((r for r in rows if r[1] == "new"), key=lambda r: r[2])
    out = []
    if not IS_STATE:
        own = next((r for r in rows if (r[0].get("communityName") or "").endswith("*")), None)   # FEMA marks the unincorporated county "*"
        if own and own[1] == "current":
            out.append(f"FEMA's current flood map for unincorporated {CS} took effect {m('map_date', _mdate(own[2]), q='own')}"
                       + (f"; {own[3]}" if own[3] else "") + ".")
        elif own and own[1] == "nsfha":
            out.append(f"For unincorporated {CS}, {own[3]}.")
        if new:
            names = [_cname_plain(r[0]) for r in new]
            out.append(f"New FEMA flood maps take effect {m('map_date', _mdate(new[0][2]), q='first_new')}"
                       + (" or later" if len({r[2] for r in new}) > 1 else "") + " for "
                       + and_list(names[:8] + ([f"{m('map_new_n', str(len(names) - 8), q='more')} more"] if len(names) > 8 else [])) + ".")
    elif new:
        out.append(f"{m('map_new_n', str(len(new)))} communities in {CS} get a new FEMA flood map after FEMA's latest report, "
                   f"the first on {m('map_date', _mdate(new[0][2]), q='first_new')}.")
    if not out: return ""
    return (f"<p class='note'><b>Flood map:</b> {' '.join(out)} Check your own address on "
            "<a href='https://msc.fema.gov/portal/home' rel='noopener' target='_blank'>FEMA's flood map</a>.</p>")

def _crs_parts():
    _has_disc = [c for c in crs if _pct(c.get("sfhaDiscount")) or _pct(c.get("nonSfhaDiscount"))]
    _no_disc = sorted((c for c in crs if c not in _has_disc), key=lambda c: html.unescape(_cname_plain(c)).casefold())   # A to Z as shown (gate H8)
    def _tagd(key, shown, q):   # a table cell: tag it when it is a figure (not "No discount" / a dash)
        return m(key, shown, q=html.unescape(q).replace('"', "")) if re.search(r"\d", shown) else shown
    def _dnum(c): return int((_pct(c.get("sfhaDiscount")) or "0%").rstrip("%"))
    _shown_disc = sorted(_has_disc, key=lambda c: -_dnum(c))[:15] if IS_STATE else _has_disc   # a state can have hundreds
    crs_rows = "".join(f"<tr><td>{_cname(c)}" + (f" ({html.escape(_tc(str(c.get('county') or '')))})" if IS_STATE and c.get('county') and _tc(str(c['county'])).lower() not in _cname_plain(c).lower() else "") + "</td>"
                       f"<td>{_tagd('crs_discount', _disc(c.get('sfhaDiscount')), _cname_plain(c) + ':sfha')}</td>"   # Risk Rating 2.0: one rate for every zone; FEMA's separate non-SFHA column is pre-2021
                       f"<td>{_tagd('crs_class', _cls(c.get('classRating')), _cname_plain(c))}</td></tr>" for c in _shown_disc)
    crs_none_note = ((f"<p class='note'>The {m('crs_count', str(len(_shown_disc)), q='shown')} largest discounts of {m('crs_count', str(len(_has_disc)), q='discounted')} discounted communities are shown; "
                      f"{m('crs_count', str(len(_no_disc)), q='none')} communities here have no CRS discount." + (f" {UNITS.title()} with their own page list their towns." if HAS_CPAGES else "") + "</p>")
                     if IS_STATE else
                     (f"<p class='note'><b>No CRS discount ({m('crs_count', str(len(_no_disc)), q='none')}):</b> " + "; ".join(_cname(c) for c in _no_disc) + ".</p>") if _no_disc else "")
    _disc_communities = [c for c in crs if _pct(c.get("sfhaDiscount"))]
    if _disc_communities:
        top = max(_disc_communities, key=lambda c: int(_pct(c["sfhaDiscount"]).rstrip("%")))
        _topd = m('crs_discount', _pct(top['sfhaDiscount']), q=html.unescape(_cname_plain(top)) + ':sfha')
        crs_lead = ((claim("Yes", "yes", ("crs_discount_communities", ">", 0)) + f": {_cname(top)}, the only NFIP community here, gets {_topd}. ") if len(crs) == 1 else
                    ((claim("Yes", "yes", ("crs_discount_communities", ">", 0)) + ", " if 2 * len(_disc_communities) >= len(crs) else "Only some: ")   # "Yes" only when most get one
                     + f"{m('crs_count', str(len(_disc_communities)), q='sfha_discounted')} of the {m('crs_count', str(len(crs)), q='all')} NFIP communities here get one, up to {_topd} in {_cname(top)}. ")) + rule("crs_auto")
    else:
        crs_lead = ("Not through a community discount: " +
                    (f"none of {CS}'s {m('crs_count', str(len(crs)), q='all')} NFIP communities has one." if len(crs) != 1 else f"{CS}'s only NFIP community has none."))
    return crs_rows, crs_none_note, crs_lead

# ---- how to get covered (factual public NFIP rules — the reader's "what do I do next" + the 30-day catch) ----
def card_howto():
    _HOWTO = ["howto_answer", "homeowners_excl", "howto_tiles", "wait_exceptions", "how_to_buy", "already_flooded", "aid_insurance"]
    howto_card = card("How do I actually get covered — and how fast?",   # limits live in the tiles once (no second copy)
        rule("howto_answer"),
        rule("howto_tiles")
        + f"<p class='note'>{rule('homeowners_excl')} {rule('wait_exceptions')} {rule('how_to_buy')}</p>"
        + f"<p class='note'>{rule('already_flooded')} {rule('aid_insurance')}</p>"
        + (_deadline_tool() if _tool_on("deadline") else ""),
        src_rules(_HOWTO + (["aid_register_60", "private_deadlines"] if _tool_on("deadline") else [])), id="covered")
    return howto_card

def _tool_on(name):   # kill switch + staged launch: tools/tools_flags.json (CLAUDE.md reader tools ship standard)
    try: on = json.load(open(os.path.join(HERE, "tools_flags.json"), encoding="utf-8")).get(name) or []
    except Exception: return False
    return on == "all" or SLUG in on

def _deadline_tool():
    # Deadline planner: only the proof-of-loss date is computed (flood date + 60 calendar days, local dates);
    # the aid window is a rule, never a computed date. Every output sentence is listed in tools/test_tools.py.
    return (f"<div class='tool' id='deadline'><p class='note'><b>Flooded? Work out the proof-of-loss deadline for an NFIP (National Flood Insurance Program) policy.</b> "
            f"{rule('aid_register_60')} {rule('private_deadlines')}</p>"
            "<label class='note' for='dl'>Date the water came in:</label> "
            "<input id='dl' type='date' style='font-size:16px;padding:8px 10px;border:1px solid var(--line);border-radius:8px'>"
            "<p id='dlo' class='note' aria-live='polite'></p>" + _DEADLINE_JS + "</div>")

_DEADLINE_JS = """<script>(function(){
var M=['January','February','March','April','May','June','July','August','September','October','November','December'];
var i=document.getElementById('dl'),o=document.getElementById('dlo');
function fmt(d){return M[d.getMonth()]+' '+d.getDate()+', '+d.getFullYear();}
function run(){
  var m=/^(\\d{4})-(\\d{2})-(\\d{2})$/.exec(i.value||'');
  if(!m){o.textContent=i.value?'That is not a date. Enter the day the water came in.':'';return;}
  var y=+m[1],mo=+m[2]-1,da=+m[3],d=new Date(y,mo,da);
  if(d.getFullYear()!==y||d.getMonth()!==mo||d.getDate()!==da){o.textContent='That is not a date. Enter the day the water came in.';return;}
  var n=new Date(),t=new Date(n.getFullYear(),n.getMonth(),n.getDate());
  if(d>t){o.textContent='That date is in the future. Enter the day the water came in.';return;}
  var due=new Date(y,mo,da+60),left=Math.round((due-t)/864e5);
  if(left>0)o.textContent='An NFIP proof of loss is due by '+fmt(due)+' ('+left+(left===1?' day':' days')+' from today). Report the loss to your insurer now if you have not.';
  else if(left===0)o.textContent='An NFIP proof of loss is due today, '+fmt(due)+'. Contact your insurer now.';
  else o.textContent='The 60-day NFIP proof-of-loss date was '+fmt(due)+'. Contact your insurer now; it may have extended the date.';
}
i.addEventListener('input',run);i.addEventListener('change',run);})();</script>"""

_MONTHS = dict(zip([f"{i:02d}" for i in range(1, 13)], "January February March April May June July August September October November December".split()))
_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
def _recent_li():
    # round 16: same-title disasters told apart by month and declaration type; ones that still read the same (two
    # declarations, same month and title: Maine Sep 2023) are one line saying how many (gate H15 bans repeated lines)
    lines = [f"{_MONTHS.get((d.get('declarationDate') or '')[5:7], '')} {html.escape(cal_year(d))} — {html.escape(_dtitle(d))}"
             f"{' (emergency declaration)' if d.get('declarationType') == 'EM' else ''}" for d in recent]
    out = []
    for ln in lines:
        if out and out[-1][0] == ln: out[-1][1] += 1
        else: out.append([ln, 1])
    return "".join(f"<li>{ln}{f' ({_WORDS.get(n, str(n))} separate declarations)' if n > 1 else ''}</li>" for ln, n in out)

GEOID_SELF = os.environ.get("FF_GEOID", "12071")   # this page's own county (state pages: any county in the state)
# ---- ZIP lookup inside the county (your-place flow): every ZIP, with the town the reader knows it by ----
try: ZIPTOWN = json.load(open(os.path.join(os.path.dirname(HERE), "data", "us", "zip_places.json"), encoding="utf-8"))
except Exception: ZIPTOWN = {}
def _zl(z): return html.escape(z) + (f" <span data-name>{html.escape(ZIPTOWN[z])}</span>" if z in ZIPTOWN else "")
def _zip_county():
    bz = [z for z in (agg["policies"].get("by_zip") or []) if z.get("units") and re.fullmatch(r"\d{5}", str(z.get("zip")))]   # hater r7: ZIP+4 strings are not ZIPs
    zip_card = ""
    if bz:
        data_js = json.dumps({z["zip"]: {"u": z["units"], "m": z["median"], "n": z["cost_n"], "t": ZIPTOWN.get(z["zip"], "")} for z in bz})
        _zi = {z["zip"]: i for i, z in enumerate(agg["policies"].get("by_zip") or [])}
        _zp = lambda z, k: f"policies.by_zip.{_zi[z['zip']]}.{k}"
        _ranked = sorted([z for z in bz if z.get("median")], key=lambda z: -z["cost_n"])[:8]   # most priced policies: the medians a reader can trust most
        toprows = "".join(
            f"<tr><td>{m('zip', _zl(z['zip']), q=z['zip'])}</td><td>{tp('zip_cost', _zp(z, 'median'), money, q=z['zip'])}</td>"
            f"<td>{tp('zip_cost_n', _zp(z, 'cost_n'), num, q=z['zip'])}</td><td>{tp('zip_units', _zp(z, 'units'), num, q=z['zip'])}</td></tr>" for z in _ranked)
        _zs = [z for z in bz if z.get("median")]
        _lo, _hi = (min(_zs, key=lambda z: z["median"]), max(_zs, key=lambda z: z["median"])) if len(_zs) > 1 else (None, None)
        zip_card = card(f"Find your ZIP in this {UNIT}",
            (f"Typical costs run from {tp('zip_cost', _zp(_lo, 'median'), money, q=_lo['zip'])} a year in {m('zip', _zl(_lo['zip']), q=_lo['zip'])} to "
             f"{tp('zip_cost', _zp(_hi, 'median'), money, q=_hi['zip'])} in {m('zip', _zl(_hi['zip']), q=_hi['zip'])}. " if _lo else "")
            + f"All {m('zip_count', str(len(bz)), q='all')} ZIPs on NFIP policy records here are in the lookup.",
            f'<input id="zq" inputmode="numeric" maxlength="5" placeholder="e.g. {bz[0]["zip"]}" aria-label="Your ZIP code" '
            f'style="font-size:18px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;width:160px">'
            f'<p id="zout" class="note" style="margin-top:10px">Enter a five-digit ZIP above.</p>'
            '<p class="note">ZIPs exactly as FEMA recorded them on policies here; a ZIP with only a policy or two may be a ZIP from elsewhere, as entered on the policy.</p>'
            f'<table style="margin-top:12px"><thead><tr><th>ZIP</th><th>Median / yr</th><th>Priced policies</th><th>Policy units</th></tr></thead>'
            f'<tbody>{toprows}</tbody></table>'
            f'<p class="note">The ZIPs with the largest number of priced single-family policies.{how("zip")}</p>'
            f'<script>var ZD={data_js};var zi=document.getElementById("zq"),zo=document.getElementById("zout");'
            'zi.addEventListener("input",function(){var z=zi.value.trim();var d=ZD[z];'
            'if(!d){zo.textContent=z.length>=5?"No NFIP policy in this ' + UNIT + ' lists ZIP "+z+"; it may belong to a neighboring ' + UNIT + '.":"Enter a five-digit ZIP above.";return;}'
            'zo.innerHTML="<b>"+z+(d.t?" ("+d.t+")":"")+"</b>: "+d.u.toLocaleString()+" policy units"+(d.m?("; median $"+d.m.toLocaleString()+" a year ("+d.n.toLocaleString()+" priced single-family policies)"):"; too few priced policies for a median.");});'
            '</script>',
            src(["zip_cost", "units"], POL_ASOF, RETR), id="zip")
    return zip_card

# ---- why published prices differ (every page): one set of FEMA records, many honest "averages" ----
_xpp = EXTRAS.get("policies") or {}
_new_ok = (_xpp.get("cost_new_n") or 0) >= MX.CONST["year_min"]   # hater r5: what policies first bought this past year really cost
_xp, _xc = EXTRAS.get("policies") or {}, EXTRAS.get("claims") or {}
_whyall = [dict(r, i=i) for i, r in enumerate(_xc.get("unpaid_reasons") or [])]
_why = [r for r in _whyall if r["code"] not in ("97", "98", "99")]   # the lead names a real reason: 97 "other", 98/99 entered in error are not one
_why_rest = (_xc.get("unpaid_n") or 0) - sum(r["n"] for r in _whyall)   # smaller reasons and claims with no reason recorded
cx = data.get("claims_extra") or {}
_decs = [d for d, v in (_xc.get("by_decade") or {}).items() if (v.get("n") or 0) >= 30 and v.get("paid_pct") is not None]   # hater r6/r7: one bad era or every era?
def card_averages():
    averages_card = ""
    _av = _xpp.get("averages") or {}
    _cby = P.get("cost_by_year") or {}
    _yrs_cb = sorted(y for y, d in _cby.items() if (d.get("n") or 0) >= MX.CONST["year_min"])
    _fees = sum(_xpp.get(k) or 0 for k in ("fee_mean", "hfiaa_mean", "reserve_mean")) if _xpp.get("fee_mean") is not None else None
    _avrows = [("Typical cost, single-family homes (median)", m("cost_p50", money(P["p50"])), "premium plus fees; the middle policy"),
               ("Typical premium only", m("prem_median", money(P["prem_median"])), "before the federal fee, reserve fund and surcharge")]
    for _y in _yrs_cb[-2:]:
        _avrows.append((f"Typical cost, policies whose term began in {_y}", tp("cost_year", f"policies.cost_by_year.{_y}.median", money, q=_y),
                        f"{tp('cost_year_n', f'policies.cost_by_year.{_y}.n', num, q=_y)} policies"))
    if _new_ok:
        _avrows.append(("Typical cost, policies first bought in the past year", tp("cost_new", "extras.policies.cost_new_median", money),
                        f"{tp('cost_new_n', 'extras.policies.cost_new_n', num)} policies, past year"))
    if P.get("frp_median"):
        _avrows.append(("FEMA's full-risk premium (median)", m("frp_median", money(P["frp_median"])), "the price FEMA's model sets for these existing policies"))
        if _fees:
            _avrows.append(("Full-risk premium plus average fees", m("frp_plus_fees", money(P["frp_median"] + _fees)), "what these existing policies would cost at FEMA's full price"))
    if _av.get("sf_cost_mean"):
        _avrows += [("Average (mean) cost, single-family homes", tp("cost_mean", "extras.policies.averages.sf_cost_mean", money), "pulled up by a few expensive policies"),
                    ("Average cost, every policy type", tp("cost_all_mean", "extras.policies.averages.all_cost_mean", money), "adds condos, rentals and businesses")]
    averages_card = card(f"Why do sites quote different prices for {CS}?",
        f"Because they measure different things. Existing single-family policies here typically cost {m('cost_p50', money(P['p50']))} a year"
        + (f", and policies first bought in the past year {tp('cost_new', 'extras.policies.cost_new_median', money)}" if _new_ok else "")
        + "; other sites count other policies, years or averages.",
        "<table><thead><tr><th>Measure</th><th>Amount</th><th>What it counts</th></tr></thead><tbody>"
        + "".join(f"<tr><td>{a_}</td><td>{b_}</td><td>{c_}</td></tr>" for a_, b_, c_ in _avrows) + "</tbody></table>"
        + (f"<p class='note'><b>Condo owners:</b> condo-unit policies are {tp('condo_unit_pct', 'extras.policies.condo_unit_pct', pct)} of NFIP policy units here"
           + (f" and whole condo buildings {tp('condo_building_pct', 'extras.policies.condo_building_pct', pct)}" if _xpp.get('condo_building_pct') else "")
           + f". The single-family figures above leave both out; "
           "only the every-policy-type average includes them.</p>" if (_xpp.get("condo_unit_pct") or 0) + (_xpp.get("condo_building_pct") or 0) >= 1 else "")
        + f"<p class='note'>All from the NFIP policies in force on {POL_ASOF}.{how('averages')}</p>",
        src(["cost_p50", "prem_median", "frp_median", "cost_year"] + (["cost_new"] if _new_ok else []) + (["cost_mean", "cost_all_mean"] if _av.get("sf_cost_mean") else []), POL_ASOF, RETR), id="prices")
    return averages_card

# ---- can I pay less? (hater r5: every top result answers it; the deductible mix and elevated premiums are in the data) ----
def card_save():
    save_card = ""
    _ded = _xpp.get("deductibles") or {}
    if _ded or _xpp.get("prem_elevated_n"):
        _top = max(_ded, key=lambda d: _ded[d]) if _ded else None
        _dl = lambda d: m("ded_amount", money(int(float(d))), q=d)   # a FEMA code label, tagged so the gate sees no loose number
        _rows = "".join(f"<tr><td>{_dl(d)}</td><td>{tp('ded_share', f'extras.policies.deductibles.{d}', pct, q=d)}</td></tr>"
                        for d in sorted(_ded, key=lambda d: float(d)))
        _elev_ok = min(_xpp.get("prem_elevated_n") or 0, _xpp.get("prem_not_elevated_n") or 0) >= MX.CONST["year_min"]
        save_card = card("Can I pay less?",
            (f"The usual building deductible here is {_dl(_top)} ({tp('ded_share', f'extras.policies.deductibles.{_top}', pct, q=_top)} "
             "of single-family policies). " if _top else "") + rule("save_ways"),
            (f"<table><thead><tr><th>Building deductible</th><th>Share of policies</th></tr></thead><tbody>{_rows}</tbody></table>"
             "<p class='note'>Single-family primary homes; the commonest deductibles. Your lender may limit how high you can go.</p>" if _rows else "")
            + ("<p class='note'><b>Elevated vs not elevated is not what raising your home would save:</b> the two groups sit in "
               "different zones and places, so compare like with like on your own quote.</p>" if _elev_ok else "")
            + (f"<ul class='kv'><li><b>Median premium, elevated buildings</b><span>{tp('prem_elevated', 'extras.policies.prem_elevated_median', money)} "
               f"({tp('prem_elevated_n', 'extras.policies.prem_elevated_n')} policies)</span></li>"
               f"<li><b>Median premium, not elevated</b><span>{tp('prem_not_elevated', 'extras.policies.prem_not_elevated_median', money)} "
               f"({tp('prem_not_elevated_n', 'extras.policies.prem_not_elevated_n')} policies)</span></li></ul>"
               "<p class='note'>Premium before fees, single-family primary homes.</p>" if _elev_ok else "")
            + "<p class='note'>Community discount: see <a href='#crs'>Does my town get a community discount?</a></p>",
            src(["ded_share"] + (["prem_elevated"] if _elev_ok else []), POL_ASOF, RETR) + src_rules(["save_ways"]), id="save")
    return save_card

# ---- STATE-ONLY blocks: cost by county (the hub), why published averages differ, policies-in-force trend ----
def _counties_table():
    zip_card = ""
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
                        f"<td>{tp('county_cost', f'counties.{g}.p50', money, q=g) if _ok(r) else 'too few'}</td>"
                        f"<td>{tp('county_share_below', f'counties.{g}.share_below', pct, q=g) if _ok(r) and r.get('share_below') is not None else 'too few'}</td>"
                        f"<td>{tp('county_claims', f'counties.{g}.claims', num, q=g)}</td></tr>" for g, r in sorted(_cty, key=lambda kv: _cn(kv[0]).casefold()))   # every one, A to Z: the reader is finding theirs
        _cheap = sorted(_priced, key=lambda kv: kv[1]["p50"])[:5]; _dear = sorted(_priced, key=lambda kv: -kv[1]["p50"])[:5]
        zip_card = "" if len(_cty) < 2 else card(f"What does it cost in my {UNIT}?",
            (f"From about {tp('county_cost', f'counties.{_cheap[0][0]}.p50', money, q=_cheap[0][0])} a year in {_cn(_cheap[0][0])} to "
             f"{tp('county_cost', f'counties.{_dear[0][0]}.p50', money, q=_dear[0][0])} in {_cn(_dear[0][0])}, "
             f"among {UNITS} with {tp('threshold', 'const.min_priced', q='min_priced')} or more priced policies. Find yours below." if len(_priced) > 1 else f"Find your {UNIT} below."),
            f"<table><thead><tr><th>{UNIT.title()}</th><th>Policy units</th><th>Median / yr</th><th>Below full-risk</th><th>Claims since 1978</th></tr></thead>"
            f"<tbody>{_rows}</tbody></table>"
            + (f"<p class='note'><b>Lowest typical cost:</b> {and_list(_cn(g) + ' (' + tp('county_cost', f'counties.{g}.p50', money, q=g) + ')' for g, r in _cheap)}. "
               f"<b>Highest:</b> {and_list(_cn(g) + ' (' + tp('county_cost', f'counties.{g}.p50', money, q=g) + ')' for g, r in _dear)}. "
               "Median annual cost of single-family primary-home policies.</p>" if len(_priced) >= 10 else "")
            + f"<p class='note'>{UNITS.title()} with fewer than {tp('threshold', 'const.min_priced', q='min_priced')} priced single-family policies say “too few” (it counts priced policies, not the policy-units column); medians from under {tp('threshold', 'const.spread_min', q='spread_min')} policies move more from year to year.</p>",
            src(["county_units", "cost_p50", "share_below", "claims_filed"], POL_ASOF, RETR), id="counties")
    return zip_card

# ---- raw-pull extras: would a policy rebuild the home, why claims went unpaid, which storms paid most ----
def card_rebuild():
    rebuild_card = unpaid_card = events_card = ""
    if (_xp.get("replacement_n") or 0) >= 30 and _xp.get("replacement_over_250k_pct") is not None:
        rebuild_card = card("Would a policy here pay to rebuild my home?",
            f"Not in full for at least {tp('rebuild_over_cap_pct', 'extras.policies.replacement_over_250k_pct', pct)} of the {tp('rebuild_n', 'extras.policies.replacement_n')} single-family policies here that report a rebuilding cost: FEMA's records put it "
            f"above {rule('building_cap')}",
            f"<ul class='kv'><li><b>Rebuilding cost above the building limit (of {tp('rebuild_n', 'extras.policies.replacement_n')} policies reporting one)</b><span>{tp('rebuild_over_cap_pct', 'extras.policies.replacement_over_250k_pct', pct)}</span>{vs_state('rebuild_over_cap_pct', 'extras.policies.replacement_over_250k_pct', pct)}</li>"
            + (f"<li><b>Single-family policies insured to the building maximum (all of them, not only those above)</b><span>{tp('at_cap_pct', 'extras.policies.at_building_max_pct', pct)}</span></li>" if _xp.get("at_building_max_pct") is not None else "")
            + (f"<li><b>Damage was more than the coverage (of {tp('damage_n', 'extras.claims.damage_n')} claims paid with a damage figure)</b><span>{tp('damage_over_cov_pct', 'extras.claims.damage_over_coverage_pct', pct)}</span></li>"
               if _xc.get("damage_over_coverage_pct") is not None and (_xc.get("damage_n") or 0) >= 30 else "")
            + f"</ul><p class='note'>The two shares have different bases: insured-to-the-maximum counts every single-family policy "
              f"with the full building limit; the rebuilding-cost share counts only the policies that report a rebuilding cost. "
              f"Homes insured for less than their own rebuilding cost can also fall short.{how('rebuild')}</p><p class='note'><b>{rule('rcv_80')}</b></p>",
            src(["rebuild_over_cap_pct", "at_cap_pct", "damage_over_cov_pct"], POL_ASOF, RETR) + src_rules(["building_cap", "rcv_80"]))
    return rebuild_card

def card_unpaid():
    unpaid_card = ""
    if _why and (_xc.get("unpaid_n") or 0) >= 10:
        unpaid_card = card("Why do flood claims here go unpaid?",
            f"Of the {tp('unpaid_n', 'extras.claims.unpaid_n')} claims here closed without payment, the top specific reason FEMA recorded was "
            f"“{html.escape(_why[0]['label']).lower()}” ({tp('unpaid_reason_n', f'extras.claims.unpaid_reasons.{_why[0][chr(105)]}.n', q=_why[0]['code'])} claims).",
            "<table><thead><tr><th>Reason recorded</th><th>Claims</th></tr></thead><tbody>"
            + "".join(f"<tr><td>{html.escape(r['label'])}</td><td>{tp('unpaid_reason_n', f'extras.claims.unpaid_reasons.{r[chr(105)]}.n', q=r['code'])}</td></tr>" for r in _whyall)
            + (f"<tr><td>Smaller reasons, or none recorded</td><td>{m('unpaid_reason_n', num(_why_rest), q='rest')}</td></tr>" if _why_rest > 0 else "")
            + f"</tbody></table><p class='note'>Some closed claims are paperwork, not a denied flood.{how('unpaid')}</p>",
            src(["unpaid_n", "unpaid_reason_n"], f"{C['year_min']}–{C['year_max']}", RETR))
    return unpaid_card

def card_events():
    events_card = ""
    def _evname(e):   # FEMA's event name plus its year(s) of loss: "Vermont/New York Flooding (2023)"
        y = e.get("years") or []
        n = re.sub(r"^\d{4}-\d{2}-", "", e["name"])                       # FEMA codes like "2026-03-KonaStorm"
        n = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", n.replace("-", " ")).strip()   # -> "Kona Storm"
        if re.match(r"not a named (storm|event)", n, re.I): n = "Unnamed flood"     # FEMA's label for a flood with no name
        return html.escape(n) +(f" ({y[0]})" if len(y) == 1 else f" ({y[0]}–{y[-1]})" if y else "")
    # an event is a label whose paid claims fall within two calendar years; a label spanning more ("Flooding" 1979-2024)
    # is FEMA's catch-all, not one flood, and is left out
    _ev = [dict(e, i=i) for i, e in enumerate(_xc.get("events") or [])
           if e.get("years") and int(e["years"][-1]) - int(e["years"][0]) <= 1
           and (e.get("claims") or 0) >= MX.CONST["event_min"]]   # a handful of claims under a far-away storm's name is a coding slip, not a flood here
    # hater r6: the catch-all labels are shown as their own rows (dropping them hid Louisiana's $1.1 billion "Flooding" claims)
    _ev_all = [dict(e, i=i) for i, e in enumerate(_xc.get("events") or [])
               if e.get("years") and int(e["years"][-1]) - int(e["years"][0]) > 1 and (e.get("claims") or 0) >= MX.CONST["event_min"]]
    _ev_years = {int(y) for e in _ev for y in e["years"]}   # hater r5/r6: Louisiana's 1995 (4th costliest year) sat under the catch-all label
    _top5 = sorted(((y, by[str(y)][1]) for y in years), key=lambda x: -x[1])[:5]
    _unnamed = [(y, p) for y, p in _top5 if int(y) not in _ev_years]
    _unnamed_note = ("<p class='note'>Among the five costliest years, these have no flood FEMA named for that year alone: "
                     + ", ".join(str(y) for y, _ in _unnamed) + " (their totals are in the yearly chart above).</p>") if _unnamed else ""
    if len(_ev) >= 2:
        events_card = card("Which floods paid out the biggest totals here?",
            f"The costliest flood FEMA named here was {_evname(_ev[0])}: {tp('event_paid', f'extras.claims.events.{_ev[0][chr(105)]}.paid', big, q=_ev[0]['name'])} across "
            f"{tp('event_claims', f'extras.claims.events.{_ev[0][chr(105)]}.claims', q=_ev[0]['name'])} NFIP flood claims."
            # round 16 (Maine): a costlier year with no flood FEMA named for it alone is said in the lead, not only in a note
            + (f" The costliest year, {_top5[0][0]} ({tp('claims_year_paid', f'claims.by_year.{_top5[0][0]}.1', money, q=str(_top5[0][0]))}), has no single named flood."
               if _top5 and int(_top5[0][0]) not in _ev_years and _top5[0][1] > (_ev[0].get("paid") or 0) else ""),
            "<table><thead><tr><th>Flood (FEMA's name)</th><th>Claims</th><th>Total paid</th><th>Average</th></tr></thead><tbody>"
            + "".join(f"<tr><td>{_evname(e)}</td><td>{tp('event_claims', f'extras.claims.events.{e[chr(105)]}.claims', q=e['name'])}</td>"
                      f"<td>{tp('event_paid', f'extras.claims.events.{e[chr(105)]}.paid', big, q=e['name'])}</td>"
                      f"<td>{tp('event_avg', f'extras.claims.events.{e[chr(105)]}.avg', money, q=e['name'])}</td></tr>" for e in _ev)
            + "".join(f"<tr><td>{_evname(e)}: FEMA's records use this name for claims in several years</td><td>{tp('event_claims', f'extras.claims.events.{e[chr(105)]}.claims', q=e['name'])}</td>"
                      f"<td>{tp('event_paid', f'extras.claims.events.{e[chr(105)]}.paid', big, q=e['name'])}</td>"
                      f"<td>{tp('event_avg', f'extras.claims.events.{e[chr(105)]}.avg', money, q=e['name'])}</td></tr>" for e in _ev_all)
            + f"</tbody></table><p class='note'>Grouped by the flood event FEMA named; only claims that paid something, and only floods with {tp('threshold', 'const.event_min', q='event_min')} or more paid claims here. Totals include code-upgrade (ICC) payments, which the yearly chart leaves out.{how('events')}</p>" + _unnamed_note,
            src(["event_paid", "event_claims"], f"{C['year_min']}–{C['year_max']}", RETR))
    return events_card

# ---- repetitive-loss properties (FEMA IA multiple-loss; a chronic repeat-flood signal, distinct from
# the annual NFIP claims) ----
def card_multiloss():
    ml = data.get("multiloss") or {}
    multiloss_card = ""
    if ml.get("total") is not None:   # 0 is a real, reassuring finding (no chronic repeat-flood homes), not "no data"
        _srl = ml.get("srl") or 0
        _mldate = ml.get("retrieved", RETR)
        # FEMA: one row per property PER declared disaster, and "there is not a way to aggregate by property" —
        # so the count is damage records on repeat-flooded homes, never a count of distinct homes.
        _ml_lead = (claim("Yes", "yes", ("ml_total", ">", 0)) + f": FEMA's disaster-aid records hold {m('ml_total', num(ml['total']))} damage records from homes here that flooded more than once"
                    + (f"; {m('ml_srl', num(_srl))} records are from homes FEMA's disaster-aid data flags as severe repeat-loss (SRL)" if _srl else "") + "."
                    if ml["total"] else
                    f"Not in FEMA's disaster-aid records since 2002: no aid applications here came from homes that flooded more than once. NFIP insurance claims are counted separately.")
        multiloss_card = card("Do the same homes flood again here?", _ml_lead,
            f"<ul class='kv'><li><b>Repeat-flood damage records</b><span>{tp('ml_total', 'data.multiloss.total')}</span></li>"
            + (f"<li><b>Records from homes flagged severe repeat-loss (SRL)</b><span>{tp('ml_srl', 'data.multiloss.srl')}</span></li>" if _srl else "")
            + f"</ul><p class='note'>These count damage events on repeat-flooded homes, not distinct homes.{how('multiloss')}</p>",
            src(["ml_total"], "FEMA's current multiple-loss list", _mldate))
    return multiloss_card

# ---- payout reality (avg paid + closed-without-payment share) ----
def card_payout():
    payout_card = ""
    if cx.get("claims"):
        _paid_pct = round(100 - cx["cwop_share"], 1)
        _ans = (claim("Most do", "most", ("cwop_share", "<", 50)) + f": {m('paid_share', str(_paid_pct) + '%')} of claims here paid something"
                if cx["cwop_share"] < 50 else
                f"{m('cwop_share', str(cx['cwop_share']) + '%')} of claims here closed with no payment"
                + (f"; the top specific reason FEMA recorded was “{html.escape(_why[0]['label']).lower()}” (all reasons below)" if _why else "")
                if cx["cwop_share"] > 50 else f"About half: {m('cwop_share', str(cx['cwop_share']) + '%')} of claims here closed with no payment")
        payout_card = card("Do flood claims here actually pay out?",
            f"{_ans}. The average paid claim was {tp('avg_paid', 'data.claims_extra.avg_paid', money)} (all years, in dollars of the day, not adjusted for inflation).",
            f"<ul class='kv'><li><b>Average paid claim, incl. code-upgrade (ICC) pay</b><span>{tp('avg_paid', 'data.claims_extra.avg_paid', money)}</span>{vs_state('avg_paid', 'data.claims_extra.avg_paid', money)}</li>"
            f"<li><b>Closed with no payment</b><span>{tp('cwop_share', 'data.claims_extra.cwop_share', pct)}</span>{vs_state('cwop_share', 'data.claims_extra.cwop_share', pct)}</li>"
            f"<li><b>Claims that paid</b><span>{tp('claims_paid_n', 'data.claims_extra.paid_n')}</span></li></ul>"
            + (("<table><thead><tr><th>Decade of the flood</th><th>Claims filed</th><th>Share that paid something</th></tr></thead><tbody>"
                + "".join(f"<tr><td>{m('decade', html.escape(d), q=d)}</td><td>{tp('decade_claims', f'extras.claims.by_decade.{d}.n', q=d)}</td>"
                          f"<td>{tp('decade_paid_share', f'extras.claims.by_decade.{d}.paid_pct', pct, q=d)}</td></tr>" for d in _decs)
                + "</tbody></table>") if len(_decs) > 1 else "")
            + f"<p class='note'>{rule('cwop')} The average is over claims that paid something and includes Increased Cost of "
            "Compliance payments (help to elevate or rebuild to code), which the yearly totals above leave out. Dollars are "
            "as paid at the time, not adjusted for inflation; a single home can file across several floods over the years.</p>",
            src(["claims_filed", "avg_paid", "cwop_share"], f"{C['year_min']}–{C['year_max']}", cx.get("retrieved", RETR)), id="payout")
    return payout_card

mani = agg.get("manifest", {})
mani_ok = all(v.get("complete") for v in mani.values()) if mani else False
mani_line = "; ".join(f"{k}: {tp('records_total', f'manifest.{k}.unique_fetched', q=k + ':fetched')} of {tp('records_total', f'manifest.{k}.reported_total', q=k + ':reported')} fetched"
                      + ("" if v["complete"] else f" (MISSING {v['missing']})") for k, v in mani.items()) or "n/a"

# ---- SEO / GEO + place registry ----
SLUG = os.environ.get("FF_SLUG", "lee-county-fl")
BASE_URL = os.environ.get("FF_BASEURL", "https://floodinsurancedata.com").rstrip("/")   # never example.com
CANON = f"{BASE_URL}/flood-insurance/{SLUG}/"
GEOID = os.environ.get("FF_GEOID", "12071")
META_DESC = (f"Median NFIP flood insurance cost for a single-family primary home in {CS} is {money(P['p50'])} a year "
             f"(middle half {money(P['p25'])}–{money(P['p75'])}); {P['share_below']}% pay below FEMA's "
             f"full-risk price. {num(P['units'])} insured units, claims, flood risk and community discounts, from FEMA's own records.")
# register this place so home/lookup/sitemap/siblings know it exists
PLACES = os.environ.get("FF_PLACES", os.path.join(HERE, "places.json"))
try: places = json.load(open(PLACES))
except Exception: places = []
if not IS_STATE and os.environ.get("FF_PLACES_RO") != "1":   # places.json lists county pages; build_counties.py writes it itself (parallel builds must not)
    places = [p for p in places if p.get("slug") != SLUG]
    places.append({"slug": SLUG, "label": CL, "short": CS, "geoid": GEOID,
                   "units": P["units"], "median": P["p50"], "state": agg.get("nri", {}).get("state") if agg.get("nri") else None})
    places.sort(key=lambda p: -(p.get("units") or 0))
    json.dump(places, open(PLACES, "w"), indent=1)
from agg_raw import NAMES as STATE_NAMES, slug as state_slug
# siblings must be ACTUAL neighbours: same-state BUILT pages (never the global top-5 by policy count,
# which just funnelled every page to the same mega-counties and orphaned the tail). No same-state page
# built yet -> link to the full directory, not a false "nearby".
_state = agg.get("state") if agg.get("level") == "county" else (agg.get("nri", {}).get("state") if agg.get("nri") else None)
_others = [p for p in places if p.get("slug") != SLUG]
_same = [p for p in _others if _state and p.get("state") == _state]
# guarantee >=3 links: same-state first; if fewer than 3, fill with the nearest-by-size other counties
# (places.json is sorted by units desc). Never leave a page with 0 lateral links.
_fill = [p for p in _others if p not in _same]
# PLAN 5b: bordering published counties first (Census county adjacency, either state), then the state's biggest
try: _adj = set(json.load(open(os.path.join(os.path.dirname(HERE), "data", "us", "county_adjacency.json"))).get(agg.get("geoid") or "", []))
except Exception: _adj = set()
_nbr = [p for p in _others if p.get("geoid") in _adj]
_near = _nbr + [p for p in _same if p not in _nbr]
siblings = _near[:6] if len(_near) >= 3 else (_near + [p for p in _fill if p not in _near])[:5]
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
def _rank(r, n):   # say the short end; "1st highest" reads as "the highest"
    return "the highest" if r == 1 else "the lowest" if r == n else f"{ordinal(r)} highest" if r <= (n + 1) // 2 else f"{ordinal(n - r + 1)} lowest"
NEIGHBORS = {   # land borders (AK and HI: none, so the West Coast states)
    "AL": "FL GA MS TN", "AK": "WA OR CA", "AZ": "CA CO NM NV UT", "AR": "LA MS MO OK TN TX", "CA": "AZ NV OR",
    "CO": "AZ KS NE NM OK UT WY", "CT": "MA NY RI", "DE": "MD NJ PA", "DC": "MD VA", "FL": "AL GA",
    "GA": "AL FL NC SC TN", "HI": "CA OR WA", "ID": "MT NV OR UT WA WY", "IL": "IN IA KY MO WI", "IN": "IL KY MI OH",
    "IA": "IL MN MO NE SD WI", "KS": "CO MO NE OK", "KY": "IL IN MO OH TN VA WV", "LA": "AR MS TX", "ME": "NH",
    "MD": "DE PA VA WV DC", "MA": "CT NH NY RI VT", "MI": "IN OH WI", "MN": "IA ND SD WI", "MS": "AL AR LA TN",
    "MO": "AR IL IA KS KY NE OK TN", "MT": "ID ND SD WY", "NE": "CO IA KS MO SD WY", "NV": "AZ CA ID OR UT",
    "NH": "ME MA VT", "NJ": "DE NY PA", "NM": "AZ CO OK TX UT", "NY": "CT MA NJ PA VT", "NC": "GA SC TN VA",
    "ND": "MN MT SD", "OH": "IN KY MI PA WV", "OK": "AR CO KS MO NM TX", "OR": "CA ID NV WA",
    "PA": "DE MD NJ NY OH WV", "RI": "CT MA", "SC": "GA NC", "SD": "IA MN MT NE ND WY", "TN": "AL AR GA KY MS MO NC VA",
    "TX": "AR LA NM OK", "UT": "AZ CO ID NV NM WY", "VT": "MA NH NY", "VA": "KY MD NC TN WV DC", "WA": "ID OR",
    "WV": "KY MD OH PA VA", "WI": "IL IA MI MN", "WY": "CO ID MT NE SD UT"}
NEIGHBORS = {k: v.split() for k, v in NEIGHBORS.items()}
def _pct_vs(a, b, q):
    d = round(100 * (a - b) / b)
    return "the same as" if d == 0 else f"{m('pct_vs', str(abs(d)) + '%', q=q)} {'above' if d > 0 else 'below'}"
cmp_line = ""
_cby1 = P.get("cost_by_year") or {}
_ly = max((y for y, d in _cby1.items() if (d.get("n") or 0) >= MX.CONST["year_min"]), default=None)
_renew_line = ('<p class="cmp">'   # hater r5: the renewing and the buying reader each get their own figure on screen 1
               + (f'<b>This year’s bills:</b> policies whose term began in {_ly} (renewals and policies sold this year together) typically pay {tp("cost_year", f"policies.cost_by_year.{_ly}.median", money, q=_ly)}. '
                  if _ly and len(_cby1) > 1 else "")
               + (f'<b>Buying?</b> Policies first bought in the past year typically pay {tp("cost_new", "extras.policies.cost_new_median", money)}. ' if _new_ok else "")
               + '<a href="#prices">Why prices differ</a>.</p>') if (_ly and len(_cby1) > 1) or _new_ok else ""
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
                + ((f'; {m("cost_rank", _rank(_r, len(_ranked)))} of the {m("rank_n", str(len(_ranked) - 1), q="states")} states and DC'
                    if "DC" in [a for _, a in _ranked] else
                    f'; {m("cost_rank", _rank(_r, len(_ranked)))} of {m("rank_n", str(len(_ranked)))} states') if _r else "") + ".</p>")
elif _sagg and not IS_STATE:
    _sc = [(r["p50"], g) for g, r in (_sagg.get("counties") or {}).items() if (r.get("cost_n") or 0) >= 100 and r.get("p50") and g[:2] == GEOID_SELF[:2]]
    _sc.sort(reverse=True)
    _r = next((i + 1 for i, (_, g) in enumerate(_sc) if g == GEOID_SELF), None)
    _sn = html.escape(STATE_NAMES[_ab])
    cmp_line = (f'<p class="cmp">That is {_pct_vs(P["p50"], _sagg["policies"]["p50"], "state")} the {_sn} median of {m("state_p50", money(_sagg["policies"]["p50"]))}'
                + (f' and {_pct_vs(P["p50"], US_P50, "us")} the U.S. median of {m("us_p50", money(US_P50))}' if US_P50 else "")
                + (f'; {m("cost_rank", _rank(_r, len(_sc)))} of {m("rank_n", str(len(_sc)))} {_sn} {UNITS} with {tp("threshold", "const.rank_min", q="rank_min")}+ priced policies' if _r else "") + ".</p>")
    _zs = [z for z in (P.get("by_zip") or []) if z.get("median")]
    if len(_zs) >= 2:   # a county median can hide coastal ZIPs paying two or three times as much: say so on screen 1
        _zlo, _zhi = min(_zs, key=lambda z: z["median"]), max(_zs, key=lambda z: z["median"])
        _zix = {z["zip"]: i for i, z in enumerate(P["by_zip"])}
        cmp_line += (f'<p class="cmp">By ZIP it ranges from {tp("zip_cost", f"policies.by_zip.{_zix[_zlo['zip']]}.median", money, q=_zlo["zip"])} '
                     f'({m("zip", _zl(_zlo["zip"]), q=_zlo["zip"])}) to {tp("zip_cost", f"policies.by_zip.{_zix[_zhi['zip']]}.median", money, q=_zhi["zip"])} '
                     f'({m("zip", _zl(_zhi["zip"]), q=_zhi["zip"])}); <a href="#zip">find your ZIP</a>.</p>')
if IS_STATE:
    _nb = [(a, STATE_NAMES[a]) for a in NEIGHBORS.get(_ab, []) if a in STATE_NAMES]   # the states that border this one
    sib_html = ("<nav class='sib'><b>Neighboring states:</b> " + " · ".join(f'<a href="../{state_slug(a)}/">{html.escape(n)}</a>' for a, n in _nb)
                + ' · <a href="../../">all states</a></nav>')
elif siblings:
    _lbl = "Bordering counties" if all(p in _nbr for p in siblings) else "Bordering and other counties" if _nbr else f"Other {html.escape(_state)} counties" if len(_same) >= 3 else "Compare other counties"
    sib_html = (f"<nav class='sib'>{_state_link}<b>{_lbl}:</b> " +
                " · ".join(f'<a href="../{p["slug"]}/">{html.escape(p["short"])}</a>' for p in siblings) +
                ' · <a href="../../">all places</a></nav>')
else:
    sib_html = f'<nav class="sib">{_state_link}<a href="../../">Browse all places by state →</a></nav>'
# Federal source catalog — single source of truth for the citation schema AND the visible sources block.
ISO_DATE = P["retrieved"]   # ISO date the federal data was last pulled
_pulls = [ISO_DATE] + [str((data.get(k) or {}).get("retrieved") or "") for k in ("claims_extra", "multiloss")]
LATEST_PULL = pretty_date(max(d for d in _pulls if d[:4].isdigit()))
# The page's dataset list is DERIVED from the source lines on the final page (page_sources). The inline cards in the
# template below build their source lines while the f-string renders, so the list, its count and the JSON-LD
# citation are placeholders filled after HTML exists. A dataset no panel cites can no longer be listed.
def page_sources():   # from the source lines on the FINAL page: code for a card that is not placed cites nothing
    seen = []
    for k in (k for keys in re.findall(r'data-src="([^"]*)"', HTML) if not keys.startswith("rule:") for k in keys.split(",")):
        ds = MX.METRICS[k]["dataset"]
        if ds not in seen: seen.append(ds)
    return [MX.DATASETS[d][:2] for d in MX.DATASETS if d in seen]
sources_li = "@@SOURCES_LI@@"
# JSON-LD: Dataset + Place + Breadcrumb (no FAQ markup: Google requires it to match visible Q&A)
_qa = [f'<a href="#required"><b>Am I required to buy it?</b> {rule("purchase_short")}'
       + (f' {rule("fl_citizens_short")}' if agg.get("state") == "FL" else "") + '</a>',
       f'<a href="#covered"><b>How fast does it start?</b> {rule("howto_short")}</a>']
_cxq = data.get("claims_extra") or {}
if _cxq.get("claims") and _cxq.get("avg_paid") and P.get("p50"):
    _sroot = ROOT_DATA.get("state") if isinstance(ROOT_DATA.get("state"), dict) else {}   # on a state page "state" is just its code
    _scx = (_sroot.get("data") or {}).get("claims_extra") or {}
    _qa.append(f'<a href="#payout"><b>Does it pay out here?</b> {m("paid_share", str(round(100 - _cxq["cwop_share"], 1)) + "%")} of claims here paid '
               + (f'something ({html.escape(STATE_NAMES[agg["state"]])}: {m("paid_share", str(round(100 - _scx["cwop_share"], 1)) + "%", q="state")}); '
                  if _scx.get("cwop_share") is not None else 'something; ')
               + f'the average paid claim was {tp("avg_paid", "data.claims_extra.avg_paid", money)} (all years, not inflation-adjusted).'
               + (f' Claims filed for losses in the {m("decade", html.escape(_decs[-1]), q=_decs[-1])}: '
                  f'{tp("decade_paid_share", f"extras.claims.by_decade.{_decs[-1]}.paid_pct", pct, q=_decs[-1])} paid something.' if len(_decs) > 1 else '')
               + ' Some unpaid claims are paperwork, not denied floods.</a>')
_qa.append('<a href="#covered"><b>Already flooded?</b> What to do now, and what FEMA aid covers.</a>')
_qa.append('<a href="#compare"><b>Is my quote normal?</b> These are existing policies, not a quote; type yours in to see where it sits.</a>')
quick_answers = '<nav class="jump qa">' + "".join(_qa) + "</nav>"

# provenance: we download every record FEMA publishes for the place and recompute; say so, with the counts
_man = agg.get("manifest") or {}
_mp, _mc = _man.get("policies") or {}, _man.get("claims") or {}
_pulled = pretty_date(_mp["pulled"]) if _mp.get("pulled") else RETR
PROV_OK = bool(_mp.get("complete") and _mc.get("complete") and not _mp.get("missing") and not _mc.get("missing"))
prov_line = (f'<p class="prov">Built from all {tp("records_policies", "manifest.policies.unique_fetched")} in-force NFIP policy records and '
             f'{tp("records_claims", "manifest.claims.unique_fetched")} claim records FEMA publishes for {CS}, downloaded {_pulled} '
             + (f'with every record for {html.escape(STATE_NAMES.get(agg.get("state"), "the state"))}, every record the download listed was received, none missing.'
                if _mp.get("scope") == "state" else "and every record the download listed was received, none missing.") + f' <a href="data.csv">Download the figures on this page (CSV)</a> · '
             f'<a href="../../methodology/">How we check them</a></p>') if PROV_OK else ""
jsonld = json.dumps([
    {"@context": "https://schema.org", "@type": "Dataset",
     "name": f"NFIP flood insurance data for {CL}", "url": CANON,
     "description": META_DESC + (f" Computed from a full download of {_mp['unique_fetched']:,} in-force NFIP policy records and "
                                 f"{_mc['unique_fetched']:,} NFIP claim records (OpenFEMA NfipPolicies v3 and NfipClaims v3), "
                                 "with every record the download listed received." if PROV_OK else ""),
     "measurementTechnique": "Full record-level download of OpenFEMA NfipPolicies v3 and NfipClaims v3, deduplicated by record id, reconciled to the API's record count, recomputed offline",
     "variableMeasured": ["annual policy cost (premium plus fees)", "full-risk premium", "flood zone", "NFIP claims paid", "claim non-payment reason", "building replacement cost"],
     "temporalCoverage": f"{C['year_min']}/{C['year_max']}",
     "spatialCoverage": {"@type": "Place", "name": CL},
     "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": CANON + "data.csv"}],
     "keywords": ["flood insurance", "NFIP", "FEMA", CS],
     "creator": {"@type": "Organization", "name": "Flood Insurance Data", "url": BASE_URL},
     "isBasedOn": "https://www.fema.gov/about/openfema/data-sets",
     "publisher": {"@type": "Organization", "name": "Flood Insurance Data", "url": BASE_URL},
     "dateModified": ISO_DATE,   # the data's real change date; no datePublished (it would move with every refresh)
     "citation": "@@CITATION@@",
     "isBasedOn": "https://www.fema.gov/about/openfema/data-sets", "license": "https://www.fema.gov/about/openfema/terms-conditions"},
    {"@context": "https://schema.org", "@type": "Place", "name": CL,
     "address": {"@type": "PostalAddress", "addressRegion": agg.get("state") or ((agg.get("nri") or {}).get("state")), "addressCountry": "US"}},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Flood insurance", "item": f"{BASE_URL}/flood-insurance/"},
        {"@type": "ListItem", "position": 2, "name": CS, "item": CANON}]},
])
# quote-compare widget (client-side; a position in the distribution, never a quote)
# plan item 1: compare the quote with the reader's own zone too (cost_by_zone medians; no estimate, no new figure on the page)
_zsel = ("<select id='qzs' aria-label='Your flood zone' style='font-size:16px;padding:8px;border:1px solid var(--line);border-radius:8px;margin-left:6px'>"
         "<option value=''>My flood zone (optional)</option>"
         + "".join(f"<option value='{html.escape(z)}'>Zone {html.escape(z)}</option>" for z, d in sorted((P.get("cost_by_zone") or {}).items()) if d["n"] >= MX.CONST["zone_min"])
         + "</select>") if sum(d["n"] >= MX.CONST["zone_min"] for d in (P.get("cost_by_zone") or {}).values()) > 1 else ""
quote_widget = f"""<section class="card" id="compare"><h2>Is my quote or renewal normal here?</h2>
<p class="stand">Type your yearly cost (premium plus fees) to see where it sits among existing single-family policies here.</p>
<input id="q" type="number" inputmode="numeric" placeholder="e.g. {int(round(P['p50'], -1))}" aria-label="Your annual premium in dollars"
 style="font-size:18px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;width:160px">
{_zsel}
<p id="qout" class="note" style="margin-top:10px">Enter an amount above.</p>
<p id="qz" class="note"></p>
<script>
var P={{p25:{P['p25']},p50:{P['p50']},p75:{P['p75']},p90:{P['p90']}}};
var Z={json.dumps({z: [d['median'], d['n']] for z, d in (P.get('cost_by_zone') or {}).items()})};
var R={json.dumps(" These are existing policies, many still below FEMA's full-risk price, so a new quote often lands higher."
                  + (f" Policies first bought in the past year typically pay {money(_xpp['cost_new_median'])}." if _new_ok else "")
                  + (f" Policies whose term began in {_ly} (renewals and new buyers) typically pay {money(_cby1[_ly]['median'])}." if _ly and len(_cby1) > 1 else ""))};
var el=document.getElementById('q'),out=document.getElementById('qout');
el.addEventListener('input',function(){{
  var v=parseFloat(el.value);
  if(!v||v<=0){{out.textContent='Enter an amount above.';zq();return;}}
  var msg;
  if(v<=P.p25) msg='in the cheapest quarter of existing policies here';
  else if(v< P.p50) msg='below the typical cost, cheaper than about half of existing policies here';
  else if(v==P.p50) msg='the typical cost here';
  else if(v< P.p75) msg='above the typical cost, more than about half of existing policies here';
  else if(v< P.p90) msg='in the top quarter, more than about 75% of existing policies here';
  else msg='higher than about 90% of existing policies here';
  out.textContent='$'+v.toLocaleString()+' is '+msg+' (half pay $'+P.p25.toLocaleString()+' to $'+P.p75.toLocaleString()+', typical $'+P.p50.toLocaleString()+').'+R;
  zq();
}});
function zq(){{var s=document.getElementById('qzs'),o=document.getElementById('qz'),v=parseFloat(el.value);
  if(!s||!s.value||!(v>0)){{o.textContent='';return;}}var d=Z[s.value],p=Math.round(100*(v-d[0])/d[0]);
  o.textContent='In Zone '+s.value+' here the typical cost is $'+d[0].toLocaleString()+' ('+d[1].toLocaleString()+' priced policies); $'+v.toLocaleString()+' is '+(p==0?'right at it':Math.abs(p)+'% '+(p>0?'above':'below')+' it')+'.';}}
if(document.getElementById('qzs'))document.getElementById('qzs').addEventListener('change',zq);
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

# ---- the cards placed in the page body: each card is one function; CARD_ORDER alone decides what shows and where ----
def card_required():
    return card("Am I required to buy it?",
      rule("purchase_answer") + " " + rule("lender_any_zone"),
      (f"<p class='note'><b>{rule('fl_citizens')}</b></p>" if agg.get("state") == "FL" else "") +
      f"<p class='note'>{rule('private_accept')}</p>" +
      f"<p class='note'>{m('sfha_share', str(P['sfha_share_units']) + '%')} of {CS}'s NFIP policy units are in high-risk zones (not {tp('sfha_share', 'policies.sfha_share_units', pct)} of all buildings, and not an answer about your own home).</p>"
      f"{_zone_body()}<p class='note'>Insured units by the zone each policy is rated in.{how('zones')}</p>" + _map_line()
      + (f"<p class='note'><b>Not in the NFIP ({m('crs_count', str(len(crs_out)), q='not_nfip')} communities here)"
         + (": " + "; ".join(sorted((_cname(c) + (" (unincorporated area only)" if re.search(r"\b(COUNTY|PARISH|BOROUGH)\b", (c.get("communityName") or "").upper()) else "") for c in crs_out), key=lambda h: html.unescape(re.sub("<[^>]+>", "", h)).casefold())))
         + f".</b> {rule('nfip_not_sold')}</p>" if crs_out else ""),
      src(["units", "sfha_share"], POL_ASOF, RETR) + (src(["map_date"], "FEMA's current Community Status Book", RETR) if _map_line() else "") + src_rules(["purchase_answer", "lender_any_zone", "private_accept"] + (["fl_citizens"] if agg.get("state") == "FL" else []) + (["nfip_not_sold"] if crs_out else [])), id="required")

def card_cost():
    cost_lead, cost_body = _cost_parts()
    return card("How much does it cost here?", cost_lead, cost_body, src(["cost_p50", "prem_median", "frp_median", "coverage"], POL_ASOF, RETR))

def card_claims():
    claims_lead, claims_ratio_note = _claims_parts()
    return card("What do floods actually pay out here?", claims_lead, claims_svg() +
      f"<p class='note'>Bar height is dollars paid that year. Orange bars are the three costliest years: " + ", ".join(f"{y} ({tp('claims_year_paid', f'claims.by_year.{y}.1', money, q=str(y))})" for y, p in top_paid) +
      f". Total paid {tp('claims_total', 'claims.total_paid', money, q='exact')}. Totals for the latest two years are not final while their claims stay open.{how('claims')}</p>" + claims_ratio_note,
      src(["claims_filed", "claims_total"], f"{C['year_min']}–{C['year_max']}", RETR))

def card_zip():   # state pages: the county table in the same slot
    return _counties_table() if IS_STATE else _zip_county()

def card_gap():
    gap_lead, glide_note = _gap_parts()
    return card("How do current premiums compare with FEMA's full-risk price?", gap_lead,
      f"<ul class='kv'><li><b>Median premium charged (before fees)</b><span>{m('prem_median', money(PREM_MED))}</span></li>"
      f"<li><b>Median full-risk premium</b><span>{m('frp_median', money(P['frp_median']))}</span></li>"
      f"<li><b>Pay below full-risk</b><span>{m('share_below', str(P['share_below']) + '%')} of {tp('units_listed', 'policies.below_n', q='below_n')}</span>{vs_state('share_below', 'agg.policies.share_below', pct)}</li></ul>" + glide_note,
      src(["prem_median", "frp_median", "share_below"], POL_ASOF, RETR))

def card_crs():
    crs_rows, crs_none_note, crs_lead = _crs_parts()
    return card("Does my town get a community discount?", crs_lead,
      (f"<table><thead><tr><th>Community</th><th>Discount</th><th>CRS class</th></tr></thead><tbody>{crs_rows}</tbody></table><p class='note'>CRS class is FEMA's grade for a community's flood work: the lower the class, the bigger the discount.</p>" if crs_rows else "")
      + crs_none_note +
      "<p class='note'>The Community Rating System cuts NFIP premiums in communities that do extra flood work. A community named for the " + UNIT + " covers its unincorporated area only.</p>",
      src(["crs_discount"], "FEMA's current Community Status Book", RETR), id="crs")

def card_disasters():
    return card(f"How often is {CS} a flood disaster?" if IS_STATE else f"How often is this {UNIT} a flood disaster?",
      f"{m('declarations', str(len(fh_events)))} federal disasters for floods or storms here"
      + (f"; the latest was {html.escape(_dtitle(recent[0]))} ({html.escape(cal_year(recent[0]))})." if recent else "."),
      f"<ul>{_recent_li()}</ul><p class='note'>Only the latest are listed, newest first; disasters with the same month and title share one line, which says how many; the count covers every flood, hurricane, tropical-storm and coastal-storm declaration FEMA lists here, plus severe-storm declarations whose title names flooding, including emergency declarations.{how('declarations')}</p>",
      src(["declarations"], "declarations through " + max((cal_year(d) for d in fh), default="the latest on file"), RETR))

def card_aid():
    return card("Did FEMA aid homeowners after floods and storms?",
      ((claim("Yes", "yes", ("ia_paid", ">", 0)) + f": FEMA approved {m('ia_paid', big(h_ihp))} for homeowners here after floods and storms, "
        f"about {m('ia_per_reg', money(h_ihp / h_regs))} per registration"
        + ".")
       if h_ihp and h_regs else "No FEMA housing aid to homeowners here after floods or storms is on record."),
      f"<p class='note'>{rule('ia_partial')} The average is over every registration, including those approved for nothing. "
      "Only disasters counted in the flood-disaster card are included; their aid can still cover wind or tornado damage from the same storm. Disasters for COVID, fire, winter storms or tornadoes alone are left out.</p>",
      src(["ia_paid", "ia_regs"],
          "homeowner aid by disaster", RETR))

def card_counts():
    return card("Are these counts complete?", ("Our counts are checked against FEMA's official figure and the download's own record total." if OFFICIAL
      else "Every record FEMA's download lists was received and counted."),
      f"<p class='note'>In-force count: {tp('units', 'policies.units')} policy units (from {tp('records_total', 'policies.rows', q='rows')} API records; condo-association records carry more than one unit). " +
      (f"FEMA's official count for {POL_ASOF} was {m('official_count', num(OFFICIAL))}: a {m('official_diff', str(round(abs(P['units']-OFFICIAL)/OFFICIAL*100,1)) + '%')} difference. " if OFFICIAL else "") +
      f"Download check: {mani_line}.</p>")

# page order (reader first: required, cost, how to get covered, payouts, then the detail cards). card_spec.py says what each covers.
CARD_ORDER = [card_required, card_cost, card_howto, card_claims, card_payout, card_unpaid, card_events, card_rebuild,
              card_zone_cost, card_zip, card_averages, card_gap, card_save, card_crs, card_risk, card_multiloss,
              card_disasters, card_aid, card_counts]
CARDS = "\n\n".join(h for h in (f() for f in CARD_ORDER) if h)
# "On this page": pages run 20+ phone screens; one link per card, in page order (owner 2026-10-28)
_toc = ('<nav class="toc card"><h2>On this page</h2><ul>'
        + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in re.findall(r'<section class="card" id="([^"]+)"><h2>(.*?)</h2>', CARDS))
        + "</ul></nav>")
# backlog 3: the county table is the state page's best tool and sits far down; screen 1 jumps to it
_jump = f'<p class="cmp"><a href="#counties">Find your {UNIT} in the table ↓</a></p>' if IS_STATE and 'id="counties"' in CARDS else ""

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{'<meta name="robots" content="noindex,follow">' if os.environ.get("FF_NOINDEX") == "1" else ""}
<title>Flood insurance cost in {CL}: {money(P['p50'])} median a year, single-family homes (FEMA data)</title>
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
.note{{color:var(--mut);font-size:15px;margin:.6em 0 0}}
ul.kv{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}}
ul.kv li{{display:flex;flex-direction:column;background:#f5f8fb;border:1px solid var(--line);border-radius:10px;padding:11px 13px}}
ul.kv b{{order:2;font-weight:600;color:var(--faint);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;margin-top:3px}}
ul.kv > li > span{{order:1;font-family:var(--serif);font-size:22px;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}}
ul.kv small.vs{{order:3;color:var(--faint);font-size:12.5px;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:4px}}
th,td{{padding:9px 10px;text-align:left}}
thead th{{color:var(--faint);font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--line)}}
tbody tr:nth-child(odd){{background:#f5f8fb}}
td:nth-child(n+2),thead th:nth-child(n+2){{text-align:right;font-variant-numeric:tabular-nums}}
td.t,th.t{{text-align:left}}
svg{{display:block;margin:6px 0}}
.ax{{fill:var(--mut);font-size:13px;text-anchor:middle}}.ax2{{fill:var(--faint);font-size:13px}}
nav.toc ul{{margin:0;padding-left:18px;columns:2;column-gap:20px;font-size:15px}}nav.toc li{{margin:3px 0;break-inside:avoid}}
@media(max-width:520px){{nav.toc ul{{columns:1}}}}
nav.jump{{font-size:14px;margin:0 0 12px;display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center}}
nav.jump a{{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:5px 11px;text-decoration:none;font-weight:600}}
nav.qa{{display:block;margin:8px 0 14px}}
nav.qa a{{display:block;border-radius:10px;padding:9px 12px;margin:0 0 6px;font-weight:400;color:var(--ink);font-size:14.5px;line-height:1.45}}
nav.qa a b{{color:var(--brand);margin-right:4px}}nav.qa a:after{{content:" →";color:var(--brand)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
nav.sib{{font-size:14px;color:var(--mut);margin:16px 0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px}}
nav.sib a{{color:var(--brand);font-weight:600}}
footer{{color:var(--faint);font-size:12.5px;margin:28px 0;border-top:1px solid var(--line);padding-top:14px}}
footer a{{color:var(--mut)}}
details.more{{margin:16px 0}}details.more>summary{{cursor:pointer;font-weight:700;color:var(--brand);padding:12px 0;list-style:none}}
details.more>summary::-webkit-details-marker{{display:none}}details.more>summary:before{{content:"▸ "}}details.more[open]>summary:before{{content:"▾ "}}
@media(max-width:620px){{.stats{{grid-template-columns:repeat(2,1fr)}}.two{{grid-template-columns:1fr}}.hero h1{{font-size:30px}}
.card{{padding:18px 15px}}.card h2{{font-size:21px}}.stat .n{{font-size:23px}}ul.kv > li > span{{font-size:19px}}ul.kv b{{font-size:11px}}
table{{font-size:13.5px}}th,td{{padding:7px 6px}}thead th{{font-size:11px;white-space:normal}}
table{{width:100%}}}}
</style></head><body>
<header class="topbar"><div class="wrap"><a class="brand" href="../../">Flood Insurance Data</a><span class="crumb">Flood insurance › {(f'<a href="../{state_slug(_state)}/" style="color:inherit">{html.escape(STATE_NAMES[_state])}</a> › ' if (not IS_STATE and _state in _built_states) else '')}{CS}</span></div></header>
<main class="wrap">
<section class="hero">
<p class="kicker">NFIP records · {CS} · policies as of {POL_ASOF}</p>
<h1>Flood insurance in {CL}</h1>
<div class="stats">
<div class="stat"><div class="n">{m('cost_p50', money(P['p50']))}</div><div class="l">Median / yr, single-family primary home</div></div>
<div class="stat"><div class="n">{m('cost_mo', median_mo)}</div><div class="l">A month, spread over the year</div></div>
<div class="stat"><div class="n">{m('cost_p25', money(P['p25']))}–{m('cost_p75', money(P['p75']))}</div><div class="l">Half pay between</div></div>
<div class="stat"><div class="n">{m('share_below', str(P['share_below']) + '%')}</div><div class="l">Pay below FEMA's full-risk price; those bills move toward it each year</div></div>
</div>
{cmp_line}{_jump}
<a class="btn" href="https://msc.fema.gov/portal/home" rel="noopener" target="_blank">Check your address on FEMA's flood map →</a>
{quick_answers}
{_renew_line}
<p class="note">Your flood zone is set at your exact address and decides whether a lender must require coverage; your price comes mainly from your own building's flood risk, and FEMA's full-risk price is its price for that risk.</p>
</section>

{quote_widget}

{prov_line}

{_toc}

{CARDS}
<p class="note"><a href="#">Back to top ↑</a></p>

<p class="note">What these records cannot tell you (your own premium, private prices, your exact zone) is on the <a href="../../methodology/#limits">methodology page</a>.</p>

<section class="card"><h2>The federal datasets behind this page</h2>
<p class="stand">Every figure comes from a public U.S. federal dataset; estimates are labeled where they appear. This page joins <span data-m="n_sources">@@N_SOURCES@@</span> of them for {CS}. The newest of these downloads was {LATEST_PULL}.</p>
<ul class="srclist">{sources_li}</ul></section>

{sib_html}

<footer>{ATTR} Place names via GeoNames (CC BY 4.0). Figures are aggregates, never individual quotes or records.
<a href="../../about/">About</a> · <a href="../../methodology/">Methodology</a> · <a href="../../data/">Download the data</a> · <a href="../../privacy/">Privacy</a> · <a href="../../terms/">Terms</a></footer>
</main></body></html>"""

SOURCES = page_sources()
HTML = (HTML.replace("@@SOURCES_LI@@", "".join(f'<li><a href="{u}">{html.escape(n)}</a></li>' for n, u in SOURCES))
            .replace("@@N_SOURCES@@", str(len(SOURCES)))
            # Search Console 2026-10-29: nested Dataset objects were checked as Datasets (no description/license/creator);
            # Google's Dataset citation takes text, so each source is one reference string
            .replace('"@@CITATION@@"', json.dumps([f"{n}. {u}" for n, u in SOURCES])))
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
