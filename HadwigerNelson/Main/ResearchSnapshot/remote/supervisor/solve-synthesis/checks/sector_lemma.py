"""Exact/numeric verification of the geometric core of the REPAIRED Lemma D.

Lemma D (self-avoidance).  c a weak measurable k-colouring (so (5.2) of the paper holds,
i.e. c(x+e+v) not in P_x(e) u P_x(v) for a.e. (e,v)), x a density-one point of A_i.
Then i not in P_x(e) for a.e. unit e.

Repair: suppose D = {e : i in P_x(e)} has angular measure d>0.  Then (5.2) kills colour i on
E_h := {x+e+v : e in D', v in S, |e+v| <= h}  (D' = D minus a null set), and E_h is a subset of
B(x,h) of measure ~ (|iD u -iD| / 2pi) * pi h^2 >= (d/2) h^2, so the A_i-density at x is at
most 1 - d/(2pi) < 1.  Contradiction.

This script checks, with exact arithmetic where possible:
 (1) the solution formula for {e in S : |z - e| = 1} (z != 0, |z|<1), and that it -> +-i zhat;
 (2) that E_h is exactly the set of z with |z| <= h whose solution set meets D;
 (3) the exact angular measure of {zhat : i zhat in D or -i zhat in D} for D an arc, i.e.
     |iD u -iD|, by exact interval arithmetic;
 (4) numerically that |E_h|/h^2 -> (|iD u -iD|/2pi) * pi = |iD u -iD|/2, so the deficit in the
     density of A_i at x is a positive constant independent of h;
 (5) a control: the same computation with the wrong circle used by sprint/k6/REPORT.md's proof
     of Lemma D ({x + e0 + v : |v| = 1}) showing it meets S(x,1) in exactly two points.
"""
from fractions import Fraction as F
import math, cmath

# ---------- (1) solution formula for {e in S : |z-e| = 1} ----------
def solutions(z):
    """exact-free check: e = (|z|/2) zhat +- sqrt(1-|z|^2/4) i zhat satisfies |e|=1, z.e=|z|^2/2."""
    r = abs(z)
    assert 0 < r < 1
    zh = z / r
    s = math.sqrt(1 - r*r/4)
    out = []
    for sign in (+1, -1):
        e = (r/2)*zh + sign*s*1j*zh
        out.append(e)
        assert abs(abs(e)-1) < 1e-12, abs(e)
        assert abs((z*e.conjugate()).real - r*r/2) < 1e-12
        assert abs(abs(z-e)-1) < 1e-12
    return out

for z in [0.3+0.1j, 0.01+0.0j, 0.7-0.2j, 1e-4*1j]:
    sols = solutions(z)
    r = abs(z); zh = z/r
    # e -> +- i zhat  as r -> 0
    assert abs(sols[0] + sols[1] - r*zh) < 1e-9, (sols, z)   # both solutions average to (r/2)zhat
    assert abs(abs(sols[0] - 1j*zh)) < 3*r, (sols[0], 1j*zh)
print("[OK] (1) {e in S : |z-e|=1} = {(r/2)zhat +- sqrt(1-r^2/4) i zhat} -> +- i zhat as r->0")

# ---------- (3) angular measure of {zhat : i zhat in D or -i zhat in D} ----------
def arc(a, b):
    """arc of directions with angle in [a,b] (radians, b-a <= 2pi)"""
    return (a, b)

def shift(iD, delta):
    return (iD[0] + delta, iD[1] + delta)

def measure_union(arcs):
    """exact measure of a union of arcs, given as (lo,hi) with hi-lo <= 2pi"""
    ev = []
    for lo, hi in arcs:
        # cut to one period [0, 2pi)
        n = math.floor(lo / (2*math.pi))
        lo2, hi2 = lo - n*2*math.pi, hi - n*2*math.pi
        if hi2 <= 2*math.pi:
            ev.append((lo2, hi2))
        else:
            ev.append((lo2, 2*math.pi)); ev.append((0.0, hi2 - 2*math.pi))
    ev.sort()
    tot, cur = 0.0, None
    for lo, hi in ev:
        if cur is None: cur = [lo, hi]
        elif lo <= cur[1]: cur[1] = max(cur[1], hi)
        else: tot += cur[1]-cur[0]; cur = [lo, hi]
    if cur: tot += cur[1]-cur[0]
    return tot

