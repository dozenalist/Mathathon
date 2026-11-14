"""d_frozen: the exact threshold for a frozen palette field at k=6.

A frozen field P (P_z == P) satisfies Lemma 5.2(3) at distance d only if
   P(u + delta) cap P(u) = empty  for a.e. u, for every delta in the shift set Sh(d).
Sh(d) contains the whole interval [delta_min(d), M(d)] (branch s_+, continuity).

If in addition (i) every palette has size >= 2 and (ii) one label is in no palette
("free label"), then no two shifts delta, 2*delta can both be effective: the three
palettes P(u), P(u+delta), P(u+2delta) would be pairwise disjoint, lie in the
5 labels left by the free one, and have total size >= 6.  So the shift set must
contain no pair {delta, 2 delta}: necessary condition M(d) < 2 delta_min(d).

d_frozen is the unique root of M(d) = 2 delta_min(d).
"""
import math
from frozen import shift, deriv

def extremes(d, N=8000):
    lo = hi = None
    for i in range(N):
        psi = -math.pi + 2*math.pi*i/N
        for sgn in (+1, -1):
            s = shift(d, psi, sgn); dv = deriv(d, psi, sgn)
            if s is None or dv is None or s <= 0 or abs(1+dv) < 1e-6:
                continue
            lo = s if lo is None else min(lo, s)
            hi = s if hi is None else max(hi, s)
    return lo, hi

def f(d, N=8000):
    lo, hi = extremes(d, N)
    return hi - 2*lo, lo, hi

if __name__ == "__main__":
    a, b = 0.25, 0.35
    for _ in range(45):
        m = (a+b)/2
        fm, _, _ = f(m)
        if fm < 0: a = m
        else:      b = m
    d = (a+b)/2
    fm, lo, hi = f(d, 40000)
    print(f"d_frozen = {d:.9f}")
    print(f"   delta_min = {lo:.9f}   M = {hi:.9f}   M - 2 delta_min = {fm:+.3e}")
    print(f"   (pi/9 = {math.pi/9:.9f}, pi/6 = {math.pi/6:.9f})")
    for dd in [0.29,0.30,0.3037,0.304,0.305,0.31,0.32]:
        fm2, lo2, hi2 = f(dd, 40000)
        print(f"   d={dd:.4f}  delta_min={lo2:.8f}  M={hi2:.8f}  M-2delta={fm2:+.8f}")
