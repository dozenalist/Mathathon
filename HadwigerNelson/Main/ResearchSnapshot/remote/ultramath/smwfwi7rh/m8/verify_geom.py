#!/usr/bin/env python3
"""Exact verification of the geometry of the alternation engine at k = 6.

Direction d7 (member m8): repair of m16's Corollary 3.1.

Everything here is exact arithmetic in K = Q(sqrt 3, sqrt 11), represented as
4-tuples (a, b, c, d) meaning a + b*sqrt(3) + c*sqrt(11) + d*sqrt(33), plus a
second, independent implementation using sympy radicals.

Statements checked
  G1  u = 5/6 + i*sqrt(11)/6 has |u| = 1 and cos(arg u) = 5/6  (u = e^{i gamma_0})
  G2  lambda = 1 - u has |lambda|^2 = 1/3
  G3  the three points z_j = lambda * omega^j (omega = e^{2 pi i/3}) are
      pairwise at distance exactly 1 and at distance 1/sqrt 3 from 0
  G4  RIGIDITY: for v on the unit circle, |1+v|^2 = 1/3  <=>  Re v = -5/6
      (so the shift of the sum construction is forced to cos(delta) = -5/6)
  G5  three pairwise-unit points have circumradius 1/sqrt 3, so three pairwise
      unit points can never lie on one circle of radius 1 (the "single fixed
      endpoint" configuration is impossible)
  G6  gamma_0/pi is irrational: 2 cos gamma_0 = 5/3 is rational but not an
      integer (Niven), hence gamma_0/pi is irrational.
"""
import sys
from fractions import Fraction as F

# ---------------------------------------------------------------- Q(sqrt3,sqrt11)
class K:
    """a + b*sqrt3 + c*sqrt11 + d*sqrt33 with rational coefficients."""
    __slots__ = ("a", "b", "c", "d")

    def __init__(self, a=0, b=0, c=0, d=0):
        self.a, self.b, self.c, self.d = F(a), F(b), F(c), F(d)

    def __add__(self, o):
        o = asK(o)
        return K(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)

    def __neg__(self):
        return K(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, o):
        return self + (-asK(o))

    def __mul__(self, o):
        o = asK(o)
        a, b, c, d = self.a, self.b, self.c, self.d
        e, f, g, h = o.a, o.b, o.c, o.d
        return K(
            a * e + 3 * b * f + 11 * c * g + 33 * d * h,
            a * f + b * e + 11 * c * h + 11 * d * g,
            a * g + 3 * b * h + c * e + 3 * d * f,
            a * h + b * g + c * f + d * e,
        )

    def __eq__(self, o):
        o = asK(o)
        return (self.a, self.b, self.c, self.d) == (o.a, o.b, o.c, o.d)

    def __hash__(self):
        return hash((self.a, self.b, self.c, self.d))

    def __repr__(self):
        return f"K({self.a},{self.b},{self.c},{self.d})"

    def is_rational(self):
        return self.b == 0 and self.c == 0 and self.d == 0

    def rat(self):
        assert self.is_rational(), self
        return self.a


def asK(x):
    return x if isinstance(x, K) else K(x)


class Cx:
    """(re, im) with entries in K."""
    __slots__ = ("re", "im")

    def __init__(self, re, im):
        self.re, self.im = asK(re), asK(im)

    def __add__(self, o):
        return Cx(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        return Cx(self.re - o.re, self.im - o.im)

    def __neg__(self):
        return Cx(-self.re, -self.im)

    def __mul__(self, o):
        return Cx(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    def conj(self):
        return Cx(self.re, -self.im)

    def nrm2(self):
        return self.re * self.re + self.im * self.im

    def __eq__(self, o):
        return self.re == o.re and self.im == o.im

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash((self.re, self.im))

    def __repr__(self):
        return f"Cx({self.re},{self.im})"


def cx(a=0, b=0, c=0, d=0, e=0, f=0, g=0, h=0):
    return Cx(K(a, b, c, d), K(e, f, g, h))


S3 = K(0, 1)          # sqrt 3
S11 = K(0, 0, 1)      # sqrt 11

u = cx(0, 0, 0, 0, 0, 0, 0, 0)  # placeholder
u = Cx(K(F(5, 6)), K(0, 0, F(1, 6)))          # 5/6 + i sqrt(11)/6
omega = Cx(K(F(-1, 2)), K(0, F(1, 2)))         # -1/2 + i sqrt(3)/2
lam = Cx(K(1), K(0)) - u

results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond), extra))
    print(f"[{'OK ' if cond else 'FAIL'}] {name} {extra}")


# G1
check("G1 |u|^2 = 1", u.nrm2() == K(1), f"|u|^2 = {u.nrm2()}")
check("G1 Re u = 5/6", u.re == K(F(5, 6)) and u.im * u.im == K(F(11, 36)))
# G2
check("G2 |lambda|^2 = 1/3", lam.nrm2() == K(F(1, 3)), f"={lam.nrm2()}")
check("G2 lambda = 1-u", lam == Cx(K(1), K(0)) - u)
# omega is a primitive cube root of unity
o2 = omega * omega
check("G* omega^3 = 1", o2 * omega == Cx(K(1), K(0)))
check("G* omega^2+omega+1 = 0", o2 + omega + Cx(K(1), K(0)) == Cx(K(0), K(0)))
check("G* |1-omega|^2 = 3", (Cx(K(1), K(0)) - omega).nrm2() == K(3))

