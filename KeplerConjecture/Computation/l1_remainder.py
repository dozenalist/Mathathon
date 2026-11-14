#!/usr/bin/env python3
"""K15-C147 -- M-CERT-002: the bounded pilot for L1' (and its obstruction).

WHAT L1' SAYS, CORRECTLY (three corrections to the 0738 spec, all forced)

  (i) QUOTIENT.  vol is exactly invariant under rotating all 12 normals, so
      "vol - V_dod >= c*sum(theta^2)" is FALSE for every c>0.  The statement is
      about the distance to the 3-dimensional rotation tangent space:
          d(theta) := |theta - P_R theta|,   P_R = projector onto Rot.
  (ii) NO POSITIVE MINIMUM ON A BALL THROUGH 0.  At theta=0 both sides vanish, so
      "min over the ball of (vol - V_dod - c d^2) > 0" is impossible.  Two sound
      reformulations, both equivalent to what the argument needs:
          (A) RATIO:   (vol - V_dod)/d^2 >= c   for 0 < d <= theta_max;
          (B) SPHERE:  min over {d = theta_max} of (vol - V_dod) >= c*theta_max^2.
      (B) has no zero set and is compact, so it is the certifiable form.
  (iii) ENTRY.  L1' is LOCAL.  The implication "vol <= V_dod+eta => d <= theta_max"
      also needs the GLOBAL-TO-LOCAL ENTRY: the sublevel set {vol <= V_dod+eta} is
      confined to the ball.  Fejes Toth supplies the global minimum V_dod and its
      equality case but NO MODULUS, so the entry is a separate obligation (C147).
      Certifying (B) on a sphere does NOT discharge it.

WHAT THIS PILOT PROVES (soundly, on the ball d <= theta_max)

  T1  Feasibility: every triple of normals keeps |det| > 0 (no vertex at infinity).
  T2  Type: the 20 active triples stay active and the 140 inactive ones stay slack,
      so the cell has exactly 12 facets and vol is smooth on the ball.
  Both are analytic: the base values are computed exactly here, and the derivatives
  are bounded by |dA| <= 1 (a unit vector rotating at unit rate) and
  |A^{-1}| <= 1/|det|min, giving |dv| <= |A^{-1}|^2 |v|.  No interval arithmetic is
  needed because the margins (1.24 and 0.47) dwarf the O(theta) motion (< 0.2).

WHAT IT DOES NOT PROVE

  The value bound (B).  Two routes, both quantified here:
    * Taylor: vol >= V_dod + (lam/2)d^2 - (M3/6)d^3 with lam the quotient Hessian's
      smallest eigenvalue and M3 a rigorous third-derivative bound.  Sufficient iff
      M3 <= 6((lam/2) - c)/theta_max.  The pilot measures lam and M3 numerically and
      reports the REQUIRED M3 -- the rigorous bound is the one missing ingredient.
    * Covering: sample the sphere and subtract L*(covering radius), L a Lipschitz
      bound on vol.  --obstruction prints why this is infeasible in 21 dimensions.

Exit codes: 0 = everything certified (never yet); 1 = T1/T2 certified, value bound
NOT certified (the honest current state); 2 = a sound part FAILED; 3 = the negative
control was not rejected, i.e. the pilot is inert.

Usage:
  python3 l1_remainder.py --certify                 # full report, exit 1
  python3 l1_remainder.py --certify --c 0.30        # negative control: must fail (3)
  python3 l1_remainder.py --margins                 # T1/T2 only
  python3 l1_remainder.py --obstruction             # covering count only
"""
import argparse
import itertools
import sys

import numpy as np

PHI = (1 + 5 ** 0.5) / 2
V_DOD = 5.550291028515510
COVER = np.sqrt(30 * np.sqrt(5) + 75) / 15      # cos(rho_c) = 0.7946544723
THETA_MAX = 0.0446544723                        # cos(rho_c) - 3/4, from d <= 3


