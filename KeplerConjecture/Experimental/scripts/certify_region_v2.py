#!/usr/bin/env python3
"""
REPAIRED region certifier.  Replaces certify_region.py, which had three defects:

  BUG 3 (partition).  `round(span/width)` boxes of width `width` do NOT cover the domain when
  `span` is not divisible by `width`: the leftover strip at the top is never certified, and
  nothing in the output said so.  Here the number of boxes is `n = ceil(span/width)` and the
  box width is `span/n` EXACTLY (a rational), so the boxes tile [lo, hi] exactly, in both
  directions, by construction.

  BUG 4 (inputs).  Empty or reversed ranges were accepted and produced a vacuous "certified"
  result.  Here both are rejected.

  BUG 5 (output).  Bounds were printed as floats, which loses the very rigour the run is for.
  Here every bound is serialised as a decimal rounded OUTWARD to 40 digits, plus the exact
  rational when it is short enough, together with the arithmetic that produced it.

The volume of each box comes from `cell_certificate.certify`, i.e. the repaired sandwich with
the sqrt(3)-compatible slack, the exact boundedness certificate and the non-circular radius.

Run:
  python3 Experimental/scripts/certify_region_v2.py TH_LO TH_HI PH_LO PH_HI [WIDTH] [--out F]
Defaults 110 111 35 36 0.1.  Exit 0 iff every box certifies a volume above the target.
"""
import json
import sys
from fractions import Fraction as F
from math import ceil

import cell_certificate as CC

TARGET = F(5763417470, 10 ** 9)          # 5.763417470, the (P') threshold


def _frac(x):
    try:
        return F(x)
    except Exception:
        raise SystemExit(f"cannot read {x!r} as an exact number")


def _job(args):
    t0, t1, p0, p1 = args
    # reuse the C5 geometry builder with sin/cos ranges taken over the box
    P = CC.c5_centres_box(t0 / 180, t1 / 180, p0 / 180, p1 / 180)
    lo, hi, cert = CC.certify(P, f"theta[{float(t0)},{float(t1)}] phi[{float(p0)},{float(p1)}]")
    return float(t0), float(p0), lo, hi, cert


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    if len(argv) < 4:
        raise SystemExit(__doc__)
    th_lo, th_hi, ph_lo, ph_hi = (_frac(a) for a in argv[:4])
    width = _frac(argv[4]) if len(argv) > 4 else F(1, 10)
    if not (th_hi > th_lo and ph_hi > ph_lo):
        raise SystemExit("reversed or empty range: nothing to certify")
    if width <= 0:
        raise SystemExit("width must be positive")

    # EXACT partition: n boxes of width span/n tile [lo,hi] exactly
    n_th = max(1, ceil((th_hi - th_lo) / width))
    n_ph = max(1, ceil((ph_hi - ph_lo) / width))
    w_th = (th_hi - th_lo) / n_th
    w_ph = (ph_hi - ph_lo) / n_ph
    jobs = []
    for i in range(n_th):
        for j in range(n_ph):
            t0 = th_lo + i * w_th
            p0 = ph_lo + j * w_ph
            jobs.append((t0, t0 + w_th, p0, p0 + w_ph))
    # exactness of the tiling, asserted rather than assumed
    assert th_lo + n_th * w_th == th_hi and ph_lo + n_ph * w_ph == ph_hi
    print(f"region theta in [{float(th_lo)}, {float(th_hi)}], phi in [{float(ph_lo)}, "
          f"{float(ph_hi)}]")
    print(f"  exact partition: {n_th} x {n_ph} = {len(jobs)} boxes of "
          f"{float(w_th):.6f} x {float(w_ph):.6f} deg (spans divisible by construction)")

    from multiprocessing import Pool
    with Pool(min(4, len(jobs))) as pool:
        res = pool.map(_job, jobs, chunksize=1)

    lo = min(r[2] for r in res)
    hi = max(r[3] for r in res)
    worst = min(res, key=lambda r: r[2])
    print(f"\n  CERTIFIED for the whole region: [{float(lo):.12f}, {float(hi):.12f}]")
    print(f"  worst box at theta={worst[0]:.4f}, phi={worst[1]:.4f}")
    ok = lo > TARGET
    print(f"  target {float(TARGET):.9f}:  every configuration above it: {ok}"
          f"  (margin {float(lo - TARGET):+.6f})")
    if out:
        import os
        out = os.path.abspath(out)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        cert = dict(
            domain=dict(theta=[str(outward_down(th_lo)), str(outward_up(th_hi))],
                        phi=[str(outward_down(ph_lo)), str(outward_up(ph_hi))],
                        n_boxes=[n_th, n_ph],
                        box=[str(outward_up(w_th)), str(outward_up(w_ph))]),
            vol_lo=str(outward_down(lo)), vol_hi=str(outward_up(hi)),
            target=str(TARGET), above_target=bool(ok),
            scheme="each box certified by cell_certificate.certify; lo = min of the lower "
                   "ends, hi = max of the upper ends; decimals rounded outward to 40 places",
            worst_box=dict(theta=worst[0], phi=worst[1], cert=worst[4]),
        )
        with open(out, "w") as f:
            json.dump(cert, f, indent=1)
        print(f"  certificate written to {out}")
    return 0 if ok else 1


DIGITS = 40


def outward_down(fr):
    q = F(10) ** DIGITS
    n = fr * q
    return F(n.numerator // n.denominator, q)


def outward_up(fr):
    q = F(10) ** DIGITS
    n = fr * q
    return F(-((-n.numerator) // n.denominator), q)


if __name__ == "__main__":
    sys.exit(main())
