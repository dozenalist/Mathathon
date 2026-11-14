"""Two-cell (piecewise direction-invariant) palette CSP at k=6, six-cycle.

Model.  Two cells (types) 1,2 with direction words A_0..A_5, B_0..B_5 (sector k
= directions in [60k,60(k+1)) degrees, cyclically indexed).  Each value is an
admissible palette for C_6 at a six-cycle centre: size 2 or 3 and not contained
in any edge {i,i+1 mod 6}.  (5.7) at 60 degrees gives within-type disjointness
A_k & A_{k+1} = {}, B_k & B_{k+1} = {}, and the transport condition in the
degenerate limit of two centres in different cells at distance -> 0
(directions at +-60 degrees between the two cells) gives
A_k & B_{k+1} = {}, B_k & A_{k+1} = {}.

Question.  Which (range_1, range_2) pairs occur, where range_r = union_k value_k?
If every occurrence has range_1 = range_2 = [6], then no cell of a two-cell
field admits a free label.

Independent check: two_cell_csp_check.py (matrix-power enumeration of closed
walks + a CaDiCaL encoding of the same system).
"""
from itertools import combinations

K = 6
E = [frozenset((j, (j + 1) % K)) for j in range(K)]
VALS = []
for r in (2, 3):
    for c in combinations(range(K), r):
        S = frozenset(c)
        if not any(S <= e for e in E):
            VALS.append(S)
V = len(VALS)
ADJ = [[not (VALS[a] & VALS[b]) for b in range(V)] for a in range(V)]


def transitions():
    """nxt[a*V+b] = list of (a',b') allowed after (a,b)."""
    return [[(a2, b2) for a2 in range(V) for b2 in range(V)
             if ADJ[a][a2] and ADJ[b][b2] and ADJ[a][b2] and ADJ[b][a2]]
            for a in range(V) for b in range(V)]


def solve():
    """Depth-first search over (A_0,B_0,...,A_5,B_5) with wrap-around
    constraints; collect achievable (range_1, range_2) bitmasks."""
    out = set()
    nxt = transitions()
    for a0 in range(V):
        for b0 in range(V):
            stack = [(1, a0, b0, frozenset(VALS[a0]), frozenset(VALS[b0]))]
            while stack:
                k, a, b, r1, r2 = stack.pop()
                if k == 6:
                    if ADJ[a][a0] and ADJ[b][b0] and ADJ[a][b0] and ADJ[b][a0]:
                        out.add((sum(1 << i for i in r1), sum(1 << i for i in r2)))
                    continue
                for a2, b2 in nxt[a * V + b]:
                    stack.append((k + 1, a2, b2, r1 | VALS[a2], r2 | VALS[b2]))
    return out


if __name__ == "__main__":
    print("domain size", V)
    print("values:", [sorted(s) for s in VALS])
    res = solve()
    full = (1 << K) - 1
    print("achievable (range_1, range_2) pairs:", len(res))
    part = sorted({(r1, r2) for r1, r2 in res if r1 != full or r2 != full})
    print("with at least one range != [6]:", len(part))
    for r1, r2 in part[:60]:
        s1 = [i for i in range(K) if r1 >> i & 1]
        s2 = [i for i in range(K) if r2 >> i & 1]
        print("   U1", s1, "free1", [i for i in range(K) if not r1 >> i & 1],
              "| U2", s2, "free2", [i for i in range(K) if not r2 >> i & 1])
    print("ranges both full [6]:", (full, full) in res)
