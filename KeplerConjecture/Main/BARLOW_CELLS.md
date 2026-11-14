# Every Voronoi cell of a Barlow packing has volume `√32` — a proof

> **Independent review pending (03:53 Pacific):** Lemma 1 does not establish
> redundancy from containment of the full intersection. E is checking the
> contact-only polytope and downstream claims. The author's PROVED labels below
> remain a working draft; see [the review](REVIEW_2026-11-14_0353.md).

Block `K15-REVIEW-0308-M-CONTINUE`, task 3. `K15-C091` proved that the **average** cell
volume is `√32` in every Barlow stacking and produced six stackings whose cells are all
`√32` numerically, but recorded the uniformity as *evidence, not proof*. This file
closes it: **every cell of every Barlow packing has volume `4√2 = √32`**. The proof is
four short steps and needs no computation; the numbers in §5 test the steps that could
have been wrong.

## 0. The class, and its scope

`Λ = ⟨a₁,a₂⟩` with `|a₁| = |a₂| = |a₁−a₂| = 2` — the triangular lattice with nearest
neighbour 2. Put

```
T = (a₁+a₂)/3,   |T| = 2/√3,      H = √(8/3),    |T|² + H² = 4.
```

A **Barlow packing** is given by a stacking `s : Z → Z/3Z` with

```
s_{k+1} − s_k  ≡  ±1  (mod 3)     for every k
```

and is the set of centres

```
P(s) = ⋃_{k ∈ Z}  ( Λ + s_k T ) × { k H } .
```

Every consecutive pair of layers is at in-plane offset equivalent to `±T`, which gives
`|T|² + H² = 4`, i.e. distance exactly 2, and in-layer neighbours are at distance 2; so
`P(s)` is 2-separated by construction (`K15-C091` checked this numerically as well).

**Scope.** This is the *layered* class, exactly the class `K15-C091` tested. The
classical characterisation "every sphere touches 12 others ⟹ layered" (Barlow, and in
modern form the subject of `Bezdek–Kuperberg`-type results) is **not** used and **not**
verified here; a packing that is 12-contact but not of the form `P(s)` is outside the
theorem as stated. Nothing below depends on that characterisation.

Throughout, `Ω(v)` is the Voronoi cell of the site `v`, `b(v) = √32 − vol Ω(v)`.

## 1. Four elementary facts

**(F1) Distances from a site.** Take `v = 0`, a site of layer 0, and note `s_0` can be
taken to be `0` (translate in the plane; cells are carried to cells).

| source | in-plane distance | 3-D distance |
| --- | --- | --- |
| own layer, `λ ∈ Λ∖{0}` | `2, 2√3, 4, …` | `2, 2√3, 4, …` |
| layer `±1`, nearest coset point | `2/√3` (three of them) | `2` |
| layer `±1`, next | `≥ 4/√3` | `≥ √(16/3 + 8/3) = 2√2` |
| layer `±2` | `≥ 0` | `≥ 2H = 3.266` |
| layer `±j`, `j ≥ 3` | `≥ 0` | `≥ 3H = 4.90` |

The in-plane distances from `T` to `Λ` are `2/√3` (attained exactly three times:
`λ = 0, a₁, a₂`, because `T` is the centroid of that equilateral triangle) and then
`≥ 4/√3`. Hence:

> **exactly twelve centres at distance 2** — the six in-layer neighbours, and three in
> each adjacent layer — and **every other centre is at distance `≥ 2√2`**, with equality
> attained in the adjacent layers.

**(F2) Layer periodicity.** `P(s)` is invariant under `Λ`: every layer is `Λ + s_k T`.
So the translation by `λ ∈ Λ` maps `Ω(v)` to `Ω(v+λ)`, and **all cells within one layer
are congruent**. Write `V_k` for the common volume in layer `k`. (Cells in *different*
layers need not be congruent — see §5 — so this fact alone does not finish the proof.)

**(F3) Covering radius `≤ √2`.** The triangular lattice has covering radius `2/√3`
(the circumradius of the equilateral triangle with side 2). Let `x ∈ R³` and let `k` be a
layer whose plane is within `H/2` of `x` (consecutive planes are `H` apart, so one is).
Then

```
dist(x, P(s))²  ≤  (2/√3)²  +  (H/2)²  =  4/3 + 2/3  =  2.
```

So every point of space is within `√2` of a centre. In particular, for `x ∈ Ω(v)`,
`|x−v| ≤ dist(x, P(s)) ≤ √2`, i.e. `Ω(v) ⊆ B(v,√2)`.

**(F4) The average is `√32`.** A layer contains one centre per area `2√3`
(`det(a₁,a₂) = 2√3`) and the layer spacing is `H`, so the volume per centre is

```
2√3 · H = 2√3 · √(8/3) = 2√3 · (2√2/√3) = 4√2 = √32 = 5.656854249492…,
```

