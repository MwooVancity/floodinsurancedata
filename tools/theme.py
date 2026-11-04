"""The site's look (owner 2026-11-04: "more professional"), one layer shared by every page type.
Loaded after each template's base <style>, so it wins; the base rules stay for layout.
ponytail: an override layer, not a rewrite of the two base sheets; merge them when the base CSS next changes."""

THEME = """:root{--bg:#f6f7f9;--ink:#0f1b26;--mut:#3f4d58;--faint:#56636d;--line:#d9dee3;--brand:#0b4f8a;--brand-d:#0b2545;--accent:#0b4f8a;
 --serif:-apple-system,BlinkMacSystemFont,"Segoe UI Variable Text","Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
body{font:17px/1.6 var(--serif);-webkit-font-smoothing:auto}
.topbar{background:var(--brand-d);border-bottom:3px solid #1f7ac2}
.topbar .wrap{padding:14px var(--gut)}
.topbar .crumb{color:#c9d6e3;font-size:14px}
h1,h2,.hero h1,.card h2{font-weight:750;letter-spacing:-.02em;color:#0b1824}
h1,.hero h1{font-size:34px;line-height:1.15}
.kicker{font-family:var(--serif);font-size:13px;letter-spacing:.02em;text-transform:none;font-weight:600;color:var(--brand)}
.prov{border-left-color:#1f7ac2;background:#eef4fa;padding:8px 12px;border-radius:0 6px 6px 0}
.stats{gap:1px;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--line)}
.stat{border:0;border-radius:0;padding:14px 16px}
.stat .n{font-weight:750;font-size:28px;letter-spacing:-.02em;color:var(--brand-d)}
.stat .l,ul.kv b,thead th{font-size:13px;text-transform:none;letter-spacing:0;color:var(--faint);font-weight:600}
.card{border-radius:8px;padding:24px 26px;box-shadow:0 1px 2px rgba(15,27,38,.04)}
.card h2{font-size:23px;padding-bottom:10px;border-bottom:1px solid var(--line);margin-bottom:12px}
.src,footer,.mut{color:var(--faint);font-size:13px}
ul.kv li{background:#fff;border-radius:6px}
ul.kv > li > span{font-weight:750;color:var(--brand-d)}
ul.kv small.vs{color:var(--faint);font-size:13px}
table{font-size:15px}
thead th{background:#eef1f4;color:#33414c;padding:10px}
tbody tr:nth-child(odd){background:#fafbfc}
tbody td{border-top:1px solid #edf0f2}
.btn{background:var(--brand);border-radius:6px;box-shadow:none;font-weight:650}
.chip{background:#e7eef6;color:var(--brand-d);border-radius:4px;font-size:13px}
nav.jump a{border-radius:4px;color:var(--brand-d)}
nav.qa a{border:1px solid var(--line);background:#fff;border-radius:6px}
nav.sib{border-radius:8px}
.gap{border-radius:6px;font-size:14.5px}
input,select{font-family:var(--serif);border:1px solid #aab4bd;border-radius:6px;background:#fff;color:var(--ink);min-height:44px}
input[type=checkbox]{min-height:0;width:18px;height:18px}
input:focus,select:focus{outline:3px solid #9cc3e6;outline-offset:1px;border-color:var(--brand)}
button{font:600 16px var(--serif);background:var(--brand);color:#fff;border:0;border-radius:6px;padding:11px 18px}
@media(max-width:620px){h1,.hero h1{font-size:28px}.stat .n{font-size:24px}.card{padding:18px 16px}.card h2{font-size:20px}
.stat .l,ul.kv b,thead th{font-size:12.5px}table{font-size:14px}}"""
