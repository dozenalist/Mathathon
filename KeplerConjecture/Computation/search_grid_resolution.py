#!/usr/bin/env python3
"""K15 search: why the first certified attempts failed -- GRID RESOLUTION, not degree.

Sweeps (degree, grid, margin eps) and reports, for each, whether the rational rounding
survives exact verification. The finding recorded in CERTIFIER.md Addendum 2: at K = 21 and
eps = 1e-7 the 2000-point grid fails exact verification while the 6000-point grid succeeds.
Raising the degree does not fix a failed certificate; refining the grid does.

Run: python3 search_grid_resolution.py      (about 50 s)
"""
import numpy as np
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre
import exactcert as EC
from fractions import Fraction as F

def lag(k,t): return eval_genlaguerre(k,0.5,t)
def bm(ts,K):
    ts=np.asarray(ts,float)
    M=np.array([[lag(k,t) for k in range(K+1)] for t in ts])
    return M*np.exp(-ts/2.0)[:,None]

def solve(K, grid, Tmax, eps):
    # shell/exterior sign region for min separation 2: t >= 8*pi
    tp=np.unique(np.concatenate([8*np.pi+(Tmax-8*np.pi)*(np.expm1(np.linspace(0,7,grid))/np.expm1(7.0)),
                                 np.linspace(8*np.pi,Tmax,grid)]))
    tq=np.unique(np.concatenate([Tmax*(np.expm1(np.linspace(0,7,grid))/np.expm1(7.0)),
                                 np.linspace(0,Tmax,grid)]))
    Mp=bm(tp,K); Mq=bm(tq,K)*((-1.0)**np.arange(K+1))[None,:]
    # column scaling
    cw=np.maximum(np.abs(np.vstack([Mp,Mq])).max(axis=0),1e-14)
    Mp,Mq=Mp/cw,Mq/cw
    A=np.vstack([Mp,-Mq]); b=np.concatenate([-eps*np.ones(len(tp)),-eps*np.ones(len(tq))])
    A=np.vstack([A,-np.eye(1,K+1,K)[0]]); b=np.concatenate([b,[-1e-9]])
    L0=np.array([lag(k,0.0) for k in range(K+1)])/cw
    cq0=L0*((-1.0)**np.arange(K+1))
    r=linprog(L0,A_ub=A,b_ub=b,A_eq=cq0[None,:],b_eq=[1.0],bounds=[(-1e5,1e5)]*(K+1),method='highs')
    if not r.success: return None,None
    f0 = float(np.dot(r.x[:K+1]/cw, np.array([lag(k,0.0) for k in range(K+1)])))
    return r.x[:K+1]/cw, f0

for K in (13,21):
    print("K=%d"%K)
    for grid in (2000,6000):
        for eps in (0.0,1e-9,1e-8,1e-7,1e-6,1e-5):
            c,f0=solve(K,grid,120.0,eps)
            if c is None: print("   g=%-5d eps=%-8g INFEAS"% (grid,eps)); continue
            for D in (10**8,10**12):
                cc=[F(int(round(x*D)),D) for x in c]
                st=EC.certify(cc,allow_touching=False,verbose=False)
                if st["ok"]:
                    d=float(F(st["p0"])/F(st["q0"]))*4*np.pi/3
                    print("   g=%-5d eps=%-8g D=1e%-2d STRICT OK  Delta<=%.6f"%(grid,eps,len(str(D))-1,d)); break
            else:
                st=EC.certify([F(int(round(x*10**10)),10**10) for x in c],allow_touching=False,verbose=False)
                rl=EC.certify([F(int(round(x*10**10)),10**10) for x in c],allow_touching=True,verbose=False)
                print("   g=%-5d eps=%-8g f0=%.6f  strict:%s  relaxed:%s"%(grid,eps,f0,
                      (st['reason'] or '')[:34],(rl['reason'] or '')[:34]))
