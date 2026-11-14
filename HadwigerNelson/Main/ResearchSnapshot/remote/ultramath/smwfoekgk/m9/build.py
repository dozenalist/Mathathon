import os,re,subprocess,sys,time,pathlib,json
T=pathlib.Path(sys.argv[1]).resolve(); B=pathlib.Path(sys.argv[2]).resolve()
ORDER_F=pathlib.Path("order.json")
mods={}
for p in sorted(T.glob("OAI/**/*.lean")):
    n=".".join(p.relative_to(T).with_suffix("").parts)
    mods[n]=[m.group(1) for m in re.finditer(r"^import\s+(OAI\.[\w.]+)\s*$",p.read_text(errors="ignore"),re.M)]
order=[];st={}
def visit(n):
    if st.get(n)==2: return
    st[n]=1
    for d in mods[n]:
        if d in mods: visit(d)
    st[n]=2; order.append(n)
for n in mods: visit(n)
ORDER_F.write_text(json.dumps(order))
env=dict(os.environ); env["LEAN_PATH"]=f"{B}:"+env.get("LEAN_PATH","")
only=sys.argv[3:]
sel=[n for n in order if not only or any(n==a or n.startswith(a+".") for a in only)]
fails=[]
for n in sel:
    p=T/(n.replace(".","/")+".lean"); out=B/(n.replace(".","/")+".olean")
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists() and out.stat().st_mtime>p.stat().st_mtime and (B/"ok.json").exists():
        pass
    t0=time.time()
    r=subprocess.run(["lean","-o",str(out),str(p)],cwd=T,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    ok=r.returncode==0
    print(("OK  " if ok else "FAIL")+f" {n} [{time.time()-t0:.0f}s]",flush=True)
    if not ok:
        print((r.stdout or "")[:2500],flush=True); fails.append(n)
        if only: break
print(f"done {len(sel)} mods, {len(fails)} failures",flush=True)
