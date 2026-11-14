#!/usr/bin/env python3
"""p-side explicit Gram with MANY squares, hill-hopped.

sos_family.py had a single square in the multiplier; sos_family2.py had two.  Here

    -p(u) = (u - T) * sum_{i<=m} r_i(u)^2 ,        r_i in Q[u],  T rational <= 4*pi

so p <= 0 on [T, inf) BY CONSTRUCTION with an explicit rational Gram (m rational squares),
and the q-side, q = M p, is verified by exact Sturm with Computation's checker.
Basin-hopping over the r_i coefficients, with the float screen steering and exact acceptance.

SCOPE.  Any certificate found is VERIFIED_EXACT for this family.  It is best-found, not
optimal.  Compare: sos_qside.py's mirror family reaches 1.37125723 on the Fourier side.

Usage:  python3 sos_pside_many.py [--m 4] [--deg 2] [--iters 3000]
"""
import argparse, copy, json, random, itertools
from fractions import Fraction as F
import numpy as np
import sympy as sp
import exactcert as EC

u = sp.Symbol('u')

def build(T, rs):
    R = [sp.expand(sum(sp.Rational(x) * u ** i for i, x in enumerate(c))) for c in rs]
    B = sp.expand(sum(x ** 2 for x in R))
    p = sp.expand(-(u - T) * B)
    return p, B, R

def p_to_q(p, K, SC):
    P = sp.Poly(p, u)
    a = [P.coeff_monomial(u ** i) for i in range(K + 1)]
    M = SC.fourier_map(K)
    b = [sum(M[i, k] * a[k] for k in range(K + 1)) for i in range(K + 1)]
    return sp.expand(sum(b[i] * u ** i for i in range(K + 1))), a, b

def screen(q, K, hi=400.0, n=4001):
    P = sp.Poly(q, u)
    c = [float(P.coeff_monomial(u ** i)) for i in range(K + 1)]
    xs = np.linspace(0.0, hi, n)
    v = np.zeros_like(xs)
    for cc in reversed(c):
        v = v * xs + cc
    return v.min()

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
    ap.add_argument("--m", type=int, default=4)
    ap.add_argument("--deg", type=int, default=2)
    ap.add_argument("--iters", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--uphill", type=float, default=0.05)
    ap.add_argument("--out", default="out/sos_pside_many.json")
    a = ap.parse_args()
    import importlib.util
    spec = importlib.util.spec_from_file_location("sc", "/tmp/sc662.py")
    SC = importlib.util.module_from_spec(spec); spec.loader.exec_module(SC)
    K = 2 * a.deg + 1                 # deg p = 1 + 2*deg
    if K % 2 == 0:
        K += 1
    T = F(12)                          # <= 4*pi, rational
    random.seed(a.seed)
    fest = F(31415926535, 10 ** 10)
    def score(Tv, rs):
        p, B, R = build(Tv, rs)
        if sp.degree(p) > K:
            return None
        q, aa, bb = p_to_q(p, K, SC)
        if sp.degree(q) > K:
            return None
        if Tv > 4 * fest:              # must stay <= 4*pi
            return None
        if screen(q, K) < 0:           # need q >= 0 on [0, inf)
            return None
        p0 = float(sp.Rational(aa[0])); q0 = float(sp.Rational(bb[0]))
        if p0 <= 0 or q0 <= 0:
            return None
        return p0 / q0, p, aa, bb, q, B, R
    rs = [[F(random.randint(-4, 4), random.choice([1, 2])) for _ in range(random.randint(1, a.deg + 1))]
          for _ in range(a.m)]
    cur = None
    for _ in range(200):
        r = score(T, rs)
        if r is not None:
            cur = (r[0], copy.deepcopy(rs)); break
        rs = [[F(random.randint(-4, 4), random.choice([1, 2])) for _ in range(random.randint(1, a.deg + 1))]
              for _ in range(a.m)]
    if cur is None:
        print("no admissible start found"); return
    best = (cur[0], copy.deepcopy(cur[1]))
    print("start: p0/q0 = %.8f  Delta = %.6f" % (best[0], best[0] * 4 * 3.141592653589793 / 3))
    for it in range(a.iters):
        rs2 = copy.deepcopy(cur[1])
        i = random.randrange(len(rs2)); j = random.randrange(len(rs2[i]))
        rs2[i][j] += F(random.choice([-2, -1, 1, 2]), random.choice([1, 2, 3, 4]))
        r = score(T, rs2)
        if r is None:
            continue
        if r[0] < cur[0] or r[0] < cur[0] * (1 + a.uphill):
            cur = (r[0], rs2)
        if r[0] < best[0] - 1e-12:
            best = (r[0], rs2)
    print("best p0/q0 = %.8f" % best[0])
    p, B, R = build(T, best[1])
    q, aa, bb = p_to_q(p, K, SC)
    rec = exact_ok(aa, K)
    if rec is None or not rec["ok"]:
        print("final candidate failed exact verification:", (rec or {}).get("reason")); return
    d = EC.delta_upper_decimal(rec, 8)
    print("EXACT: Delta <= %s" % d)
    print("  -p = (u-%s) * [ %s ]" % (T, " + ".join("(%s)^2" % sp.expand(x) for x in R)))
    print("  q(u) =", sp.expand(q))
    json.dump(dict(script="KeplerConjecture/Computation/sos_pside_many.py",
                   family="-p = (u-T) * sum r_i^2", status="VERIFIED_EXACT",
                   note=("p certified by construction with an explicit rational Gram; q by exact "
                         "Sturm with Computation's checker, not Main's (unsound)"),
                   T=str(T), m=a.m, deg=a.deg, delta=d,
                   squares=[str(sp.expand(x)) for x in R],
                   q=str(sp.expand(q)), p=str(sp.expand(p))), open(a.out, "w"), indent=1)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
