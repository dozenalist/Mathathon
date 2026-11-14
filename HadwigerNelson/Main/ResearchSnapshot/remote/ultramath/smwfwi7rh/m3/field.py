"""Exact arithmetic in Q(sqrt 3): elements a + b*sqrt(3), a,b in Q.

Every coordinate below (lattice points, hexagon vertices, p_0, square corners)
lies in Q(sqrt 3), so all comparisons are exact.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ('a', 'b')

    def __init__(self, a, b=0):
        self.a = a if isinstance(a, F) else F(a)
        self.b = b if isinstance(b, F) else F(b)

    # --- arithmetic -------------------------------------------------------
    def __add__(self, o):
        o = to3(o)
        return Q3(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-to3(o))

    def __rsub__(self, o):
        return to3(o) - self

    def __mul__(self, o):
        o = to3(o)
        # (a+b r)(c+d r) = ac+3bd + (ad+bc) r,  r=sqrt3
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = to3(o)
        # 1/(c+d r) = (c-d r)/(c^2-3d^2)
        den = o.a * o.a - 3 * o.b * o.b
        if den == 0:
            raise ZeroDivisionError
        return Q3((self.a * o.a - 3 * self.b * o.b) / den,
                  (self.b * o.a - self.a * o.b) / den)

    # --- order ------------------------------------------------------------
    def sign(self):
        """sign of a + b*sqrt3, exactly."""
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare a^2 with 3 b^2
        if a > 0:                      # a>0>b ; a+b r > 0  <=>  a^2 > 3b^2
            return 1 if a * a > 3 * b * b else (-1 if a * a < 3 * b * b else 0)
        # a<0<b ; a+b r > 0 <=> 3b^2 > a^2
        return 1 if 3 * b * b > a * a else (-1 if 3 * b * b < a * a else 0)

    def __eq__(self, o):
        o = to3(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __lt__(self, o):
        return (self - to3(o)).sign() < 0

    def __le__(self, o):
        return (self - to3(o)).sign() <= 0

    def __gt__(self, o):
        return (self - to3(o)).sign() > 0

    def __ge__(self, o):
        return (self - to3(o)).sign() >= 0

    def float(self):
        return float(self.a) + float(self.b) * 3 ** 0.5

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        return f"({self.a}+{self.b}*sqrt3)"


def to3(x):
    return x if isinstance(x, Q3) else Q3(x)


ZERO = Q3(0)
ONE = Q3(1)
HALF = Q3(F(1, 2))
S3 = Q3(0, 1)          # sqrt 3
