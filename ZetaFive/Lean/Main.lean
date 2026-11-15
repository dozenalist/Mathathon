module

public import ZetaFive.Lean.Common.Normalization
public import ZetaFive.Lean.Family.Construction
public import ZetaFive.Lean.Family.Positivity

@[expose] public section

/-! # The precise remaining inputs to the irrationality argument

`FamilyEstimates k parameters` is a list of proof obligations, NOT an instance
or an axiom. `PaperEstimates k` specializes it to Lai's parameters. No value of
either structure is currently constructed in this development.
The theorem below checks the final implication from those obligations, while
keeping the target tied to Mathlib's Riemann zeta function.
-/

open Polynomial Filter Topology

namespace ZetaFive

/-- Outstanding estimates for the actual Hankel family at weight `k`.
The exponential bounds include whatever positive slack is needed to absorb
the lower-order terms in the paper's asymptotic estimates. -/
structure FamilyEstimates (k : ℕ) (parameters : ℕ → Parameters) where
  pole_moments : PoleMoments k
  normalizer : ℕ → ℚ
  integerPolynomial : ℕ → ℤ[X]
  arithmeticExponent : ℝ
  analyticExponent : ℝ
  negative_margin : arithmeticExponent + analyticExponent < 0
  coefficients_integer : ∀ᶠ n in atTop,
    (integerPolynomial n).map (Int.castRingHom ℚ) =
      C (normalizer n) * normalized k (parameters n)
  normalizer_positive : ∀ᶠ n in atTop, 0 < normalizer n
  arithmetic_bound : ∀ᶠ n in atTop,
    (normalizer n : ℝ) ≤ Real.exp (arithmeticExponent * (n : ℝ) ^ 2)
  analytic_bound : ∀ᶠ n in atTop,
    (normalized k (parameters n)).eval₂ (Rat.castHom ℝ) (zeta k) ≤
      Real.exp (analyticExponent * (n : ℝ) ^ 2)

/-- Conditional final deduction for any family with linearly bounded size. -/
theorem irrational_of_family_estimates (k : ℕ) (hk : 2 ≤ k)
    (parameters : ℕ → Parameters) (d : ℕ)
    (hsize : ∀ n, (parameters n).h ≤ d * n) (h : FamilyEstimates k parameters) :
    Irrational (zeta k) :=
  Common.irrational_of_normalized_estimates (zeta k) d
    (fun n => normalized k (parameters n)) h.normalizer h.integerPolynomial
    h.arithmeticExponent h.analyticExponent h.negative_margin
    (fun n => (normalized_natDegree_le k (parameters n)).trans (hsize n))
    h.coefficients_integer h.normalizer_positive
    (Filter.Eventually.of_forall fun n => normalized_pos k hk h.pole_moments (parameters n))
    h.arithmetic_bound h.analytic_bound

/-- The outstanding inputs for Lai's original 40/3/37 family. -/
abbrev PaperEstimates (k : ℕ) := FamilyEstimates k laiParameters

/-- Conditional application to Lai's parameters. -/
theorem irrational_of_paper_estimates (k : ℕ) (hk : 2 ≤ k) (h : PaperEstimates k) :
    Irrational (zeta k) :=
  irrational_of_family_estimates k hk laiParameters 37 (fun _ => le_rfl) h

/-- Conditional application to the 12/1/11 family in the all-weight exposition. -/
theorem irrational_of_calegari_estimates (k : ℕ) (hk : 2 ≤ k)
    (h : FamilyEstimates k calegariParameters) : Irrational (zeta k) :=
  irrational_of_family_estimates k hk calegariParameters 11 (fun _ => le_rfl) h

/-- The conditional theorem has the standard complex-zeta conclusion. -/
theorem riemannZeta_irrational_of_paper_estimates (k : ℕ) (hk : 2 ≤ k)
    (h : PaperEstimates k) : ∃ x : ℝ, Irrational x ∧ riemannZeta (k : ℂ) = x :=
  ⟨zeta k, irrational_of_paper_estimates k hk h, riemannZeta_eq k hk⟩

/-- Uniform application over the requested range, still conditional on the estimates. -/
theorem irrational_two_through_five_of_estimates
    (h : ∀ k : ℕ, 2 ≤ k → k ≤ 5 → PaperEstimates k) :
    ∀ k : ℕ, 2 ≤ k → k ≤ 5 → Irrational (zeta k) := by
  intro k hk hk5
  exact irrational_of_paper_estimates k hk (h k hk hk5)

end ZetaFive

