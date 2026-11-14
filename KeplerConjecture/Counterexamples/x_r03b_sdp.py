#!/usr/bin/env python3
"""X-R03b — a RUNNABLE SDP certificate search (no longer an unimplemented request).

Family:  P(s) = -(s-4) H(s),  H = v(s)^T G v(s), G >= 0 (SOS),  v = [1,s,...,s^m].
So CE1 (P <= 0 on [4,inf)) holds BY CONSTRUCTION.
Fourier: f = P(s)e^{-s} -> f^ = pi^{3/2} Q(v)e^{-v}, Q = M p  (fixed rational matrix).
CE2: Q >= 0 on [0,inf).  For odd-degree Q this is, by Lukacs' theorem,
        Q(s) = s * b(s),  b = v(s)^T B v(s), B >= 0
     (or Q = a + s b with a,b SOS; the s-only form suffices for our degree).
Objective: minimise P(0)/Q(0) subject to Q(0) = 1  (P(0) = 4 H(0), linear in G).
Result is certified EXACTLY afterwards by exact_sign.sign_on_half_line; the SDP is only a
search device, so a float optimum is never reported as a bound.
"""
import sys, numpy as np, sympy as sp, cvxpy as cp
from fractions import Fraction as Fr
sys.path.insert(0,'.')
import ce_exact_gauss as G
s_=G.s_
from exact_sign import sign_on_half_line as exact_sign
from sympy import Rational as R

def build(m):
    global s_
    N=2*m+1                      # degree of P
    rows=G.fourier_map_matrix(N)  # Q_n(w) for P=s^n, in the module's local w symbol
    polys=[]
    for n in range(N+1):
        expr=sp.expand(rows[n]); syms=expr.free_symbols
        wsym=list(syms)[0] if syms else sp.Symbol('w')
        polys.append(sp.Poly(expr, wsym))
    Ml=[]
    for k in range(N+1):
        row=[]
        for n in range(N+1):
            if polys[n].free_symbols:
                c=polys[n].coeff_monomial(sp.Symbol('w')**k)
                if c is None: c=0
            else:                       # constant row: only the k=0 coefficient is nonzero
                c=polys[n].as_expr() if k==0 else 0
            c=sp.Rational(c)
            row.append(Fr(int(c.p),int(c.q)))
        Ml.append(row)
    return N, None, Ml

