#!/usr/bin/env python3
"""
Model definition + certificate checker for the Section 8 strip layer at general k.

NO SEARCH HERE.  This file defines the constraint system of Section 8.1 evaluated
at the six R-orbit directions of a single generic direction e, and a checker that
verifies a proposed certificate (delta, word) from scratch.

Geometry / derivation
---------------------
x is a cyclic centre, K_j and v_j are the exclusion continua and limiting
directions of Proposition 7.1 for a simple label cycle of length ell on labels
0..ell-1 (edge i joins i and i+1 mod ell).  theta_j = j*pi/3, R = rotation by
pi/3, e a direction with R^j e not perpendicular to any v_i (all j).

  sigma(i,j) = sign(cos(theta_j - arg v_i))            (sign of edge i at R^j e)
  For generic arg v_i the set {j : sigma(i,j) = +1} is three consecutive
  j's, so it is {delta_i, delta_i+1, delta_i+2} for a unique delta_i in Z/6.

  O_j = labels not equal to an endpoint of any POSITIVE edge at R^j e
  I_j = labels not equal to an endpoint of any NEGATIVE edge at R^j e
  (labels outside the cycle are never endpoints, so are in both)

Constraints (all of them used by the paper at k = ell = 5 in Prop 8.2):
  S0  O_j != empty and I_j != empty                    [Lemma 8.1: a nonempty
       open strip would carry no colour, contrary to the measurable partition]
  S1  1 <= |P_j| <= k-3                                [general-k palette bound]
  S2  P_j cap O_j != empty and P_j cap I_j != empty     [Lemma 8.1, (8.1)]
  S3  P_j cap P_{j+1} = empty, indices mod 6            [Cor 5.4, (5.7)]
  S4  (optional) P_j is not contained in any edge of the cycle [Lemma 6.2,(6.2)]

STRIP(k,ell) = exists delta in (Z/6)^ell and a word (P_0..P_5) of label sets
satisfying S0-S3 (and S4 when strong=True).
"""
import itertools

LABELS = lambda k: frozenset(range(k))

def runs(delta, ell):
    return [frozenset({(delta[i] + t) % 6 for t in range(3)}) for i in range(ell)]

def sign(i, j, R):
    return j in R[i]

def allowed(k, ell, delta):
    """Return list of (O_j, I_j) for j = 0..5."""
    R = runs(delta, ell)
    out = []
    for j in range(6):
        pos, neg = set(), set()
        for i in range(ell):
            ends = {i, (i + 1) % ell}
            if sign(i, j, R):
                pos |= ends
            else:
                neg |= ends
        out.append((frozenset(set(range(k)) - pos), frozenset(set(range(k)) - neg)))
    return out

def cycle_edges(ell):
    return [frozenset({i, (i + 1) % ell}) for i in range(ell)]

def check(k, ell, delta, word, strong=False):
    """Verify a certificate from scratch.  Returns list of violations."""
    bad = []
    if len(delta) != ell or len(word) != 6:
        return ["arity"]
    if any(not (0 <= d < 6) for d in delta):
        return ["delta range"]
    AI = allowed(k, ell, delta)
    for j, (O, I) in enumerate(AI):
        if not O or not I:
            bad.append(f"S0 at j={j}")
        P = frozenset(word[j])
        if not (1 <= len(P) <= k - 3):
            bad.append(f"S1 at j={j}: |P|={len(P)}")
        if not (P & O):
            bad.append(f"S2/O at j={j}")
        if not (P & I):
            bad.append(f"S2/I at j={j}")
        if not (P & frozenset(range(k))):
            bad.append(f"S1' at j={j}")
    for j in range(6):
        P, Q = frozenset(word[j]), frozenset(word[(j + 1) % 6])
        if P & Q:
            bad.append(f"S3 between j={j} and j={(j+1)%6}")
    if strong:
        CE = cycle_edges(ell)
        for j in range(6):
            P = frozenset(word[j])
            for ed in CE:
                if P <= ed:
                    bad.append(f"S4 at j={j}: {sorted(P)} <= edge {sorted(ed)}")
    return bad

def full_word(k, ell, delta, strong=False):
    """Enumerate all words satisfying S1-S4 for this delta (positions independent
    except for S3); return one or None.  Exhaustive product search with pruning.
    This is deliberately naive: it is the 'inside' of the model, used only for small
    instances; the real search is in search1.py / search2.py."""
    AI = allowed(k, ell, delta)
    if any(not O or not I for O, I in AI):
        return None
    cap = k - 3
    opts = []
    for (O, I) in AI:
        cur = []
        for size in range(1, cap + 1):
            for P in itertools.combinations(range(k), size):
                Ps = frozenset(P)
                if (Ps & O) and (Ps & I) and not (strong and any(Ps <= ed for ed in cycle_edges(ell))):
                    cur.append(Ps)
        if not cur:
            return None
        opts.append(cur)
    word = [None] * 6
    def bt(j):
        if j == 6:
            return not (word[5] & word[0])
        for P in opts[j]:
            if j and (P & word[j - 1]):
                continue
            word[j] = P
            if bt(j + 1):
                return True
        word[j] = None
        return False
    for P0 in opts[0]:
        word[0] = P0
        if bt(1):
            return [sorted(w) for w in word]
    return None

if __name__ == "__main__":
    # self-test: the headline k=6, ell=6 witness
    w = [[1, 4], [2, 5], [1, 4], [2, 5], [1, 4], [2, 5]]
    d = [0, 0, 0, 3, 3, 3]
    print("k=6 ell=6 strong:", check(6, 6, d, w, strong=True))
    print("k=6 ell=5 witness:", check(6, 5, [0, 0, 0, 3, 3], [[5], [1, 4], [5], [1, 4], [5], [1, 4]], strong=True))
    print("k=5 ell=5 (paper case) any word?", full_word(5, 5, [0, 0, 0, 0, 0]))
