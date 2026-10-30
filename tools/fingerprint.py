"""Build only what changed (PLAN scale guard; owner 2026-10-29: "daily full rebuild is not acceptable").
A page carries a fingerprint of every input it was built from; the builders skip it only when the fingerprint is identical.
Inputs: the code that writes or gates pages, the reader-tool flags, every national data file, and the files and place
lists each builder passes in. Anything else changing (a new county in the state, new data, new code) changes the print."""
import glob, hashlib, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "tools")
CODE = ["build_page.py", "build_site.py", "metrics.py", "rules_registry.py", "notes.py", "codes.py", "mapdate.py",
        "gate.py", "card_spec.py", "ffcalc.py", "tools_flags.json", "metric_defs.json"]
_G = None
def _h(*parts):
    h = hashlib.sha256()
    for p in parts: h.update(p if isinstance(p, bytes) else str(p).encode("utf-8")); h.update(b"\0")
    return h.hexdigest()[:20]
def global_fp():   # once per process: code + all national files + the built-states list
    global _G
    if _G is None:
        files = [os.path.join(T, f) for f in CODE] + sorted(glob.glob(os.path.join(ROOT, "data", "us", "*"))) \
                + [os.path.join(ROOT, "data", "states", "built.json")]
        _G = _h(*[(os.path.basename(f), open(f, "rb").read()) for f in files if os.path.isfile(f)])
    return _G
def page_fp(paths, extra=""):
    return _h(global_fp(), *[open(p, "rb").read() for p in paths if os.path.isfile(p)], json.dumps(extra, sort_keys=True))
def mark(fp): return f"<!-- inputs:{fp} -->"
def unchanged(out, fp):   # the page on disk was built from exactly these inputs
    if not os.path.isfile(out): return False
    with open(out, "rb") as f:
        f.seek(max(0, os.path.getsize(out) - 200)); return mark(fp).encode() in f.read()
def stamp(out, fp):
    with open(out, "a", encoding="utf-8") as f: f.write("\n" + mark(fp) + "\n")
