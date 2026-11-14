"""Checks for Theorem B'' and Corollary A3 of L4.md.

B'' : (i) KG(6,2) is 4-colourable -- the four families F1..F4 below partition the 15
          2-subsets of [6] and each is intersecting (no two disjoint members);
      (ii) a palette field of constant size m with disjointness at unit distance needs
           3m <= k (unit triangle);
      (iii) hence at k=6 the constant-size regimes are m=2 (killed by (i) via
           homomorphism + chi(R^2)>=6), m=3 (killed by 3m=9>6), m=1 (a proper
           6-colouring, i.e. the L2 problem).
A3 : the single-centre 6-direction design T,Q,T,Q,T,Q satisfies the rotation exclusion
     (5.7) including the wrap-around, at k=6 with a palette of size 3 and at k=5 with 2.
"""
import itertools

def check_kneser():
    P2 = [frozenset(c) for c in itertools.combinations(range(1, 7), 2)]
    F1 = [frozenset({1, i}) for i in range(2, 7)]
    F2 = [frozenset({2, i}) for i in range(3, 7)]
    F3 = [frozenset({3, 4}), frozenset({3, 5}), frozenset({3, 6})]
    F4 = [frozenset({4, 5}), frozenset({4, 6}), frozenset({5, 6})]
    fams = [F1, F2, F3, F4]
    cover = set()
    for F in fams:
        for s in F: cover.add(s)
    ok_partition = (cover == set(P2)) and sum(len(F) for F in fams) == 15
    ok_intersecting = all(len(a & b) > 0 for F in fams for a, b in itertools.combinations(F, 2))
    return dict(partition=ok_partition, sizes=[len(F) for F in fams], intersecting=ok_intersecting,
                chi_KG62_le=4)

def check_rotation(pal):
    """pal[j] is the palette at direction e_j = R^j e0, R has order 6.
    (5.7) requires pal[j] cap pal[j+1] = empty for j mod 6."""
    return all(not (pal[j] & pal[(j+1) % 6]) for j in range(6))

def main():
    print("KG(6,2):", check_kneser())
    for k, T, Q in ((6, {1, 2, 3}, {4, 5}), (5, {1, 2}, {3, 4})):
        pal = [T if j % 2 == 0 else Q for j in range(6)]
        print("k=%d  palettes=%s  (5.7) holds=%s   max|P|=%d <= k-3=%d : %s"
              % (k, pal, check_rotation(pal), max(len(p) for p in pal), k-3,
                 max(len(p) for p in pal) <= k-3))
    for k in range(4, 9):
        allowed = [m for m in range(1, k-2) if 3*m <= k]
        print("k=%d : constant palette sizes m with 3m<=k and m<=k-3 : %s" % (k, allowed))

if __name__ == "__main__":
    main()
