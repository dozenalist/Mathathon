import os, re, subprocess, sys, time, pathlib, json
ROOT = pathlib.Path("work/lean").resolve()
BUILD = ROOT/"build"/"lib"
LOG = pathlib.Path(".scratch/build2_status.json")
mods=[]
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    name=".".join(p.relative_to(ROOT).with_suffix("").parts)
    deps=[m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$", p.read_text(errors="ignore"), re.M)]
    mods.append((name,p,deps))
by={n:(p,d) for n,p,d in mods}
order=[]; state={}
def visit(n):
    if state.get(n)==2: return
    if state.get(n)==1: raise SystemExit("cycle "+n)
    state[n]=1
    for d in by[n][1]:
        if d in by: visit(d)
    state[n]=2; order.append(n)
for n,_,_ in mods: visit(n)
status=json.loads(LOG.read_text()) if LOG.exists() else {}
env=dict(os.environ); env["LEAN_PATH"]=f"{BUILD}:"+env.get("LEAN_PATH","")
t0=time.time(); done=0; fail=[]
for n in order:
    p,deps=by[n]
    out=BUILD/(n.replace(".","/")+".olean"); out.parent.mkdir(parents=True, exist_ok=True)
    deps_oleans=[BUILD/(d.replace(".","/")+".olean") for d in deps if d in by]
    newest=max([p.stat().st_mtime]+[d.stat().st_mtime for d in deps_oleans if d.exists()])
    if out.exists() and out.stat().st_mtime>newest and status.get(n,{}).get("ok"):
        continue
    t=time.time()
    r=subprocess.run(["lean","-o",str(out),str(p)],cwd=str(ROOT),env=env,capture_output=True,text=True)
    dt=time.time()-t
    ok=r.returncode==0
    status[n]={"ok":ok,"secs":round(dt,1),"err":(r.stdout or "")[:2000]}
    LOG.write_text(json.dumps(status,indent=0))
    done+=1
    print(("OK   " if ok else "FAIL ")+f"{n} [{dt:.0f}s]", flush=True)
    if not ok:
        fail.append(n); print((r.stdout or "")[:800], flush=True)
    if time.time()-t0 > 2900:
        print("STOP (time budget); built", done, "remaining", len(order)-len([x for x in order if status.get(x,{}).get('ok')])); break
print("built",done,"fails",fail, "wall", round(time.time()-t0,0))
