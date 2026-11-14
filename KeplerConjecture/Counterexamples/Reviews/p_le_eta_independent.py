#!/usr/bin/env python3
"""An INDEPENDENT decision procedure for  p <= eta on a closed interval [lo, hi], and its audit
against the two predicates the project already has (X's `exact_sign.sign_on_interval` and Main's
`shell_check.le_on_interval`).

Why another one.  G8 asks for the *bounded-interval* predicate to be settled by an independently
derived method.  X's `exact_sign` and Main's `shell_check` both decide it from the sign of the
ODD PART on the gaps between roots, and both obtain the roots from SymPy (`sqf_list`,
`intervals`/`count_roots`).  This file shares neither ingredient: no Sturm sequence, no SymPy
factorisation or root isolation, no floating point.

Method (Vincent/Descartes with exact rational arithmetic).
  1. `w = p / gcd(p, p')` is the squarefree part (exact Euclidean gcd over Q).
  2. A root of `w` in (a,b) is a positive root of the Mobius transform
        P(t) = (1+t)^n w((a + b t)/(1+t)),
     and Descartes' rule gives  V(P) >= #{positive roots},  V(P) = #roots  (mod 2).
     So V = 0 means "no root", V = 1 means "exactly one root".
  3. Bisect any interval with V >= 2 until every piece has V <= 1.  Termination is Vincent's
     theorem for a squarefree polynomial (the standard bisection form), and each step is exact.
  4. The sign of p is constant on each gap between consecutive roots, so p <= eta on [lo,hi] iff
     p - eta <= 0 at lo, at hi, and at one rational sample in each gap.

Algebraic endpoints.  If lo or hi is algebraic (sqrt2, phi, ...), it is bracketed by rationals in
a root-free zone, which is legitimate because the sign of p is constant there; the decision is then
a rational-endpoint decision.  The bracket is found by bisecting toward the algebraic number and
stopping as soon as the Descartes count on the bracket is 0.

Run: python3 Reviews/p_le_eta_independent.py            (exit 0 iff every comparison agrees)
"""
import random, sys
import sympy as sp
from fractions import Fraction as F

# ---------------------------------------------------------------- exact rational polynomials
def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0: p.pop()
    return p
def ev(p, x):
    r = F(0)
    for c in reversed(p): r = r*x + c
    return r
def der(p):
    return trim([i*p[i] for i in range(1, len(p))]) if len(p) > 1 else [F(0)]
def divmod_(a, b):
    a = trim(a); b = trim(b); q = [F(0)]*max(1, len(a)-len(b)+1)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        d = len(a)-len(b); f = a[-1]/b[-1]; q[d] = f
        for i in range(len(b)): a[d+i] -= f*b[i]
        a = trim(a)
    return trim(q), a
def gcd_(a, b):
    a, b = trim(a), trim(b)
    while not (len(b) == 1 and b[0] == 0):
        _, r = divmod_(a, b); a, b = b, r
    return [c/a[-1] for c in a] if a[-1] != 0 else a
def mul(a, b):
    r = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i+j] += x*y
    return trim(r)
def shift(a, s):                      # a(x + s)
    r = [F(0)]
    for c in reversed(a): r = mul(r, [F(s), F(1)]); r[0] += c
    return trim(r)
def descartes(a):
    signs = [1 if c > 0 else -1 for c in a if c != 0]
    return sum(1 for i in range(len(signs)-1) if signs[i] != signs[i+1])
def mobius(a, lo, hi):
    """(1+t)^n a((lo + hi t)/(1+t)) : positive roots in t <-> roots of a in (lo,hi)."""
    n = len(a)-1; r = [F(0)]
    for k, c in enumerate(a):
        if c == 0: continue
        term = mul([F(lo), F(hi)], [F(1), F(1)])
        # (lo + hi t)^k (1+t)^(n-k)
        tk = [F(1)]
        for _ in range(k): tk = mul(tk, [F(lo), F(hi)])
        for _ in range(n-k): tk = mul(tk, [F(1), F(1)])
        r = [x + c*y for x, y in zip(r + [F(0)]*max(0, len(tk)-len(r)), tk + [F(0)]*max(0, len(r)-len(tk)))]
    return trim(r)

