# Theorem AC audited against the actual sources; and five retractions

Source-only. **No computation, no Lean.** Read-only: `BinaryPalettes.lean`, `BoundaryTrace.lean`,
`AngularBoundary.lean`, `Sectors.lean`, `Exclusion.lean`, `Interfaces.lean`, `States.lean`. Grades:
**[source]** = declaration read verbatim with its line; **[proof]** = mine; **[candidate]** = paper-level,
unverified.

## 0. Five retractions, with the reason each was wrong

* **R1. `BinaryCenter` means the palette HITS the pair, not that it is contained in it.**
  `BinaryPalettes.lean:9`: `BinaryCenter c hc x i j := ∀ᵐ t ∂angularMeasure, t ∈ paletteSet c hc x i ∨
  t ∈ paletteSet c hc x j` — i.e. *at a.e. direction the palette contains `i` or contains `j`*. My "palette
  a.e. contained in the fixed pair `{i,j}`" was the wrong reading and is withdrawn.
* **R2. The four-state field DOES hit `{0,5}` a.e., so my inapplicability claim was false.**
  Its palettes are `{0,2}, {0,3}, {3,5}, {2,5}`; the first two contain `0`, the last two contain `5`. Hence
  `BinaryCenter c hc x 0 5` **holds** for the field, and `binary_centers_separated` is *not* inapplicable
  for the reason I gave. Withdrawn.
* **R3. `B2` means each palette has cardinality ≤ 2; it does not mean all palettes lie in one 2-set.** The
  field satisfies `B2` at every direction. My conflation is withdrawn, and with it the "no 2-set contains
  all four palettes" test, which tested the wrong thing.
* **R4. Bool coarsenings of four states are not only constant or parity.** There are `2^4 = 16` maps
  `Fin 4 → Bool`; singletons like `[f = 0]` are also coarsenings. My §2 proposition in
  `FOUR-PALETTE-MODEL.md` — "no `Bool` coarsening satisfies both `RealState` premises" — is **false** and
  is withdrawn. The corrected statement: take `s := [f ∈ {0,1}]`. Then `A = {f ∈ {0,1}}` has
  `paletteSet`-intersection `{0}` (palettes `{0,2}` and `{0,3}`) so `RealState c hc x A {0}` holds, and
  `B = {f ∈ {2,3}}` has intersection `{5}` so `RealState c hc x B {5}` holds; and `s` **does** flip at 60°
  since `f ↦ f+2` maps `{0,1} ↔ {2,3}`. So `hJ`, `hK` and `hflip` all hold. What fails is **`hcard`**:
  `univ \ ({0} ∪ {5}) = {1,2,3,4}` has **cardinality 4 > 2**. In general any `RealState` level set of this
  field admits at most **one** label (distinct palettes here share at most one label), so `|J ∪ K| ≤ 2` and
  `hcard` fails for every coarsening. **The binding premise of `two_state_impossible` for this field is
  `hcard`, not `RealState`.**
* **R5. A model that omits a hypothesis does not refute the theorem that assumes it.** My sentence "the
  candidate (MS) is REFUTED by Astra's field" is withdrawn: the field fails the state-determination
  hypothesis, so it is *not* a counterexample to `(MS)`. Likewise I freeze the broad no-go sentences of the
  previous block — "no purely state-theoretic generalisation of `two_state_impossible` can close the gap",
  "every licensed relation is inapplicable or slack". Neither is established, and both are withdrawn as
  statements; the individual premise-level observations above survive.

## 1. Theorem AC, stated exactly

**THEOREM AC (paper-level source corollary; candidate, not Lean-checked).** Let `k : ℕ`,
`c : ℂ → Fin k`, `hc : Measurable c`, `hw : WeakColoring k c`. Let `x : ℂ`, `v : ℂ` with `‖v‖ = 1`.
Let `ι` be a finite type (`[Fintype ι]`), `K : ι → Set ℂ`, `H : ι → Finset (Fin k)`, and suppose

    (H1)  ∀ i, ApproachingContinuum x (K i) v                      -- the SAME v for every i
    (H2)  ∀ i, ∀ j ∈ H i, Disjoint (spatialSupport c j) (Straddle (K i))
    (H3)  (univ \ ⋃ i, H i).card ≤ 2

Then `False`.

## 2. Source hypothesis table — every ingredient located

