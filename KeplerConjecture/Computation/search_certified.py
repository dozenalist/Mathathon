#!/usr/bin/env python3
"""K15 search: finds the verified certificate Delta <= 0.77996650 (degree 33).

Sweeps degree in {21,25,29,33}, grid in {6000,10000}, margin eps in {1e-7,3e-7,1e-6,3e-6},
and for each solves the CE linear program then attempts EXACT verification of the
rational-rounded coefficients. Only candidates that pass exactcert.certify(strict) are
reported; the best is written to out/best_certified.json.

The search is heuristic. The verification is not: see verify_certificate.py.

Run: python3 search_certified.py            (about 2.5 min)
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
def solve(K,grid,Tmax,eps):
    tp=np.unique(np.concatenate([8*np.pi+(Tmax-8*np.pi)*(np.expm1(np.linspace(0,7,grid))/np.expm1(7.0)),np.linspace(8*np.pi,Tmax,grid)]))
    tq=np.unique(np.concatenate([Tmax*(np.expm1(np.linspace(0,7,grid))/np.expm1(7.0)),np.linspace(0,Tmax,grid)]))
    Mp=bm(tp,K); Mq=bm(tq,K)*((-1.0)**np.arange(K+1))[None,:]
    cw=np.maximum(np.abs(np.vstack([Mp,Mq])).max(axis=0),1e-14)
    Mp,Mq=Mp/cw,Mq/cw
    A=np.vstack([Mp,-Mq,-np.eye(1,K+1,K)[0]])
    b=np.concatenate([-eps*np.ones(len(tp)),-eps*np.ones(len(tq)),[-1e-9]])
    L0=np.array([lag(k,0.0) for k in range(K+1)])/cw
    cq0=L0*((-1.0)**np.arange(K+1))
    r=linprog(L0,A_ub=A,b_ub=b,A_eq=cq0[None,:],b_eq=[1.0],bounds=[(-1e5,1e5)]*(K+1),method='highs')
    if not r.success: return None
    return r.x[:K+1]/cw
best=None
for K in (21,25,29,33):
    for grid in (6000,10000):
        for eps in (1e-7,3e-7,1e-6,3e-6):
            c=solve(K,grid,120.0,eps)
            if c is None: continue
            for D in (10**8,10**10,10**12):
                cc=[F(int(round(x*D)),D) for x in c]
                st=EC.certify(cc,allow_touching=False,verbose=False)
                if st["ok"]:
                    d=float(F(st["p0"])/F(st["q0"]))*4*np.pi/3
                    print("K=%-3d g=%-5d eps=%-8g D=1e%-2d OK  Delta<=%.7f  gap=%+.2f%%"%(K,grid,eps,len(str(D))-1,d,100*(d/0.740480489693-1)))
                    if best is None or d<best[0]: best=(d,K,grid,eps,cc)
                    break
            else:
                print("K=%-3d g=%-5d eps=%-8g  fail"%(K,grid,eps))
print("\nBEST:", best[0] if best else None)
if best:
    import json
    d,K,grid,eps,cc=best
    json.dump({"degree":K,"grid":grid,"epsilon":eps,"certified_Delta":d,
               "kepler":0.7404804896930611,"gap":d-0.7404804896930611,
               "c":[str(x) for x in cc]}, open("out/best_certified.json","w"), indent=1)
    print("saved out/best_certified.json")
