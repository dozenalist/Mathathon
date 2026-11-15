"""Independent algebra and numerical sanity checks for the unified framework.

These check the new identifications, not the manuscript's complete certificates.
Only Python's standard library is required.
"""
from fractions import Fraction as F
from math import comb, factorial, pi, exp, expm1, fsum
import json
from pathlib import Path


def bernoulli(n):
    out = [F(1)]
    for m in range(1, n + 1):
        out.append(-sum(F(comb(m + 1, k)) * out[k] for k in range(m)) / (m + 1))
    return out


B = bernoulli(35)


def tau_monomial(d):
    return F(comb(d, 3), 4) * B[d - 3] if d >= 3 else F(0)


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_eval(a, x):
    out = F(0)
    for c in reversed(a):
        out = out * x + c
    return out


def square_product(lo, hi):
    out = [F(1)]
    for j in range(lo, hi + 1):
        out = poly_mul(out, [F(j * j), F(1)])
    return out


def remainder(a, monic):
    out = a[:]
    while len(out) >= len(monic):
        c = out[-1]
        shift = len(out) - len(monic)
        for k, v in enumerate(monic):
            out[k + shift] -= c * v
        out.pop()
    return out


def determinant(a):
    a = [row[:] for row in a]
    n = len(a)
    result = F(1)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            result = -result
        value = a[k][k]
        result *= value
        for i in range(k + 1, n):
            ratio = a[i][k] / value
            for j in range(k + 1, n):
                a[i][j] -= ratio * a[k][j]
    return result


def adaptive_simpson(f, a, b, tol=1e-11, depth=24):
    fa, fb, fm = f(a), f(b), f((a + b) / 2)
    whole = (b - a) * (fa + 4 * fm + fb) / 6

    def recurse(a, b, fa, fb, fm, whole, tol, depth):
        m = (a + b) / 2
        fl, fr = f((a + m) / 2), f((m + b) / 2)
        left = (m - a) * (fa + 4 * fl + fm) / 6
        right = (b - m) * (fm + 4 * fr + fb) / 6
        err = left + right - whole
        if depth == 0 or abs(err) <= 15 * tol:
            return left + right + err / 15
        return recurse(a, m, fa, fm, fl, left, tol / 2, depth - 1) + recurse(
            m, b, fm, fb, fr, right, tol / 2, depth - 1
        )

    return recurse(a, b, fa, fb, fm, whole, tol, depth)


def weight(y):
    if y == 0:
        return 1 / pi
    q = exp(-2 * pi * y)
    return (2 * pi) ** 4 * y**5 / 12 * q * (1 + 11*q + 11*q*q + q**3) / (-expm1(-2*pi*y))**5


def hzeta5(a):
    n = 3000
    z = a + n
    return fsum((a + k)**-5 for k in range(n)) + z**-4/4 + z**-5/2 + F(5,12)*z**-6


results = {}
for d in range(25):
    translated_difference = sum(F(comb(d, k)) * tau_monomial(k) for k in range(d))
    assert translated_difference == (F(1) if d == 4 else F(0))
    reflected = (-1)**d * sum(F(comb(d, k)) * tau_monomial(k) for k in range(d + 1))
    assert reflected == -tau_monomial(d)
    for prime in [2, 3, 7]:
        distributed = sum(
            F(comb(d, k) * a**(d-k) * prime**k) * tau_monomial(k)
            for a in range(prime) for k in range(d + 1)
        ) / prime**4
        assert distributed == tau_monomial(d)
results['polynomial_axioms'] = 'exact for degrees 0..24 and p=2,3,7'

for e in range(12):
    mu = (-1)**e * B[2*e+2] * F((2*e+3)*(2*e+4)*(2*e+5), 24)
    assert mu == (-1)**e * tau_monomial(2*e+5)
results['weighted_pullback_moments'] = 'exact for degrees 0..11'

pairing_checks = []
for K, N in [(4, 1), (5, 2), (8, 3)]:
    h = K - N
    T = square_product(N + 1, K)
    DN = square_product(1, N)
    W = [F(1)]
    for _ in range(5):
        W = poly_mul(W, DN)
    H = [F(0), F(0)] + W
    nodes = [-j*j for j in range(N + 1, K + 1)]
    dT = [k*T[k] for k in range(1, len(T))]
    residues = [poly_eval(H, s)/poly_eval(dT, s) for s in nodes]
    M = []
    for i in range(h):
        row = []
        for j in range(h):
            rem = remainder([F(0)]*(i+j) + H, T)
            top = rem[h-1] if len(rem) == h else F(0)
            assert top == sum(c*s**(i+j) for c,s in zip(residues,nodes))
            row.append(top)
        M.append(row)
    expected = F((-1)**(h*(h-1)//2))
    for s in nodes:
        expected *= poly_eval(H, s)
    assert determinant(M) == expected
    assert [1 if c > 0 else -1 for c in residues] == [(-1)**(j-1) for j in range(N+1,K+1)]
    pairing_checks.append({'K':K,'N':N,'h':h,'determinant':str(expected)})
results['residue_pairing_resultant'] = pairing_checks

alpha, lam = F(3,40), F(37,40)
def b1(x): return x-F(1,2)
def b2(x): return x*x-x+F(1,6)
def b3(x): return x*x*x-F(3,2)*x*x+F(1,2)*x
for x in [F(71,13), F(291,7), F(1234,19), F(1001,17)]:
    f = x - x.numerator//x.denominator
    ax = alpha*x
    g = ax - ax.numerator//ax.denominator
    Fx = 4*lam+2*lam*f-12*lam*g
    Px = 74*g*(1-g)-lam*f*(1-f)
    Cx = F(74)/alpha*g*(1-g)*(2*g-1)/6-lam*f*(1-f)*(2*f-1)/6
    assert Fx+lam == 2*lam*b1(f)-12*lam*b1(g)
    assert Px-F(2923,240) == lam*b2(f)-74*b2(g)
    assert Cx == lam*b3(f)/3-F(74)/(3*alpha)*b3(g)
results['periodic_bernoulli_tail'] = 'exact at four rational nonbreakpoints; coefficient identities verified'

transforms = []
for a in [0.4, 1.0, 2.3]:
    integral = adaptive_simpson(lambda y: weight(y)/(y*y+a*a),0,16)
    expression = a**4*hzeta5(a)-1/(2*a)-1/4
    error = abs(integral-expression)
    assert error < 2e-10, (a, error)
    transforms.append({'a':a,'integral':integral,'hurwitz_expression':expression,'absolute_error':error})
results['stieltjes_transform_numerical'] = transforms

rows=[]
for y in [0.2,0.6,1.2]:
    # Symmetric row sum; pairing opposite n improves numerical cancellation.
    z=1j*y
    series=z**-5+sum((z+n)**-5+(z-n)**-5 for n in range(1,5000))
    from_row=1j*y**5*series/pi
    err=abs(from_row-weight(y))
    assert err < 2e-12, (y,err)
    rows.append({'y':y,'absolute_error':err})
results['cotangent_row_kernel_numerical'] = rows

path = Path('framework_checks.json')
path.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))
