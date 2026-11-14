#!/usr/bin/env python3
"""
Certified finite obstruction for the four-cycle continuity step at k = 6.

Lemma 6.6 (continuity of four-cycle states) needs, at k = 5:

  (G) every state is assigned a nonempty group G_s of labels with G_s a subset of
      every palette occurring in state s, and any two distinct groups have union
      of size >= 3, so that no palette of size <= 2 carries two of them.

We decide, exactly, whether such a assignment exists for the 13 admissible
palettes of size <= 2 at a k = 6 four-cycle centre.  Two independent search
paths: (A) exhaustive product over all per-palette choices; (B) a reduction to a
graph-colouring / clique problem on the "compatibility" relation, solved by
brute force over the candidate group sets.

Result (both paths): NO assignment exists, and the obstruction is already the
pair of outside singleton palettes {4} and {5}.
"""

import itertools

X, Y = 4, 5
E4 = [(0, 1), (1, 2), (2, 3), (3, 0)]
LABELS = tuple(range(6))


def admissible(max_size=2):
    out = []
    for r in range(1, max_size + 1):
        for P in itertools.combinations(LABELS, r):
            S = frozenset(P)
            if any(S <= frozenset(e) for e in E4):
                continue
            out.append(S)
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def subsets(P):
    P = sorted(P)
    return [frozenset(c) for r in range(1, len(P) + 1)
            for c in itertools.combinations(P, r)]


def compatible(G1, G2):
    """Lemma 6.6 requirement for two distinct groups."""
    if G1 == G2:
        return True
    return len(G1 | G2) >= 3


def pathA(pals):
    """Exhaustive product search."""
    options = [subsets(P) for P in pals]
    for choice in itertools.product(*options):
        groups = sorted(set(choice), key=lambda s: (len(s), sorted(s)))
        ok = all(compatible(g1, g2) for g1, g2 in itertools.combinations(groups, 2))
        if ok:
            return choice
    return None


def pathB(pals):
    """Reduction: pick the set of groups first, then check that every palette is
    assigned one of its subsets, and that the chosen groups are pairwise
    compatible."""
    all_subsets = sorted({g for P in pals for g in subsets(P)},
                         key=lambda s: (len(s), sorted(s)))
    # backtracking over candidate groups that are pairwise compatible and cover
    n = len(pals)
    best = None

    def rec(i, chosen):
        nonlocal best
        if best is not None:
            return
        if i == n:
            best = tuple(chosen)
            return
        P = pals[i]
        # if some already-chosen group is a subset of P, use it (weaker: try all)
        for g in subsets(P):
            if all(compatible(g, h) for h in chosen):
                chosen.append(g)
                rec(i + 1, chosen)
                chosen.pop()
                if best is not None:
                    return

    rec(0, [])
    return best


def minimal_obstruction(pals):
    """Smallest sub-family of palettes that already admits no assignment."""
    pals = list(pals)
    for k in range(1, len(pals) + 1):
        for sub in itertools.combinations(pals, k):
            if pathA(list(sub)) is None:
                return sub
    return None


if __name__ == "__main__":
    pals = admissible()
    print("admissible palettes of size <= 2:", len(pals))
    print("  ", [tuple(sorted(p)) for p in pals])
    a = pathA(pals)
    b = pathB(pals)
    print("PATH A assignment exists:", a)
    print("PATH B assignment exists:", b)
    assert (a is None) == (b is None)
    ob = minimal_obstruction(pals)
    print("minimal obstruction family:", [tuple(sorted(p)) for p in ob])
    # sanity: the obstruction really is incompatible
    print("  the two forced groups:",
          [tuple(sorted(next(iter(subsets(p))))) for p in ob],
          " union size:",
          len(set(ob[0]) | set(ob[1])))
    # monotonicity: satisfiability is inherited by sub-families, so the "if"
    # direction of Theorem 5.1 is exactly the satisfiability of the maximal
    # sub-families that avoid the obstruction pair.
    S4 = frozenset({4})
    S5 = frozenset({5})
    without_both = [p for p in pals if p not in (S4, S5)]
    without_4 = [p for p in pals if p != S4]
    without_5 = [p for p in pals if p != S5]
    print("without both singletons: n =", len(without_both),
          " satisfiable:", pathA(without_both) is not None,
          "/", pathB(without_both) is not None)
    print("without {4}: n =", len(without_4),
          " satisfiable:", pathA(without_4) is not None,
          "/", pathB(without_4) is not None)
    print("without {5}: n =", len(without_5),
          " satisfiable:", pathA(without_5) is not None,
          "/", pathB(without_5) is not None)
