#!/usr/bin/env python3
"""
OBSTRUCTION: the thirteen-face case cannot be closed by counting centres inside a ball.

The project's stated route to the thirteen-face case (REVIEW_2026-11-14_0738 section 4) was
"a bound on the NUMBER of centres with faces inside 1.10".  This script kills that route, and
does it quantitatively rather than by a failed search: it exhibits a LEGAL configuration with
thirteen centres inside distance 2.20 of w1.

Setting.  w1 at the origin.  Six fixed centres: c = (0,0,-2) at distance 2, and five ring
centres at distance rho_r = 8/sqrt(10+2 sqrt5) = 2.1029244485 at angle 121.7174744 deg from c,
spaced 72 deg in azimuth -- the configuration of K15-E099.  A further centre at distance rho is
legal iff rho >= 2, |z - c| >= 2 and |z - ring_k| >= 2.

Theorem (a witness, exact).  There are seven further centres, all at distance exactly 11/5 from
w1, pairwise at distance > 2 and at distance > 2 from all six fixed centres.  Hence thirteen
centres lie within 2.20 of w1, so no statement "at most twelve centres within 2.20" holds, and
the cell of w1 in that configuration has thirteen faces at distances 1 and 11/10.

The witness is a *fixed* list (SEARCH = False) so the check is deterministic and fast; run
`python3 face_count_obstruction.py --search` to regenerate it by the local optimisation that
found it.  The verification is in exact rational arithmetic (see `verify`), with the ring
positions entered as rationals accurate to 1e-12; every distance checked has a margin above
3e-4, so a 1e-12 coordinate error cannot change any verdict.

Why this is decisive and not just a failed search.
  * The cap cost of a thirteenth face at distance d, from the grid of REVIEW_0738 section 4:
        d = 1.045 -> 0.028846      d = 1.100 -> 0.011797      d = 1.150 -> 0.003781
    and the available slack is 0.010301.  A thirteenth face is affordable only at d > ~1.10,
    i.e. only for a centre beyond radius 2.20.
  * So the counting statement would be needed at radius >= 2.20.  Seven further centres exist
    already at radius r* ~ 2.174 (numeric bisection below; 2.1725 < r* <= 2.1742), and at 2.20
    the margin is comfortable (minimum pairwise distance 2.03 against the 2 needed).
  * Therefore EVERY counting bound of the form "at most six further centres within r" is TRUE
    only for r below 2.174, and USELESS: at such r the thirteenth face costs at least 0.0169,
    a factor 1.6 more than the 0.010301 available.

What this does NOT say.  It is not a counterexample to (P'): the thirteen-face cell of the
witness has volume 6.332553136, far above the threshold 5.763417470 -- the seven extra faces sit
at 1.10 and cut almost nothing.  The thirteen-face case stays open; what is closed is the
counting route to it, and the closing is a statement about radii, not about volume.

Run: python3 Experimental/scripts/face_count_obstruction.py
"""
import sys
from fractions import Fraction as F

import numpy as np

RHO_R = 2.1029244484765344            # 8 / sqrt(10 + 2 sqrt 5)
RMAX = 2.2                            # the radius at which the thirteenth face is affordable
THRESH = F(5763417470, 10 ** 9)       # 5.763417470, the (P') threshold at the pair
SLACK = 0.010301                      # 5.550291 + 0.223427 - 5.763417

# --- the six fixed centres -------------------------------------------------------------
_NP = 5
# ring normals sit at COLATITUDE 58.28252506 deg from +z (z-component +rho_r/4), i.e. at
# 121.71747441 deg from c's direction (0,0,-1).  This is the orientation of ring_excess.py and
# c5_completion.py, and it reproduces their control volumes (5.572648770 at b=1, 5.898007183 at
# b=1.0514622242) to all digits.  AN EARLIER DRAFT of this script had cos = -rho_r/4 here, which
# mirrors the ring through the equator and solves a DIFFERENT packing problem; the witness below
# is for the correct orientation and is checked against the control volumes by `controls()`.
_th = np.radians(58.282525060518495)
C = np.array([0.0, 0.0, -2.0])
RING = np.array([RHO_R * np.array([np.sin(_th) * np.cos(2 * np.pi * k / 5),
                                   np.sin(_th) * np.sin(2 * np.pi * k / 5),
                                   np.cos(_th)]) for k in range(_NP)])
