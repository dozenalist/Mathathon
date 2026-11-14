"""Refining the k=6 triangle interface (ell=3): which palette types really occur.

Cycle labels T = {0,1,2}, outsiders U = {3,4,5}, k = 6, all 216 ray geometries.

Established here (exact, no floating point):

(A) No label of T can lie in both O_i and I_i at the same position, and in fact
    T cap O_i and T cap I_i are never both nonempty: with three signs the three
    consecutive pairs cannot contain both a ++ pair and a -- pair.  Consequence: a
    palette P with P subset of T never meets both allowed sets, so the full-triangle
    palette "P = T" (type (iii) of the (6.2)-enumeration) is NOT admissible.
    Hence the alternating T / outside-pair pattern is a model at 0 geometries.

(B) What occurs is classified by |P cap U| in {1,2,3}:
      |P cap U| = 1  -- the paper's k=5-style binary-centre route applies;
      |P cap U| = 2  -- no alternating selection from U (|U| = 3), new argument needed;
      |P cap U| = 3  -- forces P = U exactly (|P| <= 3), so the palette meets no cycle
                        label at all.  U is admissible at EVERY position of EVERY
                        geometry (U subset of O_i cap I_i, |U| = 3 = k-3).
    So results/K6-BARRIER.md §3's "general bound 1 <= |A(e)| <= k-4" is false at k = 6,
    ell = 3: A(e) = P cap U can have size 3, e.g. P = {3,4,5}.  At k = 5 the bound holds
    (there |U| = 2 and a subset of T of size <= 2 lies in some edge).

(C) Every one of the 216 geometries has a model containing a ternary palette, even though
    every one also has a binary model (Theorem B of STEP1-VACUITY.md).

Run:  python3 ternary_models.py
"""
from itertools import product, combinations
import sympy

K, NPOS = 6, 6
COS_SIGN = [int(sympy.sign(sympy.cos(m * sympy.pi / 3))) for m in range(6)]


def sign_matrix(ell, cells):
    return [[COS_SIGN[(cells[j] + 1 - i) % 6] for j in range(ell)] for i in range(NPOS)]


def allowed_sets(ell, k, sig_i):
    U = set(range(k)) - set(range(ell))
    O, I = set(U), set(U)
    for j in range(ell):
        if sig_i[(j - 1) % ell] == -1 and sig_i[j] == -1:
            O.add(j)
        if sig_i[(j - 1) % ell] == 1 and sig_i[j] == 1:
            I.add(j)
    return frozenset(O), frozenset(I)


def admissible(ell, k, sig_i):
    O, I = allowed_sets(ell, k, sig_i)
    out = []
    for r in range(1, k - 2):
        for c in combinations(range(k), r):
            s = frozenset(c)
            if s & O and s & I:
                out.append(s)
    return out


def models(ell, k, cells):
    """(any (C1)-(C3) model, any such model containing a 3-set palette)."""
    sig = sign_matrix(ell, cells)
    adm = [admissible(ell, k, sig[i]) for i in range(NPOS)]
    if any(not a for a in adm):
        return (False, False)
    sol = []
    found = [False, False]

    def rec(i):
        if i == NPOS:
            if sol[NPOS - 1] & sol[0]:
                found[0] = True
                if any(len(p) == 3 for p in sol):
                    found[1] = True
            return
        for p in adm[i]:
            if i and (p & sol[i - 1]):
                continue
            sol.append(p)
            rec(i + 1)
            sol.pop()
            if found[0] and found[1]:
                return

    for p0 in adm[0]:
        sol[:] = [p0]
        rec(1)
        if found[0] and found[1]:
            break
    return (found[0], found[1])


def main():
    ell, k = 3, K
    T = frozenset(range(ell))
    U = frozenset(range(ell, k))
    U2 = frozenset([3, 4])
    bad_A = 0
    U_everywhere = 0
    two_outside = 0
    pattern_ok = 0
    any_model = with_ternary = 0
    example = None

    for cells in product(range(6), repeat=ell):
        sig = sign_matrix(ell, cells)
        for i in range(NPOS):
            O, I = allowed_sets(ell, k, sig[i])
            if (O & T) and (I & T):
                bad_A += 1
        adm = [admissible(ell, k, sig[i]) for i in range(NPOS)]
        if all(U in a for a in adm):
            U_everywhere += 1
            if example is None:
                example = cells
        if any(len(p & U) == 2 and (p & T) for a in adm for p in a):
            two_outside += 1
        ok = True
        for i in range(NPOS):
            O, I = allowed_sets(ell, k, sig[i])
            P = [T, U2][i % 2]
            Q = [T, U2][(i + 1) % 2]
            if not (1 <= len(P) <= k - 3 and (P & O) and (P & I)) or (P & Q):
                ok = False
                break
        pattern_ok += ok
        a, t = models(ell, k, cells)
        any_model += a
        with_ternary += t

    print(f"(A) positions with T cap O_i and T cap I_i both nonempty: {bad_A}   (want 0)")
    print(f"    alternating T/{{3,4}} pattern is a model at {pattern_ok} / {6**ell} geometries")
    print(f"(B) P = U = {sorted(U)} admissible at every position, geometries: "
          f"{U_everywhere} / {6**ell}   e.g. cells {example}")
    print(f"    geometries admitting a palette with |P cap U| = 2 plus a cycle label: "
          f"{two_outside} / {6**ell}")
    print(f"(C) geometries with a (C1)-(C3) model: {any_model} / {6**ell};"
          f" with a model containing a ternary palette: {with_ternary} / {6**ell}")
    assert bad_A == 0 and pattern_ok == 0


if __name__ == "__main__":
    main()
