#!/usr/bin/env python3
"""The rational Fourier matrix for the basis u = pi|x|^2, built here so that no script in this
directory depends on an external checker or on a scratch-directory path.

Convention (identical to Main's shell_check.fourier_map, verified in audit_fourier.py):
    f = e^{-pi|x|^2} sum_k a_k u^k   =>   fhat = e^{-pi|y|^2} sum_i b_i u'^i,   b = M a,
and M is rational: the monomial u^k = (t/2)^k expands in the Laguerre basis L_j^(1/2)(t), the
transform flips (-1)^j, and t = 2u re-expands.  M is upper triangular with M[i][i] = (-1)^i.

Why this module exists: five scripts previously loaded the matrix from a hardcoded scratch path.
That made the local-run commands non-portable.  They now import this file, which sits next to
them, so a sweep command works from a fresh checkout with nothing else present.
"""
import sympy as sp

def M_matrix(K):
    """Return M as a list of lists of sympy Rationals, M[i][k] for b_i = sum_k M[i][k] a_k."""
    t = sp.Symbol('t')
    u = sp.Symbol('u')

    def lag(j):
        return sp.expand(sp.assoc_laguerre(j, sp.Rational(1, 2), t))

    M = [[sp.Rational(0)] * (K + 1) for _ in range(K + 1)]
    for k in range(K + 1):
        poly = sp.expand((t / 2) ** k)
        a = [sp.Rational(0)] * (k + 1)
        for j in range(k, -1, -1):
            Lj = lag(j)
            cj = sp.Poly(Lj, t).coeff_monomial(t ** j)
            c = sp.Poly(poly, t).coeff_monomial(t ** j) / cj
            a[j] = sp.Rational(c)
            poly = sp.expand(poly - c * Lj)
        ex = sum(((-1) ** j) * a[j] * lag(j) for j in range(k + 1))
        ex = sp.expand(ex.subs(t, 2 * u))
        P = sp.Poly(ex, u)
        for i in range(K + 1):
            M[i][k] = sp.Rational(P.coeff_monomial(u ** i))
    return M

def self_test():
    """M must be upper triangular with diagonal (-1)^i, and M^2 = I (involution on even
    functions).  Both are structural facts a mistranscribed matrix fails."""
    ok = True
    for K in (3, 5, 7):
        M = M_matrix(K)
        tri = all(M[i][k] == 0 for i in range(K + 1) for k in range(K + 1) if k < i)
        diag = all(M[i][i] == sp.Integer(-1) ** i for i in range(K + 1))
        MM = [[sum(M[i][j] * M[j][k] for j in range(K + 1)) for k in range(K + 1)]
              for i in range(K + 1)]
        inv = all(MM[i][k] == (sp.Integer(1) if i == k else sp.Integer(0))
                  for i in range(K + 1) for k in range(K + 1))
        print("  K=%d upper triangular %s, diag (-1)^i %s, M^2 = I %s"
              % (K, tri, diag, inv))
        ok = ok and tri and diag and inv
    print("k15fourier self-test:", "PASS" if ok else "FAIL")
    return ok

if __name__ == "__main__":
    raise SystemExit(0 if self_test() else 1)
