#!/usr/bin/env python3
"""K15 exact certificate checker: rational polynomials + Sturm, no floating point.

OBJECTS (the whole point is to keep the polynomial and the function distinct)
  Variable t = 2*pi*|x|^2  (so t >= 0 always).
  Polynomial  p  in Q[t]      function  f(x) = p(t) * exp(-t/2)
  Polynomial  q  in Q[t]      function  fhat(t') = q(t') * exp(-t'/2)
  Fourier map: on the Laguerre basis L_k^(1/2)(t) the transform acts diagonally
  with eigenvalue (-1)^k, so with f = sum_{k<=K} c_k L_k^(1/2)(t) exp(-t/2),
      p = sum c_k L_k^(1/2),      q = sum (-1)^k c_k L_k^(1/2).
  The map c -> (p,q) is exact and its inverse is c_k from p alone; q is p with
  alternating signs in this basis.  Both p and q have RATIONAL coefficients
  whenever c is rational, because L_k^(1/2) has rational coefficients.

SIGN CONDITIONS (unit-radius contract, minimum separation 2)
  (A1)  f(x) <= 0 for |x| >= 2      <=>   p(t) < 0 for t >= 8*pi
  (A2)  fhat  >= 0 for all t        <=>   q(t) > 0 for t >= 0
  Bound:  Delta <= (4*pi/3) * p(0)/q(0).

HOW THE IRRATIONAL ENDPOINT 8*pi IS HANDLED
  pi lies in the rational interval [PI_LO, PI_HI] with PI_LO < pi < PI_HI
  (decimal truncations of rigorously known digits).  Since 8*PI_LO < 8*pi,
      p < 0 on [8*PI_LO, infinity)  ==>  p < 0 on [8*pi, infinity),
  so the constraint we verify is slightly STRONGER than required.  The direction
  is safe: we may only ever certify a smaller (worse) bound, never an invalid one.
  No symbolic pi and no interval arithmetic on coefficients is needed.

WHY STRICT SIGNS
  We verify "q has no real root on the half-line and is positive at the endpoint".
  Then the sign cannot change, so q > 0 on the whole half-line.  Strictness is a
  real loss: at a true optimum p and q touch zero (double zeros are forced by the
  equality case), so this route certifies a value strictly worse than the
  numerical optimum.  That is deliberate: a loose proved bound beats an
  unproved sharp one.  Closing the gap needs even-multiplicity (squarefree)
  analysis; see REQUESTS/K15-C-REQ-002.md.

WHAT THIS DOES NOT DO
  It does not prove that any particular delta is optimal; it proves
  "Delta <= X" for an explicit X, given an exact certificate in this family.
  It says nothing about the sharpness of the family.
"""
from fractions import Fraction as F

# ---------------------------------------------------------------- polynomials
# Polynomials are lists of Fractions, index = degree, no trailing zeros.

def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def padd(a, b):
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0))
                 for i in range(n)])

def pscale(a, s):
    return trim([x * s for x in a])

def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return trim(out)

def pder(a):
    if len(a) == 1:
        return [F(0)]
    return trim([a[i] * i for i in range(1, len(a))])

def peval(a, x):
    r = F(0)
    for c in reversed(a):
        r = r * x + c
    return r

def pdivmod(a, b):
    a = list(a); b = trim(list(b))
    if b == [0]:
        raise ZeroDivisionError
    if len(a) < len(b):
        return [F(0)], trim(a)
    q = [F(0)] * (len(a) - len(b) + 1)
    r = list(a)
    while len(r) >= len(b) and trim(r) != [0]:
        d = len(r) - len(b)
        c = r[-1] / b[-1]
        q[d] = c
        for i in range(len(b)):
            r[d + i] -= c * b[i]
        trim(r)
        if len(r) < len(b):
            break
    return trim(q), trim(r)

def pgcd(a, b):
    a, b = trim(list(a)), trim(list(b))
    while b != [0]:
        _, r = pdivmod(a, b)
        a, b = b, r
    if a == [0]:
        return [F(0)]
    return pscale(a, 1 / a[-1])          # monic

# ---------------------------------------------------------------- Sturm
def sturm_chain(p):
    p = trim(list(p))
    chain = [p, pder(p)]
    while chain[-1] != [0]:
        _, r = pdivmod(chain[-2], chain[-1])
        if r == [0]:
            break
        chain.append(pscale(r, F(-1)))
    return [c for c in chain if c != [0]]

def sign_variations(chain, x):
    signs = []
    for c in chain:
        v = peval(c, x)
        if v != 0:
            signs.append(1 if v > 0 else -1)
    return sum(1 for i in range(len(signs) - 1) if signs[i] != signs[i + 1])

def cauchy_bound(p):
    """All real roots satisfy |x| < 1 + max|a_i/a_n|."""
    p = trim(list(p))
    if len(p) == 1:
        return F(1)
    lead = abs(p[-1])
    m = max(abs(c) / lead for c in p[:-1])
    return F(1) + m

