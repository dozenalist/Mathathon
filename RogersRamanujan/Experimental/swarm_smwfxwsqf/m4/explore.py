"""RR127 / D4 scaffolding: exact enumeration of A_n and D_n, the given
reductions (staircase, shift T), and the level (=number of parts) decomposition
   |D_n| = sum_k p_{<=k}(n - k^2).
Pure integer arithmetic, stdlib only.
"""
from functools import lru_cache

NMAX = 22

# ---------------- direct enumeration of canonical descending tuples ----------
def enum_A(n):
    out = []
    cur = []
    def rec(rem, mx):
        if rem == 0:
            out.append(tuple(cur)); return
        p = min(rem, mx)
        while p >= 1:
            if p % 5 in (1, 4):
                cur.append(p); rec(rem - p, p); cur.pop()
            p -= 1
    rec(n, n)
    return out

def enum_D(n):
    out = []
    cur = []
    def rec(rem, mx):
        if rem == 0:
            out.append(tuple(cur)); return
        p = min(rem, mx)
        while p >= 1:
            cur.append(p); rec(rem - p, p - 2); cur.pop()
            p -= 1
    rec(n, n)
    return out

# ---------------- dynamic programming --------------------------------------
def dp_A(N):
    A = [0] * (N + 1); A[0] = 1
    for p in range(1, N + 1):
        if p % 5 in (1, 4):
            for m in range(p, N + 1):
                A[m] += A[m - p]
    return A

def dp_D(N):
    # D(n,m) = # partitions of n with gaps >= 2, all parts <= m
    # D(n,m) = D(n,m-1) + D(n-m,m-2);  D(0,m) = 1 ; D(n,m)=0 for n>0, m<1
    D = {}
    def get(n, m):
        if n == 0: return 1
        if n < 0 or m < 1: return 0
        key = (n, m)
        if key in D: return D[key]
        v = get(n, m - 1) + get(n - m, m - 2)
        D[key] = v
        return v
    return [get(n, n) for n in range(N + 1)]

@lru_cache(maxsize=None)
def p_atmost(k, w):
    """# partitions of w into at most k parts"""
    if w < 0: return 0
    if w == 0: return 1
    if k <= 0: return 0
    # partitions of w with parts <= k  (conjugate of at most k parts)
    tab = [0] * (w + 1); tab[0] = 1
    for p in range(1, k + 1):
        for m in range(p, w + 1):
            tab[m] += tab[m - p]
    return tab[w]

def level_counts(n):
    """dict k -> p_{<=k}(n-k^2) for k^2 <= n"""
    out = {}
    k = 0
    while k * k <= n:
        out[k] = p_atmost(k, n - k * k)
        k += 1
    return out

# ---------------- the two given bijections ---------------------------------
def staircase(lam):
    k = len(lam)
    return tuple(lam[i] - (2 * (k - i - 1) + 1) for i in range(k))

def staircase_inv(k, mu):
    assert len(mu) == k and all(v >= 0 for v in mu)
    return tuple(mu[i] + 2 * (k - i - 1) + 1 for i in range(k))

def shiftT(lam):
    k = len(lam)
    return tuple(lam[i] - k + 2 * i + 1 for i in range(k))

def shiftT_inv(b):
    k = len(b)
    return tuple(b[i] + k - 2 * i - 1 for i in range(k))

def weak_dec(t):
    return all(t[i] >= t[i + 1] for i in range(len(t) - 1))

# =============================== main =====================================
if __name__ == "__main__":
    import time, sys
    t0 = time.time()
    A = dp_A(NMAX); Dv = dp_D(NMAX)
    print("n : |A_n| |D_n|  equal?   sum_k p_{<=k}(n-k^2)")
    ok = True
    for n in range(NMAX + 1):
        s = sum(level_counts(n).values())
        e = (A[n] == Dv[n] == s)
        ok &= e
        print(f"{n:2d}: {A[n]:6d} {Dv[n]:6d}  {'YES' if (A[n]==Dv[n]) else 'NO '}   {s:6d}  {'YES' if e else 'NO'}")
    print("all equal:", ok)
    print("dp time %.3fs" % (time.time() - t0))

    # direct enumeration vs dp, and the two maps
    t0 = time.time()
    lim = 18
    for n in range(lim + 1):
        a = enum_A(n); d = enum_D(n)
        assert len(a) == A[n], (n, len(a), A[n])
        assert len(d) == Dv[n], (n, len(d), Dv[n])
        assert len(set(a)) == len(a) and len(set(d)) == len(d)
        for lam in d:
            assert all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1)), lam
            k = len(lam); mu = staircase(lam)
            assert len(mu) == k and weak_dec(mu) and all(v >= 0 for v in mu)
            assert sum(mu) == n - k * k
            assert staircase_inv(k, mu) == lam
            b = shiftT(lam)
            assert len(b) == k and weak_dec(b) and (k == 0 or b[-1] >= k)
            assert sum(b) == n and shiftT_inv(b) == lam
            # staircase and T commute through the (k,mu) picture
            assert tuple(mu[i] + k for i in range(k)) == b
        for al in a:
            assert all(p % 5 in (1, 4) for p in al) and sum(al) == n
    print("enumeration + staircase/T law checks n<=%d: PASS (%.3fs)" % (lim, time.time() - t0))

    # fixtures
    print("A_2", enum_A(2), "D_2", enum_D(2))
    print("A_5", enum_A(5), "D_5", enum_D(5))
    print("T(7,3,1) =", shiftT((7, 3, 1)))
    for n in range(7):
        print(f"  A_{n} = {enum_A(n)}")
        print(f"  D_{n} = {enum_D(n)}")
        print(f"  levels(n={n}) = {level_counts(n)}")
