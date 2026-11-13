"""AdSense (owner applied 11-12; owner 11-12 "add it like riverwaterlevels did"): every built page carries the account
meta tag and the AdSense code snippet in <head>, and /ads.txt holds exactly the Google line. No hand-placed ad unit
(<ins class="adsbygoogle">): where ads show is decided in the AdSense account (auto ads), owner only.
Usage: python -I tools/adsense_check.py [--test]"""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I drops the script dir
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<meta name="google-adsense-account" content="ca-pub-8997828618122077">'
SNIPPET = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8997828618122077"'
           ' crossorigin="anonymous"></script>')
ADS = "google.com, pub-8997828618122077, DIRECT, f08c47fec0942fa0"

def paper(p):   # PAPER-GATE M3.4: no ads on research paper pages (the READY papers, exactly)
    import papers
    return any(p.replace("\\", "/").endswith(f"/flood-insurance/{s['key']}/index.html") for s in papers.READY)

def check(pages, ads):
    bad = [f"{p}: tag missing" for p, h in pages.items() if TAG not in h]
    bad += [f"{p}: snippet missing or outside <head>" for p, h in pages.items() if not paper(p) and SNIPPET not in h.split("</head>")[0]]
    bad += [f"{p}: ad snippet on a research paper (M3.4)" for p, h in pages.items() if paper(p) and SNIPPET in h]
    bad += [f"{p}: hand-placed ad unit" for p, h in pages.items() if 'class="adsbygoogle"' in h]
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
                "ads.txt missing": (pages, None), "ads.txt wrong id": (pages, ADS.replace("8997", "8998"))}
        for k, (p, a) in muts.items(): assert check(p, a), f"missed: {k}"
        assert not check(pages, ads), "clean build flagged"
        print(f"adsense mutations: {len(muts)} caught"); sys.exit(0)
    bad = check(pages, ads)
    for b in bad[:10]: print("ADSENSE FAIL", b)
    print("ADSENSE FAIL" if bad else f"ADSENSE PASS ({len(pages)} pages, snippet, ads.txt)"); sys.exit(1 if bad else 0)