in every Barlow packing, independent of `s`. Equivalently the density is `π/√18`.

## 2. The two lemmas

> **Lemma 1 (the cell is the contact cell).** `Ω(v)` is the intersection of the twelve
> half-spaces determined by the twelve contacts alone.

*Proof.* Let `c` be a centre that is not one of the twelve. By (F1), `|c−v| ≥ 2√2`, so the
half-space `{x : |x−v| ≤ |x−c|}` contains the ball `B(v, |c−v|/2) ⊇ B(v,√2)`. By (F3),
`Ω(v) ⊆ B(v,√2)`. So every non-contact half-space contains `Ω(v)`, hence is redundant. ∎

(Note the equality case: `|c−v| = 2√2` does occur, so the redundant half-spaces are
*tangent* to `B(v,√2)`, not strictly redundant. Lemma 1 is still exact.)

> **Lemma 2 (exactly two contact cells).** Up to an isometry of `R³` fixing `v`, the
> twelve contacts take exactly **two** values, and they are the contact sets of `fcc` and
> of `hcp`.

*Proof.* The six in-layer contacts are the six nearest neighbours of the triangular
lattice — a regular hexagon, whose symmetry group is transitive on the choices of an
"up" direction, so it contributes no parameter. The three contacts in the layer above lie
in the coset `δ₊T + Λ`, where `δ₊ ∈ {+1,−1}` is the step from layer `k` to `k+1`; the
three below lie in `−δ₋T + Λ`, with `δ₋` the step from `k−1` to `k`. The two non-zero
cosets of `Λ` inside `(1/3)Λ` are `±T + Λ`, and the in-plane nearest sets of the two are

```
𝒜 = {30°, 150°, 270°}   (coset +T + Λ,  contacts at T − 0, T − a₁, T − a₂)
ℬ = {90°, 210°, 330°}   (coset −T + Λ)   =  𝒜 + 60°.
```

So the upper triple is in class `𝒜` when `δ₊ = +1` and in `ℬ` when `δ₊ = −1`, and the
lower triple is in class `𝒜` when `δ₋ = −1` and in `ℬ` when `δ₋ = +1`. Two cases remain:

- `δ₊ = δ₋`: the upper and lower triples are in *different* azimuth classes — the
  **fcc** configuration (`A B C`: the neighbour on one side is `B`, on the other `C`);
- `δ₊ = −δ₋`: both triples are in the *same* class — the **hcp** configuration
  (`A B A`: the neighbour on both sides is `B`).

A rotation by `60°` about the layer normal exchanges `𝒜` and `ℬ` (and is an isometry of
`R³`, whether or not it is a symmetry of the packing), and the reflection `z ↦ −z`
exchanges the upper and lower triples; together these reduce the four sign combinations
to the two cases above. Nothing else varies. ∎

**Caution recorded.** The `60°` rotation is *not* in general a symmetry of `P(s)` — along
`[111]` an fcc packing has three-fold, not six-fold, symmetry — so `𝒜` and `ℬ` are
genuinely different; the classification uses only that an isometry of `R³` carries one
cell to the other, which is what congruence of cells means.

## 3. The theorem

> **Theorem.** Every Voronoi cell of every Barlow packing has volume `4√2 = √32`.

*Proof.* Let `v` be a site, in layer `k`. By (F2) and Lemma 1, `Ω(v)` is the contact cell,
so by Lemma 2 it is congruent to the fcc cell or to the hcp cell. Let `A_fcc`, `A_hcp` be
their volumes. By (F4) the average of `V_k` over any period is `4√2`. Now take two
particular stackings:

- `ABCABC…` (`s_k = k mod 3`) has `δ₊ = δ₋ = +1` in every layer, so **every** cell is
  the fcc cell; its average is `A_fcc`, so `A_fcc = 4√2`;
- `ABAB…` (`s = (0,1)`) has `δ₊ = −δ₋` in every layer, so **every** cell is the hcp
  cell; its average is `A_hcp`, so `A_hcp = 4√2`.

Both are `4√2`, and every cell is one of the two. ∎

**Remark.** The theorem needs no vertex lists and no interval arithmetic: the only
"computation" is `2√3·√(8/3) = 4√2` and the three in-plane distances `2/√3`. The two
cells have **equal volume but are not congruent** — `fcc` gives the rhombic dodecahedron
(12 rhombic faces, face-normal dot products in `{−1,−½,0,½}`), `hcp` gives the
trapezorhombic dodecahedron (12 quadrilateral faces, dot products including `−5/6` and
`−1/3`). Both have 14 vertices and circumradius `√2`. So *"the cells are all `√32`"* is a
volume statement about a two-element family, not a shape statement about one polyhedron.

