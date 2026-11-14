"""
The (k=6, l=4) transplant of the (k=5, l=3) mechanism, in exact rational arithmetic.

Setting: k = 6 labels, interface cycle of length l = 4, cycle labels T = {0,1,2,3},
outsiders {4,5}, interface rays v_0..v_3.  The sign word at a direction e is
w_j = sign(e . v_j); it is constant on each angular arc cut out by the perpendicular
lines of the rays, so every realisable word occupies an open arc.

Balanced word := a sign word in which NEITHER sign class is a vertex cover of the
4-cycle, i.e. both allowed sets have size >= 3 = k-l+1.  The four balanced words
are ++--, -++-, +--+, --++ (each has w_0 != w_2 and w_1 != w_3).
"""
from fractions import Fraction as F
from itertools import product

def allowed(k, l, w):
    T, outside, pos, neg = set(range(l)), set(range(l, k)), set(), set()
    for j in range(l):
        ep = {j, (j+1) % l}
        (pos if w[j] > 0 else neg).update(ep)
    return (T - pos) | outside, (T - neg) | outside

def word(rays, e):
    out = []
    for (a, b) in rays:
        s = e[0]*a + e[1]*b
        if s == 0: return None
        out.append(1 if s > 0 else -1)
    return tuple(out)

BAL = {w for w in product((+1, -1), repeat=4)
       if len(allowed(6, 4, w)[0]) >= 3 and len(allowed(6, 4, w)[1]) >= 3}
print("balanced words at k=6, l=4 (both allowed sets of size >= 3):",
      sorted(''.join('+' if x > 0 else '-' for x in w) for w in BAL), f"({len(BAL)} of 16)")

print("\n== A. paired rays: v_0 = v_2.  The realisable words are then (s0,s1,s0,s1). ==")
ok = True
for s0, s1 in product((+1, -1), repeat=2):
    w = (s0, s1, s0, s1)
    O, I = allowed(6, 4, w)
    good = (len(O) == 2 or len(I) == 2) and min(len(O), len(I)) == 2
    ok &= good
    print(f"  {''.join('+' if x>0 else '-' for x in w)}: O={sorted(O)} |O|={len(O)}  "
          f"I={sorted(I)} |I|={len(I)}   2-element sliver: {good}")
print("  => with v_0 = v_2 no balanced word is realisable, and the two-element sliver, when it")
print("     exists, is ALWAYS the outsider pair {4,5}:",
      all((allowed(6,4,(s0,s1,s0,s1))[0] == {4,5} or allowed(6,4,(s0,s1,s0,s1))[1] == {4,5})
          for s0, s1 in product((+1,-1), repeat=2)))
print("     (indeed w_0 != w_2 is false for all four balanced words, so requiring v_0 = v_2")
print("      excludes exactly them; the same holds for v_1 = v_3.)")

print("\n== B. the hypothesis is not automatic: a general-position rational arrangement ==")
rays = [(F(1), F(0)), (F(1), F(1)), (F(0), F(1)), (F(-1), F(2))]
print("  rays:", [(str(a), str(b)) for a, b in rays], "- four distinct projective classes")
found = {}
for x in range(-40, 41):
    for y in range(-40, 41):
        if x == 0 and y == 0: continue
        e = (F(x), F(y))
        w = word(rays, e)
        if w is not None and w in BAL and w not in found:
            found[w] = e
for w, e in sorted(found.items(), key=lambda t: t[0]):
    print(f"  balanced word {''.join('+' if x>0 else '-' for x in w)} at e = ({e[0]}, {e[1]})"
          f"  [exact rational]; allowed sets {sorted(allowed(6,4,w)[0])}, {sorted(allowed(6,4,w)[1])}")
print("  => in general position the sliver is 3-coloured on a positive-measure set of directions,")
print("     so the transfer below genuinely needs the hypothesis v_0 = v_2.")

print("\n== C. consequences for the mechanism (proved in the note, not here) ==")
print("  (8.1) + a {4,5}-sliver at every direction  =>  P_x(e) cap {4,5} != empty for all e not in B;")
print("  (5.7) at Re  =>  |P_x(e) cap {4,5}| = 1 and s(Re) != s(e): a global binary flip.")
print("  Lemma 8.6 needs two strips carrying the SAME two labels: {4,5} on both sides of the")
print("  R-pair, whatever the sides are; it therefore transfers verbatim.")
print("  Lemma 8.7 needs at most three projective classes among the rays: here at most 3.")
print("  Lemma 8.8's region carries k-2 labels:")
for kk in (5, 6):
    print(f"    k={kk}: {kk-2} labels, gadget needs chi >= {kk-1}"
          + ("  -> Moser spindle (chi=4), paper (8.5): available"
             if kk == 5 else "  -> explicit finite 5-chromatic unit-distance graph: NOT available"))
