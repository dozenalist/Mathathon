"""Independent checker for Astra's four finite interface witnesses + the m6 two-state question.
Standalone: standard library only, exact combinatorial arithmetic, no floating point decisions.

CONSTRAINT TABLE (every row carries its source and quantifier; nothing invented).
Labels C = {0..5}. m, q in {0,3}^m, P_j = palette at angle j (j=0..5), E_i = {i, i+1 mod m}.
Angles: u_j = e^{i(t + j*pi/3)}; v_i = e^{i q_i*pi/3};  s[i][j] = sign(<v_i, u_j>).

 id  constraint                                    source                     quantifier
 C1  P_j != empty                                  relay: "P_j nonempty"      forall j
 C2  |P_j| <= 2                                    relay: "size<=2"           forall j
 C3  P_j cap P_{j+1 mod 6} = empty                 relay: "adjacentP_j disjoint"   forall j
 C4  forall i: P_j not subset of E_i               relay: "P_j not contained inany E_i"  forall j, i
 C5  for both sigma in {+,-}: P_j cap (C \\ U_sigma) != empty,  relay: "both sides require
       where U_sigma = union{E_i : s[i][j] = sigma}    P_j intersects C minus union(E_i on that side)"
                                                     forall j, sigma
 ALT the witness form: P_j = J (j even), K (j odd)   relay: "Palettes alternate J, K"

Cells: a_j = sign(cos(t + j*pi/3)) is constant on t in ((2c-1)pi/6, (2c+1)pi/6), c=0..5,
the critical points being the odd multiples of pi/6.  We evaluate at the cell centre t = c*pi/3,
where cos((c+j)pi/3) is one of 1, 1/2, -1/2, -1 exactly.
"""
import sys
from itertools import combinations, product

LBL = list(range(6))

def cell_sign(c, j):
    """sign of cos((c+j)*pi/3), exact via the residue class mod 6."""
    n = (c + j) % 6
    v = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}[n]
    return v

def sign_matrix(m, q, c):
    """s[i][j] for i in 0..m-1, j in 0..5, evaluated at the centre of cell c."""
    return [[cell_sign(c, j) * (1 if q[i] == 0 else -1) for j in range(6)] for i in range(m)]

def interfaces(m):
    return [frozenset({i, (i + 1) % m}) for i in range(m)]

def side_unions(m, s, j):
    """U_sigma for sigma in {+1,-1}: union of E_i over i with s[i][j] = sigma."""
    E = interfaces(m)
    plus = frozenset().union(*[E[i] for i in range(m) if s[i][j] == 1]) if any(s[i][j] == 1 for i in range(m)) else frozenset()
    minus = frozenset().union(*[E[i] for i in range(m) if s[i][j] == -1]) if any(s[i][j] == -1 for i in range(m)) else frozenset()
    return {1: plus, -1: minus}

def check_assignment(m, q, P, verbose=False):
    """Return (ok, failures, per-angle admissible info). P is a list of 6 frozensets."""
    E = interfaces(m)
    fails = []
    for c in range(6):
        s = sign_matrix(m, q, c)
        for j in range(6):
            Pj = P[j]
            if not Pj: fails.append((c, j, "C1 empty"))
            if len(Pj) > 2: fails.append((c, j, "C2 size>2"))
            for Ei in E:
                if Pj <= Ei: fails.append((c, j, f"C4 P subset E_{E.index(Ei)}"))
            for sigma, U in side_unions(m, s, j).items():
                if not (Pj & (frozenset(LBL) - U)):
                    fails.append((c, j, f"C5 side {sigma}"))
        for j in range(6):
            if P[j] & P[(j + 1) % 6]: fails.append((c, j, "C3 adjacent overlap"))
    return (len(fails) == 0), fails

def admissible_palettes(m, q):
    """All nonempty P with |P|<=2 satisfying C4 and C5 (C1,C2 implicit). C5 is checked
    for every cell and angle; by the invariance lemma they all agree, which we verify."""
    E = interfaces(m)
    ok = []
    for size in (1, 2):
        for S in combinations(LBL, size):
            P = frozenset(S)
            if any(P <= Ei for Ei in E): continue
            good = True
            for c in range(6):
                s = sign_matrix(m, q, c)
                for j in range(6):
                    for sigma, U in side_unions(m, s, j).items():
                        if not (P & (frozenset(LBL) - U)): good = False; break
                    if not good: break
                if not good: break
            if good: ok.append(P)
    return ok

