"""Sitemap lastmod = the later of the data's date and the day the page's visible text last changed (audit 11-10).
The change day comes from the last released copy (git HEAD): text differs from HEAD's page = today (UTC); same text =
HEAD's sitemap date for that URL. No state file; nothing is stamped on a first run or for an unchanged page (no fake freshness).
Usage: imported by build_site.py; python -I tools/lastmod.py --test"""
import datetime, re, subprocess, sys

def vis(h):   # what a reader sees: no scripts, styles, tags or the build fingerprint comment
    h = re.sub(r"<(script|style)\b.*?</\1>", "", h or "", flags=re.S)
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()

def pick(old_html, new_html, old_lm, data_lm, today):
    """old_html None = page not in the last release (new page): data date only."""
    if old_html is None: return data_lm
    changed = vis(old_html) != vis(new_html)
    when = today if changed else old_lm
    return max(x for x in (when, data_lm) if x) if (when or data_lm) else None

def head_files(root, rels):   # one git process for every page (a git call per page grows with the site)
    p = subprocess.run(["git", "cat-file", "--batch"], cwd=root, input="".join(f"HEAD:{r}\n" for r in rels).encode(), capture_output=True)
    if p.returncode: return dict.fromkeys(rels)   # not a git checkout (factory builds in a temp dir): every page counts as new
    out, buf, i = {}, p.stdout, 0
    for r in rels:
        j = buf.index(b"\n", i); hdr = buf[i:j].decode(); i = j + 1
        if hdr.endswith("missing"): out[r] = None; continue
        n = int(hdr.split()[2]); out[r] = buf[i:i + n].decode("utf-8", "replace"); i += n + 1
    return out

def head_lastmods(root):
    sm = subprocess.run(["git", "show", "HEAD:dist/sitemap.xml"], cwd=root, capture_output=True, text=True, encoding="utf-8").stdout
    return dict(re.findall(r"<loc>(.*?)</loc><lastmod>(.*?)</lastmod>", sm))

def today(): return datetime.datetime.now(datetime.timezone.utc).date().isoformat()

if __name__ == "__main__":
    if "--test" in sys.argv:
        a, b = "<p>Cost $900</p><!-- inputs: x -->", "<p>Cost $950</p><!-- inputs: y -->"
        assert pick(a, a.replace("x", "z"), "2026-09-01", "2026-08-31", "2026-11-10") == "2026-09-01", "fingerprint-only change must not move lastmod"
        assert pick(a, b, "2026-09-01", "2026-08-31", "2026-11-10") == "2026-11-10", "text change = today"
        assert pick(a, a, None, "2026-08-31", "2026-11-10") == "2026-08-31", "unchanged, no old date = data date"
        assert pick(a, a, None, None, "2026-11-10") is None, "hub page unchanged, no dates = no lastmod (never invent one)"
        assert pick(None, b, None, "2026-08-31", "2026-11-10") == "2026-08-31", "new page = data date, not today"
        assert pick(a, a, "2026-08-01", "2026-08-31", "2026-11-10") == "2026-08-31", "newer data date wins"
        assert pick(a, "<script>x=1</script>" + a, "2026-09-01", None, "2026-11-10") == "2026-09-01", "script change is not visible text"
        print("lastmod self-check: 7 cases PASS"); sys.exit()
