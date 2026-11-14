import numpy as np, json
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre
import exactcert as EC
from fractions import Fraction as F
def lag(k,t): return eval_genlaguerre(k,0.5,t)
def bm(ts,K):
    ts=np.asarray(ts,float)
    M=np.array([[lag(k,t) for k in range(K+1)] for t in ts]); return M*np.exp(-ts/2.0)[:,None]
def solve(K,grid,Tmax,eps):
    tp=np.unique(np.concatenate([8*np.pi+(Tmax-8*np.pi)*(np.expm1(np.linspace(0,8,grid))/np.expm1(8.0)),np.linspace(8*np.pi,Tmax,grid)]))
    tq=np.unique(np.concatenate([Tmax*(np.expm1(np.linspace(0,8,grid))/np.expm1(8.0)),np.linspace(0,Tmax,grid)]))
    Mp=bm(tp,K); Mq=bm(tq,K)*((-1.0)**np.arange(K+1))[None,:]
    cw=np.maximum(np.abs(np.vstack([Mp,Mq])).max(axis=0),1e-14)
    Mp,Mq=Mp/cw,Mq/cw
    A=np.vstack([Mp,-Mq,-np.eye(1,K+1,K)[0]])
    b=np.concatenate([-eps*np.ones(len(tp)),-eps*np.ones(len(tq)),[-1e-9]])
    L0=np.array([lag(k,0.0) for k in range(K+1)])/cw
    cq0=L0*((-1.0)**np.arange(K+1))
    r=linprog(L0,A_ub=A,b_ub=b,A_eq=cq0[None,:],b_eq=[1.0],bounds=[(-1e5,1e5)]*(K+1),method='highs')
    return None if not r.success else r.x[:K+1]/cw
best=None
for K in (33,37,41):
    for grid in (10000,14000):
        for eps in (1e-8,3e-8,1e-7):
            c=solve(K,grid,120.0,eps)
            if c is None: print(K,grid,eps,"INFEAS"); continue
            got=None
            for D in (10**8,10**10,10**12):
                cc=[F(int(round(x*D)),D) for x in c]
                st=EC.certify(cc,allow_touching=False,verbose=False)
                if st["ok"]:
                    got=(float(F(st["p0"])/F(st["q0"]))*4*np.pi/3, D, cc); break
            if got:
                d,D,cc=got
                print("K=%-3d g=%-6d eps=%-8g D=1e%-2d OK  Delta<=%.7f gap=%+.2f%%"%(K,grid,eps,len(str(D))-1,d,100*(d/0.740480489693-1)))
                if best is None or d<best[0]: best=(d,K,grid,eps,cc)
            else:
                print("K=%-3d g=%-6d eps=%-8g fail"%(K,grid,eps))
print("\nBEST certified:", best[0] if best else None)
if best and best[0] < json.load(open("out/best_certified.json"))["certified_Delta"]:
    d,K,g,e,cc=best
    json.dump({"degree":K,"grid":g,"epsilon":e,"certified_Delta":d,"c":[str(x) for x in cc]}, open("out/best_certified2.json","w"), indent=1)
    print("saved out/best_certified2.json")
