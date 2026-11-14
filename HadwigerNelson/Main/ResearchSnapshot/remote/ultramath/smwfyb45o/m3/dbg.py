from d3 import *
cov, unc, covA, uncA = rect_certify(24, verbose=False)
print("covered boxes (first 20):", cov[:20])
print("uncovered count:", len(unc))
# test the claimed hom at the box centre exactly
from fractions import Fraction as F
for (i,j,h) in cov[:8]:
    s = F(2*i+1, 48); t = F(2*j+1, 48)
    print("box",i,j,"hom",h,"centre s,t =",s,t, "s2+t2 =", s*s+t*t)
    bad=[]
    for p in range(-60,61):
        for q in range(-60,61):
            if p==0 and q==0: continue
            A,B=h
            if (A*p+B*q)%7: continue
            if forced(p,q,s*s,t*t): bad.append((p,q))
    print("   forced same-colour v:", bad[:10], "count", len(bad))
