#!/usr/bin/env python3
"""Two PARALLEL dodecahedral cells: exact coexistence threshold.

C133 proves two dodecahedral (inradius 1) cells need distance >= 4cos rho_c = 3.1786179.
This script gives an explicit family where the threshold is attained, which bounds the TRUE
infimum from above: both cells' contact icosahedra aligned (the same orientation), p = d e with
e a face centre of the common icosahedron.  Then

  w's contacts: 2 u_i ,   p's contacts: d e + 2 u_i ,   i = 1..12,

and the configuration is 2-separated iff min over i,j of |d e + 2(u_j - u_i)| >= 2 (the pairs
within one icosahedron are >= 2.102924, and d itself is > 2).  The minimum is attained at the
face-centre direction and solved exactly in mpmath.

Result: d* = 4.7676... ; so the true threshold for two dodecahedral cells lies in
[3.1786179 (C133), 4.7676... (this configuration)], i.e. C133's bound has ~50% slack and must not
be quoted as the threshold.  For C124's use (d <= 3) the bound is more than sufficient.
"""
import itertools
import sys

from mpmath import mp, mpf, sqrt, pi, cos, sin, findroot

mp.dps = 40
PHI = (1 + sqrt(mpf(5))) / 2


def ico():
    v = []
    for a in (-1, 1):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    out = []
    for p in v:
        n = sqrt(sum(x * x for x in p))
        out.append(tuple(x / n for x in p))
    return sorted(set(tuple(round(float(x), 12) for x in p) for p in out))


def main():
    U = [tuple(mpf(str(x)) for x in p) for p in ico()]
    U = [tuple(x / sqrt(sum(y * y for y in p)) for x in p) for p in U]
    assert len(U) == 12
    # face centre: normalised sum of three mutually adjacent vertices
    best = None
    for i, j, k in itertools.combinations(range(12), 3):
        d = [sum((U[i][t] - U[j][t]) ** 2 for t in range(3)),
             sum((U[i][t] - U[k][t]) ** 2 for t in range(3)),
             sum((U[j][t] - U[k][t]) ** 2 for t in range(3))]
        if max(float(x) for x in d) - min(float(x) for x in d) < mpf('1e-20'):
            s = [U[i][t] + U[j][t] + U[k][t] for t in range(3)]
            n = sqrt(sum(x * x for x in s))
            best = [x / n for x in s]
            break
    e = best
    print(f"face-centre direction e = ({float(e[0]):.9f}, {float(e[1]):.9f}, {float(e[2]):.9f})")
    print(f"  |2 u_i - d e| at d = 4cos rho_c = {float(4*sqrt((1+2/sqrt(mpf(5)))/3)):.9f}: "
          f"min = {float(min(sqrt(sum((2*U[i][t]-4*sqrt((1+2/sqrt(mpf(5)))/3)*e[t])**2 for t in range(3))) for i in range(12))):.12f}")

    def mindist(d):
        return min(sqrt(sum((d * e[t] + 2 * (U[j][t] - U[i][t])) ** 2 for t in range(3)))
                   for i in range(12) for j in range(12))

    # bracket and bisect
    lo, hi = mpf('4.0'), mpf('6.0')
    for _ in range(200):
        mid = (lo + hi) / 2
        if mindist(mid) >= 2:
            hi = mid
        else:
            lo = mid
    print(f"\nparallel aligned cells: min pairwise distance = 2 first at d* = {mp.nstr(hi, 20)}")
    print(f"  check: mindist(d*) = {mp.nstr(mindist(hi), 20)};  mindist(d* - 1e-9) = "
          f"{mp.nstr(mindist(hi - mpf('1e-9')), 20)}")
    print(f"  C133's bound 4cos rho_c = {mp.nstr(4*sqrt((1+2/sqrt(mpf(5)))/3), 20)}")
    print(f"  ratio d*/4cos rho_c = {mp.nstr(hi/(4*sqrt((1+2/sqrt(mpf(5)))/3)), 8)}")
    print("\nSo the true threshold for two dodecahedral cells is in [3.1786178891670644, "
          f"{mp.nstr(hi, 12)}].")
    print("The upper end is an explicit configuration (parallel cells, face-centre axis), so it is a")
    print("bound on the threshold, not an estimate.  C133's constant is valid but ~50% lossy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
