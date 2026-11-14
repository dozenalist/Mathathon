"""Implementation A: the composed single-centre orbit decision at k colours.

Geometry-free combinatorial model (row model): a configuration is a choice vector
ch in (Z/6)^ell (the index of the cyclic 3-interval carried by ray j) together
with a weak order of the slippage of the ell rays.  The orbit tuple is

    S_p = { j : p in T_{ch[j]} },   T_m = {m-1, m, m+1} subset Z/6,

and the antipodal law S_{p+3} = [ell] \\ S_p holds identically.

Per-cell system (paper's hypotheses, pointwise a.e. at the centre x):

  (S14)  P_p cap O_p != empty,  P_p cap I_p != empty          Lemma 8.1
  (PB)   1 <= |P_p| <= k-3                                     Prop 5.6
  (5.7)  P_p cap P_{p+1} = empty                               Cor 5.4
  (E)    P_p not a subset of an edge of C_ell                  Lemma 6.2
  (SA)   i not in P_p, i = colour of the (typical) centre      Lemma D

Word-level extras (each is a theorem; see NOTE.md for provenance):

  (L5)   m9 Lemma 5 (ternary rigidity):
         if no P_p is a singleton and |P_p| = 3 then
             P_{p+1} = [k] \\ (P_p cup {i})   and   P_{p+2} subset P_p
  (C1)   no two values of the word are complementary 3-sets      (5.2) on a product
  (MON)  no p with |P_p|+|P_{p+2}| = k-1, disjoint, both avoiding i   STRUCTURE L.6

Deliberately NOT word-level (they constrain other centres / the measure):
  m11 sigma{B subset P_x} <= 1/2   (implied by (5.7); see NOTE.md Lemma N1)
  m7  |P_x(e)| + |Col(S(x+e,1))| <= k  (implied by (PB) and |Col| >= 2; Lemma N2)
  m9  unit-triangle count          (pointwise implied by (TE); Lemma N3)

Everything is exact integer arithmetic.
"""
from itertools import combinations, product


def intervals():
    """The six cyclic 3-intervals of Z/6."""
    return [frozenset({(m - 1) % 6, m, (m + 1) % 6}) for m in range(6)]


def tuple_of_choice(ch, ell):
    """S_p = { j : p in T_{ch[j]} }."""
    T = intervals()
    return tuple(frozenset(j for j in range(ell) if p in T[ch[j]]) for p in range(6))


def allowed_sets(S, ell, k):
    """(O, I) of Lemma 8.1 from the positive-edge set S."""
    pos, neg = set(), set()
    for j in range(ell):
        e = {j, (j + 1) % ell}
        if j in S:
            pos |= e
        else:
            neg |= e
    return frozenset(range(k)) - pos, frozenset(range(k)) - neg


def bits(mask, k):
    return tuple(x for x in range(k) if (mask >> x) & 1)


def domain(O, I, ell, k, i):
    """All palettes admissible a.e. at a position with allowed sets (O, I)."""
    out = []
    full = (1 << k) - 1
    for size in range(1, min(3, k - 3) + 1):
        for c in combinations(range(k), size):
            m = 0
            for x in c:
                m |= 1 << x
            if not (set(c) & O):
                continue
            if not (set(c) & I):
                continue
            if i in c:
                continue
            if any(set(c) <= {j, (j + 1) % ell} for j in range(ell)):
                continue
            out.append(m)
    return out


def word_ok(w, i, k, ell, extras):
    """Word-level conditions, all of them theorems."""
    n = 6
    # (5.7) consecutive disjointness
    for p in range(n):
        if w[p] & w[(p + 1) % n]:
            return False
    if 'L5' in extras:
        nosin = all(bin(m).count('1') != 1 for m in w)
        if nosin:
            for p in range(n):
                if bin(w[p]).count('1') == 3:
                    want = ((1 << k) - 1) & ~(w[p] | (1 << i))
                    if w[(p + 1) % n] != want:
                        return False
                    if w[(p + 2) % n] & ~w[p]:
                        return False
    if 'C1' in extras:
        for a in w:
            for b in w:
                if bin(a).count('1') == 3 and bin(b).count('1') == 3 and not (a & b):
                    return False
    if 'MON' in extras:
        for p in range(n):
            a, b = w[p], w[(p + 2) % n]
            if not (a & b) and bin(a).count('1') + bin(b).count('1') == k - 1:
                if not (a >> i) & 1 and not (b >> i) & 1:
                    return False
    return True


def cell_sat(doms, i, k, ell, extras):
    """Is there a word with these per-position domains satisfying the word system?"""
    n = 6
    w = [0] * n
    order = sorted(range(n), key=lambda p: len(doms[p]))

    def bt(t):
        if t == n:
            return word_ok(w, i, k, ell, extras)
        p = order[t]
        for m in doms[p]:
            okk = True
            for d in (1, -1):
                q = (p + d) % n
                if q in order[:t] and (w[q] & m):
                    okk = False
                    break
            if okk:
                w[p] = m
                if bt(t + 1):
                    return True
        return False

    return bt(0)


def sat_choices(ell, k, i, extras, verbose=False):
    """All choice vectors whose orbit tuple is satisfiable at this label i."""
    N = 6 ** ell
    out = []
    cache = {}
    for idx in range(N):
        ch = []
        t = idx
        for _ in range(ell):
            ch.append(t % 6)
            t //= 6
        S = tuple_of_choice(ch, ell)
        ocs = tuple(allowed_sets(s, ell, k) for s in S)
        if any(not o[0] or not o[1] for o in ocs):
            continue                      # Lemma 8.1 alone
        key = ocs
        if key not in cache:
            # antipodal law: domain at p+3 is the domain at p with O,I swapped
            cache[key] = cell_sat([domain(o[0], o[1], ell, k, i) for o in ocs],
                                  i, k, ell, extras)
        if cache[key]:
            out.append(tuple(ch))
    if verbose:
        print(f"  ell={ell} k={k} label={i} extras={sorted(extras)}: "
              f"{len(out)} satisfiable (label, tuple) choices")
    return set(out)


def weak_orders(n):
    out = []

    def rec(rem, acc):
        if not rem:
            out.append(tuple(acc))
            return
        m = len(rem)
        for mask in range(1, 1 << m):
            blk = tuple(rem[t] for t in range(m) if (mask >> t) & 1)
            rest = tuple(rem[t] for t in range(m) if not ((mask >> t) & 1))
            acc.append(blk)
            rec(rest, acc)
            acc.pop()

    rec(tuple(range(n)), [])
    return out


ORDERS = {}


def survivors(ell, k, extras, verbose=False, want_counts=False):
    """Surviving configurations = (label, starting choice, weak order) whose whole
    closed cell cycle is satisfiable."""
    if ell not in ORDERS:
        ORDERS[ell] = weak_orders(ell)
    orders = ORDERS[ell]
    good = []
    satpairs = 0
    for i in range(k):
        ok = sat_choices(ell, k, i, extras, verbose)
        satpairs += len(ok)
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
                if okk and tuple(cur) == tuple(c0):
                    good.append((i, c0, order))
    if verbose:
        print(f"ell={ell} k={k} extras={sorted(extras)}: (label,tuple) pairs {satpairs}, "
              f"surviving configurations {len(good)}")
    return good, satpairs
