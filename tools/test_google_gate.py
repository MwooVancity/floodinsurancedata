"""Mutations for google_gate.py S6 (11-09: the sitemap check looked only under /flood-insurance/, so /data/ was indexable and
unlisted with the gate passing). On a copy of the built dist: the real build has no S6 failure; a page dropped from the
sitemap and a URL that is not built must each fail S6. Run after a build: python -I tools/test_google_gate.py"""
import os, re, shutil, subprocess, sys, tempfile
T = os.path.dirname(os.path.abspath(__file__)); DIST = os.path.join(os.path.dirname(T), "dist")

def s6(root):
    r = subprocess.run([sys.executable, "-I", os.path.join(T, "google_gate.py"), "--root", root, "--skip-review"], capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if "[S6]" in l]

tmp = tempfile.mkdtemp()
try:
    d = os.path.join(tmp, "dist"); shutil.copytree(DIST, d)
    sm = os.path.join(d, "sitemap.xml"); base = open(sm, encoding="utf-8").read()
    assert not s6(d), s6(d)
    # 11-11 (daily run 43105520015 failed): a site page carries <lastmod> once its text changes (tools/lastmod.py); drop the
    # /data/ <url> block in either shape, and prove the lastmod shape too, whichever shape the build has today
    drop = lambda t: re.sub(r"\s*<url><loc>[^<]*/data/</loc>(?:<lastmod>[^<]*</lastmod>)?</url>", "", t, count=1)
    alt = re.sub(r"(<url><loc>[^<]*/data/</loc>)(?:<lastmod>[^<]*</lastmod>)?(</url>)", r"\1<lastmod>2026-11-11</lastmod>\2", base, count=1)
    assert drop(alt) != alt and drop(base) != base, "drop pattern misses a sitemap shape"
    muts = {"page dropped": drop(base),
            "unbuilt url": base.replace("</urlset>", "  <url><loc>https://floodinsurancedata.com/no-such-page/</loc></url>\n</urlset>")}
    for k, v in muts.items():
        assert v != base, f"mutation did not change the sitemap: {k}"
        open(sm, "w", encoding="utf-8").write(v)
        assert s6(d), f"S6 missed: {k}"
    print(f"test_google_gate: {len(muts)} S6 mutations caught")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