def normals():
    us = []
    for a in (-1, 1):
        for b in (-1, 1):
            us += [[0, a / PHI, b], [a / PHI, b, 0], [b, 0, a / PHI]]
    u = np.array(us, float)
    u /= np.linalg.norm(u, axis=1)[:, None]
    return np.unique(np.round(u, 12), axis=0)


U = normals()
TRIPLES = list(itertools.combinations(range(12), 3))


def tangent_basis():
    rng = np.random.default_rng(1)
    dirs = []
    for u in U:
        t1 = rng.normal(size=3)
        t1 -= u * (u @ t1)
        t1 /= np.linalg.norm(t1)
        dirs.append((t1, np.cross(u, t1)))
    return dirs


DIRS = tangent_basis()


def rotation_projector():
    """Projector onto the 3-dim space spanned by the global-rotation motions."""
    B = []
    for axis in np.eye(3):
        v = np.zeros(24)
        for j in range(12):
            w = np.cross(axis, U[j])
            v[2 * j] = w @ DIRS[j][0]
            v[2 * j + 1] = w @ DIRS[j][1]
        B.append(v)
    Q, _ = np.linalg.qr(np.array(B).T)
    return Q @ Q.T


P_ROT = rotation_projector()


def perturb(theta):
    n = []
    for j in range(12):
        m = U[j] + theta[2 * j] * DIRS[j][0] + theta[2 * j + 1] * DIRS[j][1]
        n.append(m / np.linalg.norm(m))
    return np.array(n)


def vertices(N, tol=1e-10):
    out = []
    for t in TRIPLES:
        A = N[list(t)]
        d = np.linalg.det(A)
        if abs(d) < 1e-13:
            continue
        x = np.linalg.solve(A, np.ones(3))
        if np.all(N @ x <= 1 + tol):
            out.append((t, x, d))
    return out


def faces(N, verts, tol=1e-9):
    """For each normal, the (cyclically ordered) vertices on its face."""
    out = []
    for i in range(12):
        idx = [k for k, (t, x, d) in enumerate(verts) if abs(x @ N[i] - 1) < tol]
        if len(idx) < 3:
            continue
        e1 = U[i]
        a = np.cross(e1, [1.0, 0, 0])
        if np.linalg.norm(a) < 0.3:
            a = np.cross(e1, [0, 1.0, 0])
        a /= np.linalg.norm(a)
        b = np.cross(e1, a)
        ang = [np.arctan2(verts[k][1] @ b, verts[k][1] @ a) for k in idx]
        out.append([k for _, k in sorted(zip(ang, idx))])
    return out


_V0 = vertices(U)
_F0 = faces(U, _V0)


def volume(N):
    """Exact-in-structure volume: sum of tetrahedra over the (fixed) triangulation."""
    V = vertices(N)
    if len(V) != 20:
        return None
    # index by triple for a stable mapping
    pos = {t: k for k, (t, x, d) in enumerate(V)}
    tot = 0.0
    for f in _F0:
        idx = [pos[V[k][0]] for k in f]
        for m in range(1, len(idx) - 1):
            a, b, c = V[idx[0]][1], V[idx[m]][1], V[idx[m + 1]][1]
            tot += np.linalg.det(np.array([a, b, c])) / 6.0
    return tot


def margins_at_zero():
    """Classify ALL triples, not just the feasible ones.

    `vertices()` returns only the 20 feasible vertices, so computing the slack over
    its output makes every slack negative and the inactive set empty -- the first
    version of this function failed for exactly that reason.  The inactive triples
    are the ones a vertex would come FROM, so they must be enumerated separately.
    """
    dets = []
    act, inact = [], []
    for t in TRIPLES:
        A = U[list(t)]
        d = abs(np.linalg.det(A))
        if d < 1e-13:
            continue
        dets.append(d)
        x = np.linalg.solve(A, np.ones(3))
        others = [j for j in range(12) if j not in t]
        s = max(x @ U[j] - 1.0 for j in others)
        (act if s <= 1e-9 else inact).append(s)
    alldet = [abs(np.linalg.det(U[list(t)])) for t in TRIPLES
              if abs(np.linalg.det(U[list(t)])) > 1e-13]
    return dict(active=len(act), inactive=len(inact),
                min_inactive_slack=min(inact), min_det=min(act) if act else min(dets),
                min_det_all=min(alldet), n_triples=len(alldet))


