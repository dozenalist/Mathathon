"""Regenerate certificates.json: for each listed lattice spacing d, find the smallest
window of the conflict graph that is not 6-colourable.  Runtime ~10-20 min total."""
import json, sys
from fractions import Fraction as F
import cellsat as CS

DS = ["217/1000","47/200","1/4","11/40","3/10","32/100","1/3","2/5","46/100"]

def shells(d2, nmax2=200):
    return sorted({a*a-a*b+b*b for a in range(-25,26) for b in range(-25,26)
                   if (a,b)!=(0,0) and a*a-a*b+b*b<=nmax2 and CS.conflict(d2, CS.lat(a,b))})

def certify(dstr, tl=180, maxv=200):
    dd=F(dstr); d2=dd*dd; sh=shells(d2)
    for K in sh:
        if K<9: continue
        verts,edges=CS.window_graph(d2,K)
        if len(verts)>maxv: return None
        nv,cl=CS.build_cnf(verts,edges,6)
        res,_=CS.run_cadical(nv,cl,tl=tl)
        if res=="UNSAT":
            return {"d":float(dd),"shells":sh,"K":K,"V":len(verts),"E":len(edges)}
        if res is None: return None
    return None

if __name__=="__main__":
    try:
        REC=json.load(open("certificates.json"))
    except Exception:
        REC={}
    args=[a for a in sys.argv[1:] if not a.startswith("--")]
    force="--force" in sys.argv
    only = args or DS
    for dstr in only:
        if dstr in REC and not force:
            print(f"{dstr}: already recorded ({REC[dstr]['V']} vertices)"); continue
        print(f"{dstr}: running ...", flush=True)
        r=certify(dstr)
        if r: REC[dstr]=r; print(f"   UNSAT window |V|={r['V']} |E|={r['E']} (K={r['K']})")
        else: print("   no window found within limits")
        json.dump(REC,open("certificates.json","w"),indent=1)
    print("certificates.json has", len(REC), "entries")
