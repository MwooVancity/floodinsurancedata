"""Build the shared site pages from places.json: home+lookup, methodology, data (CSV),
sitemap.xml, robots.txt, llms.txt. Reads per-county agg.json for the download table.
Env: FF_PLACES (places.json), FF_DIST (dist dir), FF_DATADIR (per-county data root), FF_BASEURL."""
import collections, csv, json, os, html, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import THEME

PLACES = os.environ.get("FF_PLACES", "places.json")
DIST = os.environ.get("FF_DIST", "dist")
DATADIR = os.environ.get("FF_DATADIR", "data")
BASE = os.environ.get("FF_BASEURL", "https://floodinsurancedata.com").rstrip("/")   # never example.com: a standalone run would ship wrong canonicals
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
<style>.btn{{display:inline-block;color:#fff;text-decoration:none;padding:12px 20px;min-height:44px}}:root{{--bg:#f4f7f8;--surface:#fff;--ink:#132029;--mut:#55656f;--faint:#7d8c96;--line:#dbe3e7;--brand:#15617f;--brand-d:#0e4a61;--accent:#c2591f;--r:12px;--gut:20px;
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
@media(max-width:620px){{h1{{font-size:30px}}.stats{{grid-template-columns:1fr 1fr}}.card{{padding:18px 15px}}table{{font-size:13.5px}}th,td{{padding:7px 6px}}thead th{{font-size:11px}}}}</style><style>"""+THEME.replace("{","{{").replace("}","}}")+"""</style></head><body>
<header class="topbar"><div class="wrap"><a href="/">Flood Insurance Data</a></div></header><main class="wrap">"""
FOOT = ('<footer class="mut" style="margin:28px 0;border-top:1px solid var(--line);padding-top:14px">This product uses FEMA\'s OpenFEMA API but is not '
        'endorsed by FEMA. Place names via GeoNames (CC BY 4.0). Aggregates only, never individual quotes.'
        ' <a href="/about/">About</a> · <a href="/methodology/">Methodology</a> · <a href="/data/">Data</a>'
        ' · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a></footer></main></body></html>')

# ---- home: the reader's first questions answered, then find your state or county ----
import sys as _sys, datetime as _dtm
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rules_registry import rule, RULES
from notes import GA_TAG
_zm_zip = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_flags.json"), encoding="utf-8")).get("zip") or []
_zm_on_home = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_flags.json"), encoding="utf-8")).get("zonemap") or []
HEAD = HEAD.replace("<title>", GA_TAG.replace("{", "{{").replace("}", "}}") + "<title>", 1)   # HEAD goes through .format
def _rule_hosts(keys):   # the official sites behind these rules, from rules_registry sources
    from urllib.parse import urlparse
    return ", ".join(sorted({urlparse(u).netloc.replace('www.', '') for k in keys for u, *_ in RULES[k]['sources']}))
from ffcalc import ZONE_MIN
from agg_raw import asof as _asof   # the data's as-of date, set by the pull (one place)
_ASOF_TXT = _dtm.date.fromisoformat(_asof()).strftime("%B %d, %Y").replace(" 0", " ")
_bp = os.path.join(DATADIR, "states", "built.json")
states = json.load(open(_bp)) if os.path.exists(_bp) else []
# test_site_factory 11-08: built.json and the state folders are two copies; a half-finished refresh left a listed state with
# no agg.json and crashed the whole site. Trust only states whose data exists; national pages then hold (they need all 51).
states = [s for s in states if os.path.exists(os.path.join(DATADIR, "states", s["slug"], "agg.json"))]
rows = "".join(f'<tr data-k="{html.escape((p["short"]+" "+(p.get("state") or "")).lower())}">'
               f'<td><a href="/flood-insurance/{p["slug"]}/">{html.escape(p["short"])}, {html.escape(p.get("state") or "")}</a></td>'
               f'<td>{money(p.get("median"))}</td><td>{format(p.get("units") or 0, ",")}</td></tr>' for p in indexable)
hrows = "".join(f'<tr data-k="{html.escape((p["short"]+" "+(p.get("state") or "")).lower())}">'
                f'<td><a href="/flood-insurance/{p["slug"]}/">{html.escape(p["short"])}, {html.escape(p.get("state") or "")}</a></td>'
                f'<td>{money(p.get("median"))}</td><td>{format(p.get("units") or 0, ",")}</td></tr>' for p in places)
srows = "".join(f'<tr data-k="{html.escape((s["name"] + " " + s["abbr"]).lower())}"><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td>'
                f'<td>{money(s["median"])}</td><td>{format(s["units"], ",")}</td><td>{format(s["claims"], ",")}</td><td>{money(s["paid"])}</td></tr>' for s in sorted(states, key=lambda s: -s["median"]))
_cy = [json.load(open(os.path.join(DATADIR, "states", s["slug"], "agg.json")))["claims"] for s in states]
_cnote = (f'<p class="mut">NFIP claims on record: every claim record, paid or not, except records FEMA coded "deleted in error" or "assigned in error", for losses from {min(c["year_min"] for c in _cy)} to {max(c["year_max"] for c in _cy)}. '
          'Paid on them: building plus contents payments, in dollars as paid, not adjusted for inflation. <a href="/flood-insurance/claims/">How often claims get paid, county by county</a>.</p>') if states else ""
_bycost = sorted(states, key=lambda s: -s["median"])
extremes = (f'<p class="stand">Highest typical cost: {", ".join(html.escape(s["name"]) + " " + money(s["median"]) for s in _bycost[:3])}. '
            f'Lowest: {", ".join(html.escape(s["name"]) + " " + money(s["median"]) for s in _bycost[-3:])}. Sorted by typical cost.</p>') if len(states) > 6 else ""
national = ""
def _man(sl):   # records downloaded for a built state (its pull manifest)
    mm = json.load(open(os.path.join(DATADIR, "states", sl, "agg.json"))).get("manifest") or {}
    return (mm.get("policies") or {}).get("unique_fetched") or 0, (mm.get("claims") or {}).get("unique_fetched") or 0
_tp = sum(_man(s["slug"])[0] for s in states); _tc = sum(_man(s["slug"])[1] for s in states)
prov = (f'<p class="mut" style="font-size:14px">Built from {_tp:,} NFIP policy records and {_tc:,} claim records downloaded from FEMA (one record can cover several insured units, such as a condo building): '
        f'every record the download listed for each state, none missing. <a href="/methodology/">How we check them</a></p>') if states else ""
RENT_ON = False
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
    # renters (PAGE QUEUE row 6): tenant, residential occupancy, contents-only (extras_raw RENTER_OCC); a page only when all
    # 51 states carry the homes-only count and the U.S. median rests on 100+ priced policies (owner floor, PLAN Batch C)
    _rp = os.path.join(DATADIR, "us", "renter_hist.json")
    _rh = json.load(open(_rp)) if os.path.exists(_rp) else {}
    _rn = sum(c for st in _rh.values() for c in st.values())
    RENT_ON = len(_rh) == 51 and _rn >= 100
    _ex = [json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"] for s in states]
    _wmean = lambda mk, nk: round(sum((e["averages"][mk] or 0) * e["averages"][nk] for e in _ex) / sum(e["averages"][nk] for e in _ex))
    _sf_mean, _all_mean = _wmean("sf_cost_mean", "sf_n"), _wmean("all_cost_mean", "all_n")
    _dc = {}
    for e in _ex:
        for d, c in (e.get("ded_counts") or {}).items(): _dc[d] = _dc.get(d, 0) + c
    _dtop = max(_dc, key=_dc.get); _dshare = round(100 * _dc[_dtop] / sum(_dc.values()), 1)
    # backlog 1: U.S. cost by flood zone, summed from every state's zone histograms (extras_raw); shown once all 51 have one
    _zp = os.path.join(DATADIR, "us", "cost_hist_zone.json")
    _zh = json.load(open(_zp)) if os.path.exists(_zp) else {}
    _zone_card = ""; _zleft = "Zone D and policies with no zone are left out"   # the grouped table (no exact-zone file yet)
    _zxp = os.path.join(DATADIR, "us", "cost_hist_zone_exact.json")   # hcu 11-07: every zone a letter names, linked, not 3 groups
    _zxh = json.load(open(_zxp)) if os.path.exists(_zxp) else {}
    if len(_zh) == 51 and len(_zxh) == 51:
        _zrows = ""; _zshown_h = set()
        for _zc in ("AE", "X", "VE", "A", "AO", "AH"):
            _hz = {s: h.get(_zc) or {} for s, h in _zxh.items()}; _nn = sum(sum(v.values()) for v in _hz.values())
            if _nn >= ZONE_MIN: _zrows += f'<tr><td><a href="/flood-zones/{_zc.lower()}/">Zone {_zc}</a></td><td>{money(_hq(_hz, 0.5))}</td><td>{_nn:,}</td></tr>'; _zshown_h.add(_zc)
        # hater r107: the note said only zone D was left out; A99, C, B and the old numbered zones were too. Name them from the data.
        _zoth = collections.Counter()
        for _h in _zxh.values():
            for _z, _v in _h.items():
                if _z not in _zshown_h and _z not in ("", "Unknown"): _zoth[_z] += sum(_v.values())
        _zleft = (f'{sum(_zoth.values()):,} policies rated in other zone codes are left out ('
                  + ", ".join(f"{z} {n:,}" for z, n in _zoth.most_common(3))
                  + f" and {len(_zoth) - 3} smaller codes, including zone D and the old numbered A and V zones), as are policies with no zone") if len(_zoth) > 3 else \
                 (f'Left out: {", ".join(f"zone {z} ({n:,})" for z, n in _zoth.most_common())} and policies with no zone' if _zoth else "Policies with no zone are left out")
    elif len(_zh) == 51:
        _zrows = "".join(f'<tr><td>{lab}</td><td>{money(_hq({s: h.get(g) or {} for s, h in _zh.items()}, 0.5))}</td>'
                         f'<td>{sum(sum(h.get(g, {}).values()) for h in _zh.values()):,}</td></tr>'
                         for g, lab in (("V", "Coastal high-risk (V zones)"), ("A", "High-risk (A zones)"), ("X", "Moderate or low risk (B, C, X zones)"))
                         if any(h.get(g) for h in _zh.values()))
    if len(_zh) == 51:
        _zone_card = (f'<div class="card" id="zones"><h2>What does it cost by flood zone?</h2><p class="stand">Typical yearly cost '
                      f'(premium plus fees) of existing single-family primary-home policies, by the zone each policy is rated in.</p>'
                      f'<table><thead><tr><th>Flood zone</th><th>Median / yr</th><th>Policies</th></tr></thead><tbody>{_zrows}</tbody></table>'
                      f'<p class="mut">NFIP policies in force on {_ASOF_TXT}. {_zleft}. Your state page '
                      'breaks this down by every zone code. What each means: ' + ", ".join(f'<a href="/flood-zones/{z}/">zone {z.upper()}</a>' for z in ("ae", "x", "a", "ao", "ah", "ve", "d")) + '.</p></div>')
    national = (f'<div class="stats"><div class="stat"><div class="n">{money(_med)}</div><div class="l">U.S. median a year</div></div>'
                f'<div class="stat"><div class="n">{money(_med / 12)}</div><div class="l">Per month</div></div>'
                f'<div class="stat"><div class="n">{_units / 1e6:.1f}M</div><div class="l">Policy units in force</div></div></div>'
                f'<p class="mut">Median and per month: what existing single-family primary-home policies pay, premium plus fees. Insured units: every NFIP policy unit in force on {_ASOF_TXT}, including condos, rentals and businesses.</p>'
                f'<h2>How much is flood insurance?</h2><p class="stand">Existing NFIP policies on single-family primary homes cost a median of {money(_med)} a year, '
                f'premium plus fees; half pay between {money(_q[0.25])} and {money(_q[0.75])}, and one in ten pays {money(_q[0.9])} or more.</p>'
                f'<p class="cmp"><b>Buying?</b> Policies first bought in the past year typically pay {money(_new_med)} ({_new_n:,} policies). <a href="#prices">Why sites differ</a>. <a href="/nfip/">The NFIP in numbers</a>.' + (' <a href="/flood-insurance/renters/">What renters pay</a>.' if RENT_ON else '') + '</p>')
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
        + _zone_card +
        f'<script>var qv=document.getElementById("qv"),qo=document.getElementById("qo");qv.addEventListener("input",function(){{'
        f'var v=+qv.value.replace(/[^0-9.]/g,"");if(!v){{qo.textContent="";return;}}'
        f'qo.textContent="$"+v.toLocaleString()+" is "+(v<={_q[0.25]}?"in the lowest quarter":v<{_med}?"below the middle":v=={_med}?"right at the middle":v<{_q[0.75]}?"above the middle":v<{_q[0.9]}?"in the top quarter":"in the top tenth")'
        f'+" of U.S. single-family policies (half pay {money(_q[0.25])} to {money(_q[0.75])}). These are existing policies, many still below FEMA’s full-risk price; policies first bought in the past year typically pay {money(_new_med)}.";}});</script>')
else: home_cards = ""
home = HEAD.format(title="Flood insurance cost by state and county (FEMA data)",
    desc="What flood insurance actually costs where you live, from FEMA's own policy and claim records: typical cost, whether you're required to buy it, how fast it starts, and what floods have paid out.",
    canon=BASE + "/") + f"""
<section class="hero"><p class="kicker">NFIP records · {"50 states and DC" if len(states) == 51 else str(len(states)) + " states"} (not Puerto Rico or other U.S. territories) · {len(places)} counties</p>
<h1>What flood insurance costs in your state</h1>
<p class="lede">From FEMA's own records of existing policies and claims, not quotes: what policyholders pay, whether you're required to buy it, and how fast it starts.</p>
{national}
{prov}
<input id="s" placeholder="Type your state or county…" aria-label="Find your state or county" autocomplete="off"><p id="nomatch" class="mut" aria-live="polite"></p>{'<p>Or <a href="/flood-insurance/zip/">look up a ZIP code</a>.</p>' if (_zm_zip == "all" or "zip" in _zm_zip) else ""}</section>
<div class="card"><h2>What to know first</h2>
<p class="stand"><b>How fast does it start?</b> {rule("howto_answer")}</p>
<p class="stand"><b>Am I required to buy it?</b> {rule("purchase_answer")} {rule("lender_any_zone")} {rule("fl_citizens_short")} Check your zone on <a href="https://msc.fema.gov/portal/home" rel="noopener" target="_blank">FEMA's flood map</a>{' or with the <a href="/flood-zone-map/">flood zone lookup</a>' if (_zm_on_home == "all" or "flood-zone-map" in _zm_on_home) else ""}.</p>
<p class="stand"><b>Does my homeowners policy cover floods?</b> {rule("homeowners_excl")}</p>
<p class="stand"><b>Where do I buy it?</b> {rule("how_to_buy")} {rule("private_accept")}</p>
<p class="stand"><b>How much can it pay?</b> {rule("limits")}</p>
<p class="mut">Rules from {_rule_hosts(["howto_answer", "purchase_answer", "lender_any_zone", "fl_citizens_short", "homeowners_excl", "how_to_buy", "private_accept", "limits"])}. <a href="/methodology/">How we check them</a>.</p></div>
{home_cards}
<div class="card"><h2>Flood insurance policies and claims by state</h2>{extremes}
<table id="st"><thead><tr><th>State</th><th>Median / yr</th><th>Insured units</th><th>NFIP claims on record</th><th>Paid on them</th></tr></thead>
<tbody>{srows or '<tr><td colspan=5 class=mut>State pages are being built.</td></tr>'}</tbody></table>{_cnote}</div>
<div class="card"><h2>County pages</h2><p class="stand">{len(places)} counties so far, listed by insured units; more are added as each passes review. Every county's figures also sit in its state page's county table.</p>
<table id="t"><thead><tr><th>County</th><th>Median / yr</th><th>Insured units</th></tr></thead>
<tbody>{rows or '<tr><td colspan=3 class=mut>No counties published yet.</td></tr>'}</tbody></table></div>
<script>
var s=document.getElementById('s');
s.addEventListener('input',function(){{var q=s.value.toLowerCase();
 ['st','t'].forEach(function(id){{[].forEach.call(document.getElementById(id).tBodies[0].rows,function(r){{
   r.style.display=(!q||(r.dataset.k||'').indexOf(q)>-1)?'':'none';}});}});
 var n=[].filter.call(document.querySelectorAll('#st tbody tr,#t tbody tr'),function(r){{return r.style.display!=='none';}}).length;
 document.getElementById('nomatch').textContent=(q&&!n)?"No page matches yet. Every county's typical cost is in its state page's county table: find your state below.":'';}});
</script>{FOOT}"""
_org = json.dumps({"@context": "https://schema.org", "@graph": [   # audit 11-04: the site as an entity; nothing invented (no person, address, sameAs)
    {"@type": "Organization", "@id": BASE + "/#org", "name": "Flood Insurance Data", "url": BASE + "/"},
    {"@type": "WebSite", "@id": BASE + "/#site", "name": "Flood Insurance Data", "url": BASE + "/", "publisher": {"@id": BASE + "/#org"}}]})
home = home.replace("</body>", f'<script type="application/ld+json">{_org}</script></body>', 1) if "</body>" in home else home + f'<script type="application/ld+json">{_org}</script>'
wr(os.path.join(DIST, "index.html"), home)

# ---- /flood-insurance/ hub (the Breadcrumb target + county directory; previously a hard 404) ----
hub = HEAD.format(title="Flood insurance by state and county (FEMA data)",
    desc="Every published state and county: what NFIP policyholders pay, whether coverage is required, claims history and flood risk. Public federal data.",
    canon=BASE + "/flood-insurance/") + f"""
<section class="hero"><p class="kicker">{len(states)} state{"" if len(states) == 1 else "s"} · {len(places)} counties</p><h1>Flood insurance by state and county</h1>
<p class="lede">Find your state or county for what people there pay, whether you're required to buy it, and what floods have paid out.</p>
<input id="s" placeholder="Type your state or county…" aria-label="Find your state or county" autocomplete="off"><p id="nomatch" class="mut" aria-live="polite"></p>{'<p>Or <a href="/flood-insurance/zip/">look up a ZIP code</a>.</p>' if (_zm_zip == "all" or "zip" in _zm_zip) else ""}</section>
<div class="card"><h2>States</h2>
<table id="st"><thead><tr><th>State</th><th>Median / yr</th><th>Insured units</th><th>NFIP claims on record</th><th>Paid on them</th></tr></thead>
<tbody>{srows or '<tr><td colspan=5 class=mut>State pages are being built.</td></tr>'}</tbody></table>{_cnote}</div>
<div class="card"><h2>Counties</h2>
<table id="t"><thead><tr><th>County</th><th>Median / yr</th><th>Insured units</th></tr></thead>
<tbody>{hrows or '<tr><td colspan=3 class=mut>No counties published yet.</td></tr>'}</tbody></table></div>
<script>
var s=document.getElementById('s');
s.addEventListener('input',function(){{var q=s.value.toLowerCase();
 ['st','t'].forEach(function(id){{[].forEach.call(document.getElementById(id).tBodies[0].rows,function(r){{
   r.style.display=(!q||(r.dataset.k||'').indexOf(q)>-1)?'':'none';}});}});
 var n=[].filter.call(document.querySelectorAll('#st tbody tr,#t tbody tr'),function(r){{return r.style.display!=='none';}}).length;
 document.getElementById('nomatch').textContent=(q&&!n)?"No page matches yet. Every county's typical cost is in its state page's county table: find your state below.":'';}});
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
<li><b>NOAA Sea Level Trends</b> — NOAA Tides &amp; Currents (tidesandcurrents.noaa.gov/sltrends). NOAA's own published trend per tide station, in inches per decade with its period; county pages show only a gauge inside the county, never one from another county.</li>
<li><b>National Risk Index (counties)</b> — FEMA ArcGIS (FEMA_NationalRiskIndex). Flood expected annual loss + percentile.</li>
<li><b>Multiple-Loss Flood Properties</b> — OpenFEMA (Individual Assistance). One record per property per declared disaster that damaged it, for properties that flooded more than once; FEMA's disaster-aid data flags some as severe repeat-loss (SRL).</li>
<li><b>National Flood Hazard Layer</b> — FEMA's map service (hazards.fema.gov NFHL MapServer). County map panels and their effective dates, Letters of Map Revision and Letters of Map Amendment, counted monthly; the address tool relays FEMA's zone at a confirmed point.</li>
<li>Official <b>Policy Information by State and Community</b> workbook — listed for reference; the pages are not yet checked against it.</li></ul>
<p class="mut">Nine federal datasets; the full-risk premium is a field within Policies and the PIF workbook is a reference, not a separate fetch. Each page lists the ones it uses.</p></div>
<div class="card"><h2>Definitions &amp; rules</h2><ul>
<li><b>Policy units</b> = sum of <code>policyCount</code>, never a row count — condo-association records carry more than one unit.</li>
<li><b>Cost cohort</b>: single-family primary-residence policies (occupancy 1/11, primary residence), annual cost = premium + fees.</li>
<li><b>Percentiles</b> p25/p50/p75/p90 by inclusive interpolation.</li>
<li><b>Full-risk gap</b>: share of cohort whose premium charged (<code>totalInsurancePremiumOfThePolicy</code>) is below FEMA's full-risk premium (<code>fullRiskPremium</code>); both are premium-only. The cost figures elsewhere use <code>policyCost</code>, which FEMA defines as premium plus the reserve fund assessment, federal policy fee and HFIAA surcharge, so they are not compared with full-risk.</li>
<li><b>Claims against policies</b>: cumulative claims since 1978 beside current policy units — a historical tally, not an annual rate or a flood probability.</li>
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
<li>Compiled directly from FEMA's OpenFEMA records and FEMA's National Risk Index; no private data. One figure is a FEMA model and is labeled as such: the National Risk Index.</li>
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
later, will be disclosed here.</p>
<p>The site is run anonymously, by choice: there is no named author. Every figure instead names its exact federal
source and date, and the <a href="/methodology/">methodology</a> shows how each one is counted, so a reader can check it.</p></div>
{FOOT}"""
wr(os.path.join(DIST, "about", "index.html"), about)

# ---- 404 (round 16: a mistyped address showed the host's bare error page) ----
wr(os.path.join(DIST, "404.html"), """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
""" + GA_TAG + """<title>Page not found - Flood Insurance Data</title>
<style>body{margin:0;background:#f4f7f8;color:#132029;font:17px/1.6 system-ui,sans-serif}main{max-width:640px;margin:0 auto;padding:40px 20px}a{color:#15617f}</style>
</head><body><main><h1>Page not found</h1><p>That address has no page. Find your state or county on the
<a href="/">home page</a>, which lists every state and county.</p></main></body></html>""")

# ---- privacy policy (required for AdSense; written to current state + ad-ready, no false claims) ----
privacy = HEAD.format(title="Privacy Policy — Flood Insurance Data", desc="How Flood Insurance Data handles data, cookies, logs, and advertising.", canon=BASE + "/privacy/") + f"""
<h1>Privacy Policy</h1>
<p class="mut">Last updated {RETR}.</p>
<div class="card"><h2>What we collect</h2>
<p>Flood Insurance Data is a static reference site. We do not ask for personal information, and there
are no accounts, sign-ups, or forms. Visits are counted with Google Analytics (see below). Our host (Cloudflare) processes standard
server request logs (such as IP address and user agent) to serve the site and protect it from abuse; see
Cloudflare's privacy policy for details.</p></div>
<div class="card"><h2>Analytics and cookies</h2>
<p>We use Google Analytics to count visits and see which pages are read. It sets cookies in your browser, and
Google receives your IP address, the pages you view and basic device details. We see totals, not who you are.
You can opt out with <a href="https://tools.google.com/dlpage/gaoptout" rel="nofollow">Google's opt-out add-on</a>
or by blocking cookies in your browser. If advertising is added in future (see below), the cookies and vendors
involved will be disclosed here before they are enabled.</p></div>
<div class="card"><h2>Advertising</h2>
<p>The site currently shows no ads. If advertising is added, it may be served by Google, including Google
AdSense. Third-party vendors such as Google use cookies to serve ads based on a user's prior visits to this
and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on
visits here and elsewhere. You may opt out of personalized advertising via
<a href="https://www.google.com/settings/ads" rel="nofollow">Google Ads Settings</a>, and review other
options at <a href="https://www.aboutads.info" rel="nofollow">aboutads.info</a>. This section will be
updated to name every ad vendor at the time ads are enabled.</p></div>
<div class="card"><h2>Third-party data &amp; links</h2>
<p>All figures are compiled from public U.S. federal sources (FEMA OpenFEMA and the FEMA National Risk Index).
We link to official FEMA pages; their privacy practices are their
own. We are not affiliated with or endorsed by FEMA.</p></div>
<div class="card"><h2>Children &amp; changes</h2>
<p>The site is not directed to children under 13 and we do not knowingly collect their information. We may update this
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
                "avg_paid_claim_usd", "closed_no_payment_pct"])
    for p in places:
        ap = os.path.join(cdir(p["slug"]), "agg.json")
        if not os.path.exists(ap): continue
        a = json.load(open(ap)); P = a["policies"]; C = a["claims"]
        dp = os.path.join(cdir(p["slug"]), "data.json")
        d = json.load(open(dp)) if os.path.exists(dp) else {}
        cx = d.get("claims_extra") or {}
        w.writerow([p["slug"], p["short"], p.get("geoid"), P["units"], P["p50"], P["p25"], P["p75"], P["p90"],
                    P["frp_median"], P["share_below"], C["rows"], C["total_paid"],
                    cx.get("avg_paid"), cx.get("cwop_share")])
data = HEAD.format(title="Download the flood-insurance data", desc="Per-county NFIP flood-insurance aggregates as CSV.", canon=BASE + "/data/") + f"""
<h1>Download the data</h1>
<p>Per-county aggregates computed from FEMA OpenFEMA records: policy units, cost spread, full-risk gap, claims, average paid claim and share with no recorded payment. Blank = not available for that county.</p>
<p><a href="/data/counties.csv">counties.csv</a> — {len(places)} places.</p>
<p class="mut">Reuse freely with attribution: "This product uses FEMA's OpenFEMA API, but is not endorsed by FEMA."</p>{FOOT}"""
wr(os.path.join(DIST, "data", "index.html"), data)

# ---- one page per zone a reader meets on a letter (PLAN demand test 1): national NFIP figures, not a page per place ----
zone_urls = []
ZONES = {"ae": ("AE", "A", "all A zones (AE, A, AH, AO and others)", "zone_ae"),   # fixed text: defined even when the pages hold
         "x": ("X", "X", "X, B and C zones", "zone_x"),
         "ve": ("VE", "V", "all V zones (VE, V and others)", "zone_ve"),
         "a": ("A", "A", "all A zones (AE, A, AH, AO and others)", "zone_a"),
         "ao": ("AO", "A", "all A zones (AE, A, AH, AO and others)", "zone_ao"),
         "ah": ("AH", "A", "all A zones (AE, A, AH, AO and others)", "zone_ah"),
         "d": ("D", None, "", "zone_d")}   # D: no national cost group, units and state table only
if len(states) == 51 and len(_zh) == 51:
    def _st(sl, f): return json.load(open(os.path.join(DATADIR, "states", sl, f), encoding="utf-8"))
    _sagg = {s["slug"]: _st(s["slug"], "agg.json")["policies"] for s in states}
    _links = lambda me: " · ".join(f'<a href="/flood-zones/{k}/">Zone {v[0]}</a>' for k, v in ZONES.items() if k != me)
    def _us(f):   # a national file counts only once all 51 states carry it: never a partial total called national
        p = os.path.join(DATADIR, "us", f)
        d = json.load(open(p)) if os.path.exists(p) else {}
        return d if len(d) == 51 else {}
    _zx, _fx, _cz = _us("cost_hist_zone_exact.json"), _us("frp_hist_zone_exact.json"), _us("claims_zone.json")
    _nz = lambda H, z: sum(sum((v.get(z) or {}).values()) for v in H.values())   # priced policies behind a national exact-zone figure
    for zk, (code, grp, glab, rk) in ZONES.items():
        exact = bool(_zx) and _nz(_zx, code) >= ZONE_MIN
        # exact zone once the refresh lands; until then the group median only where the zone dominates its group (AE, X, VE)
        h = {s: v.get(code) or {} for s, v in _zx.items()} if exact else {s: v.get(grp) or {} for s, v in _zh.items()} if code in ("AE", "X", "VE") else {}
        n = sum(sum(v.values()) for v in h.values())
        med, p25, p75 = (_hq(h, 0.5), _hq(h, 0.25), _hq(h, 0.75)) if n else (None, None, None)
        fh = {s: v.get(code) or {} for s, v in _fx.items()} if _fx and _nz(_fx, code) >= ZONE_MIN else {}
        fn = sum(sum(v.values()) for v in fh.values()); fmed = _hq(fh, 0.5) if fn else None
        top = max(states, key=lambda s: ((_sagg[s["slug"]].get("cost_by_zone") or {}).get(code) or {}).get("n", 0))
        top_n = ((_sagg[top["slug"]].get("cost_by_zone") or {}).get(code) or {}).get("n", 0)
        top_line = (f' {round(100 * top_n / n)}% of them are in {top["name"]}.' if exact and n and top_n * 2 > n else "")   # AH ~86% FL, D ~58% CA: say whose price it mostly is
        def zu(s):   # None = not counted: the old top-12 field may have cut this zone off (zone_units_all lands with the next refresh)
            a = _sagg[s["slug"]].get("zone_units_all")
            if a is not None: return a.get(code, 0)
            t = _sagg[s["slug"]].get("zone_units") or {}
            return t.get(code, 0) if code in t or len(t) < 12 else None
        uncounted = sum(1 for s in states if zu(s) is None)
        units = None if uncounted else sum(zu(s) for s in states)
        known = sum(zu(s) or 0 for s in states)
        def zout(s):
            c = _st(s["slug"], "data.json").get("claims_extra") or {}
            return f'{c["outside_sfha_pct"]}%' if c.get("outside_sfha_pct") is not None and (c.get("paid_n") or 0) >= 10 else "too few"
        hr = code[0] in "AV"   # A and V zones: the 1 percent flood, the federal purchase rule, a Letter of Map Amendment
        xcol = zk == "x"
        xth = "<th>Share of the state's paid claim dollars outside zones A and V (all years, all buildings)</th>" if xcol else ""
        priced = sorted(((((_sagg[s["slug"]].get("cost_by_zone") or {}).get(code) or {}), s) for s in states), key=lambda r: -r[0].get("n", 0))
        trs = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{s["name"]}</a></td><td>{money(d["median"])}</td><td>{d["n"]:,}</td>'
                      + (f'<td>{zout(s)}</td>' if xcol else "") + "</tr>" for d, s in priced if d)
        few = sum(1 for d, s in priced if not d and zu(s))
        fewline = f" {few} more {'states have' if few > 1 else 'state has'} zone {code} policies but under {ZONE_MIN} priced ones, too few for a median." if few else ""
        xfoot = " Last column: every NFIP claim since 1978 on every building type, by the zone on the claim." if xcol else ""   # known units only: an uncounted state is never claimed to have policies
        keys = [rk, "lender_any_zone", "price_drivers", "cap", "save_ways", "howto_answer", "how_to_buy", "seller_assign", "private_accept",
                "nfip_not_sold"] + (["odds_30", "loma", "zone_review", "ec_get"] if hr else []) + (["bfe"] if code in ("AE", "AH", "VE") else []) + (["bfe_floor"] if code in ("AE", "AH") else []) + (["substantial_damage"] if hr else []) + ["glide", "loma_fee", "loma_online"] + (["tx_twia"] if zk == "ve" else [])
        vnote = (f'<p class="mut">Most insured units in this zone are not in the median: {"at least " if units is None else ""}{known:,} units are rated VE '
                 f'(condo buildings, second homes and businesses among them), while the median rests on {n:,} single-family primary-home policies.</p>') if zk == "ve" and n else ""
        # claims by the zone on each claim, ten whole loss years, dollars as paid; national only with all 51 states
        cz = {}
        for v in _cz.values():
            for z, c in v["by_zone"].items():
                t = cz.setdefault(z, [0, 0, 0]); t[0] += c["n"]; t[1] += c["paid_n"]; t[2] += c["paid"]
        yrs = f'{next(iter(_cz.values()))["from"]}–{next(iter(_cz.values()))["to"]}' if _cz else ""
        cc = cz.get(code)
        claims = ""
        # 11-08 links (CLAUDE.md Internal links): the county pages holding the most units in this zone; recomputed by zone_check Z8
        _cz10 = []
        for _p in indexable:
            _a = (json.load(open(os.path.join(cdir(_p['slug']), 'agg.json'), encoding='utf-8')).get('policies') or {}) if os.path.exists(os.path.join(cdir(_p['slug']), 'agg.json')) else {}
            _u = (_a.get('zone_units_all') or {}).get(code, 0)
            if _u: _cz10.append((-_u, _p['slug'], _p, ((_a.get('cost_by_zone') or {}).get(code) or {}).get('median')))
        _cz10 = sorted(_cz10)[:10]
        ctab = (f'<div class="card" id="counties"><h2>Which county pages have the largest numbers of zone {code} policies?</h2>'
                f'<table><thead><tr><th>County</th><th>Policy units rated {code}</th><th>Median / yr, zone {code}, single-family primary homes</th></tr></thead><tbody>'
                + ''.join(f'<tr><td><a href="/flood-insurance/{sl}/">{html.escape(pp["label"])}</a></td><td>{-nu:,}</td><td>{money(md) if md else "too few priced"}</td></tr>' for nu, sl, pp, md in _cz10)
                + f'</tbody></table><p class="mut">The {len(_cz10)} largest of the {len(indexable):,} county pages on this site by policy count, not by flood risk, and not every U.S. county. Policy units: every NFIP policy type rated exactly {code}, '
                f'in force on {_ASOF_TXT}. Median: single-family primary homes rated {code}, premium plus fees; &quot;too few priced&quot; means under {ZONE_MIN} such policies.</p></div>') if _cz10 else ''
        if cc and cc[1] >= 10:
            out_d = sum(c[2] for z, c in cz.items() if z != "blank" and z[0] not in "AV"); all_d = sum(c[2] for z, c in cz.items() if z != "blank")
            xs = (f' Of all paid claim dollars with a zone on the claim, {round(100 * out_d / all_d)}% were on claims rated outside zones A and V (zones X, B, C and D).' if xcol and all_d else "")
            claims = (f'<div class="card"><h2>What have NFIP claims in zone {code} paid?</h2><p class="stand">NFIP claims rated {code} on every building type '
                      f'(homes, condo buildings, businesses), losses in {yrs}: {cc[0]:,} claims, {cc[1]:,} paid, {money(cc[2])} paid in total, '
                      f'{money(cc[2] / cc[1])} on average per paid claim across all those buildings, not what a single home gets.{xs}</p>'
                      f'<p class="mut">Zone as rated on each claim, not today\'s map; dollars as paid, not adjusted for inflation. '
                      f'A count of claims is not a chance of flooding for any one home.</p></div>')
        elif xcol:   # until the refresh lands: the state column below is the only claims figure
            claims = ('<div class="card"><h2>How much of the claim money is outside zones A and V?</h2><p class="stand">The last column of the state table below shows, state by state, the share of NFIP claim dollars '
                      "paid on claims rated outside zones A and V, in every year on record: every zone other than A and V, not zone X alone. "
                      "It uses the zone on each claim, not today's map, and leaves out claims with no zone. That share is not a chance of flooding for any one home.</p></div>")
        cant = ("whether a zone X home is in a moderate or a minimal hazard area, because policy records do not separate them. " if xcol
                else "" if cc and cc[1] >= 10 else "claims paid in this exact zone across the country. ")
        # all zones side by side: answers "X vs AE" on every zone page instead of a separate comparison page
        def _zrow(k, v):
            hh = {s: x.get(v[0]) or {} for s, x in _zx.items()} if _zx and _nz(_zx, v[0]) >= ZONE_MIN else {}
            nn = sum(sum(x.values()) for x in hh.values())
            me = money(_hq(hh, 0.5)) if nn else "—"
            nm = f"Zone {v[0]}" if k == zk else f'<a href="/flood-zones/{k}/">Zone {v[0]}</a>'
            return f'<tr><td>{nm}</td><td>{"Yes" if v[0][0] in "AV" else "No"}</td><td>{me}</td><td>{f"{nn:,}" if nn else "—"}</td></tr>'
        ztab = (f'<div class="card"><h2>How zone {code} compares</h2><p class="stand">{rule("zone_codes")}</p><table><thead><tr><th>Zone</th>'
                f'<th>High-risk (A or V)</th><th>Median / yr</th><th>Policies in the median</th></tr></thead><tbody>'
                + "".join(_zrow(k, v) for k, v in ZONES.items()) + f'</tbody></table><p class="stand">{rule("purchase_answer")}</p><p class="mut">Median: existing single-family primary-home policies rated exactly that zone, premium plus fees, '
                f'in force on {_ASOF_TXT}; — = not yet in this data or under {ZONE_MIN} priced policies.</p></div>')
        keys += ["zone_codes", "purchase_answer"]
        if not _zx: ztab = ""   # until the refresh lands every median cell would read "—"
        if exact and n:
            tiles = (f'<div class="stat"><div class="n">{money(med)}</div><div class="l">Median / yr in zone {code}, policies in force</div></div>'
                     f'<div class="stat"><div class="n">{money(p25)}–{money(p75)}</div><div class="l">Half pay between</div></div>')   # round 72: a premium-only full-risk tile beside a with-fees median misled; back only on the same base
            base = (f'<p class="mut">{n:,} single-family primary-home policies rated {code}, premium plus fees, in force on {_ASOF_TXT}.{top_line} '
                    + 'Not a quote.</p>')
            if fmed: base += (f'<p class="mut"><b>Full-risk price:</b> FEMA&#39;s full-risk premium on zone {code} single-family primary-home policies has a median of '
                              f'{money(fmed)} ({fn:,} policies), premium only before fees, so it is not dollar-for-dollar comparable with the cost above. {rule("glide")}</p>')   # hcu 11-07
        elif n:
            tiles = (f'<div class="stat"><div class="n">{money(med)}</div><div class="l">Median / yr, {glab}</div></div>'
                     f'<div class="stat"><div class="n">{money(p25)}–{money(p75)}</div><div class="l">Half pay between</div></div>')
            base = (f'<p class="mut">{n:,} existing single-family primary-home policies in {glab}, premium plus fees, in force on {_ASOF_TXT}. '
                    f'Zone {code} alone is in the state table below. Not a quote.</p>')
        else:
            tiles, base = "", f'<p class="mut">No national median for zone {code} alone yet; <a href="#states">the state table</a> has one where {ZONE_MIN} or more priced policies exist.</p>'
        title = (f"Flood zone {code}: meaning, who must insure, cost ({money(med)} median a year)" if exact and n
                 else f"Flood zone {code}: what it means, who must insure, what it costs")
        pg = HEAD.format(title=title,
                         desc=f"What FEMA flood zone {code} means, when flood insurance is required there, and what NFIP policies in {code} cost, from FEMA's public records.",
                         canon=BASE + f"/flood-zones/{zk}/") + f"""
<h1>Flood zone {code}: what it means, who must insure, what it costs</h1>
{"<h2>Zone X, shaded X, zone B and zone C</h2>" if xcol else ""}<p class="stand">{rule(rk)}{" " + rule("odds_30") if hr else ""}</p>
<p class="stand"><b>Must I buy?</b> {rule("purchase_answer")} {rule("lender_any_zone")}</p>
<a class="btn" href="https://msc.fema.gov/portal/home" rel="noopener" target="_blank">Check your address on FEMA's flood map →</a>
{'<p><a href="/flood-zone-map/">Or look up your zone by address here</a>, with FEMA' + "'" + 's map.</p>' if (_zm_on_home == "all" or "flood-zone-map" in _zm_on_home) else ""}
<div class="stats">{tiles}</div>
{base}
{claims}{ztab}
<div class="card" id="states"><h2>What does it cost in zone {code}, by state?</h2>{vnote}
<table><thead><tr><th>State</th><th>Median / yr, zone {code}</th><th>Policies in the median</th>{xth}</tr></thead><tbody>{trs}</tbody></table>
<p class="mut">Median and policy count: single-family primary homes rated exactly {code}, premium plus fees, in force on {_ASOF_TXT}.{xfoot}{fewline}</p></div>
{ctab}
<div class="card"><h2>Buying, refinancing or questioning the zone</h2><p class="stand">{rule("seller_assign")} {rule("private_accept")}</p>
{f'<p class="stand">{rule("loma")} {rule("loma_fee")} {rule("loma_online")} {rule("zone_review")}</p>' if hr else ""}{f'<p class="stand">{rule("bfe")}</p>' if code in ("AE", "AH", "VE") else ""}{f'<p class="stand">{rule("bfe_floor")}</p>' if code in ("AE", "AH") else ""}{f'<p class="stand"><b>After a flood:</b> {rule("substantial_damage")}</p>' if hr else ""}{f'<p class="stand">{rule("ec_get")}</p>' if hr else ""}{f'<p class="stand">{rule("tx_twia")}</p>' if zk == "ve" else ""}
<p class="stand">{rule("nfip_not_sold")}</p></div>
<div class="card"><h2>Will it rise, and can I pay less?</h2><p class="stand">{rule("price_drivers")}</p><p class="stand">{rule("cap")}</p><p class="stand">{rule("save_ways")}</p></div>
<div class="card"><h2>How do I get covered?</h2><p class="stand">{rule("howto_answer")} {rule("how_to_buy")}</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">Your premium, private insurers' prices, your exact zone, why prices rise, and {cant}FEMA's map and an agent's quote answer those for your address.</p>
<p><a href="/flood-insurance/">Your state and county</a>.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 and Claims v3; rules from {_rule_hosts(keys)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "flood-zones", zk, "index.html"), pg)
        zone_urls.append((BASE + f"/flood-zones/{zk}/", None))

# ---- /flood-insurance/claims/: how often NFIP claims get any payment, county by county (agreed strategy 11-06, step 4) ----
# Loss years 2020+ (extras_raw "recent"). FEMA's data has no open/closed field, so "no recorded payment" is never "denied".
# Records FEMA coded 98 "Claim deleted in error" / 99 "Assigned in error" are bookkeeping, not claims: left out, and said so.
from codes import NONPAY_REASON as _NR
from agg_raw import FIPS as _FIPS
ERR_CODES, CLAIMS_MIN = ("98", "99"), 500
def claims_rows():   # shared with tools/claims_check.py's independent recompute only through the data files, never this code
    st_of = {v: k for k, v in _FIPS.items()}
    names = json.load(open(os.path.join(DATADIR, "us", "county_names.json"), encoding="utf-8"))
    live = {p.get("geoid"): p["slug"] for p in places}
    out = []
    for p in sorted(glob.glob(os.path.join(DATADIR, "all-counties", "*.json"))):
        g = os.path.basename(p)[:-5]
        rc = ((json.load(open(p)).get("extras") or {}).get("claims") or {}).get("recent")
        if not rc: continue
        err = sum(rc["unpaid_reasons"].get(c, 0) for c in ERR_CODES); n = rc["n"] - err
        if n < CLAIMS_MIN: continue
        un = {k: v for k, v in rc["unpaid_reasons"].items() if k not in ERR_CODES}
        top = max((k for k in un if k != "none"), key=lambda k: un[k], default=None)
        out.append({"geoid": g, "county": names.get(g, g), "state": st_of.get(g[:2], ""), "n": n, "paid": rc["paid_n"], "err": err,
                    "pct": round(100 * rc["paid_n"] / n, 1), "top": top, "top_n": un.get(top, 0), "unpaid": n - rc["paid_n"], "slug": live.get(g)})
    return sorted(out, key=lambda r: r["pct"])
import glob
if len(states) == 51:
    _cr = claims_rows()
    _us = [json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["claims"].get("recent") for s in states]
    if _cr and all(_us):
        _err = sum(sum(r["unpaid_reasons"].get(c, 0) for c in ERR_CODES) for r in _us)
        _n = sum(r["n"] for r in _us) - _err; _paid = sum(r["paid_n"] for r in _us); _pct = round(100 * _paid / _n, 1)
        _rs = {}
        for r in _us:
            for k, v in r["unpaid_reasons"].items():
                if k not in ERR_CODES: _rs[k] = _rs.get(k, 0) + v
        _un = _n - _paid
        _why = "".join(f'<tr><td>{html.escape(_NR.get(k, "No reason recorded") if k != "none" else "No reason recorded, or a code without a FEMA label")}</td><td>{v:,}</td><td>{round(100 * v / _un, 1)}%</td></tr>'
                       for k, v in sorted(_rs.items(), key=lambda kv: -kv[1])[:10])
        lo, hi = _cr[0], _cr[-1]
        cname = lambda r: f'{html.escape(r["county"])}, {r["state"]}'
        clink = lambda r: f'<a href="/flood-insurance/{r["slug"]}/">{cname(r)}</a>' if r["slug"] else cname(r)
        # top-3 compare 11-09: claims-data results name the spike years; ten costliest loss years, all 51 states summed (claims_check C6)
        _yb = {}
        for c in _cy:
            for y, (cn, cp) in c["by_year"].items(): _yb.setdefault(int(y), [0, 0]); _yb[int(y)][0] += cn; _yb[int(y)][1] += cp
        _ytop = sorted(_yb.items(), key=lambda kv: -kv[1][1])[:10]; _ya = int(_asof()[:4])
        _yopen = [y for y, _ in _ytop if y >= _ya - 1]
        _ycard = ('<div class="card" id="years"><h2>Which years paid the most?</h2><p class="stand">The ten loss years with the most paid on NFIP claims, '
                  f'all 50 states and DC, losses from {min(_yb)} to {max(_yb)}.</p><table><thead><tr><th>Year of loss</th><th>Claims on record</th><th>Paid on them</th></tr></thead><tbody>'
                  + "".join(f'<tr><td>{y}</td><td>{v[0]:,}</td><td>{money(v[1])}</td></tr>' for y, v in _ytop)
                  + '</tbody></table><p class="mut">Claims on record: every claim record, paid or not, except records FEMA coded "deleted in error" or "assigned in error", by the year of the loss. Paid on them: building plus contents payments, '
                  'in dollars as paid, not adjusted for inflation. Puerto Rico and the other territories are not in these totals.'
                  + (f' Totals for {" and ".join(map(str, sorted(_yopen)))} are not final while their claims stay open.' if _yopen else '') + '</p></div>')
        # top-3 compare 11-09: claim size; per-state median paid building claim already on each state page, here as a range (claims_check C7)
        _sz = sorted((c["paid_building_median"], s["name"], s["slug"]) for s in states
                     for c in [json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["claims"]]
                     if c.get("paid_building_median") and (c.get("damage_n") or 0) >= CLAIMS_MIN)
        _szout = sorted(s["name"] for s in states if s["slug"] not in {x[2] for x in _sz})   # r124: name who is left out
        if len(_sz) >= 2:
            _slink = lambda x: f'<a href="/flood-insurance/{x[2]}/">{html.escape(x[1])}</a>'
            _ycard += ('<div class="card" id="size"><h2>How big is a typical paid claim?</h2><p class="stand">The median paid building claim runs from '
                       f'{money(_sz[0][0])} in {_slink(_sz[0])} to {money(_sz[-1][0])} in {_slink(_sz[-1])}, among the {len(_sz)} states with {CLAIMS_MIN} or more such claims'
                       + (f' (left out, with fewer: {", ".join(html.escape(n) for n in _szout)})' if _szout else '') + '.</p>'
                       '<p class="mut">Median of the building payment on claims with recorded building damage and a building payment, every loss year since 1978, in dollars as paid, '
                       'not adjusted for inflation. Contents payments are not in it. Each state page shows its own figure.</p></div>')
        _rows = "".join(f'<tr><td>{clink(r)}</td><td>{r["n"]:,}</td><td>{r["pct"]}%</td><td>{html.escape(_NR.get(r["top"], "—")) if r["top"] else "—"}</td></tr>' for r in _cr)
        with open(os.path.join(DIST, "data", "claims-2020-counties.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["county_fips", "county", "state", "claims_loss_year_2020_on", "claims_with_recorded_payment", "share_with_payment_pct",
                                           "records_coded_deleted_or_assigned_in_error_left_out", "most_recorded_reason_for_no_payment", "claims_with_that_reason"])
            for r in _cr: w.writerow([r["geoid"], r["county"], r["state"], r["n"], r["paid"], r["pct"], r["err"], _NR.get(r["top"], "") if r["top"] else "", r["top_n"]])
        pg = HEAD.format(title=f"How often do NFIP flood claims get paid? {len(_cr)} counties compared (FEMA data)",
                         desc=f"Share of NFIP flood claims with a recorded payment, losses from 2020 on, for the {len(_cr)} counties with {CLAIMS_MIN} or more claims, and FEMA's recorded reasons when nothing was paid.",
                         canon=BASE + "/flood-insurance/claims/") + f"""
