"""Sector CSP: does there exist a piecewise-constant palette function
sigma : S^1 -> 2^I, constant on n = 6m equal sectors, such that

   sigma(i) is disjoint from sigma(j)  whenever  j - i in D  (mod n),
   D = {+-(m-1), +-m, +-(m+1)},

with every value satisfying (P0),(P1) and (P3) globally (no complementary
triple pair used)?

A model of this CSP, together with centres of diameter <= d0 = (2*pi/n)/C_ang,
gives an exact palette system meeting (P0),(P1),(P2),(P3),(P4) with all
centres in a disk of radius d0 whose transition graphs all contain the
6-cycle: see verify.py.

Usage:  python3 sector_csp.py m [m ...] [--triples {none,one,free}]
"""
import sys, itertools
from pysat.solvers import Cadical153
from palette import allowed_values, disjoint, EDGES

COMPL = {}
for A in itertools.combinations(range(6), 3):
    COMPL[frozenset(A)] = frozenset(set(range(6)) - set(A))


def usable_values(use_triples):
    V = allowed_values()
    if use_triples == "none":
        return [v for v in V if len(v) == 2]
    if use_triples == "free":
        return V
    # "one": from each complementary triple pair, keep only the lexicographically
    # smaller one; pairs all kept.
    keep = []
    seen = set()
    for v in sorted(V, key=lambda s: (len(s), sorted(s))):
        if len(v) == 3:
            if v in seen or COMPL[v] in seen:
                continue
            seen.add(v)
            seen.add(COMPL[v])
        keep.append(v)
    return keep


def solve(m, use_triples="free", window=1, want_model=True):
    n = 6 * m
    V = usable_values(use_triples)
    nv = len(V)
    idx = {}
    c = 0
    for i in range(n):
        for a in range(nv):
            idx[i, a] = c
            c += 1
    clauses = []
    # exactly one value per sector
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
    npair = 0
    for i in range(n):
        for j in sorted(D):
            k = (i + j) % n
            for a in range(nv):
                for b in range(nv):
                    if not disjoint(V[a], V[b]):
                        clauses.append([-(idx[i, a] + 1), -(idx[k, b] + 1)])
                        npair += 1
    # (P3): no complementary triple pair both used
    tri = [a for a in range(nv) if len(V[a]) == 3]
    for a in tri:
        if COMPL[V[a]] not in V:
            continue
        b = V.index(COMPL[V[a]])
        if b < a:
            continue
        for i in range(n):
            for j in range(n):
                clauses.append([-(idx[i, a] + 1), -(idx[j, b] + 1)])
    with Cadical153(bootstrap_with=clauses) as s:
        sat = s.solve()
        model = s.get_model() if (sat and want_model) else None
    sig = None
    if model:
        pos = set(x for x in model if x > 0)
        sig = [V[[a for a in range(nv) if idx[i, a] + 1 in pos][0]] for i in range(n)]
    return sat, sig, dict(n=n, nv=nv, D=sorted(D), clauses=len(clauses), npair=npair)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tri = "free"
    for a in sys.argv[1:]:
        if a.startswith("--triples"):
            tri = a.split("=")[1] if "=" in a else "free"
    for m in [int(a) for a in args]:
        sat, sig, info = solve(m, tri)
        ok = ""
        if sig:
            n = info["n"]
            D = set(info["D"])
            viol = [(i, j) for i in range(n) for j in D
                    if not disjoint(sig[i], sig[(i + j) % n])]
            ok = " recheck-violations=%d" % len(viol)
        print("m=%d triples=%s SAT=%s  %s%s" % (m, tri, sat, info, ok))
        if sig:
            print("   sigma:", " ".join("".join(map(str, sorted(v))) for v in sig))