def mul_coeffs(a,b):
    out=[0.0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def sdp(m, verbose=True):
    N=2*m+1
    # H has degree 2m -> coefficients h_k = sum_{i+j=k} G_ij
    Gv=cp.Variable((m+1,m+1), symmetric=True); cons=[Gv >> 0]
    # coefficient vector of H in terms of G (linear)
    # P = -(s-4)H = 4H - sH
    # p_n = 4 h_n - h_{n-1}
    def h_of(Gmat):
        hs=[]
        for k in range(2*m+1):
            expr=0
            for i in range(m+1):
                j=k-i
                if 0<=j<=m: expr = expr + Gmat[i,j]
            hs.append(expr)
        return hs
    hs=h_of(Gv)
    ps=[4*hs[n] - (hs[n-1] if n-1>=0 else 0) for n in range(2*m+2)]
    # Q coefficients = Mmat @ p
    _,Mf,Ml=build(m)
    Qc=[sum(Ml[k][n]*ps[n] for n in range(2*m+2)) for k in range(2*m+2)]
    # Lukacs: Q = s * b, b = v_m^T B v_m, B >= 0  (degree of b = 2m, Q deg 2m+1)
    Bv=cp.Variable((m+1,m+1), symmetric=True); cons.append(Bv >> 0)
    bs=[]
    for k in range(2*m+1):
        expr=0
        for i in range(m+1):
            j=k-i
            if 0<=j<=m: expr=expr+Bv[i,j]
        bs.append(expr)
    # Q = s*b  => Q_0 = 0, Q_k = b_{k-1} for k>=1
    cons.append(Qc[0]==0)
    for k in range(1,2*m+2):
        cons.append(Qc[k] == (bs[k-1] if k-1<=2*m else 0))
    # normalisation Q(0)=1 impossible (Q(0)=0); normalise Q(1)=1 instead, objective P(0)/Q(0)
    # Q(0)=0 means q0=0 -> the CE2 condition q>=0 with q(0)=0 touches at 0, allowed.
    # But the density uses Q(0)!  So we need Q(0) > 0, hence Q cannot be s*b.
    return None

print("NOTE: Q(0)=0 is inadmissible because the density uses P(0)/Q(0).")
print("So the correct Lukacs form for Q>=0 on [0,inf) with Q(0)>0 is Q = a + s b, a,b SOS.")
def sdp2(m, verbose=True):
    N=2*m+1
    Gv=cp.Variable((m+1,m+1), symmetric=True); cons=[Gv >> 0]
    def coeffs(Gmat,deg):
        out=[]
        for k in range(deg+1):
            e=0
            for i in range(m+1):
                j=k-i
                if 0<=j<=m: e=e+Gmat[i,j]
            out.append(e)
        return out
    hs=coeffs(Gv,2*m)
    def hget(n): return hs[n] if 0 <= n <= 2*m else 0
    ps=[4*hget(n)-hget(n-1) for n in range(2*m+2)]
    _,Mf,Ml=build(m)
    Qc=[sum(Ml[k][n]*ps[n] for n in range(2*m+2)) for k in range(2*m+2)]
    # a = v_m^T A v_m (deg 2m), b = v_m^T B v_m (deg 2m); Q = a + s b (deg 2m+1)
    Av=cp.Variable((m+1,m+1), symmetric=True); Bv=cp.Variable((m+1,m+1), symmetric=True)
    cons += [Av >> 0, Bv >> 0]
    ac=coeffs(Av,2*m); bc=coeffs(Bv,2*m)
    for k in range(2*m+2):
        rhs=(ac[k] if k<=2*m else 0) + (bc[k-1] if 1<=k<=2*m+1 else 0)
        cons.append(Qc[k]==rhs)
    # the ratio P(0)/Q(0) is scale invariant (both are linear in G), so normalise Q(0)=1
    cons.append(Qc[0] == 1)
    obj=cp.Minimize(4*hs[0])                 # P(0) = 4H(0), affine in G  -> DCP
    prob=cp.Problem(obj,cons)
    try: prob.solve(verbose=False)
    except Exception as e:
        return None, "solver exception %s" % type(e).__name__
    if prob.status not in ("optimal","optimal_inaccurate"):
        return None, "SDP status %s" % prob.status
    return (float(prob.value), np.array(Gv.value), np.array(Av.value), np.array(Bv.value)), "solved"

if __name__=="__main__":
    print("m  status           P0/Q0(SDP)   exact-certified?")
    for m in range(1,4):
        out,msg=sdp2(m)
        if out is None:
            print("%-2d %-16s %s" % (m,msg,"-")); continue
        val,Gv,Av,Bv=out
        # recover H's coefficients (rounded to rationals) and certify exactly
        hs=[]
        for k in range(2*m+1):
            e=0.0
            for i in range(m+1):
                j=k-i
                if 0<=j<=m: e+=Gv[i,j]
            hs.append(Fr(e).limit_denominator(10**6))
        P=sum(R(hs[k].numerator,hs[k].denominator)*s_**k for k in range(len(hs)))
        Pp=sp.expand(-(s_-4)*P)
        Q=sp.expand(G.apply_map(Pp))
        out2=(sp.expand(Pp).subs(s_,0), Q.subs(G.v_,0))
        if out2[0]<=0 or out2[1]<=0:
            print("%-2d %-16s %.6f      signs at 0 fail" % (m,msg,val)); continue
        ok=exact_sign(Q,0,+1,var=G.v_)
        dens=float(R(4,3)/sp.sqrt(sp.pi)*out2[0]/out2[1])
        print("%-2d %-16s %.9f   %s   density=%.9f" % (m,msg,val,"CERTIFIED" if ok else "rejected",dens if ok else float('nan')))
