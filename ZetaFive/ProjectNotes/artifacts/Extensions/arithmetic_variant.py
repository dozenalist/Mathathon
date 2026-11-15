"""Exploratory numerical normalization for numerator D_N^(2r), zeta(s).
This is not a rigorous quadrature certificate.
"""
import math
from fractions import Fraction as F
import numpy as np

alpha=3/40
lam=37/40

def ell(x,z):
    return math.floor(x-z)+math.floor(x+z)+1

def inner_R(x,r,s):
    H=lam+r*alpha
    T=math.floor(2*H*x)
    rem=H*x-T/2
    q=math.floor(2*x)
    nplus=(2*x-q)/2
    fx=x%1
    fa=(alpha*x)%1
    cuts=sorted({0.0,0.5,*[t for t in [fx,1-fx,fa,1-fa] if 0<t<0.5]})
    gamma=0.0
    for a,b in zip(cuts,cuts[1:]):
        z=(a+b)/2
        bx=r*ell(alpha*x,z)
        gamma+=(b-a)*(T-bx)*(T+bx-ell(x,z)-s)
    gamma+=rem*(2*T-q-s)+max(0,rem-nplus)
    j=math.floor(2*lam*x)
    J=j*lam*x-j*(j+1)/4
    norm=2*lam*x*math.floor(x)-4*r*lam*x*math.floor(alpha*x)-2*J
    return -gamma-norm

def integrate_inner(r,s,T=200):
    # Include all natural floor and piecewise-affine crossing breakpoints.
    H=lam+r*alpha
    cuts={3.0,float(T)}
    for freq in [1,2,2*alpha,2*lam,2*H,1-alpha,1+alpha,2*(H-1)]:
        for n in range(math.floor(3*freq),math.ceil(T*freq)+1):
            x=n/freq
            if 3<x<T: cuts.add(x)
    cuts=sorted(cuts)
    nodes,weights=np.polynomial.legendre.leggauss(8)
    total=0.0
    for a,b in zip(cuts,cuts[1:]):
        half=(b-a)/2
        mid=(a+b)/2
        total+=half*sum(float(w)*inner_R(mid+half*float(z),r,s)/(mid+half*float(z))**3 for z,w in zip(nodes,weights))
    return total

def outer_C8(y):
    a=F(3,40)
    pos=lambda z:max(0,z)
    if y<F(1,2):
        u=pos(1+a-3*y)
        return 9*(1-y)-16*a-7*min(a,1-2*y)-7*u+min(pos(1+6*a-3*y),y+u)
    return 9*(1-y)-8*min(a,1-y)-8*pos(1+a-2*y)

if __name__=='__main__':
    from arithmetic_costs import c5,piecewise_integral,breaks
    aa=F(3,40)
    cuts=sorted(set(breaks)|{(1+6*aa)/3,(1+6*aa)/4,5*aa})
    c8=piecewise_integral(outer_C8,cuts)
    c5i=piecewise_integral(c5,cuts)
    iout8=F(127751,96000)+c8-c5i
    print('C8 raw outer',c8,float(c8))
    print('Iout8',iout8,float(iout8))
    for r,s in [(3,5),(3,7),(4,7)]:
        for T in [200,1000,5000]:
            inner=integrate_inner(r,s,T)
            outer=float(F(127751,96000)) if (r,s)==(3,5) else (float(F(27071,16000)) if r==3 else float(iout8))
            print('r,s,T,inner,normalization_bound_cutoff',r,s,T,inner,outer+(s+1)*lam/T+inner)
