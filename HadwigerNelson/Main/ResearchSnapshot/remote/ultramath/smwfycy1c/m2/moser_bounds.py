"""Exact verification of the hypothesis list of
OAI.EuclideanFiveColor.region_of_rational_bounds at the 7 raw Moser-spindle
vertices, plus a cross-check of the repo's own seven_point_certificate numbers.

All arithmetic is exact: rationals (fractions.Fraction) and the biquadratic
field Q(sqrt3, sqrt11) = {p + q*sqrt3 + r*sqrt11 + s*sqrt33}.  No floats
(floats appear only in printed diagnostics).
"""
from fractions import Fraction as F

# ---------------------------------------------------------------- field Q(s3,s11)
class B:
    """p + q*s3 + r*s11 + s*s33 over Q."""
    __slots__ = ("c",)
    def __init__(self, p=0, q=0, r=0, s=0):
        self.c = (F(p), F(q), F(r), F(s))
    def __add__(self, o):
        o = asB(o); return B(*[a + b for a, b in zip(self.c, o.c)])
    __radd__ = __add__
    def __neg__(self): return B(*[-a for a in self.c])
    def __sub__(self, o): return self + (-asB(o))
    def __rsub__(self, o): return asB(o) - self
    def __mul__(self, o):
        o = asB(o)
        p, q, r, s = self.c; P, Q, R, S = o.c
        one = p*P + 3*q*Q + 11*r*R + 33*s*S
        a   = p*Q + q*P + 11*r*S + 11*s*R
        b   = p*R + r*P + 3*q*S + 3*s*Q
        ab  = p*S + s*P + q*R + r*Q
        return B(one, a, b, ab)
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = asB(o)
        assert o.c[1:] == (0, 0, 0), "only rational division supported"
        return B(*[x / o.c[0] for x in self.c])
    def israt(self): return self.c[1:] == (0, 0, 0)
    def __eq__(self, o): return self.c == asB(o).c
    def __hash__(self): return hash(self.c)
    def __lt__(self, o):
        d = self - asB(o)
        lo, hi = iv_wide(d)
        if hi < 0: return True
        if lo > 0: return False
        return _sign_exact(d.c) < 0
    # exact ordering (Fraction <= B dispatches to __ge__)
    def __ge__(self, o):
        lo, hi = iv_wide(self - asB(o))
        if lo >= 0: return True
        if hi < 0: return False
        return _sign_exact((self - asB(o)).c) > 0
    def __le__(self, o):
        lo, hi = iv_wide(self - asB(o))
        if hi <= 0: return True
        if lo > 0: return False
        return _sign_exact((self - asB(o)).c) < 0
    def __gt__(self, o): return not (self <= o)
    def __repr__(self):
        nm = ["", "s3", "s11", "s33"]
        t = [f"{c}*{n}" if n else str(c) for c, n in zip(self.c, nm) if c != 0]
        return " + ".join(t) if t else "0"

def asB(x): return x if isinstance(x, B) else B(x)

S3, S11 = B(0, 1), B(0, 0, 1)

def cmul(z, w):
    (x, y), (X, Y) = z, w
    return (x*X - y*Y, x*Y + y*X)

# --- certified rational enclosure of a field element, width 1e-55 ---
# L3 < sqrt 3 < U3 and L11 < sqrt 11 < U11, built from integer square roots
# (isqrt(3*10**110) = floor(sqrt(3)*10**55), hence exact, no floating point).
from math import isqrt
BIG = 10**55
_n3, _n11 = isqrt(3 * 10**110), isqrt(11 * 10**110)
L3, U3 = F(_n3, BIG), F(_n3 + 1, BIG)
L11, U11 = F(_n11, BIG), F(_n11 + 1, BIG)
assert 3 * 10**110 < (_n3 + 1) ** 2 and _n3**2 <= 3 * 10**110
assert 11 * 10**110 < (_n11 + 1) ** 2 and _n11**2 <= 11 * 10**110
def iv_wide(v):
    p, q, r, s = v.c
    lo = hi = p
    for c, l, h in ((q, L3, U3), (r, L11, U11)):
        if c >= 0: lo += c*l; hi += c*h
        else:      lo += c*h; hi += c*l
    l33, h33 = L3*L11, U3*U11
    if s >= 0: lo += s*l33; hi += s*h33
    else:      lo += s*h33; hi += s*l33
    assert lo <= hi
    return lo, hi

