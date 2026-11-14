#!/usr/bin/env python3
"""d7, part 4b: witnesses for the k-sensitivity table of the spindle windows."""
import itertools

EDGES = [(0, 1), (0, 2), (1, 2), (3, 1), (3, 2), (0, 4), (0, 5),
         (4, 5), (6, 4), (6, 5), (3, 6)]
n = 7
adj = [set() for _ in range(n)]
for a, b in EDGES:
    adj[a].add(b)
    adj[b].add(a)


def all_proper_colourings(k):
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


cols = {k: all_proper_colourings(k) for k in (4, 5, 6)}

print("=" * 78)
print("Selected windows: value of I_k and witnesses")
print("=" * 78)
for W in [(0, 1, 2, 3, 4, 5, 6), (0, 1, 2, 3, 6), (0, 1, 3, 6), (0, 1, 2, 6), (0, 6), (0, 3)]:
    vals = []
    wits = {}
    for k in (4, 5, 6):
        best = min(len({c[v] for v in W}) for c in cols[k])
        vals.append(best)
        cand = [c for c in cols[k] if len({c[v] for v in W}) == best]
        wits[k] = cand[0]
    print(f"W = {W}")
    print(f"   (I_4,I_5,I_6) = {tuple(vals)}")
    for k in (4, 5, 6):
        print(f"   witness at k={k}: c = {wits[k]}, colours on W = {sorted({wits[k][v] for v in W})}")
    print()

print("=" * 78)
print("All windows with I_4 != I_5, grouped by value tuple")
print("=" * 78)
groups = {}
for r in range(8):
    for W in itertools.combinations(range(7), r):
        v4 = min(len({c[v] for v in W}) for c in cols[4])
        v5 = min(len({c[v] for v in W}) for c in cols[5])
        v6 = min(len({c[v] for v in W}) for c in cols[6])
        groups.setdefault((v4, v5, v6), []).append(W)
for t, Ws in sorted(groups.items()):
    print(f"  (I_4,I_5,I_6) = {t}: {len(Ws)} windows", ("e.g. " + str(Ws[0])) if t[0] != t[1] else "")
print()
print("k = 5 -> 6: number of windows with I_5 != I_6:",
      sum(1 for t, Ws in groups.items() if t[1] != t[2] for _ in Ws))
print("changing windows of minimal size at k = 4 -> 5:",
      [W for W in groups.get((2, 1, 1), [])][:6], "and", [W for W in groups.get((3, 2, 2), [])][:6])
