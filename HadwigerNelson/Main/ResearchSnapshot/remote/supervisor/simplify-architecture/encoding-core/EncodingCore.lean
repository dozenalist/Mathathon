/-
  PROPOSED COMMON ENCODING CORE.  For review; not integrated, not built by this block.

  The proof body is a MECHANICAL TRANSPLANT of
    `OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction`
  (`lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean`, lines 324-476, source sha256 6602b9d8f20bbdfd447f2f3fcfa523f2c33d09c247e3d2983be7503df9f2dc9b),
  with exactly the 7 edits listed in `PLAN.md` §6: delete the two local `P`/`hP` bindings (now
  parameters) and rewrite the 6 sites `H ?_ (p x)` -> `H ?_ (S x)`, `hH (p x)` -> `hH (S x)`.
  Nothing else was touched. The `kernelEncoding … (p x)` arguments are NOT parametrised.

  Intended home: inside `ConditionalSpectrum.lean`, immediately before
  `finite_uniform_precision_contradiction`. As a standalone module it compiles against the same
  three imports that file uses, so it can be checked without touching shared sources.
-/
import OAI.Analysis.PlaneSpectrum.FourierTests
import OAI.Analysis.PlaneSpectrum.SmallArcs
import OAI.MeasureTheory.CompactFactors.ConditionalSelection

namespace OAI
noncomputable section
open Filter Topology
open MeasureTheory ProbabilityTheory
open EuclideanFiveColor
open scoped ENNReal BigOperators ComplexConjugate
open scoped BigOperators ENNReal

-- The two originals each declare these LOCAL instances (Spectrum:43-44,178-179,260-261;
-- Limits:363-364) and they never leak across files, so the merged file must declare them again.
-- They are the same terms in both sources (`borel Circle`), which is what makes the two statements
-- the same proposition; `Circle` is Mathlib's unit circle with `ω.real : ℝ`.
local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

namespace PlaneFiveColor.Spectral

section
variable {X Y W : Type*} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
  [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]

/-- The shared encoding hypothesis. `S : X → Z` is the read-out map: the approximating family lives
on `Z` and is sampled at `S x`. `P : X → W` is the factor map whose coefficient functions are used.

`S := p` (with `Z := Y`) gives the old `FiniteEncodingApproximationAt`;
`S := id` (with `Z := X`) gives the old `AmbientEncodingAt`. Both are *definitional*, see the two
`abbrev`s below and the `Iff.rfl` checks in `Wrappers.lean`. -/
def EncodingApproximationAt (μ : Measure X) [IsProbabilityMeasure μ] (p : X → Y) (P : X → W)
    {Z : Type*} (S : X → Z)
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

/-- Definitional shadow of the old `FiniteEncodingApproximationAt`. -/
abbrev FiniteEncodingApproximationAt' (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  EncodingApproximationAt μ p (fun x => q (p x)) p b m γ

/-- Definitional shadow of the old `AmbientEncodingAt` (whose home is `ConditionalLimits`). -/
abbrev AmbientEncodingAt' (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  EncodingApproximationAt μ p q id b m γ

