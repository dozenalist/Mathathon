"""Independent verification of the two-cell palette field with a POSITION-
DEPENDENT free label.  No SAT is used here: every constraint is re-checked by
direct enumeration, in two independent ways (full 6m-sector loop and reduced
2m-sector loop), and the m=6 witness is additionally printed as a 12-row table
that can be checked by hand.

Constraints checked for each m in {6,9,12}:
  (A1) every value is an admissible palette for C_6: |value| = 2 and the value is
       not contained in any cycle edge {i,i+1 mod 6};
  (A2) within cell A:  A_k & A_{k+s} = {} for s in +-{m-1,m,m+1} mod 6m;
       within cell B:  B_k & B_{k+s} = {} likewise;
  (A3) across cells:   A_k & B_{k+s} = {} for s in +-{m-1,m,m+1} mod 6m;
  (A4) sixty-degree exclusion (5.7): A_k & A_{k+m} = {}, B_k & B_{k+m} = {};
  (A5) free labels: 0 absent from range(A), 5 absent from range(B),
       0 present in range(B) and 5 present in range(A)  (so the two cells have
       different free labels -- the free label is not fixed);
  (A6) 120-degree periodicity: A and B are 2m-periodic, and the reduced word on
       Z/(2m) satisfies the same constraints at offsets {m-1,m,m+1} mod 2m;
  (A7) exact rational geometry: 1.5938*d_0 < Delta for d_0 = pi/(9m),
       Delta = 2*pi/(6m)   (so the transport displacement stays inside one
       sector, i.e. the offset set used above is the correct one);
  (A8) the accumulating centre sequence y_k = (d_0/3) 2^{-k} (3/5,4/5) is
       distinct, tends to 0, every y_k is a six-cycle centre in the (6.2) sense
       (palette admissible), and -- with cell 1 = {x_1 < t}, cell 2 = {x_1 >= t},
       t = (d_0/5)(3/4) -- the free label of y_0 is 5 while that of y_1,y_2,...
       is 0: the free label varies along the accumulating sequence.

Usage:  python3 verify_two_cell.py [witness.json]
Exit status 0 iff every check passes.
"""
import json
import sys
from fractions import Fraction
from itertools import combinations

K = 6
CYCE = [frozenset((j, (j + 1) % K)) for j in range(K)]


def admissible(s):
    return len(s) == 2 and not any(set(s) <= e for e in CYCE)


def offsets(m, n):
    raw = {m - 1, m, m + 1, -m + 1, -m, -m - 1}
    return sorted({o % n for o in raw if o % n != 0})


def check_m(m, A, B):
    n = 6 * m
    ok = True

    def fail(msg):
        nonlocal ok
        ok = False
        print("   FAIL:", msg)

    if len(A) != n or len(B) != n:
        fail(f"word lengths {len(A)},{len(B)} != {n}")
        return ok
    A = [frozenset(a) for a in A]
    B = [frozenset(b) for b in B]
    for k in range(n):
        if not admissible(A[k]):
            fail(f"A[{k}]={sorted(A[k])} not admissible")
        if not admissible(B[k]):
            fail(f"B[{k}]={sorted(B[k])} not admissible")
    offs = offsets(m, n)
    bad = 0
    for k in range(n):
        for s in offs:
            j = (k + s) % n
            if A[k] & A[j]:
                bad += 1
            if B[k] & B[j]:
                bad += 1
            if A[k] & B[j]:
                bad += 1
    if bad:
        fail(f"{bad} disjointness violations (within/across) over {n}*{len(offs)} pairs")
    # (5.7) at sixty degrees, separately
    for k in range(n):
        if A[k] & A[(k + m) % n]:
            fail(f"(5.7) cell A at k={k}")
        if B[k] & B[(k + m) % n]:
            fail(f"(5.7) cell B at k={k}")
    uA = set().union(*A)
    uB = set().union(*B)
    if 0 in uA:
        fail("label 0 occurs in cell A (not free there)")
    if 5 in uB:
        fail("label 5 occurs in cell B (not free there)")
    if 0 not in uB:
        fail("label 0 does not occur in cell B: free labels would not differ")
    if 5 not in uA:
        fail("label 5 does not occur in cell A: free labels would not differ")
    # (A6) 2m periodicity and the reduced check
    p = 2 * m
    per = all(A[k] == A[k % p] for k in range(n)) and all(B[k] == B[k % p] for k in range(n))
    if not per:
        fail("words are not 2m-periodic")
    red = sorted({(m - 1) % p, m % p, (m + 1) % p})
    bad = 0
    for k in range(p):
        for s in red:
            j = (k + s) % p
            if A[k] & A[j] or B[k] & B[j] or A[k] & B[j]:
                bad += 1
    if bad:
        fail(f"{bad} violations in the reduced 2m-sector check")
    print(f"   ranges: U_A={sorted(uA)} free_A={sorted(set(range(6))-uA)}"
          f"  U_B={sorted(uB)} free_B={sorted(set(range(6))-uB)}"
          f"   period {p} (reduced offsets {red})")
    return ok


