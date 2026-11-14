#!/usr/bin/env python3
"""Both-sides Gram with a margin on G as well.

Key observation: P = -(s-4)H gives P(4) = 0 for ANY H, so H need not vanish at s=4 and G need
not be singular.  The earlier m>=5 failures came from G's smallest eigenvalue sitting at ~0 by
coincidence at the SDP optimum, which exact rounding then broke.  Forcing G >= eps_G * I makes
the rational rounding safe at the price of a slightly weaker bound.
"""
import sys, numpy as np, sympy as sp, json
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
import cvxpy as cp
s_=G.s_
def joint(m,S,epsAB,epsG):
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
    cons=[Gv>>epsG*np.eye(m+1), Av>>epsAB*np.eye(m+1), Bv>>epsAB*np.eye(m+1)]
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
    for k in range(N+1): cons.append(Qc[k]==ac[k]+(bc[k-1] if k>=1 else 0))
    cons.append(Qc[0]==1)
    pr=cp.Problem(cp.Minimize(4*hco(0,Gv)),cons); pr.solve(solver=cp.CLARABEL,verbose=False)
    return dict(status=pr.status,G=np.array(Gv.value),A=np.array(Av.value),B=np.array(Bv.value))
def build(m,S):
    N=2*m+1
    rows=G.fourier_map_matrix(N)
    polys=[]
    for n in range(N+1):
        e=sp.expand(rows[n]); sy=e.free_symbols
        polys.append(sp.Poly(e, list(sy)[0] if sy else sp.Symbol('w')))
    Ml=[]
    for k in range(N+1):
        row=[]
        for n in range(N+1):
            if polys[n].free_symbols:
                c=polys[n].coeff_monomial(sp.Symbol('w')**k); row.append(0 if c is None else c)
            else: row.append(polys[n].as_expr() if k==0 else 0)
        Ml.append(row)
    ent=[(i,j) for i in range(m+1) for j in range(i,m+1)]; n=len(ent)
    L=np.zeros((N+1,3*n))
    for k in range(N+1):
        for nidx in range(N+1):
            c=Ml[k][nidx]
            if c==0: continue
            for mult,off in ((4.0,0),(-1.0,1)):
                j=nidx-off
                if j<0 or j>2*m: continue
                for ei,(a,b) in enumerate(ent):
                    if a+b==j: L[k,ei]+=c*mult*(1 if a==b else 2)*S**(-j)
        if k<=2*m:
            for ei,(a,b) in enumerate(ent):
                if a+b==k: L[k,n+ei]-=(1 if a==b else 2)*S**(-k)
        if 1<=k<=2*m+1:
            for ei,(a,b) in enumerate(ent):
                if a+b==k-1: L[k,2*n+ei]-=(1 if a==b else 2)*S**(-(k-1))
    return L,ent,n
def rat(x):
    f=sp.Rational(sp.cancel(sp.together(x))); assert f.is_rational; return f
def ldl_ok(M):
    nn=M.rows; cur=M[:,:]
    for k in range(nn):
        dd=cur[k,k]
        if dd<0: return False
        if dd==0:
            if any(cur[k,j]!=0 for j in range(k,nn)): return False
            continue
        for i in range(k+1,nn):
            f=cur[i,k]/dd
            for j in range(k,nn): cur[i,j]=cur[i,j]-f*cur[k,j]
    return True
best=None
print("%-3s %-4s %-8s %-8s %-14s %-10s %s"%("m","S","epsG","epsAB","P0/Q0","density","ok"))
for (m,S) in [(5,8)]:
    for epsG in (1e-2,):
        try: out=joint(m,S,1e-6,epsG)
        except Exception as e:
            print("%-3d %-4d %-8g solver exc %s"%(m,S,epsG,type(e).__name__)); continue
        if out['status'] not in ('optimal','optimal_inaccurate'):
            print("%-3d %-4d %-8g status %s"%(m,S,epsG,out['status'])); continue
        L,ent,n=build(m,S)
        x=np.zeros(3*n)
        for k,(a,b) in enumerate(ent):
            x[k]=out['G'][a,b]; x[n+k]=out['A'][a,b]; x[2*n+k]=out['B'][a,b]
        xp=x-L.T@np.linalg.lstsq(L@L.T,L@x,rcond=None)[0]
        xv=[R(Fr(v).limit_denominator(10**8).numerator,Fr(v).limit_denominator(10**8).denominator) for v in xp]
        Lm=sp.Matrix([[sp.Rational(int(sp.Rational(v).p),int(sp.Rational(v).q)) for v in row] for row in L])
        rr,piv=Lm.rref(); chosen=list(piv); free=[j for j in range(Lm.cols) if j not in chosen]
        try:
            sol=Lm[:,chosen].LUsolve(-Lm[:,free]*sp.Matrix([xv[j] for j in free]))
            for idx,j in enumerate(chosen): xv[j]=rat(sol[idx])
        except Exception as e:
            print("%-3d %-4d %-8g LU exc"%(m,S,epsG)); continue
        xvm=sp.Matrix(xv); ident=all(v==0 for v in Lm*xvm)
        Gm=sp.zeros(m+1);Am=sp.zeros(m+1);Bm=sp.zeros(m+1)
        for k,(a,b) in enumerate(ent):
            Gm[a,b]=Gm[b,a]=xv[k]; Am[a,b]=Am[b,a]=xv[n+k]; Bm[a,b]=Bm[b,a]=xv[2*n+k]
        vf=lambda xx: sp.Matrix([xx**i for i in range(m+1)])
        Hb=sp.expand((vf(s_/S).T*Gm*vf(s_/S))[0]); P=sp.expand(-(s_-4)*Hb); Q=sp.expand(G.apply_map(P))
        Qb=sp.expand((vf(G.v_/S).T*Am*vf(G.v_/S))[0]+G.v_*(vf(G.v_/S).T*Bm*vf(G.v_/S))[0])
        link=sp.simplify(Qb-Q)==0
        P0=P.subs(s_,0); Q0=Q.subs(G.v_,0)
        if P0<=0 or Q0<=0: print("%-3d %-4d %-8g signs0 fail"%(m,S,epsG)); continue
        rq=rat(P0/Q0); dens=float(R(4,3)/sp.sqrt(sp.pi)*rq)
        ok=ident and ldl_ok(Gm) and ldl_ok(Am) and ldl_ok(Bm) and link
        print("%-3d %-4d %-8g %-8g %-14.9f %-10.9f %s"%(m,S,epsG,1e-6,float(rq),dens,ok))
        if ok and 0.74048<dens and (best is None or dens<best[0]):
            best=(dens,m,S,epsG,rq,Gm,Am,Bm)
print("-"*80)
if best:
    dens,m,S,epsG,rq,Gm,Am,Bm=best
    print("BEST both-sides: m=%d S=%d epsG=%g density=%.12f"%(m,S,epsG,dens))
    json.dump({"m":m,"S":S,"G":[[str(Gm[i,j]) for j in range(m+1)] for i in range(m+1)],
               "A":[[str(Am[i,j]) for j in range(m+1)] for i in range(m+1)],
               "B":[[str(Bm[i,j]) for j in range(m+1)] for i in range(m+1)],
               "P_over_Q":str(rq),"density":dens},open('X_C017_certificate.json','w'),indent=1)
    print("saved X_C017_certificate.json")
