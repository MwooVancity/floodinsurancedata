"""Build the shared site pages from places.json: home+lookup, methodology, data (CSV),
sitemap.xml, robots.txt, llms.txt. Reads per-county agg.json for the download table.
Env: FF_PLACES (places.json), FF_DIST (dist dir), FF_DATADIR (per-county data root), FF_BASEURL."""
import csv, json, os, html

PLACES = os.environ.get("FF_PLACES", "places.json")
DIST = os.environ.get("FF_DIST", "dist")
DATADIR = os.environ.get("FF_DATADIR", "data")
BASE = os.environ.get("FF_BASEURL", "https://example.com").rstrip("/")
RETR = os.environ.get("FF_RETR", "October 22, 2026")   # data retrieval date, for Privacy/Terms "last updated"
places = json.load(open(PLACES)) if os.path.exists(PLACES) else []
# fail-closed: include ONLY counties that passed this run (published.json). A county that rendered a
# page but failed the gate/criteria is in places.json but not here, so it never reaches home/sitemap/CSV.
pub_path = os.environ.get("FF_PUBLISHED")
if pub_path and os.path.exists(pub_path):
    published = set(json.load(open(pub_path)))
    places = [p for p in places if p.get("slug") in published]
places.sort(key=lambda p: -(p.get("units") or 0))
# hidden counties (noindex until Search Console watches them) are linked for readers but never sent to search engines
indexable = [p for p in places if p.get("indexable", True)]
def cdir(slug):   # county data lives in data/c/<slug> (one pipeline); older builds in data/<slug>
    return os.path.join(DATADIR, "c", slug) if os.path.isdir(os.path.join(DATADIR, "c", slug)) else os.path.join(DATADIR, slug)

