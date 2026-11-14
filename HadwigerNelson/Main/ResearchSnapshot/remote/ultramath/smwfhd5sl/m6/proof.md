# Palette orbit constraints at k = 6: the ternary directions occupy at most half the circle

Member m6, direction d8 (W3 + W8). This is a sharpening of the k = 6 palette constraint
system of the §5–§7 method, with an exact finite certificate, plus the sharp form of the
angular unit-independence bound used by the "structured substitute" no-gos.

**Notation.** `Angles = ℝ/2πℤ`; `σ` is angular measure, `σ(Angles) = 2π`; `R` is rotation
of directions by `κ = π/3` (order 6 on `Angles`); for a weak measurable colouring
`c : ℂ → Fin k` (paper Definition 1.2) and `x ∈ ℂ`, `P_x(e) = palette c hc x e` is the
maximal palette of Definition 5.1, a finite subset of `Fin k`.

**Cited inputs.** Everything below is proved from exactly three facts, all already
established in the project:

* **(P) Palette bound (R5).** For every `k ≥ 3` and a.e. `e`: `1 ≤ |P_x(e)| ≤ k−3`.
  (At `k = 5` this is the paper's Proposition 5.6, machine-checked as
  `EuclideanFiveColor.palette_cardinality`; for general `k` it is the bound of
  `results/K6-BARRIER.md` §1, recorded as R5.)
* **(5.7) Sixty-degree disjointness.** `P_x(f) ∩ P_x(f+κ) = ∅` for a.e. `f`.
  Machine-checked, all `k`: `EuclideanFiveColor.palette_sixty_disjoint`
  (`lean/OAI/Geometry/PlaneColoring/PaletteTransport.lean`).
* **(5.2) Palette transfer (pair form).** For a.e. `(e,v) ∈ Angles²`:
  `c(x + dir e + dir v) ∉ P_x(e) ∪ P_x(v)`.
  Machine-checked, all `k`: `EuclideanFiveColor.palette_transfer_pair`
  (`lean/OAI/Geometry/PlaneColoring/PaletteDensity.lean`).

No other property of the colouring is used; in particular nothing is assumed about
measurability of the colour classes beyond Definition 1.2, and no separation lemma,
no cover lemma and no cycle exclusion enters.

---

## Theorem 1 (complementary palette exclusion)

Let `k ≥ 2`, `x ∈ ℂ`, and `A, B ⊆ Fin k` with `A ∪ B = Fin k`. Then **not both** sets
`B_A = {e : P_x(e) = A}` and `B_B = {e : P_x(e) = B}` have positive `σ`-measure.

*Proof.* Each `B_A` is measurable, because `P_x(e) = A` is a finite Boolean combination of
the measurable sets `{e : i ∈ P_x(e)}` (`paletteSet_measurable`). Suppose `σ(B_A) > 0` and
`σ(B_B) > 0`. Then `B_A × B_B` has positive product measure, so it is not contained in the
null set on which (5.2) fails; pick `(e,v) ∈ B_A × B_B` with
`c(x + dir e + dir v) ∉ P_x(e) ∪ P_x(v) = A ∪ B = Fin k`. That is impossible, since `c`
takes values in `Fin k`. ∎

At `k = 6` this says: **of each complementary pair `{A, A^c}` of 3-element label sets, at
most one is palette-positive at a given centre x.** (Note `A ∪ A^c = Fin 6`.)

## Theorem 2 (orbit bound at k = 6)

Let `k = 6` and let `c` be a weak measurable 6-colouring. Fix `x ∈ ℂ`. Then for a.e.
`e ∈ Angles`,

  `#{ j ∈ ℤ/6 : |P_x(R^j e)| = 3 } ≤ 3`,

i.e. **in every `R`-orbit of directions at most three of the six palettes are ternary.**
Consequently, with `E_x = {e : |P_x(e)| = 3}` (the ternary directions at `x`),

  `σ(E_x) ≤ π`   and   `(1/2π) ∫ |P_x(e)| dσ(e) ≤ 5/2`.

