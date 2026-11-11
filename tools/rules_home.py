"""National NFIP rules live once, on /nfip/#rules (owner 11-11 "Yes, move it"; black-hat review: ~2,700 identical words on
every place page). Fails when a moved rule prints on any county or state page, or is not on /nfip/ exactly once.
Usage: python -I tools/rules_home.py [--test]"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOVED = ["wait_exceptions", "wait_wildfire", "nfip_lapse", "flood_def", "not_covered", "wind_excl", "aid_insurance",
         "claim_appeal", "substantial_damage", "private_accept", "lender_amount", "lender_force", "zone_review", "seller_assign",
         "lapse_discount"]

def place_pages():
    slugs = {p["slug"] for p in json.load(open(os.path.join(ROOT, "places.json")))} | \
            {s["slug"] for s in json.load(open(os.path.join(ROOT, "data", "states", "built.json")))}
    return [f for s in sorted(slugs) for f in [os.path.join(ROOT, "dist", "flood-insurance", s, "index.html")] if os.path.exists(f)]

def check(pages, nfip):
    bad = []
    for f, h in pages:
        on = sorted(set(re.findall(r'data-rule="(\w+)"', h)) & set(MOVED))
        if on: bad.append(f"{os.path.relpath(f, ROOT)}: national rules back on a place page: {on}")
    for k in MOVED:
        n = len(re.findall(rf'data-rule="{k}"', nfip))
        if n != 1: bad.append(f"/nfip/: rule {k} printed {n} times (want once, in #rules)")
    if 'id="rules"' not in nfip: bad.append("/nfip/: no #rules section")
    return bad

if __name__ == "__main__":
    pages = [(f, open(f, encoding="utf-8").read()) for f in place_pages()]
    nfip = open(os.path.join(ROOT, "dist", "nfip", "index.html"), encoding="utf-8").read()
    if "--test" in sys.argv:
        assert not check(pages, nfip), check(pages, nfip)[:3]
        f, h = pages[0]
        assert check([(f, h + '<span data-rule="wind_excl">x</span>')], nfip), "mutation not caught: rule back on a place page"
        assert check(pages, nfip.replace('data-rule="cap"', 'data-rule="capx"').replace('data-rule="wind_excl"', 'data-rule="gone"', 1)), "mutation not caught: rule missing on /nfip/"
        assert check(pages, nfip + '<span data-rule="flood_def">x</span>'), "mutation not caught: rule twice on /nfip/"
        print("rules_home mutations: 3 caught"); sys.exit()
    bad = check(pages, nfip)
    for b in bad[:20]: print("  -", b)
    print("RULES HOME", "FAIL" if bad else "PASS", f"({len(pages)} place pages, {len(MOVED)} rules)"); sys.exit(1 if bad else 0)
