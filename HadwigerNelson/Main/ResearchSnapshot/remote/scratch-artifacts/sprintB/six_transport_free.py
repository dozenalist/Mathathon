"""Search for a translation-invariant sector palette field at a 6-cycle centre at k=6
with all palettes avoiding label 0 (self-avoidance) and satisfying the transport shifts
w_i disjoint w_{i+m+k} for all i and k in {-1,0,1} (both signs).
Domain: admissible palettes of size 2..3 avoiding 0 (16 values).
Backtracking with arc consistency, period n = 6m.
"""
from itertools import combinations
K=6
E=[frozenset((j,(j+1)%6)) for j in range(6)]
vals=[]
for r in (2,3):
    for c in combinations(range(1,K),r):
        S=frozenset(c)
        if not any(S<=e for e in E): vals.append(S)
print("domain size",len(vals))
V=len(vals)
D=[[not (vals[a]&vals[b]) for b in range(V)] for a in range(V)]

def solve(n, offs):
    dom=[list(range(V)) for _ in range(n)]
    def revise(doms):
        changed=True
        while changed:
            changed=False
            for i in range(n):
                for o in offs:
                    j=(i+o)%n
                    if i==j: continue
                    new=[a for a in doms[i] if any(D[a][b] for b in doms[j])]
                    if len(new)<len(doms[i]):
                        doms[i]=new; changed=True
                        if not new: return False
        return True
    def rec(doms):
        if not revise(doms): return None
        if all(len(d)==1 for d in doms):
            return [vals[d[0]] for d in doms]
        i=min((k for k in range(n) if len(dom[k])>1), key=lambda k:len(dom[k]))
        for a in list(doms[i]):
            nd=[list(d) for d in doms]; nd[i]=[a]
            r=rec(nd)
            if r is not None: return r
        return None
    return rec(dom)

for m in (6,9,12,15):
    n=6*m
    offs=sorted(set([(m+k)%n for k in (-1,0,1)]+[(-m+k)%n for k in (-1,0,1)]))
    r=solve(n,offs)
    print(f"m={m} n={n} offsets={offs}: {'SAT' if r else 'UNSAT'}")
    if r:
        print("   first 18 sectors:",[sorted(x) for x in r[:18]])
        break
