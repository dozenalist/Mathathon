"""Worked examples n = 0..8 for the D4 mechanism:
the PROVABLE half (staircase/T) in full, and the required size of each level
fiber (the guessed half)."""
from explore import enum_A, enum_D, level_counts, staircase, shiftT

def targets(k, w):
    out = []
    def rec(rem, mx, cur):
        if rem == 0: out.append(tuple(cur)); return
        p = min(rem, mx)
        while p >= 1:
            cur.append(p); rec(rem - p, p, cur); cur.pop(); p -= 1
    if w == 0: return [()]
    rec(w, k, [])
    return out
def conj(nu):
    if not nu: return ()
    return tuple(sum(1 for x in nu if x >= i) for i in range(1, nu[0] + 1))

for n in range(9):
    A = enum_A(n); D = enum_D(n); L = level_counts(n)
    print(f"n={n}: |A_n|={len(A)}  |D_n|={len(D)}  required fiber sizes (lev=k) = "
          + str({k: v for k, v in sorted(L.items()) if v}))
    print(f"   A_n = {A}")
    for lam in sorted(D, reverse=True):
        k = len(lam); mu = staircase(lam); nu = conj(mu)
        assert sorted(nu, reverse=True) == list(nu) and (not nu or max(nu) <= k)
        assert sum(mu) == n - k*k, (lam, mu, n, k)
        print(f"   D {str(lam):16s} -> k={k}, mu={mu} (= conjugate of nu={nu}), "
              f"nu is a partition of {n-k*k} with parts <= {k};  T(lam)={shiftT(lam)}")
    print()
