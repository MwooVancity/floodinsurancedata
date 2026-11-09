"""The site's look, one layer shared by every page type. Owner 2026-11-06: "like Forbes": modelled on Forbes Advisor's
article pages as seen 11-06 (black masthead with a centred serif wordmark, a deep-blue headline band with a large white
serif headline, serif lede, a pale blue "key takeaways" box with a blue left rule, hairline tables, squared blue buttons).
System fonts only (Georgia for serif): zero extra bytes. Small labels are dark and 14px (owner 11-06: "font blurry"
traced to thin grey 13px labels). AA contrast enforced by phone_check P7.
Loaded after each template's base <style>, so it wins; the base rules stay for layout.
ponytail: an override layer, not a rewrite of the two base sheets; merge them when the base CSS next changes."""

THEME = """:root{--bg:#fff;--surface:#fff;--ink:#111;--mut:#222;--faint:#3d3d3d;--line:#d9dce3;--brand:#1046b8;--brand-d:#0a2b8f;--accent:#1046b8;
 --head:Georgia,"Iowan Old Style","Palatino Linotype","Times New Roman",serif;
 --serif:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
body{background:#fff;color:var(--ink);font:17px/1.62 var(--serif)}
@media print{input,button,script,.topbar,#cf,#nomatch{display:none!important}h1,.hero .kicker{background:none!important;color:#000!important;box-shadow:none!important}a{color:#000}.card{break-inside:avoid-page}}
a{color:var(--brand);text-decoration-thickness:1px;text-underline-offset:2px}
.topbar{background:#000;border:0;box-shadow:none}
.topbar .wrap{padding:13px var(--gut);flex-wrap:wrap;justify-content:center;text-align:center}
.topbar a,.topbar a.brand,.topbar .brand{color:#fff;font:700 25px/1.1 var(--head);letter-spacing:-.01em;text-decoration:none}
.topbar .crumb,.topbar .crumb a{color:#c8c8c8!important;font:400 13px var(--serif);flex-basis:100%;margin-top:3px}
h1,.hero h1{position:relative;background:var(--brand-d);color:#fff;font:700 40px/1.12 var(--head);letter-spacing:-.01em;
 padding:26px 0 24px;margin:0 0 18px;box-shadow:0 0 0 100vmax var(--brand-d);clip-path:inset(0 -100vmax)}
.hero{padding-top:0;margin-top:0}.hero .kicker{background:var(--brand-d);color:#d5ddf5;margin:0;padding:16px 0 0;box-shadow:0 0 0 100vmax var(--brand-d);clip-path:inset(0 -100vmax)}.hero .kicker+h1{padding-top:6px}main.wrap>h1:first-child{margin-top:0}
h2,h3,.card h2{font-family:var(--head);font-weight:700;letter-spacing:-.005em;color:#111}
.lede,.hero .lede{font-family:var(--head);font-size:19px;line-height:1.5;color:#111}
.kicker{font:700 12px var(--serif);letter-spacing:.1em;text-transform:uppercase;color:#111}
.prov{border-left:4px solid var(--brand);background:#eef1fb;padding:10px 14px;border-radius:0}
.stats{gap:0;border:0;border-top:2px solid #111;border-bottom:1px solid #111;border-radius:0;background:none}
.stat{border:0;border-radius:0;padding:14px 12px 12px 0;background:none}
.stat:nth-child(even){padding-left:14px;border-left:1px solid var(--line)}.stat:nth-child(n+3){border-top:1px solid var(--line)}
.stat .n{font:700 34px/1.1 var(--head);color:#111;font-variant-numeric:tabular-nums lining-nums}
.stat .l,ul.kv b,thead th{font-size:14px;text-transform:none;letter-spacing:0;color:#222;font-weight:500}
.card{background:none;border:0;border-top:1px solid #111;border-radius:0;padding:22px 0 8px;box-shadow:none}
.card h2{font-size:26px;line-height:1.2;padding-bottom:0;border-bottom:0;margin:0 0 10px}
.src,footer,.mut{color:#3d3d3d;font-size:14px}
nav.qa{background:#eef1fb;border:0;border-left:4px solid var(--brand);border-radius:0;padding:6px 14px}
nav.qa a{border:0;border-bottom:1px solid #d3d9ef;background:none;border-radius:0;color:#111;padding:8px 0}
nav.qa a:last-child{border-bottom:0}nav.qa a b{color:var(--brand-d);font-family:var(--head)}
ul.kv li{background:none;border:0;border-top:1px solid var(--line);border-radius:0}
ul.kv > li > span{font:700 22px var(--head);color:#111}
ul.kv small.vs{color:#3d3d3d;font-size:14px}
table{font-size:15px;font-variant-numeric:tabular-nums;border-collapse:collapse}
thead th{background:#f2f4f9;color:#111;padding:9px 10px;border-bottom:2px solid #111;text-align:left;font-weight:700}
tbody tr:nth-child(odd){background:none}
tbody td{border-top:1px solid #e3e5ea}
.btn,button{background:var(--brand-d);color:#fff;border:0;border-radius:3px;box-shadow:none;font:600 16px var(--serif);padding:12px 18px}
.btn:hover,button:hover{background:var(--brand);filter:none}
.chip{background:#eef1fb;border:0;color:#0a2b8f;border-radius:3px;font-size:13px}
nav.jump a{border-radius:0;color:#111}
nav.sib{border-radius:0;background:none;border-top:1px solid #111}
.gap{border-radius:0;font-size:14.5px;border-left:4px solid #111;background:#f4f4f4}
input,select{font-family:var(--serif);border:1px solid #6b7280;border-radius:3px;background:#fff;color:var(--ink);min-height:44px}
input[type=checkbox]{min-height:0;width:18px;height:18px}
input:focus,select:focus{outline:3px solid #9cb8f0;outline-offset:1px}
@media(max-width:620px){h1,.hero h1{font-size:26px;line-height:1.15;padding:14px 0 13px;margin-bottom:10px}.stat .n{font-size:24px}
.stat{padding:10px 10px 8px 0}.stat:nth-child(even){padding-left:10px}.card{padding:15px 0 4px}.card h2{font-size:21px;margin-bottom:8px}
.lede,.hero .lede{font-size:16.5px;line-height:1.42}.topbar .wrap{padding:10px var(--gut)}.topbar a.brand,.topbar .brand{font-size:21px}
.stat .l,ul.kv b,thead th{font-size:13px;line-height:1.35}table{font-size:14px}}"""
