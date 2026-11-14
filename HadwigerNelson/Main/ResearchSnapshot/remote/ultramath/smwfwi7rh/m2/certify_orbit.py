"""Certificate for the single-centre R-orbit tables at k = 6 (audit of sprint/k6).

Three independent procedures, all exact integer arithmetic:
  (A) DFS over admissible palettes with incremental checks (the sprint's full list).
  (B) brute force over the whole 16^6 / 22^6 ... tuple space, numpy, no pruning
      (only used where the alphabet is small enough).
  (C) transfer matrix:  #words = tr(A^6),  A = disjointness matrix of the alphabet.

The point of the certificate is Theorem R of AUDIT.md:

  at k = 6 the seven constraint groups used by the sprint reduce to
      (PB) 1 <= |P| <= 3,  (EDG) P not contained in a cycle edge,  (SA) c(x) not in P,
      (T)  consecutive palettes disjoint,
  because (SIN), (SA2), (C1), (C2), (MON) are theorems given (PB)+(EDG)+(SA)+(T).

Hence the four counts are exactly tr(A^6) and nothing else.

Run:  python3 certify_orbit.py
"""
from itertools import combinations
from collections import Counter

K = 6
N = 6                                    # number of R-orbit positions


def alphabet(ell, i, size_max=3):
    """(PB) + (EDG) + (SA): nonempty subsets of [K]\\{i}, size <= size_max,
    not contained in a cycle edge {v, v+1 mod ell}."""
    out = []
    for r in range(1, size_max + 1):
        for c in combinations([x for x in range(K) if x != i], r):
            P = frozenset(c)
            if any(P <= {v, (v + 1) % ell} for v in range(ell)):
                continue
            out.append(P)
    return sorted(out, key=lambda s: (len(s), sorted(s)))


# ---------------------------------------------------------------- (A) DFS
def words_dfs(ell, i, extra=True):
    """extra=True: also impose (SIN), (SA2), (C1), (C2), (MON) -- the sprint's list."""
    V = set(range(ell))
    A = alphabet(ell, i)
    res = []
    def ok_trans(a, b):
        if a & b:
            return False
        if extra and len(a) == 3 and len(b) > 2:            # SA2
            return False
        if extra and len(b) == 1 and next(iter(b)) in V:     # SIN
            return False
        return True
    def ok_word(w):
        if not extra:
            return True
        if sum(1 for P in w if len(P) == 3) > 3:             # C2
            return False
        for j in range(N):
            for l in range(j + 1, N):
                a, b = w[j], w[l]
                if len(a) == 3 and len(b) == 3 and not (a & b):   # C1
                    return False
        for j in range(N):
            a, b = w[j], w[(j + 2) % N]
            if a.isdisjoint(b) and len(a) + len(b) == 5:          # MON
                return False
        return True
    def rec(p):
        if len(p) == N:
            if ok_trans(p[-1], p[0]) and ok_word(tuple(p)):
                res.append(tuple(p))
            return
        for b in A:
            if p and not ok_trans(p[-1], b):
                continue
            rec(p + [b])
    for a in A:
        rec([a])
    return A, res


# ------------------------------------------------------ (B) brute force
def count_bruteforce(ell, i):
    import numpy as np
    A = alphabet(ell, i)
    m = len(A)
    assert m ** N <= 4 * 10 ** 8, (m, N)
    dis = np.zeros((m, m), dtype=bool)
    for a in range(m):
        for b in range(m):
            dis[a, b] = not (A[a] & A[b])
    idx = np.indices((m,) * N, dtype=np.int8).reshape(N, -1)
    good = np.ones(idx.shape[1], dtype=bool)
    for j in range(N):
        good &= dis[idx[j], idx[(j + 1) % N]]
    return int(good.sum())


