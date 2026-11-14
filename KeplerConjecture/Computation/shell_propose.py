#!/usr/bin/env python3
"""K15 shell proposer, corrected architecture: propose in Laguerre, certify in Main's basis.

WHY THIS FILE EXISTS SEPARATELY FROM shell_sos.py.
  shell_sos.py builds the linear program directly in Main's monomial basis u = pi|x|^2.
  That basis is numerically hostile: the Fourier matrix has M[0][k] = (2k+1)!!/2^k, so
  M[0][7] = 15836 and the solver must cancel large coefficients to produce a small p(0).
  The result reproduces the K15-C022 failure mode -- the LP returns box vertices, not
  candidates.  Main's own C-SHELL-001c note warns against exactly this.

  The repair is architectural and costs nothing in rigour: solve the LP where it is
  well conditioned (the Laguerre basis in t = 2 pi |x|^2, which is what exactcert.py
  already validates), then CONVERT the result exactly to Main's monomial basis and let
  Main's checker (shell_check.py) deliver the verdict.  The conversion p(u) = p_t(2u) is
  exact with rational coefficients, so nothing is lost.

  Consequence worth stating: a candidate accepted here has been validated by a checker
  written by another session in a different basis and with an independently written
  Fourier matrix.  That cross-validation is the point of the exercise.

Usage:
    python3 shell_propose.py --checker /path/to/shell_check.py --degree 13
"""
import argparse, contextlib, io, json, sys, time
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre
import exactcert as EC

PI_LO = F(31415926535, 10**10)
PI_HI = F(31415926539, 10**10)

def lag(k, t):
    return eval_genlaguerre(k, 0.5, t)

def basis(ts, K):
    ts = np.asarray(ts, float)
    M = np.array([[lag(k, t) for k in range(K + 1)] for t in ts])
    return M * np.exp(-ts / 2.0)[:, None]

