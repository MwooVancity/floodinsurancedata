"""S16 internal links (owner 11-14, Google link best practices): structure (home lists every hub, county links its state,
no orphan, no broken link) and anchor quality. Used by google_gate.py; mutation tests in test_calc.py."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # papers.py sits beside this file; -I drops the script dir
from urllib.parse import urljoin, urlparse
HUBS = ("/guides/homeowners-insurance-flooding/",   # 11-13: topic guides (condo...) link only where their topic appears, never forced site-wide
         "/nfip/", "/flood-insurance/renters/", "/flood-insurance/claims/", "/flood-insurance/zip/", "/flood-zone-map/")   # papers join here when papers.READY lists them (methods review 162)

def fails(pages, indexable):
    """11-14 link rule (Google link best practices): structure only. The home page lists every hub that is built;
    topic links on county/state pages sit on words already there and are never forced (orphans: graph_fails)."""
    import papers as _P   # research papers switched on join the hubs; an import error fails the gate, never skips the papers
    _paper_hubs = tuple(f"/flood-insurance/{s['key']}/" for s in _P.READY)
    hubs = [h for h in HUBS + _paper_hubs if h in pages]
    if "/" not in pages: return []
    hr = {urlparse(urljoin("https://floodinsurancedata.com/", x)).path for x in re.findall(r"""href=["']([^"'#?]+)[#?"']""", pages["/"])}
    return [f"/: home does not list {h}" for h in hubs if h not in hr]


GENERIC = {"here", "click here", "read more", "more", "link", "website", "article", "this page", "learn more", "this"}


def anchor_fails(pages):
    """Google 'Link best practices': an anchor is real <a href>, not empty, not generic, reasonably concise (12 words max),
    and links are not chained side by side in running text (nav, footer, lists and tables exempt).
    ponytail: in-page jump links (href="#...") and screen-1 answer cards (data-ans) skip the length rule: the card is the answer.
    Chain = nothing but whitespace between two links; a comma, a middot list or a sentence break separates them."""
    out = []
    for p in sorted(pages):
        h = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", "", pages[p])
        for attrs, inner in re.findall(r"(?is)<a\b([^>]*)>(.*?)</a>", h):
            href = re.search(r"""href=["']([^"']*)["']""", attrs)
            if not href or not href.group(1).strip() or href.group(1).strip().lower().startswith("javascript:"):
                out.append(f"{p}: <a> without a real href ({attrs.strip()[:60]})"); continue
            alt = " ".join(re.findall(r"""(?i)\b(?:alt|aria-label)=["']([^"']*)["']""", attrs + inner))
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner)).strip()
            text = re.sub(r"&[a-z#0-9]+;", " ", text).strip() or alt.strip()
            t = re.sub(r"[^a-z ]", "", text.lower()).strip()
            if not text: out.append(f"{p}: empty anchor to {href.group(1)}")
            elif t in GENERIC: out.append(f"{p}: generic anchor '{text}' to {href.group(1)}")
            elif len(text.split()) > 12 and not href.group(1).startswith("#") and "data-ans=" not in attrs: out.append(f"{p}: anchor over 12 words '{text[:60]}...'")
        body = re.sub(r"(?is)<(nav|footer|ul|ol|table|dl)\b.*?</\1>", "", h)
        for m in re.finditer(r"(?is)</a>((?:\s|&nbsp;)*)<a\b", body):
            out.append(f"{p}: two links side by side with nothing between them ({body[max(0, m.start() - 60):m.start()][-60:]!r})")
    return out


def state_fails(pages, county_state):
    """11-14: a hotfix built county pages while built.json listed no states, and 312 county pages shipped without their state
    link (no gate saw it). county_state = {county path: its state page path}; each built state page must be linked."""
    out = []
    for p, sp in sorted(county_state.items()):
        if p in pages and sp in pages and not re.search(r"""href=["'](?:\.\./|/flood-insurance/)""" + re.escape(sp.rstrip("/").rsplit("/", 1)[1]) + r"""/["']""", pages[p]):
            out.append(f"{p}: no link to its state page {sp}")
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
