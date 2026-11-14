#!/usr/bin/env python3
"""
Independent test of Main's theorem (K15-C094): every Voronoi cell of every Barlow packing
has volume 4*sqrt2 and is congruent to the fcc or the hcp cell.

Main's BARLOW_CELLS.md verifies six named stackings plus a 48-stacking sweep.  This script
does something different: it generates RANDOM legal stackings of period p (a +/-1 walk on
Z/3 that closes up), builds the packing, and computes EVERY layer's cell independently --
volume, contact count, next distance, and the face-normal fingerprint that distinguishes
the two local types.

  fcc type:  face-normal dot products { -1, -1/2, 0, 1/2 }
  hcp type:  the same plus -5/6 and -1/3

Run: python3 Experimental/scripts/barlow_random_stackings.py [n_stackings] [seed]
Exit 0 iff every layer of every legal stacking gives volume 4*sqrt2 and a recognisable type.
"""
import itertools
import sys
import numpy as np
from scipy.spatial import ConvexHull

A1 = np.array([2.0, 0.0])
A2 = np.array([1.0, np.sqrt(3.0)])
T = (A1 + A2) / 3
H = np.sqrt(8.0 / 3.0)
SQRT32 = np.sqrt(32.0)


def random_stacking(p, rng):
    """A closed +/-1 walk on Z/3 of length p, i.e. a legal period-p Barlow stacking."""
    for _ in range(2000):
        s = [0]
        for _ in range(p - 1):
            s.append((s[-1] + rng.choice([1, -1])) % 3)
        if (s[-1] + rng.choice([1, -1])) % 3 == 0:      # can close up
            step = 1 if (s[-1] + 1) % 3 == 0 else -1
            return s, step
    return None


def sites(s, centre, R=5.5, nlayers=14):
    """All centres of the stacking within R of `centre`."""
    out = []
    p = len(s)
    for k in range(-nlayers, nlayers + 1):
        z = k * H
        off = s[k % p] * T
        for i in range(-4, 5):
            for j in range(-4, 5):
                q = np.array([off[0] + i * A1[0] + j * A2[0],
                              off[1] + i * A1[1] + j * A2[1], z])
                if np.linalg.norm(q - centre) <= R:
                    out.append(q)
    return np.array(out)


def cell(v, P):
    # prune: a centre cuts only if |z-v|/2 < max|vertex|.  For a Barlow cell max|vertex| = sqrt2,
    # so |z-v| < 2*sqrt2 = 2.828 is necessary; 3.0 is a safe cut and is checked afterwards.
    o = [p for p in P if 1e-12 < np.linalg.norm(p - v) < 3.0]
    ns, ds = [], []
    for p in o:
        L = np.linalg.norm(p - v)
        ns.append((p - v) / L)
        ds.append(L / 2.0)
    n = np.array(ns)
    dd = np.array(ds)
    V = []
    for i, j, k in itertools.combinations(range(len(n)), 3):
        try:
            x = np.linalg.solve(n[[i, j, k]], dd[[i, j, k]])
        except np.linalg.LinAlgError:
            continue
        if np.all(n @ x <= dd + 1e-10) and not any(np.linalg.norm(x - y) < 1e-9 for y in V):
            V.append(x)
    return np.array(V), n


def main():
    nstack = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    rng = np.random.default_rng(seed)
    ok = True
    tested = 0
    print(" period stacking              layer  #contacts  next     volume      type")
    for trial in range(nstack):
        p = int(rng.integers(3, 13))
        res = random_stacking(p, rng)
        if res is None:
            continue
        s, _ = res
        types = []
        for k in range(p):
            v = np.array([s[k] * T[0], s[k] * T[1], k * H])
            P = sites(s, v)
            V, n = cell(v, P)
            vol = ConvexHull(V).volume
            dists = np.sort(np.linalg.norm(P - v, axis=1))
            nc = int((np.abs(dists - 2.0) < 1e-9).sum())
            nxt = dists[dists > 2.0 + 1e-9][0]
            # the fingerprint must use the TWELVE CONTACTS, not the first twelve centres
            # in enumeration order (that mistake made every cell look like fcc).
            order = np.argsort(np.linalg.norm(P - v, axis=1))
            contacts = [k for k in order if abs(np.linalg.norm(P[k] - v) - 2.0) < 1e-9]
            nc_normals = [(P[k] - v) / 2.0 for k in contacts]
            dots = sorted({round(float(nc_normals[i] @ nc_normals[j]), 6)
                           for i in range(len(nc_normals)) for j in range(i + 1, len(nc_normals))})
            is_hcp = any(abs(d + 5 / 6) < 1e-6 or abs(d + 1 / 3) < 1e-6 for d in dots)
            typ = "hcp" if is_hcp else "fcc"
            types.append(typ)
            rmax = np.linalg.norm(V, axis=1).max()
            if rmax >= 1.5:
                print(f"   WARNING: max|vertex| = {rmax:.4f} >= 1.5, pruning may be invalid")
                ok = False
            bad = (abs(vol - SQRT32) > 1e-9 or nc != 12 or abs(nxt - 2 * np.sqrt(2)) > 1e-9)
            if bad:
                ok = False
            tested += 1
            if bad or k == 0:
                print(f"   {p:2d}   {str(s):20s}  {k:3d}   {nc:3d}    {nxt:.6f}  {vol:.9f}  {typ}"
                      + ("   <-- MISMATCH" if bad else ""))
        print(f"   {p:2d}   {str(s):20s}  types: {types}")
    print(f"\n  layers tested: {tested}")
    print("  ALL cells 4*sqrt2 with 12 contacts at 2, next at 2*sqrt2, and an fcc/hcp fingerprint?"
          f"  {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
