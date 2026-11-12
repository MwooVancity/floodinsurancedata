"""AdSense site verification (owner applied 11-12): every indexable built page carries the account meta tag, and
/ads.txt holds exactly the Google line. Verification only: no ad script may appear (owner: no ads before the
4-week Search Console review). Usage: python -I tools/adsense_check.py [--test]"""
import glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<meta name="google-adsense-account" content="ca-pub-8997828618122077">'
ADS = "google.com, pub-8997828618122077, DIRECT, f08c47fec0942fa0"

def check(pages, ads):
    bad = [p for p, h in pages.items() if TAG not in h]
    bad += [f"{p}: ad script present" for p, h in pages.items() if "adsbygoogle" in h or "pagead2.googlesyndication" in h]
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
        one = next(iter(pages))
        muts = {"tag removed": ({**pages, one: pages[one].replace(TAG, "")}, ads),
                "ad script added": ({**pages, one: pages[one] + "<script src=pagead2.googlesyndication.com></script>"}, ads),
                "ads.txt missing": (pages, None), "ads.txt wrong id": (pages, ADS.replace("8997", "8998"))}
        for k, (p, a) in muts.items(): assert check(p, a), f"missed: {k}"
        print(f"adsense mutations: {len(muts)} caught"); sys.exit(0)
    bad = check(pages, ads)
    for b in bad[:10]: print("ADSENSE FAIL", b)
    print("ADSENSE FAIL" if bad else f"ADSENSE PASS ({len(pages)} pages, ads.txt)"); sys.exit(1 if bad else 0)
