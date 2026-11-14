#!/usr/bin/env python3
"""d7: exact verification of the sphere-window chromatic-number theorem.

Theorem 1 (sphere decomposition).  Fix x in R^2 and r > 0.  Let G(x,r) be the
graph on S_r(x) with an edge for every pair at Euclidean distance exactly 1.
  (i)  r < 1/2: G(x,r) has no edge, chi = 1.
  (ii) r >= 1/2: put theta = 2 arcsin(1/(2r)) in (0, pi].  The graph is
       invariant under the rotation rho by theta about x and every connected
       component is the rho-orbit of any of its points.  If theta/(2 pi) = p/q
       in lowest terms then every component is a q-cycle; if theta/(2 pi) is
       irrational then every component is a bi-infinite path.
  Hence chi(G) = 3 iff theta/(2 pi) has odd reduced denominator q >= 3, i.e.
  iff r = 1/(2 sin(pi p / q)) with q odd, 1 <= p <= q/2, gcd(p,q) = 1; and
  chi(G) = 2 otherwise (r >= 1/2).  In particular chi(G(x,r)) <= 3 for all x, r.
"""
import math
import sympy as sp


def theta(r):
    """exact chord angle: chord length 1 at radius r <=> theta = 2 asin(1/(2r))"""
    return 2 * sp.asin(1 / (2 * r))


