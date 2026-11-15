"""Research-desk independent re-implementation of the all-phase staircase census.

Same mathematical model as census.py (PAT signs, columns, R+/R-, palettes hitting both sides,
consecutive palettes disjoint cyclically), but different algorithms throughout:
  * SAT via boolean transfer matrices over ALL 63 nonempty palettes (cyclic trace), not reachability sets;
  * classes indexed by base-6 digits of (tau_1..tau_5) with tau_0 = 0 (own canonicalisation);
  * census by EXPLICIT enumeration of every ordered set partition of {0..5} (Fubini number 4683),
    taking the AND of 'alive' along each chain of partial unions, not a subset-sum DP.
"""
import itertools, time
import numpy as np

t0 = time.time()
PAT = [1, 1, -1, -1, -1, 1]

# ---- classes ----
def code(t):  # t: tuple of 6 residues; canonical index with t0 subtracted
    b = t[0]
    v = 0
    for x in t[1:]:
        v = v * 6 + (x - b) % 6
    return v

def decode(c):
    d = []
    for _ in range(5):
        d.append(c % 6); c //= 6
    return (0,) + tuple(reversed(d))

N = 6 ** 5
assert all(code(decode(c)) == c for c in range(N))

# ---- fixed-phase SAT via transfer matrices ----
PALS = np.arange(1, 64)
DISJ = (PALS[:, None] & PALS[None, :]) == 0          # 63 x 63

def sides(col):
    Rp = [v for v in range(6) if col[(v - 1) % 6] <= 0 and col[v] <= 0]
    Rn = [v for v in range(6) if col[(v - 1) % 6] >= 0 and col[v] >= 0]
    return sum(1 << v for v in Rp), sum(1 << v for v in Rn)

def sat(t):
    masks = []
    for j in range(6):
        col = [PAT[(j - t[i]) % 6] for i in range(6)]
        mp, mn = sides(col)
        masks.append(((PALS & mp) != 0) & ((PALS & mn) != 0))
    M = np.eye(63, dtype=bool) & masks[0][:, None]
    for j in range(1, 6):
        step = DISJ & masks[j][None, :]
        M = (M.astype(np.int32) @ step.astype(np.int32)) > 0
    # close the cycle: sum_q M[p0,q] * DISJ[q,p0] > 0 for some p0 (P_5 disjoint from P_0)
    return bool(np.any(np.diag(M.astype(np.int32) @ DISJ.astype(np.int32)) > 0))

SAT = np.array([sat(decode(c)) for c in range(N)], dtype=bool)
print('[sat] SAT =', int(SAT.sum()), 'UNSAT =', int(N - SAT.sum()))

# ---- alive[c, A] = class [tau - 1_A] is SAT ----
alive = np.zeros((N, 64), dtype=bool)
for c in range(N):
    t = decode(c)
    for A in range(64):
        alive[c, A] = SAT[code(tuple((t[i] - ((A >> i) & 1)) % 6 for i in range(6)))]

# ---- explicit ordered set partitions ----
def ordered_partitions(items):
    if not items:
        yield []
        return
    items = list(items)
    for r in range(1, len(items) + 1):
        for first in itertools.combinations(items, r):
            rest = [x for x in items if x not in first]
            for tail in ordered_partitions(rest):
                yield [first] + tail

parts = list(ordered_partitions(range(6)))
print('[partitions] ordered set partitions of {0..5}:', len(parts))
by_k = [0] * 7
for P in parts:
    acc = np.ones(N, dtype=bool)
    U = 0
    for block in P:
        U |= sum(1 << i for i in block)
        acc &= alive[:, U]
    by_k[len(P)] += int(acc.sum())
print('[census] surviving by k=1..6:', by_k[1:])
print('[census] total surviving =', sum(by_k[1:]), 'of', N * len(parts))
print(f'[time] {time.time() - t0:.1f}s')
