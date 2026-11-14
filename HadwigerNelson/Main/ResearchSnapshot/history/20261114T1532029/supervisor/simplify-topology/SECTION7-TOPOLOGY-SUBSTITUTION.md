# §7's topological input: a referee-checkable substitution for Lemma 7.5

**Owner**: `supervisor/simplify-topology` (Simplify — topology and interfaces).
**Subject**: sections 6–7 of the five-colour proof, specifically the one genuinely topological
statement, Lemma 7.5 (the "cover obstruction on a square"), and the interface it presents to
§7.4. Nothing here concerns the parallel `k = 6` local-finiteness project.
**Trust grades**: `[M]` machine-checked in this block, `[V]` verified prior work (built, axiom-clean,
already in the repo), `[P]` paper argument, `[?]` projection / not checked.

---

## 0. What I read

| source | why |
|---|---|
| `attachments/here-are-three-files-ni5n/paper.pdf`, §6 pp. 40–46, §7.1–7.4 pp. 44–50 (`pdftotext -layout`, text at `notes/paper.txt`) | the statements of Lemmas 6.2–6.7, Theorem 6.5, Proposition 7.1, Lemmas 7.2–7.8 and their printed proofs |
| `lean/OAI/Geometry/PlaneColoring/PlanarCovers.lean` | `hit_center` (:180), `affinePair_null` (:242), `hit_center_subtype` (:252), `barycenter_two` (:274), `finite_partition_impossible` (:302), `finite_open_cover_impossible` (:348), `compact_open_cover_impossible` (:374) — the machine-checked Lemma 7.5 |
| `lean/OAI/Geometry/PlaneColoring/Five.lean` | `graph_map_small_mesh_impossible` (:22), `graph_map_large_positive` (:94), `no_measurable_weak_five_coloring` (:105) — the consumers |
| `lean/OAI/Geometry/PlaneColoring/Mesh.lean` | `no_large_positive_sequence` (:92) — §7.4's mesh/hole argument, i.e. where the diameter bound comes from |
| `lean/OAI/Geometry/PlaneColoring/GraphCuts.lean` | `graphCut_contractible` (:197), `graphMidpoint_coord_le` (:143) — Lemmas 7.3/7.7's formal side (not audited here) |
| `/opt/mathlib/Mathlib/Analysis/Complex/BranchLogRoot.lean:37` | `Complex.exists_continuousOn_eqOn_exp_comp`, the *only* topological input the machine proof uses |

---

## 1. The statement, paper vs. Lean, side by side

**Paper, Lemma 7.5** [P]: *A closed square of side ten has no relatively open cover of
multiplicity at most two and mesh at most two, where mesh is the supremum of the Euclidean
diameters of its members.*

Printed proof: compactness → finite subcover `U_1,…,U_N`; pick `z_a ∈ U_a`; partition of unity
`φ_a` subordinate to `U_a`; `F(z) = Σ φ_a(z) z_a`; at most two weights positive, so
`F(Q) ⊆ ⋃_{a,b} [z_a,z_b] ∪ {z_a}`; `|F(z) − z| ≤ 2`; for `y` with `dist(y,∂Q) > 2` the map
`z ↦ y + z − F(z)` maps `Q → Q` (convexity), so Brouwer gives `F(z) = y`; hence `F(Q)` contains
the open set `{dist(y,∂Q) > 2}`, impossible for a finite union of segments.

**Lean, `PlanarCover.compact_open_cover_impossible`** [V] (`PlanarCovers.lean:374`):

```lean
lemma compact_open_cover_impossible {ι : Type*} {Q : Set ℂ}
    (hQ : Metric.ball (0:ℂ) 5 ⊆ Q) (hQc : IsCompact Q) (U : ι → Set Q)
    (ho : ∀ i, IsOpen (U i)) (hcov : ∀ z : Q, ∃ i, z ∈ U i)
    (hm : ∀ z : Q, ∀ i j l, z ∈ U i → z ∈ U j → z ∈ U l → i = j ∨ i = l ∨ j = l)
    (hd : ∀ i, ∀ x∈U i, ∀ y∈U i, ‖x.val-y.val‖ ≤ 2) : False
```

