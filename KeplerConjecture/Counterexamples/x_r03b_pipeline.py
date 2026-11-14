#!/usr/bin/env python3
"""X-R03b pipeline: SDP (search) -> rational rounding -> feasibility descent -> EXACT certificate.
The SDP is only a search device; the reported number is always the exact-certificate value."""
import sys, numpy as np, sympy as sp, cvxpy as cp
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
s_=G.s_
import importlib.util
_spec=importlib.util.spec_from_file_location("sdpmod","x_r03b_sdp.py")
_sdpmod=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_sdpmod)
sdp2=_sdpmod.sdp2
from exact_sign import sign_on_half_line as exact_sign
from sympy import Rational as R

def poly_from_h(h, s_):
    return sum(R(h[k].numerator, h[k].denominator)*s_**k for k in range(len(h)))

def cert(h):
    P=sp.expand(-(s_-4)*poly_from_h(h,s_))
    Q=sp.expand(G.apply_map(P))
    P0=sp.expand(P).subs(s_,0); Q0=Q.subs(G.v_,0)
    if P0<=0 or Q0<=0: return None
    if not exact_sign(Q,0,+1,var=G.v_): return None
    return P0/Q0, float(R(4,3)/sp.sqrt(sp.pi)*P0/Q0), P, Q

def extract_h(Gv, m):
    hs=[]
    for k in range(2*m+1):
        e=0.0
        for i in range(m+1):
            j=k-i
            if 0<=j<=m: e+=Gv[i,j]
        hs.append(Fr(e).limit_denominator(10**7))
    return hs

def descend(h, steps=(Fr(1,64),Fr(1,256),Fr(1,1024),Fr(1,4096)), rounds=6):
    best=cert(h)
    if best is None: return None,None
    for _ in range(rounds):
        improved=False
        for k in range(len(h)):
            for st in steps:
                for sgn in (1,-1):
                    h2=list(h); h2[k]=h2[k]+sgn*st
                    r=cert(h2)
                    if r and r[0]<best[0]: best=r; h=h2; improved=True
        if not improved: break
    return h,best

if __name__=="__main__":
    print("%-3s %-14s %-14s %-12s %s" % ("m","SDP P0/Q0","after descent","density","certified"))
    best=None
    for m in range(1,6):
        out,msg=sdp2(m)
        if out is None:
            print("%-3d %-14s %s" % (m,"-",msg)); continue
        val,Gv,Av,Bv=out
        h=extract_h(Gv,m)
        # 1) direct rounding
        r=cert(h)
        if r is None:
            # 2) shrink slightly toward a feasible point, then descend
            for scale in (Fr(999,1000),Fr(95,100),Fr(9,10)):
                h2=[x*scale for x in h]
                r=cert(h2)
                if r: h=h2; break
        if r is None:
            h3,best3=descend(h)
            r=best3
        if r is None:
            print("%-3d %-14.6f %-14s %-12s %s" % (m,val,"failed","-","no"))
            continue
        r0=r[0]
        h2,b2=descend(h)
        if b2 and b2[0]<r0: r=b2; r0=b2[0]
        print("%-3d %-14.6f %-14s %-12.9f %s" % (m,val,str(sp.nsimplify(r0))[:14],r[1],"YES"))
        if best is None or r[1]<best[1]: best=(m,r[0],r[1],r[2])
    print("-"*70)
    if best:
        m,r0,dens,P=best
        print("BEST CERTIFIED: m=%d  P(0)/Q(0)=%s  density=%.9f" % (m,sp.nsimplify(r0),dens))
        print("  P(s) =", sp.factor(P))
        print("  (my previous best structural bound was 0.818086808; Kepler 0.740480489;")
        print("   C's K33 0.77996650; CDS22 CE 0.779747; Li's floor for CE volume density ~0.770657)")