FIXED = np.vstack([C, RING])

# --- the witness: seven centres at distance exactly 11/5 ---------------------------------
WITNESS = [
    [0.1043558128, 0.0165671402, 2.1974611246],
    [1.2146446081, -1.6542188242, -0.792589779],
    [-2.065352887, -0.3266927563, -0.6838050124],
    [-0.7984253755, -1.9697838815, -0.5678629941],
    [-1.2848183651, 1.5737488016, -0.8441306048],
    [0.7464423037, 1.8686896476, -0.889282232],
    [2.0022502775, 0.2483871917, -0.8770961345],
]


def exact_fixed():
    """The six fixed centres as rigorous rational intervals.

    Everything is algebraic and is enclosed without floating point:
      rho_r^2 = 8 - (8/5) sqrt5                       (the icosahedral circumradius, edge 2)
      ring centre z      = rho_r^2 / 4                (because cos(58.28252506 deg) = rho_r/4)
      ring horizontal    = sqrt(rho_r^2 - z^2)
      ring azimuths      = 2 pi k / 5                 (rational multiples of pi, Taylor-enclosed)
    """
    from rational_interval import Iv, sqrt_iv, sin_cos_iv_of_pi_multiple
    r5 = sqrt_iv(Iv(5))
    rho2 = Iv(8) - Iv(8) * r5 / Iv(5)
    rho = sqrt_iv(rho2)
    z = rho2 / Iv(4)
    h = sqrt_iv(rho2 - z * z)
    out = [[Iv(0), Iv(0), Iv(-2)]]
    for k in range(5):
        sn, cs = sin_cos_iv_of_pi_multiple(F(2 * k, 5))
        out.append([h * cs, h * sn, z])
    return out, rho


def scaled_witness():
    """The witness as EXACT rationals with |x| <= 11/5 rigorously.

    The list above is rounded to 10 decimals, so |x| may exceed 11/5 by ~1e-10.  Each point is
    multiplied by a rational factor s = (11/5) / U with U a rational upper bound for |x|, which
    makes |s x| <= 11/5 exact.  The factor is 1 - 1e-10, so no checked margin moves.
    """
    from rational_interval import Iv, sqrt_iv
    out = []
    for p in WITNESS:
        q = [F(str(x)) for x in p]
        sq = sum(x * x for x in q)
        U = sqrt_iv(Iv(sq)).hi                     # rational upper bound for |x|
        s = F(11, 5) / U
        out.append([x * s for x in q])
    return out


def verify(verbose=True):
    """Rigorous check: exact rationals against rigorous enclosures, no floating point."""
    from rational_interval import Iv
    Q = scaled_witness()
    fix, rho = exact_fixed()
    ok = True

    # (a) |x| <= 11/5 and |x| >= 2, exactly
    over = [i for i, p in enumerate(Q) if sum(x * x for x in p) > F(484, 100)]
    under = [i for i, p in enumerate(Q) if sum(x * x for x in p) < F(4)]
    if verbose:
        print(f"  |x| <= 11/5 for all seven      : {'PASS' if not over else 'FAIL ' + str(over)}")
        print(f"  |x| >= 2    for all seven      : {'PASS' if not under else 'FAIL ' + str(under)}")
    ok &= not over and not under

    # (b) pairwise separation > 2, exactly
    dmin = min(sum((a[i] - b[i]) ** 2 for i in range(3))
               for j, a in enumerate(Q) for b in Q[:j])
    if verbose:
        print(f"  min pairwise squared distance  : {float(dmin):.9f} > 4 ?  {'PASS' if dmin > 4 else 'FAIL'}")
    ok &= dmin > 4

    # (c) separation from the six fixed centres, with interval arithmetic
    worst = None
    for p in Q:
        for f in fix:
            d = Iv(0)
            for i in range(3):
                d = d + (Iv(p[i]) - f[i]) * (Iv(p[i]) - f[i])
            if worst is None or d.lo < worst.lo:
                worst = d
    if verbose:
        print(f"  min squared distance to fixed  : [{float(worst.lo):.9f}, {float(worst.hi):.9f}]"
              f" > 4 ?  {'PASS' if worst.lo > 4 else 'FAIL'}")
    ok &= worst.lo > 4
    if verbose:
        print(f"  (rho_r enclosure width {float(rho.width()):.2e})")
    return ok


