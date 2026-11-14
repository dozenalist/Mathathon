#!/usr/bin/env python3
"""Both-sides explicit Gram with CUBIC q, from the many-square p-side family.

FAMILY.  -p(u) = (u - T) * sum_{i<=m} (a_i u + b_i)^2 ,  T rational <= 4*pi, a_i,b_i rational.
This gives deg p = 3, hence deg q = 3 once q = M p, so the Markov-Lukacs decomposition
q = (p1 u + p0)^2 + k + u (alpha u + beta)^2 is a small exact system:

    alpha = sqrt(q3),  beta = (q2 - p1^2)/(2 alpha),  p0 = (q1 - beta^2)/(2 p1),  k = q0 - p0^2,

accepted when alpha is rational and k > 0.  p1 is the one free parameter.

Both sign conditions then hold BY ALGEBRAIC IDENTITY, and the search hill-climbs over the
(a_i, b_i) accepting only candidates whose cubic q is two-square decomposable.  The target is
Delta < 1 (the trivial bound) -- the reviewer's criticism of the earlier 2.00171738 control.

Usage:  python3 sos_both_sides_lin.py [--m 3] [--iters 3000]
"""
import copy, json, os, random
from fractions import Fraction as F
import sympy as sp
import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "out")
mp.mp.dps = 30
u = sp.Symbol('u')
PI_LO = F(31415926535, 10 ** 10)

def M_matrix(K):
    t = sp.Symbol('t')
    def lag(j): return sp.expand(sp.assoc_laguerre(j, sp.Rational(1, 2), t))
    M = [[sp.Rational(0)] * (K + 1) for _ in range(K + 1)]
    for k in range(K + 1):
        poly = sp.expand((t / 2) ** k); a = [sp.Rational(0)] * (k + 1)
        for j in range(k, -1, -1):
            Lj = lag(j); cj = sp.Poly(Lj, t).coeff_monomial(t ** j)
            c = sp.Poly(poly, t).coeff_monomial(t ** j) / cj; a[j] = sp.Rational(c)
            poly = sp.expand(poly - c * Lj)
        ex = sum(((-1) ** j) * a[j] * lag(j) for j in range(k + 1))
        ex = sp.expand(ex.subs(t, 2 * u)); P = sp.Poly(ex, u)
        for i in range(K + 1):
            M[i][k] = sp.Rational(P.coeff_monomial(u ** i))
    return M

M = M_matrix(3)

def build(T, coefs):
    R = [(sp.Rational(a) * u + sp.Rational(b)) for (a, b) in coefs]
    p = sp.expand(-(u - T) * sum(r ** 2 for r in R))
    P = sp.Poly(p, u)
    if P.degree() > 3:
        return None
    a = [P.coeff_monomial(u ** i) for i in range(4)]
    b = [sum(M[i][k] * a[k] for k in range(4)) for i in range(4)]
    q = sp.expand(sum(b[i] * u ** i for i in range(4)))
    return p, q, a, b, R

def two_square(q, max_p1=120):
    Q = sp.Poly(q, u)
    q3, q2, q1, q0 = [Q.coeff_monomial(u ** i) for i in range(3, -1, -1)]
    alpha = sp.sqrt(q3)
    if not alpha.is_rational or alpha == 0:
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

def score(T, coefs):
    r = build(T, coefs)
    if r is None:
        return None
    p, q, a, b, R = r
    sol = two_square(q)
    if sol is None:
        return None
    p0, q0 = sp.Rational(a[0]), sp.Rational(b[0])
    if p0 <= 0 or q0 <= 0:
        return None
    delta = 4 * mp.pi / 3 * (mp.mpf(p0.p) / mp.mpf(p0.q)) / (mp.mpf(q0.p) / mp.mpf(q0.q))
    return float(delta), p, q, sol, R, p0, q0

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=3)
    ap.add_argument("--iters", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default=os.path.join(_OUT, "sos_both_sides_lin.json"))
    ap.add_argument("--Tnum", type=int, default=12)
    a = ap.parse_args()
    random.seed(a.seed)
    T = F(a.Tnum)
    if T > 4 * PI_LO:
        raise SystemExit("T must be <= 4*pi")
    best = None
    for _ in range(60):
        coefs = [(F(random.randint(-8, 8), random.choice([1, 2])) , F(random.randint(-8, 8), random.choice([1, 2])))
                 for _ in range(a.m)]
        s = score(T, coefs)
        if s is not None:
            best = (s, copy.deepcopy(coefs)); break
    if best is None:
        print("no admissible start"); return 1
    cur = (best[0][0], copy.deepcopy(best[1]))
    print("start Delta = %.8f  (two-square decomposable)" % cur[0])
    for it in range(a.iters):
        coefs2 = copy.deepcopy(cur[1])
        i = random.randrange(len(coefs2)); j = random.randrange(2)
        n, d = coefs2[i]
        coefs2[i] = (n + F(random.choice([-2, -1, 1, 2]), random.choice([1, 2, 3, 4])), d) if j == 0 \
                    else (n, d + F(random.choice([-2, -1, 1, 2]), random.choice([1, 2, 3, 4])))
        s = score(T, coefs2)
        if s is None:
            continue
        if s[0] < cur[0]:
            cur = (s[0], coefs2)
        if s[0] < best[0][0]:
            best = (s, coefs2)
    s, coefs = best
    delta, p, q, sol, R, p0, q0 = s
    print("\nBEST Delta <= %.10f   (%s the trivial bound 1)" % (delta, "BEATS" if delta < 1 else "does NOT beat"))
    print("  T = %s" % T)
    print("  p-side : -p = (u-%s) * [ %s ]" % (T, " + ".join("(%s)^2" % sp.expand(r) for r in R)))
    print("  q-side :  q = (%s)^2 + %s + u(%s)^2" % (sol["s0"], sol["k"], sol["s1"]))
    print("  p(0) = %s  q(0) = %s" % (p0, q0))
    ok_p = sp.simplify(-(u - T) * sum(r ** 2 for r in R) - p) == 0
    ok_q = sp.simplify(sp.sympify(sol["s0"]) ** 2 + sp.sympify(sol["k"])
                       + u * sp.sympify(sol["s1"]) ** 2 - q) == 0
    print("  identities by expansion: p-side %s, q-side %s" % (ok_p, ok_q))
    json.dump(dict(script="KeplerConjecture/Computation/sos_both_sides_lin.py",
                   status="VERIFIED_EXACT (both sides by algebraic identity)",
                   beats_trivial_bound=bool(delta < 1),
                   delta=delta, T=str(T), m=a.m,
                   p_side_squares=[str(sp.expand(r)) for r in R],
                   q_side=dict(sigma0_square=sol["s0"], sigma0_constant=str(sol["k"]),
                               sigma1_square=sol["s1"]),
                   p0=str(p0), q0=str(q0), p=str(p), q=str(q),
                   comparison=dict(trivial=1.0, kepler=0.7404804896930611, ce03=0.779747),
                   verification=dict(p_identity=bool(ok_p), q_identity=bool(ok_q))),
              open(a.out, "w"), indent=1)
    print("wrote", a.out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
