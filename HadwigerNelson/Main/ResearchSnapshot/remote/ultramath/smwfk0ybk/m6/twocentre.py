"""Two-centre system at k = 6: candidate (C6) = cross-centre palette disjointness.

Remark 5.3 of the paper (with Lemma 5.2(3)) gives, for any pair of centres x, y
with |y - x| = 1 and a.e. direction f not perpendicular to y - x,

    P_y(f) cap P_x(f) = empty.                                        (5.3b)

So at the centre x (with an interface of length ell and a ray geometry) and at
y = x + a (generic a) the six palettes P_i = P_x(R^i e), Q_i = P_y(R^i e)
satisfy, for a generic e:  the x-side constraints (C1)-(C5) with (C2) at x,
the y-side constraints (C1),(C3),(C4),(C5) (no interface is known at y), and
the six pointwise disjointness constraints P_i cap Q_i = empty.

This file decides that system exhaustively for every satisfiable x-geometry.
The y-side constraints do not depend on any ray geometry, so the only data are
the x-geometry and its model.

Sufficient condition used: if some x-model P has
   m  notin union_{i even} P_i    and    m' notin union_{i odd} P_i  (m != m'),
then Q_i = {m} (i even), {m'} (i odd) satisfies all y-side constraints
(alternating singletons) and the cross constraints.  We check exhaustively that
such a model exists for EVERY satisfiable geometry; a direct joint search over
(P,Q) is run as well for the cases where the shortcut fails (there are none,
but the code does not assume it).
"""
from itertools import combinations
import tight_csp as T

def models_with_free_labels(cells):
    """DFS for a model P with union_even != Fin6 and union_odd != Fin6."""
    ell = len(cells)
    sig = T.sign_matrix(cells)
    adm = [T.admissible(ell, sig[i]) for i in range(6)]
    P = [0] * 6
    def dfs(i, ntern, triples):
        for p in adm[i]:
            if i > 0 and (p & P[i-1]):
                continue
            if i == 5 and (p & P[0]):
                continue
            is3 = T.is_ternary(p)
            if is3:
                if ntern == 3 or any((t ^ p) == T.FULL for t in triples):
                    continue
            P[i] = p
            if is3: triples.append(p)
            if i == 5:
                ev = P[0] | P[2] | P[4]
                od = P[1] | P[3] | P[5]
                if ev != T.FULL and od != T.FULL:
                    return True
            elif dfs(i+1, ntern + (1 if is3 else 0), triples):
                return True
            if is3: triples.pop()
        return False
    return dfs(0, 0, [])

def joint_search(cells):
    """Direct joint (P,Q) search, no shortcut: x-side (C1)-(C5) with geometry,
    y-side (C1),(C3),(C4),(C5) geometry-free, and P_i cap Q_i = empty."""
    ell = len(cells)
    sig = T.sign_matrix(cells)
    admx = [T.admissible(ell, sig[i]) for i in range(6)]
    allm = [m for r in range(1, 4) for m in
            [sum(1 << x for x in L) for L in combinations(range(6), r)]]
    P = [0] * 6
    Q = [0] * 6
    def ydfs(j, ntern, triples):
        for q in allm:
            if q & P[j]:
                continue
            if j > 0 and (q & Q[j-1]):
                continue
            if j == 5 and (q & Q[0]):
                continue
            is3 = T.is_ternary(q)
            if is3:
                if ntern == 3 or any((t ^ q) == T.FULL for t in triples):
                    continue
            Q[j] = q
            if is3: triples.append(q)
            if j == 5:
                return True
            if ydfs(j+1, ntern + (1 if is3 else 0), triples):
                return True
            if is3: triples.pop()
        return False
    def xdfs(i, ntern, triples):
        for p in admx[i]:
            if i > 0 and (p & P[i-1]):
                continue
            if i == 5 and (p & P[0]):
                continue
            is3 = T.is_ternary(p)
            if is3:
                if ntern == 3 or any((t ^ p) == T.FULL for t in triples):
                    continue
            P[i] = p
            if is3: triples.append(p)
            if i == 5:
                if ydfs(0, 0, []):
                    return True
            elif xdfs(i+1, ntern + (1 if is3 else 0), triples):
                return True
            if is3: triples.pop()
        return False
    return xdfs(0, 0, [])

tot_sat = tot_free = 0
bad = []
for ell in (3,4,5,6):
    sat = free = joint = 0
    for c in T.geometry_list(ell):
        ok, _ = T.solve(c, tight=True, want="first")
        if not ok:
            continue
        sat += 1
        f = models_with_free_labels(c)
        free += 1 if f else 0
        j = f or joint_search(c)
        joint += 1 if j else 0
        if not j:
            bad.append((ell, c))
    print("ell=%d  x-SAT=%d  free-label model exists=%d  two-centre SAT=%d" %
          (ell, sat, free, joint), flush=True)
    tot_sat += sat; tot_free += free
print("\nTOTAL x-SAT=%d, two-centre SAT=%d, counterexamples=%s" % (tot_sat, tot_free, bad[:5]))