# --------------------------------------------------- (C) transfer matrix
def count_transfer(ell, i):
    A = alphabet(ell, i)
    m = len(A)
    M = [[0] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            M[a][b] = 0 if (A[a] & A[b]) else 1
    def mul(X, Y):
        return [[sum(X[r][t] * Y[t][c] for t in range(m)) for c in range(m)]
                for r in range(m)]
    P = [row[:] for row in M]
    for _ in range(N - 1):                     # M, M^2, ..., M^N
        P = mul(P, M)
    return sum(P[a][a] for a in range(m))


ROWS = [(3, True), (3, False), (4, True), (4, False), (5, True), (5, False), (6, True)]
SPRINT = {("3in"): 70194, "3out": 11888, "4in": 18746, "4out": 2164,
          "5in": 3720, "5out": 380, "6in": 510}


def main():
    print("Theorem R certificate: the k=6 orbit tables are exactly tr(A^6).\n")
    print(f"{'row':10s} {'|A|':>4s} {'DFS(full)':>10s} {'DFS(reduced)':>13s} "
          f"{'tr(A^6)':>8s} {'brute':>9s} {'sprint':>7s}")
    allok = True
    for ell, i_in in ROWS:
        i = 0 if i_in else ell
        key = f"{ell}{'in' if i_in else 'out'}"
        A, full = words_dfs(ell, i, extra=True)
        _, red = words_dfs(ell, i, extra=False)
        tr = count_transfer(ell, i)
        bf = count_bruteforce(ell, i) if len(A) ** N <= BRUTE_LIMIT else -1
        ok = (len(full) == len(red) == tr == SPRINT[key]) and (bf in (-1, tr))
        allok &= ok
        print(f"{key:10s} {len(A):4d} {len(full):10d} {len(red):13d} {tr:8d} "
              f"{(bf if bf >= 0 else 'skip'):>9} {SPRINT[key]:7d}   {'OK' if ok else 'MISMATCH'}")
    print("\nall rows agree:", allok)
    print("(brute force runs whenever |A|^6 <= %d, i.e. for every row above)" % BRUTE_LIMIT)

    # decomposition of the ell=6 row (report section 6 quotes these)
    _, res = words_dfs(6, 0, extra=True)
    cnt = Counter(sum(1 for P in w if len(P) == 3) for w in res)
    print("\nell=6 words by number of ternary palettes:", dict(sorted(cnt.items())),
          " total", sum(cnt.values()))
    pat = Counter(tuple(len(P) for P in w) for w in res)
    print("  pattern (2,2,2,2,2,2):", pat[(2, 2, 2, 2, 2, 2)])
    print("  pattern (3,2,3,2,3,2):", pat[(3, 2, 3, 2, 3, 2)])
    print("  pattern (2,3,2,3,2,3):", pat[(2, 3, 2, 3, 2, 3)])
    print("  words with one or two ternary palettes:", cnt[1] + cnt[2])


# ------------------------------------------------------------- ablation
BRUTE_LIMIT = 2 * 10 ** 8


def ablate():
    """Drop one constraint group (or tighten the palette bound) and recount, DFS only."""
    import certify_orbit as me
    drops = ["none", "EDG", "SIN", "C1", "C2", "MON", "SA2", "size<=2"]
    print("\nper-constraint ablation (DFS; 'size<=2' tightens (PB) to |P| <= 2)")
    print(f"{'drop':8s} " + " ".join(f"{s:>7s}" for s in
                                     ["3in", "3out", "4in", "4out", "5in", "5out", "6in"]))
    for d in drops:
        vals = []
        for ell, i_in in ROWS:
            i = 0 if i_in else ell
            V = set(range(ell))
            A = []
            for r in range(1, 3 if d == "size<=2" else 4):
                for c in combinations([x for x in range(K) if x != i], r):
                    P = frozenset(c)
                    if d != "EDG" and any(P <= {v, (v + 1) % ell} for v in range(ell)):
                        continue
                    A.append(P)
            A = sorted(set(A), key=lambda s: (len(s), sorted(s)))
            cnt = 0
            def rec(p):
                nonlocal cnt
                if len(p) == N:
                    w = p
                    for j in range(N):
                        if w[j] & w[(j + 1) % N]:
                            return
                    if d == "C1":
                        for a in range(N):
                            for b in range(a + 1, N):
                                if len(w[a]) == 3 and len(w[b]) == 3 and not (w[a] & w[b]):
                                    return
                    if d == "C2" and sum(1 for P in w if len(P) == 3) > 3:
                        return
                    if d == "MON":
                        for j in range(N):
                            u_, v_ = w[j], w[(j + 2) % N]
                            if u_.isdisjoint(v_) and len(u_) + len(v_) == 5:
                                return
                    if d == "SA2":
                        for j in range(N):
                            if len(w[j]) == 3 and len(w[(j + 1) % N]) > 2:
                                return
                    if d == "SIN":
                        for j in range(N):
                            if len(w[j]) == 1 and next(iter(w[j])) in V:
                                return
                    cnt += 1
                    return
                for b in A:
                    if p and (p[-1] & b):
                        continue
                    rec(p + [b])
            for a in A:
                rec([a])
            vals.append(cnt)
        print(f"{d:8s} " + " ".join(f"{v:7d}" for v in vals))


if __name__ == "__main__":
    main()
    ablate()
