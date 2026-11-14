from fractions import Fraction as F
import sys
def forced(p,q,s2,t2):   # is v=(p,q) forced? s2=s^2, t2=t^2 exact Fractions
    dp = max(0,abs(p)-1); dq = max(0,abs(q)-1)
    dmin2 = dp*dp*s2 + dq*dq*t2
    if dmin2 > 1: return False
    dmax2 = (abs(p)+1)**2*s2 + (abs(q)+1)**2*t2
    return dmax2 >= 1
def hom_ok(A,B,s2,t2,one_over_s,one_over_t):
    # need: no forced v with A*p+B*q=0 mod 7, v != 0
    import math
    P = int(one_over_s)+2; Q = int(one_over_t)+2
    for p in range(-P,P+1):
        for q in range(-Q,Q+1):
            if p==0 and q==0: continue
            if (A*p+B*q)%7: continue
            if forced(p,q,s2,t2): return False
    return True
def ok_homs(s,t):
    s2=F(s)*F(s); t2=F(t)*F(t)
    # truncation: dmin>1 whenever (|p|-1)s>1 or (|q|-1)t>1 ; use |p|<=1+1/s, |q|<=1+1/t
    res=[]
    for A in range(7):
        for B in range(7):
            if (A,B)==(0,0): continue
            if hom_ok(A,B,s2,t2,F(1)/F(s),F(1)/F(t)): res.append((A,B))
    return res
for (s,t) in [(F(1,2),F(1,2)),(F(1,3),F(1,3)),(F(2,5),F(2,5)),(F(4,10),F(4,10)),
              (F(1,2),F(1,10)),(F(9,10),F(1,10)),(F(8,10),F(1,10)),(F(7,10),F(1,10)),
              (F(6,10),F(2,10)),(F(5,10),F(1,10)),(F(4,10),F(1,10)),(F(3,10),F(1,10)),
              (F(2,10),F(1,10)),(F(9,20),F(3,20)),(F(55,100),F(20,100)),(F(6,10),F(5,100)),
              (F(9,10),F(1,100)),(F(1,4),F(1,4)),(F(2,7),F(2,7)),(F(3,7),F(3,7))]:
    print(s,t,"->",ok_homs(s,t))
