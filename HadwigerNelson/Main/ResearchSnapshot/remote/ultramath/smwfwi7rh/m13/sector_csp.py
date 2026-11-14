"""Sector palette CSP at k=6 with a globally free label (the centre's colour).

Model
-----
A translation-invariant palette field on the direction circle that is constant on
n = 6*m sectors of width Delta = 2*pi/(6m) = pi/(3m) is a cyclic word
u_0,...,u_{n-1} of subsets of [6] = {0,...,5}.  Sector j is the angular interval
[j*Delta,(j+1)*Delta).

Two kinds of constraints:

(5.7)  the sixty-degree exclusion: u_j cap u_{j+m} = empty for all j
       (R = rotation by pi/3 = m sectors).

(LOC)  the local transport of Lemma 5.2(3)/Remark 5.3 at distance d>0: the paper's
       (5.3) with centres z = x+a, |a| = d and the representation z+f = x+f+a gives
       P_z(f) cap P_x(s(f)) = empty for a.e. f, where s+t = f+a, |s|=|t|=1.  For a
       translation-invariant sector field this forces u_j cap u_{j+o} = empty for every
       offset o that a reachable direction s(f), f in sector j, can take.  The reach
       is computed in geometry.py; here the offset set is a parameter:
       O = {+-o : m-K <= o <= m+K}.

Free label: every palette avoids label 0 and has size 2 or 3, and is not equal to a
cycle edge of the 6-cycle 0-1-2-3-4-5-0 (Lemma 6.2 / (6.2)).  That leaves 16 values.

This file decides S(m,K) = "does a word of length 6m exist" exactly, by arc
consistency plus depth-first search.  sector_sat.py decides the same questions by a
one-hot SAT encoding, independently.
"""
from itertools import combinations
import sys

K_LABELS = 6
FREE = 0
EDGES = [frozenset(((j) % 6, (j + 1) % 6)) for j in range(6)]


def domain():
    vals = []
    for r in (2, 3):
        for c in combinations([x for x in range(K_LABELS) if x != FREE], r):
            S = frozenset(c)
            if any(S <= e for e in EDGES):
                continue
            vals.append(S)
    return vals


VALS = domain()
V = len(VALS)


def disjoint_table():
    D = [[not (VALS[a] & VALS[b]) for b in range(V)] for a in range(V)]
    return D


D = disjoint_table()


def offsets(m, K):
    """Constraint offsets for a word of length 6m: +-o for m-K <= o <= m+K."""
    o = set()
    for e in range(-K, K + 1):
        o.add((m + e) % (6 * m))
        o.add((-(m + e)) % (6 * m))
    return sorted(o)


def solve(n, offs, verbose=False):
    """Arc consistency + DFS.  Returns a witness word (list of frozensets) or None."""
    dom = [list(range(V)) for _ in range(n)]

    def revise(doms):
        changed = True
        while changed:
            changed = False
            for i in range(n):
                for o in offs:
                    j = (i + o) % n
                    if i == j:
                        return False          # a self-disjointness constraint
                    new = [a for a in doms[i] if any(D[a][b] for b in doms[j])]
                    if len(new) < len(doms[i]):
                        doms[i] = new
                        changed = True
                        if not new:
                            return False
        return True

    def rec(doms):
        if not revise(doms):
            return None
        i = min((k for k in range(n) if len(doms[k]) > 1), key=lambda k: len(doms[k]), default=None)
        if i is None:
            return [VALS[d[0]] for d in doms]
        for a in list(doms[i]):
            nd = [list(d) for d in doms]
            nd[i] = [a]
            r = rec(nd)
            if r is not None:
                return r
        return None

    return rec(dom)


def check_word(word, offs):
    n = len(word)
    for i in range(n):
        for o in offs:
            if word[i] & word[(i + o) % n]:
                return False
    return True


def Kmax(m, kmax_cap=None):
    """Largest K with S(m,K) satisfiable, and the witness; stops at the first UNSAT."""
    cap = m - 1 if kmax_cap is None else kmax_cap
    last = None
    for K in range(0, cap + 1):
        w = solve(6 * m, offsets(m, K))
        if w is None:
            return K - 1, last, K
        assert check_word(w, offsets(m, K))
        last = w
    return cap, last, None


if __name__ == "__main__":
    print("domain size:", V)
    print("values:", [sorted(v) for v in VALS])
    args = sys.argv[1:]
    if args and args[0] == "km":
        lo, hi = int(args[1]), int(args[2])
        for m in range(lo, hi + 1):
            k, w, firstbad = Kmax(m)
            print(f"m={m:3d} n={6*m:4d}  K_max={k:3d}  first_unsat={firstbad}")
            sys.stdout.flush()
    elif args and args[0] == "one":
        m, K = int(args[1]), int(args[2])
        w = solve(6 * m, offsets(m, K))
        print(f"m={m} K={K} offsets={offsets(m,K)}: {'SAT' if w else 'UNSAT'}")
        if w:
            print([sorted(x) for x in w])
    else:
        for m in (1, 2, 3, 4, 5, 6, 9, 12):
            for K in (0, 1, 2):
                w = solve(6 * m, offsets(m, K))
                print(f"m={m:2d} K={K}: {'SAT' if w else 'UNSAT'}")
