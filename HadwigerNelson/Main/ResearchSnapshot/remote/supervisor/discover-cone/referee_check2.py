from fractions import Fraction as F
from itertools import product
import random
W=F(1,6)
E={i:frozenset({i,(i+1)%6}) for i in range(6)}
NONCONS=[(i,j) for i in range(6) for j in range(i+1,6) if (j-i)%6 not in (1,5)]
def cdist(a,b):
    d=abs(a-b)%1; return min(d,1-d)
def direct_ok(v):
    crit=sorted({(vi%1) for vi in v}|{((vi-W)%1) for vi in v}); n=len(crit)
    pts=list(crit)
    for k in range(n):
        a,b=crit[k],crit[(k+1)%n]; g=(b-a)%1
        if g>0: pts.append((a+g/2)%1)
    for a in pts:
        S=[i for i in range(6) if ((v[i]-a)%1)<=W]
        u=set()
        for i in S: u|=E[i]
        if len(u)>=4: return False
    return True
def pairwise_ok(v): return all(cdist(v[i],v[j])>W for i,j in NONCONS)

print("== 1. grid 6^6 ==")
bad=gs=0
for q in product(range(6),repeat=6):
    v=[F(x,6) for x in q]
    d=direct_ok(v); p=pairwise_ok(v)
    if d!=p: bad+=1
    if d: gs+=1
print("   direct vs pairwise mismatches:",bad," survivors:",gs," (expect 0, 36)")
six=set()
for q in product(range(6),repeat=5):
    v=[F(0)]+[F(x,6) for x in q]
    if direct_ok(v): six.add((0,)+q)
print("   q0=0 survivors:",len(six),sorted(six))

print("== 2. random rationals, direct vs pairwise ==")
random.seed(7); bad=0
for _ in range(6000):
    v=[F(random.randrange(0,36),36) for _ in range(6)]
    if direct_ok(v)!=pairwise_ok(v): bad+=1
print("   mismatches:",bad)

print("== 3. v* certificate ==")
vs=[F(x,40) for x in (1,5,14,18,28,32)]
print("   direct:",direct_ok(vs),"pairwise:",pairwise_ok(vs),
      "min dist =",min(cdist(vs[i],vs[j]) for i,j in NONCONS),"-> pi*",min(cdist(vs[i],vs[j]) for i,j in NONCONS)*2)
rho=F(19,360); print("   box: 13/20-2rho =",F(13,20)-2*rho,">1/6:",F(13,20)-2*rho>F(1,6))

print("== 4. four-parameter family ==")
fam_bad=0
def fam(a,b,c,t):
    return [((t+x)%1) for x in (0,a,F(1,3),F(1,3)+b,F(2,3),F(2,3)+c)]
for a,b,c in [(0,0,0),(F(1,4),0,0),(0,F(1,4),0),(0,0,F(1,4)),(F(1,4),F(1,4),F(1,4))]:
    if not direct_ok(fam(a,b,c,0)): fam_bad+=1; print("   FAIL",a,b,c)
for _ in range(400):
    a,b,c=[F(random.randrange(0,101),400) for _ in range(3)]
    t=F(random.randrange(0,97),97)
    if not direct_ok(fam(a,b,c,t)): fam_bad+=1; print("   FAIL rand",a,b,c,t)
print("   family failures:",fam_bad,"| stated min constrained dist 5/12*pi; check at corner (1/4,1/4,1/4):",
      min(cdist(*[fam(F(1,4),F(1,4),F(1,4),0)[i],fam(F(1,4),F(1,4),F(1,4),0)[j]]) for i,j in NONCONS)*2)

print("== 5. Theorem 6: can min constrained distance exceed 2pi/3 ? ==")
best=F(0);random.seed(11)
for _ in range(80000):
    v=[F(random.randrange(0,720),720) for _ in range(6)]
    m=min(cdist(v[i],v[j]) for i,j in NONCONS)
    if m>best: best=m
print("   random max:",best,"-> pi*",best*2," ceiling 2/3 pi")
for eps in (F(1,100),F(1,2000)):
    v=[0,eps,F(1,3),F(1,3)+eps,F(2,3),F(2,3)+eps]
    print("   three-cluster eps",eps,"min constrained = pi*",min(cdist(v[i],v[j]) for i,j in NONCONS)*2)

print("== 6. Theorem 7, with the CLOSING step enforced (sum s in Z) ==")
random.seed(3); viol=tested=0; nonclosing=0
for _ in range(200000):
    s=[F(random.randrange(-24,25),144) for _ in range(6)]
    if max(abs(x) for x in s)>W: continue
    if sum(s).denominator!=1: nonclosing+=1; continue
    u=[F(0)]
    for x in s[:-1]: u.append(u[-1]+x)
    v=[x%1 for x in u]
    if sorted(abs(s[i]) for i in range(6))==[F(0)]*6: pass
    assert max(cdist(v[i],v[(i+1)%6]) for i in range(6))<=W
    if pairwise_ok(v):
        tested+=1; t=v[0]
        alt1=[(t+F(i,6))%1 for i in range(6)]; alt2=[(t-F(i,6))%1 for i in range(6)]
        if v!=alt1 and v!=alt2: viol+=1; print("   T7 VIOLATION",s,v)
print("   confined & closing & in V tested:",tested," violations:",viol," (skipped non-closing:",nonclosing,")")

print("== 7. Corollary 7': all six strictly < pi/3 cannot be in V ==")
random.seed(5); c7=0; n7=0
for _ in range(200000):
    s=[F(random.randrange(-23,24),144) for _ in range(6)]
    if max(abs(x) for x in s)>=W: continue
    if sum(s).denominator!=1: continue
    u=[F(0)]
    for x in s[:-1]: u.append(u[-1]+x)
    v=[x%1 for x in u]
    n7+=1
    if pairwise_ok(v): c7+=1
print("   strictly-confined closing configs:",n7," of which in V:",c7," (expect 0)")
