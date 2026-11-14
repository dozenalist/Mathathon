# Audit of the cone extension of AC: geometry, the two rigidity lemmas, and the corrected discrete test

Analysis only; no computation. Sources: `Rigidity.lean` (179–196, 418–432), `AngularBoundary.lean`
(147, 235–300), `BoundaryTrace.lean` (280–290). Grades **[S]** source-read, **[P]** hand-proved,
**[C]** cited (Astra/supervisor, conditional), **[X]** open.

## 0. Two retractions

**(0a) The `q_i` interpretation.** I treated `q = (q_0,…,q_5)` as a **colour word** and read the transition
label sets as the consecutive pairs `{q_i, q_{i+1}}`. **Wrong.** The `q_i` are **directions assigned to the
fixed cycle edges** `E_i = {i, i+1 mod 6}`; the *labels* of the cycle are its vertex labels, and an edge's
exclusion is the label set of the vertices it joins. For `q = (0,0,1,3,3,4)` the edges `E_0, E_1, E_2` carry
directions `0, 0, 1` and their labels are `{0,1}, {1,2}, {2,3}`, whose union is `{0,1,2,3}` — so they exclude
`{0,1,2,3}` and leave `{4,5}`, as the supervisor states. My earlier computation of `{0,1},{1,3},{3,4},{4,0}`
and complement `{2,5}` is **withdrawn**.

**(0b) Open arcs and their six translates.** I wrote that six translates of a `60°` arc tile the circle and
that the covering condition therefore "holds" at the tight spread `w = 60°`. **Wrong for open sets:** the six
translates of an **open** arc of length exactly `τ = π/3` cover the circle **minus the six orbit points of an
endpoint**, so an orbit can lie entirely in the complement. Correct formulation, with the open/closed
bookkeeping:

* the rigidity applies on the **open** set `G = L ∩ (L − τ)`, so the conclusion is `D ⊆ Gᶜ`, and `Gᶜ` is
  **closed**;
* hence the usable condition is stated on the closed set: `D ⊆ closure(Exc ∪ (Exc − τ))`, and `D` is closed,
  `τ`-invariant and nonempty, so it contains a full six-orbit;
* **therefore the tight case `w = 60°` fails**: there the closed arcs have length exactly `τ`, the translates
  meet only at endpoints, the union is the whole circle, so every orbit is admissible and no contradiction
  follows. A **strict** inequality `w < 60°` is required, so that the translates overlap by a positive amount.
  (In the aligned AC case the exceptional set is two *points*, `|B ∪ (B−τ)| ≤ 4`, which is a cardinality bound
  and is unaffected by open/closed issues.)

## 1. The cone argument, checked against the source

**Source lemmas [S].**

* `binary_open_local_rigidity` (Rigidity.lean:179–187): for measurable `c`, `WeakColoring k c`, **two open
  sets `U, V`** each confined a.e. to `{a,b}`, a point **`p ∈ U`**, and **two unit vectors `v, w` with
  `p + v, p + w ∈ V` and `transverseDet v w ≠ 0`**, the conclusion is
  `∃ r > 0, ∃ i, ∀ᵐ q ∈ ball p r, c q = i` — **a.e. monochromatic ball**.
* `connected_local_ae_constant` (Rigidity.lean:418): a **connected** `S` whose every point lies in some
  `essentialLocalSet c i` is a.e. monochromatic, with one label (`S ⊆ essentialLocalSet c i`).

**The geometry [P], all of it.** Let the approach directions lie in a **closed cone** of aperture `a ≤ 60°`
about the axis `u`. The set of directions with a common strictly positive inner product is
`I = {t : |t − u| < 90° − a/2}`, an **open arc of half-width `90° − a/2 ≥ 60°`** (so at `a = 60°` its width is
exactly `120°` ✓ as stated). For `p = x + r e(θ)` with `1 < r < 2`, put `α := arccos(r/2) ∈ (0°, 60°)` (defined
because `r/2 ∈ (1/2, 1)`) and `β± := θ ± α`. Then

    |p − (x + e(β±))|² = r² + 1 − 2r cos α = r² + 1 − 2r·(r/2) = 1,

so **`x + e(β±)` are unit from `p`** ✓ — the exact identity the sketch uses. And `β± ∈ I` iff
`|θ − u| + α < 90° − a/2`; at `a = 60°` this reads `|θ − u| < 60° − α`, which is satisfiable **for every
`r ∈ (1, 2)`** precisely because `α < 60° ⟺ r > 1` ✓. Hence the **crescent**

    S_a := { x + r e(θ) : 1 < r < 2, |θ − u| < 90° − a/2 − arccos(r/2) }

is nonempty, **open** and **connected** ✓ [P].

