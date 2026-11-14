"""Pointwise section-8 system at a cyclic centre.

At a cyclic centre x with a simple cycle of length ell on the labels 0..ell-1,
edge j joining j and j+1, section 8.1 of the paper fixes:

  sigma_j(e) = sign(e . v_j)                (v_j = limiting direction of K_j)
  O(e) = [k] minus the endpoints of every positive edge
  I(e) = [k] minus the endpoints of every negative edge
  (8.1):  P(e) cap O(e) != empty   and   P(e) cap I(e) != empty   (a.e. e not in B)

and, at any centre (paper Prop 5.6 at k=5, the same argument at k=6):
  (5.12)  1 <= |P(e)| <= k-3                                   (a.e.)
  (5.7)   P(e) cap P(Re) = empty                               (a.e.)
  (6.2)   P(e) not a subset of {j,j+1} for every edge j of the cycle

plus, at a *typical* centre of colour i (self-avoidance, Lemma 1 of STRUCTURE.md):
  (SA)    i not in P(e)                                        (a.e.)

sigma_j(e) is piecewise constant on the circle with jumps only where e | v_j, so
the whole pointwise system is constant on the cells of the arrangement and the
decision "does a palette 6-tuple exist at parameter e" is a finite CSP per cell.
"""

from fractions import Fraction as F
from itertools import combinations, product


def sgn_cos(x):
    """sign of cos(pi*x) for a Fraction x; 0 exactly at the jumps."""
    y = x % 2
    if y == F(1, 2) or y == F(3, 2):
        return 0
    return -1 if F(1, 2) < y < F(3, 2) else 1


NORB = 6          # R has order 6 whatever the cycle length is
STEP = F(1, 3)    # q is the direction angle in units of pi, so R adds pi/3


def pattern(q, rays, p, ell):
    """S = set of positive edges at the p-th point of the R-orbit of angle pi*q."""
    S = set()
    for j in range(ell):
        s = sgn_cos(q + STEP * p - rays[j])
        if s > 0:
            S.add(j)
        elif s == 0:
            return None          # degenerate direction: in B
    return frozenset(S)


def allowed_sets(S, ell, k):
    """(O, I) from the positive-edge set S.  O removes positive endpoints,
    I removes negative endpoints; labels outside the cycle are in both."""
    pos_ep, neg_ep = set(), set()
    for j in range(ell):
        a, b = j, (j + 1) % ell
        if j in S:
            pos_ep |= {a, b}
        else:
            neg_ep |= {a, b}
    O = frozenset(range(k)) - pos_ep
    I = frozenset(range(k)) - neg_ep
    return O, I


def codeg(O, I):
    return (O, I)


def palettes_for(oc, ell, k, sa_label, w2sup):
    """All palettes a.e. admissible at a point with allowed sets oc."""
    O, I = oc
    out = []
    for size in range(1, w2sup + 1):
        for P in combinations(range(k), size):
            P = frozenset(P)
            if P & O == frozenset() or P & I == frozenset():
                continue
            if sa_label in P:
                continue
            if any(P <= frozenset({j, (j + 1) % ell}) for j in range(ell)):
                continue
            out.append(P)
    return out


def csp_sat(domains):
    """6 (or ell) variables on a cycle with the single constraint
    P_p cap P_{p+1} = empty.  Plain backtracking, domains are small."""
    n = len(domains)
    if any(len(d) == 0 for d in domains):
        return None
    order = sorted(range(n), key=lambda p: len(domains[p]))
    assign = {}
    def bt(t):
        if t == n:
            return True
        p = order[t]
        for P in domains[p]:
            ok = True
            for d in (1, -1):
                qq = (p + d) % n
                if qq in assign and assign[qq] & P:
                    ok = False
                    break
            if ok:
                assign[p] = P
                if bt(t + 1):
                    return True
                del assign[p]
        return False
    if bt(0):
        return [assign[p] for p in range(n)]
    return None


def cells(rays, ell):
    """Cells of the arrangement, with the pattern tuple of each."""
    crit = set()
    for j in range(ell):
        for p in range(NORB):
            for s in (F(1, 2), F(-1, 2)):
                crit.add((rays[j] - STEP * p + s) % 2)
    crit = sorted(crit)
    out = []
    for a, b in zip(crit, crit[1:] + [crit[0] + 2]):
        mid = (a + b) / 2
        pats = tuple(pattern(mid, rays, p, ell) for p in range(NORB))
        out.append((a, b, pats))
    return out


def decide_config(rays, ell, k, w2sup):
    """Classify one ray configuration.

    Returns a dict with:
      'status'  : 'L81'   some cell has O or I empty (Lemma 8.1 alone forbids it)
                  'CSP'   some cell with O,I both nonempty has no palette tuple
                  'SURV'  every cell is satisfiable
      'witness' : the offending cell / a full solution for every cell
    """
    cs = cells(rays, ell)
    for a, b, pats in cs:
        if any(p is None for p in pats):
            raise RuntimeError("degenerate cell")
        ocs = tuple(allowed_sets(S, ell, k) for S in pats)
        if any(len(O) == 0 or len(I) == 0 for (O, I) in ocs):
            return dict(status='L81', cells=cs, witness=(a, b, pats, ocs))
        found = None
        for i in range(k):
            doms = [palettes_for(oc, ell, k, i, w2sup) for oc in ocs]
            sol = csp_sat(doms)
            if sol is not None:
                found = (i, sol)
                break
        if found is None:
            return dict(status='CSP', cells=cs, witness=(a, b, pats, ocs))
    return dict(status='SURV', cells=cs, witness=None)


def decide_config_csp_only(rays, ell, k, w2sup):
    """Ignoring Lemma 8.1's nonemptiness: is every cell's palette tuple SAT?"""
    cs = cells(rays, ell)
    for a, b, pats in cs:
        ocs = tuple(allowed_sets(S, ell, k) for S in pats)
        found = None
        for i in range(k):
            doms = [palettes_for(oc, ell, k, i, w2sup) for oc in ocs]
            sol = csp_sat(doms)
            if sol is not None:
                found = (i, sol)
                break
        if found is None:
            return dict(status='CSP', cells=cs, witness=(a, b, pats, ocs))
    return dict(status='SURV', cells=cs, witness=None)

