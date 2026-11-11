"""Identical text across place pages (owner 11-11, black-hat review): the share of each sampled county page's sentence words
(sentences of 6+ words) found word for word on EVERY sampled county page. A WARNING only (owner 11-08: no duplicate-content gate):
it prints when the median share rises above the last released value (state/sameness.json); it never blocks. Sample: 8 fixed counties of very different sizes.
Usage: python -I tools/sameness.py [--record] [--test]"""
import json, os, re, statistics, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE = ["raleigh-county-wv", "harris-county-tx", "dixie-county-fl", "berks-county-pa", "calcasieu-parish-la", "monroe-county-fl",
          "boulder-county-co", "travis-county-tx"]
STATE = os.path.join(ROOT, "state", "sameness.json")

def sents(h):
    h = re.sub(r"<(script|style|svg|head)\b.*?</\1>", " ", h, flags=re.S)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
    return [s for s in (x.strip() for x in re.split(r"(?<=[.!?])\s+", t)) if len(s.split()) >= 6]

def shares(pages):
    ss = {k: sents(h) for k, h in pages.items()}
    common = set.intersection(*(set(v) for v in ss.values()))
    return {k: round(100 * sum(len(s.split()) for s in v if s in common) / max(1, sum(len(s.split()) for s in v)), 1) for k, v in ss.items()}, common

def load():
    out = {}
    for s in SAMPLE:
        f = os.path.join(ROOT, "dist", "flood-insurance", s, "index.html")
        if os.path.exists(f): out[s] = open(f, encoding="utf-8").read()
    return out

if __name__ == "__main__":
    pages = load()
    if len(pages) < 4: print("SAMENESS: fewer than 4 sample pages built; skipped"); sys.exit()
    sh, common = shares(pages); med = statistics.median(sh.values())
    if "--test" in sys.argv:
        k = next(iter(pages)); extra = "<p>" + " ".join(f"This added national sentence number {i} has more than six words." for i in range(400)) + "</p>"
        sh2, _ = shares({p: h.replace("</main>", extra + "</main>") for p, h in pages.items()})
        assert statistics.median(sh2.values()) > med, "mutation not caught: shared text added to every page"
        print("sameness mutation: 1 caught"); sys.exit()
    last = json.load(open(STATE)).get("median") if os.path.exists(STATE) else None
    print(f"SAMENESS: identical sentence words, median {med}% ({', '.join(f'{k.split(chr(45))[0]} {v}%' for k, v in sh.items())}); "
          f"{len(common)} sentences on every sample page; last released {last}%")
    if "--record" in sys.argv:
        json.dump({"median": med, "per_page": sh}, open(STATE, "w"), indent=1); print("recorded"); sys.exit()
    # owner 11-08: no duplicate-content gate; this only warns in the release log, never blocks a page or a release
    if last is not None and med > last + 0.5: print(f"SAMENESS WARNING: median rose from {last}% to {med}%")
    else: print("SAMENESS OK")