def _sign_exact(c):
    """Sign of p+q*s3+r*s11+s*s33, decided by a certified rational enclosure
    (width ~1e-40); the zero case is decided by the coefficients themselves."""
    if all(x == 0 for x in c):
        return 0
    lo, hi = iv_wide(B(*c))
    assert lo > 0 or hi < 0, f"enclosure too coarse to decide sign of {c}"
    return 1 if lo > 0 else -1

def absB(v): return v if not (v < B(0)) else -v

# ---------------------------------------------------------------- vertices
A  = (S3 / 2, B(F(1, 2)))
Bb = (S3 / 2, -B(F(1, 2)))
T  = (S3, B(0))
u  = (B(F(5, 6)), S11 / 6)
names = ["0", "A", "B", "T", "uA", "uB", "uT"]
verts = [(B(0), B(0)), A, Bb, T, cmul(u, A), cmul(u, Bb), cmul(u, T)]

print("=== 1. exact values at the seven raw vertices (field Q(sqrt3,sqrt11)) ===")
rows = []
for nm, (x, y) in zip(names, verts):
    r2 = x*x + y*y
    y2 = y*y
    t = 3*x*x - y*y
    rows.append((nm, x, y, r2, y2, t))
    print(f"{nm:3s} x = {x!r}")
    print(f"    y = {y!r}")
    print(f"    r2 = {r2!r}   y2 = {y2!r}   3x2-y2 = {t!r}")
    print(f"    r2 is rational? {r2.israt()}   r2 == 0 ? {r2 == B(0)}   r2 == 1 ? {r2 == B(1)}")

print()
print("=== 2. same values through exact rational interval arithmetic only ===")
print("    sqrt3 in [1.73205,1.73206], sqrt11 in [3.31662,3.31663]  (the repo's radical_bounds)")
l3, u3 = F(173205, 100000), F(173206, 100000)
l11, u11 = F(331662, 100000), F(331663, 100000)
def iv_coarse(v, l3=l3, u3=u3, l11=l11, u11=u11):
    p, q, r, s = v.c
    lo = hi = p
    for c, l, h in ((q, l3, u3), (r, l11, u11)):
        if c >= 0: lo += c*l; hi += c*h
        else:      lo += c*h; hi += c*l
    l33, h33 = l3*l11, u3*u11
    if s >= 0: lo += s*l33; hi += s*h33
    else:      lo += s*h33; hi += s*l33
    return lo, hi
for nm, x, y, r2, y2, t in rows:
    ilo, ihi = iv_coarse(r2)
    jlo, jhi = iv_coarse(y2)
    klo, khi = iv_coarse(t)
    tag = ("straddles 1 (cannot decide |r2-1|>0)" if ilo < 1 < ihi else
           "contains 1 as endpoint" if (ilo == 1 or ihi == 1) else "away from 1")
    print(f"{nm:3s} r2 in [{float(ilo):.12f},{float(ihi):.12f}] {tag}")
    print(f"    y2 in [{float(jlo):.12f},{float(jhi):.12f}]   3x2-y2 in [{float(klo):.12f},{float(khi):.12f}]"
          f"   => H needs >= {max(abs(klo),abs(khi)):.9f}")

print()
print("=== 3. the lemma's hypothesis list, decided exactly ===")
cert = {"T":  (F(3), F(3), F(0),        F(9),    F(2)),
        "uT": (F(3), F(3), F(11, 12),    F(16, 3), F(2))}
def check(nm, x, y, a, b, Y, H, d):
    r2 = x*x + y*y; y2 = y*y; t = 3*x*x - y*y
    gm = absB(r2 - B(1))
    kl = {"0<a": 0 < a, "b<4": b < 4, "0<=Y": 0 <= Y, "0<=H": 0 <= H, "0<=d": 0 <= d,
          "a<=r2": a <= r2, "r2<=b": r2 <= b, "y2<=Y": y2 <= Y,
          "|3x2-y2|<=H": not (B(H) < absB(t)),
          "d<=|r2-1|": d <= gm,
          "Y*H^2<a^3(1-b/4)d^2": Y*H**2 < a**3*(1-b/4)*d**2}
    bad = [k for k, v in kl.items() if not v]
    print(f"  {nm:3s} (a,b,Y,H,d) = ({a},{b},{Y},{H},{d})")
    print(f"      exact r2={r2!r}  y2={y2!r}  3x2-y2={t!r}  |r2-1|={gm!r}")
    print(f"      Y*H^2 = {Y*H**2} < a^3(1-b/4)d^2 = {a**3*(1-b/4)*d**2} :"
          f" {Y*H**2 < a**3*(1-b/4)*d**2}   (slack {a**3*(1-b/4)*d**2 - Y*H**2})")
    print(f"      all hypotheses hold: {not bad}   failures: {bad}")
    return not bad

