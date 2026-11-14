# Independent audit of Theorem AC (aligned exclusion continua), with the source lemmas it consumes

Analysis only; no computation. Sources read in `lean/OAI/Geometry/PlaneColoring/`:
`AngularBoundary.lean` (103–110, 147, 235–300, 334–380, 423–443), `BoundaryTrace.lean` (280–295),
`States.lean` (243–300), `BinaryPalettes.lean` (9–30). Grades **[S]** source-read with lines,
**[P]** hand-proved here, **[C]** cited (Astra/referee), **[X]** open.

## 0. Restricting two of my previous claims (they were stated too globally)

In the last two blocks I wrote "no type-mixing version exists" and "neither premise follows from
`WeakColoring`". Both were **global impossibility assertions without proof**. They are hereby restricted to
two *named finite countermodels*, which is all I actually exhibited:

* **(M1) the four-state angular field**: a palette-level object (four palettes `{0,2},{0,3},{3,5},{2,5}`)
  that satisfies the `RealState`-confinement side with `J = K = {0,2,3,5}` and evades the flip because its
  parity class is 60°-invariant. It shows that *that* argument does not exclude *that* field. It shows
  nothing about other arguments or other fields.
* **(M2) the injective-choice countermodel**: three *distinct* 2-element label sets admit an injective choice,
  so the unstrengthened multi-type pigeonhole is silent on that configuration. Nothing global follows.

No claim of the form "no version can exist" is made anywhere below.

## 1. Source inventory (the lemmas AC invokes, at their actual hypotheses) [S]

| object | statement | line |
|---|---|---|
| `Straddle K` | `{z | ∃ p ∈ K, ∃ q ∈ K, dist z p < 1 ∧ 1 < dist z q}` — **open** in `z`; `straddle_isOpen` | 147 |
| `ApproachingContinuum x K v` | a structure: `x ∈ K`, a sequence `r n > 0` with `r n → 0`, unit `w n → v`, and `x + r n · w n ∈ K`. **No reach hypothesis and no connectedness** — only the centre and one approaching ray | 235–242 |
| `ApproachingContinuum.outer_strip` | if `‖e‖ = 1` and `0 < ⟪e,v⟫`: `∃ δ > 0`, the **outer** radial strip `x + r e'` (`1 < r < 1+δ`, `dist e' e < δ`) lies in `Straddle K` | 244–250 |
| `ApproachingContinuum.inner_strip` | if `⟪e,v⟫ < 0`: same with the **inner** strip `1−δ < r < 1` | 251–258 |
| `continuum_outer_restriction` | **family** `K : ι → Set ℂ`, `v : ι → ℂ`, `[Fintype ι]`, `E : Finset ι`, and confinement `c ∈ J` a.e. on `⋂_{i∈E} Straddle(K i)`; conclusion: for a.e. `t`, if **`∀ i ∈ E, 0 < ⟪direction t, v i⟫`** then `(palette x t ∩ J).Nonempty` | 259–278 |
| `continuum_inner_restriction` | same with `⟪direction t, v i⟫ < 0` | 279–300 |
| `binary_strip_palette_rigidity` | **two** open sets `U, V` with a.e. `a ∨ b`-confinement in each, `x`, `t`, `δ > 0`, **two independent Booleans `bu`, `bv`** choosing the strips' sides, strips at directions `t` and `t * exp(iπ/3)`; conclusion: `∃ i ∈ {a,b}` and an **open angular neighbourhood** `A ∋ t` with `i ∈ palette x u` for a.e. `u ∈ A` | 280–290 |
| `angleEssential s b` | `{t | ∃ open U ∋ t, s = b a.e. on U}`; open | 334–339 |
| `angleBoundary s` | `(⋃_b angleEssential s b)ᶜ` | 349 |
| `angleBoundary_shift` | under the alternation `s(t+π/3) = ¬s(t)`: `t + π/3 ∈ angleBoundary s ↔ t ∈ angleBoundary s` (**τ-invariance**) | 370–380 |
| `angleBoundary_nonempty` | under alternation: `angleBoundary s` is nonempty | 381 |
| `angleBoundary_six` | `t ∈ angleBoundary s → t + sixAngle j ∈ angleBoundary s` for `j : Fin 6`, and `sixAngle_injective` makes the six points distinct | 423–443 |

