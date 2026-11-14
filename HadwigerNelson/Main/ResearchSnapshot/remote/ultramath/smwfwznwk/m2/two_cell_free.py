"""Two-cell palette CSP at k=6: does a cell of a two-cell (piecewise
direction-invariant) field admit a free label?

Constraints (see two_cell_csp.py):
  A_k & A_{k+1} = {}, B_k & B_{k+1} = {}, A_k & B_{k+1} = {}, B_k & A_{k+1} = {}
for cyclically indexed 60-degree sectors k = 0..5, all values admissible for C_6
(size 2 or 3, not inside a cycle edge).  Search: does a solution exist with
0 not in range(A) (label 0 free in cell 1)?  With 0 free in both cells?  With
the free label of cell 1 different from the free label of cell 2?

WLOG free label of cell 1 is 0 (relabel by a symmetry of the six-cycle).
Enumeration: all cyclic A-words over the values avoiding 0 (16 of them), then a
cyclic DP for B; the B-candidates at position k are those disjoint from both
A_{k-1} and A_{k+1}.
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


def a_words(avoid):
    """all cyclic 6-tuples of values avoiding every label in `avoid`,
    adjacent-disjoint."""
    cand = [a for a in range(V) if not (VALS[a] & avoid)]
    out = []
    for a0 in cand:
        stack = [(1, a0, (a0,))]
        while stack:
            k, a, acc = stack.pop()
            if k == 6:
                if ADJ[a][a0]:
                    out.append(acc)
                continue
            for a2 in cand:
                if ADJ[a][a2]:
                    stack.append((k + 1, a2, acc + (a2,)))
    return out


def b_words(A):
    """all cyclic 6-tuples B with B_k & B_{k+1} = {} and B_k & A_{k+-1} = {}."""
    sets = []
    for k in range(6):
        forb = VALS[A[(k - 1) % 6]] | VALS[A[(k + 1) % 6]]
        sets.append([b for b in range(V) if not (VALS[b] & forb)])
    out = []
    for b0 in sets[0]:
        stack = [(1, b0, (b0,))]
        while stack:
            k, b, acc = stack.pop()
            if k == 6:
                if ADJ[b][b0]:
                    out.append(acc)
                continue
            for b2 in sets[k]:
                if ADJ[b][b2]:
                    stack.append((k + 1, b2, acc + (b2,)))
    return out


def ranges(word):
    u = set()
    for a in word:
        u |= VALS[a]
    return u


if __name__ == "__main__":
    print("domain size", V)
    AW = a_words(frozenset([0]))
    print("cyclic A-words avoiding label 0:", len(AW))
    found = []
    seen = set()
    for A in AW:
        for B in b_words(A):
            u1, u2 = ranges(A), ranges(B)
            key = (frozenset(u1), frozenset(u2))
            if key in seen:
                continue
            seen.add(key)
            found.append((u1, u2))
    print("distinct achievable (range(A), range(B)) with 0 not in range(A):", len(found))
    for u1, u2 in sorted(found, key=lambda t: (len(t[0]), len(t[1]), sorted(t[0]), sorted(t[1]))):
        print("   U1", sorted(u1), "free1", sorted(set(range(6)) - u1),
              "| U2", sorted(u2), "free2", sorted(set(range(6)) - u2))
