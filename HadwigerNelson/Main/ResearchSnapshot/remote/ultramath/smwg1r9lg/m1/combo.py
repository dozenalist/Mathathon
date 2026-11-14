"""The composed system COMBO(ell, k): decision driver (implementation A).

COMBO = per-cell §8 system at the cyclic centre x
        + hexagon (TE) cluster at the six unit neighbours x + R^j e
        + (T) at x  (the six rim colours lie in the six orbit palettes)
        + m7's circle-set constraint |P_j| + |C_j| <= k  (implied: Lemma N2)
        + m9's unit-triangle count                       (implied: Lemma N3)
        + m11's sigma{B subset P_x} <= 1/2               (implied: Lemma N1)

A configuration survives iff every cell of its closed slip cycle admits a word
which satisfies the per-cell system AND is rim-feasible.
"""
from itertools import combinations, product
import implA
import rim as RIM


def bits(mask, k):
    return [x for x in range(k) if (mask >> x) & 1]


def words_for(doms, i, k, ell, extras, need_rim):
    """First word satisfying the per-cell word system (and, if asked, rim-feasible)."""
    n = 6
    w = [0] * n
    order = sorted(range(n), key=lambda p: len(doms[p]))
    out = []

    def bt(t):
        if t == n:
            if not implA.word_ok(w, i, k, ell, extras):
                return False
            if need_rim and not RIM.rim_ok(tuple(w), i, k, ell):
                return False
            out.append(tuple(w))
            return True
        p = order[t]
        for m in doms[p]:
            good = True
            for d in (1, -1):
                q = (p + d) % n
                if q in order[:t] and (w[q] & m):
                    good = False
                    break
            if good:
                w[p] = m
                if bt(t + 1):
                    return True
        return False

    bt(0)
    return out


def decide(ell, k, extras=(), need_rim=True, verbose=False):
    """Return (survivors, info).  Info maps (label, triple) -> (sat?, first word)."""
    orders = implA.weak_orders(ell)
    T = implA.intervals()
    ocs_of_S = {}
    dom_cache = {}
    trip_cache = {}
    info = {}
    per_label = {}
    for i in range(k):
        ok = set()
        N = 6 ** ell
        for idx in range(N):
            ch = []
            t = idx
            for _ in range(ell):
                ch.append(t % 6)
                t //= 6
            ch = tuple(ch)
            S = tuple(frozenset(j for j in range(ell) if p in T[ch[j]]) for p in range(6))
            trip = []
            dead = False
            for p in range(3):
                Sp = S[p]
                if Sp not in ocs_of_S:
                    ocs_of_S[Sp] = implA.allowed_sets(Sp, ell, k)
                oc = ocs_of_S[Sp]
                if not oc[0] or not oc[1]:
                    dead = True
                    break
                trip.append(oc)
            if dead:
                continue
            trip = tuple(trip)
            key = (trip, i)
            if key not in trip_cache:
                ocs = trip + tuple((b, a) for (a, b) in trip)
                doms = []
                for (a, b) in ocs:
                    if (a, b, i) not in dom_cache:
                        dom_cache[(a, b, i)] = implA.domain(a, b, ell, k, i)
                    doms.append(dom_cache[(a, b, i)])
                ws = words_for(doms, i, k, ell, extras, need_rim)
                trip_cache[key] = ws[0] if ws else None
                info[key] = (bool(ws), ws[0] if ws else None, len(ws))
            if trip_cache[key] is not None:
                ok.add(ch)
        per_label[i] = ok
        if verbose:
            print(f"  ell={ell} k={k} extras={sorted(extras)} rim={need_rim} label={i}: "
                  f"{len(ok)} choices")
    good = []
    for i in range(k):
        ok = per_label[i]
        for c0 in ok:
            for order in orders:
                cur = list(c0)
                fine = True
                for _ in range(6):
                    for blk in order:
                        for j in blk:
                            cur[j] = (cur[j] - 1) % 6
                        if tuple(cur) not in ok:
                            fine = False
                            break
                    if not fine:
                        break
                if fine and tuple(cur) == c0:
                    good.append((i, c0, order))
    return good, info, per_label


if __name__ == '__main__':
    import sys, time
    ell = int(sys.argv[1]); k = int(sys.argv[2])
    ex = tuple(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else ()
    t = time.time()
    good, info, per_label = decide(ell, k, ex, need_rim=True, verbose=True)
    nsat = sum(1 for v in info.values() if v[0])
    print(f"ell={ell} k={k} extras={list(ex)}: per-cell SAT (label,triple) pairs {nsat}; "
          f"surviving configurations {len(good)}  [{time.time()-t:.1f}s]")
