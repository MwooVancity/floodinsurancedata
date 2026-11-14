"""Owner 11-14: at most 25 new pages a day, every kind together (counties, guides, papers, dated copies, glossary).
New = an index.html in dist/ that the committed (live) dist does not have. The day's ledger state/new-pages.json is written
only by a run that ships (release.py --ship, or the cloud publish job), so a dry run never uses up the day.
Usage: python -I tools/new_pages_cap.py [--record] | --test"""
import datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "state", "new-pages.json")
CAP = 25

def built(root=ROOT):
    d = os.path.join(root, "dist")
    return {os.path.relpath(os.path.join(a, f), root).replace("\\", "/") for a, _, fs in os.walk(d) for f in fs if f == "index.html"}

def committed(root=ROOT):
    out = subprocess.run(["git", "ls-files", "dist"], cwd=root, capture_output=True, text=True, check=True).stdout.split()
    return {p for p in out if p.endswith("/index.html") or p == "dist/index.html"}

def over(new, ledger, day, cap=CAP):   # '' when within the cap, else why
    done = set(ledger.get(day, [])); add = sorted(set(new) - done)
    n = len(done) + len(add)
    return "" if n <= cap else f"{n} new pages on {day} (cap {cap}): {len(done)} already shipped today, {len(add)} in this release, e.g. {add[:5]}"

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        assert over({"a", "b"}, {}, "d", cap=2) == ""
        assert over({"a", "b", "c"}, {}, "d", cap=2).startswith("3 new pages")
        assert over({"c"}, {"d": ["a", "b"]}, "d", cap=2).startswith("3 new pages")   # earlier releases today count
        assert over({"a"}, {"d": ["a", "b"]}, "d", cap=2) == ""   # a page already counted today is not counted twice
        assert over({"c"}, {"x": ["a", "b"]}, "d", cap=2) == ""   # yesterday does not count
        sys.exit(print("new_pages_cap --test: 5 cases PASS"))
    day = str(datetime.datetime.now(datetime.timezone.utc).date())
    try: ledger = json.load(open(LEDGER, encoding="utf-8"))
    except (OSError, ValueError): ledger = {}
    new = built() - committed()
    why = over(new, ledger, day)
    print(why or f"new pages today: {len(set(ledger.get(day, [])) | new)} of {CAP}")
    if why: sys.exit(1)
    if "--record" in sys.argv and new:
        ledger = {d: v for d, v in ledger.items() if d >= str(datetime.date.fromisoformat(day) - datetime.timedelta(days=30))}   # capped: 30 days
        ledger[day] = sorted(set(ledger.get(day, [])) | new)
        json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), indent=0)
