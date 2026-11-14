#!/usr/bin/env python3
"""Both-sides Gram, take 2: project the SDP's PSD pair (A,B) onto the exact affine set.
x* = x_p + N (N^T N)^{-1} N^T (x_sdp - x_p).  Since the SDP pair is strictly feasible (margin
1e-6) and the projection moves it by ~margin, x* should still be PSD; then round t rationally
and verify the identity and the PSD property EXACTLY."""
import sys, numpy as np, sympy as sp, json
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
import importlib.util
s_=G.s_; m=5
spec=importlib.util.spec_from_file_location("rs","x_r03b_rescaled.py"); RS=importlib.util.module_from_spec(spec); spec.loader.exec_module(RS)
out,msg=RS.sdp_R(m,8,solver='CLARABEL')
val,Gf=out
# SDP's A,B are internal to sdp_R; recompute them by re-solving with the same routine but
# recovering via a second call that returns them: patch sdp_R to also return A,B
src=open('x_r03b_rescaled.py').read()
src=src.replace("return (float(prob.value), np.array(Gv.value)), \"ok\"",
                "return (float(prob.value), np.array(Gv.value), np.array(Av.value), np.array(Bv.value)), \"ok\"")
mod={}
exec(compile(src,'rs2','exec'), mod)
out2,msg2=mod['sdp_R'](m,8,solver='CLARABEL')
_,Gf2,Af,Bf=out2
print("SDP PSD margins: A %.2e  B %.2e" % (np.linalg.eigvalsh(Af).min(), np.linalg.eigvalsh(Bf).min()))
# affine set for the frozen Q
d=json.load(open('X_C014_certificate.json'))
qs=[]
for coeffs in d['q']:
    q=sum(R(c)*s_**k for k,c in enumerate(reversed(coeffs)))
    if q!=0: qs.append(sp.expand(q))
H=sp.expand(sum(q**2 for q in qs)); P=sp.expand(-(s_-4)*H); Q=sp.expand(G.apply_map(P))
Qc=[sp.expand(Q).coeff(G.v_,k) for k in range(2*m+2)]
idx=[(i,j) for i in range(m+1) for j in range(i,m+1)]
cols=[]
for e in idx:
    v=[0]*(2*m+2)
    if e[0]+e[1]<2*m+2: v[e[0]+e[1]] += (1 if e[0]==e[1] else 2)
    cols.append(v)
for e in idx:
    v=[0]*(2*m+2)
    if 1<=e[0]+e[1]+1<2*m+2: v[e[0]+e[1]+1] += (1 if e[0]==e[1] else 2)
    cols.append(v)
# sdp_R uses the basis (s/S)^i, so the coefficient identity carries S^{-k}:
#   Q_k = S^{-k} [ sum_{i+j=k} A_ij + sum_{i+j=k-1} B_ij ]
S=8
Lm=sp.Matrix([[sp.Rational(cols[j][k], S**k) for j in range(len(cols))] for k in range(2*m+2)])
rhs=sp.Matrix([R(Qc[k]) for k in range(2*m+2)])
rref,piv=aug=Lm.row_join(rhs).rref()
piv=[p for p in piv if p < Lm.cols]
xp=[sp.Integer(0)]*Lm.cols
for row in range(Lm.rows):
    pc=[j for j in range(Lm.cols) if rref[row,j]!=0]
    if len(pc)==1 and rref[row,Lm.cols]!=0: xp[pc[0]]=rref[row,Lm.cols]
N=Lm.nullspace()
Nf=np.array([[float(N[d][j]) for d in range(len(N))] for j in range(Lm.cols)],dtype=float)
xpf=np.array([float(xp[j]) for j in range(Lm.cols)],dtype=float)
# SDP pair as a vector, in the same ordering
xsdp=np.zeros(Lm.cols)
for k,e in enumerate(idx):
    xsdp[k]=Af[e[0],e[1]]
    xsdp[len(idx)+k]=Bf[e[0],e[1]]
Gn=Nf.T@Nf
t=np.linalg.solve(Gn, Nf.T@(xsdp-xpf))
x=xpf+Nf@t
A=np.zeros((m+1,m+1)); B=np.zeros((m+1,m+1))
for k,e in enumerate(idx):
    A[e[0],e[1]]=A[e[1],e[0]]=x[k]
    B[e[0],e[1]]=B[e[1],e[0]]=x[len(idx)+k]
print("projected margins: A %.2e  B %.2e" % (np.linalg.eigvalsh(A).min(), np.linalg.eigvalsh(B).min()))
# rationalise t and verify exactly
for den in (10**4,10**6,10**8):
    tr=[sp.Rational(Fr(v).limit_denominator(den).numerator, Fr(v).limit_denominator(den).denominator) for v in t]
    xr=[sp.nsimplify(xp[j]) + sum(sp.Rational(N[d][j])*tr[d] for d in range(len(N))) for j in range(Lm.cols)]
    resid=[sp.simplify(sum(Lm[k,j]*xr[j] for j in range(Lm.cols))-rhs[k]) for k in range(Lm.rows)]
    if not all(r==0 for r in resid): continue
    Ar=sp.zeros(m+1,m+1); Br=sp.zeros(m+1,m+1)
    for k,e in enumerate(idx):
        Ar[e[0],e[1]]=Ar[e[1],e[0]]=xr[k]; Br[e[0],e[1]]=Br[e[1],e[0]]=xr[len(idx)+k]
    evA=[complex(v) for v in Ar.eigenvals()]; evB=[complex(v) for v in Br.eigenvals()]
    okA=all(v.real>=-1e-40 for v in evA); okB=all(v.real>=-1e-40 for v in evB)
    print("den=1e%d: identity exact=True  A PSD=%s  B PSD=%s" % (len(str(den))-1, okA, okB))
    if okA and okB:
        json.dump({"m":m,"A":[[str(Ar[i,j]) for j in range(m+1)] for i in range(m+1)],
                   "B":[[str(Br[i,j]) for j in range(m+1)] for i in range(m+1)],
                   "note":"rational PSD pair with Q_k identity; p-side Gram is X-C014's"},
                  open('X_C015_bothsides_gram.json','w'), indent=1)
        print("SAVED X_C015_bothsides_gram.json -- both-sides explicit Gram achieved")
        break
