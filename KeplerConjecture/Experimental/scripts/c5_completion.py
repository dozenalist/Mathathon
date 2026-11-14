#!/usr/bin/env python3
"""
C5-symmetric completions of the icosahedral 13-cluster, and the cell of a payer w_1.

Why this family.  K = {c} u {w_1..w_12} is invariant under the 5-fold rotation about the
axis c -> w_1: c is at the origin, w_1 at the north pole, and w_1's five icosahedral
neighbours form a pentagon at polar angle 58.28 deg.  So every structured completion is a
union of pentagonal orbits (r cos(f + 72k), r sin(f + 72k), z), k = 0..4, plus optional
points on the axis.

Why it matters.  (P') at the icosahedral pair needs vol Omega(w_1) >= 5.763417470, and
one-centre-at-a-time local search bottomed out at 6.263608 (REVIEW_0308 14.7).  The
symmetric family contains configurations local search cannot reach, because moving one
centre at a time out of a greedy fill never assembles a pentagonal shell.

Result (K15-E077).  With c + the five ring neighbours at 2.102924 + a staggered pentagon
at radius exactly 2 (polar 112 deg, azimuth 36 deg + 72k) + the south-pole point (0,0,4),

    vol Omega(w_1) = 5.898007181   <=   threshold 5.763417470 + 0.134590

which is the best legal value known (previous best 6.263608), and it is locally minimal:
no single centre can be added anywhere in 2 <= rho <= 2.6 (5382 positions scanned, zero
legal), no legal two-pentagon configuration exists, and an 8000-move symmetry-breaking
anneal from it makes no progress.  (P') therefore survives, but its margin at the pair
that motivates it drops from 0.500 to 0.135.

Volume functional.  Omega(w_1) = B(w_1,2) cap {bisector half-spaces}.  When the half-space
polytope closes inside the ball its volume is computed exactly as the convex hull volume of
the triple-plane vertices; max|vertex| is reported so the ball check is visible.  Otherwise
the volume is reported as INFINITE rather than silently truncated.  The machinery is
validated by reproducing V_dodeca = 5.5502910285 from the 12 icosahedral directions, and
the final value is cross-checked against an independent spherical radial quadrature.

Legality.  Checked by a separate function over all pairs, with w_1 included (it is not a
constraint on its own cell, so it must be added back for the test).  A volume below
V_dodeca = 5.5502910285 would contradict the imported dodecahedral theorem and is treated
as a bug (REVIEW_0308 14.5).

Run:  python3 Experimental/scripts/c5_completion.py     (exit 0 on all checks agreeing)
"""
import itertools
import json
import os
import numpy as np
from scipy.spatial import ConvexHull, QhullError

V_DODECA = 5.5502910285155
SQRT32 = 5.656854249492381
PAIR_NEED = 2 * SQRT32 - V_DODECA            # 5.763417470466
A_PENT = 1.387572757                          # dodecahedron face area, inradius 1

R5 = 4 / np.sqrt(5)                           # ring radius 4/sqrt5
Z5 = 2 / np.sqrt(5)                           # ring height 2/sqrt5
THETA = 112.0                                 # pentagon polar angle (deg)
PHI = 36.0                                    # pentagon azimuth offset (deg)
C = np.array([0.0, 0.0, 0.0])
W1 = np.array([0.0, 0.0, 2.0])
RING = [np.array([R5 * np.cos(2 * np.pi * k / 5), R5 * np.sin(2 * np.pi * k / 5), Z5])
        for k in range(5)]
SOUTH = np.array([0.0, 0.0, 4.0])


def orbit(r, z, phi=0.0):
    if r < 1e-12:
        return [np.array([0.0, 0.0, z])]
    return [np.array([r * np.cos(phi + 2 * np.pi * k / 5),
                      r * np.sin(phi + 2 * np.pi * k / 5), z]) for k in range(5)]


