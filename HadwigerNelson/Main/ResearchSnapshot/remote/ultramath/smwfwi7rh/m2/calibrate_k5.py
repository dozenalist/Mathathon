"""Calibration of the k=6 single-centre framework at k=5 (AUDIT.md section 1b).

The alphabet + (T) is the same object at any k (palette bound k-3).  At k=5 and a
triangle it must reproduce the paper's section 6.3 triangle conclusion, and it must
show exactly where k=6 departs.

Run:  python3 calibrate_k5.py
"""
from itertools import combinations


def alphabet(K, ell, i):
    out = []
    for r in range(1, (K - 3) + 1):
        for c in combinations([x for x in range(K) if x != i], r):
            P = frozenset(c)
            if any(P <= {v, (v + 1) % ell} for v in range(ell)):
                continue
            out.append(P)
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def tr6(A):
    m = len(A)
    M = [[0 if (A[a] & A[b]) else 1 for b in range(m)] for a in range(m)]
    def mul(X, Y):
        return [[sum(X[r][t] * Y[t][c] for t in range(m)) for c in range(m)]
                for r in range(m)]
    P = [r[:] for r in M]
    for _ in range(5):
        P = mul(P, M)
    return sum(P[a][a] for a in range(m))


def main():
    print(f"{'k':>2s} {'ell':>3s} {'i':>2s} {'|A|':>4s} {'words':>7s} "
          f"{'outsiders':>10s}  palettes avoiding the outsiders")
    for K, ell, i in [(5, 3, 0), (5, 3, 3), (6, 3, 0), (6, 3, 3)]:
        A = alphabet(K, ell, i)
        outs = set(range(K)) - set(range(ell))
        avoid = [sorted(P) for P in A if not (P & outs)]
        print(f"{K:2d} {ell:3d} {i:2d} {len(A):4d} {tr6(A):7d} {str(sorted(outs)):>10s}  "
              f"{avoid}")
    print()
    print("reading:")
    print("  k=5, i in the triangle : every palette meets the outside PAIR {3,4}")
    print("      -> binary centre for {3,4} a.e. -> Lemma 5.5 (paper, section 6.3).")
    print("  k=5, i outside         : the four palettes {4},{0,4},{1,4},{2,4} are pairwise")
    print("      non-disjoint, so (T) admits no 6-tuple: the case is refuted outright.")
    print("  k=6, i outside         : {0,1,2} alone avoids the outsider set -> no binary centre.")
    print("  k=6, i in the triangle : palettes meet the outsider TRIPLE, which is not binary.")


if __name__ == "__main__":
    main()
