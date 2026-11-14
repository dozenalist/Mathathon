"""m4: library for the single-centre 6-cycle orbit system at k = 6."""
import itertools
from collections import defaultdict

K = 6

def pc(m):
    return bin(m).count('1')

def admissible_masklist(i):
    """Palettes at a typical 6-cycle centre (Lemma 3 + (6.2) + self-avoidance):
    nonempty subsets of the 5 labels != i, of size <= 3, not contained in a cycle edge."""
    others = [x for x in range(K) if x != i]
    edges = [(j, (j + 1) % K) for j in range(K)]
    out = []
    for r in range(1, 4):
        for c in itertools.combinations(others, r):
            P = sum(1 << x for x in c)
            if all(P & ~((1 << u) | (1 << v)) for u, v in edges):
                out.append(P)
    return out

def localok(a, b, FULL):
    """(E1) disjointness and (E2) ternary => both neighbours are the exact complement."""
    if a & b:
        return False
    if pc(a) == 3 and b != (FULL & ~a):
        return False
    if pc(b) == 3 and a != (FULL & ~b):
        return False
    return True

def words_DFS(i, need3=False):
    A = admissible_masklist(i)
    FULL = 63 ^ (1 << i)
    res = []
    def rec(p):
        if len(p) == 6:
            if not localok(p[5], p[0], FULL):
                return
            if need3 and len(set(p)) < 3:
                return
            res.append(tuple(p))
            return
        for b in A:
            if localok(p[-1], b, FULL):
                rec(p + [b])
    for a in A:
        rec([a])
    return A, res

def words_DP(i, need3=False):
    """Independent procedure: exact integer DP over (start, current, set-of-values-used)."""
    A = admissible_masklist(i)
    FULL = 63 ^ (1 << i)
    n = len(A)
    T = [[1 if localok(a, b, FULL) else 0 for b in A] for a in A]
    dp = defaultdict(int)
    for a in range(n):
        dp[(a, a, 1 << a)] += 1
    for _ in range(5):
        nd = defaultdict(int)
        for (s, c, u), cnt in dp.items():
            Tc = T[c]
            for b in range(n):
                if Tc[b]:
                    nd[(s, b, u | (1 << b))] += cnt
        dp = nd
    tot = 0
    for (s, c, u), cnt in dp.items():
        if T[c][s] and (not need3 or pc(u) >= 3):
            tot += cnt
    return A, tot
