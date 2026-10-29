"""Census county adjacency (2024) -> data/us/county_adjacency.json {geoid: [neighbour geoids]}, for the county sibling
links (PLAN.md step 5b: a county links the counties that border it, not just its state's biggest).
Source: https://www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2024.txt
Usage: python -I tools/fetch_adjacency.py <downloaded txt>"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
adj = {}
for line in open(sys.argv[1], encoding="utf-8").read().splitlines()[1:]:
    p = line.split("|")
    if len(p) == 4 and p[1] != p[3]:
        adj.setdefault(p[1], []).append(p[3])
json.dump(adj, open(os.path.join(ROOT, "data", "us", "county_adjacency.json"), "w"), separators=(",", ":"))
print(f"{len(adj)} counties, {sum(len(v) for v in adj.values())} neighbour pairs")
