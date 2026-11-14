#!/usr/bin/env python3
"""Independent cross-check of moser_exact.py by DIFFERENT methods.

 (A) Geometry redone with sympy symbols sqrt(3), sqrt(11) and expand/simplify
     instead of the hand-rolled 4-tuple basis arithmetic.
 (B) Chromatic polynomial P_G(k) computed twice more, neither time by
     enumerating k^7 colourings:
       B1  from the falling-factorial expansion
             P(k) = sum_j a_j * (k)_j,  a_j = #partitions of V into j nonempty
             independent sets   (enumerate all 877 set partitions of 7 points)
       B2  by deletion-contraction with exact integer polynomials.
     Both are compared with the brute-force values 0,0,0,0,384,5040,31680,134400.
"""

import sympy as sp
from itertools import product
from fractions import Fraction as F

s3, s11 = sp.sqrt(3), sp.sqrt(11)
I = sp.I

# ------------------------------------------------------------------ (A)
u = (sp.Integer(5) + I * s11) / 6
pts = {
    "0": sp.Integer(0),
    "A": (s3 + I) / 2,
    "B": (s3 - I) / 2,
    "T": s3,
    "uA": sp.expand(u * (s3 + I) / 2),
    "uB": sp.expand(u * (s3 - I) / 2),
    "uT": sp.expand(u * s3),
}
names = ["0", "A", "B", "T", "uA", "uB", "uT"]
edges = [("0", "A"), ("0", "B"), ("A", "B"), ("T", "A"), ("T", "B"),
         ("0", "uA"), ("0", "uB"), ("uA", "uB"), ("uT", "uA"), ("uT", "uB"),
         ("T", "uT")]


def sq(z, w):
    d = sp.expand(z - w)
    # d is x + i y with x, y real algebraic; |d|^2 = expand(re^2+im^2)
    x = sp.expand((d + sp.conjugate(d)) / 2)
    y = sp.expand((d - sp.conjugate(d)) / (2 * I))
    return sp.expand(x**2 + y**2)


print("=" * 70)
print("(A) geometry with sympy root symbols")
okA = True
for a, b in edges:
    v = sp.simplify(sp.expand(sq(pts[a], pts[b]) - 1))
    okA &= (v == 0)
    print(f"  |{a:2s}-{b:2s}|^2 - 1 simplifies to {v}")
print(f"  11 edges unit: {okA}")

distinct = True
for i in range(7):
    for j in range(i + 1, 7):
        if sp.simplify(sp.expand(pts[names[i]] - pts[names[j]])) == 0:
            distinct = False
            print("  COLLISION", names[i], names[j])
print(f"  7 points pairwise distinct: {distinct}")
# independent check of distinctness: real parts and abs values
for n in names:
    print(f"    |{n}|^2 = {sp.simplify(sp.expand(sq(pts[n], sp.Integer(0))))}")
print(f"    pairwise distinct abs values: "
      f"{len({sp.simplify(sq(pts[n], sp.Integer(0))) for n in names})} distinct "
      f"of 7  (necessary, not sufficient)")

# ------------------------------------------------------------------ (B)
idx = {n: k for k, n in enumerate(names)}
E = [tuple(sorted((idx[a], idx[b]))) for a, b in edges]
assert len(set(E)) == 11


def brute(k):
    c = 0
    for col in product(range(k), repeat=7):
        if all(col[i] != col[j] for i, j in E):
            c += 1
    return c


def indep_sets():
    for mask in range(1 << 7):
        S = [v for v in range(7) if mask >> v & 1]
        if all(not (a in S and b in S) for a, b in E):
            yield mask


IND = list(indep_sets())


def set_partitions(collection):
    collection = list(collection)
    if not collection:
        yield []
        return
    first = collection[0]
    for rest in set_partitions(collection[1:]):
        for i in range(len(rest)):
            yield rest[:i] + [[first] + rest[i]] + rest[i + 1:]
        yield [[first]] + rest


def falling(k, j):
    r = 1
    for i in range(j):
        r *= (k - i)
    return r


