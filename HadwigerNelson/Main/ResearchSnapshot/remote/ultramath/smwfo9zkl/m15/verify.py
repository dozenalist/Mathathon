"""Independent verifier for the construction of construction.py.

This file shares no code with construction.py or with the SAT encoding.
It re-derives the sector schedule from the definition and checks every
assertion; Part 2 proves Lemma G in exact rational arithmetic.

Lemma G.  Let f be a unit complex number, thetax = arg f, delta a complex
number with |delta| = d <= d0 <= pi/54, and let s, t be the two unit vectors
with delta + f = s + t, i.e. s is one of
     s_pm = w/2 +- i (w/|w|) sqrt(1-|w|^2/4),  w = delta + f .
Then
   (i)    |arg s_pm - (thetax +- pi/3)| <= 1.6 d0,
   (ii)   theta -> arg s_pm is a local diffeomorphism (|d/dtheta - 1| <= 0.66),
   (iii)  |s_+ - s_-| >= 1.69, so the two endpoints are non-parallel.

Proof.  Write r = |w| in [1-d0, 1+d0].  Then
   arg s_pm = arg w +- atan( sqrt(4-r^2) / r ),
   arg w - thetax = arg(1 + delta/f).
(a) The point 1+z with |z| <= d0 lies in the closed disc of centre 1 and
    radius d0, so |arg(1+z)| <= arcsin(d0) <= d0/sqrt(1-d0^2).
(b) g(r) := atan(sqrt(4-r^2)/r) has g(1) = pi/3 and g'(r) = -1/sqrt(4-r^2),
    so |g(r) - pi/3| <= d0 / sqrt(4-(1+d0)^2) by the mean value theorem.
(c) |arg w - thetax| = |arg(1+delta/f)| and, with z = delta/f,
    d/dthetax arg(1+z) = Im[-iz/(1+z)], of modulus <= d0/(1-d0);
    also |dr/dthetax| <= 1 and |g'| <= 1/sqrt(4-(1+d0)^2).
So (i) holds with arcsin(d0)/d0 + 1/sqrt(4-(1+d0)^2) <= 1.6, and (ii) with
d0/(1-d0) + 1/sqrt(4-(1+d0)^2) <= 0.66.  Part (iii) is
|s_+ - s_-| = 2 sqrt(1 - r^2/4) >= 2 sqrt(1 - (1+d0)^2/4) >= 1.69.
The numeric bounds are checked below with Fraction arithmetic using
pi <= 22/7, i.e. d0 <= 11/189; no transcendental value is evaluated.
"""
import math
import sys
from fractions import Fraction

# ---------------------------------------------------------------- part 1
K = 6
AVALS = {6: [(0, 3), (1, 4), (2, 5)],
         5: [(0, 2), (1, 3), (5, )],
         4: [(0, 2), (4, ), (5, )],
         3: [(3, ), (4, ), (5, )]}


def schedule(ell, m):
    """Rebuild sigma with a while loop, independently of construction.py."""
    n = 6 * m
    L = (2 * m) // 3
    assert 3 * L == 2 * m and n % (3 * L) == 0
    sig, i, b = [], 0, 0
    while i < n:
        for _ in range(L):
            sig.append(set(AVALS[ell][b]))
            i += 1
        b = (b + 1) % 3
    return n, L, sig


def part1(ell, m):
    n, L, sig = schedule(ell, m)
    edges = [frozenset(sorted((i, (i + 1) % ell))) for i in range(ell)]
    forced = sorted({t % n for b in (m - 1, m, m + 1)
                     for t in (b, -b)} - {0})
    assert len(forced) == 6
    for i in range(n):
        assert 1 <= len(sig[i]) <= K - 3                      # (P0)
        for e in edges:
            assert not sig[i] <= e                            # (P1)
        for t in forced:
            assert not (sig[i] & sig[(i + t) % n])            # (P2),(P4)
    used = {frozenset(s) for s in sig}
    for u in used:                                            # (P3)
        assert not (len(u) == 3 and frozenset(set(range(6)) - set(u)) in used)
    return n, L, sig, forced


