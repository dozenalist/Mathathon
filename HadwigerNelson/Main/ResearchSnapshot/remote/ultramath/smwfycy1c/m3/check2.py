#!/usr/bin/env python3
"""d3 independent re-check, bitmask implementation, asserts every headline number.

Exact integer set arithmetic only; no floats, no sympy needed (the objects are
subsets of Z/5Z and Z/6Z, so integer masks ARE the exact objects).
Exit status 0 iff everything asserted holds.
"""
import itertools, sys

M = 5
ALLMASK = (1 << M) - 1
def bits(m):
    return tuple(i for i in range(M) if m >> i & 1)
def Dmask(i):
    return (1 << (i % M)) | (1 << ((i + 2) % M))
def dinter(m):
    s = ALLMASK
    for i in bits(m):
        s &= Dmask(i)
    return s
def valid(m):
    return m != 0 and dinter(m) == 0
def adj(m):
    return any((m >> i & 1) and (m >> ((i + 1) % M) & 1) for i in range(M))
def nbr(m, i):
    return (m >> ((i - 1) % M) & 1) or (m >> ((i + 1) % M) & 1)

VALID = [m for m in range(1, ALLMASK + 1) if valid(m)]
MASK = lambda L: sum(1 << i for i in L)

facts = []
def A(name, cond, detail=""):
    facts.append((name, bool(cond), detail))

# ---- 0. basic structure ----
A("exactly 21 valid lists (10 of 31 excluded)", len(VALID) == 21, str(sorted(bits(m) for m in VALID)))
A("valid => contains adjacent index pair", all(adj(m) for m in VALID))
A("{2,4} is NOT valid: D_2 cap D_4 = {4}", dinter(MASK([2, 4])) == (1 << 4))
A("{2,3,4} is valid", valid(MASK([2, 3, 4])))
A("only valid list containing 2,4 that avoids 0,1 is {2,3,4}",
  [bits(m) for m in VALID if (m & MASK([2, 4])) == MASK([2, 4]) and not (m & MASK([0, 1]))] == [(2, 3, 4)])

# ---- 1. all triples (S0,S1,S5) ----
tri = []
for s0 in VALID:
    if (s0 & MASK([0, 1])) != MASK([0, 1]):
        continue
    for s1 in VALID:
        if s0 & s1:
            continue
        for s5 in VALID:
            if s0 & s5:
                continue
            if any(not nbr(s1, i) or not nbr(s5, i) for i in bits(s0)):
                continue
            tri.append((bits(s0), bits(s1), bits(s5)))
A("exactly one triple (S0,S1,S5)", len(tri) == 1, str(tri))
A("the triple is ({0,1},{2,3,4},{2,3,4})", tri == [((0, 1), (2, 3, 4), (2, 3, 4))])
forced1 = set.intersection(*[set(t[1]) for t in tri]) if tri else set()
poss1 = set().union(*[set(t[1]) for t in tri]) if tri else set()
A("S(1) forced exactly = S(5) forced exactly = {2,3,4}",
  sorted(forced1) == [2, 3, 4] and sorted(poss1) == [2, 3, 4], f"forced={sorted(forced1)} possible={sorted(poss1)}")

# ---- 2a. WEAK reading: S2 valid, {j-1,j+2} subset S2, S2 cap {2,4} = {} ----
weak = {}
for j in range(M):
    a, b = (j - 1) % M, (j + 2) % M
    weak[j] = [bits(s2) for s2 in VALID
               if (s2 & MASK([a, b])) == MASK([a, b]) and not (s2 & MASK([2, 4]))]
A("weak reading (paper: only 2,4 in S(1)): survivors exactly {1,4}",
  sorted(j for j in weak if weak[j]) == [1, 4],
  str({j: weak[j] for j in range(M)}))

# ---- 2b. STRONG reading: S1 = {2,3,4}, S2 valid, S2 cap S1 = {} ----
S1 = MASK([2, 3, 4])
strong = {}
for j in range(M):
    a, b = (j - 1) % M, (j + 2) % M
    strong[j] = [bits(s2) for s2 in VALID
                 if (s2 & MASK([a, b])) == MASK([a, b]) and not (s2 & S1)]
A("strong reading (S(1) = {2,3,4}): NO j survives",
  sorted(j for j in strong if strong[j]) == [], str({j: strong[j] for j in range(M)}))

# ---- 2c. faithful per-j search, no hand-derived {j-1,j+2}: positions (S1,S2,S3) ----
# S(3) valid hence >= an adjacent pair {j,j+1}; S(2) valid; adjacent positions disjoint;
# mutual neighbour conditions S1<->S2 and S2<->S3.
faithful = {}
for j in range(M):
    hits = []
    for s3 in VALID:
        if not ((s3 >> j & 1) and (s3 >> ((j + 1) % M) & 1)):
            continue
        for s2 in VALID:
            if s2 & S1 or s2 & s3:
                continue
            if any(not nbr(s2, i) for i in bits(s3)):
                continue
            if any(not nbr(s3, i) for i in bits(s2)):
                continue
            if any(not nbr(s2, i) for i in bits(S1)):
                continue                       # i in S1 needs neighbour in S2
            if any(not nbr(s3, i) for i in bits(S1)):
                continue
            hits.append((bits(s2), bits(s3)))
    faithful[j] = hits
