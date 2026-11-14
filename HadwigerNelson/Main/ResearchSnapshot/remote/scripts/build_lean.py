#!/usr/bin/env python3
"""Incremental builder for the extracted OAI Lean development.

Compiles modules in topological order with `lean -o`, writing oleans into
lean/build/lib (which is prepended to LEAN_PATH).  Resumable: modules whose
olean is newer than their source and all OAI deps are skipped.
"""
import os, re, subprocess, sys, time, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent / "lean"
BUILD = ROOT / "build" / "lib"
LOG = ROOT.parent / "scripts" / "build_status.json"

mods = []
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps = []
    for line in p.read_text(errors="ignore").splitlines():
        m = re.match(r"^import\s+(OAI\.[\w.]+)\s*$", line)
        if m:
            deps.append(m.group(1))
    mods.append((name, p, deps))

def topo(mods):
    by = {n: (p, d) for n, p, d in mods}
    order, state = [], {}
    def visit(n, stack=()):
        if state.get(n) == 2: return
        if state.get(n) == 1:
            raise SystemExit(f"cycle at {n}: {stack}")
        state[n] = 1
        for d in by[n][1]:
            if d in by: visit(d, stack + (n,))
        state[n] = 2
        order.append(n)
    for n, _, _ in mods: visit(n)
    return order

order = topo(mods)
by = {n: (p, d) for n, p, d in mods}
status = json.loads(LOG.read_text()) if LOG.exists() else {}
only = sys.argv[1:] if len(sys.argv) > 1 else order
if len(sys.argv) > 1:
    only = [n for n in order if any(n == a or n.startswith(a + ".") or n.endswith("." + a) for a in only)]

env = dict(os.environ)
env["LEAN_PATH"] = f"{BUILD}:" + env.get("LEAN_PATH", "")
for n in only:
    p, deps = by[n]
    out = BUILD / (n.replace(".", "/") + ".olean")
    out.parent.mkdir(parents=True, exist_ok=True)
    bad = [d for d in deps if status.get(d, {}).get("ok") is not True]
    if bad and len(sys.argv) == 1:
        status[n] = {"ok": False, "err": f"dep failed: {bad}", "t": time.time()}
        print(f"SKIP {n} (deps {bad})", flush=True); continue
    if out.exists() and out.stat().st_mtime > p.stat().st_mtime and status.get(n, {}).get("ok"):
        print(f"OK   {n} (cached)", flush=True); continue
    t0 = time.time()
    r = subprocess.run(["lean", "-o", str(out), str(p)], cwd=ROOT, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    ok = r.returncode == 0
    err = (r.stdout or "")[:4000]
    status[n] = {"ok": ok, "err": err, "secs": round(dt, 1), "t": time.time()}
    print(("OK   " if ok else "FAIL ") + f"{n} [{dt:.0f}s]", flush=True)
    if not ok:
        print(err[:1500], flush=True)
    LOG.write_text(json.dumps(status, indent=0))
print("done", flush=True)
