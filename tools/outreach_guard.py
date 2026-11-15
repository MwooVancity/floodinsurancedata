"""One email per organization, ever (CLAUDE.md "Outreach"). Run before every send; --record after a send.
Stores only sha256 of the address and of the organization domain in data/outreach.csv (no plain addresses in the repo).
Edge cases (each a --test case): E1 same address, any case or spaces; E2 same organization, other person or subdomain
(agcenter.lsu.edu = lsu.edu); E3 free-mail domains block only the exact address; E5 no record file yet = allowed.
Usage: python -I tools/outreach_guard.py check <address> | record <address> <page> | --test"""
import csv, datetime, hashlib, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "data", "outreach.csv")
FREE = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "icloud.com", "proton.me", "protonmail.com", "comcast.net", "att.net"}
h = lambda s: hashlib.sha256(s.encode()).hexdigest()

def keys(addr):
    a = addr.strip().lower()
    if a.count("@") != 1 or "." not in a.split("@")[1]: raise ValueError(f"not an email address: {addr!r}")
    dom = a.split("@")[1]
    org = ".".join(dom.split(".")[-2:])   # ponytail: last two labels; US .edu/.gov/.org/.com only, add a public-suffix list if .co.uk etc appear
    return h(a), (None if org in FREE else h(org))

def why_not(addr, rows):
    a, o = keys(addr)
    for r in rows:
        if r["addr_sha"] == a: return f"already emailed this address on {r['date']}"
        if o and r["org_sha"] == o: return f"already emailed this organization on {r['date']}"
    return ""

def load():
    return list(csv.DictReader(open(LOG, encoding="utf-8"))) if os.path.exists(LOG) else []

def record(addr, page, rows=None, path=LOG):
    a, o = keys(addr)
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["date", "addr_sha", "org_sha", "page"])
        w.writerow([datetime.date.today().isoformat(), a, o or "", page])

if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        import tempfile
        rows = [{"date": "2026-11-16", "addr_sha": keys("pskinner@agcenter.lsu.edu")[0], "org_sha": keys("pskinner@agcenter.lsu.edu")[1] or ""}]
        assert why_not(" PSkinner@AgCenter.LSU.edu ", rows), "E1 case/space"
        assert why_not("other@lsu.edu", rows) and why_not("x@other.agcenter.lsu.edu", rows), "E2 same org"
        assert not why_not("tfma@tfma.org", rows), "different org passes"
        g = [{"date": "d", "addr_sha": keys("a@gmail.com")[0], "org_sha": ""}]
        assert why_not("a@gmail.com", g) and not why_not("b@gmail.com", g), "E3 free mail: exact address only"
        assert not why_not("a@b.org", []), "E5 first run"
        try: keys("not-an-address"); assert False, "bad address accepted"
        except ValueError: pass
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "o.csv"); record("a@b.org", "/x/", path=p); record("c@d.org", "/y/", path=p)
            r = list(csv.DictReader(open(p, encoding="utf-8")))
            assert len(r) == 2 and "a@b.org" not in open(p, encoding="utf-8").read(), "E4 hashes only, header once"
        sys.exit(print("outreach_guard --test: 9 cases PASS"))
    cmd, addr = sys.argv[1], sys.argv[2]
    reason = why_not(addr, load())
    if cmd == "check": print("BLOCKED: " + reason if reason else "OK to send"); sys.exit(1 if reason else 0)
    if cmd == "record":
        if reason: sys.exit("refused: " + reason)
        record(addr, sys.argv[3]); print("recorded")
