"""Explicit uniform certificate for the (C1)-(C5) tightened CSP at k=6, l=3 and l=4.

Claim: for EVERY ray geometry (all 6^l cell vectors), the palettes
    P_i = {l}     (i even),  P_i = {l+1}   (i odd),   i = 0..5
satisfy (C1)-(C5) at k = 6, provided l <= k-2 (so that l and l+1 are both outsiders).

Reason (hand proof, no search): an outsider label is in BOTH allowed sets,
O_i and I_i, for every i -- that is display (8.1): labels outside the cycle belong
to both.  Hence a singleton outsider palette meets both O_i and I_i, which is (C2).
(C1) holds because 1 <= 1 <= k-3 = 3.  (C3) holds because consecutive palettes are
{l},{l+1} or {l+1},{l}, both empty intersections, and cyclically P_5 cap P_0 = empty.
(C4) holds vacuously: no palette is a 3-set.  (C5) holds: no palette is ternary.
"""
import itertools, sys
from csp45 import allowed, sigma

def check(l, k=6):
    labels = {(0,), (1,)}          # placeholder, not used
    bad = 0
    total = 0
    for c in itertools.product(range(6), repeat=l):
        total += 1
        pals = []
        for i in range(6):
            p = (1 << l) if i % 2 == 0 else (1 << (l + 1))
            pals.append(p)
        # (C1)
        ok = all(1 <= bin(p).count("1") <= k - 3 for p in pals)
        # (C2)
        for i in range(6):
            O, I = allowed(l, k, c, i)
            ok = ok and bool(pals[i] & O) and bool(pals[i] & I)
        # (C3)
        for i in range(6):
            ok = ok and not (pals[i] & pals[(i + 1) % 6])
        # (C4)
        full = (1 << k) - 1
        for i in range(6):
            for j in range(i + 1, 6):
                if bin(pals[i]).count("1") == 3 and pals[j] == full ^ pals[i]:
                    ok = False
        # (C5)
        ok = ok and sum(1 for p in pals if bin(p).count("1") == 3) <= 3
        if not ok:
            bad += 1
            if bad <= 3:
                print("FAIL", l, c)
    return total, bad

if __name__ == "__main__":
    for l in (3, 4):
        t, b = check(l)
        print(f"l={l}: geometries={t}, models rejected={b}")
    # sanity: l=5 fails only because l and l+1 are not both outsiders (5+1 = 6 = k)
    print("note: l <= k-2 = 4 required, so the certificate covers l = 3,4; l = 5,6 need pairs.")
