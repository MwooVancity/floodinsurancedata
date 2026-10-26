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
OFFICIAL = int(os.environ.get("FF_OFFICIAL", "132012"))        # FEMA official PIF count (0 = unknown)
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
def pretty_date(s):
    """'2026-10-25' -> 'October 25, 2026' so every block shows one date format; other text passes through."""
    import datetime
    try: d = datetime.date.fromisoformat(str(s)[:10]); return f"{d:%B} {d.day}, {d.year}"
    except ValueError: return s
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
    for v, lab in [(p25, "p25"), (p50, "median"), (p75, "p75"), (p90, "p90")]:
        if v: marks += (f'<line x1="{x(v):.1f}" y1="34" x2="{x(v):.1f}" y2="58" stroke="var(--ink)"/>'
                        f'<text x="{x(v):.1f}" y="26" class="ax" text-anchor="middle">{money(v)}</text>'
                        f'<text x="{x(v):.1f}" y="74" class="ax2" text-anchor="middle">{lab}</text>')
    rng = f'<rect x="{x(p25):.1f}" y="40" width="{x(p75)-x(p25):.1f}" height="12" rx="3" fill="var(--bar)"/>' if p25 and p75 else ""
    frpline = (f'<line x1="{x(frp):.1f}" y1="34" x2="{x(frp):.1f}" y2="58" stroke="var(--accent)" stroke-width="2"/>'
               f'<text x="{x(frp):.1f}" y="96" class="ax2" text-anchor="middle" fill="var(--accent)">full-risk {money(frp)}</text>') if frp else ""
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Annual NFIP cost spread">'
            f'<line x1="{pad}" y1="46" x2="{W-pad}" y2="46" stroke="var(--line)"/>{rng}{marks}{frpline}</svg>')

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
        if isinstance(eald, (int, float)) and eald > 0: bits.append(f"FEMA models roughly {money(eald)} of flood loss a year across all its buildings")
        return (f" {label}: " + "; ".join(bits) + ".") if bits else ""
    risk_body = ("<ul class='kv'>" + rating_row(cf, "Coastal") + rating_row(inl, "Inland") + "</ul>"
                 "<p class='note'>This is FEMA's plain risk rating for the county, a comparison — not a prediction "
                 "for your home. The rating multiplies expected flood loss by a community factor for social "
                 "vulnerability and resilience; the percentile below is expected loss alone, so the two can differ."
                 + _detail(cf, "Coastal") + _detail(inl, "Inland") +
                 " Any loss figure is a whole-county estimate across all buildings, never one home's expected loss or premium.</p>")
    parts = []
    if _present(inl.get("risk_rating")): parts.append(f"{html.escape(str(inl['risk_rating']))} for rivers and heavy rain")
    if _present(cf.get("risk_rating")): parts.append(f"{html.escape(str(cf['risk_rating']))} for coastal flooding")
    risk = card("How much flood risk is here?",
                " and ".join(parts) + ", by FEMA's county rating. That compares this county with others; it is not a forecast for your address.",
                risk_body, src(["nri_rating", "nri_eal_usd"], "NRI 2023 release", RETR))
else:
    risk = card("How much flood risk is here?",
                "FEMA's National Risk Index has no usable flood rating for this county.",
                f"<p class='gap'>Gap: NRI flood expected-annual-loss and national percentile for {CS}. "
                "Next source to pull (reachable host): FEMA NRI county table from gis.fema.gov or the "
                "NRI_Table_Counties.csv download. The public third-party ArcGIS copy was a non-national sample.</p>")

