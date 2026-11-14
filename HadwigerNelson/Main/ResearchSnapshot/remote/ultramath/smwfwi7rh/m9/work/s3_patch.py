"""s3_patch.py -- palette-field CSP on a hexagonal-lattice patch, k=6, CNF output.

The unit-distance graph of the triangular lattice L = Z e1 + Z e2 (|e1|=|e2|=1,
angle 60 deg) has edges exactly for differences in {+-e1,+-e2,+(e2-e1)}.
Palettes are indexed by the six ABSOLUTE lattice directions dir(k) = k*60 deg.

Node 0 is the centre x, a 5-cycle centre (C_5 on labels 0..4, colour i = 5).
Constraints (all from the paper):
  (P)   1 <= |P| <= 3                                    [Prop 5.6 transfer, m11]
  (5.7) P(n,k) cap P(n,k+1) = empty
  (MON) no disjoint (3,2) pair at (k, k+2)               [monochromatic unit sums]
  (C1)  no two complementary triples at one node
  (UNIT) for every unit pair (p,q) with difference direction d and every k not
         parallel to d:  P(p,k) cap P(q,k) = empty       [paper Remark 5.3 + 5.2(3)]
  (X)   at x: P not inside an edge of C_5, no singleton, ternary => next = [6]\\(P u {i})
  (SA)  each node has a colour c(n) in [6]; c(n) not in P(n,k) for all k;
        c(p) != c(q) for unit pairs; and c(y) in P(x, dir of y) for |y-x| = 1.

usage: python3 s3_patch.py R [--no-unit] [--no-colour] [--allpairs]  > patch.cnf
"""
import sys
from itertools import combinations

K = 6
I = 5
ELL = 5

def ball(R):
    pts = [(0, 0)]
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            if (i, j) != (0, 0) and abs(i) <= R and abs(j) <= R and abs(i + j) <= R:
                pts.append((i, j))
    return pts

def xy(i, j):
    # e1 = (1,0), e2 = (1/2, sqrt3/2) ; distances are exact in the triangular lattice
    return (i + j * 0.5, j * 0.8660254037844386467637)

NB = [((1, 0), 0), ((1, -1), 5), ((0, -1), 4), ((-1, 0), 3), ((-1, 1), 2), ((0, 1), 1)]
# difference -> absolute direction index ; e1 = dir 0, e2 = dir 1, e2-e1 = dir 2 ...
DIRS = {(1, 0): 0, (1, -1): 5, (0, -1): 4, (-1, 0): 3, (-1, 1): 2, (0, 1): 1}

class CNF:
    def __init__(self): self.cl = []; self.nv = 0
    def add(self, *xs): self.cl.append(list(xs))
    def atmost(self, xs, n):
        for c in combinations(xs, n + 1): self.add(*[-x for x in c])
    def atleast(self, xs, n):
        for c in combinations(xs, len(xs) - n + 1): self.add(*c)
    def imp(self, a, b): self.add(-a, b)

def build(R, unit=True, colour=True, allpairs=False):
    pts = ball(R)
    idx = {p: n for n, p in enumerate(pts)}
    N = len(pts)
    c = CNF()
    def z(n, k, l): return (n * 6 + k) * 6 + l + 1
    NZ = N * 6 * 6
    eq = {}
    base = NZ + N * 6 + 10
    def eqt(n, k, A):
        key = (n, k, frozenset(A))
        if key not in eq: eq[key] = base + len(eq) + 1
        return eq[key]
    for n in range(N):
        for k in range(6):
            for r in ((2,) if allpairs else (2, 3)):
                for A in combinations(range(K), r):
                    v = eqt(n, k, A)
                    for l in A: c.imp(v, z(n, k, l))
                    for l in range(K):
                        if l not in A: c.imp(v, -z(n, k, l))
                    c.add(*([-z(n, k, l) for l in A]
                            + [z(n, k, l) for l in range(K) if l not in A] + [v]))
    def col(n): return NZ + n * 6 + 1
    # sizes
    for n in range(N):
        for k in range(6):
            xs = [z(n, k, l) for l in range(K) if not (n == 0 and l == I)]
            c.add(*xs)
            c.atmost(xs, 3)
            if n == 0: c.add(-z(0, k, I))
    # (5.7)
    for n in range(N):
        for k in range(6):
            for l in range(K): c.add(-z(n, k, l), -z(n, (k + 1) % 6, l))
    # MON, C1
    for n in range(N):
        for k in range(6):
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
    # centre x
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
    # (UNIT)
    if unit:
        for (p, n) in idx.items():
            for (d, di) in DIRS.items():
                q = (p[0] + d[0], p[1] + d[1])
                if q not in idx: continue
                m = idx[q]
                for k in range(6):
                    if k in (di, (di + 3) % 6): continue
                    for l in range(K): c.add(-z(n, k, l), -z(m, k, l))
    # colours
    if colour:
        for n in range(N):
            xs = [col(n) + l for l in range(K)]
            c.add(*xs)
            for a in range(K):
                for b in range(a + 1, K): c.add(-(col(n) + a), -(col(n) + b))
            for k in range(6):
                for l in range(K): c.add(-(col(n) + l), -z(n, k, l))   # self-avoidance
        for (p, n) in idx.items():
            for (d, di) in DIRS.items():
                q = (p[0] + d[0], p[1] + d[1])
                if q not in idx: continue
                m = idx[q]
                for l in range(K): c.add(-(col(n) + l), -(col(m) + l))
        # trace: colour of a neighbour of x lies in P_x in that direction
        for (d, di) in DIRS.items():
            if d in idx:
                m = idx[d]
                for l in range(K): c.add(-(col(m) + l), z(0, di, l))
    mx = max(max(abs(x) for x in cl) for cl in c.cl)
    c.nv = max(mx, base + len(eq)) + 10
    return c

if __name__ == "__main__":
    R = int(sys.argv[1])
    kw = dict(unit="--no-unit" not in sys.argv,
              colour="--no-colour" not in sys.argv,
              allpairs="--allpairs" in sys.argv)
    c = build(R, **kw)
    sys.stdout.write(f"p cnf {c.nv} {len(c.cl)}\n")
    for cl in c.cl: sys.stdout.write(" ".join(map(str, cl)) + " 0\n")
