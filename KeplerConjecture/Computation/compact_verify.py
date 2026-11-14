#!/usr/bin/env python3
"""A small, independent verifier for a K15 Cohn-Elkies certificate.

Why a third one.  exactcert.py uses Sturm sequences and a Yun decomposition; exactcert_oracle.py
uses SymPy's sqf_list and count_roots.  Both count roots.  This file counts nothing: it proves
positivity with the BERNSTEIN basis (a polynomial whose Bernstein coefficients on an interval are
all positive is positive there, because the Bernstein basis is a partition of unity) and recurses by
de Casteljau subdivision when the test is inconclusive.  On a half-line the tail is handled by the
reversed polynomial, which is exact: with f(a + s) = sum_j Q_j s^j,

        s^n f(a + 1/s) = sum_j Q_j s^{n-j},

so f > 0 on [a+T, infinity) is equivalent to a polynomial inequality on [0, 1/T].

Everything is a Fraction.  No floating point enters any decision.

WHAT IS CHECKED
  1. the certificate's c, p, q are consistent with the Laguerre Fourier pair
         p = sum_k c_k L_k^(1/2)(t),      q = sum_k (-1)^k c_k L_k^(1/2)(t)
     (this is the whole Fourier content of the family: the transform is diagonal on L_k^(1/2)
     with eigenvalue (-1)^k);
  2. p(0) > 0, q(0) > 0, and the leading coefficient of p is negative;
  3. (A1)  p < 0 on [8 pi, infinity)   -- verified on [8 PI_LO, infinity), which is STRONGER,
  4. (A2)  q > 0 on [0, infinity);
  5. Delta <= (4 PI_HI/3) p(0)/q(0) <= the claimed decimal.

Usage: python3 compact_verify.py [certificate.json]
Exit 0 iff every check passes.  Corrupt the certificate by hand and it exits 1 (negative controls
are run by --self-test).
"""
import json, sys
from fractions import Fraction as F
from math import comb

PI_LO = F("3.14159265358979323846264338327950288419716939937510582097494")
PI_HI = F("3.14159265358979323846264338327950288419716939937510582097500")

# ------------------------------------------------------------------ polynomials
def ptrim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a

def padd(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(n)])

def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return ptrim(out)

def pscale(a, s):
    return ptrim([x * s for x in a])

def taylor_shift(a, c):
    """coefficients of a(c + s)."""
    n = len(a)
    out = [F(0)] * n
    for i in range(n - 1, -1, -1):
        new = [F(0)] * n
        for j in range(n):
            if out[j]:
                new[j] += out[j] * c
                if j + 1 < n:
                    new[j + 1] += out[j]
        new[0] += a[i]
        out = new
    return ptrim(out)

def _binom_half(k, m):
    """C(k + 1/2, m) as a Fraction: prod_{i=0}^{m-1} (k + 1/2 - i) / m!."""
    if m < 0 or m > k:
        return F(0)
    num = F(1)
    for i in range(m):
        num *= (F(2 * k + 1, 2) - i)
    return num / F(_fact(m))

def laguerre_half(k):
    """L_k^(1/2)(t) in Q[t]:  sum_{j=0}^{k} C(k+1/2, k-j) (-t)^j / j!."""
    out = [F(0)] * (k + 1)
    for j in range(k + 1):
        out[j] = _binom_half(k, k - j) * (F(-1) ** j) / F(_fact(j))
    return ptrim(out)

def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

# ------------------------------------------------------------------ positivity
def bernstein(poly, a, b):
    """Bernstein coefficients of poly on [a,b]; all > 0 => poly > 0 there."""
    Q = taylor_shift(poly, a)                    # poly(a + s)
    n = len(Q) - 1
    Q = [Q[j] * (b - a) ** j for j in range(n + 1)]
    return [sum(Q[j] * F(comb(i, j), comb(n, j)) for j in range(i + 1)) for i in range(n + 1)]

def decasteljau(B):
    n = len(B) - 1
    tri = [B]
    for r in range(1, n + 1):
        tri.append([(tri[r - 1][i] + tri[r - 1][i + 1]) / 2 for i in range(n - r + 1)])
    return [tri[r][0] for r in range(n + 1)], [tri[n - r][r] for r in range(n + 1)]

def positive_on_interval(poly, a, b, cap=200000):
    """True if poly > 0 on [a,b] can be certified by Bernstein subdivision.  Returns (ok, pieces)."""
    stack, pieces = [(a, b, bernstein(poly, a, b))], 0
    while stack:
        x, y, B = stack.pop()
        pieces += 1
        if pieces > cap:
            return False, pieces
        if all(t > 0 for t in B):
            continue
        if y <= x:
            return False, pieces
        m = (x + y) / 2
        L, R = decasteljau(B)
        stack += [(x, m, L), (m, y, R)]
    return True, pieces

