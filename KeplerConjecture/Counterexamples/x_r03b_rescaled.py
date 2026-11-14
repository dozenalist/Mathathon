#!/usr/bin/env python3
"""Basis-rescaled SDP: H = sum_j q_j^2 with q_j(s) = sum_i L_ij (s/S)^i.

The Gram basis {(s/S)^i} is O(1) on [0,S], which conditions the SDP for m >= 4 (the plain
basis 1,s,...,s^m spans 30^k and the solver fails).  The Fourier map is still applied in s, so
nothing is approximated: H's coefficients are h_k = S^{-k} sum_{i+j=k} G_ij.
"""
import sys, numpy as np, sympy as sp, cvxpy as cp
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from exact_sign import sign_on_half_line as exact_sign
from sympy import Rational as R
s_=G.s_

def sdp_R(m, S, eps=1e-6, solver='CLARABEL', verbose=False):
    N=2*m+1
    rows=G.fourier_map_matrix(N)
    polys=[]
    for n in range(N+1):
        e=sp.expand(rows[n]); sy=e.free_symbols
        polys.append(sp.Poly(e, list(sy)[0] if sy else sp.Symbol('w')))
    def Mcoef(k,n):
        if polys[n].free_symbols:
            c=polys[n].coeff_monomial(sp.Symbol('w')**k); return 0.0 if c is None else float(c)
        return float(polys[n].as_expr()) if k==0 else 0.0
    Ml=[[Mcoef(k,n) for n in range(N+1)] for k in range(N+1)]
    Gv=cp.Variable((m+1,m+1), symmetric=True)
    Av=cp.Variable((m+1,m+1), symmetric=True)
    Bv=cp.Variable((m+1,m+1), symmetric=True)
    cons=[Gv >> 0, Av >> eps*np.eye(m+1), Bv >> eps*np.eye(m+1)]
    def hco(k, M):                      # coefficient of s^k in  sum M_ij (s/S)^{i+j}
        e=0
        for i in range(m+1):
            j=k-i
            if 0<=j<=m: e = e + M[i,j]
        return e / (S**k)
    ps=[4*hco(n,Gv)-(hco(n-1,Gv) if n-1>=0 else 0) for n in range(N+1)]
    Qc=[sum(Ml[k][n]*ps[n] for n in range(N+1)) for k in range(N+1)]
    ac=[hco(k,Av) if k<=2*m else 0 for k in range(N+1)]
    bc=[hco(k,Bv) if k<=2*m else 0 for k in range(N+1)]
    for k in range(N+1):
        cons.append(Qc[k] == ac[k] + (bc[k-1] if 1<=k<=N else 0))
    cons.append(Qc[0] == 1)
    prob=cp.Problem(cp.Minimize(4*hco(0,Gv)), cons)
    try:
        if solver=='CLARABEL': prob.solve(solver=cp.CLARABEL, verbose=verbose)
        else: prob.solve(solver=cp.SCS, eps=1e-10, max_iters=200000, verbose=verbose)
    except Exception as e:
        return None, "solver exception %s" % type(e).__name__
    if prob.status not in ("optimal","optimal_inaccurate"): return None, "status %s" % prob.status
    return (float(prob.value), np.array(Gv.value)), "ok"

def qs_from_G(Gf, m, S, den):
    w,V=np.linalg.eigh((Gf+Gf.T)/2); w=np.clip(w,0,None); L=V@np.diag(np.sqrt(w))
    qs=[]
    for j in range(m+1):
        q=sum(R(Fr(L[i,j]).limit_denominator(den).numerator, Fr(L[i,j]).limit_denominator(den).denominator)
              *(s_/R(S))**i for i in range(m+1))
        if q!=0: qs.append(sp.expand(q))
    return qs

def certify(qs):
    H=sp.expand(sum(q**2 for q in qs)); P=sp.expand(-(s_-4)*H); Q=sp.expand(G.apply_map(P))
    P0=sp.expand(P).subs(s_,0); Q0=Q.subs(G.v_,0)
    if P0<=0 or Q0<=0: return None
    if not exact_sign(Q,0,+1,var=G.v_): return None
    return P0/Q0, float(R(4,3)/sp.sqrt(sp.pi)*P0/Q0), qs

if __name__=="__main__":
    print("%-3s %-6s %-14s %-12s %s" % ("m","S","SDP value","density","certified"))
    best=None
    for m in (3,4,5,6):
        for S in (4, 16, 64):
            for solver in ('CLARABEL','SCS'):
                out,msg=sdp_R(m,S,solver=solver)
                if out is None: continue
                val,Gf=out
                got=None
                for den in (10**4,10**6,10**8):
                    r=certify(qs_from_G(Gf,m,S,den))
                    if r: got=r; break
                if got:
                    print("%-3d %-6d %-14.9f %-12.9f %s" % (m,S,val,got[1],"YES (P0/Q0=%.9f)"%float(got[0])))
                    if best is None or got[1]<best[1]: best=(m,S,got[1],got[0],got[2])
                    break
                else:
                    print("%-3d %-6d %-14.9f %-12s %s" % (m,S,val,"-","no (Li-floor ok? %s)" % (val>=1.024466)))
    print("-"*70)
    if best:
        m,S,dens,ratio,qs=best
        print("BEST: m=%d S=%d density=%.12f P0/Q0=%.12f" % (m,S,dens,float(ratio)))
        print("  q_j =", [sp.factor(q) for q in qs])
        import json
        json.dump({"m":m,"S":S,"density":float(dens),"P0_over_Q0":float(ratio),
                   "q":[[str(c) for c in sp.Poly(q,s_).all_coeffs()] for q in qs]},
                  open('X_C014_certificate.json','w'), indent=1)
        print("  saved X_C014_certificate.json")
