#!/usr/bin/env python3
"""G8 (partial): do C's `exactcert` and Main's `shell_check` share code, and do they agree?

`Main/PROOF_GAPS.md` G8 asks X to "confirm C's exactcert and Main's shell_check share no code
path and agree on adversarial vectors".  This script answers the first exactly and the second on
a fixed adversarial sample.  It does NOT close G8: the sample is finite, and the two checkers are
compared on `q >= 0 on [0, inf)` only, which is one of the two predicates the shell pipeline uses.

Independence.  `exactcert.py` imports `fractions.Fraction` and nothing else — its polynomial
arithmetic (`pmul`, `pdivmod`, `pgcd`) and its Sturm chain are hand-written.  `shell_check.py`
imports `sympy` and delegates root isolation to it.  Neither imports the other, and there is no
common project module.  So the two agree only if their *mathematics* agrees, which is the point.

Run: python3 Reviews/g8_checker_independence.py       (exit 0 iff all three routes agree)
"""
import importlib.util, os, random, sys
import sympy as sp
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

main = load("sc", "shell_check_5caa1c9.py")
comp = load("ec", "exactcert_comp_5c10267.py")

def comp_nonneg(coeffs):
    """q >= 0 on [0,inf) using ONLY exactcert's primitives."""
    p = [F(c) for c in coeffs]
    if comp.trim(p) == [F(0)]: return True
    c, u = comp.yun_odd_part(p)
    if c is None: return True
    if comp.trim(u) == [F(1)]: return c > 0
    if comp.peval(u, F(0)) == 0:                     # u squarefree => multiplicity 1 at 0
        q, r = comp.pdivmod(u, [F(0), F(1)])
        assert comp.trim(r) == [F(0)]
        u1 = comp.trim(q)
    else:
        u1 = u
    s0 = comp.peval(u1, F(0))
    nroots = comp.roots_in_half_line(u1, F(0)) if len(u1) > 1 else 0
    return nroots == 0 and c * s0 > 0

def truth(coeffs):
    """Independent algebraic rule: no odd-multiplicity root in (0,inf), sign + just right of 0."""
    x = sp.Symbol('x')
    p = sum(sp.Rational(c) * x**i for i, c in enumerate(coeffs))
    if sp.expand(p) == 0: return True
    c0, facs = sp.sqf_list(p)
    odd = sp.Integer(1)
    for f, k in facs:
        if k % 2 == 1: odd = sp.expand(odd * f)
    O = sp.Poly(odd, x)
    if O.degree() < 1:
        # constant odd part: sign is constant everywhere
        return sp.sign(c0 * O.LC()) > 0
    # multiplicity of 0 in the odd part
    while sp.simplify(O.eval(0)) == 0:
        q, r = sp.div(O.as_expr(), x, x)
        O = sp.Poly(sp.expand(q), x)
    n = O.count_roots(0, sp.oo)
    if n > 0: return False
    return sp.sign(c0 * O.eval(0)) > 0

random.seed(99)
cases = []
# structured: root at 0, repeated roots, near-touching pair, both leading signs
cases += [[0, 1], [0, -1], [1, 0, 1], [-1, 0, -1], [0, 0, 1], [1, -2, 1], [-1, 2, -1]]
# near-touching: (x - r)^2 -/+ eps, the family that broke probe-based checkers
xs = sp.Symbol('x')
eps = sp.Rational(1, 10**20)
extra = []
for r in (sp.Rational(3,5), sp.Rational(7,5), sp.Rational(1,1)):
    for sgn in (1, -1):
        for d in (eps, sp.Rational(1, 10**8)):
            P = sp.Poly(sp.expand((xs - r)**2 + sgn*d), xs)
            extra.append([P.coeff_monomial(xs**k) for k in range(P.degree()+1)])
cases = [c for c in cases if c] + extra
# random: roots in [0,2], multiplicities 1-2, random leading sign
for _ in range(33):
    p = sp.Integer(random.choice([1, -1]))
    for _ in range(random.randint(1, 4)):
        r = sp.Rational(random.randint(0, 20), 10)
        p = sp.expand(p * (sp.Symbol('x') - r)**random.choice([1, 1, 2]))
    P = sp.Poly(p, sp.Symbol('x'))
    cases.append([P.coeff_monomial(sp.Symbol('x')**k) for k in range(P.degree() + 1)])

# fourth route: X's own exact_sign, which every X certificate rests on
es = load("es", os.path.join("..", "exact_sign.py"))
xs_ = sp.Symbol('x')
def x_side(coeffs):
    p = sum(sp.Rational(v)*xs_**i for i, v in enumerate(coeffs))
    return bool(es.sign_on_half_line(p, 0, +1, var=xs_))

bad = 0
for coeffs in cases:
    t = bool(truth(coeffs))
    a = main.nonneg_on_half_line(coeffs)
    b = comp_nonneg(coeffs)
    xv = x_side(coeffs)
    if not (t == a == b == xv):
        bad += 1
        print("  MISMATCH truth=%s main=%s comp=%s exact_sign=%s on %s" % (t, a, b, xv, coeffs))
print("%d cases: truth == Main == C == X's exact_sign on %d, mismatches %d"
      % (len(cases), len(cases)-bad, bad))
print("imports: exactcert -> {fractions}; shell_check -> {sympy, fractions}; no shared module")
sys.exit(0 if bad == 0 else 1)
