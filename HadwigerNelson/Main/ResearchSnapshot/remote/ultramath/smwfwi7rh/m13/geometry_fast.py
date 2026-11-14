"""Geometry of the transport (5.3) for a translation-invariant palette field.  Fast version.

Fix f = 1 (direction 0) and let the translation be a = d e^{i psi}.  Then r = f + a = 1 + d e^{i psi},
theta = arg r, rho = |r|, alpha = arccos(rho/2), and the two unit decompositions of r are
        s_pm = exp(i (theta +- alpha)) = (r/2)(1 +- i sqrt(4-rho^2)/rho),
which exist iff rho <= 2.  If f has angle phi and a has relative angle psi, then s has angle
        phi + dev(psi),     dev(psi) = theta(psi) + alpha(psi) - pi/3,
because the whole configuration rotates with f.  (The -pi/3 is the normalisation to the
direction R f.)  dev is odd up to conjugation: dev(-psi) = -dev(psi) (beta -> -beta conjugates r).

Hence the reachable s-set for f in sector j = [j*Delta,(j+1)*Delta) is exactly the interval
        [j*Delta - Sig(d), (j+1)*Delta + Sig(d)],     Sig(d) = max_psi dev(psi),
and a translation-invariant sector field (n = 6m sectors, Delta = pi/(3m)) must satisfy

        u_j cap u_{j+o} = empty  for all integers o with  |o - m| < 1 + Sig(d)/Delta,
        i.e.  K = ceil(3 m Sig(d)/pi)  in the notation of sector_csp.py.

d = 1 is the constant-endpoint case: psi = 0 gives rho = 2, alpha = 0, s = f (dev = -pi/3), so
Sig(1) >= pi/3 and the offset o = 0 enters: u_j cap u_j = empty.  No nonempty palette survives.
"""
import math
import mpmath as mp

mp.mp.dps = 30
PI = mp.pi
PI_F = math.pi


def _val_f(d, b):
    rho = math.sqrt(1 + 2 * d * math.cos(b) + d * d)
    if rho > 2:
        return None
    return math.atan2(d * math.sin(b), 1 + d * math.cos(b)) + math.acos(min(1.0, rho / 2))


def _dval_f(d, b):
    rho2 = 1 + 2 * d * math.cos(b) + d * d
    rho = math.sqrt(rho2)
    q = 4 - rho2
    if rho == 0 or q <= 0:
        return None
    re = 1 + d * math.cos(b)
    im = d * math.sin(b)
    return (d * math.cos(b) * re + d * math.sin(b) * im) / rho2 + d * math.sin(b) / (rho * math.sqrt(q))


def _val(d, b):
    rho = mp.sqrt(1 + 2 * d * mp.cos(b) + d * d)
    if rho > 2:
        return None
    return mp.atan2(d * mp.sin(b), 1 + d * mp.cos(b)) + mp.acos(rho / 2)


def _dval(d, b):
    rho2 = 1 + 2 * d * mp.cos(b) + d * d
    rho = mp.sqrt(rho2)
    q = 4 - rho2
    if rho == 0 or q <= 0:
        return None
    re = 1 + d * mp.cos(b)
    im = d * mp.sin(b)
    return (d * mp.cos(b) * re + d * mp.sin(b) * im) / rho2 + d * mp.sin(b) / (rho * mp.sqrt(q))


_CACHE = {}


def sigma(d):
    """Sig(d) = max_psi dev(psi), certified: returns (Sig, psi*, derivative at psi*)."""
    d = float(d)
    key = d
    if key in _CACHE:
        return _CACHE[key]
    N = 2000
    best, bb = None, 0.0
    for i in range(N + 1):
        b = 2 * PI_F * i / N
        v = _val_f(d, b)
        if v is not None and (best is None or v > best):
            best, bb = v, b
    step = 2 * PI_F / N
    lo, hi = bb - step, bb + step
    flo, fhi = _dval_f(d, lo), _dval_f(d, hi)
    if flo is None or fhi is None or not (flo > 0 > fhi):
        # fall back to a golden-section search
        gr = (math.sqrt(5) - 1) / 2
        c, e = hi - gr * (hi - lo), lo + gr * (hi - lo)
        fc, fe = _val_f(d, c), _val_f(d, e)
        for _ in range(200):
            if fc > fe:
                hi, e, fe = e, c, fc
                c = hi - gr * (hi - lo)
                fc = _val_f(d, c)
            else:
                lo, c, fc = c, e, fe
                e = lo + gr * (hi - lo)
                fe = _val_f(d, e)
        bstar = (lo + hi) / 2
    else:
        D = mp.mpf(d)
        lo_m, hi_m = mp.mpf(lo), mp.mpf(hi)
        for _ in range(120):
            mid = (lo_m + hi_m) / 2
            fm = _dval(D, mid)
            if fm > 0:
                lo_m = mid
            else:
                hi_m = mid
            if hi_m - lo_m < mp.mpf('1e-28'):
                break
        bstar = float((lo_m + hi_m) / 2)
    D = mp.mpf(d)
    out = (_val(D, mp.mpf(bstar)) - PI / 3, bstar, _dval(D, mp.mpf(bstar)))
    _CACHE[key] = out
    return out


def K(d, m):
    return int(mp.ceil(3 * m * sigma(d)[0] / PI))


def dcrit(m, lo=0.0, hi=1.5):
    """Largest d with K(d,m) <= floor(m/5)  (Sig increasing on [0,hi])."""
    target = PI * (m // 5) / (3 * m)
    dlo, dhi = mp.mpf(lo), mp.mpf(hi)
    for _ in range(80):
        mid = (dlo + dhi) / 2
        if sigma(mid)[0] <= target:
            dlo = mid
        else:
            dhi = mid
    return (dlo + dhi) / 2


if __name__ == "__main__":
    print(" d      Sig(d)                     3Sig/pi               psi*        dev'(psi*)")
    prev = None
    for d in (0.01, 0.05, 0.1, 0.1328, 0.14, 0.177, 0.2, 0.3, 0.5, 0.7, 0.73, 0.9, 1.0):
        s, b, dv = sigma(d)
        print(f"{d:5.4f}  {mp.nstr(s, 20):26s} {mp.nstr(3 * s / PI, 20):20s} {b:10.6f}  {mp.nstr(dv, 6)}")
        if prev is not None:
            assert prev < s, ("Sig not increasing", d)
        prev = s
    print()
    print("Sig(1) - pi/3 =", mp.nstr(sigma(1)[0] - PI / 3, 12))
    print()
    for m in (5, 10, 15, 20, 25, 30, 40, 50, 60, 120, 600):
        print(f"   m={m:4d}  d_crit={mp.nstr(dcrit(m), 12)}   (floor(m/5)={m//5})")
    target = PI / 15
    lo, hi = mp.mpf(0), mp.mpf(2)
    for _ in range(80):
        mid = (lo + hi) / 2
        if sigma(mid)[0] <= target:
            lo = mid
        else:
            hi = mid
    print()
    print("d* (Sig(d*) = pi/15) = " + mp.nstr((lo + hi) / 2, 20))