def roots_in_half_line(p, A):
    """Number of distinct real roots of p in [A, +inf).  Requires p(A) != 0."""
    p = trim(list(p))
    if len(p) == 1:
        return 0
    if peval(p, A) == 0:
        raise ValueError("endpoint is a root; check the value before counting")
    B = cauchy_bound(p)
    if B <= A:
        return 0
    chain = sturm_chain(p)
    return sign_variations(chain, A) - sign_variations(chain, B)

# ---------------------------------------------------------------- Laguerre
def laguerre_polys(K):
    """ell_k(t) = L_k^(1/2)(t) as exact rational polynomial lists, k = 0..K."""
    out = [[F(1)]]
    if K == 0:
        return out
    alpha = F(1, 2)
    out.append([F(1) + alpha, F(-1)])                 # L_1 = 1 + alpha - t
    for k in range(1, K):
        # (k+1) L_{k+1} = (2k+1+alpha-t) L_k - (k+alpha) L_{k-1}
        A = padd(pscale(out[k], F(2 * k + 1) + alpha), [F(0), F(-1)])
        A = padd(A, [F(0)] * len(out[k]))
        # multiply (… - t) * L_k : build explicitly
        tLk = [F(0)] + out[k]
        A = padd(pscale(out[k], F(2 * k + 1) + alpha), pscale(tLk, F(-1)))
        B = pscale(out[k - 1], -(F(k) + alpha))
        nxt = pscale(padd(A, B), F(1, k + 1))
        out.append(nxt)
    return out

def build_pq(c):
    """c rationals in the Laguerre basis -> (p, q) exact polynomials."""
    ell = laguerre_polys(len(c) - 1)
    p = [F(0)]; q = [F(0)]
    for k, ck in enumerate(c):
        p = padd(p, pscale(ell[k], F(ck)))
        q = padd(q, pscale(ell[k], F(ck) * (F(-1) ** k)))
    return p, q

# ---------------------------------------------------------------- certification
PI_LO = F(314159265358979323846264338327, 10 ** 29)      # < pi
PI_HI = F(314159265358979323846264338329, 10 ** 29)      # > pi

def certify(c, verbose=True):
    """Exact check of the two sign conditions plus the resulting bound."""
    c = [F(x) for x in c]
    p, q = build_pq(c)
    A1 = 8 * PI_LO                       # < 8*pi  (safe direction)
    rec = {"degree": len(c) - 1, "c": [str(x) for x in c],
           "p": [str(x) for x in p], "q": [str(x) for x in q],
           "endpoint_A1": str(A1), "ok": False}
    # (A1)  p < 0 on [A1, inf)
    pA = peval(p, A1)
    if pA >= 0:
        rec["reason"] = "p(A1) >= 0: %s" % pA
        if verbose: print("  FAIL A1: p(A1) =", float(pA), ">= 0")
        return rec
    n11 = roots_in_half_line(p, A1)
    if n11 != 0:
        rec["reason"] = "p has %d real root(s) on [A1,inf)" % n11
        if verbose: print("  FAIL A1: p has", n11, "root(s) on the half-line")
        return rec
    # (A2)  q > 0 on [0, inf)
    q0 = peval(q, F(0))
    if q0 <= 0:
        rec["reason"] = "q(0) <= 0"
        if verbose: print("  FAIL A2: q(0) =", float(q0), "<= 0")
        return rec
    n2 = roots_in_half_line(q, F(0))
    if n2 != 0:
        rec["reason"] = "q has %d real root(s) on [0,inf)" % n2
        if verbose: print("  FAIL A2: q has", n2, "root(s) on the half-line")
        return rec
    p0 = peval(p, F(0))
    # Delta <= (4 pi/3) p0/q0 ; compare with pi/sqrt(18):  4 p0 / (3 q0) <= 1/sqrt18
    #    <=>  4 p0 sqrt18 <= 3 q0     (q0 > 0)
    lhs = 4 * p0 * (PI_LO * PI_LO * 18) ** 0            # placeholder, replaced below
    # exact comparison using rational bounds on sqrt(18)
    # sqrt18 in [s_lo, s_hi]; need 4 p0 s <= 3 q0 for s = sqrt18.
    # If p0 > 0 then LHS decreasing in s? no: increasing. So use s_hi for a safe upper test.
    s_lo = F(4242640687119285146, 10 ** 18)             # < sqrt(18) = 4.24264068711928514640...
    s_hi = F(4242640687119285147, 10 ** 18)             # > sqrt(18)
    rec.update({"p0": str(p0), "q0": str(q0),
                "ratio_f0_fhat0": str(p0 / q0),
                "delta_rational": "(4*pi/3)*%s" % (p0 / q0),
                "beats_kepler": bool(4 * p0 * s_hi <= 3 * q0) if p0 > 0 else False,
                "ok": True})
    if verbose:
        print("  PASS A1: p < 0 on [8*PI_LO, inf),  p(A1) = %.10f" % float(pA))
        print("  PASS A2: q > 0 on [0, inf),         q(0)   = %.10f" % float(q0))
        print("  f(0)/fhat(0) = p(0)/q(0) = %.12f" % float(p0 / q0))
        print("  certified: Delta <= (4*pi/3)*%.12f = %.12f"
              % (float(p0 / q0), float(p0 / q0) * 4 * 3.141592653589793 / 3))
        print("  beats Kepler pi/sqrt18? ", "yes" if rec["beats_kepler"] else "no (expected)")
    return rec