def money(n): return "$" + format(int(n + 0.5) if n >= 0 else -int(-n + 0.5), ",") if n is not None else "—"   # half rounds up, same as build_page
def wr(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(s)

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google-site-verification" content="geYcfFcAsSIVIT2iHnH60suuJ4t3fx7unryWmcbos6A"><title>{title}</title>
<meta name="description" content="{desc}"><link rel="canonical" href="{canon}">
<style>:root{{--bg:#f4f7f8;--surface:#fff;--ink:#132029;--mut:#55656f;--faint:#7d8c96;--line:#dbe3e7;--brand:#15617f;--brand-d:#0e4a61;--accent:#c2591f;--r:12px;--gut:20px;
 --serif:"Iowan Old Style","Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;--mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;--shadow:none}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.62 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:740px;margin:0 auto;padding:0 var(--gut)}}
.topbar{{background:var(--brand-d)}}.topbar .wrap{{padding:11px var(--gut)}}.topbar a{{color:#fff;font-weight:800;text-decoration:none}}
.hero{{padding:30px 0 4px}}h1{{font-family:var(--serif);font-weight:600;font-size:36px;line-height:1.1;letter-spacing:-.01em;margin:.1em 0 .3em}}
h2{{font-family:var(--serif);font-size:24px;font-weight:600;line-height:1.2;margin:0 0 6px}}
.kicker{{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin:0}}
.lede{{color:var(--mut);max-width:62ch;margin:.2em 0 1.1em}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}}
.stat{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.stat .n{{font-family:var(--serif);font-size:27px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.15}}
.stat .l{{font-size:11.5px;color:var(--faint);margin-top:3px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:22px 24px;margin:18px 0}}
.stand{{margin:0 0 12px}}
a{{color:var(--brand)}}
table{{width:100%;border-collapse:collapse;font-size:14.5px}}
th,td{{padding:9px 10px;text-align:left}}
thead th{{color:var(--faint);font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;border-bottom:1px solid var(--line)}}
tbody tr:nth-child(odd){{background:#f5f8fb}}td:nth-child(n+2),thead th:nth-child(n+2){{text-align:right;font-variant-numeric:tabular-nums}}
td a{{font-weight:600}}
input{{font-size:17px;padding:11px 13px;border:1px solid var(--line);border-radius:10px;width:100%;max-width:380px;box-shadow:var(--shadow)}}
ul{{padding-left:20px}}li{{margin:.25em 0}}
.mut{{color:var(--mut);font-size:13px}}
@media(max-width:620px){{h1{{font-size:30px}}.stats{{grid-template-columns:1fr 1fr}}.card{{padding:18px 15px}}table{{font-size:13.5px}}th,td{{padding:7px 6px}}thead th{{font-size:11px}}}}</style></head><body>
<header class="topbar"><div class="wrap"><a href="/">Flood Insurance Data</a></div></header><main class="wrap">"""
FOOT = ('<footer class="mut" style="margin:28px 0;border-top:1px solid var(--line);padding-top:14px">This product uses FEMA\'s OpenFEMA API but is not '
        'endorsed by FEMA. Place names via GeoNames (CC BY 4.0). Aggregates only, never individual quotes.'
        ' <a href="/about/">About</a> · <a href="/methodology/">Methodology</a> · <a href="/data/">Data</a>'
        ' · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a></footer></main></body></html>')

# ---- home: the reader's first questions answered, then find your state or county ----
import sys as _sys, datetime as _dtm
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules_registry import rule
from agg_raw import asof as _asof   # the data's as-of date, set by the pull (one place)
_ASOF_TXT = _dtm.date.fromisoformat(_asof()).strftime("%B %d, %Y").replace(" 0", " ")
_bp = os.path.join(DATADIR, "states", "built.json")
states = json.load(open(_bp)) if os.path.exists(_bp) else []
rows = "".join(f'<tr data-k="{html.escape((p["short"]+" "+(p.get("state") or "")).lower())}">'
               f'<td><a href="/flood-insurance/{p["slug"]}/">{html.escape(p["short"])}, {html.escape(p.get("state") or "")}</a></td>'
               f'<td>{money(p.get("median"))}</td><td>{format(p.get("units") or 0, ",")}</td></tr>' for p in indexable)
hrows = "".join(f'<tr data-k="{html.escape((p["short"]+" "+(p.get("state") or "")).lower())}">'
                f'<td><a href="/flood-insurance/{p["slug"]}/">{html.escape(p["short"])}, {html.escape(p.get("state") or "")}</a></td>'
                f'<td>{money(p.get("median"))}</td><td>{format(p.get("units") or 0, ",")}</td></tr>' for p in places)
srows = "".join(f'<tr data-k="{html.escape((s["name"] + " " + s["abbr"]).lower())}"><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td>'
                f'<td>{money(s["median"])}</td><td>{format(s["units"], ",")}</td></tr>' for s in sorted(states, key=lambda s: -s["median"]))
_bycost = sorted(states, key=lambda s: -s["median"])
extremes = (f'<p class="stand">Highest typical cost: {", ".join(html.escape(s["name"]) + " " + money(s["median"]) for s in _bycost[:3])}. '
            f'Lowest: {", ".join(html.escape(s["name"]) + " " + money(s["median"]) for s in _bycost[-3:])}. Sorted by typical cost.</p>') if len(states) > 6 else ""
national = ""
def _man(sl):   # records downloaded for a built state (its pull manifest)
    mm = json.load(open(os.path.join(DATADIR, "states", sl, "agg.json"))).get("manifest") or {}
    return (mm.get("policies") or {}).get("unique_fetched") or 0, (mm.get("claims") or {}).get("unique_fetched") or 0
_tp = sum(_man(s["slug"])[0] for s in states); _tc = sum(_man(s["slug"])[1] for s in states)
prov = (f'<p class="mut" style="font-size:14px">Built from {_tp:,} NFIP policy records and {_tc:,} claim records downloaded from FEMA: '
        f'every record the download listed for each state, none missing. <a href="/methodology/">How we check them</a></p>') if states else ""
if len(states) == 51:   # U.S. figures only once every state is built and gated: never a partial total called national
    _h = json.load(open(os.path.join(DATADIR, "us", "cost_hist.json")))
    _units = sum(s["units"] for s in states)
    def _hq(h, q):   # q-quantile of a {cost: count} histogram summed over every state
        vs = sorted((int(v), c) for st in h.values() for v, c in st.items()); n = sum(c for _, c in vs); acc = 0
        for v, c in vs:
            acc += c
            if acc >= n * q: return v
    _hn = json.load(open(os.path.join(DATADIR, "us", "cost_hist_new.json")))
    _new_med, _new_n = _hq(_hn, 0.5), sum(c for st in _hn.values() for c in st.values())
    _med = _hq(_h, 0.5); _q = {k: _hq(_h, k) for k in (0.25, 0.75, 0.9)}
    _ex = [json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"] for s in states]
    _wmean = lambda mk, nk: round(sum((e["averages"][mk] or 0) * e["averages"][nk] for e in _ex) / sum(e["averages"][nk] for e in _ex))
    _sf_mean, _all_mean = _wmean("sf_cost_mean", "sf_n"), _wmean("all_cost_mean", "all_n")
    _dc = {}
    for e in _ex:
        for d, c in (e.get("ded_counts") or {}).items(): _dc[d] = _dc.get(d, 0) + c
    _dtop = max(_dc, key=_dc.get); _dshare = round(100 * _dc[_dtop] / sum(_dc.values()), 1)
    national = (f'<div class="stats"><div class="stat"><div class="n">{money(_med)}</div><div class="l">U.S. median a year</div></div>'
                f'<div class="stat"><div class="n">{money(_med / 12)}</div><div class="l">Per month</div></div>'
                f'<div class="stat"><div class="n">{_units / 1e6:.1f}M</div><div class="l">Insured units in force</div></div></div>'
                f'<p class="mut">Median and per month: what existing single-family primary-home policies pay, premium plus fees. Insured units: every NFIP policy unit in force on {_ASOF_TXT}, including condos, rentals and businesses.</p>'
                f'<p class="cmp"><b>Buying?</b> Policies first bought in the past year typically pay {money(_new_med)} ({_new_n:,} policies). <a href="#prices">Why sites differ</a>.</p>')
    # hater r5 (home): price drivers, ways to pay less, a quote check and the averages other sites quote, all from the same records
    home_cards = (f'<div class="card" id="check"><h2>Is my quote normal?</h2><p class="stand">Type your yearly cost (premium plus fees) to see where it '
        f'sits among U.S. single-family policies; your state page compares it with your area.</p>'
        f'<input id="qv" inputmode="numeric" placeholder="e.g. {int(round(_med, -1))}" aria-label="Your yearly flood insurance cost"><p id="qo" class="mut"></p></div>'
        f'<div class="card"><h2>What sets the price, and how do I pay less?</h2><p class="stand">{rule("price_drivers")}</p>'
        f'<p class="stand">{rule("save_ways")} The usual building deductible on U.S. single-family policies is {money(int(float(_dtop)))} '
        f'({_dshare}% of them); your state page lists the mix there and any community discount.</p></div>'
        f'<div class="card" id="prices"><h2>Why do sites quote different prices?</h2><p class="stand">Because they measure different things: '
        f'each row below is the same FEMA records counted another way.</p>'
        f'<table><thead><tr><th>Measure</th><th>Amount</th></tr></thead><tbody>'
        f'<tr><td>Typical cost, existing single-family homes (median)</td><td>{money(_med)}</td></tr>'
        f'<tr><td>Typical cost, policies first bought in the past year</td><td>{money(_new_med)}</td></tr>'
        f'<tr><td>Average (mean) cost, single-family homes</td><td>{money(_sf_mean)}</td></tr>'
        f'<tr><td>Average cost, every policy type (adds condos, rentals, businesses)</td><td>{money(_all_mean)}</td></tr>'
        f'<tr><td>Average premium alone, single-family homes (before the federal fees)</td><td>{money(_wmean("sf_prem_mean", "sf_prem_n"))}</td></tr></tbody></table>'
        f'<p class="mut">Premium plus fees except the last row, NFIP policies in force on {_ASOF_TXT}. A figure quoted without fees, or '
        'for a different mix of policies, lands lower or higher than ours. Private flood insurance is not in this data.</p></div>'
        f'<script>var qv=document.getElementById("qv"),qo=document.getElementById("qo");qv.addEventListener("input",function(){{'
        f'var v=+qv.value.replace(/[^0-9.]/g,"");if(!v){{qo.textContent="";return;}}'
        f'qo.textContent="$"+v.toLocaleString()+" is "+(v<={_q[0.25]}?"in the lowest quarter":v<{_med}?"below the middle":v=={_med}?"right at the middle":v<{_q[0.75]}?"above the middle":v<{_q[0.9]}?"in the top quarter":"in the top tenth")'
        f'+" of U.S. single-family policies (half pay {money(_q[0.25])} to {money(_q[0.75])}).";}});</script>')
else: home_cards = ""
home = HEAD.format(title="Flood insurance cost by state and county (FEMA data)",
    desc="What flood insurance actually costs where you live, from FEMA's own policy and claim records: typical cost, whether you're required to buy it, how fast it starts, and what floods have paid out.",
    canon=BASE + "/") + f"""
<section class="hero"><p class="kicker">NFIP records · {"50 states and DC" if len(states) == 51 else str(len(states)) + " states"} · {len(places)} counties</p>
<h1>What flood insurance costs in your state</h1>
<p class="lede">From FEMA's own records of existing policies and claims, not quotes: what policyholders pay, whether you're required to buy it, and how fast it starts.</p>
{national}
{prov}
<input id="s" placeholder="Type your state or county…" aria-label="Find your state or county" autocomplete="off"></section>
<div class="card"><h2>Three things to know first</h2>
<p class="stand"><b>How fast does it start?</b> {rule("howto_answer")}</p>
<p class="stand"><b>Am I required to buy it?</b> {rule("purchase_answer")} {rule("lender_any_zone")} {rule("fl_citizens_short")} Check your zone on <a href="https://msc.fema.gov/portal/home" rel="noopener" target="_blank">FEMA's flood map</a>.</p>
<p class="stand"><b>Does my homeowners policy cover floods?</b> {rule("homeowners_excl")}</p></div>
{home_cards}
<div class="card"><h2>Flood insurance by state</h2>{extremes}
<table id="st"><thead><tr><th>State</th><th>Median / yr</th><th>Insured units</th></tr></thead>
<tbody>{srows or '<tr><td colspan=3 class=mut>State pages are being built.</td></tr>'}</tbody></table></div>
<div class="card"><h2>County pages</h2><p class="stand">{len(places)} counties so far, listed by number of policies; more are added as each passes review. Every county's figures also sit in its state page's county table.</p>
<table id="t"><thead><tr><th>County</th><th>Median / yr</th><th>Insured units</th></tr></thead>
<tbody>{rows or '<tr><td colspan=3 class=mut>No counties published yet.</td></tr>'}</tbody></table></div>
<script>
var s=document.getElementById('s');
s.addEventListener('input',function(){{var q=s.value.toLowerCase();
 ['st','t'].forEach(function(id){{[].forEach.call(document.getElementById(id).tBodies[0].rows,function(r){{
   r.style.display=(!q||(r.dataset.k||'').indexOf(q)>-1)?'':'none';}});}});}});
</script>{FOOT}"""
wr(os.path.join(DIST, "index.html"), home)

# ---- /flood-insurance/ hub (the Breadcrumb target + county directory; previously a hard 404) ----
hub = HEAD.format(title="Flood insurance by state and county (FEMA data)",
    desc="Every published state and county: what NFIP policyholders pay, whether coverage is required, claims history and flood risk. Public federal data.",
    canon=BASE + "/flood-insurance/") + f"""
<section class="hero"><p class="kicker">{len(states)} state{"" if len(states) == 1 else "s"} · {len(places)} counties</p><h1>Flood insurance by state and county</h1>
<p class="lede">Find your state or county for what people there pay, whether you're required to buy it, and what floods have paid out.</p>
<input id="s" placeholder="Type your state or county…" aria-label="Find your state or county" autocomplete="off"></section>
<div class="card"><h2>States</h2>
<table id="st"><thead><tr><th>State</th><th>Median / yr</th><th>Insured units</th></tr></thead>
<tbody>{srows or '<tr><td colspan=3 class=mut>State pages are being built.</td></tr>'}</tbody></table></div>
<div class="card"><h2>Counties</h2>
<table id="t"><thead><tr><th>County</th><th>Median / yr</th><th>Insured units</th></tr></thead>
<tbody>{hrows or '<tr><td colspan=3 class=mut>No counties published yet.</td></tr>'}</tbody></table></div>
<script>
var s=document.getElementById('s');
s.addEventListener('input',function(){{var q=s.value.toLowerCase();
 ['st','t'].forEach(function(id){{[].forEach.call(document.getElementById(id).tBodies[0].rows,function(r){{
   r.style.display=(!q||(r.dataset.k||'').indexOf(q)>-1)?'':'none';}});}});}});
</script>{FOOT}"""
wr(os.path.join(DIST, "flood-insurance", "index.html"), hub)

# ---- methodology ----
from notes import NOTES   # each page card links here ("How this is counted") instead of repeating the note
_notes_html = "".join(f'<h3 id="{k}">{html.escape(h)}</h3><p>{html.escape(t)}</p>' for k, (h, t) in NOTES.items())
meth = HEAD.format(title="Methodology — flood insurance data", desc="Definitions, sources, dates, cohort rules and reconciliation for the flood-insurance data.", canon=BASE + "/methodology/") + f"""
<h1>Methodology</h1>
<div class="card"><h2>What we downloaded</h2><p>We do not use FEMA's summary tables. For every state page we download every NFIP policy record in force and every NFIP claim record FEMA publishes for that state, check the count against the API's own record total (a page is blocked if any record is missing), and compute every figure ourselves. So far: {_tp:,} policy records and {_tc:,} claim records. Each page states its own counts and offers its figures as a CSV.</p></div>
<div class="card"><h2>Sources</h2><ul>
<li>NFIP Redacted <b>Policies v3</b> and <b>Claims v3</b> — OpenFEMA API (keyless). Cost, full-risk premium, zones, claims.</li>
<li><b>Community Status Book v1</b> — OpenFEMA. CRS class and premium discount by community.</li>
<li><b>Disaster Declarations Summaries v2</b> — OpenFEMA. Federal flood/storm declarations.</li>
<li><b>Housing Assistance (Owners) v2</b> — OpenFEMA. FEMA aid paid to owners after disasters.</li>
<li><b>National Risk Index (counties)</b> — FEMA ArcGIS (FEMA_NationalRiskIndex). Flood expected annual loss + percentile.</li>
<li><b>U.S. Census ACS 5-year (B25001)</b> — U.S. Census Bureau API. Housing units, used only where FEMA's own penetration rate is missing.</li>
<li><b>Multiple-Loss Flood Properties</b> — OpenFEMA (Individual Assistance). One record per property per declared disaster that damaged it, for properties that flooded more than once; a property on FEMA's severe repetitive loss list is flagged.</li>
<li><b>NFIP Residential Penetration Rates</b> — OpenFEMA. Share of residential structures with an NFIP policy, overall and inside the high-risk zone, per county.</li>
<li><b>NOAA NCEI Storm Events</b> — NOAA. Recorded flood/flash-flood/coastal-flood events + NWS property-damage estimates, per county (1996 on).</li>
<li>Official <b>Policy Information by State and Community</b> workbook — reconciliation benchmark (a cross-check, not a dataset).</li></ul>
<p class="mut">Ten federal datasets in all; the full-risk premium is a field within Policies and the PIF workbook is a reconciliation benchmark, not separate fetches.</p></div>
<div class="card"><h2>Definitions &amp; rules</h2><ul>
<li><b>Policy units</b> = sum of <code>policyCount</code>, never a row count — condo-association records carry more than one unit.</li>
<li><b>Cost cohort</b>: single-family primary-residence policies (occupancy 1/11, primary residence), annual cost = premium + fees.</li>
<li><b>Percentiles</b> p25/p50/p75/p90 by inclusive interpolation.</li>
<li><b>Full-risk gap</b>: share of cohort whose premium charged (<code>totalInsurancePremiumOfThePolicy</code>) is below FEMA's full-risk premium (<code>fullRiskPremium</code>); both are premium-only. The cost figures elsewhere use <code>policyCost</code>, which FEMA defines as premium plus the reserve fund assessment, federal policy fee and HFIAA surcharge, so they are not compared with full-risk.</li>
<li><b>Claims per 100</b>: cumulative paid claims since 1978 over current policy units — a historical tally, not an annual rate or a flood probability.</li>
<li><b>Minimum sizes</b>: a cost spread needs 100 or more priced single-family policies; a flood-zone median 50; a county median 30; a ZIP median 25. Smaller medians move more from year to year, and the count is shown beside each.</li>
<li><b>Dates</b>: each figure shows its effective date and retrieval date; policy snapshot differs from other datasets' retrieval dates.</li></ul></div>
<div class="card" id="limits"><h2>What the data cannot tell you</h2><ul>
<li>Your own premium: it depends on your building's elevation, foundation, coverage and deductible. The pages show where existing policies fall, and what policies first bought in the past year typically cost.</li>
<li>Private (non-NFIP) flood insurance prices.</li>
<li>Your address's exact flood zone: use FEMA's Flood Map Service Center.</li>
<li>Why any one premium changes: the pages show the gap to FEMA's full-risk price, not the cause.</li>
<li>A long premium trend: the in-force records hold only current-term policies, so only the last two policy years can be compared.</li></ul></div>
<div class="card"><h2>How each figure is counted</h2>{_notes_html}</div>
{FOOT}"""
wr(os.path.join(DIST, "methodology", "index.html"), meth)

# ---- about (E-E-A-T: who runs it, purpose, corrections, non-commercial, not FEMA) ----
CONTACT = os.environ.get("FF_CONTACT", "")   # owner-supplied; omitted until provided (never fabricate one)
contact_html = (f'<li><b>Corrections &amp; contact:</b> <a href="mailto:{html.escape(CONTACT)}">{html.escape(CONTACT)}</a> — '
                'tell us about any figure that looks wrong and we will check it against the source record.</li>'
                if CONTACT else
                '<li><b>Checking a figure:</b> every figure links to its official federal source, and each page offers its '
                'figures as a CSV, so any number can be checked against the record it came from.</li>')
about = HEAD.format(title="About — Flood Insurance Data", desc="Who runs Flood Insurance Data, how the figures are compiled and checked, and our independence from FEMA and insurers.", canon=BASE + "/about/") + f"""
<h1>About Flood Insurance Data</h1>
<div class="card"><h2>What this is</h2>
<p>Flood Insurance Data is an independent, non-commercial project that makes the U.S. government's own
flood-insurance records readable one place at a time. For each county we publish what existing NFIP
policyholders actually pay, how that compares with FEMA's full-risk price, the claims history, the flood
risk, and the community discounts that lower the bill — every figure drawn from a public federal dataset,
with its exact source and the date it was pulled.</p></div>
<div class="card"><h2>How the numbers are made and checked</h2><ul>
<li>Compiled directly from FEMA's OpenFEMA records, NOAA and the U.S. Census Bureau; no private data. Two figures are FEMA models and are labeled as such: the National Risk Index and FEMA's estimate of how many homes are insured.</li>
<li>Every page is built by code and must pass an automated correctness gate before it ships: percentiles and
sums are recomputed, record counts are checked against the download's own totals (FEMA's separate official policy count is not yet compared), every ratio's denominator is
disclosed, and nothing publishes if a check fails. The <a href="/methodology/">methodology</a> defines every term.</li>
<li>We show aggregates only — never an individual property, policy, or quote.</li>
{contact_html}
</ul></div>
<div class="card"><h2>Independence</h2>
<p>This site is <b>not affiliated with or endorsed by FEMA</b> or any government agency, and has <b>no
relationship with any insurer, agent, or lead-generation service</b>. It does not sell insurance, generate
quotes, or earn commissions on policies. It is a reference, not a sales page. Any advertising, if added
later, will be disclosed here.</p></div>
{FOOT}"""
wr(os.path.join(DIST, "about", "index.html"), about)

# ---- privacy policy (required for AdSense; written to current state + ad-ready, no false claims) ----
privacy = HEAD.format(title="Privacy Policy — Flood Insurance Data", desc="How Flood Insurance Data handles data, cookies, logs, and advertising.", canon=BASE + "/privacy/") + f"""
<h1>Privacy Policy</h1>
<p class="mut">Last updated {RETR}.</p>
<div class="card"><h2>What we collect</h2>
<p>Flood Insurance Data is a static reference site. We do not ask for, collect, or store personal
information, and there are no accounts, sign-ups, or forms. Our host (Cloudflare) processes standard
server request logs (such as IP address and user agent) to serve the site and protect it from abuse; see
Cloudflare's privacy policy for details.</p></div>
<div class="card"><h2>Cookies</h2>
<p>This site sets no first-party tracking cookies of its own. If analytics or advertising are added in
future (see below), the cookies and third-party vendors involved will be disclosed here before they are
enabled.</p></div>
<div class="card"><h2>Advertising</h2>
<p>The site currently shows no ads. If advertising is added, it may be served by Google, including Google
AdSense. Third-party vendors such as Google use cookies to serve ads based on a user's prior visits to this
and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on
visits here and elsewhere. You may opt out of personalized advertising via
<a href="https://www.google.com/settings/ads" rel="nofollow">Google Ads Settings</a>, and review other
options at <a href="https://www.aboutads.info" rel="nofollow">aboutads.info</a>. This section will be
updated to name every ad vendor at the time ads are enabled.</p></div>
<div class="card"><h2>Third-party data &amp; links</h2>
<p>All figures are compiled from public U.S. federal sources (FEMA OpenFEMA, the FEMA National Risk Index,
and the U.S. Census Bureau). We link to official FEMA and Census pages; their privacy practices are their
own. We are not affiliated with or endorsed by FEMA.</p></div>
<div class="card"><h2>Children &amp; changes</h2>
<p>The site is not directed to children under 13 and collects no information from them. We may update this
policy; material changes will be reflected by the date above.</p></div>
{FOOT}"""
wr(os.path.join(DIST, "privacy", "index.html"), privacy)

# ---- terms ----
terms = HEAD.format(title="Terms of Use — Flood Insurance Data", desc="Terms for using Flood Insurance Data and reusing its figures.", canon=BASE + "/terms/") + f"""
<h1>Terms of Use</h1>
<p class="mut">Last updated {RETR}.</p>
<div class="card"><h2>What this is — and isn't</h2>
<p>Flood Insurance Data presents aggregate statistics compiled from public federal data for general
information only. It is <b>not insurance advice, not a quote, and not a substitute for FEMA's official
flood maps or a licensed agent.</b> Figures are place-level aggregates and never describe an individual
property or policy. We are not affiliated with or endorsed by FEMA or any insurer.</p></div>
<div class="card"><h2>Accuracy &amp; no warranty</h2>
<p>We work to reflect the source data faithfully and show each figure's source and date, but the data is
provided "as is" without warranty of any kind. Verify anything you rely on against the official source we
link, and confirm your own situation with FEMA's Flood Map Service Center and a licensed insurance
professional.</p></div>
<div class="card"><h2>Reusing the data</h2>
<p>The underlying figures come from public-domain U.S. government datasets and may be reused. If you cite
this site, please credit "Flood Insurance Data" and note: "This product uses FEMA's OpenFEMA API but is not
endorsed by FEMA."</p></div>
{FOOT}"""
wr(os.path.join(DIST, "terms", "index.html"), terms)

# ---- data download (CSV from per-county agg) ----
csv_path = os.path.join(DIST, "data", "counties.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["slug", "county", "geoid", "policy_units", "median_cost", "p25", "p75", "p90",
                "full_risk_median", "share_below_full_risk_pct", "claims_since_1978", "claims_paid_usd",
                "nfip_takeup_pct", "nfip_takeup_sfha_pct", "avg_paid_claim_usd", "closed_no_payment_pct",
                "paid_outside_sfha_pct", "noaa_flood_events_1996_2025", "noaa_flood_damage_usd"])
    for p in places:
        ap = os.path.join(cdir(p["slug"]), "agg.json")
        if not os.path.exists(ap): continue
        a = json.load(open(ap)); P = a["policies"]; C = a["claims"]
        dp = os.path.join(cdir(p["slug"]), "data.json")
        d = json.load(open(dp)) if os.path.exists(dp) else {}
        pen, cx, se = d.get("penetration") or {}, d.get("claims_extra") or {}, d.get("storm_events") or {}
        w.writerow([p["slug"], p["short"], p.get("geoid"), P["units"], P["p50"], P["p25"], P["p75"], P["p90"],
                    P["frp_median"], P["share_below"], C["rows"], C["total_paid"],
                    pen.get("overall_pct"), pen.get("sfha_pct"), cx.get("avg_paid"), cx.get("cwop_share"),
                    cx.get("outside_sfha_pct"), se.get("events"), se.get("damage")])
data = HEAD.format(title="Download the flood-insurance data", desc="Per-county NFIP flood-insurance aggregates as CSV.", canon=BASE + "/data/") + f"""
<h1>Download the data</h1>
<p>Per-county aggregates computed from FEMA OpenFEMA and NOAA NCEI: policy units, cost spread, full-risk gap, claims, average paid claim, share closed without payment, share of paid dollars outside the high-risk zone, NFIP take-up, and NOAA flood events (1996–2025). Blank = not available for that county.</p>
<p><a href="/data/counties.csv">counties.csv</a> — {len(places)} places.</p>
<p class="mut">Reuse freely with attribution: "This product uses FEMA's OpenFEMA API, but is not endorsed by FEMA."</p>{FOOT}"""
wr(os.path.join(DIST, "data", "index.html"), data)

# ---- sitemap, robots, llms.txt ----
# lastmod = the data's effective date (real data change), per-county from its agg; site pages use the max.
def county_lastmod(slug):
    ap = os.path.join(cdir(slug) if "/" not in slug and "\\" not in slug else os.path.join(DATADIR, slug), "agg.json")
    if os.path.exists(ap):
        a = json.load(open(ap))
        return (a.get("policies") or {}).get("asof") or _asof()
    return _asof()
county_urls = [(BASE + f"/flood-insurance/{p['slug']}/", county_lastmod(p["slug"])) for p in indexable]
# county pages carry lastmod = their data's effective date (a real data change); home/methodology/data
# have no trustworthy per-content modification date, so they omit lastmod rather than inherit a false one.
urls = [(BASE + "/", None), (BASE + "/flood-insurance/", None), (BASE + "/about/", None),
        (BASE + "/methodology/", None), (BASE + "/data/", None),
        (BASE + "/privacy/", None), (BASE + "/terms/", None)] + county_urls + \
       [(BASE + f"/flood-insurance/{s['slug']}/", county_lastmod(os.path.join("states", s["slug"]))) for s in states]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "".join(f"  <url><loc>{u}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>\n" for u, lm in urls) + \
     "</urlset>\n"
wr(os.path.join(DIST, "sitemap.xml"), sm)
wr(os.path.join(DIST, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
wr(os.path.join(DIST, "llms.txt"),
   "# Flood insurance data\n\n> Per-county NFIP flood-insurance statistics from public FEMA data: what "
   "policyholders pay, the gap to FEMA's full-risk price, claims history, flood risk, and CRS discounts.\n\n"
   "## States\n" + "".join(f"- [{s['name']}]({BASE}/flood-insurance/{s['slug']}/): median {money(s['median'])}\n" for s in states) +
   "\n## Counties\n" + "".join(f"- [{p['short']}]({BASE}/flood-insurance/{p['slug']}/): median {money(p.get('median'))}\n" for p in indexable) +
   f"- [Methodology]({BASE}/methodology/)\n- [Data CSV]({BASE}/data/counties.csv)\n\n"
   "Source: FEMA OpenFEMA. Not endorsed by FEMA. Aggregates only.\n")

print(f"built site: {len(places)} places, home+methodology+data+sitemap+robots+llms into {DIST}")
