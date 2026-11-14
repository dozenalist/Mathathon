"""Bisect the frozen threshold d_c: the unique root of M(d) = 3*delta_min(d).

M(d)      = sup of the positive endpoint shift over admissible branches,
delta_min(d) = inf of the positive endpoint shift over admissible branches.
Any centre-independent palette field with all palettes of size >= 2 that satisfies
(5.3) for every pair of centres at distance <= d0 must have d0 < d_c.
"""
import math
from frozen import shift, deriv

def extremes(d, N=6000):
    lo = hi = None
    for i in range(N):
        psi = -math.pi + 2*math.pi*i/N
        for sgn in (+1,-1):
            s = shift(d,psi,sgn); dv = deriv(d,psi,sgn)
            if s is None or dv is None or s <= 0 or abs(1+dv) < 1e-6:
                continue
            lo = s if lo is None else min(lo,s)
            hi = s if hi is None else max(hi,s)
    return lo,hi

def f(d, N=6000):
    lo,hi = extremes(d,N)
    return hi - 3*lo, lo, hi

if __name__ == "__main__":
    a,b = 0.44, 0.48
    for _ in range(40):
        m = (a+b)/2
        fm,lo,hi = f(m)
        if fm < 0: a = m
        else:      b = m
    d=(a+b)/2
    fm,lo,hi = f(d, 24000)
    print(f"d_c = {d:.8f}   delta_min={lo:.8f}  M={hi:.8f}  M-3*delta_min={fm:+.3e}")
    print(f"pi/3 = {math.pi/3:.8f}")
    print("\nvalues near the threshold (N=24000):")
    for dd in [0.44,0.45,0.46,0.46,0.4605,0.46075,0.461,0.47,0.5]:
        fm2,lo2,hi2 = f(dd,24000)
        print(f"  d={dd:.5f}  delta_min={lo2:.8f}  M={hi2:.8f}  M-3delta={fm2:+.8f}")
