"""Exhaustive sweep over ray configurations for the pointwise section-8 system."""

from fractions import Fraction as F
from itertools import product
import sys
import s8


def weak_cyclic_orders(n):
    """All weak cyclic orders of n labelled projective directions, realised exactly.

    A configuration is n rays v_j = e^{i pi r_j}.  Rotating all rays is a symmetry
    of the decision problem, so we normalise r_0 = 0.  Ties (r_i = r_j) mean the
    two rays coincide, so the weak order is a surjection [n] -> Z/m for some m.
    """
    seen = set()
    out = []
    for m in range(1, n + 1):
        for b in product(range(m), repeat=n):
            if b[0] != 0 or set(b) != set(range(m)):
                continue
            # canonical form up to rotation of Z/m: the block sequence read from 0
            key = tuple(b)
            if key in seen:
                continue
            seen.add(key)
            out.append(tuple(F(b[j], m) for j in range(n)))
    return out


_memo = {}


def csp_ok(pats, ell, k, w2sup):
    """Is there a palette tuple for this pattern tuple (common avoided label)?"""
    key = (pats, ell, k, w2sup)
    if key in _memo:
        return _memo[key]
    ocs = tuple(s8.allowed_sets(S, ell, k) for S in pats)
    if any(len(O) == 0 or len(I) == 0 for (O, I) in ocs):
        _memo[key] = ('L81', None)
        return _memo[key]
    for i in range(k):
        doms = [s8.palettes_for(oc, ell, k, i, w2sup) for oc in ocs]
        sol = s8.csp_sat(doms)
        if sol is not None:
            _memo[key] = ('OK', (i, sol))
            return _memo[key]
    _memo[key] = ('CSP', None)
    return _memo[key]


def sweep(ell, k, w2sup, verbose=True):
    worst = {}          # status -> count of configurations
    bad = None
    cfgcount = 0
    for rays in weak_cyclic_orders(ell):
        cfgcount += 1
        status = 'SURV'
        first = None
        for a, b, pats in s8.cells(rays, ell):
            st, sol = csp_ok(pats, ell, k, w2sup)
            if st != 'OK':
                status = st
                first = (float(a), float(b), [sorted(p) for p in pats])
                break
        worst[status] = worst.get(status, 0) + 1
        if status == 'SURV' and bad is None:
            bad = rays
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2sup}: {cfgcount} configurations")
        for st in ('L81', 'CSP', 'SURV'):
            if st in worst:
                print(f"   {st}: {worst[st]}")
    return worst, bad


if __name__ == '__main__':
    ell = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    w2 = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    worst, bad = sweep(ell, k, w2)
    if bad is not None:
        print("   SURVIVING CONFIGURATION:", bad)