| AC ingredient | exact declaration | what it actually requires |
|---|---|---|
| `ApproachingContinuum x K v` | `structure ApproachingContinuum` **AngularBoundary.lean:235** | fields `center_mem : x ∈ K`, `r : ℕ → ℝ` with `r n > 0` and `r → 0`, `w : ℕ → ℂ` with `‖w n‖ = 1` and `w → v`, `point_mem : ∀ n, x + r n * w n ∈ K`. **The directions converge to the single `v`** — so (H1) with a common `v` is exactly the structure, and AC's "not approximately aligned" is right. |
| `Straddle K` | `def Straddle` **:147** | `{z | ∃ p ∈ K, ∃ q ∈ K, dist z p < 1 ∧ 1 < dist z q}` — the set straddling the unit circle about `K`. |
| exclusion hypothesis | `def spatialSupport i` **:308** = `(volume.restrict {z | c z = i}).support` | (H2) is a statement about the **essential** support, so it is an a.e. statement — this is what lets AC use `∀ᵐ` throughout. |
| one-sided radial strip | `ApproachingContinuum.outer_strip` **:244** (needs `0 < ⟪e,v⟫`), `.inner_strip` **:252** (needs `⟪e,v⟫ < 0`) | a `δ > 0` giving a **direction-neighbourhood** `dist e' e < δ` *and* a **radial window** (`1 < r < 1+δ` resp. `1-δ < r < 1`) on which `x + r e' ∈ Straddle K`. |
| finite intersection open | `isOpen_iInter_of_finite`, `straddle_isOpen` | finiteness of `ι` — this is exactly why AC needs `[Fintype ι]`. |
| palette hits `J` on a direction set | `continuum_outer_restriction` **:259**, `continuum_inner_restriction` **:279** | hypothesis `hJ : ∀ᵐ z, (∀ i ∈ E, z ∈ Straddle (K i)) → c z ∈ J`; conclusion `∀ᵐ t, (∀ i ∈ E, 0 < ⟪direction t, v i⟫) → (palette c hc x t ∩ J).Nonempty`. **Note the conclusion is a HIT, not a containment** — matching `BinaryCenter`'s semantics (R1). The `v i` appears per index, but under (H1) all `v i` equal `v`, so the side condition is the single `0 < ⟪direction t, v⟫`. |
| the two sides together | `Exclusion.lean:128-129` and `Interfaces.lean:75-76` | the existing code calls exactly these two lemmas with `E s true` / `E s false` for a side function `s` — i.e. the outer/inner split is already the implemented pattern. |
| locally-a.e. gluing | `ae_of_locally_ae angularMeasure` (used inside `continuum_outer_restriction`) | converts the local statement at each `t` into an a.e. statement over the circle. |
| 60° alternation | `binary_alternation` **BinaryPalettes.lean:11** | `BinaryCenter c hc x i j` ⟹ a.e. `(t+sixty ∈ paletteSet i ↔ t ∉ paletteSet i)` and `(t ∈ paletteSet j ↔ t ∉ paletteSet i)`. |
| `a = b` impossible | `binary_pair_distinct` **:28** | `BinaryCenter … i j → i ≠ j`. |
| two-sided rigidity at `t` | `binary_strip_palette_rigidity` **BoundaryTrace.lean:280** | two open `U, V`, each `{a,b}`-coloured a.e.; **two independent side Bools `bu`, `bv`**; strips at `direction t` and at `direction t * exp(iπ/3)`; conclusion: `∃ i, (i = a ∨ i = b) ∧ ∃ A` open **with `t ∈ A`** and `∀ᵐ u ∈ A, i ∈ palette c hc x u`. The independence of `bu` and `bv` is a real feature of the statement — AC's step (c) is licensed. |
| one-sided trace production | `outer_strip_trace` **:182**, `inner_strip_trace` **:210** | `δ > 0`, open `W`, colouring constant (in `{i}`) a.e. on `W` ⟹ `i` enters the palette on a direction neighbourhood. |
| `angleBoundary` | `def angleEssential` **:334**, `def angleBoundary` **:349** = `(⋃ b, angleEssential s b)ᶜ` | the set of angles where **neither** `Bool` value is essentially constant on a neighbourhood. |
| boundary nonempty | `angleBoundary_nonempty` **:381** | `hflip : ∀ᵐ t, s (t+sixty) = !(s t)` ⟹ `Nonempty`. Its proof uses `isPreconnected_univ.subset_left_of_subset_union` — a **genuinely global** argument on the connected circle, not a partial-set one. |
| six-orbit closure | `angleBoundary_six` **:435** | `hflip`, `t ∈ angleBoundary s` ⟹ `t + sixAngle j ∈ angleBoundary s` for every `j : Fin 6`. |
| six points distinct | `sixAngle_injective` **:423** | the six orbit points are pairwise distinct. |

All eight citations AC makes resolve to real declarations; the line numbers are accurate to within a few
lines (`sixAngle_injective` is at `:423`, `angleBoundary_six` at `:435`).

## 3. Audit of AC's four steps

* **(a)** Uses `.outer_strip` / `.inner_strip` per index `i` and takes the finite minimum of the `δ i` —
  legitimate because `ι` is finite (`finite_positive_lower_bound` is exactly the device used in
  `continuum_outer_restriction`). The exceptional set is `⟨e,v⟩ = 0`, i.e. the two perpendiculars — a
  two-point set, as AC says. **Supported.**
* **(b)** `continuum_outer_restriction` (for `⟨direction t, v⟩ > 0`) and `continuum_inner_restriction` (for
  `< 0`) give `(palette ∩ J).Nonempty` on the corresponding direction set; `ae_of_locally_ae` glues them
  into `BinaryCenter c hc x a b` off the two perpendiculars; `binary_alternation` then gives the flip.
  **Supported**, with the caveat that the two perpendiculars must be removed *before* the two lemmas are
  applied, which AC does.