*Proof.* Suppose the set `G` of `e` for which the orbit of `e` has at least four ternary
palettes has positive measure. The orbit is a 6-cycle and four of its vertices contain two
adjacent ones, so `G` is the union over `j ∈ ℤ/6` of
`G_j = {e ∈ G : |P_x(R^j e)| = |P_x(R^{j+1} e)| = 3}`; some `G_j` has positive measure.
By (5.7) applied at `f = R^j e`, for a.e. `e ∈ G_j` the two triples are disjoint, hence
complementary: `P_x(R^{j+1} e) = P_x(R^j e)^c`. There are only 20 triples, so some triple
`A` has `G_j' = {e ∈ G_j : P_x(R^j e) = A}` of positive measure. Then
`B_A ⊇ R^j(G_j')` and `B_{A^c} ⊇ R^{j+1}(G_j')` both have positive measure, since
rotations preserve `σ`. This contradicts Theorem 1 (`A ∪ A^c = Fin 6`). Hence `G` is null,
which is the first assertion.

For the second, put `f(e) = #{ j : |P_x(R^j e)| = 3 } ≤ 3` a.e. Then by rotation invariance
of `σ` and Tonelli, `∫ f dσ = Σ_j σ(R^{-j} E_x) = 6 σ(E_x)`, so `6σ(E_x) ≤ 3·2π`, i.e.
`σ(E_x) ≤ π`.

For the mean: `∫ |P_x| dσ = (1/6) Σ_j ∫ |P_x(R^j e)| dσ(e) = ∫ (1/6) Σ_j |P_x(R^j e)| dσ(e)`.
For a.e. `e`, at most three of the six terms equal 3 and the remaining ones are at most 2
by (P), so `Σ_j |P_x(R^j e)| ≤ 3·3 + 3·2 = 15`. Hence `∫|P_x| dσ ≤ (15/6)·2π = 5π`, i.e.
the mean palette size is at most `5/2`. ∎

**Remarks.**
1. The proof uses only (P), (5.7), (5.2). It is therefore *inside* the class of the §5–§7
   argument: Theorem 2 is not a new hypothesis, it is a consequence of hypotheses (a), (b),
   (d) of the L4 constraint system.
2. At `k = 5` no analogue is possible: two 2-element sets cannot cover `Fin 5`, so
   Theorem 1 is vacuous and the only orbit constraint is (5.7) itself — i.e. exactly the
   binary flip of §8.4–8.6. Theorem 2 is the first `k` at which the orbit system carries
   information beyond `|P| ≤ k−3` and `P ∩ RP = ∅`.
3. **Why `k = 6` is the first case, structurally.** A complementary pair of palettes can
   occur at a centre only if two admissible palette sizes `a, b ≤ k−3` satisfy
   `a + b ≥ k`. Since `2(k−3) ≥ k ⟺ k ≥ 6`, the pair-exclusion of Theorem 1 is vacuous
   for `k ≤ 5` and non-vacuous from `k = 6` on. So the `k = 5 → k = 6` transition is exactly
   the point where the *arithmetic* of the palette bound first allows two palettes in one
   orbit to exhaust the label set. (At `k = 7` an orbit bound of the same shape follows from
   (5.7) alone, since `4 + 4 > 7`; `k = 6` is the unique case in which it needs Theorem 1.)
4. The bound `σ(E_x) ≤ π` is a statement about a **ball**'s worth of data at the centre `x`
   (all directions at once), not about a single circle sample; it is not a statement about
   the unit-distance graph of a circle (which is 2-colourable, hence `k`-blind).

## Theorem 3 (extremal unit-independent sets on the circle — sharp form of W3's angular bound)

Let `A ⊆ Angles` be measurable with `A ∩ (A + κ) = ∅` (no two of its directions enclose
`κ`, equivalently no two points of the unit circle at angular distance `κ`, i.e. chordal
distance 1). Then `σ(A) ≤ π`, and **equality holds iff `A + κ = A^c` a.e.**

*Proof.* Use the measure isomorphism
`Φ : [0,κ) × ℤ/6 → Angles`, `(b,j) ↦ b + jκ mod 2π` (a piecewise translation, and the six
translates of `[0,κ)` partition `Angles`, so `Φ_*(db ⊗ #) = σ`), and let
`S_b = {j : (b,j) ∈ Φ^{-1}(A)}`. The hypothesis says
that for a.e. `b`, `S_b` contains no two elements differing by `±1 mod 6`, i.e. `S_b` is an
independent set of the 6-cycle; hence `|S_b| ≤ 3` and
`σ(A) = ∫ |S_b| db ≤ 3·(π/3) = π`. Equality forces `|S_b| = 3` a.e., and the independent
3-sets of `C_6` are exactly the two bipartition classes `{0,2,4}`, `{1,3,5}`; that is
exactly `A + κ = A^c` a.e. ∎

