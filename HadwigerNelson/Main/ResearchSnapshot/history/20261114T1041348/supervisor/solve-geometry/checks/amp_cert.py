"""Exact certificate constructor/validator for the corrected amplifier (AMPLIFIER.md).

One process, exact Fractions, no solver, no search. Three instances:
  I1  k=2, path gadget, n=3, D=3/4            (field Q(sqrt7, sqrt5))
  I2  k=2, path gadget, n=2, D=1/2, theta=pi  (D = 1/2 edge case)
  I3  k=3, diamond,     n=1, D=sqrt3          (Moser spindle control; Q(sqrt3, sqrt11))
For each: exact coordinates, selected generating edges, ALL induced unit edges, distinctness and
count checks against |C_n| <= nV-(n-1), |X| <= 2nV-2n+1, 2nE+1 generating entries, the exact
final-endpoint distance 1, and an exhaustive non-k-colourability check (2^13 / 2^5 / 3^7 cases).
"""
import json, math
from fractions import Fraction as F
from itertools import product

# ---------------- biquadratic field  K = Q(sqrt(p), sqrt(m)), basis (1, sqrt p, sqrt m, sqrt(pm))
class Field:
    def __init__(s,p,m): s.p,s.m=F(p),F(m)
    def el(s,a=0,b=0,c=0,d=0): return (F(a),F(b),F(c),F(d))
    def add(s,x,y): return tuple(x[i]+y[i] for i in range(4))
    def neg(s,x): return tuple(-t for t in x)
    def sub(s,x,y): return s.add(x,s.neg(y))
    def mul(s,x,y):
        a,b,c,d=x; e,f,g,h=y; p,m=s.p,s.m
        return (a*e + p*b*f + m*c*g + p*m*d*h,
                a*f + b*e + m*(c*h + d*g),
                a*g + p*(b*h + d*f) + c*e,
                a*h + b*g + c*f + d*e)
    def is_one(s,x): return x==(F(1),F(0),F(0),F(0))
    def is_zero(s,x): return x==(F(0),F(0),F(0),F(0))
    def rat(s,r): return (F(r),F(0),F(0),F(0))
    def key(s,x): return tuple(x)

