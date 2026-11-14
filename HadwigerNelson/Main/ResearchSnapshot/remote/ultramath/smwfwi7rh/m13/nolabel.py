"""The same sector CSP without the free label: all 2- and 3-element palettes that are not
cycle edges of C6 (29 values).  Question: is the *free label* the binding constraint, or the
transport itself?  Also: the k=5 calibration (pairs from 4 labels)."""
from itertools import combinations
from pysat.solvers import Cadical153

def domain(k, free=None, sizes=(2,3)):
    labels = [x for x in range(k) if x != free]
    vals=[]
    for r in sizes:
        for c in combinations(labels, r):
            T=frozenset(c)
            if k == 6 and any(T <= e for e in [frozenset((j%6,(j+1)%6)) for j in range(6)]):
                continue
            vals.append(T)
    return vals

def solve(m,K,vals,k=6):
    n=6*m; NV=len(vals)
    offs=sorted({(m+e)%n for e in range(-K,K+1)}|{(-(m+e))%n for e in range(-K,K+1)})
    if 0 in offs: return False,None
    def var(j,v): return j*NV+v+1
    cls=[]
    for j in range(n):
        cls.append([var(j,v) for v in range(NV)])
        for v in range(NV):
            for w in range(v+1,NV): cls.append([-var(j,v),-var(j,w)])
    bad=[(v,w) for v in range(NV) for w in range(NV) if vals[v]&vals[w]]
    for j in range(n):
        for o in offs:
            j2=(j+o)%n
            if j2<=j: continue
            for v,w in bad: cls.append([-var(j,v),-var(j2,w)])
    with Cadical153(bootstrap_with=cls) as s:
        sat=s.solve(); mod=s.get_model() if sat else None
    if not sat: return False,None
    word=[None]*n
    for j in range(n):
        for v in range(NV):
            if mod[var(j,v)-1]>0: word[j]=vals[v]
    return True,word

if __name__=="__main__":
    D6=domain(6); print("k=6, no free label: domain size", len(D6), "(pairs 15 + triples 20 - 6 edge pairs = 29)")
    for m in (3,4,5,6,9,10,12,15,20,30):
        row=[]
        for K in range(0, m//2+2):
            sat,_=solve(m,K,D6)
            row.append((K,sat))
        kmax=max([k for k,s in row if s], default=None)
        firstbad=min([k for k,s in row if not s], default=None)
        print(f"  m={m:3d}: K_max={kmax}  first UNSAT K={firstbad}   floor(m/3)={m//3} floor(m/2)={m//2}")
    print()
    D5=domain(5,free=0,sizes=(2,)); print("k=5 calibration: free label 0, pairs from {1,2,3,4}:", len(D5), "values")
    for m in (2,3,5,6,9):
        sat,w=solve(m,0,D5,k=5)
        print(f"  m={m} K=0 ((5.7) only): {'SAT' if sat else 'UNSAT'}   word={[sorted(x) for x in w][:6] if w else None}")
