"""S16 internal links (owner 11-08): every state and county page links each money hub that exists and a zone page,
so a template change can never silently starve one (measured 11-08: /nfip/ had 2 inbound links, renters 1).
Used by google_gate.py; mutation test in test_calc.py."""
import re
HUBS = ("/nfip/", "/flood-insurance/renters/", "/flood-insurance/claims/", "/flood-insurance/zip/", "/flood-zone-map/")

def fails(pages, indexable):
    hubs = [h for h in HUBS if h in pages]
    out = []
    for p in sorted(indexable):
        if not re.fullmatch(r"/flood-insurance/[a-z0-9-]+/", p) or p in hubs: continue
        hr = set(re.findall(r"""href=["']([^"'#?]+)["']""", pages[p]))
        for h in hubs:
            if h == "/flood-insurance/zip/" and not re.search(r"""id=[\"'](zip|counties)[\"']""", pages[p]): continue   # no ZIP or county card (DC): nowhere to link from
            tail = h.rstrip("/").rsplit("/", 1)[1] + "/"
            if not any(x == h or (x.startswith("..") and x.endswith("/" + tail)) for x in hr): out.append(f"{p}: no link to {h}")
        if not any("flood-zones/" in x for x in hr): out.append(f"{p}: no link to a zone page")
    return out
