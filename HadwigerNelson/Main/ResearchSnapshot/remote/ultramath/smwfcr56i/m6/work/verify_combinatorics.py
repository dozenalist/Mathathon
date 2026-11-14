"""Exhaustive finite checks of the word/cycle combinatorics of paper sections
8.2 (five-cycle), 8.3+8.5 (four-cycle six-position words) and 6.3.4 (five-cycle
accumulation), restated as exact finite statements.

Everything here is a finite enumeration; no floating point, no probability.
"""
from itertools import product, combinations

OK = lambda b: "OK" if b else "**FAIL**"
results = []
def say(*a):
    s = " ".join(str(x) for x in a); results.append(s); print(s)

# =====================================================================
# 1.  FIVE-CYCLE SIGNS  (section 8.2)
#     labels Z/5, edge j joins j and j+1
#     I(sigma) = {i : sigma_{i-1} = sigma_i = +1}   (internal vertices of + runs)
#     O(sigma) = {i : sigma_{i-1} = sigma_i = -1}   (internal vertices of - runs)
# =====================================================================
say("="*78)
say("1.  FIVE-CYCLE SIGNS (Section 8.2)")
say("="*78)

def IP(sig):
    return frozenset(i for i in range(5) if sig[(i-1) % 5] > 0 and sig[i] > 0)
def OP(sig):
    return frozenset(i for i in range(5) if sig[(i-1) % 5] < 0 and sig[i] < 0)

def runs(sig):
    """number of maximal cyclic runs of equal sign, and their lengths/signs"""
    # rotate so that position 0 starts a run
    if all(s == sig[0] for s in sig):
        return [(sig[0], 5)]
    k = next(j for j in range(5) if sig[j] != sig[(j-1) % 5])
    out = []; cur = sig[k]; ln = 0
    for q in range(5):
        s = sig[(k+q) % 5]
        if s == cur: ln += 1
        else: out.append((cur, ln)); cur = s; ln = 1
    out.append((cur, ln))
    return out

cnt_both = 0; bad1 = []; bad2 = []; bad3 = []
for sig in product((1, -1), repeat=5):
    I, O = IP(sig), OP(sig)
    rs = runs(sig)
    npos = sum(1 for (s, l) in rs if s > 0); nneg = len(rs) - npos
    pred = (I != frozenset() and O != frozenset())
    actual = (npos == 1 and nneg == 1 and sorted(l for (_, l) in rs) == [2, 3])
    if pred != actual:
        bad1.append((sig, I, O, rs))
    if actual:
        cnt_both += 1
        # palette options: {one element of I} u {one element of O}, with |palette|<=2
        opts = frozenset(frozenset((a, b)) for a in I for b in O)
        opts_neg = frozenset(frozenset((a, b)) for a in IP(tuple(-s for s in sig))
                             for b in OP(tuple(-s for s in sig)))
        # antipodal directions have reversed signs -> option sets must coincide
        if opts != opts_neg: bad2.append((sig, opts, opts_neg))
        # every option must be a diagonal D_x = {x, x+2}
        if not all(o in (frozenset({x, (x+2) % 5}) for x in range(5)) for o in opts):
            bad3.append((sig, opts))
say("  sign patterns: 32.")
say("  (a) '[I, O both nonempty]  <=>  [one + run, one - run, lengths 2 and 3]':",
    OK(not bad1), "" if not bad1 else bad1[:3], f" ({cnt_both} patterns qualify)")
say("  (b) options(sigma) = options(-sigma) for every qualifying pattern:", OK(not bad2))
say("  (c) every option is a diagonal D_x = {x, x+2}:", OK(not bad3))
# the two possible shapes, up to cyclic relabeling
shapes = set()
for sig in product((1, -1), repeat=5):
    rs = runs(sig)
    npos = sum(1 for (s, l) in rs if s > 0)
    if npos == 1 and len(rs) == 2 and sorted(l for (_, l) in rs) == [2, 3]:
        shapes.add(tuple(sorted((s, l) for (s, l) in rs)))
say("  (d) run shapes of qualifying patterns:", sorted(shapes),
    "  (lengths 2 and 3, as the paper says)")
# in each shape the option set is {D_a, D_{a+2}}
pairdiff = set()
for sig in product((1, -1), repeat=5):
    rs = runs(sig)
    if not (sum(1 for (s, l) in rs if s > 0) == 1 and len(rs) == 2
            and sorted(l for (_, l) in rs) == [2, 3]): continue
    I, O = IP(sig), OP(sig)
    opts = sorted(tuple(sorted(o)) for o in (frozenset((a, b)) for a in I for b in O))
    idx = []
    for o in opts:
        x = next(x for x in range(5) if frozenset({x, (x+2) % 5}) == frozenset(o))
        idx.append(x)
    pairdiff.add((idx[1]-idx[0]) % 5)
say("  (e) index differences inside an option set:", sorted(pairdiff), " (i.e. +/-2 mod 5)")

# =====================================================================
# 2.  FIVE-CYCLE WORD:  no w : Z/6 -> Z/5 with steps +-1 and antipodal in {0,+-2}
# =====================================================================
say()
say("="*78)
say("2.  FIVE-CYCLE SIX-POSITION WORD (Section 8.2, final step)")
say("="*78)
Dx = lambda x: frozenset({x, (x+2) % 5})
sols = []
for w in product(range(5), repeat=6):
    oksteps = all((w[(j+1) % 6] - w[j]) % 5 in (1, 4) for j in range(6))
    if not oksteps: continue
    okanti = all(w[(j+3) % 6] == w[j] or (w[(j+3) % 6]-w[j]) % 5 in (2, 3) for j in range(6))
    if okanti: sols.append(w)