# ---- zone card (policy UNITS) ----
zu = P["zone_units"]
# compact table: zones holding >=1% of units; the rest fold into one disclosed "other" row (phone-friendly)
_zshown = [(z, v) for z, v in list(zu.items())[:8] if v >= 0.01 * P["units"]]
_zrest = P["units"] - sum(v for _, v in _zshown)   # units in zones not shown (lower-ranked) + other/unclassified
def _zrow(label, v): return f"<tr><td>{label}</td><td>{num(v)}</td><td>{round(100 * v / P['units'], 1)}%</td></tr>"
zone_body = ("<table><thead><tr><th>Flood zone</th><th>Policies</th><th>Share</th></tr></thead><tbody>"
    + "".join(_zrow(f"Zone {html.escape(z)}" + (" (high-risk)" if z[:1] in "AV" else ""), v) for z, v in _zshown)
    + (_zrow("Other or unclassified zones", _zrest) if _zrest > 0 else "")
    + "</tbody></table>")

# suppress on VALID COST observations (cost_n), not raw cohort — a cohort full of null/refund costs
# must not get a spread. agg carries spread_ok = cost_n >= 100.
SMALL_COHORT = not P.get("spread_ok", (P.get("cost_n") or 0) >= 100)
if SMALL_COHORT:
    cost_lead = (f"Only {num(P['cost_n'])} single-family primary-residence NFIP policies in {CS} have a valid "
                 f"recorded cost — too few for a reliable spread, so we show the count and median only. "
                 f"Median annual cost {m('cost_p50', money(P['p50']))}.")
    cost_body = (f"<ul class='kv'><li><b>Policies with a valid cost</b><span>{num(P['cost_n'])}</span></li>"
                 f"<li><b>Median annual cost</b><span>{m('cost_p50', money(P['p50']))}</span></li></ul>"
                 "<p class='note'>Suppressed percentile spread: fewer than 100 policies with a valid recorded cost.</p>")
else:
    cost_lead = (f"Typically about {m('cost_p50', money(P['p50']))} a year ({m('cost_mo', money(round(P['p50'] / 12)))} a month), "
                 f"fees included. Half of homeowners here pay between {m('cost_p25', money(P['p25']))} and "
                 f"{m('cost_p75', money(P['p75']))}. To check a quote, use the checker at the top.")
    cost_body = (spread_svg() + "<p class='note'>Each policy's annual cost (premium plus the federal policy fee, "
                 "reserve fund assessment and HFIAA surcharge), single-family primary residences. The bar is the middle "
                 "half (p25–p75), from " + num(P['cost_n']) + " single-family primary-home policies.</p>")
PREM_MED = P.get("prem_median")        # premium charged, before fees: the like-for-like comparator for full-risk
if P.get("coverage_building"):
    cost_body += (f"<p class='note'><b>Coverage in force:</b> {big(P['coverage_building'])} of building and "
                  f"{big(P['coverage_contents'])} of contents coverage across all {CS} policies.</p>")
# monthly framing for the median
median_mo = money(round(P['p50'] / 12)) if P.get("p50") else None

# ---- cost by flood zone (median per zone) ----
czone = P.get("cost_by_zone") or {}
zone_cost_card = ""
if czone:
    rows_ = "".join(f"<tr><td>Zone {html.escape(z)}</td><td>{money(d['median'])}</td><td>{num(d['n'])}</td></tr>"
                    for z, d in czone.items())
    _zlo = min(czone.items(), key=lambda kv: kv[1]["median"]); _zhi = max(czone.items(), key=lambda kv: kv[1]["median"])
    zone_cost_card = card("What does it cost in my flood zone?",
        (f"From about {money(_zlo[1]['median'])} a year (Zone {html.escape(_zlo[0])}) to {money(_zhi[1]['median'])} "
         f"(Zone {html.escape(_zhi[0])}) here. " if len(czone) > 1 else "")
        + "Your zone is on your lender's flood determination or FEMA's map; find its row below.",
        f"<table><thead><tr><th>Flood zone</th><th>Median / yr</th><th>Policies</th></tr></thead><tbody>{rows_}</tbody></table>"
        + (("<p class='note'><b>" + claim("Why can a high-risk zone cost less than Zone X here?", "cost less than",
                                           ("zone_inversion", "==", 1)) + "</b> " + rule("rr2_zone") + "</p>")
           if VALS["zone_inversion"] else "")
        + "<p class='note'>Zones with fewer than 50 priced single-family policies are omitted. Your own premium still depends on elevation and coverage.</p>",
        src(["zone_cost"], POL_ASOF, RETR), id="zone-cost")

