#!/usr/bin/env python3
"""K15 reproducible Cohn-Elkies baseline in dimension 3 (radial Gaussian-Laguerre basis).

WHY THIS EXISTS
  A control with a known strict gap (Li 2024, Thm 6.1): ordinary CE cannot be sharp in
  d=3, so any candidate bound must be compared against this number and must be produced
  by a *different* mechanism. This script is the control. It is NOT a route to the
  Kepler bound and no output of it should be described as one.

CONVENTION (native, "A" = sep1/number; see k15conv.py for the unit-radius conversion)
  min centre separation 1, balls radius 1/2, objective rho_A = centres per unit volume
  transform  fhat(t) = int_{R^3} f(x) e^{-2 pi i <x,t>} dx
  basis      phi_k(x) = L_k^{1/2}(2 pi |x|^2) e^{-pi |x|^2},   fhat_k = (-1)^k phi_k
             (radial eigenfunctions of the Fourier transform; eigenvalue (-1)^k)
  LP         minimise 1/fhat(0)  over  f = sum_{k<=K} c_k phi_k
             s.t.  f(0) = 1,      f(r) <= 0  for r in [r0, Rmax],
                                  fhat(s) >= 0 for s in [0, Smax],
                                  (-1)^K c_K >= 0   (sign at infinity; K odd)
  report     rho_A <= 1/fhat(0)   and   Delta <= (pi/6)/fhat(0)

  Why r0: the sharp threshold for a certificate normalised f(0)=fhat(0)=1 is
  r0 = 2^(1/6) = 1.1225, NOT the contact distance 1. r0=1 is the plain CE control.

STATUS
  Output is TESTED_FINITE: the sign conditions are imposed on a finite grid. A rigorous
  bound additionally needs a global sign/positivity argument or an interval covering with
  certified tails. Reported values are therefore numerical evidence, never certificates.

USAGE
  python3 ce3_baseline.py --degree 11 --grid 400 --r0 1.0 --out /tmp/small.json
"""
import argparse, json, sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre
from mpmath import mp, mpf, pi, sqrt

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import k15conv as CV

mp.dps = 30

def lag(k, t):
    return eval_genlaguerre(k, 0.5, t)

def basis_row(u, K, dual=False):
    """Row of design matrix at t = 2 pi r^2 ; dual flips (-1)^k."""
    v = np.array([lag(k, u) for k in range(K + 1)]) * np.exp(-u / 2.0)
    if dual:
        v[1::2] *= -1.0
    return v

def solve(K, grid, r0, rmax, smax, eps_pos=0.0):
    t = 2 * np.pi * np.linspace(r0**2, rmax**2, grid)
    u = 2 * np.pi * np.linspace(0.0, smax**2, grid)
    A = np.vstack([np.array([basis_row(x, K) for x in t]),
                   -np.array([basis_row(x, K, True) for x in u])])
    b = np.zeros(A.shape[0])
    e = np.zeros((1, K + 1)); e[0, K] = -1.0          # -c_K <= 0
    A = np.vstack([A, e]); b = np.concatenate([b, [0.0]])
    scale = np.max(np.abs(A), axis=1)
    A /= scale[:, None]; b /= scale
    b0 = np.array([lag(k, 0.0) for k in range(K + 1)])
    obj = -((-1.0) ** np.arange(K + 1)) * b0          # maximise fhat(0)
    res = linprog(obj, A_ub=A, b_ub=b, A_eq=b0[None, :], b_eq=[1.0],
                  bounds=[(None, None)] * (K + 1), method="highs")
    return res

def evaluate(c, K, r, dual=False):
    r = np.atleast_1d(np.asarray(r, float))
    t = 2 * np.pi * r * r
    out = np.empty_like(t)
    for i, x in enumerate(t):
        out[i] = basis_row(x, K, dual) @ c
    return out

