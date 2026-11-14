"""Monotonicity check: is g2(d) = M(d) - 2 delta_min(d) positive for every d >= 0.3044,
and g3(d) = M(d) - 3 delta_min(d) positive for every d >= 0.4609 ?

delta_min is decreasing and M increasing in d (nesting of the shift sets), so g2, g3 are
increasing; this script checks both halves on a grid and records the worst cases.
"""
import math
from frozen import shift, deriv

def extremes(d, N=4000):
    lo = hi = None
    for i in range(N):
        psi = -math.pi + 2*math.pi*i/N
        for sgn in (+1,-1):
            s = shift(d,psi,sgn); dv = deriv(d,psi,sgn)
            if s is None or dv is None or s <= 0 or abs(1+dv) < 1e-6: continue
            lo = s if lo is None else min(lo,s); hi = s if hi is None else max(hi,s)
    return lo,hi

prev_lo = prev_hi = None
ok_mono = True
worst2 = (1e9, None); worst3 = (1e9, None)
grid = [0.3044 + i*(0.9999-0.3044)/220 for i in range(221)]
for d in grid:
    lo, hi = extremes(d)
    if prev_lo is not None and (lo > prev_lo + 1e-9 or hi < prev_hi - 1e-9):
        ok_mono = False
        print("monotonicity violated at d =", d, lo, prev_lo, hi, prev_hi)
    prev_lo, prev_hi = lo, hi
    g2 = hi - 2*lo
    if g2 < worst2[0]: worst2 = (g2, d)
    g3 = hi - 3*lo
    if d >= 0.4609 and g3 < worst3[0]: worst3 = (g3, d)
print("nesting (delta_min decreasing, M increasing) on the grid:", ok_mono)
print("min over d>=0.3044 of  M - 2 delta_min =", worst2)
print("min over d>=0.4609 of  M - 3 delta_min =", worst3)
