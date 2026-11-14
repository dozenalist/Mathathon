"""Extract a small H-uncolourable subgraph of the m=4 constraint graph (the m<=4 obstruction).

Constraint graph for m=4: vertices Z_24, edges i--j iff j-i in {+-3,+-4,+-5} mod 24.
We shrink greedily: drop a vertex whenever the rest is still not H-colourable.
The result is a finite certificate that can be checked by exhaustive search alone.
"""
import sys
sys.path.insert(0,'work')
from itertools import combinations
A,E,B,F,D,C = (frozenset(x) for x in [(1,3),(2,5),(1,4),(3,5),(2,4),(1,5)])
H=[A,E,B,F,D,C]
ADJ={X:set(Y for Y in H if not (X&Y)) for X in H}
NAMES={A:'A',E:'E',B:'B',F:'F',D:'D',C:'C'}

def edges_of(V,m):
    n=6*m; offs=[o for o in (m-1,m,m+1) if o%n]
    return {i:sorted({(i+o)%n for o in offs+[-o for o in offs]}) for i in V}

def colourable(V, m):
    V=list(V); E=edges_of(V,m)
    deg={v:len([u for u in E[v] if u in V]) for v in V}
    order=sorted(V,key=lambda v:-deg[v])
    col={}
    def bt(k):
        if k==len(order): return True
        v=order[k]
        used={col[u] for u in E[v] if u in col}
        for X in H:
            if all(not (X&Y) for Y in used):
                col[v]=X
                if bt(k+1): return True
                del col[v]
        return False
    return bt(0)

m=4
V=set(range(24))
assert not colourable(V,m)
changed=True
while changed:
    changed=False
    for v in sorted(V):
        T=V-{v}
        if not colourable(T,m):
            V=T; changed=True
print("minimal uncolourable vertex set for m=4:",sorted(V))
E=edges_of(V,m)
print("edges (as index pairs inside the set):",[(i,j) for i in sorted(V) for j in E[i] if j in V and i<j])
print("degrees:",{i:len([j for j in E[i] if j in V]) for i in sorted(V)})
print("|V| =",len(V))
