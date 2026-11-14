#!/usr/bin/env python3
"""Where do two dodecahedral cells actually start to coexist?

C133 bounds the distance of two regular dodecahedral cells by 4cos rho_c = 3.1786179 downwards.
c133_attain.py shows that bound is not attained (at d = 4cos rho_c every relative placement has a
pair at 1.214).  This script estimates the TRUE threshold d* = min distance at which some relative
placement of two dodecahedral (inradius 1) cells is 2-separated.

Model: w = 0 with contacts 2 u_i; p = d e (e a face centre of w's icosahedron -- forced, since
p's contacts need v_j.e >= -d/4 for all j and the covering radius gives max_j(-v_j.e) >= cos rho_c);
p's contacts p + 2 v_j with v an icosahedron free in SO(3).  Objective: max over v of the minimum
pairwise distance among the 26 points {0, p, 2u_i, p+2v_j}.

Reported: the best minimum at each d, and the smallest d on the grid where it reaches 2.
This is a numerical estimate (Nelder-Mead over SO(3)), not a certificate; it bounds d* from ABOVE.
"""
import itertools
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation

PHI = (1 + 5 ** 0.5) / 2
COSRHO = ((1 + 2 / np.sqrt(5)) / 3) ** 0.5


def ico():
    v = []
    for a in (-1, 1):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(np.array(v, float), 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def face_centre(V):
    E = np.linalg.norm(V[:, None] - V[None], axis=2)
    edge = np.sort(E[0])[1]
    for i, j, k in itertools.combinations(range(12), 3):
        if abs(E[i, j] - edge) < 1e-9 and abs(E[i, k] - edge) < 1e-9 and abs(E[j, k] - edge) < 1e-9:
            w = V[i] + V[j] + V[k]
            return w / np.linalg.norm(w)
    raise RuntimeError


V = ico()
E = face_centre(V)


def best_min(d, nstart=60, seed=0):
    p = d * E
    rng = np.random.default_rng(seed)

    def score(x):
        R = Rotation.from_rotvec(x).as_matrix()
        Vr = V @ R.T
        pts = np.vstack([[np.zeros(3), p], 2 * V, p + 2 * Vr])
        dm = np.linalg.norm(pts[:, None] - pts[None], axis=2)
        np.fill_diagonal(dm, np.inf)
        return dm.min()

    best = -1.0
    for _ in range(nstart):
        x0 = rng.normal(scale=1.0, size=3)
        r = minimize(lambda x: -score(x), x0, method='Nelder-Mead',
                     options=dict(xatol=1e-10, fatol=1e-12, maxfev=4000))
        best = max(best, -r.fun)
    return best


def main():
    print(f"4cos rho_c = {4 * COSRHO:.9f}")
    print(f"{'d':>8} {'best min distance':>20}")
    rows = []
    for d in (3.18, 3.3, 3.5, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.5, 6.0):
        m = best_min(d)
        rows.append((d, m))
        print(f"{d:8.2f} {m:20.9f}")
    ok = [d for d, m in rows if m >= 2 - 1e-6]
    print()
    if ok:
        print(f"coexistence found from d = {min(ok):.2f} on the grid; the true threshold d* satisfies")
        lo = max([d for d, m in rows if m < 2 - 1e-6 and d < min(ok)], default=None)
        print(f"  {lo} < d* <= {min(ok)}   (the upper bound is numerical; the lower bound is only")
        print("   as good as the search, so it is not a certificate of non-existence)")
    else:
        print("no coexistence found up to d = 6; extend the grid")
    print("\nReading: C133's 3.1786 is a valid lower bound but far from the true threshold;")
    print("the gap is because at d = 4cos rho_c the contacts of p are forced into the face-centre")
    print("alignment, which puts them at 1.214 from w's contacts.  For C124's use (d <= 3) the")
    print("bound is more than enough, and no conclusion here changes any claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
