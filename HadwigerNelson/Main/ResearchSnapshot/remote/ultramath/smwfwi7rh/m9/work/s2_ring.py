"""s2_ring.py -- the unit wheel W_6 at a 5-cycle centre (k=6), decided by CNF + CaDiCaL.

(UNIT) [paper Remark 5.3 + Lemma 5.2(3)]: |u|=1, f not parallel to u  =>
        P_{x+u}(f) cap P_x(f) = empty.

Wheel:  x  (5-cycle centre; C_5 on labels 0..4; colour i = 5 = the outsider)
        y_j = x + w_j,  w_j = exp(i j pi/3),  j=0..5
unit pairs: spokes (x,y_j) direction w_j ;  rim (y_j,y_{j+1}) direction w_{j+2}.

Direct encoding z[i][k][l] = "label l belongs to the palette at node i, direction k".
node 6 = x, nodes 0..5 = y_j.  Auxiliary eq[i][k][A] = "palette at (i,k) is exactly A".

Ablations for the analysis:  --no-unit  --no-selfavoid  --no-mon  --no-colour
                             --allpairs-only   (sizes <= 2 everywhere)
"""
import sys
from itertools import combinations

K = 6
I = 5
ELL = 5
NV_Z = 7 * 6 * 6

def var(i, k, l): return (i * 6 + k) * 6 + l + 1
def cvar(j, l):   return NV_Z + j * 6 + l + 1

class CNF:
    def __init__(self): self.cl = []; self.nv = 0
    def add(self, *xs): self.cl.append(list(xs))
    def atmost(self, xs, n):
        for c in combinations(xs, n + 1): self.add(*[-x for x in c])
    def atleast(self, xs, n):
        for c in combinations(xs, len(xs) - n + 1): self.add(*c)
    def imp(self, a, b): self.add(-a, b)
    def write(self, fh):
        fh.write(f"p cnf {self.nv} {len(self.cl)}\n")
        for c in self.cl: fh.write(" ".join(map(str, c)) + " 0\n")

def build(unit=True, selfavoid=True, mon=True, colour=True, sizes_max=3):
    c = CNF()
    base = NV_Z + 6 * 6
    idx = {}
    def eqt(i, k, A):
        key = (i, k, frozenset(A))
        if key not in idx: idx[key] = base + len(idx) + 1
        return idx[key]
    nodes = range(7)
    for i in nodes:
        for k in range(6):
            for r in ((2, 3) if sizes_max >= 3 else (2,)):
                for A in combinations(range(K), r):
                    v = eqt(i, k, A)
                    for l in A: c.imp(v, var(i, k, l))
                    for l in range(K):
                        if l not in A: c.imp(v, -var(i, k, l))
                    c.add(*([-var(i, k, l) for l in A]
                            + [var(i, k, l) for l in range(K) if l not in A] + [v]))
    c.nv = base + len(idx) + 10
    for i in nodes:
        for k in range(6):
            xs = [var(i, k, l) for l in range(K) if not (i == 6 and l == I)]
            c.add(*xs)
            c.atmost(xs, 3)
            if sizes_max < 3: c.atmost(xs, 2)
    for k in range(6):
        for e in [(j, (j + 1) % ELL) for j in range(ELL)]:
            c.add(*[-var(6, k, j) for j in e])
        c.atleast([var(6, k, l) for l in range(K) if l != I], 2)
    for i in nodes:
        for k in range(6):
            for l in range(K):
                c.add(-var(i, k, l), -var(i, (k + 1) % 6, l))
    if mon:
        for i in nodes:
            for k in range(6):
                k2 = (k + 2) % 6
                for A in combinations(range(K), 3):
                    for B in combinations([l for l in range(K) if l not in A], 2):
                        c.add(-eqt(i, k, A), -eqt(i, k2, B))
                        c.add(-eqt(i, k, B), -eqt(i, k2, A))
    for i in nodes:
        for k1 in range(6):
            for k2 in range(k1 + 1, 6):
                for A in combinations(range(K), 3):
                    B = [l for l in range(K) if l not in A]
                    c.add(-eqt(i, k1, A), -eqt(i, k2, B))
                    c.add(-eqt(i, k1, B), -eqt(i, k2, A))
    for k in range(6):
        for A in combinations([l for l in range(K) if l != I], 3):
            B = [l for l in range(K) if l != I and l not in A]
            for l in B: c.add(-eqt(6, k, A), var(6, (k + 1) % 6, l))
            for l in range(K):
                if l not in B: c.add(-eqt(6, k, A), -var(6, (k + 1) % 6, l))
    if unit:
        UNITS = [(6, j, j) for j in range(6)] + [(j, (j + 1) % 6, (j + 2) % 6) for j in range(6)]
        for (p, q, d) in UNITS:
            for k in range(6):
                if k in (d, (d + 3) % 6): continue
                for l in range(K): c.add(-var(p, k, l), -var(q, k, l))
    if colour:
        for j in range(6):
            xs = [cvar(j, l) for l in range(K)]
            c.add(*xs)
            for a in range(K):
                for b in range(a + 1, K): c.add(-cvar(j, a), -cvar(j, b))
        for j in range(6):
            for l in range(K):
                c.imp(cvar(j, l), var(6, j, l))
                if selfavoid:
                    for k in range(6): c.imp(cvar(j, l), -var(j, k, l))
                c.add(-cvar(j, l), -cvar((j + 1) % 6, l))
    return c

if __name__ == "__main__":
    kw = dict(unit="--no-unit" not in sys.argv,
              selfavoid="--no-selfavoid" not in sys.argv,
              mon="--no-mon" not in sys.argv,
              colour="--no-colour" not in sys.argv)
    sizes = 2 if "--allpairs-only" in sys.argv else 3
    build(**kw, sizes_max=sizes).write(sys.stdout)
