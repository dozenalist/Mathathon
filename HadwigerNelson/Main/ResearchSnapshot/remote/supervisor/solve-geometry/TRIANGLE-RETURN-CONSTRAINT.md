# The unit-triangle return constraint: exact pigeonhole, its multi-type generalisation, and the four-state field

Analysis only; no computation. Sources read: `States.lean` (92–96, 243–300, 370–381), `BinaryPalettes.lean`,
`PaletteTransport.lean`. Grades **[S]** source-read with lines, **[P]** hand-proved here, **[C]** cited
(Astra/referee), **[X]** not established.

## 0. Retraction first: my (†) is not proved

`GLOBAL-COUPLING.md` §4 asserted **(†)** — that the dual endpoint constraint forces the patch labels into the
ring-centre palettes. **Retracted as unproved**: I gave no exact centre, no statement of which measure the
a.e. quantifier runs over, and no pullback through the quasi-measure-preserving maps. What a proof would need:
a named centre `x` with `|x| = 1` type data, the a.e. statement on `Angles` at that centre (from
`Trace`/`palette`), a pullback along `angleMk` and translations (`quasiMeasurePreserving.ae`), and the
endpoint-trace step (`trace_positive_le_palette`, `exact_sample_palette_fixed`). Until then (†) is **[X]** and
nothing may rest on it.

## 1. The pigeonhole, extracted from the proof of `States.two_state_impossible` [S]

The lemma (States.lean:243–248) is reduced, at the end of its proof (lines 293–300), to
`two_label_triangle_impossible hc hw (sourceTriangle x t) (Finset.univ ∖ (J ∪ K)) hcard …`, with the per-vertex
obligation

    ∀ j : Fin 3, DensityOne {q | c q ∉ J ∪ K} (sourceTriangle x t j).

So the combinatorial core is exactly:

> **Pigeonhole (PT).** Three points of the plane that are pairwise at unit distance cannot all avoid a set of
> at most two labels: three colours chosen from a two-element set repeat, and a repeated colour at distance
> exactly `1` violates properness.

The hypotheses that *produce* the per-vertex exclusion are two, and both are source facts:

* **`RealState`** (States.lean:92): `MeasurableSet A ∧ ∀ i ∈ J, A ≤ᵐ[volume] liftPalette c hc x i` — on the
  direction set `A`, the palette at `x` is contained in `J`.
* **`state_densityZero`** (States.lean:94–98): if `A` is a `RealState` set for `J`, `t` is a line-density-zero
  point of `Aᶜ` (i.e. a density-one point of `A`), `sin(u − t) ≠ 0`, and `i ∈ J`, then
  `DensityZero {z | c z = i} (angularSum x 1 (angleChart (t,u)))`. **In words: a direction where the palette is
  confined to `J` and which is a density point of that confinement forces the corresponding circle point to
  carry a colour outside `J`.** This is the only "density licence" used, and it is a source theorem.
* **The Boolean flip** `s(t + π/3) = ¬s(t)` a.e. (hypothesis `hflip`), which gives
  `f(t + 2jπ/3) = f(t)` for `j : Fin 3` (`bool_flip_even`) and `f(t + π) = ¬f(t)` (`bool_flip_three`).
* **The γ-return** `∃ᶠ t ∂(ae volume), f t = f (t + triangleAngle)` with `triangleAngle = arccos(5/6)`,
  obtained from `equal_triangleAngle_positive hs hflip` — a *positive-measure* statement about the alternating
  Boolean `s`.

## 2. The multi-type generalisation, and where it breaks [P]

Let the direction circle be partitioned into finitely many **types** `r`, each carrying its own pair of label
sets `(J_r, K_r)` and its own Boolean `s_r`, and let `ω : Angles → types` be measurable. The proof above uses
exactly three things at each triangle vertex `j`:

1. a **type assignment** at the three vertex directions (which label set applies there);
2. the **same residual label set** `univ ∖ (J_{r} ∪ K_{r})` at all three, of cardinality `≤ 2`;
3. a **shared** density point where all three exclusions hold simultaneously.

Generalising, let `L_j` be the label set that applies at vertex `j`. `state_densityZero` gives
`colour(vertex j) ∉ L_j`. Then:

> **(PT-multi)** A contradiction follows iff the three sets `univ ∖ L_j` (`j : Fin 3`) admit **no injective
> choice** — e.g. all three equal a 2-set, or their union has at most 2 elements. Three *different* 2-sets
> `{a,b}, {a,c}, {b,c}` admit the injective choice `a, c, b`, so **the pigeonhole fails whenever the types
> differ at the three vertices.**