def max_distinct_cyclic(adm):
    """Max number of DISTINCT palettes in a cyclic sequence P_0..P_5 from adm with
    adjacent (including P_5,P_0) disjoint."""
    compl = {(A, B) for A in adm for B in adm if not (A & B)}
    best = 0; witness = None
    for seq in product(adm, repeat=6):
        if any((seq[j], seq[(j + 1) % 6]) not in compl for j in range(6)): continue
        d = len(set(seq))
        if d > best: best, witness = d, seq
    return best, witness

FAIL = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond: FAIL.append(name)

WIT = [ (3, (0,0,0),      frozenset({3}),    frozenset({4})),
        (4, (0,0,0,0),    frozenset({4}),    frozenset({5})),
        (5, (0,3,3,0,0),  frozenset({0,2}),  frozenset({5})),
        (6, (0,3,3,3,0,0),frozenset({0,2}),  frozenset({3,5})) ]

print("=" * 78); print("FINITE INTERFACE WITNESSES + m6 TWO-STATE CHECK"); print("=" * 78)

print("\n[1] the four Astra witnesses, alternating palette P_j = J (j even), K (j odd)")
for (m, q, J, K) in WIT:
    P = [J if j % 2 == 0 else K for j in range(6)]
    ok, fails = check_assignment(m, q, P)
    check(f"m={m} q={q} J={sorted(J)} K={sorted(K)}", ok,
          "" if ok else f"{len(fails)} failures, first {fails[:2]}")

print("\n[2] invariance of the side-union in j and in the angle cell (the structural point)")
# With q in {0,3}^m the side partition is {i : q_i=0} or its complement, depending only on
# the SIGN of a_j; C5 quantifies over BOTH sides, so the conjunction is invariant.
for (m, q, J, K) in WIT:
    first = None; invariant = True
    for c in range(6):
        s = sign_matrix(m, q, c)
        for j in range(6):
            pair = {frozenset(U) for U in side_unions(m, s, j).values()}
            if first is None: first = pair
            elif pair != first: invariant = False
    check(f"m={m}: the set of side-unions is the same for every cell and every angle", invariant,
          f"{[sorted(tuple(sorted(u)) for u in first)]}")

print("\n[3] m=6: admissible palettes (C1,C2,C4,C5) and the maximum number of distinct ones")
for (m, q, J, K) in WIT:
    adm = admissible_palettes(m, q)
    best, wit = max_distinct_cyclic(adm)
    print(f"      m={m} q={q}: |adm| = {len(adm)}  {[sorted(A) for A in adm]}")
    print(f"          max distinct palettes in a cyclic sequence: {best}"
          + (f"  e.g. {[sorted(A) for A in wit]}" if wit else ""))
    if m == 6:
        # This is the ANSWER to the pre-registered question, not a pass/fail criterion.
        # The analysis itself succeeds whichever way it comes out.
        check("m=6: exhaustive search over admissible palettes COMPLETED (answer below)", True,
              f"max distinct palettes = {best}")
        if best < 3:
            print("      ANSWER: NO model with >= 3 distinct palettes exists for m=6.")
            print("              The finite system forces a two-valued alternation.")
        else:
            print(f"      ANSWER: a model with >= 3 distinct palettes exists (max {best}):")
            print(f"              {[sorted(A) for A in wit]}")
        check("m=6: every admissible adjacent-compatible pair is a 2-state alternation",
              best == 2, f"compatible pairs: " +
              str([[sorted(A), sorted(B)] for A, B in
                   sorted({tuple(sorted((tuple(sorted(A)), tuple(sorted(B)))))
                           for A in adm for B in adm if not (A & B)})]))

print("\n" + "=" * 78)
if FAIL:
    print("RESULT: some checks failed ->", FAIL); sys.exit(1)
print("RESULT: ALL CHECKS PASS")
print("=" * 78)
