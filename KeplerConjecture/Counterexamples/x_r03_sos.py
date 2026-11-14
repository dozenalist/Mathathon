#!/usr/bin/env python3
"""X-R03 structured SOS attempt: CE1 holds BY CONSTRUCTION, only CE2 is searched.

Family:  H(s) = sum_{j=1..r} q_j(s)^2  with q_j in Q[s] of degree <= m,
         P(s) = -(s-4) H(s)     =>  P <= 0 on [4,inf) automatically (H >= 0, -(s-4) <= 0).
         f = P(s) e^{-s},  f^ = pi^{3/2} Q(v) e^{-v}  via the exact map.
Certificate requires only: Q(v) >= 0 for v >= 0, which is decided EXACTLY (Sturm +
even-multiplicity handling).  Density = (4/(3 sqrt pi)) P(0)/Q(0).
"""
import sys, itertools, random
import sympy as sp
from fractions import Fraction as Fr
import ce_exact_gauss as G
s_=G.s_

def build_H(qs):
    H=sp.expand(sum(q**2 for q in qs))
    return sp.expand(-(s_-4)*H)

def bound_of(P):
    Q=sp.expand(G.apply_map(P))
    P0=sp.expand(P).subs(s_,0); Q0=Q.subs(G.v_,0)
    if P0<=0 or Q0<=0: return None
    ok,r=G.sign_on_half_line(Q,0,+1)
    if not ok: return None, r
    return (sp.nsimplify(P0/Q0), Q, P0, Q0)

def search(m, r, trials, seed=0, span=6):
    rng=random.Random(seed); best=None
    pool=[Fr(k,2) for k in range(-span*2,span*2+1)]
    for t in range(trials):
        qs=[]
        for j in range(r):
            c=[sp.Rational(rng.choice(pool)) for _ in range(m+1)]
            if all(x==0 for x in c): c[0]=sp.Integer(1)
            qs.append(sum(c[i]*s_**i for i in range(m+1)))
        P=build_H(qs); out=bound_of(P)
        if out and out[0] is not None:
            val,Q,P0,Q0=out[0],out[1],out[2],out[3]
            dens=sp.Rational(4,3)/sp.sqrt(sp.pi)*val
            if best is None or val<best[0]:
                best=(val,Q,P0,Q0,qs,dens)
    return best

if __name__=="__main__":
    print("CE1 is structural (P = -(s-4)*SOS). Searching CE2.")
    print("%-3s %-3s %-9s %-10s %-11s %s" % ("m","r","trials","P0/Q0","density","< Kepler?"))
    bestall=None
    for (m,r,trials) in [(1,2,300),(1,3,300),(2,2,300),(2,3,300),(3,2,200),(3,3,200)]:
        b=search(m,r,trials,seed=m*10+r)
        if b:
            val,Q,P0,Q0,qs,dens=b
            kk=G.kepler_ok(P0,Q0)
            print("%-3d %-3d %-9d %-10s %-11.6f %s" % (m,r,trials,str(val)[:10],float(dens),kk))
            if bestall is None or float(dens)<bestall[4]: bestall=(m,r,val,qs,float(dens))
        else:
            print("%-3d %-3d %-9d %-10s %-11s %s" % (m,r,trials,"-","-","no certified candidate"))
    print("-"*64)
    if bestall:
        m,r,val,qs,dens=bestall
        print("BEST CERTIFIED (SOS family): m=%d r=%d  P0/Q0=%s  density=%.9f" % (m,r,val,dens))
        print("  q_j:", [sp.factor(q) for q in qs])
        print("  STATUS: PROVED bound %.9f for all unit-ball packings (CE1 structural, CE2 exact)." % dens)
        print("  This is a valid but weak certificate; it is the pipeline, not a competitive value.")
    else:
        print("No certified candidate in the search; CE1 remains structural, CE2 unmet.")