print()
print("=" * 70)
print("(B1) chromatic polynomial via set partitions into independent sets")
counts = {}
np_ = 0
for part in set_partitions(list(range(7))):
    np_ += 1
    if all(any(sum(1 << v for v in block) == m for m in IND) for block in part):
        counts[len(part)] = counts.get(len(part), 0) + 1
print(f"  set partitions of 7 points enumerated: {np_} (Bell(7) = 877)")
print(f"  a_j = #{'j'} proper independent-set partitions: {dict(sorted(counts.items()))}")
poly = 0
k = sp.symbols('k')
for j, aj in counts.items():
    poly += aj * sp.prod([k - i for i in range(j)])
poly = sp.expand(poly)
print(f"  P_G(k) = {sp.factor(poly)}")
print(f"  expanded: {poly}")
bv = {kk: brute(kk) for kk in range(6)}
print(f"  brute force values P(0..5) = {[bv[i] for i in range(6)]}")
print(f"  set-partition values      = {[poly.subs(k, i) for i in range(6)]}")
print(f"  AGREE: {[bv[i] for i in range(6)] == [int(poly.subs(k, i)) for i in range(6)]}")
print(f"  P(3) = {poly.subs(k,3)}, P(4) = {poly.subs(k,4)}")

# ------------------------------------------------------------------ (B2)
print()
print("=" * 70)
print("(B2) chromatic polynomial by deletion-contraction (exact int polys)")
# NOTE: endpoints must be canonicalised (tuple(sorted(e))) before dedupe, not
# just the edge list.  Otherwise contracting one of two parallel edges leaves a
# twin that becomes a self-loop, and dropping self-loops instead of returning
# the zero polynomial gives a wrong P.  Canonicalising dedupes parallel edges,
# which is valid for the chromatic polynomial.
memo = {}


def chrom(verts, edgelist):
    verts = tuple(verts)
    edgelist = tuple(sorted({tuple(sorted(e)) for e in edgelist}))
    key = (tuple(sorted(verts)), edgelist)
    if key in memo:
        return memo[key]
    if not edgelist:
        res = sp.Poly(sp.expand(k**len(verts)), k)
    else:
        a, b = edgelist[0]
        rest = edgelist[1:]
        # deletion
        d = chrom(verts, rest)
        # contraction: merge b into a
        merged = [v for v in verts if v != b]
        contr = []
        for x, y in rest:
            x2 = a if x == b else x
            y2 = a if y == b else y
            if x2 != y2:
                contr.append((x2, y2))
        c = chrom(merged, contr)
        res = sp.Poly(sp.expand(d.as_expr() - c.as_expr()), k)
    memo[key] = res
    return res


pc = chrom(list(range(7)), E)
print(f"  deletion-contraction gives: {sp.factor(pc.as_expr())}")
print(f"  equals set-partition polynomial: {sp.expand(pc.as_expr() - poly) == 0}")

# ------------------------------------------------------------------ (C)
print()
print("=" * 70)
print("(C) 3-colourings of G-e : brute force vs set-partition count, all 11")
brute_all, part_all = {}, {}
for e in edges:
    ee = [x for x in E if x != tuple(sorted((idx[e[0]], idx[e[1]])))]
    c = 0
    for col in product(range(3), repeat=7):
        if all(col[i] != col[j] for i, j in ee):
            c += 1
    brute_all[e] = c
    # count partitions into exactly 3 nonempty independent sets w.r.t. ee
    cnt = 0
    for part in set_partitions(list(range(7))):
        if len(part) != 3:
            continue
        good = True
        for block in part:
            for x, y in ee:
                if x in block and y in block:
                    good = False
                    break
            if not good:
                break
        if good:
            cnt += 1
    part_all[e] = cnt * 6
print(f"  {'edge':>8s}  brute  partitions*6  agree")
allok = True
for e in edges:
    a = brute_all[e] == part_all[e]
    allok &= a
    print(f"  {e[0]:>2s}-{e[1]:<5s}  {brute_all[e]:5d}  {part_all[e]:11d}  {a}")
print(f"  ALL AGREE: {allok}")
print(f"  4-colourings of G: brute={brute(4)}, 24*a_4="
      f"{24*counts.get(4)} (a_4={counts.get(4)})")