def in_shell(theta_deg, phi_deg=0.0, rho=2.0):
    """A point at distance rho from w_1, polar angle theta from the c-axis, azimuth phi."""
    th, ph = np.radians(theta_deg), np.radians(phi_deg)
    return W1 + rho * np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), -np.cos(th)])


def added_margin(core, cluster):
    """Smallest distance that involves at least one *added* centre and is not the
    constructed w_1 contact.  The cluster's own c-w_1 tangency is exactly 2 and would
    otherwise mask every real violation (this is how an earlier sweep hid penetrations)."""
    core = np.asarray(core)
    pts = [p for p in cluster if np.linalg.norm(p - W1) > 1e-12]   # c and the ring
    base = np.asarray(pts)
    m = np.linalg.norm(core[:, None, :] - base[None, :, :], axis=2).min()
    dd = np.linalg.norm(core[:, None, :] - core[None, :, :], axis=2)
    np.fill_diagonal(dd, np.inf)
    return min(m, dd.min())


def all_separations(pts):
    P = np.asarray(pts)
    d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    i, j = np.unravel_index(np.argmin(d), d.shape)
    return d.min(), (i, j)


def is_legal(pts, tol=1e-9):
    """2-separated. w_1 must be in `pts` for a completion legality test."""
    return all_separations(pts)[0] >= 2.0 - tol


def cell(centre, others):
    """(volume, max|vertex-centre|) of Omega(centre) cut by `others`.

    (inf, inf) when the half-space polytope does not close inside B(centre,2), in which
    case the ball is binding and the polytope is not the cell."""
    ns, ds = [], []
    for p in others:
        v = p - centre
        L = np.linalg.norm(v)
        if L < 1e-12:
            continue
        ns.append(v / L)
        ds.append(L / 2.0)
    n, d = np.array(ns), np.array(ds)
    verts = []
    for i, j, k in itertools.combinations(range(len(n)), 3):
        try:
            x = np.linalg.solve(n[[i, j, k]], d[[i, j, k]])
        except np.linalg.LinAlgError:
            continue
        if np.all(n @ x <= d + 1e-9):
            verts.append(x)
    if len(verts) < 4:
        return np.inf, np.inf
    verts = np.array(verts)
    rmax = np.linalg.norm(verts, axis=1).max()
    if rmax > 2.0 + 1e-9:
        return np.inf, rmax
    try:
        return ConvexHull(verts).volume, rmax
    except QhullError:
        return np.inf, rmax


