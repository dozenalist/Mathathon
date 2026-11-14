#!/usr/bin/env python3
"""Close C's both-sides-Gram obligation: find RATIONAL symmetric PSD A,B with
   Q_k = [k<=2m] sum_{i+j=k} A_ij + [k>=1] sum_{i+j=k-1} B_ij
for the Q of X-C014 (whose p-side Gram is already explicit).

The constraint set is an affine subspace (30 free parameters at m=5).  The objective
lambda_min(A(t), B(t)) = min(lambda_min A(t), lambda_min B(t)) is CONCAVE in t, so coordinate
ascent finds a feasible point whenever the interior is non-empty.  The search uses floats to
STEER; the final t is rational and both the coefficient identity and the PSD property are then
verified EXACTLY.
"""
import sys, numpy as np, sympy as sp
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
import json
s_=G.s_; m=5
d=json.load(open('X_C014_certificate.json'))
qs=[]
for coeffs in d['q']:
    q=sum(R(c)*s_**k for k,c in enumerate(reversed(coeffs)))
    if q!=0: qs.append(sp.expand(q))
H=sp.expand(sum(q**2 for q in qs)); P=sp.expand(-(s_-4)*H); Q=sp.expand(G.apply_map(P))
Qc=[sp.expand(Q).coeff(G.v_,k) for k in range(2*m+2)]

idx=[(i,j) for i in range(m+1) for j in range(i,m+1)]      # 21 symmetric entries
def col_A(e):
    v=[0]*len(idx); v[idx.index(e)]=1 if e[0]==e[1] else 2
    out=[0]*(2*m+2)
    for k in range(2*m+2):
        if e[0]+e[1]==k: out[k]+=v[idx.index(e)]
    return out
def col_B(e):
    out=[0]*(2*m+2)
    for k in range(2*m+2):
        if 1<=k<=2*m+1 and e[0]+e[1]==k-1: out[k]+= (1 if e[0]==e[1] else 2)
    return out
cols=[col_A(e) for e in idx]+[col_B(e) for e in idx]
Lmat=sp.Matrix([[sp.Integer(cols[j][k]) for j in range(len(cols))] for k in range(2*m+2)])
rhs=sp.Matrix([R(Qc[k]) for k in range(2*m+2)])
print("L is %dx%d, rank %d -> %d free parameters" % (Lmat.rows,Lmat.cols,Lmat.rank(),Lmat.cols-Lmat.rank()))
# particular solution over Q
aug=Lmat.row_join(rhs)
rref,pivots=aug.rref()
pivots=list(pivots)[:-1] if pivots[-1]>=Lmat.cols else list(pivots)
free=[j for j in range(Lmat.cols) if j not in pivots]
xp=[sp.Integer(0)]*Lmat.cols
for row in range(Lmat.rows):
    pc=[j for j in range(Lmat.cols) if rref[row,j]!=0]
    if len(pc)==1 and rref[row,Lmat.cols]!=0:
        xp[pc[0]]=rref[row,Lmat.cols]
N=Lmat.nullspace()
print("nullspace dimension:", len(N))
def mats(t):
    x=[sp.Integer(xp[j]) + sum(sp.Integer(N[d][j])*sp.Rational(t[d]) for d in range(len(N))) for j in range(Lmat.cols)]
    A=np.zeros((m+1,m+1)); B=np.zeros((m+1,m+1))
    for k,e in enumerate(idx):
        A[e[0],e[1]]=A[e[1],e[0]]=float(x[k])
        B[e[0],e[1]]=B[e[1],e[0]]=float(x[len(idx)+k])
    return A,B,x
def obj(t):
    A,B,_=mats(t)
    return min(np.linalg.eigvalsh(A).min(), np.linalg.eigvalsh(B).min())
t0=[Fr(0)]*len(N)
best=obj(t0); print("starting objective (min eigenvalue): %.3e" % best)
import itertools, random
cur=list(t0); curv=best
for step in [Fr(1,2),Fr(1,8),Fr(1,32),Fr(1,128),Fr(1,512)]:
    improved=True
    while improved:
        improved=False
        for j in range(len(cur)):
            for sgn in (1,-1):
                cand=list(cur); cand[j]=cand[j]+sgn*step
                v=obj(cand)
                if v>curv+1e-12: cur,curv=cand,v; improved=True
    print("  step %-8s objective %.6e" % (step,curv))
print("final objective: %.6e (need >= 0)" % curv)
if curv>=0:
    A,B,x=mats(cur)
    # EXACT verification: rational x on the affine set, then exact PSD
    xr=[sp.nsimplify(v) for v in x]
    resid=[sum(Lmat[k,j]*xr[j] for j in range(Lmat.cols))-rhs[k] for k in range(Lmat.rows)]
    print("exact coefficient identity residual all zero:", all(sp.simplify(r)==0 for r in resid))
    Ar=sp.zeros(m+1,m+1); Br=sp.zeros(m+1,m+1)
    for k,e in enumerate(idx):
        Ar[e[0],e[1]]=Ar[e[1],e[0]]=xr[k]; Br[e[0],e[1]]=Br[e[1],e[0]]=xr[len(idx)+k]
    print("A PSD exactly:", Ar.is_positive_semidefinite if hasattr(Ar,'is_positive_semidefinite') else (Ar.eigenvals() and all(sp.re(v)>=0 for v in Ar.eigenvals())))
    print("B PSD exactly:", all(sp.re(v)>=0 for v in Br.eigenvals()))
    json.dump({"m":m,"A":[[str(Ar[i,j]) for j in range(m+1)] for i in range(m+1)],
               "B":[[str(Br[i,j]) for j in range(m+1)] for i in range(m+1)]},
              open('X_C015_bothsides_gram.json','w'), indent=1)
    print("saved X_C015_bothsides_gram.json")
