"""National ZIP lookup (/flood-insurance/zip/) ship standard: a Python oracle written from the data files, compared with the
page's own say() on EVERY ZIP in every dist/data/zip file; the form path for edge inputs (spaces, ZIP+4, 4 digits, letters,
00000, pasted text); fuzz (no NaN/undefined/null/Infinity); JS off = a link to the county pages.
Usage: python -I tools/test_ziptool.py [--browser chromium|webkit]"""
import functools, glob, http.server, json, os, random, re, sys, threading
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROWSER = sys.argv[sys.argv.index("--browser") + 1] if "--browser" in sys.argv else "chromium"
ZD = os.path.join(ROOT, "dist", "data", "zip")

def money(n): return "$" + format(int(n + 0.5), ",")
def oracle(z, d):
    rows = (d.get("z") or {}).get(z)
    if not rows: return [f"No NFIP policy in FEMA's records lists ZIP {z}."]
    out = [f"ZIP {z} appears on NFIP policies in {len(rows)} counties:"] if len(rows) > 1 else []
    for g, units, n, med in rows:
        name, st, p50, _ = d["c"].get(g, [g, "", None, None]); nm = name + (f", {st}" if st else "")
        if med is not None: out.append(f"{nm}: {units:,} policy units. Median {money(med)} a year ({n:,} priced single-family policies).")
        else: out.append(f"{nm}: {units:,} policy units. Too few priced single-family policies ({n:,}) for a ZIP median"
                         + (f"; the {name} median is {money(p50)} a year." if p50 is not None else "."))
    return out

def form_oracle(raw, files):
    z = re.sub(r"\s+", "", raw or "")[:5]
    if not re.fullmatch(r"\d{5}", z): return ["Enter a five-digit ZIP code."]
    return oracle(z, files.get(z[:3], {"z": {}}))

def main():
    files = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(os.path.join(ZD, "*.json"))}
    if not files: sys.exit("ZIP TOOL FAIL: no dist/data/zip files (flag 'zip' off?)")
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=os.path.join(ROOT, "dist")))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/flood-insurance/zip/"
    bad, n = [], 0
    with sync_playwright() as p:
        b = getattr(p, BROWSER).launch(); pg = b.new_page(); pg.goto(url)
        for k, d in files.items():   # every ZIP, the page's own function
            zs = sorted(d["z"]) + [k + "00", k + "99"]
            got = pg.evaluate("a => a[1].map(z => window.__zipSay(z, a[0]))", [d, zs])
            for z, g in zip(zs, got):
                n += 1
                if g != oracle(z, d): bad.append(f"{z}: page {g} != oracle {oracle(z, d)}")
                if any(re.search(r"NaN|undefined|null|Infinity", s) for s in g): bad.append(f"{z}: bad token {g}")
        r = random.Random(7)   # fuzz the form: edges + random strings
        edge = ["33480", " 33480 ", "33480-1234", "3348", "abcde", "00000", "", "33 480", "334801", "pasted: 33480", "99999", "1e300"]
        edge += ["".join(r.choice("0123456789 -abcZ") for _ in range(r.randint(0, 11))) for _ in range(40)]
        for raw in edge:
            pg.fill("#zi", raw); pg.click("#zf button"); pg.wait_for_function("!document.getElementById('zo').innerText.includes('Looking up')", timeout=10000)
            got = [x for x in pg.inner_text("#zo").split("\n") if x.strip()]
            if got != form_oracle(raw, files): bad.append(f"form {raw!r}: page {got} != oracle {form_oracle(raw, files)}")
        nj = b.new_context(java_script_enabled=False).new_page(); nj.goto(url)
        if "find your state and county" not in nj.inner_text("body").lower(): bad.append("JS off: no county fallback")
        b.close()
    srv.shutdown()
    for x in bad[:20]: print("  -", x)
    print(f"ZIP TOOL {'FAIL' if bad else 'PASS'} ({BROWSER}): {n:,} ZIPs vs oracle, {len(edge)} form inputs, JS off")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
