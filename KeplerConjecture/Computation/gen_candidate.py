#!/usr/bin/env python3
"""K15 candidate generator: float LP -> rational rounding -> EXACT certification.

Pipeline (each stage is explicit so a failure is attributable):
  1. float LP with a sign MARGIN eps, on a grid of t = 2*pi*|x|^2,
        minimise p(0)  s.t.  q(0) = 1,   p(t) <= -eps on [8*pi, Tmax],
                                        q(t) >= +eps on [0, Tmax],
     plus leading-coefficient constraints fixing the sign at infinity.
  2. round the coefficients to rationals with denominator D (adaptive).
  3. hand the ROUNDED coefficients to exactcert.certify_relaxed, which uses
     Sturm sequences over Q plus Yun squarefree decomposition, and needs no grid.
  4. try harder denominators, then a small margin; report the best certified value.

WHY THE RELAXED CHECK.  At the LP optimum the polynomials TOUCH zero (the equality
case forces double zeros), so a strict-sign test rejects the good candidates and
inflates the bound enormously.  certify_relaxed decides the sign exactly via the
squarefree odd part, so even-multiplicity touching is allowed and odd-multiplicity
crossings are still rejected.  Exactness is preserved: no floating point in the test.

The certified number is the one from stage 3 applied to stage 2's coefficients --
never the float LP objective. The float value is recorded only for comparison.

Deliberately loose is fine: at a true optimum p,q touch zero, so strict-sign
certification loses a little. A proved loose bound is the deliverable.
"""
import argparse, json, time
import numpy as np
from scipy.optimize import linprog
from scipy.special import eval_genlaguerre
from fractions import Fraction as F
import exactcert as EC

def lag(k, t):
    return eval_genlaguerre(k, 0.5, t)

def basis_matrix(ts, K):
    """FUNCTION values phi_k = L_k^(1/2)(t) exp(-t/2), which are O(1).  The LP must be
    built on these, not on the raw Laguerre values (which reach 1e11 at t=70, k=9 and
    destroy the solver).  The coefficients are identical either way; only the
    conditioning differs.  The exact polynomials are reconstructed in exactcert.py."""
    M = np.array([[lag(k, t) for k in range(K + 1)] for t in ts])
    return M * np.exp(-np.asarray(ts) / 2.0)[:, None]

def grid(lo, hi, n):
    return np.unique(np.concatenate([
        lo + (hi - lo) * (np.expm1(np.linspace(0, 5, n)) / np.expm1(5.0)),
        np.linspace(lo, hi, max(n // 4, 8))]))

def solve_float(K, eps, Tmax, npts):
    tp = grid(8 * np.pi, Tmax, npts)          # p <= -eps
    tq = grid(0.0, Tmax, npts)                # q >= +eps
    Mp = basis_matrix(tp, K)
    Mq = basis_matrix(tq, K) * ((-1.0) ** np.arange(K + 1))[None, :]
    # row scale
    sp = np.maximum(np.abs(Mp).max(axis=1), 1e-300)
    sq = np.maximum(np.abs(Mq).max(axis=1), 1e-300)
    A = np.vstack([Mp / sp[:, None], -Mq / sq[:, None]])
    b = np.concatenate([-eps / sp, -eps / sq])
    # Asymptotics.  The leading coefficient of L_k^(1/2)(t) is (-1)^k / k!, so
    #    lc(p) = (-1)^K c_K / K!,      lc(q) = c_K / K!.
    # Strict signs at both ends require lc(p) < 0 and lc(q) > 0, i.e.
    #    (-1)^K c_K < 0  and  c_K > 0,   which is consistent ONLY for K odd.
    # For K even the two requirements contradict each other: no strict-sign
    # certificate of even degree exists in this basis.  Enforced below.
    A = np.vstack([A, -np.eye(1, K + 1, K)[0] * 1.0])       # -c_K <= -1e-9
    b = np.concatenate([b, [-1e-9]])
    c0 = np.array([lag(k, 0.0) for k in range(K + 1)])
    cq0 = c0 * ((-1.0) ** np.arange(K + 1))
    res = linprog(c0, A_ub=A, b_ub=b, A_eq=cq0[None, :], b_eq=[1.0],
                  bounds=[(-1e4, 1e4)] * (K + 1), method="highs")
    return res

def round_rational(c, D):
    return [F(int(round(x * D)), D) for x in c]

def try_certify(cf, Ds=(10**6, 10**8, 10**10)):
    for D in Ds:
        c = round_rational(cf, D)
        rec = EC.certify_relaxed(c, verbose=False)
        if rec["ok"]:
            rec["denominator"] = D
            return rec
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--degree", type=int, default=8)
    ap.add_argument("--npts", type=int, default=260)
    ap.add_argument("--Tmax", type=float, default=70.0)
    ap.add_argument("--out", default="out/certificate_K8.json")
    a = ap.parse_args()
    K = a.degree
    if K % 2 == 0:
        raise SystemExit("degree must be ODD: with strict signs, lc(p)<0 and lc(q)>0 "
                         "force (-1)^K c_K<0 and c_K>0 simultaneously, so even degree "
                         "has no strict-sign certificate in the Laguerre basis.")
    t0 = time.time()
    EPS = [0.0, 1e-9, 1e-6]   # 0 is enough: certify_relaxed handles even-multiplicity touching
    best = None
    for eps in EPS:
        res = solve_float(K, eps, a.Tmax, a.npts)
        if not res.success:
            print("  eps=%-5g LP infeasible (%s)" % (eps, res.message[:40])); continue
        f0 = float(res.x @ np.array([lag(k, 0.0) for k in range(K + 1)]))
        rec = try_certify(res.x)
        if rec is None:
            print("  eps=%-5g LP f(0)=%.8f  -> rational certification FAILED" % (eps, f0)); continue
        p0 = F(rec["p0"]); q0 = F(rec["q0"])
        delta = float(p0 / q0) * 4 * np.pi / 3
        print("  eps=%-5g LP f(0)=%.8f  CERTIFIED Delta <= %.8f (D=1e%d)"
              % (eps, f0, delta, len(str(rec["denominator"])) - 1))
        if best is None or delta < best[1]:
            best = (rec, delta, eps, f0)
    if best is None:
        print("no certified candidate at degree", K); return
    rec, delta, eps, f0 = best
    out = dict(script="KeplerConjecture/Computation/gen_candidate.py",
               checker="KeplerConjecture/Computation/exactcert.py",
               convention="unit radius, min separation 2; t = 2*pi*|x|^2",
               sign_regions="p<=0 on t>=8*pi (verified on 8*PI_LO), q>=0 on t>=0",
               degree=K, epsilon=eps, float_lp_f0=f0,
               certified_delta=delta, kepler=float(np.pi / np.sqrt(18)),
               gap_absolute=delta - float(np.pi / np.sqrt(18)),
               gap_relative=delta / float(np.pi / np.sqrt(18)) - 1.0,
               certificate=rec, runtime_s=round(time.time() - t0, 2),
               status="PROVED_CONDITIONAL_ON_CE_THEOREM",
               scope=("Delta <= certified_delta for every packing, by Cohn-Elkies "
                      "Theorem 3.1 applied to the exact certificate; the CE theorem is "
                      "cited, not re-proved. Strict-sign route, so loose."))
    json.dump(out, open(a.out, "w"), indent=1)
    print("BEST certified: Delta <= %.8f  (Kepler %.8f, gap %+.3f%%)"
          % (delta, float(np.pi / np.sqrt(18)), 100 * out["gap_relative"]))
    print("wrote", a.out)

if __name__ == "__main__":
    main()