if __name__ == "__main__":
    import json, sys
    # smoke test: the trivial certificate p = -1, q = 1 is NOT in the basis, so
    # instead test the machinery on degree 0: c = (a0).  ell_0 = 1, so p = q = a0.
    print("Laguerre ell_0,ell_1,ell_2 as exact rationals:")
    for k, e in enumerate(laguerre_polys(2)):
        print("  L_%d^(1/2)(t) = " % k, [str(x) for x in e])
    print("\nsmoke test, c = (1,0):  p = q = 1  -> A1 fails (p(A1) > 0), as it must")
    certify([1, 0])
    print("\nsmoke test, c = (-1,0): p = q = -1 -> A2 fails, as it must")
    certify([-1, 0])

# ---------------------------------------------------------------- multiplicity
def yun_odd_part(p):
    """Return u, squarefree, with sign(p) == sign(u) away from roots.

    p = prod_i f_i^i (Yun's squarefree decomposition, f_i the part of multiplicity i).
    Then sign(p) = prod_{i odd} sign(f_i), so u := prod_{i odd} f_i is squarefree and
    carries the sign of p.  This is what lets us certify a certificate whose
    polynomial TOUCHES zero (even multiplicity) instead of rejecting it outright;
    the equality case forces such touching at a true optimum, so without this the
    strict-sign test is needlessly lossy.
    """
    p = trim(list(p))
    if len(p) <= 1:
        return p
    d = pder(p)
    a = pgcd(p, d)
    b, r = pdivmod(p, a)
    assert r == [0]
    c, r = pdivmod(d, a)
    assert r == [0]
    dd = padd(c, pscale(pder(b), F(-1)))
    out = [F(1)]
    i = 1
    while len(b) > 1:
        f = pgcd(b, dd)
        if i % 2 == 1:
            out = pmul(out, f)
        bn, r = pdivmod(b, f); assert r == [0]; b = bn
        cn, r = pdivmod(dd, f); assert r == [0]; c = cn
        dd = padd(c, pscale(pder(b), F(-1)))
        i += 1
    return trim(out)

def certify_relaxed(c, verbose=True):
    """Same as certify(), but allows the polynomials to touch zero (even multiplicity).
    Still exact: sign is decided by Sturm on the squarefree odd part."""
    c = [F(x) for x in c]
    p, q = build_pq(c)
    A1 = 8 * PI_LO
    rec = {"degree": len(c) - 1, "c": [str(x) for x in c],
           "p": [str(x) for x in p], "q": [str(x) for x in q],
           "endpoint_A1": str(A1), "mode": "relaxed (even multiplicity allowed)", "ok": False}
    if p == [0] or q == [0]:
        rec["reason"] = "identically zero"; return rec
    up = yun_odd_part(p)
    uq = yun_odd_part(q)
    for name, u, A, want in (("A1", up, A1, -1), ("A2", uq, F(0), +1)):
        if u == [0] or len(u) == 1:
            rec["reason"] = "%s: odd part constant" % name; return rec
        n = roots_in_half_line(u, A)
        if n != 0:
            rec["reason"] = "%s: %d simple root(s) of the odd part on the half-line" % (name, n)
            if verbose: print("  FAIL", name, ":", n, "root(s)"); return rec
        v = peval(u, A)
        if v == 0:
            rec["reason"] = "%s: odd part vanishes at the endpoint" % name; return rec
        if (v > 0) != (want > 0):
            rec["reason"] = "%s: wrong sign at the endpoint" % name
            if verbose: print("  FAIL", name, ": wrong sign at endpoint"); return rec
    p0, q0 = peval(p, F(0)), peval(q, F(0))
    if q0 <= 0:
        rec["reason"] = "q(0) <= 0"; return rec
    s_hi = F(4242640687119285147, 10 ** 18)          # > sqrt(18)
    rec.update({"p0": str(p0), "q0": str(q0), "ratio_f0_fhat0": str(p0 / q0),
                "beats_kepler": bool(4 * p0 * s_hi <= 3 * q0) if p0 > 0 else False, "ok": True})
    if verbose:
        print("  PASS A1/A2 via squarefree odd parts (roots counted exactly)")
        print("  f(0)/fhat(0) = %.12f   certified Delta <= %.12f"
              % (float(p0 / q0), float(p0 / q0) * 4 * 3.141592653589793 / 3))
    return rec
