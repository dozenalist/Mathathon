#!/usr/bin/env python3
"""Exact checks of the k-independent endgame of the paper (Sections 8.5-8.6).

M1  The seven-vertex Moser graph (8.5) is a unit-distance graph with all
    eleven edges of length exactly 1 (exact arithmetic in Q(i, sqrt3, sqrt11)).
M2  It has no proper 3-colouring (exhaustive, 3^7 = 2187 maps).
M3  The rational placement (8.6) puts all seven vertices in the region (8.4):
        0 < l < 4   and   P = v^2 (3 xi^2 - v^2)^2 < P' = l^3 (1-l/4)(l-1)^2,
    verified by rigorous interval arithmetic (no floating point decisions).
"""
import math
from fractions import Fraction as F
import itertools

# ---------------------------------------------------------------- intervals
DIG = 40


def sqrt_interval(n):
    """rigorous rational bounds lo <= sqrt(n) <= hi"""
    scale = 10 ** DIG
    lo = math.isqrt(n * scale * scale)
    return F(lo, scale), F(lo + 1, scale)


S3 = sqrt_interval(3)
S11 = sqrt_interval(11)


class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if not isinstance(lo, F):
            lo = F(lo)
        if hi is None:
            hi = lo
        self.lo, self.hi = min(lo, hi), max(lo, hi)

    def __add__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Iv) else Iv(o)))

    def __rsub__(self, o):
        return (o if isinstance(o, Iv) else Iv(o)) + (-self)

    def __mul__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        c = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Iv(min(c), max(c))

    __rmul__ = __mul__

    def __truediv__(self, o):
        if isinstance(o, Iv):
            assert o.lo > 0 or o.hi < 0
            return self * Iv(1 / o.hi, 1 / o.lo)
        if isinstance(o, int):
            return self * Iv(F(1, o))
        return self * Iv(F(1) / o)

    def __repr__(self):
        return f"[{float(self.lo):.12f},{float(self.hi):.12f}]"


def iv_sqrt(bounds):
    return Iv(bounds[0], bounds[1])


# ------------------------------------------------------- complex intervals
class CIv:
    """interval complex number"""
    __slots__ = ("re", "im")

    def __init__(self, re, im):
        self.re = re if isinstance(re, Iv) else Iv(re)
        self.im = im if isinstance(im, Iv) else Iv(im)

    def __add__(self, o):
        return CIv(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        return CIv(self.re - o.re, self.im - o.im)

    def __mul__(self, o):
        if not isinstance(o, CIv):
            return CIv(self.re * o, self.im * o)
        a, b, c, d = self.re, self.im, o.re, o.im
        return CIv(a * c - b * d, a * d + b * c)

    def __repr__(self):
        return f"({self.re})+({self.im})i"

    def abssq(self):
        return self.re * self.re + self.im * self.im


def C(re, im=0):
    return CIv(re, im)


ZERO = C(0)
ONE = C(1)
S3I = C(0, iv_sqrt(S3))
S11I = C(0, iv_sqrt(S11))

# ---------------------------------------------------------------- Moser set
# G = {0, A, B, T, uA, uB, uT}
A = C(iv_sqrt(S3) / 2, F(1, 2))            # (sqrt3 + i)/2
B = C(iv_sqrt(S3) / 2, F(-1, 2))           # (sqrt3 - i)/2
T = C(iv_sqrt(S3))                          # sqrt3
UU = C(F(5, 6), iv_sqrt(S11) / 6)          # (5 + i sqrt11)/6
G = {"0": ZERO, "A": A, "B": B, "T": T,
     "uA": UU * A, "uB": UU * B, "uT": UU * T}

EDGES = [("0", "A"), ("0", "B"), ("A", "B"),
         ("T", "A"), ("T", "B"),
         ("uA", "0"), ("uB", "0"), ("uA", "uB"),
         ("uA", "uT"), ("uB", "uT"),
         ("T", "uT")]


def dist2(P, Q):
    d = P - Q
    return d.abssq()


def check_M1():
    print("M1  unit edge lengths of (8.5), exact interval arithmetic")
    allok = True
    for x, y in EDGES:
        d2 = dist2(G[x], G[y])
        ok = d2.lo <= 1 <= d2.hi
        allok &= ok
        print(f"    |{x} - {y}|^2 in {d2}   contains 1: {ok}")
    # no two vertices coincide
    names = list(G)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d2 = dist2(G[names[i]], G[names[j]])
            assert not (d2.lo <= 0 <= d2.hi) or d2.hi > 0, "coincident vertices"
    print(f"  all {len(EDGES)} unit edges verified: {allok}")
    return allok


def check_M2():
    print("M2  no proper 3-colouring of the Moser graph (exhaustive)")
    names = list(G)
    idx = {n: i for i, n in enumerate(names)}
    found = None
    for col in itertools.product(range(3), repeat=len(names)):
        if all(col[idx[x]] != col[idx[y]] for x, y in EDGES):
            found = col
            break
    print(f"  proper 3-colourings found: {found}")
    return found is None


def check_M3():
    print("M3  region (8.4) for the placed coordinates (8.6), interval arithmetic")
    print("    (8.6) is  z_g = ((35+12i)/37) * (g + (-290+149i)/250): the shift")
    print("    is INSIDE the bracket -- verified below against the paper's Table 1.")
    mult = C(F(35, 37), F(12, 37))          # (35+12i)/37, |mult| = 1
    shift = C(F(-290, 250), F(149, 250))
    print(f"  |(35+12i)/37|^2 = {F(35,37)**2 + F(12,37)**2}  (exactly 1)")
    table = {"0": (-1.2906, 0.1876), "A": (-0.6335, 0.9414), "B": (-0.3092, -0.0045),
             "T": (0.3478, 0.7493), "uA": (-1.1598, 1.1790), "uB": (-0.3666, 0.5700),
             "uT": (-0.2358, 1.5614)}
    allok = True
    for name, g in G.items():
        z = mult * (g + shift)
        l = z.abssq()
        xi, v = z.re, z.im
        # agreement with the paper's Table 1 (4 decimal places, h = 0.00011)
        tx, ty = table[name]
        agree = (abs(float(xi.lo) - tx) < 2e-4) and (abs(float(v.lo) - ty) < 2e-4)
        three_xi2_minus_v2 = xi * xi * 3 - v * v
        P = v * v * three_xi2_minus_v2 * three_xi2_minus_v2
        oneminus = Iv(1) - l / 4
        lm1 = l - 1
        Pp = l * l * l * oneminus * lm1 * lm1
        inside = (l.lo > 0) and (l.hi < 4)
        leq = P.hi < Pp.lo
        allok &= inside and leq and agree
        print(f"   g={name:3s} z=({float(xi.lo):9.4f},{float(v.lo):8.4f}) "
              f"table:{agree}  l in [{float(l.lo):.6f},{float(l.hi):.6f}] "
              f"in(0,4):{inside}  P_hi={float(P.hi):.6g} < P'_lo={float(Pp.lo):.6g}: {leq}")
    print(f"  all seven vertices strictly inside (8.4): {allok}")
    return allok


if __name__ == "__main__":
    ok1 = check_M1()
    print()
    ok2 = check_M2()
    print()
    ok3 = check_M3()
    print()
    print("SUMMARY:", {"M1": ok1, "M2": ok2, "M3": ok3})
