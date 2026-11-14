#!/usr/bin/env python3
"""K15 SOS on the FOURIER side: q is a sum of squares by construction.

COMPLEMENT OF sos_family.py.  There the p-side (f <= 0 off the ball) was certified by an
explicit rational square and the q-side was left to exact Sturm.  Here it is the other way
round, and the point is to show that each side can be made explicit:

    q(u) = sum_{i<=m} r_i(u)^2  +  u * sum_{j<=n} s_j(u)^2 ,     r_i, s_j in Q[u]      (Q)

so q >= 0 on [0, infinity) BY CONSTRUCTION, with an explicit rational Gram matrix
    G = sum_i vec(r_i) vec(r_i)^T ,  and the u-multiplier contributes the block sum_j vec(s_j) vec(s_j)^T
to the matrix of the Markov-Lukacs form.  Verification of (Q) is expanding a finite sum of
squares: no Sturm, no root counting.

Then p is DETERMINED, since the map is an involution (M^2 = I, verified in audit_fourier.py):

    b = coefficients of q = sum_i r_i^2 + u sum_j s_j^2 ,
    a = M^{-1} b = M b      (an involution, so inversion is the same map),
    p = sum_k a_k u^k .

The remaining condition p <= 0 on [4*pi, infinity) cannot be imposed by construction, and is
decided exactly by Computation's own checker (exactcert), not by Main's (unsound, review 0138-C).

SEARCH.  Random rational r_i, s_j of low degree; a fast float screen keeps only candidates whose
p is non-positive on a dense sample of [4*pi, 400]; every survivor is verified exactly.

STATUS.  Any bound found is VERIFIED_EXACT for the stated family.  It is a demonstrator of the
certificate FORMAT (explicit rational Gram on the Fourier side) and is not expected to be
competitive; sos_family.py's 8x gap has the same structural cause.

Usage:  python3 sos_qside.py [--trials N]
"""
import argparse, json, random
from fractions import Fraction as F
import numpy as np
import sympy as sp
import exactcert as EC

def q_from_squares(rs, ss):
    u = sp.Symbol('u')
    R = lambda p: sp.expand(sum(sp.Rational(c) * u ** i for i, c in enumerate(p)))
    q = sum(R(r) ** 2 for r in rs) + u * sum(R(s) ** 2 for s in ss)
    return sp.expand(q)

def p_from_q(q, K, SC):
    u = sp.Symbol('u')
    P = sp.Poly(q, u)
    b = [P.coeff_monomial(u ** i) for i in range(K + 1)]
    M = SC.fourier_map(K)
    a = [sum(M[i, k] * b[k] for k in range(K + 1)) for i in range(K + 1)]   # M^{-1} = M
    p = sp.expand(sum(a[i] * u ** i for i in range(K + 1)))
    return p, a, b

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=4000)
    ap.add_argument("--degree", type=int, default=5)
    ap.add_argument("--out", default="out/sos_qside.json")
    a = ap.parse_args()
    import importlib.util
    spec = importlib.util.spec_from_file_location("sc", "/tmp/sc662.py")
    SC = importlib.util.module_from_spec(spec); spec.loader.exec_module(SC)
    K = a.degree
    random.seed(7)
    T_LO = float(4 * np.pi)
    best = None; found = 0
    print("q built as sum r_i^2 + u sum s_j^2 (explicit Gram), p = M q, screening p <= 0 ...")
    for trial in range(a.trials):
        nq = random.choice([2, 3, 4])
        dmax = 3 if K >= 7 else 2
        full = (K >= 7)
        rs = [[F(random.randint(-6, 6), random.choice([1, 2, 3]))
               for _ in range(dmax if full else random.randint(1, dmax))]
              for _ in range(nq)]
        ss = [[F(random.randint(-6, 6), random.choice([1, 2, 3]))
               for _ in range(dmax if full else random.randint(0, dmax))]
              for _ in range(nq)]
        if all(all(x == 0 for x in r) for r in rs):
            continue
        q = q_from_squares(rs, ss)
        if sp.degree(q) > K:
            continue
        p, aa, bb = p_from_q(q, K, SC)
        if sp.degree(p) > K:
            continue
        # fast float screen: p <= 0 on [T_LO, 400]
        pn = [float(sp.Rational(x)) for x in [sp.Poly(p, sp.Symbol('u')).coeff_monomial(sp.Symbol('u') ** i) for i in range(K + 1)]]
        xs = np.linspace(T_LO, 400.0, 4001)
        pv = np.zeros_like(xs)
        for c in reversed(pn):
            pv = pv * xs + c
        if pv.max() > 0:
            continue
        p0 = float(pn[0]); q0 = float(bb[0])
        if p0 <= 0 or q0 <= 0:
            continue
        # exact verification with my checker
        cf = [F(str(sp.Rational(x))) for x in aa]
        ell = EC.laguerre_polys(K); rem = list(cf); cl = [F(0)] * (K + 1)
        for j in range(K, -1, -1):
            lc = ell[j][-1] * (F(2) ** j); cj = rem[j] / lc; cl[j] = cj
            for i in range(len(ell[j])):
                rem[i] -= cj * ell[j][i] * (F(2) ** i)
        if not all(x == 0 for x in rem):
            continue
        r = EC.certify(cl, allow_touching=False, verbose=False)
        if not r["ok"]:
            continue
        found += 1
        d = EC.delta_upper_decimal(r, 8)
        val = float(F(r["p0"]) / F(r["q0"])) * 4 * 3.141592653589793 / 3
        if best is None or val < best[1]:
            best = (dict(rs=[[str(x) for x in rr] for rr in rs],
                         ss=[[str(x) for x in ss2] for ss2 in ss],
                         q=str(q), p=str(p), delta=d, delta_float=val,
                         gram="G = sum_i vec(r_i)vec(r_i)^T ; u-block from s_j",
                         verdict=dict(gram_by_construction=True, exact_sturm=r["ok"])), val)
            print("  trial %5d: admissible, Delta <= %s" % (trial, d))
    print("\ncandidates exactly verified: %d of %d trials" % (found, a.trials))
    if best:
        rec, val = best
        print("BEST: Delta <= %s  (Kepler 0.74048049, CE 0.779747)" % rec["delta"])
        print("  q(u) =", rec["q"])
        print("  p(u) =", rec["p"])
        print("  r_i =", rec["rs"])
        print("  s_j =", rec["ss"])
        json.dump(dict(script="KeplerConjecture/Computation/sos_qside.py",
                       family="q = sum r_i^2 + u sum s_j^2, p = M q",
                       status="VERIFIED_EXACT",
                       note=("q-side certified by construction with an explicit rational Gram; "
                             "p-side by exact Sturm with Computation's checker, NOT Main's "
                             "(unsound per review 0138-C)"),
                       best=rec, trials=a.trials, found=found),
                  open(a.out, "w"), indent=1)
        print("\nwrote", a.out)
    else:
        print("no admissible candidate found in this range")

if __name__ == "__main__":
    main()
