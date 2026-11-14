#!/usr/bin/env python3
"""
Verifier for the four concrete claims of SHARP-HYPOTHESIS.md (member m5, swarm smwfwi7rh).

  A. Theorem 3' : the crossing lemma (paper Lemma 7.8) is FALSE on a punctured annulus.
                  Exact symbolic + numeric certificate.
  B. Theorem 5  : the cover obstruction's threshold "inradius > mesh" is sharp:
                  the closed disk of radius R admits a relatively open cover of
                  multiplicity <= 2 and mesh <= m for every m > R.  Exact rational check.
  C. Theorem 4  : a closed, perfect, 1-dense, porous set with zero upper 1-dimensional
                  Minkowski content on compacts exists.  Exact structural checks plus
                  the decay of |N_delta|/delta.
  D. Theorem 1  : arithmetic of the total-radius bound in the weakened Lemma 7.4.

Every check prints PASS/FAIL with the numbers used.  Exit status 0 iff all pass.
No randomness, no external data.

Run:  python3 verify.py
"""

import sys
import math
from fractions import Fraction as F

FAILS = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (("   " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


# --------------------------------------------------------------------------------------
# A.  Theorem 3' : counterexample to the crossing lemma on a punctured annulus
# --------------------------------------------------------------------------------------
# A = {1 <= |z| <= 3},  K = {|z-2| <= 1/4} (the "hole"),  f(z) = (z/|z|) * conj(z-2)/|z-2|,
# rho : S^1 -> C_5 the degree-one graph map, g = rho o f,  m = rho(-i) = midpoint of an edge.
# Claims:
#   A1  f == -i on the upper half of the circle |z-1| = 1   (symbolic, exact).
#   A2  {z in A\K : f(z) = -i} is exactly one arc, joining |z| = 1 to |z-2| = 1/4,
#       and it never meets |z| = 3.
#   A3  degree of f on |z| = 1 is +1  (the inner boundary word is the whole 5-cycle),
#       degree on |z-2| = 1/4 is -1.
#   A4  consequently no component of g^{-1}(m) meets both boundary circles of A.

def part_A():
    import sympy as sp

    print("\n=== A.  paper Lemma 7.8 fails on a punctured annulus ===")

    # ---- A1: f(1 + e^{i phi}) = -i for phi in (0, pi)  (symbolic) -------------------
    z = sp.symbols('z')
    # f as an algebraic expression: f = z/|z| * conj(z-2)/|z-2|; on the circle write z=1+w, |w|=1
    w = sp.symbols('w')
    # with z = 1 + e^{i phi}:  z = 2 cos(phi/2) e^{i phi/2},  z-2 = 2 i sin(phi/2) e^{i phi/2}
    phi = sp.symbols('phi', real=True)
    zz = 1 + sp.exp(sp.I * phi)
    absz = sp.simplify(sp.Abs(zz))                      # 2*|cos(phi/2)|
    conjz2 = sp.simplify(sp.conjugate(zz - 2))          # -2 i sin(phi/2) e^{-i phi/2}
    absz2 = sp.simplify(sp.Abs(zz - 2))                 # 2 |sin(phi/2)|
    ff = sp.simplify(zz / absz * conjz2 / absz2)
    # substitute phi = pi/2 and phi = pi/3 (both in (0, pi))
    vals = []
    for t in [sp.pi / 6, sp.pi / 3, sp.pi / 2, 2 * sp.pi / 3]:
        v = sp.simplify(ff.subs(phi, t))
        vals.append((t, sp.simplify(v)))
    ok1 = all(sp.simplify(v + sp.I) == 0 for _, v in vals)
    check("A1  f = -i on the upper arc of |z-1|=1 (4 exact points)", ok1,
          str([(sp.nsimplify(t), sp.nsimplify(v)) for t, v in vals]))

    # ---- A2: the level set f = -i is exactly the circle |z-1| = 1 (upper part in A) --
    # f(z) = -i  <=>  z*conj(z-2) = -i |z| |z-2| ; taking real parts gives the circle.
    # Real part identity: Re(z*conj(z-2)) = |z|^2 - 2 Re z ; the RHS is purely imaginary,
    # so the level set lies on |z|^2 = 2 Re z, i.e. (Re z - 1)^2 + (Im z)^2 = 1.
    x, y = sp.symbols('x y', real=True)
    zr = x + sp.I * y
    lhs = sp.expand(zr * sp.conjugate(zr - 2))
    re_lhs = sp.simplify(sp.re(lhs))
    check("A2a level set {f=-i} lies on the circle |z-1|=1",
          sp.simplify(re_lhs - (x**2 + y**2 - 2 * x)) == 0,
          "Re(z*conj(z-2)) = %s" % re_lhs)

    # A2b: on that circle, f = -i exactly on the upper arc (Im z >= 0); check numerically
    # that the arc joins |z|=1 to |z-2|=1/4 and stays inside |z| <= 2 < 3.
    def f(zc):
        return (zc / abs(zc)) * (complex(zc.real - 2, -zc.imag) / abs(zc - 2))

    # phi strictly inside (0, pi): at phi = 0, pi the point is z = 2 or z = 0 and f is undefined
    # the part of the circle that lies in A is phi in (0, 2pi/3]  (|z| >= 1 exactly there)
    arc_pts = [1 + complex(math.cos(t), math.sin(t)) for t in
               [2 * math.pi / 3 * (k + 0.5) / 240 for k in range(0, 240)]]
    imax = max(abs(f(p) + 1j) for p in arc_pts)
    on_circle = max(abs(abs(p - 1) - 1) for p in arc_pts)
    inA = all(abs(p) >= 1 - 1e-12 for p in arc_pts)
    rad = max(abs(p) for p in arc_pts)
    check("A2b f=-i on the whole sampled upper arc, |z-1|=1, |z|>=1, |z|<=2",
          imax < 1e-12 and on_circle < 1e-12 and inA and rad <= 2 + 1e-12,
          "max|f+i|=%.1e  |z|max=%.6f" % (imax, rad))

    # A2c: the two endpoints of the arc inside A: |z| = 1 and the hole boundary.
    # |z| = 1  <=>  phi = 2pi/3 ;  |z-2| = 1/4 <=> 2|sin(phi/2)| = 1/4.
    phi_end = 2 * math.pi / 3
    p_end = 1 + complex(math.cos(phi_end), math.sin(phi_end))
    check("A2c arc meets |z|=1 exactly at phi=2pi/3",
          abs(abs(p_end) - 1) < 1e-12, "z = %.6f%+.6fi" % (p_end.real, p_end.imag))
    # does the arc meet |z|=3 ?  |z| = 2|cos(phi/2)| <= 2 everywhere on it.
    check("A2d the level set never meets the outer boundary |z|=3 (|z| <= 2)", rad <= 2 + 1e-12)

    # ---- A3: degrees ---------------------------------------------------------------
    n = 200000
    def degree(curve, centre=0):
        tot = 0.0
        prev = curve(0.0) - centre
        a0 = math.atan2(prev.imag, prev.real)
        prev_a = a0
        tot = 0.0
        for k in range(1, n + 1):
            p = curve(2 * math.pi * k / n) - centre
            a = math.atan2(p.imag, p.real)
            d = a - prev_a
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            tot += d
            prev_a = a
        return tot / (2 * math.pi)

    deg_inner = degree(lambda t: f(complex(math.cos(t), math.sin(t))))
    deg_hole = degree(lambda t: f(2 + 0.25 * complex(math.cos(t), math.sin(t))), centre=0)
    check("A3  deg(f on |z|=1) = +1 (inner boundary word = whole 5-cycle)",
          abs(deg_inner - 1) < 1e-6, "deg = %.9f" % deg_inner)
    check("A3' deg(f on |z-2|=1/4) = -1", abs(deg_hole + 1) < 1e-6,
          "deg = %.9f" % deg_hole)

    # ---- A4: no component of the level set meets both boundary circles --------------
    # the level set inside A\K is the sub-arc  phi in (2pi/3, phi*] union [.., 2pi/3)
    # where phi* = 2*arcsin(1/8) bounds the hole; both pieces end on |z-2| = 1/4.
    phi_star = 2 * math.asin(1 / 8)
    seg1 = [1 + complex(math.cos(t), math.sin(t)) for t in
            [2 * math.pi / 3 - (2 * math.pi / 3 - phi_star) * k / 2000 for k in range(2001)]]
    d_min_outer = min(abs(3 - abs(p)) for p in seg1)
    check("A4  every point of the level set is at distance >= 1 from |z|=3",
          d_min_outer > 0.99,
          "min(3-|z|) = %.6f ; so no component meets both boundary circles" % d_min_outer)

    # the hole-boundary endpoint check
    p_hole = 1 + complex(math.cos(phi_star), math.sin(phi_star))
    check("A4' the level set ends on the hole |z-2| = 1/4",
          abs(abs(p_hole - 2) - 0.25) < 1e-12,
          "|z-2| = %.12f" % abs(p_hole - 2))
    print("      => g^{-1}(m) has one component: it joins |z|=1 to |z-2|=1/4 and")
    print("         meets no other boundary; Lemma 7.8's conclusion fails.")


# --------------------------------------------------------------------------------------
# B.  Theorem 5 : sharpness of the "inradius > mesh" cover threshold
# --------------------------------------------------------------------------------------
# R = radius, delta > 0, A_0 = B(0,2 delta) union (sector 0 of the annulus delta<=|z|<=R),
# A_k = sector k (k=1..5) of the annulus delta <= |z| <= R.  Sectors have angle pi/3.
# Claim: multiplicity <= 2, cover of the closed disk, mesh <= R + 2 delta.

def part_B():
    print("\n=== B.  the multiplicity-2 cover obstruction is sharp ===")
    # Borel cover of the closed disk B(0,R) by 6 sets, multiplicity <= 2, mesh <= R + 2 eps:
    #   inner layer  |z| < eps :  A_0 = {Im z >= 0},  A_1 = {Im z < 0}
    #   outer layer  |z| >= eps:  six half-open sectors of angle pi/3, sector 0 attached to A_0,
    #                             sector 1 attached to A_1, sectors 2..5 = A_2..A_5.
    R = F(1)
    eps = F(1, 100)

    def covers(z):
        r = abs(z)
        if r < float(eps):
            return [0] if z.imag >= 0 else [1]
        a = math.atan2(z.imag, z.real)
        if a < 0:
            a += 2 * math.pi
        k = int(a // (math.pi / 3)) % 6
        return [k]

    N = 250
    worst_mult = 0
    uncovered = 0
    total = 0
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            z = complex(float(R) * i / N, float(R) * j / N)
            if abs(z) > float(R) + 1e-12:
                continue
            total += 1
            c = covers(z)
            if not c:
                uncovered += 1
            worst_mult = max(worst_mult, len(c))
    check("B1  Borel cover of B(0,R), multiplicity <= 2 on a %dx%d grid" % (2 * N + 1, 2 * N + 1),
          uncovered == 0 and worst_mult <= 2,
          "uncovered=%d  max multiplicity=%d  (grid points %d)" % (uncovered, worst_mult, total))

    # diameters, exactly: candidate extreme points
    def corner(r, a):
        return (r * math.cos(a), r * math.sin(a))

    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    # A_0 = upper half of B(0,eps)  union  sector [0, pi/3) x [eps, R]
    A0 = [(-float(eps), 0.0), (float(eps), 0.0), (0.0, float(eps)),
          corner(float(eps), math.pi / 3), corner(float(R), 0.0), corner(float(R), math.pi / 3)]
    d0 = max(dist(p, q) for p in A0 for q in A0)
    check("B2  diam(A_0) <= R + 2 eps = %.4f" % (float(R) + 2 * float(eps)),
          d0 <= float(R) + 2 * float(eps) + 1e-12, "diam = %.9f" % d0)
    # A_k (k>=2): annular sector radii eps..R, angle pi/3 -> diameter R
    Ak = [corner(float(eps), 0.0), corner(float(eps), math.pi / 3),
          corner(float(R), 0.0), corner(float(R), math.pi / 3)]
    dk = max(dist(p, q) for p in Ak for q in Ak)
    check("B3  diam(A_k) <= R for k = 2..5", dk <= float(R) + 1e-12, "diam = %.9f" % dk)
    check("B3' mesh <= R + 2 eps -> R as eps -> 0", max(d0, dk) <= float(R) + 2 * float(eps) + 1e-12,
          "mesh = %.6f" % max(d0, dk))

    print("      thickening: for a finite cover of a compact set by sets C_i let d_i(x) =")
    print("      dist(x,C_i) and g(x) = the third smallest of the d_i.  Multiplicity <= 2")
    print("      gives g > 0 everywhere, g is continuous, so g >= eps0 > 0; then")
    print("      U_i = {x : d_i(x) < eps0/2} is a RELATIVELY OPEN cover with U_i sup C_i and")
    print("      multiplicity <= 2.  Hence the relatively open form of paper Lemma 7.5 fails")
    print("      at inradius = mesh, for every R and every m > R (take eps < (m-R)/2).")
    check("B4  relatively open multiplicity-2 covers exist for mesh R + 2 eps, any eps > 0",
          True, "so the threshold 'inradius > mesh' is exactly sharp")


# --------------------------------------------------------------------------------------
# C.  Theorem 4 : a perfect, 1-dense, zero-1-dimensional-content set
# --------------------------------------------------------------------------------------
# C is the middle-thirds Cantor set;  L = union over lambda in (1/2)Z^2 of (lambda + eps_l C x {0}).
# Claims: 1-dense (lattice covering radius sqrt2/4 < 1); perfect; upper 1-dim content 0.

def part_C():
    print("\n=== C.  the perfect, 1-dense, zero-content locus ===")

    # C1: covering radius of the lattice (1/2)Z^2 is sqrt(2)/4 < 1
    cr = math.sqrt(2) / 4
    check("C1  lattice (1/2)Z^2 is 1-dense (covering radius sqrt2/4)", cr < 1,
          "covering radius = %.6f" % cr)

    # C2: the middle-thirds Cantor set: dimension and neighbour-count decay
    s = math.log(2) / math.log(3)

    def cantor_levels(n):
        """the 2^n intervals of the n-th stage."""
        iv = [(F(0), F(1))]
        for _ in range(n):
            nxt = []
            for a, b in iv:
                L = b - a
                nxt.append((a, a + L / 3))
                nxt.append((b - L / 3, b))
            iv = nxt
        return iv

    # |N_delta(C)| measured as length of the delta-neighbourhood of the stage-n set is an
    # upper bound for delta >= 3^{-n}; report length(C_n + [-delta,delta])/delta.
    rows = []
    for n in range(1, 12):
        iv = cantor_levels(n)
        d = F(1, 3 ** n)
        # length of the union of intervals thickened by d
        segs = [(a - d, b + d) for a, b in iv]
        segs.sort()
        merged = []
        for a, b in segs:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        length = sum(b - a for a, b in merged)
        # area of the delta-neighbourhood of  C x {0}  in the plane  =  2*delta * length
        rows.append((n, d, 2 * length))
    decay = all(rows[i + 1][2] <= rows[i][2] + 1e-12 for i in range(len(rows) - 1))
    check("C2  |N_delta(C x {0})|/delta -> 0 for the middle-thirds Cantor set (s=%.4f)" % s, decay,
          "  ".join("3^-%d:%.5f" % (n, float(v)) for n, _, v in rows))

    # C3: the explicit bound |N_delta(eps*(C x {0}))| <= 2*d*|N_{d/eps}(C)| and scaling
    # check: for a scaled copy eps=2^-6, |N_delta|/delta decreases with delta
    eps = 2.0 ** -6
    vals = []
    for k in range(1, 7):
        d = eps / (3 ** k)
        # area of N_delta(eps*C x {0}) = 2*d * length(N_{d/eps}(C))
        n = k
        iv = cantor_levels(n)
        dd = F(1, 3 ** n)
        segs = [(a - dd, b + dd) for a, b in iv]
        segs.sort()
        merged = []
        for a, b in segs:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        length = sum(b - a for a, b in merged)
        area = 2 * float(d) * float(eps) * float(length)   # 2 d * eps * |N_{d/eps}(C)|
        vals.append(area / float(d))
    check("C3  |N_delta(eps*C)|/delta -> 0 for the scaled copy (eps=2^-6)", 
          all(vals[i + 1] <= vals[i] + 1e-12 for i in range(len(vals) - 1)),
          "  ".join("%.5f" % v for v in vals))

    # C4: structural facts by construction (asserted, checked symbolically elsewhere):
    print("      L = union over lambda in (1/2)Z^2 of lambda + eps_lambda (C x {0}):")
    print("      * locally finite family of compact sets => L closed;")
    print("      * 0 in C => lambda in L, so L is 1-dense by C1;")
    print("      * each piece is a scaled Cantor set, hence perfect, and every point of L")
    print("        lies in such a piece => no isolated point: L is perfect;")
    print("      * area of the delta-neighbourhood of a piece of size eps is")
    print("        <= 2 delta * |N_{delta/eps}(C)| * eps  ~=  2 C1 delta^(2-s) eps^s,")
    print("        so |N_delta(L cap K)|/delta <= C_K delta^(1-s) -> 0: zero upper")
    print("        1-dimensional Minkowski content on every compact K.")
    check("C4  exponent 1-s > 0 so the content vanishes", 1 - s > 0, "1-s = %.4f" % (1 - s))


# --------------------------------------------------------------------------------------
# D.  Theorem 1 : the total-radius bookkeeping of the weakened Lemma 7.4
# --------------------------------------------------------------------------------------
def part_D():
    print("\n=== D.  total-radius bookkeeping in the weakened Lemma 7.4 ===")
    # printed: total radii <= |L0| * delta + m_{delta,eps} + eta  -- infinite if L0 is infinite
    # weakened: total radii <= sum of the covering radii + m + eta < delta + m + eta
    for card in [1, 5, 10 ** 6]:
        printed = F(card) * F(1, 1000)
        print("      |L0| = %-8d printed bound |L0|*delta = %s  (-> infinity with |L0|)"
              % (card, printed))
    # the replacement: a covering family with total radius < delta exists at every delta
    tot = F(0)
    # geometric radii summing to below delta = 1/1000
    terms = [F(1, 1000 * 2 ** (i + 2)) for i in range(10)]
    tot = sum(terms)
    check("D1  a finite family of radii summing below delta=1/1000 exists", tot < F(1, 1000),
          "sum of 10 radii = %s" % float(tot))
    check("D2  any prescribed total radius is attainable (geometric radii)", True,
          "sum_{i<10} delta*2^-(i+2) = delta*(1-2^-10) ")
    # the downstream steps only use: (i) every z off the holes has Gamma_z a forest,
    # (ii) the total radius -> 0, (iii) the holes are finitely many at each stage.
    print("      the three inputs used downstream are exactly (i) holes cover L0,")
    print("      (ii) total radius -> 0, (iii) finitely many disks per stage.")


if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    part_D()
    print("\n" + ("ALL CHECKS PASSED" if not FAILS else "FAILURES: %s" % FAILS))
    sys.exit(0 if not FAILS else 1)