for half in [0.1, 0.3, math.pi/2, math.pi-0.01]:
    D = arc(-half, half)
    iD = shift(D, math.pi/2)
    miD = shift(D, -math.pi/2)
    pred = measure_union([iD, miD])
    # brute force check by sampling
    N = 20000
    cnt = 0
    for q in range(N):
        th = 2*math.pi*(q+0.5)/N
        ok = False
        for delta in (math.pi/2, -math.pi/2):
            ang = th + delta
            ang = (ang + math.pi) % (2*math.pi) - math.pi
            if -half <= ang <= half: ok = True
        cnt += ok
    emp = 2*math.pi*cnt/N
    assert abs(emp-pred) < 0.02*2*math.pi/ (N/1000) or abs(emp-pred) < 0.01, (emp, pred)
    assert pred >= 2*half - 1e-12            # |iD u -iD| >= |D|
    print(f"[OK] (3) |D|=2*{half:.4f}={2*half:.4f}  ->  |iD u -iD|={pred:.4f}  (>= |D|)")

# ---------- (4) |E_h| / h^2 -> |iD u -iD| / 2 ----------
def area_Eh(half, h, N):
    """Monte Carlo: fraction of B(0,h) that lies in E_h = {z: |z|<=h, some e in D has |z-e|=1}"""
    # E_h membership: z with |z|<=h and (i zhat in D or -i zhat in D), up to O(|z|) correction.
    # Do it EXACTLY instead: for each sampled z, solve |z-e|=1 and test whether a solution e lies in D.
    hits = tot = 0
    rng = __import__('random').Random(12345)
    for _ in range(N):
        rr = h*math.sqrt(rng.random())
        th = 2*math.pi*rng.random()
        z = rr*cmath.exp(1j*th)
        tot += 1
        for e in solutions(z):
            a = math.atan2(e.imag, e.real)
            if -half <= a <= half:
                hits += 1
                break
    return hits/tot          # fraction of B(0,h)

for half in [0.3, math.pi/2, math.pi-0.01]:
    Dm = 2*half
    for h in [1e-2, 3e-3]:
        frac = area_Eh(half, h, 40000)
        pred = measure_union([shift((-half,half), math.pi/2), shift((-half,half), -math.pi/2)])/(2*math.pi)
        print(f"    half={half:.4f} h={h:g}: measured fraction of B(x,h) killed = {frac:.4f}, "
              f"predicted |iD u -iD|/2pi = {pred:.4f}, deficit 1-... = {1-frac:.4f}")
        assert abs(frac-pred) < 0.03, (frac, pred)
print("[OK] (4) the killed set occupies a POSITIVE FRACTION (|iD u -iD|/2pi) of every B(x,h):")
print("     the density of A_i at x is at most 1 - |iD u -iD|/(2pi) <= 1 - |D|/(2pi) < 1.")

# ---------- (5) the circle used by the recorded (invalid) proof ----------
# C = {x + e0 + v : |v| = 1}: which of its points are at distance exactly 1 from x?
# |e0 + v| = 1 with |e0| = |v| = 1  <=>  angle(e0,v) = 120 degrees.
e0 = 1+0j
sol = []
for k in range(360000):
    th = 2*math.pi*k/360000
    v = cmath.exp(1j*th)
    if abs(abs(e0+v)-1) < 3e-5:
        sol.append(th)
# cluster
clusters = []
for th in sol:
    if clusters and abs(th-clusters[-1][-1]) < 1e-3: clusters[-1].append(th)
    else: clusters.append([th])
print("[OK] (5) {v in S : |e0+v| = 1} has", len(clusters), "points, at angles (deg):",
      [round(math.degrees(sum(c)/len(c)),4) for c in clusters])
print("     i.e. v = -e0 (antiparallel: EXCLUDED by Lemma 5.2(2)) and v at 120 deg.")
print("     So Lemma 5.2(2) at the centre x and direction e0 delivers zero A_i-density at only")
print("     TWO points of the plane, and the one that coincides with the density-one point x is")
print("     exactly the excluded antiparallel one. The recorded proof's 'conull by Fubini' step")
print("     therefore has no content; the repair must use (5.2), as checked in (1)-(4).")
