#!/usr/bin/env python3
"""REPAIRED exact sign predicate — complete algebraic root isolation, no sampling.

Defect repaired (K15-REVIEW-0138): the previous predicate converted each real root with
Rational(nsimplify(root)) inside a try/except; IRRATIONAL roots raised and were silently
SKIPPED, so e.g. (t^2-2)*(t^2-3) was reported >= 0 on [0,inf) although it is -3/16 at t=3/2.
That was a false-accept (soundness) failure, the worst direction.

Repair: never convert roots.  Split p = c * prod f_i^{m_i} (Yun/squarefree).  Away from roots
sign(p) = sign(c) * prod_{m_i odd} sign(f_i) = sign(c)*sign(u) with u = prod_{m_i odd} f_i.
The sign of p on (a,inf) is constant iff u has no real root there, which is decided COMPLETELY
by Sturm counting (Poly.count_roots), which handles irrational and repeated roots exactly.
Endpoint a is handled by the multiplicity check division-free: p(a) is evaluated exactly.
"""
import sympy as sp

_T = sp.Symbol('t')

def sign_on_half_line(p, a, want, full=False, var=None):
    """EXACT: is sign(p) == want (-1/0/+1) on [a, inf)?
    Endpoint zeros are allowed (touching), interior odd-multiplicity roots are not.
    Returns bool, or (bool, reason) when full=True."""
    p = sp.expand(p)
    fs = p.free_symbols
    if var is not None: t = var
    elif len(fs) == 1:  t = list(fs)[0]
    elif len(fs) == 0:  t = _T
    else: raise ValueError("need a univariate polynomial")
    P = sp.Poly(p, t)
    if P.is_zero:
        r = (want == 0), "zero polynomial"
        return r if full else r[0]
    a = sp.nsimplify(a)
    coeff, facs = sp.sqf_list(p)
    u = sp.Integer(1)
    for f, m in facs:
        if m % 2 == 1:
            u = sp.expand(u * f)
    U = sp.Poly(u, t)
    # roots of the odd part in the OPEN interval (a, inf): remove any factor (t-a)^m first,
    # because sympy's count_roots counts the CLOSED endpoint and a zero AT a is allowed.
    W = sp.Poly(sp.expand(u), t)
    if W.degree() >= 1 and sp.simplify(W.eval(a)) == 0:
        while True:
            q, r = sp.div(W.as_expr(), (t - a), t)
            if sp.simplify(r) != 0: break
            W = sp.Poly(sp.expand(q), t)
            if W.degree() < 1: break
    n_int = W.count_roots(a, sp.oo) if W.degree() >= 1 else 0
    if n_int > 0:
        r = (False, "%d real root(s) of the odd part in (%s, inf)" % (n_int, a))
        return r if full else r[0]
    s_open = sp.sign(coeff) * sp.sign(U.LC())
    ok = (s_open == want)
    reason = "sign on (%s,inf) = %s" % (a, s_open)
    pa = sp.simplify(P.eval(a))
    if pa < 0 and want >= 0: ok, reason = False, "p(a) < 0"
    if pa > 0 and want <= 0: ok, reason = False, "p(a) > 0"
    if pa == 0: reason += "; p(a)=0 (touching allowed)"
    r = (ok, reason)
    return r if full else r[0]