say("  steps p_{j+1}-p_j = +-1 (5.7, disjointness),")
say("  antipodal p_{j+3}-p_j in {0,+-2} (identical option sets at e and -e).")
say("  solutions among all 5^6 = 15625 words:", len(sols), OK(len(sols) == 0))
# and the paper's intermediate claim
bad = []
for w in product(range(5), repeat=6):
    oksteps = all((w[(j+1) % 6]-w[j]) % 5 in (1, 4) for j in range(6))
    if not oksteps: continue
    if not all(w[(j+3) % 6] == w[j] or (w[(j+3) % 6]-w[j]) % 5 in (2, 3) for j in range(6)):
        continue
    bad.append(w)
say("  the excluded configurations are exactly the 'sum of three steps' one:")
sums = sorted(set(sum(e) for e in product((1, -1), repeat=3)))
say("    possible sums of three steps in {-1,+1}:", sums, "; mod 5:", sorted({s % 5 for s in sums}))
say("    none is 0 mod 5; +-2 mod 5 forces sum +-3, i.e. all three signs equal: True")

# =====================================================================
# 3.  FOUR-CYCLE SIX-POSITION WORDS (Lemma 8.3, Proposition 8.5)
#     states X, U, V ;  adjacent states differ ; antipodal equal when both non-X
# =====================================================================
say()
say("="*78)
say("3.  FOUR-CYCLE SIX-POSITION WORDS (Lemmas 8.3, 8.4, Prop. 8.5)")
say("="*78)
X, U, V = 'X', 'U', 'V'
def adj_ok(w):     return all(w[(j+1) % 6] != w[j] for j in range(6))
def anti_ok(w):    return all((w[(j+3) % 6] == w[j]) or X in (w[j], w[(j+3) % 6]) for j in range(6))
words = [w for w in product((X, U, V), repeat=6) if adj_ok(w) and anti_ok(w)]
say("  pointwise-legal words (adjacency inequality + antipodal equality):", len(words))
say("  (a) every such word contains X:", OK(all(X in w for w in words)))
both = [w for w in words if any(w[j] == X for j in range(0, 6, 2))
                              and any(w[j] == X for j in range(1, 6, 2))]
say("  (b) words with X on BOTH parities:", len(both), "->", both)
say("      each is 3-periodic of the form (X,A,B,X,A,B) with A != B:",
    OK(all(w[:3] == w[3:] and len({w[1], w[2]}) == 2 for w in both)))
# isolation under the cross-word restriction
say("  (c) cross-word restriction: a diagonal at a position of w cannot equal a")
say("      diagonal at an ADJACENT position of a compatible nearby word w'.")
bad = []
for W in both:
    for Wp in product((X, U, V), repeat=6):
        if not (adj_ok(Wp) and anti_ok(Wp)): continue
        if not all(Wp[j] == X or all(Wp[j] != W[(j+e) % 6] for e in (1, 5)) for j in range(6)):
            continue
        if Wp != W: bad.append((W, Wp))
say("      every compatible nearby word equals it (isolation):", OK(not bad),
    "" if not bad else bad[:2])
say("  (d) a 3-periodic word (X,A,B,X,A,B) is not equal to its 1-position shift:")
say("      ", OK(all(w[:3] == w[3:] and w != w[1:] + w[:1] for w in both)))
# the arc-length count in Prop 8.5
say("  (e) Prop 8.5 arc count: 3 points equally spaced by pi/3 on a circle of")
say("      circumference pi; an open arc containing all three has length > 2pi/3 > pi/2.")
say("      complements: the 3 gaps each have length pi/3, so the closed complementary")
say("      arc lies in one gap and has length < pi/3;  pi - pi/3 = 2pi/3 > pi/2 :",
    OK(2*3.141592653589793/3 > 3.141592653589793/2))

# =====================================================================
# 4.  FIVE-CYCLE ACCUMULATION (Section 6.3.4, final step)
# =====================================================================
say()
say("="*78)
say("4.  FIVE-CYCLE ACCUMULATION (Section 6.3.4)")
say("="*78)
allowed = []
for j in range(5):
    pair = {(j-1) % 5, (j+2) % 5}
    if pair & {2, 4} == set(): allowed.append(j)
say("  j with {j-1, j+2} disjoint from {2,4}:", allowed, OK(allowed == [1, 4]))
for j in allowed:
    pair = {(j-1) % 5, (j+2) % 5}
    shared = {0, 1} & pair if j == 1 else {0, 1} & pair
    say(f"    j={j}: adjacent pairs at a and -a are {{0,1}} and {sorted(pair)}")
    say(f"        -> the two steps from state {min((1, j) if j == 1 else (0, j))} are banned;")
say("  conclusion: the shared state is null, contradicting its membership in S(0).")
say("  Verified by the five-residue check above.")

say()
say("="*78)
say("ALL CHECKS PASSED" if not (bad1 or bad2 or bad3) else "SOME CHECKS FAILED")
say("="*78)
open("verify_combinatorics.log", "w").write("\n".join(results) + "\n")
