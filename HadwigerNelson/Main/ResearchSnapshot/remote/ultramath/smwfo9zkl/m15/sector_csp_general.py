"""General sector CSP for k labels and a specified simple cycle.

A "sector palette system" of resolution n = 6m is a function sigma on the n
equal sectors of S^1 taking palette values (subsets of the label set I).

Constraints encoded (all palette-level; see palette.py docstring for the
provenance of each):

 (P0) 1 <= |sigma| <= k-3                       palette bound
 (P1) sigma(i) is not contained in a cycle edge  paper (6.2)  [Gamma_x contains
                                                 the cycle]
 (P2) sigma(i) cap sigma(i+m) = empty            paper (5.7)  [R f]
 (P3) no two complementary (k-3)-sets both used  paper (5.2) at k=6
 (P4) sigma(i) cap sigma(i +- (m-1,m,m+1)) = empty   paper (5.3) two-centre
      exclusion, exact: see verify.py

The sector resolution must satisfy: a palette system at resolution n with its
palette values satisfying (P4)-as-a-sector-condition is an exact model of
(P0)-(P4) for centres of diameter <= pi/(6m).  verify.py checks that reduction.
"""
import itertools, sys
from pysat.solvers import Cadical153


def cycle_edges(k, ell, labels=None):
    if labels is None:
        labels = list(range(ell))
    return [frozenset((labels[i], labels[(i + 1) % ell])) for i in range(ell)]


def allowed_values(k, ell, triples=True):
    edges = cycle_edges(k, ell)
    out = []
    for r in range(1, k + 1):
        if r > k - 3:
            break
        if r == 3 and not triples:
            continue
        for c in itertools.combinations(range(k), r):
            S = frozenset(c)
            if any(S <= e for e in edges):
                continue
            out.append(S)
    return out


def complementary_triples(k):
    """pairs {A, A^c} of 3-subsets (only used when k = 6)."""
    if k != 6:
        return []
    out = []
    for c in itertools.combinations(range(6), 3):
        A = frozenset(c)
        B = frozenset(set(range(6)) - set(c))
        if A < B:
            out.append((A, B))
    return out


def build(k, ell, m, window=1, triples=True):
    n = 6 * m
    V = allowed_values(k, ell, triples)
    nv = len(V)
    idx = {(i, a): i * nv + a for i in range(n) for a in range(nv)}
    clauses = []
    for i in range(n):
        clauses.append([idx[i, a] + 1 for a in range(nv)])
        for a, b in itertools.combinations(range(nv), 2):
            clauses.append([-(idx[i, a] + 1), -(idx[i, b] + 1)])
    D = set()
    for s in range(-window, window + 1):
        for base in (m - 1, m, m + 1):
            D.add((base + s) % n)
            D.add((-base + s) % n)
    D.discard(0)
    for i in range(n):
        for j in sorted(D):
            kk = (i + j) % n
            for a in range(nv):
                for b in range(nv):
                    if V[a] & V[b]:
                        clauses.append([-(idx[i, a] + 1), -(idx[kk, b] + 1)])
    for A, B in complementary_triples(k):
        if A not in V or B not in V:
            continue
        a, b = V.index(A), V.index(B)
        for i in range(n):
            for j in range(n):
                clauses.append([-(idx[i, a] + 1), -(idx[j, b] + 1)])
    return dict(n=n, V=V, idx=idx, clauses=clauses, D=sorted(D), nv=nv)


def solve(k, ell, m, window=1, triples=True):
    info = build(k, ell, m, window, triples)
    with Cadical153(bootstrap_with=info["clauses"]) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    sig = None
    if model:
        pos = {x for x in model if x > 0}
        V, idx, n, nv = info["V"], info["idx"], info["n"], info["nv"]
        sig = []
        for i in range(n):
            for a in range(nv):
                if idx[i, a] + 1 in pos:
                    sig.append(V[a])
                    break
    return sat, sig, info


if __name__ == "__main__":
    k = int(sys.argv[1])
    triple_mode = not (len(sys.argv) > 2 and sys.argv[2] == "notriples")
    for ell in range(3, k + 1):
        for m in (6, 9, 12, 18):
            sat, sig, info = solve(k, ell, m, triples=triple_mode)
            extra = ""
            if sig:
                n, D = info["n"], set(info["D"])
                bad = sum(1 for i in range(n) for j in D if sig[i] & sig[(i + j) % n])
                extra = " violations=%d" % bad
            print("k=%d ell=%d m=%2d  |V|=%2d  SAT=%s%s"
                  % (k, ell, m, info["nv"], sat, extra), flush=True)
