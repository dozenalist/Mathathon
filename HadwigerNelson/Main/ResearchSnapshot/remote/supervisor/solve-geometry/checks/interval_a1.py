"""Exact (Q(sqrt3)) per-offset extrema at a = 1, checked against interval_cert.json."""
import json, os, math
from fractions import Fraction as F

# Q(sqrt3): (u,w) = u + w*sqrt3
Z=(F(0),F(0)); ONE=(F(1),F(0)); TWO=(F(2),F(0))
O=((F(0),F(0)),(F(0),F(0)))                       # origin, as a POINT
def qadd(x,y): return (x[0]+y[0],x[1]+y[1])
def qsub(x,y): return (x[0]-y[0],x[1]-y[1])
def qmul(x,y): return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def qdiv(x,y):
    d=y[0]*y[0]-3*y[1]*y[1]; return ((x[0]*y[0]-3*x[1]*y[1])/d,(x[1]*y[0]-x[0]*y[1])/d)
def sign(x):
    u,w=x
    if w==0: return (u>0)-(u<0)
    if u>0: return 1 if (w>0 or u*u>3*w*w) else -1
    if w>0: return 1 if 3*w*w>u*u else -1
    return -1
def qlt(x,y): return sign(qsub(x,y))<0
def psub(a,b): return (qsub(a[0],b[0]),qsub(a[1],b[1]))
def padd(a,b): return (qadd(a[0],b[0]),qadd(a[1],b[1]))
def smul(s,a): return (qmul(s,a[0]),qmul(s,a[1]))
def qmin(xs):
    m=xs[0]
    for x in xs[1:]:
        if qlt(x,m): m=x
    return m
def qmax(xs):
    m=xs[0]
    for x in xs[1:]:
        if qlt(m,x): m=x
    return m
def nrm2(p): return qadd(qmul(p[0],p[0]),qmul(p[1],p[1]))

# hexagon, circumradius 1, inradius sqrt3/2, vertices at 30,90,...,330 degrees
h=lambda u,v:((u,v))
H=[((F(0),F(1,2)),(F(1,2),F(0))),   # (  sqrt3/2,  1/2)
   ((F(0),F(0)),  (F(1),F(0))),     # (  0,       1  )
   ((F(0),-F(1,2)),(F(1,2),F(0))),  # ( -sqrt3/2,  1/2)
   ((F(0),-F(1,2)),(-F(1,2),F(0))), # ( -sqrt3/2, -1/2)
   ((F(0),F(0)),  (-F(1),F(0))),    # (  0,      -1  )
   ((F(0),F(1,2)),(-F(1,2),F(0)))]  # (  sqrt3/2, -1/2)
H2=[smul(TWO,v) for v in H]                         # H - H = 2H
def offset(p,q): return ((F(0),F(p)+F(q,2)),(F(3,2)*q,Z[1]))   # a = 1
def d2seg(o,x,y):
    d=psub(y,x); w=psub(o,x); dd=nrm2(d)
    if sign(dd)==0: return nrm2(w),'V'
    t=qdiv(qadd(qmul(w[0],d[0]),qmul(w[1],d[1])),dd)
    inner = sign(qsub(t,Z))>0 and sign(qsub(ONE,t))>0
    if qlt(t,Z): t=Z
    if qlt(ONE,t): t=ONE
    return nrm2(psub(w,smul(t,d))), ('E' if inner else 'V')
def extrema(p,q):
    v=offset(p,q); V=[padd(v,w) for w in H2]
    ds=[d2seg(O,V[i],V[(i+1)%6]) for i in range(6)]
    dmin=qmin([d for d,_ in ds]); kind=next(k for d,k in ds if sign(qsub(d,dmin))==0)
    dmax=qmax([nrm2(z) for z in V])
    return dmin,kind,dmax

C=json.load(open(os.path.join("..","..","supervisor","solve-independent","interval_cert.json")))
rows=C["per_offset_at_a_eq_1"]; bad=[]; mus=[]; nus=[]; kinds={}
for r in rows:
    p,q=r["v"]; dmin,kind,dmax=extrema(p,q)
    mu=int(r["mu2"].split(")")[0].lstrip("(")); nu=int(r["nu2"].split(")")[0].lstrip("("))
    if not(dmin[1]==0 and dmin[0]==mu and dmax[1]==0 and dmax[0]==nu): bad.append((r["v"],dmin,dmax,mu,nu))
    mus.append(dmin[0]); nus.append(dmax[0]); kinds[kind]=kinds.get(kind,0)+1

out=[]
def say(*a):
    s=" ".join(str(x) for x in a); out.append(s); print(s)
say(f"[15] per-offset extrema at a=1, recomputed exactly in Q(sqrt3): {len(rows)} offsets")
say(f"     mismatches vs interval_cert.json (mu2, nu2): {len(bad)}  {bad[:2]}")
say(f"     distinct min^2 {sorted(set(mus))}; distinct max^2 {sorted(set(nus))}")
say(f"     contacts realising the minimum: {kinds}   (E = edge interior, V = polygon vertex)")
lo2=int(qmin.__self__ if False else min(nus)); hi2=int(max(mus))
say(f"     binding: largest min^2 = {hi2} (=> a < 1/sqrt{hi2}); smallest max^2 = {lo2} (=> a > 1/sqrt{lo2})")
say(f"     interval (1/sqrt{lo2}, 1/sqrt{hi2}) = ({math.sqrt(1/lo2):.9f}, {math.sqrt(1/hi2):.9f})")
say(f"     [19/100, 22/100] inside: {(F(19,100)**2>F(1,lo2)) and (F(22,100)**2<F(1,hi2))};"
    f"  a = 1/5 inside: {25<lo2 and 25>hi2}  (1/5 > 1/sqrt{lo2} iff {lo2}>25; 1/5 < 1/sqrt{hi2} iff 25>{hi2})")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","supervisor_checks.out"),"a").write("\n".join(out)+"\n")
