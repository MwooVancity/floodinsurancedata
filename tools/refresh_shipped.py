"""Prints yes when the built county data comes from the latest refresh, no when a refresh still has to ship.
Compares content, not git history, so a docs commit or a shallow clone cannot hide a refresh."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def pulled(*p): return json.load(open(os.path.join(ROOT, "data", *p)))["manifest"]["policies"]["pulled"]
print("yes" if pulled("states", "florida", "agg.json") == pulled("c", "palm-beach-county-fl", "agg.json") else "no")