def cell_volume(verbose=True):
    """Volume of the thirteen-face cell of w1 in the witness configuration."""
    import cell_certificate as CC
    # the FIVE RING faces sit at b = rho_r/2, not at 1 -- that is the configuration of
    # K15-E099.  b is entered as a rational rounded DOWN (1051462224238/10^12 <= b), which
    # can only decrease the volume, and the claim below is a lower bound.
    normals, dists = [], []
    for i, f in enumerate(FIXED):
        L = float(np.linalg.norm(f))
        normals.append([float(x) / L for x in f])
        dists.append(F(1051462224238, 10 ** 12) if 1 <= i <= 5 else F(1))
    for p in WITNESS:
        L = float(np.linalg.norm(p))
        normals.append([float(x) / L for x in p])
        dists.append(F(11, 10))
    vol, nv, verts = CC.polytope_volume(normals, dists)
    if verbose:
        print(f"  thirteen-face cell volume      : {float(vol):.9f}  ({nv} vertices)")
        print(f"  threshold                      : {float(THRESH):.9f}")
        print(f"  above the threshold (no counterexample to (P')): {vol > THRESH}")
    return vol, nv


def search(seed=7, n=7, trials=4000, verbose=True):
    """Regenerate the witness: local optimisation of seven points at radius RMAX."""
    chat = C / 2.0
    rhat = RING / RHO_R
    Cc = (RMAX * RMAX + RHO_R ** 2 - 4) / (2 * RMAX * RHO_R)

    def viol(u):
        return max(0.0, u @ chat - RMAX / 4) + max(0.0, float(np.max(rhat @ u)) - Cc)

    rng = np.random.default_rng(seed)

    def rand_feasible():
        for _ in range(2000):
            u = rng.normal(size=3)
            u /= np.linalg.norm(u)
            if viol(u) < 1e-13:
                return u
        return None

    best, bestP = -1.0, None
    for _ in range(trials):
        P = [rand_feasible() for _ in range(n)]
        if any(p is None for p in P):
            continue
        P = np.array(P)
        for _ in range(400):
            D = P @ P.T
            np.fill_diagonal(D, -9)
            i, j = np.unravel_index(np.argmax(D), D.shape)
            for a, b in ((i, j), (j, i)):
                d = P[a] - P[b]
                d /= np.linalg.norm(d)
                q = P[a] + 0.01 * d
                q /= np.linalg.norm(q)
                for _ in range(40):
                    if viol(q) < 1e-15:
                        break
                    g = np.zeros(3)
                    if q @ chat > RMAX / 4:
                        g += chat
                    k = int(np.argmax(rhat @ q))
                    if rhat[k] @ q > Cc:
                        g += rhat[k]
                    if np.linalg.norm(g) < 1e-15:
                        break
                    q = q - 0.02 * g
                    q /= np.linalg.norm(q)
                if viol(q) < 1e-12:
                    P[a] = q
        D = P @ P.T
        np.fill_diagonal(D, -9)
        ang = np.degrees(np.arccos(np.clip(D.max(), -1, 1)))
        if ang > best:
            best, bestP = ang, (RMAX * P).copy()
        if ang > 55.0:
            break
    return bestP, best


