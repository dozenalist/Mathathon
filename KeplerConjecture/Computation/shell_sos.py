#!/usr/bin/env python3
"""K15 shell proposer: structured route to a shell-allowance candidate, decided exactly.

ROLE.  This is a PROPOSER, not a certifier.  It searches a small structured family and then
hands every candidate to Main's exact checker (`shell_check.py`, K15-C018/C019/C022) for the
verdict.  A candidate that the checker rejects is not a bound, whatever the LP objective says.

BASIS (Main's, deliberately not mine).  u = pi*|x|^2, f = exp(-pi|x|^2) * sum_k a_k u^k,
so p(u) is a rational polynomial and q(u) = (M a)(u) with M the rational matrix in
shell_check.fourier_map.  This is a DIFFERENT parametrisation from Computation/exactcert.py
(Laguerre in t = 2 pi |x|^2); using Main's basis here is the point, so that the same file
certifies the result.

CONSTRAINTS (all decided by exact Sturm in shell_check):
    q(u) >= 0                 for u >= 0                 (fhat >= 0)
    p(u) <= eta               for T_LO <= u <= T_HI(rho) (shell allowance)
    p(u) <= 0                 for u >= T_HI(rho)         (outside the ball)
    q(0) > 0, and p(0) > 0    (a Cohn-Elkies certificate needs f(0) > 0)
with T_LO = 12 <= 4*pi and T_HI(rho) <= pi*rho^2, both rational and both checked.

WHY T_HI DEPENDS ON rho.  shell_check.check() hardcodes T_HI = 27/2 for rho = 2.09, but
pi*2.05^2 = 13.20 < 13.5, so that default is INVALID for rho = 2.05.  The individual
predicates (le_on_interval, _ray) are parameterised, so this file uses them directly with a
rational T_HI per rho and checks the containment.

COUNTS.  n = 12 at rho = 2.09 is CONDITIONAL on the Tammes-13 enclosure (K15-C019).
n = 27 at rho = 2.05 is UNCONDITIONAL by the volume bound K15-C013(a),
n <= floor((rho+1)^3) - 1 = floor(3.05^3) - 1 = 27.  Both are labelled in the output.

USAGE
    python3 shell_sos.py --checker /path/to/shell_check.py --degree 8
"""
import argparse, contextlib, io, json, sys, time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

