#!/usr/bin/env python3
"""Try to produce ONE certificate with an explicit rational Gram on BOTH sides.

p-side: P = -(s-4) * sum_j q_j^2            (explicit already, from X-C014)
q-side: Q = a + u b with a, b explicit rational sums of squares,
        i.e. symmetric PSD rational A, B with the linear coefficient identity.

Method: take the SDP's strictly feasible (A,B) (margin 1e-6), round to rationals, then
solve the 12 linear coefficient identities EXACTLY for a chosen set of 12 unknowns while
holding the other 30 fixed.  Check PSD exactly; if it fails, retry with a different choice.
"""
import sys, numpy as np, sympy as sp
sys.path.insert(0,'.')
from fractions import Fraction as Fr
import ce_exact_gauss as G
from sympy import Rational as R
import importlib.util
s_=G.s_
spec=importlib.util.spec_from_file_location("rs","x_r03b_rescaled.py"); RS=importlib.util.module_from_spec(spec); spec.loader.exec_module(RS)
import json
m=5
d=json.load(open('X_C014_certificate.json'))
qs=[]
for coeffs in d['q']:
    q=sum(R(c)*s_**k for k,c in enumerate(reversed(coeffs)))
    if q!=0: qs.append(sp.expand(q))
H=sp.expand(sum(q**2 for q in qs)); P=sp.expand(-(s_-4)*H); Q=sp.expand(G.apply_map(P))
Qc=[sp.expand(Q).coeff(G.v_,k) for k in range(2*m+2)]
out,msg=RS.sdp_R(m,8,solver='CLARABEL')
val,Gf=out
Av,Bv=None,None
# recover A,B by re-solving with warm structure is not available; use the identity to solve directly
# unknowns: symmetric A (21) and B (21); equations: 12 coefficient identities
Aent=[(i,j) for i in range(m+1) for j in range(i,m+1)]
Bent=[(i,j) for i in range(m+1) for j in range(i,m+1)]
symsA={e:sp.Symbol('A_%d%d'%e) for e in Aent}
symsB={e:sp.Symbol('B_%d%d'%e) for e in Bent}
def coeff_of(ent, syms, off, k):
    """coefficient of u^k in sum_{i+j=k-off} M_ij (symmetric: off-diagonal counted twice)."""
    tot=0
    for (i,j),s in syms.items():
        if i+j==k-off:
            tot += s*(1 if i==j else 2) if False else s*( (1 if i==j else 2) if False else 1 )
    return tot
# careful: a = sum_{i,j} A_ij u^{i+j} over the FULL symmetric matrix
def fullcoeff(syms, k):
    tot=0
    for (i,j),s in syms.items():
        deg=i+j
        if deg==k:
            tot += s*(1 if i==j else 2)   # symmetric matrix: both (i,j) and (j,i)
    return tot
eqs=[]
for k in range(2*m+2):
    lhs=fullcoeff(symsA,k)
    if k>=1: lhs = lhs + fullcoeff(symsB,k-1)
    eqs.append(sp.Eq(lhs, Qc[k]))
allv=list(symsA.values())+list(symsB.values())
sol=sp.linsolve([e.lhs-e.rhs for e in eqs], allv)
print("linear system: %d unknowns, %d equations; solvable: %s" % (len(allv), len(eqs), bool(sol) and sol != sp.EmptySet))
if sol and sol != sp.EmptySet:
    tup=next(iter(sol))
    free=[s for s in allv if s in set().union(*[t.free_symbols for t in tup])] if False else None
    print("  particular solution has %d free parameters" % len(set().union(*[t.free_symbols for t in tup])))
