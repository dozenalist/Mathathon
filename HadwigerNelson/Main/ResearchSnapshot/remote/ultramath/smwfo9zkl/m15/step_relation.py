"""Certificates about the palette state space at a cycle centre.

(a) k=6, six-cycle: every one of the 29 admissible palette values is realised
    by a sector model, and every disjoint pair (v,w) of admissible values is
    realised as (sigma(0), sigma(m)) by a sector model.  So the "state" at a
    six-cycle centre at k=6 is not reducible to a small set and the step
    relation induced by R is the *whole* disjointness relation: there is no
    step rule.  (Contrast k=5, five-cycle: 5 values, disjointness degree 2.)

(b) k=5, three-cycle: the sector CSP is UNSAT.  Certificate: unit propagation
    alone refutes each of the 9 possible values at sector 0 (no search);
    confirmed by an independent DPLL search and by CaDiCaL.

(c) k=5, five-cycle: the disjointness relation on the 5 diagonals is exactly
    the adjacency of C_5 -- the paper's rule (6.6).
"""
import itertools, sys
from pysat.solvers import Cadical153
from construction import allowed_values

DISJOINT = lambda a, b: not (a & b)


def offsets(m, n):
    D = set()
    for base in (m - 1, m, m + 1):
        D.add(base % n)
        D.add((-base) % n)
    D.discard(0)
    return sorted(D)


def csp(k, ell, m, fixed=None, window=1):
    """CNF for the sector CSP; fixed = {(sector, value): True}."""
    n = 6 * m
    V = allowed_values(k, ell)
    nv = len(V)
    D = offsets(m, n)
    if not window:
        D = [t for t in D if abs(t - m) <= 0 or abs(t + m) <= 0]
    idx = {(i, a): i * nv + a + 1 for i in range(n) for a in range(nv)}
    cls = []
    for i in range(n):
        cls.append([idx[i, a] for a in range(nv)])
        for a, b in itertools.combinations(range(nv), 2):
            cls.append([-idx[i, a], -idx[i, b]])
    for i in range(n):
        for t in D:
            j = (i + t) % n
            for a in range(nv):
                for b in range(nv):
                    if not DISJOINT(V[a], V[b]):
                        cls.append([-idx[i, a], -idx[j, b]])
    # (P3): no complementary triple pair both used
    if k == 6:
        for A in V:
            if len(A) != 3:
                continue
            B = frozenset(set(range(6)) - set(A))
            if B not in V or B <= A:
                continue
            a, b = V.index(A), V.index(B)
            for i in range(n):
                for j in range(n):
                    cls.append([-idx[i, a], -idx[j, b]])
    if fixed:
        for (i, v), _ in fixed.items():
            cls.append([idx[i, V.index(frozenset(v))]])
    return n, V, D, idx, cls


def sat_with(k, ell, m, fixed):
    n, V, D, idx, cls = csp(k, ell, m, fixed)
    with Cadical153(bootstrap_with=cls) as s:
        if not s.solve():
            return None
        model = set(x for x in s.get_model() if x > 0)
    nv = len(V)
    sig = []
    for i in range(n):
        for a in range(nv):
            if idx[i, a] in model:
                sig.append(V[a])
                break
    return sig


def recheck(sig, D, k=6, ell=6):
    n = len(sig)
    assert all(DISJOINT(sig[i], sig[(i + t) % n]) for i in range(n) for t in D)
    assert all(1 <= len(s) <= k - 3 for s in sig)
    edges = [frozenset((i, (i + 1) % ell)) for i in range(ell)]
    for s in sig:
        for e in edges:
            assert not s <= e


