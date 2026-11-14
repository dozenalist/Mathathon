import subprocess, tempfile, os
from itertools import combinations
E=[(1<<j)|(1<<((j+1)%6)) for j in range(6)]
def adm(S): return 1<=bin(S).count('1')<=3 and not any(S&e==S for e in E)
def dom(pairs_only):
    out=[]
    for r in (2,3):
        for c in combinations(range(1,6),r):
            S=sum(1<<i for i in c)
            if adm(S): out.append(S)
    return [v for v in out if bin(v).count('1')==2] if pairs_only else out
def offsets(m):
    n=6*m; return sorted({(m+k)%n for k in (-1,0,1)}|{(-m+k)%n for k in (-1,0,1)})
def run(m, vals):
    n=6*m; S=offsets(m); V=len(vals)
    def var(i,v): return i*V+v+1
    cl=[]
    for i in range(n):
        cl.append([var(i,v) for v in range(V)])
        for a,b in combinations(range(V),2): cl.append([-var(i,a),-var(i,b)])
    for i in range(n):
        for d in S:
            j=(i+d)%n
            if i==j: continue
            for a in range(V):
                for b in range(V):
                    if vals[a]&vals[b]: cl.append([-var(i,a),-var(j,b)])
    with tempfile.NamedTemporaryFile('w',suffix='.cnf',delete=False) as f:
        f.write(f"p cnf {n*V} {len(cl)}\n")
        for c in cl: f.write(" ".join(map(str,c))+" 0\n")
        path=f.name
    r=subprocess.run(['/opt/lean/bin/cadical','-q',path],capture_output=True,text=True,timeout=600)
    os.unlink(path)
    return r.stdout
for m in (1,2,3,4):
    out=run(m, dom(True))
    print(f"--- m={m} pairs: first lines of cadical output:")
    print("\n".join(out.splitlines()[:4]))
    print("   last:", out.splitlines()[-1] if out.splitlines() else "(empty)")
