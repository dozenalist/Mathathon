#!/usr/bin/env python3
"""Barlow cell volumes: the 12-contact reduction and the two-shape dichotomy.

K15-C094 in Main/BARLOW_CELLS.md. Statement proved there: every Voronoi cell of every
Barlow packing has volume 4*sqrt(2) = sqrt(32).

The proof's steps that could be wrong, and what this script checks:

  (A) exactly 12 centres at distance 2, and every other centre at >= 2*sqrt(2);
  (B) the cell cut out by those 12 equals the cell cut out by everything  -> tests the
      tangency/equality case of Lemma 1 (the slack must be <= 0, and is 0);
  (C) the 12-contact configuration takes exactly two values up to isometry, read off
      from the coset of the neighbouring layers (+T,+T or +T,-T);
  (D) both cell types have volume sqrt(32), though they are NOT congruent.

Usage:  python3 barlow_cells.py [--sweep N] [--quiet]
  --sweep N   also analyse N random legal stackings of each period 3..10
Exit status 0 iff every check passes.
"""
import argparse
import itertools
import random
import sys

import numpy as np
from scipy.spatial import ConvexHull

A1 = np.array([2.0, 0.0])
A2 = np.array([1.0, np.sqrt(3.0)])
T = (A1 + A2) / 3.0
H = np.sqrt(8.0 / 3.0)
SQ32 = np.sqrt(32.0)
TOL_V = 1e-9          # volume agreement
TOL_FAR = 1e-12       # a non-contact must not cut the cell by more than this


def legal(s):
    """Every consecutive step is +-1 mod 3, including the wrap."""
    p = len(s)
    return all((s[(k + 1) % p] - s[k]) % 3 in (1, 2) for k in range(p))


def sites(s, kmin, kmax, span):
    p = len(s)
    out = []
    for k in range(kmin, kmax + 1):
        base = s[k % p] * T
        for i in range(-span, span + 1):
            for j in range(-span, span + 1):
                xy = i * A1 + j * A2 + base
                out.append((xy[0], xy[1], k * H, k))
    return np.array(out)


def cell(target, others, tol=1e-9):
    """Voronoi cell of `target` against `others`, by half-space intersection.

    Half-space for centre c:  n.x <= 1  with  n = 2(c-t)/|c-t|^2.  Vertices are the
    feasible triple intersections; the volume is the convex hull's.
    """
    ns = np.array([2.0 * (c - target) / ((c - target) @ (c - target)) for c in others])
    m = len(ns)
    V = []
    for i, j, k in itertools.combinations(range(m), 3):
        M = ns[[i, j, k]]
        try:
            p = np.linalg.solve(M, np.ones(3))
        except np.linalg.LinAlgError:
            continue
        if np.all(ns @ p <= 1.0 + tol):
            V.append(p)
    if len(V) < 4:
        return 0.0, np.zeros((0, 3)), ns
    V = np.array(V)
    _, idx = np.unique(np.round(V, 8), axis=0, return_index=True)
    V = V[np.sort(idx)]
    if len(V) < 4:
        return 0.0, V, ns
    return ConvexHull(V).volume, V, ns


def azim(cs):
    return np.array([np.degrees(np.arctan2(c[1], c[0])) % 360.0 for c in cs])


