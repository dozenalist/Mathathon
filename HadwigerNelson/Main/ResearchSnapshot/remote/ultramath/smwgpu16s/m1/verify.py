"""Numerical checks for referee report: direction-packing theorem, unit-chord angle
bound, sector/section engine, covering arithmetic, aperture reduction.
Every check is a True/False assertion; the report quotes this output verbatim.
"""
import itertools
import math
import random
from math import cos, sin, pi, asin, atan, sqrt

out = []
def p(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)

D = math.degrees
R = math.radians

# ---------------------------------------------------------------- 1
p("=== 1. unit-chord bound: |y-y'|=1 and |y-x|,|y'-x| >= r  =>  separation <= 2asin(1/(2r)) ===")
for r in [1.0, 1.0001, 1.01, 1.1, 1.5, 2.0, 10.0, 100.0]:
    b = 2 * asin(1 / (2 * r))
    p(f"  r={r:<8} bound={D(b):.10f} deg   <60deg? {b < pi/3}   =60deg? {abs(b - pi/3) < 1e-15}")
p("  sharpness: radii both = r, separation = the bound, chord comes out 1:")
for r in [1.0, 1.1, 2.0, 10.0]:
    b = 2 * asin(1 / (2 * r))
    chord = sqrt(2 * r * r * (1 - cos(b)))
    p(f"    r={r:<5} chord={chord:.15f}   |chord-1|={abs(chord - 1):.2e}")

def min_chord(theta, r, steps=200000):
    """min of |y-y'| over radii in [r, r*1.3] at fixed separation theta."""
    best = float('inf')
    for k in range(steps + 1):
        r1 = r * (1 + 0.3 * k / steps)
        r2 = max(r, r1 * cos(theta))
        d = sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 * cos(theta))
        best = min(best, d)
    return best
p("  converse (strictness): at separation = bound + 1e-6 deg, min chord over radii >= r is > 1:")
for r in [1.1, 2.0]:
    th = 2 * asin(1 / (2 * r)) + R(1e-6)
    m = min_chord(th, r)
    p(f"    r={r}: min chord={m:.12f}   >1? {m > 1}")

# ---------------------------------------------------------------- 2
p("")
p("=== 2. packing theorem on S1: gaps g1+g2+g3 = 360, all gaps in [120,240] => all = 120 ===")
def gaps(th):
    th = sorted(x % (2 * pi) for x in th)
    n = len(th)
    return [(th[i + 1] - th[i]) if i + 1 < n else th[0] + 2 * pi - th[i] for i in range(n)]

def circ_dist(a, b):
    d = abs((a - b) % (2 * pi))
    return min(d, 2 * pi - d)

step = R(1.0)
vals = [k * step for k in range(120, 241)]        # WLOG first angle 0 => others in [120,240]
cnt3, dev3 = 0, 0.0
for a, b in itertools.combinations(vals, 2):
    th = [0.0, a, b]
    if min(circ_dist(x, y) for x, y in itertools.combinations(th, 2)) >= 2 * pi / 3 - 1e-12:
        cnt3 += 1
        dev3 = max(dev3, max(abs(g - 2 * pi / 3) for g in gaps(th)))
p(f"  1-deg grid, WLOG theta_1 = 0: triples with all pairwise circular distances >= 120 deg: {cnt3}")
p(f"  max |gap - 120deg| among them: {D(dev3):.6f} deg  (bounded by grid resolution)")
cnt4 = 0
for trip in itertools.combinations(vals, 3):
    th = [0.0] + list(trip)
    if min(circ_dist(x, y) for x, y in itertools.combinations(th, 2)) >= 2 * pi / 3 - 1e-12:
        cnt4 += 1
p(f"  same grid, 4 directions with all pairwise circular distances >= 120 deg: {cnt4}")

p("  counterexample to the LINEAR (ordered-difference) reading: 0, 120, 250 degrees")
th = [R(0), R(120), R(250)]
g = gaps(th)
p(f"    gaps (deg) = {[round(D(x), 6) for x in g]}   all gaps >= 120? {min(g) >= 2*pi/3 - 1e-12}")
lin = [120, 130, 250]
p(f"    ordered differences (deg) = {lin}   all >= 120? {min(lin) >= 120}")
p(f"    circular distances (deg) = "
  f"{[round(D(circ_dist(a, b)), 6) for a, b in itertools.combinations(th, 2)]}")
p(f"    minimal containing arc (deg) = {D(2*pi - max(g)):.6f}")
g = gaps([0.0, 2 * pi / 3, 4 * pi / 3])
p(f"  equilateral triple {{0,120,240}}: gaps = {[round(D(x),6) for x in g]}, "
  f"minimal containing arc = {D(2*pi - max(g)):.6f} deg")

