"""Decisive test: does one ray configuration have its WHOLE cell cycle satisfiable?

Facts (proved in proof.md).

(i)  sigma_j(e) = sign(e . v_j); each ray is positive on an open semicircle.
(ii) R^{p+3} e is the antipode of R^p e and an open semicircle contains exactly one
     of an antipodal pair, so  S_{p+3} = [ell] \\ S_p  ("antipodal law").
(iii) Writing q for the direction angle of e in units of pi, the six orbit positions
     are q + p/3 (p in Z/6), and ray j is positive at position p exactly when q + p/3
     lies in the semicircle centred at v_j, i.e. j in S_p iff p in P_j(q) where
         P_j(q) = { p in Z/6 : 3(q + p/3 - arg v_j / pi) in (-1/2,1/2) mod 2 }
     is, for a.e. q, a cyclic 3-interval of Z/6.
(iv) The map j -> P_j can be prescribed arbitrarily by choosing the rays, so the
     achievable sign tuples are exactly  S_p = { j : p in P_j }  over all choices of
     cyclic 3-interval P_j.
(v)  As q increases, one ray at a time changes its interval: P_j -> P_j + 1.  Ray j
     slips at the six phases q = arg v_j/pi + 1/2 - p/3, all in the class
     (arg v_j/pi + 1/2) mod 1/3, so two rays slip together exactly when
     arg v_i = arg v_j mod (pi/3).  Over q in [0,1/3) the slips occur in the cyclic
     order of the residues arg v_j mod (pi/3), and over q in [0,2pi) that pattern
     repeats six times, all rows advancing by one.

So a configuration is exactly (weak cyclic order of the six residues, the row
assignment in one cell), and the colouring exists iff some configuration has every
cell of its cycle satisfiable.
"""

from itertools import permutations
import decision
from rows import achievable

ELL, K, W2 = 6, 6, 3


def weak_linear_orders(n):
    """All weak linear orders of {0..n-1}: ordered set partitions."""
    out = []

    def rec(remaining, acc):
        if not remaining:
            out.append(tuple(acc))
            return
        # choose the first nonempty block
        m = len(remaining)
        for mask in range(1, 1 << m):
            block = tuple(remaining[i] for i in range(m) if mask >> i & 1)
            rest = tuple(remaining[i] for i in range(m) if not (mask >> i & 1))
            acc.append(block)
            rec(rest, acc)
            acc.pop()

    rec(tuple(range(n)), [])
    return out


def main(e=ELL, k=K, w2=W2, use_sa=True, verbose=True):
    dtab = {}
    rows = list(achievable(e))
    S_of = dict(rows)
    # satisfiability of every (label, row assignment)
    satmemo = {}
    sat_rows = {}

    def sat(choice, i):
        key = (choice, i)
        if key in satmemo:
            return satmemo[key]
        S = S_of[choice]
        ocs = tuple(decision.s8.allowed_sets(s, e, k) for s in S)
        if any(not oc[0] or not oc[1] for oc in ocs):
            satmemo[key] = False
            return False
        doms = [decision.domain(oc, e, k, w2, i, dtab) for oc in ocs]
        val = decision.solve(doms, k, i)
        satmemo[key] = val
        return val

    labels = list(range(k)) if use_sa else [None]
    for i in labels:
        for choice, _ in rows:
            if sat(choice, i):
                sat_rows.setdefault(i, []).append(choice)
    if verbose:
        print("SAT (label,row) pairs:", {i: len(v) for i, v in sat_rows.items()})

    orders = weak_linear_orders(e)
    if verbose:
        print("weak linear orders of the six slips:", len(orders))
    good = []
    for i, choices in sat_rows.items():
        for c0 in choices:
            for order in orders:
                cur = list(c0)
                ok = True
                for block in order:
                    for j in block:
                        cur[j] = (cur[j] + 1) % 6
                    if not sat(tuple(cur), i):
                        ok = False
                        break
                if ok:
                    # one period done; the second period is the same pattern
                    # with every row advanced by one, and the tuple set repeats,
                    # so check the six periods explicitly to be safe
                    cur0 = list(c0)
                    full_ok = True
                    for _ in range(6):
                        for block in order:
                            for j in block:
                                cur0[j] = (cur0[j] + 1) % 6
                            if not sat(tuple(cur0), i):
                                full_ok = False
                                break
                        if not full_ok:
                            break
                    if full_ok and cur0 == list(c0):
                        good.append((i, c0, order))
    if verbose:
        print("SURVIVING configurations (label, start cell, slip order):", len(good))
        for g in good[:3]:
            print("   ", g[0], g[1], [list(b) for b in g[2]])
    return sat_rows, good


if __name__ == '__main__':
    main()
