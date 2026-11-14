# `graph_map_large_positive` and the small/large dichotomy (Five.lean) — source audit

Block 17, analysis only, no builds. All statements below were **read from source**, not inferred from names
or greps. Grades: **[S]** source read; **[S+]** source read and the step follows by the cited lines; **[P]**
paper; **[C]** my reading.

File: `lean/OAI/Geometry/PlaneColoring/Five.lean` unless stated. The clock reading for this block is in
`STATUS.json` (`updated_utc`).

## 1. Exact statements

```
lemma graph_map_small_mesh_impossible                                   -- Five.lean:29-36
    (F : C(closedBall 0 5, GraphSpace (⊤ : SimpleGraph (Fin 5))))
    (hmesh : ∀ (i : Fin 5) (K : Set ℂ), IsPreconnected K → K ⊆ closedBall 0 5 →
        (∀ z : closedBall 0 5, z.val ∈ K → 0 < (F z).val i) → ∀ x ∈ K, ∀ y ∈ K, dist x y ≤ 2) : False

lemma graph_map_large_positive                                          -- Five.lean:94-98
    (F : C(closedBall 0 5, GraphSpace (⊤ : SimpleGraph (Fin 5)))) :
    ∃ i : Fin 5, ∃ K : Set ℂ, IsPreconnected K ∧ K ⊆ closedBall 0 5 ∧
      (∀ z : closedBall 0 5, z.val ∈ K → 0 < (F z).val i) ∧
      ∃ x ∈ K, ∃ y ∈ K, 2 < dist x y
```

**Quantifier reading.** `hmesh` is *uniform in the label and the set*: for **every** `i` and **every**
preconnected `K ⊆ closedBall 0 5` on which the `i`-th coordinate is positive throughout. It is not "there
exists a label whose component is small". `graph_map_large_positive` is its negation in the used direction:
`∃ i ∃ K` with the same positivity and a pair at distance `> 2`. `by_contra!` on `hmesh` produces exactly the
`∃ i ∃ K ∃ x ∃ y` shape, which is why the proof is two lines (`Five.lean:99-100`).

**Supplied assumptions.** Both lemmas take *only* a continuous map `F : closedBall 0 5 → GraphSpace ⊤`.
No colouring, no measurability, no weak colouring, no `FullApprox` — these are pure topology statements about
continuous maps into the realization of `K₅`. That is a real strength: the "graph map" hypothesis is not
smuggling colouring data.

## 2. How `graph_map_small_mesh_impossible` builds the cover (body read, :38-92)

| step | line(s) | what it uses |
|---|---|---|
| `U i := {z : Q ∣ 0 < (F z).val i}` is open in the subtype | :40-44 | continuity of the coordinates of `F` |
| component family `I := {p : Fin 5 × Set Q // ∃ x, p.2 = connectedComponentIn (U p.1) x}`, `W p := p.val.2` | :45-50 | — |
| `W` members are open in `Q` | :51-55 | `IsOpen.connectedComponentIn` |
| **coverage** `∀ z : Q, ∃ p, z ∈ W p` | :56-65 | `graphRealization_sum` ($\sum_i (Fz)_i = 1$) — a point of the realization has some **positive** coordinate; the "by_contra! all ≤ 0" branch contradicts the sum being 1 |
| **multiplicity ≤ 2** | :66-74 | `graphRealization_positive_three` (`:8-20`): three points of `graphRealization ⊤` with positive coordinates cannot carry three distinct labels, since `graphEdgePoint i j t` is supported on `{i,j}`; equal labels at the same `z` give equal components (`heq`), so the three component indices satisfy `i = j ∨ i = l ∨ j = l` |
| **diameter ≤ 2** | :75-92 | the hypothesis `hmesh` applied to `i := p.val.1` and `K := Subtype.val '' W p`, with `IsPreconnected` from `IsPreconnected.image` of the (preconnected) component and `dist_eq_norm` at the end |
| contradiction | :54 | `PlanarCover.compact_open_cover_impossible` with `Q = closedBall 0 5`, `Metric.ball_subset_closedBall`, `isCompact_closedBall` |

