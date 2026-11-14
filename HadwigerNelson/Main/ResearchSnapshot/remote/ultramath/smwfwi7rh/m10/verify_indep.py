#!/usr/bin/env python3
"""Independent re-decision of the finite statements of `verify.py`.

A second code path: label sets are integer bitmasks (not frozensets), the search
order is dynamic (min-domain / MRV) rather than positional, there is no forward
checking, and the disjointness graph is built once.  Run:

    python3 verify_indep.py

It re-decides the SIX-CYCLE FREE-LABEL PAIR SYSTEM for the sector resolutions
n in {12,18,24,30,36} and re-verifies the witnesses of record.  Exit 0 on
agreement with verify.py, 1 otherwise.
"""
import itertools
import sys

# ------------------------------------------------------------------ utilities
def edges(ell):
    return [((j) % ell, (j + 1) % ell) for j in range(ell)]


def adm_pairs(ell=6):
    bad = set()
    for (a, b) in edges(ell):
        bad.add((1 << a) | (1 << b))
    out = []
    for a, b in itertools.combinations(range(ell), 2):
        m = (1 << a) | (1 << b)
        if m not in bad:
            out.append(m)
    return out


def bits(m):
    return [i for i in range(6) if m >> i & 1]


# ------------------------------------------------------------------ the solver
def decide(n, domain, offsets):
    """Complete search, dynamic MRV, no forward checking.  Returns (witness|None)."""
    nbr = {i: sorted({(i + d) % n for d in offsets}) for i in range(n)}
    # static adjacency in the value graph
    ok_val = {}
    for A in domain:
        for B in domain:
            ok_val[(A, B)] = (A & B) == 0
    assign = {}

    def domains():
        d = {}
        for i in range(n):
            if i in assign:
                continue
            cand = []
            for A in domain:
                good = True
                for j in nbr[i]:
                    if j in assign and not ok_val[(A, assign[j])]:
                        good = False
                        break
                if good:
                    cand.append(A)
            d[i] = cand
        return d

    def rec():
        if len(assign) == n:
            return True
        d = domains()
        if any(len(v) == 0 for v in d.values()):
            return False
        # MRV with a deterministic tie-break (smallest index)
        i = min(d, key=lambda k: (len(d[k]), k))
        for A in d[i]:
            assign[i] = A
            if rec():
                return True
            del assign[i]
        return False

    if rec():
        return [assign[i] for i in range(n)]
    return None


def verify(n, w, domain, offsets, forbid_label):
    if w is None:
        return False, "none"
    if any(v not in domain for v in w):
        return False, "value outside domain"
    if any(v >> forbid_label & 1 for v in w):
        return False, "free label used"
    for i in range(n):
        for d in offsets:
            if w[i] & w[(i + d) % n]:
                return False, "overlap at offset %d, position %d" % (d, i)
    return True, "ok"


# ------------------------------------------------------------------- the runs
WITNESSES = {
    # n = 36, from verify.py  (period 12)
    36: [[1, 3], [1, 3], [1, 3], [1, 4], [1, 4], [2, 4],
         [2, 4], [2, 4], [2, 5], [2, 5], [3, 5], [3, 5]] * 3,
    # n = 30, from verify.py  (period 10)
    30: [[1, 3], [1, 3], [1, 4], [1, 4], [2, 4],
         [2, 4], [2, 5], [2, 5], [3, 5], [3, 5]] * 3,
}


def main():
    P = adm_pairs(6)
    assert len(P) == 9, len(P)
    print("admissible pairs of C_6 as bitmasks:", [bits(m) for m in P])
    ok_all = True
    for n in (12, 18, 24, 30, 36):
        m = n // 6
        offs = sorted({(m - 1) % n, m % n, (m + 1) % n,
                       (-(m - 1)) % n, (-m) % n, (-(m + 1)) % n})
        verdicts = []
        for free in range(6):
            dom = [p for p in P if not (p >> free & 1)]
            assert len(dom) == 6
            w = decide(n, dom, offs)
            if w is None:
                verdicts.append("UNSAT")
            else:
                good, why = verify(n, w, dom, offs, free)
                verdicts.append("SAT" if good else "SAT-BUT-BAD(%s)" % why)
                if not good:
                    ok_all = False
            if n in WITNESSES and free == 0:
                w2 = [[1 << a | 1 << b for (a, b) in [v]][0] for v in WITNESSES[n]]
                good, why = verify(n, w2, dom, offs, free)
                print("   n=%2d : witness of record re-verified: %s (%s)" % (n, good, why))
                ok_all = ok_all and good
        print("   n=%2d offsets %s : verdicts over the six free labels: %s"
              % (n, offs, verdicts))
        if len(set(verdicts)) != 1:
            print("   !! free-label dependence")
            ok_all = False
    print()
    print("INDEPENDENT CHECK:", "agrees" if ok_all else "DISAGREES")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
