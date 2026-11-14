"""Direct exact verification of the geometry behind the decision procedure.

Checks, on explicit rational ray configurations and with no use of the row-interval
abstraction:

  (1) row model     j in S_p(q)  iff  p in P_j(q), where P_j(q) is a cyclically
                    consecutive triple of Z/6;
  (2) row sizes     every P_j(q) has exactly three elements;
  (3) antipodal law S_{p+3} = [ell] \\ S_p;
  (4) slippage      consecutive cells differ by a nonempty set of rays, each ray's
                    triple advancing by exactly one, all in the same direction.
"""

from fractions import Fraction as F
import random
import s8


def sign_cos(x):
    y = x % 2
    if y == F(1, 2) or y == F(3, 2):
        return 0
    return -1 if F(1, 2) < y < F(3, 2) else 1


def row(q, r):
    out = []
    for p in range(6):
        d = (q + F(p, 3) - r) % 2
        if d < F(1, 2) or d > F(3, 2):
            out.append(p)
    return tuple(out)


def idx(iv):
    for m in range(6):
        if set(iv) == {(m - 1) % 6, m, (m + 1) % 6}:
            return m
    return None


def cells(rays, ell=6):
    crit = set()
    for r in rays:
        for p in range(6):
            for s in (F(1, 2), F(-1, 2)):
                crit.add((r - F(p, 3) + s) % 2)
    crit = sorted(crit)
    out = []
    for a, b in zip(crit, crit[1:] + [crit[0] + 2]):
        mid = (a + b) / 2
        pats = tuple(frozenset(j for j in range(ell) if sign_cos(mid + F(p, 3) - rays[j]) > 0)
                     for p in range(6))
        out.append((mid, pats))
    return out


def main(trials=400, seed=7, ell=6):
    random.seed(seed)
    nconf = nrow = nanti = 0
    badrow = badanti = 0
    sizes = set()
    transitions = 0
    badtrans = 0
    for _ in range(trials):
        den = random.choice([5, 7, 11, 13, 17, 19, 23, 29, 31])
        rays = [F(random.randrange(den), den) for _ in range(ell)]
        nconf += 1
        prev = None
        for q, pats in cells(rays, ell):
            # (1),(2) row model
            rows = [row(q, r) for r in rays]
            for t in rows:
                sizes.add(len(t))
            S2 = tuple(frozenset(j for j in range(ell) if p in rows[j]) for p in range(6))
            if [set(x) for x in pats] != [set(x) for x in S2]:
                badrow += 1
            # (3) antipodal law
            for p in range(6):
                if pats[(p + 3) % 6] == frozenset(range(ell)) - pats[p]:
                    nanti += 1
                else:
                    badanti += 1
            # (4) slippage
            ids = [idx(t) for t in rows]
            if any(i is None for i in ids):
                continue
            if prev is not None:
                d = [(ids[j] - prev[j]) % 6 for j in range(ell)]
                nz = [x for x in d if x]
                transitions += 1
                if not nz or any(x != 5 for x in nz):
                    badtrans += 1
            prev = ids
    print(f"configurations checked           : {nconf}")
    print(f"row-model mismatches             : {badrow}")
    print(f"row sizes observed               : {sorted(sizes)}")
    print(f"antipodal law ok / bad           : {nanti} / {badanti}")
    print(f"cell transitions checked / bad   : {transitions} / {badtrans}")


if __name__ == '__main__':
    main()