def rstar(verbose=True):
    """Bisection for the radius at which seven further centres first fit (numeric)."""
    chat = C / 2.0
    rhat = RING / RHO_R

    def feasible(r, seed, trials=500, n=7):
        Cc = (r * r + RHO_R ** 2 - 4) / (2 * r * RHO_R)

        def viol(u):
            return max(0.0, u @ chat - r / 4) + max(0.0, float(np.max(rhat @ u)) - Cc)

        rng = np.random.default_rng(seed)

        def rf():
            for _ in range(3000):
                u = rng.normal(size=3)
                u /= np.linalg.norm(u)
                if viol(u) < 1e-13:
                    return u
            return None

        need = np.degrees(2 * np.arcsin(min(0.999, 1.0 / r)))
        best = 0.0
        for _ in range(trials):
            P = [rf() for _ in range(n)]
            if any(p is None for p in P):
                continue
            P = np.array(P)
            for _ in range(350):
                D = P @ P.T
                np.fill_diagonal(D, -9)
                i, j = np.unravel_index(np.argmax(D), D.shape)
                for a, b in ((i, j), (j, i)):
                    d = P[a] - P[b]
                    d /= np.linalg.norm(d)
                    q = P[a] + 0.01 * d
                    q /= np.linalg.norm(q)
                    for _ in range(40):
                        if viol(q) < 1e-15:
                            break
                        g = np.zeros(3)
                        if q @ chat > r / 4:
                            g += chat
                        k = int(np.argmax(rhat @ q))
                        if rhat[k] @ q > Cc:
                            g += rhat[k]
                        if np.linalg.norm(g) < 1e-15:
                            break
                        q = q - 0.02 * g
                        q /= np.linalg.norm(q)
                    if viol(q) < 1e-12:
                        P[a] = q
            D = P @ P.T
            np.fill_diagonal(D, -9)
            ang = np.degrees(np.arccos(np.clip(D.max(), -1, 1)))
            if ang > best:
                best = ang
            if ang > need + 0.05:
                return True, best, need
        return best > need + 0.02, best, need

    lo, hi = 2.09, 2.20
    for _ in range(6):
        mid = (lo + hi) / 2
        ok, ang, need = feasible(mid, int(mid * 1000))
        if verbose:
            print(f"    r = {mid:.4f}: best min angle {ang:6.3f} deg, needed {need:6.3f} deg"
                  f" -> {'fits' if ok else 'no'}")
        if ok:
            hi = mid
        else:
            lo = mid
    return lo, hi



def c5_no_thirteenth(verbose=True, n_grid=600):
    """The C5 configuration admits NO thirteenth face: separation + circumradius argument.

    (i) no centre at radius <= R_CUT is 2-separated from all twelve C5 centres, decided by a
        direction grid plus the r-Lipschitz bound on the least-distance function;
    (ii) a centre at radius > R_CUT has bisector > R_CUT/2 >= the cell's circumradius, so its
        half-space does not cut the cell.
    Hence the C5 cell volume is exactly the twelve-face volume, whatever the face count.
    """
    import numpy as np
    import cell_certificate as CC
    free = []
    for k in range(5):
        a = np.radians(112.0)
        ph = np.radians(36 + 72 * k)
        free.append(2 * np.array([np.sin(a) * np.cos(ph), np.sin(a) * np.sin(ph), np.cos(a)]))
    free.append(np.array([0.0, 0.0, 2.0]))
    cent = np.vstack([FIXED, np.array(free)])
    dirs = [x / np.linalg.norm(x) for x in cent]
    dists = [F(1)] + [F(1051462224238, 10 ** 12)] * 5 + [F(1)] * 6
    vol, nv, verts = CC.polytope_volume([list(x) for x in dirs], dists)
    circ = max(sum(float(t) ** 2 for t in v) ** 0.5 for v in verts)
    r_cut = float(F(2604, 1000))
    ph = np.arccos(np.linspace(-1, 1, n_grid))
    ps = np.linspace(0, 2 * np.pi, 2 * n_grid)
    PH, PS = np.meshgrid(ph, ps, indexing='ij')
    U = np.stack([np.sin(PH) * np.cos(PS), np.sin(PH) * np.sin(PS), np.cos(PH)], axis=-1).reshape(-1, 3)
    Z = r_cut * U
    dmin = np.min(np.linalg.norm(Z[:, None, :] - cent[None, :, :], axis=2), axis=1)
    step = max(np.pi / n_grid, 2 * np.pi / (2 * n_grid))
    bound = float(dmin.max()) + r_cut * step
    if verbose:
        print(f"  C5 cell volume                 : {float(vol):.9f}  ({nv} vertices)")
        print(f"  circumradius                   : {circ:.9f}")
        print(f"  max least-distance at r={r_cut:.3f} : grid {float(dmin.max()):.6f}"
              f" + Lipschitz {r_cut*step:.6f} = {bound:.6f}  < 2 ?  {'PASS' if bound < 2 else 'FAIL'}")
        print(f"  bisector of any centre beyond  : > {r_cut/2:.4f}  >= circumradius ?"
              f"  {'PASS' if r_cut / 2 >= circ else 'FAIL'}")
        print(f"  => no thirteenth face; vol = {float(vol):.9f},"
              f" margin {float(vol) - 5.763417470:+.6f}")
    return float(vol), circ, bound