# ---- premium trend: REMOVED. An in-force annual-policy snapshot holds only current-term policies, so
# there are never enough distinct effective-years for an honest like-for-like trend — and showing one
# would contradict the page's own "what this data cannot tell you" note. The glide-path below is the
# sourced, rule-based answer to "is it going up?" instead. (No trend card is rendered.)

MX.compare("prem_median", "frp_median")   # like-for-like or it raises
gap_lead = ((claim("Many bills here can keep rising", "rising", ("share_below", ">", 0))
             + f": {m('share_below', str(P['share_below']) + '%')} of policies pay less than FEMA's full-risk price. "
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
                  f"{int(ffcalc.HFIAA_CAP*100)}% cap, a policy at today's median premium ({m('prem_median', money(PREM_MED))}) would take at "
                  f"least about {_yrs} annual renewal{'s' if _yrs != 1 else ''} to reach the median full-risk premium "
                  f"({m('frp_median', money(P['frp_median']))}). "
                  + claim("This is the limit on how fast a bill can climb, not a forecast of any one policy.", "climb",
                          ("frp_median", ">", "prem_median")) + "</p>")
claims_lead = (f"Floods here have led to {m('claims_filed', num(C['rows']))} NFIP flood claims and "
               f"{m('claims_total', big(C['total_paid']))} in payouts since {C['year_min']}"
               + (f"; the worst years were {and_list(y for y, _ in top_paid)}." if top_paid else "."))
# the ratio reads like a risk score, so it is demoted to a note with both numbers shown, never the headline.
claims_ratio_note = (f"<p class='note'>That is {m('claims_filed', num(C['rows']))} claims since {C['year_min']} against "
                     f"{m('units', num(P['units']))} policies in force today — a cumulative tally spanning ~{C['year_max']-C['year_min']+1} "
                     f"years over a present-day snapshot, not an annual claim rate or a flood probability.</p>")

def _pct(v):
    if v in ABSENT or str(v).strip() in ABSENT: return None
    s = str(v).strip().rstrip("%")
    try: n = int(float(s))
    except ValueError: return None
    return None if n == 0 else f"{n}%"
def _cls(v): return html.escape(str(v)) if (v not in ABSENT and str(v).strip() not in ABSENT) else "—"
def _disc(v): return _pct(v) or "No discount"
def _cname(c):
    """FEMA's 'CAPE CANAVERAL, CITY OF' -> 'Cape Canaveral' (the reader looks for their town's name, not the legal form)."""
    n = re.sub(r",\s*(city|town|village|borough|township|county|parish)\s+of\s*$", "", c['communityName'].replace('*', '').strip(), flags=re.I)
    return html.escape(n.title())
# table only for communities with a discount; the rest fold into one named line (a screen of "No discount" rows helps no one)
_has_disc = [c for c in crs if _pct(c.get("sfhaDiscount")) or _pct(c.get("nonSfhaDiscount"))]
_no_disc = [c for c in crs if c not in _has_disc]
crs_rows = "".join(f"<tr><td>{_cname(c)}</td>"
                   f"<td>{_disc(c.get('sfhaDiscount'))}</td><td>{_disc(c.get('nonSfhaDiscount'))}</td><td>{_cls(c.get('classRating'))}</td></tr>" for c in _has_disc)
crs_none_note = (f"<p class='note'><b>No CRS discount ({len(_no_disc)}):</b> " + "; ".join(_cname(c) for c in _no_disc) + ".</p>") if _no_disc else ""
_disc_communities = [c for c in crs if _pct(c.get("sfhaDiscount"))]
if _disc_communities:
    top = max(_disc_communities, key=lambda c: int(_pct(c["sfhaDiscount"]).rstrip("%")))
    crs_lead = (claim("Yes", "yes", ("crs_discount_communities", ">", 0))
                + f", in {len(_disc_communities)} of the {len(crs)} towns here: up to "
                f"{_pct(top['sfhaDiscount'])} off in {_cname(top)}. "
                + rule("crs_auto") + " Find your town below.")
else:
    crs_lead = f"Not through a community discount: none of {CS}'s {len(crs)} NFIP communities has one."

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
    f"<li>{html.escape(cal_year(d))} — {html.escape(d.get('incidentType',''))}: "
    f"{html.escape((d.get('declarationTitle') or '').title())}</li>" for d in recent)

