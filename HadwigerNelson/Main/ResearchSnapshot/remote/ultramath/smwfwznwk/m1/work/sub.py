"""Which subsets of the six transport offsets already force UNSAT?  (exhaustive DFS)"""
import sys
sys.path.insert(0,'work')
from csp import offsets
A,E,B,F,D,C = (frozenset(x) for x in [(1,3),(2,5),(1,4),(3,5),(2,4),(1,5)])
H=[A,E,B,F,D,C]
ADJ={X:set(Y for Y in H if not (X&Y)) for X in H}
def decide(m, offs, fix0=None):
    n=6*m
    dom={i:set(H) for i in range(n)}
    sols=[]
    def propagate():
        changed=True
        while changed:
            changed=False
            for i in range(n):
                for o in offs:
                    j=(i+o)%n
                    for X in list(dom[i]):
                        if not (dom[j]&ADJ[X]): dom[i].discard(X); changed=True
                    if not dom[i]: return False
        return True
    def search():
        if not propagate(): return
        cand=None
        for i in range(n):
            if not dom[i]: return
            if len(dom[i])>1 and (cand is None or len(dom[i])<len(dom[cand])): cand=i
        if cand is None:
            sols.append({i:next(iter(dom[i])) for i in range(n)}); return
        saved={i:set(dom[i]) for i in range(n)}
        for X in sorted(dom[cand],key=lambda S:sorted(S)):
            for i in range(n): dom[i]=set(saved[i])
            dom[cand]={X}; search()
            if sols: return
        for i in range(n): dom[i]=set(saved[i])
    if fix0 is not None: dom[0]={fix0}
    search()
    return sols[0] if sols else None
import itertools
for m in (2,3,4,5):
    O=[o for o in offsets(m) if o%(6*m)!=0]
    half=[o for o in O if o<3*m]          # representatives of +-(m-1),m,m+1
    print("m",m,"offsets",O)
    for r in range(1,4):
        for sub in itertools.combinations(half,r):
            full=sorted(set(sub)|set((6*m-o)%(6*m) for o in sub))
            w=decide(m,full)
            print("   ",sub,"->", "SAT" if w else "UNSAT")
