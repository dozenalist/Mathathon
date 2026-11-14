"""Independent exhaustive backtracking decision for the sector-word CSP.

Complete search: no SAT solver involved.  Uses
  * arc consistency for the "disjointness" constraints (a letter excludes
    itself and its H-non-neighbours at every offset),
  * vertex-transitivity of the constraint graph (Z_n rotation) and the
    order-2 automorphism group of H to break symmetry: w(0) is fixed to one
    representative of each orbit of values.
Counts nodes so that the search is auditable.
"""
import sys
sys.path.insert(0,'work')
from csp import domain, offsets

A,E,B,F,D,C = (frozenset(x) for x in [(1,3),(2,5),(1,4),(3,5),(2,4),(1,5)])
NAMES={A:'A',E:'E',B:'B',F:'F',D:'D',C:'C'}
H=[A,E,B,F,D,C]
ADJ={X:set(Y for Y in H if not (X&Y)) for X in H}

def decide(m, fix0=None, verbose=True):
    n=6*m; offs=[o for o in offsets(m) if o%n!=0]
    dom={i:set(H) for i in range(n)}
    nodes=[0]; sols=[]
    def propagate():
        # simple AC-3 style fixpoint
        changed=True
        while changed:
            changed=False
            for i in range(n):
                if not dom[i]: return False
                # if singleton, restrict neighbours
                if len(dom[i])==1:
                    X=next(iter(dom[i]))
                    for o in offs:
                        j=(i+o)%n
                        nd=dom[j]&ADJ[X]
                        if nd!=dom[j]:
                            if not nd: return False
                            dom[j]=nd; changed=True
        return True
    def search():
        nodes[0]+=1
        if not propagate(): return
        # pick unassigned vertex with smallest domain (all domains are sets; we
        # branch by restricting a domain to a single value)
        cand=None
        for i in range(n):
            if len(dom[i])>1 and (cand is None or len(dom[i])<len(dom[cand])): cand=i
            if len(dom[i])==0: return
        if cand is None:
            sols.append({i:next(iter(dom[i])) for i in range(n)})
            return
        saved={i:set(dom[i]) for i in range(n)}
        for X in sorted(dom[cand],key=lambda S:sorted(S)):
            for i in range(n): dom[i]=set(saved[i])
            dom[cand]={X}
            search()
            if sols: return     # one solution is enough for SAT
        for i in range(n): dom[i]=set(saved[i])
    if fix0 is not None:
        dom[0]={fix0}
    search()
    return sols[0] if sols else None, nodes[0]

if __name__=='__main__':
    for m in [int(x) for x in sys.argv[1:]]:
        total=0; res=None
        for start in [A,B,D,C]:
            r,nodes=decide(m,fix0=start)
            total+=nodes
            if r is not None:
                res=(start,r); break
        if res is None:
            print(f"m={m} n={6*m}: UNSAT (exhaustive DFS, {total} nodes, w(0) fixed to A,B,D,C)")
        else:
            start,r=res
            print(f"m={m} n={6*m}: SAT w(0)={NAMES[start]} nodes={total}")
            print("   ","".join(NAMES[r[i]] for i in range(6*m)))
