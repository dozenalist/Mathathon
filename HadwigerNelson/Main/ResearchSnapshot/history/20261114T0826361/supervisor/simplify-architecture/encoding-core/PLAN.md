# Common encoding core: `finite_uniform_precision_contradiction` = `ambient_uniform_precision_contradiction`

Block 6. Source-level, **uncompiled**. The CENSUS twin pair is the target; the retired claim that
certain "dead instances" could simply be deleted is **refuted by the compiler** and is not used
(see §7). Nothing here is claimed verified.

## 1. What was checked, and how

Both proofs were read in full and **diffed**: `ConditionalSpectrum.lean:324–476` against
`ConditionalLimits.lean:399–551` (153 lines each). The diff is 6 lines:

```
finite                                                    ambient
let P : X → W := q ∘ p                                    let P : X → W := q
have hP : Measurable P := hq.comp hp                      have hP : Measurable P := hq
let : IsProbabilityMeasure (μ.map P) :=                   let : IsProbabilityMeasure (μ.map P) :=
  (Measure.isProbabilityMeasure_map_iff hP.aemeasurable)    inferInstance
    .mpr inferInstance
… coeff (u j) (P x) i • H i (p x)                          … coeff (u j) (P x) i • H i x     (×2: Ap, Am)
hbins … (fun k => H k (p x)) (hH (p x))                    hbins … (fun k => H k x) (hH x)
change … H k (p x) … (×4 in two `change` lines)            change … H k x …
```

Everything else — `ν := differenceLaw (μ.map P) (condDistrib b P μ)`, the `hn` nonnegativity from
`predecessor_moment_sq`, `τ`, `γ`, `hτδ`, the `FiniteBins.bounded_coefficient_bins` step,
`M := 20*(L+1)*m²`, `MomentTest M N`, `ε := min 1 (c²/(4*(card T+1)))`, `harc`, the final
contradiction — is **identical, line for line**.

Conclusion: the two theorems are one theorem with `H` read through a map and `P` abstracted. The
merge is mechanical, not a new mathematical claim.

## 2. Module placement (measured)

Transitive import closure of `lean/OAI` (one BFS over `^import` lines; the block's single
computation, ~0.1 s):

* `ConditionalSpectrum ∈ closure(ConditionalLimits)` = **True**
* `ConditionalLimits ∈ closure(ConditionalSpectrum)` = **False**

So `ConditionalLimits` already imports `ConditionalSpectrum`. The general definition and the common
theorem therefore go into **`Analysis/PlaneSpectrum/ConditionalSpectrum.lean`** (namespace
`PlaneFiveColor.Spectral`), and `ConditionalLimits.lean` gets the wrapper only. No new module, no new
import, no cycle.

Names are effectively module-local: `grep -rn` for both identifiers across `lean/` returns **no**
consumer outside the two defining files, so aliasing them does not disturb any other module.

## 3. The interface: one definition, parametrised by the read-out map

The only structural difference is *where the approximating family lives*: on `Y` composed with `p`
(finite case) or on `X` (ambient case). Introduce a read-out `S : X → Z`:

```lean
def EncodingApproximationAt (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (P : X → W) {Z : Type*} (S : X → Z)
    (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  ∃ (r : ℕ) (B C : ℝ) (H : Fin r → Z → Fin m → ℂ),
    0 ≤ B ∧ 0 ≤ C ∧ (∀ z, ∑ i, ‖H i z‖ ≤ C) ∧
    ∀ k : K, ∃ coeff : W → Fin r → ℂ,
      (∀ w, ‖coeff w‖ ≤ B) ∧
      Integrable (fun x => dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (P x) i • H i (S x)) ^ 2) μ ∧
      (∫ x, dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (P x) i • H i (S x)) ^ 2 ∂μ) < γ^2
```

Then, definitionally (`Z := Y, S := p`, resp. `Z := X, S := id`):

```lean
abbrev FiniteEncodingApproximationAt μ p q b m γ : Prop :=
  EncodingApproximationAt μ p (fun x => q (p x)) p b m γ
abbrev AmbientEncodingAt μ p q b m γ : Prop :=
  EncodingApproximationAt μ p q id b m γ
```

Both are **definitional** aliases: the old bodies have `H i (p x)` and `H i x` respectively, which are
exactly `H i (S x)` at `S := p` and `S := id` (`id` is reducible). So no conversion lemma is needed and
`happrox` of either old statement is accepted unchanged. *This is why the `S`-parametrisation beats the
alternative* "abstract family `Kf : Fin r → X → Fin m → ℂ`": that version needs `∃Kf` which is strictly
weaker than `∃H` (not every ambient `Kf` factors through `p`), so it would force an unpacking prologue
in each wrapper and would not be definitionally equal; rejected.

Chosen over `Z` being inferred: `Z` is an explicit implicit for clarity; `S := id` also fixes it.

## 4. The common theorem

```lean
theorem uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (P : X → W) {Z : Type*} (S : X → Z) (b : X → D)
    (hp : Measurable p) (hP : Measurable P) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : ∀ᵐ y ∂μ.map p, condDistrib b p μ y =
      (m : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (g y i))
    (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map P)
      (condDistrib b P μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : ∀ (ω : Measure Circle) [IsProbabilityMeasure ω],
      (∀ n, 0 < n → n ≤ N → ‖∫ w, (w : ℂ)^n ∂ω‖ < c) →
      ω.real {w | ‖(w : ℂ)-1‖ ≤ 4*ρ} < 1/(4*(m : ℝ)^2))
    (happrox : EncodingApproximationAt μ p P S b m (((ρ^m/(m : ℝ))/100)/100)) :
    False
```

