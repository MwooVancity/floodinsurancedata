"""Build the shared site pages from places.json: home+lookup, methodology, data (CSV),
sitemap.xml, robots.txt, llms.txt. Reads per-county agg.json for the download table.
Env: FF_PLACES (places.json), FF_DIST (dist dir), FF_DATADIR (per-county data root), FF_BASEURL."""
import collections, csv, json, os, html, re, shutil, sys
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
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google-site-verification" content="geYcfFcAsSIVIT2iHnH60suuJ4t3fx7unryWmcbos6A"><meta name="google-adsense-account" content="ca-pub-8997828618122077"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8997828618122077" crossorigin="anonymous"></script><title>{title}</title>
<meta name="description" content="{desc}"><link rel="canonical" href="{canon}"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
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
@media(max-width:620px){{h1{{font-size:30px}}.stats{{grid-template-columns:1fr 1fr}}.card{{padding:18px 15px}}table{{font-size:13.5px}}th,td{{padding:7px 6px}}thead th{{font-size:11px}}}}.tw{{overflow-x:auto}}</style><style>"""+THEME.replace("{","{{").replace("}","}}")+"""</style></head><body>
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
          'Paid on them: building plus contents payments, in dollars as paid, not adjusted for inflation. <a href="/flood-insurance/claims/">How often claims get paid, county by county</a>.' + "".join(f' <a href="/flood-insurance/{_p["key"]}/">{html.escape(_p["title"])}</a>.' for _p in __import__("papers").READY) + '</p>') if states else ""
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
        f'<div class="card"><h2>What sets the price, and how do I pay less?</h2><p class="stand">{rule("price_drivers")}</p><p class="stand">{rule("cap")}</p>'
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
<p class="stand"><b>Does my homeowners policy cover floods?</b> {rule("homeowners_excl")} <a href="/guides/homeowners-insurance-flooding/">What FEMA's flood records show</a>. <a href="/guides/">More flood insurance questions, answered with FEMA's records</a>.</p>
<p class="stand"><b>Where do I buy it?</b> {rule("how_to_buy")} {rule("private_accept")}</p>
<p class="stand"><b>How much can it pay?</b> {rule("limits")}</p>
<p class="mut">Rules from {_rule_hosts(["howto_answer", "purchase_answer", "lender_any_zone", "fl_citizens_short", "homeowners_excl", "how_to_buy", "private_accept", "limits"])}. <a href="/methodology/">How we check them</a>.</p></div>
{home_cards}
<div class="card"><h2>Flood insurance policies and claims by state</h2>{extremes}
<div class="tw"><table id="st"><thead><tr><th>State</th><th>Median / yr</th><th>Insured units</th><th>NFIP claims on record</th><th>Paid on them</th></tr></thead>
<tbody>{srows or '<tr><td colspan=5 class=mut>State pages are being built.</td></tr>'}</tbody></table></div>{_cnote}</div>
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
<div class="tw"><table id="st"><thead><tr><th>State</th><th>Median / yr</th><th>Insured units</th><th>NFIP claims on record</th><th>Paid on them</th></tr></thead>
<tbody>{srows or '<tr><td colspan=5 class=mut>State pages are being built.</td></tr>'}</tbody></table></div>{_cnote}</div>
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
<div class="card" id="papers"><h2>Research papers: shared methods</h2><ul>
<li>Each county's share carries a 90% Wilson score interval (z = 1.64485). The overall range on each paper resamples whole counties 2,000 times: claims in one county are not independent of each other.</li>
<li>Counties are grouped into fifths by share instead of numbered ranks, since neighbouring counties' intervals overlap; counties with the same printed share are always in the same fifth. A fifth is a position in a list, not a grade, a risk score or a prediction.</li>
<li>No statistical test is run: a difference between two counties is a difference in FEMA's records, not a tested effect. Each paper gives two overall figures: every county with at least one record pooled, and the listed counties pooled, with its range.</li>
<li>On claims papers, records FEMA codes as deleted or assigned in error (nonPaymentReasonBuilding 98 or 99) are left out; unless a paper's Base says otherwise, a claim counts as paid when building, contents and Increased Cost of Compliance payments add to more than $0; the county is the one FEMA codes on the claim (countyCode).</li>
<li>Each data refresh adds a new dated version of every paper at its own address; earlier versions are not changed. Each paper names its data date, which is the date to give when citing a figure.</li></ul></div>
{FOOT}"""
wr(os.path.join(DIST, "methodology", "index.html"), meth)

# ---- about (E-E-A-T: who runs it, purpose, corrections, non-commercial, not FEMA) ----
CONTACT = os.environ.get("FF_CONTACT", "contact@floodinsurancedata.com")   # owner 11-12; Cloudflare Email Routing to owner inbox (MX live 11-12)
contact_html = (f'<li><b>Corrections &amp; contact:</b> <a href="mailto:{html.escape(CONTACT)}">{html.escape(CONTACT)}</a> — '
                'tell us about any figure that looks wrong and we will check it against the source record.</li>'
                if CONTACT else
                '<li><b>Checking a figure:</b> every figure links to its official federal source, and each page offers its '
                'figures as a CSV, so any number can be checked against the record it came from.</li>')
about = HEAD.format(title="About — Flood Insurance Data", desc="Who runs Flood Insurance Data, how the figures are compiled and checked, and our independence from FEMA and insurers.", canon=BASE + "/about/") + f"""
<h1>About Flood Insurance Data</h1>
<div class="card"><h2>What this is</h2>
<p>Flood Insurance Data is an independent project that makes the U.S. government's own
flood-insurance records readable one place at a time. For each county we publish what existing NFIP
policyholders actually pay, how that compares with FEMA's full-risk price, the claims history, the flood
risk, and the community discounts that lower the bill — every figure drawn from a public federal dataset,
with its exact source and the date it was pulled.</p></div>
<div class="card"><h2>How the numbers are made and checked</h2><ul>
<li>Compiled directly from FEMA's OpenFEMA records and FEMA's National Risk Index; no private data. One figure is a FEMA model and is labeled as such: the National Risk Index.</li>
<li>Every page is built by code and ships only after an automated correctness gate passes it: percentiles and
sums are recomputed, record counts are checked against the download's own totals (FEMA's separate official policy count is not yet compared), every ratio's denominator is
disclosed, and nothing publishes if a check fails. The <a href="/methodology/">methodology</a> defines every term.</li>
<li>We show aggregates only — never an individual property, policy, or quote.</li>
{contact_html}
</ul></div>
<div class="card"><h2>Independence</h2>
<p>This site is <b>not affiliated with or endorsed by FEMA</b> or any government agency, and has <b>no
relationship with any insurer, agent, or lead-generation service</b>. It does not sell insurance, generate
quotes, or earn commissions on policies. It is a reference, not a sales page. The site shows ads served by
Google AdSense (see the <a href="/privacy/">privacy page</a>); ads never change a figure, and no advertiser has a say in what is published.</p>
</div>
<div class="card" id="who"><h2>Who runs it</h2>
<p>Flood Insurance Data is run by <b>Michael Woo</b>, who works with data and is not an insurance agent, adjuster or engineer. The pages are written and checked with AI tools (Anthropic's Claude)
working under fixed rules: every figure is recomputed from FEMA's files by separate code before a page ships, every rule is quoted from
its official source, and each page goes through separate AI review passes looking for anything wrong or misleading. The site gives no
insurance advice. Every figure names its federal source and date, and the <a href="/methodology/">methodology</a> shows how each one is
counted, so anyone can check it. Corrections: <a href="mailto:contact@floodinsurancedata.com">contact@floodinsurancedata.com</a>.</p></div>
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
or by blocking cookies in your browser. Advertising cookies are described below.</p></div>
<div class="card"><h2>Advertising</h2>
<p>Every page loads Google AdSense's code, and Google may show ads on this site. Ads are served through
Google AdSense, which can include ads from other ad companies in Google's network. Third-party vendors such as Google use cookies to serve ads based on a user's prior visits to this
and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on
visits here and elsewhere. You may opt out of personalized advertising via
<a href="https://www.google.com/settings/ads" rel="nofollow">Google Ads Settings</a>, and review other
options at <a href="https://www.aboutads.info" rel="nofollow">aboutads.info</a>. Ads never change a figure
on this site.</p></div>
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
                "nfip_not_sold"] + (["odds_30", "loma", "zone_review", "ec_get"] if hr else []) + (["bfe"] if code in ("AE", "AH", "VE") else []) + (["bfe_floor"] if code in ("AE", "AH") else []) + (["floodway"] if code == "AE" else []) + (["substantial_damage"] if hr else []) + ["glide", "loma_fee", "loma_online"] + (["tx_twia"] if zk == "ve" else [])
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
                + "".join(_zrow(k, v) for k, v in ZONES.items()) + f'</tbody></table><p class="mut">High-risk "Yes": the purchase rule in "Must I buy?" above can apply there. Median: existing single-family primary-home policies rated exactly that zone, premium plus fees, '
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
{f'<p class="stand">{rule("loma")} {rule("loma_fee")} {rule("loma_online")} {rule("zone_review")}</p>' if hr else ""}{f'<p class="stand">{rule("bfe")}</p>' if code in ("AE", "AH", "VE") else ""}{f'<p class="stand">{rule("bfe_floor")}</p>' if code in ("AE", "AH") else ""}{f'<p class="stand">{rule("floodway")}</p>' if code == "AE" else ""}{f'<p class="stand"><b>After a flood:</b> {rule("substantial_damage")}</p>' if hr else ""}{f'<p class="stand">{rule("ec_get")}</p>' if hr else ""}{f'<p class="stand">{rule("tx_twia")}</p>' if zk == "ve" else ""}
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
def story_rows():   # 11-10 news stories, every county with CLAIMS_MIN+ claims in each base (claims_check C9-C11 recompute from the data files)
    st_of = {v: k for k, v in _FIPS.items()}
    names = json.load(open(os.path.join(DATADIR, "us", "county_names.json"), encoding="utf-8"))
    live = {p.get("geoid"): p["slug"] for p in places}
    out, left = {"out": [], "cause": [], "moved": []}, {"out": 0, "cause": 0, "moved": 0}
    pc = lambda a, b: round(100 * a / b, 1)
    for p in sorted(glob.glob(os.path.join(DATADIR, "all-counties", "*.json"))):
        g = os.path.basename(p)[:-5]; c = (json.load(open(p)).get("extras") or {}).get("claims") or {}
        base = {"geoid": g, "county": names.get(g, g), "state": st_of.get(g[:2], ""), "slug": live.get(g)}
        z, k, m = c.get("zone_split") or {}, c.get("cause10") or {}, c.get("moved") or {}
        if z.get("known_n"):
            if z["known_n"] >= CLAIMS_MIN:   # audit 11-10: $0 paid stays in the table ("—"), never in the "1 to 499" count
                out["out"].append(dict(base, n=z["known_n"], pct=pc(z["out_n"], z["known_n"]), dpct=pc(z.get("out_paid", 0), z["known_paid"]) if z.get("known_paid") else "—", yrs=(z["from"], z["to"])))
            else: left["out"] += 1
        if k.get("with_cause"):
            if k["with_cause"] >= CLAIMS_MIN:
                b = k["by_code"]; out["cause"].append(dict(base, n=k["with_cause"], rain=pc(b.get("4", 0), k["with_cause"]), river=pc(b.get("2", 0), k["with_cause"]),
                                                          tide=pc(b.get("1", 0), k["with_cause"]), yrs=(k["from"], k["to"])))
            else: left["cause"] += 1
        if m.get("rated_out_known"):
            if m["rated_out_known"] >= CLAIMS_MIN:
                out["moved"].append(dict(base, n=m["rated_out_known"], pct=pc(m["now_av"], m["rated_out_known"]), blank=m["current_blank"], yrs=(m["from"], m["to"])))
            else: left["moved"] += 1
    key = {"out": "pct", "cause": "rain", "moved": "pct"}   # rank by value, highest first; ties by county name
    for s, rs in out.items(): rs.sort(key=lambda r: (-r[key[s]], r["county"], r["state"]))
    return out, left

