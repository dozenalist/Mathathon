#!/usr/bin/env python3
"""K15 shell-bench: count-strengthened two-point bound vs the SAME-DEGREE eta=0 control.

THE MATHEMATICS (derived here, not asserted)
  Unit balls, centre separation 2, f admissible with fhat >= 0.  Suppose
    (SHELL)   at most 12 centres lie within distance rho of any centre,
    (A1)      f(x) <= eta   for 2 <= |x| <= rho          (eta >= 0),
    (A2)      f(x) <= 0     for |x| >= rho.
  For a periodic packing with period lattice L, covolume V and N centres per cell,
  Poisson summation gives
      sum_{x,y} sum_{lam} f(x-y+lam) = (1/V) sum_mu fhat(mu) |sum_x e^{2 pi i <mu,x>}|^2
                                    >= N^2 fhat(0)/V.
  On the left the N diagonal terms contribute N f(0); every other term is a difference
  of two distinct centres, so |x-y+lam| >= 2, and by (A1),(A2) each is at most eta,
  with at most 12 such terms per centre by (SHELL).  Hence
      N f(0) + 12 N eta >= N^2 fhat(0)/V,
  i.e. centre density <= (f(0) + 12 eta)/fhat(0), and in occupied-volume density
      Delta <= (4 pi/3) (f(0) + 12 eta)/fhat(0).                        (*)

  The count-strengthening framework is that of de Laat, de Oliveira Filho and
  Vallentin, "Upper bounds for packings of spheres of several radii",
  Forum Math. Sigma 2 (2014) e23, arXiv:1206.2608.  This file is an
  implementation of that framework's count idea at degree K in one dimension family;
  it is NOT a new mechanism and NOT a new theorem.

** (SHELL) IS CONDITIONAL. **  rho = 2.09 gives a shell of positive width, and "at most
  12 centres within distance rho" is NOT the kissing-number theorem (which concerns
  distance exactly 2).  It is assumed here and every output carries
  conditional_on_shell_count = true.  Experimental owns the check.

WHY eta CAN HELP.  (A1) is a WEAKER constraint on f than f <= 0 on the shell, while the
  objective charges 12*eta.  Whether the trade is favourable is an empirical question
  at each degree, which is what this script measures.  The eta = 0 case in the same code
  path, same basis, same degree, is the control.

STATUS: every number is TESTED_FINITE.  Signs are checked on finite grids, so no output
  is a certificate.  A global compact-interval exponential bound and a tail certificate
  are a separate obligation (the Gaussian factor decays, but the polynomial sign on
  [Tmax, infinity) is not discharged here).
"""
import argparse, json, time
import numpy as np
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre

KEPLER = np.pi / np.sqrt(18)
CE03 = 0.779747

def lag(k, t):
    return eval_genlaguerre(k, 0.5, t)

def basis(ts, K):
    """phi_k(t) = L_k^(1/2)(t) exp(-t/2): FUNCTION values, all O(1)."""
    ts = np.asarray(ts, float)
    M = np.array([[lag(k, t) for k in range(K + 1)] for t in ts])
    return M * np.exp(-ts / 2.0)[:, None]

