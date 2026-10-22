"""Build the Lee County FL flood page from data.json (small datasets) + agg.json (bulk).
River-style: white cards, every number has a unit, one line of context, source + as-of once.
No verdict, no advice prose. Writes directly to the repo dist path. -> OUT_HTML."""
import json, html, os
from collections import defaultdict

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
fh = [d for d in decl if d.get("incidentType") in ("Flood", "Hurricane", "Tropical Storm", "Coastal Storm", "Severe Storm")]
fh_events = {d.get("disasterNumber") for d in fh}
recent, seen = [], set()
for d in sorted(fh, key=lambda x: x.get("declarationDate") or "", reverse=True):
    dn = d.get("disasterNumber")
    if dn in seen: continue
    seen.add(dn); recent.append(d)
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
    def risk_rows(block, label):
        rr, pctl, ealr = block.get("risk_rating"), block.get("eal_national_pctl"), block.get("eal_rating")
        if not _present(rr): return ""
        p = f" ({round(pctl)}th national percentile)" if isinstance(pctl, (int, float)) else ""
        eal = f"<li><b>{label} expected annual loss</b><span>{html.escape(str(ealr))}{p}</span></li>" if _present(ealr) else ""
        return f"<li><b>{label} flood risk</b><span>{html.escape(str(rr))}</span></li>" + eal
    risk_body = "<ul class='kv'>" + risk_rows(cf, "Coastal") + risk_rows(inl, "Inland") + "</ul>"
    parts = []
    if _present(cf.get("risk_rating")): parts.append(f"coastal flood risk {html.escape(str(cf['risk_rating']))}")
    if _present(inl.get("risk_rating")): parts.append(f"inland flood risk {html.escape(str(inl['risk_rating']))}")
    risk = card("How much flood risk is here?",
                f"FEMA's National Risk Index rates {CS}'s " + " and ".join(parts) + ", from expected annual loss.",
                risk_body, src("NRI 2023 release", RETR))
else:
    risk = card("How much flood risk is here?",
                "FEMA's National Risk Index has no usable flood rating for this county.",
                f"<p class='gap'>Gap: NRI flood expected-annual-loss and national percentile for {CS}. "
                "Next source to pull (reachable host): FEMA NRI county table from gis.fema.gov or the "
                "NRI_Table_Counties.csv download. The public third-party ArcGIS copy was a non-national sample.</p>")

# ---- zone card (policy UNITS) ----
zu = P["zone_units"]
zone_body = "<ul class='kv'>" + "".join(
    f"<li><b>Zone {html.escape(z)}</b><span>{num(v)} policy units</span></li>" for z, v in list(zu.items())[:8]) + "</ul>"

cost_lead = (f"Among existing single-family primary-residence NFIP policies in {CS}, the median "
             f"annual cost is {money(P['p50'])}, with the middle half between {money(P['p25'])} and "
             f"{money(P['p75'])} ({num(P['cost_n'])} policies). This is what current policyholders pay — "
             f"a new policy on a different building can differ.")
gap_lead = (f"{P['share_below']}% of {num(P['below_n'])} single-family policies pay less than FEMA's own "
            f"full-risk price; the median full-risk premium is {money(P['frp_median'])} versus the "
            f"{money(P['p50'])} actually charged.")
claims_lead = (f"Between {C['year_min']} and {C['year_max']}, {CS} had {num(C['rows'])} paid NFIP flood "
               f"claims totalling {money(C['total_paid'])} — about {C['cumulative_per_100_current_units']} "
               f"claims over that whole period for every 100 policies in force today (a cumulative tally, "
               f"not an annual rate or a flood probability).")

def _pct(v):
    if v in ABSENT or str(v).strip() in ABSENT: return None
    s = str(v).strip().rstrip("%")
    try: n = int(float(s))
    except ValueError: return None
    return None if n == 0 else f"{n}%"
def _cls(v): return html.escape(str(v)) if (v not in ABSENT and str(v).strip() not in ABSENT) else "—"
def _disc(v): return _pct(v) or "No discount"
crs_rows = "".join(f"<tr><td>{html.escape(c['communityName'].title())}</td><td>{_cls(c.get('classRating'))}</td>"
                   f"<td>{_disc(c.get('sfhaDiscount'))}</td><td>{_disc(c.get('nonSfhaDiscount'))}</td></tr>" for c in crs)