Differences, all in the *hypotheses' shape*, none in the conclusion:

1. **Domain**: `Q` is any compact set with `ball 0 5 ⊆ Q`, not a square of side ten. Every closed
   square of side ten contains `ball 0 5` about its centre (inradius 5), and every hypothesis is
   invariant under the isometry taking that disk to `ball 0 5`; §5 below turns this into a Lean
   instance `paper_lemma_7_5`.
2. **Membership** is expressed in the subtype `Set Q`; `IsOpen (U i)` is relative openness in `Q`,
   exactly the paper's "relatively open".
3. **Multiplicity** is the triple form `i = j ∨ i = l ∨ j = l`, equivalent to "at most two
   distinct members at each point" and the form in which §7.4's graph map supplies it (at most two
   positive barycentric coordinates).
4. **Mesh** is `diam (U i) ≤ 2` in the norm of `ℂ`; no separate "mesh" notion.

There is **no convexity hypothesis and no square**: the printed proof's two uses of `Q` being a
convex square (`F(Q) ⊆ Q`, and `dist(y,∂Q) > 2 ⇒ B̄(y,2) ⊆ Q`) are replaced by replaying the
argument on a single ball `B(y,c)`, `c > d`. This is the substitution in §3.

---

## 2. Dependency audit: what the machine proof actually uses

The chain is `compact_open_cover_impossible → finite_open_cover_impossible → finite_partition_impossible → {hit_center_subtype → hit_center, barycenter_two, affinePair_null}`.

| ingredient | status | substitute for |
|---|---|---|
| `PartitionOfUnity.exists_isSubordinate` | mathlib, standard | "choose a continuous partition of unity φ_a with φ_a(z) > 0 only when z ∈ U_a" |
| `barycenter_two` + `small_support_pair` (`:274`) | elementary, 25 lines | "at most two weights positive ⇒ image in a finite union of segments" |
| `affinePair_null` (`:242`) | `addHaar_affineSubspace` | "a finite union of segments has empty interior" (done as: it is Lebesgue-null, and the image contains a ball) |
| `hit_center` (`:180`) → `hit_center_subtype` (`:252`) | **winding / covering space**, via `Complex.exists_continuousOn_eqOn_exp_comp` (mathlib `BranchLogRoot.lean:37`) | **the Brouwer fixed point theorem** of the printed proof |

Two findings a referee should have:

* **The degree input is a mathlib theorem, not bespoke machinery.** `Complex.exists_continuousOn_eqOn_exp_comp`
  is the standard branch-of-log / covering-space lift for a nowhere-zero continuous map on a simply
  connected open set. `hit_center` then shows: `F` continuous on `B(y,4)` with `‖F z − z‖ ≤ 2`
  hits `y`. The loop `γ(t) = y + 3e^{it}` stays in `B(y,4)`; `H(t) = (F(γt) − y)/e^{it}` has
  `Re H ≥ 3 − 2 > 0`, so `F ∘ γ` winds once about `y` while `y ∉ F(·)` would force a
  continuous argument `Φ` with `exp Φ = F(γ·)−y` and `Φ(0) = Φ(2π)`; comparing imaginary parts
  gives `0 = −2π`. Brouwer is not used anywhere in the §7.3 obstruction.
* **The paper's Lemma 7.5 is therefore not where "bespoke" topology sits.** All three remaining
  steps are standard facts (partition of unity; convexity of a segment; nullity of a line). The
  printed proof's demand that `Q` be convex is an artefact of the Brouwer route: the winding route
  needs only a ball around the point to be hit, so it works on any `Q` containing that ball.

---

## 3. The substitution (statements, with the constants exposed)

