"""D4: proposed mechanism A_n -> D_n, plus honest machine verdict.

THE MECHANISM ("level framework").  Every weight-preserving bijection
Phi: A_n -> D_n that is *level compatible* (i.e. the number of parts of
Phi(alpha) depends only on alpha) factors as

  (F1)  lev : A_n -> {0,1,...,floor(sqrt n)}     [THE GUESSED COMPONENT]
  (F2)  fiber_k := lev^{-1}(k)  <-->  { nu : parts(nu) <= k, |nu| = n-k^2 }
        (canonical choice: lexicographic rank matching; invertible, no trace)
  (F3)  nu |--> staircase(conjugate(nu))  i.e. mu := nu' (parts<=k <=> len(mu)<=k),
        lambda_i = mu_i + 2(k-i)+1   -- the given staircase map, PROVED.

The inverse reads k off the D-side as its number of parts, recovers mu and nu,
then un-ranks nu inside the fiber.  No trace is stored.
Preserved invariant: weight n.  Terminating measure: k^2 (strictly increases
along the staircase peel; k^2 <= n bounds it).  Guessed part: F1 only.

We machine-check:
  (a) the staircase/T laws and the identity |D_n| = sum_k p_{<=k}(n-k^2);
  (b) the framework end-to-end, using a witness lev built to be correct;
  (c) whether three *natural* candidate lev survive the necessary condition
      |fiber_k| = p_{<=k}(n-k^2)  for all n <= NLIM.
"""
from itertools import islice
from explore import (enum_A, enum_D, level_counts, staircase, staircase_inv,
                     shiftT, p_atmost)

NLIM = 14

# ---- target sets: nu with parts <= k, |nu| = n-k^2 -------------------------
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

# ---- candidate level functions (all guessed) ------------------------------
CAND = {
 "lev_carrier  (#parts = 4 mod 5)": lambda a: sum(1 for p in a if p % 5 == 4),
 "lev_len      (number of parts)":  lambda a: len(a),
 "lev_len_cap  min(len, floor sqrt n)":
     lambda a: min(len(a), int(len(a) and __import__('math').isqrt(sum(a)))),
}

def fiber_check(lev, n):
    a = enum_A(n)
    lev_c = level_counts(n)
    got = {}
    for x in a:
        got[lev(x)] = got.get(lev(x), 0) + 1
    want = {k: v for k, v in lev_c.items() if v}
    # for n>0 level 0 must be empty
    if n > 0 and got.get(0, 0):
        return False, ("level 0 nonempty", sorted(x for x in a if lev(x) == 0)[:1])
    got = {k: v for k, v in got.items() if v}
    return got == want, (got, want)

# ---- the framework, with a *witness* level function that is correct --------
def witness_bijection(n):
    """Build (Phi, rank data) using the canonical lex-rank matching, and verify
    Phi: A_n -> D_n is a weight-preserving bijection whose D-side inverse
    recovers alpha without storing a trace."""
    A = sorted(enum_A(n))
    D = sorted(enum_D(n))
    assert len(A) == len(D)
    return dict(zip(A, D)), dict(zip(D, A))

def framework_bijection(n, lev):
    """Full mechanism for a lev whose fibers have the required sizes."""
    A = sorted(enum_A(n))
    fibers = {}
    for x in A:
        fibers.setdefault(lev(x), []).append(x)
    lev_c = level_counts(n)
    Phi = {}
    for k, fib in fibers.items():
        T = sorted(targets(k, n - k * k))
        assert len(fib) == len(T) == lev_c[k], (n, k, len(fib), len(T))
        fib.sort(); T.sort()
        for alpha, nu in zip(fib, T):
            mu = tuple(list(conj(nu)) + [0] * (k - len(conj(nu))))  # length EXACTLY k
            assert len(mu) == k and sum(mu) == n - k * k
            Phi[alpha] = staircase_inv(k, mu)  # the given staircase map
    # inverse, from the D-side alone
    inv = {}
    order = {}
    for k in fibers: order[k] = sorted(fibers[k])
    for alpha, lam in Phi.items():
        k = len(lam)
        mu = staircase(lam)
        nu = conj(mu)
        rank = sorted(targets(k, n - k * k)).index(nu)
        inv[lam] = order[k][rank]
    return Phi, inv

if __name__ == "__main__":
    import math
    print("(a) staircase / T laws and |D_n| = sum_k p_{<=k}(n-k^2): checked in explore.py, PASS n<=18,22")
    # (b) F2+F3 end-to-end with a level function that is CORRECT by construction
    #     (lev read off the canonical lex-rank bijection).  This tests the parts of
    #     the mechanism that are supposed to be provable: targets(k,n-k^2), the
    #     conjugate step, staircase_inv, and the trace-free inverse.
    import math
    okall = True
    for n in range(NLIM + 1):
        A = sorted(enum_A(n)); D = sorted(enum_D(n))
        assert len(A) == len(D), n
        rank_lev = {a: len(d) for a, d in zip(A, D)}   # witness lev
        Phi, inv = framework_bijection(n, lambda x, rl=rank_lev: rl[x])
        assert len(Phi) == len(inv) == len(A) == len(D), n
        assert sorted(Phi.keys()) == A and sorted(Phi.values()) == D, n
        for a, l in Phi.items():
            assert sum(a) == n == sum(l), (n, a, l)
            assert all(l[i] >= l[i+1] + 2 for i in range(len(l)-1)), (n, l)
            assert inv[l] == a, (n, a, l)
        # fibre sizes really are d(n,k)
        got = {}
        for a in Phi:
            got[len(Phi[a])] = got.get(len(Phi[a]), 0) + 1
        want = {k: v for k, v in level_counts(n).items() if v}
        assert got == want, (n, got, want)
        okall &= True
    print("(b) F2+F3 end-to-end (correct-by-construction lev, trace-free inverse): PASS n<=%d" % NLIM)

    print("\n(c) natural candidate level functions: necessary condition")
    print("    |fiber_k| = p_{<=k}(n-k^2) for every k, level 0 empty for n>0")
    for name, lev in CAND.items():
        firstbad = None
        for n in range(NLIM + 1):
            ok, wit = fiber_check(lev, n)
            if not ok:
                firstbad = (n, wit); break
        if firstbad is None:
            print(f"    {name:44s} SURVIVES n<={NLIM}")
        else:
            n, wit = firstbad
            print(f"    {name:44s} FAILS first at n={n}: {wit}")
    # demonstrate on n=5,6 in detail
    for n in (5, 6):
        print(f"\n    n={n}: required level sizes {dict(sorted(level_counts(n).items()))}")
        A = enum_A(n)
        for name, lev in CAND.items():
            got = {}
            for x in A: got[lev(x)] = got.get(lev(x), 0) + 1
            print(f"      {name:42s} gives {dict(sorted(got.items()))}")