_disc_communities = [c for c in crs if _pct(c.get("sfhaDiscount"))]
if _disc_communities:
    top = max(_disc_communities, key=lambda c: int(_pct(c["sfhaDiscount"]).rstrip("%")))
    crs_lead = (f"{len(_disc_communities)} of {CS}'s {len(crs)} NFIP communities carry a Community Rating System "
                f"discount that cuts every eligible policy's premium — up to {_pct(top['sfhaDiscount'])} inside the "
                f"high-risk zone ({html.escape(top['communityName'].title())}).")
else:
    crs_lead = (f"None of {CS}'s {len(crs)} NFIP communities currently carries a Community Rating System discount; "
                f"they participate in the NFIP without the extra CRS premium reduction.")

recent_li = "".join(
    f"<li>{html.escape(str(d.get('fyDeclared')))} — {html.escape(d.get('incidentType',''))}: "
    f"{html.escape((d.get('declarationTitle') or '').title())}</li>" for d in recent)

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
siblings = [p for p in places if p.get("slug") != SLUG][:5]
sib_html = ("<nav class='sib'><b>Compare nearby:</b> " +
            " · ".join(f'<a href="../{p["slug"]}/">{html.escape(p["short"])}</a>' for p in siblings) +
            ' · <a href="../../">all places</a></nav>') if siblings else '<nav class="sib"><a href="../../">All places</a></nav>'
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

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flood insurance in {CL} — the data</title>
<meta name="description" content="{html.escape(META_DESC)}">
<link rel="canonical" href="{CANON}">
<meta property="og:type" content="website"><meta property="og:title" content="Flood insurance in {html.escape(CL)}">
<meta property="og:description" content="{html.escape(META_DESC)}"><meta property="og:url" content="{CANON}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{jsonld}</script>
<style>
nav.sib{{font-size:13px;color:var(--mut);margin:10px 0}}nav.sib a{{color:var(--brand)}}
.crumb{{font-size:13px;color:var(--mut);margin:4px 0}}.crumb a{{color:var(--brand)}}
:root{{--bg:#f4f6f8;--card:#fff;--ink:#16202b;--mut:#5a6672;--line:#d7dde3;--bar:#9db4c6;--accent:#b4531f;--brand:#1f5c7a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:16px}}
header h1{{font-size:26px;margin:.2em 0}}
.chip{{display:inline-block;background:#e7edf2;color:var(--mut);border-radius:20px;padding:3px 11px;font-size:13px;margin-right:6px}}
.answer{{background:var(--brand);color:#fff;border-radius:12px;padding:16px 18px;font-size:18px;margin:14px 0}}
.answer b{{font-size:22px}}.answer .caveat{{display:block;font-size:13px;opacity:.9;margin-top:8px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:12px 0}}
.card h2{{font-size:18px;margin:0 0 6px}}.stand{{margin:0 0 12px}}
.src{{color:var(--mut);font-size:12px;margin:10px 0 0}}.gap{{color:var(--accent);font-size:14px}}
ul.kv{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:6px 18px}}
ul.kv li{{display:flex;justify-content:space-between;border-bottom:1px dotted var(--line);padding:4px 0;font-size:14px}}
ul.kv b{{font-weight:600}}ul.kv span{{color:var(--mut)}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{text-align:left;padding:6px 4px;border-bottom:1px solid var(--line)}}th{{color:var(--mut);font-weight:600}}
.ax{{fill:var(--mut);font-size:10px;text-anchor:middle}}.ax2{{fill:var(--mut);font-size:9px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media(max-width:560px){{.two{{grid-template-columns:1fr}}ul.kv{{grid-template-columns:1fr}}}}
.note{{color:var(--mut);font-size:13px}}footer{{color:var(--mut);font-size:12px;margin:24px 0}}
</style></head><body><div class="wrap">
<header>
<p class="crumb"><a href="../../">Flood insurance</a> › {CS}</p>
<span class="chip">Policies as of {POL_ASOF}</span><span class="chip">{num(P['units'])} policy units in force</span>
<h1>Flood insurance in {CL}</h1>
</header>

<div class="answer">Existing single-family policyholders here pay a median <b>{money(P['p50'])}</b> a year
(middle half {money(P['p25'])}–{money(P['p75'])}). {P['share_below']}% pay less than FEMA's full-risk price.
<span class="caveat">This is what current policies cost, not a quote — your own premium depends on your building, coverage and elevation.</span></div>

{risk}

{card("Am I required to carry it?",
  f"About {P['sfha_share_units']}% of {CS} policy units sit in a high-risk Special Flood Hazard Area (zones A/V), where a federally backed mortgage legally requires flood insurance.",
  f"<div class='two'><div>{zone_body}</div><div><p class='note'>Zone mix by policy units (summed policyCount). Federal rule: a lender must require flood insurance on a building in a Special Flood Hazard Area with a federally backed loan (42 U.S.C. §4012a). This is the mix of existing policies, not of all buildings, and does not establish any one property's obligation.</p></div></div>",
  src(POL_ASOF, RETR))}

{card("How much does it cost here?", cost_lead, spread_svg() +
  "<p class='note'>Each policy's annual cost (premium plus fees), single-family primary residences. The bar is the middle half (p25–p75); the orange line is FEMA's full-risk price.</p>", src(POL_ASOF, RETR))}

{card("How far below the true price is it?", gap_lead,
  f"<ul class='kv'><li><b>Median charged now</b><span>{money(P['p50'])}</span></li>"
  f"<li><b>Median full-risk price</b><span>{money(P['frp_median'])}</span></li>"
  f"<li><b>Pay below full risk</b><span>{P['share_below']}% of {num(P['below_n'])}</span></li></ul>", src(POL_ASOF, RETR))}

{card("What do floods actually pay out here?", claims_lead, claims_svg() +
  f"<p class='note'>Orange bars are the three costliest years: " + ", ".join(f"{y} ({money(p)})" for y, p in top_paid) +
  ". Net building + contents payments by year of loss. Claims are matched by the claims dataset's county code, which may not exactly match a policy's property county.</p>",
  src(f"{C['year_min']}–{C['year_max']}", RETR))}

{card("How often is this county a flood disaster?",
  f"{CS} has had {len(fh_events)} distinct federal flood, hurricane or tropical-storm disaster declarations. The most recent:",
  f"<ul>{recent_li}</ul><p class='note'>Distinct declared events (deduplicated by disaster number), not individual declaration records.</p>",
  src("declarations through 2026", RETR))}

{card("Did the government pay homeowners after floods?",
  f"FEMA approved {money(h_ihp)} in Individual &amp; Households housing help to {CS} homeowners across {h_disasters} disasters, on {num(h_regs)} valid registrations.",
  "<p class='note'>FEMA Individual Assistance is disaster aid, usually capped and partial — separate from NFIP insurance and not a substitute for a policy.</p>",
  src("owner registrations by disaster", RETR))}

{card("Can I pay less than the sticker price?", crs_lead,
  f"<table><thead><tr><th>Community</th><th>CRS class</th><th>High-risk discount</th><th>Other-area discount</th></tr></thead><tbody>{crs_rows}</tbody></table>"
  "<p class='note'>The Community Rating System cuts NFIP premiums for every eligible policy in a community that does extra flood work. The discount shown is the community's rate; what share of its policies currently receive it is not in this data. Confirm with your agent.</p>",
  src("Community Status Book", RETR))}

{card("Reconciliation &amp; data completeness", "Our counts are checked against FEMA's official figure and the API's own totals.",
  f"<p class='note'>In-force count: {num(P['units'])} policy units (from {num(P['rows'])} API records; condo-association records carry more than one unit). " +
  (f"FEMA's official count for 2026-07-31 was {num(OFFICIAL)} — a {round(abs(P['units']-OFFICIAL)/OFFICIAL*100,1)}% difference. " if OFFICIAL else "FEMA official reconciliation count pending for this county. ") +
  f"Pull completeness: {mani_line}.</p>")}

<section class="card"><h2>What this data cannot tell you</h2>
<ul class="note">
<li>Your own premium — it depends on elevation, coverage and deductible. We show where existing policies fall.</li>
<li>Private (non-NFIP) flood insurance prices.</li>
<li>Your address's exact flood zone — use FEMA's Flood Map Service Center.</li>
<li>Why premiums are rising — we show the gap to full-risk, not the cause.</li>
</ul></section>

{quote_widget}

{sib_html}

<footer>{ATTR} Place names via GeoNames (CC BY 4.0). Figures are aggregates, never individual quotes or records.
<a href="../../methodology/">Methodology</a> · <a href="../../data/">Download the data</a></footer>
</div></body></html>"""

open(OUT_HTML, "w", encoding="utf-8").write(HTML)
print("wrote", OUT_HTML, len(HTML), "bytes; NRI:", "yes" if NRI else "GAP",
      "; zones=policyUnits; completeness", mani_ok)
