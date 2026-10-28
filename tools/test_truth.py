"""Proof that each fixed defect is fixed ON THE BUILT PAGES (round 5 claimed a fix the page did not have).
  python -I tools/test_truth.py      after build_all.py; exits 1 on any failure.
One line per fixed hater item: a phrase that must be gone from every page, or must be on a named page."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def page(slug): return open(os.path.join(ROOT, "dist", *(["index.html"] if slug == "home" else ["flood-insurance", slug, "index.html"])), encoding="utf-8").read()
def text(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", h, flags=re.S)))

GONE = {   # wrong or misleading text (hater round): must be on no page
    "now shown as AE": "r6 zone note contradicted the zone table",
    "count different policies": "r6 rebuild note gave the wrong reason",
    "paperwork closures": "r6 tile wrong where the top reason is a denial",
    "no specific reason recorded": "r6 reasons exist for most unpaid claims",
    "a fair new quote can land high": "r5 false price claim",
    "brand-new policy is priced at full risk": "r5 false price claim",
    'placeholder="e.g. 1800"': "r6 checker example was a constant",
    "Below full-risk price: bills step up yearly": "r6 jargon on screen 1",
}
HAS = [   # (page, phrase, why): a fix that must be visible where the reviewer found the defect
    ("louisiana", "1995", "r5/r6 Louisiana's 1995 flood year was hidden"),
    ("louisiana", "FEMA's general label, many separate floods", "r6 catch-all claims were dropped"),
    ("louisiana", "insured for at least 80% of its full rebuilding cost", "r6 the 80% rebuild rule was missing"),
    ("palm-beach-county-fl", "Top reason for unpaid claims", "r6 43.5% paid had no context on screen 1"),
    ("palm-beach-county-fl", "since January 2026", "r6 Citizens tense"),
    ("home", "Average premium alone, single-family homes", "r6 home headline not reconciled with premium-only figures"),
]
bad = []
for f in glob.glob(os.path.join(ROOT, "dist", "**", "index.html"), recursive=True):
    h = open(f, encoding="utf-8").read()
    for p, why in GONE.items():
        if p in h: bad.append(f"{os.path.relpath(f, ROOT)}: still has {p!r} ({why})")
for slug, p, why in HAS:
    if p not in text(page(slug)): bad.append(f"{slug}: missing {p!r} ({why})")
print("\n".join(bad) or f"TRUTH PROOF PASS: {len(GONE)} phrases gone from every page, {len(HAS)} fixes visible")
sys.exit(1 if bad else 0)
