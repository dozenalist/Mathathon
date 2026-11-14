#!/usr/bin/env python3
"""RR127 independent adversarial checker (X / Counterexamples).

Independence policy.  This file shares NO code with Computation/: it re-derives
the two enumerators, the staircase map, the shift T and the property suite from
the problem statement.  The candidate map under test (bz82.forward / .inverse) is
imported as a black box, because a checker of a map must call the map; every
*property* it asserts about that map is written here from scratch.

Run:  python3 RogersRamanujan/Counterexamples/checker.py [NMAX]
Exit status 0 iff every check passes.  Prints a machine-readable summary last.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.normpath(os.path.join(HERE, '..', 'Computation'))
sys.path.insert(0, COMP)

import bz82  # the candidate, black box

FAILS = []


def fail(kind, detail):
    FAILS.append({'kind': kind, 'detail': detail})


# ---------------------------------------------------------------- enumerators
def parts_of(n):
    """Every partition of n as a descending tuple.  Naive, exhaustive."""
    res = []

    def go(rem, cap, acc):
        if rem == 0:
            res.append(tuple(acc))
            return
        hi = cap if cap < rem else rem
        for v in range(hi, 0, -1):
            acc.append(v)
            go(rem - v, v, acc)
            acc.pop()

    go(n, n, [])
    return res


def A(n):
    return sorted([p for p in parts_of(n) if all(v % 5 in (1, 4) for v in p)],
                  reverse=True)


def D(n):
    return sorted([p for p in parts_of(n)
                   if all(p[i] - p[i + 1] >= 2 for i in range(len(p) - 1))],
                  reverse=True)


# ------------------------------------------------------------- own reductions
def stair(lam):
    k = len(lam)
    return tuple(lam[i] - (2 * (k - i - 1) + 1) for i in range(k))


def unstair(mu):
    k = len(mu)
    return tuple(mu[i] + (2 * (k - i - 1) + 1) for i in range(k))


def shiftT(lam):
    k = len(lam)
    return tuple(lam[i] - k + 2 * (i + 1) - 1 for i in range(k))


def shiftTinv(b):
    k = len(b)
    return tuple(b[i] + k - 2 * (i + 1) + 1 for i in range(k))


# ------------------------------------------------------------------- checks
def check_reductions(NMAX):
    for n in range(NMAX + 1):
        for lam in D(n):
            k = len(lam)
            mu = stair(lam)
            if len(mu) != k:
                fail('stair-length', [n, list(lam)])
            if any(m < 0 for m in mu):
                fail('stair-negative', [n, list(lam), list(mu)])
            if any(mu[i] < mu[i + 1] for i in range(k - 1)):
                fail('stair-order', [n, list(lam), list(mu)])
            if sum(mu) != n - k * k:
                fail('stair-weight', [n, list(lam), sum(mu), n - k * k])
            if unstair(mu) != lam:
                fail('stair-inverse', [n, list(lam)])
            b = shiftT(lam)
            if sum(b) != n:
                fail('T-weight', [n, list(lam)])
            if any(x < k for x in b):
                fail('T-smallest', [n, list(lam), list(b)])
            if shiftTinv(b) != lam:
                fail('T-inverse', [n, list(lam)])
            if any(b[i] != mu[i] + k for i in range(k)):
                fail('T-vs-stair', [n, list(lam)])


def check_map(NMAX):
    for n in range(NMAX + 1):
        a, d = A(n), D(n)
        if len(a) != len(d):
            fail('count-mismatch', [n, len(a), len(d)])
        fw = {}
        for p in a:
            try:
                q = bz82.forward(p)
            except Exception as exc:                    # noqa: BLE001
                fail('forward-raised', [n, list(p), repr(exc)])
                continue
            fw[p] = q
            if q not in set(d):
                fail('codomain', [n, list(p), list(q)])
            if sum(q) != n:
                fail('weight', [n, list(p), list(q), sum(q)])
            if bz82.forward(p) != q:
                fail('determinism', [n, list(p)])
        vals = list(fw.values())
        if len(set(vals)) != len(vals):
            fail('collision', [n])
        if set(vals) != set(d):
            fail('coverage', [n, sorted(set(d) - set(vals))[:3]])
        for q in d:
            try:
                p = bz82.inverse(q)
            except Exception as exc:                    # noqa: BLE001
                fail('inverse-raised', [n, list(q), repr(exc)])
                continue
            if p not in set(a):
                fail('inverse-codomain', [n, list(q), list(p)])
            if fw.get(p) != q:
                fail('inverse-right', [n, list(q), list(p)])
        for p in a:
            q = fw.get(p)
            if q is None:
                continue
            if bz82.inverse(q) != p:
                fail('inverse-left', [n, list(p), list(q)])


def check_regressions():
    """The fixtures and the degenerate families named in the assignment."""
    fixtures = {
        0: (((),), ((),)),
        2: (((1, 1),), ((2,),)),
    }
    for n, (fa, fd) in fixtures.items():
        if tuple(A(n)) != fa:
            fail('fixture-A', [n, [list(p) for p in A(n)]])
        if tuple(D(n)) != fd:
            fail('fixture-D', [n, [list(p) for p in D(n)]])
    if A(2) != [(1, 1)] or D(2) != [(2,)]:
        fail('n2-length-obstruction', [])
    # empty partition, all ones, single allowed part, odd staircase, large gap
    for probe in [(), (1,), (1, 1), (1,) * 12, (4,), (6,), (4, 4, 4),
                  (2,), (13,), (5, 3), (7, 3, 1), (9, 6, 4, 1)]:
        w = sum(probe)
        inA = all(v % 5 in (1, 4) for v in probe)
        inD = all(probe[i] - probe[i + 1] >= 2 for i in range(len(probe) - 1))
        try:
            if inA and inD:
                q = bz82.forward(probe)
                if bz82.inverse(q) != probe or sum(q) != w:
                    fail('probe-A-D', [list(probe)])
            elif inA:
                q = bz82.forward(probe)
                if sum(q) != w or bz82.inverse(q) != probe:
                    fail('probe-A', [list(probe)])
            elif inD:
                p = bz82.inverse(probe)
                if sum(p) != w or bz82.forward(p) != probe:
                    fail('probe-D', [list(probe)])
            else:
                try:
                    bz82.forward(probe)
                    fail('accepted-invalid-input', [list(probe)])
                except Exception:                       # noqa: BLE001
                    pass
        except Exception as exc:                        # noqa: BLE001
            fail('probe-raised', [list(probe), inA, inD, repr(exc)])


def check_obstructions(NMAX=14):
    """Statistics that no weight-preserving bijection can preserve, with witnesses."""
    out = {'largest_part': None, 'length': None, 'forced': []}
    for n in range(NMAX + 1):
        la = sorted([p[0] if p else 0 for p in A(n)])
        ld = sorted([p[0] if p else 0 for p in D(n)])
        if la != ld and out['largest_part'] is None:
            out['largest_part'] = {'n': n, 'A': la, 'D': ld}
        sa = sorted([len(p) for p in A(n)])
        sd = sorted([len(p) for p in D(n)])
        if sa != sd and out['length'] is None:
            out['length'] = {'n': n, 'A': sa, 'D': sd}
        lmax = {p[0] if p else 0 for p in D(n)}
        forced = [list(p) for p in A(n) if (p[0] if p else 0) not in lmax]
        if forced:
            out['forced'].append({'n': n, 'count': len(forced),
                                  'minimal_witness': forced[0]})
    return out


def check_cutoff():
    """The roadmap's warning: equal largest-part cutoffs are not an identity."""
    a = [p for p in A(5) if (p[0] if p else 0) <= 4]
    d = [p for p in D(5) if (p[0] if p else 0) <= 4]
    return {'n': 5, 'cutoff': 4, 'A': [list(p) for p in a], 'D': [list(p) for p in d],
            'equal': len(a) == len(d)}


def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    check_regressions()
    check_reductions(NMAX)
    check_map(NMAX)
    obs = check_obstructions()
    cut = check_cutoff()
    summary = {
        'nmax': NMAX,
        'fails': len(FAILS),
        'first_fails': FAILS[:10],
        'obstructions': obs,
        'cutoff_5_4': cut,
        'verdict': 'PASS' if not FAILS else 'FAIL',
    }
    print(json.dumps(summary, indent=1))
    return 0 if not FAILS else 1


if __name__ == '__main__':
    sys.exit(main())
