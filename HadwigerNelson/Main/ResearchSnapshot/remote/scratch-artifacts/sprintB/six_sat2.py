"""SAT encoding (external cadical): 6-cycle free-label transport word."""
from itertools import combinations
import subprocess, tempfile, os
K=6
E=[frozenset((j,(j+1)%6)) for j in range(6)]
vals=[]
for r in (2,3):
    for c in combinations(range(1,K),r):
        S=frozenset(c)
        if not any(S<=e for e in E): vals.append(S)
V=len(vals)
print("domain",V)
def solve(m):
    n=6*m
    offs=sorted(set([(m+k)%n for k in (-1,0,1)]+[(-m+k)%n for k in (-1,0,1)]))
    def var(i,v): return i*V+v+1
    clauses=[]
    for i in range(n):
        clauses.append([var(i,v) for v in range(V)])
        for a,b in combinations(range(V),2):
            clauses.append([-var(i,a),-var(i,b)])
    for i in range(n):
        for o in offs:
            j=(i+o)%n
            if i==j: continue
            for a in range(V):
                for b in range(V):
                    if vals[a]&vals[b]:
                        clauses.append([-var(i,a),-var(j,b)])
    with tempfile.NamedTemporaryFile('w',suffix='.cnf',delete=False) as f:
        f.write(f"p cnf {n*V} {len(clauses)}\n")
        for c in clauses: f.write(" ".join(map(str,c))+" 0\n")
        path=f.name
    try:
        r=subprocess.run(['/opt/lean/bin/cadical','-q',path],capture_output=True,text=True,timeout=240)
        out=r.stdout
        if 's SATISFIABLE' not in out:
            return None,len(clauses),out.strip().splitlines()[-1] if out else 'no output'
        lits=[]
        for line in out.splitlines():
            if line.startswith('v '): lits += [int(x) for x in line.split()[1:]]
        word=[]
        for i in range(n):
            for v in range(V):
                if var(i,v) in lits: word.append(vals[v]); break
        return word,len(clauses),'SAT'
    finally:
        os.unlink(path)
for m in (6,9,12,15,18,24):
    w,nc,st=solve(m)
    print(f"m={m} n={6*m} clauses={nc}: {st}")
    if w:
        print("   first 12:",[sorted(x) for x in w[:12]])
        break
