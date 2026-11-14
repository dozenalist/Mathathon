#!/usr/bin/env python3
"""Re-verify a published K15 certificate JSON with exact arithmetic.

Usage:  python3 verify_certificate.py out/verified_certificate_K33.json
Exit 0 iff both exact implementations accept it.

What is checked, in exact rational arithmetic with no floating point in any decision:
  1. exactcert.certify (hand-rolled Fraction polynomials, own Sturm chain, Yun decomposition)
  2. exactcert_oracle.oracle (independent SymPy sqf_list + count_roots)
  3. the stored ratio p0/q0 and the directed (upward-rounded) Delta agree with recomputation.
"""
import json, sys
from fractions import Fraction as F
import exactcert as EC

def main(path):
    d = json.load(open(path))
    c = [F(x) for x in d["coefficients_rational"]]
    r = EC.certify(c, allow_touching=False, verbose=False)
    print("certificate:", path)
    print("  degree      :", d.get("degree"))
    print("  exactcert   :", "ACCEPT" if r["ok"] else "REJECT (%s)" % r["reason"])
    if not r["ok"]:
        return 1
    ratio = F(r["p0"]) / F(r["q0"])
    print("  p0/q0       :", ratio)
    print("  Delta upper :", EC.delta_upper_decimal(r, 12), "(rounded up)")
    if "ratio_exact" in d:
        ok = (F(d["ratio_exact"]) == ratio)
        print("  stored ratio matches:", ok)
        if not ok:
            return 1
    try:
        import exactcert_oracle as OR
        r2 = OR.oracle(c)
        print("  sympy oracle:", "ACCEPT" if r2["ok"] else "REJECT (%s)" % r2["reason"])
        if not r2["ok"]:
            return 1
    except ImportError:
        print("  sympy oracle: SKIPPED (sympy unavailable)")
    print("  VERIFIED")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "out/verified_certificate_K33.json"))
