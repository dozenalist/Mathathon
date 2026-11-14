# The three-palette full-circle family: exact cross-centre conditions and the missing propagation

Source-only. **No computation, no Lean.** Read-only: `States.lean`, `BinaryPalettes.lean`. Grades:
**[source]** declaration read with line; **[proof]** mine, hand-written; **[candidate]** angular data only.

## 0. The candidate, and what it does and does not satisfy

    P(t) = A_{⌊(t+π/6)/(π/3)⌋ mod 3},     A_0 = {1,4},  A_1 = {2,5},  A_2 = {0,3}.

Eight sectors of `π/3`; the index cycles `0,1,2,0,1,2`; `A_0, A_1, A_2` are pairwise **disjoint** and
**partition** `Fin 6`; each has cardinality 2, so `B2` holds at every direction. `P(t+π/3)` is the next
palette (disjoint), `P(t+π) = P(t)` because `π = 3·(π/3) ≡ 0 (mod 3)`. **It is angular data only** — a
function `Angles → Finset (Fin 6)`, not a colouring and not input to any lemma.

**At one centre** it yields three `RealState`s: on the sector set `S_l := {t : index(t) = l}` the palette
*is* `A_l`, so `RealState c hc x S_l A_l` holds for each `l` **[source: `States.lean:92`]**. And because
the `A_l` partition `Fin 6`,

    univ \ (A_{l} ∪ A_{l'}) = A_{l''}  for the third index,   cardinality 2 ≤ 2.

So `states_densityOne` **[source: `States.lean:109`]** with the pair `(A_l, A_{l'})` delivers

    DensityOne {q | c q ∈ A_{l''}} (angularSum x 1 (angleChart (t,u)))      (sin(u−t) ≠ 0),

i.e. **density one of the third palette** at the angular-sum point. This is the single-centre content.

## 1. The cross-centre tool, stated exactly

**`two_label_triangle_impossible` [`States.lean:198`].**

    (hc) (hw) (z : Fin 3 → ℂ) (J : Finset (Fin k)) (hJ : J.card ≤ 2)
    (hd : ∀ v w, v ≠ w → ‖z v − z w‖ = 1) :
    ¬ (∀ v, DensityOne {q | c q ∈ J} (z v))

Its proof uses `finite_density_realization` to translate the triangle into `{c ∈ J}` simultaneously, then
`hd` makes the three colours pairwise distinct while all lie in a set of cardinality ≤ 2 — pigeonhole.

**So the cross-centre requirement is exactly: ONE label set `J` of card ≤ 2, density one at THREE
pairwise-unit points.** Everything else is bookkeeping. Written out, the five conditions are:

* **(XC1) same residual.** The three applications must deliver the *same* palette `A_*`. This is the
  binding condition — it is what makes `J` single.
* **(XC2) unit triangle.** The three angular-sum points must be pairwise at distance 1.
* **(XC3) non-parallel directions.** `sin(u_j − t_j) ≠ 0` at each application
  (`states_densityOne`'s hypothesis).
* **(XC4) sector membership.** `t_j, u_j` must lie in the sector sets of the two chosen indices
  (`LineDensityZero` side conditions; automatic a.e.).
* **(XC5) centre compatibility.** Control of which point the angular sum lands on when the base centres
  differ.

## 2. A concrete compatible-centre producer — conditional, and it works

**Observation [proof].** `angularSum x 1 (angleChart (t,u)) = x + w(t,u)` where `w(t,u)` depends only on
`(t,u)` — the `x`-dependence is a pure translation. (This is visible in `sourceTriangle_eq`
[`BinaryPalettes.lean:334`]: `sourceTriangle x t j = x + (Circle.exp t) · (Circle.exp (2jπ/3)) · (…)` —
every occurrence of `x` is an additive translate.)

**Producer.** Fix a direction pair `(t,u)` with `sin(u−t) ≠ 0`, whose sector indices are `l_1 ≠ l_2`, so
the residual is the third palette `A_*`. Suppose the three-palette angular data holds at each of three
centres `x_0, x_1, x_2`. Then

* (XC1): the **same** `(t,u)` at each centre gives the same pair of indices, hence the same `A_*` ✓;
* (XC3), (XC4): inherited from the single choice ✓;
* (XC2): `z_j = x_j + w(t,u)`, so `‖z_j − z_k‖ = ‖x_j − x_k‖` — **the density points form a unit triangle
  exactly when the base centres do** ✓.

So: **if the three-palette angular structure holds at the three vertices of a unit triangle, then
`two_label_triangle_impossible` with `J = A_*` (card 2) and `z = x + w(t,u)` yields `False`.** That is a
real consumer, and it uses three `RealState` density arguments at three *different* base centres, exactly
as `states_densityOne` permits.

## 3. Why the single-centre producer cannot do it — the residual rotates

The existing producer is `sourceTriangle x t` [`BinaryPalettes.lean:332`], used inside
`two_state_impossible` at `States.lean:291`, which builds three pairwise-unit points from **one** base
centre `x` and **one** angle `t` using, at vertex `j`, the directions

    d_1(j) = t + 2jπ/3 ,        d_2(j) = t + 2jπ/3 + π + triangleAngle ,   triangleAngle = arccos(5/6) ∈ (0, π/3).

**Hand computation of the sector indices** for our cycling family. Since `π = 3·(π/3) ≡ 0 (mod 3)` and
`2π/3 = 2·(π/3) ≡ 2 (mod 3)`:

    index(d_1(j)) = φ_j := index(t) + 2j  (mod 3)           — takes all three values as j = 0,1,2
    index(d_2(j)) = φ_j + δ_j,   δ_j ∈ {0,1}  (because triangleAngle ∈ (0, π/3) shifts by at most one sector)

* If `δ_j = 0`, the two directions lie in the **same** palette, so the residual is `univ \ A_{φ_j}`, of
  cardinality **4 > 2** — `hcard` fails and that vertex contributes nothing.
* If `δ_j = 1`, the residual is the third palette `A_{φ_j+2}`. Since `φ_j` runs through all three values,
  **the three vertices carry the three different residuals** `A_{φ_0+2}, A_{φ_1+2}, A_{φ_2+2}`.

Either way `two_label_triangle_impossible`'s single-`J` hypothesis is **not** met. And this is
`δ`-independent: a 2-element subset of a 3-element set can never be invariant under the 3-cycle
`φ ↦ φ + 2`, so no choice of `triangleAngle` repairs it. **The rotating residual is exactly why the
three-palette family survives the two-state argument**: with two palettes `(J,K)` the residual
`univ\(J∪K)` is the same at every vertex, whereas here it rotates with the vertex.

The three statements actually obtained,
`DensityOne {c ∈ A_{φ_0+2}}(z_0)`, `DensityOne {c ∈ A_{φ_1+2}}(z_1)`, `DensityOne {c ∈ A_{φ_2+2}}(z_2)`,
are *mutually consistent* — three disjoint label sets at three different points — so no contradiction
arises. That is the precise sense in which the family is not yet refuted.

## 4. The missing lemma, quantified

> **(XC-propagation).** Let `k : ℕ`, `c : ℂ → Fin k`, `hc : Measurable c`, `hw : WeakColoring k c`, and let
> `x : ℂ`. Suppose the three-palette angular data holds at `x`: measurable sector sets `S_0,S_1,S_2`
> partitioning `Angles`, `2π`-periodic with period `π` in the index, and `RealState c hc x S_l A_l` for each
> `l : Fin 3`, with the `A_l` pairwise disjoint of cardinality 2 and `⋃_l A_l = univ`.
> **Conclusion:** there exist `x_0, x_1, x_2 : ℂ` pairwise at distance 1, **each** again carrying the
> three-palette angular data, or — equivalently for the consumer — there exist three pairwise-unit points
> `z : Fin 3 → ℂ` and one index `*` with `∀ v, DensityOne {q | c q ∈ A_*}(z v)`.

**Status.** Not proved here, and **not claimed impossible**. What §2–§3 establish is the exact shape of
what is missing: the *propagation of the three-palette structure from one centre to the three vertices of a
unit triangle*. Given that input, the consumer chain is complete
(`states_densityOne` at each of the three centres → `two_label_triangle_impossible` with `J = A_*` →
`False`). Without it, the three residuals rotate and the argument is consistent.

**Two honest caveats, as required.** (i) I do **not** assume neighbouring palettes are equal — here they
are pairwise disjoint, and disjointness is used only to compute the residual. (ii) `P` is angular data; no
statement about `WeakColoring` is made, and no model is claimed to be a colouring.

## 5. Scope

* **[source]** `two_label_triangle_impossible` (single `J`, card ≤ 2, three pairwise-unit centres),
  `states_densityOne` (two `RealState`s at one centre → one density-one at the angular sum),
  `sourceTriangle` and `triangleAngle = arccos(5/6)`.
* **[proof]** §1's five conditions; §2's translate-invariance and the producer; §3's index computation and
  the `δ`-independence of its failure.
* **[candidate]** `(XC-propagation)`: quantified input/output given, unproved, and not claimed false.
* **Not claimed:** any global conclusion; any blanket no-go; that neighbouring palettes are equal; that the
  three-palette family is or is not realisable by a genuine six-cycle. Single-centre constraints are
  Claude's track and are not touched here beyond what `states_densityOne` supplies.