File: `lean/CoverObstruction.lean` (225 lines, one import: `OAI.Geometry.PlaneColoring.PlanarCovers`).
Every declaration below is a re-parameterisation of the corresponding declaration in
`PlanarCovers.lean`; no new idea, but the constants become visible and the hypotheses weaken.

* `hit_center_gen` **(c, d symbolic)** [M]:
  `F` continuous on `Metric.ball y c`, `∀ z ∈ ball y c, ‖F z − z‖ ≤ d`, `0 ≤ d < c`
  ⟹ `y ∈ F '' ball y c`. (`hit_center` is `c = 4`, `d = 2`.)
  Proof: identical winding argument with the loop radius `ρ = (d+c)/2 ∈ (d,c)`; the two places the
  printed/Lean numerals appear are `3 > 2` (positivity of `Re H`) and `3 < 4` (the loop stays in the
  ball), so the hypothesis is exactly `d < c`.
* `hit_center_subtype_gen` [M]: the same for `F : Q → ℂ` with `ball y c ⊆ Q`.
* `finite_partition_impossible_gen` [M]: partition-of-unity/barycentric contradiction with
  `ball 0 R ⊆ Q`, `0 ≤ d < R`, and `‖p i − z‖ ≤ d` on the support of the `i`-th weight.
  The image of the barycentric map contains `ball 0 r` for `r = (R − d)/2 > 0` and is contained in
  a finite union of lines; `volume (ball 0 r) > 0` gives the contradiction.
* `finite_open_cover_impossible_gen` [M]: same, from a finite relatively open cover of multiplicity
  ≤ 2 with `diam ≤ d`.
* **`compact_cover_obstruction_gen`** [M] — the interface:

  > Let `Q ⊆ ℂ` be compact, `ball 0 R ⊆ Q`, `0 ≤ d < R`. Then there is **no** family
  > `U : ι → Set Q` of relatively open sets covering `Q` with `∀ z, at most two i have z ∈ U i`
  > and `diam (U i) ≤ d` for every `i`.

* **`paper_lemma_7_5`** [M] — the paper's statement, as an instance at `R = 5`, `d = 2`, for the
  axis-parallel closed square of side ten `square10 = {z : |Re z| ≤ 5 ∧ |Im z| ≤ 5}`
  (`isCompact_square10`, `ball_subset_square10 : ball 0 5 ⊆ square10`).
* `disk3_cover_obstruction` [M] — the same conclusion for `Q = closedBall 0 3` and `d = 2`,
  which is *not* a statement about a square at all: the domain is 5/2 times smaller than the
  paper's while every other hypothesis is unchanged.

**What the substitution buys.** The paper's `(side ten, mesh two)` and the Lean's
`(ball 0 5, ≤ 2)` are both far from tight: the only relation used is `R > d`, so for mesh bound `2`
any compact domain containing a disk of radius `> 2` works, and the paper's square of side ten may
be replaced by a closed square of side `> 4`, or by `closedBall 0 3`. There is no hidden sharpness
in §7.3, so §7.4 is free to deliver any diameter bound `< R`.

---

## 4. Constants audit of the §7.4 → §7.3 interface

Where the `2` in `diam ≤ 2` actually comes from [V, files as above]:

1. `Mesh.lean:no_large_positive_sequence` (:92), given a positive-coordinate connected set `K` per
   scale with `x, y ∈ K`, `2 < dist x y`, and `t n ≤ 1/16`, produces points `a, b ∈ K` (after
   escaping the holes, `connected_escape_holes`) with `dist (a n) (b n) ≥ 3/2`, then passes to a
   limit `3/2 ≤ dist p.1 p.2` and derives `spatialSupport c i` meets a ball while being disjoint from
   it. So the mesh argument's *machine* constant is `3/2`, not `1 + o(1)`; `1/16` is the only
   combinatorial input (`2 − 2/16 = 15/8 ≥ 3/2`).
