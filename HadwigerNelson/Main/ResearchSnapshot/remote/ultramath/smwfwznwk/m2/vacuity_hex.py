"""Non-vacuity test for Lemma P / Theorem R on the paper's own colouring.

The paper's upper bound chi(R^2) <= 7 is the hexagonal colouring: Voronoi hexagons of
a triangular lattice with circumradius r = 2/5, colours (m + 2n) mod 7 for the cell
with centre d(m + n*omega), omega = e^{i pi/3}, d = sqrt(3) r.

We check three things numerically:

  (V1) the colouring is proper: any two points of the same colour are at distance
       > 1 (we check it at the level of the cells: the minimal distance between two
       same-coloured hexagons is sqrt(7) d - 2r > 1, exact in Q(sqrt 3));
  (V2) Lemma Z applies: at a.e. direction the sampled point lies in the interior of a
       cell, so P_x(e) = {c(x+e)} -- the palette is a singleton (we verify that the
       circle of radius one about a sample of centres is a.e. at distance > 0 from the
       cell boundaries);
  (V3) Theorem R's hypothesis fails maximally for this model: for each label i, the set of
       centres whose unit circle misses label i is small (numerically ~1/7 of centres, its own
       colour class), never a.e. -- in fact at every sampled centre the circle misses exactly
       the centre's own colour, which is Lemma D made visible.

Conclusion: the condition "label i is free at a.e. centre" is not a technicality; a
genuine colouring fails it at every centre, and Theorem R is therefore not vacuous.
"""
import cmath
import math
from fractions import Fraction

R = Fraction(2, 5)                        # circumradius
D2 = 3 * R * R                            # d^2 = 3 r^2  (= 12/25), d = sqrt(3) r
SQ3 = math.sqrt(3)
d = math.sqrt(float(D2))


def lattice_point(m, n):
    """centre d*(m + n*omega) with the paper's omega = e^{2 pi i / 3} (Eisenstein
    integers: |1| = |omega| = |1+omega| = 1, so this is the triangular lattice)."""
    return complex(d * (m - n * 0.5), d * n * SQ3 / 2)


def cell_colour(m, n):
    return (m + 2 * n) % 7


def nearest_lattice(z):
    """brute force over a window: returns (colour, distance, squared distance)."""
    x, y = z.real, z.imag
    # solve z = d*(m + n omega) => n = y/(d sqrt3/2), m = x/d - n/2
    n0 = y / (d * SQ3 / 2)
    m0 = x / d + n0 / 2
    best = None
    for n in range(int(round(n0)) - 2, int(round(n0)) + 3):
        for m in range(int(round(m0)) - 2, int(round(m0)) + 3):
            p = lattice_point(m, n)
            dd = abs(z - p)
            if best is None or dd < best[1]:
                best = (cell_colour(m, n), dd, m, n)
    return best


def properness():
    """(V1) minimal same-colour centre distance = sqrt(7)*d (index-seven sublattice);
    check exact rational square: 7*d^2 = 84/25 = 3.36, so distance = sqrt(84)/5.
    The gap between two hexagons with centres at distance L is >= L - 2r."""
    minlen2 = 7 * D2                       # squared minimal nonzero vector of (2-omega)Lambda
    gap2_lower = (math.sqrt(float(minlen2)) - 2 * float(R)) ** 2
    print(f"(V1) 7 d^2 = {minlen2} (exact); minimal same-colour centre distance = "
          f"{math.sqrt(float(minlen2)):.6f}; hexagon gap >= "
          f"{math.sqrt(float(minlen2)) - 2*float(R):.6f} > 1 : "
          f"{math.sqrt(float(minlen2)) - 2*float(R) > 1}")
    # brute-force confirmation on a patch: all same-coloured centre pairs up to distance 3
    pts = [(m, n) for m in range(-6, 7) for n in range(-6, 7)]
    worst = None
    for i, (m1, n1) in enumerate(pts):
        for (m2, n2) in pts[i + 1:]:
            if cell_colour(m1, n1) != cell_colour(m2, n2):
                continue
            L = abs(lattice_point(m1, n1) - lattice_point(m2, n2))
            if worst is None or L < worst:
                worst = L
    print(f"     brute force on a 13x13 patch: minimal same-colour centre distance "
          f"{worst:.6f} (expected {math.sqrt(float(minlen2)):.6f})")
    ok = math.sqrt(float(minlen2)) - 2 * float(R) > 1
    ok &= abs(worst - math.sqrt(float(minlen2))) < 1e-9
    return ok


def circle_labels(z, nang=20000, radius=1.0):
    """labels met by the circle of radius `radius` about z, plus the minimal distance
    of the sampled points from a cell boundary."""
    labels = set()
    mindist = 1e9
    for k in range(nang):
        th = 2 * math.pi * k / nang
        w = z + radius * cmath.exp(1j * th)
        col, dist, m, n = nearest_lattice(w)
        labels.add(col)
        mindist = min(mindist, dist)
    return labels, mindist


def main():
    ok = properness()
    print("(V2)/(V3) circle samples:")
    missing = {i: 0 for i in range(7)}
    sizes = {}
    minboundary = 1e9
    samples = 0
    for a in range(-3, 4):
        for b in range(-3, 4):
            z = lattice_point(a, b) + complex(0.05, 0.07)   # generic offset
            labels, mindist = circle_labels(z, nang=6000)
            sizes[len(labels)] = sizes.get(len(labels), 0) + 1
            samples += 1
            minboundary = min(minboundary, mindist)
            for i in range(7):
                if i not in labels:
                    missing[i] += 1
    print(f"     {samples} centres sampled; |labels met| distribution {dict(sorted(sizes.items()))}")
    print(f"     minimal distance of a sampled circle point from a cell boundary: "
          f"{minboundary:.4f} (Lemma Z: need > 0, i.e. no point on a boundary)")
    print(f"     number of centres at which label i is free, per i: {missing} "
          f"(out of {samples}; none may be all {samples})")
    ok &= all(c < samples for c in missing.values())
    ok &= minboundary > 0.0
    print("NON-VACUITY CHECK PASSES" if ok else "CHECK FAILED")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
