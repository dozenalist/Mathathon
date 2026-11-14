"""Vacuity / non-vacuity: the same system at k=5 and at k=7.

k=5 (paper: local finiteness is TRUE at k=5).  Palette bound 1<=|P|<=2 (Prop 5.6).
  ell=5 (the longest cycle in 5 labels), free label 0:
  admissible pairs avoiding 0 = {1,3},{1,4},{2,4}; the only disjointness edge is
  {1,3}--{2,4}, so a sector word must alternate those two values:
  a solution exists iff the transport graph C_{6m}(+-(m-1),+-m,+-(m+1)) is BIPARTITE.

k=7 (paper: k>=7 has a genuine accumulating colouring, m3).
  Three pairwise disjoint admissible palettes for C_ell leave k-3 = 4 labels, so a free
  label always exists: the m15 3-block word works for m divisible by 3 at k>=7, for every ell.
"""
import sys
sys.path.insert(0,'work')
from generic import *

def bipartite(n, offs):
    col={}
    adj={i:[(i+o)%n for o in offs] for i in range(n)}
    for s in range(n):
        if s in col: continue
        col[s]=0; stack=[s]
        while stack:
            v=stack.pop()
            for u in adj[v]:
                if u in col:
                    if col[u]==col[v]: return False
                else:
                    col[u]=1-col[v]; stack.append(u)
    return True

print("k=5, C_5, free label 0, pairs: domain, disjointness, and the decision")
V=domain(5,5,0,(2,))
print("   domain:",[sorted(x) for x in V])
edges=[(sorted(V[i]),sorted(V[j])) for i in range(len(V)) for j in range(i+1,len(V)) if not (V[i]&V[j])]
print("   disjointness edges:",edges)
print()
print(f"{'m':>4} {'n=6m':>5} {'transport graph bipartite':>26} {'free-label word':>17}")
for m in range(2,31):
    n=6*m; offs=[o for o in offsets(m,n) if o%n]
    b=bipartite(n,offs)
    ok,_=decide_sat(5,5,0,(2,),m)
    okd,_,_=decide_dfs(5,5,0,(2,),m)
    assert ok==okd==b, (m,ok,okd,b)
    print(f"{m:>4} {n:>5} {str(b):>26} {('SAT' if ok else 'UNSAT'):>17}")
print()
print("k=7, C_6, free label 0: the m15 three-block word at m=6, L=4")
for ell,M in [(6,({1,3},{2,4},{5,6}))]:
    m=6;n=6*m;L=2*m//3
    w=[frozenset(M[(i//L)%3]) for i in range(n)]
    print("   values",[sorted(x) for x in M],"free labels",
          sorted(set(range(7))-set().union(*[set(x) for x in M])))
    print("   check:",check(7,ell,0,w,m,(2,3)) or "all conditions hold")
