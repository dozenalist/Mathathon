#!/usr/bin/env python3
"""
Does the premise vol D' >= 5.5400 hold for the actual family?

D' is the unit-distance polytope of the twelve directions: c, the five ring directions
(58.2825 deg), and six free ones from a legal completion.  The conditional twelve-face
theorem of REVIEW_0608 requires vol D' >= V_dod - 5(b-1)A_min = 5.5400.

This script MINIMISES vol D' over the admissible six-direction sets, by local search from the
C5 configuration and from random legal starts.  It is an upper bound on the minimum (a
numerical minimisation, not a proof): if the minimum found is comfortably above 5.5400 the
premise is plausible; if it approaches 5.5400 the premise is delicate; if it goes below, the
premise is FALSE and the conditional theorem is empty.

Run: python3 Experimental/scripts/premise_audit.py [seconds]
Every start is capped at 120 s regardless of the total (review 2026-11-14_0738).
"""
import itertools
import sys
import time

import numpy as np
from scipy.spatial import ConvexHull

TH_R = np.radians(58.282525060518495)
RING = [np.array([np.sin(TH_R) * np.cos(2 * np.pi * k / 5),
                  np.sin(TH_R) * np.sin(2 * np.pi * k / 5), np.cos(TH_R)]) for k in range(5)]
CFIX = np.array([0.0, 0.0, -1.0])
COS_R = np.cos(np.radians(58.2825))
COS60 = 0.5


def dprime_volume(dirs):
    ns = np.array([d / np.linalg.norm(d) for d in dirs])
    ds = np.ones(len(ns))
    V = []
    for a, b, c in itertools.combinations(range(len(ns)), 3):
        try:
            x = np.linalg.solve(ns[[a, b, c]], ds[[a, b, c]])
        except np.linalg.LinAlgError:
            continue
        if np.all(ns @ x <= ds + 1e-12) and not any(np.linalg.norm(x - y) < 1e-11 for y in V):
            V.append(x)
    if len(V) < 4:
        return None
    try:
        if not np.all(ns @ np.mean(V, axis=0) < 1 - 1e-9):
            pass
        return ConvexHull(np.array(V)).volume
    except Exception:
        return None


def legal(free):
    for f in free:
        u = f / np.linalg.norm(f)
        if np.dot(u, CFIX) > COS60 + 1e-9:
            return False
        for r in RING:
            if np.dot(u, r) > COS_R - 1e-9:
                return False
    for i in range(len(free)):
        for j in range(i + 1, len(free)):
            if np.dot(free[i], free[j]) > COS60 + 1e-9:
                return False
    return True


def c5_free():
    th_p = np.radians(112.0)
    free = [np.array([np.sin(th_p) * np.cos(np.radians(36 + 72 * k)),
                      np.sin(th_p) * np.sin(np.radians(36 + 72 * k)), np.cos(th_p)])
            for k in range(5)]
    free.append(np.array([0.0, 0.0, 1.0]))
    return free


def random_free(rng, walk=400):
    """A legal set found by a random walk INSIDE the legal region, started from C5.

    Rejection sampling from scratch fails completely (the legal region is tiny relative to
    the ambient 12 dimensions): a first version found zero legal sets in 6 x 4000 tries.
    A random walk that only takes legal steps works."""
    free = [f.copy() for f in c5_free()]
    for _ in range(walk):
        i = int(rng.integers(6))
        cand = [f.copy() for f in free]
        q = cand[i] + 0.25 * rng.normal(size=3)
        q /= np.linalg.norm(q)
        cand[i] = q
        if legal(cand):
            free = cand
    return free


def minimise(free0, seconds, rng):
    cur = [f.copy() for f in free0]
    cv = dprime_volume([CFIX] + RING + cur)
    best = (cv, [f.copy() for f in cur])
    t0 = time.time()
    step = 0.15
    while time.time() - t0 < seconds:
        i = int(rng.integers(6))
        cand = [f.copy() for f in cur]
        q = cand[i] + step * rng.normal(size=3)
        q /= np.linalg.norm(q)
        cand[i] = q
        if not legal(cand):
            continue
        v = dprime_volume([CFIX] + RING + cand)
        if v is None:
            continue
        if v < cv:
            cur, cv = cand, v
            if v < best[0]:
                best = (v, [f.copy() for f in cand])
        step = max(0.01, step * 0.9995)
    return best


def main():
    secs = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
    rng = np.random.default_rng(2026)
    base = dprime_volume([CFIX] + RING + c5_free())
    print(f"C5 configuration: vol D' = {base:.9f}")
    print(f"premise needed   : vol D' >= 5.540000")
    print(f"V_dod            : 5.550291\n")
    # PER-START CAP.  A first version passed `secs` to the first start, so `--seconds 600`
    # spent 600 s on it -- over the 120 s per-start cap the pilot request specifies
    # (review 2026-11-14_0738).  Every start, including the first, is now bounded by 120 s.
    per_start = min(120.0, max(5.0, secs / 7.0))
    best = (base, c5_free(), "C5")
    v, f = minimise(c5_free(), per_start, rng)
    print(f"local search from C5 ({per_start:.0f}s): {v:.9f}")
    if v < best[0]:
        best = (v, f, "C5 basin")
    for trial in range(6):
        f0 = random_free(rng)
        if f0 is None:
            print(f"  random start {trial}: no legal set found")
            continue
        v, f = minimise(f0, per_start, rng)
        print(f"  random start {trial}: {v:.9f}"
              + ("   <-- new minimum" if v < best[0] else ""))
        if v < best[0]:
            best = (v, f, f"random {trial}")
    print(f"\nMINIMUM vol D' found: {best[0]:.9f}   ({best[2]})")
    print(f"  premise 5.5400: {'HOLDS with slack %.6f' % (best[0]-5.54) if best[0] > 5.54 else 'FAILS'}")
    print(f"  V_dod = 5.550291: minimum is {best[0]-5.550291:+.6f} from it")
    return 0 if best[0] > 5.54 else 1


if __name__ == "__main__":
    sys.exit(main())