* **(c)** `binary_strip_palette_rigidity` gives a single `i ∈ {a,b}` present on an **open angular
  neighbourhood** of `t`, with `bu`, `bv` chosen independently — exactly AC's "the radial sides may be
  chosen independently". `binary_alternation` then makes `s` constant on that neighbourhood.
  **Supported**, and this is the step that a recurrence/orbitwise argument cannot reproduce: it uses two
  strips at 60° apart simultaneously.
* **(d)** `D = angleBoundary s`; if step (c) holds off `B ∪ (B − τ)` then `D ⊆ B ∪ (B−τ)`, at most four
  points; `angleBoundary_nonempty` gives `D ≠ ∅`; `angleBoundary_six` gives a full six-orbit inside `D`;
  `sixAngle_injective` makes those six points distinct — contradiction with `|D| ≤ 4`. **Supported.**

**Residual weakness, stated plainly.** AC's step (a) asserts strips for *every* unit `e` with `⟨e,v⟩ ≠ 0`;
that is what `.outer_strip`/`.inner_strip` give, but the resulting `δ` depends on `e` and the argument needs
a lower bound on `e` ranging over an angular neighbourhood — which is exactly the statement of those two
lemmas (`∀ e' with dist e' e < δ`), so the step is fine. What I did **not** verify is whether
`continuum_*_restriction`'s hypothesis `hJ` can be discharged from (H2) alone in the multi-`i` case: the
lemma is stated for a *single* label set `J` and a finite index family `E`, and (H2) gives a *different*
`H i` per index. Forming `J := ⋂_{i ∈ E} (univ \ H i)` requires the surviving label set to be constant
across the family, which under (H3) is `{a,b}` — so `J = {a,b}` and the hypothesis becomes
`∀ᵐ z, (∀ i, z ∈ Straddle (K i)) → c z ∈ {a,b}`. That is exactly "finite support exclusion on the
intersection", so it discharges. **I believe it closes, but I flag it as the one place a Lean
implementation would need care**, since it is where `H i`-dependence must be collapsed to a single `J`.

## 4. What additional strip data the four-state field lacks

The field is a function `P : Angles → Finset (Fin 6)` and nothing else. To state AC's hypotheses one needs
**all four** of the following, and the field supplies **none**:

1. an actual colouring `c : ℂ → Fin k` with `WeakColoring` — the field has no plane-level object at all;
2. for each `i`, a **set** `K i ⊆ ℂ` together with a full `ApproachingContinuum` witness (`center_mem`,
   `r → 0+`, `w → v`, `point_mem`), not merely a direction `v i`;
3. the exclusions `Disjoint (spatialSupport c j) (Straddle (K i))` for `j ∈ H i` — a.e. statements about
   where label `j` lives in the plane;
4. a finite index family, so that the minimum of the widths exists.

**And the symptom of that gap is visible exactly where AC bites.** AC's step (c) forces, at each angle off
the two perpendiculars, **one fixed label of `{a,b}` present on an open neighbourhood**. The field violates
this at `t = 0`: as `f` runs `3 → 0` (i.e. crossing 0) the label of `{0,5}` that is present jumps from `5`
(Palate `{2,5}`) to `0` (palette `{0,2}`). So the field is *not* a source-level trace field, and the failure
is precisely the one `binary_strip_palette_rigidity` forbids. That is a sharper statement than my previous
block's, and it is the correct reason the field cannot be a counterexample to AC.

## 5. The six-colour consumer, checked

Astra's q-vector `q = (0,3,3,3,0,0)` gives `v_i = e^{q_i π/3}`, so `v_1 = v_2 = v_3 = e^{iπ} = -1`: the three
edges `E_1 = {1,2}`, `E_2 = {2,3}`, `E_3 = {3,4}` approach in the **same** direction `-1`, which is exactly
what (H1) requires (common `v`). Their endpoint sets union to `{1,2,3,4}`, so
`univ \ ({1,2,3,4}) = {0,5}`, cardinality **2 = the `hcard` bound**. So AC applies with `a = 0`, `b = 5`,
and rules that configuration out **for actual common interfaces**. Note this is a strictly stronger
hypothesis set than the combinatorial premises alone: the finite orbit model passes the combinatorial
premises but cannot supply (1)–(4), so there is no conflict, and the field remains a valid counterexample
only to the weaker orbitwise/recurrence reduction — not to AC.

## 6. Scope

* **[source]** §2: every declaration, with its line, read this block. `ApproachingContinuum` requires a
  *common* `v`; `continuum_*_restriction` conclude a **hit**; `binary_strip_palette_rigidity` allows
  **independent** sides and concludes essential local constancy.
* **[proof]** §3 (a)–(d): AC's steps are supported by those declarations, with the one flagged
  `H i`-to-`J` collapse in step (a).
* **[candidate]** AC itself: paper-level, **not Lean-checked**, pending independent review. Its novelty
  relative to unpublished worker work or the literature has not been investigated, as Astra states.
* **Not claimed:** AC is not F6 — general direction configurations, including non-aligned vectors, remain.
  No numerical bound; no statement about `L6`; no global conclusion from the angular model; no claim that
  the four-state field is refuted.