def certify_margins(theta_max, verbose=True):
    """T1 and T2, soundly.  Derivatives: |dA| <= 1 per entry, |dv| <= |A^-1|^2 |v|."""
    m = margins_at_zero()
    rmax = 1.258408572                              # dodecahedron circumradius
    inv = 1.0 / m["min_det"]                        # |A^-1| <= 1/min|det|
    dv = inv * inv * rmax                            # vertex motion per unit theta
    feas = m["min_det_all"] - 3.0 * theta_max        # Hadamard on the determinants
    type_margin = m["min_inactive_slack"] - (dv + 1.0) * theta_max
    ok = (feas > 0) and (m["active"] == 20) and (type_margin > 0)
    if verbose:
        print("T1 feasibility (no vertex at infinity)")
        print(f"   min |det| over all {m['n_triples']} triples at theta=0 : {m['min_det_all']:.9f}")
        print(f"   Hadamard slack at theta_max                        : {feas:.6f}  "
              f"{'OK' if feas > 0 else 'FAIL'}")
        print("T2 type (exactly 12 facets, vol smooth on the ball)")
        print(f"   active triples {m['active']} / inactive {m['inactive']} at theta=0")
        print(f"   min inactive slack at theta=0                      : {m['min_inactive_slack']:.9f}")
        print(f"   vertex motion per unit theta <= |A^-1|^2 R        : {dv:.4f}")
        print(f"   slack left at theta_max                            : {type_margin:.6f}  "
              f"{'OK' if type_margin > 0 else 'FAIL'}")
    return ok, m, feas, type_margin


def quotient_dirs(n, seed=0, rng=None):
    """Unit directions in the quotient (orthogonal to the rotation modes)."""
    r = rng or np.random.default_rng(seed)
    out = []
    Q = np.linalg.eigh(P_ROT)[1][:, :3]
    for _ in range(n):
        u = r.normal(size=24)
        u -= Q @ (Q.T @ u)
        nu = np.linalg.norm(u)
        if nu > 1e-9:
            out.append(u / nu)
    return out


def ratio_and_m3(theta_max, c, ndir=400, seed=0):
    """Minimum of (vol - V_dod)/d^2 over sampled quotient directions, and M3.

    The value bound is driven by the RATIO, not by a finite-difference Hessian: the
    24x24 FD Hessian has a ~1e-3 rotation leakage (its three null directions come out
    at -1.7e-3 rather than 0), which makes any eigenvalue near zero meaningless and an
    enclosure through H unreliable.  The ratio is robust and is what the argument uses.
    """
    v0 = volume(U)
    best = (1e9, None)
    for u in quotient_dirs(ndir, seed):
        v = volume(perturb(u * theta_max))
        if v is None:
            continue
        r = (v - v0) / theta_max ** 2
        if r < best[0]:
            best = (r, u)
    ratio_min, u = best
    # cubic coefficient along the worst direction
    c3s = []
    for t in (0.02, 0.03):
        vp = volume(perturb(u * t))
        d2 = (vp - 2 * v0 + volume(perturb(-u * t))) / t ** 2
        c3s.append((vp - v0 - 0.5 * d2 * t * t) / t ** 3)
    m3 = 6.0 * abs(float(np.mean(c3s)))
    return ratio_min, m3


def certified_taylor(theta_max, c, ratio_min, m3_measured):
    """ratio_min - M3*theta_max/6 >= c  =>  sufficient (ratio_min plays the role of lam/2)."""
    need = 6.0 * (ratio_min - c) / theta_max
    return need, need >= m3_measured


