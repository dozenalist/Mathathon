# The equilateral paired configuration α = (0,0,120,120,240,240): forced content, and the exact missing width bound

Source-only analysis by the coordinator. **No compute beyond exact integer arithmetic (one 64-subset
fixpoint, sub-millisecond); no Lean, no cloud.** Swarm `smwgpvm6o` (`m1`, `m2`,
`deepseek/deepseek-v4.1-flash`, effort `max`) is running two complementary directions on the same target;
its findings are not yet in.

Grades: **[proof]** = mine, hand-checked and machine-confirmed by the fixpoint; **[source]** = declaration
read earlier with its line; **[candidate]** = the missing lemma, unproved.

## 0b. Convention, stated once (an earlier draft of this file had it backwards)

`(7.1)` says the two **endpoint labels of edge `i` are ABSENT** from the straddle region `Δ(K_i)`. So the
outer-region colour lies in `[6] \ E_i`, and for a set `P` of positive edges in `[6] \ ⋃_{i∈P} E_i`.
The constraint is therefore a **complement of a union**, not an intersection of label sets — for a block
`B_j` (union of two adjacent edges) the colour avoids `B_j`, so on an arc where two blocks are both
positive the colour is forced to the **leftover** `[6] \ (B_0 ∪ B_1)`, a singleton. That is exactly the
`MC120` shape: the exclusions leave ≤ 1 colour.

## 1. The configuration and its six arcs

`α = (0°,0°,120°,120°,240°,240°)`, `E_i = {i, i+1 mod 6}`:

    E_0={0,1}, E_1={1,2} at 0° ;  E_2={2,3}, E_3={3,4} at 120° ;  E_4={4,5}, E_5={5,0} at 240°
    B_0 = E_0∪E_1 = {0,1,2} ;  B_1 = E_2∪E_3 = {2,3,4} ;  B_2 = E_4∪E_5 = {0,4,5}
    B_0∪B_1 leaves {5} ;  B_1∪B_2 leaves {1} ;  B_2∪B_0 leaves {3}

An edge at angle `β` has a positive (outer) strip where `cos(t − β) > 0`, i.e. `|t − β| < 90°`. Hence the
circle splits into **six arcs** of exactly 60°, alternating between two positive edges and four:

| arc (centred) | positive edges | `J_j = [6] \ ⋃` label sets | outer colour |
|---|---|---|---|
| `A_0` (0°) | `E_0, E_1` | `{3,4,5}` | in `{3,4,5}` |
| `A_1` (60°) | `E_0,E_1,E_2,E_3` | **`{5}`** | **`5`** |
| `A_2` (120°) | `E_2, E_3` | `{0,1,5}` | in `{0,1,5}` |
| `A_3` (180°) | `E_2,E_3,E_4,E_5` | **`{1}`** | **`1`** |
| `A_4` (240°) | `E_4, E_5` | `{1,2,3}` | in `{1,2,3}` |
| `A_5` (300°) | `E_4,E_5,E_0,E_1` | **`{3}`** | **`3`** |

**(i)** On each four-positive arc the outer region is a.e. **monochromatic**, in colours `5`, `1`, `3`
respectively — three *distinct* colours. **(ii)** By `continuum_outer_restriction` the palette at `x`
**hits** `J_j`; on a four-positive arc `J_j` is a singleton, so the hit upgrades to **containment**. (The
lemma concludes a hit; only the singleton case gives containment, which is why the `BinaryCenter`
hit-semantics matters.)

## 2. What is forced at the palette: a diagonal, and nothing more

Adding the sixty-degree exclusion `P(t) ∩ P(t+π/3) = ∅` (neighbouring arcs are exactly `π/3` apart) and
running the containment-hits/disjointness fixpoint over all `2^6` candidate palettes per arc:

    forced:  4 ∈ P(A_0),  5 ∈ P(A_1),  0 ∈ P(A_2),  1 ∈ P(A_3),  2 ∈ P(A_4),  3 ∈ P(A_5)
    nothing else is forced — the fixpoint closes after two rounds with exactly these six members.

*Hand proof of the six.* `5 ∈ P(A_1)` and disjointness give `5 ∉ P(A_0), P(A_2)`; `P(A_0)` hits `{3,4,5}`
so it contains `3` or `4`, and `3 ∈ P(A_5)` (with `3 ∉ P(A_0)`) forces `4 ∈ P(A_0)`. Similarly
`P(A_2)` hits `{0,1,5}` with `1,5` excluded, so `0 ∈ P(A_2)`; and `P(A_4)` hits `{1,2,3}` with `1,3`
excluded, so `2 ∈ P(A_4)`. ∎

**Answer to Member 1's question (established here independently of the swarm): the canonical
three-disjoint-pair field is NOT forced almost everywhere.** The forced content is the six-member
**diagonal containment**, which is strictly weaker and pins no palette. The three-palette family
`{1,4}, {2,5}, {0,3}` *is* a consistent completion — it contains every forced member
(`4∈{1,4}`, `5∈{2,5}`, `0∈{0,3}`, `1∈{1,4}`, `2∈{2,5}`, `3∈{0,3}`) and its members are pairwise and
consecutively disjoint — but nothing in the exclusion data or in `(5.7)` separates it from other
completions (e.g. palettes of size 3 or more, since `B2` is not assumed).

