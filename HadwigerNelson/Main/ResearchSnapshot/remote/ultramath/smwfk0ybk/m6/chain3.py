"""Candidate (C6) at one and two further centres, decided at k = 6.

Sound extra constraints from the paper's own machinery (Lemma 5.2(3) with
Remark 5.3: the representation (x+a)+f = x+f+a is admissible off f = +-a):

    P_y(f) cap P_x(f) = empty   for a.e. f,   whenever |y - x| = 1.      (5.3b)

`twocentre.py` decides the system with ONE further centre y = x + a,
`chain3.py` the chain x, x+a, x+2a (no constraint between x and x+2a: their
distance is 2).  At every centre the orbit constraints (C1),(C3),(C4),(C5) hold
(m6 Thms 1-2 are stated for every centre); (C2) is imposed only at x, where the
interface cycle lives.  The further centres' constraints do not depend on a ray
geometry.

Both systems turn out to be satisfiable for EVERY satisfiable x-geometry, i.e.
(C6) in this form is also inert at k = 6.
"""
from itertools import combinations
import tight_csp as T

ALLM = [sum(1 << x for x in L) for r in range(1, 4) for L in combinations(range(6), r)]

def centre_model(avoid):
    """One geometry-free centre: (C1),(C3),(C4),(C5) plus pointwise disjointness
    from every palette list in `avoid`.  Returns True iff such a model exists."""
    R = [0] * 6
    def dfs(i, ntern, triples):
        for q in ALLM:
            if any(q & F[i] for F in avoid):
                continue
            if i > 0 and (q & R[i-1]):
                continue
            if i == 5 and (q & R[0]):
                continue
            is3 = T.is_ternary(q)
            if is3:
                if ntern == 3 or any((t ^ q) == T.FULL for t in triples):
                    continue
            R[i] = q
            if is3: triples.append(q)
            if i == 5:
                return True
            if dfs(i+1, ntern + (1 if is3 else 0), triples):
                return True
            if is3: triples.pop()
        return False
    return dfs(0, 0, [])

def chain2(P):
    """exists Q with the y-constraints and Q perp P, and (for the chain) exists R
    with the z-constraints, R perp Q."""
    Q = [0] * 6
    def dq(i, n, tr):
        for q in ALLM:
            if q & P[i]: continue
            if i > 0 and (q & Q[i-1]): continue
            if i == 5 and (q & Q[0]): continue
            is3 = T.is_ternary(q)
            if is3:
                if n == 3 or any((t ^ q) == T.FULL for t in tr): continue
            Q[i] = q
            if is3: tr.append(q)
            if i == 5:
                if centre_model([Q]):
                    return True
            elif dq(i+1, n + (1 if is3 else 0), tr):
                return True
            if is3: tr.pop()
        return False
    return dq(0, 0, [])

def x_search(cells):
    """exists an x-model (C1)-(C5) for `cells` extending to the two-centre system"""
    ell = len(cells); sig = T.sign_matrix(cells)
    adm = [T.admissible(ell, sig[i]) for i in range(6)]
    P = [0] * 6
    def dfs(i, n, tr):
        for p in adm[i]:
            if i > 0 and (p & P[i-1]): continue
            if i == 5 and (p & P[0]): continue
            is3 = T.is_ternary(p)
            if is3:
                if n == 3 or any((t ^ p) == T.FULL for t in tr): continue
            P[i] = p
            if is3: tr.append(p)
            if i == 5:
                if chain2(P): return True
            elif dfs(i+1, n + (1 if is3 else 0), tr):
                return True
            if is3: tr.pop()
        return False
    return dfs(0, 0, [])

if __name__ == "__main__":
    for ell in (3, 4, 5, 6):
        sat = two = 0
        fails = []
        for c in T.geometry_list(ell):
            ok, _ = T.solve(c, tight=True, want="first")
            if not ok:
                continue
            sat += 1
            if x_search(c):
                two += 1
            else:
                fails.append(c)
        print("ell=%d  x-SAT=%d  SAT with two further centres (chain x, x+a, x+2a)=%d  "
              "failures=%s" % (ell, sat, two, fails[:4]), flush=True)
