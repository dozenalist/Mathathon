#!/usr/bin/env python3
"""Cross-check between Main's convention and Computation's exactcert convention.

Main (shell_check.py):   u = pi|x|^2,      f = P(u) e^{-pi|x|^2},  fhat = Q(u) e^{-pi|x|^2}
Computation (exactcert): t = 2 pi|x|^2,    f = p(t) e^{-t/2},      fhat = q(t) e^{-t/2}

Since u = t/2 and e^{-pi|x|^2} = e^{-t/2}, the two are related by
    p(t) = P(t/2),   q(t) = Q(t/2),
i.e. coefficient-wise p_k = P_k / 2^k.  Nothing else may differ: same sphere
radius, same minimum separation, same unnormalised Fourier transform
fhat(t) = integral f(x) e^{-2 pi i <x,t>} dx, same bound Delta <= (4 pi/3) p(0)/q(0).

This script takes a rational coefficient vector in MAIN's monomial basis, emits
the same object (a) as a Main-basis vector, (b) as a Computation-basis Laguerre
vector c ready for exactcert.certify, and (c) prints p(0), q(0) from both routes.
Agreement of p(0), q(0) and of the sign verdicts is the reconciliation test.

Usage:  python3 interface_xcheck.py [--degree 3]
"""
import json, sys
from fractions import Fraction as F
import sympy as sp

sys.path.insert(0, str(__file__).rsplit('/', 1)[0])
from shell_check import fourier_map, PI_LO, PI_HI

t = sp.Symbol('t')
u = sp.Symbol('u')


def lag(j):
    return sp.expand(sp.assoc_laguerre(j, sp.Rational(1, 2), t))


def main_to_comp(a):
    """a: rational coefficients in Main's basis e^{-pi r^2} u^k, u = pi r^2.
    Returns c with f = sum_k c_k L_k^{1/2}(t) e^{-t/2}  (Computation's basis)."""
    K = len(a) - 1
    P = sum(sp.Rational(a[k].numerator, a[k].denominator) * u ** k for k in range(K + 1))
    p_t = sp.expand(P.subs(u, t / 2))            # p(t) = P(t/2)
    # Laguerre expansion of p_t
    rem = sp.Poly(p_t, t)
    c = [sp.Rational(0)] * (K + 1)
    for j in range(K, -1, -1):
        Lj = sp.Poly(lag(j), t)
        cj = Lj.coeff_monomial(t ** j)
        cj_val = rem.coeff_monomial(t ** j) / cj
        c[j] = sp.Rational(cj_val)
        rem = sp.Poly(sp.expand(rem.as_expr() - cj_val * Lj.as_expr()), t)
    assert sp.expand(rem.as_expr()) == 0, "Laguerre expansion failed"
    return [F(int(x.p), int(x.q)) for x in c]


def comp_pq(c):
    """Computation's p, q from c: p = sum c_k L_k, q = sum (-1)^k c_k L_k (in t)."""
    K = len(c) - 1
    p = sum(sp.Rational(c[k].numerator, c[k].denominator) * lag(k) for k in range(K + 1))
    q = sum((-1) ** k * sp.Rational(c[k].numerator, c[k].denominator) * lag(k)
            for k in range(K + 1))
    return sp.expand(p), sp.expand(q)


def main_pq(a):
    K = len(a) - 1
    M = fourier_map(K)
    b = [sum(M[i, k] * sp.Rational(a[k].numerator, a[k].denominator)
             for k in range(K + 1)) for i in range(K + 1)]
    P = sum(sp.Rational(a[k].numerator, a[k].denominator) * u ** k for k in range(K + 1))
    Q = sum(sp.expand(b[i]) * u ** i for i in range(K + 1))
    return sp.expand(P), sp.expand(Q)


def main(degree=3):
    # a deliberately non-trivial rational vector; sign verdicts are not the point
    a = [F(7, 2), F(-3), F(1, 5), F(-1, 7)][:degree + 1]
    a = a + [F(0)] * (degree + 1 - len(a))
    print("Main-basis a =", [str(x) for x in a])
    P, Q = main_pq(a)
    c = main_to_comp(a)
    print("Computation-basis c =", [str(x) for x in c])
    p_t, q_t = comp_pq(c)
    print("  Main   P(0) = %s   Q(0) = %s" % (P.subs(u, 0), Q.subs(u, 0)))
    print("  Comp   p(0) = %s   q(0) = %s" % (p_t.subs(t, 0), q_t.subs(t, 0)))
    same_p = sp.simplify(sp.expand(p_t - P.subs(u, t / 2))) == 0
    same_q = sp.simplify(sp.expand(q_t - Q.subs(u, t / 2))) == 0
    print("  PASS  p(t) = P(t/2) identically" if same_p else "  FAIL  p mismatch")
    print("  PASS  q(t) = Q(t/2) identically" if same_q else "  FAIL  q mismatch")
    rec = {"object": "interface cross-check Main <-> Computation",
           "main_basis": "e^{-pi r^2} u^k, u = pi r^2",
           "comp_basis": "L_k^{1/2}(t) e^{-t/2}, t = 2 pi r^2",
           "main_a": [str(x) for x in a],
           "comp_c": [str(x) for x in c],
           "p0_main": str(P.subs(u, 0)), "q0_main": str(Q.subs(u, 0)),
           "p0_comp": str(p_t.subs(t, 0)), "q0_comp": str(q_t.subs(t, 0)),
           "identity_p": bool(same_p), "identity_q": bool(same_q)}
    with open("KeplerConjecture/Computation/out/interface_xcheck.json", "w") as fh:
        json.dump(rec, fh, indent=2)
    return 0 if (same_p and same_q) else 1


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[2]) if len(sys.argv) > 2 else 3))