So the generalised statement is *conditional on the type being constant along the triangle* (equivalently: on
the three residual sets coinciding). There is no way to "mix" types and still get three forced exclusions: the
mixed case is exactly the one where `(PT-multi)` is silent.

## 3. The four-state field, tested against this [C]+[P]

The field: `h = π/6`, `f(t) = ⌊t/h⌋ mod 4`, `P(t) = ({0,2},{0,3},{3,5},{2,5})[f(t)]`, and
`A₀ = {f even}`, `A₁ = {f odd}`, each of measure `π`, each **60°-invariant** (since `+60°` moves `f` by `2`).

* **`RealState` holds at the palette level, with the same set on both sides:** on `A₀` the palettes are
  `{0,2}` and `{3,5}`; on `A₁` they are `{0,3}` and `{2,5}`; all four are contained in `J = {0,2,3,5}`. So
  `RealState x A₀ J` and `RealState x A₁ J` both hold with **`J = K = {0,2,3,5}`**, and
  `|univ ∖ (J ∪ K)| = |{1,4}| = 2 ≤ 2`. Cardinality hypothesis: **satisfied.**
* **The flip fails.** With `s := 1_{A₀}`, `s(t + π/3) = s(t)` (the parity of `f` is invariant under `+2`), so
  `hflip` is **false**. Hence `two_state_impossible` does not apply — not because of the label sets, but
  because the type does not alternate along the 60° orbit.
* **The γ-return fails too, at the palette level.** Astra's localisation gives no same-phase `γ`-return on the
  class `A` it works with; and both same-phase `γ`-return sets are **null** in this field
  (`f(t+γ) − f(t) ∈ {1,2} (mod 4)` with `γ/h` irrational, so exact returns are a null set). The step
  `equal_triangleAngle_positive` that supplies the return is a theorem about an **alternating** measurable
  Boolean; with `s` invariant it does not apply, and with `A` partial the ergodic global step is unavailable.

**Verdict on the question asked.** The generalised return constraint does **not** exclude the four-state field.
It forces the field's eventual exclusion onto one of two *strengthened, unproved* premises:

> **(S1)** the type function `ω` alternates along the 60° orbit at a positive-measure set of centres
> (field: `ω` is invariant — false), **or**
> **(S2)** a positive-measure same-phase `γ`-return exists inside one type class (field: null — false, and for
> a partial class `A` the ergodic step that would produce it is exactly what Astra reports as failing).

Neither premise follows from `WeakColoring`, and both are *false* for the field's own palette data. So the field
is a genuine **palette-level** object that satisfies the `RealState` side of the machinery while evading the
return machinery — it refutes the *orbitwise-two-states ⇒ one-global-pair* inference, and it does **not**
refute, and is not refuted by, `WeakColoring 6`.

## 4. The exact conditional theorem that *is* available [P]

> **Theorem (conditional return exclusion).** Let `c` be measurable with `WeakColoring k c`, `x : ℂ`, and let
> `s : Angles → Bool` be measurable with `s(t + π/3) = ¬s(t)` a.e. Suppose `J, K` satisfy the two `RealState`
> hypotheses and `|univ ∖ (J ∪ K)| ≤ 2`. Then `False` (States.two_state_impossible).
>
> **Corollary (multi-type form).** If in addition the type function `ω` is constant on the 60°-orbit of `x`'s
> triangle directions, the same conclusion holds with `L_j` replacing `J ∪ K`, provided the three residual sets
> coincide. If `ω` is *not* constant, no conclusion follows from these hypotheses (by the injective-choice
> remark of §2).

What is **not** available: a version whose hypothesis is satisfied by an *invariant* type function. That would
need a genuine global coupling between the invariant classes — precisely the gap the four-state field exposes,
and the same gap the referee's contact-ban theorem does **not** close (it is a local/contact statement, accepted
at paper level, and it is the basis of the validated local bank with source SHA `9a904d4d…82ba1`).

## 5. Status and blockers

* Retracted: (†) of `GLOBAL-COUPLING.md` (unproved; needs exact centres and AE pullbacks).
* Extracted: the exact pigeonhole (`PT`), its single licensed density licence (`state_densityZero`), and the
  four hypotheses that make `two_state_impossible` fire.
* Proved: the multi-type form is silent unless the type is constant on the triangle (§2, injective-choice
  argument), and the four-state field fails `hflip` and the γ-return, so it is **not** excluded (§3).
* Precise gap: premises **(S1)** or **(S2)**. Both are stronger than `WeakColoring`, both hold nowhere in the
  field, and neither is in the validated local bank.
* No claim about a global 6-colouring, `(W)`, or `χ(ℝ²)`; no new placement, no computation.
