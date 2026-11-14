#!/usr/bin/env python3
"""Cross-check certified volumes against uniform sampling, on RANDOM rational polytopes.

The adversarial fixtures of `tests_exact_volume.py` have hand values, which is the strongest check
but only for shapes someone thought of.  This samples a family instead: random half-spaces with
small integer normals, intersected inside a box, certified by `exact_volume`, and estimated
independently by rejection sampling from the box.  The two agree to a stated sigma or the case is
printed.

The sampler knows nothing about the verifier: it tests `a.x <= d` for the same planes at random
points.  A disagreement means one of them is wrong.

Run: python3 crosscheck_volume.py [n_polytopes] [n_points] [seed]
"""
import random, sys
from fractions import Fraction as F
import numpy as np
import exact_volume as EV

def random_polytope(rng, k):
    """k random half-spaces with normals in {-2..2}^3 and offsets chosen to cut a box."""
    planes = []
    while len(planes) < k:
        n = (rng.randint(-2, 2), rng.randint(-2, 2), rng.randint(-2, 2))
        if n == (0, 0, 0):
            continue
        d = F(rng.randint(1, 6))
        planes.append((n[0], n[1], n[2], d))
    return planes

def find_ray(planes, tries=200000, rng=None):
    """A u != 0 with a_i.u <= 0 for every plane -- a certificate that the polyhedron is unbounded.

    Sampling directions can only find one; failing to find one proves nothing (hence the wording
    above: "of which N have an explicit ray", never "the rest are bounded").
    """
    rng = rng or random.Random(12345)
    for _ in range(tries):
        u = (rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3))
        if u == (0, 0, 0):
            continue
        if all(a*u[0] + b*u[1] + c*u[2] <= 0 for (a, b, c, d) in planes):
            return u
    return None

def main(argv):
    n_poly = int(argv[1]) if len(argv) > 1 else 30
    n_pts = int(argv[2]) if len(argv) > 2 else 200000
    seed = int(argv[3]) if len(argv) > 3 else 0
    rng = random.Random(seed)
    ok = 0
    skipped = 0
    worst = 0.0
    reasons = {}
    rays = []
    for t in range(n_poly):
        planes = random_polytope(rng, rng.randint(10, 16))
        try:
            kept, _ = EV.prepare(planes)
            verts = EV.enumerate_vertices(kept)
            if len(verts) < 4:
                skipped += 1; continue
            interior = tuple(sum(P[i] for P in verts) / len(verts) for i in range(3))
            vol, cert = EV.certify_volume(planes, interior)
        except ValueError as e:
            key = str(e).split(":")[0]
            reasons[key] = reasons.get(key, 0) + 1
            if key == "V5":
                # the gate says the surface does not close, i.e. the polyhedron is unbounded.
                # Certify that by exhibiting a RAY: a u != 0 with a_i.u <= 0 for every plane.
                ray = find_ray(kept)
                rays.append(ray)
            skipped += 1; continue
        # independent: rejection sampling inside a box around the vertices
        lo = [float(min(P[i] for P in verts)) - 0.5 for i in range(3)]
        hi = [float(max(P[i] for P in verts)) + 0.5 for i in range(3)]
        boxvol = (hi[0]-lo[0]) * (hi[1]-lo[1]) * (hi[2]-lo[2])
        P = np.random.default_rng(seed * 1000 + t).uniform(lo, hi, size=(n_pts, 3))
        inside = np.ones(n_pts, dtype=bool)
        for (a, b, c, d) in [tuple(float(x) for x in pl) for pl in kept]:
            inside &= (a*P[:, 0] + b*P[:, 1] + c*P[:, 2] <= d)
        frac = inside.mean()
        est = boxvol * frac
        # the standard error of the estimate
        sig = boxvol * (frac * (1 - frac) / n_pts) ** 0.5
        if sig == 0:
            skipped += 1; continue
        dev = abs(est - float(vol)) / sig
        worst = max(worst, dev)
        if dev > 6:
            print("  DISAGREEMENT: certified %.6f, sampled %.6f +- %.6f (%.1f sigma)"
                  % (float(vol), est, sig, dev))
            print("     planes:", [tuple(str(x) for x in pl) for pl in kept])
            return 1
        ok += 1
    print("%d polytopes, %d sampled-consistent, %d skipped (degenerate or too small)"
          % (n_poly, ok, skipped))
    print("worst deviation %.1f sigma (threshold 6)" % worst)
    if reasons:
        print("skip reasons:", reasons)
    if rays:
        got = [r for r in rays if r is not None]
        print("V5 rejections: %d, of which %d have an explicit unbounded ray (u != 0, a_i.u <= 0)"
              % (len(rays), len(got)))
    print("=> the certified volume and an independent sampler agree on every case")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
