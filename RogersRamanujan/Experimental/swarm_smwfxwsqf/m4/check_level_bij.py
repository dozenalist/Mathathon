"""Sharper form of the given staircase reduction, machine checked for n<=20:
   D_n  <-->  { (k, nu) : nu a partition of n-k^2 with every part <= k }.
k is the number of parts of the D-partition; nu = conjugate(staircase(lam))."""
from explore import enum_D, staircase, level_counts
def conj(t):
    if not t: return ()
    return tuple(sum(1 for x in t if x >= i) for i in range(1, t[0] + 1))
bad = []
for n in range(21):
    seen = set()
    for lam in enum_D(n):
        k = len(lam); mu = staircase(lam); nu = conj(mu)
        ok = (len(mu) == k and sum(mu) == n - k*k and all(v >= 0 for v in mu)
              and all(1 <= p <= k for p in nu) and list(nu) == sorted(nu, reverse=True))
        if not ok: bad.append((n, lam, k, mu, nu))
        seen.add((k, nu))
    # every (k,nu) with nu parts<=k of n-k^2 is hit exactly once, and sizes agree
    tot = sum(level_counts(n).values())
    if len(seen) != len(enum_D(n)) or tot != len(enum_D(n)):
        bad.append(("count", n, len(seen), len(enum_D(n)), tot))
print("D_n <-> {(k,nu): parts(nu)<=k, |nu|=n-k^2}, k=#parts : n<=20",
      "PASS" if not bad else ("FAIL", bad[:3]))
print("level table d(n,k)=p_{<=k}(n-k^2) for n=0..20:")
for n in range(21):
    print("  n=%2d: %s" % (n, {k: v for k, v in sorted(level_counts(n).items()) if v}))
