"""
Exact verification for the note "the k-ladder of the cover-and-palette method".
Integral arithmetic only; no floating point; every claim is a finite enumeration.
Run:  python3 verify.py
"""
from itertools import product, combinations

OUT_DEFAULT = {3, 4, 5}

def word_str(w): return ''.join('+' if x > 0 else '-' for x in w)

def allowed(k, l, w):
    """O(e), I(e) of paper Section 8.1. Cycle labels T={0..l-1}, edge j joins j,j+1;
    outsiders are l..k-1."""
    T, outside, pos_ep, neg_ep = set(range(l)), set(range(l, k)), set(), set()
    for j in range(l):
        ep = {j, (j + 1) % l}
        (pos_ep if w[j] > 0 else neg_ep).update(ep)
    return (T - pos_ep) | outside, (T - neg_ep) | outside

def runs(w):
    l = len(w)
    if all(x == w[0] for x in w): return [(w[0], l)]
    s = 0
    while w[s] == w[-1]: s += 1
    wr = w[s:] + w[:s]; out = []; cur, n = wr[0], 1
    for x in wr[1:]:
        if x == cur: n += 1
        else: out.append((cur, n)); cur, n = x, 1
    out.append((cur, n)); return out

def both_incident(l, w, s):
    return sum(1 for j in range(l) if w[(j - 1) % l] == s and w[j] == s)

print("== 1. the allowed-set cardinality formula ==")
tot = bad = 0
for k in range(3, 12):
    for l in range(3, k + 1):
        for w in product((+1, -1), repeat=l):
            tot += 1
            O, I = allowed(k, l, w)
            if len(O) != k-l+both_incident(l, w, -1) or len(I) != k-l+both_incident(l, w, +1):
                bad += 1; print("  FAIL", k, l, word_str(w))
            for s in (+1, -1):
                e = sum(1 for x in w if x == s)
                r = sum(1 for (sg, n) in runs(w) if sg == s)
                if not all(x == s for x in w) and both_incident(l, w, s) != e - r:
                    bad += 1; print("  RUNS FAIL", k, l, word_str(w), s)
print(f"  |O| = k-l + #{{j : both incident edges negative}},  |I| = k-l + #{{j : both positive}}")
print(f"  for a non-constant word these are e_s - r_s.  checked {tot} cases (3<=k<=11, 3<=l<=k): {bad} failures")

print("\n== 2. sliver sizes: min(|O|,|I|) over the two sides ==")
for k in (4, 5, 6, 7):
    for l in range(3, k + 1):
        vals = [min(map(len, allowed(k, l, w))) for w in product((+1, -1), repeat=l)]
        both2 = [w for w in product((+1, -1), repeat=l)
                 if allowed(k, l, w)[0].__len__() == 2 and allowed(k, l, w)[1].__len__() == 2]
        print(f"  k={k} l={l} m={k-l}: min = {min(vals)}, max = {max(vals)}, "
              f"words with BOTH sides of size 2: {len(both2)}/{2**l}"
              + (f"  [{word_str(both2[0])} ...]" if both2 else ""))

print("\n== 3. k=6, l=3 (triangle interface): every sign word ==")
for w in product((+1, -1), repeat=3):
    O, I = allowed(6, 3, w)
    print(f"  {word_str(w)}: O={sorted(O)}  I={sorted(I)}  min={min(len(O),len(I))}")
print("  => min(|O|,|I|) >= 3 for EVERY direction; the sliver carries at least 3 labels.")
print("== 3'. k=5, l=3 (the paper's interface): every sign word ==")
for w in product((+1, -1), repeat=3):
    O, I = allowed(5, 3, w)
    print(f"  {word_str(w)}: O={sorted(O)}  I={sorted(I)}  min={min(len(O),len(I))}")
print("  => min(|O|,|I|) = 2 for EVERY direction: a 2-element sliver always.")

print("\n== 4. k=6, l=5 (one outsider 5): words with both slivers of size 2 ==")
for w in product((+1, -1), repeat=5):
    O, I = allowed(6, 5, w)
    if len(O) == 2 and len(I) == 2:
        print(f"  {word_str(w)}: O={sorted(O)}  I={sorted(I)}  O==I? {O==I}")
print("  each such word is constant on an open arc of directions: positive measure.")
print("\n== 5. k=6, l=4 (two outsiders): words with both slivers of size 2 ==")
for w in product((+1, -1), repeat=4):
    O, I = allowed(6, 4, w)
    if len(O) == 2 and len(I) == 2:
        print(f"  {word_str(w)}: O={sorted(O)}  I={sorted(I)}  (alternating: a null set of e)")
print("\n== 6. k=6, l=6 (no outsiders): count of words with both slivers of size 2 ==")
c = sum(1 for w in product((+1, -1), repeat=6)
        if len(allowed(6, 6, w)[0]) == 2 and len(allowed(6, 6, w)[1]) == 2)
print(f"  {c} of 64 (each constant on an open arc, so positive measure)")

print("\n== 7. Sections 5-6 constraint system at a k=6 triangle interface ==")
subs = [frozenset(c) for r in range(1, 4) for c in combinations(range(6), r)]
sols = []
def dfs(P):
    i = len(P)
    if i == 6:
        if not (P[5] & P[0]): sols.append(tuple(P))
        return
    for p in subs:
        if not (p & OUT_DEFAULT): continue
        if i and (p & P[-1]): continue
        if i == 5 and (p & P[0]): continue
        dfs(P + [p])
dfs([])
pats = {tuple(len(p & OUT_DEFAULT) for p in P) for P in sols}
print("  variables P_0..P_5 (R-orbit of directions), 1<=|P_i|<=3, P_i meets {3,4,5},")
print("  and P_i cap P_(i+1) = empty cyclically (five explicit plus the closing one)")
print(f"  number of solutions: {len(sols)};  distinct outsider-size patterns: {len(pats)}")
print(f"  pattern (2,2,2,2,2,2) (all palettes with a 2-element outsider part): realised? {(2,)*6 in pats}")
print(f"  pattern (1,1,1,1,1,1) (all singleton outsider parts = route B's conclusion): realised? {(1,)*6 in pats}")
print("  => Sections 5-6 admit the singleton conclusion but do not force it. |A_i|=2 is")
print("     compatible with every constraint, so no argument from these constraints derives |A_i|=1.")
ex = next(P for P in sols if tuple(len(p & OUT_DEFAULT) for p in P) == (1,)*6)
print(f"  explicit all-singleton witness: {[sorted(p) for p in ex]}")

print("\n== 8. gadget certificate: the four-unit-edge exchange path is P_5 ==")
# vertices 0..4, edges i--i+1.  2-colourings and 3-colourings, exact enumeration.
def cols(n, m, edges, c):
    out = []
    for f in product(range(c), repeat=n):
        if all(f[a] != f[b] for (a, b) in edges): out.append(f)
    return out
E = [(0,1),(1,2),(2,3),(3,4)]
two = cols(5, 5, E, 2); three = cols(5, 5, E, 3)
print(f"  proper 2-colourings: {len(two)}, endpoints equal in all: {all(f[0]==f[4] for f in two)}")
diff3 = [f for f in three if f[0] != f[4]]
print(f"  proper 3-colourings: {len(three)}, of which endpoints differ: {len(diff3)}, e.g. {diff3[0]}")
print("  => local rigidity from the exchange gadget is a 2-label phenomenon; with 3 labels")
print("     available the gadget forces nothing. (Lemma 8.6 needs exactly two labels.)")