Wrappers (statements byte-identical to today's; bodies are the whole change):

```lean
theorem finite_uniform_precision_contradiction … :=
  uniform_precision_contradiction μ p (fun x => q (p x)) p b hp (hq.comp hp) hb
    m hm g hg hwild ρ c N hρ hc hN harc happrox

theorem ambient_uniform_precision_contradiction … :=
  uniform_precision_contradiction μ p q id b hp hq hb
    m hm g hg hwild ρ c N hρ hc hN harc happrox
```

## 5. Assumption-to-use table (from the two bodies, entry by entry)

| hypothesis | where consumed | notes |
|---|---|---|
| `μ`, `[IsProbabilityMeasure μ]` | `ν` construction, `Integrable`/`∫` in `happrox` | unchanged |
| `p : X → Y`, `hp` | `condDistrib b p μ` (kernel of the encoding); `hp` also feeds the map-instance route | `p x` appears in the encoding argument only — **never** in the approximation's second slot |
| `P : X → W`, `hP` | `hP.aemeasurable` for `IsProbabilityMeasure (μ.map P)`; `coeff (· j) (P x)` | the single genuine difference: ambient uses `inferInstance`. Kept as `hP` in the common statement; the `let`-route works for both, so no extra hypothesis |
| `S`, `H` | `Ap`, `Am`, `hbins`, the two `change` lines — always as `H k (S x)`, and `hH (S x)` | this is the whole abstraction |
| `hb` | `condDistrib b p μ` | unchanged |
| `m`, `hm` | `0 < m` for `(m:ℝ)` positivity, `NeZero M`, `hτδ`, `1/(4m²)` | unchanged |
| `g`, `hg` | finite-support structure of every conditional law; `predecessor_moment_sq` nonnegativity `hn` | unchanged; the *only* place `Y` survives in the proof |
| `hwild` | final contradiction against `harc` | **kept as a hypothesis, at `P`**; under `P := q∘p` it is literally the finite statement's hypothesis, under `P := q` the ambient one — no new premise, no disguised assumption |
| `hρ, hc, hN, harc` | the arc/measure bound; `τ`, `γ`, `ε` budget | unchanged |
| `happrox` | unpacked to `⟨r,B,C,H,hB,hC,hH,happ⟩`, then `choose coeff`, then `hbins (fun k => H k (S x)) (hH (S x))` | definitionally supplied by either alias |

No hypothesis is added, dropped or strengthened. In particular nothing about weak mixing, `M3`,
`(W)` or the compact tower appears: the difference law's wildness stays a hypothesis, exactly as now.

## 6. Edit sites for the transplant (exactly 7)

In the finite proof body, before pasting into `uniform_precision_contradiction`:

1. **delete** `let P : X → W := q ∘ p` (now a parameter);
2. **delete** `have hP : Measurable P := hq.comp hp` (now a parameter);
3. **keep** `let : IsProbabilityMeasure (μ.map P) := (Measure.isProbabilityMeasure_map_iff hP.aemeasurable).mpr inferInstance`;
4. `Ap`: `H i (p x)` → `H i (S x)`;
5. `Am`: `H i (p x)` → `H i (S x)`;
6. `hbins … (fun k => H k (p x)) (hH (p x))` → `(fun k => H k (S x)) (hH (S x))`;
7. the two `change` lines: 4 occurrences of `H k (p x)` → `H k (S x)`.

Everything else is copied verbatim. `FiniteBins.bounded_coefficient_bins`, `MomentTest`,
`predecessor_moment_sq`, `PhaseEncoding.kernelEncoding`, `harc`'s `Measure Circle` API and
`kCoeff`/`eval` are all already in scope in `ConditionalSpectrum`.

## 7. Preserved corrections and risks

* **Preserved (retired worker's correction):** the proposal to *delete* the allegedly dead instances
  here was **refuted by the compiler**; this plan is a merge, not a deletion, and the two theorem
  statements remain in the tree unchanged.
* **Risk 1 (instances).** Ambient uses `inferInstance` for `IsProbabilityMeasure (μ.map P)`, finite
  needs the explicit `.map` route. Both are proofs of a `Prop`; the common body uses the explicit
  route, which is available in both modules *if* `hP` is in scope — it is. To be confirmed at build.
* **Risk 2 (`abbrev` vs `def`).** Turning the two `def`s into `abbrev`s changes the *printed* type of
  every downstream hypothesis (line 479 `finite_uniform_successor_contradiction`, and the two
  `AmbientEncodingAt → EncodingApproximationAt` conversion lemmas around `ConditionalLimits:592`).
  Definitional equality should make them transparent, but this is a statement-display change, not a
  statement change, and per project policy must be re-elaborated and re-`#check`ed, not assumed.
* **Risk 3 (`omit` pragmas).** Both statements carry
  `omit [StandardBorelSpace Y] [Nonempty Y]`. The common statement should keep the same `omit`
  (only `Y` is used, through `p` and `Map Circle` in `harc`); verify at build.
* **Risk 4 (transparency of `id`).** `S := id` must elaborate `H i (id x)` ≡ `H i x`; reducible, but
  the ambient alias should be checked by `rfl` in a two-line test, not assumed.
* Saving: two 153-line bodies → one 153-line body + two 2-line bodies; plus two `def`s (31 lines) →
one `def` + two `abbrev`s (~20). Net ≈ **150 lines across two modules, with zero statement change.**
This is the *whole* of the CENSUS result 2; the CENSUS's own reserve about "the largest
declaration-level redundancy" is confirmed, and its negative result (rigidity half capped at ~70 lines)
is untouched.

## 8. What is not done

No build, no elaboration, no `#check`. `SCAFFOLD.lean` in this directory is **uncompiled and contains
one `sorry`** standing for the transplant; it is not part of the build and proves nothing.