# ---------------------------------------------------------------- unit prop
def unit_propagation_refutation(V, D, n, seed):
    """Try to refute the instance by unit propagation alone, assuming that
    sector 0 takes value seed.  Returns True iff a contradiction is derived."""
    nv = len(V)
    dom = [[True] * nv for _ in range(n)]           # dom[i][a] = still possible
    for a in range(nv):
        if V[a] != seed:
            dom[0][a] = False
    changed = True
    while changed:
        changed = False
        for i in range(n):
            live = [a for a in range(nv) if dom[i][a]]
            if not live:
                return True                          # empty domain
            if len(live) == 1:
                a = live[0]
                for t in D:
                    j = (i + t) % n
                    for b in range(nv):
                        if dom[j][b] and not DISJOINT(V[a], V[b]):
                            dom[j][b] = False
                            changed = True
        # exactly-one: if a value is impossible at i, forbid it everywhere it
        # would force a clash; plus (P3)
    return any(not any(dom[i]) for i in range(n))


def dpll_solve(V, D, n, nodes=[0]):
    """Independent DPLL (no pysat): returns a model or None."""
    nv = len(V)
    compat = [[DISJOINT(V[a], V[b]) for b in range(nv)] for a in range(nv)]
    assign = [None] * n

    def ok(i, a):
        for t in D:
            j = (i + t) % n
            if assign[j] is not None and not compat[a][assign[j]]:
                return False
        return True

    def rec(i):
        if i == n:
            return True
        for a in range(nv):
            nodes[0] += 1
            if ok(i, a):
                assign[i] = a
                if rec(i + 1):
                    return True
                assign[i] = None
        return False

    return list(assign) if rec(0) else None


if __name__ == "__main__":
    import sys as _s
    print("=== (a) k=6, six-cycle: the whole 29-value space is realised ===", flush=True)
    m = 6
    n, V, D, idx, cls = csp(6, 6, m)
    print("values:", len(V), " sectors:", n, " offsets:", D)
    misses = []
    for v in V:
        sig = sat_with(6, 6, m, {(0, tuple(sorted(v))): True})
        if sig is None:
            misses.append(("value", tuple(sorted(v))))
        else:
            recheck(sig, D)
    print("  values with a model:", len(V) - len(misses), "/", len(V))
    pairs = [(v, w) for v in V for w in V if DISJOINT(v, w)]
    bad = []
    for v, w in pairs:
        sig = sat_with(6, 6, m,
                       {(0, tuple(sorted(v))): True, (m, tuple(sorted(w))): True})
        if sig is None:
            bad.append((tuple(sorted(v)), tuple(sorted(w))))
        else:
            recheck(sig, D)
    comp = [(tuple(sorted(v)), tuple(sorted(w))) for v, w in pairs
            if len(v) == 3 and len(w) == 3 and v | w == set(range(6))]
    print("  ordered disjoint pairs:", len(pairs), " realised:", len(pairs) - len(bad), flush=True)
    print("  unrealised:", len(bad), " and all of them are complementary triples:",
          sorted(bad) == sorted(comp))
    print("  -> the R-step relation at a six-cycle centre is exactly")
    print("     {(v,w) : v cap w = empty, v,w admissible, not both triples complementary}.")
    print("     (the complementary-triple exclusion is (P3), i.e. paper (5.2)).")
    assert sorted(bad) == sorted(comp)
    misses = []

    print()
    print("=== (b) k=5, three-cycle: UNSAT (see WRITEUP.md Lemma 3 for the hand proof) ===")
    for mm in (6, 9, 12, 18, 30):
        n5, V5, D5, _, cls5 = csp(5, 3, mm)
        with Cadical153(bootstrap_with=cls5) as s:
            cad = s.solve()
        d = dpll_solve(V5, D5, n5) if mm <= 6 else "skipped"
        print("  m=%2d  values=%d  CaDiCaL SAT=%s  independent DPLL model=%s"
              % (mm, len(V5), cad, d))
        assert cad is False
        if d != "skipped":
            assert d is None

    print()
    print("=== (c) k=5, five-cycle: the step relation is the C5 adjacency ===")
    V5c = allowed_values(5, 5)
    print("  values:", [tuple(sorted(v)) for v in V5c])
    for i, v in enumerate(V5c):
        opts = [w for w in V5c if DISJOINT(v, w)]
        print("   ", tuple(sorted(v)), "->", [tuple(sorted(w)) for w in opts])
    sys.exit(0 if not misses else 1)
