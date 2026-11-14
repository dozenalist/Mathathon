#!/usr/bin/env python3
"""K15 strengthened-candidate evaluator #1: the equality-case-constrained inverse problem.

THE CANDIDATE (route R3, symmetric functions / interpolation)
  A sharp certificate at FCC must vanish on every FCC shell and its transform on every
  dual BCC shell (Cohn-Elkies 2003 sec.5; recovered note r1, Thm 2.1). The natural
  "inverse problem" therefore prescribes those zeros as linear constraints and asks
  whether the LP optimum drops to the Kepler value.

RESULT (measured, see RESULTS_baseline.md): it does not. Imposing necessary conditions
  can only enlarge a *minimisation*... precisely: it shrinks the feasible set, so the
  optimum can only increase. The evaluator measures by how much -- i.e. the price of
  the inverse-problem route. This is a deliberately reported NEGATIVE result.

NOT A ROUTE TO THE BOUND. Pure CE is excluded by Li 2024 Thm 6.1, and adding the
  forced zeros moves the value away from Kepler, not toward it.
"""
import sys, json, argparse
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import ce3_baseline as B
import k15conv as CV
from mpmath import mp, mpf, pi

mp.dps = 30

def is3sq(n):
    while n % 4 == 0: n //= 4
    return n % 8 != 7

def fcc_shells(kmax=14):
    """squared radii of FCC shells (sep1): k with 2k a sum of three squares (Legendre)."""
    return [float(k) for k in range(1, kmax + 1) if is3sq(2 * k)]

def dual_shells(kmax=14):
    """squared radii of the dual BCC shells: {2m : m sum of 3 squares} u {4j + 3/2}."""
    s = set()
    for m in range(1, kmax + 1):
        if is3sq(m): s.add(2.0 * m)
    j = 0
    while 1.5 + 4 * j <= 2 * kmax:
        s.add(1.5 + 4 * j); j += 1
    return sorted(s)

def solve_constrained(K, grid, r0, rmax, smax, zf=(), zfh=()):
    t = 2 * np.pi * np.linspace(r0**2, rmax**2, grid)
    u = 2 * np.pi * np.linspace(0.0, smax**2, grid)
    A = np.vstack([np.array([B.basis_row(x, K) for x in t]),
                   -np.array([B.basis_row(x, K, True) for x in u])])
    b = np.zeros(A.shape[0])
    e = np.zeros((1, K + 1)); e[0, K] = -1.0
    A = np.vstack([A, e]); b = np.concatenate([b, [0.0]])
    sc = np.max(np.abs(A), axis=1); A /= sc[:, None]; b /= sc
    b0 = np.array([B.lag(k, 0.0) for k in range(K + 1)])
    Aeq = [b0]; beq = [1.0]
    for r2 in zf:
        v = B.basis_row(2 * np.pi * r2, K); s = np.max(np.abs(v))
        Aeq.append(v / s); beq.append(0.0)
    for r2 in zfh:
        v = B.basis_row(2 * np.pi * r2, K, True); s = np.max(np.abs(v))
        Aeq.append(v / s); beq.append(0.0)
    res = linprog(-((-1.0)**np.arange(K + 1)) * b0, A_ub=A, b_ub=b,
                  A_eq=np.array(Aeq), b_eq=np.array(beq),
                  bounds=[(None, None)] * (K + 1), method="highs")
    return res

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--degree", type=int, default=25)
    ap.add_argument("--grid", type=int, default=900)
    ap.add_argument("--out", default="out/constrained.json")
    a = ap.parse_args()
    K = a.degree
    fsh, dsh = fcc_shells(), dual_shells()
    print("FCC shells (r^2):", fsh)
    print("dual BCC shells (r^2):", dsh)
    cases = [("control: plain CE", ((), ())),
             ("f=0 on first 2 FCC shells", (fsh[:2], ())),
             ("f=0 on first 4 FCC shells", (fsh[:4], ())),
             ("fhat=0 on first 2 dual shells", ((), dsh[:2])),
             ("fhat=0 on first 4 dual shells", ((), dsh[:4])),
             ("both, 1 shell each", (fsh[:1], dsh[:1])),
             ("both, 2 shells each", (fsh[:2], dsh[:2])),
             ("both, 3 shells each", (fsh[:3], dsh[:3]))]
    rows = []
    kep = float(CV.KEPLER_DELTA)
    for name, (zf, zfh) in cases:
        r = solve_constrained(K, a.grid, 1.0, 5.0, 5.0, zf, zfh)
        if r.success:
            rho = 1.0 / (-r.fun); D = float(CV.rhoA_to_Delta(rho))
            rows.append(dict(case=name, rho_A=rho, Delta=D, ratio_to_kepler=D / kep, feasible=True))
            print("  %-32s Delta <= %.7f   (%.4f x Kepler)" % (name, D, D / kep))
        else:
            rows.append(dict(case=name, feasible=False, message=r.message))
            print("  %-32s INFEASIBLE" % name)
    json.dump(dict(degree=K, grid=a.grid, convention="min-separation-1 native, Delta=(pi/6)rho_A",
                   status="TESTED_FINITE", rows=rows), open(a.out, "w"), indent=1)
    print("wrote", a.out)
