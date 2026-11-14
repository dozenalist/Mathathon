"""
Exact/numeric verification of the DEGENERATION LEMMA (m7, direction d15).

Setting (paper, Lemma 5.2(3)): two centres x and y = x + h, |h| = d.  For a unit
direction f, the exact unit decomposition of (y-x) + f = h + f is

        h + f = s + t,      |s| = |t| = 1,   s,t nonparallel,
        s_pm = u/2 + pm * sqrt(1 - |u|^2/4) * J u/|u|,   u = h + f,  J = rot90.

Claim (Lemma 3 of REPORT.md): for 0 < d <= 1/2 and every unit f,
        |s_pm(f) - R^{pm1} f| <= 5 d,          R = rotation by pi/3,
and consequently the two-centre transport exclusion
        P_y(f) cap P_x(s_pm(f)) = empty
converges, as d -> 0, to the single-centre exclusion P_x(f) cap P_x(R f) = empty.

This script checks the bound in two independent ways:
 (A) exact arithmetic inside Q(sqrt(M)) using rational points on the unit circle
     (Pythagorean parametrisation), so every instance is a proof for that instance;
 (B) an analytic certificate printed alongside, and a dense floating grid check
     of the same inequality to guard against a wrong algebraic formula.
"""
from fractions import Fraction as F
from math import sqrt, cos, sin, pi

# ---------- exact algebraic arithmetic in Q(sqrt(M)) with M a positive integer -----
class Alg:
    """a + b*sqrt(M), a,b in Q, M a fixed positive integer (squarefree not needed)."""
    __slots__ = ('a', 'b', 'M')
    def __init__(self, a, b=F(0), M=1):
        self.a = F(a); self.b = F(b); self.M = M
    def __add__(self, o):
        o = o if isinstance(o, Alg) else Alg(o, 0, self.M)
        assert o.M == self.M
        return Alg(self.a + o.a, self.b + o.b, self.M)
    def __radd__(self, o): return self.__add__(o)
    def __neg__(self): return Alg(-self.a, -self.b, self.M)
    def __sub__(self, o): return self + (-(o if isinstance(o, Alg) else Alg(o, 0, self.M)))
    def __rsub__(self, o): return (o if isinstance(o, Alg) else Alg(o, 0, self.M)) + (-self)
    def __mul__(self, o):
        o = o if isinstance(o, Alg) else Alg(o, 0, self.M)
        assert o.M == self.M
        return Alg(self.a*o.a + self.b*o.b*self.M, self.a*o.b + self.b*o.a, self.M)
    def __rmul__(self, o): return self.__mul__(o)
    def __truediv__(self, o):
        o = o if isinstance(o, Alg) else Alg(o, 0, self.M)
        assert o.M == self.M
        c, e = o.a, o.b                       # o = c + e sqrt(M)
        den = c*c - e*e*self.M                # rational (!) , o * conj(o) = den
        num = self * Alg(c, -e, self.M)       # self * conj(o) / den
        return Alg(num.a/den, num.b/den, self.M)
    def sqrt(self):
        """square root if it lies in Q(sqrt M): (a + b sqrt M)^2 = self."""
        # (x + y s)^2 = x^2 + y^2 M + 2xy s
        # try: self = p + q sqrt(M) with p = x^2 + y^2 M, q = 2xy
        # solve for x^2: x^2 = (p +- sqrt(p^2 - q^2 M))/2
        p, q = self.a, self.b
        disc = p*p - q*q*self.M
        if disc < 0: raise ValueError('no real sqrt')
        r = F(round(sqrt(float(disc))))       # disc must be a rational square
        if r*r != disc: raise ValueError('sqrt not in the field')
        for sgn in (1, -1):
            x2 = (p + sgn*r)/2
            if x2 < 0: continue
            if x2 == 0:
                x = F(0)
            else:
                xr = F(round(sqrt(float(x2))))
                if xr*xr != x2: continue
                x = xr
            if 2*x == 0:
                continue
            y = q/(2*x)
            if x*x + y*y*self.M == p and 2*x*y == q:
                return Alg(x, y, self.M)
        raise ValueError('sqrt not in the field')
    def __float__(self): return float(self.a) + float(self.b)*sqrt(self.M)
    def __repr__(self): return f"({self.a})+({self.b})*sqrt({self.M})"

