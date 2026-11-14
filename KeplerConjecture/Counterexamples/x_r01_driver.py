#!/usr/bin/env python3
"""X-R01 driver (runnable): LP search + EXACT certification in the family
f(x)=P(|x|^2)e^{-|x|^2}, P in Q[s], with the exact Fourier map of ce_exact_gauss.py.

Usage:  python3 x_r01_driver.py [DEG] [ITERS]
Output: one line per iteration; final line is the best EXACTLY CERTIFIED bound.
Only exactly certified candidates are reported as bounds; everything else is a
search artefact and is labelled as such.
"""
import sys, math
import numpy as np, sympy as sp
from fractions import Fraction as F
from scipy.optimize import linprog
import ce_exact_gauss as G

s_ = G.s_

# ---- corrected constants (supervisor review 41644, item 2; re-derived here) ----
# f = P(s)e^{-s}, f^ = pi^{3/2}Q(v)e^{-v}, so
#   Delta <= (4 pi/3) f(0)/f^(0) = (4/(3 sqrt(pi))) P(0)/Q(0).
# Kepler comparison for P(0),Q(0) > 0:
#   (4/(3 sqrt pi)) P0/Q0 < pi/sqrt18  <=>  4 sqrt18 P0 < 3 pi^{3/2} Q0
#   <=> (squaring, both sides positive twice) 32 P0^2 < pi^3 Q0^2.
def density_factor():
    return 4/(3*sp.sqrt(sp.pi))

def kepler_ok(P0, Q0):
    return bool(sp.N(32*sp.Integer(P0)**2, 30) < sp.N(sp.pi**3*sp.Integer(Q0)**2, 30))

def density(P0, Q0):
    return density_factor()*sp.Rational(P0)/sp.Rational(Q0)

# Exact feasible control: P = 2 - 2s/3  =>  Q = 1 + 2v/3 exactly (Q_0=1, Q_1=3/2-v).
CONTROL_P = 2 - sp.Rational(2,3)*s_

def build(N, ngrid=600, smax=120.0, vmax=400.0):
    # P-column values: coefficient of s^n at grid points
    S = np.linspace(4.0, smax, ngrid)
    V = np.concatenate([np.linspace(0.0, vmax, ngrid)])
    AP = np.array([[v**n for n in range(N+1)] for v in S])              # P(s_i)
    # Q = M c ; Q(v) linear in c
    M = [sp.Poly(G.apply_map(s_**n), G.v_).all_coeffs()[::-1] for n in range(N+1)]  # M[n] = coeffs of v
    def qrow(v):
        return np.array([sum(float(c)*v**k for k, c in enumerate(M[n])) for n in range(N+1)])
    AQ = np.array([qrow(v) for v in V])
    globals()['qrow'] = qrow
    # ---- column equilibration: divide each basis column by its max |entry| ----
    sc_P = np.abs(AP).max(axis=0); sc_P[sc_P == 0] = 1.0
    sc_Q = np.abs(AQ).max(axis=0); sc_Q[sc_Q == 0] = 1.0
    sc = np.maximum(sc_P, sc_Q)
    AP = AP / sc; AQ = AQ / sc
    def unscale(cs): return np.asarray(cs)*sc
    p0 = np.array([1.0] + [0.0]*N)                                      # P(0)=c_0
    q0 = np.array([float(sp.N(G.apply_map(s_**n).subs(G.v_,0))) for n in range(N+1)])
    return AP, S, AQ, V, p0, q0, sc

def certify_vec(c, N):
    P = sum(sp.Rational(int(round(ci*10**9)), 10**9)*s_**n for n, ci in enumerate(c))
    return G.certify(sp.expand(P))

