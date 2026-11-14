#!/usr/bin/env python3
"""K15 callable evaluator interface for Experimental (E) and Counterexamples (X).

E supplies a candidate auxiliary function; this module reports the resulting
three-dimensional bound in BOTH normalisations, plus the sign diagnostics that decide
whether the candidate is anywhere near admissible. It never claims a bound is proved.

TWO INPUT FORMS
  1. bound_from_callable(f, fhat)      -- any radial f and its radial transform, as
                                          python callables of the radius r >= 0.
                                          fhat need not be supplied if compute_fhat=True,
                                          in which case it is obtained by radial quadrature.
  2. bound_from_coefficients(c)        -- coefficients in the Gaussian-Laguerre basis
                                          phi_k(r) = L_k^{1/2}(2 pi r^2) e^{-pi r^2},
                                          the family used by ce3_baseline.py.

WHAT IS COMPUTED (native convention A, see k15conv.py)
  A(f)  = f(0)/fhat(0)          -> rho_A <= A(f)
  Delta = (pi/6) A(f)           -> occupied-volume bound, unit-radius packing
  max f on [r0, R], min fhat on [0, S], and their locations
  Pass/fail flags: f <= 0 off r0, fhat >= 0 everywhere (grid evidence only)

STATUS OF ANY RESULT: TESTED_FINITE. Grid evidence is not a proof. A usable certificate
needs a global sign argument or interval covering with certified tails; that is a separate
obligation and is recorded as remaining_obligations in every returned dict.
"""
import sys
import numpy as np
from scipy.integrate import quad
from scipy.special import eval_genlaguerre
from mpmath import mp, mpf, pi
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import k15conv as CV

mp.dps = 25

def _radial_fourier(f, s):
    """Radial Fourier transform in R^3 with e^{-2 pi i <x,t>}:
       fhat(s) = (2/s) int_0^inf r f(r) sin(2 pi s r) dr      (s>0),
       fhat(0) = 4 pi int_0^inf r^2 f(r) dr."""
    if s < 1e-12:
        return 4 * pi_over() * quad(lambda r: r * r * f(r), 0, np.inf, limit=400)[0]
    return (2.0 / s) * quad(lambda r: r * f(r) * np.sin(2 * np.pi * s * r),
                            0, np.inf, limit=400)[0]

def pi_over():
    from math import pi as P
    return P

def bound_from_callable(f, fhat=None, r0=1.0, R=6.0, S=6.0, n=4001, compute_fhat=False):
    f0 = f(0.0)
    if fhat is None:
        fhat = (lambda s: _radial_fourier(f, s)) if compute_fhat else None
    if fhat is None:
        raise ValueError("supply fhat, or set compute_fhat=True (quadrature, slower)")
    fh0 = fhat(0.0)
    if fh0 == 0 or f0 == 0:
        return dict(ok=False, reason="f(0) or fhat(0) is zero")
    A = f0 / fh0
    rhoA = float(A)
    D = float(CV.rhoA_to_Delta(rhoA))
    rr = np.linspace(r0, R, n); ss = np.linspace(0.0, S, n)
    fv = np.array([f(x) for x in rr]); fhv = np.array([fhat(s) for s in ss])
    imax = int(np.argmax(fv)); imin = int(np.argmin(fhv))
    return dict(
        ok=True, A=rhoA, rho_A_bound=rhoA, Delta_bound=D, Kepler=float(CV.KEPLER_DELTA),
        gap_absolute=D - float(CV.KEPLER_DELTA), gap_relative=D / float(CV.KEPLER_DELTA) - 1.0,
        rho_B=float(CV.rhoA_to_rhoB(rhoA)),
        max_f_outside=float(fv[imax]), argmax_f=float(rr[imax]),
        min_fhat=float(fhv[imin]), argmin_fhat=float(ss[imin]),
        f_nonpositive_off_r0=bool(fv[imax] <= 1e-9),
        fhat_nonnegative=bool(fhv[imin] >= -1e-9),
        status="TESTED_FINITE", convention="native A (sep1 number) + converted Delta",
        remaining_obligations=["global sign of f off r0", "global fhat >= 0",
                               "tail decay for admissibility", "interval/exact certification"],
        certified=False,
    )

def bound_from_coefficients(c, r0=1.0, R=6.0, S=6.0, n=4001):
    c = np.asarray(c, float); K = len(c) - 1
    def f(x):
        t = 2 * np.pi * x * x
        return sum(c[k] * eval_genlaguerre(k, 0.5, t) for k in range(K + 1)) * np.exp(-t)
    def fhat(x):
        t = 2 * np.pi * x * x
        return sum(((-1) ** k) * c[k] * eval_genlaguerre(k, 0.5, t)
                   for k in range(K + 1)) * np.exp(-t)
    out = bound_from_callable(f, fhat, r0=r0, R=R, S=S, n=n)
    out["degree"] = K
    return out

if __name__ == "__main__":
    import json
    # self-test on the stored K=31 baseline coefficients
    try:
        blob = json.load(open("out/ce3_K31_g1200.json"))
        r = bound_from_coefficients(blob["coefficients"])
        print("self-test on out/ce3_K31_g1200.json coefficients")
        print("  rho_A <= %.9f   Delta <= %.9f   gap %+.4f%%"
              % (r["rho_A_bound"], r["Delta_bound"], 100 * r["gap_relative"]))
        print("  f<=0 off r0: %s (max %.2e at r=%.3f)" % (r["f_nonpositive_off_r0"], r["max_f_outside"], r["argmax_f"]))
        print("  fhat>=0     : %s (min %.2e at s=%.3f)" % (r["fhat_nonnegative"], r["min_fhat"], r["argmin_fhat"]))
        print("  status:", r["status"], "| certified:", r["certified"])
    except FileNotFoundError:
        print("run ce3_baseline.py first to create the self-test input")
