"""Exact coverage intervals, using EVERY lattice vector (not one per shell),
so that shells with several orbits (first: |v|^2 = 49) are handled correctly."""
import math, json
import cellsat as CS
from fractions import Fraction as F

def qf(x): return float(x[0])+float(x[1])*math.sqrt(3)

VECS=[]
for a in range(-25,26):
    for b in range(-25,26):
        nn=a*a-a*b+b*b
        if 0<nn<=200: VECS.append((a,b,nn))

BOUNDS=[]
for (a,b,nn) in VECS:
    v=CS.lat(a,b)
    dm=math.sqrt(max(0.0,qf(CS.delta_min2(v)))); dx=math.sqrt(qf(CS.delta_max2(v)))
    BOUNDS.append((nn, (0.0 if dm==0 else 1.0/dm), 1.0/dx))   # (norm2, lower entry, upper exit)

def shellset(d):
    d2=F(d).limit_denominator(10**9); d2=d2*d2
    return frozenset(nn for (a,b,nn) in VECS if CS.conflict(d2, CS.lat(a,b)))

crit=sorted({x for (nn,lo,hi) in BOUNDS for x in (lo,hi) if 0<x<1.0})
bounds=[0.0]+crit+[1.0]
segs=[]
for i in range(len(bounds)-1):
    a,b=bounds[i],bounds[i+1]
    if b-a<1e-12: continue
    segs.append((a,b,(a+b)/2))
print(f"critical values below 1: {len(crit)};  segments: {len(segs)}")
SETS={}
for (a,b,m) in segs: SETS[m]=shellset(m)
def coverage(d0):
    S0=shellset(d0)
    idx=next(i for i,(a,b,m) in enumerate(segs) if SETS[m]==S0)
    L,R=segs[idx][0],segs[idx][1]
    i=idx
    while i>0 and SETS[segs[i-1][2]]==S0: i-=1; L=segs[i][0]
    i=idx
    while i<len(segs)-1 and SETS[segs[i+1][2]]==S0: i+=1; R=segs[i][1]
    return S0,L,R

REC=json.load(open("certificates.json"))
print(f"{'d tested':>8} {'|V|':>5} {'6-col':>5}   coverage interval")
for k,v in sorted(REC.items(), key=lambda kv: kv[1]['d']):
    S,L,R=coverage(v['d'])
    print(f"{v['d']:8.4f} {str(v.get('V')):>5} {'no':>5}   ({L:.5f}, {R:.5f})  shells={sorted(S)}")