print("  -- the vertices that DO admit the list --")
allok = True
for nm in ("T", "uT"):
    x, y = verts[names.index(nm)]
    allok &= check(nm, x, y, *cert[nm])
print("  every vertex admits the list?", allok, "<- answer to the claim under test")

print()
print("  -- the vertices where the list is UNSATISFIABLE, with the exact reason --")
for nm, x, y, r2, y2, t in rows:
    if nm in cert: continue
    if r2 == B(0):
        print(f"  {nm:3s}: r2 = 0 exactly, so a <= r2 = 0 contradicts 0 < a.")
        print(f"       (ThreeLabelRegion is false here too: 0 < x^2+y^2 fails.)")
    elif r2 == B(1):
        print(f"  {nm:3s}: r2 = 1 exactly, so 0 <= d and d <= |r2-1| = 0 force d = 0;")
        print(f"       then Y*H^2 < a^3(1-b/4)*0 = 0 <= Y*H^2 is a contradiction.")
        print(f"       (ThreeLabelRegion is false here too: y2*(3x2-y2)^2 = {y2*(t*t)!r}"
              f" is not < r2^3(1-r2/4)(r2-1)^2 = 0.)")

print()
print("=== 4. cross-check of the repo's own placedMoser certificates (seven_point_certificate) ===")
rot   = (B(F(35, 37)), B(F(12, 37)))
shift = (B(F(-290, 250)), B(F(149, 250)))
certX = [F(-12906,10**4),F(-6335,10**4),F(-3092,10**4),F(3478,10**4),F(-11598,10**4),F(-3666,10**4),F(-2358,10**4)]
certY = [F(1876,10**4),F(9414,10**4),F(-45,10**4),F(7493,10**4),F(11790,10**4),F(5700,10**4),F(15614,10**4)]
certs = [(F(170,100),F(171,100),F(353,10**4),F(4963,1000),F(70,100)),
         (F(128,100),F(129,100),F(887,1000),F(319,1000),F(28,100)),
         (F(95,1000),F(96,1000),F(22,10**6),F(287,1000),F(904,1000)),
         (F(682,1000),F(683,1000),F(562,1000),F(199,1000),F(317,1000)),
         (F(273,100),F(274,100),F(1391,1000),F(2647,1000),F(173,100)),
         (F(459,1000),F(46,100),F(326,1000),F(79,1000),F(54,100)),
         (F(2493,1000),F(2495,1000),F(244,100),F(2273,1000),F(1493,1000))]
ok_all = True
for i in range(7):
    zx, zy = cmul(rot, (verts[i][0] + shift[0], verts[i][1] + shift[1]))
    xlo, xhi = iv_coarse(zx); ylo, yhi = iv_coarse(zy)
    box = max(abs(xlo - certX[i]), abs(xhi - certX[i]), abs(ylo - certY[i]), abs(yhi - certY[i]))
    a, b, Y, H, d = certs[i]
    r2 = zx*zx + zy*zy; y2 = zy*zy; t = 3*zx*zx - zy*zy
    gm = absB(r2 - B(1))
    keys = {"0<a": 0 < a, "b<4": b < 4, "0<=Y": 0 <= Y, "0<=H": 0 <= H, "0<=d": 0 <= d,
            "a<=r2": a <= r2, "r2<=b": r2 <= b, "y2<=Y": y2 <= Y,
            "|3x2-y2|<=H": not (B(H) < absB(t)), "d<=|r2-1|": d <= gm,
            "hnum": Y*H**2 < a**3*(1-b/4)*d**2}
    ok = box <= F(11,10**5) and all(keys.values())
    ok_all &= ok
    print(f"  placedMoser {i}: box residual <= 11/100000 : {box <= F(11,10**5)}"
          f"   full certificate: {ok}   failures: {[k for k, v in keys.items() if not v]}"
          f"   (Y*H^2={float(Y*H**2):.6f} < {float(a**3*(1-b/4)*d**2):.6f})"
          f"   exact r2={r2!r}")
    print(f"      exact y2={y2!r}  3x2-y2={t!r}  |r2-1|={gm!r}")
print("  ALL seven placedMoser certificates verify exactly:", ok_all)