# ---- take-up: how common NFIP coverage is here (policy units vs Census housing units) ----
hu = data.get("housing_units")
hu_yr = data.get("housing_units_year", "2023")
takeup_card = ""
if hu and P.get("units") and (data.get("penetration") or {}).get("overall_pct") is None:   # Census proxy only when FEMA's rate is missing
    tu = round(100 * P["units"] / hu, 1)
    takeup_card = card("How common is flood insurance here?",
        f"{CS} has about {tu} NFIP flood policies for every 100 homes ({num(P['units'])} policy units vs "
        f"{num(hu)} housing units).",
        f"<ul class='kv'><li><b>NFIP policy units</b><span>{num(P['units'])}</span></li>"
        f"<li><b>Housing units</b><span>{num(hu)}</span></li>"
        f"<li><b>Policies per 100 homes</b><span>{tu}</span></li></ul>"
        "<p class='note'>A coverage-commonness proxy: policy units include some multi-unit and "
        "non-residential policies and exclude private flood insurance, so read it as how widespread NFIP "
        "coverage is here, not an exact share of households.</p>",
        src(["units", "housing_units"], f"ACS 5-year {hu_yr}", RETR))
else:
    takeup_card = card("How common is flood insurance here?",
        "Not shown — Census housing-unit data was not available for this county.",
        "<p class='gap'>Gap: U.S. Census ACS 5-year B25001 housing units, to divide into NFIP policy units.</p>")

# ---- state flood-risk tile-map (every county in the state, this one highlighted) ----
import math
GEOID_SELF = os.environ.get("FF_GEOID", "12071")
state_risk = agg.get("state_risk") or []
RISK_COL = {4: "#8a1f11", 3: "#c2591f", 2: "#d9a441", 1: "#6aa0b8", 0: "#bcd4df", -1: "#dfe4e8"}
RISK_ORD = {"Very High": 4, "Relatively High": 3, "Relatively Moderate": 2, "Relatively Low": 1, "Very Low": 0}
def _ord(r): return RISK_ORD.get(r, -1)
tilemap_card = ""
if len(state_risk) >= 4:
    n = len(state_risk); cols = math.ceil(math.sqrt(n * 1.6)); rows_ = math.ceil(n / cols)
    cell, gap = 26, 3; W = cols * (cell + gap) + gap; H = rows_ * (cell + gap) + gap
    tiles = []
    for i, c in enumerate(state_risk):
        x = gap + (i % cols) * (cell + gap); y = gap + (i // cols) * (cell + gap)
        col = RISK_COL[_ord(c.get("rating"))]
        here = (c.get("fips") == GEOID_SELF)
        stroke = ' stroke="#132029" stroke-width="2.5"' if here else ' stroke="#fff" stroke-width="1"'
        tiles.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{col}"{stroke}>'
                     f'<title>{html.escape(c.get("county") or "")}: {html.escape(str(c.get("rating") or "no rating"))}'
                     f'{" (this county)" if here else ""}</title></rect>')
    legend = ('<div class="note" style="margin-top:8px">Flood-risk rating (FEMA National Risk Index): '
              + " ".join(f'<span style="display:inline-block;width:11px;height:11px;border-radius:2px;'
                         f'background:{RISK_COL[o]};vertical-align:middle"></span> {lab}'
                         for lab, o in [("Very Low",0),("Low",1),("Moderate",2),("High",3),("Very High",4)])
              + '. Your county is outlined.</div>')
    tilemap_card = card(f"How {CS} compares across the state",
        ((lambda own: f"{CS} is rated {html.escape(str(own.get('rating')))}: {sum(1 for c in state_risk if _ord(c.get('rating')) >= _ord(own.get('rating')))} "
                        f"of the state's {len(state_risk)} counties are rated the same or higher. {CS} is outlined.")
         (next((c for c in state_risk if c.get("fips") == GEOID_SELF), None) or {"rating": "unrated"})),
        f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" role="img" aria-label="State counties by flood risk">{"".join(tiles)}</svg>{legend}',
        src(["nri_rating"], "NRI 2023 release", RETR))

