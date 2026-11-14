"""Exact coverage intervals for the clique witnesses and the SAT certificates."""
import math, json
from fractions import Fraction as F
import cellsat as CS

def interval_of_shells(shells, verbose=True):
    los=[]; his=[]
    for nn in shells:
        rep=None
        for a in range(-30,31):
            for b in range(-30,31):
                if a*a-a*b+b*b==nn: rep=(a,b); break
            if rep: break
        v=CS.lat(*rep)
        dm2=CS.delta_min2(v); dx2=CS.delta_max2(v)
        def qf(x): return float(x[0])+float(x[1])*math.sqrt(3)
        dm=math.sqrt(max(0.0,qf(dm2))); dx=math.sqrt(qf(dx2))
        los.append(0.0 if dm==0 else 1.0/dm)
        his.append(1.0/dx)
        if verbose:
            print(f"      shell norm2={nn}: delta_min={dm:.6f} delta_max={dx:.6f}"
                  f"  -> conflict for d in ({1.0/dx:.6f}, {'inf' if dm==0 else f'{1.0/dm:.6f}'})")
    return max(los), min(his)

print("=== clique witnesses (explicit 7-cliques) ===")
C1=[(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]
CLIQUES = {
 "C1 = {0} u N(0), shells {1,3,4}": (C1, [1,3,4]),
 "C2 (translated/rotated sqrt3-scaled clique), shells {3,9,12}":
     ([(-1,0),(0,-1),(0,2),(1,1),(2,0),(2,3),(3,2)], [3,9,12]),
 "C3 = 2*C1, shells {4,12,16}": ([(2*a,2*b) for a,b in C1], [4,12,16]),
}
for name,(pts,sh) in CLIQUES.items():
    print(f"  {name}")
    norms=set(); ok=True
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            a=pts[i]; b=pts[j]
            nn=(a[0]-b[0])**2-(a[0]-b[0])*(a[1]-b[1])+(a[1]-b[1])**2
            norms.add(nn)
            if nn not in sh: ok=False
    print(f"    pairwise norm^2 values: {sorted(norms)}  (all in shell set: {ok})")
    lo,hi=interval_of_shells(sh, verbose=False)
    print(f"    => 7-clique valid for d in ({lo:.6f}, {hi:.6f})")

print()
print("=== SAT certificates: interval on which the shell set is constant ===")
REC=json.load(open("certificates.json"))
for k,v in REC.items():
    print(f"  d = {v['d']:.4f}: shells {v['shells']}, window |V|={v['V']} |E|={v['E']},"
          f" 6-colourable = NO, minimal witness |V|={v['witness_V']}")
for sh in [[3,4,7,9],[4,7,9,12,13],[7,9,12,13,16,19],[9,12,13,16,19,21]]:
    print(f"  shell set {sh}:")
    lo,hi=interval_of_shells(sh, verbose=False)
    print(f"    covers d in ({lo:.6f}, {hi:.6f})")
