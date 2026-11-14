# Audit of the periodic-to-arbitrary density bridge (closest-source comparison)

Written by M for block `K15-REVIEW-0223-M`. The bridge is `K15-C002b` (repaired
periodic approximation). This file compares it with the closest source actually in
the repository and states what is accepted, what is open.

## 1. What the two sources do

**Cohn–Elkies 2003, Appendix A ("Technicalities about density"), Annals 157,
pp. 708–709** — read from `Literature/Papers/CohnElkies2003.pdf`:

1. Density is defined by a limit over `B(p,r)`; they note (citing [Gr] = Groemer)
   that if the limit exists for one `p` it exists for all and is equal.
2. *Uniform* density: the limit exists uniformly in `p`; then the limit also holds
   for `rR + p` for any compact `R` that is the closure of its interior.
3. Upper density: `Δ̄ = lim_{r→∞} sup_{p∈R^n} vol(B(p,r) ∩ P)/vol B(p,r)`, and
   "[i]t is proved in [Gr] that the supremum of all upper densities is achieved by a
   uniformly dense packing".
4. **The reduction.** Let `P` be *that* uniformly dense packing of density `Δ`.
   Take the fundamental parallelotope `R` of any lattice `Λ`, choose `r` large so
   the spheres entirely inside `rR` carry at least `(Δ − ε) vol(rR)` "because only a
   negligible fraction of the spheres can intersect the sides of `rR`", and
   periodise by `rΛ`. The result has density `≥ Δ − ε`.

**`K15-C002b` (this project).** Take *any* 2-separated packing `Λ`. Tile by cubes of
side `S`; let `C*` be a tile with the maximal number of centres; delete the `2`-wide
slabs at its boundary and periodise by `Sℤ³`. Losses: `O(S/R)` (tile geometry) and
`O(1/S)` (boundary slabs), both explicit; a separate case for `δ(Λ) = 0`.

## 2. Comparison

| Aspect | Cohn–Elkies App. A | `K15-C002b` |
| --- | --- | --- |
| starting object | a **uniformly dense extremal** packing, whose existence is Groemer's theorem | **any** packing, no extremal object needed |
| boundary control | asserted: "only a negligible fraction … can intersect the sides" | quantitative: `O(R²S)` centres in a shell of width `2S√3`, via disjoint unit balls |
| error terms | `ε` from `r` large at fixed `R`; uniformity from [Gr] | `O(S/R) + O(1/S)`, both explicit, with the diagonal choice `R(S)/S → ∞` |
| density notion | `limsup sup_p` (uniform upper density) | `limsup_R` at a fixed centre, i.e. `K15-C001` |
| what is periodised | the spheres *entirely inside* `rR` | the centres inside a cube minus a slab; the periodic set is `Λ_S + Sℤ³` |
| zero-density case | not distinguished | separated (the bound holds vacuously) |

**Assessment.** The two arguments are different in structure, not merely in
notation: CE pass to an extremal, uniformly dense packing and then need only a
"negligible fraction" assertion, while `K15-C002b` stays with the given packing and
pays with two explicit losses. Neither can be obtained from the other by
rearranging constants. `K15-C002b` is *more* self-contained (no Groemer), *weaker*
in that it delivers `≥ δ(Λ) − ε` for the given `Λ` rather than for the extremal one
— which is all the bound needs — and *more* quantitative.

## 3. What is accepted, and what is open

**Accepted.**
- The reduction is valid for 2-separated packings, with explicit losses
  (`K15-C002b`, audited item by item in `K15-C037`).
- The project's `limsup`-at-a-fixed-centre density and CE's uniform upper density
  agree for 2-separated packings: the two differ by a boundary term
  `O(R²)/R³ → 0` (disjoint unit balls), so any bound proved for one is valid for
  the other. This is used implicitly whenever a CE number is quoted in
  `Main/RESULTS.md`.
- The relation between occupied-volume density and centre density,
  `δ = (4π/3)c`, including the counting-to-volume step (`K15-C024` items 3–4).

**Open.**
1. **Uniformity bookkeeping in `K15-C002b`.** The `o(1)` in
   `n(C*)/S³ ≥ c − O(S/R)` is uniform in `S` only after the diagonal choice
   `R = R(S)`, `R/S → ∞`. Written out in `K15-C037`, but not Lean-checked.
2. **The `δ(Λ) = 0` case** is separated by an argument ("the right side is ≥ 0"),
   correct but not integrated into the single inequality.
3. **Non-saturated packings**: the bridge does not need saturation, but Hales'
   Lemma 3.3 does (it uses `Ω(v) ⊆ B(v,2)`); the passage from an arbitrary packing
   to a saturated one is by Zorn, and is used in `K15-C043`. That step is standard
   and is recorded, not proved.
4. **Hales' route needs no bridge at all** — Lemma 3.3 works with local densities
   and `limsup` directly. So for the geometric route the bridge is not on the
   critical path; it matters only for the analytic (certificate) route.

## 4. Closest-source note on [Gr]

CE cite Groemer for two facts (translation-invariance of the density limit, and
existence of a uniformly dense packing attaining the supremal upper density). This
project does not have Groemer's paper; `K15-C002b` avoids both facts, which is why
it is written out. Nothing in the ledger depends on [Gr].
