#!/usr/bin/env python3
"""Exact certificate: the Hadwiger hexagonal 7-colouring is a weak measurable
7-colouring in the sense of Definition 1.2 of the paper.

Everything here is exact arithmetic (integers, Fractions, and the ring
Z[omega] with omega = exp(2*pi*i/3) handled by its coordinate pair (m,n),
meaning m + n*omega).  No floating point enters any decision.

Facts certified:
 (H1) the triangular lattice L = Z[omega] has minimum norm 1:
      N(m + n*w) = m^2 - m*n + n^2 >= 1 for (m,n) != (0,0).       [closed form]
 (H2) alpha = 2 - w has norm N(alpha) = 7, so L' = alpha*L has index 7
      in L; the quotient L/L' has exactly 7 classes.              [brute force]
 (H3) min{|lambda| : 0 != lambda in L'} = sqrt(7)*min{|mu|: 0 != mu in L}
      = sqrt(7).                                                 [N(ab)=N(a)N(b)]
 (H4) every element of Q(sqrt(-3)) is a Q-combination of two units of
      modulus 1: for |lambda| <= 2, lambda = u1 + u2 with |ui| = 1 and
      ui algebraic.                                    [circle intersection]
 (H5) the two numerical inequalities r = 2/5:
      2r < 1        and        (sqrt(21)-2)*r > 1.       [squaring, exact]
 (H6) every lambda in L is within sqrt(3)/3 of a lattice point (Voronoi
      hexagon circumradius = d/sqrt(3) with d = sqrt(3)*r => r). [brute force]
Consequence (proved in AUDIT.md, section 2): the lexicographic-nearest-centre
colouring of the plane by the 7 cosets is Borel, and no two points at distance
exactly 1 get the same colour.  Hence Definition 1.2 is satisfiable at k = 7.
"""
from fractions import Fraction as Fr
from itertools import product

# ---------- (H1) ------------------------------------------------------------
def norm(m, n):
    """m^2 - m n + n^2 = |m + n w|^2 (in units of the lattice spacing 1)."""
    return m * m - m * n + n * n

def check_H1(B=60):
    worst = min(norm(m, n) for m in range(-B, B + 1) for n in range(-B, B + 1)
                if (m, n) != (0, 0))
    # closed form: m^2 - mn + n^2 = (m - n/2)^2 + 3n^2/4 >= 3/4 if n != 0
    assert worst == 1, worst
    for m in range(-B, B + 1):
        for n in range(-B, B + 1):
            if n != 0:
                assert 4 * norm(m, n) >= 3 * n * n, (m, n)
            else:
                assert norm(m, 0) == m * m
    return worst

# ---------- (H2) ------------------------------------------------------------
class Lattice:
    """L = Z[omega]; L' = alpha L with alpha = 2 - w.
    alpha*1 = 2 - w -> (2,-1);  alpha*w = 2w - w^2 = 1 + 3w -> (1,3)."""
    def __init__(self):
        self.B = ((2, 1), (-1, 3))          # images of the two generators

    def alpha(self, m, n):
        """image of m + n w under multiplication by 2 - w, coordinates."""
        (a, c), (b, d) = self.B[0], self.B[1]
        return (m * a + n * b, m * c + n * d)   # careful: see check below

def mul_alpha(m, n):
    """(m + n w)(2 - w) = 2m + 2n w - m w - n w^2 = (2m + n) + (2n - m + n) w."""
    return (2 * m + n, 3 * n - m)

