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

---

# Part 2 — line-by-line audit against Cohn–Elkies Appendix A, and the exact
# logical form of the bridge

Written for block `K15-REVIEW-0308-M-CONTINUE`, task 4. Part 1 above compared the two
arguments structurally. This part does the item-by-item audit and then fixes the one
thing about the bridge that has been repeatedly mis-stated in the ledger.

## 5. Correspondence, item by item

`K15-C002b`'s chain has four items and a case split (ledger, lines 336–357). CE's
Appendix A has four moves. The correspondence is *not* one-to-one, and the row order
below is by CE's moves, because that is where a reader is likely to look.

| CE App. A move | `K15-C002b` counterpart | What `K15-C002b` has to add |
| --- | --- | --- |
| (a1) the density limit, if it exists at one centre, exists at all and is equal (via Groemer) | **not used** | nothing — `K15-C001` defines `δ` as a `limsup` at a fixed centre, so no invariance is needed |
| (a2) uniform density, and passage to a compact set that is the closure of its interior | **not used** | nothing — the tiling by cubes of side `S` is a fixed concrete family, no compact-limit argument |
| (a3) every packing has a *uniformly dense* one with the same upper density (Groemer) | **replaced** by "take the tile `C*` with the maximal centre count" | the whole of item (iii): a counting argument that a maximal tile is not atypical. This is where `#C_in(R) ≤ vol B(0,R)/S³` (item (i)) and the `O(R²S)` boundary-shell count (item (ii)) are spent |
| (a4) "only a negligible fraction of the spheres can intersect the sides of `rR`"; periodise by `rΛ` | item (ii) quantitatively, then item (iv): periodise `Λ ∩ (z + [2,S−2]³)` | the *quantitative* shell count `O(R²S)`, obtained from 2-separation via disjoint unit balls; and the observation that deleting a 2-wide slab costs `O(S²)` centres, which is `K15-C083`'s `12/S` |
| (a5) the resulting periodic packing has density `≥ Δ − ε` | `c(Π) ≥ c(1 − O(1/S))` | the explicit `S`-dependence of `ε` |

**Audit verdict.** Items (i)–(iv) of `K15-C002b` are each correct and each is needed;
`K15-C037` checked them one at a time. Two things a reader of `K15-C002b` alone does not
see, both now recorded:

1. **The counting-to-volume step is implicit** (`K15-C037` item 6, `K15-C024` item 3).
   The chain bounds `n(C*)/S³`, a *centre* density; the theorem is about *occupied
   volume*. The conversion `δ = (4π/3)c` up to an `O(1/R)` boundary term has to be
   inserted. This is the one place where a mis-statement could slip through unnoticed,
   because both sides are `O(1)` constants.
2. **Status token inconsistency (found here).** `K15-C002b`'s own status line still
   reads `PROPOSED`, while `RESULTS.md`, `ACCEPTED.md` and `C037` all treat it as
   audited. Under `D13` those cannot both stand. Corrected token, this block:
   **`AUDITED` (Main, `K15-C037`); outside check still outstanding (`G1`)**, which is
   what `ACCEPTED.md` now says. Nothing in the mathematics changes; the ledger is simply
   no longer claiming two different things.

## 6. The exact logical form of the bridge — and why `12/S` costs nothing

This is the point that has been wrong in this project's prose twice (once as `O(1/S)`
with constant 1, `K15-C083`; once as "the bridge says nothing quantitative", also
`K15-C083`). Both are repaired by writing the implication out.

**What is proved for periodic packings** (the analytic route's own content, `C002b`'s
hypotheses + the certificate machinery): for `f` with `f̂ ≥ 0`, `f ≤ 0` off `|x| ≥ 2`,
`f̂(0) > 0`, and for every **periodic** packing `Π`,

```
δ(Π)  ≤  (4π/3) f(0)/f̂(0).                                   (P)
```

**What the bridge gives.** For every packing `Λ` with `δ(Λ) > 0` and every `S ≥ 10`
there is a periodic `Π_S` with

```
δ(Π_S)  ≥  δ(Λ)·(1 − 12/S)                                    (B)
```

— a *relative* loss with constant `12`, not additive, because the kept region is a
fraction `(1 − 4/S)³ ≥ 1 − 12/S` of the maximal tile (`K15-C083`). The case `δ(Λ) = 0`
is separated: then `(G)` is trivial.

**Derivation of the general statement.**

```
δ(Λ)  ≤  δ(Π_S)/(1 − 12/S)  ≤  (4π/3)f(0)/f̂(0) · (1 + O(1/S))    for every S ≥ 10.
```

The left side does not depend on `S`. Let `S → ∞`. Hence

```
δ(Λ)  ≤  (4π/3) f(0)/f̂(0)      for EVERY packing Λ.           (G)
```

**So the `12/S` does not appear in the conclusion.** It is an intermediate quantity that
is cancelled by the limit. `K15-C083`'s second sentence ("it says nothing quantitative at
any computable scale") is true of a *different* ambition — extracting a bound with an
explicit finite-`S` error term — and false as a statement about `(G)`. The distinction
matters: a future block that reads `K15-C083` as "the bridge is only qualitative" might
try to strengthen the bridge, which would be wasted work. **The bridge is exact for its
purpose**; what is `12/S`-lossy is only the *choice of `S`*, and `(G)` never chooses one.

Two consequences worth stating once:

- **No uniformity in `Λ` is needed.** `(G)` is proved packing by packing: `S` is chosen
  after `Λ`, and `R(S)` after `S`. A bound that had to be uniform in `Λ` would need more;
  this one does not, and `C002b` is therefore correctly stated for "any 2-separated `Λ`".
- **The bridge is on the critical path for exactly one route.** Hales' Lemma 3.3 works
  with local densities and `limsup` directly (`K15-C043`), so the geometric route never
  needs `(G)`; the analytic (certificate) route needs it, because a certificate is a
  statement about periodic packings.