## 2. Audit of AC's four steps

**(a) Openness, confinement, strips, widths.** `W = ⋂_i Straddle(K_i)` is open by `isOpen_iInter_of_finite`
[S] ✓. On `W`, each `j ∈ H_i` has `support j ∩ Straddle(K_i) = ∅ ⊇ W`, so a.e. `z ∈ W` is not a density point
of `A_j`; over the finite union `⋃H_i`, a.e. `z ∈ W` has `c z ∈ {a,b}` ✓ **[P]**. The strips: **the source
already has them, for a family with individual directions `v i`** (`continuum_outer/inner_restriction`), and
the *widths* are handled by `finite_positive_lower_bound` applied to the finite index set `E` — so AC's
"finiteness lets us take the minimum of the positive widths" is exactly the source's own step, and
`[Fintype ι]` is genuinely needed ✓. Side selection: `outer_strip` when `⟪e,v⟫ > 0`, `inner_strip` when `< 0`
✓ matches AC.

**(b) Hitting and `BinaryCenter`.** The restriction lemmas conclude `(palette x t ∩ J).Nonempty`, i.e. a
**hitting** statement, and `BinaryCenter x a b` is exactly `∀ᵐ t, t ∈ paletteSet x a ∪ paletteSet x b`
(BinaryPalettes.lean:9) with `J = {a,b}` ✓ — so "hitting" is the right reading and the source produces
precisely it, a.e. in `t`, via `ae_of_locally_ae` (the "locally-a.e. gluing lemma") ✓. `a = b` is excluded by
`binary_pair_distinct` ✓; else `s(t) := (a ∈ P_x(t))` and `binary_alternation` gives
`s(t + τ) = ¬s(t)` a.e. plus `b ∈ P_x(t) ↔ a ∉ P_x(t)` ✓.

**(c) Two strips on independently chosen sides.** `binary_strip_palette_rigidity` takes **`bu`, `bv : Bool`
independently** ✓ [S], and takes **only two open sets** `U, V` — setting `U = V = W` is permitted, since the
hypotheses are merely `IsOpen` plus the a.e. `a∨b`-confinement, with no distinctness or disjointness
requirement ✓ [S]. **This is the check the task asked for, and it passes.** The conclusion is
`i ∈ palette x u` for a.e. `u` in an open `A ∋ t`, i.e. `t ∈ angleEssential s (i=a)` or `(i=b)` ✓.

**(d) Boundary count.** If `t ∉ B ∪ (B − τ)` (with `B` the exceptional directions), both strips exist and
step (c) gives `t ∉ angleBoundary s`. So `D := angleBoundary s ⊆ B ∪ (B − τ)`. With a **common** `v`, `B` is the
two perpendicular directions, `|B| = 2`, hence `|B ∪ (B − τ)| ≤ 4`, so `|D| ≤ 4`. But `D` is nonempty
(`angleBoundary_nonempty`) and τ-invariant (`angleBoundary_shift`), hence contains the full six-point orbit
(`angleBoundary_six`, `sixAngle_injective`) ⇒ `|D| ≥ 6`. Contradiction ✓ **[P]**. Note the count only needs
`|D| ≥ 6`, so any bound `|D| ≤ 5` would do; `≤ 4` is what this route gives.

**Where AC overstates.** AC says *"The `K_i` need not coincide. Their approach DIRECTIONS must coincide."*
The source's restriction lemmas take **individual** directions `v i` and need only a **common sign of the
inner products with `direction t`**. So the coincidence of directions is *not* what the source requires; what
forces coincidence here is the **boundary count** (see §4).

## 3. The theorem, restated with exact hypotheses [P]

