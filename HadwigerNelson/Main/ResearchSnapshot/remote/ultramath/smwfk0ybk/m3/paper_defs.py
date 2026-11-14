"""Independent check of the sliver encoding against the paper's literal definition.

Paper, S8.1 (verbatim, p.51): "Let B be the finite, antipodally symmetric set of
directions perpendicular to at least one v_j.  At e not in B, give edge j sign + or
- according as e . v_j is positive or negative.  Let O(e) be the set of labels
remaining after the endpoints of every positive edge are removed, and let I(e) be
the set remaining after the endpoints of every negative edge are removed.  Labels
outside the cycle belong to both sets."

So, literally, with the l-cycle on labels 0..l-1 and edge j = {j, j+1}:

    O(e) = [k] \\ union{ {j, j+1} : sig_j = +1 }
    I(e) = [k] \\ union{ {j, j+1} : sig_j = -1 }

The encoding used by the accepted input (m5) is
    O = U | {j : sig_{j-1} = -1 and sig_j = -1},  I = U | {j : both +1},
with U = [k] \\ {0..l-1}.  This file checks the two agree for every (l, k, geometry)
at k = 6, and records the two consequences the argument uses:
    (i)  U subset of O(e) and of I(e)  (this is the paper's own sentence);
    (ii) O(e) cap I(e) contains U, hence any palette meeting U meets both slivers.
"""
from itertools import product
from csp_vacuity import COS, sig_matrix, slivers

K = 6


def paper_slivers(l, k, s):
    full = set(range(k))
    O = set(full)
    I = set(full)
    for j in range(l):
        e = {j, (j + 1) % l}
        if s[j] == 1:
            O -= e
        else:
            I -= e
    return O, I


def m5_slivers(l, k, s):
    O, I = slivers(l, k, s)
    return {x for x in range(k) if (O >> x) & 1}, {x for x in range(k) if (I >> x) & 1}


def main():
    bad = 0
    checked = 0
    U_in_both = True
    for k in (4, 5, 6, 7):
        for l in range(3, k + 1):
            for tail in product(range(6), repeat=l - 1):
                c = (0,) + tail
                sig = sig_matrix(l, c)
                U = set(range(k)) - set(range(l))
                for i in range(6):
                    a = paper_slivers(l, k, sig[i])
                    b = m5_slivers(l, k, sig[i])
                    checked += 1
                    if a != b:
                        bad += 1
                        if bad < 5:
                            print("MISMATCH", k, l, c, i, sorted(a[0]), sorted(b[0]))
                    if not (U <= a[0] and U <= a[1]):
                        U_in_both = False
                        print("U NOT CONTAINED", k, l, c, i)
    print(f"sliver sets compared: {checked}, mismatches: {bad}")
    print(f"U subset of O(e) and I(e) on every one: {U_in_both}")


if __name__ == "__main__":
    main()
