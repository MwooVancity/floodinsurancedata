"""Map every page card in build_page.py: what it reads, when it shows, what rules and notes it prints.
  python -I tools/card_map.py          -> state/card-map.json (+ graphify extraction graphify-out/.graphify_extract.json)
A card is a card(...) call. Its inputs are every metric key and data path passed to tp()/m()/vs_state() inside it, plus
data.get()/EXTRAS/P[...] reads in the lines that build it; its condition is the enclosing if-test."""
import ast, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(ROOT, "tools", "build_page.py"), encoding="utf-8").read()
tree = ast.parse(SRC); lines = SRC.splitlines()
parent = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}

def s(node):   # a constant string, or the literal parts of an f-string
    if isinstance(node, ast.Constant) and isinstance(node.value, str): return node.value
    if isinstance(node, ast.JoinedStr): return "".join(v.value for v in node.values if isinstance(v, ast.Constant))
    return None
def name(call): return getattr(call.func, "id", None) or getattr(call.func, "attr", None)

cards = []
for c in (n for n in ast.walk(tree) if isinstance(n, ast.Call) and name(n) == "card"):
    title = s(c.args[0]) if c.args else None
    seg = ast.get_source_segment(SRC, c) or ""
    keys, paths, rules, notes = set(), set(), set(), set()
    for n in ast.walk(c):
        if not isinstance(n, ast.Call): continue
        f = name(n); a = [s(x) for x in n.args]
        if f in ("tp", "m", "vs_state") and a and a[0]: keys.add(a[0])
        if f in ("tp", "vs_state") and len(a) > 1 and a[1]: paths.add(re.sub(r"\.\d+\.|\.$", ".N.", a[1]).rstrip("."))
        if f == "rule" and a and a[0]: rules.add(a[0])
        if f == "src_rules" and n.args and isinstance(n.args[0], ast.List): rules |= {s(x) for x in n.args[0].elts if s(x)}
        if f == "how" and a and a[0]: notes.add(a[0])
        if f == "claim" and len(n.args) > 2: keys.add("claim:" + (s(n.args[1]) or "?"))
    # show condition: the nearest enclosing if-test, or an inline "... if X else ''"
    cond, p = None, parent.get(c)
    while p is not None and cond is None:
        if isinstance(p, (ast.If, ast.IfExp)): cond = ast.get_source_segment(SRC, p.test)
        p = parent.get(p)
    # variable the card is assigned to (rebuild_card = card(...)), for the gate/test link
    var, p = None, parent.get(c)
    while p is not None and var is None:
        if isinstance(p, ast.Assign) and isinstance(p.targets[0], ast.Name): var = p.targets[0].id
        p = parent.get(p)
    # reads of the raw data in the lines just above the card (its inputs prepared there)
    pre = "\n".join(lines[max(0, c.lineno - 25):c.lineno])
    reads = set(re.findall(r"(?:data|EXTRAS|_xp|_xc|_xpp|cx|P|C|se|pen|ml)\.get\(\"(\w+)\"\)|(?:P|C|cx|se|pen)\[\"(\w+)\"\]", pre + seg))
    reads = {x for t in reads for x in t if x}
    cards.append({"title": title or "(computed title)", "var": var, "line": c.lineno, "condition": cond,
                  "metrics": sorted(keys), "paths": sorted(paths), "reads": sorted(reads),
                  "rules": sorted(rules), "notes": sorted(notes)})

os.makedirs(os.path.join(ROOT, "state"), exist_ok=True)
json.dump(cards, open(os.path.join(ROOT, "state", "card-map.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# graphify extraction: card -> metric / data path / rule / note
nodes, edges, seen = [], [], set()
def node(i, label, kind):
    if i not in seen: seen.add(i); nodes.append({"id": i, "label": label, "file_type": "code", "source_file": "tools/build_page.py", "kind": kind})
for c in cards:
    cid = f"card:{c['line']}"; node(cid, c["title"][:60], "card")
    for k, pre_ in (("metrics", "metric"), ("paths", "path"), ("rules", "rule"), ("notes", "note"), ("reads", "field")):
        for v in c[k]:
            node(f"{pre_}:{v}", v, pre_); edges.append({"source": cid, "target": f"{pre_}:{v}", "relation": f"uses_{pre_}", "confidence": "EXTRACTED", "source_file": "tools/build_page.py"})
os.makedirs(os.path.join(ROOT, "graphify-out"), exist_ok=True)
json.dump({"nodes": nodes, "edges": edges, "hyperedges": [], "input_tokens": 0, "output_tokens": 0},
          open(os.path.join(ROOT, "graphify-out", ".graphify_extract.json"), "w", encoding="utf-8"))
print(f"{len(cards)} cards; {sum(1 for c in cards if c['condition'])} with a show condition; graph {len(nodes)} nodes, {len(edges)} edges")
for c in sorted(cards, key=lambda c: c["line"]):
    print(f"  L{c['line']:<5} {c['title'][:52]:52} metrics {len(c['metrics']):2}  rules {','.join(c['rules'])[:40]}")
