"""Exact open interval in a on which the SAME 42 offsets (hence the same 888 edges of G[P], hence the
same 6-UNSAT certificate p19.cnf/p19.drup) stay strictly forced.
Homothety: the whole configuration at parameter a is a times the one at a = 1, so
   dmin(v,a) = a*dmin(v,1) = a*mu(v),   dmax(v,a) = a*dmax(v,1) = a*nu(v).
Forced strictly  <=>  dmin < 1 < dmax  <=>  1/nu(v) < a < 1/mu(v).
Intersecting over the finitely many used offsets gives  ( max_v 1/nu(v), min_v 1/mu(v) ).
ONE process: derive from the geometry at a = 1, then CROSS-CHECK by recomputing dmin/dmax directly at
several exact rational values of a (not via scaling), including points just outside the interval."""
from fractions import Fraction as F
import json, itertools, time
t0=time.time()
class Q3:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a,s.b=F(a),F(b)
    def __add__(s,o): o=t(o); return Q3(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q3(-s.a,-s.b)
    def __sub__(s,o): o=t(o); return Q3(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return t(o)-s
    def __mul__(s,o):
        o=t(o); return Q3(s.a*o.a+3*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s):
        d=s.a*s.a-3*s.b*s.b; assert d
        return Q3(s.a/d,-s.b/d)
    def __truediv__(s,o): return s*t(o).inv()
    def sign(s):
        a,b=s.a,s.b
        if a==0: return 0 if b==0 else (1 if b>0 else -1)
        if b==0: return 1 if a>0 else -1
        if a>0 and b>0: return 1
        if a<0 and b<0: return -1
        sq=a*a-3*b*b
        return (1 if a>0 else -1) if sq>0 else ((1 if b>0 else -1) if sq<0 else 0)
    def __eq__(s,o): return (s-t(o)).sign()==0
    def __lt__(s,o): return (s-t(o)).sign()<0
    def __gt__(s,o): return (s-t(o)).sign()>0
    def __le__(s,o): return (s-t(o)).sign()<=0
    def __ge__(s,o): return (s-t(o)).sign()>=0
    def __repr__(s): return f"({s.a})+({s.b})r3"
def t(x): return x if isinstance(x,Q3) else Q3(x)
S3=Q3(0,1)
V=lambda u,v:(u[0]+v[0], u[1]+v[1]); W=lambda u,v:(u[0]-v[0], u[1]-v[1])
SC=lambda c,u:(t(c)*u[0],t(c)*u[1]); DT=lambda u,v:u[0]*v[0]+u[1]*v[1]; NN=lambda u:DT(u,u)
def hexverts(a):
    a=t(a); h=F(1,2)
    cs=[(S3/F(2),h),(0,1),(-S3/F(2),h),(-S3/F(2),-h),(0,-1),(S3/F(2),-h)]
    return [(a*t(c[0]),a*t(c[1])) for c in cs]
def pseg2(p,x,y):
    d=W(y,x); w=W(p,x); dd=NN(d)
    if dd.sign()==0: return NN(w)
    s=DT(w,d)/dd
    if s<=Q3(0): s=Q3(0)
    elif s>=Q3(1): s=Q3(1)
    return NN(W(p,V(x,SC(s,d))))
def centre(p,q,a):
    s=t(a)*S3
    return (s*t(p)+s*t(q)/2, s*t(q)*S3/F(2))
def ranges(p,q,a):
    """exact (dmin^2, dmax^2) between cell (0,0) and cell (p,q) at circumradius a -- direct geometry"""
    fig=[V(centre(p,q,a),z) for z in hexverts(t(2)*a)]
    return min(pseg2((Q3(0),Q3(0)),fig[i],fig[(i+1)%6]) for i in range(6)), max(NN(z) for z in fig)
Norm=lambda p,q:p*p+p*q+q*q
Fset=sorted([(p,q) for p in range(-5,6) for q in range(-5,6) if 0<Norm(p,q)<=16])
# forced set at a = 1/5, exactly (re-derivation)
Fs=[v for v in Fset if (lambda r: r[0]<Q3(1) and Q3(1)<r[1])(ranges(v[0],v[1],F(1,5)))]
Fs=sorted(Fs)
assert len(Fs)==42 and set(Norm(*v) for v in Fs)=={4,7,9,12,13}
out=[]
def say(s): out.append(s); print(s)
say(f"[0] F at a=1/5 re-derived exactly: |F| = {len(Fs)}, rings {sorted(set(Norm(*v) for v in Fs))}  ({time.time()-t0:.2f}s)")

# ---- 1. confirm the 888 edges use exactly these 42 offsets -------------------
C=json.load(open('patch19_cert.json'))
cells=[tuple(c) for c in C["cells"]]
diffs=set()
for (i,j) in C["edges_indexed"]:
    d=(cells[j][0]-cells[i][0], cells[j][1]-cells[i][1])
    diffs.add(d if d in set(Fs) else (-d[0],-d[1]))
say(f"[1] distinct offsets realised by the 888 recorded edges: {len(diffs)}; equals F? {diffs==set(Fs)}")
assert diffs==set(Fs)
say(f"    -> the certificate p19.cnf is the 6-colouring CNF of the graph whose edge set is")
say(f"       {{(u,w) in P^2 : w-u in F}}, a combinatorial condition that does not mention 'a'.")
say(f"       So keeping these 42 offsets strictly forced keeps the SAME 888 edges and the SAME CNF.")

# ---- 2. mu^2, nu^2 at a = 1, per offset -------------------------------------
rows=[]; MU={}; NU={}
for v in Fs:
    mu2,nu2=ranges(v[0],v[1],Q3(1))
    rows.append({"v":list(v),"N":Norm(*v),"mu2":str(mu2),"nu2":str(nu2)})
    N=Norm(*v)
    MU.setdefault(N,[]).append(mu2); NU.setdefault(N,[]).append(nu2)
MUraw=MU; NUraw=NU
MU={N:v[0] for N,v in MUraw.items()}; NU={N:v[0] for N,v in NUraw.items()}
for N in MUraw:      # constancy on the ring, checked exactly
    assert all(x==MUraw[N][0] for x in MUraw[N]), N
    assert all(x==NUraw[N][0] for x in NUraw[N]), N
rings={}
for r in rows:
    rings.setdefault(r["N"],[]).append(r)
say("")
say("[2] exact per-ring values at a = 1 (mu = dmin, nu = dmax).  Constant on a ring? (D6 symmetry)")
say("      N   mu^2 (dmin^2)      nu^2 (dmax^2)     #vectors   constant?")
for N in sorted(rings):
    ms={r["mu2"] for r in rings[N]}; ns={r["nu2"] for r in rings[N]}
    say(f"     {N:3d}   {sorted(ms)}   {sorted(ns)}    {len(rings[N]):2d}        {len(ms)==1 and len(ns)==1}")
    assert len(ms)==1 and len(ns)==1
max_mu2=max((MU[N] for N in rings), key=lambda x:(x.a,x.b))
min_nu2=min((NU[N] for N in rings), key=lambda x:(x.a,x.b))
N_of_maxmu=[N for N in rings if MU[N]==max_mu2][0]
N_of_minnu=[N for N in rings if NU[N]==min_nu2][0]
say("")
say(f"[3] max_v mu^2 = {max_mu2} at ring N={N_of_maxmu}   ->  upper endpoint  a < 1/sqrt({max_mu2})")
say(f"    min_v nu^2 = {min_nu2} at ring N={N_of_minnu}   ->  lower endpoint  a > 1/sqrt({min_nu2})")
assert max_mu2.b==0 and min_nu2.b==0
# endpoints as exact algebraics: 1/sqrt(q) for rational q ; here q = 19 and 28
import math
QMAX=max_mu2.a; QMIN=min_nu2.a
say(f"    INTERVAL:  a in ( 1/sqrt({QMIN}) , 1/sqrt({QMAX}) ) = ( {float(1/QMIN)**0.5:.9f} , {float(1/QMAX)**0.5:.9f} )")
a15=F(1,5)
say(f"    a = 1/5 = 0.2 inside?  1/{QMIN} < 1/25 < 1/{QMAX}  <=>  {QMAX} < 25 < {QMIN} : {QMAX<25<QMIN}")
assert QMAX<25<QMIN

# ---- 3. CROSS-CHECK: recompute dmin/dmax directly at exact rational a ---------
say("")
say("[4] cross-check NOT using homothety: recompute every offset's (dmin^2,dmax^2) directly at each a")
tests=[("just outside, below", F(188,1000), False),
       ("closed endpoint (rational subinterval)", F(19,100), True),
       ("a = 1/5", F(20,100), True),
       ("closed endpoint (rational subinterval)", F(22,100), True),
       ("just outside, above", F(230,1000), False)]
for label,av,expect in tests:
    def ok_at(v):
        r=ranges(v[0],v[1],t(av)); return r[0]<Q3(1) and Q3(1)<r[1]
    ok=all(ok_at(v) for v in Fs)
    bad=[v for v in Fs if not ok_at(v)]
    say(f"    a = {av} (~{float(av):.6f}) [{label}] : all 42 strictly forced = {ok}"
        + ("" if ok else f"   ; failing offsets: {bad[:4]}{' ...' if len(bad)>4 else ''}"))
    assert ok==expect, (av,ok,expect)
say("    -> the direct computation agrees with the homothety-derived interval at both ends.")
# exact rational closed subinterval with strict margins
lo_r, hi_r = F(19,100), F(22,100)
say("")
say(f"[5] modest RATIONAL closed subinterval  [{lo_r}, {hi_r}]  = [{float(lo_r)}, {float(hi_r)}]")
say(f"    lower margin:  (19/100)^2 = 361/10000 vs 1/28 = 1/28 -> 361*28 = {361*28} > 10000  {361*28>10000}")
say(f"    upper margin:  (22/100)^2 = 484/10000 vs 1/19      -> 484*19 = {484*19} < 10000  {484*19<10000}")
assert F(19,100)**2 > F(1,28) and F(22,100)**2 < F(1,19)
say("    both strict in exact integer arithmetic, so [19/100, 22/100] lies strictly inside the open interval.")
say("")
say("CONCLUSION (conditional on the 73-cell 6-UNSAT certificate being independently accepted):")
say("  for EVERY a in (1/sqrt28, 1/sqrt19) = (0.188982, 0.229416), and in particular for every")
say("  a in [0.19, 0.22], no colouring of the plane constant on honeycomb cell interiors uses six")
say("  colours.  Same 42 offsets, same 888 edges, same CNF, same refutation; the interval is")
say("  non-empty and open, with 1/sqrt28 and 1/sqrt19 the exact binding endpoints.")
json.dump({"claim":"the 42 offsets stay strictly forced for a in (1/sqrt28,1/sqrt19)",
           "homothety":"dmin(v,a)=a*dmin(v,1), dmax(v,a)=a*dmax(v,1)",
           "per_offset_at_a_eq_1":rows,
           "binding":{"max_mu2":[str(max_mu2),N_of_maxmu],"min_nu2":[str(min_nu2),N_of_minnu]},
           "open_interval":{"lo":"1/sqrt(28)","hi":"1/sqrt(19)",
                            "lo_float":float(1/QMIN)**0.5,"hi_float":float(1/QMAX)**0.5},
           "rational_closed_subinterval":{"lo":"19/100","hi":"22/100",
              "lo_margin":"(19/100)^2 > 1/28 : 361*28=10108 > 10000",
              "hi_margin":"(22/100)^2 < 1/19 : 484*19=9196 < 10000"},
           "certificate_reused":{"cnf":"p19.cnf","drup":"p19.drup","steps":42109},
           "conditional_on":"independent acceptance of the 73-cell 6-UNSAT certificate"},
          open('interval_cert.json','w'))
open('interval_a.out','w').write("\n".join(out)+"\n")
print(f"\nwrote interval_cert.json, interval_a.out  ({time.time()-t0:.2f}s total)")
