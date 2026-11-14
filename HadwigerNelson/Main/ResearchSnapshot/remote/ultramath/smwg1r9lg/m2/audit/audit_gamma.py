"""Audit of m12's sum-set criterion (Theorem 1 + Theorem 2) on the record's models.

For a pair of palette values A != B (as subsets of [6]) carried on the direction sets
E_A, E_B of a (centre-independent) palette field, m12's Theorem 2 gives a contradiction
with |I \\ (A u B)| >= 3  provided  there is  t  with
      t, t+120, t+240 in E_A   and   t+psi, t+psi+120, t+psi+240 in E_B   (or swapped),
where psi = 180 + gamma, gamma = 2 arcsin(1/(2 sqrt 3))  (cos gamma = 5/6).

Decision, exactly: U_A = {t : t+120j in E_A, j<3}, U_B likewise (rational interval sets),
    witness exists  <=>  psi in U_B - U_A   (mod 360)  or  psi in U_A - U_B.
psi is irrational (gamma/pi irrational: 2cos(gamma) = 5/3 would be a sum of roots of
unity, i.e. an algebraic integer, but 5/3 is not), so the enclosure test below is decisive
as soon as the enclosure does not straddle a boundary of the rational set U_B - U_A.
Witnesses are verified by interval containment for the WHOLE enclosure of psi (not just
its endpoints, which is what m12/verify.py does).
"""
from fractions import Fraction as F
import itertools
from ival import (norm, inter, rotate, diff, contains, member, width, maxint,
                  models, dirset)
import consts

PSI_LO, PSI_HI = consts.PSI_LO, consts.PSI_HI

def orbit3(E):
    """{t : t, t+120, t+240 in E} = E cap (E-120) cap (E-240)."""
    return inter(inter(E, rotate(E, 120)), rotate(E, 240))

def decide(EA, EB):
    """return ('yes', t, role) / ('no',) for the criterion  psi in U_B - U_A (or swapped)."""
    UA, UB = orbit3(EA), orbit3(EB)
    if width(UA) == 0 or width(UB) == 0:
        return ('no',)
    for role, U1, U2 in (('A->B', UA, UB), ('B->A', UB, UA)):
        D = diff(U1, U2)                     # psi must lie in {u2 - u1}
        if width(D) == 0:
            continue
        # is the whole enclosure inside D, or disjoint from it?
        inside = any(a <= PSI_LO and PSI_HI < b for a, b in norm(D))
        if not inside:
            # check disjointness (no refinement needed: intervals are exact)
            if all(PSI_HI < a or PSI_LO >= b for a, b in norm(D)):
                continue
            raise RuntimeError("psi enclosure straddles a boundary of D")
        # construct t: find intervals I in U1, J in U2 with psi_lo,psi_hi in J - I
        for (a1, a2) in norm(U1):
            for (b1, b2) in norm(U2):
                lo_ok, hi_ok = b1 - a2, b2 - a1
                if lo_ok <= PSI_LO and PSI_HI <= hi_ok:
                    t_lo = max(a1, b1 - PSI_LO)
                    t_hi = min(a2, b2 - PSI_HI)
                    if t_hi - t_lo > 0:
                        t = (t_lo + t_hi) / 2
                        if verify(EA, EB, t, role):
                            return ('yes', t, role)
        raise RuntimeError("interval algebra says yes but no witness constructed")
    return ('no',)

def verify(EA, EB, t, role):
    """rigorous: t + 120j in E_first, and the whole psi-enclosure of t+psi+120j in E_second."""
    Ef, Es = (EA, EB) if role == 'A->B' else (EB, EA)
    for j in range(3):
        if not member(Ef, t + 120 * j):
            return False
        lo, hi = (t + PSI_LO + 120 * j) % 360, (t + PSI_HI + 120 * j) % 360
        if lo <= hi:
            if not contains(Es, lo, hi):
                return False
        else:                                   # enclosure wraps at 360: split
            if not (contains(Es, lo, F(360)) and contains(Es, F(0), hi)):
                return False
    return True

def card_union(A, B):
    return len(set(A) | set(B))

def main():
    print("psi = 180+gamma in degrees: (%.24f, %.24f)" % (float(PSI_LO), float(PSI_HI)))
    print("chi(unit triangle) = 3, so a pair with |A u B| >= 4 is a contradiction at k = 6")
    print()
    rows = []
    for name, word in models().items():
        vals = sorted(set(word), key=lambda s: (len(s), sorted(s)))
        status, kills = "survives", []
        for A, B in itertools.combinations(vals, 2):
            if A & B:
                continue
            EA, EB = dirset(word, A), dirset(word, B)
            res = decide(EA, EB)
            if res[0] == 'yes' and card_union(A, B) >= 4:
                kills.append((sorted(A), sorted(B), card_union(A, B), res[1], res[2]))
        if kills:
            status = "ELIMINATED"
        rows.append((name, [sorted(v) for v in vals], status, kills))
        print("%-36s %s" % (name, status))
        for A, B, u, t, role in kills[:3]:
            print("      A=%-9s B=%-9s |AuB|=%d  T'=%d  role %s  t = %.6f deg (exact %s)"
                  % (A, B, u, 6 - u, role, float(t), t))
    print()
    n_elim = sum(1 for r in rows if r[2] == "ELIMINATED")
    print("eliminated: %d of %d" % (n_elim, len(rows)))
    print("survivors:", [r[0] for r in rows if r[2] != "ELIMINATED"])

if __name__ == "__main__":
    main()