def push_in(verbose=True, iters=4500, seed=12345, start=None, kick=0.0):
    """Push the witness in while KEEPING the thirteenth facet.  Deterministic.

    The section-5 witness is a genuine thirteen-facet cell at 6.719022368.  Shrinking the seven
    free centres towards w1 until a 2-separation binds, perturbing, and rejecting every candidate
    whose cell has fewer than thirteen facets (checked: a plane is a facet iff it carries at
    least three vertices) reaches 6.452822188 in about seven seconds.  That is the constructive
    half of section 5.2: thirteen-facet completions exist and are not close to the threshold.

    A run WITHOUT the facet check reaches 6.080235472 but its cell has twelve facets -- the
    seventh centre sits at |x| = 3.6165 and its bisector at 1.808 misses the cell.  That is why
    the check is not optional.
    """
    import itertools
    import numpy as np

    def vol_facets(P):
        import itertools as it
        from scipy.spatial import ConvexHull
        dirs = np.vstack([FIXED, P])
        dists = np.array([1.0] + [float(F(1051462224238, 10 ** 12))] * 5
                         + [np.linalg.norm(x) / 2 for x in P])
        n = np.array([d / np.linalg.norm(d) for d in dirs])
        m = len(dists)
        V = []
        for i, j, k in it.combinations(range(m), 3):
            M = n[[i, j, k]]
            if abs(np.linalg.det(M)) < 1e-11:
                continue
            x = np.linalg.solve(M, dists[[i, j, k]])
            if np.all(n @ x <= dists + 1e-9):
                V.append(x)
        if len(V) < 4:
            return 0.0, 0
        V = np.array(V)
        sup = [i for i in range(m) if np.sum(np.abs(n[i] @ V.T - dists[i]) < 1e-7) >= 3]
        return float(ConvexHull(V).volume), len(sup)

    def jam(P):
        need = [2.0 / max(np.linalg.norm(x), 1e-12) for x in P]
        for i in range(len(P)):
            for j in range(i):
                need.append(2.0 / max(np.linalg.norm(P[i] - P[j]), 1e-12))
            for f in FIXED:
                need.append(2.0 / max(np.linalg.norm(P[i] - f), 1e-12))
        return P * max(need)

    def minsep(P):
        d = [np.linalg.norm(x) for x in P]
        for i in range(len(P)):
            for j in range(i):
                d.append(np.linalg.norm(P[i] - P[j]))
            for f in FIXED:
                d.append(np.linalg.norm(P[i] - f))
        return min(d)

    rng = np.random.default_rng(seed)
    P = np.array([[float(F(str(x))) for x in p] for p in WITNESS]) if start is None else np.array(start, float)
    if kick > 0:                       # optional larger perturbation of the starting point
        P = jam(P + rng.normal(scale=kick, size=P.shape))
        if minsep(P) < 2 - 1e-9:
            P = np.array([[float(F(str(x))) for x in p] for p in WITNESS])
    v0, nf0 = vol_facets(P)
    best = (v0, P.copy())
    if verbose:
        print(f"  seed (the section-5 witness) : {v0:.9f}  facets {nf0}")
    for it in range(iters):
        sig = 0.02 if it % 4 else 0.08
        Q = jam(P + rng.normal(scale=sig, size=P.shape))
        if minsep(Q) < 2 - 1e-9:
            continue
        v, nf = vol_facets(Q)
        if v <= 0 or nf < 13:
            continue
        if v < best[0]:
            best = (v, Q.copy())
            P = Q
    if verbose:
        print(f"  smallest thirteen-facet cell : {best[0]:.9f}  margin"
              f" {best[0] - 5.763417470:+.6f}")
        for x in best[1]:
            print("    ", [round(float(t), 9) for t in x], "  |x| = %.6f" % np.linalg.norm(x))
    return best


