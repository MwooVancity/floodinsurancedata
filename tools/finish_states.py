"""After pull_raw.py: aggregate, extras, small datasets, then the full release build (counties + every state, gated).
One background job. Usage: python -I tools/finish_states.py"""
import os, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(T)

def step(*cmd):
    print("==", *cmd, flush=True)
    return subprocess.run([sys.executable, "-I", os.path.join(T, cmd[0]), *cmd[1:]], cwd=ROOT).returncode

step("agg_raw.py")
step("extras_raw.py")
step("collect_state_small.py")
# retry states whose small-dataset pull failed (FEMA 503s are transient)
missing = [d for d in os.listdir(os.path.join(ROOT, "data", "states"))
           if os.path.isdir(os.path.join(ROOT, "data", "states", d)) and not os.path.exists(os.path.join(ROOT, "data", "states", d, "data.json"))]
if missing:
    from agg_raw import NAMES, slug
    retry = [st for st in NAMES if slug(st) in missing]
    print("retry small:", retry, flush=True); step("collect_state_small.py", *retry)
sys.exit(step("release.py"))
