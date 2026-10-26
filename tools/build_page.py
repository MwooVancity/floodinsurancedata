"""Build one county's flood page from data.json (small datasets) + agg.json (bulk); parameterized by env.
River-style: white cards, every number has a unit, one line of context, source + as-of once.
No verdict, no advice prose. Writes directly to the repo dist path. -> OUT_HTML."""
import json, html, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops script dir; restore for ffcalc
import ffcalc

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
def num(n): return format(int(n), ",") if n is not None else "—"
def src(effective, retrieved, extra=""):
    return (f'<p class="src">Source: FEMA OpenFEMA. Data effective {effective}; retrieved {retrieved}. '
            f'{html.escape(extra)}{" " if extra else ""}{ATTR}</p>')

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
    y0, y1 = years[0], years[-1]; W, H, pad = 680, 220, 28; span = max(1, y1 - y0)
    bars = []
    for y in years:
        c = by[str(y)][0]; x = pad + (y - y0) / span * (W - 2 * pad); bh = (c / maxc) * (H - 2 * pad)
        col = "var(--accent)" if any(y == ty for ty, _ in top_paid) else "var(--bar)"
        bars.append(f'<rect x="{x:.1f}" y="{H-pad-bh:.1f}" width="3.2" height="{bh:.1f}" fill="{col}"><title>{y}: {num(c)} claims, {money(by[str(y)][1])}</title></rect>')
    labs = "".join(f'<text x="{pad+(y-y0)/span*(W-2*pad):.1f}" y="{H-8}" class="ax">{y}</text>' for y in range(((y0+9)//10)*10, y1+1, 10))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="NFIP claims per year">'
            f'{"".join(bars)}<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="var(--line)"/>{labs}</svg>')

def spread_svg():
    p25, p50, p75, p90, frp = P["p25"], P["p50"], P["p75"], P["p90"], P["frp_median"]
    if not p50: return ""
    hi = max(p90 or 0, frp or 0) * 1.1; W, H, pad = 680, 120, 40
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

def card(title, standfirst, body, source=""):
    return f'<section class="card"><h2>{title}</h2><p class="stand">{standfirst}</p>{body}{source}</section>'

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
        if isinstance(pctl, (int, float)): bits.append(f"higher flood risk than about {round(pctl)}% of U.S. counties")
        if isinstance(eald, (int, float)) and eald > 0: bits.append(f"FEMA models roughly {money(eald)} of flood loss a year across all its buildings")
        return (f" {label.lower()}: " + "; ".join(bits) + ".") if bits else ""
    risk_body = ("<ul class='kv'>" + rating_row(cf, "Coastal") + rating_row(inl, "Inland") + "</ul>"
                 "<p class='note'>This is FEMA's plain risk rating for the county, a comparison — not a prediction "
                 "for your home."
                 + _detail(cf, "Coastal") + _detail(inl, "Inland") +
                 " Any loss figure is a whole-county estimate across all buildings, never one home's expected loss or premium.</p>")
    parts = []
    if _present(cf.get("risk_rating")): parts.append(f"coastal flood risk {html.escape(str(cf['risk_rating']))}")
    if _present(inl.get("risk_rating")): parts.append(f"inland flood risk {html.escape(str(inl['risk_rating']))}")
    risk = card("How much flood risk is here?",
                f"FEMA rates {CS}'s " + " and ".join(parts) + " — how this county compares with others, not odds for your address.",
                risk_body, src("NRI 2023 release", RETR))
else:
    risk = card("How much flood risk is here?",
                "FEMA's National Risk Index has no usable flood rating for this county.",
                f"<p class='gap'>Gap: NRI flood expected-annual-loss and national percentile for {CS}. "
                "Next source to pull (reachable host): FEMA NRI county table from gis.fema.gov or the "
                "NRI_Table_Counties.csv download. The public third-party ArcGIS copy was a non-national sample.</p>")

# ---- zone card (policy UNITS) ----
zu = P["zone_units"]
_zshown = list(zu.items())[:8]
_zrest = P["units"] - sum(v for _, v in _zshown)   # units in zones not shown (lower-ranked) + other/unclassified
zone_body = ("<ul class='kv'>" + "".join(
    f"<li><b>Zone {html.escape(z)}</b><span>{num(v)} policy units</span></li>" for z, v in _zshown)
    + (f"<li><b>Other or unclassified zones</b><span>{num(_zrest)} policy units</span></li>" if _zrest > 0 else "")
    + "</ul>")

# suppress on VALID COST observations (cost_n), not raw cohort — a cohort full of null/refund costs
# must not get a spread. agg carries spread_ok = cost_n >= 100.
SMALL_COHORT = not P.get("spread_ok", (P.get("cost_n") or 0) >= 100)
if SMALL_COHORT:
    cost_lead = (f"Only {num(P['cost_n'])} single-family primary-residence NFIP policies in {CS} have a valid "
                 f"recorded cost — too few for a reliable spread, so we show the count and median only. "
                 f"Median annual cost {money(P['p50'])}.")
    cost_body = (f"<ul class='kv'><li><b>Policies with a valid cost</b><span>{num(P['cost_n'])}</span></li>"
                 f"<li><b>Median annual cost</b><span>{money(P['p50'])}</span></li></ul>"
                 "<p class='note'>Suppressed percentile spread: fewer than 100 policies with a valid recorded cost.</p>")
else:
    cost_lead = (f"Among existing single-family primary-residence NFIP policies in {CS}, the median "
                 f"annual cost is {money(P['p50'])}, with the middle half between {money(P['p25'])} and "
                 f"{money(P['p75'])} ({num(P['cost_n'])} policies). This is what current policyholders pay — "
                 f"a new policy on a different building can differ.")
    cost_body = (spread_svg() + "<p class='note'>Each policy's annual cost (premium plus fees), single-family "
                 "primary residences. The bar is the middle half (p25–p75); the orange line is FEMA's full-risk price.</p>")
if P.get("frp_median") and P.get("share_below"):
    cost_lead += (f" Most policyholders here pay below FEMA's full &ldquo;risk-based&rdquo; price — what a policy "
                  f"would cost without today's discounts and yearly caps, about {money(P['frp_median'])} median — "
                  f"the gap a bill can climb toward over time; see below.")
if P.get("coverage_building"):
    cost_body += (f"<p class='note'><b>Coverage in force:</b> {money(P['coverage_building'])} of building and "
                  f"{money(P['coverage_contents'])} of contents coverage across all {CS} policies.</p>")
# monthly framing for the median
median_mo = money(round(P['p50'] / 12)) if P.get("p50") else None

# ---- cost by flood zone (median per zone) ----
czone = P.get("cost_by_zone") or {}
zone_cost_card = ""
if czone:
    rows_ = "".join(f"<tr><td>Zone {html.escape(z)}</td><td>{money(d['median'])}</td><td>{num(d['n'])}</td></tr>"
                    for z, d in czone.items())
    zone_cost_card = card("What does it cost in my flood zone?",
        f"Median annual cost of existing single-family policies by rated flood zone in {CS} — so you can read the row for your own zone (it's on your lender's determination).",
        f"<table><thead><tr><th>Flood zone</th><th>Median annual cost</th><th>Policies</th></tr></thead><tbody>{rows_}</tbody></table>"
        "<p class='note'>Zones with fewer than 50 priced single-family policies are omitted. Your own premium still depends on elevation and coverage.</p>",
        src(POL_ASOF, RETR))

# ---- premium trend: REMOVED. An in-force annual-policy snapshot holds only current-term policies, so
# there are never enough distinct effective-years for an honest like-for-like trend — and showing one
# would contradict the page's own "what this data cannot tell you" note. The glide-path below is the
# sourced, rule-based answer to "is it going up?" instead. (No trend card is rendered.)

gap_lead = (f"{P['share_below']}% of {num(P['below_n'])} single-family policies pay less than FEMA's own "
            f"full-risk price; the median full-risk premium is {money(P['frp_median'])} versus the "
            f"{money(P['p50'])} actually charged.")
# Years-to-full-risk glide path — derived from data we already hold + the statutory annual cap (a RULE,
# not a model). Honest, sourced counter to competitors' black-box projections.
glide_note = ""
_yrs = ffcalc.years_to_full_risk(P.get("p50"), P.get("frp_median"))
if _yrs is not None:
    glide_note = (f"<p class='note'><b>Years to the full-risk price:</b> under the statutory cap, premiums for most "
                  f"primary residences rise at most {int(ffcalc.HFIAA_CAP*100)}% a year (HFIAA cap, FEMA Risk Rating 2.0). At that maximum "
                  f"rate a policy at today's median ({money(P['p50'])}) would take at least about {_yrs} annual "
                  f"renewal{'s' if _yrs != 1 else ''} to reach the median full-risk price ({money(P['frp_median'])}). This is the cap on how "
                  f"fast a bill can climb, not a forecast of any one policy; statutory surcharges and fees are "
                  f"outside the cap.</p>")
claims_lead = (f"Between {C['year_min']} and {C['year_max']}, {CS} had {num(C['rows'])} paid NFIP flood "
               f"claims totalling {money(C['total_paid'])}.")
# the ratio reads like a risk score, so it is demoted to a note with both numbers shown, never the headline.
claims_ratio_note = (f"<p class='note'>That is {num(C['rows'])} paid claims since {C['year_min']} against "
                     f"{num(P['units'])} policies in force today — a cumulative tally spanning ~{C['year_max']-C['year_min']+1} "
                     f"years over a present-day snapshot, not an annual claim rate or a flood probability.</p>")

def _pct(v):
    if v in ABSENT or str(v).strip() in ABSENT: return None
    s = str(v).strip().rstrip("%")
    try: n = int(float(s))
    except ValueError: return None
    return None if n == 0 else f"{n}%"
def _cls(v): return html.escape(str(v)) if (v not in ABSENT and str(v).strip() not in ABSENT) else "—"
def _disc(v): return _pct(v) or "No discount"
crs_rows = "".join(f"<tr><td>{html.escape(c['communityName'].replace('*','').strip().title())}</td><td>{_cls(c.get('classRating'))}</td>"
                   f"<td>{_disc(c.get('sfhaDiscount'))}</td><td>{_disc(c.get('nonSfhaDiscount'))}</td></tr>" for c in crs)
_disc_communities = [c for c in crs if _pct(c.get("sfhaDiscount"))]
if _disc_communities:
    top = max(_disc_communities, key=lambda c: int(_pct(c["sfhaDiscount"]).rstrip("%")))
    crs_lead = (f"{len(_disc_communities)} of {CS}'s {len(crs)} NFIP communities carry a Community Rating System "
                f"discount — a group discount a town earns for extra flood-prevention work — that cuts every "
                f"eligible policy's premium, up to {_pct(top['sfhaDiscount'])} inside the "
                f"high-risk zone ({html.escape(top['communityName'].replace('*','').strip().title())}).")
else:
    crs_lead = (f"None of {CS}'s {len(crs)} NFIP communities currently carries a Community Rating System discount; "
                f"they participate in the NFIP without the extra CRS premium reduction.")

# ---- how to get covered (factual public NFIP rules — the reader's "what do I do next" + the 30-day catch) ----
howto_card = card("How do I actually get covered — and how fast?",
    "Flood damage is almost never covered by a standard homeowners policy; you buy flood insurance separately "
    "through the federal NFIP or a private insurer. Two facts change your timing and your limits:",
    "<ul class='kv'><li><b>Waiting period</b><span>~30 days</span></li>"
    "<li><b>NFIP building limit</b><span>$250,000</span></li>"
    "<li><b>NFIP contents limit</b><span>$100,000</span></li></ul>"
    "<p class='note'>Most NFIP policies take effect <b>30 days after you buy</b>, so you can't buy today and be "
    "covered for a storm this week — a flood-zone letter or an approaching season is a reason to act now. "
    "(Exceptions: no wait when coverage is required to close a loan, or one day after a map change puts a home "
    "in a high-risk zone.) NFIP covers up to <b>$250,000</b> on the building and <b>$100,000</b> on contents "
    "(contents bought separately); higher-value homes add private &ldquo;excess&rdquo; flood insurance. To buy: "
    "call the NFIP at <b>1-877-336-2627</b>, go to <a href='https://www.floodsmart.gov' rel='nofollow noopener' "
    "target='_blank'>FloodSmart.gov</a>, or ask any licensed insurance agent — NFIP's price is set federally, so "
    "it is the same whichever agent you use.</p>",
    '<p class="src">Source: FEMA National Flood Insurance Program — waiting period, coverage limits and how to '
    'buy, via FloodSmart.gov. Not endorsed by FEMA.</p>')

recent_li = "".join(
    f"<li>{html.escape(cal_year(d))} — {html.escape(d.get('incidentType',''))}: "
    f"{html.escape((d.get('declarationTitle') or '').title())}</li>" for d in recent)

# ---- take-up: how common NFIP coverage is here (policy units vs Census housing units) ----
hu = data.get("housing_units")
hu_yr = data.get("housing_units_year", "2023")
if hu and P.get("units"):
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
        f"Source: FEMA OpenFEMA NFIP + U.S. Census ACS 5-year {hu_yr} (B25001), retrieved {RETR}.")
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
        f"Every county in the state shaded by its FEMA flood-risk rating — {CS} is outlined, so you can see whether it runs hotter or cooler than its neighbours.",
        f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px" role="img" aria-label="State counties by flood risk">{"".join(tiles)}</svg>{legend}',
        src("NRI 2023 release", RETR))