def run(N=6, iters=40, eps=1e-9):
    print("CONTROL CHECK (must certify; proves the family is non-empty):")
    cc, cmsg = G.certify(sp.expand(CONTROL_P))
    if cc:
        cP0 = sp.nsimplify(CONTROL_P.subs(s_,0)); cQ0 = sp.nsimplify(G.apply_map(CONTROL_P).subs(G.v_,0))
        print("   P = 2 - 2s/3 , Q = %s , P(0)=%s Q(0)=%s" % (sp.expand(G.apply_map(CONTROL_P)), cP0, cQ0))
        print("   certified; density = %s = %.6f  (trivial >1, but a valid certificate)"
              % (sp.nsimplify(density(cP0,cQ0)), float(density(cP0,cQ0))))
        print("   => the fixed family IS feasible; a solver failure must not be reported as infeasibility.")
    else:
        print("   CONTROL FAILED TO CERTIFY:", cmsg, " <- implementation error, stop")
        return
    AP, S, AQ, V, p0, q0, sc = build(N)
    extra_P, extra_Q = [], []
    best = None
    print("   scaled constraint matrix: max |entry| = %.3e (was ~1e15 unscaled)"
          % max(np.abs(AP).max(), np.abs(AQ).max()))
    for it in range(iters):
        Aub = np.vstack([AP] + ([np.array(extra_P)] if extra_P else []) +
                        [-AQ] + ([-np.array(extra_Q)] if extra_Q else []))
        bub = np.concatenate([np.full(len(AP), -eps)] +
                             ([np.full(len(extra_P), -eps)] if extra_P else []) +
                             [np.zeros(len(AQ))] +
                             ([np.zeros(len(extra_Q))] if extra_Q else []))
        Aeq = q0.reshape(1, -1); beq = [1.0]
        res = linprog(p0/sc, A_ub=Aub, b_ub=bub, A_eq=Aeq/sc, b_eq=beq,
                      bounds=[(None, None)]*(N+1), method='highs')
        if res.success:
            res.x = np.asarray(res.x)*sc
        if not res.success:
            print("iter %2d: SOLVER DID NOT RETURN A SOLUTION -- raw status %s, message %r."
                  % (it, res.status, (res.message or '')[:90]))
            print("           This is NOT a proof of infeasibility; check scaling first")
            print("           (max |entry| of the constraint matrix here = %.3e)." % np.abs(Aub).max())
            break
        P = sum(sp.Rational(int(round(ci*10**9)), 10**9)*s_**n for n, ci in enumerate(res.x))
        cert, msg = G.certify(sp.expand(P))
        if cert:
            P0, Q0 = sp.nsimplify(P.subs(s_,0)), sp.nsimplify(G.apply_map(P).subs(G.v_,0))
            bound = density(P0, Q0); okk = kepler_ok(P0, Q0)
            if best is None or sp.N(bound) < best[0]:
                best = (sp.N(bound), bound, P, P0, Q0, okk)
            print("iter %2d: CERTIFIED  P0/Q0 = %-14s bound = %.9f  (<Kepler? %s)"
                  % (it, str(sp.nsimplify(P0/Q0))[:14], float(bound), okk))
            break
        else:
            # cutting plane: locate a violation of the exact sign conditions
            Pp = sp.Poly(P, s_)
            Q  = sp.expand(G.apply_map(P)); Qp = sp.Poly(Q, G.v_)
            bad = None
            for vv in np.linspace(4.0, 400.0, 4000):
                if float(sp.N(Pp.eval(vv))) > 0 and bad is None:
                    bad = ('P', vv); break
            if bad is None:
                for vv in np.linspace(0.0, 800.0, 4000):
                    if float(sp.N(Qp.eval(vv))) < 0:
                        bad = ('Q', vv); break
            if bad is None:
                print("iter %2d: exact certifier failed but no sampled violation found: %s" % (it, msg)); break
            kind, vv = bad
            if kind == 'P': extra_P.append(list(np.array([vv**n for n in range(N+1)])/sc))
            else:           extra_Q.append(list(np.array(qrow(vv))/sc))
            print("iter %2d: rejected (%s at %s); adding cutting plane" % (it, kind, ("%.4f"%vv)))
    print("-"*70)
    if best:
        b, ex, P, P0, Q0, okk = best
        print("BEST CERTIFIED: bound = %s = %.9f" % (ex, float(b)))
        print("  P =", sp.factor(P)); print("  P(0)=%s  Q(0)=%s" % (P0, Q0))
        print("  32 P0^2 < pi Q0^2 ?  %s" % okk)
        print("  STATUS: PROVED for all packings of unit balls (exact sign certificate)")
    else:
        print("NO CERTIFIED CANDIDATE in %d iterations." % iters)
        print("  STATUS: exploratory only; no bound claimed.")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv)>1 else 6
    IT = int(sys.argv[2]) if len(sys.argv)>2 else 30
    run(N, IT)