def rational_T_HI(rho, digits=6):
    x = PI_LO * F(rho).limit_denominator(10**6) ** 2
    s = 10 ** digits
    return F((x.numerator * s) // x.denominator, s)

def solve_laguerre(K, T_LO, T_HI, Umax, use_eta, n, eps_shell, extra_hat=(), eps_q=None):
    """Variables c_0..c_K, eta.  q(0)=1.  minimise p(0) + n*eta."""
    tp = np.unique(np.concatenate([2 * np.linspace(float(T_LO), float(T_HI), 300),
                                   2 * np.linspace(float(T_LO), float(T_HI), 60)]))
    te = np.unique(np.concatenate([2 * (float(T_HI) + (Umax - float(T_HI)) *
                    (np.expm1(6 * np.linspace(0, 1, 600)) / np.expm1(6.0))),
                    2 * np.linspace(float(T_HI), Umax, 300)]))
    # The dual grid must resolve q over the whole range: degree-K Laguerre values oscillate
    # on a scale ~1/K in u, so the grid is deliberately dense and geometric near 0.
    th = np.unique(np.concatenate([2 * Umax * (np.expm1(7 * np.linspace(0, 1, 1500)) / np.expm1(7.0)),
                                   2 * np.linspace(0.0, Umax, 1500),
                                   2 * np.linspace(0.0, 3.0 * Umax, 3000),
                                   np.asarray(list(extra_hat), float)]))
    Ms, Me, Mh = basis(tp, K), basis(te, K), basis(th, K) * ((-1.0) ** np.arange(K + 1))[None, :]
    cw = np.maximum(np.abs(np.vstack([Ms, Me, Mh])).max(axis=0), 1e-14)
    Ms, Me, Mh = Ms / cw, Me / cw, Mh / cw
    rs = np.maximum(np.abs(Ms).max(axis=1), 1e-300)
    re = np.maximum(np.abs(Me).max(axis=1), 1e-300)
    rh = np.maximum(np.abs(Mh).max(axis=1), 1e-300)
    eta_col = -np.ones((len(rs), 1)) if use_eta else np.zeros((len(rs), 1))
    A_parts = [np.hstack([Ms / rs[:, None], eta_col]),
               np.hstack([Me / re[:, None], np.zeros((len(re), 1))]),
               np.hstack([-Mh / rh[:, None], np.zeros((len(rh), 1))]),
               # eta >= 0.  The coefficient must be -1: with +1 this row reads eta <= 0,
               # a needless tightening that also lets the objective drive eta -> -inf
               # (measured: eta hit the -1e5 box bound and the candidate was rejected).
               np.hstack([np.zeros((1, K + 1)),
                          -np.ones((1, 1)) if use_eta else np.zeros((1, 1))])]
    asym = np.zeros((1, K + 2)); asym[0, K] = -1.0
    A_parts.append(asym)
    A = np.vstack(A_parts)
    # A margin is required on BOTH sign conditions.  Without one on q >= 0 the LP parks q
    # exactly on a double root (measured: min q = -1.1e-07), which exact Sturm correctly
    # rejects and which no amount of grid refinement repairs, because the constraint is
    # already satisfied to solver tolerance at those points.
    if eps_q is None:
        eps_q = max(eps_shell, 1e-5)
    b = np.concatenate([-eps_shell * np.ones(len(rs)),
                        -eps_q * np.ones(len(re)), -eps_q * np.ones(len(rh)),
                        [0.0], [-1e-9]])
    L0 = np.array([lag(k, 0.0) for k in range(K + 1)]) / cw
    cq0 = np.concatenate([L0 * ((-1.0) ** np.arange(K + 1)), [0.0]])
    obj = np.concatenate([L0, [float(n) if use_eta else 0.0]])
    res = linprog(obj, A_ub=A, b_ub=b, A_eq=cq0[None, :], b_eq=[1.0],
                  bounds=[(-1e5, 1e5)] * (K + 2), method="highs")
    if not res.success:
        return None
    # COLUMN SCALING: the constraint row is (Ms/cw)[i,:] . x = sum_k Ms[i,k] (x_k/cw[k]),
    # so x_k = c_k*cw[k] and the recovery is c = x/cw.  (Dividing is correct; an earlier
    # "fix" to multiply was wrong and produced q(0) != 1, which the checker caught.)
    return res.x[:K + 1] / cw, (float(res.x[K + 1]) if use_eta else 0.0)

def to_monomial_u(c, K):
    """p(u) = sum_k c_k L_k^(1/2)(2u); return rational coefficients a_0..a_K in u."""
    ell = EC.laguerre_polys(K)                     # ell[k] in t
    a = [F(0)] * (K + 1)
    for k, ck in enumerate(c):
        for j, coef in enumerate(ell[k]):
            if coef:
                a[j] += F(ck) * coef * (F(2) ** j)  # t = 2u
    return a

def exact_verdict(SC, a, eta, K, T_LO, T_HI):
    M = SC.fourier_map(K)
    import sympy as sp
    b = []
    for i in range(K + 1):
        s = sp.Rational(0)
        for k in range(K + 1):
            s += sp.Rational(M[i, k]) * sp.Rational(a[k].numerator, a[k].denominator)
        b.append(F(int(sp.numer(s)), int(sp.denom(s))))
    with contextlib.redirect_stdout(io.StringIO()):
        ok = (SC.nonneg_on_half_line(b) and SC.le_on_interval(a, eta, T_LO, T_HI)
              and SC._ray(a, T_HI) and b[0] > 0 and a[0] > 0)
    return ok, b

def negative_intervals(b, K, umax=400.0, npts=400001):
    """Narrow negative excursions of q that a uniform grid can miss.

    A grid constraint q(t_i) >= 0 at spacing h cannot see a dip of width < h that crosses
    below zero and returns between two sample points.  This finds those dips exactly enough
    to cut them: locate real root intervals numerically, keep the ones where q < 0, and
    return their midpoints as extra constraint points.  The exact checker still decides;
    these points only steer the LP.
    """
    xs = np.linspace(0.0, umax, npts)
    vals = np.zeros_like(xs)
    for i, c in enumerate(b):                    # Horner in float, steering only
        vals = vals * xs + float(c)
    neg = np.where(vals < 0)[0]
    if neg.size == 0:
        return []
    # group contiguous negative runs, take the midpoint of each
    cuts, run = [], [neg[0]]
    for j in neg[1:]:
        if j == run[-1] + 1:
            run.append(j)
        else:
            cuts.append(xs[run[len(run) // 2]]); run = [j]
    cuts.append(xs[run[len(run) // 2]])
    return [2.0 * u for u in cuts]               # t = 2u


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", required=True)
    ap.add_argument("--degree", type=int, default=13)
    ap.add_argument("--Umax", type=float, default=40.0)
    ap.add_argument("--out", default="out/shell_propose.json")
    ap.add_argument("--tlo-exact", action="store_true",
                    help="use T_LO = 4*PI_LO = 12.566... instead of Main's conservative "
                         "default 12.  CE requires f <= 0 only for |x| >= 2, i.e. u >= 4*pi; "
                         "T_LO = 12 additionally demands it on 12 <= u < 4*pi, INSIDE the ball, "
                         "which costs bound and is not part of the theorem.")
    a = ap.parse_args()
    if a.degree % 2 == 0:
        raise SystemExit("degree must be odd (lc(q)=(-1)^K a_K and lc(p)=a_K must have "
                         "opposite signs; see shell_sos.py)")
    import importlib.util
    spec = importlib.util.spec_from_file_location("shell_check", a.checker)
    SC = importlib.util.module_from_spec(spec); spec.loader.exec_module(SC)
    K = a.degree
    t0 = time.time()
    cases = [("n=27 rho=2.05 UNCONDITIONAL (K15-C013a)", F(205, 100), 27, "unconditional"),
             ("n=12 rho=2.09 CONDITIONAL (K15-C019)",     F(209, 100), 12, "conditional")]
    rows = []
    for label, rho, n, status in cases:
        T_LO = (4 * PI_LO) if a.tlo_exact else F(12)
        T_HI = rational_T_HI(rho)
        print("\n== %s   T_LO=%s  T_HI=%s" % (label, T_LO, T_HI))
        for use_eta in (False, True):
            tag = "eta_free" if use_eta else "eta=0"
            got = None
            cuts = []
            # smallest margin first: the margin is a cost, so prefer the tightest one
            # that still survives rounding and exact verification.
            for eps in (1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
                for _round in range(12):          # cutting-plane refinement
                    sol = solve_laguerre(K, T_LO, T_HI, a.Umax, use_eta, n, eps, cuts)
                    if sol is None:
                        break
                    c, eta = sol
                    cr = [F(int(round(x * 10**9)), 10**9) for x in c]
                    er = F(int(round(eta * 10**9)), 10**9)
                    am = to_monomial_u(cr, K)
                    ok, b = exact_verdict(SC, am, er, K, T_LO, T_HI)
                    if ok:
                        for D in (10**6, 10**9, 10**12):
                            cr2 = [F(int(round(x * D)), D) for x in c]
                            er2 = F(int(round(eta * D)), D)
                            am2 = to_monomial_u(cr2, K)
                            ok2, b2 = exact_verdict(SC, am2, er2, K, T_LO, T_HI)
                            if ok2:
                                p0, q0 = am2[0], b2[0]
                                val = (p0 + n * er2) / q0
                                got = dict(eps=eps, denominator=D, eta=str(er2),
                                           a_monomial=[str(x) for x in am2],
                                           c_laguerre=[str(x) for x in cr2],
                                           p0=str(p0), q0=str(q0), cuts=len(cuts),
                                           delta_lo=float(4 * PI_LO / 3 * val),
                                           delta_hi=float(4 * PI_HI / 3 * val))
                                break
                        break
                    new = negative_intervals(b, K)
                    if not new:
                        break
                    cuts.extend(x for x in new if x not in cuts)
                if got:
                    break
            if got:
                print("   %-9s EXACT PASS (eps=%g, D=1e%d)  eta=%s  delta <= %.8f"
                      % (tag, got["eps"], len(str(got["denominator"])) - 1, got["eta"], got["delta_hi"]))
            else:
                print("   %-9s no exact pass at any margin/denominator" % tag)
            rows.append(dict(case=label, count=n, rho=str(rho), shell_status=status,
                             variant=tag, verdict=got))
    print("\n== comparison (exact, Main's checker) ==")
    for label, rho, n, status in cases:
        e0 = next((r["verdict"] for r in rows if r["case"] == label and r["variant"] == "eta=0"), None)
        e1 = next((r["verdict"] for r in rows if r["case"] == label and r["variant"] == "eta_free"), None)
        if e0 and e1:
            print("  %-40s eta=0 %.8f  eta>0 %.8f  gain %+.8f"
                  % (label, e0["delta_hi"], e1["delta_hi"], e0["delta_hi"] - e1["delta_hi"]))
        else:
            print("  %-40s eta=0: %s   eta>0: %s"
                  % (label, "PASS" if e0 else "no exact candidate",
                     "PASS" if e1 else "no exact candidate"))
    json.dump(dict(script="KeplerConjecture/Computation/shell_propose.py", degree=K,
                   basis_propose="Laguerre in t=2 pi|x|^2",
                   basis_certify="monomial u=pi|x|^2 (Main's shell_check)",
                   checker=a.checker, rows=rows, runtime_s=round(time.time() - t0, 2)),
              open(a.out, "w"), indent=1)
    print("\nwrote", a.out, "in %.1fs" % (time.time() - t0))

if __name__ == "__main__":
    main()
