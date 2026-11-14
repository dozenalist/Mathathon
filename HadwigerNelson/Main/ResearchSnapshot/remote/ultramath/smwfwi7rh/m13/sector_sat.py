"""Independent decision of the sector CSP S(m,K) by a one-hot SAT encoding (pysat/CaDiCaL).

This shares no code with sector_csp.py: the domain table is rebuilt from scratch, the
encoding is one-hot with pairwise exclusion clauses, and the search is CDCL rather than
DFS with arc consistency.  Variables x[j,v] mean "sector j carries palette values[v]".
Clauses:
  (1) for each j:  x[j,0] or ... or x[j,15]                      (each sector has a palette)
  (2) for each j, v<w:  not x[j,v] or not x[j,w]                 (only one palette per sector)
  (3) for each constraint (j,j+o) and each (v,w) with values[v] cap values[w] != empty:
        not x[j,v] or not x[(j+o)%n,w]
"""
from itertools import combinations
from pysat.solvers import Cadical153

K6 = 6
FREE = 0
EDGES = [frozenset((j % 6, (j + 1) % 6)) for j in range(6)]


def build_domain():
    vals = []
    for r in (2, 3):
        for c in combinations([x for x in range(K6) if x != FREE], r):
            S = frozenset(c)
            if any(S <= e for e in EDGES):
                continue
            vals.append(S)
    return vals


VALS = build_domain()
NV = len(VALS)


def offsets(m, K):
    n = 6 * m
    return sorted({(m + e) % n for e in range(-K, K + 1)} | {(-(m + e)) % n for e in range(-K, K + 1)})


def solve(m, K, want_model=False):
    n = 6 * m
    offs = offsets(m, K)
    if 0 in offs:
        return False, None
    def var(j, v):
        return j * NV + v + 1
    cls = []
    for j in range(n):
        cls.append([var(j, v) for v in range(NV)])
        for v in range(NV):
            for w in range(v + 1, NV):
                cls.append([-var(j, v), -var(j, w)])
    bad = [(v, w) for v in range(NV) for w in range(NV) if VALS[v] & VALS[w]]
    for j in range(n):
        for o in offs:
            j2 = (j + o) % n
            if j2 <= j:
                continue
            for v, w in bad:
                cls.append([-var(j, v), -var(j2, w)])
    with Cadical153(bootstrap_with=cls) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    if not sat:
        return False, None
    word = [None] * n
    if model:
        for j in range(n):
            for v in range(NV):
                if model[var(j, v) - 1] > 0:
                    word[j] = VALS[v]
    return True, word


def check(word, m, K):
    n = 6 * m
    for j in range(n):
        for o in offsets(m, K):
            if word[j] & word[(j + o) % n]:
                return False
    return True


if __name__ == "__main__":
    print("domain size", NV)
    for m in (1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 20, 25, 30):
        row = []
        for K in range(0, min(m, max(1, m // 5) + 2) + 1):
            sat, w = solve(m, K)
            if sat:
                assert check(w, m, K), (m, K)
            row.append((K, "S" if sat else "U"))
        kmax = max([k for k, s in row if s == "S"], default=None)
        print(f"m={m:3d}: " + " ".join(f"{k}{s}" for k, s in row) + f"   K_max={kmax} floor(m/5)={m//5}")