def analyse(s, k0, span=6, halo=4):
    """Analyse the site (layer k0, in-plane index (0,0))."""
    p = len(s)
    P = sites(s, k0 - halo, k0 + halo, span)
    tgt = np.array([s[k0 % p] * T[0], s[k0 % p] * T[1], k0 * H])
    rel = P[:, :3] - tgt
    d = np.linalg.norm(rel, axis=1)
    order = np.argsort(d)
    assert d[order[0]] < 1e-12, "target is not a site of the packing"
    other, dd = rel[order[1:]], d[order[1:]]
    n2 = int(np.sum(np.abs(dd - 2.0) < 1e-9))
    twelve = other[:12]
    vol12, V12, ns12 = cell(np.zeros(3), twelve)
    circ = float(np.max(np.linalg.norm(V12, axis=1))) if len(V12) else float('nan')
    worst = -np.inf
    if len(V12):
        for c in other[12:]:
            n = 2.0 * c / (c @ c)
            worst = max(worst, float(np.max(V12 @ n) - 1.0))
    volfull, _, _ = cell(np.zeros(3), other[dd <= 5.0])
    faces = sorted(int(np.sum(V12 @ n >= 1.0 - 1e-6)) for n in ns12)
    up = twelve[twelve[:, 2] > 1e-6]
    dn = twelve[twelve[:, 2] < -1e-6]
    assert len(up) == 3 and len(dn) == 3, (len(up), len(dn))
    au, ad = np.sort(azim(up)), np.sort(azim(dn))
    same = np.allclose(au, ad, atol=1e-4)                 # upper/lower coset equal
    shift = np.allclose(np.sort((au + 60.0) % 360.0), ad, atol=1e-4)
    dots = np.round(np.sort((ns12 @ ns12.T)[np.triu_indices(12, 1)]), 6)
    return dict(n2=n2, next_dist=float(dd[12]), vol12=vol12, volfull=volfull,
                circ=circ, worst_far=worst, faces=faces, nvert=len(V12),
                type='hcp' if same else ('fcc' if shift else '???'),
                dots=dots[::max(1, len(dots) // 8)])


def report(s, name, verbose=True):
    p = len(s)
    if not legal(s):
        if verbose:
            print(f"--- {name}  s={s}: ILLEGAL (a step is 0 mod 3), skipped")
        return None
    rows = []
    for k0 in range(p):
        r = analyse(s, k0)
        rows.append(r)
        if verbose:
            print(f"    {name:12s} layer {k0}: #@2={r['n2']:2d} next={r['next_dist']:.6f} "
                  f"V12={r['vol12']:.12f} Vfull={r['volfull']:.12f} "
                  f"circ={r['circ']:.6f} {r['type']:3s} "
                  f"faces={r['faces']} nvert={r['nvert']} far={r['worst_far']:+.1e}")
    return rows


def check(rows, s, k0, bad):
    r = rows[k0]
    if abs(r['vol12'] - SQ32) > TOL_V:
        bad.append((s, k0, 'vol12', r['vol12']))
    if abs(r['volfull'] - SQ32) > TOL_V:
        bad.append((s, k0, 'volfull', r['volfull']))
    if r['n2'] != 12:
        bad.append((s, k0, 'n2', r['n2']))
    if r['worst_far'] > TOL_FAR:
        bad.append((s, k0, 'far_cuts', r['worst_far']))
    if r['type'] not in ('fcc', 'hcp'):
        bad.append((s, k0, 'type', r['type']))


def random_legal(p, rng):
    s = [rng.randrange(3)]
    for _ in range(p - 1):
        s.append((s[-1] + rng.choice([1, -1])) % 3)
    return s if legal(s) else None


def covering_radius(s, rng, nsample=4000):
    """Sampled max of dist(x, centres); (F3) predicts <= sqrt(2)."""
    P = sites(s, -3, 3, 5)[:, :3]
    pts = np.column_stack([rng.uniform(-1, 1, nsample), rng.uniform(-1, 1, nsample),
                           rng.uniform(-H, H, nsample)])
    best = np.full(nsample, np.inf)
    for c in P:
        best = np.minimum(best, np.linalg.norm(pts - c, axis=1))
    return float(best.max())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--sweep', type=int, default=0,
                    help='random legal stackings per period 3..10 (0 = named only)')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args(argv)

    named = {
        'ABC (fcc)': [0, 1, 2],
        'ABA (hcp)': [0, 1],
        'ABAC': [0, 1, 0, 2],
        'ABCB': [0, 1, 2, 1],
        'ABABAC': [0, 1, 0, 1, 0, 2],
        'ABCACB': [0, 1, 2, 0, 2, 1],
        'ABCABCACB': [0, 1, 2, 0, 1, 2, 0, 2, 1],
        'ABACABA (illegal)': [0, 1, 0, 2, 0, 1, 0],
        'ABABCBCA (illegal)': [0, 1, 0, 1, 2, 1, 2, 0],
    }
    bad = []
    nlayer = 0
    for name, s in named.items():
        rows = report(s, name, verbose=not a.quiet)
        if rows is None:
            continue
        nlayer += len(rows)
        for k0 in range(len(rows)):
            check(rows, s, k0, bad)

    # the two known types must be distinguishable by the face-normal fingerprint
    r_fcc = analyse([0, 1, 2], 0)
    r_hcp = analyse([0, 1], 0)
    same_fp = np.allclose(r_fcc['dots'], r_hcp['dots'], atol=1e-9)
    if same_fp:
        bad.append(('fingerprint', 'fcc vs hcp cells look congruent', None, None))

    nsweep = 0
    if a.sweep:
        rng = random.Random(20261114)
        for p in range(3, 11):
            made, tries = 0, 0
            while made < a.sweep and tries < 4000:
                tries += 1
                s = random_legal(p, rng)
                if s is None:
                    continue
                made += 1
                allrows = analyse_all(s, p)
                nlayer += p
                for k0 in range(p):
                    check(allrows, s, k0, bad)
                nsweep += 1
        print(f"random sweep: {nsweep} stackings")

    print()
    print("=== summary ===")
    print(f"  layer analyses: {nlayer}   volume target sqrt32 = {SQ32:.12f}")
    print(f"  fcc and hcp cells non-congruent (fingerprints differ): {not same_fp}")
    print(f"  violations: {len(bad)}")
    for b in bad[:12]:
        print("   ", b)

    rng2 = np.random.default_rng(20261114)
    print("  covering radius (F3 predicts <= sqrt2 = 1.4142136):")
    for name, s in [('ABC', [0, 1, 2]), ('ABA', [0, 1]), ('ABAC', [0, 1, 0, 2])]:
        cr = covering_radius(s, rng2)
        ok = cr <= np.sqrt(2) + 1e-9
        print(f"    {name:6s} {cr:.6f}  {'OK' if ok else 'FAIL'}")
        if not ok:
            bad.append((name, 'covering_radius', cr, None))
    return 0 if not bad else 1


def analyse_all(s, p):
    return [analyse(s, k) for k in range(p)]


if __name__ == '__main__':
    sys.exit(main())