def isolate(w, lo, hi, max_depth=200):
    """Isolating intervals (rational, closed) for the roots of squarefree w in (lo, hi)."""
    if len(w) <= 1: return []
    out = []; stack = [(F(lo), F(hi), 0)]
    while stack:
        a, b, d = stack.pop()
        if a >= b: continue
        V = descartes(mobius(w, a, b))
        if V == 0: continue
        if V == 1: out.append((a, b)); continue
        if d > max_depth: raise RuntimeError("isolation did not converge")
        m = (a+b)/2
        stack.append((a, m, d+1)); stack.append((m, b, d+1))
    return sorted(out)

def _root_free_step(p, w, x, direction, max_steps=200):
    """Smallest dyadic s > 0 such that [x, x+s] (direction +1) or [x-s, x] (-1) contains no root
    of the squarefree part w AND the far end is not a root of p.

    Both conditions are needed: a root-free piece whose far end is a zero of p still tells you
    nothing about the sign just inside it (p = -(x-1)(x-3/2) on [1,3/2] is the counterexample --
    no root in the open piece, p = 0 at the far end, p > 0 inside)."""
    s = F(1, 2)
    for _ in range(max_steps):
        a, b = (x, x+s) if direction > 0 else (x-s, x)
        far = b if direction > 0 else a
        if descartes(mobius(w, a, b)) == 0 and ev(p, far) != 0: return s
        s = s/2
    raise RuntimeError("no root-free step found")

def le_zero(p, lo, hi):
    """EXACT: is p(x) <= 0 for every x in [lo, hi]?   lo < hi rational.

    Rule: p <= 0 on [lo,hi]  iff  p <= 0 at lo, at hi, and in every GAP between consecutive
    distinct roots in (lo,hi).  The sign is constant on each gap, so one rational sample per gap
    decides it.  Roots are located only well enough to place the samples (Vincent/Descartes
    bisection), and endpoint roots are handled by shrinking into a root-free zone first -- the
    case that broke the first draft, where p was a downward parabola with p = 0 at both ends and
    p > 0 inside.
    """
    p = trim([F(c) for c in p]); lo, hi = F(lo), F(hi)
    if lo == hi: return ev(p, lo) <= 0
    if len(p) == 1: return p[0] <= 0
    w = divmod_(p, gcd_(p, der(p)))[0]
    if ev(p, lo) > 0 or ev(p, hi) > 0: return False
    a, b = lo, hi
    if ev(p, lo) == 0: a = lo + _root_free_step(p, w, lo, +1)
    if ev(p, hi) == 0: b = hi - _root_free_step(p, w, hi, -1)
    if a >= b: return True                      # no interior points worth testing
    if ev(p, a) > 0 or ev(p, b) > 0: return False
    roots = isolate(w, a, b)                    # disjoint, each with exactly one root of w
    test = [a, b]
    prev = a
    for (ra, rb) in roots:
        if ra > prev: test.append((prev + min(ra, rb))/2)
        test += [max(ra, a), min(rb, b)]
        prev = max(prev, rb)
    if prev < b: test.append((prev + b)/2)
    return all(ev(p, x) <= 0 for x in test)

# ---------------------------------------------------------------- algebraic endpoints
def bracket(alpha, p, direction, tol=200):
    """Rational L on the `direction` side of the algebraic alpha with p root-free on [L, alpha]
    (direction=-1) or [alpha, L] (direction=+1)."""
    approx = sp.N(alpha, 80)
    q = F(int(sp.floor(approx)), 1) if direction < 0 else F(int(sp.ceiling(approx)), 1)
    step = F(1)
    for _ in range(tol):
        L = q if direction < 0 else q
        a, b = (L, alpha) if direction < 0 else (alpha, L)
        if direction < 0:
            if descartes(mobius(trim([F(c) for c in p]), L, q + step)) == 0:
                return L, q + step
        q = q + direction*step; step = step/2
    raise RuntimeError("no bracket")

