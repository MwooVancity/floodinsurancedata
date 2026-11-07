"""The site's look, one layer shared by every page type. Owner 2026-11-06: "redesign like Forbes or WSJ":
newspaper style. White page, near-black ink, system serif headlines and figures (no web font: zero extra bytes),
thin black rules instead of boxes and shadows, a masthead with a double rule, hairline tables.
Loaded after each template's base <style>, so it wins; the base rules stay for layout. AA contrast is enforced by
phone_check P7. ponytail: an override layer, not a rewrite of the two base sheets; merge them when the base CSS next changes."""

THEME = """:root{--bg:#fff;--surface:#fff;--ink:#111;--mut:#333;--faint:#555;--line:#d6d6d6;--brand:#0b4a8b;--brand-d:#111;--accent:#0b4a8b;
 --head:Georgia,"Iowan Old Style","Palatino Linotype","Times New Roman",serif;
 --serif:-apple-system,BlinkMacSystemFont,"Segoe UI Variable Text","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
body{background:#fff;color:var(--ink);font:17px/1.62 var(--serif);-webkit-font-smoothing:auto}
a{color:var(--brand);text-decoration-thickness:1px;text-underline-offset:2px}
.topbar{background:#fff;border-bottom:4px double #111;box-shadow:none}
.topbar .wrap{padding:16px var(--gut) 12px}
.topbar a,.topbar a.brand,.topbar .brand{color:#111;font:700 24px/1.1 var(--head);letter-spacing:-.01em;text-decoration:none}
.topbar .crumb,.topbar .crumb a{color:#444!important;font:400 13px var(--serif)}
h1,h2,h3,.hero h1,.card h2{font-family:var(--head);font-weight:700;letter-spacing:-.01em;color:#111}
h1,.hero h1{font-size:38px;line-height:1.12}
.lede{font-family:var(--head);font-size:20px;line-height:1.5;color:#222}
.kicker{font:700 12px var(--serif);letter-spacing:.12em;text-transform:uppercase;color:#111}
.prov{border-left:3px solid #111;background:#f5f5f5;padding:8px 12px;border-radius:0}
.stats{gap:0;border:0;border-top:2px solid #111;border-bottom:1px solid #111;border-radius:0;background:none}
.stat{border:0;border-radius:0;padding:14px 12px 12px 0;background:none}
.stat:nth-child(even){padding-left:14px;border-left:1px solid var(--line)}.stat:nth-child(n+3){border-top:1px solid var(--line)}
.stat .n{font:700 34px/1.1 var(--head);letter-spacing:-.01em;color:#111;font-variant-numeric:tabular-nums lining-nums}
.stat .l,ul.kv b,thead th{font-size:13px;text-transform:none;letter-spacing:0;color:#444;font-weight:600}
.card{background:none;border:0;border-top:1px solid #111;border-radius:0;padding:22px 0 8px;box-shadow:none}
.card h2{font-size:26px;line-height:1.2;padding-bottom:0;border-bottom:0;margin:0 0 10px}
.src,footer,.mut{color:#555;font-size:13px}
footer{border-top:4px double #111}
ul.kv li{background:none;border:0;border-top:1px solid var(--line);border-radius:0}
ul.kv > li > span{font:700 22px var(--head);color:#111}
ul.kv small.vs{color:#555;font-size:13px}
table{font-size:15px;font-variant-numeric:tabular-nums;border-collapse:collapse}
thead th{background:none;color:#111;padding:8px 10px;border-bottom:2px solid #111;text-align:left}
tbody tr:nth-child(odd){background:none}
tbody td{border-top:1px solid #e3e3e3}
.btn,button{background:#111;color:#fff;border:0;border-radius:2px;box-shadow:none;font:600 16px var(--serif);padding:12px 18px}
.btn:hover,button:hover{background:#0b4a8b;filter:none}
.chip{background:none;border:1px solid #111;color:#111;border-radius:2px;font-size:13px}
nav.jump a{border-radius:0;color:#111;border-bottom:1px solid #111}
nav.qa a{border:1px solid #111;background:#fff;border-radius:2px}
nav.sib{border-radius:0;background:none;border-top:1px solid #111}
.gap{border-radius:0;font-size:14.5px;border-left:3px solid #111;background:#f5f5f5}
input,select{font-family:var(--serif);border:1px solid #111;border-radius:2px;background:#fff;color:var(--ink);min-height:44px}
input[type=checkbox]{min-height:0;width:18px;height:18px}
input:focus,select:focus{outline:3px solid #9cc3e6;outline-offset:1px}
@media(max-width:620px){h1,.hero h1{font-size:26px;line-height:1.14}.stat .n{font-size:24px}.stat{padding:10px 10px 8px 0}.stat:nth-child(even){padding-left:10px}.topbar .wrap{flex-wrap:wrap}.topbar .crumb{flex-basis:100%;margin:4px 0 0}.card{padding:15px 0 4px}.card h2{font-size:21px;margin-bottom:8px}.lede{font-size:16.5px;line-height:1.42}.topbar .wrap{padding:12px var(--gut) 9px}
.topbar a.brand,.topbar .brand{font-size:21px}.stat .l,ul.kv b,thead th{font-size:12.5px}table{font-size:14px}}"""
