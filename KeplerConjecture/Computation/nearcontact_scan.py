#!/usr/bin/env python3
"""Is the cut condition EVER non-vacuous in the near-contact regime?  A broad scan.

`fixture_nonuniform.py` found t* = 0 at 18 instances of one family.  Eighteen is not many, and one
family is one family.  This scans three:

  F1  FCC of cubic side a in [2.83, 3.00] (density 0.7393 down to 0.6206; Kepler is 0.7405), one
      site displaced along +x by a fraction of the contact slack;
  F2  tetragonal FCC: lattice (a, a, a t) with the same basis, t in [0.94, 1.06] -- a distortion
      that removes the cubic symmetry and so produces UNEQUAL cells;
  F3  FCC at a in [2.83, 3.00] with the displacement in a random rational direction rather than +x.

For each instance the cell volumes are computed EXACTLY (rational vertex enumeration), b is an exact
rational interval, and t* is the maximum of sum_U b/|delta^+(U)| over all 2^4 subsets.  A positive t*
would mean the cut condition constrains the capacity in the near-contact band.

WHAT A NEGATIVE RESULT MEANS.  t* = 0 everywhere says only that these families give the criterion
nothing: the deficits are all negative, so every finite U satisfies the condition at Phi = 0.  It is
evidence about the geometry of the near-contact regime, not a theorem about all packings.

Run: python3 nearcontact_scan.py            (~8 minutes)
"""
import itertools, json, os, random, sys
from fractions import Fraction as F
import fixture_nonuniform as FN
import cut_flow as CF

_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

def t_star_of(L, sites, R=F("2.13")):
    fx = FN.make_fixture(L, sites, R)
    scan = CF.exhaustive_cut_scan([F(x) for x in fx["b_lo"]], [tuple(e) for e in fx["edges"]])
    vols = [F(x) for x in fx["cell_volumes_exact"]]
    return scan["t_star"], vols, fx

def density(L, sites):
    detL = abs(FN.det3(*L))
    return F(len(sites)) * F(4, 3) * F(314159265358979323846, 10 ** 20) / detL

def f1():
    rows = []
    for i in range(18):                       # a = 3.00, 2.99, ..., 2.83
        a = F(300 - i, 100)
        L, S = FN.fcc_cubic(a)
        dx = FN.max_displacement_within_slack(L, S, 0)
        for j in range(11):                   # delta = 0, 0.1, ..., 1.0 of the slack
            frac = F(j, 10)
            S2 = [(S[0][0] + dx * frac, S[0][1], S[0][2])] + S[1:]
            t, vols, _ = t_star_of(L, S2)
            rows.append(dict(family="F1", a=str(a), frac=str(frac), delta=str(dx * frac),
                             density=float(density(L, S2)), t_star=str(t),
                             vols=[str(v) for v in vols]))
    return rows

def f2():
    rows = []
    for i in range(13):                       # t = 0.94 .. 1.06
        t_ax = F(94 + i, 100)
        a = F(283, 100)                        # near contact in-plane
        L = [[a, F(0), F(0)], [F(0), a, F(0)], [F(0), F(0), a * t_ax]]
        S = [(F(0), F(0), F(0)), (F(0), a / 2, a * t_ax / 2),
             (a / 2, F(0), a * t_ax / 2), (a / 2, a / 2, F(0))]
        if FN.min_separation(L, S) < 4:
            continue
        for frac in (F(0), F(1)):
            dx = FN.max_displacement_within_slack(L, S, 0)
            S2 = [(S[0][0] + dx * frac, S[0][1], S[0][2])] + S[1:]
            if FN.min_separation(L, S2) < 4:
                continue
            t, vols, _ = t_star_of(L, S2)
            rows.append(dict(family="F2", a=str(a), t_ax=str(t_ax), frac=str(frac),
                             density=float(density(L, S2)), t_star=str(t),
                             vols=[str(v) for v in vols]))
    return rows

def f3(seed=0, per_a=4):
    rng = random.Random(seed)
    rows = []
    for i in range(18):
        a = F(300 - i, 100)
        L, S = FN.fcc_cubic(a)
        dx0 = FN.max_displacement_within_slack(L, S, 0)
        for k in range(per_a):
            # a rational direction with small integer components
            while True:
                d = (F(rng.randint(-2, 2)), F(rng.randint(-2, 2)), F(rng.randint(-2, 2)))
                if any(d):
                    break
            lo, hi = F(0), dx0
            for _ in range(30):
                mid = (lo + hi) / 2
                S2 = [(S[0][0] + d[0] * mid, S[0][1] + d[1] * mid, S[0][2] + d[2] * mid)] + S[1:]
                if FN.min_separation(L, S2) >= 4:
                    lo = mid
                else:
                    hi = mid
            S2 = [(S[0][0] + d[0] * lo, S[0][1] + d[1] * lo, S[0][2] + d[2] * lo)] + S[1:]
            if FN.min_separation(L, S2) < 4:
                continue
            t, vols, _ = t_star_of(L, S2)
            rows.append(dict(family="F3", a=str(a), direction=[str(x) for x in d], delta=str(lo),
                             density=float(density(L, S2)), t_star=str(t),
                             vols=[str(v) for v in vols]))
    return rows

def main():
    allrows = []
    for name, fn in (("F1 FCC, x-displacement", f1),
                     ("F2 tetragonal FCC", f2),
                     ("F3 FCC, random direction", f3)):
        print("running %s ..." % name, flush=True)
        rows = fn()
        pos = [r for r in rows if F(r["t_star"]) > 0]
        print("   %3d instances, %d with t* > 0, max t* = %s"
              % (len(rows), len(pos), max((F(r["t_star"]) for r in rows), default=None)), flush=True)
        allrows += rows
    pos = [r for r in allrows if F(r["t_star"]) > 0]
    dmin = min(r["density"] for r in allrows); dmax = max(r["density"] for r in allrows)
    print("\nTOTAL %d instances, densities %.4f - %.4f (Kepler 0.7405)" % (len(allrows), dmin, dmax))
    print("      %d instances with t* > 0" % len(pos))
    if pos:
        for r in pos[:5]:
            print("      ", r)
    json.dump(dict(instances=len(allrows), with_positive_t_star=len(pos),
                   density_range=[dmin, dmax], rows=allrows),
              open(os.path.join(_OUT, "nearcontact_scan.json"), "w"), indent=1)
    print("wrote out/nearcontact_scan.json")
    return 0 if not pos else 1

if __name__ == "__main__":
    sys.exit(main())