# ---- ZIP lookup inside the county (your-place flow) ----
bz = [z for z in (agg["policies"].get("by_zip") or []) if z.get("units")]
zip_card = ""
if bz:
    data_js = json.dumps({z["zip"]: {"u": z["units"], "m": z["median"], "n": z["cost_n"]} for z in bz})
    toprows = "".join(
        f"<tr><td>{html.escape(z['zip'])}</td><td>{money(z['median']) if z.get('median') else '—'}</td>"
        f"<td>{num(z['units'])}</td></tr>" for z in bz[:8])
    zip_card = card("Find your ZIP in this county",
        f"Type your ZIP to see its own NFIP policy count and median cost within {CS}. Biggest ZIPs are listed below.",
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
        src(POL_ASOF, RETR))

# ---- repetitive-loss properties (FEMA IA multiple-loss; a chronic repeat-flood signal, distinct from
# the annual NFIP claims) ----
ml = data.get("multiloss") or {}
multiloss_card = ""
if ml.get("total") is not None:   # 0 is a real, reassuring finding (no chronic repeat-flood homes), not "no data"
    _srl = ml.get("srl") or 0
    _mldate = ml.get("retrieved", RETR)
    multiloss_card = card("How often do the same homes flood here?",
        f"FEMA has recorded {num(ml['total'])} properties in {CS} that flooded more than once and drew "
        f"federal disaster aid for repeat flood losses"
        + (f", including {num(_srl)} rated severe repetitive-loss" if _srl else "") + ".",
        f"<ul class='kv'><li><b>Repeat-loss properties</b><span>{num(ml['total'])}</span></li>"
        + (f"<li><b>Severe repetitive-loss</b><span>{num(_srl)}</span></li>" if _srl else "")
        + "</ul><p class='note'>FEMA-designated repetitive-loss (RL) and severe repetitive-loss (SRL) "
        "properties — individual homes with more than one flood loss over time, aggregated to the county and "
        "distinct from the annual NFIP claim counts above. A high count means the same homes flood again and "
        "again here. These drew FEMA Individual Assistance (for uninsured losses), so read it as a "
        "chronic-flooding signal, not an insured-claims total.</p>",
        src(_mldate, _mldate, "FEMA repetitive-loss flood-property records."))