# ---- ZIP lookup inside the county (your-place flow) ----
bz = [z for z in (agg["policies"].get("by_zip") or []) if z.get("units")]
zip_card = ""
if bz:
    data_js = json.dumps({z["zip"]: {"u": z["units"], "m": z["median"], "n": z["cost_n"]} for z in bz})
    toprows = "".join(
        f"<tr><td>{html.escape(z['zip'])}</td><td>{money(z['median']) if z.get('median') else '—'}</td>"
        f"<td>{num(z['units'])}</td></tr>" for z in bz[:8])
    zip_card = card("Find your ZIP in this county",
        ((lambda meds: f"Costs vary by ZIP here, from about {money(min(meds))} to {money(max(meds))} a year among the largest. " if len(meds) > 1 else "")
         ([z["median"] for z in bz if z.get("median")])) + "Type yours to see its own figures.",
        f'<input id="zq" inputmode="numeric" maxlength="5" placeholder="e.g. {bz[0]["zip"]}" aria-label="Your ZIP code" '
        f'style="font-size:18px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;width:160px">'
        f'<p id="zout" class="note" style="margin-top:10px">Enter a 5-digit ZIP above.</p>'
        f'<table style="margin-top:12px"><thead><tr><th>ZIP</th><th>Median annual cost</th><th>Policy units</th></tr></thead>'
        f'<tbody>{toprows}</tbody></table>'
        '<p class="note">Median shown only for ZIPs with 25+ priced single-family policies; smaller ZIPs show count only.</p>'
        f'<script>var ZD={data_js};var zi=document.getElementById("zq"),zo=document.getElementById("zout");'
        'zi.addEventListener("input",function(){var z=zi.value.trim();var d=ZD[z];'
        'if(!d){zo.textContent=z.length>=5?"No NFIP data for ZIP "+z+" in this county.":"Enter a 5-digit ZIP above.";return;}'
        'zo.innerHTML="<b>"+z+"</b>: "+d.u.toLocaleString()+" policy units"+(d.m?("; median $"+d.m.toLocaleString()+" / yr ("+d.n.toLocaleString()+" priced policies)"):" (too few priced policies for a median).");});'
        '</script>',
        src(["zip_cost", "units"], POL_ASOF, RETR))

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
        f"<ul class='kv'><li><b>Repeat-flood damage records</b><span>{m('ml_total', num(ml['total']))}</span></li>"
        + (f"<li><b>Records from homes hit 4+ times</b><span>{m('ml_srl', num(_srl))}</span></li>" if _srl else "")
        + "</ul><p class='note'>One home appears once for each declared disaster that damaged it, so this counts "
        "damage events on repeat-flooded homes, not distinct homes (FEMA says these records cannot be totaled by "
        "property). Disaster-aid applications since 2002, separate from NFIP insurance claims.</p>",
        src(["ml_total"], _mldate, _mldate))

