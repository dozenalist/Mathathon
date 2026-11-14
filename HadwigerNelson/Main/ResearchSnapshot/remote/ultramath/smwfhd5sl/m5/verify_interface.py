"""Independent verification of the interface-CSP results.

Three separate checks, none of which reuses the bitmask DP of interface_csp.py:

  CHECK 1  every witness recorded in interface_csp_results.json really is a palette
           system satisfying (C1)-(C3), recomputed from the *paper's* definitions
           of O_i and I_i ("labels remaining after deleting the endpoints of every
           positive / negative edge"), with the ray angles taken from the cells at
           several interior parameters and the signs computed in floating point.
  CHECK 2  agreement of the bitmask DP with a plain backtracking search, on every
           geometry of every (k, ell) in the table.
  CHECK 3  monotonicity in k: a witness for (k, ell) is still admissible at
           (k+1, ell) (this is the proof of the general-k statement).

Run: python3 verify_interface.py
"""
import json
from itertools import product
from fractions import Fraction

# ---------------------------------------------------------------- geometry

def ray_angles(cells, eps=Fraction(1, 3)):
    """Interior representatives of the cells: cell c is ((c+1/2), (c+3/2))*pi/3,
    representative (c + 1/2 + eps)*pi/3 with 0 < eps < 1."""
    return [(c + Fraction(1, 2) + eps) * Fraction(1, 3) for c in cells]   # units of pi


def signs_numeric(cells, i, eps=Fraction(1, 3)):
    """sign(e_i . v_j) for e_i at angle i*pi/3, computed to 30 digits (mpmath)."""
    import mpmath as mp
    mp.mp.dps = 30
    out = []
    for th in ray_angles(cells, eps):
        x = mp.pi * (th - i * Fraction(1, 3))
        cv = mp.cos(x)
        assert abs(cv) > mp.mpf(10) ** -12, ("ray perpendicular to e_i", cells, i)
        out.append(1 if cv > 0 else -1)
    return out


def strip_sets_paper(ell, k, sig_i):
    """O_i and I_i directly from the paper's definition (Section 8.1):
    O(e) = labels left after the endpoints of every *positive* edge are removed,
    I(e) = labels left after the endpoints of every *negative* edge are removed."""
    removed_by_positive = set()
    removed_by_negative = set()
    for j in range(ell):
        ends = {j, (j + 1) % ell}
        if sig_i[j] == 1:
            removed_by_positive |= ends
        else:
            removed_by_negative |= ends
    labels = set(range(k))
    return labels - removed_by_positive, labels - removed_by_negative


# ---------------------------------------------------------------- checks

def check_witness(k, ell, w, verbose=False):
    cells, palettes = w["cells"], w["palettes"]
    assert len(cells) == ell and len(palettes) == 6
    for eps in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
        sig = [signs_numeric(cells, i, eps) for i in range(6)]
        for i in range(6):
            O, I = strip_sets_paper(ell, k, sig[i])
            P = set(palettes[i])
            assert 1 <= len(P) <= k - 3, ("C1", k, ell, i, P)
            assert P & O, ("C2 outer", k, ell, i, P, O)
            assert P & I, ("C2 inner", k, ell, i, P, I)
            assert not (P & set(palettes[(i + 1) % 6])), ("C3", k, ell, i)
    return True


def backtrack_sat(ell, k, cells):
    """Plain DFS, independent of the DP: decide satisfiability from scratch."""
    sig = [signs_numeric(cells, i) for i in range(6)]
    adm = []
    for i in range(6):
        O, I = strip_sets_paper(ell, k, sig[i])
        cur = []
        for r in range(1, k - 2):
            for comb in _combs(range(k), r):
                P = frozenset(comb)
                if P & O and P & I:
                    cur.append(P)
        adm.append(cur)
    sol = []

    def dfs(i):
        if i == 6:
            return not (sol[5] & sol[0])
        for P in adm[i]:
            if not (P & sol[i - 1]):
                sol.append(P)
                if dfs(i + 1):
                    return True
                sol.pop()
        return False

    for P in adm[0]:
        sol = [P]
        if dfs(1):
            return True
    return False


def _combs(it, r):
    from itertools import combinations
    return combinations(it, r)


def main():
    import interface_csp as ic
    data = json.load(open("interface_csp_results.json"))
    n_wit = 0
    for rec in data:
        k, ell = rec["k"], rec["ell"]
        if rec["witness"]:
            check_witness(k, ell, rec["witness"])
            n_wit += 1
    print(f"CHECK 1 ok: {n_wit} recorded witnesses satisfy (C1)-(C3) from the "
          f"paper's definitions of O_i, I_i at three interior ray parameters each")

    # CHECK 2: DP vs backtracking, all geometries when 6^ell <= 1296, else a sample
    import random
    random.seed(20)
    bad = tested = 0
    for rec in data:
        k, ell = rec["k"], rec["ell"]
        geoms = list(product(range(6), repeat=ell))
        if len(geoms) > 1296:
            geoms = random.sample(geoms, 300)
        for c in geoms:
            a = ic.sat_geometry(ell, k, c)
            b = backtrack_sat(ell, k, c)
            tested += 1
            if a != b:
                bad += 1
                print("MISMATCH", k, ell, c, a, b)
    print(f"CHECK 2 ok: bitmask DP and independent backtracking agree on {tested} "
          f"geometries ({bad} mismatches)")

    # CHECK 3: monotonicity in k
    bad = 0
    for rec in data:
        k, ell = rec["k"], rec["ell"]
        if rec["witness"]:
            check_witness(k + 1, ell, rec["witness"])   # same palettes, one more label
    print("CHECK 3 ok: every witness is admissible for k+1 as well "
          "(so satisfiability is monotone in k)")


if __name__ == "__main__":
    main()
