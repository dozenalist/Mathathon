"""Exact verification of paper Lemma 8.9 (the seven-point Moser certificate, Sec. 8.5-8.6).

Everything is computed in K = Q(sqrt3, sqrt11) with exact Fraction coefficients; signs of
elements of K are decided with rigorous rational interval enclosures of sqrt3, sqrt11,
sqrt33.  No floating point is used in any decision.

(1) G = {0, A, B, T, uA, uB, uT}, A=(r3+i)/2, B=(r3-i)/2, T=r3, u=(5+i r11)/6 : all
    eleven graph edges have |.|^2 exactly 1.
(3) Placement (8.6):  z_g = ((35+12i)/37) * (g + (-290+149i)/250).  [pdftotext garbles
    the formula; the translation is INSIDE the rotation.]  For all seven g:
       0 < |z_g|^2 < 4   and   P := v^2 (3x^2-v^2)^2  <  P' := L^3 (1-L/4)(L-1)^2 ,
    with z_g = x + i v, L = x^2+v^2.  This is region (8.4), i.e. Lemma 8.9.
(4) The paper's Table 1 bounds P+ and P'- are consistent with the exact values.

Non-3-colourability of G (used in Theorem A of quantitative.md): {0,A,B} and {T,A,B} are
equilateral of side 1, so c(0)=c(T); {0,uA,uB} and {uT,uA,uB} are equilateral of side 1,
so c(0)=c(uT); but |T-uT|^2 = 3|1-u|^2 = 1, so c(T) != c(uT).  Contradiction.
"""
from fractions import Fraction as Fr
from decimal import Decimal, getcontext, ROUND_FLOOR

# ---------- exact arithmetic in K = Q(sqrt3, sqrt11) ----------
class K:
    __slots__ = ('a',)
    def __init__(s, a, b=0, c=0, d=0): s.a = (Fr(a), Fr(b), Fr(c), Fr(d))
    def __add__(s, o):
        o = o if isinstance(o, K) else K(o)
        return K(*[x+y for x, y in zip(s.a, o.a)])
    __radd__ = __add__
    def __neg__(s): return K(*[-x for x in s.a])
    def __sub__(s, o):
        o = o if isinstance(o, K) else K(o)
        return K(*[x-y for x, y in zip(s.a, o.a)])
    def __rsub__(s, o): return (-s)+o
    def __mul__(s, o):
        o = o if isinstance(o, K) else K(o)
        a, b, c, d = s.a; e, f, g, h = o.a
        return K(a*e+3*b*f+11*c*g+33*d*h, a*f+b*e+11*c*h+11*d*g,
                 a*g+c*e+3*b*h+3*d*f,     a*h+d*e+b*g+c*f)
    __rmul__ = __mul__
    def __repr__(s): return f"({s.a[0]}+{s.a[1]}r3+{s.a[2]}r11+{s.a[3]}r33)"

