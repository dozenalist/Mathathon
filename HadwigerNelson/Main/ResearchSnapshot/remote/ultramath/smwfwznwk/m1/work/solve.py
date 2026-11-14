import sys, subprocess, tempfile, os
sys.path.insert(0,'work')
from csp import *

def build_cnf(m, V):
    n=6*m; d=len(V)
    def var(i,v): return i*d+v+1
    cl=[]
    for i in range(n):
        cl.append([var(i,v) for v in range(d)])
        for a,b in combinations(range(d),2):
            cl.append([-var(i,a),-var(i,b)])
    offs=offsets(m)
    seen=set()
    for i in range(n):
        for o in offs:
            j=(i+o)%n
            if i==j: continue
            for a in range(d):
                for b in range(d):
                    if V[a]&V[b]:
                        cl.append([-var(i,a),-var(j,b)])
    return n*d, cl

def solve(m, sizes=(2,3), timeout=300):
    V=domain(sizes=sizes)
    nv,cl=build_cnf(m,V)
    with tempfile.NamedTemporaryFile('w',suffix='.cnf',delete=False) as f:
        f.write(f"p cnf {nv} {len(cl)}\n")
        for c in cl: f.write(" ".join(map(str,c))+" 0\n")
        path=f.name
    try:
        r=subprocess.run(['/opt/lean/bin/cadical','-q',path],capture_output=True,text=True,timeout=timeout)
        out=r.stdout
        if 's SATISFIABLE' not in out:
            last=[l for l in out.splitlines() if l.startswith('s ')]
            return None, len(cl), (last[-1] if last else 'UNKNOWN')
        lits=set()
        for line in out.splitlines():
            if line.startswith('v '): lits|=set(int(x) for x in line.split()[1:] if x!='0')
        word=[]
        for i in range(6*m):
            got=[V[v] for v in range(len(V)) if (i*len(V)+v+1) in lits]
            assert len(got)==1, (i,got)
            word.append(got[0])
        return word, len(cl), 'SAT'
    finally:
        os.unlink(path)

if __name__=='__main__':
    sizes=eval(sys.argv[1]) if len(sys.argv)>1 else (2,3)
    ms=eval(sys.argv[2]) if len(sys.argv)>2 else list(range(2,31))
    for m in ms:
        w,nc,st=solve(m,sizes=sizes)
        extra=''
        if w:
            extra=' check='+str(check_word(w,m,verbose=False))
        print(f"m={m:3d} n={6*m:4d} dom={len(domain(sizes=sizes))} clauses={nc} {st}{extra}",flush=True)