# ---------------------------------------------------------------- part 2
def part2(m):
    d0 = Fraction(22, 7) / (9 * m)          # d0 = pi/(9m) <= 11/189
    A = 4 - (1 + d0) ** 2                   # lower bound for 4 - r^2
    B = 1 - d0 ** 2                         # lower bound for 1 - |z|^2
    assert Fraction(1005, 1000) ** 2 * B >= 1        # 1/sqrt(B) <= 1.005
    c2 = Fraction(next(p for p in range(1, 2000)
                       if Fraction(p, 1000) ** 2 * A >= 1), 1000)
    C = Fraction(1005, 1000) + c2
    Delta = 2 * Fraction(314159, 100000) / (6 * m)   # pi >= 3.14159
    assert C * d0 < Delta                            # (i)
    ders = d0 / (1 - d0) + c2
    assert ders <= Fraction(66, 100)                 # (ii)
    assert 4 * (1 - (1 + d0) ** 2 / 4) >= Fraction(169, 100) ** 2   # (iii)
    return float(d0), float(Delta), float(C), float(ders)


def part2_numeric(m, samples=20000):
    """Floating-point sanity check of Lemma G against the exact formula."""
    d0 = math.pi / (9 * m)
    worst = 0.0
    kap = math.pi / 3
    for j in range(samples):
        th = 2 * math.pi * j / samples
        f = complex(math.cos(th), math.sin(th))
        for phi in (0.0, 1.0, 2.5, 4.0):
            for frac in (0.1, 0.5, 1.0):
                d = d0 * frac
                delta = d * complex(math.cos(phi), math.sin(phi))
                w = delta + f
                r = abs(w)
                h = math.sqrt(max(0.0, 1 - r * r / 4))
                for sgn in (1, -1):
                    s = w / 2 + sgn * 1j * (w / r) * h
                    diff = math.atan2(s.imag, s.real) - (th + sgn * kap)
                    diff = (diff + math.pi) % (2 * math.pi) - math.pi
                    worst = max(worst, abs(diff))
    return worst / d0


# ------------------------------------------------------------ part 3
def part3(m):
    d0 = math.pi / (9 * m)
    ys = [(d0 / 3) * 2.0 ** (-k) for k in range(64)]
    assert len(set(ys)) == len(ys) and ys[-1] < 1e-18
    assert max(abs(a - b) for a in ys for b in ys) <= d0
    return d0, ys


if __name__ == "__main__":
    print("=== PART 1: exact re-check of the construction (independent code) ===")
    for ell in (3, 4, 5, 6):
        for m in (6, 12, 30, 300):
            n, L, sig, forced = part1(ell, m)
        print("  ell=%d  n=%d L=%d  forced offsets %s  OK"
              % (ell, n, L, forced))
    print()
    print("=== PART 2: Lemma G in exact rational arithmetic ===")
    for m in (6, 12, 60, 600):
        d0, Delta, C, ders = part2(m)
        print("  m=%3d  d0=%.6f  Delta=%.6f  C=%.3f  C*d0=%.5f < Delta  "
              "deriv bound=%.3f < 0.66" % (m, d0, Delta, C, C * d0, ders))
    print("  floating-point sanity check (m=6): sup |arg s - (theta+-kappa)|/d0"
          " = %.4f   (rigorous bound %.4f)"
          % (part2_numeric(6), part2(6)[2]))
    print()
    print("=== PART 3: the accumulating centre set ===")
    for m in (6, 12):
        d0, ys = part3(m)
        print("  m=%2d  d0=%.5f  64 centres y_k=(d0/3)2^-k, y_63=%.3e, "
              "diameter %.3e <= d0" % (m, d0, ys[-1],
                                       max(abs(a - b) for a in ys for b in ys)))
    print()
    print("ALL CHECKS PASSED")
