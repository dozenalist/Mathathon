"""Exhaustive decision for a cycle of length ell at k colours.

Geometry used (proved in proof.md):

  For a cyclic centre x with a simple cycle of length ell, edge j = {j,j+1} with
  continuum K_j and limiting unit direction v_j, section 8.1 of the paper sets
      sigma_j(e) = sign(e . v_j),   O(e) = [k] minus endpoints of positive edges,
      I(e) = [k] minus endpoints of negative edges,
  and (8.1) of Lemma 8.1 says  P_x(e) cap O(e) != empty and P_x(e) cap I(e) != empty
  for a.e. e outside the finite set B.

  Each sigma_j is positive on the open semicircle I_j = {e : e.v_j > 0}.  The six
  orbit directions R^p e (p in Z/6) are equally spaced, so R^{p+3}e is the antipode
  of R^p e; an open semicircle contains exactly one of an antipodal pair, hence

      sigma_j(R^{p+3} e) = -sigma_j(R^p e)      i.e.  S_{p+3} = [ell] \\ S_p,   (*)

  and therefore (O,I)_{p+3} = (I,O)_p.

  Define the row of ray j:  P_j(q) = {p in Z/6 : sigma_j(R^p e_q) = +1} where e_q is
  the direction of angle pi*q.  Since I_j has angular length pi = half a turn and
  the six orbit directions are a regular hexagon, P_j(q) is a cyclic interval of
  length 3 in Z/6 (for a.e. q), and the map j -> P_j can be prescribed arbitrarily
  by choosing the rays.  So the achievable sign tuples are exactly

      S_p = { j : p in P_j },   P_j any cyclic 3-interval of Z/6,

  and as q advances each ray's interval moves by one step, one ray at a time, in the
  order of the residues v_j mod pi/3.

  The pointwise palette system at the orbit is
      (8.1)      P_p cap O_p, P_p cap I_p nonempty
      (5.7)      P_p cap P_{p+1} = empty  (indices mod 6)
      (5.12)     1 <= |P_p| <= k-3
      (6.2)      P_p not contained in an edge of the cycle
      (SA)       the centre's own colour i is in no P_p.
"""

from itertools import combinations, product
import s8
import orbit


def intervals6():
    """The six cyclic 3-intervals of Z/6 and a name for each."""
    out = []
    for m in range(6):
        out.append((m, frozenset({(m - 1) % 6, m, (m + 1) % 6})))
    return out


def tuple_from_rows(rows, ell):
    """S_p = {j : p in rows[j]}."""
    return tuple(frozenset(j for j in range(ell) if p in rows[j]) for p in range(6))


def achievable(ell):
    """All achievable orbit sign-tuples, from all row assignments."""
    iv = intervals6()
    for choice in product(range(6), repeat=ell):
        rows = [iv[c][1] for c in choice]
        yield choice, tuple_from_rows(rows, ell)


def adjacent(c1, c2):
    """Do the two row assignments differ in exactly one ray, by one step?"""
    diff = [j for j in range(len(c1)) if c1[j] != c2[j]]
    if len(diff) != 1:
        return False
    j = diff[0]
    return (c1[j] - c2[j]) % 6 in (1, 5)


def decide(ell, k, w2sup, verbose=True):
    orbit._build_disj(k)
    table = orbit.domain_table(ell, k, w2sup)
    grp = orbit.dihedral(k)
    keys = sorted(table)
    img = {(g, oc): (frozenset(g[x] for x in oc[0]), frozenset(g[x] for x in oc[1]))
           for g in grp for oc in keys}
    cache = {}

    def status(S):
        ocs = tuple(s8.allowed_sets(s, ell, k) for s in S)
        if any(oc not in table for oc in ocs):
            return 'L81'
        # canonicalise the triple (oc0,oc1,oc2) up to the dihedral group
        trip = (ocs[0], ocs[1], ocs[2])
        best = None
        for g in grp:
            tt = (img[(g, trip[0])], img[(g, trip[1])], img[(g, trip[2])])
            for i in range(k):
                key = (tt, i)
                if best is None or key < best:
                    best = key
        if best in cache:
            return cache[best]
        tt = best[0]
        val = 'CSP'
        for i in range(k):
            if orbit.walk_exists(table[tt[0]][i], table[tt[1]][i], table[tt[2]][i]):
                val = 'OK'
                break
        cache[best] = val
        return val

    stats = {}
    rows_of = {}
    for choice, S in achievable(ell):
        st = status(S)
        stats[st] = stats.get(st, 0) + 1
        rows_of.setdefault(choice, (S, st))
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2sup}: {len(rows_of)} achievable sign tuples -> {stats}")
    sat_rows = {c: v for c, v in rows_of.items() if v[1] == 'OK'}
    if verbose:
        print(f"   SAT row assignments: {len(sat_rows)}")
    bad = [(a, b) for a in sat_rows for b in sat_rows if a < b and adjacent(a, b)]
    if verbose:
        print(f"   adjacent SAT pairs: {len(bad)}")
        for a, b in bad[:6]:
            print("     ", a, "->", b, " tuples", [sorted(x) for x in sat_rows[a][0]],
                  [sorted(x) for x in sat_rows[b][0]])
    return stats, sat_rows, bad


if __name__ == '__main__':
    import sys
    ell, k, w2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    decide(ell, k, w2)