def certified_radius():
    """The largest theta on which T1 and T2 are proved by this pilot."""
    m = margins_at_zero()
    inv = 1.0 / m["min_det"]
    dv = inv * inv * 1.258408572
    t1 = m["min_det_all"] / 3.0                      # Hadamard on the determinants
    t2 = m["min_inactive_slack"] / (dv + 1.0)        # the type margin
    return min(t1, t2), t1, t2


def delta0_ladder(c, ratio_min, theta_cap=(0.25, 1.0, 10.0, 100.0, 1000.0),
                  m3_bounds=(0.25, 1.0, 10.0, 100.0, 1000.0)):
    """What delta_0 a given rigorous M3 bound would buy.

    delta_0 = 2 V_dod * c * theta_max^2 with theta_max = 6(ratio_min - c)/M3, so
    delta_0 ~ M3^-2 -- but theta_max may never exceed the radius on which T1/T2 are
    certified, so the ladder is CAPPED.  Without the cap it reports delta_0 for balls
    it has not certified (a 1.75 rad ball, where the type is long gone).
    """
    rows = []
    for m in m3_bounds:
        th = min(6.0 * (ratio_min - c) / m, theta_cap)
        eta = c * th * th
        rows.append((m, th, eta, 2.0 * V_DOD * eta))
    return rows


def obstruction(theta_max, c, ndir_note=True):
    L = 16.650873086 * 1.31          # surface area * circumradius: |grad vol| bound
    slack = 0.24 * theta_max ** 2 - c * theta_max ** 2
    if slack <= 0:
        return None
    r = slack / L
    return L, slack, r, (1.0 / r) ** 20


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certify", action="store_true")
    ap.add_argument("--margins", action="store_true")
    ap.add_argument("--obstruction", action="store_true")
    ap.add_argument("--theta", type=float, default=THETA_MAX)
    ap.add_argument("--c", type=float, default=0.13)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--m3-bound", type=float, default=None,
                    help="a RIGOROUS third-derivative bound from an independent "
                         "interval computation; without it the value bound cannot "
                         "be certified, only shown plausible")
    a = ap.parse_args()

    print(f"l1_remainder.py -- theta_max={a.theta:.8f}  c={a.c:.3f}  V_dod={V_DOD:.9f}")
    print(f"   quotient: ||P_Rot|| = {np.linalg.norm(P_ROT):.3f} (3 dims removed of 24)")

    ok, m, feas, type_margin = certify_margins(a.theta)
    if a.margins:
        return 0 if ok else 2

    ratio_min, m3 = ratio_and_m3(a.theta, a.c, seed=a.seed)
    print("\nVALUE BOUND (not certified by this pilot)")
    print(f"   min quotient ratio (vol - V_dod)/d^2 over sampled dirs = {ratio_min:.6f}")
    print(f"   measured M3 = 6|c3| along the worst direction          = {m3:.6f}")
    need, enough = certified_taylor(a.theta, a.c, ratio_min, m3)
    print(f"   Taylor sufficient iff M3 <= 6(ratio_min - c)/theta_max = {need:.4f}")
    print(f"   measured M3 {m3:.4f} vs required {need:.4f} -> "
          f"{'PLAUSIBLE (factor %.1f of headroom)' % (need / m3) if m3 > 0 and need > m3 else 'NOT SUFFICIENT'}")

    if a.obstruction or a.certify:
        ob = obstruction(a.theta, a.c)
        print("\nCOVERING ROUTE (why it is not used)")
        if ob is None:
            print("   no covering can work: the target exceeds the quadratic term itself")
        else:
            L, slack, r, n = ob
            print(f"   Lipschitz bound L = {L:.2f} (surface area x circumradius)")
            print(f"   slack = (0.24 - c) theta_max^2 = {slack:.3e}")
            print(f"   net radius needed r = slack/L = {r:.3e}")
            print(f"   points to cover S^20 at that radius: ~ (1/r)^20 = {n:.3e}  -> infeasible")

    print("\nWHAT A RIGOROUS M3 BOUND WOULD BUY (delta0 ~ M3^-2)")
    print("   M3 bound   theta_max      eta          delta0")
    tcert, t1c, t2c = certified_radius()
    print(f"   certified ball radius (T1 {t1c:.4f}, T2 {t2c:.4f}) = {tcert:.4f}")
    for m, th, eta, d0 in delta0_ladder(a.c, ratio_min, theta_cap=tcert):
        print(f"   {m:8.2f}   {th:.3e}    {eta:.3e}   {d0:.3e}")
    print(f"   capped at the certified radius, so any M3 <= {6.0*(ratio_min-a.c)/tcert:.2f} reaches the ceiling;")
    print(f"   the measured M3 is {m3:.4f}, i.e. a factor {6.0*(ratio_min-a.c)/tcert/max(m3,1e-12):.0f} of headroom before the cap binds")
    print("   Elementary-partial route: the DIRECTIONAL third derivative is bounded by")
    print("   24^{3/2} = 118 times the largest elementary third partial, so a rigorous")
    print("   computation needs elementary partials <= %.3f to reach the required M3."
          % (need / 118.0))

    print("\nNEGATIVE CONTROL")
    lam_half = ratio_min
    inert = a.c < lam_half
    print(f"   c = {a.c:.3f} vs measured ratio_min = {lam_half:.6f}: "
          f"{'accepted (c is below the measured curvature)' if inert else 'REJECTED (c exceeds the curvature)'}")

    if not ok:
        print("\nVERDICT: FAIL — a sound part (T1/T2) did not hold")
        return 2
    if not inert:
        print("\nVERDICT: INERT — the pilot accepted a constant above the measured curvature")
        return 3
    if a.m3_bound is not None:
        if a.m3_bound <= need:
            print(f"\nVERDICT: CERTIFIED (Taylor) with the supplied rigorous M3 bound "
                  f"{a.m3_bound:.4f} <= {need:.4f}")
            print("   NOTE: the global-to-local entry (C147) is still a separate obligation.")
            return 0
        print(f"\nVERDICT: NOT CERTIFIED — the supplied M3 bound {a.m3_bound:.4f} "
              f"exceeds the required {need:.4f}")
        return 1
    print("\nVERDICT: T1/T2 CERTIFIED; value bound NOT certified.")
    print("   Missing ingredient: a rigorous enclosure of M3 (or of the Hessian entries)")
    print("   with M3 <= %.4f.  Measured M3 = %.4f, so the headroom is a factor %.1f." % (need, m3, need / m3))
    print("   The global-to-local entry (C147) is a separate obligation and is not addressed here.")
    return 1