# ---- payout reality (avg paid + closed-without-payment share) ----
cx = data.get("claims_extra") or {}
payout_card = ""
if cx.get("claims"):
    _paid_pct = round(100 - cx["cwop_share"], 1)
    _ans = (claim("Most do", "most", ("cwop_share", "<", 50)) + f": {_paid_pct}% of claims here paid something"
            if cx["cwop_share"] < 50 else
            claim("Most don't", "most", ("cwop_share", ">", 50)) + f": {m('cwop_share', str(cx['cwop_share']) + '%')} of claims here closed with no payment"
            if cx["cwop_share"] > 50 else f"About half: {m('cwop_share', str(cx['cwop_share']) + '%')} of claims here closed with no payment")
    payout_card = card("Do flood claims here actually pay out?",
        f"{_ans}. The average paid claim was {m('avg_paid', money(cx['avg_paid']))}.",
        f"<ul class='kv'><li><b>Average paid claim</b><span>{m('avg_paid', money(cx['avg_paid']))}</span></li>"
        f"<li><b>Closed with no payment</b><span>{m('cwop_share', str(cx['cwop_share']) + '%')}</span></li>"
        f"<li><b>Claims that paid</b><span>{m('claims_paid_n', num(cx['paid_n']))}</span></li></ul>"
        f"<p class='note'>{rule('cwop')} The average is over claims that paid something; a single home can file "
        "across several floods over the years.</p>",
        src(["claims_filed", "avg_paid", "cwop_share"], cx.get("retrieved", RETR), cx.get("retrieved", RETR)))

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
        + (f"<li><b>Zone X median cost</b><span>{money(_xmed)}</span></li>" if _xmed else "")
        + f"</ul><p class='note'>{rule('lender_any_zone')} Insured claims only, by each policy's rated zone.</p>",
        src(["outside_sfha_dollars", "outside_sfha_policies", "zone_cost"], cx.get("retrieved", RETR), cx.get("retrieved", RETR)))

# ---- how common flood insurance is: prefer NFIP penetration (overall + inside-SFHA) over the Census proxy ----
pen = data.get("penetration") or {}
if pen.get("overall_pct") is not None:
    takeup_card = card("How many homes here carry flood insurance?",
        (f"About 1 in {round(100 / pen['overall_pct'])} homes here has flood insurance ({m('pen_overall', str(pen['overall_pct']) + '%')}). "
         if pen["overall_pct"] else f"Almost no homes here have NFIP flood insurance ({m('pen_overall', str(pen['overall_pct']) + '%')}). ")
        + f"Inside the high-risk zone it's {m('pen_sfha', str(pen['sfha_pct']) + '%')}.",
        f"<ul class='kv'><li><b>All homes insured</b><span>{m('pen_overall', str(pen['overall_pct']) + '%')}</span></li>"
        f"<li><b>High-risk-zone homes insured</b><span>{m('pen_sfha', str(pen['sfha_pct']) + '%')}</span></li>"
        f"<li><b>Residential policies in force</b><span>{num(pen['contracts'])}</span></li></ul>"
        "<p class='note'>FEMA's NFIP residential take-up rate — share of residential structures with an NFIP "
        "policy, overall and inside the Special Flood Hazard Area. NFIP only (excludes private flood insurance); "
        "the structure count is a FEMA estimate.</p>",
        src(["pen_overall", "pen_sfha"], pen.get("asof", RETR), pen.get("asof", RETR)))
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
        + "</ul><p class='note'>Physical flood events recorded by the National Weather Service for this county "
        "(1996 on), separate from insured NFIP claims — it counts floods that happened, insured or not. Damage "
        "figures are NWS field estimates, not audited, and undercount in early years.</p>",
        src(["storm_events", "storm_damage"], se.get("period", "1996-2025"), se.get("retrieved", RETR)))

# ---- premium trend: median cost by the YEAR a policy was written (cohort-mix caveat, not a like-for-like index) ----
cyear = agg["policies"].get("cost_by_year") or {}
trend_card = ""
if len(cyear) >= 3:
    yrs = sorted(cyear.items())[-8:]
    rows_ = "".join(f"<tr><td>{y}</td><td>{money(d['median'])}</td><td>{num(d['n'])}</td></tr>" for y, d in yrs)
    trend_card = card("What have premiums done over time here?",
        f"Median annual cost of {CS} single-family policies by the year each policy was written, "
        f"{yrs[0][0]} to {yrs[-1][0]}.",
        f"<table><thead><tr><th>Policy written</th><th>Median annual cost</th><th>Policies</th></tr></thead><tbody>{rows_}</tbody></table>"
        "<p class='note'>This is what policies <i>written in each year</i> cost — NOT the same homes tracked over "
        "time, so it reflects which properties bought each year and FEMA's Risk Rating 2.0 phase-in, not a "
        "like-for-like price index. For how a single bill can rise, see the full-risk glide-path above. Years with "
        "under 30 priced policies are omitted.</p>",
        src(["cost_p50"], POL_ASOF, RETR))

