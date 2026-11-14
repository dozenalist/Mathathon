"""
Exact certificate for the LAST step of the paper (section 8.5-8.6):

  * the seven-vertex graph of (8.5) is a unit-distance graph whose eleven listed edges have length
    exactly 1 and which is not 3-colourable;
  * the placement (8.6) is a congruence (|c| = 1);
  * all seven placed vertices satisfy 0 < |z|^2 < 4 and P < P' in (8.4), with strict rational margins.

Everything is computed in the ring Z[1/N][sqrt3, sqrt11] (closed under multiplication, since
sqrt3*sqrt11 = sqrt33) and compared by exact rational interval arithmetic: sqrt3 and sqrt11 are
bounded by rational intervals whose endpoints are verified by squaring.  No floating point is used
for any decision.

Run:  python3 work/moser_certificate.py
"""
from fractions import Fraction as Fr

# ---------------------------------------------------------------- the ring Q(sqrt3, sqrt11, sqrt33)
# element = (a,b,c,d) meaning a + b*sqrt3 + c*sqrt11 + d*sqrt33, all coefficients in Q.
ONE = (Fr(1), Fr(0), Fr(0), Fr(0))
ZERO = (Fr(0), Fr(0), Fr(0), Fr(0))


def R(a=0, b=0, c=0, d=0):
    return (Fr(a), Fr(b), Fr(c), Fr(d))


def add(x, y):
    return tuple(p + q for p, q in zip(x, y))


def sub(x, y):
    return tuple(p - q for p, q in zip(x, y))


def neg(x):
    return tuple(-p for p in x)


def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a*e + 3*b*f + 11*c*g + 33*d*h,
            a*f + b*e + 11*c*h + 11*d*g,
            a*g + c*e + 3*b*h + 3*d*f,
            a*h + d*e + b*g + c*f)


def scale(x, q):
    return tuple(p*Fr(q) for p in x)


def sq(x):
    return mul(x, x)


# complex numbers over the ring: (re, im)
def Cadd(x, y):
    return (add(x[0], y[0]), add(x[1], y[1]))


def Csub(x, y):
    return (sub(x[0], y[0]), sub(x[1], y[1]))


def Cmul(x, y):
    return (sub(mul(x[0], y[0]), mul(x[1], y[1])), add(mul(x[0], y[1]), mul(x[1], y[0])))


def Cscale(x, q):
    return (scale(x[0], q), scale(x[1], q))


def conj(x):
    return (x[0], neg(x[1]))


def normsq(x):                       # |x|^2, an element of the ring
    return add(sq(x[0]), sq(x[1]))


# ---------------------------------------------------------------- rational interval arithmetic
# sqrt3 in [17320508075, 17320508077]/10^10  (1.7320508075^2 = 2.99999999... < 3 < 1.7320508077^2)
# sqrt11 in [33166247903, 33166247904]/10^10
S3 = (Fr(17320508075, 10**10), Fr(17320508077, 10**10))
S11 = (Fr(33166247903, 10**10), Fr(33166247904, 10**10))
S33 = (S3[0]*S11[0], S3[1]*S11[1])


def check_radical_bounds():
    ok = S3[0]**2 < 3 < S3[1]**2 and S11[0]**2 < 11 < S11[1]**2
    return ok


def iv_ring(x):
    """rigorous enclosure of a ring element as a rational interval [lo,hi]"""
    a, b, c, d = x
    terms = [(a, None), (b, S3), (c, S11), (d, S33)]
    lo = Fr(0); hi = Fr(0)
    for coef, bd in terms:
        if bd is None:
            lo += coef; hi += coef
        elif coef >= 0:
            lo += coef*bd[0]; hi += coef*bd[1]
        else:
            lo += coef*bd[1]; hi += coef*bd[0]
    return (lo, hi)


def iv_add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def iv_sub(x, y):
    return (x[0]-y[1], x[1]-y[0])


def iv_mul(x, y):
    cands = [x[0]*y[0], x[0]*y[1], x[1]*y[0], x[1]*y[1]]
    return (min(cands), max(cands))


def iv_pow(x, n):
    r = (Fr(1), Fr(1))
    for _ in range(n):
        r = iv_mul(r, x)
    return r


# ---------------------------------------------------------------- the Moser spindle of (8.5)
s3 = R(0, 1)
A = (scale(s3, Fr(1, 2)), R(Fr(1, 2)))                 # (sqrt3 + i)/2
B = (scale(s3, Fr(1, 2)), R(Fr(-1, 2)))                # (sqrt3 - i)/2
T = (s3, ZERO)                                          # sqrt3
u = (R(Fr(5, 6)), scale(R(0, 0, 1), Fr(1, 6)))          # (5 + i sqrt11)/6
G = {'0': (ZERO, ZERO), 'A': A, 'B': B, 'T': T,
     'uA': Cmul(u, A), 'uB': Cmul(u, B), 'uT': Cmul(u, T)}
