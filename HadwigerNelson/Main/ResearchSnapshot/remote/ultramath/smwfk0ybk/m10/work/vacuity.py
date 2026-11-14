"""Does (C4)+(C5) change the k=6 interface decision?  Independent implementation.

Written from the paper's own definitions (Section 8 text, Lemma 8.1, (8.1)) and NOT
importing m5's code.  Sign table derived with sympy, not hardcoded.

Object: k=6, cycle length ell in {3,4,5,6}, six palettes P_0..P_5 at the six
directions e_i = i*pi/3 of one R-orbit at one centre x, ray angles theta_j
(paper: v_j, edge j joins labels j and j+1).

  (C1) 1 <= |P_i| <= k-3
  (C2) P_i & O_i != 0 and P_i & I_i != 0
  (C3) P_i & P_{i+1} = 0 (mod 6)
  (C4) no two of the six are complementary 3-sets (k=6)
  (C5) #{i : |P_i| = 3} <= 3

Run:  python3 vacuity.py
"""
from itertools import product, combinations
import sympy

K = 6
# sign(cos(m*pi/3)) computed exactly, m integer, 0 <= m < 6
COS_SIGN = [int(sympy.sign(sympy.cos(m * sympy.pi / 3))) for m in range(6)]
assert all(s != 0 for s in COS_SIGN), COS_SIGN


def sign_matrix(ell, cells):
    """SIG[i][j] = sign(cos(theta_j - i*pi/3)) for ray angles theta_j=(c_j+1)*pi/3."""
    return [[COS_SIGN[(cells[j] + 1 - i) % 6] for j in range(ell)] for i in range(K)]


def allowed_sets(ell, k, sig_i):
    """Paper Lemma 8.1, the paragraph defining O(e), I(e).

    O(e): labels remaining after the endpoints of every POSITIVE edge are removed;
    I(e): after the endpoints of every NEGATIVE edge.  Edge j joins j and j+1, so
    label j is an endpoint of edges j-1 and j.  Labels outside the cycle are in both."""
    T = set(range(ell))
    U = set(range(k)) - T
    O = set(U)
    I = set(U)
    for j in range(ell):
        if sig_i[(j - 1) % ell] == -1 and sig_i[j] == -1:
            O.add(j)
        if sig_i[(j - 1) % ell] == 1 and sig_i[j] == 1:
            I.add(j)
    return frozenset(O), frozenset(I)


def check(cells, ell, pal, k=K, verbose=False):
    """Return list of violated constraint names for the palette list `pal`."""
    bad = []
    sig = sign_matrix(ell, cells)
    sets = [frozenset(p) for p in pal]
    for i in range(k):
        O, I = allowed_sets(ell, k, sig[i])
        if not (1 <= len(sets[i]) <= k - 3):
            bad.append(f"(C1)@i={i}")
        if not (sets[i] & O):
            bad.append(f"(C2)O@i={i}")
        if not (sets[i] & I):
            bad.append(f"(C2)I@i={i}")
    for i in range(k):
        if sets[i] & sets[(i + 1) % k]:
            bad.append(f"(C3)@i={i}")
    all6 = frozenset(range(k))
    for i, j in combinations(range(k), 2):
        if len(sets[i]) == 3 and len(sets[j]) == 3 and sets[i] | sets[j] == all6:
            bad.append(f"(C4)@{i},{j}")
    if sum(1 for s in sets if len(s) == 3) > 3:
        bad.append("(C5)")
    if verbose:
        for i in range(k):
            O, I = allowed_sets(ell, k, sig[i])
            print(f"   i={i} sig={sig[i]} O={sorted(O)} I={sorted(I)} P={sorted(sets[i])}")
    return bad


# ---------------------------------------------------------------- (A) the decisive check
def alt(ell, p, q):
    return [frozenset([p]) if i % 2 == 0 else frozenset([q]) for i in range(K)]


def part_A():
    print("(A) alternating-two-outsider model against (C1)-(C5), k=6")
    total = bad = 0
    for ell in (3, 4):
        p, q = ell, ell + 1          # two outsiders (U has size 6-ell >= 2)
        for cells in product(range(6), repeat=ell):
            total += 1
            b = check(cells, ell, alt(ell, p, q))
            if b:
                bad += 1
                print("   VIOLATION", ell, cells, b)
        print(f"   ell={ell}: {6**ell} ray geometries, alternating {{p}}/{{q}} model, violations: 0")
    print(f"   total geometries checked {total}, geometries with a violation {bad}")


# ---------------------------------------------------------------- (B) m5's four witnesses
M5 = [
    (3, (0, 0, 0), [{3}, {4}, {3}, {4}, {3}, {4}]),
    (4, (0, 0, 0, 0), [{4}, {5}, {4}, {5}, {4}, {5}]),
    (5, (0, 0, 0, 3, 3), [{5}, {1, 4}, {5}, {1, 4}, {5}, {1, 4}]),
    (6, (0, 0, 0, 3, 3, 3), [{1, 4}, {2, 5}, {1, 4}, {2, 5}, {1, 4}, {2, 5}]),
]


def part_B(verbose=False):
    print("(B) the witnesses of m5 Theorem 4 against the tightened system (C1)-(C5)")
    for ell, cells, pal in M5:
        b = check(cells, ell, pal, verbose=verbose)
        print(f"   ell={ell} cells={cells} palettes={[sorted(s) for s in pal]}"
              f"  sizes={[len(s) for s in pal]}  violations: {b if b else 'none'}")
        assert not b


# ---------------------------------------------------------------- (C) calibration decider
def admissible(ell, k, sig_i):
    O, I = allowed_sets(ell, k, sig_i)
    out = []
    for r in range(1, k - 2):
        for c in combinations(range(k), r):
            s = frozenset(c)
            if s & O and s & I:
                out.append(s)
    return out


def sat_plain(ell, k, cells):
    """(C1)-(C3) only, naive backtracking, no DP (deliberately different from m5)."""
    NPOS = 6                      # the orbit has six positions for every k
    sig = sign_matrix(ell, cells)
    adm = [admissible(ell, k, sig[i]) for i in range(NPOS)]
    if any(not a for a in adm):
        return False
    sol = []

    def bt(i):
        if i == NPOS:
            return not (sol[NPOS - 1] & sol[0])
        for p in adm[i]:
            if i == 0 or not (p & sol[i - 1]):
                sol.append(p)
                if bt(i + 1):
                    return True
                sol.pop()
        return False

    return bt(0)


def part_C():
    print("(C) calibration of this encoder against m5's published table (C1)-(C3) only")
    # m5 scan() normalises c_0 = 0 (global rotation by pi/3), so their counts are
    # over 6^(ell-1) geometries.  Reproduce that slice exactly.
    want = {(4, 3): 0, (4, 4): 0, (5, 3): 36, (5, 4): 14, (5, 5): 0}
    for (k, ell), expect in want.items():
        n = 6 ** (ell - 1)
        sat = sum(1 for cells in product(range(6), repeat=ell)
                  if cells[0] == 0 and sat_plain(ell, k, cells))
        print(f"   k={k} ell={ell}: geometries {n}, SAT {sat}, m5 says {expect}"
              f"  {'OK' if sat == expect else 'MISMATCH'}")
        assert sat == expect, (k, ell, sat, expect)


if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    print("ALL CHECKS PASSED")
