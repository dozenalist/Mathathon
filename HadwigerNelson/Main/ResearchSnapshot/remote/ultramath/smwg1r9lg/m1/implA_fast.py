"""Fast driver for implA: same model, memoised.  Exact integer arithmetic."""
from itertools import combinations
import implA


def rows_tuple(ch, ell, cache={}):
    key = (ch, ell)
    if key in cache:
        return cache[key]
    T = implA.intervals()
    S = tuple(frozenset(j for j in range(ell) if p in T[ch[j]]) for p in range(6))
    cache[key] = S
    return S


def sat_choices(ell, k, i, extras):
    """Choice vectors whose orbit tuple admits a word satisfying the system."""
    ocs_cache = {}
    sat_cache = {}
    dom_cache = {}
    out = set()
    N = 6 ** ell
    for idx in range(N):
        ch = []
        t = idx
        for _ in range(ell):
            ch.append(t % 6)
            t //= 6
        ch = tuple(ch)
        S = rows_tuple(ch, ell)
        trip = []
        dead = False
        for p in range(3):
            Sp = S[p]
            if Sp not in ocs_cache:
                ocs_cache[Sp] = implA.allowed_sets(Sp, ell, k)
            oc = ocs_cache[Sp]
            if not oc[0] or not oc[1]:
                dead = True
                break
            trip.append(oc)
        if dead:
            continue
        trip = tuple(trip)
        if trip not in sat_cache:
            # antipodal law: position p+3 has the pair (O_p, I_p) swapped
            ocs = tuple(trip) + tuple((b, a) for (a, b) in trip)
            doms = []
            for (a, b) in ocs:
                key = (a, b)
                if key not in dom_cache:
                    dom_cache[key] = implA.domain(a, b, ell, k, i)
                doms.append(dom_cache[key])
            sat_cache[trip] = implA.cell_sat(doms, i, k, ell, extras)
        if sat_cache[trip]:
            out.add(ch)
    return out


def survivors(ell, k, extras, verbose=False):
    orders = implA.weak_orders(ell)
    good = []
    satpairs = 0
    for i in range(k):
        ok = sat_choices(ell, k, i, extras)
        satpairs += len(ok)
        if verbose:
            print(f"  ell={ell} k={k} label={i} extras={sorted(extras)}: {len(ok)} choices")
        for c0 in ok:
            for order in orders:
                cur = list(c0)
                okk = True
                for _ in range(6):
                    for blk in order:
                        for j in blk:
                            cur[j] = (cur[j] + 1) % 6
                        if tuple(cur) not in ok:
                            okk = False
                            break
                    if not okk:
                        break
                if okk and tuple(cur) == c0:
                    good.append((i, c0, order))
    if verbose:
        print(f"ell={ell} k={k} extras={sorted(extras)}: (label,tuple) pairs {satpairs}, "
              f"surviving configurations {len(good)}")
    return good, satpairs


if __name__ == '__main__':
    import sys, time
    ell = int(sys.argv[1]); k = int(sys.argv[2])
    exs = sys.argv[3].split(',') if len(sys.argv) > 3 and sys.argv[3] else []
    t = time.time()
    survivors(ell, k, exs, verbose=True)
    print("time %.2fs" % (time.time() - t))