edges = [('0', 'A'), ('0', 'B'), ('A', 'B'), ('T', 'A'), ('T', 'B'),
         ('0', 'uA'), ('0', 'uB'), ('uA', 'uB'), ('uT', 'uA'), ('uT', 'uB'), ('T', 'uT')]

print("radical interval bounds verified by squaring:", check_radical_bounds())
print()
print("== (8.5): the eleven edges have length exactly 1 ==")
allunit = True
for (x, y) in edges:
    d2 = normsq(Csub(G[x], G[y]))
    ok = (d2 == ONE)
    allunit &= ok
    print("   |%s-%s|^2 = %s   exact 1? %s" % (x, y, d2, ok))
dT0 = normsq(G['T'])
print("   |T-0|^2 = %s   (this pair is NOT an edge)" % (dT0,))
print("   all eleven edges exactly unit:", allunit)
print("   not 3-colourable: triangles (0,A,B) and (T,A,B) force colour(0) = colour(T);")
print("   triangles (0,uA,uB) and (uT,uA,uB) force colour(0) = colour(uT); but |T-uT| = 1.")
print("   exact: |T-uT|^2 =", normsq(Csub(G['T'], G['uT'])), "  = 3|1-u|^2 = 3*(12/36)")

# ---------------------------------------------------------------- the placement (8.6)
print()
print("== (8.6): z_g = c*(g + t),  c = (35+12i)/37,  t = (-290+149i)/250 ==")
c = (R(Fr(35, 37)), R(Fr(12, 37)))
t = (R(Fr(-290, 250)), R(Fr(149, 250)))
print("   |c|^2 =", normsq(c), " (= 1, so the placement is a congruence)")
Z = {k: Cmul(c, Cadd(G[k], t)) for k in G}

print()
print("== certificate (8.4): 0 < |z|^2 < 4  and  P < P' , strictly, in rational interval arithmetic ==")
allok = True
for k in ['0', 'A', 'B', 'T', 'uA', 'uB', 'uT']:
    xi, up = Z[k][0], Z[k][1]
    l = add(sq(xi), sq(up))
    P = mul(sq(up), sq(sub(scale(sq(xi), 3), sq(up))))
    Pm = mul(mul(mul(sq(l), l), sub(ONE, scale(l, Fr(1, 4)))), sq(sub(l, ONE)))
    li, Pi, Pmi = iv_ring(l), iv_ring(P), iv_ring(Pm)
    ok = (0 < li[0]) and (li[1] < 4) and (Pi[1] < Pmi[0])
    allok &= ok
    print("   %-3s |z|^2 in [%.12f, %.12f]   P in [%.12f, %.12f]   P' in [%.12f, %.12f]  -> %s"
          % (k, float(li[0]), float(li[1]), float(Pi[0]), float(Pi[1]),
             float(Pmi[0]), float(Pmi[1]), "OK" if ok else "FAIL"))
print()
print("ALL SEVEN VERTICES STRICTLY INSIDE THE REGION (8.4):", allok)

# ---------------------------------------------------------------- the paper's own Table 1
print()
print("== the paper's Table 1: coordinate centres and the strict bounds P < P+ < P-' < P' ==")
table1 = {'0': ('-1.2906', '0.1876', '0.90', '1.35'),
          'A': ('-0.6335', '0.9414', '0.095', '0.110'),
          'B': ('-0.3092', '-0.0045', '0.000002', '0.00065'),
          'T': ('0.3478', '0.7493', '0.023', '0.026'),
          'uA': ('-1.1598', '1.1790', '9.8', '19.0'),
          'uB': ('-0.3666', '0.5700', '0.0022', '0.024'),
          'uT': ('-0.2358', '1.5614', '12.65', '12.9')}
h = Fr(11, 100000)                       # 0.00011
ok_tab = True
for k, (x0, y0, Pp, Pm) in table1.items():
    d = Csub(Z[k], (R(Fr(x0)), R(Fr(y0))))
    dn = iv_ring(normsq(d))
    pp, pmp = iv_ring(mul(sq(Z[k][1]), sq(sub(scale(sq(Z[k][0]), 3), sq(Z[k][1]))))), None
    xi, up = Z[k][0], Z[k][1]
    l = add(sq(xi), sq(up))
    P = mul(sq(up), sq(sub(scale(sq(xi), 3), sq(up))))
    Pmv = mul(mul(mul(sq(l), l), sub(ONE, scale(l, Fr(1, 4)))), sq(sub(l, ONE)))
    Pi, Pmi = iv_ring(P), iv_ring(Pmv)
    close = dn[1] < h*h
    bounds = Pi[1] < Fr(Pp) and Fr(Pm) < Pmi[0]
    ok_tab &= close and bounds
    print("   %-3s |z_g-(xi0+i ups0)| <= %.8f  (< 0.00011: %s)   P < %s (:%s)   %s < P' (:%s)"
          % (k, float(dn[1])**0.5, close, Pp, Pi[1] < Fr(Pp), Pm, Fr(Pm) < Pmi[0]))
print("TABLE 1 FULLY CONFIRMED:", ok_tab)