class Cx:                                   # complex numbers over K
    __slots__ = ('re', 'im')
    def __init__(s, re, im=0):
        s.re = re if isinstance(re, K) else K(re)
        s.im = im if isinstance(im, K) else K(im)
    def __add__(s, o): return Cx(s.re+o.re, s.im+o.im)
    def __sub__(s, o): return Cx(s.re-o.re, s.im-o.im)
    def __mul__(s, o): return Cx(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    def abs2(s): return s.re*s.re + s.im*s.im

def rat_sqrt_bounds(n, digits=45):
    getcontext().prec = digits
    lo = Decimal(n).sqrt().quantize(Decimal(1).scaleb(-(digits-5)), rounding=ROUND_FLOOR)
    return Fr(lo), Fr(lo + Decimal(1).scaleb(-(digits-5)))

B3, B11, B33 = rat_sqrt_bounds(3), rat_sqrt_bounds(11), rat_sqrt_bounds(33)

def enclosure(v):
    """rigorous rational interval [lo,hi] containing the K-element v"""
    a, b, c, d = v.a
    lo = hi = a
    for coef, (l, h) in ((b, B3), (c, B11), (d, B33)):
        if coef >= 0: lo += coef*l; hi += coef*h
        else:         lo += coef*h; hi += coef*l
    return lo, hi

def sgn(v):
    lo, hi = enclosure(v)
    return 1 if lo > 0 else (-1 if hi < 0 else 0)

# ---------- the graph (8.5) ----------
half = K(Fr(1, 2))
A = Cx(K(0, 1)*half, half)                  # (r3+i)/2
B = Cx(K(0, 1)*half, -half)                 # (r3-i)/2
T = Cx(K(0, 1), K(0))                       # r3
u = Cx(K(Fr(5, 6)), K(0, 0, Fr(1, 6)))      # (5+i r11)/6
G = {'0': Cx(K(0)), 'A': A, 'B': B, 'T': T, 'uA': u*A, 'uB': u*B, 'uT': u*T}
EDGES = [('0','A'),('0','B'),('A','B'),('T','A'),('T','B'),('uA','uB'),
         ('0','uA'),('0','uB'),('uT','uA'),('uT','uB'),('T','uT')]

print("(1) the eleven edges of the seven-vertex graph (8.5), |.|^2 exactly 1:")
ok1 = True
for p, q in EDGES:
    z = (G[p]-G[q]).abs2()
    good = z.a[0] == 1 and all(x == 0 for x in z.a[1:])
    ok1 = ok1 and good
    print(f"    |{p}-{q}|^2 = {z.a[0]}   exactly 1: {good}")
print("    all eleven exact:", ok1)
print("    |T-uT|^2 = 3|1-u|^2 =", 3*((u-Cx(K(1))).abs2()).a[0], " (the forced-equality killer)")

# ---------- the placement (8.6) ----------
mult = Cx(K(Fr(35, 37)), K(Fr(12, 37)))
off  = Cx(K(Fr(-290, 250)), K(Fr(149, 250)))
print("(3) region (8.4) at the seven points z_g = ((35+12i)/37)(g + (-290+149i)/250):")
ok3 = True
for k, g in G.items():
    z = mult*(g+off); x, v = z.re, z.im
    L  = x*x + v*v
    P  = v*v*(K(3)*x*x - v*v)*(K(3)*x*x - v*v)
    Pp = L*L*L*(K(1) - L*K(Fr(1, 4)))*(L - K(1))*(L - K(1))
    ok = sgn(L) == 1 and sgn(L - K(4)) == -1 and sgn(P - Pp) == -1
    ok3 = ok3 and ok
    loL, _ = enclosure(L); _, hiP = enclosure(P); loQ, _ = enclosure(Pp)
    print(f"    {k:3s} L={float(loL):.12f}    P<{float(hiP):.8f}  <  {float(loQ):.8f}<P'    OK={ok}")
print("    all seven certified:", ok3)

print("(4) consistency with the paper's Table 1 (bounds P+ and P'-):")
tab = {'0': (Fr(90,100), Fr(135,100)), 'A': (Fr(95,1000), Fr(110,1000)),
       'B': (Fr(2,10**6), Fr(65,10**5)), 'T': (Fr(23,1000), Fr(26,1000)),
       'uA': (Fr(98,10), Fr(19)), 'uB': (Fr(22,10**4), Fr(24,1000)),
       'uT': (Fr(1265,100), Fr(129,10))}
ok4 = True
for k, g in G.items():
    z = mult*(g+off); x, v = z.re, z.im
    L = x*x + v*v
    P = v*v*(K(3)*x*x - v*v)*(K(3)*x*x - v*v)
    Pp = L*L*L*(K(1) - L*K(Fr(1, 4)))*(L - K(1))*(L - K(1))
    _, phi = enclosure(P); qlo, _ = enclosure(Pp)
    good = phi < tab[k][0] and qlo > tab[k][1]
    ok4 = ok4 and good
    print(f"    {k:3s}  P <= {float(phi):.8g} < P+ = {float(tab[k][0]):g}"
          f"    P' >= {float(qlo):.8g} > P'- = {float(tab[k][1]):g}    {good}")

print("\nSUMMARY  (1) unit distances:", ok1, " (3) region (8.4):", ok3, " (4) Table 1:", ok4)