def diagnose(c, K, r0):
    rr = np.linspace(0, 12, 400001)
    f = evaluate(c, K, rr); fh = evaluate(c, K, rr, True)
    mask = rr >= r0
    return dict(
        max_f_outside=float(f[mask].max()), argmax_f=float(rr[mask][np.argmax(f[mask])]),
        min_fhat=float(fh.min()), argmin_fhat=float(rr[np.argmin(fh)]),
        max_f_inside=float(f[~mask].max()) if (~mask).any() else None,
        n_sign_change_f=int(np.sum(np.diff(np.sign(f[mask])) != 0)),
        note="grid evidence only; not a certificate",
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--degree", type=int, default=11)
    ap.add_argument("--grid", type=int, default=400)
    ap.add_argument("--r0", type=float, default=1.0)
    ap.add_argument("--rmax", type=float, default=5.0)
    ap.add_argument("--smax", type=float, default=5.0)
    ap.add_argument("--out", default="ce3_baseline_out.json")
    ap.add_argument("--digits", type=int, default=12, help="rounding digits for stored coefficients")
    a = ap.parse_args()
    if a.degree % 2 == 0:
        sys.exit("degree must be odd (asymptotic sign condition)")
    t0 = time.time()
    res = solve(a.degree, a.grid, a.r0, a.rmax, a.smax)
    if not res.success:
        print("SOLVER FAILED:", res.message); sys.exit(2)
    c = res.x
    fh0 = float(-res.fun)
    # CE Theorem 3.2 form: a certificate with f(0)=1 and f <= 0 off radius r0 bounds
    # the centre density of a minimum-distance-r0 packing by r0^n f(0)/fhat(0).  On
    # rescaling to minimum distance 1 the count density scales by r0^n, so the native
    # number density here is r0^3/fhat(0).  Omitting r0^3 (as an earlier revision did)
    # understates every r0 != 1 run by that factor -- e.g. 2^(1/2) at r0 = 2^(1/6).
    rhoA = (a.r0 ** 3) / fh0
    D = float(CV.rhoA_to_Delta(rhoA))
    kep = float(CV.KEPLER_DELTA)
    diag = diagnose(c, a.degree, a.r0)
    out = dict(
        script="KeplerConjecture/Computation/ce3_baseline.py",
        convention_native="A (min separation 1, number density)",
        transform="fhat(t) = int f(x) exp(-2 pi i <x,t>) dx",
        basis="L_k^{1/2}(2 pi |x|^2) exp(-pi |x|^2), eigenvalue (-1)^k",
        degree=a.degree, grid=a.grid, r0=a.r0, rmax=a.rmax, smax=a.smax,
        r0_scale_factor=a.r0 ** 3,
        r0_note=("rho_A = r0^3 * f(0)/fhat(0); the r0^3 is the sphere-volume scaling "
                 "and is 1 only at r0 = 1"),
        solver="scipy.optimize.linprog / HiGHS", numpy=np.__version__,
        rho_A_bound=rhoA, fhat0=fh0,
        Delta_bound=D, Kepler=kep,
        gap_absolute=D - kep, gap_relative=D / kep - 1.0,
        Delta_li_lower=float(CV.rhoB_to_Delta(mpf("0.18398089"))),
        Delta_ce03=float(CV.PUBLISHED["ce03_lp"][0]),
        Delta_cds_general3pt=float(CV.PUBLISHED["cds22_general_3pt"][0]),
        Delta_dodecahedral=float(CV.PUBLISHED["dodecahedral_HM10"][0]),
        diagnostics=diag, status="TESTED_FINITE",
        certification="none: sign conditions imposed on a finite grid only",
        # store full double precision (17 sig digits) so that re-evaluation from the
        # stored file reproduces Delta; a fixed low-digit rounding changes fhat(0) and
        # with it the reported bound, which was a real inconsistency in revision 1.
        coefficients=[float(x) for x in c],
        coefficient_format="IEEE double, repr precision (17 significant digits)",
        Delta_from_stored_coefficients=None,   # filled below
        runtime_s=round(time.time() - t0, 2),
    )
    import evaluator as EV
    rt = EV.bound_from_coefficients(out["coefficients"], r0=a.r0)
    out["Delta_from_stored_coefficients"] = rt["Delta_bound"]
    out["re_evaluation_gap"] = rt["Delta_bound"] - D
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    print("degree K=%d grid=%d r0=%.4f" % (a.degree, a.grid, a.r0))
    print("  r0 = %.6f -> scale factor r0^3 = %.6f" % (a.r0, a.r0 ** 3))
    print("  rho_A <= %.9f     (FCC sqrt2 = %.9f)" % (rhoA, float(CV.FCC_RHO_A)))
    print("  Delta <= %.9f     (Kepler = %.9f)" % (D, kep))
    print("  gap    = %+.9f  (%+.3f%% of Kepler)" % (D - kep, 100 * (D / kep - 1)))
    print("  reference: CE03 %.6f | CDS general 3pt %.6f | Li lower %.6f | dodecahedral %.7f"
          % (out["Delta_ce03"], out["Delta_cds_general3pt"], out["Delta_li_lower"], out["Delta_dodecahedral"]))
    print("  diagnostics: max f outside r0 = %.2e (at r=%.3f), min fhat = %.2e (at s=%.3f)"
          % (diag["max_f_outside"], diag["argmax_f"], diag["min_fhat"], diag["argmin_fhat"]))
    print("  status: TESTED_FINITE (grid evidence only; not a certificate)")
    print("  wrote", a.out, "in %.1fs" % out["runtime_s"])

if __name__ == "__main__":
    main()
