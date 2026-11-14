#!/usr/bin/env python3
"""D1 EXACT ENUMERATION (SAIR RR127).

A_n = partitions of n, every part = 1 or 4 (mod 5)      (multiplicities allowed)
D_n = partitions of n with lambda_i >= lambda_{i+1} + 2 for all i

Four counts per n (two independent methods each, plus two extra cross-checks):
  A-direct : generate canonical descending tuples over allowed parts (size cap)
  A-dp     : unbounded coin change over allowed parts <= n
  D-direct : generate canonical descending tuples, gap >= 2, parts <= n
  D-dp     : d(n,m) = d(n,m-1) + d(n-m,m-2), d(0,m)=1,
             d(n,m)=0 for n<0 or (n>0 and m<0) or (n>0 and m<1)
  plus brute-force over ALL partitions of n (filter) as a third check,
  and the Rogers-Ramanujan identity |A_n| == |D_n|.
Stdlib only. Exact integer arithmetic.
"""
import time, json, sys
from functools import lru_cache

NMAX = 30

# ---------------------------------------------------------------- method (i)
def gen_A_direct(n):
    """All partitions of n into parts == 1 or 4 (mod 5), canonical descending tuples."""
    allowed = [p for p in range(n, 0, -1) if p % 5 in (1, 4)]
    out = []
    def rec(rem, i, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        if i >= len(allowed):
            return
        p = allowed[i]
        # take t copies of p, then only parts strictly smaller than p are allowed
        t = 0
        while t * p <= rem:
            if t:
                acc.append(p)
            rec(rem - t * p, i + 1, acc)
            t += 1
        del acc[len(acc) - (t - 1):]
    rec(n, 0, [])
    return out

def gen_D_direct(n):
    """All partitions of n with adjacent gaps >= 2, canonical descending tuples."""
    out = []
    def rec(rem, maxpart, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        hi = min(maxpart, rem)
        for p in range(hi, 0, -1):
            acc.append(p)
            rec(rem - p, p - 2, acc)
            acc.pop()
    rec(n, n, [])
    return out

# --------------------------------------------------------------- method (ii)
def dp_A(N):
    a = [0] * (N + 1)
    a[0] = 1
    for p in range(1, N + 1):
        if p % 5 in (1, 4):
            for v in range(p, N + 1):
                a[v] += a[v - p]
    return a

def _mk_d():
    @lru_cache(maxsize=None)
    def d(n, m):
        if n == 0:
            return 1               # the empty partition
        if n < 0:
            return 0
        if m < 1:
            return 0               # n > 0 and m < 1
        return d(n, m - 1) + d(n - m, m - 2)
    return d

def dp_D(N):
    d = _mk_d()
    return [d(n, n) for n in range(N + 1)]

# ------------------------------------------------- third check: brute force
def all_partitions(n):
    out = []
    def rec(rem, maxpart, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        for p in range(min(maxpart, rem), 0, -1):
            acc.append(p); rec(rem - p, p, acc); acc.pop()
    rec(n, n, [])
    return out

def in_A(lam):
    return all(p % 5 in (1, 4) for p in lam)

def in_D(lam):
    return all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1))

# ------------------------------------------------------------------- damage
def main():
    res = {"n": [], "A_direct": [], "A_dp": [], "A_bf": [],
           "D_direct": [], "D_dp": [], "D_bf": []}
    times = {}
    sets_A, sets_D = {}, {}

    t0 = time.perf_counter()
    for n in range(NMAX + 1):
        s = time.perf_counter()
        A = gen_A_direct(n); tA = time.perf_counter() - s
        s = time.perf_counter()
        D = gen_D_direct(n); tD = time.perf_counter() - s
        times.setdefault("direct", []).append(tA + tD)
        if n <= 6:
            sets_A[n] = [list(x) for x in A]
            sets_D[n] = [list(x) for x in D]
        res["n"].append(n)
        res["A_direct"].append(len(A))
        res["D_direct"].append(len(D))
        # canonicality / membership spot-check of generators
        assert all(in_A(x) for x in A) and all(sum(x) == n for x in A)
        assert all(in_D(x) for x in D) and all(sum(x) == n for x in D)
        assert len(set(A)) == len(A) and len(set(D)) == len(D)
    times["direct_total"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    a = dp_A(NMAX)
    times["dp_A"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    dd = dp_D(NMAX)
    times["dp_D"] = time.perf_counter() - t0
    res["A_dp"] = a
    res["D_dp"] = dd

    t0 = time.perf_counter()
    for n in range(NMAX + 1):
        P = all_partitions(n)
        res["A_bf"].append(sum(1 for x in P if in_A(x)))
        res["D_bf"].append(sum(1 for x in P if in_D(x)))
    times["brute_total"] = time.perf_counter() - t0
    times["p(n) for n<=30"] = [len(all_partitions(n)) for n in range(0, 8)]

    checks = {
        "A direct == A dp": res["A_direct"] == res["A_dp"],
        "D direct == D dp": res["D_direct"] == res["D_dp"],
        "A direct == A brute": res["A_direct"] == res["A_bf"],
        "D direct == D brute": res["D_direct"] == res["D_bf"],
        "|A_n| == |D_n| (RR)": res["A_direct"] == res["D_direct"],
    }
    # explicit boundary spot values of the D-recurrence the task flagged
    d = _mk_d()
    boundary = {"d(1,1)": d(1, 1), "d(2,1)": d(2, 1), "d(2,2)": d(2, 2),
                "d(0,0)": d(0, 0), "d(1,0)": d(1, 0), "d(3,1)": d(3, 1),
                "d(2,0)": d(2, 0), "d(0,-5)": d(0, -5)}
    fixtures = {"|A_2|": res["A_direct"][2], "|D_2|": res["D_direct"][2],
                "D_5": sets_D.get(5) or [list(x) for x in gen_D_direct(5)],
                "A_5": [list(x) for x in gen_A_direct(5)]}

    out = {"counts": res, "times_s": times, "checks": checks,
           "d_boundary": boundary, "fixtures": fixtures,
           "sets_A_n_le_6": sets_A, "sets_D_n_le_6": sets_D}
    with open("d1_counts.json", "w") as f:
        json.dump(out, f, indent=1)

    print(" n  |A_n| |D_n|  A_dp A_bf  D_dp D_bf")
    for i, n in enumerate(res["n"]):
        print(f"{n:2d} {res['A_direct'][i]:6d} {res['D_direct'][i]:6d}"
              f" {res['A_dp'][i]:5d} {res['A_bf'][i]:5d}"
              f" {res['D_dp'][i]:5d} {res['D_bf'][i]:5d}")
    print()
    for k, v in checks.items():
        print(f"CHECK {k}: {v}")
    print("d-boundary:", boundary)
    print("fixtures:", fixtures)
    print("times(s):", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in times.items()})
    print("counts_30:", " ".join(str(x) for x in res["A_direct"]))
    for n in range(7):
        print(f"A_{n} = {[tuple(x) for x in sets_A[n]]}")
        print(f"D_{n} = {[tuple(x) for x in sets_D[n]]}")
    assert all(checks.values()), "A CHECK FAILED"

if __name__ == "__main__":
    main()
