"""s2_ring.py -- the unit wheel W_6 at a 5-cycle centre (k=6), decided by CNF + CaDiCaL.

(UNIT) [paper Remark 5.3 + Lemma 5.2(3)]: |u|=1, f not parallel to u  =>
        P_{x+u}(f) cap P_x(f) = empty.

Wheel:  x  (5-cycle centre; C_5 on labels 0..4; colour i = 5 = the outsider)
        y_j = x + w_j,  w_j = exp(i j pi/3),  j=0..5
unit pairs: spokes (x,y_j) direction w_j ;  rim (y_j,y_{j+1}) direction w_{j+2}.

Direct encoding z[i][k][l] = "label l belongs to the palette at node i, direction k".
node 6 = x, nodes 0..5 = y_j.

usage:  python3 s2_ring.py [--no-selfavoid] [--allpairs-only]  > ring.cnf
"""
import sys, itertools
from itertools import combinations

K = 6
I = 5
ELL = 5

def var(i, k, l):                       # 1..42*6
    return i * 36 + k * 6 + l + 1

class CNF:
    def __init__(self): self.cl = []; self.nv = 252 + 36 + 8
    def add(self, *xs): self.cl.append(list(xs))
    def atmost(self, xs, n):
        for c in combinations(xs, n + 1):
            self.add(*[-x for x in c])
    def atleast(self, xs, n):
        for c in combinations(xs, len(xs) - n + 1):
            self.add(*c)
    def imp(self, a, b): self.add(-a, b)
    def write(self, fh):
        fh.write(f"p cnf {self.nv} {len(self.cl)}\n")
        for c in self.cl: fh.write(" ".join(map(str, c)) + " 0\n")

def build(selfavoid=True, allpairs_only=False, subtypes=None):
    c = CNF()
    nodes = 7
    # ---- sizes ----
    for i in range(nodes):
        adm = (lambda l: l != I) if i == 6 else (lambda l: True)
        for k in range(6):
            xs = [var(i, k, l) for l in range(K) if adm(l)]
            c.add(*xs)                       # nonempty
            c.atmost(xs, 2 if allpairs_only else 3)
    # ---- x is a 5-cycle centre: palette not inside an edge of C_5, and not a singleton ----
    for k in range(6):
        for e in [(j, (j + 1) % ELL) for j in range(ELL)]:
            c.add(*[-var(6, k, j) for j in e])          # P not subset of edge
        # sinlgetons are impossible (Lemma 3 + V(C5)=Z5, self-avoidance kills {5})
        c.atleast([var(6, k, l) for l in range(K) if l != I], 2)
    # ---- (5.7) at every node: consecutive palettes disjoint ----
    for i in range(nodes):
        for k in range(6):
            for l in range(K):
                c.add(-var(i, k, l), -var(i, (k + 1) % 6, l))
    # ---- MON at every node: no disjoint (3,2) pair at distance 2 ----
    for i in range(nodes):
        for k in range(6):
            k2 = (k + 2) % 6
            for A in combinations(range(K), 3):
                for B in combinations([l for l in range(K) if l not in A], 2):
                    for (p, q) in ((A, B), (B, A)):
                        c.add(*([-var(i, k, l) for l in p] + [-var(i, k2, l) for l in q]))
    # ---- C1 at every node: no two complementary triples ----
    for i in range(nodes):
        for k1 in range(6):
            for k2 in range(k1 + 1, 6):
                for A in combinations(range(K), 3):
                    B = [l for l in range(K) if l not in A]
                    c.add(*([-var(i, k1, l) for l in A] + [-var(i, k2, l) for l in B]))
                    c.add(*([-var(i, k1, l) for l in B] + [-var(i, k2, l) for l in A]))
    # ---- Lemma A at x: ternary => next is the complementary pair ----
    for k in range(6):
        for A in combinations([l for l in range(K) if l != I], 3):
            B = [l for l in range(K) if l != I and l not in A]
            for a in A:
                for b in B:
                    c.add(-var(6, k, a), var(6, (k + 1) % 6, b))
    # ---- (UNIT) ----
    UNITS = [(6, j, j) for j in range(6)] + [(j, (j + 1) % 6, (j + 2) % 6) for j in range(6)]
    for (p, q, d) in UNITS:
        for k in range(6):
            if k in (d, (d + 3) % 6): continue
            for l in range(K):
                c.add(-var(p, k, l), -var(q, k, l))
    # ---- colours at the rim ----
    # colour variables: (20 + j)*6 + l
    def cvar(j, l): return 252 + j * 6 + l + 1
    for j in range(6):
        xs = [cvar(j, l) for l in range(K)]
        c.add(*xs)                                    # nonempty
        for a in range(K):
            for b in range(a + 1, K):
                c.add(-cvar(j, a), -cvar(j, b))       # at most one
    for j in range(6):
        for l in range(K):
            c.imp(cvar(j, l), var(6, j, l))           # c_j in X[j]
            if selfavoid:
                for k in range(6):
                    c.imp(cvar(j, l), -var(j, k, l))  # c_j not in any palette of y_j
        for l in range(K):
            c.add(-cvar(j, l), -cvar((j + 1) % 6, l)) # c_j != c_{j+1}
    return c

if __name__ == "__main__":
    sa = "--no-selfavoid" not in sys.argv
    ap = "--allpairs-only" in sys.argv
    c = build(sa, ap)
    c.write(sys.stdout)
