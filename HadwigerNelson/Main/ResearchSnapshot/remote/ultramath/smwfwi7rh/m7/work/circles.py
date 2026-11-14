"""
Exact enumeration for the circle side of the k=6 palette system (m7, direction d15).

m sectors of equal angle 2*pi/m, m divisible by 6; R (rotation by pi/3) = shift s = m/6.
All constraints have the form value(i) compatible with value(i+s), so the constraint
graph on Z/m is a disjoint union of gcd(m,s) = s cycles of length 6.  Hence the number
of solutions is  tr(A^6)^s  where A is the compatibility matrix.  Procedure A is this
transfer-matrix count; procedure B is a brute-force product enumeration for m = 6, 12.

Systems:
 (1) 2-colourings with c(i) != c(i+s).
 (2) 3-colourings with c(i) != c(i+s).
 (3) inward palettes of a T-coloured circle (T = {1,2,3}): Q(i) a nonempty subset of
     T^c = {4,5,6} with Q(i) cap Q(i+s) = empty.
"""
from itertools import product, combinations

def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t]*B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]

def matpow(A, e):
    n = len(A); R = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1: R = matmul(R, A)
        A = matmul(A, A); e >>= 1
    return R

def count_transfer(A, s):
    M6 = matpow(A, 6)
    return sum(M6[i][i] for i in range(len(A)))**s

def brute(m, alphabet, compat):
    s = m // 6
    return sum(1 for c in product(alphabet, repeat=m)
               if all(compat(c[i], c[(i+s) % m]) for i in range(m)))

def main():
    ne = lambda a, b: a != b
    print("(1) 2-colourings of the circle with c(theta+60deg) != c(theta)")
    A2 = [[int(ne(a, b)) for b in (1, 2)] for a in (1, 2)]
    for m in (6, 12, 18, 24, 60):
        s = m//6
        n = count_transfer(A2, s)
        line = f"    m={m:2d}: {n:8d}"
        if m <= 12:
            line += f"   brute force: {brute(m, (1,2), ne):8d}"
        print(line)
    print("    closed form 2^s (s = m/6):", [2**(m//6) for m in (6,12,18,24,60)])

    print("\n(2) 3-colourings of the circle with c(theta+60deg) != c(theta)")
    A3 = [[int(ne(a, b)) for b in (1, 2, 3)] for a in (1, 2, 3)]
    for m in (6, 12, 18):
        s = m//6
        line = f"    m={m:2d}: {count_transfer(A3, s):8d}"
        if m <= 12:
            line += f"   brute force: {brute(m, (1,2,3), ne):8d}"
        print(line)

    print("\n(3) inward palettes of a {1,2,3}-coloured circle: Q nonempty subset of {4,5,6},")
    print("    Q(i) cap Q(i+s) = empty  (the 60-degree exclusion at the circle's points)")
    subs = [frozenset(S) for r in (1, 2, 3) for S in combinations((4, 5, 6), r)]
    disj = lambda a, b: not (a & b)
    AQ = [[int(disj(a, b)) for b in subs] for a in subs]
    for m in (6, 12, 18, 24):
        s = m//6
        line = f"    m={m:2d}: {count_transfer(AQ, s):12d}"
        if m == 6:
            line += f"   brute force: {brute(m, subs, disj):12d}"
        print(line)

    print("\n(4) the same with the extra requirement that the palette bounds hold, i.e. |Q| <= 3")
    print("    (automatic) and the self-avoidance c(x) not in Q(x) for every point x:")
    # the circle colour at sector i is c(i); the inward palette of the point in sector i is Q(i).
    # self-avoidance couples c and Q; count pairs (c,Q) with c(i) in T, Q(i) subset of T^c:
    # then c(i) not in Q(i) is automatic (T and T^c are disjoint).
    print("    automatic: Q(i) subset of {4,5,6} and c(i) in {1,2,3}, so c(i) not in Q(i).")

    print("\n(5) explicit witness at m = 12")
    m, s = 12, 2
    c = tuple(1 + (i // s) % 3 for i in range(m))
    Q = tuple(frozenset({4 + (i // s) % 2}) for i in range(m))
    ok = (all(c[i] != c[(i+s) % m] for i in range(m))
          and all(Q[i] and not (Q[i] & Q[(i+s) % m]) for i in range(m))
          and all(set(q) <= {4,5,6} for q in Q)
          and all(c[i] not in Q[i] for i in range(m)))
    print("    c =", c)
    print("    Q =", [sorted(q) for q in Q])
    print("    passes all four checks:", ok)

main()
