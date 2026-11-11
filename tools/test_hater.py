"""Prove hater.py record: PASS only for a clean section, FAIL if any BLOCKER/MAJOR, and ignore non-page sections."""
import os, sys, json, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools")); import hater, review as RV
p = os.path.join(hater.DIR, "hater-round99.md")
open(p, "w", encoding="utf-8").write(
    "# x\n## home\n1. **MINOR** tiny\nVerdict: PASS\n"
    "## louisiana\n1. **MAJOR** bad thing\nVerdict: PASS\n"
    "## palm-beach-county-fl\n1. **BLOCKER** wrong\nVerdict: FAIL\n"
    "## Classes\n**MAJOR** everywhere\n")
keep = {s: RV.get(s) for s in ("home", "louisiana", "palm-beach-county-fl")}
tf = os.path.join(hater.DIR, "round99-template.txt"); open(tf, "w").write("seenbyreviewer99")   # the hash prep saved
hater.record(99)
got = {s: RV.get(s)["verdict"] for s in keep}
stamped = {RV.get(s)["template"] for s in keep}   # a PASS carries the template the reviewer saw, not today's

for s, r in keep.items():   # restore whatever was there
    f = os.path.join(RV.DIR, s + ".json")
    if r: json.dump(r, open(f, "w", encoding="utf-8"), indent=1)
    elif os.path.exists(f): os.remove(f)
os.remove(p); os.remove(tf)
assert stamped == {"seenbyreviewer99"}, stamped
assert got == {"home": "PASS", "louisiana": "FAIL", "palm-beach-county-fl": "FAIL"}, got
print("hater record self-test OK", got)
# template review + code flags: a county far from its state is flagged; an ordinary one is not
assert RV.flags("palm-beach-county-fl"), "Palm Beach (56.5% unpaid vs Florida 30.1%) must be flagged"
assert not RV.flags("lee-county-fl"), RV.flags("lee-county-fl")
assert RV.flags("home") == [] and RV.flags("louisiana") == []
print("flag self-test OK")

# carry with no slugs must take every page on the samples' approved template, never a FAIL
import hater as _H
_s = _H.stamped_slugs()
assert {"home", "louisiana", "palm-beach-county-fl", "new-york-county-ny"} <= set(_s), _s   # the samples + one flagged page; Broward left 11-04 (not re-reviewed, not required by S12)
assert "horry-county-sc" not in _s and "atlantic-county-nj" not in _s, _s   # a FAIL and an older template stay out
print("carry slug list OK:", len(_s))
# 11-10: carry into a round that already holds a review must refuse (it overwrote reviewer round 128)
try: _H.carry("128", "HEAD", ["home"]); raise AssertionError("carry overwrote an existing round file")
except SystemExit as e: assert "exists" in str(e), e
print("carry refuses an existing round file OK")