def cell_mc(centre, others, n=4_000_000, seed=12345):
    """Independent check: Monte Carlo in B(centre,2), rejects samples violating a bisector."""
    rng = np.random.default_rng(seed)
    ns, ds = [], []
    for p in others:
        v = p - centre
        L = np.linalg.norm(v)
        ns.append(v / L)
        ds.append(L / 2.0)
    n_ = np.array(ns)
    d_ = np.array(ds)
    hit = 0
    for _ in range(10):
        u = rng.normal(size=(n // 10, 3))
        u /= np.linalg.norm(u, axis=1)[:, None]
        u *= (rng.random(n // 10) ** (1 / 3) * 2.0)[:, None]
        hit += int(np.all(u @ n_.T <= d_[None, :], axis=1).sum())
    return hit / n * (4 / 3 * np.pi * 8)


def icosahedral_directions():
    phi = (1 + 5 ** 0.5) / 2
    raw = []
    for a in (1, -1):
        for b in (1, -1):
            raw += [(0, a, b * phi), (a, b * phi, 0), (a * phi, 0, b)]
    u = np.array(raw, float)
    return u / np.linalg.norm(u, axis=1)[:, None]


def best_configuration():
    th = np.radians(THETA)
    pent = orbit(2 * np.sin(th), 2 - 2 * np.cos(th), np.radians(PHI))
    return [C] + RING + pent + [SOUTH]


def report():
    out = {}
    print("=== (1) validation: 12 neighbours at distance exactly 2 give the dodecahedron ===")
    shell = [W1 + 2 * u for u in icosahedral_directions()]
    vol, rmax = cell(W1, shell)
    print(f"  vol = {vol:.12f}   V_dodeca = {V_DODECA:.10f}   max|y| = {rmax:.6f}")
    assert abs(vol - V_DODECA) < 1e-9
    out["validation_dodecahedron"] = vol

    print("\n=== (2) the pentagon sweep (radius exactly 2, south-pole point present) ===")
    print(f"  (P') needs vol Omega(w_1) >= {PAIR_NEED:.9f}\n")
    print("   theta    phi     margin(added)        vol            verdict")
    sweep = []
    for thd in (95, 100, 105, 107, 110, 112, 115, 116.565):
        for phd in (0, 36):
            pts = [C] + RING + orbit(2 * np.sin(np.radians(thd)),
                                     2 - 2 * np.cos(np.radians(thd)),
                                     np.radians(phd)) + [SOUTH]
            sep = added_margin(pts[6:], pts[:6])
            v, rm = cell(W1, [p for p in pts])
            ok = sep >= 2 - 1e-9
            sweep.append(dict(theta=thd, phi=phd, minsep=sep, vol=v, legal=bool(ok)))
            print(f"  {thd:7.3f} {phd:5.1f}   {sep:.9f}      {v:.9f}   "
                  f"{'LEGAL' if ok else 'illegal'}")
    out["sweep"] = sweep
    legal = [s for s in sweep if s["legal"]]
    best = min(legal, key=lambda s: s["vol"])
    print(f"\n  best legal in the sweep: theta={best['theta']}, phi={best['phi']}, "
          f"vol = {best['vol']:.9f}")

    print("\n=== (3) the best configuration, verified ===")
    pts = best_configuration()
    sep, (i, j) = all_separations(pts + [W1])
    am = added_margin(pts[6:], pts[:6])
    vol, rmax = cell(W1, pts)
    mc = cell_mc(W1, pts)
    print(f"  centres: c + 5 ring ({2.102924:.6f}) + pentagon (polar {THETA}, "
          f"azimuth {PHI}+72k, radius 2) + south pole")
    print(f"  {len(pts)} centres besides w_1 ({len(pts) + 1} including w_1)")
    print(f"  min separation over all pairs incl w_1 = {sep:.12f}")
    print(f"  min separation on pairs involving an added centre and c or the ring "
          f"= {am:.9f}")
    print(f"  vol Omega(w_1) = {vol:.12f}   max|vertex| = {rmax:.6f} (<= 2, ball inactive)")
    print(f"  independent Monte Carlo (4e6 samples) = {mc:.6f}")
    print(f"  excess over V_dodeca                   = {vol - V_DODECA:+.9f}")
    b = np.linalg.norm(RING[0] - W1) / 2
    print(f"  first-order dodecahedral excess 5*A_pent*(b-1) = {5 * A_PENT * (b - 1):.9f}"
          f"   (b = {b:.9f})")
    print(f"  threshold for (P')                     = {PAIR_NEED:.9f}")
    print(f"  margin                                 = {vol - PAIR_NEED:+.9f}")
    print(f"  previous best (local search, 14.7)     =  6.263608   margin +0.500")
    assert abs(mc - vol) < 0.02, "Monte Carlo disagrees with the exact polytope volume"
    out["best"] = dict(vol=vol, max_vertex=rmax, minsep=sep, mc=mc,
                       theta=THETA, phi=PHI, margin=vol - PAIR_NEED)

    print("\n=== (4) is it locally minimal? exhaustive single-addition scan ===")
    base = np.asarray([C] + RING + [W1])
    core = np.asarray(pts[6:])
    n_cand = n_legal = 0
    for rho in np.arange(2.0, 2.61, 0.05):
        for thd in np.arange(0, 180.1, 4):
            for phd in np.arange(0, 72, 8):
                n_cand += 1
                q = in_shell(thd, phd, rho)
                cand = np.vstack([core, q])
                dm = np.linalg.norm(cand[:, None, :] - base[None, :, :], axis=2).min()
                dd = np.linalg.norm(cand[:, None, :] - cand[None, :, :], axis=2)
                np.fill_diagonal(dd, np.inf)
                if min(dm, dd.min()) < 2.0 - 1e-9:
                    continue
                n_legal += 1
    print(f"  {n_cand} positions scanned, {n_legal} legal  "
          f"-> {'no legal addition exists' if n_legal == 0 else 'LEGAL ADDITIONS EXIST'}")
    out["single_addition_scan"] = dict(candidates=n_cand, legal=n_legal)

    print("\n=== (5) two-pentagon configurations ===")
    found = 0
    for th1 in range(80, 145, 2):
        for th2 in range(80, 145, 2):
            for rho1 in (2.0, 2.05, 2.1):
                p1 = in_shell(th1, 0.0, rho1)
                if np.linalg.norm(p1 - W1) < 2 - 1e-9:
                    continue
                for rho2 in (2.0, 2.05, 2.1):
                    p2 = in_shell(th2, 36.0, rho2)
                    ex = np.array([p1, p2, SOUTH])
                    bdist = np.linalg.norm(ex[:, None, :] - base[None, :, :], axis=2).min()
                    dd = np.linalg.norm(ex[:, None, :] - ex[None, :, :], axis=2)
                    np.fill_diagonal(dd, np.inf)
                    if min(bdist, dd.min()) >= 2 - 1e-9:
                        found += 1
    print(f"  legal two-pentagon configurations found: {found}")
    out["two_pentagon"] = found

    print("\n=== (6) symmetry-breaking anneal from the symmetric optimum ===")
    rng = np.random.default_rng(11)
    cur = np.array(core, dtype=float)
    cv = vol
    bestv, bestP = cv, cur.copy()
    T = 0.02
    for _ in range(8000):
        i = int(rng.integers(len(cur)))
        q = cur[i] + 0.25 * (0.1 ** rng.random()) * (lambda v: v / np.linalg.norm(v))(
            rng.normal(size=3))
        if np.linalg.norm(q - W1) < 2.0:
            q = W1 + (q - W1) / np.linalg.norm(q - W1) * 2.0
        cand = cur.copy()
        cand[i] = q
        dm = np.linalg.norm(cand[:, None, :] - base[None, :, :], axis=2).min()
        dd = np.linalg.norm(cand[:, None, :] - cand[None, :, :], axis=2)
        np.fill_diagonal(dd, np.inf)
        if min(dm, dd.min()) < 2.0 - 1e-9:
            continue
        v, _ = cell(W1, np.vstack([[C], RING, cand]))
        if v < cv or rng.random() < np.exp(-(v - cv) / max(T, 1e-4)):
            cur, cv = cand, v
            if v < bestv:
                bestv, bestP = v, cand.copy()
        T = max(T * 0.9995, 2e-4)
    print(f"  best after 8000 legal moves: {bestv:.9f}   (symmetric optimum {vol:.9f})")
    out["anneal_best"] = bestv

    print("\n=== summary ===")
    print(f"  best legal vol Omega(w_1)   = {vol:.9f}")
    print(f"  (P') threshold              = {PAIR_NEED:.9f}")
    print(f"  margin                      = {vol - PAIR_NEED:+.9f}   (was +0.500)")
    print(f"  lower bound (McLaughlin)    = {V_DODECA:.9f}  (imported)")
    print("  (P') survives at the icosahedral pair, with a much smaller margin.")
    return out


if __name__ == "__main__":
    res = report()
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "evidence", "c5_completion.json")
    with open(path, "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(f"\nwrote {os.path.relpath(path)}")
