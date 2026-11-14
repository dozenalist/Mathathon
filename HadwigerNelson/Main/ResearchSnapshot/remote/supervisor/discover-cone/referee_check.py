from fractions import Fraction as F
from itertools import product
import random, sys
T = 1  # circle of circumference 1; pi/3 = 1/6; pi = 1/2
W = F(1,6)
E = {i: frozenset({i,(i+1)%6}) for i in range(6)}
NONCONS = [(i,j) for i in range(6) for j in range(i+1,6) if (j-i)%6 not in (1,5)]

def cdist(a,b):
    d = abs(a-b) % 1
    return min(d, 1-d)

def direct_ok(v):
    """CC60-arc by DIRECT enumeration of closed arcs of length exactly W.
    Index set changes only when the left endpoint passes some v_i or v_i - W,
    so testing those points and the midpoints between consecutive critical
    values is exhaustive for a piecewise-constant membership function."""
    crit = sorted({(vi % 1) for vi in v} | {((vi - W) % 1) for vi in v})
    n = len(crit)
    pts = list(crit)
    for k in range(n):
        a, b = crit[k], crit[(k+1) % n]
        gap = (b - a) % 1
        if gap > 0:
            pts.append((a + gap/2) % 1)
    for a in pts:
        S = [i for i in range(6) if ((v[i] - a) % 1) <= W]   # v_i in closed [a, a+W]
        u = set()
        for i in S: u |= E[i]
        if len(u) >= 4:
            return False, a, S, sorted(u)
    return True, None, None, None

def pairwise_ok(v):
    return all(cdist(v[i], v[j]) > W for i, j in NONCONS)

# ---- Check 1: direct vs pairwise on the grid 6^6, and random rationals
bad = 0
grid_surv = 0
for q in product(range(6), repeat=6):
    v = [F(x,6) for x in q]
    if direct_ok(v)[0] != pairwise_ok(v): bad += 1
    if direct_ok(v)[0]: grid_surv += 1
print("grid 6^6: direct-vs-pairwise mismatches =", bad, "| grid survivors =", grid_surv)

random.seed(7)
bad = 0
for _ in range(4000):
    v = [F(random.randrange(0,24),24) for _ in range(6)]
    if direct_ok(v)[0] != pairwise_ok(v): bad += 1; print("MISMATCH", v)
print("random /24 rationals: mismatches =", bad)

# ---- Check 2: q0=0 survivors must be exactly the six AC-CONE-SIX words
six = set()
for q in product(range(6), repeat=5):
    v = [F(0)] + [F(x,6) for x in q]
    if direct_ok(v)[0]: six.add((0,)+q)
print("q0=0 survivors:", len(six), sorted(six))

# ---- Check 3: v* certificate, exact
vs = [F(1,20),F(5,20),F(14,20),F(18,20),F(28,20),F(32,20)]  # in units of 2*pi/... careful
# v* = (pi/20)(1,5,14,18,28,32) -> in units of 2*pi: x/40
vs = [F(x,40) for x in (1,5,14,18,28,32)]
ds = {(i,j): cdist(vs[i],vs[j]) for i,j in NONCONS}
print("v* direct ok:", direct_ok(vs)[0], "| pairwise ok:", pairwise_ok(vs))
print("v* min constrained distance (units of 2pi):", min(ds.values()), "= pi *", min(ds.values())*2,
      "| threshold pi/3 =", float(F(1,6)), "| slack(pi units):", min(ds.values())*2 - F(1,3))
# sup-box radius 19deg = 19/360 of circumference
rho = F(19,360)
print("box radius rho in 2pi-units:", rho, "| 13/20 - 2rho =", F(13,20)-2*rho, "> 1/6 ?", F(13,20)-2*rho > F(1,6))

# ---- Check 4: four-parameter family, corners + random exact points
fam_bad = 0
for a,b,c in [(0,0,0),(F(1,4),0,0),(0,F(1,4),0),(0,0,F(1,4)),(F(1,4),F(1,4),F(1,4)),
              (F(1,8),F(1,4),F(3,16)),(F(1,4),F(1,8),F(1,16))]:
    v = [0, a, F(1,3), F(1,3)+b, F(2,3), F(2,3)+c]  # in 2pi units: 2pi/3 -> 1/3
    if not direct_ok(v)[0]: fam_bad += 1; print("FAMILY FAIL", a,b,c, v)
for _ in range(300):
    a,b,c = [F(random.randrange(0,101),400) for _ in range(3)]
    t = F(random.randrange(0,97),97)
    v = [(t+x) % 1 for x in (0,a,F(1,3),F(1,3)+b,F(2,3),F(2,3)+c)]
    if not direct_ok(v)[0]: fam_bad += 1; print("FAMILY FAIL rand", a,b,c,t)
print("family failures:", fam_bad, "| family min constrained dist (2pi units):", F(5,24), "= pi*", F(5,12))

# ---- Check 5: Theorem 6 necessity -- can any v beat 2pi/3 ?
best = F(0); bestv=None
random.seed(11)
for _ in range(60000):
    v = [F(random.randrange(0,360),360) for _ in range(6)]
    m = min(cdist(v[i],v[j]) for i,j in NONCONS)
    if m > best: best, bestv = m, v
print("random search: max over v of min constrained distance (2pi units) =", best, "= pi*", best*2, "(ceiling pi*2/3)")
# structured: three clusters
for eps in (F(1,100),F(1,1000)):
    v=[0,eps,F(1,3),F(1,3)+eps,F(2,3),F(2,3)+eps]
    print("  three-cluster eps",eps,"min constrained =",min(cdist(v[i],v[j]) for i,j in NONCONS)*2,"pi")

# ---- Check 6: Theorem 7 -- confined data (all consecutive <= 1/6) and V forces grid
random.seed(3)
viol = 0; tested = 0
for _ in range(20000):
    s = [F(random.randrange(-24,25),144) for _ in range(6)]   # in [-1/6,1/6] in 2pi units
    if max(abs(x) for x in s) > F(1,6): continue
    u=[F(0)]
    for x in s: u.append(u[-1]+x)
    v=[x % 1 for x in u[:6]]
    if pairwise_ok(v):
        tested += 1
        # must be rotation of alternating grid, up to reflection
        t=v[0]
        alt1=[(t+F(i,6))%1 for i in range(6)]
        alt2=[(t-F(i,6))%1 for i in range(6)]
        if v!=alt1 and v!=alt2: viol+=1; print("T7 VIOLATION", s, v)
print("T7: confined+V tested:", tested, "violations:", viol)
# Corollary 7': all consecutive strictly < 1/6 -> not in V
c7=0
for _ in range(20000):
    s=[F(random.randrange(-23,24),144) for _ in range(6)]
    if max(abs(x) for x in s) >= F(1,6): continue
    u=[F(0)]
    for x in s: u.append(u[-1]+x)
    v=[x % 1 for x in u[:6]]
    if pairwise_ok(v): c7+=1
print("Cor 7' counterexamples (all-strict confined in V):", c7)
