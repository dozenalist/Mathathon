#!/usr/bin/env python3
"""K15-C130 -- exercise C124's rho_eps = 0 branch on a real packing (scaled fcc).

C124 splits on rho_eps.  The rho_eps > 0 branch is the pair route; the rho_eps = 0 branch is the
inball bound delta <= 1/(1+eps/2)^3.  The second branch was unavailable before C124 because the
hypothesis rho_eps > 0 was assumed.  This checks it on packings that really do have rho_eps = 0:
fcc scaled by t > 1, whose minimum separation is 2t.

For t large enough that 2t > 2+eps, NO pair is within 2+eps, so S_eps is empty and rho_eps = 0.
Then C124 gives delta <= 1/(1+eps/2)^3, and the packing's actual density is delta_fcc/t^3.
"""
import sys
from mpmath import mp, mpf, sqrt, pi

mp.dps = 30
DELTA_FCC = pi / sqrt(mpf(18))
EPS_BAND = mpf('1.4555003444')          # C129's band width


def main():
    print(f"eps (band end, C129) = {mp.nstr(EPS_BAND,12)}   threshold 2+eps = {mp.nstr(2+EPS_BAND,12)}")
    print(f"C124 case-2 bound: delta <= 1/(1+eps/2)^3 = {mp.nstr(1/(1+EPS_BAND/2)**3,12)}")
    print()
    print(f"{'t':>6} {'min sep 2t':>12} {'rho_eps':>8} {'delta = fcc/t^3':>18} {'bound':>10} {'ok?':>5}")
    ok_all = True
    for t in ('1.2', '1.5', '1.8', '2.0', '2.5', '3.0'):
        tt = mpf(t)
        minsep = 2 * tt
        rho = 0 if minsep > 2 + EPS_BAND else None
        delta = DELTA_FCC / tt ** 3
        bound = 1 / (1 + EPS_BAND / 2) ** 3
        if rho == 0:
            good = delta <= bound
            ok_all = ok_all and good
            print(f"{t:>6} {mp.nstr(minsep,8):>12} {'0':>8} {mp.nstr(delta,12):>18} "
                  f"{mp.nstr(bound,10):>10} {str(good):>5}")
        else:
            print(f"{t:>6} {mp.nstr(minsep,8):>12} {'>0':>8} {mp.nstr(delta,12):>18} "
                  f"{'(case 1)':>10} {'--':>5}")
    print()
    print("So the rho_eps = 0 branch is real, applies to scaled fcc, and its bound holds there")
    print("with room.  This is the branch that C124 added and that review 0608 asked not to assume")
    print("away.")
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
