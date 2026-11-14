#!/usr/bin/env python3
"""Adversarial tests for exactcert.py.  Regression suite for review 48443.

Every test states what would constitute a bug.  Run: python3 exactcert_tests.py
Exit status 0 iff all pass.
"""
import json, sys
from fractions import Fraction as F
import exactcert as EC

FAILS = []

def check(name, cond, detail=""):
    if cond:
        print("  PASS  %s" % name)
    else:
        print("  FAIL  %s  %s" % (name, detail)); FAILS.append(name)

def main():
    print("T1 verbosity invariance: ok/reason identical in both modes")
    cases = [[2, -1], [1, 0], [-1, 0], [0, 0, 1], [F(1, 3), F(-2, 7), F(5, 11)],
             [1, -1, 1, -1], [3, 0, -2, 0, 1]]
    bad = []
    for c in cases:
        a = EC.certify(c, verbose=False)
        b = EC.certify(c, verbose=True)
        if (a["ok"] != b["ok"]) or (a["reason"] != b["reason"]):
            bad.append((c, a["ok"], b["ok"], a["reason"], b["reason"]))
    check("verbosity invariance", not bad, str(bad[:2]))

    print("T2 [2,-1] must be rejected (review 48443 case; p = t+1/2 > 0 off the ball)")
    r = EC.certify([2, -1])
    check("[2,-1] rejected", r["ok"] is False, r["reason"])
    check("[2,-1] no beats_kepler field", "beats_kepler" not in r or not r.get("beats_kepler"))

    print("T3 yun_odd_part preserves leading sign (the -t-1 -> t+1 defect)")
    c1, u1 = EC.yun_odd_part([F(-1), F(-1)])          # -t-1
    c2, u2 = EC.yun_odd_part([F(1), F(1)])            #  t+1
    check("odd part monic both signs", u1 == u2 == [F(1), F(1)], "%s %s" % (u1, u2))
    check("leading coefficients differ", (c1 < 0) != (c2 < 0), "%s %s" % (c1, c2))
    # sign identity at a sample point
    t0 = F(7, 2)
    s_p = (EC.peval([F(-1), F(-1)], t0) > 0)
    s_pred = (c1 > 0) == (EC.peval(u1, t0) > 0)
    check("sign(p) = sign(c)*sign(u)", s_p == s_pred, "%s %s" % (s_p, s_pred))

    print("T4 degenerate inputs fail closed")
    check("zero polynomial rejected", EC.certify([0, 0, 0])["ok"] is False)
    check("constant c rejected", EC.certify([F(-3)])["ok"] is False)
    c3, u3 = EC.yun_odd_part([F(0)])
    check("yun(0) returns (None,None)", c3 is None and u3 is None)
    c4, u4 = EC.yun_odd_part([F(-5)])
    check("yun(constant) keeps sign", c4 == F(-5) and u4 == [F(1)], "%s %s" % (c4, u4))

    print("T5 the submitted K21 certificate must be REJECTED (review 48443)")
    try:
        blob = json.load(open("out/certificate_K21.json"))
        c = [F(str(x)) for x in blob["certificate"]["c"]]
        r = EC.certify(c, verbose=False)
        check("K21 rejected", r["ok"] is False, r["reason"])
        # Rejection may come from either condition.  This implementation finds simple
        # roots of p on the half-line (A1); the reviewer's independent reconstruction
        # found ten simple roots of q (A2).  Either refutes the candidate.
        check("K21 reason cites a failed condition",
              ("A1" in (r["reason"] or "")) or ("A2" in (r["reason"] or "")), r["reason"])
        # reproduce the reviewer's witness directly
        w = F(57955199, 21687900)
        p, q = EC.build_pq(c)
        qv = EC.peval(q, w)
        check("witness q(57955199/21687900) < 0", qv < 0, "q = %s ~ %.6e" % (qv, float(qv)))
        check("witness value matches review ~ -3.876e-5",
              abs(float(qv) + 3.876231892749308e-05) < 1e-9, "%.6e" % float(qv))
    except FileNotFoundError:
        print("  SKIP  out/certificate_K21.json absent")

    print("T5b every retained candidate file declares REFUTED and is rejected")
    for K in (9, 11, 13, 15, 17, 19, 21):
        path = "out/certificate_K%d.json" % K
        try:
            blob = json.load(open(path))
        except FileNotFoundError:
            print("  SKIP  %s absent" % path)
            continue
        check("%s declares status REFUTED" % path, blob.get("status") == "REFUTED",
              blob.get("status"))
        check("%s keeps the old claim as declared_status_original" % path,
              "declared_status_original" in blob, list(blob.keys())[:4])
        cc = [F(str(x)) for x in blob["certificate"]["c"]]
        rr = EC.certify(cc, verbose=False)
        check("%s is rejected by the repaired checker" % path, rr["ok"] is False, rr["reason"])

    print("T6 independent oracle agreement (sympy), random low-degree c")
    try:
        import random
        import sympy as sp
        t = sp.symbols("t")
        def oracle(c):
            K = len(c) - 1
            p = sum(sp.Rational(x) * sp.assoc_laguerre(k, sp.Rational(1, 2), t) for k, x in enumerate(c))
            q = sum(sp.Rational(x) * sp.Rational((-1) ** k) * sp.assoc_laguerre(k, sp.Rational(1, 2), t)
                    for k, x in enumerate(c))
            A1 = 8 * sp.pi.evalf(30)
            for poly, lo, want in ((p, A1, -1), (q, 0, 1)):
                # sample densely; a sign disagreement means the oracle rejects
                for j in range(4001):
                    x = lo + (lo + 20) * j / 4000.0
                    v = float(poly.subs(t, x))
                    if v != 0 and (v > 0) != (want > 0):
                        return False
            return True
        random.seed(0)
        dis = []
        agree = 0
        for _ in range(25):
            K = random.choice([1, 3, 5, 7])
            c = [F(random.randint(-4, 4), random.randint(1, 5)) for _ in range(K + 1)]
            if all(x == 0 for x in c):
                continue
            mine = EC.certify(c, verbose=False)["ok"]
            theirs = oracle(c)
            agree += 1
            if mine and not theirs:
                dis.append(("I accept, oracle rejects", c))
        check("no case accepted by me but rejected by oracle", not dis, str(dis[:1]))
        print("        (%d random candidates cross-checked)" % agree)
    except ImportError:
        print("  SKIP  sympy unavailable")

    print()
    if FAILS:
        print("FAILED: %d -> %s" % (len(FAILS), FAILS)); return 1
    print("ALL TESTS PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
