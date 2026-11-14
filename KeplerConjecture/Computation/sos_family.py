#!/usr/bin/env python3
"""K15 structured sum-of-squares certificate family, with EXPLICIT rational Gram data.

WHY THIS FILE EXISTS.  Review 0138-C asks for actual SOS certificates with explicit rational
polynomial/Gram identities and independent exact verification, rather than an LP that is
described as if it were an SDP.  This file constructs a family in which the sign conditions are
met BY AN EXPLICIT SQUARE, so that the certificate is an algebraic identity checkable by
expansion alone -- no Sturm sequence, no root counting, no trusting anybody's checker.

THE FAMILY (dimension 3, unit spheres, minimum separation 2, u = pi|x|^2)
    f = e^{-pi|x|^2} p(u),      fhat = e^{-pi|y|^2} q(u'),      q = M p   (M rational, M^2 = I)

  For rational  T <= 4*pi  and rational  c,  take

      p(u) = -(u - T)(u - c)^2 .                                            (F)

  Then, identically as polynomials in Q[u],

      -p = (u - T) * (u - c)^2 = sigma_0 + (u - T) sigma_1 ,
      with sigma_0 = 0 and sigma_1 = (u - c)^2, a single rational square,

  so  p <= 0 on [T, infinity), hence on [4*pi, infinity) since T <= 4*pi.  This is
  Markov-Lukacs in its most explicit form: the multiplier is literally a square.

  Also  p(0) = T c^2 > 0 , so f(0) > 0 as a Cohn-Elkies certificate requires.

  The remaining condition is  q >= 0 on [0, infinity), where q = M p is DETERMINED by p -- it
  cannot be imposed by construction because M is an involution coupling the two sides.  It is
  therefore verified exactly, by Computation's own checker (exactcert.py), and the search below
  is over (T, c) only.

WHAT IS AND IS NOT CLAIMED
  * Claimed for any (T, c) that passes:  Delta <= (4 pi/3) p(0)/q(0)  for every unit-sphere
    packing, with the p-side certified by an explicit rational square and the q-side by exact
    Sturm over Q.
  * NOT claimed: that these are optimal, or that the LP-optimal certificates admit a rational
    Gram export.  They do not: measured, the LP-optimal q and -p are IRREDUCIBLE over Q at
    every degree 5, 7, 9, 13, 33 (see REVIEW_0138.md), so no factorisation-based rational SOS
    representation of those objects exists.

Usage:
    python3 sos_family.py                 # small search, a few seconds
    python3 sos_family.py --out out/sos_family.json
"""
import argparse, json, itertools
from fractions import Fraction as F
import sympy as sp
import exactcert as EC

def M_matrix(K, checker):
    return checker.fourier_map(K)

def certificate(T, c, SC, K=3):
    """Rational p, q, Gram data and the exact verdict.  All in Q[u]."""
    u = sp.Symbol('u')
    T = sp.Rational(F(T).numerator, F(T).denominator)
    c = sp.Rational(F(c).numerator, F(c).denominator)
    p = sp.expand(-(u - T) * (u - c) ** 2)
    P = sp.Poly(p, u)
    a = [P.coeff_monomial(u ** i) for i in range(4)]
    M = SC.fourier_map(3)
    b = [sum(M[i, k] * a[k] for k in range(4)) for i in range(4)]
    q = sp.expand(sum(b[i] * u ** i for i in range(4)))
    # explicit Gram data for the p-side: -p = sigma_0 + (u-T) sigma_1
    sigma0 = sp.Integer(0)
    r1 = sp.expand(u - c)                     # the single square
    gram_ok = sp.expand(sigma0 + (u - T) * r1 ** 2 - (-p)) == 0
    return dict(T=str(T), c=str(c), p=str(p), q=str(q),
                a=[str(x) for x in a], b=[str(x) for x in b],
                gram_p=dict(sigma0="0", sigma1_squares=[str(r1)],
                            identity="-p = sigma0 + (u - T) * (u - c)^2",
                            verified_by_expansion=bool(gram_ok)),
                p0=str(a[0]), q0=str(b[0]))

