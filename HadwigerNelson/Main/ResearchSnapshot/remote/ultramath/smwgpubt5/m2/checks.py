#!/usr/bin/env python3
"""Tiny exact finite certificates for the palette-block collapse (member m2, swarm smwgpubt5).

All checks are exhaustive over the stated finite universes. Runtime is well under 1 s each.
No floating point is used except the single exact-symbolic check at the end (sympy).
"""
from itertools import chain, combinations
from fractions import Fraction

def subsets(k):
    out = []
    for r in range(k + 1):
        for c in combinations(range(k), r):
            out.append(frozenset(c))
    return out

def complement_one(k, J, K):
    """the unique X with (forall i, i not in J|K <-> i = X), or None."""
    rest = [i for i in range(k) if i not in (J | K)]
    return rest[0] if len(rest) == 1 else None

# ---------------------------------------------------------------- check A
# The inner finset step (`key` / `forced_label_of_complement`).
#   hl : forall i, i notin J|K <-> i = X ; J <= q ; not p <= K ; Disjoint p q  ==>  X in p
def check_A(k):
    subs, n = subsets(k), 0
    for J in subs:
        for K in subs:
            X = complement_one(k, J, K)
            if X is None:
                continue
            for q in subs:
                if not J <= q:
                    continue
                for p in subs:
                    if p <= K or not p.isdisjoint(q):
                        continue
                    n += 1
                    assert X in p, ("FAIL A", k, J, K, X, p, q)
    return n

# ---------------------------------------------------------------- check B
# The full master `palette_block_ban`, brute force over abstract palettes.
#   hl1 hl2, J1<=Px1, J2<=Px2, not Py1<=K1, not Py2<=K2, Py1 disjoint Px1,
#   Py2 disjoint Px2   ==>   Py1 not disjoint Py2
def check_B(k):
    subs, n = subsets(k), 0
    triples = [(J, K, X) for J in subs for K in subs
               for X in [complement_one(k, J, K)] if X is not None]
    for (J1, K1, X1) in triples:
        for (J2, K2, X2) in triples:
            if X1 != X2:
                continue
            for Px1 in subs:
                if not J1 <= Px1:
                    continue
                for Px2 in subs:
                    if not J2 <= Px2:
                        continue
                    for Py1 in subs:
                        if Py1 <= K1 or not Py1.isdisjoint(Px1):
                            continue
                        for Py2 in subs:
                            if Py2 <= K2 or not Py2.isdisjoint(Px2):
                                continue
                            n += 1
                            assert not Py1.isdisjoint(Py2), \
                                ("FAIL B", k, (J1, K1, X1), (J2, K2, X2), Px1, Px2, Py1, Py2)
    return n

# ---------------------------------------------------------------- check C
# The five-label data used by `five_support_step_ban`, on Fin 5 = Z/5.
def fiveDiag(i):          # fiveDiag i = {i, i+2}   (Exclusion.lean:9)
    return frozenset({i, (i + 2) % 5})
def fiveAdj(i, j):        # fiveAdj i j = (i+1 = j or j+1 = i)  (Exclusion.lean:10)
    return (i + 1) % 5 == j or (j + 1) % 5 == i

def check_C():
    subs, n = subsets(5), 0
    for i in range(5):
        for j in range(5):
            if not fiveAdj(i, j):
                continue
            J, K = fiveDiag(i), fiveDiag(j)
            assert not (J & K), ("diag not disjoint", i, j)          # five_diag_disjoint
            X = complement_one(5, J, K)
            assert X is not None, ("no complement label", i, j)      # five_adj_four
            # second slot uses the SAME X (union is symmetric)
            assert complement_one(5, K, J) == X
            # and `five_forced_label` (Exclusion.lean:26) holds for every p
            for p in subs:
                if p.isdisjoint(J) and not p <= K:
                    n += 1
                    assert X in p, ("FAIL C", i, j, X, p)
    return n

# ---------------------------------------------------------------- check D
# direction_sixty_unit_real (FourTransport.lean:204), exactly with sympy.
def check_D():
    import sympy as sp
    a = sp.symbols('a', real=True)
    # (i) e^{ia} - e^{i(a+pi/3)} = e^{ia} (1 - e^{i pi/3})   exactly
    ident = sp.simplify(sp.expand(sp.exp(sp.I * a) - sp.exp(sp.I * (a + sp.pi / 3))
                                  - sp.exp(sp.I * a) * (1 - sp.exp(sp.I * sp.pi / 3))))
    # (ii) |1 - e^{i pi/3}|^2 = (1/2-1)^2 + (sqrt(3)/2)^2 = 1, exactly in Q(sqrt 3)
    z = sp.Rational(1, 2) - 1                       # Re(1 - e^{i pi/3})
    w = -sp.sqrt(3) / 2                             # Im(1 - e^{i pi/3})
    return ident, sp.simplify(z**2 + w**2)

if __name__ == "__main__":
    print("A(k=2,3,4,5) premise instances checked:", [check_A(k) for k in (2, 3, 4, 5)])
    print("B(k=2) full master instances checked:", check_B(2))
    print("B(k=3) full master instances checked:", check_B(3))
    print("C five-label instances checked:", check_C())
    print("D ||e^{ia}-e^{i(a+pi/3)}||^2 =", check_D())