def sign_on_interval(p, lo, hi, want, full=False, var=None):
    """EXACT: is sign(p) == want (-1/0/+1) on the CLOSED interval [lo, hi]?

    Same algebraic rule as the half-line version, but the interior sign must be read from the
    odd part EVALUATED INSIDE the interval: sign(lc) is only the sign on the rightmost gap, so
    using it here would be wrong (that is the trap in Main's le_on_interval and in my own first
    oracle draft).  A root of the odd part strictly inside forces a sign change -> reject.
    Endpoint zeros are allowed.
    """
    p = sp.expand(p)
    fs = p.free_symbols
    if var is not None: t = var
    elif len(fs) == 1:  t = list(fs)[0]
    elif len(fs) == 0:  t = _T
    else: raise ValueError("need a univariate polynomial")
    lo = sp.nsimplify(lo); hi = sp.nsimplify(hi)
    if sp.simplify(p.subs(t, lo)) == 0 and sp.simplify(p.subs(t, hi)) == 0 and lo == hi:
        r = (want == 0), "degenerate point interval"
        return r if full else r[0]
    P = sp.Poly(p, t)
    if P.is_zero:
        r = (want == 0), "zero polynomial"
        return r if full else r[0]
    coeff, facs = sp.sqf_list(p)
    u = sp.Integer(1)
    for f, m in facs:
        if m % 2 == 1: u = sp.expand(u * f)
    U = sp.Poly(u, t)
    # odd-multiplicity roots strictly inside (lo, hi): remove endpoint factors, then count
    W = U
    for a in (lo, hi):
        while W.degree() >= 1 and sp.simplify(W.eval(a)) == 0:
            q, r = sp.div(W.as_expr(), (t - a), t)
            if sp.simplify(r) != 0: break
            W = sp.Poly(sp.expand(q), t)
    if W.degree() >= 1 and W.count_roots(lo, hi) > 0:
        r = (False, "odd-multiplicity root strictly inside (%s,%s)" % (lo, hi))
        return r if full else r[0]
    mid = (lo + hi) / 2
    s_in = sp.sign(coeff) * sp.sign(sp.simplify(sp.expand(u).subs(t, mid)))
    ok = (s_in == want); reason = "interior sign = %s" % s_in
    for a, nm in ((lo, "p(lo)"), (hi, "p(hi)")):
        va = sp.simplify(P.eval(a))
        if va < 0 and want >= 0: ok, reason = False, nm + " < 0"
        if va > 0 and want <= 0: ok, reason = False, nm + " > 0"
    r = (ok, reason)
    return r if full else r[0]

def controls():
    t = sp.Symbol('t')
    cases = [
        # (poly, a, want, expected, label)
        ((t**2-2)*(t**2-3), 0, +1, False, "irrational roots sqrt2,sqrt3 in (0,inf)  <-- the reported witness"),
        ((t**2-2)*(t**2-3), 0, -1, False, "same, want -1 (sign not constant)"),
        ((t**2-2)**2, 0, +1, True,  "irrational DOUBLE root: square, >= 0 everywhere"),
        (-(t**2-2)**2, 0, -1, True, "negated square <= 0 everywhere"),
        ((t**2-3)*(t-sp.Rational(3,2))**2, 0, +1, False, "irrational root + even root"),
        (-(t-4), 4, -1, True,  "endpoint zero, sign correct to the right"),
        ((t-4), 4, +1, True,  "endpoint zero, positive to the right"),
        (-(t-4)**2, 4, -1, True, "endpoint double zero"),
        ((t-4), 4, -1, False, "endpoint zero but sign wrong to the right"),
        (-(t-30), sp.Rational(251327,10000), -1, False, "30-t is POSITIVE just above a (sign not constant)"),
        ((t-30), sp.Rational(251327,10000), +1, False, "simple root above a, wrong sign"),
        # ---- closed-interval cases: these exercise sign_on_interval, NOT the half-line rule ----
        ((t-1)**2*(3*t-7)/3, 0, -1, True,  "interval [0,1]: odd root 7/3 OUTSIDE -> accept le 0"),
        (-(t-1)**2*(3*t-7)/3, 0, +1, True, "interval [0,1]: negated -> accept ge 0"),
        (t*(t-sp.Rational(1,2))*(t-1), 0, -1, False, "interval [0,1]: odd roots INSIDE -> reject"),
        (-(t-1)**2*(3*t-7)/3, 0, -1, False, "interval [0,1]: wrong sign inside -> reject"),
        ((t-1)**2, 0, +1, True,  "interval [0,1]: even zero inside, >= 0 -> accept"),
        ((t-1)**2, 0, -1, False, "interval [0,1]: even zero inside, <= 0 false -> reject"),
        (sp.Integer(0), 0, +1, False, "identically zero, want +1"),
        (sp.Integer(0), 0, 0, True,  "identically zero, want 0"),
        (-(t**2+1), 0, -1, True, "always negative"),
        ((t**2+1), 0, -1, False, "always positive, want -1"),
    ]
    print("%-58s %-8s %-8s %s" % ("control","expected","got","verdict"))
    bad=0
    for poly, a, want, exp, label in cases:
        if "interval" in label:
            got, reason = sign_on_interval(poly, sp.Integer(0), sp.Integer(1), want, full=True)
        else:
            got, reason = sign_on_half_line(poly, a, want, full=True)
        ok = (got == exp)
        if not ok: bad+=1
        print("%-58s %-8s %-8s %s   [%s]" % (label[:58], exp, got, "OK" if ok else "*** MISMATCH ***", reason[:44]))
    print("\ncontrols: %d, mismatches: %d" % (len(cases), bad))
    return bad==0

if __name__=="__main__":
    import sys
    ok = controls()
    sys.exit(0 if ok else 1)