# ---- payout reality (avg paid + closed-without-payment share) ----
cx = data.get("claims_extra") or {}
payout_card = ""
if cx.get("claims"):
    payout_card = card("Do flood claims here actually pay out?",
        f"Of {num(cx['claims'])} NFIP flood claims ever filed in {CS}, the average paid claim came to "
        f"{money(cx['avg_paid'])}, and {cx['cwop_share']}% were closed with no payment.",
        f"<ul class='kv'><li><b>Average paid claim</b><span>{money(cx['avg_paid'])}</span></li>"
        f"<li><b>Closed with no payment</b><span>{cx['cwop_share']}%</span></li>"
        f"<li><b>Claims that paid</b><span>{num(cx['paid_n'])}</span></li></ul>"
        "<p class='note'>\"Closed without payment\" is not the same as \"denied\" — it includes claims below the "
        "deductible, withdrawn, or duplicate filings. Average is over claims that paid something; a single "
        "home can file across several floods over the years.</p>",
        src(cx.get("retrieved", RETR), cx.get("retrieved", RETR), "FEMA NFIP paid-claim records."))

# ---- claims OUTSIDE the high-risk zone (the "I'm not in the flood zone" rebuttal) ----
outside_note = ""
if cx.get("outside_sfha_pct") is not None:
    outside_note = (f"<p class='note'><b>Floods don't stop at the zone line:</b> {cx['outside_sfha_pct']}% of the "
                    f"NFIP claim dollars paid in {CS} went to policies rated <b>outside</b> the mapped high-risk "
                    f"(A/V) zone. Being outside a Special Flood Hazard Area lowers the odds and drops the federal "
                    f"requirement — it does not mean zero risk. (Insured claims only, by each policy's rated zone.)</p>")

