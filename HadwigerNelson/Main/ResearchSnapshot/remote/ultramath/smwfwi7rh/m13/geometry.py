"""Geometry of the transport (5.3) for a translation-invariant palette field.

Setup.  Paper's Lemma 5.2(3) with centres x and z = x + a:
        z + f = x + s + t,    |s| = |t| = 1,
hence P_z(f) cap P_x(s) = empty for a.e. f  (Remark 5.3: the second endpoint t may be
constant, f = +-a being the only exceptions).  Fix f = 1 (direction 0) and a = d e^{i b}.
With r = 1 + d e^{i b}, theta = arg r, rho = |r| <= 2, the two unit decompositions are
        s(b) = (r/2)(1 +- i sqrt(4-rho^2)/rho),   |s| = 1,
i.e. arg s = theta +- arccos(rho/2).

Let  Sig(d) = max_b [ arg s_+(b) ] - pi/3   (the -pi/3 normalises to the R-rotated
direction).  The reachable set of s for f ranging over one sector of width
Delta = pi/(3m) is the interval [j*Delta + pi/3 - Sig, (j+1)*Delta + pi/3 + Sig]
(the reach is symmetric, so both sides reach Sig).

A translation-invariant sector field of resolution n = 6m therefore satisfies, for every
translation length d that occurs,

        u_j cap u_{j+o} = empty  for every integer o with |o - m| < 1 + Sig(d)/Delta,

i.e. CSP S(m,K) with  K = ceil(3 m Sig(d)/pi).

d = 1 is the constant-endpoint case: b = 0 gives r = 1+d, theta = 0, alpha = 0, s = f,
so Sig(1) >= pi/3 and K >= m: offset 0 enters and the constraint is u_j cap u_j = empty.
"""
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi


def _val(d, b):
    rho = mp.sqrt(1 + 2 * d * mp.cos(b) + d * d)
    if rho > 2:
        return None
    return mp.atan2(d * mp.sin(b), 1 + d * mp.cos(b)) + mp.acos(rho / 2)


def _dval(d, b):
    """d/db of _val."""
    rho2 = 1 + 2 * d * mp.cos(b) + d * d
    rho = mp.sqrt(rho2)
    if rho > 2 or rho == 0:
        return None
    re = 1 + d * mp.cos(b)
    im = d * mp.sin(b)
    theta_dot = (d * mp.cos(b) * re + d * mp.sin(b) * im) / rho2   # Im(r'/r), r'=i d e^{ib}
    q = 4 - rho2
    if q <= 0:
        return None
    return theta_dot + d * mp.sin(b) / (rho * mp.sqrt(q))


def sigma(d, prec=30):
    """Sig(d) = max_b arg s_+ - pi/3, with the maximiser certified to prec digits."""
    d = mp.mpf(d)
    N = 3000
    best, bb = None, None
    for i in range(N + 1):
        b = 2 * PI * i / N
        v = _val(d, b)
        if v is not None and (best is None or v > best):
            best, bb = v, b
    # robust local refinement by golden-section search on the bracket
    step = 2 * PI / N
    lo, hi = bb - step, bb + step
    gr = (mp.sqrt(5) - 1) / 2
    c = hi - gr * (hi - lo)
    e = lo + gr * (hi - lo)
    fc, fe = _val(d, c), _val(d, e)
    tol = mp.mpf(10) ** (-prec - 10)
    while hi - lo > tol:
        if fc > fe:
            hi, e, fe = e, c, fc
            c = hi - gr * (hi - lo)
            fc = _val(d, c)
        else:
            lo, c, fc = c, e, fe
            e = lo + gr * (hi - lo)
            fe = _val(d, e)
    bstar = (lo + hi) / 2
    return _val(d, bstar) - PI / 3, bstar


def K(d, m):
    s, _ = sigma(d)
    return int(mp.ceil(3 * m * s / PI))


def dcrit(m):
    """Largest d with K(d,m) <= floor(m/5)."""
    target = PI * (m // 5) / (3 * m)
    lo, hi = mp.mpf(0), mp.mpf(2)
    for _ in range(120):
        mid = (lo + hi) / 2
        s, _ = sigma(mid)
        if s <= target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    print(" d      Sig(d)                     3Sig/pi               argmax")
    for d in (0.01, 0.05, 0.1, 0.1328, 0.14, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0):
        s, b = sigma(d)
        print(f"{d:5.4f}  {mp.nstr(s, 20):26s} {mp.nstr(3 * s / PI, 20):20s} {mp.nstr(b, 10)}")
    print()
    print("Sig(1) - pi/3 =", mp.nstr(sigma(1)[0] - PI / 3, 12))
    print()
    print(" d_crit(m):")
    for m in (5, 10, 15, 20, 25, 30, 40, 50, 60, 120, 600):
        print(f"   m={m:4d}  d_crit={mp.nstr(dcrit(m), 12)}")
    target = PI / 15
    lo, hi = mp.mpf(0), mp.mpf(2)
    for _ in range(120):
        mid = (lo + hi) / 2
        s, _ = sigma(mid)
        if s <= target:
            lo = mid
        else:
            hi = mid
    print()
    print("d* (Sig(d*) = pi/15) = " + mp.nstr((lo + hi) / 2, 20))
