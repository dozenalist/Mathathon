#!/usr/bin/env python3
"""Both-sides explicit rational Gram, corrected identity.

Identity (matching sdp_R's basis (s/S)^i exactly):
    Q_k = S^{-k} sum_{i+j=k} A_ij  +  S^{-(k-1)} sum_{i+j=k-1} B_ij        (B-term only for k>=1)
with H = v^T G v, v_i = (s/S)^i, and Q = M p the Fourier image of p = -(s-4)H.
Earlier attempts used S^{-k} for BOTH blocks, which is wrong and is why the projection failed.
"""
import sys, numpy as np, sympy as sp, json
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
s_=G.s_

def build(m,S):
    N=2*m+1
    rows=G.fourier_map_matrix(N); polys=[]
    for n in range(N+1):
        e=sp.expand(rows[n]); sy=e.free_symbols
        polys.append(sp.Poly(e, list(sy)[0] if sy else sp.Symbol('w')))
    def Mcoef(k,n):
        if polys[n].free_symbols:
            c=polys[n].coeff_monomial(sp.Symbol('w')**k); return 0.0 if c is None else float(c)
        return float(polys[n].as_expr()) if k==0 else 0.0
    Ml=[[Mcoef(k,n) for n in range(N+1)] for k in range(N+1)]
    ent=[(i,j) for i in range(m+1) for j in range(i,m+1)]
    n=len(ent)
    L=np.zeros((N+1, 3*n))
    for k in range(N+1):
        # Q_k = sum_n Ml[k][n] ps_n ; ps_n = 4 h_n - h_{n-1} ; h_j = S^{-j} sum_{i+j} G
        for nidx in range(N+1):
            c=Ml[k][nidx]
            if c==0: continue
            for mult, off in ((4.0,0),(-1.0,1)):
                j=nidx-off
                if j<0 or j>2*m: continue
                for ei,(a,b) in enumerate(ent):
                    if a+b==j: L[k,ei] += c*mult*(1 if a==b else 2)*S**(-j)
        if k<=2*m:
            for ei,(a,b) in enumerate(ent):
                if a+b==k: L[k,n+ei] -= (1 if a==b else 2)*S**(-k)
        if 1<=k<=2*m+1:
            for ei,(a,b) in enumerate(ent):
                if a+b==k-1: L[k,2*n+ei] -= (1 if a==b else 2)*S**(-(k-1))
    return L, ent, n

def joint_sdp(m,S,eps):
    import cvxpy as cp
    N=2*m+1
    rows=G.fourier_map_matrix(N); polys=[]
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
        return e*S**(-k)
    ps=[4*hco(n,Gv)-(hco(n-1,Gv) if n-1>=0 else 0) for n in range(N+1)]
    Qc=[sum(Ml[k][n]*ps[n] for n in range(N+1)) for k in range(N+1)]
    ac=[hco(k,Av) if k<=2*m else 0 for k in range(N+1)]
    bc=[hco(k,Bv) if k<=2*m else 0 for k in range(N+1)]
    for k in range(N+1):
        cons.append(Qc[k]==ac[k]+(bc[k-1] if k>=1 else 0))
    cons.append(Qc[0]==1)
    prob=cp.Problem(cp.Minimize(4*hco(0,Gv)),cons); prob.solve(solver=cp.CLARABEL,verbose=False)
    return dict(status=prob.status,val=float(prob.value),G=np.array(Gv.value),A=np.array(Av.value),B=np.array(Bv.value))

def ldl_psd(M):
    """exact PSD test via rational LDL^T (no pivoting); returns (psd, min pivot)."""
    n=M.rows; A=sp.Matrix(M); L=sp.eye(n); D=[sp.Integer(0)]*n; cur=A[:,:]
    for k in range(n):
        d=cur[k,k]
        D[k]=d
        if d==0:
            # zero pivot: PSD iff the whole remaining block is zero on the diagonal row
            if any(cur[k,j]!=0 for j in range(k,n)): return False, sp.Integer(0)
            continue
        for i in range(k+1,n):
            f=cur[i,k]/d
            L[i,k]=f
            for j in range(k,n): cur[i,j]=cur[i,j]-f*cur[k,j]
    return all(d>=0 for d in D), min(D)

