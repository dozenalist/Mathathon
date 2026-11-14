"""Interface state CSP at a cyclic centre, exact integer arithmetic, bitmask DP.

Setup and derivation: see INTERFACE-NOGO.md.  This file is the executable part:
for each (k, ell) and each ray geometry it decides whether the six-position
palette system (C1)-(C3) is satisfiable, and records explicit witnesses.

Bitmask encoding: label i -> bit i.  Disjointness is (p & q) == 0.
"""

from itertools import product, combinations

# sign of cos(m*pi/3): +1 for m = 0,1,5 (mod 6), -1 for m = 2,3,4 (mod 6).  No zero.
COS_SIGN = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}


def sign_matrix(ell, c):
    """6 x ell: SIG[i][j] = sign(e_i . v_j) for ray cells c (c_j in 0..5)."""
    return [[COS_SIGN[(c[j] + 1 - i) % 6] for j in range(ell)] for i in range(6)]


def allowed_sets(ell, k, sig_i):
    """(O_i, I_i) as bitmasks, from paper (8.1)."""
    T = (1 << ell) - 1
    U = ((1 << k) - 1) ^ T
    O = I = 0
    for j in range(ell):
        if sig_i[(j - 1) % ell] == -1 and sig_i[j] == -1:
            O |= 1 << j
        if sig_i[(j - 1) % ell] == 1 and sig_i[j] == 1:
            I |= 1 << j
    return O | U, I | U


def admissible_masks(ell, k, sig_i):
    """All P with 1 <= |P| <= k-3 and P meeting O_i and I_i  ((C1),(C2))."""
    O, I = allowed_sets(ell, k, sig_i)
    out = []
    for r in range(1, k - 2):
        for comb in combinations(range(k), r):
            p = 0
            for i in comb:
                p |= 1 << i
            if (p & O) and (p & I):
                out.append(p)
    return out


def sat_geometry(ell, k, c):
    """True iff the six-position CSP is satisfiable for this ray geometry."""
    sig = sign_matrix(ell, c)
    adm = [admissible_masks(ell, k, sig[i]) for i in range(6)]
    if any(not a for a in adm):
        return False
    pos = {p: n for n, p in enumerate(adm[0])}
    reach = {p: 1 << n for p, n in pos.items()}
    for i in range(1, 6):
        nxt = {}
        for q in adm[i]:
            acc = 0
            for p, v in reach.items():
                if not (p & q):
                    acc |= v
            if acc:
                nxt[q] = acc
        reach = nxt
        if not reach:
            return False
    for q, v in reach.items():          # need q disjoint from the start state
        for p, n in pos.items():
            if not (p & q) and (v >> n) & 1:
                return True
    return False


def witness(ell, k, c):
    """Return an explicit solution as a list of 6 sorted label lists, or None."""
    sig = sign_matrix(ell, c)
    adm = [admissible_masks(ell, k, sig[i]) for i in range(6)]

    def bt(i, sol):
        if i == 6:
            return not (sol[5] & sol[0])
        for q in adm[i]:
            if not (q & sol[i - 1]):
                sol.append(q)
                if bt(i + 1, sol):
                    return True
                sol.pop()
        return False

    for s in adm[0]:
        sol = [s]
        if bt(1, sol):
            return [[i for i in range(k) if (p >> i) & 1] for p in sol]
    return None


def scan(ell, k, fix_first_cell=True):
    """(total geometries scanned, number satisfiable, first witness)."""
    cells = range(6)
    if fix_first_cell:                  # global rotation by pi/3 is a symmetry
        tuples = ((0,) + t for t in product(cells, repeat=ell - 1))
        total = 6 ** (ell - 1)
    else:
        tuples = product(cells, repeat=ell)
        total = 6 ** ell
    sat = 0
    first = None
    for c in tuples:
        if sat_geometry(ell, k, c):
            sat += 1
            if first is None:
                first = {"cells": list(c), "palettes": witness(ell, k, c)}
    return total, sat, first


if __name__ == "__main__":
    import json
    results = []
    print(f"{'k':>2} {'ell':>3} {'m':>2} {'geometries':>10} {'SAT':>8}  status")
    for k in (4, 5, 6, 7):
        for ell in range(3, k + 1):
            total, sat, first = scan(ell, k)
            st = "SAT" if sat else "UNSAT (all ray geometries)"
            print(f"{k:>2} {ell:>3} {k-ell:>2} {total:>10} {sat:>8}  {st}", flush=True)
            results.append({"k": k, "ell": ell, "m": k - ell, "geometries": total,
                            "sat": sat, "witness": first})
    with open("interface_csp_results.json", "w") as f:
        json.dump(results, f, indent=1)
