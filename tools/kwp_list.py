"""Keyword Planner upload list (<= 9,900 lines, the limit that works). Output: kwp-upload.txt in the repo root (untracked).
Run: python -I tools/kwp_list.py. Owner pastes it into Keyword Planner "Get search volume and forecasts", United States, last 12 months."""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agg_raw import NAMES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = 9900
GENERIC = ["flood insurance", "flood insurance cost", "average flood insurance cost", "how much is flood insurance",
           "flood insurance quote", "flood insurance by zip code", "flood insurance rates by zip code", "flood zone map",
           "flood zone by address", "flood zone map by address", "what flood zone am i in", "fema flood map by address",
           "do i need flood insurance", "is flood insurance required", "flood insurance waiting period", "nfip",
           "fema flood insurance", "flood insurance claims", "flood insurance for renters", "flood insurance companies"]
ZONES = ["a", "ae", "ah", "ao", "v", "ve", "x", "shaded x", "d", "b", "c"]

kw = list(GENERIC)
for z in ZONES:
    kw += [f"flood zone {z}", f"flood zone {z} meaning", f"flood insurance cost zone {z}"]
for st in NAMES.values():
    s = st.lower()
    kw += [f"flood insurance {s}", f"flood insurance cost {s}", f"flood zone map {s}"]
for name in json.load(open(os.path.join(ROOT, "data", "us", "county_names.json"), encoding="utf-8")).values():
    n = name.split(",")[0].strip().lower()  # "Palm Beach County, Florida" -> "palm beach county"
    kw += [f"{n} flood insurance", f"{n} flood zone map"]
# towns: ZIP town names, most ZIPs first (proxy for size), until the cap
towns = collections.Counter(t.lower() for t in json.load(open(os.path.join(ROOT, "data", "us", "zip_places.json"), encoding="utf-8")).values())
seen = set(kw)
for t, _ in towns.most_common():
    if len(seen) >= CAP: break
    if "zona urbana" in t or "comunidad" in t: continue  # Puerto Rico census labels, not search words
    k = f"flood insurance {t}"
    if k not in seen: seen.add(k); kw.append(k)
kw = list(dict.fromkeys(kw))[:CAP]
open(os.path.join(ROOT, "kwp-upload.txt"), "w", encoding="utf-8").write("\n".join(kw) + "\n")
print(len(kw), "keywords;", sum(k.startswith("flood insurance ") and k.split(" ", 2)[2] in towns for k in kw), "towns")
