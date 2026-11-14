#!/usr/bin/env python3
"""Both-sides explicit rational Gram at useful strength — strict rational handling.
No nsimplify anywhere: every rational is built from integer numerator/denominator."""
import sys, numpy as np, sympy as sp, json
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
src=open('both_sides_gram5.py').read(); _m={}
exec(compile(src.split('if __name__')[0],'bs','exec'), _m)
joint_sdp=_m['joint_sdp']; build=_m['build']; ldl_psd=_m['ldl_psd']
s_=G.s_
def rat(x):
    if isinstance(x,sp.Rational): return x
    f=sp.Rational(sp.cancel(sp.together(x)))
    assert f.is_rational, ("non-rational", x)
    return f
def ldl_min(M):
    nn=M.rows; cur=M[:,:]; piv=[]
    for k in range(nn):
        d=cur[k,k]
        if d<0: return d
        if d==0:
            if any(cur[k,j]!=0 for j in range(k,nn)): return sp.Integer(-1)
            piv.append(sp.Integer(0)); continue
        piv.append(d)
        for i in range(k+1,nn):
            f=cur[i,k]/d
            for j in range(k,nn): cur[i,j]=cur[i,j]-f*cur[k,j]
    return min(piv) if piv else sp.Integer(0)
best=None
print("%-3s %-4s %-7s %-6s %-6s %-6s %-8s %-14s %s" % ("m","S","eps","ident","PSD G","PSD A/B","link","P0/Q0","density"))
for (m,S) in [(3,6),(3,8),(4,8),(4,12),(5,8)]:
    for eps in (1e-2,1e-3,1e-4):
        try: out=joint_sdp(m,S,eps)
        except Exception as e:
            print("%-3d %-4d %-7g solver exc %s"%(m,S,eps,type(e).__name__)); continue
        if out['status'] not in ('optimal','optimal_inaccurate'):
            print("%-3d %-4d %-7g status %s"%(m,S,eps,out['status'])); continue
        L,ent,n=build(m,S)
        x=np.zeros(3*n)
        for k,(a,b) in enumerate(ent):
            x[k]=out['G'][a,b]; x[n+k]=out['A'][a,b]; x[2*n+k]=out['B'][a,b]
        xp=x-L.T@np.linalg.lstsq(L@L.T,L@x,rcond=None)[0]
        xv=[R(Fr(v).limit_denominator(10**7).numerator, Fr(v).limit_denominator(10**7).denominator) for v in xp]
        Lm=sp.Matrix([[sp.Rational(int(sp.Rational(v).p),int(sp.Rational(v).q)) for v in row] for row in L])
        rr,piv=Lm.rref(); chosen=list(piv); free=[j for j in range(Lm.cols) if j not in chosen]
        try:
            sol=Lm[:,chosen].LUsolve(-Lm[:,free]*sp.Matrix([xv[j] for j in free]))
            for idx,j in enumerate(chosen): xv[j]=rat(sol[idx])
        except Exception as e:
            print("%-3d %-4d %-7g LU exc %s"%(m,S,eps,type(e).__name__)); continue
        xvm=sp.Matrix(xv)
        ident=all(v==0 for v in Lm*xvm)
        Gm=sp.zeros(m+1);Am=sp.zeros(m+1);Bm=sp.zeros(m+1)
        for k,(a,b) in enumerate(ent):
            Gm[a,b]=Gm[b,a]=xv[k]; Am[a,b]=Am[b,a]=xv[n+k]; Bm[a,b]=Bm[b,a]=xv[2*n+k]
        mG=ldl_min(Gm); mA=ldl_min(Am); mB=ldl_min(Bm)
        vf=lambda xx: sp.Matrix([xx**i for i in range(m+1)])
        Hb=sp.expand((vf(s_/S).T*Gm*vf(s_/S))[0]); P=sp.expand(-(s_-4)*Hb); Q=sp.expand(G.apply_map(P))
        Qb=sp.expand((vf(G.v_/S).T*Am*vf(G.v_/S))[0]+G.v_*(vf(G.v_/S).T*Bm*vf(G.v_/S))[0])
        link=sp.simplify(Qb-Q)==0
        P0=P.subs(s_,0); Q0=Q.subs(G.v_,0)
        if P0<=0 or Q0<=0: print("%-3d %-4d %-7g signs at 0 fail"%(m,S,eps)); continue
        rq=rat(P0/Q0); dens=float(R(4,3)/sp.sqrt(sp.pi)*rq)
        print("%-3d %-4d %-7g %-6s %-6s %-6s %-8s %-14.9f %.9f"
              % (m,S,eps,ident,mG>=0,(mA>=0 and mB>=0),link,float(rq),dens))
        if ident and mG>=0 and mA>=0 and mB>=0 and link and 0.74048<dens and (best is None or dens<best[0]):
            best=(dens,m,S,eps,rq,Gm,Am,Bm)
print("-"*84)
if best:
    dens,m,S,eps,rq,Gm,Am,Bm=best
    print("BEST BOTH-SIDES at useful strength: m=%d S=%d eps=%g  density=%.12f"%(m,S,eps,dens))
    json.dump({"m":m,"S":S,"G":[[str(Gm[i,j]) for j in range(m+1)] for i in range(m+1)],
               "A":[[str(Am[i,j]) for j in range(m+1)] for i in range(m+1)],
               "B":[[str(Bm[i,j]) for j in range(m+1)] for i in range(m+1)],
               "P_over_Q":str(rq),"density":dens},open('X_C016_certificate.json','w'),indent=1)
    print("saved X_C016_certificate.json")