**Audit consequence (W3).** In a weak measurable 5-colouring, for each label `i` the set
`D_{x,i} = {e : i ∈ P_x(e)}` satisfies `D_{x,i} ∩ (D_{x,i} + κ) = ∅` by (5.7); so
`σ(D_{x,i}) ≤ π` with equality iff `D_{x,i} + κ = D_{x,i}^c`. At a centre `x` that is
*binary for the pair* `{i,j}` in the sense of §5 (i.e. `P_x(e) ∩ {i,j}` is a singleton for
a.e. `e`) one has `D_{x,i} ∪ D_{x,j} = Angles` and `D_{x,i} ∩ D_{x,j} = ∅`, so
`D_{x,j} = D_{x,i}^c` and **both are extremal**. This reproduces the paper's (5.8)
(`s_x(t+κ) = −s_x(t)`, `|A_s| = π` per period) and shows that the binary-centre structure
is precisely the equality case of the angular no-go: the two accepted results are the same
object seen from the two sides.

---

## Sharpness and non-vacuity (exact)

The script `orbit_check.py` (exact integer arithmetic, no floating point) computes, for
`O_k = {(P_0,…,P_5) : ∅ ≠ P_j ⊆ Fin k, |P_j| ≤ k−3, P_j ∩ P_{j+1} = ∅}` — the pointwise
consequences of (P) and (5.7) on one `R`-orbit — the number `|O_k| = tr(A_k^6)` where `A_k`
is the disjointness matrix of the admissible label sets:

| k | \|O_k\| | orbits with all six palettes of size k−3 | max # of size-(k−3) palettes |
|---|-----------|---------------------------------------------|------------------------------|
| 3 | 0         | 0                                           | 0 (no admissible set)        |
| 4 | 732       | 732                                         | 6                            |
| 5 | 225 590   | 990                                         | 6                            |
| 6 | 10 581 680| **20**                                      | 6 (combinatorially)          |
| 7 | 294 272 482 | 0                                         | 3                            |
| 8 | 6 750 365 146 | 0                                       | 3                            |

At `k = 6` the 20 orbits in which all six palettes are ternary are exactly the alternating
patterns `A, A^c, A, A^c, A, A^c` (one for each of the 20 triples `A`); **every one of them
is excluded by Theorem 1**, since it puts `A` and `A^c` both on the orbit. Consequently,
under (P), (5.2), (5.7), a `k = 6` orbit carries at most three ternary palettes, and the
combinatorial maximum `6` is not attained. This is a second, independent verification of
Theorem 2's orbit bound, by exhaustive enumeration rather than by the measure argument.

**The bound `σ(E_x) ≤ π` and the mean bound `5/2` are attained** by the following explicit
palette assignment, constant on the six angular cells
`C_j = [jκ,(j+1)κ)` (`j = 0,…,5`), with the ternary cells `E = C_0 ∪ C_2 ∪ C_4`
(`σ(E) = π`):

```
P(C_0) = A_0 = {1,2,3}      P(C_1) = {5,6}
P(C_2) = A_2 = {1,2,4}      P(C_3) = {5,6}
P(C_4) = A_4 = {1,3,4}      P(C_5) = {5,6}
```

The script verifies exactly: (i) `1 ≤ |P| ≤ 3`; (ii) `P(C_j) ∩ P(C_{j+1}) = ∅` for all six
consecutive pairs (so (5.7) holds); (iii) no two of the six palettes are complementary (so
the assignment does not violate Theorem 1); (iv) exactly three ternary cells and
`σ(E)/2π = 1/2`, mean palette size `5/2`. So Theorems 1–2 are non-vacuous and their bounds
are attained within the constraint system (this is a one-centre palette system, not a model
of the whole §5–§7 system).

**Genuineness of the sharpening.** The printed information `|P| ≤ 3` together with (5.7)
alone does **not** give Theorem 2: the 20 all-ternary orbits in the table satisfy both and
are only excluded by Theorem 1. Hence Theorem 2 is not a restatement of the accepted bound.

## Machine-checked combinatorial core (`OrbitLemma.lean`)

The finite content behind the table is machine-checked in Lean 4.33.1 + Mathlib:

```
PaletteOrbit.card_compl_six        : A.card = 3 → (univ \ A).card = 3        (in Fin 6)
PaletteOrbit.eq_compl_of_disjoint  : disjoint 3-sets in Fin 6 are complementary
PaletteOrbit.six_triples_alternate : consecutive-disjoint triples alternate: P(j+1) = (P j)ᶜ, P(j+2) = P j
PaletteOrbit.all_ternary_is_alternating :
    P1 = (P0)ᶜ ∧ P2 = P0 ∧ P3 = (P0)ᶜ ∧ P4 = P0 ∧ P5 = (P0)ᶜ
```

