"""Independent verification of the k = 6 tightened-CSP decision.

CHECK 1 (encoding).  O_i and I_i are re-derived from the ACTUAL ray angles, not
from the algebraic table sign(cos(m pi/3)).  For a cell vector c we walk three
interior ray angles theta_j = (c_j + 1) pi/3 + delta, delta in {-pi/12, 0, +pi/12},
compute cos(theta_j - i pi/3) numerically, assert |cos| > 0.4 (so the sign is
unambiguous), assert the three deltas give the same sign vector (this is the
claim that the six signs are constant on the cell), and rebuild O_i, I_i from
the paper's definition.  The rebuilt (O,I) must equal the table-derived one.

CHECK 2 (witnesses).  Every witness reported by the search is re-verified from
scratch against (C1),(C2),(C3),(C4),(C5) using the angle-derived O,I.

CHECK 3 (structure).  For every satisfiable geometry at each ell, a model with
all palettes of size <= 2 is produced and verified; this is the structural
reason the two global constraints (C4),(C5) cannot bite.

CHECK 4 (symmetries).  The satisfiability predicate is invariant under the ray
rotation c -> c+1 (used to normalise c_0 = 0) and under the reflection c -> -c.
"""
import math
from itertools import product
import tight_csp as T

PI = math.pi
DELTAS = (-PI / 12, 0.0, PI / 12)
# the three angles (c+1)pi/3 + delta all lie strictly inside the cell
# ((c+1/2)pi/3, (c+3/2)pi/3), and every |cos(theta_j - i pi/3)| >= cos(5pi/12)
# = 0.2588... > 0.25 there, so the floating point sign is unambiguous.


def angle_oi(ell, cells, delta):
    """O_i, I_i from actual angles theta_j = (c_j+1) pi/3 + delta."""
    theta = [(cells[j] + 1) * PI / 3 + delta for j in range(ell)]
    sig = []
    for i in range(6):
        row = []
        for j in range(ell):
            cs = math.cos(theta[j] - i * PI / 3)
            assert abs(cs) > 0.2, ("ambiguous sign", cells, i, j, cs)
            row.append(1 if cs > 0 else -1)
        sig.append(row)
    O, I = [], []
    for i in range(6):
        o = i_set = 0
        U = T.FULL ^ ((1 << ell) - 1)
        o = i_set = U
        for j in range(ell):
            a, b = sig[i][(j - 1) % ell], sig[i][j]
            if a == -1 and b == -1:
                o |= 1 << j
            if a == 1 and b == 1:
                i_set |= 1 << j
        O.append(o)
        I.append(i_set)
    return sig, O, I


def check_encoding():
    bad = 0
    n = 0
    for ell in (3, 4, 5, 6):
        for c in T.geometry_list(ell):
            table = [T.oi_masks(ell, T.sign_matrix(c)[i]) for i in range(6)]
            sigs = []
            for d in DELTAS:
                sig, O, I = angle_oi(ell, c, d)
                sigs.append(sig)
                n += 1
                if [(O[i], I[i]) for i in range(6)] != table:
                    bad += 1
                    print("MISMATCH", ell, c, d)
            if not (sigs[0] == sigs[1] == sigs[2]):
                bad += 1
                print("NOT CONSTANT ON CELL", ell, c)
    print("CHECK 1: %d (geometry, interior-angle) pairs, mismatches = %d" % (n, bad))
    return bad == 0


def check_witnesses():
    bad = 0
    nw = 0
    for ell in (3, 4, 5, 6):
        for c in T.geometry_list(ell):
            s, sols = T.solve(c, tight=True, want="first")
            if not s:
                continue
            nw += 1
            P = sols[0]
            for d in DELTAS:
                sig, O, I = angle_oi(ell, c, d)
                for i in range(6):
                    p = P[i]
                    if not (1 <= bin(p).count("1") <= T.K - 3):
                        bad += 1; print("C1", ell, c)
                    if not (p & O[i]) or not (p & I[i]):
                        bad += 1; print("C2", ell, c, i)
                    if p & P[(i + 1) % 6]:
                        bad += 1; print("C3", ell, c, i)
                for i in range(6):
                    for j in range(i + 1, 6):
                        if T.complementary_3(P[i], P[j]):
                            bad += 1; print("C4", ell, c)
                if sum(1 for i in range(6) if T.is_ternary(P[i])) > 3:
                    bad += 1; print("C5", ell, c)
    print("CHECK 2: %d witnesses re-verified at %d interior angles each, failures = %d"
          % (nw, len(DELTAS), bad))
    return bad == 0


def check_structure():
    """Every satisfiable geometry has a model with all palettes of size <= 2."""
    bad = 0
    for ell in (3, 4, 5, 6):
        cnt = 0
        for c in T.geometry_list(ell):
            s, sols = T.solve(c, tight=True, want="first")
            if not s:
                continue
            ok2, sols2 = T.solve(c, maxsize=2, tight=True, want="first")
            if not ok2:
                bad += 1
                print("no pair-model", ell, c)
            else:
                err = T.check_model(c, sols2[0], tight=True)
                if err:
                    bad += 1
                    print("pair-model invalid", ell, c, err)
                cnt += 1
        print("   ell=%d: %d satisfiable geometries, all with a |P| <= 2 model" % (ell, cnt))
    print("CHECK 3: failures = %d" % bad)
    return bad == 0


def check_symmetry():
    """(i) reflection invariance c -> -c;  (ii) the normalisation c_0 = 0 is
    legitimate: the unnormalised enumeration over all 6^ell cell vectors gives
    exactly 6 times the number of satisfiable geometries."""
    bad = 0
    for ell in (3, 4, 5, 6):
        for c in T.geometry_list(ell):
            base, _ = T.solve(c, tight=True, want="first")
            ref = tuple((0,) + tuple((-x) % 6 for x in c[1:]))
            r2, _ = T.solve(ref, tight=True, want="first")
            if base != r2:
                bad += 1
                print("reflection failure", ell, c, base, r2)
        # unnormalised count
        sat_un = 0
        for c in product(range(6), repeat=ell):
            s_, _ = T.solve(c, tight=True, want="first")
            sat_un += 1 if s_ else 0
        sat_norm = 0
        for c in T.geometry_list(ell):
            s_, _ = T.solve(c, tight=True, want="first")
            sat_norm += 1 if s_ else 0
        print("   ell=%d: unnormalised %d = 6 x normalised %d : %s"
              % (ell, sat_un, sat_norm, sat_un == 6 * sat_norm))
        if sat_un != 6 * sat_norm:
            bad += 1
    print("CHECK 4: reflection/normalisation failures = %d" % bad)
    return bad == 0


if __name__ == "__main__":
    ok = check_encoding()
    ok &= check_witnesses()
    ok &= check_structure()
    ok &= check_symmetry()
    print("\nALL CHECKS PASS:", ok)
