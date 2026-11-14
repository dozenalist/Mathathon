#!/usr/bin/env python3
"""Sequential port driver over m8/work (own copy), oleans into m8/lib.
Mirrors scripts/build_lean.py but operates only on this member's tree."""
import os, re, subprocess, sys, time, pathlib, json
ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / os.environ.get("PORT_SRC", "work")
BUILD = ROOT / os.environ.get("PORT_LIB", "lib")
LOG = ROOT / os.environ.get("PORT_LOG", "status.json")
mods = []
for p in sorted(SRC.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(SRC).with_suffix("").parts)
    deps = [m.group(1) for m in (re.match(r"^import\s+(OAI\.[\w.]+)\s*$", l)
            for l in p.read_text(errors="ignore").splitlines()) if m]
    mods.append((name, p, deps))
by = {n: (p, d) for n, p, d in mods}
def topo():
    order, state = [], {}
    def visit(n):
        if state.get(n) == 2: return
        state[n] = 1
        for d in by[n][1]:
            if d in by: visit(d)
        state[n] = 2; order.append(n)
    for n, _, _ in mods: visit(n)
    return order
order = topo()
status = json.loads(LOG.read_text()) if LOG.exists() else {}
env = dict(os.environ); env["LEAN_PATH"] = f"{BUILD}:" + env.get("LEAN_PATH", "")
only = sys.argv[1:]
if only: order = [n for n in order if any(n == a or n.startswith(a + ".") or n.endswith("." + a) for a in only)]
budget = float(os.environ.get("PORT_BUDGET", "1e9")); t_start = time.time()
for n in order:
    p, deps = by[n]
    out = BUILD / (n.replace(".", "/") + ".olean")
    out.parent.mkdir(parents=True, exist_ok=True)
    bad = [d for d in deps if status.get(d, {}).get("ok") is not True]
    if bad:
        status[n] = {"ok": False, "err": f"dep failed: {bad}", "t": time.time()}
        print(f"SKIP {n} ({bad[0]}{'...' if len(bad)>1 else ''})", flush=True); continue
    newest = max([p.stat().st_mtime] + [BUILD.joinpath(d.replace(".", "/") + ".olean").stat().st_mtime
                                        for d in deps if BUILD.joinpath(d.replace(".", "/") + ".olean").exists()])
    if out.exists() and out.stat().st_mtime > newest and status.get(n, {}).get("ok"):
        continue
    if time.time() - t_start > budget:
        print("budget exhausted"); break
    t0 = time.time()
    r = subprocess.run(["lean", "-o", str(out), str(p.relative_to(SRC))], cwd=SRC, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0; ok = r.returncode == 0
    status[n] = {"ok": ok, "err": (r.stdout or "")[:3000], "secs": round(dt, 1), "t": time.time()}
    print(("OK   " if ok else "FAIL ") + f"{n} [{dt:.0f}s]", flush=True)
    if not ok: print((r.stdout or "")[:1200], flush=True)
    LOG.write_text(json.dumps(status, indent=0))
print("done", flush=True)