**Boundary cases that are actually handled.** (i) the cover includes `∂Q` — `W` is a cover of the whole
subtype, and `compact_open_cover_impossible` asks exactly for relative openness in `Q`; (ii) a point with a
single positive coordinate is covered once, and the `i = j` disjunct of the triple condition absorbs repeated
membership; (iii) `connectedComponentIn` is nonempty at a point of the set, so no component is empty; (iv) the
diameter conclusion is in `dist` while the obstruction wants `‖x.val - y.val‖`, bridged by
`simpa only [dist_eq_norm]` at `:91`.

## 3. Fidelity/dependency table: which existing formal result replaces which paper use

| paper | Lean theorem | status |
|---|---|---|
| Lemma 7.5 (cover obstruction: closed square of side 10, multiplicity ≤ 2, mesh ≤ 2) | `PlanarCover.compact_open_cover_impossible` (`PlanarCovers.lean:374`), used at `Five.lean:54` with `Q = closedBall 0 5` | **[S+]** already existing result; the square is replaced by any compact `Q ⊇ ball 0 5` |
| the extraction of a graph-valued map plus "each positive-coordinate component has diameter ≤ 2" (paper §7.4's mesh step, l. 2430-2470) | `graph_map_small_mesh_impossible` (`Five.lean:29`) | **[S+]** a *derived* statement: it builds the component cover and applies Lemma 7.5 |
| the mesh/hole contradiction (paper's shrinking-budget argument) | `no_large_positive_sequence` (`Mesh.lean:92`), using `connected_escape_holes` (`Mesh.lean:12`) | **[S+]** different argument, same purpose |
| the dichotomy "either the mesh bound holds or some component is wide" | `graph_map_large_positive` (`Five.lean:94`) | **[S+]** *no paper counterpart*: the paper carries the mesh bound through Lemma 7.4's construction; the Lean splits on it |
| Proposition 7.1 and Lemmas 7.6-7.8 (continuum extraction) | **none** | **[S]** replaced by the dichotomy; see `LEMMA78-COMPARISON.md` |

So the honest description of §7's Lean route is: *Lemma 7.5 as a cover obstruction + a case split on the mesh
bound*, **not** the paper's continuum-extraction argument. That is a differing argument reaching the same
statement, not a transcription — and it is **not** an overnight discovery: every component was already in the
tree before this chat's blocks.

## 4. Is any premise genuinely unsupported?

No. Checked one by one:

* `hmesh` is a hypothesis of `graph_map_small_mesh_impossible` but is **discharged** by `graph_map_large_positive`,
  which is proved from the topology alone; the final consumer `no_measurable_weak_five_coloring` uses only
  `graph_map_large_positive` (`Five.lean:120-124`). So the mesh bound is never assumed.
* positivity of some coordinate at every point is **proved** from `graphRealization_sum`, not assumed.
* multiplicity ≤ 2 is **proved** from the graph structure (`graphRealization_positive_three`), not assumed.
* continuity of `F` is carried by the codomain `C(…)`, and in `no_measurable_weak_five_coloring` it is
  `(F n).map`, a continuous map by construction.
* the numeric side (`α = 1/10 < 1/5`, `t n = min (1/16) (1/(n+1)) ≤ 1/16`, `t n → 0`) is supplied at
  `Five.lean:105-107` and checked by `norm_num`.

The one thing I did **not** verify, and which is not an unsupported premise but an unchecked comparison, is
whether the paper's own §7.4 mesh argument and this dichotomy prove the *same* intermediate statement — a
paper-level mapping, [P], outside what source reading can settle.

## 5. Retained corrections

* `connected_escape_holes` is **not** Lemma 7.8 (`LEMMA78-COMPARISON.md`).
* `diskAnnulus d = closedBall d.center (1 + d.radius) \ ball d.center (1 - d.radius)`, area `4πr`
  for `0 ≤ r ≤ 1` — corrected in `LEMMA78-COMPARISON.md` §3 (my earlier "`ball(c,r+1)` minus
  `closedBall(c,r)`" was wrong at both endpoints).
* `initialDisks`' L-part carries `core := true` (the paper's core family); `centerDisks` is a separate family
  with `core := false`.
