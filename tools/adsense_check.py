"""AdSense (owner applied 11-12; owner 11-12 "add it like riverwaterlevels did"): every built page carries the account
meta tag and the AdSense code snippet in <head>, and /ads.txt holds exactly the Google line. No hand-placed ad unit
(<ins class="adsbygoogle">): where ads show is decided in the AdSense account (auto ads), owner only.
Usage: python -I tools/adsense_check.py [--test]"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I drops the script dir
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<meta name="google-adsense-account" content="ca-pub-8997828618122077">'
SNIPPET = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8997828618122077"'
           ' crossorigin="anonymous"></script>')
ADS = "google.com, pub-8997828618122077, DIRECT, f08c47fec0942fa0"

def paper(p):   # PAPER-GATE M3.4: no ads on research paper pages (the READY papers and their dated versions, M2.5)
    import papers, re
    return any(re.search(rf"/flood-insurance/{re.escape(s['key'])}/(\d{{4}}-\d{{2}}-\d{{2}}/)?index\.html$", p.replace("\\", "/")) for s in papers.READY)

def check(pages, ads):
    bad = [f"{p}: tag missing" for p, h in pages.items() if TAG not in h]
    bad += [f"{p}: snippet missing or outside <head>" for p, h in pages.items() if not paper(p) and SNIPPET not in h.split("</head>")[0]]
    bad += [f"{p}: ad snippet on a research paper (M3.4)" for p, h in pages.items() if paper(p) and SNIPPET in h]
    bad += [f"{p}: hand-placed ad unit" for p, h in pages.items() if 'class="adsbygoogle"' in h]
    # Adsterra (PLAN 4k, owner 11-24): one 300x250 banner slot, only on county/state pages (not papers, lookups, privacy, home); never any other format
    bad += [f"{p}: {n} Adsterra slots (max 1)" for p, h in pages.items() if (n := h.count('class="adslot"')) > 1]
    bad += [f"{p}: Adsterra slot on a page that must have none" for p, h in pages.items() if 'class="adslot"' in h and not re.search(r"/flood-insurance/[^/]+/index\.html$", p.replace("\\", "/"))]
    bad += [f"{p}: Adsterra slot before the opening answer" for p, h in pages.items() if 'class="adslot"' in h and h.find('class="adslot"') < h.find("</section>")]
    bad += [f"{p}: banned ad format ({w})" for p, h in pages.items() for w in ("popunder", "social bar", "smartlink", "allow-top-navigation") if w in h.lower()]
    bad += [f"{p}: privacy page does not name Adsterra" for p, h in pages.items() if "privacy" in p and "Adsterra" not in h]
    bad += [f"{p}: privacy page denies the ads it loads" for p, h in pages.items()   # outside review 11-12
            if "privacy" in p and ("shows no ads" in h or "AdSense" not in h)]
    if (ads or "").strip() != ADS: bad.append(f"ads.txt is {ads!r}")
    return bad

def load(dist):
    pages = {p: open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(dist, "**", "index.html"), recursive=True)}
    a = os.path.join(dist, "ads.txt")
    return pages, open(a, encoding="utf-8").read() if os.path.exists(a) else None

if __name__ == "__main__":
    pages, ads = load(os.path.join(ROOT, "dist"))
    assert len(pages) > 300, f"only {len(pages)} pages built"
    if "--test" in sys.argv:
        one = next(p for p in pages if not paper(p))
        muts = {"tag removed": ({**pages, one: pages[one].replace(TAG, "")}, ads),
                "snippet removed": ({**pages, one: pages[one].replace(SNIPPET, "")}, ads),
                "ad unit added": ({**pages, one: pages[one] + '<ins class="adsbygoogle"></ins>'}, ads),
                "privacy says no ads": ({**pages, **{p: h + "The site currently shows no ads." for p, h in pages.items() if "privacy" in p}}, ads),
                "snippet on a paper": ({**pages, **{p: h.replace("</head>", SNIPPET + "</head>", 1) for p, h in pages.items() if paper(p)}}, ads),
                "second slot": ({**pages, one: pages[one] + '<aside class="adslot"></aside><aside class="adslot"></aside>'}, ads),
                "popunder added": ({**pages, one: pages[one] + "<script>popunder()</script>"}, ads),
                "top navigation allowed": ({**pages, one: pages[one] + 'sandbox="allow-top-navigation"'}, ads),
                "slot on home": ({**pages, [p for p in pages if p.replace("\\", "/").endswith("/dist/index.html")][0]: '<section></section><aside class="adslot"></aside>'}, ads),
                "privacy omits Adsterra": ({**pages, **{p: h.replace("Adsterra", "") for p, h in pages.items() if "privacy" in p}}, ads),
                "ads.txt missing": (pages, None), "ads.txt wrong id": (pages, ADS.replace("8997", "8998"))}
        for k, (p, a) in muts.items(): assert check(p, a), f"missed: {k}"
        assert not check(pages, ads), "clean build flagged"
        print(f"adsense mutations: {len(muts)} caught"); sys.exit(0)
    bad = check(pages, ads)
    fr = os.path.join(ROOT, "dist", "ad-frame.html")   # the ad iframe's page: must exist, stay noindex, be the one script (11-25)
    f = open(fr, encoding="utf-8").read() if os.path.exists(fr) else ""
    if 'name="robots" content="noindex"' not in f or f.count("<script") != 2 or "bauval.org" not in f: bad.append("dist/ad-frame.html missing, indexable or not the one Adsterra banner")
    hd = os.path.join(ROOT, "dist", "_headers")   # site-wide X-Frame-Options DENY would blank the ad box: /ad-frame.html must say SAMEORIGIN
    if "/ad-frame.html\n  ! X-Frame-Options\n  X-Frame-Options: SAMEORIGIN" not in (open(hd, encoding="utf-8").read().replace("\r\n", "\n") if os.path.exists(hd) else ""): bad.append("_headers lets DENY block the ad frame")
    for b in bad[:10]: print("ADSENSE FAIL", b)
    print("ADSENSE FAIL" if bad else f"ADSENSE PASS ({len(pages)} pages, snippet, ads.txt)"); sys.exit(1 if bad else 0)
