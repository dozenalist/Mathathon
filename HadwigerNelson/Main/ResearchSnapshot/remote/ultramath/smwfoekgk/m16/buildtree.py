#!/usr/bin/env python3
"""Rebuild (incrementally) a modified copy of OAI, using prebuilt oleans for unchanged modules.

Usage: python3 buildtree.py <tree-root-containing-OAI> <build-lib-dir>
Compiles, in topological order, every module whose source differs from lean/OAI's.
"""
import os, re, subprocess, sys, pathlib, time, filecmp

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
ORIG = REPO / "lean" / "OAI"
tree = pathlib.Path(sys.argv[1]).resolve()
build = pathlib.Path(sys.argv[2]).resolve()
force = "--all" in sys.argv

mods = []
for p in sorted(tree.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(tree).with_suffix("").parts)
    deps = []
    for line in p.read_text(errors="ignore").splitlines():
        m = re.match(r"^import\s+(OAI\.[\w.]+)\s*$", line)
        if m:
            deps.append(m.group(1))
    mods.append((name, p, deps))

by = {n: (p, d) for n, p, d in mods}
order, state = [], {}

def visit(n, stack=()):
    if state.get(n) == 2:
        return
    if state.get(n) == 1:
        raise SystemExit(f"cycle at {n}")
    state[n] = 1
    for d in by[n][1]:
        if d in by:
            visit(d, stack + (n,))
    state[n] = 2
    order.append(n)

for n, _, _ in mods:
    visit(n)

changed = set()
for n, p, _ in mods:
    q = ORIG / p.relative_to(tree / "OAI")
    if force or not q.exists() or not filecmp.cmp(p, q, shallow=False):
        changed.add(n)
print(f"{len(mods)} modules, {len(changed)} with modified sources", flush=True)

env = dict(os.environ)
env["LEAN_PATH"] = str(build) + ":" + env.get("LEAN_PATH", "")
t0 = time.time()
fails = []
for n in order:
    if n not in changed:
        continue
    p, _ = by[n]
    out = build / (n.replace(".", "/") + ".olean")
    out.parent.mkdir(parents=True, exist_ok=True)
    if not force and out.exists() and out.stat().st_mtime > p.stat().st_mtime:
        print(f"SKIP {n} (olean newer)", flush=True)
        continue
    s = time.time()
    r = subprocess.run(["lean", "-o", str(out), str(p)], cwd=tree, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    tag = "OK  " if r.returncode == 0 else "FAIL"
    print(f"{tag} {n} ({time.time()-s:.0f}s)", flush=True)
    if r.returncode != 0:
        print(r.stdout[:4000], flush=True)
        fails.append(n)
print(f"done in {time.time()-t0:.0f}s, {len(fails)} failures")
if fails:
    print("FAILURES:", fails)
    sys.exit(1)
