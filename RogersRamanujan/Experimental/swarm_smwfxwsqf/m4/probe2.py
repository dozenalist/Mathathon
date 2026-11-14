"""D4 probe, fair version.

Question: is the D-side staircase level k (#parts of the D-partition, with
d(n,k) = p_{<=k}(n-k^2) elements of D_n at level k) a function of some simple
statistic f of the A-partition?  lev = g o f  iff the level sizes d(n,1..)
can be obtained by MERGING the value-classes of f.  We test that exactly
(small DFS over which classes merge into which level) for n <= NMAX.
"""
from itertools import product
from collections import Counter
from explore import enum_A, level_counts, NMAX
from probe import STATS

NMAX = 14

def can_merge(class_sizes, level_sizes, tie=None):
    """partition the multiset class_sizes into |level_sizes| groups with the
    given sums; return one such grouping or None."""
    cs = sorted(class_sizes, reverse=True)
    ls = list(level_sizes)
    n = len(cs)
    groups = [[] for _ in ls]
    def dfs(i, rem):
        if i == n:
            return [] if all(r == 0 for r in rem) else None
        for j in range(len(ls)):
            if rem[j] >= cs[i]:
                rem[j] -= cs[i]
                r = dfs(i + 1, rem)
                if r is not None:
                    rem[j] += cs[i]
                    return [(j, cs[i])] + r
                rem[j] += cs[i]
        return None
    return dfs(0, list(ls))

def main():
    res = {}
    for n in range(NMAX + 1):
        a = enum_A(n)
        lev = level_counts(n)
        lv = [lev[k] for k in sorted(lev) if lev[k] > 0] if n > 0 else [1]
        for name, f in STATS.items():
            c = Counter(f(x) for x in a)
            sizes = [v for v in c.values() if v > 0]
            ok = can_merge(sizes, lv) is not None
            if name not in res:
                res[name] = [n, None]
            if ok:
                res[name][0] = n           # last n that worked
            elif res[name][1] is None and n > 0:
                res[name][1] = n           # first n where it broke
    print("statistic                  last n<=%d OK   first n where lev cannot be a function of it" % NMAX)
    for name in STATS:
        last, bad = res[name]
        print(f"  {name:26s} {last:6d}        {bad}")
    print()
    print("survivors (OK for all n<=%d): %s" % (NMAX, [m for m in STATS if res[m][1] is None]))

    # explicit n=6 worked example of the merge failure
    for nn in (4, 6, 8):
        a = enum_A(nn); lev = level_counts(nn)
        lv = [lev[k] for k in sorted(lev) if lev[k] > 0]
        print(f"\nn={nn}: |A_n|={len(a)}, level sizes (k>=1, k^2<=n) = {lv}")
        for name in ("len", "nparts_eq4", "max", "durfee"):
            c = Counter(STATS[name](x) for x in a)
            print(f"   {name:14s} classes {dict(sorted(c.items()))}  mergeable={can_merge(list(c.values()), lv) is not None}")

if __name__ == "__main__":
    main()
