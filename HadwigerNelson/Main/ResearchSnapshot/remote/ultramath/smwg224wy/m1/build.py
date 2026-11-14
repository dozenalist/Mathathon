#!/usr/bin/env python3
"""Incremental topological builder for a copy of the OAI tree (m1's own)."""
import os, re, subprocess, sys, time, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE / "tree"
BUILD = ROOT / "build" / "lib"
LOG = HERE / "build_status.json"
mods = []
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps = [m.group(1) for line in p.read_text(errors="ignore").splitlines()
            if (m := re.match(r"^import\s+(OAI\.[\w.]+)\s*$", line))]
    mods.append((name, p, deps))
def topo(mods):
    by = {n: d for n, _, d in mods}; order=[]; state={}
    def visit(n, stack=()):
        if state.get(n)==2: return
        if state.get(n)==1: raise SystemExit(f"cycle at {n}: {stack}")
        state[n]=1
        for d in by[n]:
            if d in by: visit(d, stack+(n,))
        state[n]=2; order.append(n)
    for n,_,_ in mods: visit(n)
    return order
order = topo(mods); by = {n:(p,d) for n,p,d in mods}
status = json.loads(LOG.read_text()) if LOG.exists() else {}
only = sys.argv[1:] if len(sys.argv)>1 else order
if len(sys.argv)>1:
    only = [n for n in order if any(n==a or n.startswith(a+".") or n.endswith("."+a) for a in only)]
env = dict(os.environ); env["LEAN_PATH"] = f"{BUILD}:" + env.get("LEAN_PATH","")
fail=0
for n in only:
    p, deps = by[n]
    out = BUILD / (n.replace(".","/") + ".olean")
    out.parent.mkdir(parents=True, exist_ok=True)
    bad = [d for d in deps if status.get(d,{}).get("ok") is not True]
    if bad and len(sys.argv)==1 and not all((BUILD/(d.replace(".","/")+".olean")).exists() for d in bad):
        status[n]={"ok":False,"err":f"dep failed: {bad}"}; print(f"SKIP {n} {bad}",flush=True); fail+=1; continue
    if out.exists() and out.stat().st_mtime > p.stat().st_mtime and status.get(n,{}).get("ok"):
        continue
    t0=time.time()
    r = subprocess.run(["lean","-o",str(out),str(p)],cwd=ROOT,env=env,
                       stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    dt=time.time()-t0; ok = r.returncode==0
    status[n]={"ok":ok,"err":(r.stdout or "")[:4000],"secs":round(dt,1)}
    print(("OK   " if ok else "FAIL ")+f"{n} [{dt:.0f}s]",flush=True)
    if not ok:
        fail+=1; print((r.stdout or "")[:2000],flush=True)
    LOG.write_text(json.dumps(status,indent=0))
print("done, failures:",fail,flush=True)
sys.exit(1 if fail else 0)
