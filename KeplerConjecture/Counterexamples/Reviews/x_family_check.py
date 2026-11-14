#!/usr/bin/env python3
"""Parameterised adversarial FAMILY check (not a finite probe list).

For random rational roots r_i in [0,2] and exponents e_i in {1,2}, form
    p(u) = c * prod (u - r_i)^{e_i},   c = +-1,
and query the closed-interval / half-line predicates.  The TRUTH is computed from
the proven algebraic rule, implemented here independently of any checker:
    the sign of p is constant and NONZERO on every gap between distinct real roots,
    and equals  sign(c) * sign(lc(odd part of p))  on all gaps at once;
so   p <= 0 on [lo,hi]  <=>  (gap sign <= 0)  and  p(lo) <= 0  and  p(hi) <= 0.
No sampling, no probe placement, and the expectation never depends on the checker.

Usage: python3 x_family_check.py <shell_check.py> [n_cases] [seed]
"""
import importlib.util, sys, random
import sympy as sp
from fractions import Fraction as Fr

def gap_sign(p, u):
    """sign of p on every gap between its distinct real roots (proven constant)."""
    c, facs = sp.sqf_list(p)
    odd = sp.Integer(1)
    for f, m in facs:
        if m % 2 == 1: odd = sp.expand(odd * f)
    O = sp.Poly(odd, u)
    return sp.sign(c) * (sp.sign(O.LC()) if O.degree() >= 1 else 1)

def _odd_roots_in(p, a, b, u):
    """number of real roots of the ODD part in the open interval (a,b); b may be oo.
    A root of odd multiplicity forces a sign change, so the polynomial cannot have a
    constant sign on an interval containing it."""
    c, facs = sp.sqf_list(p)
    odd = sp.Integer(1)
    for f, m in facs:
        if m % 2 == 1: odd = sp.expand(odd * f)
    O = sp.Poly(odd, u)
    if O.degree() < 1: return 0
    W = O
    while W.degree() >= 1 and sp.simplify(W.eval(a)) == 0:
        q, r = sp.div(W.as_expr(), (u - a), u)
        if sp.simplify(r) != 0: break
        W = sp.Poly(sp.expand(q), u)
    n = W.count_roots(a, b) if W.degree() >= 1 else 0
    if b is not sp.oo and W.degree() >= 1 and sp.simplify(W.eval(b)) == 0:
        n -= 1
    return n

def _sign_in_domain(p, lo, mid, u):
    """sign of p on the (root-free) interior, from the odd part evaluated INSIDE the domain.
    sign(lc) is only the sign on the rightmost gap, so it must not be used for a bounded
    interval.  The odd part has no root in the interior, so evaluating it anywhere inside
    is valid (even at an even-multiplicity zero of p, where the odd part is nonzero)."""
    c, facs = sp.sqf_list(p)
    odd = sp.Integer(1)
    for f, m in facs:
        if m % 2 == 1: odd = sp.expand(odd * f)
    return sp.sign(c) * sp.sign(sp.simplify(odd.subs(u, mid)))

def truth_le_interval(p, lo, hi, u):
    if _odd_roots_in(p, lo, hi, u) > 0: return False
    mid = (sp.Rational(lo) + sp.Rational(hi)) / 2
    if _sign_in_domain(p, lo, mid, u) > 0: return False
    return sp.simplify(p.subs(u, lo)) <= 0 and sp.simplify(p.subs(u, hi)) <= 0

def truth_ge_half_line(p, u):
    """on [0,inf) the odd part has no root, so its sign IS sign(lc) (rightmost gap)."""
    if _odd_roots_in(p, 0, sp.oo, u) > 0: return False
    return gap_sign(p, u) >= 0 and sp.simplify(p.subs(u, 0)) >= 0

def truth_le_ray(p, hi, u):
    if _odd_roots_in(p, hi, sp.oo, u) > 0: return False
    return gap_sign(p, u) <= 0 and sp.simplify(p.subs(u, hi)) <= 0

