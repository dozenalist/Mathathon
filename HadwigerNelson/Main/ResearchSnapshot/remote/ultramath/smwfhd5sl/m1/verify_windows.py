#!/usr/bin/env python3
"""d7, part 4: how does the window colour-count invariant
      I_k(S,W) = min { |c(W)| : c : S -> {1..k} proper }
depend on k?

Computed exhaustively for the 7-vertex Moser spindle (exact unit-distance graph
of lean/OAI/Geometry/PlaneColoring/Moser.lean) over all 128 windows W, for
k = 3,4,5,6.  I_k(S,W) = infinity when S is not k-colourable.
"""
import itertools

EDGES = [(0, 1), (0, 2), (1, 2), (3, 1), (3, 2), (0, 4), (0, 5),
         (4, 5), (6, 4), (6, 5), (3, 6)]
n = 7
adj = [set() for _ in range(n)]
for a, b in EDGES:
    adj[a].add(b)
    adj[b].add(a)


def all_proper_colourings(k):
    """all proper colourings S -> {0..k-1}, as tuples"""
    out = []
    col = [0] * n
    order = sorted(range(n), key=lambda v: -len(adj[v]))

    def rec(i):
        if i == n:
            out.append(tuple(col))
            return
        v = order[i]
        for c in range(k):
            if all(col[u] != c for u in adj[v]):
                col[v] = c
                rec(i + 1)
                col[v] = 0

    rec(0)
    return out


print("=" * 78)
print("window colour-count invariant I_k(spindle, W)")
print("=" * 78)
cols = {k: all_proper_colourings(k) for k in (3, 4, 5, 6)}
for k, v in cols.items():
    print(f"  number of proper {k}-colourings of the spindle: {len(v)}")

INF = float('inf')
table = {}
for r in range(0, 8):
    for W in itertools.combinations(range(7), r):
        vals = []
        for k in (3, 4, 5, 6):
            if not cols[k]:
                vals.append(INF)
            else:
                vals.append(min(len({c[v] for v in W}) for c in cols[k]))
        table[W] = tuple(vals)

changes = {("4->5"): [], ("5->6"): []}
for W, v in table.items():
    if v[1] != v[2]:
        changes["4->5"].append((W, v))
    if v[2] != v[3]:
        changes["5->6"].append((W, v))

print()
print("windows where I_4 != I_5:", len(changes["4->5"]))
for W, v in sorted(changes["4->5"])[:12]:
    print("   W =", W, " (I_3,I_4,I_5,I_6) =", v)
print()
print("windows where I_5 != I_6:", len(changes["5->6"]))
for W, v in sorted(changes["5->6"])[:12]:
    print("   W =", W, " (I_3,I_4,I_5,I_6) =", v)
print()
print("summary of the possible tuples (I_3,I_4,I_5,I_6):",
      sorted({v for v in table.values()}))