> **Theorem AC (restated).** Let `c : ℂ → Fin k` be measurable with `WeakColoring k c`, `x : ℂ`,
> `v : ℂ` with `‖v‖ = 1`, `ι` a **finite** index type, `K : ι → Set ℂ` with `ApproachingContinuum x (K i) v`
> for all `i`, and `H : ι → Finset (Fin k)` with `Disjoint (spatialSupport c j) (Straddle (K i))` for every
> `i` and `j ∈ H i`. If `⋃_i H i` has complement of cardinality `≤ 2` in `Fin k`, then `False`.

Proof: §2 (a)–(d), each step a named source lemma: `isOpen_iInter_of_finite`, `finite_positive_lower_bound`,
`continuum_outer/inner_restriction`, `ae_of_locally_ae`, `binary_pair_distinct`, `binary_alternation`,
`binary_strip_palette_rigidity` with `U = V = W` and independent `bu, bv`, `angleBoundary_shift`,
`angleBoundary_nonempty`, `angleBoundary_six`, `sixAngle_injective`. Fulcrum: `|D| ≤ 4 < 6 ≤ |D|`. ∎

No palette-size bound, no triple exclusion, no local finiteness of the cyclic core, and no global two-state
classification is used — the audit confirms this, since the only `k`-dependence is
`|(⋃H_i)ᶜ| ≤ 2`. **The `k = 6` consumer checks out arithmetically:** for `q = (0,3,3,3,0,0)` the three edge
label sets `E1 = {1,2}`, `E2 = {2,3}`, `E3 = {3,4}` have union `{1,2,3,4}`, whose complement is `{0,5}`, of
size 2 ✓.

## 4. The strongest nonaligned extension with an actual consumer [P]

Not by angle continuity — by the **size of the exceptional set**. Replace "common `v`" by
`ApproachingContinuum x (K i) (v i)` with distinct `v i`. Then step (a)–(c) still run (the source states them
for individual `v i`), but the exceptional set becomes

    B = {t : ∃ i, ⟪direction t, v i⟫ = 0},        |B| ≤ 2·#{distinct axes},

and the count needs `|B ∪ (B − τ)| ≤ 5` to contradict `|D| ≥ 6`, i.e. **`|B| ≤ 2`**. Hence:

> **(AC-axis)** The argument survives iff all `v i` lie on one common **line**, `v i ∈ {v, −v}`.
> For mixed orientations one further source input is needed: a **mixed-sign family restriction** (outer for
> some `i`, inner for others). The source has the independent-side flexibility only for the *two-strip*
> lemma (`bu`, `bv`), not for a family, so **(AC-axis) is a precise gap, not a guess**: the missing lemma is
> `continuum_mixed_restriction` with a per-index sign choice.
>
> For **non-parallel** `v i` the route provably stops: `|B| ≥ 4` gives `|B ∪ (B−τ)| ≤ 8`, and `|D| ≥ 6` no
> longer contradicts anything. That is a quantitative limit of this method, not a claim that the
> configuration is possible.

**Consumer.** The six-colour common-interface stage, exactly as AC states: three consecutive edges with
label sets whose union leaves `{0,5}`. With **(AC-axis)** the consumer covers also the case where the three
continua approach along the same *line* with possibly opposite orientations — a strictly larger configuration
class than AC, with the same downstream consumer and no continuity assumption. Anything beyond that (a
genuinely non-parallel triple) is outside this method by the count above.

## 5. Verdict

* AC's four steps, its use of `U = V = W`, the independent sides `bu, bv`, the hitting form of
  `BinaryCenter`, the finite-intersection widths, and the boundary count: **all check against the source**,
  and the one arithmetic consumer `q = (0,3,3,3,0,0)` is correct. AC is **accepted as a paper-level source
  corollary**, pending independent/Lean verification as the supervisor states.
* One overstatement corrected: the alignment requirement is not "directions must coincide" but "the
  exceptional set must have at most two points", which the source delivers only for a common line.
* My own previous global claims are restricted to (M1) and (M2) per §0.
* Not claimed: any `k = 6` global conclusion, any statement about non-aligned triples, `(W)`, or `χ(ℝ²)`.