<h1>How often do NFIP flood claims get paid?</h1>
<p class="lede">Of {_n:,} NFIP flood claims for losses from 2020 on, {_pct}% had a recorded payment. In the {len(_cr)} counties with {CLAIMS_MIN} or more such claims, the share runs from {lo["pct"]}% in {cname(lo)} to {hi["pct"]}% in {cname(hi)}.</p>
<div class="stats"><div class="stat"><div class="n">{_pct}%</div><div class="l">Claims with a recorded payment, U.S., losses 2020 on</div></div>
<div class="stat"><div class="n">{_n:,}</div><div class="l">NFIP claims counted</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Claims v3, as of {_ASOF_TXT}. A recorded payment is any building, contents or Increased Cost of Compliance payment above $0. Left out: {_err:,} records FEMA coded "Claim deleted in error" or "Assigned in error"; counted as claims with no payment, the U.S. share would be {round(100 * _paid / (_n + _err), 1)}%. FEMA's data does not say whether a claim is still open, so a recent claim with no payment may still be paid.</p>
<div class="card"><h2>Why claims had no recorded payment</h2><p class="stand">FEMA's recorded reason on the building part of each of the {_un:,} U.S. claims with no recorded payment, losses from 2020 on.</p>
<table><thead><tr><th>FEMA's recorded reason</th><th>Claims</th><th>Share of claims with no payment</th></tr></thead><tbody>{_why}</tbody></table>
<p class="mut">The ten most common reasons, as FEMA labels its codes. A reason is FEMA's record, not a finding about what happened to the building.</p></div>
{_ycard}
<div class="card" id="counties"><h2>County by county</h2><p class="stand">Every county with {CLAIMS_MIN} or more NFIP claims for losses from 2020 on, lowest share with a payment first. Recent claims with no payment may still be paid: FEMA's data has no open or closed field.</p>
<table><thead><tr><th>County</th><th>Claims</th><th>With a recorded payment</th><th>Most recorded reason when nothing was paid</th></tr></thead><tbody>{_rows}</tbody></table>
<p class="mut">County as coded on each claim record, which can differ from where the building stands. <a href="/data/claims-2020-counties.csv">Download this table (CSV)</a>.</p></div>
<div class="card"><h2>What these numbers cannot tell you</h2><p class="stand">No recorded payment does not mean a claim was denied: it includes damage under the deductible, claims not pursued and reasons FEMA does not record. These are shares of claims filed, not a chance that any one claim gets paid.</p>
<p><a href="/flood-insurance/">Your state and county</a>: what policies there cost and every claim paid since 1978.</p>
<p class="mut">Source: FEMA OpenFEMA NFIP Claims v3 (fema.gov/openfema-data-page/nfip-redacted-claims-v3). Reason labels from FEMA's data dictionary. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "flood-insurance", "claims", "index.html"), pg)
        zone_urls.append((BASE + "/flood-insurance/claims/", None))

