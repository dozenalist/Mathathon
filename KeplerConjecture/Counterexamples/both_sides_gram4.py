#!/usr/bin/env python3
"""Both-sides explicit rational Gram, JOINT construction.

Unknowns: G (p-side, H = v^T G v, v_i = (s/S)^i), A, B (q-side, Q = v^T A v + u v^T B v).
Constraints: one linear identity Q(G) = a(A) + u b(B) (12 equations at m=5), and G,A,B >= 0.
The SDP solves it with a LARGE margin so that exact rational rounding survives; then the
rounded triple is projected onto the exact identity and all three are tested PSD exactly.
"""
import sys, numpy as np, sympy as sp, json
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
s_=G.s_

def joint_sdp(m, S, eps, solver='CLARABEL'):
    import cvxpy as cp
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
    Gv=cp.Variable((m+1,m+1),symmetric=True); Av=cp.Variable((m+1,m+1),symmetric=True); Bv=cp.Variable((m+1,m+1),symmetric=True)
    cons=[Gv>>0, Av>>eps*np.eye(m+1), Bv>>eps*np.eye(m+1)]
    def hco(k,M):
        e=0
        for i in range(m+1):
            j=k-i
            if 0<=j<=m: e=e+M[i,j]
        return e/(S**k)
    ps=[4*hco(n,Gv)-(hco(n-1,Gv) if n-1>=0 else 0) for n in range(N+1)]
    Qc=[sum(Ml[k][n]*ps[n] for n in range(N+1)) for k in range(N+1)]
    ac=[hco(k,Av) if k<=2*m else 0 for k in range(N+1)]
    bc=[hco(k,Bv) if k<=2*m else 0 for k in range(N+1)]
    for k in range(N+1):
        cons.append(Qc[k] == ac[k] + (bc[k-1] if 1<=k<=N else 0))
    cons.append(Qc[0]==1)
    prob=cp.Problem(cp.Minimize(4*hco(0,Gv)), cons)
    prob.solve(solver=cp.CLARABEL, verbose=False)
    return dict(status=prob.status, val=float(prob.value), G=np.array(Gv.value),
                A=np.array(Av.value), B=np.array(Bv.value), m=m, S=S, Ml=Ml)

def identity_matrix(m,S,Ml):
    """12 x 63 matrix of the identity Q(G) - a(A) - u b(B) = 0 (homogeneous)."""
    ent=[(i,j) for i in range(m+1) for j in range(i,m+1)]
    n=len(ent)
    L=[[sp.Rational(0)]*(3*n) for _ in range(2*m+2)]
    # Q_k in terms of G: Q_k = sum_n Ml[k][n] * ps_n ; ps_n = 4 h_n - h_{n-1} ; h_k = S^{-k} sum_{i+j=k} G_ij
    for k in range(2*m+2):
        for nidx in range(2*m+2):
            c=Ml[k][nidx]
            if c==0: continue
            for sign,off in ((4,0),(1,1)):     # ps_n = 4 h_n - h_{n-1}
                coef = sp.Rational(c)*(4 if sign==4 else -1)
                kk = nidx - off
                if kk<0 or kk>2*m: continue
                for e_i,e in enumerate(ent):
                    if e[0]+e[1]==kk:
                        L[k][e_i] += coef*sp.Rational(1 if e[0]==e[1] else 2, S**kk)
    for k in range(2*m+2):
        if k<=2*m:
            for e_i,e in enumerate(ent):
                if e[0]+e[1]==k: L[k][n+e_i] -= sp.Rational(1 if e[0]==e[1] else 2, S**k)
        if 1<=k<=2*m+1:
            for e_i,e in enumerate(ent):
                if e[0]+e[1]==k-1: L[k][2*n+e_i] -= sp.Rational(1 if e[0]==e[1] else 2, S**k)
    return sp.Matrix(L), ent

def vec_of(Gm,Am,Bm,ent):
    n=len(ent); x=[sp.Rational(0)]*(3*n)
    for k,e in enumerate(ent):
        x[k]=sp.Rational(Gm[e[0],e[1]]); x[n+k]=sp.Rational(Am[e[0],e[1]]); x[2*n+k]=sp.Rational(Bm[e[0],e[1]])
    return sp.Matrix(x)

def mats_from(x,ent,m):
    n=len(ent); Gm=sp.zeros(m+1); Am=sp.zeros(m+1); Bm=sp.zeros(m+1)
    for k,e in enumerate(ent):
        Gm[e[0],e[1]]=Gm[e[1],e[0]]=x[k]
        Am[e[0],e[1]]=Am[e[1],e[0]]=x[n+k]
        Bm[e[0],e[1]]=Bm[e[1],e[0]]=x[2*n+k]
    return Gm,Am,Bm

if __name__=="__main__":
    m,S=3,6
    for eps in (1e-3,1e-4,1e-5):
        out=joint_sdp(m,S,eps)
        if out['status'] not in ('optimal','optimal_inaccurate'):
            print("m=%d eps=%g status %s" % (m,eps,out['status'])); continue
        Lm,ent=identity_matrix(m,S,out['Ml'])
        x=vec_of(out['G'],out['A'],out['B'],ent)
        r=Lm*x
        resid=max(abs(float(v)) for v in r)
        # rational projection onto ker(Lm): x* = x - L^T (L L^T)^{-1} L x
        LLt=Lm*Lm.T
        try:
            corr=Lm.T*(LLt.inv()*r)
        except Exception as e:
            print("   inverse failed:",type(e).__name__); continue
        xr=x-corr
        r2=Lm*xr
        exact = all(sp.simplify(v)==0 for v in r2)
        Gm,Am,Bm=mats_from(xr,ent,m)
        evG=[complex(v) for v in Gm.eigenvals()]; evA=[complex(v) for v in Am.eigenvals()]; evB=[complex(v) for v in Bm.eigenvals()]
        ok = (min(v.real for v in evG)>=-1e-30 and min(v.real for v in evA)>=-1e-30 and min(v.real for v in evB)>=-1e-30)
        print("m=%d S=%d eps=%-6g |Lx|max=%.1e identity-exact-after-projection=%s PSD(G,A,B)=%s  margins(%.1e,%.1e,%.1e)"
              % (m,S,eps,resid,exact,ok,min(v.real for v in evG),min(v.real for v in evA),min(v.real for v in evB)))
        if exact and ok:
            json.dump({"m":m,"S":S,"G":[[str(Gm[i,j]) for j in range(m+1)] for i in range(m+1)],
                       "A":[[str(Am[i,j]) for j in range(m+1)] for i in range(m+1)],
                       "B":[[str(Bm[i,j]) for j in range(m+1)] for i in range(m+1)],
                       "note":"joint PSD triple; p-side H=v^T G v, q-side Q=v^T A v + u v^T B v"},
                      open('X_C015_bothsides_gram.json','w'),indent=1)
            print("   SAVED X_C015_bothsides_gram.json")
            break