`#print axioms` gives `[propext, Classical.choice, Quot.sound]` for both main lemmas; there
is no `sorry` and no extra axiom. This is exactly the statement that an all-ternary
`k = 6` orbit is `A, A^c, A, A^c, A, A^c`, i.e. contains a complementary pair of palettes,
which is what Theorem 1 forbids.

## Audit of the structured-substitute no-gos (W3)

The audit asked for by W3 is: are the accepted "no colouring of class C" results correct, are
their hypotheses sharp, and are they independent? Three findings, all exact.

1. **Angular bound (sharp form).** Theorem 3 above: `σ(D_{x,i}) ≤ π`, equality iff
   `D_{x,i} + κ = D_{x,i}^c`. The extremal objects are exactly the binary-centre direction
   sets of (5.8), so the bound is attained and is not improvable; a set of measure `π`
   that is not anti-periodic necessarily contains a pair of directions at distance `κ`
   (e.g. the half-circle `[0,π)`, whose shift by `κ` meets it in `[κ,π)`).
2. **Diameter bound (sharp form).** R3 says a connected unit-free set has diameter `≤ 1`.
   If the set is **closed** the bound improves to `< 1`: a closed set of diameter exactly 1
   is bounded, hence compact, and `K × K` is compact, so the distance function *attains*
   the value 1 — i.e. the set contains a unit pair. The open disc of radius `1/2` is
   unit-free, connected, has diameter
   exactly 1 and is not closed, so `≤ 1` is sharp and `< 1` is exactly the closed case.
   (Consequently every connected component of a closed unit-free set has diameter `< 1`.)
   This does not by itself exclude any class of colourings — a closed unit-free class can
   be a union of small closed discs — and I do not claim that it does.
3. **Independence.** The angular bound uses only (5.7); the diameter bound uses only
   connectedness of the class and the Euclidean distance function; the pair-exclusion
   (Theorem 1) uses only (5.2). No two of the three imply each other, so the audit does not
   collapse any pair of the accepted no-gos into one.

## What this changes for L4

For the no-go of L4 the relevant object is the constraint system that a faithful `k = 6`
palette system must satisfy. Theorems 1–2 add two constraints that are *derived* from
hypotheses (a), (b), (d) of that system (so they are available to every argument in the
class, and cannot be dropped from a faithful model):

* **(C1)** no two complementary 3-element label sets are both palette-positive at one centre;
* **(C2)** at every centre the ternary directions occupy at most half the circle
  (`σ(E_x) ≤ π`); equivalently the mean palette size is at most `5/2`, and in every
  `R`-orbit at least three of the six palettes are pairs (or smaller).

**Falsification test.** A `k = 6` palette system that satisfies the listed constraints of
§§5–§7 but has *four* ternary palettes in one `R`-orbit, or `σ(E_x) > π`, cannot be
realised by a weak measurable 6-colouring — by Theorem 2 it is not a faithful model, so it
does not certify satisfiability of the method's constraints. Conversely, if a model can be
built with (C1)–(C2), the L4 no-go is strictly stronger than one built without them.

## Scope, and what is not claimed

* The result is a theorem about **any** weak measurable `k`-colouring at `k = 6`
  (hence, by Theorem 1.3 of the paper, about any proper 6-colouring of the plane).
* It does **not** prove `|P_x(e)| ≤ 2`, does not exclude ternary palettes, and does not
  decide `χ(ℝ²)`. The bound `k−3 = 3` is not improved at any single direction; what is
  improved is the *distribution* of the ternary directions.
* W8 (extraction or a size bound for a finite witness of `χ ≥ 6`) is **not** delivered
  here; the only W8-relevant content is that any finitely presented palette system
  extracted from a 6-colouring must obey (C1)–(C2).

## Reproduction

From the project root:

```
python3 .ultramath/smwfhd5sl/m6/orbit_check.py     # exact table, sharpness model, 20 alternating orbits
lean .ultramath/smwfhd5sl/m6/OrbitLemma.lean       # machine-checked combinatorial core (exit 0, axioms clean)
```

`orbit_check.py` writes `orbit_report.json` next to itself. The three cited Lean lemmas are in
`lean/OAI/Geometry/PlaneColoring/{PaletteTransport,PaletteDensity}.lean`.