mani = agg.get("manifest", {})
mani_ok = all(v.get("complete") for v in mani.values()) if mani else False
mani_line = "; ".join(f"{k}: {v['unique_fetched']}/{v['reported_total']} fetched"
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
places = [p for p in places if p.get("slug") != SLUG]
places.append({"slug": SLUG, "label": CL, "short": CS, "geoid": GEOID,
               "units": P["units"], "median": P["p50"], "state": agg.get("nri", {}).get("state") if agg.get("nri") else None})
places.sort(key=lambda p: -(p.get("units") or 0))
json.dump(places, open(PLACES, "w"), indent=1)
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
if siblings:
    _lbl = f"Other {html.escape(_state)} counties" if len(_same) >= 3 else "Compare other counties"
    sib_html = (f"<nav class='sib'><b>{_lbl}:</b> " +
                " · ".join(f'<a href="../{p["slug"]}/">{html.escape(p["short"])}</a>' for p in siblings) +
                ' · <a href="../../">all places</a></nav>')
else:
    sib_html = '<nav class="sib"><a href="../../">Browse all places by state →</a></nav>'
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
jsonld = json.dumps([
    {"@context": "https://schema.org", "@type": "Dataset",
     "name": f"NFIP flood insurance data for {CL}", "description": META_DESC, "url": CANON,
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
  out.textContent='$'+v.toLocaleString()+' is '+msg+' (p25 $'+P.p25.toLocaleString()+', median $'+P.p50.toLocaleString()+', p75 $'+P.p75.toLocaleString()+').';
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
<header class="topbar"><div class="wrap"><a class="brand" href="../../">Flood Insurance Data</a><span class="crumb">Flood insurance › {CS}</span></div></header>
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
<p class="chips"><span class="chip">{num(P['units'])} insured units in force (all types)</span></p>
<p class="caveat">This is what existing single-family policies cost — not a quote. Your own premium depends on your building, coverage and elevation.</p>
<a class="btn" href="https://msc.fema.gov/portal/home" rel="nofollow noopener" target="_blank">Check your address on FEMA's flood map →</a>
<p class="note">Your flood zone is set at your exact address and drives your price and whether coverage is required. Look it up first, then read your zone's row in "What does it cost in my flood zone?" below.</p>
</section>

{quote_widget}

{card("Am I required to carry it?",
  rule("purchase_answer") + " Check your zone on <a href=\"https://msc.fema.gov/portal/home\" rel=\"nofollow noopener\" target=\"_blank\">FEMA's flood map</a>.",
  f"<p class='note'>{m('sfha_share', str(P['sfha_share_units']) + '%')} of {CS}'s NFIP policies are in high-risk zones (not {P['sfha_share_units']}% of all buildings, and not an answer about your own home).</p>"
  f"{zone_body}<p class='note'>Policies by rated zone (summed policyCount; condo buildings count each unit). {rule('lender_any_zone')}</p>",
  src(["units", "sfha_share"], POL_ASOF, RETR) + src_rules(["purchase_answer", "lender_any_zone"]), id="required")}

{outside_note}

{card("How much does it cost here?", cost_lead, cost_body, src(["cost_p50", "prem_median", "frp_median", "coverage"], POL_ASOF, RETR))}

{howto_card}

{zone_cost_card}

{zip_card}

{card("How do current premiums compare with FEMA's full-risk price?", gap_lead,
  f"<ul class='kv'><li><b>Median premium charged (before fees)</b><span>{m('prem_median', money(PREM_MED))}</span></li>"
  f"<li><b>Median full-risk premium</b><span>{m('frp_median', money(P['frp_median']))}</span></li>"
  f"<li><b>Pay below full-risk</b><span>{m('share_below', str(P['share_below']) + '%')} of {num(P['below_n'])}</span></li></ul>" + glide_note,
  src(["prem_median", "frp_median", "share_below"], POL_ASOF, RETR))}

{trend_card}

{card("Can I pay less than the sticker price?", crs_lead,
  (f"<table><thead><tr><th>Community</th><th>High-risk zone</th><th>Other areas</th><th>CRS class</th></tr></thead><tbody>{crs_rows}</tbody></table>" if crs_rows else "")
  + crs_none_note +
  "<p class='note'>The Community Rating System cuts NFIP premiums for every eligible policy in a community that does extra flood work. The discount shown is the community's rate; what share of its policies currently receive it is not in this data. Confirm with your agent.</p>",
  src(["crs_discount"], RETR, RETR))}

{risk}

{card("What do floods actually pay out here?", claims_lead, claims_svg() +
  f"<p class='note'>Orange bars are the three costliest years: " + ", ".join(f"{y} ({money(p)})" for y, p in top_paid) +
  f". Total paid {money(C['total_paid'])}: net building + contents payments by year of loss. Claims are matched by the claims dataset's county code, which may not exactly match a policy's property county.</p>" + claims_ratio_note,
  src(["claims_filed", "claims_total"], f"{C['year_min']}–{C['year_max']}", RETR))}

{payout_card}

{storm_card}

{multiloss_card}

{tilemap_card}

{takeup_card}

{card("How often is this county a flood disaster?",
  f"{m('declarations', str(len(fh_events)))} federal disasters for floods or storms here"
  + (f"; the latest was {html.escape((recent[0].get('declarationTitle') or '').title())} ({html.escape(cal_year(recent[0]))})." if recent else "."),
  f"<ul>{recent_li}</ul><p class='note'>Distinct storms by calendar year (one storm's emergency and major-disaster declarations are counted once), not individual declaration records.</p>",
  src(["declarations"], "declarations through 2026", RETR))}

{card("Did the government pay homeowners after floods?",
  ((claim("Yes", "yes", ("ia_paid", ">", 0)) + f", but not much per household: FEMA approved {m('ia_paid', big(h_ihp))} for homeowners here, "
    f"about {money(h_ihp / h_regs)} per registration"
    + (f", against an average paid flood claim of {m('avg_paid', money((data.get('claims_extra') or {})['avg_paid']))}"
       if (data.get('claims_extra') or {}).get('avg_paid') else "") + ".")
   if h_ihp and h_regs else "No FEMA housing aid to homeowners here is on record."),
  f"<p class='note'>{rule('ia_partial')}</p>",
  src(["ia_paid", "ia_regs"] + (["avg_paid"] if (data.get('claims_extra') or {}).get('avg_paid') and h_ihp and h_regs else []),
      "owner registrations by disaster", RETR))}

{card("Reconciliation &amp; data completeness", "Our counts are checked against FEMA's official figure and the API's own totals.",
  f"<p class='note'>In-force count: {num(P['units'])} policy units (from {num(P['rows'])} API records; condo-association records carry more than one unit). " +
  (f"FEMA's official count for 2026-07-31 was {num(OFFICIAL)} — a {round(abs(P['units']-OFFICIAL)/OFFICIAL*100,1)}% difference. " if OFFICIAL else "FEMA official reconciliation count pending for this county. ") +
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
<p class="stand">Every figure comes from a public U.S. federal dataset; estimates are labeled where they appear. This page joins @@N_SOURCES@@ of them for {CS}. Last pulled {LATEST_PULL}.</p>
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
print("wrote", OUT_HTML, len(HTML), "bytes; NRI:", "yes" if NRI else "GAP",
      "; zones=policyUnits; completeness", mani_ok)
