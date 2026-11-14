"""SAT encoding: translation-invariant sector palette field at a 6-cycle centre, k=6,
all palettes avoiding label 0, admissible (size 2..3, not in a C6 edge), satisfying
w_i disjoint w_{i+o} for o in {+-(m-1), +-m, +-(m+1)} mod n, n=6m.
"""
from itertools import combinations
from pysat.solvers import Solver
K=6
E=[frozenset((j,(j+1)%6)) for j in range(6)]
vals=[]
for r in (2,3):
    for c in combinations(range(1,K),r):
        S=frozenset(c)
        if not any(S<=e for e in E): vals.append(S)
V=len(vals)
print("domain",V)
def solve(m, timeout=120):
    n=6*m
    offs=sorted(set([(m+k)%n for k in (-1,0,1)]+[(-m+k)%n for k in (-1,0,1)]))
    # var index: i*V+v+1
    def var(i,v): return i*V+v+1
    clauses=[]
    for i in range(n):
        clauses.append([var(i,v) for v in range(V)])  # at least one
        for a,b in combinations(range(V),2):
            clauses.append([-var(i,a),-var(i,b)])     # at most one
    for i in range(n):
        for o in offs:
            j=(i+o)%n
            if i==j: continue
            for a in range(V):
                for b in range(V):
                    if vals[a]&vals[b]:
                        clauses.append([-var(i,a),-var(j,b)])
    with Solver(name='cadical', bootstrap_with=clauses) as s:
        r=s.solve()
        if not r: return None, len(clauses)
        model=s.get_model()
        word=[]
        for i in range(n):
            for v in range(V):
                if model[var(i,v)-1]>0: word.append(vals[v]); break
        return word, len(clauses)
for m in (6,9,12,15,18,24):
    w,nc=solve(m)
    print(f"m={m} n={6*m} clauses={nc}: {'SAT' if w else 'UNSAT'}")
    if w:
        print("   first 12:",[sorted(x) for x in w[:12]])
        break
