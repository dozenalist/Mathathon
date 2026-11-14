#!/usr/bin/env python3
"""
Closed-form satisfying word for STRIP(k,ell) when k >= 6 (and for (5,3), (5,4)).

Phase vector:  p = floor(ell/2);  delta_i = 0 for i < p,  delta_i = 3 for i >= p.
With this delta, for j = 0,1,2:
    positive edges  {0,...,p-1}   -> endpoints {0,...,p}
    negative edges  {p,...,ell-1} -> endpoints {0} u {p,...,ell-1}
  so   O = {p+1,...,k-1},   I = {1,...,p-1} u {ell,...,k-1},
and for j = 3,4,5 the two sets are exchanged (R^3 = -1 flips every sign).

Word (period two):  P, Q, P, Q, P, Q.

  (A) k - ell >= 2 :  P = {k-2},        Q = {k-1}
  (B) k - ell == 1 :  P = {k-1},        Q = {1, p+1}
  (C) ell == k     :  P = {1, p+1},     Q = {2, p+2}

Verification runs model.check (S0..S4) for every (k,ell) in range, so the
closed form is checked, not asserted.
"""
from model import allowed, check

def make_word(k, ell):
    p = ell // 2
    if k - ell >= 2:
        P, Q = [k - 2], [k - 1]
    elif k - ell == 1:
        P, Q = [k - 1], [1, p + 1]
    else:                                   # ell == k
        P, Q = [1, p + 1], [2, p + 2]
    delta = [0] * p + [3] * (ell - p)
    word = [P if j % 2 == 0 else Q for j in range(6)]
    return delta, word

if __name__ == "__main__":
    bad = []
    sat = []
    for k in range(4, 41):
        for ell in range(3, k + 1):
            delta, word = make_word(k, ell)
            errs = check(k, ell, delta, word, strong=True)
            if errs:
                bad.append((k, ell, errs))
            else:
                sat.append((k, ell, delta[:4], word[0], word[1]))
    print("construction verified (S0-S4) for", len(sat), "(k,ell) pairs")
    fails = sorted({(k, ell) for k, ell, _ in bad})
    print("fails at:", fails)
    for k, ell, e in bad[:6]:
        print("   e.g.", k, ell, e[:3])
    print("\nSample rows:")
    for row in sat[:3] + [r for r in sat if r[0] == 6] + sat[-2:]:
        print("  k=%d ell=%d delta[:4]=%s P0=%s P1=%s" % row)