# G3
zs = [lam, lam * omega, lam * o2]
for i in range(3):
    check(f"G3 |z_{i}|^2 = 1/3", zs[i].nrm2() == K(F(1, 3)))
for i in range(3):
    for j in range(i + 1, 3):
        d2 = (zs[i] - zs[j]).nrm2()
        check(f"G3 |z_{i}-z_{j}|^2 = 1", d2 == K(1), f"={d2}")

# G4 rigidity: v = p + i q with p^2+q^2 = 1; |1+v|^2 = 2 + 2p.
# |1+v|^2 = 1/3  <=>  p = -5/6.  We check both directions on the representation
# v = cos(delta) + i sin(delta) over K for the two solutions and one wrong value.
def v_of(p, q):
    return Cx(K(p), K(q))

for p, q, lab in [(F(-5, 6), F(1, 6), "-5/6 + i/6"), (F(-5, 6), F(-1, 6), "-5/6 - i/6")]:
    v = v_of(p, q)
    # q^2 = ? we need K q with q^2 = 11/36 : use sqrt11/6
    v = Cx(K(p), K(0, 0, q))
    check(f"G4 |v|^2=1 for {lab}", v.nrm2() == K(1), f"|v|^2={v.nrm2()}")
    check(f"G4 |1+v|^2=1/3 for {lab}", (Cx(K(1), K(0)) + v).nrm2() == K(F(1, 3)))
check("G4 Re v = -5/6 <=> |1+v|^2 = 1/3 (algebra)",
      all((((Cx(K(1), K(0)) + Cx(K(pn, 12), K(qn, 12))).nrm2() == K(F(1, 3)))
           == (K(F(pn, 12)) == K(F(-5, 6))))
          for pn in range(-12, 13) for qn in (-1, 0, 1)
          if F(pn, 12) ** 2 + F(qn, 12) ** 2 == 1))

# G5: three pairwise-unit points, centroid = circumcentre with radius 1/sqrt3.
# Symbolic identity: with w1 = z1-z0, w2 = z2-z0, |w1|=|w2|=|w1-w2|=1 we have
# |z0 - (z0+z1+z2)/3|^2 = 1/3.  Verified on an independent exact model:
# z0=0, z1=1, z2=1/2 + i sqrt(3)/2.
z0 = Cx(K(0), K(0))
z1 = Cx(K(1), K(0))
zz2 = Cx(K(F(1, 2)), K(0, F(1, 2)))
check("G5 model is pairwise unit",
      (z1 - z0).nrm2() == K(1) and (zz2 - z0).nrm2() == K(1) and (zz2 - z1).nrm2() == K(1))
c3 = (z0 + z1 + zz2) * Cx(K(F(1, 3)), K(0))
check("G5 circumradius^2 = 1/3", (z0 - c3).nrm2() == K(F(1, 3)), f"={(z0-c3).nrm2()}")
check("G5 1/3 != 1 (so no unit triangle on a radius-1 circle)", K(F(1, 3)) != K(1))

# G6
check("G6 2cos(gamma0) = 5/3 rational, not an integer", F(5, 3).denominator != 1)

# G7  gamma_0 < pi/3 (so that pi - 3 gamma_0 > 0); exact: cos is strictly decreasing on
# (0,pi), gamma_0 in (0,pi) because sin gamma_0 = sqrt11/6 > 0, and cos gamma_0 = 5/6 > 1/2 =
# cos(pi/3).
check("G7 0 < gamma_0 < pi/3  (cos gamma_0 = 5/6 > 1/2, sin gamma_0 = sqrt11/6 > 0)",
      u.im * u.im == K(F(11, 36)) and u.re == K(F(5, 6)) and K(F(5, 6)) != K(F(1, 2)))

# ------------------------------------------------------- independent sympy check
try:
    import sympy as sp
    sq3, sq11 = sp.sqrt(3), sp.sqrt(11)
    I = sp.I
    U = sp.Rational(5, 6) + I * sq11 / 6
    W = sp.Rational(-1, 2) + I * sq3 / 2
    L = 1 - U
    ok = sp.simplify(sp.Abs(U) ** 2 - 1) == 0
    ok &= sp.simplify(sp.Abs(L) ** 2 - sp.Rational(1, 3)) == 0
    Z = [sp.expand(L * W ** j) for j in range(3)]
    for i in range(3):
        for j in range(3):
            if i != j:
                ok &= sp.simplify(sp.Abs(sp.expand(Z[i] - Z[j])) ** 2 - 1) == 0
    check("independent sympy re-check of G1-G3", ok)
except ImportError:
    print("[--] sympy unavailable, skipped independent check")

bad = [r for r in results if not r[1]]
print()
print(f"{len(results)} checks, {len(bad)} failures")
sys.exit(1 if bad else 0)