**Phase and null representatives.** The arcs are fixed by the three block directions, so the phase is not
free; but every containment is an a.e. statement, and at the six perpendicular directions (`cos = 0`) the
strip lemmas do not apply at all — those six directions are null. So no containment may be asserted
pointwise, and a representative choice on a null set cannot be excluded. That is the precise sense in
which the field is forced: a.e. on each open arc, at the palette, and nowhere else.

## 3. The three 60° arcs are each the MC120 endpoint — and the missing bound

`MC120` rules out exclusions leaving ≤ 1 colour at strict aperture < 120° because the common positive arc
then has width > 60° and a unit pair fits inside the monochromatic region. Here each double-positive arc
has width **exactly 60°**: the endpoint. Compute the endpoint deficit. A monochromatic arc of angular
half-width `30° − ε` (compact subarc) and radial window `1 < r < 1 + δ` contains a unit pair at equal
radius iff `2r sin(θ/2) = 1`, i.e. `θ(r) = 2 arcsin(1/(2r))`. Since `θ(1) = 60°` and
`dθ/dr|_{r=1} = −2/√3 rad ≈ −66.2°` per unit `r`, the requirement `θ(r) ≤ 60° − 2ε` becomes

    r − 1  ≥  0.0302 · ε        (at the subarc scale; with the δ-neighbourhood of directions the
                                 constant improves slightly, which is immaterial).

So the endpoint closes **iff the strip width at angular distance ε from the perpendicular is at least
about `ε/33`**. And that is exactly what the source statement does not provide.

> **Missing lemma (Q-width).** There is a universal constant `c > 0` such that for every `K` with
> `ApproachingContinuum x K v`, every unit `e` with `⟪e,v⟫ > 0`, the `δ` of
> `ApproachingContinuum.outer_strip` (`AngularBoundary.lean:244`) may be taken with `δ ≥ c · ⟪e,v⟫`
> — equivalently `δ ≥ c · sin ε` when `e` makes angle `90° − ε` with `v`.

At angular distance `ε` from the perpendicular we have `⟪e,v⟫ = sin ε ≈ ε`, so any universal `c ≥ 1/33`
suffices to close all three arcs and hence to rule out the equilateral configuration. **What the source
gives instead** is `∃δ > 0` with no relation to `⟪e,v⟫`: the proof obtains `δ` from
`approaching_direction_inside` and `outer_straddle_strip`, both of which degenerate as the scalar product
tends to `0`. So `(Q-width)` is a genuine strengthening, not a restatement, and I do not claim it.

**Why the inner side does not help.** For radius `r < 1` the unit-pair separation `2 arcsin(1/(2r))`
exceeds `60°`, so it cannot fit inside a 60° arc at all; the inner strips are useless for this geometry.
That is exactly why `MC120` is phrased about an *outer* width.

## 4. Member 2's direction: no cross-arc coupling at one centre

Within the radial window, two points in *different* arcs are at angular separation at least `120° − O(δ)`,
hence at distance at least `√3 − O(δ) > 1`; and the three monochromatic arcs carry three *distinct*
colours (`5, 1, 3`), so no same-colour pair spans two arcs anyway. **Therefore the three endpoint problems
are independent at a single centre**: no cross-block or cross-arc constraint appears beyond the palette
diagonal of §2. A cross-centre obstruction must either (i) close each endpoint via `(Q-width)`, or
(ii) use the fact that the same structure must hold at *every* centre, which is the
`two_label_triangle_impossible`-style route — but that needs one label set of cardinality ≤ 2 dense at
three pairwise-unit points, and §2 shows the equilateral data delivers three *different* singleton
palettes on three arcs, not one set at three points.

## 5. Scope

* **[proof]** §1's six-arc table and the mono-chromaticity of the three double-positive arcs; §2's diagonal
  (hand proof plus the exact fixpoint) and the non-forcing of any three-disjoint-pair field; §3's endpoint
  arithmetic and the `c ≥ 1/33` threshold; §4's cross-arc distance bound.
* **[candidate]** `(Q-width)` — quantified, unproved, and the only gap between the equilateral
  configuration and a contradiction by this route.
* **[given]** `CC60`, `MC120` (including "endpoint 120 not claimed"), and the derived consequence that three
  distinct directions each carrying an adjacent edge pair must be equilateral. Not re-derived.
* **Not claimed:** any global chromatic bound; any 6-colouring construction; that the three-disjoint-pair
  field is forced; that `(Q-width)` is true. `B2` is nowhere assumed. `BinaryCenter` is used in its
  hit form only, and the singleton upgrade is justified explicitly in §1.
* **Not claimed either:** that `57/60` of cyclic orders or six grid cases exhaust actual angles — that
  caveat from the bank is respected; nothing here enumerates configurations.