**The delicate point the sketch glosses, and why it is harmless.** The points `x + e(β±)` have radius **exactly
1**, so they are **not** in `W`: the outer strips are one-sided (`1 < r < 1+δ`). What is needed — and what the
sketch's "transverse outward perturbation" supplies — is: move from `x + e(β±)` a small amount **along the
circle about `p`** in the direction of increasing `|· − x|`. Since `|p − x| = r > 1` strictly, that outward
displacement has a positive radial component, so for small perturbations the images still satisfy
`1 < r' < 1+δ` and remain in the strip, hence in `W` ✓ **[P]**. This is exactly where the hypothesis `r > 1`
(not `r ≥ 1`) is used, and it is the same reason the cone's aperture `60°` is the tight value.

**Non-parallelism is free [P].** The two neighbour directions are `u± = e(β±) − r e(θ)`. They are antiparallel
iff `e(β₊) + e(β₋) = 2r e(θ)`, i.e. `2 cos α · e(θ) = 2r e(θ)`, i.e. `cos α = r`; but `cos α = r/2` and
`r > 0`, so this is impossible. Hence `transverseDet u₊ u₋ ≠ 0` automatically ✓.

**The contradiction [P].** Take `U = V = W` (open by `isOpen_iInter_of_finite`; confined to `{a,b}` a.e. by
the support exclusions). For each `p ∈ S_a` the two outward-perturbed neighbours are nonparallel unit
neighbours of `p` inside `W`, so `binary_open_local_rigidity` gives a ball around `p` that is **a.e.
monochromatic**. An a.e.-monochromatic open set violates the a.e. properness of `WeakColoring`: the pairs
`(q, q') ∈ B × B` with `|q − q'| = 1` form a positive-measure family, a.e. of whose members are pair-typical,
and all carry the same label. **`connected_local_ae_constant` is not needed for the contradiction itself**
(the rigidity already gives a monochromatic ball at one point); it is what upgrades the per-point conclusion
to a single label on the whole crescent, should one want the larger statement.

**No `BinaryCenter` is used** ✓ — this is the structural novelty over AC, and it is why the cone version
escapes the aligned-direction obstruction of `SIGNED-DOMAIN-AUDIT.md` §1.

## 2. The conditional theorem

> **Theorem AC-cone (paper candidate, [C], pending review).** Let `c` be measurable with `WeakColoring k c`,
> `x : ℂ`, `ι` finite, `K : ι → Set ℂ`, and suppose all the approach directions `v i` lie in a **closed cone
> of aperture `≤ 60°`**. Let `H i` be label sets with `Disjoint (spatialSupport c j) (Straddle (K i))` for
> `j ∈ H i`, and suppose `⋂_i Straddle (K i) ≠ ∅` meets the outer strips, and that the complement of
> `⋃_i H i` has at most two elements. Then `False`.

Proof: §1 — crescent ⇒ `binary_open_local_rigidity` with `U = V = W` ⇒ a.e.-monochromatic ball ⇒ contradicts
a.e. properness. The aperture bound `≤ 60°` enters twice: it makes `I` at least `120°` wide, and it makes
`α < 60°` compatible with `β ∈ I` for every `r > 1`.

**Hypotheses I would want tightened before banking:** (i) the family must be finite (used for the width
minimum, as in AC); (ii) `W` must contain the outer strips — this is the content of the cone hypothesis plus
`finite_positive_lower_bound`; (iii) the "≤ 2 labels" condition is on the union of the `H i`.

## 3. Corrected discrete test

With `q_i` read as the **direction of edge `E_i`**, the cone filter on `q = (0,0,1,3,3,4)` selects the edge
subfamily whose directions lie in a closed `60°` cone. Under the discrete indexing (`0` and `1` adjacent
directions, `60°` apart) the edges `E_0, E_1, E_2` have directions `0, 0, 1` — inside one `60°` cone — and
their cycle labels `{0,1}, {1,2}, {2,3}` give union `{0,1,2,3}`, complement **`{4,5}` of size 2**. So
**AC-cone applies to this `q` and excludes it**, conditional on the printed theorem. The edges `E_3, E_4,
E_5` (directions `3,3,4`) span `180°` from `E_0` and are not in the same cone; they are irrelevant to the
filter. The supervisor's count (174 audited words, 6 survivors) is `[C]` and I have not recomputed it.

## 4. Status and limits

* Retracted: the `q`-as-colour-word reading (0a) and the open-arc tiling claim, replaced by the strict
  `w < 60°` requirement (0b).
* Verified by hand: the cone geometry (`cos α = r/2`; the crescent; `β ∈ I ⟺ r > 1` at `a = 60°`), the
  necessary outward perturbation (needed because the strip is open in `r`), and automatic non-parallelism.
* Source-checked: both rigidity lemmas have exactly the hypotheses the sketch needs, with `U = V = W`.
* Not claimed: that AC-cone is banked (it is a paper candidate under review); any global six-colour
  conclusion; anything about non-cone direction families, `(W)`, or `χ(ℝ²)`.
