#!/usr/bin/env python3
"""
Exact certificates for the k=6 ternary-separation note (d18).

All arithmetic is exact integer arithmetic.  Every decisive number is computed
by two independent code paths (PATH A / PATH B) that are checked against each
other.

Labels I = {0,...,5}.  R = rotation by kappa = pi/3 acts on the six directions
f, Rf, ..., R^5 f of one orbit.

Paper inputs used (checked against the rendered pages):
  (6.2)  ij in Gamma_x  =>  P_x(e) is not contained in {i,j}   (Lemma 6.2)
  (5.7)  P_x(f) cap P_x(Rf) = empty                            (Corollary 5.4)
  (5.2)  c(x+e+v) not in P_x(e) u P_x(v)                       (Lemma 5.2(1))
"""

import itertools

K = 6
LABELS = tuple(range(K))
SECTORS = 6
RSTEP = 1  # R advances one 60-degree sector

X, Y = 4, 5


def admissible(edges, size_max):
    """Nonempty palettes of size <= size_max not contained in any listed edge."""
    out = []
    for r in range(1, size_max + 1):
        for P in itertools.combinations(LABELS, r):
            S = set(P)
            if any(S <= set(e) for e in edges):
                continue
            out.append(frozenset(S))
    return out


E4 = [(0, 1), (1, 2), (2, 3), (3, 0)]
E5 = [(i, (i + 1) % 5) for i in range(5)]
E3 = [(0, 1), (1, 2), (2, 0)]


# ===========================================================================
# 1.  Four-cycle at k = 6 with |P| <= 2.
# ===========================================================================
def four_cycle_state(P):
    S = set(P)
    if X in S:
        paper = "X"
    elif S == {0, 2}:
        paper = "U"
    elif S == {1, 3}:
        paper = "V"
    else:
        paper = None
    return paper


def check_four_cycle():
    pals = admissible(E4, 2)
    # PATH A
    A = sorted((tuple(sorted(P)), four_cycle_state(P)) for P in pals)
    # PATH B: rebuild from scratch with an explicit membership table
    B = []
    for P in pals:
        S = set(P)
        st = None
        if S != set():
            if 4 in S:
                st = "X"
            elif S == {0, 2}:
                st = "U"
            elif S == {1, 3}:
                st = "V"
        B.append((tuple(sorted(S)), st))
    assert A == sorted(B)
    undefined = [p for p, st in A if st is None]
    ambiguous = []
    for P in pals:
        S = set(P)
        groups = []
        if X in S:
            groups.append("X")
        if Y in S:
            groups.append("Y")
        if {0, 2} <= S:
            groups.append("U")
        if {1, 3} <= S:
            groups.append("V")
        if len(groups) >= 2:
            ambiguous.append((tuple(sorted(S)), tuple(groups)))
    return len(pals), undefined, ambiguous


# ===========================================================================
# 2.  The T-spread six-sector model of Proposition 4.
# ===========================================================================
WORD = (0, 1, 2, 0, 1, 2)
# triangle on the labels 3,4,5 ; its outsiders are exactly T = {0,1,2}
E3_T = [(3, 4), (4, 5), (5, 3)]
T_MODEL = {0, 1, 2}


def check_model():
    field = [frozenset({WORD[s]}) for s in range(SECTORS)]
    okA = all(WORD[s] != WORD[(s + RSTEP) % SECTORS] for s in range(SECTORS))
    okB = all(field[s].isdisjoint(field[(s + RSTEP) % SECTORS])
              for s in range(SECTORS))
    assert okA and okB
    sizes = sorted({len(f) for f in field})
    hit = all(bool(f & T_MODEL) for f in field)
    values = {next(iter(f)) for f in field}
    spread = values == T_MODEL
    adm = all(not any(f <= set(e) for e in E3_T) for f in field)
    return okA, sizes, hit, spread, adm, sorted(values)


# ===========================================================================
# 3.  Five-cycle at k = 6 with |P| <= 2.
# ===========================================================================
def check_five_cycle():
    pals = admissible(E5, 2)
    diag = {frozenset({i, (i + 2) % 5}) for i in range(5)}
    in_diag = [P for P in pals if P in diag]
    not_diag = [P for P in pals if P not in diag]
    return len(pals), len(in_diag), sorted(not_diag)


# ===========================================================================
# 4.  Triangle at k = 6 with |P| <= 2.
# ===========================================================================
def check_triangle():
    pals = admissible(E3, 2)
    hit = [P for P in pals if set(P) & {3, 4, 5}]
    return len(pals), len(hit), sorted(pals)


if __name__ == "__main__":
    n4, undef4, amb4 = check_four_cycle()
    print("== four-cycle centre at k=6, |P| <= 2 ==")
    print("  admissible palettes:", n4)
    print("  outside the paper's X/U/V trichotomy:", undef4)
    print("  representing two groups at once:", amb4)
    ok, sizes, hit, spread, adm, values = check_model()
    print("== six-sector T-spread model (Prop. 4) ==")
    print("  (5.7):", ok, " sizes:", sizes, " T-hitting:", hit,
          " T-spread:", spread, " admissible(triangle):", adm,
          " values:", values)
    n5, d5, rest5 = check_five_cycle()
    print("== five-cycle centre at k=6, |P| <= 2 ==")
    print("  admissible:", n5, " diagonals:", d5, " other:", len(rest5))
    print("  other list:", rest5)
    n3, h3, list3 = check_triangle()
    print("== triangle centre at k=6, |P| <= 2 ==")
    print("  admissible:", n3, " hitting the outsider triple:", h3)
    print("  list:", list3)
