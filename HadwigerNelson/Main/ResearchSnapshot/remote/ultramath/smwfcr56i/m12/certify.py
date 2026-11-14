"""For selected lattice spacings d: find a finite window of the conflict graph
that is not 6-colourable, minimise it greedily, and record the witness."""
import math, json
from fractions import Fraction as F
import cellsat as CS

def shells(d2, nmax2=400):
    return sorted({a*a-a*b+b*b for a in range(-25,26) for b in range(-25,26)
                   if (a,b)!=(0,0) and a*a-a*b+b*b<=nmax2 and CS.conflict(d2, CS.lat(a,b))})

def window_unsat(d2, K, k=6, tl=60):
    verts, edges = CS.window_graph(d2, K)
    nv, clauses = CS.build_cnf(verts, edges, k)
    res,_ = CS.run_cadical(nv, clauses, tl=tl)
    return res, verts, edges

def minimise(d2, verts, edges, k=6, tl=60):
    cur = list(verts)
    changed = True
    while changed:
        changed = False
        for v in list(cur):
            trial = [w for w in cur if w != v]
            ts = set(trial)
            es = [e for e in edges if e[0] in ts and e[1] in ts]
            nv, clauses = CS.build_cnf(trial, es, k)
            res,_ = CS.run_cadical(nv, clauses, tl=tl)
            if res == "UNSAT":
                cur = trial; changed = True
    ts=set(cur); es=[e for e in edges if e[0] in ts and e[1] in ts]
    return cur, es

REC={}
for dstr in ["46/100","2/5","1/3","3/10","1/4"]:
    dd=F(dstr); d2=dd*dd
    sh=shells(d2)
    print(f"d = {dstr} = {float(dd):.4f}: shells (norm^2) = {sh}")
    found=None
    for K in sh+[s+1 for s in sh]:
        if K<9: continue
        res, verts, edges = window_unsat(d2,K)
        print(f"   K={K}: |V|={len(verts)} |E|={len(edges)} -> {res}")
        if res=="UNSAT":
            found=(K,verts,edges); break
        if res is None: break
    if found:
        K, verts, edges = found
        wv, we = minimise(d2, verts, edges)
        print(f"   minimal witness: |V|={len(wv)} |E|={len(we)}  vertices={wv}")
        REC[dstr]={"d":float(dd),"shells":sh,"K":K,"V":len(verts),"E":len(edges),
                   "witness_V":len(wv),"witness_E":len(we),"witness":wv}
    else:
        REC[dstr]={"d":float(dd),"shells":sh,"status":"no window found"}
json.dump(REC, open("certificates.json","w"), indent=1)
print("\nwritten to certificates.json")