def build_grids(rho, Tmax, n_shell, n_out, n_held):
    t_shell_lo = 8 * np.pi            # |x| = 2
    # dual grid for fhat(t) >= 0 on [0, infinity): dense near 0, geometric out to Tmax
    v = np.linspace(0, 1, n_out)
    that = np.unique(np.concatenate([Tmax * (np.expm1(6 * v) / np.expm1(6.0)),
                                     np.linspace(0.0, Tmax, n_out // 2)]))
    held_hat = Tmax * (np.linspace(0, 1, n_held) ** 1.7)
    t_shell_hi = 2 * np.pi * rho**2   # |x| = rho
    shell = np.linspace(t_shell_lo, t_shell_hi, n_shell)
    # exterior: geometric from the shell edge to Tmax, dense near the edge
    u = np.linspace(0, 1, n_out)
    ext = t_shell_hi + (Tmax - t_shell_hi) * (np.expm1(6 * u) / np.expm1(6.0))
    # held-out: a DIFFERENT sampling scheme on both regions
    held_shell = np.linspace(t_shell_lo, t_shell_hi, n_held)
    held_ext = t_shell_hi + (Tmax - t_shell_hi) * (np.linspace(0, 1, n_held) ** 1.5)
    return dict(shell=shell, ext=np.unique(ext), that=that,
                held_shell=held_shell, held_ext=np.unique(held_ext),
                held_hat=np.unique(held_hat),
                t_shell_lo=t_shell_lo, t_shell_hi=t_shell_hi)

def solve(K, rho, G, use_eta, col_scale=True):
    """LP: variables (c_0..c_K, eta).  fhat(0)=1.  minimise f(0) + 12 eta."""
    Ms = basis(G["shell"], K)
    Me = basis(G["ext"], K)
    Mh = basis(G["that"], K) * ((-1.0) ** np.arange(K + 1))[None, :]   # fhat values
    n = K + 1
    # column scaling: balance the columns of the constraint matrix
    if col_scale:
        stack = np.vstack([Ms, Me, Mh])
        colw = np.maximum(np.abs(stack).max(axis=0), 1e-12)
    else:
        colw = np.ones(n)
    Ms, Me, Mh = Ms / colw, Me / colw, Mh / colw
    # row scaling by the row max (after column scaling)
    rs = np.maximum(np.abs(Ms).max(axis=1), 1e-300)
    re = np.maximum(np.abs(Me).max(axis=1), 1e-300)
    rh = np.maximum(np.abs(Mh).max(axis=1), 1e-300)
    if use_eta:
        A = np.vstack([
            np.hstack([Ms / rs[:, None], -np.ones((len(rs), 1))]),   # f <= eta
            np.hstack([Me / re[:, None], np.zeros((len(re), 1))]),   # f <= 0
            np.hstack([-Mh / rh[:, None], np.zeros((len(rh), 1))]),  # fhat >= 0
            np.hstack([np.zeros((1, n)), -np.ones((1, 1))]),         # -eta <= 0
            np.hstack([-np.eye(1, n, K), np.zeros((1, 1))]),         # -c_K <= -1e-9
        ])
        b = np.concatenate([np.zeros(len(rs)), np.zeros(len(re)), np.zeros(len(rh)),
                            [0.0], [-1e-9]])
    else:
        A = np.vstack([
            np.hstack([Ms / rs[:, None], np.zeros((len(rs), 1))]),
            np.hstack([Me / re[:, None], np.zeros((len(re), 1))]),
            np.hstack([-Mh / rh[:, None], np.zeros((len(rh), 1))]),  # fhat >= 0
            np.hstack([np.zeros((1, n)), np.ones((1, 1))]),          # eta <= 0  => eta = 0
            np.hstack([-np.eye(1, n, K), np.zeros((1, 1))]),
        ])
        b = np.concatenate([np.zeros(len(rs)), np.zeros(len(re)), np.zeros(len(rh)),
                            [0.0], [-1e-9]])
    L0 = np.array([lag(k, 0.0) for k in range(K + 1)]) / colw
    cq0 = np.concatenate([L0 * ((-1.0) ** np.arange(K + 1)), [0.0]])   # eta absent from fhat(0)
    obj = np.concatenate([L0, [12.0 if use_eta else 0.0]])
    res = linprog(obj, A_ub=A, b_ub=b, A_eq=cq0[None, :], b_eq=[1.0],
                  bounds=[(-1e5, 1e5)] * (n + 1), method="highs")
    return res, colw

def diagnostics(c, eta, K, G, colw):
    """Evaluate the candidate on the HELD-OUT grid and on the shell endpoints."""
    cc = np.asarray(c)            # already in the scaled variables? no: recover raw
    def f(ts):
        return basis_vals(ts, cc, K)
    hs, he = G["held_shell"], G["held_ext"]
    fs, fe = f(hs), f(he)
    viol_shell = float(np.max(fs - eta))
    viol_ext = float(np.max(fe))
    p0 = float(basis_vals([0.0], cc, K)[0])
    return dict(held_shell_max_f_minus_eta=viol_shell,
                held_ext_max_f=viol_ext,
                held_shell_ok=bool(viol_shell <= 1e-9),
                held_ext_ok=bool(viol_ext <= 1e-9),
                f_at_contact=float(f([G["t_shell_lo"]])[0]),
                f_at_rho=float(f([G["t_shell_hi"]])[0]),
                f0=p0)

def basis_vals(ts, c, K):
    M = basis(ts, K)
    return M @ np.asarray(c, float)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho", type=float, default=2.09)
    ap.add_argument("--degree", type=int, default=13)
    ap.add_argument("--grid", type=int, default=600)
    ap.add_argument("--n-shell", type=int, default=300)
    ap.add_argument("--n-held", type=int, default=1201)
    ap.add_argument("--Tmax", type=float, default=120.0)
    ap.add_argument("--out", default="out/shellbench.json")
    a = ap.parse_args()
    if a.degree % 2 == 0:
        raise SystemExit("degree must be ODD. With fhat >= 0 imposed, the leading "
                         "coefficients give lc(q) = c_K/K! > 0 and lc(p) = (-1)^K c_K/K! <= 0, "
                         "which are consistent only for K odd. (Confirmed in practice: even "
                         "degree returns infeasible.)")
    K = a.degree
    t0 = time.time()
    G = build_grids(a.rho, a.Tmax, a.n_shell, a.grid, a.n_held)
    rows = []
    for use_eta in (False, True):
        res, colw = solve(K, a.rho, G, use_eta)
        tag = "eta_shell" if use_eta else "CE_control_eta0"
        if not res.success:
            rows.append(dict(case=tag, solver_status=int(res.status),
                             solver_message=str(res.message), feasible=False))
            print("  %-16s INFEASIBLE/FAILED: %s" % (tag, res.message))
            continue
        c = res.x[:K + 1] / colw          # unscale to the natural basis
        eta = float(res.x[K + 1])
        dg = diagnostics(c, eta, K, G, colw)
        f0 = dg["f0"]
        fh0 = float(np.dot(((-1.0) ** np.arange(K + 1)) * np.array([lag(k, 0.0) for k in range(K + 1)]), c))
        obj = f0 + (12.0 * eta if use_eta else 0.0)
        d = dict(case=tag, feasible=True, solver_status=int(res.status),
                 degree=K, eta=eta, f0=f0, fhat0=fh0,
                 objective_f0_plus_12eta=obj,
                 Delta_bound=float(4 * np.pi / 3 * obj / fh0),
                 gap_to_kepler=float(4 * np.pi / 3 * obj / fh0 - KEPLER),
                 gap_to_ce03=float(4 * np.pi / 3 * obj / fh0 - CE03),
                 coefficients=[float(x) for x in c],
                 column_scaling=[float(x) for x in colw],
                 diagnostics=dg)
        rows.append(d)
        print("  %-16s eta=%.6g  f0=%+.6f  obj=%+.6f  Delta<=%.8f  gap_vs_Kepler=%+.3f%%  heldout_ok=%s/%s"
              % (tag, eta, f0, obj, d["Delta_bound"], 100 * d["gap_to_kepler"],
                 dg["held_shell_ok"], dg["held_ext_ok"]))
    ok = [r for r in rows if r.get("feasible")]
    out = dict(script="KeplerConjecture/Computation/shell_bench.py",
               convention="unit radius, minimum separation 2, t = 2*pi*|x|^2",
               objective="(4*pi/3)(f(0)+12 eta)/fhat(0), fhat(0)=1 imposed",
               rho=a.rho, degree=K, grid=a.grid, n_shell=a.n_shell,
               Tmax=a.Tmax, held_out_points=2 * a.n_held,
               shell_interval_t=[float(8 * np.pi), float(2 * np.pi * a.rho ** 2)],
               attribution="count-strengthening of de Laat-de Oliveira Filho-Vallentin, Forum Math. Sigma 2 (2014) e23, arXiv:1206.2608",
               conditional_on_shell_count=True,
               shell_assumption="at most 12 centres within distance rho of any centre; NOT the kissing number, positive-width shell; checked by Experimental",
               status="TESTED_FINITE",
               certification="none: finite grids only; no global sign or tail certificate",
               rows=rows, runtime_s=round(time.time() - t0, 2))
    if len(ok) == 2:
        out["strengthening_gain"] = ok[0]["Delta_bound"] - ok[1]["Delta_bound"]
        print("  strengthening gain over the same-degree control: %+.6f (positive = eta helps)"
              % out["strengthening_gain"])
    json.dump(out, open(a.out, "w"), indent=1)
    print("wrote", a.out, "in %.1fs" % out["runtime_s"])

if __name__ == "__main__":
    main()