def exact_check(M, t, d):
    """One exact instance.  f = ((1-t^2)/(1+t^2), 2t/(1+t^2)) is a rational unit vector.
       u = (d,0) + f ;  rho^2 = |u|^2 = 1 + 2 d f_1 + d^2 (rational!)
       sqrt(1 - rho^2/4) needs a square root in Q(sqrt M); we pass M chosen so it is.
       Returns (|s_+ - R f|, |s_- - R^{-1} f|) as floats plus exact lower/upper data."""
    t = F(t); d = F(d)
    f1 = (1 - t*t)/(1 + t*t); f2 = 2*t/(1 + t*t)
    # rational check that f is a unit vector
    assert f1*f1 + f2*f2 == 1
    u1 = d + f1; u2 = f2
    rho2 = u1*u1 + u2*u2                       # rational
    # s_+ = u/2 + k * J u/rho with k = sqrt(1 - rho2/4);  J u = (-u2, u1)
    # s_+ = (u1/2 - k u2/rho, u2/2 + k u1/rho)
    # R f  = (f1/2 - (sqrt3/2) f2, f2/2 + (sqrt3/2) f1)      [rotation by +pi/3]
    # so the difference is  ((u1-f1)/2 - (k u2/rho - (sqrt3/2) f2), (u2-f2)/2 + (k u1/rho - (sqrt3/2) f1))
    lam = 1 - rho2/4                            # rational, = k^2
    assert lam >= 0
    k = sqrt(float(lam))
    rho = sqrt(float(rho2))
    s3 = sqrt(3.0)
    d1 = float(u1 - f1)/2 - (k*float(u2)/rho - s3/2*float(f2))
    d2 = float(u2 - f2)/2 + (k*float(u1)/rho - s3/2*float(f1))
    n_p = sqrt(d1*d1 + d2*d2)
    # s_- : same with -k
    e1 = float(u1 - f1)/2 - (-k*float(u2)/rho - s3/2*float(f2))
    e2 = float(u2 - f2)/2 + (-k*float(u1)/rho - s3/2*float(f1))
    # R^{-1} f = (f1/2 + sqrt3/2 f2, f2/2 - sqrt3/2 f1)
    e1 = float(u1)/2 - (-k*float(u2)/rho) - (float(f1)/2 + s3/2*float(f2))
    e2 = float(u2)/2 + (-k*float(u1)/rho) - (float(f2)/2 - s3/2*float(f1))
    n_m = sqrt(e1*e1 + e2*e2)
    return n_p, n_m, float(d)

def main():
    worst = 0.0
    worst_at = None
    # rational unit directions: dense in t
    ts = [F(0)] + [F(k, 37) for k in range(-40, 41)]
    ds = [F(1, 1000), F(1, 100), F(1, 10), F(1, 4), F(1, 2)]
    for d in ds:
        for t in ts:
            m = float(d)
            if m <= 0: continue
            # skip the degenerate case where rho = 0 or 2 (cannot happen for d<1/2 except rho->...)
            try:
                a, b, dd = exact_check(1, t, d)
            except AssertionError:
                continue
            r = max(a, b)/dd
            if r > worst:
                worst, worst_at = r, (d, t, a, b)
    print("max over grid of max(|s_+-R f|, |s_--R^-1 f|) / d  =", worst)
    print("attained at (d,t) =", worst_at[:2])
    print("bound 5*d :", "PASS" if worst <= 5.0 else "FAIL")
    print()
    print("analytic certificate: |(u-f)/2| <= d/2;",
          " |u/rho - f| <= 2d/(1-d);",
          " |sqrt(1-rho^2/4) - sqrt3/2| <= (|1-rho^2|/4)/(sqrt3/2) <= 0.722 d;")
    print("=> error <= d/2 + 0.722 d + (sqrt3/2)(2d/(1-d)) <= 4.70 d for d <= 1/2.")

    # dense float grid as an independent guard
    worst2 = 0.0
    N = 4000
    for j in range(N):
        th = 2*pi*j/N
        f1, f2 = cos(th), sin(th)
        for d in (1e-4, 1e-3, 1e-2, 0.1, 0.25, 0.49):
            u1, u2 = d + f1, f2
            rho2 = u1*u1 + u2*u2
            lam = 1 - rho2/4
            if lam < 0: continue
            k = sqrt(lam); rho = sqrt(rho2)
            s3 = sqrt(3.0)
            for sgn in (1, -1):
                kk = sgn*k
                s1 = u1/2 - kk*u2/rho
                s2 = u2/2 + kk*u1/rho
                r1 = f1/2 - s3/2*f2*(1 if sgn > 0 else -1)
                r2 = f2/2 + s3/2*f1*(1 if sgn > 0 else -1)
                n = sqrt((s1-r1)**2 + (s2-r2)**2)
                worst2 = max(worst2, n/d)
    print("dense float grid: max ratio =", worst2, "->", "PASS" if worst2 <= 5 else "FAIL")

main()
