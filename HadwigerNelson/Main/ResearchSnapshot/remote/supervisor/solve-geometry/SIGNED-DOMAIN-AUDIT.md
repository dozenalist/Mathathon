# Correction of AC-axis: the exact signed-direction domain, what it licenses, and the six-orbit question

Analysis only; no computation, no placement. Sources: `AngularBoundary.lean` (147, 235–300, 334–380,
423–443), `BoundaryTrace.lean` (280–290), `BinaryPalettes.lean` (9–30), `States.lean` (243). Grades
**[S]** source-read, **[P]** hand-proved here, **[C]** cited (Astra/supervisor), **[X]** open.

## 0. AC-axis is wrong — retracted, with the reason

I proposed that continua approaching along a *common line* with **mixed orientations** could still be
handled, because `binary_strip_palette_rigidity` allows independent sides. **That is a misreading.** The
lemma's two Booleans `bu, bv` choose the sides at **two angular locations** (`t` and `t + π/3`), inside two
sets `U`, `V` — they do **not** allow a per-index choice of side *within one* `W = ⋂_i Straddle(K_i)`.

The supervisor's counterexample settles it. Take `x = 0`, `v₊ = 1`, `v₋ = −1`,
`K₊ = [0, ρ]`, `K₋ = [−ρ, 0]` on the real axis, and `e = 1`:
* `Straddle(K₊)` contains the **outer** radii `(1, 1+ρ)` near `e` (from `outer_strip`, since `⟨e,v₊⟩ = 1 > 0`);
* `Straddle(K₋)` contains the **inner** radii `(1−ρ, 1)` (from `inner_strip`, since `⟨e,v₋⟩ = −1 < 0`);
* their intersection therefore contains **no one-sided radial strip** at `e`, so `W` contains none, and the
  trace production of step (b) of AC fails at that `e`.

So mixed orientations do not extend AC. **(AC-axis) is withdrawn in full.**

## 1. The exact signed-direction domain [P], using only [S] inputs

Let `v_i` (`i` in a finite set `I`) be unit approach directions, `P_i := {t : ⟨direction t, v_i⟩ > 0}` — the
**open semicircle** of directions within `90°` of `v_i` — and put

    S := ⋂_{i∈I} P_i ,          L := S ⊔ (S + π) ,          Exc := 𝕊¹ ∖ L .

Since each `P_i` is an open semicircle, `S` is an open arc (possibly empty) of length `ℓ ≤ π`; and
`P_i^c = P_i + π`, so `⋂_i P_i^c = S + π`, giving `L = S ⊔ (S+π)` and `Exc = S^c ∩ (S^c + π)`.

**Hitting on `L` [S]→[P].** If `t ∈ L`, all inner products `⟨direction t, v_i⟩` share a **common strict
sign** — positive on `S`, negative on `S+π`. By `ApproachingContinuum.outer_strip` (positive case) or
`inner_strip` (negative case) each `Straddle(K_i)` contains the same one-sided radial strip at `direction t`;
by `finite_positive_lower_bound` over the finite index set (the same step AC uses) the strip is in
`W = ⋂_i Straddle(K_i)`; and `continuum_outer_restriction` / `continuum_inner_restriction` then give

    (palette c hc x t ∩ J).Nonempty   for a.e. t ∈ L,  with J = {a,b} the two remaining labels.

**Consequence — the precise obstruction to nonalignment.** `BinaryCenter x a b` requires the hitting a.e. on
the **whole** circle, i.e. `Exc` **null**. With `Exc = S^c ∩ (S^c+π)`: if `ℓ < π` then `S^c` has length
`2π − ℓ > π`, so it contains an antipodal pair and `Exc` has **positive measure**. Hence

> **`BinaryCenter` holds iff `ℓ = π`, iff all `v_i` coincide (spread `0`).**

The two-direction computation makes the failure concrete: `v₁ = 0°`, `v₂ = 60°` gives
`S = (−30°, 90°)`, `ℓ = 120°`, `L` two arcs of `120°`, and `Exc` an arc-pair of total measure `180°` — positive.
Antiparallel directions (§0) give `S = ∅`, `L = ∅`: **no hitting anywhere**.

This is why the alignment hypothesis is not an artefact of AC's proof style: it is forced by `BinaryCenter`.

## 2. What rigidity / local constancy is actually licensed [S]

On the *smaller* set `G := L ∩ (L − τ)` (`τ = π/3`), i.e. the directions `t` with **both** `t` and `t+τ` in
`L`, `binary_strip_palette_rigidity` applies with `U = V = W` and independent sides (now legitimately, because
the two strips sit at the two *angular locations*):

> for a.e. `t ∈ G` there is `i ∈ {a,b}` and an open angular neighbourhood `A ∋ t` with `i ∈ palette x u` for
> a.e. `u ∈ A`.

