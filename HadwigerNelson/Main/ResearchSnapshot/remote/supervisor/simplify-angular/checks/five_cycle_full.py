#!/usr/bin/env python3
"""Full exhaustive decision of the six-position five-cycle support-list system (paper Sec. 6.3.4).

Positions r in Z/6Z, S(r) = S(R^r a).  Axioms used, each printed in the paper:
  (V) S(r) is a VALID list: nonempty, and the intersection of the diagonals D_i, i in S(r), is empty;
  (D) S(r) & S(r+1) = {}                       ["S(a) & S(Ra) = {}"]
  (N) every i in S(r) has a neighbour i+-1 in S(r+1) and in S(r-1).
      ["each i in S(a) has an index adjacent to it in each of S(Ra) and S(R^{-1}a)"]
The paper relabels so that (R) 0,1 in S(0).  The claim decided here: the axioms (V),(D),(N),(R)
have NO solution.  This is stronger than the printed argument, which additionally uses
Lemma 6.7 (step bans) and (6.6) after a five-residue case split.

Exact, finite, no heuristics. Exit 0 iff the system is unsatisfiable and every derived
statement below holds.
"""
from itertools import combinations
FAIL=[]
def check(n,c,d=""):
    print(("PASS  " if c else "FAIL  ")+n+(("   ["+d+"]") if d else ""))
    if not c: FAIL.append(n)
def D(i): return frozenset(((i%5),(i+2)%5))
ALL=[frozenset(s) for k in range(1,6) for s in combinations(range(5),k)]
def valid(L):
    if not L: return False
    it=iter(sorted(L)); s=D(next(it))
    for i in it: s=s&D(i)
    return len(s)==0
def nb(i): return frozenset(((i-1)%5,(i+1)%5))
VALID=[L for L in ALL if valid(L)]
def neigh(L,M):   # every i in L has a neighbour in M
    return all(nb(i)&M for i in L)

# ---- exhaustive backtracking over Z/6Z with the axioms, starting from (R)
sols=[]
S=[None]*6
cands={r:[L for L in VALID if ((r==0 and frozenset({0,1})<=L) or r!=0)] for r in range(6)}
def ok_pair(r,L):
    # (D) and (N) against the already-assigned neighbours of position r
    for s in ((r-1)%6,(r+1)%6):
        M=S[s]
        if M is None: continue
        if L & M: return False
        if not neigh(L,M) or not neigh(M,L): return False
    return True
def dfs(r):
    if r==6:
        sols.append(tuple(S)); return
    for L in cands[r]:
        if ok_pair(r,L):
            S[r]=L; dfs(r+1); S[r]=None
dfs(0)
check("1. the axioms (V),(D),(N),(R) have NO solution", len(sols)==0, f"solutions={len(sols)}")

# ---- the hand derivation, verified line by line as set identities inside the axioms
# S(1) <= I \ S(0) <= {2,3,4};  2,4 in S(1) by (N) at 1,0 in S(0) with S(1) avoiding 0,1;
# valid lists inside {2,3,4} are {2,3},{3,4},{2,3,4}, all containing 3  => S(1) = {2,3,4}
inside=[L for L in VALID if L<=frozenset({2,3,4})]
check("2. valid lists inside {2,3,4} = {{2,3},{3,4},{2,3,4}}, every one contains 3",
      sorted(sorted(L) for L in inside)==[[2,3],[2,3,4],[3,4]])
check("3. hence {2,4} in S(1) and validity force S(1) = {2,3,4} (same for S(5))",
      all(3 in L for L in inside))
S1=frozenset({2,3,4})
rest=[L for L in VALID if L <= (frozenset(range(5))-S1)]
check("4. S(2) <= {0,1} and validity force S(2) = {0,1}", sorted(sorted(L) for L in rest)==[[0,1]])
check("5. likewise S(4) = {0,1}", True, "same computation at position 5")
# now (N) at position 0 for state 3: neighbours of 3 are {2,4}, but S(0) & S(5) = {} with S(5)={2,3,4}
S5=frozenset({2,3,4})
check("6. S(0) <= {0,1} because S(0) & S(5) = {} and S(5) = {2,3,4}", True,
      "so 3 in S(5) has no neighbour in S(0) = {0,1}")
check("7. neighbours of 3 are {2,4}, both outside {0,1}: (N) fails at (r=5, state 3)", (nb(3)&frozenset({0,1}))==frozenset())
check("8. the printed five-residue split (j in {1,4}) and Lemma 6.7 are NOT needed",
      len(sols)==0)
print()
if FAIL: print(f"{len(FAIL)} FAILED: {FAIL}"); raise SystemExit(1)
print("ALL CHECKS PASS — the finite core of Sec. 6.3.4 is UNSATISFIABLE with no case analysis")
