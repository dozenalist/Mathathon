"""Two-centre and multi-centre check at k=6 for the four-cycle stratum.

Class: 'sector palette systems' -- at each centre the palette map is constant on the six
sectors [j*kappa,(j+1)*kappa) of the R-orbit, values chosen from the 33 admissible palettes of a
four-cycle centre (palette bound + (6.2)).  Constraints
  (b) consecutive-sector values disjoint                                    (5.7)
  (c) no two values have union I                                            (5.2)
  (d) mechanism silence at sector offsets 3 and 4                          (Theorem 2)
  (e) centres at distance exactly 1 have sector-wise disjoint palettes      (5.3), s = f
This is a *subclass* of all palette systems, so a SAT answer is a genuine model of the constraint
level; an UNSAT answer is a statement about this class only.
"""
from itertools import combinations
from collections import Counter
import random, sys, time

k = 6
edges = [frozenset({i, (i+1) % 4}) for i in range(4)]
adm = []
for sz in range(1, k-2):
    for p in combinations(range(k), sz):
        p = frozenset(p)
        if not any(p <= e for e in edges):
            adm.append(p)
adm.sort(key=lambda s: (len(s), sorted(s)))
mask = [sum(1 << i for i in p) for p in adm]
N = len(adm)

def disjoint(a, b): return (mask[a] & mask[b]) == 0
def union_ok(a, b): return bin(mask[a] | mask[b]).count("1") < k
def mech_ok(a, b):
    if mask[a] & mask[b]: return True
    return bin(mask[a]).count("1") + bin(mask[b]).count("1") <= k-3

def valid_sequence(v):
    if any(not disjoint(v[i], v[(i+1) % 6]) for i in range(6)): return False
    if any(not union_ok(v[i], v[j]) for i in range(6) for j in range(i+1, 6)): return False
    for i in range(6):
        for off in (3, 4):
            if not mech_ok(v[i], v[(i+off) % 6]): return False
    return True

print("k=6, four-cycle centre, 6-sector palette systems")
print("  admissible palettes:", N)

# ---------------------------------------------------------------- explicit models
print("\n--- explicit models (bright-line certificates) ---")
def show(name, seqs):
    print(f"\n{name}")
    for nm, s in seqs.items():
        print(f"   {nm}: " + "  ".join(str(sorted(adm[a])) for a in s))
        assert valid_sequence(s), nm + " violates (a)-(d)"
    ok = True
    names = sorted(seqs)
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            A = seqs[names[i]]; B = seqs[names[j]]
            if any(not disjoint(A[s], B[s]) for s in range(6)): ok = False
    print("   sector-wise disjoint on every pair of centres:", ok)
    return ok

one = {"x": (adm.index(frozenset({4})), adm.index(frozenset({0, 2})))*3}
one = {"x": tuple([adm.index(frozenset({4})), adm.index(frozenset({0,2}))]*3)}
show("one centre (Theorem 4 of RESULT.md):", one)

two = {"x": tuple([adm.index(frozenset({4})), adm.index(frozenset({0,2}))]*3),
       "y": tuple([adm.index(frozenset({5})), adm.index(frozenset({1,3}))]*3)}
show("two centres at distance 1 (the translation exclusion (5.3)):", two)

three = {"x": tuple([adm.index(frozenset({4})), adm.index(frozenset({5}))]*3),
         "y": tuple([adm.index(frozenset({5})), adm.index(frozenset({0,2}))]*3),
         "z": tuple([adm.index(frozenset({0,2})), adm.index(frozenset({4}))]*3)}
show("three centres pairwise at distance 1 (a unit triangle of four-cycle centres):", three)

# ---------------------------------------------------------------- cliques / homomorphisms
def compatible(A, B):
    return all(disjoint(A[s], B[s]) for s in range(6))

print("\n--- search for larger centre configurations ---")
# rebuild the valid-sequence list (needed for the search)
valid = []
def extend(v, depth):
    if depth == 6:
        if disjoint(v[5], v[0]) and valid_sequence(tuple(v)):
            valid.append(tuple(v))
        return
    for a in range(N):
        if depth > 0 and not disjoint(v[depth-1], a): continue
        ok = True
        for i in range(depth):
            if not union_ok(v[i], a): ok = False; break
        if not ok: continue
        for i in range(depth):
            if (depth - i) % 6 in (3, 4) and not mech_ok(v[i], a): ok = False; break
            if (i - depth) % 6 in (3, 4) and not mech_ok(v[i], a): ok = False; break
        if not ok: continue
        v.append(a); extend(v, depth+1); v.pop()
extend([], 0)
print("  valid sector sequences:", len(valid))

def find_hom(n, pairs, tries=200000, seed=0):
    """randomised greedy with restarts: hom from the centre graph into the compatibility graph"""
    rnd = random.Random(seed)
    for _ in range(tries):
        order = list(range(n)); rnd.shuffle(order)
        asg = {}
        ok = True
        for c in order:
            nb = [asg[d] for (p, q) in pairs
                  for d in ((q,) if p == c else (p,) if q == c else ()) if d in asg]
            for _ in range(400):
                cand = valid[rnd.randrange(len(valid))]
                if all(compatible(cand, x) for x in nb):
                    asg[c] = cand; break
            else:
                ok = False; break
        if ok: return asg
    return None

moser = [(0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,4),(3,5),(4,5),(4,6),(5,6)]
for name, n, pairs in [("4 centres forming a unit-distance K_3 plus a pendant", 4,
                        [(0,1),(1,2),(0,2),(2,3)]),
                       ("Moser spindle (7 centres, chi = 4)", 7, moser)]:
    t0 = time.time()
    asg = find_hom(n, pairs, tries=200, seed=1)
    print(f"\n  {name}: {'SAT' if asg else 'not found'}   ({time.time()-t0:.1f}s)")
    if asg:
        for c in sorted(asg):
            print("     centre", c, ":", [sorted(adm[v]) for v in asg[c]])
        bad = [(p, q) for (p, q) in pairs if not compatible(asg[p], asg[q])]
        print("     all unit-distance pairs sector-wise disjoint:", not bad)
        print("     every centre's sequence satisfies (a)-(d):",
              all(valid_sequence(asg[c]) for c in asg))
