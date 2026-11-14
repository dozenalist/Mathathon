from fractions import Fraction as F
from itertools import product
import random
W=F(1,6)
E={i:frozenset({i,(i+1)%6}) for i in range(6)}
NC=[(i,j) for i in range(6) for j in range(i+1,6) if (j-i)%6 not in (1,5)]
def cd(a,b):
    d=abs(a-b)%1; return min(d,1-d)
def direct_ok(v):
    crit=sorted({(x%1) for x in v}|{((x-W)%1) for x in v}); n=len(crit)
    pts=list(crit)+[ (crit[k]+((crit[(k+1)%n]-crit[k])%1)/2)%1 for k in range(n) if ((crit[(k+1)%n]-crit[k])%1)>0]
    for a in pts:
        S=[i for i in range(6) if ((v[i]-a)%1)<=W]
        u=set()
        for i in S: u|=E[i]
        if len(u)>=4: return False
    return True
def pok(v): return all(cd(v[i],v[j])>W for i,j in NC)

bad=gs=0
for q in product(range(6),repeat=6):
    v=[F(x,6) for x in q]; d=direct_ok(v); p=pok(v)
    if d!=p: bad+=1
    if d: gs+=1
print("grid 6^6: direct-vs-pairwise mismatches",bad,"| survivors",gs,"(expect 0, 36)")
six=set()
for q in product(range(6),repeat=5):
    v=[F(0)]+[F(x,6) for x in q]
    if direct_ok(v): six.add((0,)+q)
print("q0=0 survivors:",len(six),sorted(six))
random.seed(7); bad=0
for _ in range(6000):
    v=[F(random.randrange(0,36),36) for _ in range(6)]
    if direct_ok(v)!=pok(v): bad+=1
print("random /36: mismatches",bad)

# family INSIDE hypothesis 0<=a,b,c<=pi/4 = 1/8 in 2pi units
def fam(a,b,c,t): return [((t+x)%1) for x in (0,a,F(1,3),F(1,3)+b,F(2,3),F(2,3)+c)]
fb=0
for a,b,c in [(0,0,0),(F(1,8),0,0),(0,F(1,8),0),(0,0,F(1,8)),(F(1,8),F(1,8),F(1,8)),(F(1,8),0,F(1,8))]:
    if not direct_ok(fam(a,b,c,0)): fb+=1; print("  FAIL",a,b,c)
for _ in range(600):
    a,b,c=[F(random.randrange(0,101),800) for _ in range(3)]   # in [0,1/8]
    t=F(random.randrange(0,97),97)
    if not direct_ok(fam(a,b,c,t)): fb+=1
print("family failures in-hypothesis:",fb,"/ 606")
v=fam(F(1,8),0,0,0)
print("min constrained dist at (pi/4,0,0):",min(cd(v[i],v[j]) for i,j in NC),"= pi*",min(cd(v[i],v[j]) for i,j in NC)*2,"(stated 5/12)")
print("family at (pi/4,pi/4,pi/4): six distinct non-grid:",len(set(fam(F(1,8),F(1,8),F(1,8),0))))

# Theorem 6: maximise min constrained distance by exact local search
def score(v): return min(cd(v[i],v[j]) for i,j in NC)
best=F(0);bv=None
random.seed(2)
for trial in range(300):
    base=[F(random.randrange(0,120),120) for _ in range(6)]
    v=base[:]
    step=F(1,120)
    for it in range(400):
        improved=False
        for i in range(6):
            for delta in (step,-step):
                w=v[:]; w[i]=(w[i]+delta)%1
                if score(w)>score(v): v=w; improved=True
        if not improved:
            if step>F(1,100000): step=step/2
            else: break
    if score(v)>best: best,bv=score(v),v
print("local-search max of min constrained dist:",best,"= pi*",best*2,"| ceiling 2/3 =",float(F(2,3)),"| v:",bv)

# Theorem 7, targeted: confined (all six cyclic distances <= 1/6) and closing
print("== T7 targeted ==")
viol=0;cnt=0
# m=1 branch: steps near +1/6 summing to 1
for _ in range(4000):
    a=[F(random.randrange(-20,21),2000) for _ in range(5)]
    s=a+[1-sum(a)-sum([F(0)])]
    s=[F(1,6)+x for x in a]; s.append(1-sum(s))
    if any(abs(x)>W for x in s): continue
    u=[F(0)]
    for x in s[:-1]: u.append(u[-1]+x)
    v=[x%1 for x in u]
    if pok(v):
        cnt+=1
        t=v[0]; alt1=[(t+F(i,6))%1 for i in range(6)]; alt2=[(t-F(i,6))%1 for i in range(6)]
        if v!=alt1 and v!=alt2: viol+=1; print("  VIOL",s)
print("m=1 branch: confined+closing+inV tested:",cnt,"violations:",viol)
# m=0 branch: force sum 0 with mixed signs
cnt2=viol2=0
for _ in range(6000):
    s=[F(random.randrange(-24,25),144) for _ in range(5)]
    s.append(-sum(s))
    if any(abs(x)>W for x in s): continue
    if sum(s)!=0: continue
    u=[F(0)]
    for x in s[:-1]: u.append(u[-1]+x)
    v=[x%1 for x in u]
    if pok(v): cnt2+=1; viol2+=1; print("  m=0 IN V (contradicts T7):",s,v)
print("m=0 branch: in V count:",cnt2,"(theorem says 0)")