# ---- /nfip/: "The NFIP in numbers" (PAGE QUEUE row 5: "nfip", "fema flood insurance"). Every figure from the same files the
# home page uses (cost_hist, built.json); program facts only via rule(). tools/claims_check.py --nfip recomputes them.
if len(states) == 51:
    _paid_all = sum(s["paid"] for s in states); _cl_all = sum(s["claims"] for s in states)
    _top = sorted(states, key=lambda s: -s["units"])[:10]
    _trs = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td><td>{s["units"]:,}</td><td>{round(100 * s["units"] / _units, 1)}%</td></tr>' for s in _top)
    _nk = ["purchase_answer", "lender_any_zone", "nfip_not_sold", "how_to_buy", "limits", "wait_30", "nfip_lapse", "private_accept"]
    pg = HEAD.format(title=f"The NFIP in numbers: {_units / 1e6:.1f} million policy units, {money(_med)}/yr median, claims since 1978",
                     desc="The National Flood Insurance Program from FEMA's own records: policy units in force, what single-family homes pay, claims and dollars paid since 1978, and where the policies are.",
                     canon=BASE + "/nfip/") + f"""
<h1>The NFIP in numbers</h1>
<p class="lede">The National Flood Insurance Program had {_units:,} policy units in force on {_ASOF_TXT}. Existing single-family primary-home policies cost a median of {money(_med)} a year, premium plus fees. Since 1978 FEMA's records list {_cl_all:,} NFIP claims, paid or not, and {money(_paid_all)} paid in total on them.</p>
<div class="stats"><div class="stat"><div class="n">{_units / 1e6:.1f}M</div><div class="l">Policy units in force</div></div>
<div class="stat"><div class="n">{money(_med)}</div><div class="l">Median / yr, single-family primary home</div></div>
<div class="stat"><div class="n">${_paid_all / 1e9:.1f}B</div><div class="l">Paid on NFIP claims since 1978, dollars as paid</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3 and Claims v3, as of {_ASOF_TXT}. Policy units: every NFIP policy unit, including condos, rentals and businesses. Claims paid: building plus contents payments, not adjusted for inflation. <a href="/flood-insurance/claims/">How often claims get paid, county by county</a>.</p>
<div class="card"><h2>Am I required to buy it?</h2><p class="stand">{rule("purchase_answer")} {rule("lender_any_zone")}</p></div>
<div class="card"><h2>How does the NFIP work?</h2><p class="stand">{rule("nfip_not_sold")} {rule("limits")} {rule("wait_30")}</p><p class="stand">{rule("how_to_buy")}</p><p class="stand">{rule("nfip_lapse")}</p><p class="stand">{rule("private_accept")}</p></div>
<div class="card"><h2>Where are the NFIP policies?</h2><p class="stand">The ten states with the most NFIP policy units, and their share of all units in force.</p>
<table><thead><tr><th>State</th><th>Policy units</th><th>Share of U.S.</th></tr></thead><tbody>{_trs}</tbody></table>
<p class="mut">Every state, with costs and claims: <a href="/flood-insurance/">states and counties</a>. Cost in each flood zone: <a href="/flood-zones/ae/">zone AE</a>, <a href="/flood-zones/x/">zone X</a>. <a href="/flood-insurance/zip/">Cost by ZIP code</a>.</p></div>
<div class="card"><h2>What these numbers cannot tell you</h2><p class="stand">Your premium, private insurers' prices, or why a price changed. The median is what existing policies pay, not a quote.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 and Claims v3; rules from {_rule_hosts(_nk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
    wr(os.path.join(DIST, "nfip", "index.html"), pg)
    zone_urls.append((BASE + "/nfip/", None))

# ---- /flood-insurance/renters/ (PAGE QUEUE row 6: "flood insurance for renters"). Base: NFIP policies in force marked tenant,
# residential occupancy, no building coverage, contents above $0; priced = policyCost above $0. claims_check.py --renters recomputes.
if RENT_ON:
    _rq = {k: _hq(_rh, k) for k in (0.25, 0.5, 0.75)}
    _rs = sorted(((st, sum(h.values()), _hq({st: h}, 0.5)) for st, h in _rh.items() if sum(h.values()) >= 30), key=lambda r: -r[1])
    _snm = {s["abbr"]: s for s in states} if states and "abbr" in states[0] else {}
    _rtr = "".join(f'<tr><td>{(f'<a href="/flood-insurance/{_snm[st]["slug"]}/">' + html.escape(_snm[st]["name"]) + "</a>") if st in _snm else st}</td><td>{money(md)}</td><td>{n:,}</td></tr>' for st, n, md in _rs)
    _rk = ["renters_cover", "wait_30", "how_to_buy", "not_covered", "flood_def"]
    pg = HEAD.format(title=f"Flood insurance for renters: {money(_rq[0.5])}/yr NFIP median, by state",
                     desc=f"What renters pay for NFIP flood insurance on their belongings: a median of {money(_rq[0.5])} a year on {_rn:,} priced renter policies, by state, from FEMA's own records.",
                     canon=BASE + "/flood-insurance/renters/") + f"""
