"""Second decision procedure for the tightened class: forward DP that COUNTS models.

Different algorithm from csp_vacuity.py (which backtracks).  Here the state is
(previous palette, set of ternary palettes used so far) and the DP accumulates the
number of prefixes; the first palette is fixed by an outer loop so that the cyclic
disjointness constraint can be checked at the end.  Counting, not just deciding,
makes the check sharp: the model counts per instance must agree with an independent
backtracking enumeration.

Class B  (tightened, (C1)-(C5)):  1 <= |P| <= k-3, P meets O_i and I_i, consecutive
and cyclic disjointness, no two ternary palettes disjoint (in Fin 6 two 3-sets are
complementary iff disjoint), and (C5) which follows from the previous two.
Class C  (binary): the same with |P| <= 2, where (C4) and (C5) are vacuous.
"""
from itertools import product
from csp_vacuity import sig_matrix, admissible, pc

K = 6


def count_models(adm, c4, rmax):
    """exact number of admissible 6-cycles, by forward DP over (prev, ternary-used)."""
    total = 0
    per_first = []
    for p0 in adm[0]:
        if pc(p0) > rmax:
            continue
        start = (p0, frozenset([p0]) if (c4 and pc(p0) == 3) else frozenset())
        dp = {start: 1}
        for i in range(1, 6):
            nd = {}
            for (prev, used), cnt in dp.items():
                for q in adm[i]:
                    if pc(q) > rmax or (prev & q):
                        continue
                    if c4 and pc(q) == 3:
                        if any(not (t & q) for t in used):
                            continue
                        nu = used | {q}
                    else:
                        nu = used
                    key = (q, nu)
                    nd[key] = nd.get(key, 0) + cnt
            dp = nd
            if not dp:
                break
        c = 0
        for (prev, used), cnt in dp.items():
            if prev & p0:
                continue
            c += cnt
        per_first.append((p0, c))
        total += c
    return total


def scan(l, k):
    sat = 0
    binary = 0
    same = 0
    modelsB = 0
    modelsC = 0
    for tail in product(range(6), repeat=l - 1):
        c = (0,) + tail
        adm = admissible(l, k, sig_matrix(l, c), k - 3)
        if any(not a for a in adm):
            continue
        nb = count_models(adm, True, k - 3)
        nc = count_models(adm, True, 2)
        if nb:
            sat += 1
        if nc:
            binary += 1
        if nb and nc:
            same += 1
        modelsB += nb
        modelsC += nc
    return sat, binary, modelsB, modelsC


if __name__ == "__main__":
    for k in (5, 6):
        for l in range(3, k + 1):
            sat, binary, mB, mC = scan(l, k)
            print(f"k={k} l={l}: instances with a (C1)-(C5) model = {sat}, "
                  f"with a binary model = {binary}; total models = {mB}, binary models = {mC}",
                  flush=True)