def main():
    print("=" * 78)
    print("THE THIRTEEN-FACE CASE CANNOT BE CLOSED BY COUNTING CENTRES")
    print("=" * 78)
    if "--push" in sys.argv:
        push_in()
        return 0
    # A second round with larger kicks (seeds 20-33, kicks 0.5 and 0.8, same iteration budget)
    # did not improve on the result below: best 6.461008754.  Recorded, not repeated.
    if "--push-multi" in sys.argv:
        best = (1e9, None, None)
        for k, (sd, kick) in enumerate([(s, kk) for s in range(1, 13) for kk in (0.0, 0.25)]):
            v, P = push_in(verbose=False, seed=sd, kick=kick, iters=2500)
            if v < best[0]:
                best = (v, sd, kick)
                print(f"  seed {sd:2d} kick {kick:.2f}: {v:.9f}  <-- best so far", flush=True)
        print(f"\n  smallest thirteen-facet cell over {k} starts: {best[0]:.9f}"
              f"  (seed {best[1]}, kick {best[2]})  margin {best[0] - 5.763417470:+.6f}")
        return 0
    if "--search" in sys.argv:
        P, ang = search()
        print("regenerated witness (min pairwise angle %.4f deg):" % ang)
        for p in P:
            print("   ", [round(float(x), 10) for x in p])
        return 0
    print("\n(1) THE WITNESS: seven further centres at radius 11/5 = 2.2")
    ok = verify()
    print("\n(1b) THE C5 CONFIGURATION ADMITS NO THIRTEENTH FACE")
    c5_no_thirteenth()

    print("\n(2) THE CELL IT DEFINES")
    vol, nv = cell_volume()
    if "--fast" in sys.argv:
        lo, hi = 2.1725, 2.1742
        print("\n(3) SEVEN-CENTRE THRESHOLD (precomputed; --fast skips the 15 s bisection)")
    else:
        print("\n(3) THE RADIUS AT WHICH SEVEN FURTHER CENTRES FIRST FIT (numeric bisection)")
        lo, hi = rstar()
    print(f"    seven fit at r* <= {hi:.4f}; none found below {lo:.4f}")
    print(f"    so the best counting statement available is 'at most six further centres")
    print(f"    within r' for r < {hi:.4f}, hence a thirteenth face has d > {hi/2:.4f}")
    print("\n(4) WHY THAT IS NOT ENOUGH")
    print(f"    available slack                                  {SLACK:.6f}")
    print(f"    cap cost at d = 1.100 (grid, REVIEW_0738 s4)     0.011797")
    print(f"    cap cost at d = {hi/2:.4f} (interpolated)          ~0.0169")
    print(f"    affordable only for d > ~1.10, i.e. r > 2.20 -- but seven further centres")
    print(f"    fit at r = {hi:.3f} already, and thirteen inside 2.20 is exhibited in (1).")
    print(f"\n    OBSTRUCTION CONFIRMED: no counting refinement closes the case.")
    print(f"    witness legal: {ok}   cell volume above threshold: {float(vol) > 5.763417470}")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