A("faithful (S1,S2,S3) search with S1={2,3,4}: empty for EVERY j",
  all(not faithful[j] for j in range(M)), str({j: faithful[j] for j in range(M)}))

# ---- 3. full 6-position configuration, exhaustive corrected DFS ----
sols = []
def dfs(pos, cur):
    if len(sols) > 200:
        return
    if pos == 6:
        s5, s0 = cur[5], cur[0]
        if s5 & s0:
            return
        if any(not nbr(s0, i) for i in bits(s5)):
            return
        if any(not nbr(s5, i) for i in bits(s0)):
            return
        sols.append(tuple(bits(x) for x in cur))
        return
    for L in VALID:
        if pos == 0:
            if (L & MASK([0, 1])) != MASK([0, 1]):
                continue
        else:
            P = cur[pos - 1]
            if L & P:
                continue
            if any(not nbr(L, i) for i in bits(P)):     # each i in S(pos-1) meets S(pos)
                continue
            if any(not nbr(P, i) for i in bits(L)):     # each i in S(pos) meets S(pos-1)
                continue
        cur.append(L)
        dfs(pos + 1, cur)
        cur.pop()

dfs(0, [])
A("full 6-position configuration set is EMPTY", len(sols) == 0, str(sols[:3]))

# ---- 4. where exactly does the hypothesis set die? prefix (S0..S_{k-1}) searches ----
# mutual=False: only the problem statement's one-directional rule (i in S(r) needs a
#               neighbour in S(r+1)); mutual=True: the paper's rule applied at every
#               direction, i.e. also i in S(r+1) needs a neighbour in S(r).
def prefix_solvable(k, mutual):
    found = []
    def go(pos, cur):
        if found:
            return
        if pos == k:
            found.append(tuple(bits(x) for x in cur)); return
        for L in VALID:
            if pos == 0 and (L & MASK([0, 1])) != MASK([0, 1]):
                continue
            if pos > 0:
                P = cur[pos - 1]
                if L & P: continue
                if any(not nbr(L, i) for i in bits(P)): continue
                if mutual and any(not nbr(P, i) for i in bits(L)): continue
            cur.append(L); go(pos + 1, cur); cur.pop()
    go(0, [])
    return found[0] if found else None

pref1 = {k: prefix_solvable(k, False) for k in range(1, 7)}
prefm = {k: prefix_solvable(k, True) for k in range(1, 7)}
A("one-directional rule: (S0,S1) solvable = ({0,1},{2,3,4}); (S0,S1,S2) already empty",
  pref1[2] == ((0, 1), (2, 3, 4)) and pref1[3] is None, str(pref1))
A("mutual (paper) rule: ALREADY the pair (S(0),S(1)) is contradictory (k=2 empty)",
  prefm[1] is not None and prefm[2] is None and prefm[6] is None, str(prefm))
A("Level B kernel: in the forced triple, 3 in S(1) has NO neighbour in S(0)={0,1}",
  (3 in tri[0][1]) and not (nbr(MASK([0, 1]), 3)),
  "nbrs(3)={2,4}, S(0)={0,1}")

ok = True
for name, cond, detail in facts:
    print(("PASS " if cond else "FAIL ") + name + (("   [" + detail + "]") if detail and not cond else ""))
    ok = ok and cond

# ---- 5. by-hand chain, checked mechanically as set identities ----
print("\n--- by-hand chain ---")
print("D_2 =", sorted(bits(Dmask(2))), " D_4 =", sorted(bits(Dmask(4))),
      " D_2 cap D_4 =", sorted(bits(dinter(MASK([2, 4])))))
print("0 in S(0) needs neighbour 4 or 1 in S(1); 1 not in S(1) (S(1) cap S(0) = {}) => 4 in S(1)")
print("1 in S(0) needs neighbour 0 or 2 in S(1); 0 not in S(1) => 2 in S(1)")
print("S(1) valid and avoids 0,1 => S(1) subset {2,3,4}; with 2,4 => S(1) = {2,3,4}")
print("similarly S(5) = {2,3,4}; S(0) cap S(1) = {} => S(0) subset {0,1} => S(0) = {0,1}")
print("S(2) valid, S(2) cap S(1) = {} => S(2) subset {0,1}; but {j-1,j+2} has size 2 and")
print("j-1 != j+2 (mod 5); {0,1} needs j-1=0,j+2=1 (j=1 & j=4) or j-1=1,j+2=0 (j=2 & j=3): both impossible.")
print("")
print("Level B (paper's rule at every direction): 3 in S(1)={2,3,4} has neighbours {2,4},")
print("both already in S(1), so 3 has no neighbour in S(0)={0,1}; the pair (S(0),S(1)) is")
print("already contradictory: the whole Sec 6.3.4 hypothesis set is empty.")
print("\nALL CHECKS PASS" if ok else "\nSOME CHECK FAILED")
sys.exit(0 if ok else 1)
