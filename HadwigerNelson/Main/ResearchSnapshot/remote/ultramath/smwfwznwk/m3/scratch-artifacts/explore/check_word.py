"""Independent exact checker for six-cycle free-label sector words.

A *word* is a list sigma[0..n-1] of palettes (frozensets of labels) with n = 6m.
Conditions checked (all exact, integer arithmetic):
  A. every value is admissible for C_6:  1 <= |P| <= 3 and P is not a subset of
     any cycle edge {i,i+1} mod 6                                (paper (6.2), Lemma 6.2)
  B. label 0 is absent from every value                        (non-proper self-avoidance)
  C. for every sector i and every offset j in
        {+-(m-1), +-m, +-(m+1)} mod 6m,  sigma[i] cap sigma[i+j] = empty   (paper (5.3))
Conditions B/C are reported separately so pairs-only / pairs+triples domains differ.
"""
from itertools import combinations

K = 6
EDGES = [frozenset((j, (j + 1) % 6)) for j in range(6)]


def admissible(S):
    S = frozenset(S)
    return 1 <= len(S) <= 3 and not any(S <= e for e in EDGES)


def offsets(m):
    n = 6 * m
    return sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})


def check(m, word, avoid0=True, verbose=False):
    n = 6 * m
    bad = []
    if len(word) != n:
        return ["length"]
    for i, v in enumerate(word):
        v = frozenset(v)
        if not admissible(v):
            bad.append(("not admissible", i, sorted(v)))
        if avoid0 and 0 in v:
            bad.append(("contains 0", i, sorted(v)))
    offs = offsets(m)
    for i in range(n):
        for j in offs:
            q = (i + j) % n
            if frozenset(word[i]) & frozenset(word[q]):
                bad.append(("transport", i, j, sorted(word[i]), sorted(word[q])))
    if verbose:
        print(f"m={m} n={n} offsets={offs} violations={len(bad)}")
        print("  values used:", sorted({tuple(sorted(v)) for v in word}))
    return bad


def domain(pairs_only=True, avoid0=True):
    vals = []
    for r in (2, 3):
        for c in combinations(range(K), r):
            S = frozenset(c)
            if avoid0 and 0 in S:
                continue
            if admissible(S):
                vals.append(S)
    if pairs_only:
        vals = [v for v in vals if len(v) == 2]
    return vals


if __name__ == "__main__":
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path:
        W = json.load(open(path))
        print("file:", path, "m =", W["m"])
        print("recorded offsets:", W["offsets"], " checker offsets:", offsets(W["m"]))
        bad = check(W["m"], W["word"], verbose=True)
        print("VIOLATIONS:", bad if bad else "none")
    print()
    for po in (True, False):
        print(("pairs-only" if po else "pairs+triples"), "domain:", len(domain(po)),
              [sorted(v) for v in domain(po)])
