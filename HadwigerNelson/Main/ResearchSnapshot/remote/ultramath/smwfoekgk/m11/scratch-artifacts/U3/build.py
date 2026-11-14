import os, re, subprocess, sys, time, pathlib, json
ROOT = pathlib.Path(".").resolve(); BUILD = ROOT/"build"/"lib"
LOG = pathlib.Path("build_status.json")
env=dict(os.environ); env["LEAN_PATH"]=f"{BUILD}:"+env.get("LEAN_PATH","")
mods=[]
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name=".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps=[m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$", p.read_text(errors="ignore"), re.M)]
    mods.append((name,p,deps))
by={n:(p,d) for n,p,d in mods}; order=[]; state={}
def visit(n):
    if state.get(n)==2: return
    if state.get(n)==1: raise SystemExit("cycle "+n)
    state[n]=1
    for d in by[n][1]:
        if d in by: visit(d)
    state[n]=2; order.append(n)
for n,_,_ in mods: visit(n)
status=json.loads(LOG.read_text()) if LOG.exists() else {}
t0=time.time(); done=0; fails=[]
for n in order:
    p,deps=by[n]
    out=BUILD/(n.replace(".","/")+".olean"); out.parent.mkdir(parents=True, exist_ok=True)
    deps_ol=[BUILD/(d.replace(".","/")+".olean") for d in deps if d in by]
    newest=max([p.stat().st_mtime]+[d.stat().st_mtime for d in deps_ol if d.exists()])
    if out.exists() and out.stat().st_mtime>newest and status.get(n,{}).get("ok"): continue
    t=time.time()
    r=subprocess.run(["lean","-o",str(out),str(p)],cwd=str(ROOT),env=env,capture_output=True,text=True)
    dt=time.time()-t; ok=r.returncode==0
    status[n]={"ok":ok,"secs":round(dt,1),"err":(r.stdout or "")[:3000]}
    LOG.write_text(json.dumps(status,indent=0)); done+=1
    print(("OK   " if ok else "FAIL ")+f"{n} [{dt:.0f}s]", flush=True)
    if not ok: fails.append(n); print((r.stdout or "")[:1200], flush=True)
    if time.time()-t0>3200: print("STOP time; done",done); break
print("built",done,"fails",fails,"wall",round(time.time()-t0))
