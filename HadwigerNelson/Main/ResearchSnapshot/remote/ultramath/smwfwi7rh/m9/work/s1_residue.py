"""s1_residue.py  --  the (3,2) residue catalogue at k=6.

For a cycle length ell in {3,4,5,6} at a typical centre x (colour i), a palette P
is admissible if it is not contained in any edge of C_ell (Lemma 6.2 / (6.2)),
i not in P, and 1 <= |P| <= 3.

A "2-valued (3,2) field" is a pair (A,B) with |A| = 3, |B| = 2, A cap B = empty,
A union B = [6] \ {i}; the field is A on U and B on S \ U with U = R^2 U
(3-fold symmetry), so along the R-orbit of 6 positions it reads A,B,A,B,A,B.

Everything here is exact integer/set arithmetic.
"""
from itertools import combinations

K = 6
FULL = frozenset(range(K))

def edges(ell):
    return [frozenset((j, (j + 1) % ell)) for j in range(ell)]

def admissible(P, ell, i):
    if i in P or not (1 <= len(P) <= 3):
        return False
    return all(not P <= e for e in edges(ell))

def admissible_palettes(ell, i):
    return [frozenset(c) for r in (1, 2, 3)
            for c in combinations([x for x in range(K) if x != i], r)
            if admissible(frozenset(c), ell, i)]

def catalogue(ell, i):
    """All 2-valued (3,2) fields: A ternary admissible, B = complement of A+i, a pair,
    also admissible, and A,B disjoint (automatic)."""
    out = []
    vals = admissible_palettes(ell, i)
    for A in vals:
        if len(A) != 3:
            continue
        B = FULL - A - {i}
        if len(B) != 2 or frozenset(B) not in vals:
            continue
        out.append((A, frozenset(B)))
    return out

def main():
    print("=" * 78)
    print("(3,2) residue catalogue at k=6   (A ternary, B = [6]\\{A,i} a pair)")
    print("=" * 78)
    allcat = {}
    for ell in (3, 4, 5, 6):
        for i in range(K):
            cat = catalogue(ell, i)
            if not cat:
                continue
            allcat[(ell, i)] = cat
            where = "centre colour in the cycle" if i < ell else "centre colour = the outsider"
            print(f"\nell={ell}  centre colour i={i}   ({where})")
            print(f"  {len(cat)} residue field(s):")
            for A, B in cat:
                # 3-fold symmetry along the R-orbit: positions j and j+2 equal
                word = [A if j % 2 == 0 else B for j in range(6)]
                sym = all(word[j] == word[(j + 2) % 6] for j in range(6))
                print(f"    A={sorted(A)}  B={sorted(B)}   word={[''.join(map(str, sorted(p))) for p in word]}"
                      f"   3fold={sym}")
    print()
    print("=" * 78)
    print("same-direction disjointness at unit separation (paper Remark 5.3)")
    print("=" * 78)
    print("A translation-invariant field has P_{x+u}(f) = P_x(f) =: P(f), so the")
    print("constraint P_{x+u}(f) cap P_x(f) = empty forces P(f) = empty, which")
    print("contradicts non-emptiness of the palette.  Hence: no translation-")
    print("invariant palette field satisfies (5.3) at separation 1.")
    for (ell, i), cat in allcat.items():
        for A, B in cat:
            assert A & B == set()
            print(f"  ell={ell} i={i}: A cap B = empty, A|B = [6]\\{{{i}}}  -> "
                  f"violates same-direction disjointness at separation 1 (both nonempty)")
    print()
    print("=" * 78)
    print("m2 two-centre bound under translation invariance")
    print("=" * 78)
    for (ell, i), cat in allcat.items():
        for A, B in cat:
            bad = []
            for P in (A, B):
                if len(P) == 3:
                    bad.append(f"|P_x|+|P_y| = 3+3 = 6 > 5 at a unit pair with P_x = {sorted(P)}")
            print(f"  ell={ell} i={i} A={sorted(A)}: {'; '.join(bad) if bad else 'no ternary value -> m2 satisfied'}")

if __name__ == "__main__":
    main()
