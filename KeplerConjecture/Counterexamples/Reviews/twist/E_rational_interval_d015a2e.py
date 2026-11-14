#!/usr/bin/env python3
"""
Exact rational interval arithmetic, and certified enclosures of the few transcendental
quantities this project needs.  No floating-point decision is ever made here.

Why a separate module.  The rule for this block (K15-REVIEW-0523-E) is that any artifact
called *exact* must decide signs by exact rational comparison.  A previous version of
`barlow_contact_cell.py` admitted vertices by `sp.N(expr,30) > 1e-25`, which is a floating
test dressed as exactness; Main's GEOMETRIC_LEMMA_0438.md 4 records the same objection.
Everything downstream imports from here instead.

The one non-rational input is `pi` and hence `sin`/`cos` at rational multiples of pi.  Those
are obtained as *enclosures* from mpmath's rigorous interval arithmetic and immediately
converted to `Fraction` endpoints; from then on every operation is exact.
"""
from fractions import Fraction
from math import isqrt

# ---------- exact rational intervals ----------

class Iv:
    """A closed interval [lo, hi] with Fraction endpoints.  Rigorous operations."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Fraction(lo)
        self.hi = self.lo if hi is None else Fraction(hi)
        if self.lo > self.hi:
            raise ValueError(f"empty interval [{float(self.lo)}, {float(self.hi)}]")

    def __repr__(self):
        return f"Iv({self.lo}, {self.hi})"

    # -- arithmetic -------------------------------------------------------
    def __add__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        return Iv(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return Iv(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        c = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(c), max(c))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, Iv) else Iv(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("interval divisor straddles 0")
        return self * Iv(1 / o.hi, 1 / o.lo)

    # -- exact predicates --------------------------------------------------
    def sign(self):
        """'-' if strictly negative, '+' if strictly positive, '0' if exactly [0,0], else '?'."""
        if self.hi < 0:
            return "-"
        if self.lo > 0:
            return "+"
        if self.lo == 0 and self.hi == 0:
            return "0"
        return "?"

    def strictly_negative(self):
        return self.hi < 0

    def strictly_positive(self):
        return self.lo > 0

    def contains_zero(self):
        return self.lo <= 0 <= self.hi

    def width(self):
        return self.hi - self.lo

    def mid(self):
        return (self.lo + self.hi) / 2

    def abs_upper(self):
        return max(abs(self.lo), abs(self.hi))


def sqrt_iv(x, bits=200):
    """Rigorous enclosure of sqrt([lo,hi]) for lo >= 0, via integer square roots."""
    x = x if isinstance(x, Iv) else Iv(x)
    if x.lo < 0:
        raise ValueError("sqrt of an interval with negative part")
    scale = 1 << bits

    def lo_sqrt(q):
        return Fraction(isqrt(int(q * scale * scale)), scale)

    def hi_sqrt(q):
        s = isqrt(int(q * scale * scale))
        # make sure the upper end is >= sqrt(q)
        while Fraction(s * s, scale * scale) < q:
            s += 1
        return Fraction(s, scale)

    return Iv(lo_sqrt(x.lo), hi_sqrt(x.hi))


# ---------- certified enclosures of pi, sin, cos: rational series only ----------
#
# No interval library and no floating point is used.  pi comes from Machin's formula
#     pi/4 = 4 arctan(1/5) - arctan(1/239),   arctan(1/m) = sum_k (-1)^k / ((2k+1) m^(2k+1)),
# an alternating series with decreasing terms, so the truncation error is bounded by the
# first omitted term.  sin/cos come from Taylor series with the standard remainder bound
#     |sin x - sum_{j<n} (-1)^j x^(2j+1)/(2j+1)!| <= |x|^(2n+1)/(2n+1)! ,
# evaluated on the *interval* argument, so the bound is carried through the arithmetic.

def _arctan_inv(m: int, terms: int):
    """[lo, hi] containing arctan(1/m) for integer m >= 2, from the alternating series."""
    total = Fraction(0)
    for k in range(terms):
        total += Fraction((-1) ** k, (2 * k + 1) * m ** (2 * k + 1))
    tail = Fraction(1, (2 * terms + 1) * m ** (2 * terms + 1))
    return Iv(total - tail, total + tail)


_PI_CACHE = {}


def pi_iv(terms: int = 50):
    """Rigorous rational enclosure of pi (Machin).

    The truncation error of arctan(1/5) after N terms is ~5^-(2N+1), so N must be pushed
    until that is below the target accuracy: N = 30 leaves only 1e-44, which is what a
    first version of this module reported as its width."""
    if terms in _PI_CACHE:
        return _PI_CACHE[terms]
    a = _arctan_inv(5, terms)                 # 5^-(2N+1) decays slowly: N = 50 -> 1e-70
    b = _arctan_inv(239, max(8, terms // 2))  # 239^-(2N+1) decays fast: N = 25 -> 1e-129
    lo = 4 * (4 * a.lo - b.hi)
    hi = 4 * (4 * a.hi - b.lo)
    _PI_CACHE[terms] = Iv(lo, hi)
    return _PI_CACHE[terms]


def _taylor_sin(x: Iv, terms: int = 30):
    """[lo,hi] containing sin(x) for |x| <= 4, by the term recurrence
    t_{j+1} = -t_j x^2 / ((2j+2)(2j+3)); the alternating remainder is bounded by |t_terms|."""
    t = x                      # t_0 = x
    s = t
    for j in range(terms):
        t = -t * x * x / ((2 * j + 2) * (2 * j + 3))
        s = s + t
    tail = t.abs_upper()
    return Iv(s.lo - tail, s.hi + tail)


def _taylor_cos(x: Iv, terms: int = 30):
    t = Iv(1)                  # t_0 = 1
    s = t
    for j in range(terms):
        t = -t * x * x / ((2 * j + 1) * (2 * j + 2))
        s = s + t
    tail = t.abs_upper()
    return Iv(s.lo - tail, s.hi + tail)


def sin_cos_iv_of_pi_multiple(num: Fraction, terms: int = 30, pi_terms: int = 50):
    """Certified (sin, cos) enclosure at the angle num * pi (num rational)."""
    P = pi_iv(pi_terms)
    x = P * num                          # interval argument
    # reduce modulo 2*pi into [-pi, pi]
    two_p = P * 2
    k = Fraction(round(float(x.mid() / two_p.mid())))
    x = x - two_p * k
    return _taylor_sin(x, terms), _taylor_cos(x, terms)


if __name__ == "__main__":
    # Consistency tests.  The enclosures are far narrower than a float (or than any decimal
    # one writes down), so the test is that the interval *midpoint* agrees with an independent
    # 45-digit reference to well within the interval's own accuracy budget.  The artifact
    # itself never uses these references: it decides everything with Fractions.
    import mpmath as mp
    mp.mp.dps = 60

    def mpf(fr):
        return mp.mpf(fr.numerator) / fr.denominator

    def agrees(iv, ref, tol):
        return abs(mpf(iv.mid()) - ref) < tol

    r5 = sqrt_iv(Iv(5))
    assert r5.lo ** 2 <= 5 <= r5.hi ** 2, "sqrt(5): the enclosure must contain the true value"
    assert agrees(r5, mp.sqrt(5), mp.mpf('1e-50'))
    print(f"sqrt(5):  width {float(r5.width()):.2e}, agrees with sqrt(5) to 1e-50")

    P = pi_iv(50)
    assert agrees(P, mp.pi, mp.mpf('1e-45'))
    print(f"pi:       width {float(P.width()):.2e}, agrees with pi to 1e-45")

    for frac, name in [(Fraction(1, 6), "pi/6"), (Fraction(1, 4), "pi/4"),
                       (Fraction(2, 5), "2pi/5"), (Fraction(7, 13), "7pi/13")]:
        s_, c_ = sin_cos_iv_of_pi_multiple(frac)
        ang = mp.mpf(frac.numerator) / frac.denominator * mp.pi
        assert agrees(s_, mp.sin(ang), mp.mpf('1e-40')), f"sin({name})"
        assert agrees(c_, mp.cos(ang), mp.mpf('1e-40')), f"cos({name})"
        print(f"sin/cos({name:7s}) width {float(s_.width()):.2e} / {float(c_.width()):.2e}, agree to 1e-40")

    # rigorous internal consistency: the enclosures must satisfy sin^2 + cos^2 = 1
    for frac in (Fraction(1, 6), Fraction(2, 5), Fraction(3, 7), Fraction(9, 23)):
        s_, c_ = sin_cos_iv_of_pi_multiple(frac)
        t = s_ * s_ + c_ * c_
        assert t.lo <= 1 <= t.hi, f"sin^2+cos^2 != 1 for {frac}"
    print("sin^2+cos^2 contains 1 for four angles (rigorous, no reference value used)")

    x = Iv(Fraction(1, 3), Fraction(1, 2))
    y = Iv(Fraction(2, 5), Fraction(3, 5))
    assert (x * y).lo <= Fraction(2, 15) and (x * y).hi >= Fraction(3, 10)
    print("rational_interval: all self-tests passed")
