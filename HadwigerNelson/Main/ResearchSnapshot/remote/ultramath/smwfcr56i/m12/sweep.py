"""Sweep over the distinct conflict-graph shell sets for d in (0, sqrt3/2),
and for each find a finite window that is not 6-colourable (SAT refutation)."""
import math, subprocess, sys
from fractions import Fraction as F
import cellsat as CS

S3=math.sqrt(3)
# critical d-values: for shell with norm^2 n, conflict iff d in (1/dmax, 1/dmin)
crit=[]
for a in range(-25,26):
    for b in range(-25,26):
        nn=a*a-a*b+b*b
        if nn==0 or nn>500: continue
        v=CS.lat(a,b)
        dm2=CS.delta_min2(v); dx2=CS.delta_max2(v)
        # 1/dmax^2 = 1/dx2   (in Q(sqrt3)); use float for the sweep grid
        def qf(x):
            return float(x[0])+float(x[1])*S3
        dm=math.sqrt(qf(dm2)); dx=math.sqrt(qf(dx2))
        if dx>0: crit.append(1.0/dx)
        if dm>0: crit.append(1.0/dm)
crit=sorted(set(round(c,9) for c in crit if 0<c<1.2))
crit=[c for c in crit if c < S3/2]
print(f"critical d values below sqrt3/2: {len(crit)}")
print("range:", crit[0], "..", crit[-1])

def shells_of(d2):
    return sorted({a*a-a*b+b*b for a in range(-30,31) for b in range(-30,31)
                   if (a,b)!=(0,0) and a*a-a*b+b*b<=300 and CS.conflict(F(d2), CS.lat(a,b))})

def test_d(dd, Ks, k=6, tl=15):
    d2=F(dd).limit_denominator(10**6)**2 if False else F(dd)*F(dd)
    out=[]
    for K in Ks:
        verts, edges = CS.window_graph(d2, K)
        if len(verts)>260: break
        nv, clauses = CS.build_cnf(verts, edges, k)
        res, model = CS.run_cadical(nv, clauses, tl=tl)
        out.append((K,len(verts),len(edges),res))
        if res=="UNSAT": return out
        if res is None: return out
    return out

# representative d for each interval
lo, hi = 0.15, S3/2
pts = [lo]
for i,c in enumerate(crit):
    if c<=lo or c>=hi: continue
    pts.append(c)
pts.append(hi)
mids=[]
for i in range(len(pts)-1):
    a,b=pts[i],pts[i+1]
    if b-a < 1e-9: continue
    mids.append(round((a+b)/2,6))
print(f"intervals to test: {len(mids)}")
outcomes={}
for m in mids:
    if m<=lo or m>=hi: continue
    sh=shells_of(m)
    Ks=[9,12,13,16,19,21,25,27,28,31,36,39,43]
    res=test_d(m,Ks)
    ok=[r for r in res if r[3]=="UNSAT"]
    outcomes[m]=(sh,res)
    tag = f"UNSAT at K={ok[0][0]} |V|={ok[0][1]}" if ok else f"no UNSAT up to K={res[-1][0] if res else '-'} ({res[-1][3] if res else '-'})"
    print(f"  d={m:.6f} shells={sh} -> {tag}")