2. `Five.lean:graph_map_large_positive` (:94) turns that into: some positive-coordinate preconnected
   `K ⊆ closedBall 0 5` has `2 < dist x y` for some `x, y ∈ K`.
3. `Five.lean:graph_map_small_mesh_impossible` (:22) is the contrapositive used: if every
   positive-coordinate preconnected `K` has `diam ≤ 2` then `False`, via
   `PlanarCover.compact_open_cover_impossible` at `Q = closedBall 0 5`, `d = 2`.

Interface checks:

* **Strictness is respected.** §7.4 delivers `2 < diam` (strict) against the obstruction's
  `diam ≤ d` with `d = 2`; there is no `≤ 2`-versus-`< 2` mismatch, and by §3 the obstruction
  would still hold for any `d < 5`.
* **The mesh hypothesis is applied componentwise, and that is enough.** `Five.lean` indexes the
  cover by *connected components* of `{z : (F z)_i > 0}` (`I` in `graph_map_small_mesh_impossible`)
  but states the mesh hypothesis for *arbitrary* preconnected `K`. The extra generality is
  harmless: a preconnected subset of an open set lies in a single connected component, so a
  componentwise diameter bound implies the hypothesis. (This is the one place where the Lean
  statement is *stronger* than what §7.4 proves; it is nevertheless discharged, not assumed.)
* **Boundary conditions.** Members are relatively open in `Q`, so `∂Q` is covered; no regularity of
  `∂Q` is used, and the paper's "none of the `U_a` equals `Q`, since its diameter would exceed two"
  is not needed in the Lean proof (`PartitionOfUnity.exists_is_subordinate` is applied to the cover
  of the whole space indexed by `ι`, not to a cover of `Q` by subsets of `Q` with the extra
  "≠ Q" clause). The one place a degenerate case would bite — a member of diameter `0` when
  `d = 0` — is excluded by `0 ≤ d < R` with `R > 0`: an open cover by singletons cannot cover a
  disk, which is what the theorem says.

---

## 5. What this block did *not* do (scope, so nothing here is over-claimed)

* **No line-count reduction.** The substitution is a re-parameterisation: `CoverObstruction.lean`
  reproduces the chain with symbolic constants and adds two instances. The gain is statement-level
  (constants exposed, convexity and square-shape dropped, Brouwer replaced by a mathlib lift).
* **§6 untouched.** `Theorem 6.5` (local finiteness of cyclic centres) and Lemmas 6.2–6.7 are
  dynamical/density arguments; their only topological input is compactness of a circle, and I did
  not audit them in this block.
* **Lemma 7.8 and the annulus content untouched.** The connected-preimage-crosses-the-annulus
  statement, the Fubini/straddle step (`straddle_connected_unit`) and the hole approximations of
  Lemma 7.4 are not covered by the substitution and still rest on `[P]` + partial `[V]`.
* **Lemma 7.7 (midpoint detection) audited only for location**, not for content:
  `GraphCuts.lean` carries `graphCut_contractible` (:197) and `graphMidpoint_coord_le` (:143).

---

## 6. Referee checklist

```bash
# toolchain: Lean 4.34.1 + pinned mathlib d13f23b
source scripts/env4341.sh
cd supervisor/simplify-topology/lean
lean -o CoverObstruction.olean -i CoverObstruction.ilean CoverObstruction.lean   # expect: no output
lean Check.lean                                                                  # expect: no axioms beyond propext, Classical.choice, Quot.sound
```
Recorded run of this block: `checks/lean-build3.log` = `BUILD_EXIT=0` with no diagnostics;
`checks/axioms.log`:

```
'OAI.PlanarCover.paper_lemma_7_5' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlanarCover.compact_cover_obstruction_gen' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlanarCover.hit_center_gen' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.PlanarCover.disk3_cover_obstruction' depends on axioms: [propext, Classical.choice, Quot.sound]
```

so no `sorryAx`, no `native_decide`, no extra axioms.
