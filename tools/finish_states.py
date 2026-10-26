"""After pull_raw.py: aggregate, extras, small datasets, then the full release build (counties + every state, gated).
One background job. Usage: python -I tools/finish_states.py [--retry-only]"""
import os, subprocess, sys, time
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)
sys.path.insert(0, T)
from agg_raw import NAMES, slug

def step(*cmd):
    print("==", *cmd, flush=True)
    return subprocess.run([sys.executable, "-I", os.path.join(T, cmd[0]), *cmd[1:]], cwd=ROOT).returncode

if "--retry-only" not in sys.argv:
    step("agg_raw.py"); step("extras_raw.py"); step("collect_state_small.py")
# FEMA 503s are transient: up to 3 more passes over states with no data.json, pausing between passes
for i in range(3):
    retry = [st for st in NAMES if not os.path.exists(os.path.join(ROOT, "data", "states", slug(st), "data.json"))]
    if not retry: break
    print("retry small:", retry, flush=True)
    if i: time.sleep(120)
    step("collect_state_small.py", *retry)
sys.exit(step("release.py"))