# ---------------------------------------------------------------- 3
p("")
p("=== 3. aperture = max pairwise circular distance, and is attained by a pair (A < 180) ===")
random.seed(7)
ok = True
for _ in range(3000):
    m = random.randint(2, 7)
    th = [random.uniform(0, 2 * pi) for _ in range(m)]
    A = 2 * pi - max(gaps(th))
    mx = max(circ_dist(a, b) for a, b in itertools.combinations(th, 2))
    i, j = max(itertools.combinations(range(m), 2), key=lambda ij: circ_dist(th[ij[0]], th[ij[1]]))
    A2 = 2 * pi - max(gaps([th[i], th[j]]))
    if A < pi and (abs(A - mx) > 1e-9 or abs(A - A2) > 1e-9):
        ok = False
p(f"  aperture equals max pairwise circular distance and is attained by a pair of directions: {ok}")

# ---------------------------------------------------------------- 4
p("")
p("=== 4. covering arithmetic for k = 6 ===")
U = set(range(6))
B3 = [set(c) for c in itertools.combinations(sorted(U), 3)]
B2 = [set(c) for c in itertools.combinations(sorted(U), 2)]
for name, coll in [("size-2", B2), ("size-3", B3)]:
    inter = sorted({len(x & y) for x in coll for y in coll if 6 - len(x | y) <= 1})
    p(f"  {name} blocks: intersection sizes admitting residual <= 1: {inter}")
p("  two size-2 blocks cover at most 4 < 5 labels: residual >= 2 always")
sizes = {}
for x in B3:
    for y in B3:
        sizes[len(x & y)] = sizes.get(len(x & y), 0) + 1
p(f"  ordered pairs of size-3 blocks by |B1 cap B2|: {dict(sorted(sizes.items()))}  (total {sum(sizes.values())})")
p(f"  residual exactly 1 (union = 5): {sizes[1]} ordered pairs; residual 0 (union = 6): {sizes[0]}")
cnt = 0
for x, y, z in itertools.product(B3, repeat=3):
    if all(len(a & b) == 1 for a, b in itertools.combinations([x, y, z], 2)):
        if len(x | y | z) >= 5:
            cnt += 1
p(f"  ordered triples of size-3 blocks pairwise sharing exactly one label with union >= 5: {cnt}")

# ---------------------------------------------------------------- 5
p("")
p("=== 5. sector engine: width needed for a positive circle-section ===")
def section_length(t0, w_half, r1, r2, n=200001):
    tot = 0.0
    dth = 2 * pi / n
    for k in range(n):
        th = k * dth
        y = (t0 + cos(th), sin(th))
        rad = math.hypot(*y)
        if r1 < rad < r2:
            ang = math.atan2(y[1], y[0])
            d = min(abs(ang) % (2 * pi), 2 * pi - (abs(ang) % (2 * pi)))
            if d < w_half:
                tot += dth
    return tot

for (r1, r2, w_deg) in [(1.1, 5.0, 60.0), (1.1, 5.0, 20.0), (1.1, 5.0, 5.0),
                        (1.1, 5.0, 1.0), (1.1, 5.0, 0.1), (1.1, 200.0, 1.0)]:
    thr = 2 * atan(1 / sqrt(r2 * r2 - 1))
    t0 = 0.5 * (r1 + sqrt(r2 * r2 - 1)) if sqrt(r2 * r2 - 1) > r1 else 0.5 * (r1 + r2)
    L = section_length(t0, R(w_deg) / 2, r1, r2)
    p(f"  r1={r1} r2={r2} w={w_deg:5} deg   threshold w > 2atan(1/sqrt(r2^2-1)) = {D(thr):.6f} deg"
      f"   exceeds? {R(w_deg) > thr}   section length = {L:.6f} rad")
p("  (S) is NOT automatic: for W = union of open disks of radius 0.01 whose centres are")
p("  pairwise >= 2.1 apart, any two points of W are either <= 0.02 or >= 2.08 apart, so W")
p("  contains no unit pair and every section is empty, while W is open with |W| = infinity.")

# ---------------------------------------------------------------- 6
p("")
p("=== 6. L1 endpoint: at r = 1 the bound 60 deg is attained (equilateral triple) ===")
pts = [(cos(a), sin(a)) for a in (0.0, pi / 3, 2 * pi / 3)]
p(f"  radii = {[round(math.hypot(*q), 12) for q in pts]}")
p(f"  |p0-p1| = {math.dist(pts[0], pts[1]):.12f}  |p1-p2| = {math.dist(pts[1], pts[2]):.12f}")

open("verify_out.txt", "w").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- 7
p("")
p("=== 7. three size-3 blocks: pairwise |Bi cap Bj| <= 1 forces union = ALL SIX labels ===")
unions = {}
ti = {}
for x, y, z in itertools.product(B3, repeat=3):
    if all(len(a & b) <= 1 for a, b in itertools.combinations([x, y, z], 2)):
        u = len(x | y | z)
        unions[u] = unions.get(u, 0) + 1
        t = len(x & y & z)
        ti[t] = ti.get(t, 0) + 1
