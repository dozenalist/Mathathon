#!/usr/bin/env python3
"""K15-X-C070 -- independent recheck of K15-C102's nearest admissible 13th centre.

Written because the previous worker block recorded (as a pending entry) that C102's
constant 3.206870905 was 0.881% too high and that the true minimum was 3.178617889
"at" C102's own direction.  That comparison is a scale confusion: 3.178617889 is the
value at rho = 2, and the problem is *not* scale invariant (the contact distance 2 is
fixed while rho varies -- case (B) of K15-C101 lives on rho in [2, 4]).  This script
recomputes at rho = 2.09 and reproduces C102's number to 1e-9.

What is checked:
  1. the twelve contacts at rho = 2.09 are 2-separated (edge 2.19770.. > 2);
  2. the admissible-radius function is the one C102 states, and since
     r+(c) = c + sqrt(c^2 - (rho^2-4)) is strictly increasing in c on its domain,
     min_u max_i r+(<u,x_i>) = max(rho, r+(rho * kappa)) with kappa the covering
     radius cosine of the icosahedral vertex set -- so the minimisation is exactly
     a covering-radius problem, and the face centres (dodecahedron vertices) are
     where it is attained;
  3. three independent routes to the minimum agree: exact face-centre evaluation,
     2e6 random directions, Nelder-Mead from 32 starts;
  4. the rho = 2 value (3.178618) and the reason it is not the rho = 2.09 value;
  5. two defects in Computation/nearest_13th.py that do NOT affect the constant:
     its "dodecahedral (hole)" list is a 12-point set, not the 20 face centres, and CLAIMS.md calls
     the minimising direction an edge midpoint when it is a face centre.

Exit 0 iff the constant is reproduced and the conclusion's margin holds.
"""
import numpy as np
from mpmath import mp, mpf, sqrt, cos, pi

mp.dps = 30
RHO = mpf(209) / 100
PHI = (1 + sqrt(mpf(5))) / 2
KAPPA = sqrt((5 + 2 * sqrt(mpf(5))) / 15)      # cos of an icosahedral face's angular radius


def ico_dirs():
    """12 unit vertex directions of the icosahedron, (0,+-1,+-phi) etc."""
    v = []
    for a in (-1, 1):
        for b in (-PHI, PHI):
            v += [(0, a, b), (a, b, 0), (b, 0, a)]
    V = np.array(sorted(set(map(tuple, np.round(np.array(v, float), 12)))), float)
    return V / np.linalg.norm(V, axis=1)[:, None]


def dod_dirs():
    """20 unit face-centre directions = dodecahedron vertices, as normalised sums of
    the three mutually adjacent vertices of each icosahedral face."""
    D = ico_dirs()
    edge = 2.0 / np.linalg.norm([0, 1, PHI])          # unit-radius edge length = 2/sqrt(1+phi^2)
    E = np.linalg.norm(D[:, None] - D[None], axis=2)
    out = []
    for i in range(12):
        for j in range(i + 1, 12):
            if abs(E[i, j] - edge) > 1e-9:
                continue
            for k in range(j + 1, 12):
                if abs(E[i, k] - edge) < 1e-9 and abs(E[j, k] - edge) < 1e-9:
                    v = D[i] + D[j] + D[k]
                    out.append(tuple(v / np.linalg.norm(v)))
    W = np.array(sorted(set(map(tuple, np.round(out, 12)))), float)
    return W / np.linalg.norm(W, axis=1)[:, None]


def rplus_np(c, rho=2.09):
    fl = rho * rho - 4.0
    disc = c * c - fl
    out = np.full_like(c, -np.inf)
    m = disc >= 0
    out[m] = c[m] + np.sqrt(disc[m])
    return out


def rmin_np(U, X, rho=2.09):
    return np.maximum(rplus_np(U @ X.T, rho).max(axis=1), rho)


