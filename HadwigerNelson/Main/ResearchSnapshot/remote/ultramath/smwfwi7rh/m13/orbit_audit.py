"""Independent count of the six-cycle single-centre orbit words (audit of 510).

Own implementation: cyclic words of length 6 over the 16 admissible free-label palettes
(size 2..3, not a C6 edge, avoiding the centre colour 0), with
  (5.7)      consecutive disjointness, including the wrap,
  Lemma 2    |P_j| = 3  =>  |P_{j+1}| <= 2,
  MON        not (|P_j| + |P_{j+2}| = 5 and P_j cap P_{j+2} = empty),
  (C1)       no two complementary triples,
  (C2)       at most three ternary palettes.
"""
from itertools import product
import sector_csp as S

VALS = S.VALS
FULL = frozenset({0, 1, 2, 3, 4, 5})


def ok_pair(a, b):
    if a & b:
        return False
    if len(a) == 3 and len(b) > 2:
        return False
    return True


def count(with_extras=True):
    words = []
    for w in product(range(len(VALS)), repeat=6):
        P = [VALS[i] for i in w]
        if not all(ok_pair(P[j], P[(j + 1) % 6]) for j in range(6)):
            continue
        if with_extras:
            if sum(1 for p in P if len(p) == 3) > 3:
                continue
            bad = False
            for j in range(6):
                a, b = P[j], P[(j + 2) % 6]
                if len(a) + len(b) == 5 and not (a & b):
                    bad = True
                for k in range(6):
                    c = P[k]
                    if len(a) == 3 and len(c) == 3 and not (a & c):
                        bad = True
                if len(a) == 1 and next(iter(a)) in range(6):
                    bad = True
            if bad:
                continue
        words.append(tuple(P))
    return words


if __name__ == "__main__":
    w0 = count(False)
    w1 = count(True)
    print("cyclic words, (5.7) only          :", len(w0))
    print("cyclic words, with Lemma 2/MON/C1/C2:", len(w1))
    from collections import Counter
    print("size patterns:", dict(Counter(tuple(len(p) for p in w) for w in w1)))
    print("all-pairs stratum:", sum(1 for w in w1 if all(len(p) == 2 for p in w)))