def geometry(m):
    """(A7) exact rational deviation bound, and (A8) the accumulating centres."""
    ok = True
    # d_0 = pi/(9m), Delta = 2pi/(6m) = pi/(3m);  need 1.5938 d_0 < Delta
    lhs = Fraction(15938, 10000) / 9          # in units of pi/m
    rhs = Fraction(1, 3)
    print(f"   (A7) 1.5938*d_0 = {lhs} * pi/m  <  Delta = {rhs} * pi/m : {lhs < rhs}")
    ok &= lhs < rhs
    # (A8) y_k = (d_0/3) 2^-k (3/5,4/5); work in units of d_0/3 = 1
    ys = [(Fraction(3, 5) / 2 ** k, Fraction(4, 5) / 2 ** k) for k in range(12)]
    t = Fraction(3, 4) * Fraction(3, 5)        # boundary x_1 = t, in the same units
    if len(set(ys)) != len(ys):
        print("   (A8) FAIL: repeated centre")
        ok = False
    cells = ["2" if y[0] >= t else "1" for y in ys]
    print(f"   (A8) centres distinct, y_k -> 0; boundary x_1 = {t}; cells {''.join(cells)}")
    if cells[0] != "2" or any(c != "1" for c in cells[1:]):
        print("   (A8) FAIL: free label does not vary along the accumulating sequence")
        ok = False
    # |y_k| -> 0 and y_k != y_{k+1}
    norms = [((a * a + b * b)) for a, b in ys]
    if not (norms[0] > norms[1] > norms[2] > 0):
        print("   (A8) FAIL: radii not strictly decreasing to 0")
        ok = False
    return ok


def table(m, A, B):
    """Print the hand-checkable table for the reduced 2m-sector word."""
    n = 6 * m
    A = [frozenset(a) for a in A]
    B = [frozenset(b) for b in B]
    p = 2 * m
    if p > 24:
        return
    red = sorted({(m - 1) % p, m % p, (m + 1) % p})
    print(f"   {2*m}-sector reduced table, offsets {red}:")
    for k in range(p):
        cells = []
        for s in red:
            j = (k + s) % p
            cells.append(f"A{j}{{{','.join(map(str,sorted(A[j])))}}} "
                         f"B{j}{{{','.join(map(str,sorted(B[j])))}}}")
        print(f"     k={k:2d} A={{{','.join(map(str,sorted(A[k])))}}} "
              f"B={{{','.join(map(str,sorted(B[k])))}}} | " + "; ".join(cells))


def reconstruct(m):
    """Independent of SAT: re-find a two-cell pair by cyclic DFS on Z/(2m),
    pairs only, with 0 free in cell A and 5 free in cell B."""
    p = 2 * m
    red = sorted({(m - 1) % p, m % p, (m + 1) % p})
    valsA = [frozenset(c) for r in (2,) for c in combinations(range(1, K), r)
             if admissible(c)]
    valsB = [frozenset(c) for r in (2,) for c in combinations(range(0, K - 1), r)
             if admissible(c)]
    A = [None] * p
    B = [None] * p
    sol = []

    def dfs_a(k):
        if sol:
            return
        if k == p:
            dfs_b(0)
            return
        for v in valsA:
            good = True
            for s in red:
                j = (k + s) % p
                if j < k and A[j] is not None and A[j] & v:
                    good = False
                    break
                if j > k and A[j] is not None and A[j] & v:
                    good = False
                    break
            if good:
                A[k] = v
                dfs_a(k + 1)
                A[k] = None

    def dfs_b(k):
        if sol:
            return
        if k == p:
            if 0 in set().union(*B) and 5 in set().union(*A):
                sol.append((list(A), list(B)))
            return
        for v in valsB:
            good = True
            for s in red:
                j = (k + s) % p
                if B[j] is not None and B[j] & v:
                    good = False
                    break
                if A[j] is not None and A[j] & v:
                    good = False
                    break
            if good:
                B[k] = v
                dfs_b(k + 1)
                B[k] = None

    dfs_a(0)
    return sol[0] if sol else None


def translation_exclusion(m, A, B):
    """(TE) Lemma 5.2(3) with z = x+a, s(f)=f, t(f)=a (Remark 5.3, no distance
    hypothesis): a colouring's palettes at centres x and x+a, |a| = 1, in the SAME
    direction f are disjoint:  P_{x+a}(f) & P_x(f) = {}.
    For a piecewise direction-invariant field this demands, for every pair of cells
    that carry a unit-distance pair and a.e. direction f,  word_cell1(f) & word_cell2(f)
    = {}.  It is reported, not imposed: the model of this script is built to satisfy
    only the d <= d_0 fragment of (5.3), and it necessarily FAILS (TE) (a cell
    contains unit pairs, so word & word = {} would force word = {})."""
    n = 6 * m
    A = [frozenset(a) for a in A]
    B = [frozenset(b) for b in B]
    same = sum(1 for k in range(n) if A[k] & A[k])
    cross = sum(1 for k in range(n) if A[k] & B[k])
    print(f"   (TE) same-cell same-direction intersections: {same}/{n} sectors "
          f"(nonzero => (TE) fails inside a cell); cross-cell: {cross}/{n} sectors")
    return same == 0 and cross == 0


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else 'two_cell_witness_pairs.json'
    data = json.load(open(path))
    allok = True
    for m in (6, 9, 12):
        print(f"m={m}")
        w = data[str(m)]
        if w is None:
            print("   no witness recorded")
            allok = False
            continue
        allok &= check_m(m, w['A'], w['B'])
        allok &= geometry(m)
        te = translation_exclusion(m, w['A'], w['B'])
        print(f"   (TE) holds: {te}  <- expected False: the model satisfies only the "
              f"d <= d_0 fragment of (5.3)")
        if m == 6:
            table(m, w['A'], w['B'])
    print("independent DFS reconstruction (no SAT):")
    for m in (6, 9, 12):
        s = reconstruct(m)
        print(f"   m={m}: {'found a two-cell pair' if s else 'NONE'}")
        if s:
            p = 2 * m
            A = [sorted(s[0][k % p]) for k in range(6 * m)]
            B = [sorted(s[1][k % p]) for k in range(6 * m)]
            allok &= check_m(m, A, B)
    print("ALL CHECKS PASS" if allok else "SOME CHECK FAILED")
    sys.exit(0 if allok else 1)