def to_coeffs(p, u):
    P = sp.Poly(sp.expand(p), u); d = P.degree()
    return [P.coeff_monomial(u**k) for k in range(d+1)]

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'shell_check_9461aae.py'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    spec = importlib.util.spec_from_file_location("sc", path); sc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sc)
    u = sp.Symbol('u'); rng = random.Random(seed)
    roots_pool = [Fr(k, 2) for k in range(0, 5)] + [Fr(1, 4), Fr(3, 4), Fr(5, 4), Fr(7, 3)]
    fails = {'le_on_interval': [], 'nonneg_on_half_line': [], '_ray': []}
    for _ in range(n):
        k = rng.choice([1, 2, 3, 4])
        rs = [rng.choice(roots_pool) for _ in range(k)]
        es = [rng.choice([1, 2]) for _ in range(k)]
        c = rng.choice([1, -1])
        p = sp.Integer(c)
        for r, e in zip(rs, es): p = sp.expand(p * (u - sp.Rational(r.numerator, r.denominator))**e)
        cs = to_coeffs(p, u)
        t1 = truth_le_interval(p, sp.Integer(0), sp.Integer(1), u)
        try: g1 = sc.le_on_interval(cs, sp.Integer(0), sp.Integer(0), sp.Integer(1))
        except Exception as e: g1 = "EXC"
        if g1 != t1: fails['le_on_interval'].append((p, t1, g1))
        t2 = truth_ge_half_line(p, u)
        try: g2 = sc.nonneg_on_half_line(cs)
        except Exception as e: g2 = "EXC"
        if g2 != t2: fails['nonneg_on_half_line'].append((p, t2, g2))
        t3 = truth_le_ray(p, sp.Integer(0), u)
        try: g3 = sc._ray(cs, sp.Integer(0))
        except Exception as e: g3 = "EXC"
        if g3 != t3: fails['_ray'].append((p, t3, g3))
    print("family check against %s : %d random polynomials, roots in [0,2], exponents in {1,2}" % (path, n))
    tot = 0
    for name, fl in fails.items():
        tot += len(fl)
        print("  %-22s %3d wrong verdicts" % (name, len(fl)))
        for p, t, g in fl[:3]:
            print("      e.g. p = %-42s truth=%-5s got=%s" % (str(sp.factor(p))[:42], t, g))
    print("  TOTAL wrong verdicts (random family): %d / %d queries" % (tot, 3*n))

    # ---- TARGETED family: place even-multiplicity roots AT the implementation's fixed probes.
    # Random/parameterised families cannot hit this coincidence (probability ~1e-4), which is
    # why a "broad random audit" reporting zero failures proves very little.
    print("\n  targeted family: roots exactly at the fixed probe positions")
    tgt = 0
    for (probes, name) in [((0, sp.Rational(1,2), 1), "le_on_interval probes (lo, mid, hi) on [0,1]"),
                           ((0, 1, 2), "_ray probes (hi, hi+1, hi+2) at hi=0")]:
        for c in (1, -1):
            for es in ([2,2,2], [2,2,1], [1,2,2]):
                p = sp.Integer(c)
                for r, e in zip(probes, es):
                    p = sp.expand(p * (u - sp.Rational(r))**e)
                cs = to_coeffs(p, u)
                if name.startswith("le"):
                    t = truth_le_interval(p, sp.Integer(0), sp.Integer(1), u)
                    try: g = sc.le_on_interval(cs, sp.Integer(0), sp.Integer(0), sp.Integer(1))
                    except Exception: g = "EXC"
                else:
                    t = truth_le_ray(p, sp.Integer(0), u)
                    try: g = sc._ray(cs, sp.Integer(0))
                    except Exception: g = "EXC"
                if g != t:
                    tgt += 1
                    print("      p = %-44s truth=%-5s got=%-5s  <-- false accept" % (str(sp.factor(p))[:44], t, g))
    print("  TOTAL wrong verdicts (probe-targeted family): %d" % tgt)
    return 1 if (tot + tgt) else 0

if __name__ == "__main__":
    sys.exit(main())