def story_cards(clink):
    out, left = story_rows(); h = ""
    lo_hi = lambda rs, f: f'{rs[0][f]}% in {clink(rs[0])} to {rs[-1][f]}% in {clink(rs[-1])}'
    caveat = f'County as coded on each claim; see the by-county note. Left out: counties with 1 to {CLAIMS_MIN - 1:,} such claims'
    if len(out["out"]) >= 2:
        rs = out["out"]; y = rs[0]["yrs"]
        h += (f'<div class="card" id="outside"><h2>Flood claims rated outside the high-risk zones, county by county</h2><p class="stand">Losses {y[0]}–{y[1]}: the share of NFIP claims '
              f'rated outside zones A and V (FEMA\'s high-risk zones) runs from {lo_hi(rs[::-1], "pct")}, among the {len(rs)} counties with {CLAIMS_MIN} or more claims with a zone on the claim.</p>'
              '<table><thead><tr><th>County</th><th>Claims with a zone</th><th>Rated outside A and V</th><th>Claims rated outside A and V: share of dollars paid on claims with a zone</th></tr></thead><tbody>'
              + "".join(f'<tr><td>{clink(r)}</td><td>{r["n"]:,}</td><td>{r["pct"]}%</td><td>{r["dpct"]}{"%" if r["dpct"] != "—" else ""}</td></tr>' for r in rs)
              + f'</tbody></table><p class="mut">Highest share first. The zone is the one used to rate each policy, not today\'s map; claims with no zone are not counted. '
              'Dollars as paid, not adjusted for inflation. Claims from recent years may still be open: FEMA\'s data has no open or closed field. '
              f'{caveat} ({left["out"]:,} counties). A share of claims is not a chance of flooding for any one home.</p></div>')
    if len(out["cause"]) >= 2:
        rs = out["cause"]; y = rs[0]["yrs"]
        h += (f'<div class="card" id="cause"><h2>Rain, river or tide: what FEMA records as the cause of paid flood claims, county by county</h2><p class="stand">Losses {y[0]}–{y[1]}: among paid NFIP claims '
              f'with a cause recorded, the share FEMA codes as "accumulation of rainfall or snowmelt" runs from {lo_hi(rs[::-1], "rain")}, in the {len(rs)} counties with {CLAIMS_MIN} or more such claims.</p>'
              '<table><thead><tr><th>County</th><th>Paid claims with a cause</th><th>Rain or snowmelt</th><th>River, stream or lake overflow</th><th>Tidal water overflow</th></tr></thead><tbody>'
              + "".join(f'<tr><td>{clink(r)}</td><td>{r["n"]:,}</td><td>{r["rain"]}%</td><td>{r["river"]}%</td><td>{r["tide"]}%</td></tr>' for r in rs)
              + '</tbody></table><p class="mut">Highest rain share first. FEMA lets a claim carry more than one cause, so a row can add up to more than 100%; other causes '
              '(alluvial fan, closed basin lake, erosion, earth movement, other) are not shown. Codes for how a claim was handled (expedited or remote adjustment) are not causes and are not counted. '
              f'{caveat} ({left["cause"]:,} counties).</p></div>')
    if len(out["moved"]) >= 2:
        rs = out["moved"]; y = rs[0]["yrs"]
        h += (f'<div class="card" id="moved"><h2>Zone on the claim vs the zone FEMA lists now: claims rated outside zones A and V</h2><p class="stand">Losses {y[0]}–{y[1]}: of NFIP claims rated outside '
              f'zones A and V that also have a current zone listed, the share whose property FEMA\'s data now lists in zone A or V runs from {lo_hi(rs[::-1], "pct")}, in the {len(rs)} counties with {CLAIMS_MIN} or more such claims.</p>'
              '<table><thead><tr><th>County</th><th>Claims rated outside A and V, current zone listed</th><th>Current zone A or V</th></tr></thead><tbody>'
              + "".join(f'<tr><td>{clink(r)}</td><td>{r["n"]:,}</td><td>{r["pct"]}%</td></tr>' for r in rs)
              + '</tbody></table><p class="mut">Highest share first. "Current zone" is FEMA\'s field for the zone "where the insured property is currently located"; FEMA\'s data does not say why '
              f'the two zones differ. Claims with no current zone are not counted. {caveat} ({left["moved"]:,} counties).</p></div>')
    if any(out.values()):
        with open(os.path.join(DIST, "data", "claims-stories-counties.csv"), "w", newline="", encoding="utf-8") as f:
            mean = {"outside_zones_a_v": "base: NFIP claims with a rated zone; share: rated outside zones A and V; second: their share of paid dollars on claims with a zone",
                    "cause_rain_river_tide": "base: paid NFIP claims with a FEMA cause code; share: rain or snowmelt (code 4); second: river, stream or lake (code 2); third: tidal (code 1); a claim can carry several codes",
                    "rated_outside_now_a_v": "base: NFIP claims rated outside zones A and V with a current zone listed; share: current zone A or V (floodZoneCurrent)"}
            src = f"FEMA OpenFEMA NFIP Claims v3, as of {_ASOF_TXT}; county as coded on the claim; codes 98/99 left out"
            w = csv.writer(f); w.writerow(["story", "county_fips", "county", "state", "loss_years", "claims_in_base", "share_pct", "second_share_pct", "third_share_pct", "meaning", "source"])
            for r in out["out"]: w.writerow(["outside_zones_a_v", r["geoid"], r["county"], r["state"], "%s-%s" % r["yrs"], r["n"], r["pct"], r["dpct"], "", mean["outside_zones_a_v"], src])
            for r in out["cause"]: w.writerow(["cause_rain_river_tide", r["geoid"], r["county"], r["state"], "%s-%s" % r["yrs"], r["n"], r["rain"], r["river"], r["tide"], mean["cause_rain_river_tide"], src])
            for r in out["moved"]: w.writerow(["rated_outside_now_a_v", r["geoid"], r["county"], r["state"], "%s-%s" % r["yrs"], r["n"], r["pct"], "", "", mean["rated_outside_now_a_v"], src])
        h += '<p class="mut"><a href="/data/claims-stories-counties.csv">Download these three tables (CSV)</a>.</p>'
    return h

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
            _csf = os.path.join(DATADIR, "us", "claim_size.json"); _cs = json.load(open(_csf)) if os.path.exists(_csf) else {}   # extras_raw, all 51 states in one run
            _ycard += ('<div class="card" id="size"><h2>How big is a typical paid claim?</h2><p class="stand">'
                       + (f'Across the 50 states and DC, the median paid building claim is {money(_cs["p50"])}, on {_cs["n"]:,} claims. ' if _cs.get("p50") and _cs.get("asof") == _asof() else '')
                       + 'By state, the median paid building claim runs from '
                       f'{money(_sz[0][0])} in {_slink(_sz[0])} to {money(_sz[-1][0])} in {_slink(_sz[-1])}, among the {len(_sz)} states with {CLAIMS_MIN} or more such claims'
                       + (f' (left out, with fewer: {", ".join(html.escape(n) for n in _szout)})' if _szout else '') + '.</p>'
                       '<p class="mut">Median of the building payment on claims with recorded building damage and a building payment, every loss year since 1978, in dollars as paid, '
                       'not adjusted for inflation. Contents payments are not in it. Each state page shows its own figure.</p></div>')
        _ycard += story_cards(clink)
        # audit 11-10: "nfip claims by county" had no current table in Google's top 3; every county's claims since 1978 (claims_check C12)
        _stof = {v: k for k, v in _FIPS.items()}; _live = {p.get("geoid"): p["slug"] for p in places}
        _cnames = json.load(open(os.path.join(DATADIR, "us", "county_names.json"), encoding="utf-8"))
        _bc = []
        for p in sorted(glob.glob(os.path.join(DATADIR, "all-counties", "*.json"))):
            c = json.load(open(p)).get("claims") or {}; g = os.path.basename(p)[:-5]
            if c.get("rows"): _bc.append({"geoid": g, "county": _cnames.get(g, g), "state": _stof.get(g[:2], ""), "slug": _live.get(g),
                                          "n": c["rows"], "paid": c["total_paid"], "y0": c["year_min"], "y1": c["year_max"]})
        _bc.sort(key=lambda r: (-r["paid"], r["county"]))
        with open(os.path.join(DIST, "data", "claims-by-county.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["county_fips", "county", "state", "claims_on_record", "paid_usd", "first_loss_year", "last_loss_year", "meaning", "source"])
            for r in _bc: w.writerow([r["geoid"], r["county"], r["state"], r["n"], r["paid"], r["y0"], r["y1"],
                                      "claims on record: every NFIP claim record, paid or not, except records FEMA coded deleted or assigned in error; paid: building plus contents payments, as paid, not adjusted for inflation; county as coded on the claim",
                                      f"FEMA OpenFEMA NFIP Claims v3, as of {_ASOF_TXT}"])
        _bcy0, _bcy1 = min(r["y0"] for r in _bc), max(r["y1"] for r in _bc)
        _bycard = ('<div class="card" id="bycounty"><h2>NFIP claims by county, ' f'{_bcy0}–{_bcy1}</h2><p class="stand">The 25 counties with the most paid on NFIP flood claims, '
                   f'of the {len(_bc):,} counties with at least one NFIP claim on record, losses from {_bcy0} to {_bcy1}, most paid first. Every county is in the download.</p>'
                   '<table><thead><tr><th>County</th><th>Claims on record</th><th>Paid on them</th></tr></thead><tbody>'
                   + "".join(f'<tr><td>{clink(r)}</td><td>{r["n"]:,}</td><td>{money(r["paid"])}</td></tr>' for r in _bc[:25])
                   + '</tbody></table><p class="mut">Claims on record: every claim record, paid or not, except records FEMA coded "deleted in error" or "assigned in error". '
                   'Paid on them: building plus contents payments, in dollars as paid, not adjusted for inflation; Increased Cost of Compliance payments are not in it. '
                   'County as coded on each claim record, which can differ from where the building stands. '
                   "Claims FEMA records with no county are in no county's row, so the county rows add to less than the U.S. total. "
                   f'Claims from {_ya - 1} and {_ya} may still be open, so totals that include them are not final. '
                   f'<a href="/data/claims-by-county.csv">Download every county ({len(_bc):,} rows, CSV)</a>.</p></div>')
        # PLAN row 13 (11-13, G1): "flood insurance claim / proof of loss / ICC" folds into this page, no twin guide. G6: none of the top 3
        # (FloodSmart, insurance.com, NerdWallet) prints how many paid claims carried an ICC payment (claims_check C13). Appeal rule says
        # "denied" (C4), so it is linked on /nfip/, not printed here.
        _ex = [json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["claims"] for s in states]
        _icc = (sum(c["icc_claims"] for c in _ex), sum(c["paid_n"] for c in _ex)) if all(c.get("icc_claims") is not None and c.get("paid_n") for c in _ex) else None
        _y0, _y1 = min(c["year_min"] for c in _cy), max(c["year_max"] for c in _cy)
        _filecard = ('<div class="card" id="file"><h2>Filing an NFIP flood claim: proof of loss and rebuilding costs</h2>'
                     f'<p class="stand">{rule("already_flooded")}</p><p class="stand">{rule("substantial_damage")}</p>'
                     + (f'<p class="stand">Of the {_icc[1]:,} NFIP claims with a recorded payment for losses from {_y0} to {_y1}, all 50 states and DC, '
                        f'{_icc[0]:,} ({round(100 * _icc[0] / _icc[1], 1)}%) include an Increased Cost of Compliance payment.</p>' if _icc and _icc[0] else '')
                     + '<p class="mut">FEMA OpenFEMA NFIP Claims v3. A recorded payment is any building, contents or Increased Cost of Compliance payment above $0; records FEMA coded "deleted in error" or "assigned in error" are left out. '
                     'Puerto Rico and the other territories are not in these totals. FEMA\'s data has no open or closed field, so counts for recent loss years are not final. '
                     '<a href="/nfip/#rules">NFIP claim appeal deadlines</a> are with the other program rules.</p></div>')
        _rows = "".join(f'<tr><td>{clink(r)}</td><td>{r["n"]:,}</td><td>{r["pct"]}%</td><td>{html.escape(_NR.get(r["top"], "—")) if r["top"] else "—"}</td></tr>' for r in _cr)
        with open(os.path.join(DIST, "data", "claims-2020-counties.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["county_fips", "county", "state", "claims_loss_year_2020_on", "claims_with_recorded_payment", "share_with_payment_pct",
                                           "records_coded_deleted_or_assigned_in_error_left_out", "most_recorded_reason_for_no_payment", "claims_with_that_reason"])
            for r in _cr: w.writerow([r["geoid"], r["county"], r["state"], r["n"], r["paid"], r["pct"], r["err"], _NR.get(r["top"], "") if r["top"] else "", r["top_n"]])
        pg = HEAD.format(title=f"NFIP claims by county: payouts since {_bcy0} and how often claims get paid (FEMA data)",
                         desc=f"NFIP flood claims and dollars paid in every U.S. county since {_bcy0}; share of claims with a recorded payment, losses from 2020 on, for the {len(_cr)} counties with {CLAIMS_MIN} or more claims, and FEMA's recorded reasons when nothing was paid.",
                         canon=BASE + "/flood-insurance/claims/") + f"""
<h1>NFIP flood claims by county: how often they get paid</h1>
<p class="lede">Of {_n:,} NFIP flood claims for losses from 2020 on, {_pct}% had a recorded payment. In the {len(_cr)} counties with {CLAIMS_MIN} or more such claims, the share runs from {lo["pct"]}% in {cname(lo)} to {hi["pct"]}% in {cname(hi)}.</p>
<div class="stats"><div class="stat"><div class="n">{_pct}%</div><div class="l">Claims with a recorded payment, U.S., losses 2020 on</div></div>
<div class="stat"><div class="n">{_n:,}</div><div class="l">NFIP claims counted</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Claims v3, as of {_ASOF_TXT}. A recorded payment is any building, contents or Increased Cost of Compliance payment above $0. Left out: {_err:,} records FEMA coded "Claim deleted in error" or "Assigned in error"; counted as claims with no payment, the U.S. share would be {round(100 * _paid / (_n + _err), 1)}%. FEMA's data does not say whether a claim is still open, so a recent claim with no payment may still be paid.</p>
{_filecard}
<div class="card"><h2>Why claims had no recorded payment</h2><p class="stand">FEMA's recorded reason on the building part of each of the {_un:,} U.S. claims with no recorded payment, losses from 2020 on.</p>
<table><thead><tr><th>FEMA's recorded reason</th><th>Claims</th><th>Share of claims with no payment</th></tr></thead><tbody>{_why}</tbody></table>
<p class="mut">The ten most common reasons, as FEMA labels its codes. A reason is FEMA's record, not a finding about what happened to the building.</p></div>
{_bycard}
{_ycard}
<div class="card" id="counties"><h2>County by county</h2><p class="stand">Every county with {CLAIMS_MIN} or more NFIP claims for losses from 2020 on, lowest share with a payment first. Recent claims with no payment may still be paid: FEMA's data has no open or closed field.</p>
<table><thead><tr><th>County</th><th>Claims</th><th>With a recorded payment</th><th>Most recorded reason when nothing was paid</th></tr></thead><tbody>{_rows}</tbody></table>
<p class="mut">County as coded on each claim; see the by-county note. <a href="/data/claims-2020-counties.csv">Download this table (CSV)</a>.</p></div>
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
    _nk = ["purchase_answer", "lender_any_zone", "nfip_not_sold", "how_to_buy", "limits", "wait_30"] + __import__("rules_home").MOVED   # owner 11-11: the national rules live here once
    pg = HEAD.format(title=f"The NFIP in numbers: {_units / 1e6:.1f} million policy units, {money(_med)}/yr median, claims since 1978",
                     desc="The National Flood Insurance Program from FEMA's own records: policy units in force, what single-family homes pay, claims and dollars paid since 1978, and where the policies are.",
                     canon=BASE + "/nfip/") + f"""
<h1>The NFIP in numbers</h1>
<p class="lede">The National Flood Insurance Program had {_units:,} policy units in force on {_ASOF_TXT}. Existing single-family primary-home policies cost a median of {money(_med)} a year, premium plus fees. Since 1978 FEMA's records list {_cl_all:,} NFIP claims, paid or not, and {money(_paid_all)} paid in total on them.</p>
<div class="stats"><div class="stat"><div class="n">{_units / 1e6:.1f}M</div><div class="l">Policy units in force</div></div>
<div class="stat"><div class="n">{money(_med)}</div><div class="l">Median / yr, single-family primary home</div></div>
<div class="stat"><div class="n">${_paid_all / 1e9:.1f}B</div><div class="l">Paid on NFIP claims since 1978, dollars as paid</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3 and Claims v3, as of {_ASOF_TXT}. Policy units: every NFIP policy unit, including condos, rentals and businesses. Claims: every claim record, paid or not, except records FEMA coded "deleted in error" or "assigned in error". Claims paid: building plus contents payments, not adjusted for inflation. <a href="/flood-insurance/claims/">How often claims get paid, county by county</a>.</p>
<div class="card"><h2>Am I required to buy it?</h2><p class="stand">{rule("purchase_answer")} {rule("lender_any_zone")}</p></div>
<div class="card"><h2>How does the NFIP work?</h2><p class="stand">{rule("nfip_not_sold")} {rule("limits")} {rule("wait_30")}</p><p class="stand">{rule("how_to_buy")}</p></div>
<div class="card" id="rules"><h2>NFIP rules in full: waits, what it won't pay, claims, rebuilding, closings</h2><p class="stand">These rules are the same in every state and county; each county and state page links here instead of repeating them.</p>
<h3>The 30-day wait and its exceptions</h3><p class="stand">{rule("wait_exceptions")} {rule("wait_wildfire")}</p>
<h3>Premium increases and surcharges</h3><p class="stand">{rule("glide")} {rule("cap")} {rule("surcharge")}</p>
<h3>Lapses</h3><p class="stand">{rule("nfip_lapse")} {rule("lapse_discount")}</p>
<h3>What a policy won't pay</h3><p class="stand">{rule("flood_def")} {rule("not_covered")} {rule("wind_excl")}</p>
<h3>FEMA disaster aid and insurance</h3><p class="stand">{rule("aid_insurance")}</p>
<h3>Appeals and rebuilding</h3><p class="stand">{rule("claim_appeal")} {rule("substantial_damage")}</p>
<h3>At a closing, and private policies</h3><p class="stand">{rule("lender_amount")} {rule("lender_force")} {rule("zone_review")} {rule("seller_assign")} {rule("private_accept")}</p></div>
<div class="card"><h2>Where are the NFIP policies?</h2><p class="stand">The ten states with the most NFIP policy units, and their share of all units in force.</p>
<table><thead><tr><th>State</th><th>Policy units</th><th>Share of U.S.</th></tr></thead><tbody>{_trs}</tbody></table>
<p class="mut">Every state, with costs and claims: <a href="/flood-insurance/">states and counties</a>. Cost in each flood zone: <a href="/flood-zones/ae/">zone AE</a>, <a href="/flood-zones/x/">zone X</a>. <a href="/flood-insurance/zip/">Cost by ZIP code</a>.</p></div>
<div class="card"><h2>What these numbers cannot tell you</h2><p class="stand">Your premium, private insurers' prices, or why a price changed. The median is what existing policies pay, not a quote.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 and Claims v3; rules from {_rule_hosts(_nk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
    wr(os.path.join(DIST, "nfip", "index.html"), pg)
    zone_urls.append((BASE + "/nfip/", None))

# ---- /guides/: one searched question per page (PLAN "Pages to build", owner 11-12). Answer first from rule() quotes read raw;
# figures only from the FEMA files every other national page uses; tools/claims_check.py --guides recomputes them.
GUIDES = []
def _nst(rows):   # review r167: "48 states" counted DC; label = states, plus "and DC" when DC is a row
    n = sum(1 for s, _ in rows if s.get("abbr") != "DC"); dc = any(s.get("abbr") == "DC" for s, _ in rows)
    return f"{n} states" + (" and DC" if dc else "")
if len(states) == 51:
    _czg = json.load(open(os.path.join(DATADIR, "us", "claims_zone.json")))
    _g_from, _g_to = min(v["from"] for v in _czg.values()), max(v["to"] for v in _czg.values())
    _zk = lambda z: z and z != "blank"   # 11-12: "blank" = no zone on the claim; counting it as outside A/V printed 25% vs the zone pages' 24%
    _g_all = sum(c["paid"] for v in _czg.values() for z, c in v["by_zone"].items() if _zk(z))
    _g_out = sum(c["paid"] for v in _czg.values() for z, c in v["by_zone"].items() if _zk(z) and z.upper()[:1] not in ("A", "V"))
    _g_n = sum(c["n"] for v in _czg.values() for z, c in v["by_zone"].items() if _zk(z))
    _g_pn = sum(c["paid_n"] for v in _czg.values() for z, c in v["by_zone"].items() if _zk(z))
    _gk = ["homeowners_excl", "how_to_buy", "wait_30", "flood_def", "not_covered", "purchase_answer", "lender_any_zone"]
    # site factory 11-12 claims_by_zone_empty: no zoned claims = no share (never a divide by zero); the page stays, its links stay live
    _g_pc = round(100 * _g_out / _g_all) if _g_all else None
    _g_tile = (f'<div class="stat"><div class="n">{_g_pc}%</div><div class="l">Of NFIP claim dollars {_g_from}–{_g_to} paid outside zones A and V</div></div>'
               if _g_pc is not None else "")
    _g_claims = (f"<p class=\"stand\">In FEMA's NFIP claims for losses {_g_from}–{_g_to}, {_g_pn:,} of the {_g_n:,} claims with a rated zone had a payment, "
                 f"and {_g_pc}% of the dollars paid on them went to claims rated outside zones A and V (zones X, B, C and D). These are insured claims only: "
                 "flood damage on homes without flood insurance is not in this data.</p>" if _g_pc is not None
                 else "<p class=\"stand\">FEMA's claims-by-zone figures are not in this build.</p>")
    pg = HEAD.format(title="Does homeowners insurance cover flooding? What FEMA's flood records show",
                     desc=f"Most homeowners insurance does not cover flood damage. What NFIP flood insurance costs and what its claims paid, from FEMA's records as of {_ASOF_TXT}.",
                     canon=BASE + "/guides/homeowners-insurance-flooding/") + f"""
<h1>Does homeowners insurance cover flooding?</h1>
<p class="lede">{rule("homeowners_excl")} {rule("how_to_buy")}</p>
<div class="stats"><div class="stat"><div class="n">{money(_med)}</div><div class="l">Median NFIP cost / yr, single-family primary home</div></div>
{_g_tile}
<div class="stat"><div class="n">{_units / 1e6:.1f}M</div><div class="l">NFIP policy units in force</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3 and Claims v3, as of {_ASOF_TXT}. Cost: premium plus fees on single-family primary-home policies in force, not a quote. Claims: losses {_g_from}–{_g_to} with a rated zone, every building type, dollars as paid, not adjusted for inflation.</p>
<div class="card"><h2>What counts as a flood?</h2><p class="stand">{rule("flood_def")}</p><p class="stand">{rule("not_covered")}</p></div>
<div class="card"><h2>Do floods happen outside the high-risk zones?</h2>{_g_claims}
<p class="stand">{rule("purchase_answer")} {rule("lender_any_zone")}</p></div>
<div class="card"><h2>How fast does a new policy start?</h2><p class="stand">{rule("wait_30")}</p></div>
<div class="card"><h2>What it costs where you live</h2><p class="stand">The median above is for the whole U.S. Each state and county page shows the median for that place, by flood zone: <a href="/flood-insurance/">find your state or county</a>, or <a href="/flood-insurance/zip/">look up a ZIP code</a>.</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">What your own homeowners policy covers (only its wording can say), private flood insurers' prices, or your premium.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 and Claims v3; rules from {_rule_hosts(_gk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
    wr(os.path.join(DIST, "guides", "homeowners-insurance-flooding", "index.html"), pg)
    zone_urls.append((BASE + "/guides/homeowners-insurance-flooding/", None))
    GUIDES.append(("/guides/homeowners-insurance-flooding/", "Does homeowners insurance cover flooding?"))
    # condo guide (KWP 11-12 "condo flood insurance" 100-1K x2): FEMA code U = "Individual Condominium Unit insured by a unit owner or by an
    # association" (DataSetFields read 11-12); premium plus fees; a state shows a median only from 30+ priced unit policies (min_priced)
    MX_MIN = __import__("metrics").CONST["min_priced"]   # the same floor extras_raw applies before a condo-unit median exists
    _cd = sorted(((s, json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"]) for s in states), key=lambda t: -(t[1].get("condo_unit_cost_n") or 0))
    _cdr = [(s, x) for s, x in _cd if x.get("condo_unit_cost_median")]
    if len(_cdr) >= 10:
        _cdn = sum(x["condo_unit_cost_n"] for _, x in _cdr)
        _ck = ["condo_rcbap", "condo_contents", "condo_own", "wait_30", "flood_def"]
        _ctr = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td><td>{money(x["condo_unit_cost_median"])}</td><td>{x["condo_unit_cost_n"]:,}</td></tr>' for s, x in _cdr)
        _cnone = [s["name"] for s, x in _cd if not x.get("condo_unit_cost_median")]
        pg = HEAD.format(title=f"Condo flood insurance: what NFIP condo-unit policies cost in {_nst(_cdr)}",
                         desc=f"What an association's flood policy covers and what it leaves to unit owners, and the median NFIP condo-unit cost in {_nst(_cdr)} from FEMA's records as of {_ASOF_TXT}.",
                         canon=BASE + "/guides/condo-flood-insurance/") + f"""
<h1>Condo flood insurance</h1>
<p class="lede">{rule("condo_rcbap")} {rule("condo_contents")}</p>
<div class="card"><h2>What do condo-unit policies cost in each state?</h2><p class="stand">Median premium plus fees on NFIP policies FEMA codes as an individual condominium unit (insured by a unit owner or by an association), in force on {_ASOF_TXT}: {_nst(_cdr)} with at least {MX_MIN} priced unit policies, {_cdn:,} policies in all, most policies first. Not a quote.</p>
<table><thead><tr><th>State</th><th>Median / yr, condo-unit policy</th><th>Priced unit policies</th></tr></thead><tbody>{_ctr}</tbody></table>
{f'<p class="mut">Too few priced unit policies for a median: {", ".join(html.escape(n) for n in _cnone)}.</p>' if _cnone else ""}
<p class="mut">County pages show the county's condo-unit median where it rests on at least {MX_MIN} policies: <a href="/flood-insurance/">find your county</a>.</p></div>
<div class="card"><h2>What each policy covers</h2><p class="stand">{rule("condo_own")}</p><p class="stand">{rule("wait_30")}</p><p class="stand">{rule("flood_def")}</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">What your association's policy covers or its limit, whether your unit policy has building coverage, private insurers' prices, or your premium. A state median mixes units insured by owners and by associations, as FEMA's code does.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 (condominiumCoverageTypeCode U, policyCost), as of {_ASOF_TXT}; rules from {_rule_hosts(_ck)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "condo-flood-insurance", "index.html"), pg)
        zone_urls.append((BASE + "/guides/condo-flood-insurance/", None))
        GUIDES.append(("/guides/condo-flood-insurance/", "Condo flood insurance"))

if len(states) == 51:   # buyer guide (KWP 11-12 "buying a house in a flood zone" 100-1K): what a NEW policy costs, by state
    _bx = [(s, json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"]) for s in states]
    _bxr = sorted(((s, x) for s, x in _bx if x.get("cost_new_median") and (x.get("cost_new_n") or 0) >= __import__("metrics").CONST["min_priced"]),
                  key=lambda t: -t[1]["cost_new_n"])
    if len(_bxr) >= 10:
        _bk = ["purchase_answer", "lender_any_zone", "lender_amount", "lender_force", "wait_30", "start_loan", "seller_assign", "zone_review", "private_accept"]
        _btr = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td><td>{money(x["cost_new_median"])}</td><td>{x["cost_new_n"]:,}</td></tr>' for s, x in _bxr)
        pg = HEAD.format(title="Buying a house in a flood zone: what new flood policies cost, by state",
                         desc=f"Whether your lender will require flood insurance, when it can start at closing, and what policies first bought in the past year cost in each state, from FEMA's records as of {_ASOF_TXT}.",
                         canon=BASE + "/guides/buying-a-house-in-a-flood-zone/") + f"""
<h1>Buying a house in a flood zone</h1>
<p class="lede">{rule("purchase_answer")} {rule("lender_any_zone")}</p>
<div class="stats"><div class="stat"><div class="n">{money(_new_med)}</div><div class="l">Typical cost, U.S. policies first bought in the past year</div></div>
<div class="stat"><div class="n">{_new_n:,}</div><div class="l">Such single-family primary-home policies</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3, as of {_ASOF_TXT}: median premium plus fees on single-family primary-home policies first written in the 12 months to that date. Not a quote: a new policy is priced for the building.</p>
<div class="card"><h2>What the lender can require</h2><p class="stand">{rule("lender_amount")} {rule("lender_force")}</p><p class="stand">{rule("private_accept")}</p></div>
<div class="card"><h2>When the policy starts</h2><p class="stand">{rule("wait_30")}</p><p class="stand">{rule("start_loan")}</p><p class="stand">{rule("seller_assign")}</p></div>
<div class="card"><h2>If you think the zone is wrong</h2><p class="stand">{rule("zone_review")} <a href="/flood-zone-map/">Check an address on FEMA's map</a>.</p></div>
<div class="card"><h2>What new policies cost in each state</h2><p class="stand">Median premium plus fees on single-family primary-home policies first written in the 12 months to {_ASOF_TXT}, in {_nst(_bxr)} with at least {__import__("metrics").CONST["min_priced"]} such policies, most policies first.</p>
<table><thead><tr><th>State</th><th>Typical cost, new policy</th><th>New policies</th></tr></thead><tbody>{_btr}</tbody></table>
<p class="mut">The county page shows the costs by flood zone in that county: <a href="/flood-insurance/">find your county</a>.</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">This house's premium, its flood zone (only FEMA's map and the lender's determination can say), whether a seller's policy can be assigned to you, or private insurers' prices.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 (policyCost, originalNBDate), as of {_ASOF_TXT}; rules from {_rule_hosts(_bk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "buying-a-house-in-a-flood-zone", "index.html"), pg)
        zone_urls.append((BASE + "/guides/buying-a-house-in-a-flood-zone/", None))
        GUIDES.append(("/guides/buying-a-house-in-a-flood-zone/", "Buying a house in a flood zone"))

if len(states) == 51:   # private flood guide (KWP 11-12 "private flood insurance" 1K-10K): FEMA holds no private policy, so the page gives
    # the lender rules (rule()) and the one FEMA figure the top 3 lack: rebuilding cost above the NFIP's $250,000 building limit.
    # extras store one-decimal shares, never counts: the U.S. share is printed only when every rounding of the state shares gives
    # the same whole percent (bounds +/-0.05), so a rounded-share sum can never print a wrong figure (claims_check P1 recomputes)
    _pv = [(s, json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"]) for s in states]
    _pvr = sorted(((s, x) for s, x in _pv if x.get("replacement_over_250k_pct") is not None and (x.get("replacement_n") or 0) >= __import__("metrics").CONST["min_priced"]),
                  key=lambda t: -t[1]["replacement_n"])
    def _pwhole(rows, pk, nk):   # whole-percent U.S. share from one-decimal state shares, or None when the rounding could tip it
        n = sum(x[nk] for _, x in rows)
        lo, hi = (sum((x[pk] + d) * x[nk] for _, x in rows) / n for d in (-0.05, 0.05))
        return (int(lo + 0.5), n) if n and int(lo + 0.5) == int(hi + 0.5) else (None, n)
    _prc, _prn = _pwhole(_pvr, "replacement_over_250k_pct", "replacement_n")
    _pmx, _pmn = _pwhole([(s, x) for s, x in _pv if x.get("at_building_max_pct") is not None and x.get("sf_n")], "at_building_max_pct", "sf_n")
    if len(_pvr) >= 10 and _prc is not None:
        _pk = ["private_accept", "private_statement", "lender_amount", "lender_force", "limits_quoted"]
        _ptr = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td><td>{x["replacement_over_250k_pct"]}%</td><td>{x["replacement_n"]:,}</td></tr>' for s, x in _pvr)
        _pdoc = next((p for p in __import__("papers").READY if p["key"] == "damage-over-coverage"), None)
        pg = HEAD.format(title="Private flood insurance: what lenders must accept, and how often a home's rebuilding cost tops the NFIP limit",
                         desc=f"When a lender must accept a private flood policy, and the share of NFIP single-family primary-home policies with a rebuilding cost above the NFIP's $250,000 building limit, by state, from FEMA's records as of {_ASOF_TXT}.",
                         canon=BASE + "/guides/private-flood-insurance/") + f"""
<h1>Private flood insurance</h1>
<p class="lede">In FEMA's records, {_prc}% of the {_prn:,} single-family primary-home NFIP policies that report a rebuilding cost report one above $250,000: for those buildings, NFIP building coverage cannot reach the full rebuilding cost. {rule("private_accept")}</p>
<div class="stats"><div class="stat"><div class="n">{_prc}%</div><div class="l">of {_prn:,} U.S. NFIP single-family primary-home policies that report a rebuilding cost: rebuilding cost above $250,000</div></div>
{f'<div class="stat"><div class="n">{_pmx}%</div><div class="l">of all {_pmn:,} U.S. NFIP single-family primary-home policies: building coverage of $250,000 or more</div></div>' if _pmx is not None else ""}</div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3, as of {_ASOF_TXT}: {_prn:,} single-family primary-home policies in force that report a rebuilding cost above $0 (buildingReplacementCost){f"; the second figure counts building coverage (totalBuildingInsuranceCoverage) of $250,000 or more over all {_pmn:,} such policies" if _pmx is not None else ""}. NFIP policies only: private policies are not in FEMA's records.</p>
<div class="card"><h2>Does the NFIP's limit cover the whole house?</h2><p class="stand">{rule("limits_quoted")}</p>
{f'<p class="stand">How often NFIP claims found more building damage than the coverage, county by county: <a href="/flood-insurance/damage-over-coverage/">flood damage over building coverage</a>.</p>' if _pdoc else ""}</div>
<div class="card"><h2>When must a lender accept a private policy?</h2><p class="stand">{rule("private_statement")}</p>
<p class="stand">{rule("lender_amount")} {rule("lender_force")}</p></div>
<div class="card"><h2>Rebuilding cost above $250,000, by state</h2><p class="stand">Share of single-family primary-home NFIP policies reporting a rebuilding cost that report one above $250,000, in {_nst(_pvr)} with at least {__import__("metrics").CONST["min_priced"]} such policies, most policies first.</p>
<table><thead><tr><th>State</th><th>Rebuilding cost above $250,000</th><th>Policies reporting one</th></tr></thead><tbody>{_ptr}</tbody></table>
<p class="mut">The rebuilding cost is the figure recorded on the NFIP policy, not an appraisal. Each state and county page shows what NFIP policies cost there: <a href="/flood-insurance/">find your state or county</a>.</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">Private insurers' prices, how many private flood policies exist or what they pay on claims, whether a given private policy meets the federal definition, or your premium. FEMA's records hold NFIP policies only. No company is named, ranked or recommended here.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 (buildingReplacementCost, totalBuildingInsuranceCoverage), as of {_ASOF_TXT}; rules from {_rule_hosts(_pk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "private-flood-insurance", "index.html"), pg)
        zone_urls.append((BASE + "/guides/private-flood-insurance/", None))
        GUIDES.append(("/guides/private-flood-insurance/", "Private flood insurance"))

if len(states) == 51:   # deductible guide (cloud field batch 11-12): building deductible on single-family primary-home policies, by zone
    # group (AE exact; X = B, C, X), counts summed over every state = exact U.S. shares; FEMA buildingDeductibleCode via codes.DEDUCTIBLE
    _dz = {}
    for s in states:
        for zg, cn in ((json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"].get("deductibles_by_zone")) or {}).items():
            for d, c in cn.items(): _dz.setdefault(zg, collections.Counter())[d] += c
    if set(_dz) >= {"AE", "X"} and all(sum(_dz[z].values()) >= 1000 for z in ("AE", "X")):
        _dn = {z: sum(_dz[z].values()) for z in ("AE", "X")}
        _dsh = lambda z, d: round(100 * _dz[z].get(d, 0) / _dn[z], 1)
        _dall = sorted({d for z in ("AE", "X") for d in _dz[z]}, key=lambda d: float(d))
        _dmain = [d for d in _dall if max(_dsh("AE", d), _dsh("X", d)) >= 1]   # deductibles under 1% in both groups: one "other" row
        _dtr = "".join(f'<tr><td>{money(float(d))}</td><td>{_dsh("AE", d)}%</td><td>{_dsh("X", d)}%</td></tr>' for d in _dmain)
        _doth = {z: round(100 - sum(_dsh(z, d) for d in _dmain), 1) for z in ("AE", "X")}
        _dtop = {z: max(_dz[z], key=lambda d: _dz[z][d]) for z in ("AE", "X")}
        _dhi = {z: round(100 * sum(_dz[z].get(d, 0) for d in _dall if float(d) >= 5000) / _dn[z], 1) for z in ("AE", "X")}   # from counts, never summed rounded shares
        _dk = ["save_ways", "price_drivers"]
        pg = HEAD.format(title="Flood insurance deductibles on NFIP policies: zone AE vs zones X, B or C",
                         desc=f"The building deductibles on {_dn['AE'] + _dn['X']:,} NFIP single-family primary-home policies in zone AE and zones X, B or C, from FEMA's records as of {_ASOF_TXT}.",
                         canon=BASE + "/guides/flood-insurance-deductible/") + f"""
<h1>Flood insurance deductibles</h1>
<p class="lede">In FEMA's records, the most common building deductible on single-family primary-home NFIP policies is {money(float(_dtop['AE']))} in zone AE and {money(float(_dtop['X']))} in zones X, B or C, and {_dhi['AE']}% of zone AE policies carry one of $5,000 or more, against {_dhi['X']}% in zones X, B or C. {rule("save_ways")}</p>
<div class="card"><h2>Which building deductible do NFIP homeowners have?</h2><p class="stand">Share of single-family primary-home NFIP policies in force on {_ASOF_TXT} by building deductible: {_dn['AE']:,} rated zone AE, {_dn['X']:,} rated zone X, B or C (the moderate- and low-risk zones).</p>
<table><thead><tr><th>Building deductible</th><th>Zone AE</th><th>Zone X, B or C</th></tr></thead><tbody>{_dtr}{f"<tr><td>Every other amount</td><td>{_doth['AE']}%</td><td>{_doth['X']}%</td></tr>" if max(_doth.values()) >= 0.1 else ""}</tbody></table>
<p class="mut">Shares are of policies, not homes; a policy's contents deductible is separate and not shown. Rounded to one decimal, so a column can miss 100% by 0.1.</p></div>
<div class="card"><h2>What FEMA prices a policy on</h2><p class="stand">{rule("price_drivers")}</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">How much a higher deductible would lower your premium, which deductible suits you, or what private policies offer. Each county page shows that county's most common deductibles: <a href="/flood-insurance/">find your county</a>.{" Every county's share at $5,000 or more, with its 90% range: <a href='/flood-insurance/deductible-choice/'>building deductibles on record by county</a>." if any(p["key"] == "deductible-choice" for p in __import__("papers").READY) else ""}</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 (buildingDeductibleCode, ratedFloodZone), as of {_ASOF_TXT}; rules from {_rule_hosts(_dk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "flood-insurance-deductible", "index.html"), pg)
        zone_urls.append((BASE + "/guides/flood-insurance-deductible/", None))
        GUIDES.append(("/guides/flood-insurance-deductible/", "Flood insurance deductibles"))

if len(states) == 51:   # vents guide (KWP 11-12 "flood vents" 1K-10K): FEMA obstructionType on elevated single-family primary-home
    # policies (cloud field batch 11-12); code text quoted from FEMA's DataSetFields, read raw 11-13; 44 CFR 60.3(c)(5) via rule()
    _OBS = {"10": "Free of obstruction", "15": "Enclosure or crawlspace with proper openings (not used for rating; not applicable in V zones)",
            "50": "Non-breakaway walls, crawlspace or finished enclosure, no machinery or equipment below the lowest elevated floor",
            "54": "Non-breakaway walls, crawlspace or finished enclosure, with machinery or equipment below the lowest elevated floor",
            "60": "With obstruction (FEMA's code gives no further detail)"}
    _oc = collections.Counter(); _ost = []
    for s in states:
        oc = json.load(open(os.path.join(DATADIR, "states", s["slug"], "extras.json")))["policies"].get("obstruction_counts") or {}
        _oc.update(oc); kn = sum(v for k, v in oc.items() if k != "blank")
        if kn >= 100: _ost.append((s, kn, oc.get("15", 0)))
    _okn = sum(v for k, v in _oc.items() if k != "blank")
    if _okn >= 1000 and len(_ost) >= 10:
        _osh = lambda k: round(100 * _oc.get(k, 0) / _okn, 1)
        _orest = round(100 - sum(_osh(k) for k in _OBS), 1)
        _ostr = "".join(f'<tr><td>{html.escape(v)}</td><td>{_osh(k)}%</td><td>{_oc.get(k, 0):,}</td></tr>' for k, v in sorted(_OBS.items(), key=lambda kv: -_oc.get(kv[0], 0)))   # r174: largest first
        _ost.sort(key=lambda t: -t[1])
        _ostt = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td><td>{round(100 * c / kn, 1)}%</td><td>{kn:,}</td></tr>' for s, kn, c in _ost)
        _vk = ["openings_rule", "save_ways"]
        pg = HEAD.format(title="Flood vents: the federal openings rule and FEMA's records of proper openings on elevated buildings",
                         desc=f"What federal floodplain rules require of flood openings, and the share of {_okn:,} elevated single-family primary-home NFIP policies with an obstruction code that FEMA records with proper openings, as of {_ASOF_TXT}.",
                         canon=BASE + "/guides/flood-vents/") + f"""
<h1>Flood vents and flood openings</h1>
<p class="lede">{rule("openings_rule")}</p>
<div class="stats"><div class="stat"><div class="n">{_osh("15")}%</div><div class="l">Elevated single-family primary-home NFIP policies recorded with an enclosure or crawlspace with proper openings</div></div>
<div class="stat"><div class="n">{_okn:,}</div><div class="l">Elevated single-family primary-home policies with an obstruction code</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3 (obstructionType, elevatedBuildingIndicator), as of {_ASOF_TXT}: single-family primary-home policies FEMA marks as elevated buildings and gives an obstruction code; {_oc.get("blank", 0):,} more have no code and are left out.</p>
<div class="card"><h2>What is recorded under elevated buildings on NFIP policies?</h2><p class="stand">FEMA's obstruction code describes what is below the lowest elevated floor. Its five most common codes, in FEMA's words, shortened:</p>
<table><thead><tr><th>FEMA obstruction code</th><th>Share</th><th>Policies</th></tr></thead><tbody>{_ostr}<tr><td>Every other code</td><td>{_orest}%</td><td>{_okn - sum(_oc.get(k, 0) for k in _OBS):,}</td></tr></tbody></table>
<p class="mut">A code records how the policy was written, not an inspection today. "Not used for rating" is FEMA's own wording for this code.</p></div>
<div class="card"><h2>Proper openings, state by state</h2><p class="stand">Share of elevated single-family primary-home policies with an obstruction code that FEMA records as an enclosure or crawlspace with proper openings, in {len(_ost)} states with at least 100 such policies, most policies first.{(" Fewer than 100 such policies: " + ", ".join(html.escape(s["name"]) for s in states if s not in [t[0] for t in _ost]) + ".") if len(_ost) < len(states) else ""}</p>
<table><thead><tr><th>State</th><th>With proper openings</th><th>Elevated policies with a code</th></tr></thead><tbody>{_ostt}</tbody></table></div>
<div class="card"><h2>What FEMA lists as ways that may lower a bill</h2><p class="stand">{rule("save_ways")}</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">Whether a home's openings meet the rule (only an inspection, an engineer's certificate or an Elevation Certificate can say), what a given product costs, or how much any change would lower a premium. No product or company is named or recommended here.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 and its field definitions; rules from {_rule_hosts(_vk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "flood-vents", "index.html"), pg)
        zone_urls.append((BASE + "/guides/flood-vents/", None))
        GUIDES.append(("/guides/flood-vents/", "Flood vents and flood openings"))

if len(states) == 51:   # Risk Rating 2.0 guide (KWP 11-12 "risk rating 2.0" 100-1K): the figure FEMA's page, its fact sheet and USAFacts lack
    # (top-3 read 11-13) = today's share of policies still below FEMA's full-risk premium, by state, with the median gap. Base:
    # ffcalc.premium_gap on single-family primary-home policies with both premiums > 0, premium-only vs premium-only (agg.json)
    _rg = [(s, json.load(open(os.path.join(DATADIR, "states", s["slug"], "agg.json")))["policies"]) for s in states]
    _rgr = sorted(((s, x) for s, x in _rg if x.get("gap_basis") == "premium" and x.get("share_below") is not None
                   and (x.get("below_n") or 0) >= __import__("metrics").CONST["min_priced"]), key=lambda t: -t[1]["below_n"])
    _rpc, _rpn = _pwhole(_rgr, "share_below", "below_n")   # whole U.S. percent only when the state roundings cannot tip it
    if len(_rgr) >= 10 and _rpc is not None:
        _rk = ["rr2_start", "price_drivers", "glide", "cap"]
        _rtr = "".join(f'<tr><td><a href="/flood-insurance/{s["slug"]}/">{html.escape(s["name"])}</a></td><td>{x["share_below"]}%</td><td>{money(x.get("below_gap_median"))}</td><td>{x["below_n"]:,}</td></tr>' for s, x in _rgr)
        _rno = [s["name"] for s, x in _rg if (s, x) not in _rgr]
        pg = HEAD.format(title="Risk Rating 2.0: how many NFIP policies still pay below FEMA's full-risk premium, by state",
                         desc=f"What Risk Rating 2.0 is, the yearly cap on increases, and the share of {_rpn:,} NFIP single-family primary-home policies whose premium is below FEMA's full-risk premium, by state, from FEMA's records as of {_ASOF_TXT}.",
                         canon=BASE + "/guides/risk-rating-2/") + f"""
<h1>Risk Rating 2.0</h1>
<p class="lede">In FEMA's records, {_rpc}% of the {_rpn:,} U.S. single-family primary-home NFIP policies with both premiums recorded pay a premium below FEMA's full-risk premium on {_ASOF_TXT}. {rule("rr2_start")}</p>
<div class="stats"><div class="stat"><div class="n">{_rpc}%</div><div class="l">of {_rpn:,} U.S. NFIP single-family primary-home policies: premium below FEMA's full-risk premium</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3, as of {_ASOF_TXT}: single-family primary-home policies in force with a premium (totalInsurancePremiumOfThePolicy) and a full-risk premium (fullRiskPremium) both above $0. Both are premium only, before fees and surcharges.</p>
<div class="card"><h2>How fast can a bill below full risk rise?</h2><p class="stand">{rule("glide")}</p><p class="stand">{rule("cap")}</p></div>
<div class="card"><h2>What FEMA prices a policy on</h2><p class="stand">{rule("price_drivers")}</p></div>
<div class="card"><h2>Policies below full-risk premium, by state</h2><p class="stand">Share of single-family primary-home NFIP policies in force on {_ASOF_TXT} whose premium is below FEMA's full-risk premium, and the median gap per policy among those below, in {_nst(_rgr)} with at least {__import__("metrics").CONST["min_priced"]} such policies, most policies first.</p>
<table><thead><tr><th>State</th><th>Below full-risk premium</th><th>Median gap per policy below, premium only</th><th>Policies with both premiums</th></tr></thead><tbody>{_rtr}</tbody></table>
{f'<p class="mut">Too few such policies: {", ".join(html.escape(n) for n in _rno)}.</p>' if _rno else ""}
<p class="mut">The gap is FEMA's full-risk premium minus the premium charged, for each policy below full risk; a small median gap means most of those bills are close to full risk already. Each county page shows the county's share: <a href="/flood-insurance/">find your county</a>.</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">Your premium, your full-risk premium, when your bill will reach it, or why a price changed. FEMA's 2021 forecasts of who would pay more are not repeated here; these are the policies in force today.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3 (totalInsurancePremiumOfThePolicy, fullRiskPremium), as of {_ASOF_TXT}; rules from {_rule_hosts(_rk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "risk-rating-2", "index.html"), pg)
        zone_urls.append((BASE + "/guides/risk-rating-2/", None))
        GUIDES.append(("/guides/risk-rating-2/", "Risk Rating 2.0"))

_lmf = os.path.join(DATADIR, "us", "map_status.json")
_lms = json.load(open(_lmf)) if os.path.exists(_lmf) else {}
_lmp = [p for p in places if isinstance(_lms.get(p.get("geoid")), dict)]   # live county pages only (G3: "counties on this site", never U.S.)
_lml = [p for p in _lmp if _lms[p["geoid"]].get("loma") is not None]     # LL4: a county whose LOMA query failed is left out and counted
if len(_lml) >= 50:   # LOMA/LOMR guide (KWP 11-12 "loma flood zone" 100-1K, "lomr" 100-1K): top 3 (North Port, Key West, FEMA) print the process,
    # none prints what the rulings decided; FEMA's map service does (NFHL layer 34 OUTCOME, grouped by codes.loma_group as county pages do)
    from codes import loma_group as _lg
    _lgt = collections.Counter(); _lst = {}
    for p in _lml:
        for k, n in _lms[p["geoid"]]["loma"].items():
            _lgt[_lg(k)] += n; _lst.setdefault(p["state"], collections.Counter())[_lg(k)] += n
        _lst.setdefault(p["state"], collections.Counter())["_c"] += 1   # a county with zero rulings ({}) still counts (KeyError before 11-14)
    _ltot = sum(v for k, v in _lgt.items())
    _lrm, _lam, _lden, _loth = _lgt["bldg"] + _lgt["whole"] + _lgt["part"], _lgt["bldg_out"] + _lgt["out"], _lgt["denied"], _lgt["other"]
    _lpc = lambda n, t=None: f"{100 * n / (t or _ltot):.1f}%"
    _lrp = [p for p in _lmp if "lomr" in _lms[p["geoid"]]]; _lsince = {_lms[p["geoid"]].get("lomr_since") for p in _lrp}
    _lrn, _lrr = sum(_lms[p["geoid"]]["lomr"] for p in _lrp), sum(_lms[p["geoid"]]["lomr_recent"] for p in _lrp)
    _lret = _dtm.date.fromisoformat(_lms["_retrieved"]).strftime("%B %d, %Y").replace(" 0", " ") if _lms.get("_retrieved") else None
    _snm2 = {s.get("abbr"): s for s in states}
    _lrows = sorted(((ab, c) for ab, c in _lst.items() if ab in _snm2), key=lambda t: -sum(v for k, v in t[1].items() if k != "_c"))
    def _lrow(ab, c):
        t = sum(v for k, v in c.items() if k != "_c")
        return (f'<tr><td><a href="/flood-insurance/{_snm2[ab]["slug"]}/">{html.escape(_snm2[ab]["name"])}</a></td><td>{c["_c"]}</td><td>{t:,}</td>'
                f'<td>{_lpc(c["bldg"] + c["whole"] + c["part"], t) if t else "—"}</td><td>{_lpc(c["denied"], t) if t else "—"}</td></tr>')
    _lrt = "".join(f'<tr><td>{lab}</td><td>{_lpc(n)}</td><td>{n:,}</td></tr>' for lab, n in sorted([   # rank by value, never file order
        ("Building taken out (part of the lot still inside)", _lgt["bldg"]), ("Denied", _lden), ("Whole property taken out", _lgt["whole"]),
        ("Part of the property taken out", _lgt["part"]), ("Already outside the zone as mapped", _lam), ("Other, mixed or no outcome recorded", _loth)], key=lambda t: -t[1]))
    if _ltot and len(_lsince) <= 1 and None not in _lsince and _lret:   # LL6: one "since" date, or no LOMR counties and no LOMR sentence; LL10: retrieval date printed
        _lk = ["loma", "lomr_def", "lomr_f_def", "loma_fee", "lomr_fees", "loma_online", "zone_review", "ec_get", "prelim"]
        pg = HEAD.format(title="LOMA and LOMR: getting a home out of a FEMA flood zone, and what FEMA's rulings decided",
                         desc=f"What a Letter of Map Amendment (LOMA) and a Letter of Map Revision (LOMR) are, and how {_ltot:,} rulings in FEMA's LOMA map layer in {len(_lml)} of the {len(places)} counties on this site came out, from FEMA's map service.",
                         canon=BASE + "/guides/loma-lomr/") + f"""
<h1>LOMA and LOMR: getting a home out of a FEMA flood zone</h1>
<p class="lede">FEMA's map service lists {_ltot:,} rulings in its LOMA map layer for owners in {len(_lml)} of the {len(places)} counties on this site who asked FEMA to take a building or lot out of the high-risk flood zone: {_lpc(_lrm)} took the building or some or all of the lot out, {_lpc(_lden)} were denied. {rule("loma")}</p>
<div class="stats"><div class="stat"><div class="n">{_lpc(_lrm)}</div><div class="l">of {_ltot:,} rulings in FEMA's LOMA layer: building or some or all of the lot taken out of the high-risk zone</div></div>
<div class="stat"><div class="n">{_lpc(_lden)}</div><div class="l">of {_ltot:,} rulings in FEMA's LOMA layer: denied</div></div></div>
<p class="mut">FEMA National Flood Hazard Layer map service (LOMA layer, OUTCOME field), retrieved {_lret}: every ruling FEMA lists for the National Flood Insurance Program (NFIP) communities in {len(_lml)} of the {len(places)} counties on this site{f"; {len(_lmp) - len(_lml)} counties returned no LOMA list and are left out" if len(_lmp) > len(_lml) else ""}. These are rulings for owners who applied, not your home's odds, and FEMA's map service gives no dates for them.</p>
<div class="card"><h2>How did the rulings come out?</h2><p class="stand">Counted by FEMA's own outcome wording. "Removed" means taken out of the high-risk zone on the map, never torn down.</p>
<table><thead><tr><th>FEMA's ruling</th><th>Share</th><th>Rulings</th></tr></thead><tbody>
{_lrt}</tbody></table>
<p class="mut">"Already outside as mapped" means FEMA found the building or property was not in the high-risk zone on the map to begin with. "Other" holds FEMA's "Multiple" and "UNKNOWN", rulings with no outcome recorded, and rarer wordings.</p></div>
<div class="card"><h2>LOMA or LOMR: what is the difference?</h2><p class="stand">{rule("lomr_def")}</p><p class="stand">{rule("lomr_f_def")}</p><p class="stand">{rule("loma_fee")} {rule("lomr_fees")}</p>
{f'<p class="stand">FEMA has revised the countywide flood maps of {len(_lrp)} of the {len(places)} counties on this site with {_lrn:,} Letters of Map Revision, {_lrr:,} of them in effect since {_dtm.date.fromisoformat(next(iter(_lsince))).strftime("%B %d, %Y").replace(" 0", " ")}. Counties without a countywide digital map are not counted.</p>' if _lrp else ""}</div>
<div class="card"><h2>How to ask FEMA</h2><p class="stand">{rule("loma_online")} {rule("ec_get")} {rule("zone_review")}</p><p class="stand">{rule("prelim")}</p>
<p class="mut">To see the zone FEMA's map shows at an address: <a href="/flood-zone-map/">flood zone map</a>.</p></div>
<div class="card"><h2>Rulings in FEMA's LOMA layer, state by state</h2><p class="stand">Rulings for owners in the counties on this site, by state, most rulings first. Each state page lists its counties; each county page shows its own rulings.</p>
<table><thead><tr><th>State</th><th>Counties</th><th>Rulings</th><th>Taken out</th><th>Denied</th></tr></thead><tbody>{"".join(_lrow(ab, c) for ab, c in _lrows)}</tbody></table>
<p class="mut">Counted by the towns and areas FEMA lists in each county, so a city that reaches into a neighboring county counts in full in its own county.</p></div>
<div class="card"><h2>What this page cannot tell you</h2><p class="stand">Whether your home would get a LOMA, whether your lender will still require flood insurance after one, your premium, or rulings for counties not on this site.</p>
<p class="mut">Sources: FEMA National Flood Hazard Layer (map service), retrieved {_lret}; rules from {_rule_hosts(_lk)}. <a href="/methodology/">How we check them</a>.</p></div>{FOOT}"""
        wr(os.path.join(DIST, "guides", "loma-lomr", "index.html"), pg)
        zone_urls.append((BASE + "/guides/loma-lomr/", None))
        GUIDES.append(("/guides/loma-lomr/", "LOMA and LOMR: getting out of a flood zone"))

if GUIDES:   # /guides/: every guide that built this run, nothing typed by hand (11-13); home links it
    pg = HEAD.format(title="Flood insurance questions answered with FEMA's records", desc="Guides to common flood-insurance questions, each answered with FEMA's own rules and records.",
                     canon=BASE + "/guides/") + "<h1>Flood insurance questions, answered with FEMA's records</h1><div class=\"card\"><ul>" \
         + "".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for u, t in GUIDES) + f"</ul></div>{FOOT}"
    wr(os.path.join(DIST, "guides", "index.html"), pg)
    zone_urls.append((BASE + "/guides/", None))

# ---- /flood-insurance/renters/ (PAGE QUEUE row 6: "flood insurance for renters"). Base: NFIP policies in force marked tenant,
# residential occupancy, no building coverage, contents above $0; priced = policyCost above $0. claims_check.py --renters recomputes.
if RENT_ON:
    _rq = {k: _hq(_rh, k) for k in (0.25, 0.5, 0.75)}
    _rs = sorted(((st, sum(h.values()), _hq({st: h}, 0.5)) for st, h in _rh.items() if sum(h.values()) >= 30), key=lambda r: -r[1])
    _snm = {s["abbr"]: s for s in states} if states and "abbr" in states[0] else {}
    _rtr = "".join(f'<tr><td>{(f'<a href="/flood-insurance/{_snm[st]["slug"]}/">' + html.escape(_snm[st]["name"]) + "</a>") if st in _snm else st}</td><td>{money(md)}</td><td>{n:,}</td></tr>' for st, n, md in _rs)
    _rk = ["renters_cover", "wait_30", "how_to_buy", "not_covered", "flood_def", "nfip_not_sold", "tx_tenant_notice"]
    pg = HEAD.format(title=f"Flood insurance for renters: {money(_rq[0.5])}/yr NFIP median, by state",
                     desc=f"What renters pay for NFIP flood insurance on their belongings: a median of {money(_rq[0.5])} a year on {_rn:,} priced renter policies, by state, from FEMA's own records.",
                     canon=BASE + "/flood-insurance/renters/") + f"""
<h1>Flood insurance for renters</h1>
<p class="lede">Renters with an NFIP policy on their belongings paid a median of {money(_rq[0.5])} a year, premium plus fees, across {_rn:,} priced renter policies in force on {_ASOF_TXT}. The middle half paid {money(_rq[0.25])} to {money(_rq[0.75])}.</p>
<div class="stats"><div class="stat"><div class="n">{money(_rq[0.5])}</div><div class="l">Median / yr, NFIP renter policy</div></div>
<div class="stat"><div class="n">{money(_rq[0.25])}–{money(_rq[0.75])}</div><div class="l">Middle half / yr</div></div>
<div class="stat"><div class="n">{_rn:,}</div><div class="l">Priced renter policies</div></div></div>
<p class="mut">FEMA OpenFEMA NFIP Policies v3, as of {_ASOF_TXT}. Renter policy: FEMA marks the policyholder a tenant, the building residential, no building coverage and some contents coverage. Priced: a policy cost above $0. <a href="/methodology/">How we check them</a>.</p>
<div class="card"><h2>What does renters flood insurance cover?</h2><p class="stand">{rule("renters_cover")}</p><p class="stand">{rule("wait_30")}</p><p class="stand">{rule("how_to_buy")} {rule("nfip_not_sold")}</p><p class="stand"><b>What it won't pay:</b> {rule("not_covered")} {rule("flood_def")}</p><p class="stand">{rule("tx_tenant_notice")}</p></div>
<div class="card"><h2>What do renters pay in each state?</h2><p class="stand">States with at least 30 priced NFIP renter policies, most policies first.</p>
<table><thead><tr><th>State</th><th>Median / yr</th><th>Priced renter policies</th></tr></thead><tbody>{_rtr}</tbody></table>
<p class="mut">What homeowners pay: <a href="/nfip/">the NFIP in numbers</a>. <a href="/flood-insurance/zip/">Cost by ZIP code</a> (single-family homes).</p></div>
<div class="card"><h2>What these numbers cannot tell you</h2><p class="stand">Your premium, private insurers' prices, or why a price changed. The median is what existing NFIP renter policies pay, not a quote. Whether you are required to buy it is not in FEMA's data: only your lease or landlord can say.</p>
<p class="mut">Sources: FEMA OpenFEMA NFIP Policies v3; rules from {_rule_hosts(_rk)}.</p></div>{FOOT}"""
    wr(os.path.join(DIST, "flood-insurance", "renters", "index.html"), pg)
    zone_urls.append((BASE + "/flood-insurance/renters/", None))

# ---- /flood-insurance/<paper>/: national research papers (owner 11-12: national data, "PubMed worthy"; docs/PAPER-GATE-PROMPT.md).
# Every U.S. county in data/all-counties whose count base meets the minimum; share = num/den on one base with a 90% Wilson interval;
# fifths, never a bare rank (methods review 162). Sections in the gate's order; tools/paper_gate.py fails a page missing one.
import papers as _PA, statistics as _st
_recs = _PA.load() if _PA.READY else {}; _cn = _PA.names() if _PA.READY else {}; _live = {p.get("geoid"): p["slug"] for p in places}
_snames = {x.get("abbr"): x["name"] for x in states}
_FIFTH = {1: "Highest fifth", 2: "Second fifth", 3: "Middle fifth", 4: "Fourth fifth", 5: "Lowest fifth"}
# CSV columns: fifth, county_fips, county, state, share_pct, ci90_low_pct, ci90_high_pct, numerator, denominator (written below)
_LOOKJS = """<script>(function(){var s=document.getElementById('ps'),q=document.getElementById('pq'),o=document.getElementById('po'),R=null,
F=['','Highest fifth','Second fifth','Middle fifth','Fourth fifth','Lowest fifth'],MO=__MO__,MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
function mn(c){return c?c.split(';').map(function(m){return MN[+m.slice(-2)-1]+(m.length>2?' '+m.slice(0,4):'')}).join(' and '):''}
function p(l){var a=[],c='',Q=false;for(var i=0;i<l.length;i++){var h=l[i];if(h=='"')Q=!Q;else if(h==','&&!Q){a.push(c);c=''}else c+=h}a.push(c);return a}
function e(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function n(x){return Number(x).toLocaleString('en-US')}
function show(){if(!s.value){o.innerHTML='';return}var t=q.value.trim().toLowerCase(),h=R.filter(function(r){return r[3]==s.value&&(!t||r[2].toLowerCase().indexOf(t)>=0)});
o.innerHTML=h.length?'<div style="overflow-x:auto"><table><thead><tr><th>__FH__</th><th>County</th><th>Share</th><th>90% range</th><th>Count</th>'+(MO?'<th>Busiest month</th><th>One year over half of it</th>':'')+'</tr></thead><tbody>'+h.map(function(r){return '<tr><td>'+e(F[+r[0]]||'')+'</td><td>'+e(r[2])+'</td><td>'+e(r[4])+'%</td><td>'+e(r[5])+'\\u2013'+e(r[6])+'%</td><td>'+n(r[7])+' of '+n(r[8])+'</td>'+(MO?'<td>'+e(mn(r[11]))+'</td><td>'+e(mn(r[12]))+'</td>':'')+'</tr>'}).join('')+'</tbody></table></div>':'<p class="stand">No listed county in this state matches that name. Counties under the minimum are not listed.</p>'}
function go(){if(R)return show();fetch('__CSV__').then(function(x){if(!x.ok)throw 0;return x.text()}).then(function(x){R=x.trim().split(/\\r?\\n/).slice(1).map(p);show()}).catch(function(){o.innerHTML='<p class="stand">The lookup could not load; every county is in the table and the CSV below.</p>'})}
s.onchange=go;q.oninput=function(){if(s.value)go()}})();</script>"""
def _cty(x):
    nm = html.escape(f'{_cn.get(x["geoid"], x["geoid"])}, {x["state"]}')
    return f'<a href="/flood-insurance/{_live[x["geoid"]]}/">{nm}</a>' if x["geoid"] in _live else nm
def _vers(key):   # PAPER-GATE M2.5: the current as-of plus every earlier dated folder already in dist, newest first
    d = os.path.join(DIST, "flood-insurance", key)
    ds = sorted({x for x in (os.listdir(d) if os.path.isdir(d) else []) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)} | {_asof()}, reverse=True)
    fmt = lambda x: _dtm.date.fromisoformat(x).strftime("%B %d, %Y").replace(" 0", " ")
    return (f'Data as of {_ASOF_TXT} (current), kept at <a href="/flood-insurance/{key}/{_asof()}/">its own dated address</a> with its CSV. '
            + (f'Earlier versions, each kept at its own address: {", ".join(f"<a href={chr(34)}/flood-insurance/{key}/{x}/{chr(34)}>data as of {fmt(x)}</a>" for x in ds if x != _asof())}.' if len(ds) > 1 else "This is the first version.")
            + ' Each data refresh adds a new dated version; earlier versions are not changed.')
def _look(key, r, sp):   # rater Needs Met: a state + county filter on the paper's own CSV; owner 11-14 "read it like a human": on every paper, at the top
    sts = sorted({x["state"] for x in r}, key=lambda a: _snames.get(a, a))
    return (f'<form id="pl" onsubmit="return false"><label>State <select id="ps"><option value="">Select a state</option>'
            + "".join(f'<option value="{html.escape(a)}">{html.escape(_snames.get(a, a))}</option>' for a in sts)
            + f'</select></label> <label>County name <input id="pq" autocomplete="off"></label></form><div id="po" aria-live="polite"></div>'
            + f'<noscript><p class="stand">The state lookup needs JavaScript; every county is in {"the table and " if len(r) <= 500 else ""}the CSV below.</p></noscript>'
            + _LOOKJS.replace("__CSV__", f"/data/{key}.csv").replace("__FH__", "Fifth by excess over chance" if sp.get("null") else "Fifth by share").replace("__MO__", "true" if sp.get("months") else "false").replace("the table and the CSV below", "the table and the CSV below" if len(r) <= 500 else "the CSV below"))
def _gapli(r):   # Price Gap M2 sensitivity + M3 CRS split, pooled over the listed counties, every figure from the county files
    P = [(_recs[x["geoid"]].get("policies") or {}) for x in r]; n = sum(p["below_n"] for p in P)
    s = lambda f: round(100 * sum(p.get(f) or 0 for p in P) / n, 1)
    crs = collections.defaultdict(lambda: [0, 0])
    for x in r:
        for c, (a, b) in (((_recs[x["geoid"]].get("extras") or {}).get("policies") or {}).get("below_by_crs") or {}).items(): crs[c][0] += a; crs[c][1] += b
    cl = sorted(((c, v) for c, v in crs.items() if v[0] >= 1000), key=lambda cv: (cv[0] == "blank", int(cv[0]) if cv[0].isdigit() else 99))
    return (f'<li>The line moves the figure: pooled over the {len(r):,} counties, {s("below_k")}% of {n:,} {_sp["unit"]} are below full-risk by any amount, '
            f'{s("below10_k")}% by $10 or more and {s("below100_k")}% by ${_PA.GAP_MIN} or more.</li>'
            + ("" if not cl else f'<li>By the CRS class code FEMA records on the policy (classes with 1,000 or more policies here; descriptive, no test), the share below by any amount is '
            + "; ".join(f'{"no class code" if c == "blank" else "class " + c} {round(100 * v[1] / v[0], 1)}% of {v[0]:,}' for c, v in cl) + '.</li>'))   # bug review 11-14: no class with 1,000+ (old data) = no line, never "is ."
def _recon(sp):   # methods review 162 M9: one county set beside the prior work's own figure for it
    if not sp.get("reconcile"): return ""
    g, t = sp["reconcile"]; c = _PA.gap_ctx(_recs[g]); p = _recs[g]["policies"]
    return (f' {html.escape(_cn.get(g, g))}, {_recs[g].get("state", "")}: here {c["any_pct"]}% of {p["below_n"]:,} {sp["unit"]} are below full-risk by any amount and '
            f'{round(100 * p["below100_k"] / p["below_n"], 1)}% by ${_PA.GAP_MIN} or more, as of {_ASOF_TXT}; {html.escape(t)}.')
for _sp in _PA.READY:
    _r = _PA.rows(_sp, _recs)
    if len(_r) < 50: continue   # PLAN E9: no thin paper
    _nul, _small = _PA.skipped(_sp, _recs); _w0, _w1 = _PA.window(_sp, _recs)
    _key, _N = _sp["key"], len(_r)
    _lw = f"losses {_w0}–{_w1}" if _w0 else "policies in force"   # a policy snapshot (Deductible Choice) has no loss window
    _rk = f" for losses {_w0}–{_w1}" if _w0 else " in force on the data date"
    _K, _NN = sum(x["k"] for x in _r), sum(x["n"] for x in _r)
    _pool = round(100 * _K / _NN, 1); _plo, _phi = _PA.pooled_boot(_r)   # review outside-zone-2 M2: resample counties, not claims
    _xn, _xmed, _xpool = _PA.excluded(_sp, _recs)   # M3: the counties left out, shown beside the listed ones
    _ctx = {x["geoid"]: _PA.context(_sp, _recs[x["geoid"]], _w0, _w1) for x in _r}   # M1 policy share, M4 largest named flood
    _med = round(_st.median(x["value"] for x in _r), 1)
    _top, _bot = _r[0], _r[-1]
    _t50 = collections.Counter(x["state"] for x in _r[:50]).most_common(1)[0]
    _show = _r if _N <= 500 else _r[:100] + _r[-100:]   # PAPER-GATE M2.7: more than 500 rows = top and bottom 100 here, all in the CSV
    _pc = lambda c: f'<td>{c["pol_out"]}%</td>' if c["pol_out"] is not None else '<td>—</td>'
    _xc = lambda c: (f'<td>{money(c["excess"])}</td>' if c["excess"] is not None else '<td>—</td>') + f'<td>{c["one_year"] or ""}</td>'   # M1.4 size, M1.8 one-year flag
    _isn = bool(_sp.get("null"))   # Flood Calendar: rows carry the expected peak share at random and are ranked on the excess over it
    _mc = lambda x, c: (f'<td>{x["exp"]}%</td><td>{x["excess"]:+.1f}</td><td>{html.escape(_PA.month_words(c)[0])}</td>'
                        f'<td>{" and ".join(f"{y}%" for y in c["top_share"])}</td><td>{" and ".join(f"{y:,}" for y in c["years"])}</td>'
                        f'<td>{" and ".join(f"{y:,}" for y in c["years10"])}</td><td>{html.escape(_PA.month_words(c)[1])}</td>')
    _gc = lambda c: f'<td>{c["any_pct"]}%</td><td>{money(c["gap_med"]) if c["gap_med"] is not None else "—"}</td>'   # Price Gap M2: any-amount share, median gap
    _mflag = sum(1 for x in _r if _ctx[x["geoid"]].get("storm"))
    _trs = "".join(f'<tr><td>{_FIFTH[x["fifth"]]}</td><td>{_cty(x)}</td><td>{x["value"]}%</td><td>{x["lo"]}–{x["hi"]}%</td><td>{x["k"]:,} of {x["n"]:,}</td>'
                   + (_pc(_ctx[x["geoid"]]) if _sp.get("policy_col") else "") + (_xc(_ctx[x["geoid"]]) if _sp.get("excess") else "") + (_mc(x, _ctx[x["geoid"]]) if _sp.get("months") else "") + (_gc(_ctx[x["geoid"]]) if _sp.get("gap") else "") + '</tr>' for x in _show)
    _allp, _alln = _PA.all_pooled(_sp, _recs)   # M2: every county with one or more records, the figure set beside FEMA's
    _rcor = _PA.corr([(_ctx[x["geoid"]]["pol_out"], x["value"]) for x in _r]) if _sp.get("policy_col") else None
    _tk = "excess" if _isn else "value"
    _ties = lambda x: sum(1 for y in _r if y[_tk] == x[_tk])   # review 162 B1: a tied extreme is never one county
    if _isn:   # statistician + rater round 2: chance baseline beside every observed share; lead with the one-year finding
        _mtop = round(_st.median(_ctx[x["geoid"]]["top_share"][0] for x in _r), 1); _m10 = _st.median(_ctx[x["geoid"]]["years10"][0] for x in _r)   # review round 3: graded, not the flag alone
        _L = int(_w1) - int(_w0) + 1
        _mexp = round(_st.median(x["exp"] for x in _r), 1); _pexp = round(sum(x["n"] * x["exp"] for x in _r) / _NN, 1)
        _sup = lambda x: f'{_cty(x)}: {x["value"]}% against {x["exp"]}% expected at random ({x["k"]:,} of {x["n"]:,})'
        _nlede = (f"In FEMA's records for {_lw}, across the {_N:,} counties with at least {_sp['min']} {_sp['unit']} each, {_pool}% (90% range {_plo}–{_phi}%, resampling counties) "
                  f"of those claims {_sp['meets']}; had each county's claims fallen at random, each of the twelve months equally likely, {_pexp}% would be expected to; the largest of twelve months always holds at least a twelfth.")
        _nfind = (f'<p class="stand"><b>Main finding:</b> In {_mflag:,} of the {_N:,} counties the peak month has at least {_PA.ONE_YEAR_MIN} claims and one year holds over half of them. '
                  f"That mark does not say whether the month floods in other years. Graded instead, the median county's largest loss year holds {_mtop}% of its peak month "
                  f"(the earlier month where two tie), and that month has {_PA.ONE_YEAR_MIN} or more claims in {_m10:g} of the {_L:,} loss years at the median county.</p>")
        _nres = (f'<b>Result:</b> across those counties, {_pool}% (90% range {_plo}–{_phi}%, resampling counties) of {_sp["unit"]} {_sp["meets"]}, against {_pexp}% expected at random; '
                 f"the median county's share is {_med}%, against a median expected share at random of {_mexp}% (each county at its own claim count). Ranked by share minus that expectation, "
                 f'the largest excess is {_sup(_top)}{_tie(_top)}'
                 + (f'; its peak month is {_PA.month_words(_ctx[_top["geoid"]])[0]}, and over half of those claims are from {_PA.month_words(_ctx[_top["geoid"]])[1]} alone' if _ctx[_top["geoid"]]["storm"] else "")
                 + (f'; the smallest is {_sup(_bot)}.' if _ties(_bot) == 1 else f'; the smallest excess, {_bot["excess"]:+.1f} points, is shared by {_ties(_bot):,} counties.'))
        _nmeth = (f" The expected share at random is, for each county, the mean share of the largest month over {_PA.NULL_R:,} draws of the county's own number of claims "
                  "spread at random over twelve equally likely months (seeded by that number, so it reruns exactly); counties are ranked and put in fifths by share minus "
                  "that expectation, in percentage points, and an equal excess always gets the same fifth.")
        _nnote = ("Largest excess over chance first; counties with a page on this site are linked. The 90% ranges are narrower than they should be for two reasons: "
                  "the peak month is picked from the same claims it is measured on, and claims from one flood are not independent, most of all in the marked rows, where "
                  "one year holds over half of the peak month. Each range is the one that would hold if claims were independent.")
        _nli = (f'<li>Median county: {_med}%, against a median expected share at random of {_mexp}%. Largest excess over chance: {_cty(_top)}, {_top["value"]}% '
                f'(90% range if claims were independent {_top["lo"]}–{_top["hi"]}%) against {_top["exp"]}% expected at random{_tie(_top)}.</li>')
    _tie = lambda x: f", tied with {_ties(x) - 1:,} other count{'y' if _ties(x) == 2 else 'ies'}" if _ties(x) > 1 else ""
    with open(os.path.join(DIST, "data", f"{_key}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(_cols := ["fifth", "county_fips", "county", "state", "share_pct", "ci90_low_pct", "ci90_high_pct", "numerator", "denominator", "loss_years" if _w0 else "in_force_on", "as_of"]
                   + (["policy_units_outside_a_v_pct"] if _sp.get("policy_col") else []) + (["median_excess_usd", "loss_year_over_half"] if _sp.get("excess") else []) + (["peak_months", "year_month_over_half", "expected_share_at_random_pct", "excess_points", "peak_month_loss_years_any", "largest_year_share_of_peak_pct", "peak_month_loss_years_10plus"] if _sp.get("months") else [])
                   + (["below_any_amount_n", "below_any_amount_pct", "median_gap_usd_below_any_amount"] if _sp.get("gap") else []))
        for x in _r: w.writerow([x["fifth"], x["geoid"], _cn.get(x["geoid"], ""), x["state"], x["value"], x["lo"], x["hi"], x["k"], x["n"], f"{_w0}-{_w1}" if _w0 else _asof(), _asof()]
                                + ([_ctx[x["geoid"]]["pol_out"]] if _sp.get("policy_col") else [])
                                + ([_ctx[x["geoid"]]["excess"], _ctx[x["geoid"]]["one_year"] or ""] if _sp.get("excess") else [])
                                + ([";".join(_ctx[x["geoid"]]["peak"]), ";".join(_ctx[x["geoid"]]["storm"]), x["exp"], x["excess"], ";".join(map(str, _ctx[x["geoid"]]["years"])), ";".join(map(str, _ctx[x["geoid"]]["top_share"])), ";".join(map(str, _ctx[x["geoid"]]["years10"]))] if _sp.get("months") else [])
                                + ([_ctx[x["geoid"]]["any_k"], _ctx[x["geoid"]]["any_pct"], "" if _ctx[x["geoid"]]["gap_med"] is None else _ctx[x["geoid"]]["gap_med"]] if _sp.get("gap") else []))
    _glede = f"""In FEMA's records for {_lw}, {_allp}% of {_alln:,} {_sp["unit"]} across all U.S. counties combined {_sp["meets"]}; across the {_N:,} counties with at least {_sp["min"]} each, {_pool}% (90% range {_plo}–{_phi}%, resampling counties).{f" Across those counties, a county's claim share and its share of policy units outside zones A and V go together (correlation {_rcor:.2f}, descriptive, no test), so compare the two columns." if _rcor is not None else ""}""" if not _isn else ""
    _gres = f"""<b>Result:</b> across those counties, {_pool}% (90% range {_plo}–{_phi}%, resampling counties) of {_sp["unit"]} {_sp["meets"]}; the median county's share is {_med}%. The highest share is {_cty(_top)} at {_top["value"]}% ({_top["k"]:,} of {_top["n"]:,}){_tie(_top)}{f'; over half of those {_top["k"]:,} are from one loss year, {_ctx[_top["geoid"]]["one_year"]}, which may hold one flood or several ({sum(1 for x in _r if _ctx[x["geoid"]]["one_year"]):,} of the {_N:,} counties have at least 10 such claims and one year holding over half)' if _sp.get("excess") and _ctx[_top["geoid"]]["one_year"] else ""}; the lowest share, {_bot["value"]}%, {"is " + _cty(_bot) + f' ({_bot["k"]:,} of {_bot["n"]:,})' if _ties(_bot) == 1 else f"is shared by {_ties(_bot):,} counties"}.""" if not _isn else ""
    # owner 11-14 "read the papers like a real human": one short answer in plain words, every figure the same variable the lede and Results print
    _plain = lambda sp: {
        "damage-over-coverage": f"Of paid claims on NFIP (federal flood insurance) policies for single-family primary homes, with damage and coverage recorded ({_lw}), {_allp}% recorded more building damage than the policy's building coverage. In the median listed county it was {_med}%.",
        "outside-the-zone": f"{_allp}% of paid NFIP (federal flood insurance) claims with a rated zone ({_lw}) were on buildings rated outside FEMA's high-risk flood zones A and V; zone D, where FEMA has not determined the risk, counts as outside. In the median listed county it was {_med}%.",
        "deductible-choice": f"{_allp}% of NFIP (federal flood insurance) policies in force on {_ASOF_TXT} on single-family primary homes with a known building deductible have a building deductible of $5,000 or more on record. In the median listed county it is {_med}%.",
        "price-gap": f"Of NFIP (federal flood insurance) policies in force on {_ASOF_TXT} on single-family primary homes with both premiums recorded, {_allp}% pay a premium at least $100 a year below the full-risk premium FEMA records for the same policy. In the median listed county it is {_med}%. FEMA defines the full-risk premium as “The chargeable premium for a property based on its determined flood risk and the full cost to pay anticipated losses and expenses for that property.”",
        "flood-calendar": f"In {_mflag:,} of the {_N:,} listed counties, over half of the busiest month's NFIP claims ({_lw}) came in a single year. The busiest month is the month of the year with the most claims over {_w0}–{_w1}; this does not say whether it floods in other years. In the median listed county the busiest month held {_med}% of claims.",
    }.get(sp["key"]) or sys.exit(f"STOP: no plain-words answer for paper {sp['key']}")
    _cite = f'Michael Woo, Flood Insurance Data, "{_sp["title"]}," NFIP {_lw}, data as of {_ASOF_TXT}, {BASE}/flood-insurance/{_key}/'
    pg = HEAD.format(title=f'{_sp["title"]}: {_N:,} U.S. counties',
                     desc=f'The {_sp["measure"]}, {_lw}, in {_N:,} U.S. counties with at least {_sp["min"]} {_sp["unit"]}, from {_sp["dataset"]} as of {_ASOF_TXT}. Method, 90% ranges, limits and CSV.',
                     canon=f"{BASE}/flood-insurance/{_key}/") + f"""
<h1>{html.escape(_sp["title"])}</h1>
<div class="card" id="plain"><h2>In plain words</h2><p class="stand">{_plain(_sp)}</p><p class="stand"><b>Find your county</b> ({_N:,} listed; a county with fewer than {_sp["min"]} {_sp["unit"]} is not):</p>{_look(_key, _r, _sp)}</div>
<p class="lede">{_nlede if _isn else _glede}</p>
{"".join(f'<p class="stand">{rule(k)} (<a href="https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk" rel="nofollow">FloodSmart</a>.) {html.escape(_sp.get("prior_note") or "")}</p>' for k in _sp.get("prior_rules") or [])}
<p class="mut">By Michael Woo, publisher of Flood Insurance Data (<a href="/about/">about the site</a>), who works with data, is not an insurance agent, adjuster or engineer, and answers for every figure here. Written with AI tools; every row is recomputed from FEMA's records by a separate check before publishing.{f" First published {_sp['published']}; data as of {_ASOF_TXT}." if _sp.get("published") else ""}</p>
<div class="card" id="abstract"><h2>Abstract</h2>{_nfind if _isn else ""}
<p class="stand"><b>Data:</b> {_N:,} counties with at least {_sp["min"]} {_sp["unit"]} each ({_NN:,} in all), from {_sp["dataset"]}, {_lw}, as of {_ASOF_TXT}.</p>
<p class="stand">{_nres if _isn else _gres}</p></div>
<div class="card" id="question"><h2>Question</h2><p class="stand">{html.escape(_sp["question"])} The measure is the {html.escape(_sp["measure"])}.</p>{"".join(f'<p class="stand">{html.escape(d)}</p>' for d in _sp.get("why") or [])}{"".join(f'<p class="stand">{rule(k)}</p>' for k in _sp.get("why_rules") or [])}</div>
<div class="card" id="data"><h2>Data</h2><p class="stand">{_sp["dataset"]} (<a href="{_sp["api"]}" rel="nofollow">API</a>) records as of {_ASOF_TXT}, FEMA fields {html.escape(_sp["fields"])}. Base: {html.escape(_sp["base"])}.</p>
{"".join(f'<p class="stand">{html.escape(d)}</p>' for d in _sp["defs"])}{"".join(f'<p class="stand">{rule(k)}</p>' for k in _sp["rules"])}</div>
<div class="card" id="methods"><h2>Methods</h2><p class="stand">The share is the number of {_sp["unit"]} that {_sp["meets"]}, divided by all {_sp["unit"]} in the county FEMA codes on the record, both counted from the same records. A county is listed only with at least {_sp["min"]} {_sp["unit"]}. Left out: {_small:,} counties with fewer than {_sp["min"]} {_sp["unit"]} and {_nul:,} with none; across the {_xn:,} left-out counties with at least one, the median share of {_sp["short"]} is {_xmed}% and the pooled share {_xpool}%, so the listed counties are not a sample of every county.{_nmeth if _isn else ""} Intervals, fifths, the county-resampling range, records left out and why no test is run: <a href="/methodology/#papers">shared methods for every paper</a>.</p></div>
<div class="card" id="results"><h2>Results</h2><ul>
<li>Pooled over the {_N:,} counties: {_pool}% (90% range {_plo}–{_phi}%) of {_NN:,} {_sp["unit"]}{f", against {_pexp}% expected at random" if _isn else ""}; the {_xn:,} counties left out pool to {_xpool}%.</li>

{_gapli(_r) if _sp.get("gap") else ""}
{(lambda pc: f'<li>Peak month by county: {", ".join(f"{_PA.MONTHS[int(k) - 1]} in {v:,}" for k, v in pc.most_common(3))} of the {_N:,} counties (ties count each month); in {_mflag:,} of them over half of the peak month is one year.</li>')(collections.Counter(mo for x in _r for mo in _ctx[x["geoid"]]["peak"])) if _sp.get("months") else ""}
{_nli if _isn else f'<li>Median county: {_med}%. Highest: {_cty(_top)}, {_top["value"]}% (90% range {_top["lo"]}–{_top["hi"]}%){_tie(_top)}.</li>'}
<li>{_t50[1]} of the 50 counties with the {"largest excess over chance in" if _isn else "highest share of"} {html.escape(_sp["short"])} are in {html.escape(_snames.get(_t50[0], _t50[0]))}, which has {sum(1 for x in _r if x["state"] == _t50[0]):,} of the {_N:,} listed counties.</li></ul></div>
<div class="card" id="prior"><h2>Prior work</h2><p class="stand">{html.escape(_sp["prior"])} {"".join(f'<a href="{u}" rel="nofollow">{html.escape(t)}</a>. ' for t, u in _sp.get("prior_links") or [])}{"FEMA's own figure is set beside this one at the top of the page." if _sp.get("prior_rules") else ""}{_recon(_sp)}</p></div>
<div class="card" id="table"><h2>{"All " if _N <= 500 else "Top and bottom 100 of "}{_N:,} counties</h2><p class="stand">{_nnote if _isn else f'Highest share of {html.escape(_sp["short"])} first; counties with a page on this site are linked. '}{html.escape(_sp.get("policy_note") or "")}</p>
<div style="overflow-x:auto"><table><thead><tr><th>{"Fifth by excess over chance" if _isn else "Fifth by share"}</th><th>County</th><th>Share</th><th>{"90% range if claims were independent" if _isn else "90% range"}</th><th>Count</th>{f"<th>Policy units outside A and V (FEMA NFIP Policies, {_ASOF_TXT})</th>" if _sp.get("policy_col") else ""}{f"<th>Share below by any amount</th><th>Median yearly gap, policies below by any amount (only with {_PA.GAP_MED_MIN} or more)</th>" if _sp.get("gap") else ""}{"<th>Median amount damage was over coverage, on those claims</th><th>Loss year with over half of them (only with 10 or more)</th>" if _sp.get("excess") else ""}{f"<th>Expected share at random (twelve equal months, this county's claim count)</th><th>Excess over chance (points)</th><th>Peak month</th><th>Largest loss year's share of the peak month</th><th>Loss years with at least one claim in the peak month</th><th>Loss years with {_PA.ONE_YEAR_MIN} or more claims in the peak month</th><th>One year with over half of the peak month (only with {_PA.ONE_YEAR_MIN} or more)</th>" if _sp.get("months") else ""}</tr></thead><tbody>{_trs}</tbody></table></div>
<p class="mut"><a href="/data/{_key}.csv">Download all {_N:,} rows as CSV</a> ({len(_cols)} columns: {", ".join(_cols)}).{" " + html.escape(_sp["csv_note"]) if _sp.get("csv_note") else ""}</p></div>
<div class="card" id="limitations"><h2>Limitations</h2><ul>{"".join(f"<li>{html.escape(t)}</li>" for t in _sp["limits"])}<li>Only NFIP records: private flood insurance is not in FEMA's data.</li><li>A fifth is a position in this list, not a grade, a risk score or a prediction.</li></ul></div>
<div class="card" id="reproduce"><h2>Reproduce</h2><p class="stand">Download every record from <a href="{_sp["api"]}" rel="nofollow">{_sp["dataset"]}</a>, keep the {html.escape(_sp["unit"])}{_rk}, group by the county FEMA codes, count the base and the records meeting the measure, drop counties under {_sp["min"]}, and compute each share of {html.escape(_sp["short"])} with a 90% Wilson interval (z = 1.64485), checking against the CSV, which gives every numerator and denominator.{" Then compute each county's expected peak share at random as in Methods and rank on share minus it; the CSV gives both." if _isn else ""}</p></div>
<div class="card" id="cite"><h2>How to cite</h2><p class="stand">{html.escape(_cite)}. This product uses FEMA's OpenFEMA API, but is not endorsed by FEMA.</p></div>
<div class="card" id="versions"><h2>Versions</h2><p class="stand">{_vers(_key)}</p></div>
<div class="card" id="corrections"><h2>Corrections</h2>{"<ul>" + "".join(f"<li>{html.escape(d)}: {html.escape(t)}</li>" for d, t in _sp.get("corrections", [])) + "</ul>" if _sp.get("corrections") else ""}<p class="stand">{"" if _sp.get("corrections") else "No corrections so far. "}Report a figure that looks wrong to <a href="mailto:contact@floodinsurancedata.com">contact@floodinsurancedata.com</a>; every correction is listed here with its date.</p></div>{FOOT}"""
    pg = pg.replace('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8997828618122077" crossorigin="anonymous"></script>', "", 1)   # M3.4: no ads on papers (adsense_check)
    if not _sp.get("indexable"):   # PAPER-GATE M3.5 staged indexing: noindex and out of the sitemap until both reviews pass + 7 days live
        pg = pg.replace("<title>", '<meta name="robots" content="noindex,follow"><title>', 1)
    wr(os.path.join(DIST, "flood-insurance", _key, "index.html"), pg)
    # PAPER-GATE M2.5: the same page kept at /<key>/<as-of>/ with its own CSV, noindex (the current page is the indexed one);
    # earlier as-of folders are never touched, so every version stays at its address (build_all.py keeps paper folders)
    _vp = pg.replace(f'href="{BASE}/flood-insurance/{_key}/"', f'href="{BASE}/flood-insurance/{_key}/{_asof()}/"', 1).replace(f'href="/data/{_key}.csv"', f'href="/data/{_key}-{_asof()}.csv"').replace(f"fetch('/data/{_key}.csv')", f"fetch('/data/{_key}-{_asof()}.csv')")
    assert f"/data/{_key}.csv" not in _vp, f"{_key} dated copy still reads the current CSV"   # bug review 11-14: the lookup fetched it
    if "noindex" not in _vp: _vp = _vp.replace("<title>", '<meta name="robots" content="noindex,follow"><title>', 1)
    # a frozen copy must never call itself current once a newer refresh lands
    _vp = _vp.replace(f'<p class="stand">{_vers(_key)}</p>', f'<p class="stand">This is a fixed copy of the version with data as of {_ASOF_TXT}; it is not changed by later refreshes. <a href="/flood-insurance/{_key}/">The current version</a> has the latest data.</p>', 1)
    assert "(current)" not in _vp, f"{_key} dated copy still says current"
    _dcsv = os.path.join(DIST, "data", f"{_key}-{_asof()}.csv")   # bug review 11-14: "not changed by later refreshes" must hold, checked before the dated page is written
    if os.path.exists(_dcsv) and open(_dcsv, "rb").read() != open(os.path.join(DIST, "data", f"{_key}.csv"), "rb").read():
        sys.exit(f"STOP: {_key} figures changed inside as-of {_asof()}: the fixed copy would change; add a Corrections entry and delete {_dcsv} on purpose")
    wr(os.path.join(DIST, "flood-insurance", _key, _asof(), "index.html"), _vp)
    shutil.copyfile(os.path.join(DIST, "data", f"{_key}.csv"), _dcsv)
    if _sp.get("indexable"): zone_urls.append((f"{BASE}/flood-insurance/{_key}/", _asof()))   # M2.5: lastmod = as-of, never build day

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
for _f in ("favicon.ico", "favicon.svg"): shutil.copy(os.path.join(_ST, _f), os.path.join(DIST, _f))   # audit 11-10: /favicon.ico was a 404 on every page
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
<div class="card"><h2>If the zone looks wrong</h2><p class="stand">{rule("loma")} {rule("loma_fee")} {rule("loma_online")} {rule("zone_review")}</p>{'<p>How FEMA ruled on past requests: <a href="/guides/loma-lomr/">LOMA and LOMR rulings</a>.</p>' if any(u == "/guides/loma-lomr/" for u, _ in GUIDES) else ""}</div>
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
import lastmod as _LM   # audit 11-10: lastmod also moves on the day a page's visible text changed (tools/lastmod.py, vs the last release)
_lmroot = os.path.dirname(os.path.abspath(DIST)); _rels = {u: os.path.relpath(os.path.abspath(DIST), _lmroot).replace("\\", "/") + u[len(BASE):] + "index.html" for u, _ in urls}
_old, _olm, _today = _LM.head_files(_lmroot, list(_rels.values())), _LM.head_lastmods(_lmroot), _LM.today()
urls = [(u, _LM.pick(_old[_rels[u]], open(os.path.join(_lmroot, _rels[u]), encoding="utf-8").read(), _olm.get(u), lm, _today)) for u, lm in urls]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "".join(f"  <url><loc>{u}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>\n" for u, lm in urls) + \
     "</urlset>\n"
wr(os.path.join(DIST, "sitemap.xml"), sm)
from indexnow import KEY as _INKEY
wr(os.path.join(DIST, _INKEY + ".txt"), _INKEY)   # IndexNow key file (tools/indexnow.py)
wr(os.path.join(DIST, "ads.txt"), "google.com, pub-8997828618122077, DIRECT, f08c47fec0942fa0\n")   # owner applied to AdSense 11-12 (verification only; no ad units)
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
