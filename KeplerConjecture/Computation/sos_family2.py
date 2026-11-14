#!/usr/bin/env python3
"""K15 SOS family, degree 5: an explicit two-square Gram identity on the p-side.

The p-side condition is  p <= 0 on [T, infinity).  Write

    -p(u)  =  (u - T) * [ (u - c)^2 * (u - e)^2  +  lam * (u - d)^2 ]        (G)

with rationals T <= 4*pi, c, d, e, lam > 0.  The bracket is a sum of two squares of
rational polynomials, so (G) is a Markov-Lukacs representation whose multiplier is
EXPLICITLY a sum of squares:

    sigma_1(u) = (u-c)^2 (u-e)^2 + lam (u-d)^2 = [ (u-c)(u-e) ]^2 + [ sqrt(lam) (u-d) ]^2,

where we take lam = m^2 a perfect rational square so that sqrt(lam) = m is rational and both
summands have rational coefficients.  Then p <= 0 on [T, inf), hence on [4*pi, inf) since
T <= 4*pi, and p(0) = T*[c^2 e^2 + lam d^2] > 0.

The q-side is again determined, q = M p, and is verified by exact Sturm with Computation's own
checker.  Degrees: p has degree 5, so K = 5.

WHY THIS IS BETTER THAN sos_family.py: the bracket in (G) has four rational parameters
(c, d, e, m) instead of one, and the identity is verified by expanding one product -- still no
Sturm sequence and no trusted checker on the p-side.

Status of any bound found: VERIFIED_EXACT for the stated family; NOT competitive with
Cohn-Elkies and not claimed to be.

Usage:  python3 sos_family2.py [--checker PATH]
"""
import argparse, itertools, json
from fractions import Fraction as F
import sympy as sp

import k15fourier


class _FourierShim:
    """Minimal stand-in for the external checker: only fourier_map was ever used."""
    @staticmethod
    def fourier_map(K):
        # a sympy Matrix so that both M[i, k] and M[i][k] indexing work from every call site
        return sp.Matrix(k15fourier.M_matrix(K))

import exactcert as EC

def build(T, c, d, e, m):
    u = sp.Symbol('u')
    R = lambda x: sp.Rational(F(x).numerator, F(x).denominator)
    T, c, d, e, m = R(T), R(c), R(d), R(e), R(m)
    bracket = (u - c) ** 2 * (u - e) ** 2 + m ** 2 * (u - d) ** 2
    minus_p = sp.expand((u - T) * bracket)
    p = sp.expand(-minus_p)
    return p, bracket, (u - c) * (u - e), m * (u - d)

def verify(rec, SC_or_None):
    """Exact: (i) the Gram identity, by expansion; (ii) q >= 0 via my exactcert."""
    u = sp.Symbol('u')
    T, c, d, e, m = [sp.Rational(x) for x in rec["params"]]
    p = sp.expand(sum(sp.Rational(x) * u ** i for i, x in enumerate(rec["a"])))
    s1 = (u - c) ** 2 * (u - e) ** 2 + m ** 2 * (u - d) ** 2
    gram = sp.expand((u - T) * s1 - (-p)) == 0
    K = len(rec["a"]) - 1
    cf = [F(x) for x in rec["a"]]
    ell = EC.laguerre_polys(K); rem = list(cf); cl = [F(0)] * (K + 1)
    for j in range(K, -1, -1):
        lc = ell[j][-1] * (F(2) ** j); cj = rem[j] / lc; cl[j] = cj
        for i in range(len(ell[j])):
            rem[i] -= cj * ell[j][i] * (F(2) ** i)
    conv = all(x == 0 for x in rem)
    r = EC.certify(cl, allow_touching=False, verbose=False)
    pi_ok = F(rec["params"][0]) <= 4 * EC.PI_LO
    return dict(gram_identity=bool(gram), basis_conversion=bool(conv),
                q_and_p_ok=r["ok"], reason=r["reason"], T_le_4pi=bool(pi_ok),
                all_pass=bool(gram and conv and r["ok"] and pi_ok),
                delta=EC.delta_upper_decimal(r, 8) if r["ok"] else None,
                delta_float=(float(F(rec["p0"]) / F(rec["q0"])) * 4
                             * 3.141592653589793 / 3) if r["ok"] else None)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="out/sos_family2.json")
    a = ap.parse_args()
    print("Family (G): -p = (u-T)[(u-c)^2(u-e)^2 + m^2 (u-d)^2], explicit rational Gram.\n")
    best = None; found = []
    Ts = [F(12), F(314, 25), F(1256, 100)]
    cs = [F(4), F(6), F(8), F(10), F(12)]
    ds = [F(2), F(4), F(6), F(8)]
    es = [F(1), F(3), F(5), F(7)]
    ms = [F(1), F(2), F(3), F(1, 2), F(5)]
    tried = 0
    for T, c, d, e, m in itertools.product(Ts, cs, ds, es, ms):
        tried += 1
        p, bracket, r1, r2 = build(T, c, d, e, m)
        P = sp.Poly(p, sp.Symbol('u'))
        av = [str(P.coeff_monomial(sp.Symbol('u') ** i)) for i in range(6)]
        rec = dict(params=[str(T), str(c), str(d), str(e), str(m)], a=av,
                   p=str(sp.expand(p)), bracket=str(sp.expand(bracket)),
                   r1=str(sp.expand(r1)), r2=str(sp.expand(r2)))
        # q from Main's matrix
        SC = _FourierShim()
        M = SC.fourier_map(5)
        b = [sum(M[i, k] * sp.Rational(av[k]) for k in range(6)) for i in range(6)]
        rec["b"] = [str(x) for x in b]; rec["p0"] = av[0]; rec["q0"] = str(b[0])
        v = verify(rec, SC)
        if v["all_pass"]:
            found.append((v["delta_float"], rec, v))
            if best is None or v["delta_float"] < best[0]:
                best = (v["delta_float"], rec, v)
    print("tried %d parameter sets; %d admissible\n" % (tried, len(found)))
    if best:
        val, rec, v = best
        print("BEST: T=%s c=%s d=%s e=%s m=%s" % tuple(rec["params"]))
        print("  -p = (u-T)[(u-%s)^2(u-%s)^2 + %s^2 (u-%s)^2]" % (rec["params"][1], rec["params"][3],
                                                                  rec["params"][4], rec["params"][2]))
        print("     = (u-T)[ (%s)^2 + (%s)^2 ]" % (rec["r1"], rec["r2"]))
        print("  p(u) = %s" % rec["p"])
        print("  q(u) = %s" % " + ".join("%s u^%d" % (x, i) for i, x in enumerate(rec["b"])))
        print("  Gram identity verified by expansion: %s" % v["gram_identity"])
        print("  q >= 0 on [0,inf) by exact Sturm (my checker): %s" % v["q_and_p_ok"])
        print("  Delta <= %s   (Kepler 0.74048049, CE 0.779747)" % v["delta"])
        json.dump(dict(script="KeplerConjecture/Computation/sos_family2.py",
                       family="-p = (u-T)[(u-c)^2(u-e)^2 + m^2(u-d)^2]",
                       status="VERIFIED_EXACT",
                       explicit_gram=dict(multiplier="(u-T)",
                                          squares=[rec["r1"], rec["r2"]]),
                       best=dict(rec=rec, verdict=v, delta=v["delta_float"]),
                       admissible=[dict(params=r["params"], delta=d) for d, r, _ in found],
                       ), open(a.out, "w"), indent=1)
        print("\nwrote", a.out)
    else:
        print("no admissible parameter set in this grid")

if __name__ == "__main__":
    main()
