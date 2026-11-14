#!/usr/bin/env python3
"""HYBRID structural certificate: relax CE1 on the contact shell and pay the count price.

Shell: |x| in [2, rho], rho = 209/100, i.e. s=|x|^2 in [4, S0], S0 = (209/100)^2.
Hybrid theorem (K15-C003 with the count n=12 from K15-C019/E015):
    Delta <= (4 pi/3) * (P(0) + n*eta) / Q(0),   eta >= max{P(s) : 4 <= s <= S0},
provided P <= 0 for s >= S0 and Q >= 0 on [0,inf).
Structural choice:  P(s) = -(s - S0) H(s),  H = sum q_j^2 >= 0,
so P <= 0 for s >= S0 BY CONSTRUCTION, and eta = (S0-4) H(4) (attained at s=4).
CE2 (Q >= 0) is the only thing certified.
"""
import sys, itertools
import sympy as sp
from fractions import Fraction as Fr
import ce_exact_gauss as G
s_=G.s_
S0=Fr(209,100)**2
N=12

def certify(H):
    P=sp.expand(-(s_-sp.Rational(S0.numerator,S0.denominator))*H)
    Q=sp.expand(G.apply_map(P)); P0=sp.expand(P).subs(s_,0); Q0=Q.subs(G.v_,0)
    if P0<=0 or Q0<=0: return None
    ok,_=G.sign_on_half_line(Q,0,+1)
    if not ok: return None
    eta=sp.expand(P.subs(s_,4))              # max on [4,S0] for this shape
    if eta<0: eta=0
    num=P0+N*eta
    if num<=0: return None
    ratio=sp.nsimplify(num/Q0)
    dens=sp.Rational(4,3)/sp.sqrt(sp.pi)*num/Q0
    return ratio, dens, eta, P0, Q0

if __name__=="__main__":
    print("S0 = (209/100)^2 = %.6f ; shell s in [4, S0] ; count price n = %d" % (float(S0),N))
    print("(plain structural certificate for comparison: P = -(s-4)H, density 0.818086808)")
    best=None; tested=0
    pool=[Fr(k,4) for k in range(-12,13)]
    for (a,b,c) in itertools.product(pool,repeat=3):
        if a<=0: continue
        H=sp.Rational(a.numerator,a.denominator)+sp.Rational(b.numerator,b.denominator)*s_ \
          +sp.Rational(c.numerator,c.denominator)*s_**2
        # H must be >= 0 for all s >= 0: require a>=0, b>=0, c>=0 (sufficient)
        if b<0 or c<0: continue
        r=certify(sp.expand(H)); tested+=1
        if r:
            ratio,dens,eta,P0,Q0=r
            if best is None or float(dens)<best[1]:
                best=(H,dens,ratio,eta,P0,Q0)
    print("tested %d positive quadratics H" % tested)
    if best:
        H,dens,ratio,eta,P0,Q0=best
        print("BEST HYBRID: H = %s" % sp.factor(H))
        print("  eta = %.9f  P0 = %.9f  Q0 = %.9f" % (float(eta),float(P0),float(Q0)))
        print("  (P0 + 12 eta)/Q0 = %s = %.9f" % (ratio,float(ratio)))
        print("  density = %.9f   (plain structural bound was 0.818086808)" % dens)
        print("  improvement: %+.6f" % (0.818086808-dens))
    else:
        print("no certified hybrid candidate")
