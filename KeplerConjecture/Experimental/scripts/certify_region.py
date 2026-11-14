#!/usr/bin/env python3
"""
Certify a REGION of the C5 family, not a sample: every (theta, phi) in a rectangle, to a
two-sided enclosure.

This is the branch-and-bound atom applied for real.  The region is cut into boxes; each box
gets the rational sandwich of rigorous_cell_volume.box_volume, which is valid for every
configuration whose parameters lie in that box (the sin/cos ranges are the hull of the corner
values, legitimate because both are monotone on the ranges used).  The result is

    min over boxes of the certified LOWER end,  max over boxes of the certified UPPER end

and if the lower end exceeds a target, the target is certified for the whole continuum — not
merely observed at finitely many points.

Run:  python3 Experimental/scripts/certify_region.py [theta_lo] [theta_hi] [phi_lo] [phi_hi] [width]
Defaults: 110 111 35 36 0.1   (theta, phi in degrees; width in degrees)
Exit 0 iff every box certifies a volume above 0 (the trivial failure) and prints the min.
"""
import sys
from fractions import Fraction as F
from multiprocessing import Pool

import rigorous_cell_volume as R

TARGET = F(5763417470, 10 ** 9)      # the (P') threshold 5.763417470


def _job(args):
    t0, t1, p0, p1 = args
    lo, hi, _, _ = R.box_volume((t0 / 180, t1 / 180), (p0 / 180, p1 / 180))
    return (float(t0), float(p0), lo, hi)


def main():
    a = [F(x).limit_denominator(10 ** 6) if '.' not in x else F(x).limit_denominator(10 ** 6)
         for x in sys.argv[1:]]
    th_lo, th_hi, ph_lo, ph_hi, w = (a + [F(110), F(111), F(35), F(36), F(1, 10)])[:5]
    n_th = int(round((th_hi - th_lo) / w))
    n_ph = int(round((ph_hi - ph_lo) / w))
    jobs = []
    for i in range(n_th):
        for j in range(n_ph):
            t0 = th_lo + i * w
            p0 = ph_lo + j * w
            jobs.append((t0, t0 + w, p0, p0 + w))
    print(f"region theta in [{float(th_lo)}, {float(th_hi)}], phi in [{float(ph_lo)}, "
          f"{float(ph_hi)}], boxes of {float(w)} deg")
    print(f"  {len(jobs)} boxes, {min(4, len(jobs))} workers, ~18 s each")
    with Pool(min(4, len(jobs))) as pool:
        res = pool.map(_job, jobs, chunksize=1)
    lo = min(r[2] for r in res)
    hi = max(r[3] for r in res)
    worst = min(res, key=lambda r: r[2])
    print(f"\n  CERTIFIED for the whole region: [{float(lo):.9f}, {float(hi):.9f}]")
    print(f"  worst box at theta={worst[0]:.3f}, phi={worst[1]:.3f}")
    print(f"  (P') threshold {float(TARGET):.9f}")
    ok = lo > TARGET
    print(f"  every configuration in the region has vol Omega(w1) > threshold: {ok}"
          f"   (margin {float(lo - TARGET):+.6f})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
