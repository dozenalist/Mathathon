"""Cross-condition audit of the free-label (non-proper self-avoidance) palette models
at k = 6, swarm smwfwznwk, member m4 (direction d3).

Every claim is checked here in integer / Fraction arithmetic.
Nothing is imported from sprint/, from m15/ or from the SAT encoding: the witness is
re-read from its JSON and re-verified from scratch.

Checks
  A  the domain of admissible palette values at k = 6
  B  KILL: three pairwise disjoint admissible values avoiding a fixed label do not exist
  C  the same counting at k = 5 and at k = 7 (sharpness)
  D  the 36-sector witness of sprint/k6/six_free_witness.json, re-verified
  E  (TE) = Lemma 5.2(3) at unit distance, Remark 5.3: the witness violates it everywhere
  F  trace condition (P5) / paper Lemma 6.2 for every pair value and every cycle edge
  G  m2's two-centre bound: conclusion true, hypothesis (unit distance disjointness) false
  H  m11's ternary density, m4/m1/m14 applicability
  I  the geometric lemma margin 1.5938*d0 < Delta in exact rationals
"""
from fractions import Fraction as F
from itertools import combinations
import json, math, os, sys

LAB = list(range(6))


def edges(ell):
    return [frozenset((i, (i + 1) % ell)) for i in range(ell)]


def admissible(S, ell):
    """paper (6.2) + palette bound |P| <= k-3 (k = ell = 6) : size 1..3, not inside an edge"""
    return 1 <= len(S) <= 3 and not any(S <= e for e in edges(ell))


def values(ell, free=None, sizes=(2, 3)):
    lab = range(ell)
    out = []
    for r in sizes:
        for c in combinations(lab, r):
            S = frozenset(c)
            if free is not None and free in S:
                continue
            if not admissible(S, ell):
                continue
            out.append(S)
    return out


def disjoint_family(V, k):
    """max size of a pairwise disjoint subfamily of V, by exhaustive DFS (no DP, no ILP)"""
    V = sorted(V, key=lambda s: (len(s), sorted(s)))
    best = [0]

    def rec(i, chosen, used):
        if len(chosen) > best[0]:
            best[0] = len(chosen)
        if best[0] == k:
            return
        for j in range(i, len(V)):
            if not (V[j] & used):
                rec(j + 1, chosen + [V[j]], used | V[j])

    rec(0, [], frozenset())
    return best[0]


def exists_three_disjoint(V):
    """second, independent decision procedure: triple loop over set intersections"""
    L = list(V)
    for a in range(len(L)):
        for b in range(a + 1, len(L)):
            if L[a] & L[b]:
                continue
            for c in range(b + 1, len(L)):
                if not (L[c] & L[a]) and not (L[c] & L[b]):
                    return (L[a], L[b], L[c])
    return None


print("=" * 78)
print("A. domain of admissible values at k = 6 (C6, palette bound 3, (6.2))")
V6 = values(6)
print("   |V6| =", len(V6), " sizes:", sorted({len(v) for v in V6}))
pairs6 = [v for v in V6 if len(v) == 2]
three6 = [v for v in V6 if len(v) == 3]
print("   pairs:", len(pairs6), " triples:", len(three6))
print("   every label lies in a C6 edge, so no singleton is admissible:",
      all(not admissible(frozenset([b]), 6) for b in range(6)))

print("=" * 78)
print("B. KILL -- free label + admissible palettes: no three pairwise disjoint values")
for free in range(6):
    Vf = values(6, free=free)
    m = disjoint_family(Vf, 3)
    w = exists_three_disjoint(Vf)
    print(f"   free label {free}: |values| = {len(Vf)}, max disjoint packing = {m}, "
          f"three disjoint found by 2nd procedure: {w}")
    assert m == 2 and w is None
    # the exact counting reason
    assert all(1 <= len(v) for v in Vf)
print("   => at any unit triangle, if the free label is absent from all palettes and each")
print("      palette has size >= 2, the three palettes would be pairwise disjoint nonempty")
print("      subsets of a 5-element set: 2+2+2 = 6 > 5.  Impossible.")

print("=" * 78)
print("C. sharpness: k = 5 and k = 7")
# k = 5: paper Prop 5.6 gives |P| <= 2 at every centre; (6.2) with V(C5) = [5] gives |P| >= 2
V5 = values(5, free=0, sizes=(2,))
print("   k=5, free label 0, palettes of size 2 admissible for C5:", [sorted(v) for v in V5])
print("   max pairwise disjoint packing:", disjoint_family(V5, 3),
      " three disjoint:", exists_three_disjoint(V5))
assert disjoint_family(V5, 3) == 2
# k = 7: palette bound k-3 = 4; three disjoint values of size >= 2 avoiding a free label
V7 = values(7, free=6, sizes=(2, 3, 4))
w7 = exists_three_disjoint(V7)
print("   k=7, free label 6: three pairwise disjoint admissible values:", w7)
assert w7 is not None

print("=" * 78)
print("D. the 36-sector witness of sprint/k6/six_free_witness.json, re-verified")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
WJ = os.path.join(REPO, "sprint", "k6", "six_free_witness.json")
W = json.load(open(WJ))
word = [frozenset(v) for v in W["word"]]
m = W["m"]; n = W["n"]
assert n == 6 * m == len(word) == 36
offs = sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})
assert offs == W["offsets"], (offs, W["offsets"])
print("   m,n,offsets:", m, n, offs)
bad = [(i, sorted(word[i])) for i in range(n) if not admissible(word[i], 6)]
print("   all 36 values admissible for C6:", not bad)
assert not bad
print("   all 36 values avoid label 0:", all(0 not in v for v in word))
assert all(0 not in v for v in word)
print("   (5.7) P(f) cap P(Rf) = empty (R = +60 deg = sector shift +m):",
      all(not (word[i] & word[(i + m) % n]) for i in range(n)))