**Corollary (the equality case is tiny).** `b ≡ 0` on every Barlow packing. Hence at such
a packing every cut of `K15-C044` is *tight*: `Σ_U b = 0 = Φ|δ⁺_R(U)|` with `Φ = 0` and
`φ ≡ 0`. So `t*(Λ) = 0` on every Barlow packing, and the equality case of the cut
condition at `Φ = 0` is the two-shape family of Lemma 2 — a *finite local*
classification, in contrast with Hales' decomposition stars.

## 4. Consequences for the ledger

1. **`K15-C091` upgraded.** `TESTED_FINITE` → the uniformity is `PROVED` for all `s`.
   The six stackings are now examples rather than evidence.
2. **`K15-C078` extended.** That claim proved the cut condition trivial on `fcc` and
   `hcp`; by the theorem it is trivial (with `Φ = 0`) on **every** Barlow packing. The
   cut formulation is therefore consistent with the whole known extremal family, not only
   with its two uniform members.
3. **No slack at the extremal points (new).** By the corollary, a proof of the cut
   condition cannot proceed by exhibiting a *positive* margin: at every Barlow packing the
   margin is exactly zero, for every cut. Any argument of the form "find `δ > 0` with
   `Σ_U b ≤ (Φ−δ)|δ⁺(U)|` on a compact class and use `K15-C087` for large `U`" fails at
   the extremal configurations themselves. This is the transfer-route analogue of Hales'
   observation that pure subdivision fails at a tight point (§17.2 of his proof).
4. **It is not a step toward the density bound.** `K15-C087` is untouched: the cut
   condition still implies `δ ≤ π/√18` and is not implied by it. The theorem says the
   cut condition is *satisfiable* at the extremal packings; it does not make it easier
   anywhere else.

## 5. What the numerics test

The proof's steps that could have been wrong, and the checks that they are not.
`Computation/barlow_cells.py` and `Computation/barlow_sweep.py`; all times are seconds on
the SAIR VM.

`barlow_cells.py` builds a periodic Barlow packing, takes an explicit site, computes its
cell by half-space intersection (vertex enumeration over triples with a feasibility test),
and reports, per layer: the number of centres at distance 2, the next distance, the
volume from the 12 contacts alone, the volume from *all* centres within radius 5, the
circumradius, the face sizes, and the largest value of `max_vertex n·x − 1` over the
non-contact half-spaces (positive would mean a non-contact cuts the cell, i.e. that
Lemma 1 failed).

| stacking | period | legal | types seen | all 12 cells `√32`? |
| --- | --- | --- | --- | --- |
| `ABC` (fcc) | 3 | yes | fcc ×3 | yes |
| `ABA` (hcp) | 2 | yes | hcp ×2 | yes |
| `ABAC` | 4 | yes | fcc, hcp alternating | yes |
| `ABCB` | 4 | yes | hcp, fcc alternating | yes |
| `ABABAC` | 6 | yes | both | yes |
| `ABCACB` | 6 | yes | both | yes |
| `ABCABCACB` | 9 | yes | both | yes |
| `ABACABA` | 7 | **no** | — | wrap step `0 ≢ ±1`, excluded as in `K15-C091` |
| `ABABCBCA` | 8 | **no** | — | wrap step `0 ≢ ±1`, excluded |

Across every layer of every legal stacking above: `#@2 = 12` and next distance
`2√2 = 2.828427` exactly as (F1) predicts; `V₁₂ = V_full = 5.656854249492` to `1e−12`;
circumradius `1.414213562 = √2`; all faces quadrilateral, 14 vertices; and the
non-contact slack is `0` to `1e−16` — i.e. the far half-spaces are **tangent**, exactly
the equality case named under Lemma 1. The face-normal dot-product fingerprints of the
fcc and hcp cells differ (`−½` only versus `−5/6, −1/3` as well), confirming Lemma 2's
"two shapes, not one".

The committed script also sweeps: `python3 barlow_cells.py --sweep 6` adds 6 random legal
stackings of each period 3–10 — **48 stackings, 346 layer analyses, 0 violations** — and
re-checks `#@2 = 12`, the next distance, both volumes, the tangency slack (`≤ 1e−12`) and
the type dichotomy on every layer. Exit status 0. It also samples the covering radius, to
test (F3): largest sampled value `1.379` at `ABC`, against the proved bound `√2 = 1.41421`.
(Runtime 22 s for the named stackings, about 6 min for `--sweep 6`, on the SAIR VM.)

## 6. Not claimed

- **Not the classification of densest packings.** The theorem says `b ≡ 0` on Barlow
  packings. It does **not** say that `b ≡ 0` forces a packing to be Barlow: that would
  require knowing all densest packings, which is open.
- **Not the classical 12-contact characterisation** (§0).
- **Not new bounds.** No number in `RESULTS.md` moves.
- **Not an improvement to the cut condition.** The corollary makes it *harder*, not
  easier: it removes the possibility of a slack argument. That is a real cost and it is
  the main reason to record it.