def load_checker(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("shell_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def rational_upper_pi2(rho, digits=6):
    """T_HI with T_HI <= pi*rho^2, built from a rational lower bound for pi."""
    PI_LO = F(31415926535, 10**10)
    x = PI_LO * F(rho).limit_denominator(10**6) ** 2
    scale = 10 ** digits
    return F((x.numerator * scale) // x.denominator, scale)     # floor => safe

def build_lp(SC, K, rho, T_LO, T_HI, Umax, n_shell, n_ext, n_hat, use_eta):
    """Variables: a_0..a_K, eta.  Normalise q(0) = 1.  Minimise p(0) + n*eta."""
    u_shell = np.linspace(float(T_LO), float(T_HI), n_shell)
    u_ext = np.unique(np.concatenate([float(T_HI) + (Umax - float(T_HI)) *
                                      (np.expm1(5 * np.linspace(0, 1, n_ext)) / np.expm1(5.0)),
                                      np.linspace(float(T_HI), Umax, n_ext // 2)]))
    u_hat = np.unique(np.concatenate([Umax * (np.expm1(5 * np.linspace(0, 1, n_hat)) / np.expm1(5.0)),
                                      np.linspace(0.0, Umax, n_hat // 2)]))
    def mono(us):
        us = np.asarray(us, float)
        return np.array([[u ** k for k in range(K + 1)] for u in us])
    Ms = mono(u_shell); Me = mono(u_ext)
    # q values: coefficients b = M a, so the q-row in u is (M^T mono_row)
    M = np.array([[float(SC.fourier_map(K)[i, k]) for k in range(K + 1)] for i in range(K + 1)])
    # q(u) = sum_i b_i u^i with b = M a, so q(u) = sum_k a_k (sum_i M[i][k] u^i);
    # the coefficient row in a is therefore mono(u) @ M, NOT mono(u) @ M.T.
    Mh = mono(u_hat) @ M                         # rows: q(u) coefficient vector in a
    cw = np.maximum(np.abs(np.vstack([Ms, Me, Mh])).max(axis=0), 1e-14)
    Ms, Me, Mh = Ms / cw, Me / cw, Mh / cw
    rs = np.maximum(np.abs(Ms).max(axis=1), 1e-300)
    re = np.maximum(np.abs(Me).max(axis=1), 1e-300)
    rh = np.maximum(np.abs(Mh).max(axis=1), 1e-300)
    eta_col = -np.ones((len(rs), 1)) if use_eta else np.zeros((len(rs), 1))
    rows = [np.hstack([Ms / rs[:, None], eta_col]),               # p <= eta
            np.hstack([Me / re[:, None], np.zeros((len(re), 1))]),  # p <= 0
            np.hstack([-Mh / rh[:, None], np.zeros((len(rh), 1))]),  # q >= 0
            np.hstack([np.zeros((1, K + 1)), np.ones((1, 1)) if use_eta else np.zeros((1, 1))])]
    b = np.concatenate([np.zeros(len(rs)), np.zeros(len(re)), np.zeros(len(rh)), [0.0]])
    # asymptotic: lc(p) < 0  <=>  a_K < 0
    asym = np.zeros((1, K + 2)); asym[0, K] = -1.0
    rows.append(asym); b = np.concatenate([b, [-1e-9]])
    # p(0) > 0 is REQUIRED of a CE certificate and must be in the LP, not only in the
    # checker: without it the solver drives p(0) -> -inf through under-resolution (the
    # K15-C022 failure mode, reproduced and fixed here).
    pos0 = np.zeros((1, K + 2)); pos0[0, 0] = -1.0
    rows.append(pos0); b = np.concatenate([b, [-1e-9]])
    A = np.vstack(rows)
    # q(0) = 1
    q0row = np.concatenate([M[0, :] / cw, [0.0]])
    L0 = np.concatenate([np.array([0.0] * 1 + [0.0] * 0), [0.0]])
    p0row = np.concatenate([np.eye(1, K + 1, 0)[0] / cw, [0.0]])
    obj = p0row.copy()
    return A, b, q0row, p0row, cw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", required=True)
    ap.add_argument("--degree", type=int, default=8)
    ap.add_argument("--Umax", type=float, default=30.0)
    ap.add_argument("--out", default="out/shell_sos.json")
    a = ap.parse_args()
    if a.degree > 8:
        raise SystemExit("degree cap is 8 in this proposer (the SOS route is meant to scale)")
    if a.degree % 2 == 0:
        raise SystemExit(
            "degree must be ODD. In this basis M is upper triangular with diagonal (-1)^i, "
            "so lc(q) = (-1)^K a_K and lc(p) = a_K. p <= 0 at infinity needs a_K <= 0 while "
            "q >= 0 at infinity needs (-1)^K a_K >= 0; both hold only for K odd (for K even "
            "they force a_K = 0, i.e. the degree drops). Verified numerically: M[K][K] = (-1)^K.")
    SC = load_checker(a.checker)
    K = a.degree
    t0 = time.time()
    cases = [("n=27 rho=2.05 UNCONDITIONAL (K15-C013a)", F(205, 100), 27, "unconditional"),
             ("n=12 rho=2.09 CONDITIONAL (K15-C019)",    F(209, 100), 12, "conditional")]
    results = []
    for label, rho, n, status in cases:
        T_LO = F(12)
        T_HI = rational_upper_pi2(rho)
        print("\n== %s   T_LO=%s  T_HI=%s  (pi*rho^2 > %s)"
              % (label, T_LO, T_HI, float(F(31415926535, 10**10) * rho ** 2)))
        for use_eta in (False, True):
            A, b, q0row, p0row, cw = build_lp(SC, K, rho, T_LO, T_HI, a.Umax, 400, 500, 500, use_eta)
            obj = p0row.copy()
            if use_eta:
                obj = obj + np.concatenate([np.zeros(K + 1), [float(n)]])
            res = linprog(obj, A_ub=A, b_ub=b, A_eq=q0row[None, :], b_eq=[1.0],
                          bounds=[(-1e4, 1e4)] * (K + 2), method="highs")
            tag = "eta_free" if use_eta else "eta=0"
            if not res.success:
                print("   %-9s LP infeasible (%s)" % (tag, res.message[:40]))
                results.append(dict(case=label, count=n, rho=str(rho), shell_status=status,
                                    variant=tag, feasible=False, message=res.message))
                continue
            av = res.x[:K + 1] / cw
            eta = float(res.x[K + 1]) if use_eta else 0.0
            lp_obj = float(np.dot(av, np.eye(K + 1)[0])) + n * eta
            # ---- exact validation with Main's checker, for a ladder of denominators ----
            verdict = None
            for D in (10**4, 10**6, 10**8):
                ar = [F(int(round(x * D)), D) for x in av]
                er = F(int(round(eta * D)), D) if use_eta else F(0)
                bco = exact_q(SC, ar, K)
                ok = True
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    ok = ok and SC.nonneg_on_half_line(bco)
                    ok = ok and SC.le_on_interval(ar, er, T_LO, T_HI)
                    ok = ok and SC._ray(ar, T_HI)
                    ok = ok and (bco[0] > 0) and (F(ar[0]) > 0)
                if ok:
                    p0, q0 = F(ar[0]), F(bco[0])
                    val = (p0 + n * er) / q0
                    lo = 4 * F(31415926535, 10**10) / 3 * val
                    hi = 4 * F(31415926539, 10**10) / 3 * val
                    verdict = dict(denominator=D, eta=str(er), a=[str(x) for x in ar],
                                   b=[str(x) for x in bco], p0=str(p0), q0=str(q0),
                                   delta_lo=str(lo), delta_hi=str(hi),
                                   delta_hi_float=float(hi))
                    break
            if verdict:
                print("   %-9s LP obj=%.8f  EXACT PASS (D=1e%d)  eta=%s  delta <= %.8f"
                      % (tag, lp_obj, len(str(verdict["denominator"])) - 1, verdict["eta"],
                         verdict["delta_hi_float"]))
            else:
                print("   %-9s LP obj=%.8f  exact check FAILS at all denominators" % (tag, lp_obj))
            results.append(dict(case=label, count=n, rho=str(rho), shell_status=status,
                                variant=tag, feasible=True, lp_objective=lp_obj, eta=eta,
                                coefficients=[float(x) for x in av], verdict=verdict))
    # ---- comparison summary ----
    print("\n== comparison ==")
    for label, rho, n, status in cases:
        got = {r["variant"]: r for r in results if r["case"] == label and r.get("feasible")}
        e0 = got.get("eta=0", {}).get("verdict")
        e1 = got.get("eta_free", {}).get("verdict")
        if e0 and e1:
            print("  %-40s eta=0: %.8f   eta_free: %.8f   gain: %+.8f"
                  % (label, e0["delta_hi_float"], e1["delta_hi_float"],
                     e0["delta_hi_float"] - e1["delta_hi_float"]))
        else:
            print("  %-40s incomplete (see table)" % label)
    json.dump(dict(script="KeplerConjecture/Computation/shell_sos.py", degree=K,
                   basis="u = pi|x|^2 monomial (Main's)", checker=str(a.checker),
                   status="TESTED_FINITE for proposer; exact for any verdict != null",
                   rows=results, runtime_s=round(time.time() - t0, 2)), open(a.out, "w"), indent=1)
    print("\nwrote", a.out, "in %.1fs" % (time.time() - t0))

def exact_q(SC, ar, K):
    """q = M a exactly, as Fractions."""
    M = SC.fourier_map(K)
    import sympy as sp
    out = []
    for i in range(K + 1):
        s = sp.Rational(0)
        for k in range(K + 1):
            s += sp.Rational(M[i, k]) * sp.Rational(ar[k].numerator, ar[k].denominator)
        out.append(F(int(sp.numer(s)), int(sp.denom(s))))
    return out

if __name__ == "__main__":
    main()
