#!/usr/bin/env python3
"""Check 3: (i) the hand-rolled basis arithmetic and sympy agree on all 21
squared pair distances; (ii) the paper's structural argument (two diamonds
sharing vertex 0) holds; (iii) P_G at k=6,7 from the closed form matches
brute force (independent degree check)."""

import sympy as sp
from itertools import product
from fractions import Fraction as F

# ---- hand-rolled basis arithmetic (same code as moser_exact.py) ----
def E(a=0, b=0, c=0, d=0):
    return (F(a), F(b), F(c), F(d))

ZERO, ONE = E(0), E(1)
def add(x, y): return tuple(x[i] + y[i] for i in range(4))
def sub(x, y): return tuple(x[i] - y[i] for i in range(4))
def neg(x): return tuple(-x[i] for i in range(4))
def mul(x, y):
    a1, b1, c1, d1 = x; a2, b2, c2, d2 = y
    return (a1*a2 + 3*b1*b2 + 11*c1*c2 + 33*d1*d2,
            a1*b2 + b1*a2 + 11*(c1*d2 + d1*c2),
            a1*c2 + c1*a2 + 3*(b1*d2 + d1*b2),
            a1*d2 + d1*a2 + b1*c2 + c1*b2)

R3, R11, R33 = E(0, 1), E(0, 0, 1), E(0, 0, 0, 1)
HALF, SIXTH = E(F(1, 2)), E(F(1, 6))

def cmul(z, w):
    (x1, y1), (x2, y2) = z, w
    return (sub(mul(x1, x2), mul(y1, y2)), add(mul(x1, y2), mul(y1, x2)))

u = (E(F(5, 6)), mul(SIXTH, R11))
P4 = {"0": (ZERO, ZERO),
      "A": (mul(HALF, R3), HALF),
      "B": (mul(HALF, R3), neg(HALF)),
      "T": (R3, ZERO)}
P4["uA"] = cmul(u, P4["A"]); P4["uB"] = cmul(u, P4["B"]); P4["uT"] = cmul(u, P4["T"])
names = ["0", "A", "B", "T", "uA", "uB", "uT"]

def sq4(z, w):
    dx, dy = sub(z[0], w[0]), sub(z[1], w[1])
    return add(mul(dx, dx), mul(dy, dy))

# ---- sympy version ----
s3, s11, I = sp.sqrt(3), sp.sqrt(11), sp.I
uu = (sp.Integer(5) + I*s11)/6
Ps = {"0": sp.Integer(0), "A": (s3+I)/2, "B": (s3-I)/2, "T": s3}
Ps["uA"] = sp.expand(uu*(s3+I)/2); Ps["uB"] = sp.expand(uu*(s3-I)/2); Ps["uT"] = sp.expand(uu*s3)

def sqs(z, w):
    d = sp.expand(z - w)
    x = sp.expand((d + sp.conjugate(d))/2); y = sp.expand((d - sp.conjugate(d))/(2*I))
    return sp.expand(x**2 + y**2)

edges = [("0","A"),("0","B"),("A","B"),("T","A"),("T","B"),("0","uA"),("0","uB"),
         ("uA","uB"),("uT","uA"),("uT","uB"),("T","uT")]
Eset = {frozenset(e) for e in edges}

print("=" * 70)
print("(i) all 21 squared pair distances: hand basis vs sympy")
ok = True
for a_i in range(7):
    for b_i in range(a_i+1, 7):
        n1, n2 = names[a_i], names[b_i]
        q = sq4(P4[n1], P4[n2])
        back = sp.expand(sp.simplify(sqs(Ps[n1], Ps[n2]) -
                (q[0] + q[1]*s3 + q[2]*s11 + q[3]*s3*s11)))
        agree = (sp.simplify(back) == 0)
        ok &= agree
        is_unit = (q == ONE)
        tag = "EDGE" if frozenset((n1, n2)) in Eset else "----"
        print(f"  {n1:>2s}-{n2:<3s} {tag}  |d|^2 = {q}  unit={is_unit}  agree={agree}")
print(f"  ALL 21 AGREE BETWEEN THE TWO ARITHMETICS: {ok}")

print()
print("=" * 70)
print("(ii) the paper's structural argument: two diamonds sharing vertex 0")
D1 = {"0", "A", "B", "T"}
D2 = {"0", "uA", "uB", "uT"}
for nm, D in (("D1 = {0,A,B,T}", D1), ("D2 = {0,uA,uB,uT}", D2)):
    ins = [e for e in edges if set(e) <= D]
    allp = [(x, y) for i, x in enumerate(sorted(D)) for y in sorted(D)[i+1:]]
    missing = [p for p in allp if frozenset(p) not in {frozenset(e) for e in ins}]
    print(f"  {nm}: {len(ins)} internal edges {ins}")
    print(f"      K4 minus edge {missing} -> {len(ins)==5 and len(missing)==1}")
print(f"  shared vertices of D1,D2: {D1 & D2}")
# in a proper 3-colouring of a diamond the two non-adjacent vertices have equal colour
idx = {n: i for i, n in enumerate(names)}
adj = [tuple(sorted((idx[a], idx[b]))) for a, b in edges]
for nm, pair in (("D1", ("0", "T")), ("D2", ("0", "uT"))):
    x, y = idx[pair[0]], idx[pair[1]]
    same = True
    for c in product(range(3), repeat=7):
        if all(c[i] != c[j] for i, j in adj):
            same &= (c[x] == c[y])
    print(f"  every proper 3-colouring of G forces colour({pair[0]}) = colour({pair[1]}): {same} (vacuous, G is not 3-colourable)")
# the forcing is real: check it on the maximal 3-colourable subgraphs (each diamond alone)
for nm, D in (("D1", D1), ("D2", D2)):
    di = {n: k for k, n in enumerate(sorted(D))}
    dn = sorted(D)
    de = [(di[a], di[b]) for a, b in edges if set((a, b)) <= D]
    x, y = di["0"], di["T"] if nm == "D1" else di["uT"]
    cnt = tot = 0
    for c in product(range(3), repeat=4):
        if all(c[i] != c[j] for i, j in de):
            tot += 1
            cnt += (c[x] == c[y])
    print(f"  {nm} alone: {tot} proper 3-colourings, all force the equality: {cnt == tot and tot > 0}")

print()
print("=" * 70)
print("(iii) closed form vs brute force at k = 6, 7")
k = sp.symbols('k')
Pg = k*(k-1)*(k-2)**2*(k-3)*(k**2-3*k+4)
def brute(kk):
    return sum(1 for c in product(range(kk), repeat=7) if all(c[i] != c[j] for i, j in adj))
for kk in (6, 7):
    b = brute(kk)
    print(f"  k={kk}: brute={b}  formula={int(Pg.subs(k, kk))}  equal={b == int(Pg.subs(k, kk))}")
