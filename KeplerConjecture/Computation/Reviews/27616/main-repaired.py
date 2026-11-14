#!/usr/bin/env python3
"""Small, runnable Cohn-Elkies two-point baseline in dimension 3.

EXPLORATORY.  This is a discretised linear program, not a certificate: the sign
conditions are imposed on finite grids, so its value is an *optimistic* bound
(the true LP optimum is an upper bound on it).  Promotion requires an exact SOS
identity; see Main/LOCAL_COMPUTE_REQUESTS.md (K15-COMPUTE-001, revised).

Conventions (frozen; K15-C001, K15-C007, K15-C013)
-------------------------------------------------
  packing      : Lambda subset R^3, |x-y| >= 2, balls of radius 1
  delta        : occupied-volume upper density
  c            : centre density, c = 3*delta/(4*pi), vol(B_1) = 4*pi/3
  fhat(t)      : int f(x) exp(-2*pi*i*<x,t>) dx          (no normalising factor)

  Radial variable: s = |x|^2 >= 0.  The Laguerre argument is  t = 2*pi*s.
  This distinction is the one that matters: with |x| >= 2 the sign region is
  s >= 4, i.e. t >= 8*pi ~ 25.133, NOT t >= 4.

  Basis:  phi_k(x) = exp(-pi*s) * L_k^(1/2)(2*pi*s),
          phi_k_hat = (-1)^k phi_k                          (radial d=3 Hermite).

  f    = sum_{k<=n} a_k phi_k      ->  P(t) = sum a_k L_k^(1/2)(t)
  fhat = sum_k (-1)^k a_k phi_k    ->  Q(t) = sum (-1)^k a_k L_k^(1/2)(t)

  (A2) fhat >= 0 everywhere   <=>  Q(t) >= 0 for t >= 0
  (A1) f <= 0 for |x| >= 2    <=>  P(t) <= 0 for t >= 8*pi
  Objective:  min f(0)/fhat(0),  f(0) = sum a_k c_k,  fhat(0) = sum (-1)^k a_k c_k,
              c_k = L_k^(1/2)(0) = (2k+1) * C(2k,k) / 4^k.

  The ratio is scale invariant, so the LP fixes fhat(0) = 1 and minimises f(0).
"""
import argparse, json, sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre

def lag(k, t):
    return eval_genlaguerre(k, 0.5, t)

def ck(k):
    from math import comb
    return (2 * k + 1) * comb(2 * k, k) / 4.0 ** k

def grid(lo, hi, n, geometric=True):
    if not geometric:
        return np.linspace(lo, hi, n)
    # dense near `lo`, sparse at `hi`, plus explicit far points
    x = lo + (hi - lo) * (np.expm1(np.linspace(0, 6.0, n)) / np.expm1(6.0))
    return np.unique(np.concatenate([x, [hi * 2, hi * 5, hi * 20]]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--degree", type=int, default=10)
    ap.add_argument("--grid", type=int, default=3000)
    ap.add_argument("--tmax", type=float, default=120.0)
    ap.add_argument("--out", default="Computation/out/ce_laguerre.json")
    args = ap.parse_args()
    n = args.degree
    t0 = time.time()

    # --- constraint sets -------------------------------------------------
    t_hat = grid(0.0, args.tmax, args.grid)                 # Q >= 0
    t_f = grid(8.0 * np.pi, args.tmax, args.grid)           # P <= 0
    M_hat = np.array([[(-1) ** k * lag(k, t) for k in range(n + 1)] for t in t_hat])
    M_f = np.array([[lag(k, t) for k in range(n + 1)] for t in t_f])

    c = np.array([ck(k) for k in range(n + 1)])
    pm = np.array([(-1) ** k * c[k] for k in range(n + 1)])

    # Row scaling: the Laguerre values grow like t^k, so scale each constraint
    # row by its max modulus.  Without this HiGHS reports spurious infeasibility.
    def scaled(M):
        sc = np.maximum(np.abs(M).max(axis=1), 1e-300)
        return M / sc[:, None]
    M_hat_s, M_f_s = scaled(M_hat), scaled(M_f)

    # variables a_0..a_n ; minimise f(0) = c . a  subject to pm . a = 1
    B = [(-1e6, 1e6)] * (n + 1)
    res_free = linprog(c, A_ub=np.vstack([M_f_s, -M_hat_s]), b_ub=np.zeros(len(t_f) + len(t_hat)),
                       A_eq=pm[None, :], b_eq=[1.0], bounds=B, method="highs")
    # Rigorous floor: fhat(0) = int f = 1 and f <= 0 off |x| < 2 give
    #   1 <= f(0) * vol(B(0,2)) = f(0) * 32 pi / 3,  i.e.  f(0) >= 3/(32 pi).
    floor = 3.0 / (32.0 * np.pi)
    res_floor = linprog(c, A_ub=np.vstack([M_f_s, -M_hat_s, -c[None, :] / np.abs(c).max()]),
                        b_ub=np.concatenate([np.zeros(len(t_f) + len(t_hat)), [-floor / np.abs(c).max()]]),
                        A_eq=pm[None, :], b_eq=[1.0], bounds=B, method="highs")

    # --- independent fine-grid audit of the floored solution -------------
    a = np.zeros(n + 1) if res_floor.x is None else res_floor.x
    ratio = float(c @ a)
    tfine = np.concatenate([np.linspace(0, 400, 400001),
                            np.geomspace(400, 1e5, 20000)])
    Pf = np.array([lag(k, tfine) for k in range(n + 1)])
    Qv = (-1) ** np.arange(n + 1)[:, None] * a[:, None] * Pf
    Pv = a[:, None] * Pf
    qmin = float(Qv.sum(0).min()); qarg = float(tfine[int(Qv.sum(0).argmin())])
    m = tfine >= 8 * np.pi
    pmax = float(Pv[:, m].sum(0).max()); parg = float(tfine[m][int(Pv[:, m].sum(0).argmax())])

    out = {
        "status": "EXPLORATORY local repair; finite grid only",
        "conclusion": "Both sign matrices included; finite-grid diagnostic only, no global certificate.",
        "degree": n, "basis": "exp(-pi s) L_k^{1/2}(2 pi s), s = |x|^2",
        "sign_region_f_nonpositive": "t = 2*pi*s >= 8*pi  (|x| >= 2)",
        "grid_points": int(len(t_f)), "tmax": args.tmax,
        "lp_free_status": int(res_free.status),
        "lp_free_objective": (None if res_free.x is None else float(c @ res_free.x)),
        "rigorous_floor_f0": floor,
        "lp_floored_status": int(res_floor.status),
        "lp_floored_f0": ratio,
        "delta_from_floor": float(4 * np.pi / 3 * floor),
        "coefficients": [float(x) for x in a],
        "audit_min_fhat": qmin, "audit_min_fhat_at_t": qarg,
        "audit_max_f_on_region": pmax, "audit_max_f_at_t": parg,
        "seconds": round(time.time() - t0, 2),
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({k: out[k] for k in
          ("degree", "lp_free_status", "lp_free_objective", "rigorous_floor_f0",
           "lp_floored_status", "lp_floored_f0", "delta_from_floor", "seconds")}, indent=2))

if __name__ == "__main__":
    main()
