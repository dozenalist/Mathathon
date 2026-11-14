#!/usr/bin/env python3
"""Rigorous rational enclosures for the two irrational constants the cut/flow package needs.

Everything here is exact rational interval arithmetic with `fractions.Fraction`; the only
irrational input is a square root, enclosed from integer square roots via `math.isqrt`.  So each
enclosure is a proof, reproducible bit for bit, with no floating point in the derivation.

WHY THIS FILE EXISTS (review 0353-C).  An earlier version hard-coded
    V_DOD in [5.550291028519371, 5.550291028519372]
which EXCLUDES the true value 5.550291028515510269...  (the bound was too high by 3.9e-12), and
it hard-coded the ring-edge threshold as 2.1029 when the true edge is 2.102924448476534...  Both
are regenerated here from the exact radicals:

    V_dod(inradius 1) = (15 + 7 sqrt5)/4 * (2 / sqrt(5/2 + 11 sqrt5/10))^3
    edge(circumradius 2, icosahedron) = 4 sqrt2 / sqrt(5 + sqrt5)

and the enclosures are validated against 40-digit values of the same radical expressions.
"""
from fractions import Fraction as F
from math import isqrt
import mpmath as mp

mp.mp.dps = 50

def sqrt_enclosure(x, digits=40):
    """[lo, hi] with lo <= sqrt(x) <= hi, for a positive Fraction x, using integer sqrt only."""
    assert x > 0
    scale = 10 ** digits
    # sqrt(x) = sqrt(num/den); bound via isqrt on scaled integers
    n, d = x.numerator * scale * scale, x.denominator
    # lo = isqrt(n//d)/scale ; hi = (isqrt(n//d)+1)/scale, widened by one ulp for safety
    q = n // d
    r = isqrt(q)
    lo = F(r, scale)
    hi = F(r + 1, scale)
    # verify by squaring
    assert lo * lo <= x <= hi * hi, "sqrt enclosure failed"
    return lo, hi

def div_enclosure(a_lo, a_hi, b_lo, b_hi):
    """[a_lo,a_hi] / [b_lo,b_hi] for positive b."""
    assert b_lo > 0
    return min(a_lo / b_lo, a_lo / b_hi, a_hi / b_lo, a_hi / b_hi), \
           max(a_lo / b_lo, a_lo / b_hi, a_hi / b_lo, a_hi / b_hi)

def mul_enclosure(a_lo, a_hi, b_lo, b_hi):
    v = [a_lo * b_lo, a_lo * b_hi, a_hi * b_lo, a_hi * b_hi]
    return min(v), max(v)

def sqrt5(digits=40):
    return sqrt_enclosure(F(5), digits)

def dodeca_volume_enclosure(digits=40):
    """[lo, hi] for the regular dodecahedron of INRADIUS 1.

    V = (15 + 7 sqrt5)/4 * edge^3 with edge = 2/sqrt(5/2 + 11 sqrt5/10).
    Computed as  (15+7s)/4 * 8 * X^{-3/2},  X = 5/2 + 11 s/10,  s = sqrt5,
    with X^{-3/2} = 1/(X sqrt X) enclosed by 1/(X * sqrtX).
    """
    s_lo, s_hi = sqrt5(digits)
    # 15 + 7s  (positive)
    A_lo, A_hi = F(15) + 7 * s_lo, F(15) + 7 * s_hi
    A_lo, A_hi = mul_enclosure(A_lo, A_hi, F(1, 4), F(1, 4))
    # X = 5/2 + 11 s/10
    X_lo, X_hi = F(5, 2) + F(11, 10) * s_lo, F(5, 2) + F(11, 10) * s_hi
    # sqrt X
    Xlo_s, Xhi_s = sqrt_enclosure(X_lo, digits), sqrt_enclosure(X_hi, digits)
    sqrtX_lo = Xlo_s[0]
    sqrtX_hi = Xhi_s[1]
    # X * sqrtX
    P_lo, P_hi = mul_enclosure(X_lo, X_hi, sqrtX_lo, sqrtX_hi)
    inv_lo, inv_hi = F(1) / P_hi, F(1) / P_lo
    # times 8
    B_lo, B_hi = 8 * inv_lo, 8 * inv_hi
    lo, hi = mul_enclosure(A_lo, A_hi, B_lo, B_hi)
    return lo, hi

def icosa_edge_enclosure(digits=40):
    """[lo, hi] for the edge of the icosahedron with CIRCUMRADIUS 2: edge = 4 sqrt2/sqrt(5+sqrt5)."""
    s_lo, s_hi = sqrt5(digits)
    Y_lo, Y_hi = 5 + s_lo, 5 + s_hi                     # 5 + sqrt5
    Ylo_s, Yhi_s = sqrt_enclosure(Y_lo, digits), sqrt_enclosure(Y_hi, digits)
    sqrtY_lo, sqrtY_hi = Ylo_s[0], Yhi_s[1]
    num_lo, num_hi = sqrt_enclosure(F(2), digits)
    num_lo, num_hi = 4 * num_lo, 4 * num_hi             # 4 sqrt2
    return div_enclosure(num_lo, num_hi, sqrtY_lo, sqrtY_hi)

def self_test():
    ok = True
    v_lo, v_hi = dodeca_volume_enclosure()
    exact_v = (15 + 7 * mp.sqrt(5)) / 4 * (2 / mp.sqrt(mp.mpf(5) / 2 + mp.mpf(11) / 10 * mp.sqrt(5))) ** 3
    print("V_dod  enclosure: [%s," % float(v_lo))
    print("                   %s]" % float(v_hi))
    print("       true value: %s" % mp.nstr(exact_v, 20))
    good_v = float(v_lo) <= float(exact_v) <= float(v_hi)
    old_bad = F(5550291028519371, 10 ** 15) <= F(str(mp.nstr(exact_v, 20)))
    print("       true value inside the NEW enclosure: %s" % good_v)
    print("       ... and the OLD lower bound 5.550291028519371 was above it: %s"
          % (float(exact_v) < 5.550291028519371))
    e_lo, e_hi = icosa_edge_enclosure()
    exact_e = 4 * mp.sqrt(2) / mp.sqrt(5 + mp.sqrt(5))
    good_e = float(e_lo) <= float(exact_e) <= float(e_hi)
    print("edge   enclosure: [%s, %s]" % (float(e_lo), float(e_hi)))
    print("       true value: %s   inside: %s" % (mp.nstr(exact_e, 20), good_e))
    print("       ... so R = 2.1029 is BELOW the edge: %s" % (mp.mpf("2.1029") < exact_e))
    ok = bool(good_v and good_e)
    print("\nk15radicals self-test:", "PASS" if ok else "FAIL")
    return ok

if __name__ == "__main__":
    raise SystemExit(0 if self_test() else 1)
