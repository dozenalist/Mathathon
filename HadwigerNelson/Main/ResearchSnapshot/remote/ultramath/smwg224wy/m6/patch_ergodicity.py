#!/usr/bin/env python3
"""Replace `ergodic_wild_fourier`'s proof by the Theorem-A route, leaving
`TerminalObligation` as the sole non-derived ingredient (a declared axiom)."""
import pathlib

p = pathlib.Path("tree/lean/OAI/Analysis/PlaneSpectrum/Ergodicity.lean")
s = p.read_text()
s = s.replace("import OAI.Analysis.PlaneSpectrum.SpectralMeasure\n",
              "import OAI.Analysis.PlaneSpectrum.SpectralMeasure\nimport OAI.Analysis.PlaneSpectrum.TheoremA\n", 1)
old = """lemma ergodic_wild_fourier (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
    (hw : IsWild μ) (z : E) (hz : z ≠ 0) : ∫ d, (eval z d : ℂ) ∂μ = 0 := by
  obtain ⟨q,hq,hqc,hgood,hmix⟩ := exists_terminal_factor μ
  have := hmix
  have hd : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ)) := by
    refine ⟨relative_difference_invariant μ id q measurable_id hq (fun k => Eventually.of_forall (fun d => rfl)) hqc,?_⟩
    exact hgood id measurable_id (fun k => Eventually.of_forall (fun d => rfl)) (by simpa using hw)
  exact fourier_vanish_of_terminal μ q hq hqc hd z hz"""
new = """/-- DIAGNOSTIC PLACEHOLDER (m6 / d10).  The single non-derived ingredient: the factor
with an ergodic relative square and a non-diagonal relative product that the R1
restructure is meant to construct.  Everything below is proved. -/
def TerminalObligation (μ : Measure D) [IsProbabilityMeasure μ] : Prop :=
  ∃ (q : D → OrbitSpace K) (hq : Measurable q),
    (∀ k : K, ∀ᵐ d ∂μ, q (k • d) = k • q d) ∧
    ErgodicSMul K (D × D) (EuclideanFiveColor.RelativeProduct.law μ q hq) ∧
    ¬ ∀ᵐ z ∂(EuclideanFiveColor.RelativeProduct.law μ q hq), z.1 = z.2

axiom terminalObligation_diagnostic (μ : Measure D) [IsProbabilityMeasure μ]
  [ErgodicSMul K D μ] : TerminalObligation μ

lemma ergodic_wild_fourier (μ : Measure D) [IsProbabilityMeasure μ] [ErgodicSMul K D μ]
    (hw : IsWild μ) (z : E) (hz : z ≠ 0) : ∫ d, (eval z d : ℂ) ∂μ = 0 := by
  obtain ⟨q, hq, hqc, herg, hdiag⟩ := terminalObligation_diagnostic μ
  have hC : DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ) C = 0 :=
    RelativeSingularity.relative_singularity_of_ergodic μ q hq id measurable_id
      (fun k x => rfl) hdiag
  have hd : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ)) :=
    ⟨relative_difference_invariant μ id q measurable_id hq
      (fun k => Eventually.of_forall (fun d => rfl)) hqc, hC⟩
  exact fourier_vanish_of_terminal μ q hq hqc hd z hz"""
assert old in s, "anchor not found"
p.write_text(s.replace(old, new, 1))
print("Ergodicity.lean patched")