def rmin_exact(u, X, rho=RHO):
    """Same function in mpmath, single direction."""
    c = max(sum(mpf(u[k]) * X[i][k] for k in range(3)) for i in range(12))
    fl = rho * rho - 4
    r = c + sqrt(c * c - fl)
    return max(r, rho)


def main():
    D = ico_dirs()
    Xn = D * 2.09
    assert len(D) == 12

    # 1. separation of the twelve contacts
    Dm = np.linalg.norm(Xn[:, None] - Xn[None], axis=2)
    iu = np.triu_indices(12, 1)
    dmin = float(Dm[iu].min())
    print(f"[1] twelve contacts at rho = 2.09: min mutual distance {dmin:.9f}  (>= 2: {dmin >= 2})")
    assert dmin >= 2 - 1e-12

    # 2. the minimum over directions: r+ monotone => covering radius
    Dd = dod_dirs()
    assert len(Dd) == 20
    # every face centre must be max-distance from the vertices: check the angle
    cosface = float(np.max(Dd @ D.T))
    print(f"[2] max_i <u_face, x_i_hat> at a face centre = {cosface:.12f}"
          f"   (kappa = {float(KAPPA):.12f})")
    assert abs(cosface - float(KAPPA)) < 1e-12

    # 2b. a three-line proof that max_i <u, x_i_hat> >= kappa for *every* u.
    # On a face triangle with unit vertices a1,a2,a3 (pairwise dot m = 1/sqrt5),
    # write u = sum l_k a_k / |sum l_k a_k| with l_k >= 0, sum l_k = 1, and t = max l_k.
    # Then max_j <u,a_j> = ((1-m) t + m)/|sum l a| and |sum l a|^2 = (1-m) sum l_k^2 + m
    # <= (1-m) t + m.  Since t >= 1/3 and w := (1-m)t + m is increasing with
    # w(1/3) = (1+2m)/3 = kappa^2, we get max_j <u,a_j> >= w/sqrt(w) >= kappa.
    m = 1 / sqrt(mpf(5))
    assert abs(KAPPA ** 2 - (1 + 2 * m) / 3) < mpf(10) ** -28
    worst = min(float((1 - float(m)) * t + float(m)) for t in np.linspace(1 / 3, 1, 2001))
    print(f"[2b] kappa^2 = (1+2m)/3 exactly (m = 1/sqrt5);  min_t w(t) over [1/3,1] = "
          f"{worst:.12f} = kappa^2 = {float(KAPPA**2):.12f}")
    assert worst >= float(KAPPA ** 2) - 1e-15
    print("     => max_i <u,x_i_hat> >= kappa for every u, equality only at the 20 face centres;")
    print("        the minimisation is exactly a covering-radius problem, proved, not sampled.")

    # 3. three routes
    val_face = rmin_exact([float(x) for x in Dd[0]], Xn)
    U = np.vstack([Dd] + [D])
    vals = rmin_np(U, Xn)
    rng = np.random.default_rng(20261114)
    best, bu = np.inf, None
    for _ in range(40):
        S = rng.normal(size=(50000, 3))
        S /= np.linalg.norm(S, axis=1)[:, None]
        r = rmin_np(S, Xn)
        j = int(np.argmin(r))
        if r[j] < best:
            best, bu = r[j], S[j]
    print(f"[3] face-centre value (mpmath, dps=30) : {float(val_face):.12f}")
    print(f"    min over the 32 symmetric dirs      : {vals.min():.12f}")
    print(f"    random 2e6 directions               : {best:.9f}")

    from scipy.optimize import minimize

    def f(v):
        v = v / np.linalg.norm(v)
        return float(rmin_np(v[None, :], Xn)[0])

    glob, gu = np.inf, None
    for s in [bu] + list(Dd) + list(D):
        res = minimize(f, s, method='Nelder-Mead',
                       options=dict(xatol=1e-12, fatol=1e-14, maxfev=20000))
        if res.fun < glob:
            glob, gu = res.fun, res.x / np.linalg.norm(res.x)
    print(f"    after Nelder-Mead from 32 starts    : {glob:.9f}  dir {np.round(gu, 9)}")

    claimed = 3.206870905
    err = abs(float(val_face) - claimed)
    print(f"[4] C102 claims {claimed}; reproduced up to {err:.2e}")
    assert err < 1e-8, err
    assert abs(glob - float(val_face)) < 1e-7

    # the closed form: rho*kappa + sqrt(rho^2 kappa^2 - rho^2 + 4)
    r = RHO * KAPPA + sqrt(RHO * RHO * KAPPA * KAPPA - RHO * RHO + 4)
    print(f"    closed form rho*kappa + sqrt(...)   : {float(r):.12f}")
    assert abs(float(r) - float(val_face)) < 1e-12

    # 4. the rho = 2 value that the previous block compared against this one
    X2 = D * 2.0
    v2 = rmin_np(Dd, X2, rho=2.0).min()   # rho = 2 *throughout*: contacts and floor
    print(f"[5] same function at rho = 2 (x_i at radius 2): {float(v2):.9f}"
          f"   <- the '3.178617889' of the handover")
    print(f"    ratio 3.206871/3.178618 = {3.206870905 / float(v2):.9f}, rho-ratio = 1.045 -- "
          f"not equal: the problem is not scale invariant")
    print(f"    (at rho = 2 the floor is 2 and the discriminant is c^2-0, so r+ = 2c; the")
    print(f"     contact distance 2 equals the radius there, at rho = 2.09 it does not)")
    assert abs(float(v2) - 3.178617889) < 1e-8

    # 5. Main's "dodecahedral (hole)" block is not the face-centre set
    p = 1 / PHI
    dd = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            dd += [(0, s1 / p, s2), (s1 / p, s2, 0), (s2, 0, s1 / p)]
    Ddmain = np.array(sorted(set(map(tuple, np.round(np.array(dd, float), 12)))), float)
    Ddmain /= np.linalg.norm(Ddmain, axis=1)[:, None]
    maxdot = float(np.abs(Ddmain @ D.T).max(axis=1).max())
    print(f"[6] Main's dd block: {len(Ddmain)} directions (labelled 'dodecahedral (hole)'), "
          f"max_i <u, x_i_hat> = {maxdot:.9f}")
    print(f"    a face centre has max_i <u, x_i_hat> = kappa = {float(KAPPA):.9f}; "
          f"there are 20, not 12")
    assert len(Ddmain) == 12
    assert abs(maxdot - 2 / np.sqrt(5)) < 1e-9
    print(f"    so its printed 'nearest among holes' line is *not* the hole value; "
          f"on that set it is {rmin_np(Ddmain, Xn).min():.9f}")
    print(f"    the true face-centre value is {float(val_face):.9f} = the global minimum")

    # 6. the conclusion: bisector outside the cell's circumradius
    two_Rcell = 2 * (2.09 / 2) * np.sqrt(2)
    print(f"[7] 2*R_cell (C102's conservative bound (rho/2)*sqrt2) = {two_Rcell:.9f}")
    print(f"    3.206871 - {two_Rcell:.9f} = {3.206870905 - two_Rcell:.9f} > 0  -> redundant")
    assert 3.206870905 > two_Rcell
    hd = 1.258408572 * 1.045            # true cell circumradius at rho = 2.09 = 1.045*h_D
    print(f"    true dodecahedral circumradius 2*1.045*1.258408572 = {2 * hd:.9f} "
          f"-- margin {3.206870905 - 2 * hd:.9f}, larger than against 2*R_cell")
    assert 3.206870905 > 2 * hd

    print("\nVERDICT: C102's constant 3.206870905 is CORRECT at rho = 2.09 and its "
          "conclusion stands.\n         The handover's '3.178617889 / 0.881% too high' is the rho = 2 value "
          "of the same\n         function; two prose/auxiliary defects remain (face centre called "
          "an edge midpoint;\n         the hole enumeration is the vertex set). Constant right, "
          "conclusion right.")


if __name__ == '__main__':
    main()
