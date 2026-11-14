"""s6_residue_patch.py -- can the (3,2) residue be sustained on a hexagonal patch?

Same constraint set as s3_patch.py, plus for every node in a chosen set the requirement that
the six palettes at that node take EXACTLY TWO values, one of size 3 and one of size 2
(the (3,2) residue of Theorem 5 of REPORT.md).

usage: python3 s6_residue_patch.py R {centre|all}   > res.cnf
       python3 s6_residue_patch.py R none           (baseline, = s3_patch.py)
"""
import sys
from itertools import combinations

K = 6
I = 5
ELL = 5

def ball(R):
    out = [(0, 0)]
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            if (i, j) != (0, 0) and abs(i) <= R and abs(j) <= R and abs(i + j) <= R:
                out.append((i, j))
    return out

DIRS = {(1, 0): 0, (1, -1): 5, (0, -1): 4, (-1, 0): 3, (-1, 1): 2, (0, 1): 1}

class CNF:
    def __init__(self): self.cl = []; self.nv = 0
    def add(self, *xs): self.cl.append(list(xs))
    def atmost(self, xs, n):
        for c in combinations(xs, n + 1): self.add(*[-x for x in c])
    def atleast(self, xs, n):
        for c in combinations(xs, len(xs) - n + 1): self.add(*c)
    def imp(self, a, b): self.add(-a, b)

def build(R, mode="centre", unit=True, colour=True):
    pts = ball(R); idx = {p: n for n, p in enumerate(pts)}; N = len(pts)
    c = CNF()
    def z(n, k, l): return (n * 6 + k) * 6 + l + 1
    NZ = N * 36
    eq = {}
    base = NZ + N * 6 + 10
    def eqt(n, k, A):
        key = (n, k, frozenset(A))
        if key not in eq: eq[key] = base + len(eq) + 1
        return eq[key]
    for n in range(N):
        for k in range(6):
            for r in (2, 3):
                for A in combinations(range(K), r):
                    v = eqt(n, k, A)
                    for l in A: c.imp(v, z(n, k, l))
                    for l in range(K):
                        if l not in A: c.imp(v, -z(n, k, l))
                    c.add(*([-z(n, k, l) for l in A]
                            + [z(n, k, l) for l in range(K) if l not in A] + [v])
                          )
    def col(n): return NZ + n * 6 + 1
    for n in range(N):
        for k in range(6):
            xs = [z(n, k, l) for l in range(K) if not (n == 0 and l == I)]
            c.add(*xs); c.atmost(xs, 3)
            if n == 0: c.add(-z(0, k, I))
    for n in range(N):
        for k in range(6):
            for l in range(K): c.add(-z(n, k, l), -z(n, (k + 1) % 6, l))
            k2 = (k + 2) % 6
            for A in combinations(range(K), 3):
                for B in combinations([l for l in range(K) if l not in A], 2):
                    c.add(-eqt(n, k, A), -eqt(n, k2, B))
                    c.add(-eqt(n, k, B), -eqt(n, k2, A))
        for k1 in range(6):
            for k2 in range(k1 + 1, 6):
                for A in combinations(range(K), 3):
                    B = [l for l in range(K) if l not in A]
                    c.add(-eqt(n, k1, A), -eqt(n, k2, B))
                    c.add(-eqt(n, k1, B), -eqt(n, k2, A))
    # centre constraints
    for k in range(6):
        for e in [(j, (j + 1) % ELL) for j in range(ELL)]:
            out = [l for l in range(K) if l not in e]
            c.add(*([-z(0, k, l) for l in e] + [z(0, k, l) for l in out]))   # P not subset of the edge
        c.atleast([z(0, k, l) for l in range(K) if l != I], 2)
        for A in combinations([l for l in range(K) if l != I], 3):
            B = [l for l in range(K) if l != I and l not in A]
            for l in B: c.add(-eqt(0, k, A), z(0, (k + 1) % 6, l))
            for l in range(K):
                if l not in B: c.add(-eqt(0, k, A), -z(0, (k + 1) % 6, l))
    if unit:
        for (p, n) in idx.items():
            for (d, di) in DIRS.items():
                q = (p[0] + d[0], p[1] + d[1])
                if q not in idx: continue
                m = idx[q]
                for k in range(6):
                    if k in (di, (di + 3) % 6): continue
                    for l in range(K): c.add(-z(n, k, l), -z(m, k, l))
    if colour:
        for n in range(N):
            xs = [col(n) + l for l in range(K)]
            c.add(*xs)
            for a in range(K):
                for b in range(a + 1, K): c.add(-(col(n) + a), -(col(n) + b))
            for k in range(6):
                for l in range(K): c.add(-(col(n) + l), -z(n, k, l))
        for (p, n) in idx.items():
            for (d, di) in DIRS.items():
                q = (p[0] + d[0], p[1] + d[1])
                if q not in idx: continue
                m = idx[q]
                for l in range(K): c.add(-(col(n) + l), -(col(m) + l))
        for (d, di) in DIRS.items():
            if d in idx:
                m = idx[d]
                for l in range(K): c.add(-(col(m) + l), z(0, di, l))
    # ---- the (3,2) residue at the chosen nodes ----
    targets = range(N) if mode == "all" else ([0] if mode == "centre" else [])
    for n in targets:
        sel = []
        pairs = []
        for T in combinations(range(K), 3):
            for B in combinations([l for l in range(K) if l not in T], 2):
                pairs.append((T, B))
        sb = base + len(eq) + 10
        for pi_, (T, B) in enumerate(pairs):
            v = sb + n * 100 + pi_
            sel.append(v)
            for k in range(6):
                c.add(-v, eqt(n, k, T), eqt(n, k, B))          # value in {T,B}
            c.add(-v, *(eqt(n, k, T) for k in range(6)))       # T occurs
            c.add(-v, *(eqt(n, k, B) for k in range(6)))       # B occurs
        c.add(*sel)
    mx = max(max(abs(x) for x in cl) for cl in c.cl)
    c.nv = mx + 10
    return c

if __name__ == "__main__":
    R = int(sys.argv[1]); mode = sys.argv[2]
    import argparse
    c = build(R, mode, unit="--no-unit" not in sys.argv, colour="--no-colour" not in sys.argv)
    sys.stdout.write(f"p cnf {c.nv} {len(c.cl)}\n")
    for cl in c.cl: sys.stdout.write(" ".join(map(str, cl)) + " 0\n")
