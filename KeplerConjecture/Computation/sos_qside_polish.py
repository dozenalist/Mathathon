#!/usr/bin/env python3
"""Hill-climb the explicit-Gram Fourier-side family from a known admissible point.

Starting point: the degree-5 certificate of sos_qside.py,
    q = 3^2 + (3u/2 - 6)^2 + u(3/2 - 2u/3)^2,   p = -4u^3/9 + 59u^2/12 + 17u/6 + 1351/48,
    Delta <= 2.61993314.

SEARCH: perturb the coefficients of the rational polynomials r_i, s_j by small rational steps,
keep a step when the objective p(0)/q(0) improves AND a float screen still has p <= 0 on a dense
sample of [4*pi, 400].  Every improvement is re-verified exactly at the end with Computation's
checker (not Main's, unsound per review 0138-C).

A float screen is used ONLY to steer; acceptance is exact.  The final certificate is reported
only if exactcert accepts it.

Usage:  python3 sos_qside_polish.py [--iters N] [--out out/sos_qside_polish.json]
"""
import argparse, json, random, copy
from fractions import Fraction as F
import numpy as np
import sympy as sp
import exactcert as EC

u = sp.Symbol('u')

def to_exprs(rs, ss):
    R = lambda c: sp.expand(sum(sp.Rational(x) * u ** i for i, x in enumerate(c)))
    return [R(c) for c in rs], [R(c) for c in ss]

def build(rs, ss):
    r, s = to_exprs(rs, ss)
    q = sp.expand(sum(x ** 2 for x in r) + u * sum(x ** 2 for x in s))
    return q

def q_to_p(q, K, SC):
    P = sp.Poly(q, u)
    b = [P.coeff_monomial(u ** i) for i in range(K + 1)]
    M = SC.fourier_map(K)
    a = [sum(M[i, k] * b[k] for k in range(K + 1)) for i in range(K + 1)]
    return sp.expand(sum(a[i] * u ** i for i in range(K + 1))), a, b

def screen(p, K, T_LO=4 * np.pi, hi=400.0, n=4001):
    P = sp.Poly(p, u)
    c = [float(P.coeff_monomial(u ** i)) for i in range(K + 1)]
    xs = np.linspace(T_LO, hi, n)
    v = np.zeros_like(xs)
    for cc in reversed(c):
        v = v * xs + cc
    return v.max()