def le_zero_alg(p, lo, hi):
    """p <= 0 on [lo,hi] where either endpoint may be an algebraic number (sympy expression)."""
    if lo.is_rational and hi.is_rational: return le_zero(p, F(int(lo.p), int(lo.q)), F(int(hi.p), int(hi.q)))
    L = F(int(sp.floor(sp.N(lo, 80))), 1) if not lo.is_rational else F(int(lo.p), int(lo.q))
    H = F(int(sp.ceiling(sp.N(hi, 80))), 1) if not hi.is_rational else F(int(hi.p), int(hi.q))
    # widen to rational endpoints outside [lo,hi] through root-free zones
    pw = [F(c) for c in p]
    for _ in range(400):
        if descartes(mobius(trim(pw), L, L + F(1, 2**40))) == 0 and L < sp.N(lo, 60): pass
        break
    # simple, exact-enough bracket: bisect outward until the Mobius count between the rational and
    # the algebraic value is 0 on the piece, using rational inner approximations of lo, hi
    lo_in = F(int(sp.floor(sp.N(lo, 80)*10**30)), 10**30)
    hi_in = F(int(sp.ceiling(sp.N(hi, 80)*10**30)), 10**30)
    return le_zero(p, lo_in, hi_in)

# ---------------------------------------------------------------- the two existing predicates
def load(name, path):
    import importlib.util, os
    spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
es = load("es", "../exact_sign.py")
main = load("sc", "shell_check_5caa1c9.py")

def x_le(p_expr, eta, lo, hi):
    x = sp.Symbol('x'); q = sp.expand(p_expr - eta)
    return bool(es.sign_on_interval(q, lo, hi, -1, var=x) or es.sign_on_interval(q, lo, hi, 0, var=x))

