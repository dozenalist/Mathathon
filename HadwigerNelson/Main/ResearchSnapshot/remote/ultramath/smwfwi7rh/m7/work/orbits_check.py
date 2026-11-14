"""
Independent reproduction of the single-centre R-orbit counts of sprint/k6 (STRUCTURE.md,
Theorem 5 items 1-7 plus the edge trace (6.2)), as a third implementation.

Constraints, from the specification:
  alphabet: nonempty A subseteq [6] minus {i}, |A| <= 3, A not contained in any edge of C_ell
  (1) i notin P_j for all j                                   [self-avoidance]
  (2) P_j cap P_{j+1} = empty                                 [(5.7)]
  (3) |P_j| = 3 => |P_{j+1}| <= 2                             [ternary forces pair]
  (4) |P_j| = 1 => its label notin V(C_ell)                   [singletons avoid cycle vertices]
  (5) not (|P_j|+|P_{j+2}| = 5 and P_j cap P_{j+2} = empty)   [no monochromatic unit sum]
  (6) no two members are complementary 3-sets                 [(C1)]
  (7) at most three ternary members                           [(C2)]
DFS over positions 0..5 with early rejection; every word is re-checked by an independent
whole-word predicate before being counted.
"""
from itertools import combinations

k = 6
labels = tuple(range(k))

def admissible(ell, i):
    V = set(range(ell))
    out = []
    for r in (1, 2, 3):
        for S in combinations([x for x in labels if x != i], r):
            A = frozenset(S)
            if any(A <= frozenset({j, (j + 1) % ell}) for j in range(ell)):
                continue
            out.append(A)
    return sorted(out, key=lambda A: (len(A), sorted(A)))

def step_ok(a, b, V):
    if a & b:
        return False
    if len(a) == 3 and len(b) > 2:
        return False
    if len(a) == 1 and next(iter(a)) in V:
        return False
    return True

def word_ok(w, V):
    n = len(w)
    for j in range(n):
        a, b = w[j], w[(j + 1) % n]
        if not step_ok(a, b, V):
            return False
        if len(b) == 1 and next(iter(b)) in V:
            return False
        c = w[(j + 2) % n]
        if len(a) + len(c) == 5 and not (a & c):
            return False
        for d in range(n):
            e = w[d]
            if len(a) == 3 and len(e) == 3 and not (a & e):
                return False
    if sum(1 for A in w if len(A) == 3) > 3:
        return False
    return True

def count(ell, i):
    A = admissible(ell, i)
    V = set(range(ell))
    res = []
    def rec(p):
        if len(p) == 6:
            if word_ok(tuple(p), V):
                res.append(tuple(p))
            return
        for b in A:
            if p and not step_ok(p[-1], b, V):
                continue
            rec(p + [b])
    rec([])
    return A, res

def main():
    print(f"{'ell':>3} {'centre':>7} {'|alphabet|':>10} {'words':>8} {'all-pairs':>10} {'(3,2,3,2,3,2)':>14}")
    table = {}
    for ell in (3, 4, 5, 6):
        for i_in in (True, False):
            if not i_in and ell == 6:
                continue
            i = 0 if i_in else ell
            A, res = count(ell, i)
            allpairs = sum(1 for w in res if all(len(a) == 2 for a in w))
            pat = sum(1 for w in res if all(len(w[j]) == (3 if j % 2 == 0 else 2) for j in range(6)))
            table[(ell, i_in)] = len(res)
            print(f"{ell:>3} {('in' if i_in else 'out'):>7} {len(A):>10} {len(res):>8} {allpairs:>10} {pat:>14}")
    expect = {(3, True): 70194, (3, False): 11888, (4, True): 18746, (4, False): 2164,
              (5, True): 3720, (5, False): 380, (6, True): 510}
    print()
    ok = True
    for key, v in expect.items():
        got = table.get(key)
        if got != v: ok = False
        print(f"  ell={key[0]} centre {'in' if key[1] else 'out'}: reported {v}, reproduced {got}  "
              + ("OK" if got == v else "MISMATCH"))
    print("\nall counts reproduced:", ok)

main()
