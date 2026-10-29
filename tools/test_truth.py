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
    "change coverage at renewal": "r7 44 CFR 61.11 says a coverage increase waits 30 days",
    "A policy can carry the full limit": "r7 unsourced program claim",
    "upper-middle": "r7 checker called the median itself above the middle",
    "costliest single flood": "r11 an unnamed year paid more than the 'costliest single flood'",
    "many separate floods": "r11 a storm-named catch-all label was called many floods",
    "ice-storm and tornado aid are left out": "r11 severe-storm aid with tornado damage was counted",
    "a tile map shows": "r11 methodology described the retired tile map",
    "severe repetitive loss list": "r12 FEMA's disaster-aid SRL flag was called the NFIP list",
    "the top reason FEMA recorded": "r12 the lead skipped 'Other', the table's first row",
}
HAS = [   # (page, phrase, why): a fix that must be visible where the reviewer found the defect
    ("louisiana", "1995", "r5/r6 Louisiana's 1995 flood year was hidden"),
    ("louisiana", "FEMA's records use this name for claims in several years", "r6 catch-all claims were dropped"),
    ("louisiana", "insured for at least 80% of its full rebuilding cost", "r6 the 80% rebuild rule was missing"),
    ("palm-beach-county-fl", "Some unpaid claims are paperwork, not denied floods", "r6/r16 43.5% paid had no context on screen 1"),
    ("palm-beach-county-fl", "since January 2026", "r6 Citizens tense"),
    ("palm-beach-county-fl", "Share that paid something", "r6/r7 43.5% paid had no era breakdown (r8: header named the wrong column)"),
    ("louisiana", "Not in full for at least", "r7 rebuild lead ignored under-insurance"),
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
