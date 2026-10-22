"""Build the Lee County FL flood page from data.json (small datasets) + agg.json (bulk).
River-style: white cards, every number has a unit, one line of context, source + as-of once.
No verdict, no advice prose. Self-contained static HTML -> lee.html."""
import json, html
from collections import defaultdict

data = json.load(open("data.json"))
agg = json.load(open("agg.json"))
P = agg["policies"]; C = agg["claims"]; NRI = agg.get("nri")
ASOF = "July 31, 2026"
SRC = ("Source: FEMA OpenFEMA NFIP Redacted Policies v3 and Claims v3; this product uses the "
       "Federal Emergency Management Agency's OpenFEMA API, but is not endorsed by FEMA.")

def money(n):
    return "$" + format(int(round(n)), ",") if n is not None else "—"
def num(n):
    return format(int(n), ",") if n is not None else "—"

# ---- housing assistance: aggregate Lee rows ----
h_rows = data.get("housing", [])
h_regs = sum(int(r.get("validRegistrations") or 0) for r in h_rows)
h_ihp = sum(float(r.get("totalApprovedIhpAmount") or 0) for r in h_rows)
h_disasters = len(set(r.get("disasterNumber") for r in h_rows))

# ---- declarations: flood/hurricane, recent ----
decl = data.get("declarations", [])
fh = [d for d in decl if d.get("incidentType") in ("Flood", "Hurricane", "Severe Storm", "Coastal Storm")]
fh_years = sorted({d.get("fyDeclared") for d in fh if d.get("fyDeclared")}, reverse=True)
recent = []
seen = set()
for d in sorted(fh, key=lambda x: x.get("declarationDate") or "", reverse=True):
    k = (d.get("fyDeclared"), d.get("incidentType"), d.get("declarationTitle"))
    if k in seen: continue
    seen.add(k); recent.append(d)
    if len(recent) >= 6: break

# ---- CRS discounts ----
crs = sorted(data.get("crs", []), key=lambda x: -(int(x.get("sfhaDiscount", "0%").rstrip("%") or 0)))

# ---- claims by year chart ----
by = C["by_year"]  # {year:[count,paid]}
years = sorted(int(y) for y in by)
maxc = max((by[str(y)][0] for y in years), default=1)
top_paid = sorted(((y, by[str(y)][1]) for y in years), key=lambda x: -x[1])[:3]