omit [StandardBorelSpace Y] [Nonempty Y] in
/-- Both uniform-precision contradictions are this statement at `S := p, P := q ∘ p` and
`S := id, P := q`. No hypothesis is added, dropped or strengthened; in particular `hwild` stays a
hypothesis at `P` — the wildness of the difference law is neither derived nor hidden. -/
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
    False := by
    classical
    let : IsProbabilityMeasure (μ.map P) :=
      (Measure.isProbabilityMeasure_map_iff hP.aemeasurable).mpr inferInstance
    let ν := DifferenceFourier.differenceLaw (μ.map P) (condDistrib b P μ)
    let : IsProbabilityMeasure ν := inferInstance
    have hn (a : E) : 0 ≤ (∫ d, (eval a d : ℂ) ∂ν).re := by
      rw [← predecessor_moment_sq μ P b hP hb a]
      exact integral_nonneg fun _ => sq_nonneg _
    let τ := (ρ^m/(m : ℝ))/100
    let γ := τ/100
    have hmr : (0 : ℝ) < m := Nat.cast_pos.mpr hm
    have hτ : 0 < τ := by dsimp [τ]; positivity
    have hτδ : 18*τ^2 < (ρ^m/(m : ℝ))^2/20 := by
      dsimp [τ]
      nlinarith [sq_pos_of_pos (div_pos (pow_pos hρ m) hmr)]
    obtain ⟨r, B, C, H, hB, hC, hH, happ⟩ := happrox
    choose coeff hcoeff hInt hErr using happ
    obtain ⟨L, bins, hbins⟩ := FiniteBins.bounded_coefficient_bins
      (V := Fin m → ℂ) r B C τ hC hτ
    let M := 20*(L+1)*m^2
    have hM : 2 ≤ M := by dsimp [M]; nlinarith [Nat.one_le_iff_ne_zero.mpr hm.ne']
    let : NeZero M := ⟨by omega⟩
    let T := MomentTest M N
    let ε := min 1 (c^2/(4*(Fintype.card T+1)))
    have hε : 0 < ε := by dsimp [ε]; apply lt_min (by norm_num); positivity
    have hε1 : ε ≤ 1 := min_le_left _ _
    obtain ⟨t, ht, htM, hTest⟩ := exists_simultaneous_moment_parameter ν hwild hn M N hM hN ε hε hε1
    let xs : Fin M → F := fun j => (j.val+1)*t
    have hxs (j : Fin M) : |(xs j : ℝ)| < 2 := by
      have hMr : (0 : ℝ) < M := Nat.cast_pos.mpr (by omega)
      have hj : (j.val+1 : ℝ) ≤ M := by exact_mod_cast j.isLt
      have hx : |(xs j : ℝ)| = (j.val+1 : ℝ)*|(t : ℝ)| := by
        simp [xs, abs_mul, abs_of_nonneg (show (0 : ℝ) ≤ j.val+1 by positivity)]
      rw [hx]
      have hmul := mul_lt_mul_of_pos_left htM (by positivity : (0 : ℝ) < j.val+1)
      have hbound : (j.val+1 : ℝ) * (1/(M : ℝ)) ≤ 1 := by
        rw [mul_one_div, div_le_one hMr]
        exact hj
      linarith
    choose u v huv using fun j => real_algebraic_sum_two_rotations (xs j) (hxs j)
    let β := condDistrib b p μ
    let enc : K → Y → Fin m → ℂ := fun k =>
      PhaseEncoding.kernelEncoding β (fun d => (eval (kCoeff k) d : ℂ)) m
    let Hp : Fin M → X → Fin m → ℂ := fun j x => enc (u j) (p x)
    let Hm : Fin M → X → Fin m → ℂ := fun j x => enc (v j) (p x)
    let Ap : Fin M → X → Fin m → ℂ := fun j x => ∑ i, coeff (u j) (P x) i • H i (S x)
    let Am : Fin M → X → Fin m → ℂ := fun j x => ∑ i, coeff (v j) (P x) i • H i (S x)
    let ap : Fin M → X → Circle := fun j x => eval (kCoeff (u j)) (b x)
    let am : Fin M → X → Circle := fun j x => eval (kCoeff (v j)) (b x)
    let zp : X → Fin M → Fin m → Circle := fun x j i => eval (kCoeff (u j)) (g (p x) i)
    let zm : X → Fin M → Fin m → Circle := fun x j i => eval (kCoeff (v j)) (g (p x) i)
    have henc : ∀ᵐ x ∂μ, ∀ j, PhaseEncoding.encoding (zp x j) = Hp j x ∧
        PhaseEncoding.encoding (zm x j) = Hm j x := by
      filter_upwards [ae_of_ae_map hp.aemeasurable hg] with x hx
      intro j
      exact ⟨(PhaseEncoding.kernelEncoding_eq_encoding β (eval (kCoeff (u j))) m hm (p x) (g (p x)) hx).symm,
        (PhaseEncoding.kernelEncoding_eq_encoding β (eval (kCoeff (v j))) m hm (p x) (g (p x)) hx).symm⟩
    have hmem : ∀ᵐ x ∂μ, ∀ j, (∃ i, ap j x = zp x j i) ∧ (∃ i, am j x = zm x j i) := by
      filter_upwards [SampledAtoms.ae_sampled_list μ p b hp hb hm g hg] with x hx
      obtain ⟨i, hi⟩ := hx
      intro j
      exact ⟨⟨i, congrArg (eval (kCoeff (u j))) hi⟩, ⟨i, congrArg (eval (kCoeff (v j))) hi⟩⟩
    let f : T → W → ℝ := fun z w =>
      ‖∫ x, (eval (momentArgument z * ofF t) (b x) : ℂ) ∂condDistrib id P μ w‖^2
    have hf (z : T) : Integrable (f z) (μ.map P) :=
      integrable_predecessor_moment_sq μ P b hP hb _
    have hfTest (z : T) : (∫ w, f z w ∂μ.map P) < ε := by
      rw [show (∫ w, f z w ∂μ.map P) =
        (∫ d, (eval (momentArgument z * ofF t) d : ℂ) ∂ν).re from
          predecessor_moment_sq μ P b hP hb _]
      exact hTest z
    have hfBudget : (∑ z, ∫ w, f z w ∂μ.map P)/(c^2) < 1/4 :=
      simultaneous_test_budget _ c hc hfTest
    have heBudget : 10*(∑ j, ((∫ x, dist (Hp j x) (Ap j x)^2 ∂μ) +
        (∫ x, dist (Hm j x) (Am j x)^2 ∂μ)))/((M : ℝ)*τ^2) < 1/4 := by
      have hs : (∑ j, ((∫ x, dist (Hp j x) (Ap j x)^2 ∂μ) +
          (∫ x, dist (Hm j x) (Am j x)^2 ∂μ))) < (M : ℝ)*(2*γ^2) := by
        calc
          _ < ∑ _j : Fin M, 2*γ^2 := Finset.sum_lt_sum_of_nonempty Finset.univ_nonempty
            (fun j _ => by
              have h1 : (∫ x, dist (Hp j x) (Ap j x)^2 ∂μ) < γ^2 := hErr (u j)
              have h2 : (∫ x, dist (Hm j x) (Am j x)^2 ∂μ) < γ^2 := hErr (v j)
              linarith)
          _ = _ := by simp
      have hMr : (0 : ℝ) < M := Nat.cast_pos.mpr (by omega)
      rw [div_lt_iff₀ (mul_pos hMr (sq_pos_of_pos hτ))]
      dsimp [γ] at hs
      nlinarith
    let arr : W → Fin M → {a : Fin 2 → Fin r → ℂ // ‖a‖ ≤ B} := fun w j =>
      ⟨![coeff (u j) w, coeff (v j) w], two_array_norm_bound (hcoeff _ _) (hcoeff _ _) hB⟩
    let bin : W → Fin M → Fin L := fun w j => bins (arr w j)
    have hlarge : (L : ℝ)*(10*m^2 : ℕ) < (9/10 : ℝ)*Fintype.card (Fin M) := by
      simp only [Fintype.card_fin]
      dsimp [M]
      push_cast
      nlinarith [sq_pos_of_pos hmr, Nat.cast_nonneg (α := ℝ) L]
    have hbin : ∀ᵐ w ∂μ.map P, ∀ i j, bin w i = bin w j →
        ∀ᵐ x ∂condDistrib id P μ w, dist (Ap i x) (Ap j x) ≤ τ ∧
          dist (Am i x) (Am j x) ≤ τ := by
      filter_upwards [ConditionalFiber.ae_in_own_fiber μ P hP] with w hw
      intro i j hij
      filter_upwards [hw] with x hx
      have hh := hbins (arr w i) (arr w j) hij (fun k => H k (S x)) (hH (S x))
      have h0 := (hh 0).le
      have h1 := (hh 1).le
      change dist (∑ k, coeff (u i) (P x) k • H k (S x))
        (∑ k, coeff (u j) (P x) k • H k (S x)) ≤ τ ∧
        dist (∑ k, coeff (v i) (P x) k • H k (S x))
        (∑ k, coeff (v j) (P x) k • H k (S x)) ≤ τ
      rw [hx]
      exact ⟨h0, h1⟩
    have hupper : ∀ᵐ w ∂μ.map P, (∀ z, f z w < c^2) → ∀ i j, i ≠ j →
        (condDistrib id P μ w).real {x |
          dist ((ap i x : ℂ)*(am i x : ℂ)) ((ap j x : ℂ)*(am j x : ℂ)) ≤ 4*ρ}
          < 1/(4*(m : ℝ)^2) := by
      apply Filter.Eventually.of_forall
      intro w hw i j hij
      have hMom : ∀ n : ℕ, 0 < n → n ≤ N →
          ‖∫ x, (eval ((n : E)*(ofF (xs i)-ofF (xs j))) (b x) : ℂ)
            ∂condDistrib id P μ w‖ < c := by
        intro n hn hnN
        let z : T := (⟨n-1, by omega⟩, ⟨(i,j), hij⟩)
        have he : (n : E)*(ofF (xs i)-ofF (xs j)) = momentArgument z * ofF t := by
          have hnv : (n-1)+1 = n := by omega
          have hnv' : ((n-1 : ℕ) : E)+1=(n : E) := by exact_mod_cast hnv
          simp only [momentArgument, z, hnv']
          dsimp [xs]
          simp only [map_mul, map_add, map_natCast, map_one]
          ring
        have hh := hw z
        change ‖∫ x, (eval (momentArgument z * ofF t) (b x) : ℂ)
           ∂condDistrib id P μ w‖^2 < c^2 at hh
        rw [he]
        nlinarith [norm_nonneg (∫ x, (eval (momentArgument z * ofF t) (b x) : ℂ)
           ∂condDistrib id P μ w)]
      have hh := pair_collision_upper (condDistrib id P μ w) b hb
        (ofF (xs i)) (ofF (xs j)) m N ρ c harc hMom
      have he (j : Fin M) (x : X) : (ap j x : ℂ)*(am j x : ℂ) =
          (eval (ofF (xs j)) (b x) : ℂ) := by
        change (eval (kCoeff (u j)) (b x) : ℂ) * (eval (kCoeff (v j)) (b x) : ℂ) = _
        rw [huv j]
        exact congrArg (fun z : Circle => (z : ℂ)) (eval_add _ _ _).symm
      simpa only [he] using hh
    apply FiniteModule.common_fiber_contradiction μ P hP m hm ρ τ (c^2) hρ hτ
      (sq_pos_of_pos hc) hτδ Hp Hm Ap Am
      (fun j => (PhaseEncoding.measurable_kernelEncoding β _ (measurable_eval_coe _) m).comp hp)
      (fun j => (PhaseEncoding.measurable_kernelEncoding β _ (measurable_eval_coe _) m).comp hp)
      (fun j => hInt (u j)) (fun j => hInt (v j)) zp zm ap am
      (fun j => (measurable_eval _).comp hb) (fun j => (measurable_eval _).comp hb)
      henc hmem f hf (Filter.Eventually.of_forall (fun w z => sq_nonneg _))
      (by simp only [Fintype.card_fin]; linarith) L bin hlarge hbin hupper

end
end PlaneFiveColor.Spectral
end
end OAI
