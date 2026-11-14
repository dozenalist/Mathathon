"""Exact independence number of the circulant C_n(pm[m-K..m+K]), n = 6m, by MILP.

Why this decides the free-label sector CSP in a second, independent way.
Every palette has size >= 2 and is a subset of the five labels other than the free one.
For a word u (satisfying u_j cap u_{j+o} = empty for all offsets o in the connection set),
the set A_l = {j : l in u_j} is an independent set of the circulant for each of the five
labels l.  Summing,  sum_l |A_l| = sum_j |u_j| >= 2n = 12m.  Hence

        5 * alpha(C_n(O_K)) >= 12m      is NECESSARY for satisfiability.

So alpha < 12m/5 proves UNSAT.  (The converse is not needed.)

The graph C_n(O_K) is a circular-arc graph, so its maximum independent set is what the
MILP below computes exactly; scipy's HiGHS is exact for this 0-1 program.
"""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix


def alpha(m, K):
    n = 6 * m
    offs = sorted({(m + e) % n for e in range(-K, K + 1)} | {(-(m + e)) % n for e in range(-K, K + 1)})
    rows = []
    for j in range(n):
        for o in offs:
            j2 = (j + o) % n
            if j < j2:
                rows.append((j, j2))
    A = lil_matrix((len(rows), n))
    for r, (i, j) in enumerate(rows):
        A[r, i] = 1
        A[r, j] = 1
    res = milp(c=-np.ones(n), constraints=LinearConstraint(A.tocsr(), -np.inf, 1),
               integrality=np.ones(n), bounds=Bounds(0, 1))
    assert res.success, res.message
    return int(round(-res.fun))


if __name__ == "__main__":
    print(" m   K   alpha    3(m-K)   12m/5   verdict          (alpha < 12m/5 => UNSAT)")
    for m in range(4, 21):
        kk = m // 5
        for K in (max(1, kk - 1), kk, kk + 1, kk + 2):
            if K < 1 or K >= m:
                continue
            a = alpha(m, K)
            verdict = "UNSAT" if 5 * a < 12 * m else "necessary-cond-holds"
            print(f"{m:3d} {K:3d} {a:5d}  {3*(m-K):6d}  {12*m/5:7.1f}   {verdict}")
        print()