def self_test():
    """The pilot must return the RIGHT exit code for each question, and the control
    must be able to fail.  Without this, a pilot that always exits 1 looks the same as
    a pilot that works."""
    import subprocess
    here = __file__
    cases = [
        (["--margins"], 0, "T1/T2 margins certify"),
        (["--certify", "--c", "0.30", "--seed", "3"], 3, "negative control rejected (inert)"),
        (["--certify", "--seed", "3", "--m3-bound", "9.0"], 0, "certifies with a tight bound"),
        (["--certify", "--seed", "3", "--m3-bound", "20.0"], 1, "rejects a loose bound"),
        (["--certify", "--seed", "3"], 1, "uncertified without a rigorous M3"),
        (["--certify", "--theta", "0.30", "--seed", "3"], 2, "a ball beyond the certified radius FAILS"),
    ]
    ok = True
    for argv, want, why in cases:
        r = subprocess.run([sys.executable, here] + argv, capture_output=True, text=True)
        good = (r.returncode == want)
        print(f"  [{'ok' if good else 'FAIL'}] exit {r.returncode} (want {want}) -- {why}")
        ok = ok and good
    tcert, t1c, t2c = certified_radius()
    inside = tcert > THETA_MAX
    print(f"  [{'ok' if inside else 'FAIL'}] certified radius {tcert:.4f} exceeds the "
          f"default ball {THETA_MAX:.4f}")
    print("  SELF-TEST:", "PASS" if (ok and inside) else "FAIL")
    return 0 if (ok and inside) else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
