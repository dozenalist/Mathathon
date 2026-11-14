"""Independent second implementation of the m12 criterion: brute-force rational scan.

Different algorithm from audit_gamma.py (which computes the difference set
U_B - U_A and tests psi against it).  Here we scan t over a grid of rationals and test
the six membership conditions directly, requiring the WHOLE psi enclosure to land inside
E_B.  The scan is a search, not a decision procedure, but combined with the interval
algebra of audit_gamma.py (which decides emptiness exactly) the two together give the
two-independent-procedures requirement: every ELIMINATION is certified by an explicit
witness that both programs verify, and every survival is decided by the exhaustion in
audit_gamma.py and confirmed by the scan finding nothing.
"""
from fractions import Fraction as F
import itertools
from ival import models, dirset, member, contains, norm
import consts

STEP = F(1, 20)             # grid of t in steps of 0.05 degree

def scan(EA, EB, tmax=360):
    hits = []
    t = F(0)
    while t < tmax:
        ok = True
        for j in range(3):
            if not member(EA, t + 120 * j):
                ok = False
                break
        if ok:
            for j in range(3):
                lo = (t + consts.PSI_LO + 120 * j) % 360
                hi = (t + consts.PSI_HI + 120 * j) % 360
                if lo <= hi:
                    good = contains(EB, lo, hi)
                else:
                    good = contains(EB, lo, F(360)) and contains(EB, F(0), hi)
                if not good:
                    ok = False
                    break
        if ok:
            hits.append(t)
        t += STEP
    return hits

def main():
    print("independent grid scan (step 0.05 deg) of the six membership conditions")
    for name, word in models().items():
        vals = sorted(set(word), key=lambda s: (len(s), sorted(s)))
        found = []
        for A, B in itertools.permutations(vals, 2):
            if A & B:
                continue
            EA, EB = dirset(word, A), dirset(word, B)
            h = scan(EA, EB)
            if h:
                found.append((sorted(A), sorted(B), len(set(A) | set(B)), h[0]))
        killed = [f for f in found if f[2] >= 4]
        print("%-36s witnesses=%-3d  lethal(|AuB|>=4)=%s"
              % (name, len(found), "YES" if killed else "no"))
        for A, B, u, t in killed[:2]:
            print("        A=%-9s B=%-9s |AuB|=%d  t = %s deg = %.6f"
                  % (A, B, u, t, float(t)))

if __name__ == "__main__":
    main()