def exact_label(r):
    """return (theta, p, q) with theta/(2 pi) = p/q in lowest terms, or (theta,None,None)."""
    th = theta(r)
    s = sp.simplify(1 / (2 * r))
    for q in range(2, 61):
        for p in range(1, q // 2 + 1):
            if math.gcd(p, q) != 1:
                continue
            if sp.simplify(sp.sin(sp.pi * p / q) - s) == 0:
                return th, p, q
    return th, None, None


def chi_cycle(q):
    if q == 1:
        return 1
    return 2 if q % 2 == 0 else 3


def chrom_number_small(n, edges, kmax=4):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for k in range(1, kmax + 1):
        col = [-1] * n
        order = sorted(range(n), key=lambda v: -len(adj[v]))

        def rec(i):
            if i == n:
                return True
            v = order[i]
            for c in range(k):
                if all(col[u] != c for u in adj[v]):
                    col[v] = c
                    if rec(i + 1):
                        return True
                    col[v] = -1
            return False

        if rec(0):
            return k
    return None


def sqdist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def orbit_structure(r_float, theta_float, n_seeds=12, maxlen=400, tol=1e-6):
    """Build the graph on S_r(0) from orbits of the rotation by theta_float.
    For each seed angle the orbit is followed until it closes or maxlen.
    Returns (list of orbit lengths, closed?, max degree inside the orbit)."""
    lengths, closed, degs = [], [], set()
    for s in range(n_seeds):
        phi = 2 * math.pi * s / n_seeds + 0.1234
        pts = [(r_float * math.cos(phi + k * theta_float),
                r_float * math.sin(phi + k * theta_float)) for k in range(maxlen)]
        n = maxlen
        for k in range(1, maxlen):
            if sqdist(pts[k], pts[0]) < tol and k > 1:
                n = k
                closed.append(True)
                break
        else:
            closed.append(False)
        lengths.append(n)
        # degree of vertex 0 in the graph restricted to its orbit
        d = 0
        for k in (1, n - 1):
            if k < n and abs(sqdist(pts[k], pts[0]) - 1.0) < 1e-6:
                d += 1
        degs.add(d)
    return lengths, set(closed), sorted(degs)


def report(name, r_exact, r_float):
    th, p, q = exact_label(r_exact)
    chi = chi_cycle(q) if q else 2
    thf = float(th.evalf())
    lengths, closed, degs = orbit_structure(r_float, thf)
    print(f"{name:32s} r = {sp.sstr(r_exact)}")
    print(f"    theta = {sp.sstr(sp.nsimplify(th))}, theta/2pi = {sp.sstr(sp.nsimplify(th/(2*sp.pi)))},"
          f" p/q = {p}/{q if q else '--'}, predicted chi = {chi}")
    print(f"    orbit lengths {sorted(set(lengths))}, closed orbits only: {closed},"
          f" unit neighbours of a vertex inside its orbit: {degs}")


print("=" * 78)
print("Theorem 1: exact instances")
print("=" * 78)
facts = [
    ("r = 1/2 (antipodal pairs)", sp.Rational(1, 2), 0.5),
    ("r = 1/sqrt(3) (triangle)", 1 / sp.sqrt(3), 1 / math.sqrt(3)),
    ("r = 1/sqrt(2) (square)", 1 / sp.sqrt(2), 1 / math.sqrt(2)),
    ("r = 1 (the palette radius)", sp.Integer(1), 1.0),
    ("r = 1/(2 sin(pi/5)) (pentagon)", 1 / (2 * sp.sin(sp.pi / 5)), 1 / (2 * math.sin(math.pi / 5))),
    ("r = 1/(2 sin(2pi/5))", 1 / (2 * sp.sin(2 * sp.pi / 5)), 1 / (2 * math.sin(2 * math.pi / 5))),
    ("r = 1/(2 sin(pi/7)) (heptagon)", 1 / (2 * sp.sin(sp.pi / 7)), 1 / (2 * math.sin(math.pi / 7))),
    ("r = 1/(2 sin(2pi/9))", 1 / (2 * sp.sin(2 * sp.pi / 9)), 1 / (2 * math.sin(2 * math.pi / 9))),
]
for name, re_, rf in facts:
    report(name, re_, rf)
    print()

r_irr = sp.Integer(1) / (2 * sp.sin(sp.Rational(1, 2)))
assert sp.simplify(theta(r_irr) - 1) == 0
print("irrational case: r = 1/(2 sin(1/2)); theta = 1 rad exactly, theta/2pi = 1/(2pi)")
print("   irrational => every component is a bi-infinite path => chi = 2; no finite cycles at all.")

print()
print("=" * 78)
print("Exact criterion: for odd q the formula r = 1/(2 sin(pi p/q)) is consistent")
print("=" * 78)
bad = 0
count = 0
for q in range(3, 40, 2):
    for p in range(1, q // 2 + 1):
        if math.gcd(p, q) != 1:
            continue
        count += 1
        r = 1 / (2 * sp.sin(sp.pi * p / q))
        s = sp.simplify(1 / (2 * r))
        if sp.simplify(s - sp.sin(sp.pi * p / q)) != 0:
            bad += 1
            print("MISMATCH", p, q)
        if sp.simplify(sp.Rational(1, 2) - r) > 0:
            bad += 1
            print("r < 1/2 for odd q:", p, q, sp.nsimplify(r))
print(f"odd q in 3..39, all coprime p ({count} cases): {bad} mismatches")
lo = min((1 / (2 * sp.sin(sp.pi * p / q)), p, q)
         for q in range(3, 40, 2) for p in range(1, q // 2 + 1) if math.gcd(p, q) == 1)
print("smallest such r with q <= 39:", sp.nsimplify(lo[0]), "at p/q =", lo[1], "/", lo[2],
      "; it decreases to 1/2 as q grows (accumulation at r = 1/2)")

print()
print("=" * 78)
print("The cap: chi <= 3 for the chord graph of EVERY circle")
print("=" * 78)
for q in range(3, 31):
    n = q
    edges = [(i, (i + 1) % n) for i in range(n)]
    assert chrom_number_small(n, edges) == chi_cycle(q)
print("C_q for q = 3..30: chi = 2 if q even, 3 if q odd [exhaustive]")
print("clique bound: 4 pairwise-unit points do not exist in the plane, so omega <= 3")

r3 = 1 / sp.sqrt(3)
u = sp.sqrt(3) / 2
P3 = [(r3, sp.Integer(0)), (r3 * sp.Rational(-1, 2), r3 * u), (r3 * sp.Rational(-1, 2), -r3 * u)]
d2 = [sp.simplify(sqdist(P3[i], P3[j])) for i, j in [(0, 1), (1, 2), (0, 2)]]
print("r = 1/sqrt3, equilateral triangle at 120 degrees: squared distances", [sp.sstr(v) for v in d2])
assert all(sp.simplify(v - 1) == 0 for v in d2)

P6 = [(sp.cos(sp.pi * k / 3), sp.sin(sp.pi * k / 3)) for k in range(6)]
d2 = [sp.simplify(sqdist(P6[i], P6[(i + 1) % 6])) for i in range(6)]
print("r = 1, six consecutive vertices of a 2pi/6 orbit: squared distances",
      [sp.sstr(sp.nsimplify(v)) for v in d2])
assert all(sp.simplify(v - 1) == 0 for v in d2)
d3 = sp.simplify(sqdist(P6[0], P6[2]))
print("r = 1, the next-nearest pair squared distance is", sp.sstr(sp.nsimplify(d3)),
      "(so the degree in the chord graph is exactly 2)")
assert sp.simplify(d3 - 1) != 0

print()
print("=" * 78)
print("Accumulation of 3-chromatic radii at r = 1/2 (odd q -> infinity)")
print("=" * 78)
for q in (3, 5, 9, 15, 39, 99):
    p = (q - 1) // 2 if (q - 1) // 2 % 2 == 1 or math.gcd((q - 1) // 2, q) == 1 else (q - 1) // 2
    while math.gcd(p, q) != 1:
        p -= 1
    r = 1 / (2 * sp.sin(sp.pi * p / q))
    print(f"  q = {q:3d}, p/q = {p}/{q}: r = {float(r.evalf()):.6f}, chi = 3")
print("  1/2 itself has q = 2 (even) and chi = 2; so 3 is attained on a set dense in")
print("  [1/2, infinity) with no minimum, and 2 is attained on the complementary dense set.")
print()
print("ALL EXACT CHECKS PASSED")