if __name__=="__main__":
    for (m,S,eps) in [(2,4,1e-3),(3,6,1e-3),(3,6,1e-2),(4,8,1e-2)]:
        out=joint_sdp(m,S,eps)
        if out['status'] not in ('optimal','optimal_inaccurate'):
            print("m=%d S=%d eps=%g status=%s"%(m,S,eps,out['status'])); continue
        L,ent,n=build(m,S)
        x=np.zeros(3*n)
        for k,(a,b) in enumerate(ent):
            x[k]=out['G'][a,b]; x[n+k]=out['A'][a,b]; x[2*n+k]=out['B'][a,b]
        r=L@x
        # float projection onto ker L
        corr=L.T@np.linalg.lstsq(L@L.T, r, rcond=None)[0]
        xp=x-corr
        def mats(xv):
            Gm=np.zeros((m+1,m+1)); Am=np.zeros((m+1,m+1)); Bm=np.zeros((m+1,m+1))
            for k,(a,b) in enumerate(ent):
                Gm[a,b]=Gm[b,a]=xv[k]; Am[a,b]=Am[b,a]=xv[n+k]; Bm[a,b]=Bm[b,a]=xv[2*n+k]
            return Gm,Am,Bm
        Gm,Am,Bm=mats(xp)
        mar=[np.linalg.eigvalsh(M).min() for M in (Gm,Am,Bm)]
        print("m=%d S=%d eps=%-5g |Lx|=%.1e  projected margins G,A,B = %.2e, %.2e, %.2e"
              % (m,S,eps,np.abs(r).max(),*mar))
        if min(mar)>-1e-6:
            # rationalise and repair the identity exactly by solving for 12 chosen unknowns
            xr=[sp.nsimplify(Fr(v).limit_denominator(10**6)) for v in xp]
            xv=sp.Matrix(xr); Lm=sp.Matrix([[sp.nsimplify(v) for v in row] for row in L])
            res=Lm*xv
            # choose 12 unknowns with the largest |column| to solve for
            cols=[(sum(abs(Lm[k,j]) for k in range(Lm.rows)), j) for j in range(Lm.cols)]
            cols.sort(reverse=True); chosen=[j for _,j in cols[:Lm.rows]]
            free=[j for j in range(Lm.cols) if j not in chosen]
            A11=Lm[:,chosen]; rhs=-Lm[:,free]*sp.Matrix([xv[j] for j in free])
            try:
                sol=A11.LUsolve(rhs)
                for idx,j in enumerate(chosen): xv[j]=sp.nsimplify(sol[idx])
                res2=Lm*xv
                exact=all(sp.simplify(v)==0 for v in res2)
                # EXACT: build the matrices from the RATIONAL solution, not from floats
                def matsQ(xq):
                    Gm=sp.zeros(m+1,m+1); Am=sp.zeros(m+1,m+1); Bm=sp.zeros(m+1,m+1)
                    for k,(a,b) in enumerate(ent):
                        Gm[a,b]=Gm[b,a]=xq[k]; Am[a,b]=Am[b,a]=xq[n+k]; Bm[a,b]=Bm[b,a]=xq[2*n+k]
                    return Gm,Am,Bm
                Gm2,Am2,Bm2=matsQ([sp.nsimplify(v) for v in xv])
                assert all(v.is_rational for v in list(Gm2)+list(Am2)+list(Bm2)), "non-rational entry!"
                pG,mG=ldl_psd(Gm2); pA,mA=ldl_psd(Am2); pB,mB=ldl_psd(Bm2)
                print("     exact identity=%s ; PSD exact G=%s A=%s B=%s ; min pivots %.2e %.2e %.2e"
                      % (exact,pG,pA,pB,float(mG),float(mA),float(mB)))
                if exact and pG and pA and pB:
                    json.dump({"m":m,"S":S,
                               "G":[[str(sp.Rational(Gm2[i,j])) for j in range(m+1)] for i in range(m+1)],
                               "A":[[str(sp.Rational(Am2[i,j])) for j in range(m+1)] for i in range(m+1)],
                               "B":[[str(sp.Rational(Bm2[i,j])) for j in range(m+1)] for i in range(m+1)],
                               "note":"BOTH-SIDES explicit rational Gram; identity exact, all three PSD exact"},
                              open('X_C015_bothsides_gram.json','w'),indent=1)
                    print("     *** SAVED X_C015_bothsides_gram.json ***")
                    break
            except Exception as e:
                print("     rational repair failed:",type(e).__name__,str(e)[:50])
