"""Member m4. Independent decision of the single-centre R-orbit system at a typical
6-cycle centre, k=6, with the STRENGTHENED ternary rule.

  labels [6], centre colour i, palettes are subsets of [5] = [6]\{i};
  (E1) P_j cap P_{j+1} = empty                              (5.7), j mod 6
  (E2) |P_j| = 3  =>  P_{j-1} = P_{j+1} = [5] \ P_j          Lemma 2 + self-avoidance + |P|>=2
  (E3) P_j not contained in any edge of the 6-cycle          (6.2)
  (E4) i not in P_j                                          self-avoidance
  (F1) at least 3 distinct palette values                    m7/m16 2-valued bound
Two INDEPENDENT procedures: A = recursive DFS, B = exact DP over (start,current,value-set).
"""
import itertools
from collections import defaultdict

k = 6

def pc(m):
    return bin(m).count('1')

def admissible_masklist(i):
    others = [x for x in range(k) if x != i]
    edges = [(j, (j + 1) % k) for j in range(k)]
    out = []
    for r in range(1, 4):
        for c in itertools.combinations(others, r):
            P = sum(1 << x for x in c)
            if all(P & ~((1 << u) | (1 << v)) for u, v in edges):
                out.append(P)
    return out

def localok(a, b, FULL):
    if a & b:
        return False
    if pc(a) == 3 and b != (FULL & ~a):
        return False
    if pc(b) == 3 and a != (FULL & ~b):
        return False
    return True

def words_DFS(i, need3=True):
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

def words_DP(i, need3=True):
    A = admissible_masklist(i)
    n = len(A)
    FULL = 63 ^ (1 << i)
    T = [[1 if localok(a, b, FULL) else 0 for b in A] for a in A]
    dp = defaultdict(int)
    for a in range(n):
        dp[(a, a, 1 << a)] += 1
    for _ in range(5):
        nd = defaultdict(int)
        for (s, c, u), cnt in dp.items():
            for b in range(n):
                if T[c][b]:
                    nd[(s, b, u | (1 << b))] += cnt
        dp = nd
    tot = 0
    for (s, c, u), cnt in dp.items():
        if T[c][s] and (not need3 or pc(u) >= 3):
            tot += cnt
    return A, tot

for i in (0, 2):
    A, _ = words_DFS(i)
    w1 = len(words_DFS(i, need3=False)[1])
    w2 = len(words_DFS(i, need3=True)[1])
    b1 = words_DP(i, need3=False)[1]
    b2 = words_DP(i, need3=True)[1]
    print("i=%d: |admissible|=%d" % (i, len(A)))
    print("  (E1)+(E2)             : DFS=%d  DP=%d  agree=%s" % (w1, b1, w1 == b1))
    print("  (E1)+(E2)+(F1 >=3 val): DFS=%d  DP=%d  agree=%s" % (w2, b2, w2 == b2))
    # distribution of the number of distinct values
    ww = words_DFS(i, need3=False)[1]
    from collections import Counter
    print("  #distinct-value histogram (E1+E2 only):", dict(sorted(Counter(len(set(w)) for w in ww).items())))