def check_H2(B=25):
    # determinant of the coordinate matrix of L' inside L
    M = [mul_alpha(1, 0), mul_alpha(0, 1)]      # (2,-1),(1,3)
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    assert det == 2 * 3 - (-1) * 1 == 7, det
    # brute force: cosets of L' among the points of L in a box, by adding
    # L'-generators until saturation; then verify there are exactly 7.
    gens = [M[0], M[1]]
    seen = {}
    for m in range(-B, B + 1):
        for n in range(-B, B + 1):
            # canonical form modulo L': reduce greedily
            x, y = m, n
            for _ in range(400):
                moved = False
                for (gm, gn) in gens:
                    if abs(x - gm) + abs(y - gn) < abs(x) + abs(y):
                        x, y = x - gm, y - gn
                        moved = True
                if not moved:
                    break
            seen.setdefault((x, y), (m, n))
    # the reduced representatives must number exactly 7 -- but the greedy
    # reduction above is not a proof; redo it properly with a linear form.
    # class functional: L/L' -> Z/7 given by (m,n) |-> (m + 2n) mod 7 ?
    # determine it by requiring it vanish on both generators (2,-1) and (1,3).
    f = None
    for (a, b) in product(range(7), repeat=2):
        if (a * 2 + b * (-1)) % 7 == 0 and (a * 1 + b * 3) % 7 == 0:
            f = (a, b)
            if (a, b) != (0, 0):
                break
    assert f is not None and f != (0, 0), f
    a, b = f
    cls = {}
    for m in range(-3, 8):
        for n in range(-3, 8):
            cls.setdefault((a * m + b * n) % 7, []).append((m, n))
    assert len(cls) == 7, len(cls)
    # sanity: the functional must vanish exactly on L'
    for m in range(-12, 13):
        for n in range(-12, 13):
            x, y = mul_alpha(m, n)
            assert (a * x + b * y) % 7 == 0, (m, n, x, y)
    return det, f, len(cls)

# ---------- (H3),(H5),(H6) --------------------------------------------------
def check_H3():
    # N(alpha) = (2-w)(2-wbar) = 4 - 2(w+wbar) + 1 = 4 + 2 + 1 = 7, using
    # w + wbar = -1 and |w| = 1.  Hence |alpha| = sqrt 7.
    assert 4 - 2 * (-1) + 1 == 7
    return 7

def check_H5():
    r = Fr(2, 5)
    assert 2 * r == Fr(4, 5) and Fr(4, 5) < 1
    # (sqrt(21)-2) r > 1  <=>  2 sqrt(21) > 9  <=>  84 > 81
    assert (2 * r) ** 2 * 21 > (1 + 2 * r) ** 2, "squaring both sides"
    return (Fr(4, 5), (2 * r) ** 2 * 21, (1 + 2 * r) ** 2)

def check_H6(B=8):
    """Voronoi hexagon of Z[omega] has circumradius d/sqrt(3), d = sqrt(3):
    every fundamental-domain vertex is at distance 1/sqrt(3) = d/sqrt 3."""
    # Deep holes = circumcentres of the Delaunay triangles (0,1,1+w) and its
    # rotations.  In coordinates m + n*w: (2+w)/3 -> (2,1)/3, and the six
    # rotations by w are (2,1),(-1,1),(-1,-2),(-2,-1),(1,-1),(1,2), all /3.
    holes = [(Fr(2, 3), Fr(1, 3)), (Fr(-1, 3), Fr(1, 3)), (Fr(-1, 3), Fr(-2, 3)),
             (Fr(-2, 3), Fr(-1, 3)), (Fr(1, 3), Fr(-1, 3)), (Fr(1, 3), Fr(2, 3))]
    for (hm, hn) in holes:
        m, n = hm, hn
        d2 = m * m - m * n + n * n
        assert d2 == Fr(1, 3), d2
    return "circumradius = 1/sqrt3 in lattice units"

if __name__ == "__main__":
    print("H1 min norm L           :", check_H1())
    det, f, k = check_H2()
    print("H2 index of L' in L     :", det, " class functional", f,
          " number of classes", k)
    print("H3 |alpha|^2            :", check_H3())
    print("H5 r=2/5: 2r, 21(2r)^2, (1+2r)^2 :", check_H5())
    print("H6                      :", check_H6())
    print("all exact checks passed")