# ---- how common flood insurance is: prefer NFIP penetration (overall + inside-SFHA) over the Census proxy ----
pen = data.get("penetration") or {}
if pen.get("overall_pct") is not None:
    takeup_card = card("How many homes here carry flood insurance?",
        f"About {pen['overall_pct']}% of {CS}'s homes carry an NFIP flood policy — but {pen['sfha_pct']}% of the "
        f"homes inside the mapped high-risk zone do.",
        f"<ul class='kv'><li><b>All homes insured</b><span>{pen['overall_pct']}%</span></li>"
        f"<li><b>High-risk-zone homes insured</b><span>{pen['sfha_pct']}%</span></li>"
        f"<li><b>Residential policies in force</b><span>{num(pen['contracts'])}</span></li></ul>"
        "<p class='note'>FEMA's NFIP residential take-up rate — share of residential structures with an NFIP "
        "policy, overall and inside the Special Flood Hazard Area. NFIP only (excludes private flood insurance); "
        "the structure count is a FEMA estimate.</p>",
        src(pen.get("asof", RETR), pen.get("asof", RETR), "FEMA NFIP residential penetration rates."))
# (else: the Census-based takeup_card defined earlier stands)

# ---- physical flood history (NOAA Storm Events) — distinct from insured claims ----
se = data.get("storm_events") or {}
storm_card = ""
if se.get("events"):
    storm_card = card("How often has it actually flooded here?",
        f"NOAA logged {num(se['events'])} flood, flash-flood or coastal-flood events in {CS} from {se.get('period','1996-2025')}"
        + (f", with about {money(se['damage'])} in reported property damage" if se.get("damage") else "") + ".",
        f"<ul class='kv'><li><b>Flood events logged</b><span>{num(se['events'])}</span></li>"
        + (f"<li><b>Reported property damage</b><span>{money(se['damage'])}</span></li>" if se.get("damage") else "")
        + "</ul><p class='note'>Physical flood events recorded by the National Weather Service for this county "
        "(1996 on), separate from insured NFIP claims — it counts floods that happened, insured or not. Damage "
        "figures are NWS field estimates, not audited, and undercount in early years.</p>",
        src(se.get("period", "1996-2025"), se.get("retrieved", RETR), "NOAA NCEI Storm Events Database."))

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
        src(POL_ASOF, RETR))

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
SOURCES = [
    ("FEMA OpenFEMA — NFIP Policies", "https://www.fema.gov/openfema-data-page/fima-nfip-redacted-policies-v2"),
    ("FEMA OpenFEMA — NFIP Claims", "https://www.fema.gov/openfema-data-page/fima-nfip-redacted-claims-v2"),
    ("FEMA — National Risk Index (flood)", "https://www.fema.gov/flood-maps/products-tools/national-risk-index"),
    ("FEMA OpenFEMA — NFIP Community Status Book (CRS)", "https://www.fema.gov/openfema-data-page/nfip-community-status-book-v1"),
    ("FEMA OpenFEMA — Disaster Declarations Summaries", "https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2"),
    ("FEMA OpenFEMA — Housing Assistance (Owners)", "https://www.fema.gov/openfema-data-page/housing-assistance-program-data-owners-v2"),
    ("U.S. Census Bureau — ACS 5-year B25001 (housing units)", "https://data.census.gov/table/ACSDT5Y2023.B25001"),
    ("FEMA OpenFEMA — Repetitive-Loss Flood Properties", "https://www.fema.gov/openfema-data-page/individual-assistance-multiple-loss-flood-properties-v1"),
]
# conditional sources: list a dataset only when its panel actually renders for THIS county, so the gate's
# source==panel check stays honest and "joins N" is accurate per place.
if (data.get("penetration") or {}).get("overall_pct") is not None:
    SOURCES.append(("FEMA OpenFEMA — NFIP Residential Penetration Rates", "https://www.fema.gov/openfema-data-page/nfip-residential-penetration-rates-v1"))
