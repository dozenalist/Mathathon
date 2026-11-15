"""Exact piecewise rational integration of the transferred inner cost.

The result certifies the finite integral for the formulas, not all local
valuation estimates. Breakpoint verification is described in the notes.
"""
from fractions import Fraction as F
import math
import json
from pathlib import Path

A=F(3,40)
L=1-A

def floor(x):return x.numerator//x.denominator
def ell(x,z):return floor(x-z)+floor(x+z)+1

def R(x,r,s):
    H=L+r*A
    T=floor(2*H*x)
    rem=H*x-F(T,2)
    q=floor(2*x)
    nplus=x-F(q,2)
    fx=x-floor(x)
    fa=A*x-floor(A*x)
    cuts=sorted({F(0),F(1,2),*[v for v in (fx,1-fx,fa,1-fa) if 0<v<F(1,2)]})
    gamma=F(0)
    for a,b in zip(cuts,cuts[1:]):
        z=(a+b)/2
        bb=r*ell(A*x,z)
        gamma+=(b-a)*(T-bb)*(T+bb-ell(x,z)-s)
    gamma+=rem*(2*T-q-s)+max(0,rem-nplus)
    j=floor(2*L*x)
    J=j*L*x-F(j*(j+1),4)
    norm=2*L*x*floor(x)-4*r*L*x*floor(A*x)-2*J
    return -gamma-norm

def cuts_for(r,end):
    H=L+r*A
    cuts={F(3),F(end)}
    for freq in [F(1),F(2),2*A,2*L,2*H,1-A,1+A,2*(H-1)]:
        for n in range(floor(3*freq),math.ceil(end*freq)+1):
            x=F(n)/freq
            if 3<x<end:cuts.add(x)
    return sorted(cuts)

def integral(r,s,end):
    cuts=cuts_for(r,end)
    rat=F(0)
    logterms=[]
    maxquad=F(0)
    for a,b in zip(cuts,cuts[1:]):
        d=(b-a)/4
        x1,x2,x3=a+d,a+2*d,a+3*d
        y1,y2,y3=R(x1,r,s),R(x2,r,s),R(x3,r,s)
        c2=(y3-2*y2+y1)/(2*d*d)
        c1=(y3-y1)/(2*d)-2*c2*x2
        c0=y2-c2*x2*x2-c1*x2
        # Fourth independent point detects an omitted breakpoint in this interval.
        xp=a+(b-a)/7
        assert R(xp,r,s)==c2*xp*xp+c1*xp+c0,(a,b)
        maxquad=max(maxquad,abs(c2))
        rat+=c1*(1/a-1/b)+c0/2*(1/a**2-1/b**2)
        if c2:logterms.append((c2,b/a))
    return rat,logterms,len(cuts)-1,maxquad

if __name__=='__main__':
    results=[]
    for r,s in [(3,5),(3,7),(4,7)]:
        for end in [20,200]:
            rat,logs,count,mq=integral(r,s,end)
            assert not logs and mq==0
            if (r,s,end)==(3,5,20):
                assert rat==F(322437603634266857629,7535670527041937280000)
            val=float(rat)+sum(float(c)*math.log(float(v)) for c,v in logs)
            print('r,s,end,intervals,logterms,maxquad',r,s,end,count,len(logs),mq)
            print('value',val)
            print('rational_part',rat)
            if (r,s,end)==(4,7,200):
                outer=F(453803,288000)
                coefficient=outer+8*L/200+rat
                results.append({'numerator_power':8,'zeta':7,'M':200,
                                'intervals':count,
                                'inner_integral_exact':str(rat),
                                'inner_integral_decimal':float(rat),
                                'outer_integral_exact':str(outer),
                                'normalization_coefficient_exact':str(coefficient),
                                'normalization_coefficient_decimal':float(coefficient),
                                'method':'Exact rational piecewise affine integration; see arithmetic_variant_notes.txt'})
    target=Path(__file__).with_name('arithmetic_variant_results.json')
    target.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('Wrote',target)
