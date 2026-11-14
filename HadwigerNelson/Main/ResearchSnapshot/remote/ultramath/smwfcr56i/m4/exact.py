"""Exact arithmetic in K = Q(sqrt3, sqrt11), represented in the Q-basis (1, s3, s11, s33).

Purpose: every numeric claim in the Hadwiger-Nelson paper that is algebraic
lives in this field, so each can be decided exactly rather than by interval
arithmetic.  sign() is exact: no floating point is used in any decision.
"""
from fractions import Fraction as F
from math import isqrt

class X:
    """a + b*s3 + c*s11 + d*s33 with a,b,c,d in Q."""
    __slots__ = ("a", "b", "c", "d")
    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = F(a); self.b = F(b); self.c = F(c); self.d = F(d)
    # ---- arithmetic -------------------------------------------------
    def __add__(self, o):
        o = K(o)
        return X(self.a+o.a, self.b+o.b, self.c+o.c, self.d+o.d)
    __radd__ = __add__
    def __neg__(self):
        return X(-self.a, -self.b, -self.c, -self.d)
    def __sub__(self, o):
        return self + (-K(o))
    def __rsub__(self, o):
        return K(o) + (-self)
    def __mul__(self, o):
        o = K(o)
        # (a1+b1 s3+c1 s11+d1 s33)(a2+...) ; s3s3=3, s11s11=11, s33=s3 s11
        a1,b1,c1,d1 = self.a,self.b,self.c,self.d
        a2,b2,c2,d2 = o.a,o.b,o.c,o.d
        a = a1*a2 + 3*b1*b2 + 11*c1*c2 + 33*d1*d2
        b = a1*b2 + b1*a2 + 11*c1*d2 + 11*d1*c2
        c = a1*c2 + c1*a2 + 3*b1*d2 + 3*d1*b2
        d = a1*d2 + d1*a2 + b1*c2 + c1*b2
        return X(a,b,c,d)
    __rmul__ = __mul__
    def inv(self):
        s = sign(self)
        if s == 0:
            raise ZeroDivisionError
        # 1/x = conj-ish: use norm via multiplication by conjugates
        # conjugates: replace s3->-s3, s11->-s11, s33->s33 (two independent signs)
        x1 = X(self.a,-self.b,-self.c, self.d)   # s3,s11 both negated
        x2 = X(self.a,-self.b, self.c,-self.d)   # s3 negated only
        x3 = X(self.a, self.b,-self.c,-self.d)   # s11 negated only
        num = x1*x2*x3
        den = self*num
        assert den.b == 0 and den.c == 0 and den.d == 0, den
        return num * K(1/den.a)
    def __truediv__(self, o):
        return self * K(o).inv()
    def __rtruediv__(self, o):
        return K(o) * self.inv()
    def __eq__(self, o):
        o = K(o)
        return self.a == o.a and self.b == o.b and self.c == o.c and self.d == o.d
    def __hash__(self):
        return hash((self.a, self.b, self.c, self.d))
    def __repr__(self):
        return f"X({self.a},{self.b},{self.c},{self.d})"
    def approx(self, digits=25):
        from decimal import Decimal, getcontext
        getcontext().prec = digits
        s3 = Decimal(3).sqrt(); s11 = Decimal(11).sqrt()
        return (Decimal(self.a.numerator)/Decimal(self.a.denominator)
                + Decimal(self.b.numerator)/Decimal(self.b.denominator)*s3
                + Decimal(self.c.numerator)/Decimal(self.c.denominator)*s11
                + Decimal(self.d.numerator)/Decimal(self.d.denominator)*s3*s11)

def K(v):
    if isinstance(v, X):
        return v
    if isinstance(v, (int, F)):
        return X(v)
    raise TypeError(v)

s3 = X(0,1); s11 = X(0,0,1); s33 = X(0,0,0,1)
ZERO, ONE = X(0), X(1)

# ------------- exact sign ------------------------------------------------
def _sign_Q_sqrt3(p, q):
    """exact sign of p + q*sqrt3, p,q in Q."""
    if q == 0:
        return (p > 0) - (p < 0)
    if p == 0:
        return (q > 0) - (q < 0)
    if p > 0 and q > 0:
        return 1
    if p < 0 and q < 0:
        return -1
    # opposite signs: compare p^2 with 3 q^2
    lhs = p*p; rhs = 3*q*q
    if p > 0:                      # p>0, q<0 : sign(p+q s3) = sign if p^2 > 3q^2
        return 1 if lhs > rhs else (-1 if lhs < rhs else 0)
    else:                          # p<0, q>0
        return -1 if lhs > rhs else (1 if lhs < rhs else 0)

def sign(x):
    """exact sign of a + b s3 + c s11 + d s33."""
    # x = (a + b s3) + (c + d s3) s11
    p = _sign_Q_sqrt3(x.a, x.b)
    q = _sign_Q_sqrt3(x.c, x.d)
    if p == 0 and q == 0:
        return 0
    if p == 0:
        return q
    if q == 0:
        return p
    if p == q:
        return p
    # opposite signs: compare (a+b s3)^2 with 11 (c+d s3)^2
    left = X(x.a,x.b)*X(x.a,x.b)
    right = 11*(X(x.c,x.d)*X(x.c,x.d))
    diff = left - right
    assert diff.c == 0 and diff.d == 0, diff
    sd = _sign_Q_sqrt3(diff.a, diff.b)
    if p > 0:                      # p>0, q<0
        return 1 if sd > 0 else (-1 if sd < 0 else 0)
    else:
        return -1 if sd > 0 else (1 if sd < 0 else 0)

def is_pos(x): return sign(x) > 0
def is_neg(x): return sign(x) < 0
