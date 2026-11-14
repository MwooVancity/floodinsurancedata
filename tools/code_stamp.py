"""Code bug-review stamp (owner 11-14: "I don't want to ship nonperfect pages"). The page gates check what a page says;
this checks that the code that writes pages was bug-reviewed. release.py --ship (and the cloud publish) stops when any
tools/*.py, *.sh, *.mjs, tools/static/*.js or workflow file differs from the version the last /code-review medium passed (every finding fixed or ruled out).
Usage: python -I tools/code_stamp.py --check | --stamp "review note" | --test"""
import datetime, glob, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAMP = os.path.join(ROOT, "state", "reviews", "code-reviewed.json")
PATTERNS = ("tools/*.py", "tools/*.sh", "tools/*.mjs", "tools/static/*.js", ".github/workflows/*.yml")   # bug review 11-14: page JS (zonemap.js) and the deploy script are code too; vendor/ and data .json are not

def files(root=ROOT):
    return sorted(os.path.relpath(f, root).replace("\\", "/") for p in PATTERNS for f in glob.glob(os.path.join(root, p)))

def code_hash(root=ROOT):   # line endings normalised: a checkout with CRLF is the same code
    h = hashlib.sha256()
    for f in files(root):
        h.update(f.encode() + b"\0" + open(os.path.join(root, f), "rb").read().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()

def check(root=ROOT, stamp=STAMP):
    try: s = json.load(open(stamp, encoding="utf-8"))
    except Exception: return "no code review stamp yet"
    return "" if s.get("hash") == code_hash(root) else f"code changed since the bug review of {s.get('date')} ({s.get('note', '')[:80]})"

if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--test"]:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "tools")); os.makedirs(os.path.join(d, ".github", "workflows"))
            open(os.path.join(d, "tools", "x.py"), "w").write("a = 1\n"); st = os.path.join(d, "s.json")
            assert check(d, st) == "no code review stamp yet"
            json.dump({"hash": code_hash(d), "date": "t", "note": ""}, open(st, "w"))
            assert check(d, st) == "", "fresh stamp refused"
            open(os.path.join(d, "tools", "x.py"), "wb").write(b"a = 1\r\n"); assert check(d, st) == "", "CRLF counted as a change"
            open(os.path.join(d, "tools", "x.py"), "w").write("a = 2\n"); assert check(d, st), "edited code passed"
            open(os.path.join(d, "tools", "x.py"), "w").write("a = 1\n"); open(os.path.join(d, "tools", "y.py"), "w").write("")
            assert check(d, st), "new file passed"
            open(os.path.join(d, "tools", "y.yml"), "w").write(""); os.remove(os.path.join(d, "tools", "y.py"))
            open(os.path.join(d, ".github", "workflows", "w.yml"), "w").write("on: push\n"); assert check(d, st), "new workflow passed"
            os.makedirs(os.path.join(d, "tools", "static")); json.dump({"hash": code_hash(d), "date": "t", "note": ""}, open(st, "w"))
            open(os.path.join(d, "tools", "static", "z.js"), "w").write("x()"); assert check(d, st), "page JS change passed"
            os.remove(os.path.join(d, "tools", "static", "z.js")); open(os.path.join(d, "tools", "d.sh"), "w").write("w"); assert check(d, st), "deploy script change passed"
        sys.exit(print("code_stamp --test: 7 cases PASS"))
    if a[:1] == ["--stamp"] and len(a) == 2:
        os.makedirs(os.path.dirname(STAMP), exist_ok=True)
        json.dump({"hash": code_hash(), "date": str(datetime.date.today()), "note": a[1]}, open(STAMP, "w", encoding="utf-8"), indent=1)
        sys.exit(print("stamped", code_hash()[:12]))
    why = check(); print(why or "code review stamp matches"); sys.exit(1 if why else 0)
