"""Exact arithmetic in K = Q(sqrt3, sqrt11) and rigorous rational interval arithmetic.

An element of K is a tuple (a0,a1,a2,a3) of Fractions meaning
    a0 + a1*r3 + a2*r11 + a3*r3*r11,   r3=sqrt3, r11=sqrt11.
"""
from fractions import Fraction as F

# ---------- exact field K ----------
def K(a0=0, a1=0, a2=0, a3=0):
    return (F(a0), F(a1), F(a2), F(a3))

ZERO = K()
ONE = K(1)

def add(x, y): return tuple(a + b for a, b in zip(x, y))
def sub(x, y): return tuple(a - b for a, b in zip(x, y))
def neg(x):    return tuple(-a for a in x)

def mul(x, y):
    a0,a1,a2,a3 = x
    b0,b1,b2,b3 = y
    # (a0 + a1 r3 + a2 r11 + a3 r3r11)(b0 + b1 r3 + b2 r11 + b3 r3r11)
    # basis 1, r3, r11, r3r11 ;  r3^2=3, r11^2=11, (r3r11)^2=33, r3*r3r11=3 r11, r11*r3r11=11 r3
    c0 = a0*b0 + 3*a1*b1 + 11*a2*b2 + 33*a3*b3
    c1 = a0*b1 + a1*b0 + 11*a2*b3 + 11*a3*b2
    c2 = a0*b2 + a2*b0 + 3*a1*b3 + 3*a3*b1
    c3 = a0*b3 + a3*b0 + a1*b2 + a2*b1
    return (c0, c1, c2, c3)

def iszero(x): return all(c == 0 for c in x)
def eq(x, y):  return iszero(sub(x, y))
def kscale(q, x): return tuple(F(q)*c for c in x)
def kdiv(x, y):
    """exact division in K, via solving the 4x4 rational linear system x = y*z"""
    import itertools
    # y*z as Q-linear map in z; build matrix
    cols = []
    for i in range(4):
        e = [F(0)]*4; e[i] = F(1)
        cols.append(mul(y, tuple(e)))
    # Solve  sum_i z_i * cols[i] = x
    import fractions
    # Gaussian elimination on 4x5
    M = [[cols[i][r] for i in range(4)] + [x[r]] for r in range(4)]
    n = 4
    piv = 0
    for c in range(n):
        p = None
        for r in range(piv, n):
            if M[r][c] != 0:
                p = r; break
        if p is None:
            raise ZeroDivisionError("not invertible")
        M[piv], M[p] = M[p], M[piv]
        pv = M[piv][c]
        M[piv] = [v/pv for v in M[piv]]
        for r in range(n):
            if r != piv and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f*b for a, b in zip(M[r], M[piv])]
        piv += 1
    return tuple(M[i][n] for i in range(n))

def kshow(x, name="x"):
    a0,a1,a2,a3 = x
    return f"{name} = {a0} + {a1}*r3 + {a2}*r11 + {a3}*r3r11"

R3 = K(0,1)
R11 = K(0,0,1)

# ---------- rigorous rational interval arithmetic ----------
def iadd(x,y): return (x[0]+y[0], x[1]+y[1])
def isub(x,y): return (x[0]-y[1], x[1]-y[0])
def imul(x,y):
    a,b = x; c,d = y
    return (min(a*c,a*d,b*c,b*d), max(a*c,a*d,b*c,b*d))
def ipow(x,n):
    r = (F(1),F(1))
    for _ in range(n): r = imul(r,x)
    return r
def ipos(x): return x[0] > 0          # strictly positive
def ineg(x): return x[1] < 0
def izerosafe(x): return not (x[1] < 0 or x[0] > 0)   # contains 0

# rational enclosures of r3, r11 at given decimal precision (verified by squaring)
def encl(n):
    """return ((lo,hi),(lo,hi)) rational brackets for sqrt3 and sqrt11 with 10^-n accuracy,
    each verified by exact squaring of the rational endpoints."""
    from decimal import Decimal, getcontext
    getcontext().prec = n + 30
    s3 = Decimal(3).sqrt(); s11 = Decimal(11).sqrt()
    q = 10**n
    def br(s, val):
        lo = F(int(s*q)) / q
        hi = lo + F(1,q)
        assert lo*lo <= val, (lo,)
        assert val <= hi*hi
        assert lo > 0
        return (lo, hi)
    return br(s3, F(3)), br(s11, F(11))

def kint(x, brs):
    """rational interval enclosure of the K-element x given brackets brs=(I3,I11)."""
    I3, I11 = brs
    a0,a1,a2,a3 = x
    t = (F(a0),F(a0))
    t = iadd(t, imul((F(a1),F(a1)), I3))
    t = iadd(t, imul((F(a2),F(a2)), I11))
    t = iadd(t, imul((F(a3),F(a3)), imul(I3,I11)))
    return t
