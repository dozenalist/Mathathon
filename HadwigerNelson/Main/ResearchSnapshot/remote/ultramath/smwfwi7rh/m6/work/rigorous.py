"""The rigorous per-cell system at a typical cyclic centre, k colours.

Only constraints that hold pointwise a.e. at the centre are used:

  (S14) P_p meets O_p and I_p                     Lemma 8.1, (8.1)
  (5.7) P_p cap P_{p+1} = empty                   Corollary 5.4
  (PB)  1 <= |P_p| <= k-3                         Prop 5.6 (at k colours)
  (E)   P_p is not a subset of an edge of the cycle   Lemma 6.2, (6.2)
  (SA)  i notin P_p, i = colour of the typical centre Lemma 1

Deliberately NOT used (and why):

  * P_p cup P_{p'} != [k] for the six orbit positions.  (5.2) holds for a.e. pairs
    (u,v) in S x S, but the six orbit positions of one base direction form a
    1-dimensional family, a null subset of S x S, so Fubini does not reach it.
    In the rigorous form -- no two positive-measure direction sets carry palettes
    whose union is [k] -- the constraint is automatically satisfied here, because
    (SA) puts every palette in the 5-set [k] \\ {i}, and two subsets of a 5-set
    cannot have union [k].
  * P_p cup P_{p+2} != [k] \\ {i}.  Same reason: the unit-sum family is a curve.
    The rigorous form needs the interior of U_A + U_B to meet the unit circle,
    which is a geometric condition on the arcs, not a cell-combinatorial one.
"""

from itertools import combinations
import s8
from rows import achievable

FULL = None


def dom(oc, ell, k, w2, sa):
    out = set()
    for P in s8.palettes_for(oc, ell, k, -1, w2):
        if sa in P:
            continue
        out.add(sum(1 << x for x in P))
    return sorted(out)


def solve(doms, k):
    full = (1 << k) - 1
    assign = {}

    def ok(p, m):
        for q, mq in assign.items():
            d = (q - p) % 6
            if d == 0 or d == 3:
                continue
            if d in (1, 5) and (m & mq):
                return False
        return True

    def bt(t):
        if t == 6:
            return True
        for m in doms[t]:
            if ok(t, m):
                assign[t] = m
                if bt(t + 1):
                    return True
                del assign[t]
        return False

    return bt(0)


def analyse(ell, k, w2, use_sa=True, verbose=True):
    cache = {}
    rows = list(achievable(ell))
    labels = list(range(k)) if use_sa else [None]
    stat = {}
    sat = set()
    for i in labels:
        for choice, S in rows:
            ocs = tuple(s8.allowed_sets(s, ell, k) for s in S)
            if any(not oc[0] or not oc[1] for oc in ocs):
                stat['L81'] = stat.get('L81', 0) + 1
                continue
            doms = []
            for oc in ocs:
                key = (frozenset(oc[0]), frozenset(oc[1]), i)
                if key not in cache:
                    cache[key] = dom(oc, ell, k, w2, i)
                doms.append(cache[key])
            ok = solve(doms, k)
            stat['OK' if ok else 'CSP'] = stat.get('OK' if ok else 'CSP', 0) + 1
            if ok:
                sat.add((i, choice))
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2} SA={use_sa}: {stat}; SAT (label,row) {len(sat)}")
    return sat, rows


def walk(ell, k, w2, use_sa=True, verbose=True):
    sat, rows = analyse(ell, k, w2, use_sa, verbose)
    S_of = dict(rows)
    memo = {}

    def is_sat(choice, i):
        key = (choice, i)
        if key in memo:
            return memo[key]
        S = S_of[choice]
        ocs = tuple(s8.allowed_sets(s, ell, k) for s in S)
        if any(not oc[0] or not oc[1] for oc in ocs):
            memo[key] = False
            return False
        memo[key] = solve([dom(oc, ell, k, w2, i) for oc in ocs], k)
        return memo[key]

    groups = {}
    for (i, c) in sat:
        groups.setdefault(i, []).append(c)
    from rows import intervals6
    orders = _weak_orders(ell)
    good = []
    for i, lst in groups.items():
        for c0 in lst:
            for order in orders:
                cur = list(c0)
                ok = True
                for _ in range(6):
                    for blk in order:
                        for j in blk:
                            cur[j] = (cur[j] + 1) % 6
                        if not is_sat(tuple(cur), i):
                            ok = False
                            break
                    if not ok:
                        break
                if ok and cur == list(c0):
                    good.append((i, c0, order))
    if verbose:
        print(f"   surviving configurations: {len(good)}")
    return sat, good


def _weak_orders(n):
    out = []

    def rec(rem, acc):
        if not rem:
            out.append(tuple(acc))
            return
        m = len(rem)
        for mask in range(1, 1 << m):
            blk = tuple(rem[t] for t in range(m) if mask >> t & 1)
            rest = tuple(rem[t] for t in range(m) if not (mask >> t & 1))
            acc.append(blk)
            rec(rest, acc)
            acc.pop()

    rec(tuple(range(n)), [])
    return out


if __name__ == '__main__':
    import sys
    ell, k, w2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    walk(ell, k, w2, True)
