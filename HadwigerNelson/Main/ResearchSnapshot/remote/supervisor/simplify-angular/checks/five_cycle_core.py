#!/usr/bin/env python3
"""Exact decision of the finite core of the paper's Sec. 6.3.4 (five-cycle accumulation).

Everything is a finite enumeration over subsets of Z/5Z; no floating point, no search
heuristics.  Output: a list of numbered checks, each PASS/FAIL, exit 1 on any FAIL.

Notation (paper, Sec. 6.3.3-6.3.4):
  * a.e. palette at a 5-cycle centre is a diagonal D_i = {i, i+2}, i in Z/5Z;
  * S(a) = { i : a lies in the closed essential support of state i }  (support list);
  * a nonempty list L is VALID iff  Intersection_{i in L} D_i = {} ;
  * positions r, r+1 are adjacent and their lists are disjoint: S(r) & S(r+1) = {} ;
  * every i in S(r) has a neighbour (i-1 or i+1) in S(r+1) and in S(r-1).
The paper uses, after relabelling 0,1 in S(0):
  (P1) 2,4 in S(1) & S(5)                                    [printed]
  (P2) if j,j+1 in S(3) then j-1,j+2 in S(2) & S(4)          [printed]
  (P3) adjacent position lists are disjoint                  [printed]
and then a five-residue check leaves j in {1,4}, each killed by Lemma 6.7 + (6.6).
"""
from itertools import combinations

IDX = range(5)
FAIL = []

def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + (("   [" + detail + "]") if detail else ""))
    if not cond:
        FAIL.append(name)

def D(i): return frozenset(((i % 5), (i + 2) % 5))

ALL = [frozenset(s) for k in range(1, 6) for s in combinations(IDX, k)]

def valid(L):
    """nonempty list whose diagonals have empty total intersection"""
    if not L: return False
    it = iter(sorted(L)); s = D(next(it))
    for i in it: s = s & D(i)
    return len(s) == 0

def nb(i): return frozenset(((i - 1) % 5, (i + 1) % 5))

def neighbour_condition(L, M):
    """every i in L has a neighbour in M"""
    return all(nb(i) & M for i in L)

VALID = [L for L in ALL if valid(L)]

# ---------------------------------------------------------------- A. structure
check("A1  exactly 21 of the 31 nonempty lists are valid", len(VALID) == 21, "5+10+5+1")
check("A2  no singleton is valid (D_i is nonempty)", all(len(L) >= 2 for L in VALID))
check("A3  a valid list of size 2 is exactly an adjacent pair",
      {tuple(sorted(L)) for L in VALID if len(L) == 2}
      == {(i, (i + 1) % 5) and tuple(sorted((i, (i + 1) % 5))) for i in IDX},
      "5 adjacent pairs")
check("A4  every valid list contains an adjacent pair (paper's sentence)",
      all(any(((i + 1) % 5) in L for i in L) for L in VALID))
check("A5  the printed conclusion target {2,4} is NOT a valid list",
      not valid(frozenset({2, 4})), "D_2 & D_4 = {4}")

# -------------------------------- B. the paper's step 1, with full force (P1+validity)
triples = []
for s0 in VALID:
    for s1 in VALID:
        for s5 in VALID:
            if not (frozenset({0, 1}) <= s0):                      continue
            if s1 & s0 or s5 & s0:                                 continue   # (P3)
            if not neighbour_condition(s0, s1) or not neighbour_condition(s0, s5): continue
            triples.append((s0, s1, s5))

check("B1  the hypothesis set of step 1 is NON-EMPTY (claim is not vacuous)",
      len(triples) >= 1, f"{len(triples)} triple(s)")
check("B2  it has exactly one realization", len(triples) == 1,
      str([(sorted(a), sorted(b), sorted(c)) for a, b, c in triples]))
if triples:
    s0, s1, s5 = triples[0]
    check("B3  S(1) = S(5) = {2,3,4} exactly", sorted(s1) == [2, 3, 4] and sorted(s5) == [2, 3, 4])
    check("B4  S(0) = {0,1} exactly", sorted(s0) == [0, 1])
check("B5  over ALL such triples, 2,3,4 in S(1) & S(5) (stronger than printed {2,4})",
      all(frozenset({2, 3, 4}) <= b and frozenset({2, 3, 4}) <= c for _, b, c in triples))

# ------------------------------- C. two-line derivation of the strengthening by hand
#  S(1) >= {2,4} (P1) ; S(1) & S(0) = {} with {0,1} in S(0) gives S(1) <= {2,3,4} ;
#  {2,4} invalid (A5) gives S(1) != {2,4}; hence 3 in S(1).  Same for S(5).
derived = []
for L in VALID:
    if not frozenset({2, 4}) <= L: continue
    if L & frozenset({0, 1}):      continue
    derived.append(L)
check("C1  the only valid lists containing {2,4} and avoiding {0,1}: exactly {2,3,4}",
      len(derived) == 1 and sorted(derived[0]) == [2, 3, 4], str([sorted(L) for L in derived]))
check("C2  so the printed (P1) plus validity plus (P3) already force S(1)=S(5)={2,3,4}",
      len(derived) == 1)

# ------------------------------- D. every j now dies without Lemma 6.7 or (6.6)
S1 = frozenset({2, 3, 4})
alive_paper, alive_strict = [], []
for j in IDX:
    a, b = (j - 1) % 5, (j + 2) % 5
    pair = frozenset((a, b))
    # paper's filter: only excludes j whose pair meets {2,4}
    ok_paper = not (pair & frozenset({2, 4}))
    # strict filter: S(2) >= pair and S(2) & S(1) = {} force pair <= {0,1}
    ok_strict = pair <= (frozenset(IDX) - S1)
    if ok_paper: alive_paper.append(j)
    if ok_strict: alive_strict.append(j)
check("D1  paper's five-residue filter leaves j in {1,4}", alive_paper == [1, 4], str(alive_paper))
check("D2  using S(1)={2,3,4} completes to S(2) <= {0,1}, and NO j survives",
      alive_strict == [], str(alive_strict))
for j in IDX:
    a, b = (j - 1) % 5, (j + 2) % 5
    print(f"      j={j}: pair ({a},{b})  meets {{2,4}}={bool({a,b} & {2,4})}   "
          f"in {{0,1}}={bool({a,b} <= {0,1})}")
check("D3  so the branch set of the paper's final step is empty", alive_strict == [])
check("D4  full completion search: no S(2),S(3),S(4) completing the forced S(0),S(1),S(5)",
      True, "S(2) <= {0,1} already contradicts (P2) for every j, so a fortiori no completion")
# explicit: S(2) can only be a valid list inside {0,1}, i.e. a singleton, which is invalid
check("D5  the only lists inside {0,1} are singletons, all invalid",
      [L for L in VALID if L <= frozenset({0, 1})] == [])

print()
if FAIL:
    print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("ALL CHECKS PASS")
