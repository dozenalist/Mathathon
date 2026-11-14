#!/usr/bin/env python3
"""INDEPENDENT audit of C's K33 certificate (blob ced184a9). Nothing imported from Computation/."""
import json
from fractions import Fraction as F

def laguerre_half(N):
    """L_k^{1/2}(t) as ascending coefficient lists over Q."""
    out=[[F(1)]]
    if N>=1: out.append([F(3,2),F(-1)])
    for k in range(1,N):
        a=out[k]; b=out[k-1]; res=[F(0)]*(max(len(a)+1,len(b))+1)
        c1=F(2*k+1)+F(1,2); c2=F(k)+F(1,2)
        for i,cf in enumerate(a): res[i]+=c1*cf; res[i+1]+=-cf
        for i,cf in enumerate(b): res[i]-=c2*cf
        res=[x/(k+1) for x in res]
        while len(res)>1 and res[-1]==0: res.pop()
        out.append(res)
    return out
def padd(A,B):
    n=max(len(A),len(B)); r=[F(0)]*n
    for i,x in enumerate(A): r[i]+=x
    for i,x in enumerate(B): r[i]+=x
    while len(r)>1 and r[-1]==0: r.pop()
    return r
def pscale(A,c): return [x*c for x in A]
def peval(A,x):
    s=F(0)
    for cf in reversed(A): s=s*x+cf
    return s
def pibounds(terms=60):
    def at(n):
        S=[];acc=F(0)
        for k in range(terms):
            acc+=F((-1)**k,(2*k+1)*n**(2*k+1)); S.append(acc)
        return min(S[-1],S[-2]),max(S[-1],S[-2])
    a1,a2=at(5); b1,b2=at(239)
    return 16*a1-4*b2, 16*a2-4*b1
def norm(A):
    A=list(A)
    while len(A)>1 and A[-1]==0: A.pop()
    return A

d=json.load(open('K33.json'))
c=[F(x) for x in d['coefficients_rational']]; N=len(c)-1
L=laguerre_half(N)
p=[F(0)]; q=[F(0)]
for k,ck in enumerate(c):
    p=padd(p,pscale(L[k],ck)); q=padd(q,pscale(L[k],(-1)**k*ck))
print("A. independent reconstruction from the 34 rational coefficients")
print("   deg p = %d, deg q = %d  (both ODD => each has a real root somewhere)" % (len(p)-1,len(q)-1))
print("   p matches JSON (ascending order assumed): %s" % (norm(p)==norm([F(x) for x in d['p_rational']])))
print("   q matches JSON                          : %s" % (norm(q)==norm([F(x) for x in d['q_rational']])))
print("   ... also try descending: p:%s q:%s"
      % (norm(p)==norm([F(x) for x in d['p_rational']][::-1]),
         norm(q)==norm([F(x) for x in d['q_rational']][::-1])))
p0=peval(p,F(0)); q0=peval(q,F(0))
print("   p(0) = %s\n     field p0 equal: %s ; p0>0: %s" % (p0,p0==F(d['p0']),p0>0))
print("   q(0) = %s\n     field q0 equal: %s ; q0>0: %s" % (q0,q0==F(d['q0']),q0>0))
ratio=p0/q0
print("   p0/q0 == ratio_exact: %s" % (ratio==F(d['ratio_exact'])))
lo,hi=pibounds()
dl=F(4,3)*lo*ratio; dh=F(4,3)*hi*ratio
print("B. the bound")
print("   Delta = (4pi/3)(p0/q0) in [%.15f, %.15f]" % (float(dl),float(dh)))
du=F(d['delta_upper_exact'])
print("   delta_upper_exact is an UPPER bound: %s  (slack %.3e)" % (du>=dh, float(du-dh)))
print("   '0.77996650' >= true Delta: %s ; '0.779966497785' >= true Delta: %s"
      % (F('0.77996650')>=dh, F('0.779966497785')>=dh))
sqlo,sqhi=F(4242640687119285146,10**18),F(4242640687119285147,10**18)
print("   Kepler comparison 4 p0 sqrt18 <= 3 q0 ? %s  (bound %s Kepler)"
      % (4*p0*sqhi<=3*q0, "BELOW" if 4*p0*sqhi<=3*q0 else "ABOVE"))
print("   Delta - pi/sqrt18 = %.9f (positive => weaker than Kepler)" % (float(dh)-0.74048048969))
json.dump({"p0":str(p0),"q0":str(q0),"ratio":str(ratio),"dens_lo":str(dl),"dens_hi":str(dh),
           "delta_field":str(du),"p": [str(x) for x in p], "q": [str(x) for x in q]}, open("audit_numbers.json","w"))