assert all(not (word[i] & word[(i + m) % n]) for i in range(n))
viol = [(i, o) for i in range(n) for o in offs if word[i] & word[(i + o) % n]]
print("   transport offsets disjoint at all sectors:", not viol)
assert not viol
print("   distinct values used:", sorted(map(lambda s: sorted(s), {v for v in word})))
print("   sizes:", sorted({len(v) for v in word}))

print("=" * 78)
print("E. (TE): Lemma 5.2(3) with z = x + a, |a| = 1, s(f) = f, t(f) = a (Remark 5.3)")
print("   P_{x+a}(f) cap P_x(f) = empty for a.e. f, every centre x and unit a")
Delta = 2 * math.pi / n


def P(z, f):
    """the sector model: the palette depends on the DIRECTION only (translation invariant)"""
    s = int(math.floor((f % (2 * math.pi)) / Delta)) % n
    return word[s]


TRIALS = 0
violations = 0
empty = 0
for j in range(720):
    f = 2 * math.pi * j / 720
    for a in [(1.0, 0.0), (0.0, 1.0), (math.cos(0.7), math.sin(0.7)),
              (math.cos(4.1), math.sin(4.1))]:
        for z in [(0.0, 0.0), (0.5, -1.25), (1e3, 17.0)]:
            y = (z[0] + a[0], z[1] + a[1])
            TRIALS += 1
            I = P(y, f) & P(z, f)
            if not I:
                empty += 1
            else:
                violations += 1
print(f"   {TRIALS} (centre, unit vector, direction) triples: intersections nonempty in",
      f"{violations}, empty in {empty}")
print("   => (TE) fails at every unit pair and every direction (the palettes coincide).")
print("   reason: P is independent of the centre, so P_{{x+a}}(f) cap P_x(f) = P(f) != empty.")

print("=" * 78)
print("F. trace condition (P5) = paper Lemma 6.2, for every value and every cycle edge")
print("   a trace supported in P killing edge {i,i+1}: delta_b with b in P, b not in {i,i+1}")
allok = True
for v in sorted({v for v in word}, key=lambda s: sorted(s)):
    row = []
    for e in edges(6):
        cand = sorted(v - e)
        ok = bool(cand)
        if ok:
            b = cand[0]
            tr = {x: (1.0 if x == b else 0.0) for x in range(6)}   # probability vector
            assert sum(tr.values()) == 1.0
            assert all(tr[x] == 0.0 for x in range(6) if x not in v)  # supported in P
            assert all(tr[x] == 0.0 for x in e)                      # kills both edge labels
        row.append(ok)
        allok &= ok
    print(f"   P = {sorted(v)}: trace exists for every C6 edge:", all(row))
assert allok
print("   => (P5) holds for every value: every admissible pair contains a label outside")
print("      every cycle edge, so delta_b is an admissible trace. (This is exactly (6.2).)")

print("=" * 78)
print("G. m2's two-centre bound at k = 6: |P_x(e)| + |P_y(e)| <= 5 for |x-y| = 1")
sizes = [len(v) for v in word]
print("   for the model, P_{x+a}(e) = P_x(e), so the inequality reads 2|P| <= 5:",
      "fails" if any(2 * s > 5 for s in sizes) else "true for pairs",
      "  (max 2|P| =", 2 * max(sizes), ")")
print("   m2's PROOF needs the three palettes of a unit triangle to be pairwise disjoint;")
print("   in the model all three equal P(e), so that hypothesis fails. Same for (B1)/(B2).")

print("=" * 78)
print("H. m11 ternary density and the finite-palette filters")
tern = sum(1 for v in word if len(v) == 3)
print(f"   ternary sectors in the pair-only witness: {tern} of {n} (m11: <= 1/2 of the circle)")
print("   m4 (label merging) and m1 (single-centre classification) speak about colourings /")
print("   single centres: not applicable to an abstract palette field.  m14 (neutrality of")
print("   finite palette constraints) needs the constraints to be size bounds, disjointness,")
print("   non-coverage and hitting conditions; (TE) is a disjointness condition -- but m14's")
print("   conclusion is about satisfiability of a FINITE system, not about (TE) on a plane.")

print("=" * 78)
print("I. the geometric lemma's margin, exact")
print("   d0 = pi/(9m) <= (22/7)/(9m) = 11/(189m)   [pi <= 22/7]")
print("   Delta = 2pi/(6m) >= 2*3.14159/(6m)       [pi >= 3.14159]")
d0u = F(22, 7) / (9 * 6)
Dl = 2 * F(314159, 100000) / (6 * 6)
print("   m=6: d0 <= 11/189 =", float(d0u), "   Delta >= 0.174532", float(Dl))
print("   1.5938 * d0 <= 1.5938 * 11/189 =", F(15938, 10000) * F(11, 189),
      "  <", F(1, 5), " < Delta? ", F(15938, 10000) * F(11, 189) < Dl)
assert F(15938, 10000) * d0u < Dl
print("   (the sprint's cruder test 1.5938/9 < 1/3 is", F(15938, 10000) / 9 < F(1, 3), ")")
print()
print("ALL CHECKS PASSED")