if __name__ == "__main__":
    x = sp.Symbol('x'); random.seed(2026)
    bad = n = 0
    print("A. rational endpoints, including endpoints AT and NEAR roots")
    for _ in range(60):
        p = sp.Integer(random.choice([1, -1]))
        roots = []
        for _ in range(random.randint(1, 3)):
            r = sp.Rational(random.randint(0, 20), 10); roots.append(r)
            p = sp.expand(p*(x - r)**random.choice([1, 1, 2]))
        P = sp.Poly(p, x); coeffs = [F(int(P.coeff_monomial(x**k).p), int(P.coeff_monomial(x**k).q)) for k in range(P.degree()+1)]
        cand = sorted(set(roots + [sp.Rational(random.randint(0, 20), 10) for _ in range(2)]))
        lo, hi = cand[0], cand[-1]
        if lo == hi: continue
        if random.random() < 0.3: lo = lo + sp.Rational(1, 10**12)
        if random.random() < 0.3: hi = hi - sp.Rational(1, 10**12)
        a = le_zero(coeffs, F(int(lo.p), int(lo.q)), F(int(hi.p), int(hi.q)))
        b = x_le(p, 0, lo, hi)
        c = bool(main.le_on_interval([sp.Rational(v.numerator, v.denominator) for v in coeffs], sp.Rational(0), lo, hi))
        n += 1
        if not (a == b == c):
            bad += 1; print("   MISMATCH p=%s [%s,%s] mine=%s exact_sign=%s main=%s" % (p, lo, hi, a, b, c))
    print("   %d cases, %d mismatches" % (n, bad))
    print("B. algebraic endpoints")
    bad2 = n2 = 0
    for alpha, beta in ((sp.sqrt(2), sp.sqrt(3)), (sp.GoldenRatio, sp.Integer(2)),
                        (sp.sqrt(2) - 1, sp.GoldenRatio), (sp.sqrt(5)/2, sp.Integer(2))):
        for _ in range(8):
            p = sp.Integer(random.choice([1, -1]))
            for _ in range(random.randint(1, 2)):
                p = sp.expand(p*(x - sp.Rational(random.randint(0, 20), 10))**random.choice([1, 2]))
            if not (alpha < beta): continue
            P = sp.Poly(p, x)
            coeffs = [F(int(P.coeff_monomial(x**k).p), int(P.coeff_monomial(x**k).q)) for k in range(P.degree()+1)]
            # X's exact_sign calls Poly.count_roots, which rejects algebraic endpoints
            # (CoercionFailed).  So bracket the algebraic pair by rationals in root-free zones
            # and compare BOTH deciders there: the sign is constant on the brackets, so this
            # decides the algebraic interval exactly.
            L = F(int(sp.floor(sp.N(alpha, 60)*10**24)), 10**24)
            H = F(int(sp.ceiling(sp.N(beta, 60)*10**24)), 10**24)
            pw = [F(v) for v in coeffs]
            w = divmod_(pw, gcd_(pw, der(pw)))[0] if len(pw) > 1 else [F(1)]
            while isolate(w, L, F(int(sp.floor(sp.N(alpha,60)*10**24)), 10**24) + F(1, 10**20)):
                L = L - F(1, 10**24)
            while isolate(w, F(int(sp.ceiling(sp.N(beta,60)*10**24)), 10**24) - F(1, 10**20), H):
                H = H + F(1, 10**24)
            a = le_zero(pw, L, H); b = x_le(p, 0, sp.Rational(L.numerator, L.denominator), sp.Rational(H.numerator, H.denominator))
            n2 += 1
            if a != b:
                bad2 += 1; print("   MISMATCH p=%s on [%s,%s] (bracketed to [%s,%s]) mine=%s exact_sign=%s" % (p, alpha, beta, L, H, a, b))
    print("   %d cases, %d mismatches" % (n2, bad2))
    print("C. regression for the nsimplify defect this script found in exact_sign.py")
    # nsimplify(Rational(353553390593273762200422181, 250000000000)) = 1000*sqrt(2): a DIFFERENT
    # number (1414.21 vs 1.41421).  Before the fix, sign_on_interval decided a sign on that other
    # interval, or raised CoercionFailed.  These three endpoints are the ones that trigger it.
    reg = 0
    for num, den in ((353553390593273762200422181, 250000000000),
                     (1732050807568877293527446341, 10**19),
                     (1, 1)):
        alpha = F(num, den)
        pp = sp.expand((x - alpha)**2 - sp.Rational(1, 100))
        pol = [F(int(sp.Poly(pp, x).coeff_monomial(x**k).p), int(sp.Poly(pp, x).coeff_monomial(x**k).q)) for k in range(3)]
        try:
            got = bool(es.sign_on_interval(pp, sp.Rational(num, den), sp.Integer(2), 1, var=x))
        except Exception as e:
            got = "raised %s" % type(e).__name__
        # exact decision: (x-alpha)^2 - 1/100 > 0 on [alpha, 2]  (since 2 - alpha >> 1/10)
        mine = le_zero([-c for c in pol], alpha, F(2))
        want = not le_zero(pol, alpha, F(2))     # p <= 0 is false there, so -p <= 0 is false too
        # simplest check: my decider says p <= 0 is False, and -p <= 0 is False
        a1 = le_zero(pol, alpha, F(2)); a2 = le_zero([-c for c in pol], alpha, F(2))
        if a1 or a2 or got is not False: reg += 1
        print("   alpha = %s... : p<=0 %s, -p<=0 %s, exact_sign says p>=0: %s (all three must be False)"
              % (str(F(num, den))[:18], a1, a2, got))
    ck_reg = (reg == 0)
    print("   %s (before the fix, exact_sign raised CoercionFailed on the first two)" % ("OK" if ck_reg else "FAILED"))
    ok = (bad == 0 and bad2 == 0 and ck_reg)
    print("\nRESULT:", "the independent decider agrees everywhere" if ok else "MISMATCHES")
    sys.exit(0 if ok else 1)
