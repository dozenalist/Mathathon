#!/usr/bin/env python3
"""
d2: §8 at k=6, cycle length ell=5.

Combinatorial core.  At a cyclic centre x carrying an interface ell-cycle, Lemma 8.1 of the
paper gives, for a.e. direction e outside the finite set B of directions perpendicular to some
v_j, two allowed label sets

    I(e) = { i : both incident edges of the cycle at label i have sign + }  ∪  outsiders
    O(e) = { i : both incident edges of the cycle at label i have sign - }  ∪  outsiders

and requires   P_x(e) ∩ I(e) /= {}   and   P_x(e) ∩ O(e) /= {}   for a.e. e.

Signs only change at the 2*ell directions perp to v_j, so the sign pattern (a subset
Q of Z/ell = the set of positive edges) is piecewise constant; the pattern at a direction e is
Q(e) = { j : e . v_j > 0 } which equals { j : phi_j in (theta, theta+pi) } for phi_j = arg(v_j)+pi/2.

R = rotation by pi/3 = 60 degrees, and (5.7) is  P_x(e) ∩ P_x(Re) = {}  a.e.   (Corollary 5.4).

Two decisions:
  (I)  k = 5, ell = 5  -- calibration: must reproduce Proposition 8.2 (UNSAT, geometry-free).
  (II) k = 6, ell = 5  -- the case at issue: palettes bounded by the k=6 palette bound |P| <= 3.

Geometric reduction: 6 sample directions theta, theta+60, ..., theta+300 with theta generic
WLOG theta = 0 (rotate).  Each phi_j lies in one of the six open 60-degree gaps; only the gap
matters for the six sampled patterns.  Positive set at sample m = { j : gap(j) in {m,m+1,m+2} }.
So the realizable data is a function gap : {0..4} -> Z/6  (6**5 = 7776 of them).
"""
import itertools
import sys

# ---------------------------------------------------------------- basic pattern utilities

def runs(Q, ell):
    """cyclic runs of the bit string Q (subset of Z/ell) in index order 0,1,...,ell-1.
    Returns list of (sign, length) with sign 1 for a + edge (in Q), 0 for a - edge."""
    b = [1 if (i % ell) in Q else 0 for i in range(ell)]
    if all(x == b[0] for x in b):
        return [(b[0], ell)]
    # find a rotation start where the value changes
    s = 0
    while b[s] == b[s - 1]:
        s += 1
    out = []
    i = s
    cnt = 0
    cur = b[s]
    for t in range(ell):
        idx = (s + t) % ell
        if b[idx] == cur:
            cnt += 1
        else:
            out.append((cur, cnt))
            cur = b[idx]
            cnt = 1
    out.append((cur, cnt))
    return out


def internal(Q, ell, sign):
    """labels i of the cycle Z/ell with BOTH incident edges (i-1,i) and (i,i+1) equal to `sign`."""
    return frozenset(i % ell for i in range(ell)
                     if ((i - 1) % ell in Q) == bool(sign) and ((i) % ell in Q) == bool(sign))


def allowed(Q, ell, k):
    """(I, O) per Lemma 8.1: internal + vertices plus outsiders, internal - vertices plus outsiders."""
    outs = frozenset(range(ell, k))
    return internal(Q, ell, 1) | outs, internal(Q, ell, 0) | outs


# ---------------------------------------------------------------- geometry: gaps -> patterns

def patterns_from_gaps(gap, ell, nsamp=6):
    """gap: tuple of length ell, gap[j] in Z/nsamp = the open gap containing phi_j.
    Positive set at sample m = { j : gap[j] in {m, m+1, m+2} mod nsamp }."""
    out = []
    for m in range(nsamp):
        Q = frozenset(j for j in range(ell) if (gap[j] - m) % nsamp in (0, 1, 2))
        out.append(Q)
    return tuple(out)


def all_geometries(ell, nsamp=6):
    """distinct realizable 6-tuples of sign patterns."""
    seen = {}
    for gap in itertools.product(range(nsamp), repeat=ell):
        pt = patterns_from_gaps(gap, ell, nsamp)
        if pt not in seen:
            seen[pt] = gap
    return seen


# ---------------------------------------------------------------- palette CSP

def admissible(Q, ell, k, b, forbidden=frozenset()):
    """all palettes P subset of [k], |P| <= b, P avoids `forbidden`, meeting I(Q) and O(Q)."""
    I, O = allowed(Q, ell, k)
    labels = [i for i in range(k) if i not in forbidden]
    res = []
    for sz in range(1, b + 1):
        for comb in itertools.combinations(labels, sz):
            P = frozenset(comb)
            if P & I and P & O:
                res.append(P)
    return res


def decide(patterns, ell, k, b, forbidden=frozenset(), require_strong=False):
    """SAT check: palettes P_0..P_5 with P_i admissible at patterns[i], consecutive (cyclic)
    disjoint.  require_strong=True additionally demands P_i meet I\\outs and O\\outs (valid when
    the centre's own colour is a forbidden label that is an outsider, see the write-up)."""
    n = len(patterns)
    for Q in patterns:
        I, O = allowed(Q, ell, k)
        outs = frozenset(range(ell, k))
        if require_strong:
            if not (I - outs) or not (O - outs):
                return None
        else:
            if not I or not O:
                return None
    adm = []
    for Q in patterns:
        I, O = allowed(Q, ell, k)
        outs = frozenset(range(ell, k))
        labels = [i for i in range(k) if i not in forbidden]
        opts = []
        for sz in range(1, b + 1):
            for comb in itertools.combinations(labels, sz):
                P = frozenset(comb)
                if not (P & I and P & O):
                    continue
                if require_strong and not (P & (I - outs) and P & (O - outs)):
                    continue
                opts.append(P)
        adm.append(opts)

    sol = []

    def dfs(i, prev):
        if i == n:
            return sol[0] & sol[n - 1] == frozenset() if False else (sol[0] & sol[-1] == frozenset())
        for P in adm[i]:
            if prev is not None and (P & prev):
                continue
            sol.append(P)
            if dfs(i + 1, P):
                return True
            sol.pop()
        return False

    if dfs(0, None):
        return tuple(sol)
    return None


# ---------------------------------------------------------------- driver

def run(k, ell, b, require_strong, calib=False, verbose=True):
    geos = all_geometries(ell)
    sat = []
    unsat = 0
    for pt, gap in geos.items():
        w = decide(pt, ell, k, b, forbidden=frozenset(), require_strong=require_strong)
        if w is None:
            unsat += 1
        else:
            sat.append((pt, gap, w))
    if verbose:
        print(f"k={k} ell={ell} b={b} strong={require_strong}: geometries={len(geos)}  "
              f"UNSAT={unsat}  SAT={len(sat)}")
    return sat, unsat, len(geos)


if __name__ == "__main__":
    print("== calibration k=5, ell=5, palette bound b = k-3 = 2 (Prop 5.6), no outsider ==")
    run(5, 5, 2, require_strong=False)
    print()
    print("== k=6, ell=5, palette bound b = k-3 = 3, outsider X=5 ==")
    for b in (1, 2, 3, 4, 5):
        run(6, 5, b, require_strong=False, verbose=True)
    print()
    print("== k=6, ell=5, strong form (centre colour = the outsider, so X not in P) ==")
    for b in (2, 3, 4, 5):
        run(6, 5, b, require_strong=True, verbose=True)