def claims_svg():
    if not years: return "<p>No claims recorded.</p>"
    y0, y1 = years[0], years[-1]
    W, H, pad = 680, 220, 28
    span = max(1, y1 - y0)
    bars = []
    for y in years:
        c = by[str(y)][0]
        x = pad + (y - y0) / span * (W - 2 * pad)
        bh = (c / maxc) * (H - 2 * pad)
        top = any(y == ty for ty, _ in top_paid)
        col = "var(--accent)" if top else "var(--bar)"
        bars.append(f'<rect x="{x:.1f}" y="{H-pad-bh:.1f}" width="3.2" height="{bh:.1f}" fill="{col}"><title>{y}: {num(c)} claims, {money(by[str(y)][1])}</title></rect>')
    labs = "".join(f'<text x="{pad+(y-y0)/span*(W-2*pad):.1f}" y="{H-8}" class="ax">{y}</text>'
                   for y in range(((y0+9)//10)*10, y1+1, 10))
    return (f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="NFIP claims per year">'
            f'{"".join(bars)}<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="var(--line)"/>{labs}</svg>')

# ---- cost spread chart (p25..p90 range bar) ----
def spread_svg():
    p25, p50, p75, p90 = P["p25"], P["p50"], P["p75"], P["p90"]
    frp = P["frp_median"]
    if not p50: return ""
    hi = max(p90 or 0, frp or 0) * 1.1
    W, H, pad = 680, 120, 40
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

def card(title, standfirst, body, source=None):
    s = f'<p class="src">{html.escape(source)}</p>' if source else ""
    return f'<section class="card"><h2>{title}</h2><p class="stand">{standfirst}</p>{body}{s}</section>'

# ---- risk card (NRI or gap) ----
if NRI:
    cr = NRI.get("Coastal_Flooding___Expected_Annual_Loss_Rate___National_Percentile___Composite") or NRI.get("Coastal_Flooding___Expected_Annual_Loss_Rating")
    risk_body = "<ul class='kv'>" + "".join(
        f"<li><b>{html.escape(k.replace('___',' – ').replace('_',' '))}</b><span>{html.escape(str(v))}</span></li>"
        for k, v in list(NRI.items())[:8]) + "</ul>"
    risk = card("How much flood risk is here?", "FEMA's National Risk Index rates this county's flood risk below.", risk_body,
                "Source: FEMA National Risk Index (counties), accessed 2026-10-22.")
else:
    risk = card("How much flood risk is here?",
                "Not available at this place yet — the FEMA National Risk Index county query is being finalized.",
                "<p class='gap'>Gap line: NRI flood expected-annual-loss and national percentile for Lee County. Public data to pull next: NRI_Counties_EAL FeatureServer, field State_County_FIPS_Code.</p>")

sfha = round(sum(v for z, v in P["zones"].items() if z and z[0] in "AV") / max(1, P["rows"]) * 100, 1)
zone_body = "<ul class='kv'>" + "".join(f"<li><b>Zone {html.escape(z)}</b><span>{num(v)} policies</span></li>" for z, v in list(P["zones"].items())[:8]) + "</ul>"

cost_lead = (f"Single-family homeowners in Lee County pay a median {money(P['p50'])} a year for NFIP flood "
             f"insurance, with the middle half between {money(P['p25'])} and {money(P['p75'])} "
             f"(from {num(P['cost_n'])} policies).")
gap_lead = (f"{P['share_below']}% of {num(P['below_n'])} single-family policies pay less than FEMA's own "
            f"full-risk price; the median full-risk premium is {money(P['frp_median'])} versus the "
            f"{money(P['p50'])} actually charged.")
claims_lead = (f"Since 1978, Lee County has had {num(C['rows'])} paid NFIP flood claims totalling "
               f"{money(C['total_paid'])} — about {C['claims_per_100_policies']} claims for every 100 policies in force.")

crs_rows = "".join(f"<tr><td>{html.escape(c['communityName'].title())}</td><td>Class {c.get('classRating','—')}</td>"
                   f"<td>{c.get('sfhaDiscount','—')}</td><td>{c.get('nonSfhaDiscount','—')}</td></tr>" for c in crs)
crs_lead = (f"Most of Lee County's flood-insurance customers already get a discount for community flood work: "
            f"Cape Coral, Sanibel and Lee County itself cut premiums 25% inside the high-risk zone.")

recent_li = "".join(f"<li>{html.escape(str(d.get('fyDeclared')))} — {html.escape(d.get('incidentType',''))}: {html.escape((d.get('declarationTitle') or '').title())}</li>" for d in recent)

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flood insurance in Lee County, Florida — the data</title>
<style>
:root{{--bg:#f4f6f8;--card:#fff;--ink:#16202b;--mut:#5a6672;--line:#d7dde3;--bar:#9db4c6;--accent:#b4531f;--brand:#1f5c7a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:16px}}
header h1{{font-size:26px;margin:.2em 0}}
.chip{{display:inline-block;background:#e7edf2;color:var(--mut);border-radius:20px;padding:3px 11px;font-size:13px;margin-right:6px}}
.answer{{background:var(--brand);color:#fff;border-radius:12px;padding:16px 18px;font-size:18px;margin:14px 0}}
.answer b{{font-size:22px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:12px 0}}
.card h2{{font-size:18px;margin:0 0 6px}}
.stand{{color:var(--ink);margin:0 0 12px}}
.src{{color:var(--mut);font-size:12px;margin:10px 0 0}}
.gap{{color:var(--accent);font-size:14px}}
ul.kv{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:6px 18px}}
ul.kv li{{display:flex;justify-content:space-between;border-bottom:1px dotted var(--line);padding:4px 0;font-size:14px}}
ul.kv b{{font-weight:600}}ul.kv span{{color:var(--mut)}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{text-align:left;padding:6px 4px;border-bottom:1px solid var(--line)}}th{{color:var(--mut);font-weight:600}}
.ax{{fill:var(--mut);font-size:10px;text-anchor:middle}}.ax2{{fill:var(--mut);font-size:9px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media(max-width:560px){{.two{{grid-template-columns:1fr}}ul.kv{{grid-template-columns:1fr}}}}
.note{{color:var(--mut);font-size:13px}}
footer{{color:var(--mut);font-size:12px;margin:24px 0}}
</style></head><body><div class="wrap">
<header>
<span class="chip">Data as of {ASOF}</span><span class="chip">{num(P['units'])} policies in force</span>
<h1>Flood insurance in Lee County, Florida</h1>
</header>

<div class="answer">Single-family homeowners here pay a median <b>{money(P['p50'])}</b> a year.
Middle half {money(P['p25'])}–{money(P['p75'])}. {P['share_below']}% pay less than FEMA's full-risk price.</div>

{risk}

{card("Am I required to carry it?",
  f"About {sfha}% of Lee County policies sit in a high-risk Special Flood Hazard Area (zones A/V), where a federally backed mortgage legally requires flood insurance.",
  f"<div class='two'><div>{zone_body}</div><div><p class='note'>Federal rule: lenders must require flood insurance on a building in a Special Flood Hazard Area with a federally backed loan (42 U.S.C. §4012a). Zone from each policy's rated flood zone.</p></div></div>",
  SRC)}

{card("How much does it cost here?", cost_lead, spread_svg() +
  "<p class='note'>Each policy's annual premium cost, single-family primary residences. The bar is the middle half (p25–p75); the orange line is FEMA's full-risk price for comparison.</p>", SRC)}

{card("How far below the true price is it?", gap_lead,
  f"<ul class='kv'><li><b>Median charged now</b><span>{money(P['p50'])}</span></li>"
  f"<li><b>Median full-risk price</b><span>{money(P['frp_median'])}</span></li>"
  f"<li><b>Pay below full risk</b><span>{P['share_below']}% of {num(P['below_n'])}</span></li></ul>", SRC)}

{card("What do floods actually pay out here?", claims_lead, claims_svg() +
  f"<p class='note'>Orange bars are the three costliest years: " +
  ", ".join(f"{y} ({money(p)})" for y,p in top_paid) + ". Net building + contents payments, by year of loss.</p>", SRC)}

{card("How often is this county a flood disaster?",
  f"Lee County has had {len(fh)} federal flood, hurricane or storm disaster declarations. The most recent:",
  f"<ul>{recent_li}</ul>", "Source: FEMA OpenFEMA DisasterDeclarationsSummaries v2, accessed 2026-10-22.")}

{card("Did the government pay homeowners after floods?",
  f"FEMA approved {money(h_ihp)} in Individual &amp; Households housing help to Lee County homeowners across {h_disasters} disasters, on {num(h_regs)} valid registrations.",
  "<p class='note'>FEMA Individual Assistance is separate from NFIP insurance — it is disaster aid, usually capped and partial, not a substitute for a policy.</p>",
  "Source: FEMA OpenFEMA HousingAssistanceOwners v2, accessed 2026-10-22.")}

{card("Can I pay less than the sticker price?", crs_lead,
  f"<table><thead><tr><th>Community</th><th>CRS class</th><th>High-risk discount</th><th>Other-area discount</th></tr></thead><tbody>{crs_rows}</tbody></table>"
  "<p class='note'>The Community Rating System cuts NFIP premiums for every policy in a community that does extra flood work. Ask your agent to confirm the discount is applied.</p>",
  "Source: FEMA OpenFEMA NFIP Community Status Book v1, accessed 2026-10-22.")}

{card("Reconciliation", "Our count is checked against FEMA's official figure.",
  f"<p class='note'>This page's in-force count for Lee County is {num(P['units'])} policy units (from {num(P['rows'])} API records; condo-association records carry more than one unit). FEMA's official Policy Information by State and Community count for 2026-07-31 was 132,012 — a difference of {round(abs(P['units']-132012)/132012*100,1)}%.</p>")}

<section class="card"><h2>What this data cannot tell you</h2>
<ul class="note">
<li>Your own premium — it depends on elevation, coverage and deductible. We show where real policies fall.</li>
<li>Private (non-NFIP) flood insurance prices.</li>
<li>Your address's exact flood zone — use FEMA's Flood Map Service Center.</li>
<li>Why premiums are rising — we show the gap to full-risk, not the cause.</li>
</ul></section>

<footer>{SRC} Place names via GeoNames (CC BY 4.0). Figures are aggregates, not individual quotes.</footer>
</div></body></html>"""

open("lee.html", "w", encoding="utf-8").write(HTML)
print("wrote lee.html", len(HTML), "bytes; NRI:", "yes" if NRI else "GAP")
