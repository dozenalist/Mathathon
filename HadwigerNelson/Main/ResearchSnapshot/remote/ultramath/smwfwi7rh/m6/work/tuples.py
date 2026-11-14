"""Pattern-tuple decision, exploiting the antipodal structure S_{p+3} = complement of S_p.

Geometry.  The ray v_j gives the arc of directions  I_j = {e : e.v_j > 0}, an open
semicircle.  The six orbit directions R^p e, p = 0..5, are six equally spaced
directions, so R^{p+3} e is the antipode of R^p e and

   (*)  sigma_j(R^{p+3} e) = -sigma_j(R^p e)   for every j and p,
        i.e.  S_{p+3} = [ell] \\ S_p.

Hence the whole orbit tuple is determined by (S_0, S_1, S_2), and the allowed sets
satisfy (O,I)_{p+3} = (I,O)_p.

The pointwise system at a cyclic centre is:
  (8.1)  P_p cap O_p != empty,  P_p cap I_p != empty
  (5.7)  P_p cap P_{p+1} = empty   (p mod 6)
  (5.12) 1 <= |P_p| <= k-3
  (6.2)  P_p is not a subset of any edge of the cycle
  (SA)   the centre's own label i is in no P_p
"""

from itertools import combinations, product
import s8

_CACHE = {}


def palettes(oc, ell, k, i, w2sup):
    key = (oc, ell, k, i, w2sup)
    v = _CACHE.get(key)
    if v is None:
        v = s8.palettes_for(oc, ell, k, i, w2sup)
        _CACHE[key] = v
    return v


def comp(S, ell):
    return frozenset(range(ell)) - S


def build(S0, S1, S2, ell):
    return (S0, S1, S2, comp(S0, ell), comp(S1, ell), comp(S2, ell))


def sat_tuple(pats, ell, k, w2sup):
    ocs = tuple(s8.allowed_sets(S, ell, k) for S in pats)
    if any(len(O) == 0 or len(I) == 0 for (O, I) in ocs):
        return ('L81', None)
    for i in range(k):
        doms = [palettes(oc, ell, k, i, w2sup) for oc in ocs]
        sol = s8.csp_sat(doms)
        if sol is not None:
            return ('OK', (i, sol))
    return ('CSP', None)


def census(ell, k, w2sup):
    counts, survivors = {}, []
    subs = [frozenset(c) for r in range(ell + 1) for c in combinations(range(ell), r)]
    for S0, S1, S2 in product(subs, repeat=3):
        pats = build(S0, S1, S2, ell)
        st, sol = sat_tuple(pats, ell, k, w2sup)
        counts[st] = counts.get(st, 0) + 1
        if st == 'OK':
            survivors.append((pats, sol))
    return counts, survivors


if __name__ == '__main__':
    import sys
    ell = int(sys.argv[1]); k = int(sys.argv[2]); w2 = int(sys.argv[3])
    c, surv = census(ell, k, w2)
    print(f"ell={ell} k={k} |P|<={w2}: {c}")
    for pats, sol in surv[:6]:
        i, ps = sol
        print("  SAT tuple, avoided label", i)
        print("   S:", [sorted(p) for p in pats])
        print("   P:", [sorted(p) for p in ps])
