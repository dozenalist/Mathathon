"""The k=6 interface decision with (C4)+(C5): plain vs. tightened, all ray geometries.

Same independent encoder as vacuity.py (paper's definitions, not m5's code), but the
model search is a DFS that records, for each ray geometry, which of three kinds of model
exists:

  plain     (C1)+(C2)+(C3)                     [m5's system]
  max2      (C1)+(C2)+(C3) with all |P_i| <= 2 [implies (C4)+(C5): see TRIVIALITY.md]
  tight     (C1)+(C2)+(C3)+(C4)+(C5)

Output: counts per ell, plus a verified witness for each row.
Run:  python3 tightened_table.py
"""
from itertools import product, combinations
import json
import sympy

K = 6
NPOS = 6
COS_SIGN = [int(sympy.sign(sympy.cos(m * sympy.pi / 3))) for m in range(6)]


def sign_matrix(ell, cells):
    return [[COS_SIGN[(cells[j] + 1 - i) % 6] for j in range(ell)] for i in range(NPOS)]


def allowed_sets(ell, k, sig_i):
    U = set(range(k)) - set(range(ell))
    O, I = set(U), set(U)
    for j in range(ell):
        if sig_i[(j - 1) % ell] == -1 and sig_i[j] == -1:
            O.add(j)
        if sig_i[(j - 1) % ell] == 1 and sig_i[j] == 1:
            I.add(j)
    return frozenset(O), frozenset(I)


def admissible(ell, k, sig_i):
    O, I = allowed_sets(ell, k, sig_i)
    out = []
    for r in range(1, k - 2):
        for c in combinations(range(k), r):
            s = frozenset(c)
            if s & O and s & I:
                out.append(s)
    return out


def models(ell, k, cells):
    """Return (plain, max2, tight) booleans."""
    sig = sign_matrix(ell, cells)
    adm = [admissible(ell, k, sig[i]) for i in range(NPOS)]
    if any(not a for a in adm):
        return (False, False, False)
    allk = frozenset(range(k))
    found = [False, False, False]
    sol = []

    def complementary(a, b):
        return len(a) == 3 and len(b) == 3 and a | b == allk

    def rec(i, ntern, tern):
        if found[0] and found[1] and found[2]:
            return
        if i == NPOS:
            if sol[NPOS - 1] & sol[0]:
                return
            found[0] = True
            if ntern == 0:
                found[1] = True
            # (C4) and (C5) were enforced incrementally below
            found[2] = True
            return
        for p in adm[i]:
            if i and (p & sol[i - 1]):
                continue
            if len(p) == 3:
                if ntern + 1 > 3:                                    # (C5)
                    continue
                if any(complementary(p, q) for q in tern):           # (C4)
                    continue
                sol.append(p)
                tern.add(p)
                rec(i + 1, ntern + 1, tern)
                tern.discard(p)
                sol.pop()
            else:
                sol.append(p)
                rec(i + 1, ntern, tern)
                sol.pop()
            if found[0] and found[1] and found[2]:
                return

    # start position 0 separately so that (C5)/(C4) bookkeeping is uniform
    for p0 in adm[0]:
        sol[:] = [p0]
        tern = set()
        n = 0
        if len(p0) == 3:
            tern.add(p0)
            n = 1
        rec(1, n, tern)
        if found[0] and found[1] and found[2]:
            break
    return tuple(found)


def witness_tight(ell, k, cells):
    """Return a (C1)-(C5) model or None (independent check: validate() below)."""
    sig = sign_matrix(ell, cells)
    adm = [admissible(ell, k, sig[i]) for i in range(NPOS)]
    if any(not a for a in adm):
        return None
    allk = frozenset(range(k))
    sol = []

    def rec(i, tern):
        if i == NPOS:
            return not (sol[NPOS - 1] & sol[0])
        for p in adm[i]:
            if i and (p & sol[i - 1]):
                continue
            if len(p) == 3:
                if len(tern) + 1 > 3:
                    continue
                if any(q != p and len(q) == 3 and p | q == allk for q in tern):
                    continue
                if any(p | q == allk for q in [x for x in sol if len(x) == 3]):
                    continue
                sol.append(p)
                tern.add(p)
                if rec(i + 1, tern):
                    return True
                tern.discard(p)
                sol.pop()
            else:
                sol.append(p)
                if rec(i + 1, tern):
                    return True
                sol.pop()
        return False

    for p0 in adm[0]:
        sol[:] = [p0]
        t = set([p0]) if len(p0) == 3 else set()
        if rec(1, t):
            return [sorted(x) for x in sol]
    return None


def validate(ell, k, cells, pal):
    """Re-check (C1)-(C5) from scratch, slowly and literally."""
    sig = sign_matrix(ell, cells)
    S = [frozenset(p) for p in pal]
    assert len(S) == NPOS
    for i in range(NPOS):
        O, I = allowed_sets(ell, k, sig[i])
        assert 1 <= len(S[i]) <= k - 3, ("C1", i)
        assert S[i] & O, ("C2 O", i)
        assert S[i] & I, ("C2 I", i)
        assert not (S[i] & S[(i + 1) % NPOS]), ("C3", i)
    for i, j in combinations(range(NPOS), 2):
        assert not (len(S[i]) == 3 and len(S[j]) == 3 and S[i] | S[j] == frozenset(range(k))), ("C4", i, j)
    assert sum(1 for s in S if len(s) == 3) <= 3, "C5"
    return True


if __name__ == "__main__":
    rows = []
    for ell in (3, 4, 5, 6):
        counts = {"geometries": 6 ** (ell - 1), "plain": 0, "max2": 0, "tight": 0, "plain_not_tight": 0}
        first = {}
        for cells in product(range(6), repeat=ell):
            if cells[0] != 0:                   # rotation symmetry, as in m5's scan()
                continue
            pl, m2, ti = models(ell, K, cells)
            counts["plain"] += pl
            counts["max2"] += m2
            counts["tight"] += ti
            if pl and not ti:
                counts["plain_not_tight"] += 1
            if ti and "tight" not in first:
                w = witness_tight(ell, K, cells)
                validate(ell, K, cells, w)
                first["tight"] = {"cells": list(cells), "palettes": w}
            if m2 and "max2" not in first:
                first["max2"] = {"cells": list(cells)}
        print(f"ell={ell}: {counts}", flush=True)
        if first.get("tight"):
            print(f"    witness tight ell={ell}: cells={first['tight']['cells']}"
                  f" palettes={first['tight']['palettes']}", flush=True)
        rows.append({"ell": ell, **counts, "witness": first})
    with open("tightened_table.json", "w") as f:
        json.dump(rows, f, indent=1)
    print("m5's published plain counts (c_0=0): ell=3:36 ell=4:216 ell=5:225 ell=6:177")