if (data.get("storm_events") or {}).get("events"):
    SOURCES.append(("NOAA NCEI — Storm Events Database", "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"))
sources_li = "".join(f'<li><a href="{u}">{html.escape(n)}</a></li>' for n, u in SOURCES)
# JSON-LD: Dataset + Place + FAQPage + Breadcrumb
_faq = [
    (f"How much is flood insurance in {CS}?",
     f"Existing single-family NFIP policyholders pay a median {money(P['p50'])} a year, with the middle "
     f"half between {money(P['p25'])} and {money(P['p75'])}. This is what current policies cost, not a quote."),
    (f"Is {CS} flood insurance below FEMA's full-risk price?",
     f"Yes — {P['share_below']}% of single-family policies pay less than FEMA's full-risk premium "
     f"(median full-risk {money(P['frp_median'])} vs {money(P['p50'])} charged)."),
    (f"How many flood claims has {CS} had?",
     f"{num(C['rows'])} paid NFIP claims totalling {money(C['total_paid'])} between {C['year_min']} and {C['year_max']}."),
]
jsonld = json.dumps([
    {"@context": "https://schema.org", "@type": "Dataset",
     "name": f"NFIP flood insurance data for {CL}", "description": META_DESC, "url": CANON,
     "creator": {"@type": "Organization", "name": "FEMA OpenFEMA"},
     "publisher": {"@type": "Organization", "name": "Flood Insurance Data", "url": BASE_URL},
     "dateModified": ISO_DATE, "datePublished": ISO_DATE,
     "citation": [{"@type": "Dataset", "name": n, "url": u} for n, u in SOURCES],
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
quote_widget = f"""<section class="card"><h2>Where would your premium fall?</h2>
<p class="stand">Type your annual flood premium to see where it sits among {CS}'s existing single-family policies. This is a comparison, not a quote.</p>
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
<title>Flood insurance in {CL} — the data</title>
<meta name="description" content="{html.escape(META_DESC)}">
<link rel="canonical" href="{CANON}">
<meta property="og:type" content="website"><meta property="og:title" content="Flood insurance in {html.escape(CL)}">
<meta property="og:description" content="{html.escape(META_DESC)}"><meta property="og:url" content="{CANON}">
{_og_meta}
<script type="application/ld+json">{jsonld}</script>
<style>
:root{{--bg:#eef2f5;--surface:#fff;--ink:#132029;--mut:#5c6b78;--faint:#8795a0;--line:#e3e9ee;
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
.hero h1{{font-size:31px;line-height:1.14;margin:.05em 0 .35em;letter-spacing:-.015em}}
.lede{{color:var(--mut);font-size:16.5px;margin:.2em 0 1.2em;max-width:62ch}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:0 0 14px}}
.stat{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow)}}
.stat .n{{font-size:21px;font-weight:800;letter-spacing:-.01em;font-variant-numeric:tabular-nums}}
.stat .l{{font-size:11.5px;color:var(--faint);margin-top:3px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}}
.chips{{margin:2px 0 10px}}
.chip{{display:inline-block;background:#dde8ee;color:var(--brand-d);border-radius:999px;padding:4px 12px;font-size:12.5px;margin:0 6px 6px 0;font-weight:600}}
.caveat{{color:var(--mut);font-size:14px;margin:.2em 0 1.1em;max-width:62ch}}
.btn{{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;padding:12px 20px;border-radius:10px;box-shadow:var(--shadow)}}
.btn:hover{{filter:brightness(.96)}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px 22px;margin:16px 0;box-shadow:var(--shadow)}}
.card h2{{font-size:20px;font-weight:700;margin:0 0 5px;letter-spacing:-.01em}}
.stand{{margin:0 0 14px}}
.src{{color:var(--faint);font-size:12px;margin:14px 0 0;border-top:1px solid var(--line);padding-top:9px}}
.gap{{color:#9a3d12;font-size:14px;background:#fbf0e9;border:1px solid #f0d9c9;border-radius:9px;padding:10px 13px}}
.note{{color:var(--mut);font-size:13.5px;margin:.6em 0 0}}
ul.kv{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}}
ul.kv li{{display:flex;flex-direction:column;background:#f5f8fb;border:1px solid var(--line);border-radius:10px;padding:11px 13px}}
ul.kv b{{order:2;font-weight:600;color:var(--faint);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;margin-top:3px}}
ul.kv span{{order:1;font-size:19px;font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums}}
table{{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:4px}}
th,td{{padding:9px 10px;text-align:left}}
thead th{{color:var(--faint);font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--line)}}
tbody tr:nth-child(odd){{background:#f5f8fb}}
td:nth-child(n+2),thead th:nth-child(n+2){{text-align:right;font-variant-numeric:tabular-nums}}
svg{{display:block;margin:6px 0}}
.ax{{fill:var(--faint);font-size:10px;text-anchor:middle}}.ax2{{fill:var(--faint);font-size:9px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
nav.sib{{font-size:14px;color:var(--mut);margin:16px 0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px}}
nav.sib a{{color:var(--brand);font-weight:600}}
footer{{color:var(--faint);font-size:12.5px;margin:28px 0;border-top:1px solid var(--line);padding-top:14px}}
footer a{{color:var(--mut)}}
details.more{{margin:16px 0}}details.more>summary{{cursor:pointer;font-weight:700;color:var(--brand);padding:12px 0;list-style:none}}
details.more>summary::-webkit-details-marker{{display:none}}details.more>summary:before{{content:"▸ "}}details.more[open]>summary:before{{content:"▾ "}}
@media(max-width:620px){{.stats{{grid-template-columns:repeat(2,1fr)}}.two,ul.kv{{grid-template-columns:1fr}}.hero h1{{font-size:25px}}
table{{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;width:auto;min-width:100%;white-space:nowrap}}}}
</style></head><body>
<header class="topbar"><div class="wrap"><a class="brand" href="../../">Flood Insurance Data</a><span class="crumb">Flood insurance › {CS}</span></div></header>
<main class="wrap">
<section class="hero">
<h1>Flood insurance in {CL}</h1>
<p class="lede">What existing NFIP policyholders here actually pay, how that compares with FEMA's full-risk price, the flood risk, the claims history, and how to pay less — every figure from public federal data, sourced and dated.</p>
<div class="stats">
<div class="stat"><div class="n">{money(P['p50'])}</div><div class="l">Median / yr</div></div>
<div class="stat"><div class="n">{median_mo}</div><div class="l">Per month</div></div>
<div class="stat"><div class="n">{money(P['p25'])}–{money(P['p75'])}</div><div class="l">Middle half</div></div>
<div class="stat"><div class="n">{P['share_below']}%</div><div class="l">Below full-risk</div></div>
</div>
<p class="chips"><span class="chip">Policies as of {POL_ASOF}</span><span class="chip">{num(P['units'])} policy units in force</span></p>
<p class="caveat">This is what existing single-family policies cost — not a quote. Your own premium depends on your building, coverage and elevation.</p>
<a class="btn" href="https://msc.fema.gov/portal/home" rel="nofollow noopener" target="_blank">Check your address on FEMA's flood map →</a>
<p class="note">Your flood zone is set at your exact address and drives your price and whether coverage is required. Look it up first, then read your zone's row in "What does it cost in my flood zone?" below.</p>
</section>

{card("Am I required to carry it?",
  f"Whether <b>you</b> must carry flood insurance depends on your exact address and loan — look your address up on <a href=\"https://msc.fema.gov/portal/home\" rel=\"nofollow noopener\" target=\"_blank\">FEMA's flood map</a>. The rule: a federally backed mortgage on a building in a high-risk zone (a Special Flood Hazard Area) legally requires it. For context, {P['sfha_share_units']}% of {CS}'s existing NFIP policies sit in those high-risk (A/V) zones — not {P['sfha_share_units']}% of all buildings, and not an answer about your own home.",
  f"<div class='two'><div>{zone_body}</div><div><p class='note'>Zone mix by policy units (summed policyCount). Federal rule: a lender must require flood insurance on a building in a Special Flood Hazard Area with a federally backed loan (42 U.S.C. §4012a). This is the mix of existing policies, not of all buildings, and does not establish any one property's obligation.</p></div></div>",
  src(POL_ASOF, RETR))}

{outside_note}

{card("How much does it cost here?", cost_lead, cost_body, src(POL_ASOF, RETR))}

{howto_card}

{zone_cost_card}

{zip_card}

{card("How do current premiums compare with FEMA's full-risk price?", gap_lead,
  f"<ul class='kv'><li><b>Median charged now</b><span>{money(P['p50'])}</span></li>"
  f"<li><b>Median full-risk price</b><span>{money(P['frp_median'])}</span></li>"
  f"<li><b>Pay below full risk</b><span>{P['share_below']}% of {num(P['below_n'])}</span></li></ul>" + glide_note, src(POL_ASOF, RETR))}

{trend_card}

{card("Can I pay less than the sticker price?", crs_lead,
  f"<table><thead><tr><th>Community</th><th>CRS class</th><th>High-risk discount</th><th>Other-area discount</th></tr></thead><tbody>{crs_rows}</tbody></table>"
  "<p class='note'>The Community Rating System cuts NFIP premiums for every eligible policy in a community that does extra flood work. The discount shown is the community's rate; what share of its policies currently receive it is not in this data. Confirm with your agent.</p>",
  src(RETR, RETR))}

{risk}

{card("What do floods actually pay out here?", claims_lead, claims_svg() +
  f"<p class='note'>Orange bars are the three costliest years: " + ", ".join(f"{y} ({money(p)})" for y, p in top_paid) +
  ". Net building + contents payments by year of loss. Claims are matched by the claims dataset's county code, which may not exactly match a policy's property county.</p>" + claims_ratio_note,
  src(f"{C['year_min']}–{C['year_max']}", RETR))}

{payout_card}

{storm_card}

{multiloss_card}

{tilemap_card}

{takeup_card}

{card("How often is this county a flood disaster?",
  f"{CS} has had {len(fh_events)} distinct federal flood, hurricane or tropical-storm disaster declarations. The most recent:",
  f"<ul>{recent_li}</ul><p class='note'>Distinct storms by calendar year (one storm's emergency and major-disaster declarations are counted once), not individual declaration records.</p>",
  src("declarations through 2026", RETR))}

<details class="more"><summary>More data: FEMA disaster aid &amp; reconciliation</summary>
{card("Did the government pay homeowners after floods?",
  f"FEMA approved {money(h_ihp)} in Individual &amp; Households housing help to {CS} homeowners across {h_disasters} disasters, on {num(h_regs)} valid registrations.",
  "<p class='note'>FEMA Individual Assistance is disaster aid, usually capped and partial — separate from NFIP insurance and not a substitute for a policy.</p>",
  src("owner registrations by disaster", RETR))}

{card("Reconciliation &amp; data completeness", "Our counts are checked against FEMA's official figure and the API's own totals.",
  f"<p class='note'>In-force count: {num(P['units'])} policy units (from {num(P['rows'])} API records; condo-association records carry more than one unit). " +
  (f"FEMA's official count for 2026-07-31 was {num(OFFICIAL)} — a {round(abs(P['units']-OFFICIAL)/OFFICIAL*100,1)}% difference. " if OFFICIAL else "FEMA official reconciliation count pending for this county. ") +
  f"Count reconciliation (not a snapshot proof): {mani_line}.</p>")}
</details>

<section class="card"><h2>What this data cannot tell you</h2>
<ul class="note">
<li>Your own premium — it depends on elevation, coverage and deductible. We show where existing policies fall.</li>
<li>Private (non-NFIP) flood insurance prices.</li>
<li>Your address's exact flood zone — use FEMA's Flood Map Service Center.</li>
<li>Why premiums are rising — we show the gap to full-risk, not the cause.</li>
<li>A year-over-year premium trend — the in-force snapshot holds only current-term policies, so a like-for-like multi-year index isn't possible from this data. A per-effective-year median is shown only where several years of policies exist.</li>
</ul></section>

<section class="card"><h2>The federal datasets behind this page</h2>
<p class="stand">Every figure here comes from a public U.S. federal dataset — no estimates, no private data. This page joins {len(SOURCES)} of them for {CS}, each linked to its official source. Data last pulled {RETR}.</p>
<ul class="srclist">{sources_li}</ul></section>

{quote_widget}

{sib_html}

<footer>{ATTR} Place names via GeoNames (CC BY 4.0). Figures are aggregates, never individual quotes or records.
<a href="../../about/">About</a> · <a href="../../methodology/">Methodology</a> · <a href="../../data/">Download the data</a> · <a href="../../privacy/">Privacy</a> · <a href="../../terms/">Terms</a></footer>
</main></body></html>"""

open(OUT_HTML, "w", encoding="utf-8").write(HTML)
print("wrote", OUT_HTML, len(HTML), "bytes; NRI:", "yes" if NRI else "GAP",
      "; zones=policyUnits; completeness", mani_ok)
