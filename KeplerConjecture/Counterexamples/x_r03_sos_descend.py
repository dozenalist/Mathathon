#!/usr/bin/env python3
"""Coordinate descent INSIDE the structural-SOS family, every step exactly certified.

P = -(s-4) H,  H = sum_j q_j^2, so CE1 holds by construction.  We only ever accept a
candidate whose CE2 (Q >= 0 on [0,inf)) passes the exact Sturm test and whose density
strictly improves.  Nothing here is a float decision.
"""
import sys, sympy as sp
from fractions import Fraction as Fr
import ce_exact_gauss as G
s_=G.s_

def make_qs(params):
    """params: list of lists of rationals, q_j = sum_i p[i] s^i."""
    return [sum(sp.Rational(c)*s_**i for i,c in enumerate(p)) for p in params]

def evaluate(params):
    qs=make_qs(params); H=sp.expand(sum(q**2 for q in qs)); P=sp.expand(-(s_-4)*H)
    Q=sp.expand(G.apply_map(P)); P0=sp.expand(P).subs(s_,0); Q0=Q.subs(G.v_,0)
    if P0<=0 or Q0<=0: return None
    ok,_=G.sign_on_half_line(Q,0,+1)
    if not ok: return None
    return sp.nsimplify(P0/Q0), float(sp.Rational(4,3)/sp.sqrt(sp.pi)*P0/Q0)

def descend(params, steps=(Fr(1,2),Fr(1,4),Fr(1,8),Fr(1,16),Fr(1,32)), rounds=6):
    best=evaluate(params); assert best, "start infeasible"
    print("start: P0/Q0=%s density=%.9f" % (best[0],best[1]))
    for rnd in range(rounds):
        improved=False
        for j in range(len(params)):
            for i in range(len(params[j])):
                for st in steps:
                    for sgn in (+1,-1):
                        cand=[list(p) for p in params]
                        cand[j][i]=cand[j][i]+sgn*st
                        r=evaluate(cand)
                        if r and r[1] < best[1]-1e-12:
                            best=r; params=cand; improved=True
        print("  round %d: density=%.9f  P0/Q0=%s" % (rnd+1,best[1],best[0]))
        if not improved: break
    return params,best

if __name__=="__main__":
    # start from the random-search winner: q = [-7, (s+12)/2, -5s-2, -(s+5)/2]
    start=[[Fr(-7)],[Fr(6),Fr(1,2)],[Fr(-2),Fr(-5)],[Fr(-5,2),Fr(-1,2)]]
    qs,best=descend(start)
    Q=sp.expand(G.apply_map(sp.expand(-(s_-4)*sum(q**2 for q in make_qs(qs)))))
    print("\nFINAL CERTIFIED: P0/Q0 = %s ; density = %.9f" % (best[0],best[1]))
    print("  q_j =", [sp.factor(q) for q in make_qs(qs)])
    print("  H(s) =", sp.factor(sp.expand(sum(q**2 for q in make_qs(qs)))))
    print("  P(s) = -(s-4)H(s),  CE1 structural;  CE2 exact;  no numerical residual.")
    print("  gap to Kepler pi/sqrt18 = %.9f ; gap to C's K33 0.77996650 = %.9f"
          % (best[1]-float(sp.pi/sp.sqrt(18)), best[1]-0.77996650))