def exact_ok(a, K):
    cf = [F(str(sp.Rational(x))) for x in a]
    ell = EC.laguerre_polys(K); rem = list(cf); cl = [F(0)] * (K + 1)
    for j in range(K, -1, -1):
        lc = ell[j][-1] * (F(2) ** j); cj = rem[j] / lc; cl[j] = cj
        for i in range(len(ell[j])):
            rem[i] -= cj * ell[j][i] * (F(2) ** i)
    if not all(x == 0 for x in rem):
        return None
    return EC.certify(cl, allow_touching=False, verbose=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=900)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--uphill", type=float, default=0.0,
                    help="basin-hopping tolerance: accept moves up to this relative worsening")
    ap.add_argument("--degree", type=int, default=5,
                    help="5 or 7; the degree-5 optimum is embedded as the degree-7 start")
    ap.add_argument("--out", default="out/sos_qside_polish.json")
    a = ap.parse_args()
    import importlib.util
    spec = importlib.util.spec_from_file_location("sc", "/tmp/sc662.py")
    SC = importlib.util.module_from_spec(spec); spec.loader.exec_module(SC)
    K = a.degree
    random.seed(a.seed)
    if K == 5:
        rs = [[F(0)], [F(3)], [F(-6), F(3, 2)]]
        ss = [[F(3, 2), F(-2, 3)]]
    elif K == 7:
        # the degree-5 optimum, PADDED to degree 3 factors.  Padding with zeros keeps q and p
        # unchanged, so the start is admissible and the hill-climb begins at 1.99064200.
        rs = [[F(0)], [F(-1, 12)], [F(-19, 4), F(11, 6)]]
        ss = [[F(7, 4), F(-2, 3)]]
        rs = [r + [F(0)] * (4 - len(r)) for r in rs] + [[F(0)]]
        ss = [s + [F(0)] * (4 - len(s)) for s in ss] + [[F(0)]]
    else:
        raise SystemExit("degree must be 5 or 7")
    def score(rs, ss):
        q = build(rs, ss)
        if sp.degree(q) > K:
            return None
        p, aa, bb = q_to_p(q, K, SC)
        if sp.degree(p) > K:
            return None
        if screen(p, K) > 0:
            return None
        p0 = float(sp.Rational(aa[0])); q0 = float(sp.Rational(bb[0]))
        if p0 <= 0 or q0 <= 0:
            return None
        return p0 / q0, p, aa, bb, q
    base = score(rs, ss)
    assert base is not None, "start point must be admissible"
    best = (base[0], copy.deepcopy(rs), copy.deepcopy(ss), base[2], base[3], base[4])
    print("start: p0/q0 = %.10f  -> Delta = %.8f" % (best[0], best[0] * 4 * 3.141592653589793 / 3))
    improved = 0
    cur = (best[0], copy.deepcopy(best[1]), copy.deepcopy(best[2]))
    for it in range(a.iters):
        rs2 = copy.deepcopy(cur[1]); ss2 = copy.deepcopy(cur[2])
        # pick a random polynomial and a random coefficient, perturb
        which = random.random() < 0.6
        pool = rs2 if which else ss2
        i = random.randrange(len(pool)); j = random.randrange(len(pool[i]))
        pool[i][j] += F(random.choice([-2, -1, 1, 2]), random.choice([1, 2, 3, 4]))
        r = score(rs2, ss2)
        if r is not None:
            # basin-hopping: move to the new point if it is better than the CURRENT one, or
            # within UPHILL of it; keep `best` separately so a bad walk cannot lose the record.
            if r[0] < cur[0] or (a.uphill > 0 and r[0] < cur[0] * (1 + a.uphill)):
                cur = (r[0], rs2, ss2)
            if r[0] < best[0] - 1e-12:
                best = (r[0], rs2, ss2, r[2], r[3], r[4]); improved += 1
            if improved % 5 == 0 and r[0] < best[0] - 1e-12:
                print("  iter %4d improved: p0/q0 = %.10f  Delta = %.8f"
                      % (it, best[0], best[0] * 4 * 3.141592653589793 / 3))
    print("\nimprovements: %d ; best p0/q0 = %.10f" % (improved, best[0]))
    rec = exact_ok(best[3], K)
    if rec is None or not rec["ok"]:
        print("final candidate FAILED exact verification:", (rec or {}).get("reason"))
        return
    d = EC.delta_upper_decimal(rec, 8)
    print("EXACT: Delta <= %s" % d)
    print("  q(u) =", sp.expand(best[5]))
    print("  p(u) =", sp.expand(sum(sp.Rational(x) * u ** i for i, x in enumerate(best[3]))))
    print("  r_i =", [[str(x) for x in c] for c in best[1]])
    print("  s_j =", [[str(x) for x in c] for c in best[2]])
    json.dump(dict(script="KeplerConjecture/Computation/sos_qside_polish.py",
                   start_delta=2.61993314, status="VERIFIED_EXACT",
                   note=("q certified by construction as a sum of squares; p by exact Sturm with "
                         "Computation's checker. Float screen used to steer only."),
                   delta=d, p0_q0=float(F(rec["p0"])) / float(F(rec["q0"])),
                   q=str(sp.expand(best[5])), p=str(sp.expand(sum(sp.Rational(x) * u ** i
                                                                   for i, x in enumerate(best[3])))),
                   r=[[str(x) for x in c] for c in best[1]],
                   s=[[str(x) for x in c] for c in best[2]],
                   improvements=improved), open(a.out, "w"), indent=1)
    print("\nwrote", a.out)

if __name__ == "__main__":
    main()
