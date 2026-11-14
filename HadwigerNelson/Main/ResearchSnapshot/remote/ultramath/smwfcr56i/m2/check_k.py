#!/usr/bin/env python3
"""k-dependence checks for the Hadwiger-Nelson palette / state machinery
(paper: "The Euclidean plane is not five-colorable", sections 5.4-8.4).

Every check is exact finite enumeration; no floating point.

C1  Section 6.3.1, four-cycle locus: palettes avoiding all cycle labels.
C2  Section 8.4 / Theorem B: external state alphabet at a cycle interface,
    size bound 1 <= |A| <= k-l-1, and the disjointness graph (paper (5.7)).
C3  Section 5.4 / Theorem A: growth of the palette alphabet with k.
C4  Section 8.2, five-cycle step arithmetic (k = 5), exhaustive.
C5  Section 6.3.3, five-cycle diagonals (k = 5).
C6  Small colouring certificates.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product


def labels(k):
    return tuple(range(k))


def nonempty_subsets(S, lo, hi):
    S = sorted(S)
    out = []
    for r in range(max(lo, 1), hi + 1):
        out.extend(frozenset(c) for c in combinations(S, r))
    return out


def cycle_edges(l):
    return [frozenset({i, (i + 1) % l}) for i in range(l)]


def inside_an_edge(P, l):
    return any(P <= e for e in cycle_edges(l))


# ------------------------------------------------------------------ C1
def c1_all(k, l, cap):
    """all admissible palettes at a centre in the l-cycle locus:
    1 <= |P| <= cap and P not contained in a cycle edge (paper (6.2))"""
    return [P for P in nonempty_subsets(labels(k), 1, cap)
            if not inside_an_edge(P, l)]


def c1(k, l, cap):
    """the subfamily whose palette is made of cycle labels only"""
    return [P for P in c1_all(k, l, cap) if P <= frozenset(range(l))]


# ------------------------------------------------------------------ C2
def external_alphabet(k, l):
    """A = P cap T^c with 1 <= |A| <= k-l-1  (Theorem B)"""
    return nonempty_subsets(set(labels(k)) - set(range(l)), 1, k - l - 1)


def disjoint_graph(S):
    adj = {a: set() for a in S}
    for a, b in combinations(S, 2):
        if not (a & b):
            adj[a].add(b)
            adj[b].add(a)
    return adj


def bipartite(adj):
    col = {}
    for s in adj:
        if s in col:
            continue
        col[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in col:
                    col[v] = 1 - col[u]
                    stack.append(v)
                elif col[v] == col[u]:
                    return None
    return col


def find_odd_cycle(adj, maxr=7):
    nodes = list(adj)
    for r in range(3, maxr + 1, 2):
        for C in combinations(nodes, r):
            first = C[0]
            for rest in permutations(C[1:]):
                cyc = (first,) + rest
                if all(cyc[i + 1] in adj[cyc[i]] for i in range(r - 1)) \
                   and cyc[0] in adj[cyc[-1]]:
                    return cyc
    return None


# ------------------------------------------------------------------ C4
def c4_five_cycle_arithmetic():
    """paper 8.2: indices in Z/5, steps eps_j in {+-1}, six positions.
    (i) antipodal positions j and j+3 admit index differences 0, +-2 only,
        and the sum -3,-1,1,3 of three steps is never 0 mod 5, so it must be
        +-2 mod 5, i.e. the three steps are equal;
    (ii) six positions close: the total sum is 0 mod 5."""
    good = []
    for eps in product((1, -1), repeat=6):
        if all(eps[(j + t) % 6] == eps[j] for j in range(6) for t in range(3)) \
           and sum(eps) % 5 == 0:
            good.append(eps)
    return good


# ------------------------------------------------------------------ C5
def c5_diagonals():
    D = {i: frozenset({i, (i + 2) % 5}) for i in range(5)}
    ok = True
    for a, b in combinations(range(5), 2):
        disj = not (D[a] & D[b])
        ok &= (disj == (((b - a) % 5) in (1, 4)))
    return ok, D


# ------------------------------------------------------------------ C6
def c6_triangle():
    col = {0: 4, 1: 5, 2: 6}
    return all(col[a] != col[b] for a, b in combinations(range(3), 2)), col


def c6_path():
    col = {0: 4, 1: 5, 2: 6, 3: 4, 4: 5}
    return all(col[i] != col[i + 1] for i in range(4)), col


# ------------------------------------------------------------------ main
if __name__ == "__main__":
    W = 76

    def head(t):
        print("=" * W)
        print(t)
        print("=" * W)

    head("C1  four-cycle locus (paper 6.3.1): palettes made of cycle labels only")
    for k, cap in ((5, 2), (6, 3)):
        free, allp = c1(k, 4, cap), c1_all(k, 4, cap)
        print(f" k={k}, palette bound {cap}: {len(allp)} admissible palettes, "
              f"{len(free)} of them cycle-label only:")
        for P in free:
            used = set(P)
            print(f"   {sorted(P)}:  U={{0,2}} part {sorted(used & {0,2})}, "
                  f"V={{1,3}} part {sorted(used & {1,3})}")

    head("C1b  palette {0,2,4} at the k=6 four-cycle locus (ambiguity witness)")
    for k, cap in ((5, 2), (6, 3)):
        P = frozenset({0, 2, 4})
        ok = (1 <= len(P) <= cap) and not inside_an_edge(P, 4)
        print(f" k={k}: palette {{0,2,4}} admissible = {ok} "
              f"(|P|={len(P)} vs bound {cap}); "
              f"contains state X={{4}}: {4 in P}, contains state U={{0,2}}: {P >= {0,2}}")

    head("C2  external alphabet at a TRIANGLE interface (Theorem B) and the "
         "disjointness graph (paper (5.7))")
    for k in (4, 5, 6):
        S = external_alphabet(k, 3)
        adj = disjoint_graph(S)
        two = bipartite(adj)
        print(f" k={k}: |Sigma| = {len(S)}   bipartite = {two is not None}"
              f"   states = {[sorted(s) for s in S]}")
        if two is None:
            print("      odd cycle:", [sorted(s) for s in find_odd_cycle(adj)])

    head("C3  admissible palette counts (bound k-3)")
    for k in (4, 5, 6):
        print(f" k={k} (bound {k-3}): " + "  ".join(
            f"l={l}:{len(c1_all(k, l, k-3))}" for l in (3, 4, 5)))

    head("C4  five-cycle step arithmetic of paper 8.2 (k=5), exhaustive")
    good = c4_five_cycle_arithmetic()
    print(f" admissible six-step sequences: {len(good)}   (paper: none)")

    head("C5  five-cycle diagonals D_i = {i,i+2} (paper 6.3.3)")
    ok, D = c5_diagonals()
    print(" D_a cap D_b empty <=> b-a = +-1 mod 5, for all 10 pairs:", ok)

    head("C6  colouring certificates")
    ok, col = c6_triangle()
    print(f" unit equilateral triangle properly 3-coloured with labels 4,5,6: {ok} {col}")
    ok, col = c6_path()
    print(f" 4-edge unit path, proper 3-colouring, endpoints differ:        {ok} {col}")

    head("C7  four-cycle splits (Proposition B4): outsider-free palettes per split")
    for k, cap in ((5, 2), (6, 3)):
        for mid in ((0, 2), (1, 3)):
            # split with run-middle vertices mid[0], mid[1]: the palette must
            # contain both, avoid all outsiders, and avoid containment in an edge
            adm = [P for P in nonempty_subsets(set(range(k)), 1, cap)
                   if P <= frozenset(range(4))
                   and set(mid) <= set(P)
                   and not inside_an_edge(P, 4)]
            print(f"  k={k}, split with middles {mid}: {len(adm)} palettes {[sorted(P) for P in adm]}")

    head("C8  a k=6 triangle-interface model with |A| = 2 (constraint level)")
    # six arcs D_0..D_5 of length pi/3, R(D_k) = D_{k+1 mod 6}; T = {0,1,2},
    # T^c = {3,4,5}.  Outsider set A = {3,4} on the even arcs, {5} on the odd ones.
    T = frozenset({0, 1, 2})
    Tc = frozenset({3, 4, 5})
    A = [frozenset({3, 4}) if k % 2 == 0 else frozenset({5}) for k in range(6)]
    print("   arcs D_0..D_5, R(D_k) = D_(k+1):", [sorted(a) for a in A])
    c_a1 = all(1 <= len(a) <= 2 for a in A)
    c_a2 = all(not (A[k] & A[(k + 1) % 6]) for k in range(6))
    c_sub = all(a <= Tc for a in A)
    two_measure = 3 * (F(1, 3))          # three arcs of length pi/3, in units of pi
    print(f"   1 <= |A| <= 2 : {c_a1}   A cap A(R.) = empty : {c_a2}   "
          f"A subset of T^c : {c_sub}")
    print(f"   arcs with |A| = 2 : {[k for k in range(6) if len(A[k]) == 2]}, "
          f"total angular measure {two_measure}*pi = {float(two_measure)}*pi")
    # palette P(e) := A(e): check the k=6 palette-level constraints
    P = A
    c_p1 = all(1 <= len(p) <= 3 for p in P)
    c_p2 = all(not (P[k] & P[(k + 1) % 6]) for k in range(6))
    c_p3 = all(not inside_an_edge(p, 3) for p in P)
    c_p4 = all(p & Tc for p in P)                    # meets O(e) and I(e), both >= T^c
    print(f"   palette constraints: 1<=|P|<=3 {c_p1}, P cap P(R.)=empty {c_p2}, "
          f"not inside a cycle edge {c_p3}, meets T^c (hence O and I) {c_p4}")
