"""Rigorous enclosures of pi, gamma = 2 arcsin(1/(2 sqrt3)), psi = pi + gamma (degrees).

Method: interval arithmetic (mpmath.iv, correct rounding) for the transcendental
evaluations; every boundary is converted to an exact dyadic rational (fractions.Fraction)
so that all later comparisons are exact rational comparisons.
gamma is obtained by bisection on cos(gamma) = 5/6 with gamma in (0, pi/2);
cos is strictly decreasing there, so the test is unambiguous.
No floating point enters any decision.
"""
from fractions import Fraction as F
from mpmath import iv

iv.dps = 60
K = 260                      # dyadic resolution of the bisection grid: x = n / 2^K

def _mpf_to_F(t):
    """exact Fraction of a raw mpf tuple (sign, man, exp, bc): value = (-1)^sign man 2^exp."""
    sign, man, exp, bc = t
    if man == 0:
        return F(0)
    v = F(int(man)) * (F(2) ** int(exp))
    return -v if sign else v

def _mpf_exact(num, den):
    """mpf for a rational num/2^K, exact in binary."""
    return iv.mpf(int(num)) / iv.mpf(int(den))

def _cos_iv(x_mpf):
    """rigorous (lo,hi) Fractions with lo <= cos(x) <= hi, x a point mpf."""
    c = iv.cos(x_mpf)
    lo, hi = c._mpi_
    return _mpf_to_F(lo), _mpf_to_F(hi)

# ---- pi ---------------------------------------------------------------------
_pi = iv.pi
_pl, _ph = _pi._mpi_
PI_LO, PI_HI = _mpf_to_F(_pl), _mpf_to_F(_ph)

# ---- gamma: cos(gamma) = 5/6, gamma in (0, pi/2) -----------------------------
_twoK = 2 ** K
_lo_n, _hi_n = 0, 2 * _twoK   # x from 0 to 2 (> pi/2)
_target = F(5, 6)
# stop well above the width of the iv.cos enclosure (dps=60 -> ~1e-60), and widen on a
# straddle instead of failing: 2**130 / 2**K = 2**-130 < 1e-39.
while _hi_n - _lo_n > 2 ** 130:
    _mid = (_lo_n + _hi_n) // 2
    _c_lo, _c_hi = _cos_iv(_mpf_exact(_mid, _twoK))
    if _c_lo > _target:
        _lo_n = _mid
    elif _c_hi < _target:
        _hi_n = _mid
    else:                                  # enclosure straddles 5/6: widen and stop
        _lo_n, _hi_n = _mid - 2 ** 100, _mid + 2 ** 100
        break

GAMMA_LO = F(_lo_n, _twoK)
GAMMA_HI = F(_hi_n, _twoK)

PSI_LO = (PI_LO + GAMMA_LO) * 180 / PI_HI
PSI_HI = (PI_HI + GAMMA_HI) * 180 / PI_LO
GAMMA_DEG_LO = GAMMA_LO * 180 / PI_HI
GAMMA_DEG_HI = GAMMA_HI * 180 / PI_LO

if __name__ == "__main__":
    fl = lambda q: float(q)
    print("pi width            : %.3e" % fl(PI_HI - PI_LO))
    print("gamma (rad)         : (%.22f, %.22f)" % (fl(GAMMA_LO), fl(GAMMA_HI)))
    print("gamma (deg)         : (%.22f, %.22f)  width %.2e"
          % (fl(GAMMA_DEG_LO), fl(GAMMA_DEG_HI), fl(GAMMA_DEG_HI - GAMMA_DEG_LO)))
    print("psi = pi+gamma (deg): (%.22f, %.22f)" % (fl(PSI_LO), fl(PSI_HI)))
    print("psi - 180 (deg)     : (%.22f, %.22f)" % (fl(PSI_LO - 180), fl(PSI_HI - 180)))
    print("2-2cos(gamma) == 1/3:", 2 - 2 * F(5, 6) == F(1, 3))
