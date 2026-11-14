import json, pathlib, re, subprocess, os, sys, time
REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
MIN = pathlib.Path("min"); BUILD = pathlib.Path("minbuild/lib")
mods = {}
for p in sorted(MIN.glob("OAI/**/*.lean")):
    name = ".".join(p.relative_to(MIN).with_suffix("").parts)
    deps = re.findall(r"^import\s+(OAI\.[\w.]+)\s*$", p.read_text(errors="ignore"), re.M)
    mods[name] = (p, deps)
order, state = [], {}
def visit(n, st=()):
    if state.get(n)==2: return
    if state.get(n)==1: raise SystemExit(f"cycle {n} {st}")
    state[n]=1
    for d in mods[n][1]:
        if d in mods: visit(d, st+(n,))
    state[n]=2; order.append(n)
for n in sorted(mods): visit(n)
env = dict(os.environ)
_lp = ":".join(x for x in env["LEAN_PATH"].split(":") if "lean/build/lib" not in x)
env["LEAN_PATH"] = f"{BUILD.resolve()}:" + _lp
print("LEAN_PATH =", env["LEAN_PATH"][:300])
fails = []
t0=time.time()
for n in order:
    p, deps = mods[n]
    out = BUILD/(n.replace(".","/")+".olean"); out.parent.mkdir(parents=True, exist_ok=True)
    if len(sys.argv)>1 and n not in sys.argv[1:]: continue
    if out.exists() and out.stat().st_mtime > p.stat().st_mtime:
        depsok = all((BUILD/(d.replace(".","/")+".olean")).exists() and
                     (BUILD/(d.replace(".","/")+".olean")).stat().st_mtime > p.stat().st_mtime
                     for d in deps if d in mods)
        if depsok:
            print("CACH "+n, flush=True); continue
    r = subprocess.run(["lean","-o",str(out),str(p)], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    ok = r.returncode==0
    print(("OK   " if ok else "FAIL ")+n, flush=True)
    if not ok:
        fails.append(n); print(r.stdout[:2500], flush=True)
print(f"--- {len(order)-len(fails)}/{len(order)} ok in {time.time()-t0:.0f}s")
json.dump(fails, open("minbuild_fails.json","w"))