def exactly_verify(T, c, rec, SC):
    """Independent verification: (i) the Gram identity by expansion, (ii) q >= 0 by exact
    Sturm using Computation's own checker (not Main's, which review 0138-C shows is unsound),
    (iii) the rational pi containment T <= 4*pi."""
    u = sp.Symbol('u')
    Tq = sp.Rational(rec["T"]); cq = sp.Rational(rec["c"])
    p = sp.expand(sum(sp.Rational(x) * u ** i for i, x in enumerate(rec["a"])))
    gram = sp.expand((u - Tq) * (u - cq) ** 2 - (-p)) == 0
    # q >= 0 on [0,inf) and p <= 0 on [T,inf), both by my own exact Sturm checker
    K = 3
    cfr = [F(rec["a"][i]) for i in range(K + 1)]
    # convert monomial-u coefficients to Laguerre-t for exactcert
    ell = EC.laguerre_polys(K); rem = list(cfr); cl = [F(0)] * (K + 1)
    for j in range(K, -1, -1):
        lc = ell[j][-1] * (F(2) ** j); cj = rem[j] / lc; cl[j] = cj
        for i in range(len(ell[j])):
            rem[i] -= cj * ell[j][i] * (F(2) ** i)
    conv_ok = all(x == 0 for x in rem)
    r = EC.certify(cl, allow_touching=False, verbose=False)
    pi_ok = F(rec["T"]) <= 4 * EC.PI_LO
    return dict(gram_identity=bool(gram), basis_conversion=bool(conv_ok),
                q_nonneg_and_p_negative=r["ok"], checker_reason=r["reason"],
                T_le_4pi=bool(pi_ok),
                all_pass=bool(gram and conv_ok and r["ok"] and pi_ok),
                delta_upper=EC.delta_upper_decimal(r, 8) if r["ok"] else None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", default="/tmp/sc662.py")
    ap.add_argument("--out", default="out/sos_family.json")
    a = ap.parse_args()
    import importlib.util
    spec = importlib.util.spec_from_file_location("sc", a.checker)
    SC = importlib.util.module_from_spec(spec); spec.loader.exec_module(SC)
    print("Searching p(u) = -(u-T)(u-c)^2 for a certificate with an explicit rational Gram.")
    print("T must satisfy T <= 4*pi = 12.566...\n")
    best = None; rows = []
    for Tn, Td in ((12, 1), (125, 10), (1256, 100)):
        T = F(Tn, Td)
        for cn in range(1, 13):
            for cd in (1, 2):
                c = F(cn, cd)
                rec = certificate(T, c, SC)
                ver = exactly_verify(T, c, rec, SC)
                if ver["all_pass"]:
                    val = float(F(rec["p0"]) / F(rec["q0"])) * 4 * 3.141592653589793 / 3
                    rows.append(dict(T=str(T), c=str(c), delta=val, verdict=ver, cert=rec))
                    if best is None or val < best[1]:
                        best = (rec, val, ver)
    print("certificates found: %d" % len(rows))
    if best:
        rec, val, ver = best
        print("BEST in the family: T=%s c=%s" % (rec["T"], rec["c"]))
        print("  p(u) = %s" % rec["p"])
        print("  q(u) = %s" % rec["q"])
        print("  Gram identity: -p = 0 + (u-%s)*(u-%s)^2   verified by expansion: %s"
              % (rec["T"], rec["c"], ver["gram_identity"]))
        print("  q >= 0 on [0,inf) by exact Sturm (my checker): %s" % ver["q_nonneg_and_p_negative"])
        print("  Delta <= %.8f   (Kepler 0.74048049, CE 0.779747)" % val)
        json.dump(dict(script="KeplerConjecture/Computation/sos_family.py",
                       family="p(u) = -(u-T)(u-c)^2, explicit rational Gram on the p-side",
                       status="VERIFIED_EXACT",
                       note=("p-side certified by the identity -p = sigma0 + (u-T) sigma1 with "
                             "sigma1 = (u-c)^2 a single rational square; q-side by exact Sturm "
                             "using Computation's own checker, NOT Main's (unsound per review 0138-C)"),
                       best=dict(verdict=ver, cert=rec, delta=val),
                       all_found=[dict(T=r["T"], c=r["c"], delta=r["delta"]) for r in rows],
                       ), open(a.out, "w"), indent=1)
        print("wrote", a.out)
    else:
        print("no certificate found in this family at these parameters")

if __name__ == "__main__":
    main()
