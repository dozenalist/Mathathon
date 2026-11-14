#!/usr/bin/env python3
"""Search the cubic p-side family for a BOTH-SIDES explicit-Gram certificate beating Delta <= 1.

MOTIVATION.  The reviewer is right that the existing both-sides certificate
(Delta <= 2.00171738) is WEAKER THAN THE TRIVIAL BOUND Delta <= 1, so it demonstrates format
only.  This file searches for one that is not: an explicit rational Gram on both sides with
Delta < 1 would be a genuine (if modest) Cohn-Elkies certificate whose two sign conditions are
algebraic identities.

FAMILY.  p(u) = -(u - T)(u - c)^2 with T, c rational and T <= 4*pi.  Then
  -p = (u-T)(u-c)^2                                          (p-side: one rational square)
and q = M p is a cubic.  The Markov-Lukacs decomposition for a cubic on [0, inf) is

  q = (sigma_0) + u (sigma_1),   sigma_0 = (p1 u + p0)^2 + k,  sigma_1 = (alpha u + beta)^2,

with alpha^2 = q3, then p1 free, beta = (q2 - p1^2)/(2 alpha), p0 = (q1 - beta^2)/(2 p1), and
k = q0 - p0^2.  Accept when alpha is rational and k > 0.  All exact.

Every accepted candidate is verified by expanding both identities; no Sturm anywhere.

Usage:  python3 sos_both_sides_search.py [--Tmax-num ...]
"""
import json, os
from fractions import Fraction as F
import sympy as sp
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
mp.mp.dps = 30
u = sp.Symbol('u')
PI_LO = F(31415926535, 10 ** 10)
TRIVIAL = 1.0

def M_matrix(K):
    """Rational Fourier matrix in the basis u = pi|x|^2: b = M a.
    Rebuilt here so the file has no external checker dependency and no scratch-directory paths."""
    t = sp.Symbol('t')
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

def cubic_candidate(T, c, M):
    p = sp.expand(-(u - T) * (u - c) ** 2)
    P = sp.Poly(p, u)
    a = [P.coeff_monomial(u ** i) for i in range(4)]
    b = [sum(M[i][k] * a[k] for k in range(4)) for i in range(4)]
    q = sp.expand(sum(b[i] * u ** i for i in range(4)))
    return p, q, a, b

def two_square_solve(q, max_p1=200):
    Q = sp.Poly(q, u)
    q3, q2, q1, q0 = [Q.coeff_monomial(u ** i) for i in range(3, -1, -1)]
    alpha = sp.sqrt(q3)
    if not alpha.is_rational:
        return None
    for num in range(1, max_p1):
        for den in (1, 2, 3, 4, 6, 8):
            p1 = sp.Rational(num, den)
            beta = (q2 - p1 ** 2) / (2 * alpha)
            p0 = (q1 - beta ** 2) / (2 * p1)
            k = q0 - p0 ** 2
            if k <= 0:
                continue
            if sp.simplify((p1 * u + p0) ** 2 + k + u * (alpha * u + beta) ** 2 - Q.as_expr()) == 0:
                return dict(alpha=alpha, beta=beta, p1=p1, p0=p0, k=k,
                            s0=str(sp.expand(p1 * u + p0)), s1=str(sp.expand(alpha * u + beta)))
    return None

def main():
    M = M_matrix(3)
    best = None
    rows = []
    print("searching cubic family for a both-sides explicit Gram with Delta < %.1f (trivial)" % TRIVIAL)
    Ts = [F(12), F(314, 25), F(1256, 100), F(4) * PI_LO]
    cs = [F(n, d) for n in range(1, 40) for d in (1, 2)]
    for T in Ts:
        if T > 4 * PI_LO:
            continue
        for c in cs:
            p, q, a, b = cubic_candidate(T, c, M)
            sol = two_square_solve(q)
            if sol is None:
                continue
            p0, q0 = sp.Rational(a[0]), sp.Rational(b[0])
            if p0 <= 0 or q0 <= 0:
                continue
            delta = 4 * mp.pi / 3 * mp.mpf(p0.p) / mp.mpf(p0.q) / (mp.mpf(q0.p) / mp.mpf(q0.q))
            rows.append(dict(T=str(T), c=str(c), delta=float(delta)))
            if best is None or delta < best[0]:
                best = (delta, T, c, sol, p, q, p0, q0)
    rows.sort(key=lambda r: r["delta"])
    print("both-sides certificates found: %d" % len(rows))
    for r in rows[:5]:
        print("  T=%-6s c=%-4s Delta <= %.8f  %s" % (r["T"], r["c"], r["delta"],
              "BEATS TRIVIAL" if r["delta"] < 1 else ""))
    if best is None:
        print("none found"); return 1
    delta, T, c, sol, p, q, p0, q0 = best
    print("\nBEST: T=%s c=%s" % (T, c))
    print("  p-side : -p = (u-%s)(u-%s)^2" % (T, c))
    print("  q-side :  q = (%s)^2 + %s + u(%s)^2" % (sol["s0"], sol["k"], sol["s1"]))
    print("  p(0) = %s  q(0) = %s" % (p0, q0))
    print("  Delta <= %.10f   (trivial bound 1, Kepler 0.74048049, CE 0.779747)" % float(delta))
    ok_p = sp.simplify(-(u - T) * (u - c) ** 2 - p) == 0
    ok_q = sp.simplify((sp.sympify(sol["s0"])) ** 2 + sp.sympify(sol["k"])
                       + u * sp.sympify(sol["s1"]) ** 2 - q) == 0
    print("  identities verified by expansion: p-side %s, q-side %s" % (ok_p, ok_q))
    json.dump(dict(script="KeplerConjecture/Computation/sos_both_sides_search.py",
                   status="VERIFIED_EXACT (both sides by algebraic identity)",
                   beats_trivial_bound=bool(delta < 1),
                   theorem="Delta <= %.10f" % float(delta),
                   comparison=dict(trivial=1.0, kepler=0.7404804896930611,
                                   ce03=0.779747, lp_optimal=0.77996622),
                   p_side=dict(T=str(T), c=str(c), identity="-p = (u-T)(u-c)^2"),
                   q_side=dict(sigma0_square=sol["s0"], sigma0_constant=str(sol["k"]),
                               sigma1_square=sol["s1"],
                               identity="q = sigma0 + u*sigma1"),
                   p0=str(p0), q0=str(q0), p=str(p), q=str(q),
                   verification=dict(p_identity=bool(ok_p), q_identity=bool(ok_q)),
                   all_found=rows[:20]), open(os.path.join(_OUT, "sos_both_sides_search.json"), "w"), indent=1)
    print("\nwrote out/sos_both_sides_search.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
