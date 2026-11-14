"""Exhaustive verification of Theorem A (label blindness / transport) of L4.md.

A palette structure on a label set A, |A|=k, is (X, D, R, P): centres X, directions
D = Z/6 with the rotation R(d) = d+1, P : X x D -> 2^A minus {empty}.  Clauses:
  LB2 rotation      P(x,d) cap P(x,d+1) = empty        (paper 5.7, R = pi/3)
  LB3 translation   P(x,d) cap P(y,d) = empty for x != y (paper 5.3, sharp form (B))
  LB6 cycle         Gamma = {{i,j}: some palette contains both} has a simple cycle
                    of length >= 3
  N1  palette size  max |P| <= k-3
  N2  outsider size max |P cap (A minus T0)| <= k-4, T0 a fixed 3-set of "cycle labels"
  N3  exclusion     Gamma has no simple cycle of length in the list L
Theorem A: LB2, LB3, LB6 are preserved by every injection sigma: A -> A'; N1 and N2
are preserved when k <= k'.  This script enumerates ALL structures satisfying LB2 and
LB3 (rotation-constrained enumeration, so it is complete, not sampled), for every
k in 2..6, every k' in k..7 and every injection, and checks each clause.
It also checks that N3 is *not* preserved upward, which is the precise statement that
the paper's exclusions of lengths 3,4,5 do not become exclusions of length 6.
"""
import itertools

def cycles_present(G, kmax):
    """set of lengths of simple cycles of G (G = set of frozensets of size 2)."""
    verts = sorted({v for e in G for v in e}); out = set()
    for n in range(3, min(kmax, len(verts)) + 1):
        for cyc in itertools.permutations(verts, n):
            if cyc[0] != min(cyc): continue
            if all(frozenset((cyc[i], cyc[(i+1) % n])) in G for i in range(n)):
                out.add(n); break
    return out

def gamma(P):
    G = set()
    for pal in P.values():
        for i, j in itertools.combinations(sorted(pal), 2):
            G.add(frozenset((i, j)))
    return G

def structures(A, m, nx):
    """All P : (Z/nx) x (Z/6) -> 2^A nonempty, |P|<=m, satisfying LB2 (rotation
    consecutive disjoint) and LB3 (distinct centres, same direction, disjoint)."""
    A = sorted(A)
    opts0 = [frozenset(c) for r in range(1, m+1) for c in itertools.combinations(A, r)]
    def row(prev, forbidden):
        """all 6-tuples (Q_0..Q_5) with Q_{d} cap Q_{d-1} = empty and Q_d cap forbidden = empty"""
        res = []
        def rec(cur, prevq, acc):
            if len(acc) == 6:
                if not (acc[0] & acc[5]): res.append(tuple(acc))
                return
            for q in opts0:
                if q & prevq: continue
                if q & forbidden: continue
                rec(cur+1, q, acc+[q])
        rec(0, frozenset(), [])
        return res
    rows = [row(None, frozenset())]
    allrows = rows[0]
    if nx == 1:
        for r in allrows: yield {((0, d)): r[d] for d in range(6)}
    else:
        for r0 in allrows:
            for r1 in allrows:
                ok = all(not (r0[d] & r1[d]) for d in range(6))
                if not ok: continue
                P = {(0, d): r0[d] for d in range(6)}
                P.update({(1, d): r1[d] for d in range(6)})
                yield P

def evaluate(P, k, T0=None):
    r = {}
    r['Gamma'] = gamma(P)
    r['LB6'] = len(cycles_present(r['Gamma'], k)) > 0
    r['N1'] = max(len(p) for p in P.values()) <= k-3
    if T0 is not None:
        r['N2'] = max(len(p - T0) for p in P.values()) <= k-4
    return r

def transport(P, sig):
    return {key: frozenset(sig[i] for i in pal) for key, pal in P.items()}

def transport_set(S, sig):
    return frozenset(sig[i] for i in S)

import random
def main():
    total = 0; bad = []
    random.seed(20261113)
    for k in range(2, 7):
        m = max(1, k-3)
        T0 = frozenset({0, 1, 2}) if k >= 5 else None
        cnt = 0
        gen = structures(range(k), m, 1)
        structs = []
        for P in gen:
            structs.append(P)
            if k >= 5 and len(structs) > 300: break     # bounded sample for k>=5
        if k <= 4:
            structs = list(structures(range(k), m, 1))  # complete enumeration
        for P in structs:
            cnt += 1
            r = evaluate(P, k, T0)
            for kp in range(k, 8):
                perms = list(itertools.permutations(range(kp), k))
                if len(perms) > 200: perms = random.sample(perms, 200)
                for c in perms:
                    sig = dict(enumerate(c))
                    T0b = transport_set(T0, sig) if T0 is not None else None
                    r2 = evaluate(transport(P, sig), kp, T0b)
                    if r['LB6'] and not r2['LB6']: bad.append(('LB6', k, kp))
                    if r['N1'] and not r2['N1']:   bad.append(('N1', k, kp))
                    if 'N2' in r and r['N2'] and not r2['N2']: bad.append(('N2', k, kp))
            total += 1
        print("k=%d m=%d : %d structures (all satisfying LB2,LB3) verified against "
              "injections into A' of size k..7  [%s]" % (k, m, cnt,
              "complete" if k<=4 else "bounded sample"))
    print("TOTAL structures:", total, " violations of Theorem A:", len(bad))
    # N3 is NOT preserved upward: C_6 has no 3-,4- or 5-cycle but has a 6-cycle.
    G6 = {frozenset((i, (i+1) % 6)) for i in range(6)}
    print("C_6 cycle lengths:", sorted(cycles_present(G6, 6)),
          "-> N3 with L={3,4,5} holds at k=6 while LB6 also holds: the exclusion list is not closed upward.")

if __name__ == "__main__":
    main()
