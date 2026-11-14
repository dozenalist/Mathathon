#!/usr/bin/env python3
"""Independent audit of Main's Fourier matrix (shell_check.fourier_map) and of mine.

THE OBJECT UNDER AUDIT.  In the basis u = pi|x|^2, with f = e^{-pi|x|^2} sum_k a_k u^k,
Main asserts fhat = e^{-pi|y|^2} sum_i b_i u'^i with u' = pi|y|^2 and b = M a, M rational.

THREE INDEPENDENT CHECKS, in increasing order of independence:

  A1  my own exact construction of M (rational polynomials via L_j^(1/2), a different code
      path from shell_check's sympy expansion) agrees entry by entry.
  A2  the eigen-relation: phi_j = L_j^(1/2)(2 pi |x|^2) e^{-pi|x|^2} must satisfy
      phihat_j = (-1)^j phi_j.  Checked here through the matrix: if f = sum_k a_k u^k then
      b = M a, and the map must be an involution composed with sign flip on the monomial
      degree.  Concretely M must satisfy the identity implied by M^2 = (degree-reversing sign).
  A3  DIRECT QUADRATURE, which shares nothing with any polynomial algebra: compute
      fhat(y) = int f(x) e^{-2 pi i <x,y>} dx for f(x) = u^k e^{-pi|x|^2} at a few explicit y
      and compare with M's prediction.  This is the check that would catch a wrong
      normalisation (missing factor, wrong variable, factor 2 in the exponent).

A3 is a float computation and is labelled TESTED_FINITE; A1 and A2 are exact.
"""
import importlib.util, sys
from fractions import Fraction as F
import numpy as np
import exactcert as EC

def load(path):
    spec = importlib.util.spec_from_file_location("shell_check", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def my_fourier_map(K):
    """b = M a built from ell_j(t) = L_j^(1/2)(t) as exact rational polynomials.

    f = u^k e^{-pi|x|^2} = (t/2)^k e^{-t/2} with t = 2 pi |x|^2.
    Expand (t/2)^k = sum_j alpha_j ell_j(t); then f = sum_j alpha_j phi_j and
    fhat = sum_j (-1)^j alpha_j phi_j(y) = e^{-pi|y|^2} sum_j (-1)^j alpha_j ell_j(2u').
    """
    ell = EC.laguerre_polys(K)                      # ell[j] in t, rational
    M = [[F(0)] * (K + 1) for _ in range(K + 1)]
    for k in range(K + 1):
        # alpha_j: expand (t/2)^k in the ell basis
        rem = [F(0)] * (k + 1); rem[k] = F(1, 2 ** k)
        alpha = [F(0)] * (k + 1)
        for j in range(k, -1, -1):
            lc = ell[j][-1]                         # ell_j is degree j
            a = rem[j] / lc
            alpha[j] = a
            for i in range(len(ell[j])):
                rem[i] -= a * ell[j][i]
        assert all(x == 0 for x in rem), "expansion failed"
        # coefficient of u'^i in sum_j (-1)^j alpha_j ell_j(2 u')
        for j in range(k + 1):
            sgn = F(-1) ** j * alpha[j]
            for i in range(len(ell[j])):
                if ell[j][i]:
                    M[i][k] += sgn * ell[j][i] * (F(2) ** i)
    return M

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/shell_check.py"
    SC = load(path)
    K = 6
    Mmain = [[F(int(SC.fourier_map(K)[i, k].p), int(SC.fourier_map(K)[i, k].q))
              for k in range(K + 1)] for i in range(K + 1)]
    Mmine = my_fourier_map(K)
    bad = [(i, k, Mmain[i][k], Mmine[i][k]) for i in range(K + 1) for k in range(K + 1)
           if Mmain[i][k] != Mmine[i][k]]
    print("A1 exact matrix agreement (K=%d, %d entries): %s"
          % (K, (K + 1) ** 2, "PASS" if not bad else "FAIL"))
    if bad:
        for b in bad[:5]:
            print("   mismatch at (%d,%d): main %s vs mine %s" % b)
        return 1
    print("   M[0][k] = (2k+1)!!/2^k check:",
          [str(Mmain[0][k]) for k in range(4)],
          "expected", [str(F(int(np.prod(range(1, 2 * k + 2, 2))), 2 ** k)) for k in range(4)])

    # A2: the sign-flip involution.  f -> fhat -> fhat^hat = f(-.) = f (f is even).
    # In matrix terms, applying M twice must return the identity on the polynomial.
    MM = [[sum(Mmain[i][j] * Mmain[j][k] for j in range(K + 1)) for k in range(K + 1)]
          for i in range(K + 1)]
    ident = all(MM[i][k] == (F(1) if i == k else F(0)) for i in range(K + 1) for k in range(K + 1))
    print("A2 M composed with itself is the identity:", "PASS" if ident else "FAIL")
    if not ident:
        print("   (M^2 - I) nonzeros:", [(i, k, MM[i][k]) for i in range(K + 1) for k in range(K + 1)
                                         if MM[i][k] != (F(1) if i == k else F(0))][:5])

    # A3: direct quadrature, sharing nothing with polynomial algebra
    print("A3 direct quadrature of the transform (float; TESTED_FINITE)")
    from scipy.integrate import quad
    def fhat_quad(k, y):
        # radial: fhat(y) = (2/|y|) int r f(r) sin(2 pi |y| r) dr ; f(r) = (pi r^2)^k e^{-pi r^2}
        if y < 1e-9:
            return 4 * np.pi * quad(lambda r: r * r * (np.pi * r * r) ** k * np.exp(-np.pi * r * r),
                                    0, np.inf, limit=400)[0]
        return (2.0 / y) * quad(lambda r: r * (np.pi * r * r) ** k * np.exp(-np.pi * r * r)
                                * np.sin(2 * np.pi * y * r), 0, np.inf, limit=400)[0]
    ok = True
    for k in (0, 1, 2):
        for y in (0.35, 0.9):
            got = fhat_quad(k, y)
            u = np.pi * y * y
            want = np.exp(-u) * sum(float(Mmain[i][k]) * u ** i for i in range(K + 1))
            rel = abs(got - want) / max(abs(want), 1e-300)
            good = rel < 1e-8
            ok = ok and good
            print("   k=%d y=%.2f  quad=%+.10e  M-prediction=%+.10e  rel=%.1e  %s"
                  % (k, y, got, want, rel, "PASS" if good else "FAIL"))
    print("\nAUDIT", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