<h1>Flood insurance for renters</h1>
<p class="lede">Renters with an NFIP policy on their belongings paid a median of {money(_rq[0.5])} a year, premium plus fees, across {_rn:,} priced renter policies in force on {_ASOF_TXT}. The middle half paid {money(_rq[0.25])} to {money(_rq[0.75])}.</p>
<div class="stats"><div class="stat"><div class="n">{money(_rq[0.5])}</div><div class="l">Median / yr, NFIP renter policy</div></div>
<div class="stat"><div class="n">{money(_rq[0.25])}–{money(_rq[0.75])}</div><div class="l">Middle half / yr</div></div>
<div class="stat"><div class="n">{_rn:,}</div><div class="l">Priced renter policies</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3, as of {_ASOF_TXT}. Renter policy: FEMA marks the policyholder a tenant, the building residential, no building coverage and some contents coverage. Priced: a policy cost above $0. <a href="/methodology/">How we check them</a>.</p>
<div class="card"><h2>What does renters flood insurance cover?</h2><p class="stand">{rule("renters_cover")}</p><p class="stand">{rule("wait_30")}</p><p class="stand">{rule("how_to_buy")}</p><p class="stand"><b>What it won't pay:</b> {rule("not_covered")} {rule("flood_def")}</p></div>
<div class="card"><h2>What do renters pay in each state?</h2><p class="stand">States with at least 30 priced NFIP renter policies, most policies first.</p>
<table><thead><tr><th>State</th><th>Median / yr</th><th>Priced renter policies</th></tr></thead><tbody>{_rtr}</tbody></table>
<p class="mut">What homeowners pay: <a href="/nfip/">the NFIP in numbers</a>. <a href="/flood-insurance/zip/">Cost by ZIP code</a> (single-family homes).</p></div>
<div class="card"><h2>What these numbers cannot tell you</h2><p class="stand">Your premium, private insurers' prices, or why a price changed. The median is what existing NFIP renter policies pay, not a quote. Whether you must buy it is not in FEMA's data: only your lease or landlord can say.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3; rules from {_rule_hosts(_rk)}.</p></div>{FOOT}"""
    wr(os.path.join(DIST, "flood-insurance", "renters", "index.html"), pg)
    zone_urls.append((BASE + "/flood-insurance/renters/", None))

# ---- /flood-insurance/zip/: national ZIP lookup (PLAN target C). Static JSON per 3-digit ZIP prefix, a few KB per lookup.
# Figures exactly as each county's agg holds them (by_zip: units, priced single-family policies, median at ZIP_MIN+); a ZIP
# below the floor shows no ZIP median, and the county median labelled as the county. tools/test_ziptool.py = oracle.
_zip_on = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_flags.json"), encoding="utf-8")).get("zip") or []
if len(states) == 51 and (_zip_on == "all" or "zip" in _zip_on):
    from ffcalc import ZIP_MIN
    _names = json.load(open(os.path.join(DATADIR, "us", "county_names.json"), encoding="utf-8"))
    _stof = {v: k for k, v in _FIPS.items()}
    _live = {p.get("geoid"): p["slug"] for p in places}
    _z3, _cty = {}, {}
    for p in sorted(glob.glob(os.path.join(DATADIR, "all-counties", "*.json"))):
        g = os.path.basename(p)[:-5]; P = json.load(open(p))["policies"]
        for r in P.get("by_zip") or []:
            z = str(r["zip"]).strip()
            if len(z) != 5 or not z.isdigit(): continue
            _z3.setdefault(z[:3], {}).setdefault(z, []).append([g, r["units"], r["cost_n"], r["median"]])
            _cty[g] = [_names.get(g, g), _stof.get(g[:2], ""), P["p50"] if (P.get("cost_n") or 0) >= 30 else None, _live.get(g)]
    _zd = os.path.join(DIST, "data", "zip"); shutil.rmtree(_zd, ignore_errors=True); os.makedirs(_zd)   # no stale prefix files (review 11-07)
    for k, zs in _z3.items():
        for v in zs.values(): v.sort(key=lambda x: -x[1])   # most policy units first
        used = {x[0] for v in zs.values() for x in v}
        json.dump({"z": zs, "c": {g: _cty[g] for g in sorted(used)}}, open(os.path.join(_zd, k + ".json"), "w"), separators=(",", ":"))
    _zjs = """<script>(function(){var f=document.getElementById('zf'),i=document.getElementById('zi'),o=document.getElementById('zo');
function m(n){return '$'+Math.round(n).toLocaleString('en-US')}function c(n){return Number(n).toLocaleString('en-US')}
function e(s){return String(s).replace(/[&<>"]/g,function(x){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[x]})}
function say(z,d){var r=d&&d.z&&d.z[z];if(!r)return['No NFIP policy in FEMA\\'s records lists ZIP '+z+'.'];var L=[];
if(r.length>1)L.push('ZIP '+z+' appears on NFIP policies in '+r.length+' counties:');
r.forEach(function(x){var k=d.c[x[0]]||[x[0],'',null,null],nm=k[0]+(k[1]?', '+k[1]:'');
L.push(nm+': '+c(x[1])+' policy units. '+(x[3]!=null?'Median '+m(x[3])+' a year ('+c(x[2])+' priced single-family policies).'+(k[2]!=null?' The '+k[0]+' median for the same kind of policy is '+m(k[2])+' a year.':''):
'Too few priced single-family policies ('+c(x[2])+') for a ZIP median'+(k[2]!=null?'; the '+k[0]+' median is '+m(k[2])+' a year.':'.')))});return L}
window.__zipSay=say;
f.addEventListener('submit',function(ev){ev.preventDefault();var z=(i.value||'').replace(/\\s+/g,'').slice(0,5);
if(!/^\\d{5}$/.test(z)){o.innerHTML='<p>Enter a five-digit ZIP code.</p>';return}o.innerHTML='<p>Looking up '+z+'…</p>';
fetch('/data/zip/'+z.slice(0,3)+'.json').then(function(r){return r.status===404?{z:{}}:r.ok?r.json():null}).then(function(d){
if(!d){o.innerHTML='<p>The ZIP data did not load. Try again, or <a href="/flood-insurance/">find your county</a>.</p>';return}
o.innerHTML=say(z,d).map(function(s){return '<p>'+e(s)+'</p>'}).join('')}).catch(function(){o.innerHTML='<p>The ZIP data did not load. Try again, or <a href="/flood-insurance/">find your county</a>.</p>'})})})();</script>"""
    pg = HEAD.format(title="Flood insurance cost by ZIP code: NFIP median for your ZIP (FEMA data)",
                     desc="Type a ZIP code to see the median yearly cost of NFIP flood insurance on single-family homes there, how many policies it rests on, and the county figure when a ZIP has too few.",
                     canon=BASE + "/flood-insurance/zip/") + f"""
<h1>Flood insurance cost by ZIP code</h1>
<p class="lede">Type a ZIP code to see what existing NFIP flood insurance policies on single-family homes there typically cost a year, and how many policies that rests on.</p>
<form id="zf" class="zm"><label for="zi"><b>ZIP code</b></label><input id="zi" inputmode="numeric" autocomplete="postal-code" maxlength="10" style="width:100%;min-height:44px">
<p><button type="submit" class="btn">Look up</button></p></form><div id="zo" aria-live="polite"></div>
<noscript><p>This lookup needs JavaScript. <a href="/flood-insurance/">Find your state and county</a> instead: each county page lists its ZIPs.</p></noscript>
<p class="mut">Median: existing single-family primary-home NFIP policies, premium plus fees, in force on {_ASOF_TXT}; shown only where {ZIP_MIN} or more priced policies exist. Policy units: every NFIP policy unit with that ZIP, all building types. ZIPs exactly as FEMA recorded them on policies; a ZIP with only a policy or two in a county may have been entered with the wrong county. Not a quote.</p>
<div class="card"><h2>Why one ZIP's figure is not your price</h2><p class="stand">{rule("price_drivers")}</p><p>For the full picture where you live, open <a href="/flood-insurance/">your state and county</a>.</p>
<p class="mut">Source: FEMA OpenFEMA NFIP Policies v3; rules from {_rule_hosts(["price_drivers"])}. <a href="/methodology/">How we check them</a>.</p></div>{_zjs}{FOOT}"""
    wr(os.path.join(DIST, "flood-insurance", "zip", "index.html"), pg)
    zone_urls.append((BASE + "/flood-insurance/zip/", None))

# ---- address tool: static files + the /flood-zone-map/ hub (map debate 11-06; kill switch "zonemap" in tools_flags.json) ----
import shutil
from zonemap_block import block as _zm_block
_ST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
_zm_on = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools_flags.json"), encoding="utf-8")).get("zonemap") or []
if _zm_on:
    shutil.copytree(os.path.join(_ST, "vendor"), os.path.join(DIST, "vendor"), dirs_exist_ok=True)
    shutil.copy(os.path.join(_ST, "zonemap.js"), os.path.join(DIST, "zonemap.js"))
if _zm_on == "all" or "flood-zone-map" in _zm_on:
    _zkeys = ["zone_codes", "purchase_answer", "lender_any_zone", "zone_review", "loma", "fema_asis"]
    pg = HEAD.format(title="Flood zone map: find your FEMA flood zone by address",
                     desc="Type an address or use your location, confirm the pin on your building, and see the flood zone FEMA's own map shows there, with its map panel and date.",
                     canon=BASE + "/flood-zone-map/") + f"""
<h1>Flood zone map: find your FEMA flood zone by address</h1>
<p class="lede">Type an address or use your location, put the pin on your building, and see the zone FEMA's own map shows there, with its map panel and the date it took effect.</p>
{_zm_block(rule)}
<div class="card"><h2>What the zones mean</h2><p class="stand">{rule("zone_codes")}</p>
{("<p>Each zone, with what it costs and what claims there paid: " + " · ".join(f'<a href="/flood-zones/{k}/">Zone {v[0]}</a>' for k, v in ZONES.items() if os.path.exists(os.path.join(DIST, "flood-zones", k, "index.html"))) + ".</p>") if any(os.path.exists(os.path.join(DIST, "flood-zones", k, "index.html")) for k in ZONES) else ""}</div>
<div class="card"><h2>Must I buy flood insurance in my zone?</h2><p class="stand">{rule("purchase_answer")} {rule("lender_any_zone")}</p></div>
<div class="card"><h2>If the zone looks wrong</h2><p class="stand">{rule("loma")} {rule("loma_fee")} {rule("loma_online")} {rule("zone_review")}</p></div>
<div class="card"><h2>Is my map about to change?</h2><p class="stand">{rule("prelim")}</p></div>
<div class="card"><h2>What this tool cannot tell you</h2><p class="stand">Your premium, whether your lender will require a policy, and anything FEMA's digital map does not cover. The zone shown is FEMA's map, not an official determination.</p>
<p><a href="/flood-insurance/">Your state and county</a>: what policies there cost and what floods there paid.</p>
<p class="mut">Sources: FEMA National Flood Hazard Layer (map service), U.S. Census Bureau geocoder; rules from {_rule_hosts(_zkeys)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
    wr(os.path.join(DIST, "flood-zone-map", "index.html"), pg)
    zone_urls.append((BASE + "/flood-zone-map/", None))

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
        (BASE + "/methodology/", None), (BASE + "/data/", None), (BASE + "/privacy/", None), (BASE + "/terms/", None)] + zone_urls + county_urls + \
       [(BASE + f"/flood-insurance/{s['slug']}/", county_lastmod(os.path.join("states", s["slug"]))) for s in states]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "".join(f"  <url><loc>{u}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>\n" for u, lm in urls) + \
     "</urlset>\n"
wr(os.path.join(DIST, "sitemap.xml"), sm)
from indexnow import KEY as _INKEY
wr(os.path.join(DIST, _INKEY + ".txt"), _INKEY)   # IndexNow key file (tools/indexnow.py)
wr(os.path.join(DIST, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
wr(os.path.join(DIST, "_headers"), "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
   "  X-Frame-Options: DENY\n  Strict-Transport-Security: max-age=31536000\n"   # audit 11-04; no CSP: inline scripts + GA tag
   "/flood-insurance/*/data.csv\n  X-Robots-Tag: noindex\n")   # a download, not a search result
# 11-08: AI assistants (ChatGPT sends visitors) read this file and quote it: every figure carries its base and date, every
# county its state, and the reader tools are listed (a bare "median $1,169" or "Jefferson County" would be quoted wrong)
_llm_tools = [(u, t) for u, t in (("/flood-zone-map/", "Flood zone map lookup by address (FEMA's own map service, not an official determination)"),
                                   ("/flood-insurance/zip/", "Flood insurance cost by ZIP code"), ("/flood-insurance/claims/", "How often NFIP flood claims got paid, by county, since 2020 (+ CSV)"),
                                   ("/nfip/", "The NFIP in numbers"), ("/flood-insurance/renters/", "What renters pay for NFIP flood insurance"))
              if os.path.exists(os.path.join(DIST, u.strip("/"), "index.html"))]
_llm_zones = [k for k in ZONES if os.path.exists(os.path.join(DIST, "flood-zones", k, "index.html"))]
wr(os.path.join(DIST, "llms.txt"),
   "# Flood insurance data\n\n> What U.S. homeowners actually pay for NFIP flood insurance, by state, county, ZIP and flood zone, "
   "with claims history, flood risk and community discounts, all computed from FEMA's public records (OpenFEMA). Not quotes, "
   "not advice, not endorsed by FEMA.\n\n"
   f"Every \"median\" below is the median yearly cost (premium plus fees) of existing NFIP policies on single-family primary homes, "
   f"in force on {_ASOF_TXT}. Private flood insurance is not in FEMA's data. How each figure is counted: {BASE}/methodology/\n\n"
   "## Tools\n" + "".join(f"- [{t}]({BASE}{u})\n" for u, t in _llm_tools)
   + "".join(f"- [What flood zone {ZONES[k][0]} means" + (" and what it costs" if ZONES[k][1] else "") + f"]({BASE}/flood-zones/{k}/)\n" for k in _llm_zones) +   # D: no cost group
   "\n## States\n" + "".join(f"- [{s['name']}]({BASE}/flood-insurance/{s['slug']}/): median {money(s['median'])} a year\n" for s in states) +
   "\n## Counties\n" + "".join(f"- [{p['short']}, {p.get('state') or ''}]({BASE}/flood-insurance/{p['slug']}/): median {money(p.get('median'))} a year\n" for p in indexable) +
   f"\n## Data\n- [Methodology]({BASE}/methodology/)\n- [All counties (CSV)]({BASE}/data/counties.csv)\n\n"
   "Source: FEMA OpenFEMA (NFIP policies and claims, National Risk Index, disaster declarations, map service). Aggregates only.\n")

print(f"built site: {len(places)} places, home+methodology+data+sitemap+robots+llms into {DIST}")
