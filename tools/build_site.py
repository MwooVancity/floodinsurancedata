"""Build the shared site pages from places.json: home+lookup, methodology, data (CSV),
sitemap.xml, robots.txt, llms.txt. Reads per-county agg.json for the download table.
Env: FF_PLACES (places.json), FF_DIST (dist dir), FF_DATADIR (per-county data root), FF_BASEURL."""
import csv, json, os, html

PLACES = os.environ.get("FF_PLACES", "places.json")
DIST = os.environ.get("FF_DIST", "dist")
DATADIR = os.environ.get("FF_DATADIR", "data")
BASE = os.environ.get("FF_BASEURL", "https://example.com").rstrip("/")
places = json.load(open(PLACES)) if os.path.exists(PLACES) else []
places.sort(key=lambda p: -(p.get("units") or 0))

def money(n): return "$" + format(int(round(n)), ",") if n is not None else "—"
def wr(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(s)

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<meta name="description" content="{desc}"><link rel="canonical" href="{canon}">
<style>:root{{--bg:#f4f6f8;--card:#fff;--ink:#16202b;--mut:#5a6672;--line:#d7dde3;--brand:#1f5c7a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:16px}}h1{{font-size:26px}}h2{{font-size:19px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:12px 0}}
a{{color:var(--brand)}}table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{text-align:left;padding:6px 4px;border-bottom:1px solid var(--line)}}th{{color:var(--mut)}}
input{{font-size:17px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;width:100%;max-width:360px}}
.mut{{color:var(--mut);font-size:13px}}</style></head><body><div class="wrap">"""
FOOT = ('<footer class="mut" style="margin:24px 0">This product uses FEMA\'s OpenFEMA API but is not '
        'endorsed by FEMA. Place names via GeoNames (CC BY 4.0). Aggregates only, never individual quotes.'
        ' <a href="/methodology/">Methodology</a> · <a href="/data/">Data</a></footer></div></body></html>')

# ---- home + client-side lookup ----
rows = "".join(f'<tr data-k="{html.escape((p["short"]+" "+(p.get("state") or "")).lower())}">'
               f'<td><a href="/flood-insurance/{p["slug"]}/">{html.escape(p["short"])}</a></td>'
               f'<td>{money(p.get("median"))}</td><td>{format(p.get("units") or 0, ",")}</td></tr>' for p in places)
home = HEAD.format(title="Flood insurance by place — real NFIP data",
    desc="What NFIP flood-insurance policyholders actually pay by county: cost spread, FEMA full-risk gap, claims, flood risk and CRS discounts. Federal data.",
    canon=BASE + "/") + f"""
<h1>Flood insurance, by the numbers</h1>
<p>For each place: what existing NFIP policyholders actually pay, how far below FEMA's full-risk price,
how often it floods, what claims paid out, and the community discounts that lower the bill. All from
public federal data, every figure sourced and dated.</p>
<div class="card"><h2>Find your place</h2>
<input id="s" placeholder="Type a county or state…" aria-label="Search places" autocomplete="off">
<table id="t" style="margin-top:12px"><thead><tr><th>County</th><th>Median annual cost</th><th>Policies in force</th></tr></thead>
<tbody>{rows or '<tr><td colspan=3 class=mut>No places published yet.</td></tr>'}</tbody></table></div>
<script>
var s=document.getElementById('s'),t=document.getElementById('t');
s.addEventListener('input',function(){{var q=s.value.toLowerCase();
 [].forEach.call(t.tBodies[0].rows,function(r){{r.style.display=(!q||(r.dataset.k||'').indexOf(q)>-1)?'':'none';}});}});
</script>{FOOT}"""
wr(os.path.join(DIST, "index.html"), home)

# ---- methodology ----
meth = HEAD.format(title="Methodology — flood insurance data", desc="Definitions, sources, dates, cohort rules and reconciliation for the flood-insurance data.", canon=BASE + "/methodology/") + f"""
<h1>Methodology</h1>
<div class="card"><h2>Sources</h2><ul>
<li>NFIP Redacted <b>Policies v3</b> and <b>Claims v3</b> — OpenFEMA API (keyless). Cost, full-risk premium, zones, claims.</li>
<li><b>Community Status Book v1</b> — OpenFEMA. CRS class and premium discount by community.</li>
<li><b>Disaster Declarations Summaries v2</b> — OpenFEMA. Federal flood/storm declarations.</li>
<li><b>Housing Assistance (Owners) v2</b> — OpenFEMA. FEMA aid paid to owners after disasters.</li>
<li><b>National Risk Index (counties)</b> — FEMA ArcGIS (FEMA_NationalRiskIndex). Flood expected annual loss + percentile.</li>
<li>Official <b>Policy Information by State and Community</b> workbook — reconciliation benchmark.</li></ul></div>
<div class="card"><h2>Definitions &amp; rules</h2><ul>
<li><b>Policy units</b> = sum of <code>policyCount</code>, never a row count — condo-association records carry more than one unit.</li>
<li><b>Cost cohort</b>: single-family primary-residence policies (occupancy 1/11, primary residence), annual cost = premium + fees.</li>
<li><b>Percentiles</b> p25/p50/p75/p90 by inclusive interpolation.</li>
<li><b>Full-risk gap</b>: share of cohort whose cost is below FEMA's full-risk premium.</li>
<li><b>Claims per 100</b>: cumulative paid claims since 1978 over current policy units — a historical tally, not an annual rate or a flood probability.</li>
<li><b>Suppression</b>: cost charts need ≥100 cohort policies; a ZIP page exists only if it passes the 3-part publish test (sufficiency, decision-relevant difference, distinct intent).</li>
<li><b>Dates</b>: each figure shows its effective date and retrieval date; policy snapshot differs from other datasets' retrieval dates.</li></ul></div>
<div class="card"><h2>What the data cannot tell you</h2><ul>
<li>Your own premium (depends on elevation, coverage, deductible).</li><li>Private (non-NFIP) prices.</li>
<li>Your address's exact flood zone — use FEMA's Flood Map Service Center.</li><li>Why premiums are rising.</li></ul></div>
{FOOT}"""
wr(os.path.join(DIST, "methodology", "index.html"), meth)

# ---- data download (CSV from per-county agg) ----
csv_path = os.path.join(DIST, "data", "counties.csv")
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["slug", "county", "geoid", "policy_units", "median_cost", "p25", "p75", "p90",
                "full_risk_median", "share_below_full_risk_pct", "claims_since_1978", "claims_paid_usd"])
    for p in places:
        ap = os.path.join(DATADIR, p["slug"], "agg.json")
        if not os.path.exists(ap): continue
        a = json.load(open(ap)); P = a["policies"]; C = a["claims"]
        w.writerow([p["slug"], p["short"], p.get("geoid"), P["units"], P["p50"], P["p25"], P["p75"], P["p90"],
                    P["frp_median"], P["share_below"], C["rows"], C["total_paid"]])
data = HEAD.format(title="Download the flood-insurance data", desc="Per-county NFIP flood-insurance aggregates as CSV.", canon=BASE + "/data/") + f"""
<h1>Download the data</h1>
<p>Per-county aggregates computed from FEMA OpenFEMA: policy units, cost spread, full-risk gap, and claims.</p>
<p><a href="/data/counties.csv">counties.csv</a> — {len(places)} places.</p>
<p class="mut">Reuse freely with attribution: "This product uses FEMA's OpenFEMA API, but is not endorsed by FEMA."</p>{FOOT}"""
wr(os.path.join(DIST, "data", "index.html"), data)

# ---- sitemap, robots, llms.txt ----
urls = [BASE + "/", BASE + "/methodology/", BASE + "/data/"] + [BASE + f"/flood-insurance/{p['slug']}/" for p in places]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
wr(os.path.join(DIST, "sitemap.xml"), sm)
wr(os.path.join(DIST, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
wr(os.path.join(DIST, "llms.txt"),
   "# Flood insurance data\n\n> Per-county NFIP flood-insurance statistics from public FEMA data: what "
   "policyholders pay, the gap to FEMA's full-risk price, claims history, flood risk, and CRS discounts.\n\n"
   "## Pages\n" + "".join(f"- [{p['short']}]({BASE}/flood-insurance/{p['slug']}/): median {money(p.get('median'))}\n" for p in places) +
   f"- [Methodology]({BASE}/methodology/)\n- [Data CSV]({BASE}/data/counties.csv)\n\n"
   "Source: FEMA OpenFEMA. Not endorsed by FEMA. Aggregates only.\n")

print(f"built site: {len(places)} places, home+methodology+data+sitemap+robots+llms into {DIST}")