def squarefree(n):
    """n>0 rational -> (m squarefree positive int, t rational) with n = m*t^2."""
    n=F(n); num,den=n.numerator,n.denominator
    m=1; ts=1
    for x,sign in ((num,1),(den,-1)):
        i=2
        while i*i<=x:
            e=0
            while x%i==0: x//=i; e+=1
            if e:
                m*= i**(e%2); ts*= i**(e//2) if sign==1 else F(1,i**(e//2))
            i+=1
        if x>1:
            m*=x
            if sign==-1: ts*= F(1,x)
    return m,F(ts)

def build(name,k,gadget,p,qidx,n,theta_pi=False):
    """gadget: list of (x,y) rational tuples; p,q are indices. Returns a full certificate dict."""
    # squared distances in the rational plane (gadget coordinates are rational here except sqrt
    # parts, so we carry gadget coordinates as field elements directly)
    Fld = gadget["field"]; pts = gadget["points"]
    P = pts[qidx]; Pp = pts[p]
    def psub(u,w): return (Fld.sub(u[0],w[0]), Fld.sub(u[1],w[1]))
    v = psub(P,Pp)                                      # displacement, no square roots taken
    v2 = Fld.add(Fld.mul(v[0],v[0]), Fld.mul(v[1],v[1]))   # ||v||^2
    # v2 must be rational
    assert v2[1]==0 and v2[2]==0 and v2[3]==0, v2
    v2r = v2[0]
    D2 = n*n*v2r
    cos = 1 - F(1,2)/D2                     # cos theta = 1 - 1/(2D^2)
    if theta_pi:
        sin_r, sin_sq = F(0), None
    else:
        four_D2_minus_1 = 4*D2 - 1
        assert four_D2_minus_1 >= 0, "D < 1/2: no real theta"
        m,t = squarefree(four_D2_minus_1)
        sin_r, sin_sq = t/(2*D2), m        # sin theta = sin_r * sqrt(sin_sq)
    # the rotation lives in Fld only if sqrt(sin_sq) is in Fld (check) ------------------------
    # basis of Fld is (1, sqrt p, sqrt m). sin theta must be sin_r*sqrt(sin_sq).
    pf, mf = Fld.p, Fld.m
    if sin_sq is None: S=(F(0),F(0),F(0),F(0))
    elif F(sin_sq)==pf and sin_r!=0: S=Fld.el(0,sin_r)
    elif F(sin_sq)==mf and sin_r!=0: S=Fld.el(0,0,sin_r)
    elif sin_r==0: S=Fld.el(0)
    else: raise SystemExit(f"{name}: sin theta needs sqrt({sin_sq}) but field is Q(sqrt{pf},sqrt{mf})")
    C=Fld.rat(cos)
    def rot(z):
        x,y=z
        return (Fld.sub(Fld.mul(x,C),Fld.mul(y,S)), Fld.add(Fld.mul(x,S),Fld.mul(y,C)))
    # chain, translated so that p = 0
    def shift(z,j):
        jv=(Fld.mul(Fld.rat(j),v[0]), Fld.mul(Fld.rat(j),v[1]))
        return (Fld.add(Fld.sub(z[0],Pp[0]),jv[0]), Fld.add(Fld.sub(z[1],Pp[1]),jv[1]))
    chain=[[shift(z,j) for z in pts] for j in range(n)]
    rchain=[[rot(z) for z in copy] for copy in chain]
    allpts=[]; meta=[]
    for j,copy in enumerate(chain):
        for i,z in enumerate(copy): allpts.append(z); meta.append(("A",j,i))
    for j,copy in enumerate(rchain):
        for i,z in enumerate(copy): allpts.append(z); meta.append(("B",j,i))
    # dedupe exactly
    key=lambda z: Fld.key(z)
    uniq={}; order=[]
    for z,mm in zip(allpts,meta):
        kk=key(z)
        if kk not in uniq: uniq[kk]=len(order); order.append(z)
    npts=len(order)
    def d2(u,w):
        dx=Fld.sub(u[0],w[0]); dy=Fld.sub(u[1],w[1])
        return Fld.add(Fld.mul(dx,dx),Fld.mul(dy,dy))
    induced=[(i,j) for i in range(npts) for j in range(i+1,npts) if Fld.is_one(d2(order[i],order[j]))]
    # selected generating edges: images of the gadget's edges in each copy of each chain, plus the end
    E=gadget["edges"]; gen=[]
    for j in range(n):
        for (a,b) in E:
            gen.append((key(chain[j][a]),key(chain[j][b])))
            gen.append((key(rchain[j][a]),key(rchain[j][b])))
    farA=chain[n-1][qidx]; farB=rchain[n-1][qidx]
    gen.append((key(farA),key(farB)))
    gen_distinct={frozenset(g) for g in gen}
    # exact checks
    idx=lambda z: uniq[key(z)]
    gen_ok=all(Fld.is_one(d2(order[idx(a)],order[idx(b)])) for (a,b) in gen_distinct)
    final_ok=Fld.is_one(d2(farA,farB))
    final_distinct=key(farA)!=key(farB)
    adj=[set() for _ in range(npts)]
    for (i,j) in induced: adj[i].add(j); adj[j].add(i)
    # exhaustive non-k-colourability (bounded: 2^13 / 2^5 / 3^7 cases)
    sols=0
    for ass in product(range(k),repeat=npts):
        if all(ass[i]!=ass[j] for (i,j) in induced): sols+=1; break
    return dict(name=name,k=k,n=n,V=len(pts),E=len(E),field=[str(Fld.p),str(Fld.m)],
        D=float(F(n)*math.sqrt(float(v2r))) if v2r else 0.0, v2=str(v2r),
        cos_theta=str(cos), sin_theta=(f"{sin_r}*sqrt({sin_sq})" if sin_sq else "0"),
        chain_points=sum(1 for m_ in meta if m_[0]=="A"), distinct_points=npts,
        bound_chain=f"{n*len(pts)-(n-1)}", bound_total=f"{2*n*len(pts)-2*n+1}",
        generating_entries=len(gen), generating_distinct=len(gen_distinct),
        induced_edges=len(induced), all_generating_are_unit_edges=gen_ok,
        final_edge_unit=final_ok, final_ends_distinct=final_distinct,
        proper_k_colourings=sols, points=[[str(t) for t in z] for z in order],
        induced_edge_list=induced)

# ---------------- the three instances
L=Field(7,5)      # Q(sqrt7, sqrt5)
path_pts=[(L.el(0),L.el(0)), (L.el(F(1,8)),L.el(0,F(3,8))), (L.el(F(1,4)),L.el(0))]
path={"field":L,"points":path_pts,"edges":[(0,1),(1,2)]}
D3=Field(3,11)    # Q(sqrt3, sqrt11)
dia=[(D3.el(0),D3.el(0)),(D3.el(1),D3.el(0)),(D3.el(F(1,2)),D3.el(0,F(1,2))),(D3.el(F(1,2)),D3.el(0,-F(1,2)))]
diamond={"field":D3,"points":dia,"edges":[(0,1),(0,2),(1,2),(0,3),(1,3)]}

certs=[build("k2-path-n3",2,path,0,2,3),
       build("k2-path-n2-D-half",2,path,0,2,2,theta_pi=True),
       build("k3-diamond-n1",3,diamond,2,3,1)]
for c in certs:
    print(f"== {c['name']}: k={c['k']} n={c['n']} |X|={c['distinct_points']} "
          f"(bound <= {c['bound_total']}) induced edges {c['induced_edges']} "
          f"generating {c['generating_distinct']}/{c['generating_entries']} "
          f"final edge unit={c['final_edge_unit']} distinct ends={c['final_ends_distinct']} "
          f"gen-all-unit={c['all_generating_are_unit_edges']} proper {c['k']}-colourings={c['proper_k_colourings']}")
    print(f"   field Q(sqrt{c['field'][0]}, sqrt{c['field'][1]}), cos={c['cos_theta']}, sin={c['sin_theta']}, ||v||^2={c['v2']}, D={c['D']:.6f}")
open("amp_certificates.json","w").write(json.dumps({"instances":certs},indent=1))
print("saved amp_certificates.json")
