#!/usr/bin/env python3
"""X-R03b (corrected): SDP -> round the CHOLESKY FACTOR -> exact SOS -> exact CE2 certificate.

Why: rounding the Gram matrix or its coefficients destroys H >= 0 (I made that error and the
resulting 0.810774751 claim was invalid: the rounded H had negative coefficients).  Rounding a
FACTOR L with H = |L^T v|^2 keeps H an explicit sum of squares, so CE1 holds exactly:
    H(s) = sum_j q_j(s)^2 >= 0  for all real s, hence P = -(s-4)H <= 0 for s >= 4.
Then CE2 (Q >= 0 on [0,inf)) is decided exactly, and the bound (4/(3 sqrt pi)) P(0)/Q(0) is proved.
"""
import sys, numpy as np, sympy as sp
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import importlib.util
spec=importlib.util.spec_from_file_location("sdpmod","x_r03b_sdp.py"); M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
import ce_exact_gauss as G
from exact_sign import sign_on_half_line as exact_sign
from sympy import Rational as R
s_=G.s_

def factor_round(Gf, m, den):
    w,V=np.linalg.eigh((Gf+Gf.T)/2)
    w=np.clip(w,0,None)
    L=V@np.diag(np.sqrt(w))                  # Gf ~ L L^T
    return [[Fr(L[i,j]).limit_denominator(den) for j in range(m+1)] for i in range(m+1)]

def H_from_qs(qs):
    return sp.expand(sum(q**2 for q in qs))

def build_qs(Lr, m):
    # rows of Lr give q_j = sum_i Lr[i,j] s^i   (so H = sum_j q_j^2 = v^T (Lr Lr^T) v)
    qs=[]
    for j in range(m+1):
        qs.append(sum(R(Lr[i][j].numerator,Lr[i][j].denominator)*s_**i for i in range(m+1)))
    return [q for q in qs if q!=0]

def cert_from(Lr, m):
    qs=build_qs(Lr,m); H=H_from_qs(qs)
    P=sp.expand(-(s_-4)*H); Q=sp.expand(G.apply_map(P))
    P0=sp.expand(P).subs(s_,0); Q0=Q.subs(G.v_,0)
    if P0<=0 or Q0<=0: return None
    if not exact_sign(Q,0,+1,var=G.v_): return None
    return P0/Q0, float(R(4,3)/sp.sqrt(sp.pi)*P0/Q0), H, qs, Q

print("%-3s %-14s %-12s %s" % ("m","SDP value","density","certified"))
best=None
for m in range(1,6):
    out,msg=M.sdp2(m)
    if out is None: print("%-3d %-14s %s" % (m,"-",msg)); continue
    val,Gf,Af,Bf=out
    got=None
    for den in (10**4,10**5,10**6,10**8):
        Lr=factor_round(Gf,m,den)
        r=cert_from(Lr,m)
        if r: got=r; break
    if got is None:
        print("%-3d %-14.6f %-12s %s" % (m,val,"-","no (rounding of the factor still broke CE2)"))
        continue
    print("%-3d %-14.6f %-12.9f %s" % (m,val,got[1],"YES  P0/Q0=%s" % str(sp.nsimplify(got[0]))[:14]))
    if best is None or got[1]<best[1]: best=(m,got)
print("-"*66)
if best:
    m,got=best
    print("BEST CERTIFIED: m=%d  density=%.9f" % (m,got[1]))
    print("  H(s) =", sp.factor(got[2]))
    print("  q_j  =", [sp.factor(q) for q in got[3]])
    print("  CE1: H = sum q_j^2 >= 0 exactly;  CE2: Q >= 0 on [0,inf) exact.")
    print("  reference: Kepler 0.740480489 ; CDS22 CE 0.779747 ; Li's CE floor ~0.770657 ;")
    print("             previous X best 0.818086808 (from the explicit SOS descent)")
else:
    print("no certified value from this route; the explicit SOS descent's 0.818086808 stands")