So on `G` the palette is **essentially locally constant, but with the label allowed to vary with `t`**. What
is *not* licensed is the step that AC performs next: `binary_alternation` — which needs `BinaryCenter` — and
hence (i) the definition of the Boolean `s`, (ii) the identification `b ∈ P_x(t) ↔ a ∉ P_x(t)`, and (iii) the
object `angleBoundary s` itself. **Without alternation there is no boundary set to count.** At `t + τ` the same
local-constancy statement holds, with a possibly different label; nothing compares the two labels.

## 3. The six-orbit question: it cannot rescue the nonaligned case [P]

The six-orbit invariance of `angleBoundary` (`angleBoundary_shift`, `angleBoundary_six`,
`sixAngle_injective`; `D := angleBoundary s` is closed, `τ`-invariant, and nonempty) is a statement about an
object that **only exists after alternation**, i.e. after `BinaryCenter`. Since §1 shows `BinaryCenter` forces
`ℓ = π` (all `v_i` equal), the orbit refinement is available **only in AC's aligned case**, where it is not
needed (the cardinality bound `|D| ≤ 4 < 6` already closes it).

For completeness, here is the sharpened form that *would* apply if alternation were available by some other
route: `t ∈ D ⇒ t ∈ Exc or t+τ ∈ Exc`, i.e. `D ⊆ Exc ∪ (Exc − τ)`; with `D` nonempty, closed and
`τ`-invariant, `D` contains a full `60°`-orbit, so the sharp sufficient condition is the **cover condition**

    (C)   ⋃_{j=0}^{5} (G − jτ) = 𝕊¹ ,      G = L ∩ (L − τ),

strictly weaker than the cardinality bound. Worked example of how much weaker: two directions `60°` apart give
`G` a single arc of length exactly `τ`, whose six `τ`-translates tile the circle, so **(C) holds** even though
`|Exc| = π`. In the centred-arc family (`v_i` spread `w`) one has `ℓ = π − w` and `G` a pair of arcs; the
translates cover exactly when `ℓ ≥ 2π/3`, i.e. **`w ≤ 60°`**. But all of this is conditional on alternation,
and §1 forbids exactly that: for `w > 0` there is no `BinaryCenter`, so no `s`, so no `D`. **(C) is therefore a
conditional lemma with an empty hypothesis set in the nonaligned regime.**

**Weakest sufficient geometric condition for AC's route, stated exactly:** `Exc = ∅`, equivalently `ℓ = π`,
equivalently **all approach directions coincide**. Any weaker condition (e.g. `w ≤ 60°`) suffices only for the
*conditional* variant of §3 and has no consumer without alternation.

## 4. Test on `q = (0,0,1,3,3,4)` — analytic, no assertion of impossibility

Reading `q` as the label sequence on the six cycle positions, the *proper* transition pairs are the
consecutive pairs with distinct entries:

    {0,1}, {1,3}, {3,4}, {4,0}      (the pairs {0,0} and {3,3} are not transitions)

Their union is `{0,1,3,4}`, whose complement in `Fin 6` is **`{2,5}`, of size 2** — so the *cardinality*
hypothesis of AC is met with `J = {2,5}`, exactly as for `q = (0,3,3,3,0,0)`.

What that does **not** give: the four continua must have a **common approach direction** for AC to apply. So:

* **Aligned case** (all four edges' continua have the same `v`): the configuration is **excluded** by AC, with
  `J = {2,5}` and the six-orbit count `|D| ≤ 4 < 6`.
* **Any spread** (`w > 0`): `Exc` has positive measure (§1), so `BinaryCenter` fails, no `s` exists, and the
  method yields **nothing**. This is *not* a proof that the configuration is possible — it is the statement
  that AC's machinery has no purchase there, and I do not assert impossibility.

Note the same arithmetic shows why `q = (0,0,1,3,3,4)` is a *harder* test than `q = (0,3,3,3,0,0)`: both leave
the same two labels `{2,5}`, but the first has four proper transitions (four continua) spread around the cycle,
so a common approach direction for all four is geometrically more demanding than for the three consecutive
edges of `q = (0,3,3,3,0,0)`.

## 5. Summary

* **(AC-axis) withdrawn**; the supervisor's `K₊ = [0,ρ]`, `K₋ = [−ρ,0]` example is a genuine counterexample:
  at `e = 1` the two straddles contribute the outer and inner sides respectively, and `W` contains neither.
* The exact signed domain is `L = S ⊔ (S+π)` with `S = ⋂_i P_i`; hitting holds on `L`; `BinaryCenter` holds
  iff `Exc = ∅` iff **all `v_i` coincide**. Alignment is therefore *forced*, not assumed.
* Licensed on `G = L ∩ (L−τ)`: essential local constancy of *one* of `{a,b}` on a neighbourhood — no
  alternation, hence no Boolean, no `angleBoundary`, no orbit count.
* Six-orbit refinement: correct but unusable off the aligned case; the cover condition (C) and the `w ≤ 60°`
  threshold are recorded as conditional facts, not as an exclusion.
* `q = (0,0,1,3,3,4)`: cardinality hypothesis met with `J = {2,5}`; excluded in the aligned case; open for the
  method otherwise. No impossibility asserted.
