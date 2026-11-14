"""Max size of a subset of an arc [0,2m) with no two elements differing by a value in
[m-K, m+K]  (the 'one arc' part of the 3-arc decomposition of Z_{6m}).

Exact DP over positions with a sliding bitmask of the last m+K positions.
"""
import sys


def arc_max(m, K):
    n = 2 * m
    W = m + K          # window of remembered positions
    lo, hi = m - K, m + K
    # dp[mask][j] = best count for positions < j with occupancy bitmask of last W positions
    cur = {0: 0}
    for j in range(n):
        nxt = {}
        for mask, val in cur.items():
            # option: leave j empty
            nm = (mask << 1) & ((1 << W) - 1)
            if nxt.get(nm, -1) < val:
                nxt[nm] = val
            # option: put j in, if no conflict with a previous point at distance in [lo,hi]
            ok = True
            for d in range(lo, hi + 1):
                if d > 0 and (mask >> (d - 1)) & 1:
                    ok = False
                    break
                if d == 0:
                    continue
            if ok:
                nm = ((mask << 1) | 1) & ((1 << W) - 1)
                if nxt.get(nm, -1) < val + 1:
                    nxt[nm] = val + 1
        cur = nxt
    return max(cur.values())


if __name__ == "__main__":
    print(" m   K   arc_max   m-K   m-K+1   m")
    for m in range(4, 19):
        for K in (max(1, m // 5), max(1, m // 5) + 1):
            if K >= m:
                continue
            a = arc_max(m, K)
            print(f"{m:3d} {K:3d} {a:7d}  {m-K:4d}  {m-K+1:5d}  {m:4d}")
