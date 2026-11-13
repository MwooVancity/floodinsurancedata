"""S16 internal links (owner 11-08): every state and county page links each money hub that exists and a zone page,
so a template change can never silently starve one (measured 11-08: /nfip/ had 2 inbound links, renters 1).
Used by google_gate.py; mutation test in test_calc.py."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # papers.py sits beside this file; -I drops the script dir
from urllib.parse import urljoin, urlparse
HUBS = ("/guides/homeowners-insurance-flooding/",   # 11-13: topic guides (condo...) link only where their topic appears, never forced site-wide
         "/nfip/", "/flood-insurance/renters/", "/flood-insurance/claims/", "/flood-insurance/zip/", "/flood-zone-map/")   # papers join here when papers.READY lists them (methods review 162)

def fails(pages, indexable):
    import papers as _P   # research papers switched on join the hubs; an import error fails the gate, never skips the papers
    _paper_hubs = tuple(f"/flood-insurance/{s['key']}/" for s in _P.READY)
    hubs = [h for h in HUBS + _paper_hubs if h in pages]
    out = []
    for p in sorted(indexable):
        if not re.fullmatch(r"/flood-insurance/[a-z0-9-]+/", p) or p in hubs: continue
        hr = set(re.findall(r"""href=["']([^"'#?]+)[#?"']""", pages[p]))
        for h in hubs:
            if h == "/flood-insurance/zip/" and not re.search(r"""id=[\"'](zip|counties)[\"']""", pages[p]): continue   # no ZIP or county card (DC): nowhere to link from
            tail = h.rstrip("/").rsplit("/", 1)[1] + "/"
            if not any(x == h or (x.startswith("..") and x.endswith("/" + tail)) for x in hr): out.append(f"{p}: no link to {h}")
        if not any("flood-zones/" in x for x in hr): out.append(f"{p}: no link to a zone page")
    return out


def graph_fails(pages, indexable):
    """Every internal link lands on a built page; every indexable page has an inbound link from another page."""
    out, inbound = [], {p: 0 for p in indexable}
    for p in sorted(pages):
        for h in set(re.findall(r"""href=["']([^"'#?]+)[#?"']""", pages[p])):
            if h.startswith(("http", "mailto:", "tel:")) and "floodinsurancedata.com" not in h: continue
            t = urlparse(urljoin("https://floodinsurancedata.com" + p, h)).path
            if not t.endswith("/") or t == p: continue   # files (csv, json, xml) are checked elsewhere
            if t not in pages: out.append(f"{p}: links {t}, which is not a built page")
            elif t in inbound: inbound[t] += 1
    out += [f"{p}: orphan (no page links to it)" for p, n in inbound.items() if n == 0 and p != "/"]
    return out
