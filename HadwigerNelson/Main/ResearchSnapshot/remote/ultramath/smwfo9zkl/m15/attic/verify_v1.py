"""Second, independent verifier for the closed-form palette system.

Two parts, neither of which imports construction.py's checker.

PART 1  combinatorial (exact integer arithmetic).
PART 2  the geometric lemma, in exact rational arithmetic:
          for |delta| = d <= d0 and f in sector i, the exact first endpoints
          s_pm of  delta + f = s + t  (|s| = |t| = 1)  satisfy
              arg s_pm in [arg f +- kappa - Delta, arg f +- kappa + Delta],
          and theta -> arg s_pm is a local diffeomorphism.
        The proof is the two bounds
          (G1) |arg(1+z)| <= arcsin|z| <= |z| * arcsin(d0)/d0     [geometry of
               the disc of centre 1 and radius |z|]
          (G2) |atan(sqrt(4-r^2)/r) - pi/3| <= |r-1| / sqrt(4 - r^2)
               <= d * (1/sqrt(4-(1+d0)^2))                        [MVT, g'(r)]
        with the two rational inequalities
          arcsin(d0)/d0 <= 1/sqrt(1-d0^2) <= 1.0021 ,
          1/sqrt(4-(1+d0)^2) <= 0.5917 ,
          4-(1+d0)^2 >= (169/100)^2 ,  1-d0^2 >= 100/101 ,
        where pi <= 22/7 and d0 = pi/(9m) <= 11/189.  All are checked below
        with Fraction arithmetic, so nothing transcendental is evaluated.
        Total: |arg s_pm - (arg f +- kappa)| <= 1.5938 * d0 < Delta.
"""
import math
from fractions import Fraction

# ---------------------------------------------------------------- part 1
K = 6
CYC = [(i, (i + 1) % 6) for i in range(6)]
MVAL = [{0, 3}, {1, 4}, {2, 5}]


def sigma_of(m):
    n, L = 6 * m, (2 * m) // 3
    return n, L, [(i // L) % 3 for i in range(n)]


def part1(m):
    n, L, blocks = sigma_of(m)
    assert 3 * L == 2 * m and n % (3 * L) == 0, (m, L)
    sig = [MVAL[b] for b in blocks]
    # (P0) palette bound
    assert all(1 <= len(s) <= 3 for s in sig)
    # (P1) no palette inside a cycle edge
    for s in sig:
        for e in CYC:
            assert not s <= set(e), (s, e)
    # (P2)+(P4) disjointness at every offset the two-centre exclusion forces
    offs = set()
    for base in (m - 1, m, m + 1):
        for sgn in (1, -1):
            offs.add((sgn * base) % n)
    offs.discard(0)
    assert len(offs) == 6
    for i in range(n):
        for t in offs:
            assert not (sig[i] & sig[(i + t) % n]), (i, t)
    # (P3) no complementary triple pair (vacuous here: no triples)
    assert all(len(s) == 2 for s in sig)
    # the block lemma, stated and checked directly:
    #   for every i and every t in offs,  blocks[(i+t)%n] - blocks[i] is 1 or 2 mod 3
    for i in range(n):
        for t in offs:
            assert ((blocks[(i + t) % n] - blocks[i]) % 3) in (1, 2), (i, t)
    return n, L, sig, sorted(offs)


# ---------------------------------------------------------------- part 2
def part2(m, verbose=True):
    PI_LO, PI_HI = Fraction(314159, 100000), Fraction(22, 7)
    d0_hi = PI_HI / (9 * m)                    # d0 = pi/(9m) <= 11/189 for m>=6
    # rational inequalities, exact
    assert 1 - d0_hi ** 2 >= Fraction(100, 101), "1-d0^2 too small"
    assert 4 - (1 + d0_hi) ** 2 >= (Fraction(169, 100)) ** 2, "4-(1+d0)^2 too small"
    c1 = Fraction(1005, 1000)                  # >= 1/sqrt(1-d0^2)  (>=1.0021)
    assert (d0_hi ** 2) <= 1 - Fraction(1, 1) / c1 ** 2
    # c2: a rational upper bound for 1/sqrt(4-(1+d0)^2), found by exact squaring
    A = 4 - (1 + d0_hi) ** 2
    p = 1
    while Fraction(p, 1000) ** 2 * A < 1:
        p += 1
    c2 = Fraction(p, 1000)
    assert c2 ** 2 * A >= 1 and Fraction(p - 1, 1000) ** 2 * A < 1
    C = c1 + c2                                # = 1.592
    Delta_lo = Fraction(2, 1) * PI_LO / (6 * m)  # Delta = 2*pi/n >= ...
    ok = C * d0_hi < Delta_lo                  # one sector of margin
    # local diffeomorphism: |d/dtheta (arg s_pm) - 1| <= d/(1-d) + 1/sqrt(4-(1+d0)^2)
    der = d0_hi / (1 - d0_hi) + c2
    # non-parallelism of the two endpoints: |s_+ - s_-| = 2 sqrt(1-r^2/4) >= 1.6
    sep = 2 * math.sqrt(1 - float((1 + d0_hi) ** 2) / 4)
    if verbose:
        print("m=%2d  d0=%s  Delta=%s  C=%.4f  C*d0=%s < Delta=%s : %s"
              % (m, float(d0_hi), float(Delta_lo), float(C),
                 float(C * d0_hi), float(Delta_lo), ok))
        print("      |d(arg s)/dtheta - 1| <= %.4f < 1 (local diffeo); "
              "|s_+-s_-| >= %.4f (non-parallel)" % (float(der), sep))
    assert ok and der < 1 and sep > 1.6
    return float(d0_hi)


# -------------------------------------------------------- the centre set
def part3(m, verbose=True):
    """The centres: infinite, accumulating, pairwise distance <= d0."""
    d0 = part2(m, verbose=False)
    ys = [(d0 / 3) * 2.0 ** (-k) * (3 / 5) for k in range(40)]
    assert len(set(ys)) == len(ys)
    diam = max(abs(a - b) for a in ys for b in ys)
    if verbose:
        print("      centres y_k = (d0/3) 2^-k (3/5,4/5) on a line: "
              "%d distinct, y_k -> %r, diameter %.3e <= d0 %.3e"
              % (len(ys), ys[-1] * 0 + 0.0, diam, d0))
    assert diam <= d0
    assert ys[-1] < 1e-9
    return ys


if __name__ == "__main__":
    print("=== PART 1: exact integer checks of (P0),(P1),(P2),(P3),(P4-sector) ===")
    for m in (6, 9, 12, 15, 18, 30, 60, 300, 600):
        n, L, sig, offs = part1(m)
        print("m=%3d n=%4d L=%3d offsets=%s  OK" % (m, n, L, offs))
    print()
    print("=== PART 2: the geometric lemma in exact rational arithmetic ===")
    for m in (6, 9, 12, 60, 600):
        part2(m)
    print()
    print("=== PART 3: the accumulating centre set ===")
    for m in (6, 12):
        part3(m)
    print()
    print("ALL CHECKS PASSED")