p(f"  |B1 cup B2 cup B3| distribution: {dict(sorted(unions.items()))}")
p(f"  |B1 cap B2 cap B3| distribution: {dict(sorted(ti.items()))}")
p("  => residual J = [6] \ (B1 cup B2 cup B3) is ALWAYS empty; no triple leaves a label over")
p("  inclusion-exclusion check: 9 - (sum of pairwise) + triple = 9 - 3 + 0 = 6")
# and with block size 4
B4 = [set(c) for c in itertools.combinations(sorted(U), 4)]
u4 = sorted({len(x | y | z) for x, y, z in itertools.product(B4, repeat=3)})
p(f"  for size-4 blocks, achievable |union| of three blocks: {u4}  (so a residual can survive)")

# ---------------------------------------------------------------- 8
p("")
p("=== 8. duality: aperture A (A<180) => common-negative directions form an open arc of width 180-A ===")
def aperture(th):
    return 2 * pi - max(gaps(th))

def common_negative_width(th):
    # width of {u : u.v < 0 for all v in th}, computed on a fine grid
    n = 72000
    cnt = 0
    for k in range(n):
        u = k * 2 * pi / n
        if all(cos(u - v) < 0 for v in th):
            cnt += 1
    return cnt * 2 * pi / n

for th in ([R(0), R(90)], [R(0), R(60)], [R(10), R(50), R(130)], [R(0), R(119)]):
    A = aperture(th)
    Wc = common_negative_width(th)
    p(f"  directions {[round(D(t),3) for t in th]} deg: aperture={D(A):.4f} deg, "
      f"common-negative arc width={D(Wc):.4f} deg, 180-A={D(pi-A):.4f} deg, "
      f"match? {abs(Wc-(pi-A)) < 2*pi/72000+1e-9}")
p("  boundary case aperture exactly 120 deg: width = 60 deg exactly")
th = [R(0), R(120)]
p(f"    aperture={D(aperture(th)):.6f}, width={D(common_negative_width(th)):.6f}")

open("verify_out.txt", "w").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- 9
p("")
p("=== 9. exact sector threshold: required width = 2*psi*(t) with psi*(t) = 2 asin(1/(2t)) ===")
p("   psi*(t) = atan( sqrt(4t^2-1)/(2t^2-1) )  should equal  2 asin(1/(2t))")
for t in [1.0001, 1.5, 1.9318517, 2.0, 3.0, 5.0, 100.0, 200.0]:
    psi = atan(sqrt(4*t*t - 1) / (2*t*t - 1))
    alt = 2 * asin(1 / (2 * t))
    need = 2 * psi                     # required sector width w >= need
    p(f"   t={t:<12} psi*={D(psi):.10f} deg 2asin={D(alt):.10f} deg match={abs(psi-alt)<1e-12}"
      f"   required w={D(need):.6f} deg   aperture excluded up to {180-D(need):.6f} deg")
p("   t such that required w = 60 deg: w = 4 asin(1/(2t)) = 60 => t = 0.5 csc(15 deg) =", 0.5/math.sin(R(15)))
p("   section positivity at t0 = 2 (r1 = 1.1, r2 = 5) just below and just above the threshold:")
thr = 4 * asin(1 / (2 * 2.0))
for w_deg in [D(thr) - 0.5, D(thr) - 0.05, D(thr) + 0.05, D(thr) + 0.5, 60.0]:
    L = section_length(2.0, R(w_deg) / 2, 1.1, 5.0)
    p(f"   w={w_deg:.4f} deg (threshold {D(thr):.4f}): section length at z=(2,0) = {L:.6f} rad")

open("verify_out.txt", "w").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- 10
p("")
p("=== 10. vacuity is exactly at uniform block size 3: exhaustive over triples of subsets of [6] ===")
subs = [frozenset(c) for r in range(7) for c in itertools.combinations(range(6), r)]
for minsize, exact in ((2, None), (3, None), (4, None), (5, None), (3, 3)):
    dist = {}
    for B1 in subs:
        if len(B1) < minsize or (exact and len(B1) != exact):
            continue
        for B2 in subs:
            if len(B2) < minsize or (exact and len(B2) != exact) or len(B1 | B2) < 5:
                continue
            for B3 in subs:
                if len(B3) < minsize or (exact and len(B3) != exact):
                    continue
                if len(B1 | B3) < 5 or len(B2 | B3) < 5:
                    continue
                u = len(B1 | B2 | B3)
                dist[u] = dist.get(u, 0) + 1
    label = f"exactly {exact}" if exact else f">= {minsize}"
    p(f"  block sizes {label:>12}: triples by |union| = {dict(sorted(dist.items()))}")
p("  => uniform size 3: union is ALWAYS 6 (residual empty, vacuous claim).")
p("  => size >= 4: union 5 occurs, e.g. {1,2,3,4},{1,2,3,5},{1,2,4,5} -> union {1,2,3,4,5}, J = {6}.")

open("verify_out.txt", "w").write("\n".join(out) + "\n")