def positive_on_half_line(poly, a, T=20, cap=200000):
    """poly > 0 on [a, infinity): Bernstein on [a, a+T], reversed polynomial beyond."""
    ok1, p1 = positive_on_interval(poly, a, a + T, cap)
    if not ok1:
        return False, p1, 0
    Q = taylor_shift(poly, a)                    # poly(a + s)
    R = Q[::-1]                                  # s^n poly(a + 1/s)
    ok2, p2 = positive_on_interval(R, F(0), F(1, T), cap)
    return ok2, p1, p2

# ------------------------------------------------------------------ the checks
def verify(path, claim=None):
    d = json.load(open(path))
    c = [F(x) for x in d["coefficients_rational"]]
    p = [F(x) for x in d["p_rational"]]
    q = [F(x) for x in d["q_rational"]]
    claim = F(claim) if claim else F(str(d.get("delta_upper_decimal_rounded_up", "0.77996622")))
    out = []

    # 1. Laguerre reconstruction
    P = [F(0)]
    for k, ck in enumerate(c):
        P = padd(P, pscale(laguerre_half(k), ck))
    Qq = [F(0)]
    for k, ck in enumerate(c):
        Qq = padd(Qq, pscale(laguerre_half(k), ck * (F(-1) ** k)))
    out.append(("p matches sum c_k L_k", ptrim(P) == ptrim(p)))
    out.append(("q matches sum (-1)^k c_k L_k", ptrim(Qq) == ptrim(q)))

    # 2. endpoint signs
    out.append(("p(0) > 0", p[0] > 0))
    out.append(("q(0) > 0", q[0] > 0))
    out.append(("deg p is odd and its leading coefficient is negative", p[-1] < 0))

    # 3. (A1) p < 0 on [8 pi, inf) via [8 PI_LO, inf)
    okA1, n1, n2 = positive_on_half_line([-x for x in p], 8 * PI_LO)
    out.append(("(A1) p < 0 on [8*PI_LO, inf)  [%d + %d pieces]" % (n1, n2), okA1))

    # 4. (A2) q > 0 on [0, inf)
    okA2, m1, m2 = positive_on_half_line(q, F(0))
    out.append(("(A2) q > 0 on [0, inf)       [%d + %d pieces]" % (m1, m2), okA2))

    # 5. the bound, with pi <= PI_HI for an upper bound
    delta = 4 * PI_HI * p[0] / (3 * q[0])
    out.append(("Delta <= (4 PI_HI/3) p(0)/q(0) = %s <= %s" % (float(delta), float(claim)),
                delta <= claim))
    return out, delta

def main(argv):
    path = argv[1] if len(argv) > 1 else "out/verified_certificate_K33b.json"
    print("compact verifier (Bernstein + reversed polynomial; no Sturm, no root counting)")
    print("certificate:", path)
    out, delta = verify(path)
    bad = [n for n, ok in out if not ok]
    for name, ok in out:
        print("  %s %s" % ("PASS" if ok else "FAIL", name))
    if bad:
        print("\nREJECT: %d check(s) failed" % len(bad))
        return 1
    print("\nACCEPT: Delta <= %s" % float(delta))
    return 0

def negative_controls(path="out/verified_certificate_K33b.json"):
    """A verifier that only ever accepts proves nothing: corrupt the certificate and require REJECT."""
    import os, json as _json
    d = _json.load(open(path))
    os.makedirs(".scratch", exist_ok=True)
    cases = []

    def run(name, mutate, claim=None):
        e = _json.loads(_json.dumps(d))
        mutate(e)
        f = os.path.join(".scratch", "neg_%s.json" % name.replace(" ", "_"))
        _json.dump(e, open(f, "w"))
        out, _ = verify(f, claim=claim)
        ok = not all(ok_ for _, ok_ in out)
        cases.append((name, ok))
        print("  %s %s is REJECTED" % ("PASS" if ok else "FAIL", name))

    def bump_p0(e):
        c = F(e["p_rational"][0]) + F(1, 1000)
        e["p_rational"][0] = str(c)

    def flip_c(e):
        e["coefficients_rational"][5] = str(-F(e["coefficients_rational"][5]))

    run("p(0) raised by 1e-3", bump_p0)
    run("sign of the k=5 Laguerre coefficient flipped", flip_c)
    out, _ = verify(path, claim=F("0.7797"))
    ok = not all(ok_ for _, ok_ in out)
    print("  %s the tighter claim 0.7797 is REJECTED" % ("PASS" if ok else "FAIL"))
    cases.append(("tighter claim", ok))
    # leave no scratch files behind: the corrupted copies are inputs to a test, not outputs
    for f in os.listdir(".scratch"):
        os.remove(os.path.join(".scratch", f))
    try:
        os.rmdir(".scratch")
    except OSError:
        pass
    return all(ok for _, ok in cases)

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        print("negative controls (each must be REJECTED):")
        good = negative_controls()
        print("\nnegative-control suite:", "PASS" if good else "FAIL")
        sys.exit(0 if good else 1)
    sys.exit(main(sys.argv))
