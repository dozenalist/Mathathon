# Where the §7 topology substitution stops being evidence for §7

Purpose: make sure that a successful local compilation of
`supervisor/simplify-topology/lean/CoverObstruction.lean` is not read as "§7 is now proved".
Grades as elsewhere: **[K?]** compiled by its owner, logs present, not re-run by me; **[S]** source
read only; **[P]** paper argument.

## 1. The structural wall (exact, verified)

* `CoverObstruction.lean` proves `OAI.PlanarCover.paper_lemma_7_5`,
  `compact_cover_obstruction_gen`, `hit_center_gen`, `disk3_cover_obstruction` — statements about an
  **abstract** relatively open cover of a compact `Q ⊇ ball 0 R` with member diameter `d < R`.
* **Nothing in `lean/` refers to any of them.** `rg -n 'compact_cover_obstruction_gen|paper_lemma_7_5'
  lean/` returns zero hits. The development's only consumer of a cover obstruction is
  `lean/OAI/Geometry/PlaneColoring/Five.lean:54`, which applies the *in-tree*
  `PlanarCover.compact_open_cover_impossible` (`PlanarCovers.lean:374`).
* The new lemmas live outside the `OAI` module tree, so no module of the development can import them
  as things stand. Making the substitution real is a **source edit plus a rebuild of the 25-module
  cone**, not a corollary of the compilation. Until that edit is made and rebuilt, the substitution is
  a parallel statement, and §7's compiled content is still the old lemma.

## 2. The analytic wall (the earliest one, [S] + [P])

Walk the chain that actually proves the lower bound, backwards from the cover obstruction:

| step | where | status |
|---|---|---|
| §7.4 cover of the disk by positive-coordinate components, multiplicity ≤ 2 | `Five.lean:31-53` (`graph_map_small_mesh_impossible`, `hU`, `hW`, `I`, `W`) | **[S]** in-tree proof, feeds the obstruction directly |
| the mesh bound (member diameter ≤ 2) | `Five.lean:29` hypothesis `hmesh` | **not a supplied hypothesis in the end**: `graph_map_large_positive` (`Five.lean:94`) runs `by_contra`, so the final theorem splits into "mesh bound holds → obstruction" and "some component is wider than 2 → `Mesh.no_large_positive_sequence`". Both branches are in-tree. |
| connected straddling of the unit circle (the Fubini/`(7.1)` step) | `AngularBoundary.lean:156` `straddle_connected_unit`, used at `Mesh.lean:140`, `ContinuumLimits.lean:213` | **[S]** it exists as a proved lemma — so this is *not* the wall, contrary to the most pessimistic reading of the topology document's §5 |
| the approximating continuous graph maps and their agreement with the colouring off the holes | `FullApproximation.lean:255` (`structure FullApprox`, field `agrees`) and its producer `fullApprox_exists` (:330) / `fullApprox_exists_of_finite_core` (:268) | **[S] this is the earliest wall I can name** |

Why the last row is the answer. `FullApprox.agrees` says: for `z` outside the holes,
`(map z).val = thresholdMap c ε α z.val`. The auxiliary lemma at `FullApproximation.lean:71` takes
that agreement as a **hypothesis** `hf`; `fullApprox_exists_of_finite_core` is the ~60-line proof that
discharges it (plus `disjoint`, `positive`, `sum_lt`) from the colouring. Its paper sources are exactly
the two items the topology document itself lists as untouched:

* paper Lemma 7.4 (hole approximation, `[P]` + partial `[V]` per that document's §5), and
* paper Lemma 7.8 (connected components of inverse images crossing the annulus, `[P]`),

together with the mid-point detection of Lemma 7.7, which the same document says was audited "only
for location".

So: **the first point at which the compiled §7 chain stops certifying the paper is the agreement
interface at `FullApproximation.lean:71/255-265`, and it sits *upstream* of the cover obstruction.**
Compiling the cover obstruction — with either the old or the substituted statement — says nothing
about it. I have not audited `FullApproximation.lean`'s proof body; the claim here is about *where* the
interface is, not that it is wrong.

## 2a. RETRACTION (block 16): I mislabelled Lemma 7.8

This document's §2 (and `FULLAPPROX-AGREES-AUDIT.md` §3) called `connected_escape_holes` (`Mesh.lean:12`)
"the tree's counterpart of Lemma 7.8". It is not: `connected_escape_holes` is a point-displacement lemma for
a preconnected set (`∃ a' ∈ K, a' ∉ diskHoles S, dist a a' ≤ 2t`), while Lemma 7.8 is a winding/fundamental-group
statement about a component of `g⁻¹({m})` meeting both boundary circles of an annulus. There is **no**
formal counterpart of 7.8, 7.7 or the reduced-word machinery anywhere in `lean/OAI` (grep for `winding`,
`reducedWord`, `free_homotopic`: no hits), and the word "annulus" in the Lean means `diskAnnulus`, a unit-thick
rim used for area budgets. See `LEMMA78-COMPARISON.md` for the side-by-side and for why the dichotomy route at
`Five.lean:94` makes 7.8 unnecessary rather than missing.

## 3. What a referee should ask for next

1. A theorem in `lean/` (not in `supervisor/`) whose statement is §7's cover obstruction with the
   constants exposed, and `Five.lean:54` re-pointed at it — that closes §1.
2. A statement-level audit of `fullApprox_exists_of_finite_core`: is `agrees` really derived, or is it
   weakened on the way (e.g. agreement only on a conull set, only outside a shrinking set, or with
   `thresholdMap`'s parameters relaxed)? That closes §2.
3. Only then does "§7 is fully formalised" become a claim about the paper's §7 rather than about an
   in-tree reformulation of it.
