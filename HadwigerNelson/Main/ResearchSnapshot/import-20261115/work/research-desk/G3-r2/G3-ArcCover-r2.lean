/-
  G3 — `A6.ArcCover`, lane A of swarm smwgwui56 (member m1).

  STATUS: **UNCOMPILED**.  Source only: the swarm rules forbid running `lean`/`lake`/any
  build, so nothing in this file has been elaborated.  Every Mathlib/repository name used
  below was checked by reading the pinned checkout
  `.scratch/mathlib4/Mathlib` (Lean 4.34.1, Mathlib d13f23b7) and the repository
  `lean/OAI/...`; see NOTES-mA.md for the name → file:line table and for the informal
  proof.

  TARGET (exactly the bridge's `A6-Bridge-m2.lean`, `def ArcCover`, section 8):

    def arc : Set Angles := {t | ∃ s : ℝ, |s| < Real.pi / 6 ∧ (s : Angles) = t}

    def ArcCover : Prop :=
      ∀ᵐ θ ∂angularMeasure, ∃ t ∈ arc, ∃ j : Fin 6, θ = t + sixAngle j

  where (repository, not in the bridge)

    Angles        : `abbrev Angles := AddCircle (2 * Real.pi)`      Coloring.lean:16
    angularMeasure: `def angularMeasure : Measure Angles
                       := AddCircle.haarAddCircle`                  Coloring.lean:17
    sixty         : `def sixty : ℝ := Real.pi / 3`                  PaletteTransport.lean:390
    sixAngle      : `def sixAngle (j : Fin 6) : Angles
                       := j.val • (sixty : Angles)`                 AngularBoundary.lean:103

  THEOREM PROVED HERE: `OAI.EuclideanFiveColor.A6.arcCover`, with the bridge's statement
  verbatim (`θ : Angles`, measure `angularMeasure`, not a real variable).

  Argument (see NOTES-mA.md for the details and for the exact API audit):
  for `r : ℝ`, let `n = ⌊(r + sixty/2)/sixty⌋` (nearest integer to `r/sixty`) and
  `s = r - n·sixty`.  Floor bounds give `-π/6 ≤ s < π/6`; `s = -π/6` happens exactly at
  `r = π/6 + (n-1)·sixty`, one of the six exceptional points.  Reducing `n` modulo 6 gives
  `j : Fin 6` with `n = j.val + 6m`, and `6·sixty = 2π` makes `↑r = ↑s + sixAngle j` in
  `Angles`.  The exceptional set is countable and `angularMeasure` has no atoms, so it is
  null.
-/

import Mathlib

noncomputable section

open MeasureTheory Set Filter

namespace OAI
namespace EuclideanFiveColor

/-! ## 0. Scaffold — already in the repository, DELETE THIS BLOCK when pasting into
`A6-Bridge-m2.lean` (there `Angles`, `angularMeasure`, `sixty`, `sixAngle` and the two
instances of `BinaryPalettes.lean` are already in scope). -/

instance anglePeriodPositive : Fact (0 < 2 * Real.pi) := ⟨by positivity⟩

abbrev Angles := AddCircle (2 * Real.pi)

def angularMeasure : Measure Angles := AddCircle.haarAddCircle

instance : IsProbabilityMeasure angularMeasure :=
  inferInstanceAs (IsProbabilityMeasure (AddCircle.haarAddCircle (T := 2 * Real.pi)))

instance : angularMeasure.IsAddHaarMeasure :=
  inferInstanceAs (AddCircle.haarAddCircle (T := 2 * Real.pi)).IsAddHaarMeasure

/-- `sixty = π/3` (`PaletteTransport.lean:390`). -/
def sixty : ℝ := Real.pi / 3

/-- `sixAngle j = j • 60°` (`AngularBoundary.lean:103`). -/
def sixAngle (j : Fin 6) : Angles := j.val • (sixty : Angles)

/-- Verbatim from `BinaryPalettes.lean:152-156`. -/
instance anglesNontrivial : Nontrivial Angles := by
  have : Nontrivial Circle := ⟨⟨1, -1, by
    intro h
    have hh := congrArg (fun z : Circle => (z : ℂ)) h
    norm_num at hh⟩⟩
  exact AddCircle.homeomorphCircle'.toEquiv.nontrivial

/-- Verbatim from `BinaryPalettes.lean:159-160`: the angular measure has no atoms. -/
instance angularMeasure_nullSingleton : NullSingletonClass angularMeasure :=
  Measure.IsAddHaarMeasure.nullSingletonClass angularMeasure

namespace A6

/-! ## 1. The bridge's fundamental arc (verbatim) -/

def arc : Set Angles := {t | ∃ s : ℝ, |s| < Real.pi / 6 ∧ (s : Angles) = t}

/-! ## 2. Arithmetic of `sixty` and of `sixAngle` -/

lemma sixty_pos : (0 : ℝ) < sixty := by
  simp only [sixty]
  positivity

lemma sixty_ne : sixty ≠ 0 := sixty_pos.ne'

/-- `6 · 60° = 360°`. -/
lemma two_pi_eq_six_sixty : 2 * Real.pi = 6 * sixty := by
  simp only [sixty]
  ring

/-- `30° = π/6`. -/
lemma pi_six_eq : sixty / 2 = Real.pi / 6 := by
  simp only [sixty]
  ring

/-- `sixAngle j` is the circle point `j · 60°`, written as a real multiple of `sixty`. -/
lemma sixAngle_eq_coe (j : Fin 6) : sixAngle j = (((j.val : ℝ) * sixty : ℝ) : Angles) := by
  show j.val • (sixty : Angles) = (((j.val : ℝ) * sixty : ℝ) : Angles)
  rw [← AddCircle.coe_nsmul, nsmul_eq_mul]

/-- An integral multiple of `2π` is `0` in `Angles`. -/
lemma coe_period_mul (m : ℤ) : (((m : ℝ) * (2 * Real.pi) : ℝ) : Angles) = 0 := by
  rw [AddCircle.coe_eq_zero_iff]
  exact ⟨m, by rw [zsmul_eq_mul]⟩

/-- Euclidean division by `6`: every integer is `j.val + 6m` with `j : Fin 6`. -/
lemma mod_six_spec (n : ℤ) :
    ∃ j : Fin 6, ∃ m : ℤ, (n : ℝ) = (j.val : ℝ) + 6 * (m : ℝ) := by
  have h0 : 0 ≤ n % 6 := Int.emod_nonneg n (by norm_num)
  have h6 : n % 6 < 6 := Int.emod_lt_of_pos n (by norm_num)
  have hdiv : (n : ℝ) = (((n % 6).toNat : ℕ) : ℝ) + 6 * ((n / 6 : ℤ) : ℝ) := by
    have h : (n : ℤ) = ((n % 6).toNat : ℤ) + 6 * (n / 6) := by
      have h' := Int.emod_add_mul_ediv n 6
      rw [← Int.toNat_of_nonneg h0] at h'
      linarith
    exact_mod_cast h
  have hk : (n % 6).toNat < 6 := by omega
  exact ⟨⟨(n % 6).toNat, hk⟩, n / 6, hdiv⟩

/-! ## 3. The pointwise covering step off the six exceptional points -/

/-- **Real-level covering step.**  If `r : ℝ` is not one of the six points
`π/6 + m·sixty` (`m : ℤ`), then its image in `Angles` lies in one of the six translates
`arc + sixAngle j`.  This is `arcCover` with the a.e. statement replaced by its pointwise
form off the (countable) exceptional set. -/
lemma exists_arc_of_not_bad (r : ℝ)
    (hbad : ∀ m : ℤ, r ≠ Real.pi / 6 + (m : ℝ) * sixty) :
    ∃ t ∈ arc, ∃ j : Fin 6, ((r : ℝ) : Angles) = t + sixAngle j := by
  classical
  -- `n` is the nearest integer to `r / sixty`, obtained as `⌊(r + sixty/2)/sixty⌋`.
  obtain ⟨n, hn_le, hn_lt⟩ :
      ∃ n : ℤ, (n : ℝ) * sixty ≤ r + sixty / 2 ∧
        r + sixty / 2 < ((n : ℝ) + 1) * sixty := by
    refine ⟨⌊(r + sixty / 2) / sixty⌋, ?_, ?_⟩
    · rw [← le_div_iff₀ sixty_pos]
      exact Int.floor_le _
    · rw [← div_lt_iff₀ sixty_pos]
      exact Int.lt_floor_add_one _
  -- the fractional shift, in `[-π/6, π/6)`
  set s : ℝ := r - (n : ℝ) * sixty with hs
  have hs_expand : ((n : ℝ) + 1) * sixty = (n : ℝ) * sixty + sixty := by ring
  have hlow : -(Real.pi / 6) ≤ s := by
    rw [hs]
    linarith [pi_six_eq]
  have hhigh : s < Real.pi / 6 := by
    rw [hs]
    rw [hs_expand] at hn_lt
    linarith [pi_six_eq]
  have hs_le : |s| ≤ Real.pi / 6 := by
    rcases le_or_gt 0 s with hs0 | hs0
    · rw [abs_of_nonneg hs0]
      linarith
    · rw [abs_of_neg hs0]
      linarith
  -- the lower endpoint `s = -π/6` is exactly one of the six exceptional points
  have hs_ne : |s| ≠ Real.pi / 6 := by
    intro habs
    rcases le_or_gt 0 s with hs0 | hs0
    · -- `s = π/6` is excluded by the strict floor bound
      have hs1 : s = sixty / 2 := by
        rw [abs_of_nonneg hs0] at habs
        linarith [pi_six_eq]
      rw [hs] at hs1
      have h2 : ((n : ℝ) + 1) * sixty = (n : ℝ) * sixty + sixty := by ring
      rw [h2] at hn_lt
      linarith
    · -- `s = -π/6` forces `r = π/6 + (n-1)·sixty`
      have hs1 : s = -(sixty / 2) := by
        rw [abs_of_neg hs0] at habs
        linarith [pi_six_eq]
      refine hbad (n - 1) ?_
      rw [hs] at hs1
      push_cast
      linarith [pi_six_eq]
  have hs_lt : |s| < Real.pi / 6 := lt_of_le_of_ne hs_le hs_ne
  -- reduce `n` modulo `6` and absorb the difference as a period
  obtain ⟨j, m, hm⟩ := mod_six_spec n
  refine ⟨(s : Angles), ⟨s, hs_lt, rfl⟩, j, ?_⟩
  have hreal : r - (s + (j.val : ℝ) * sixty) = (m : ℝ) * (2 * Real.pi) := by
    rw [hs, hm, two_pi_eq_six_sixty]
    ring
  have hzero : (((r - (s + (j.val : ℝ) * sixty)) : ℝ) : Angles) = 0 := by
    rw [AddCircle.coe_eq_zero_iff]
    exact ⟨m, by rw [zsmul_eq_mul]; exact hreal.symm⟩
  have hEq : ((r : ℝ) : Angles) -
      (((s : ℝ) : Angles) + (((j.val : ℝ) * sixty : ℝ) : Angles)) = 0 := by
    rw [← AddCircle.coe_add, ← AddCircle.coe_sub]
    exact hzero
  have hfin : ((r : ℝ) : Angles) = ((s : ℝ) : Angles) +
      (((j.val : ℝ) * sixty : ℝ) : Angles) := sub_eq_zero.mp hEq
  rw [← sixAngle_eq_coe] at hfin
  exact hfin

/-! ## 4. The six exceptional points are null -/

/-- The six points `π/6 + m·60°` of the circle (`m : ℤ`; only `m mod 6` matters). -/
def badSet : Set Angles :=
  Set.range fun m : ℤ => ((Real.pi / 6 + (m : ℝ) * sixty : ℝ) : Angles)

lemma badSet_countable : badSet.Countable := Set.countable_range _

lemma badSet_measure_zero : angularMeasure badSet = 0 :=
  badSet_countable.measure_zero angularMeasure

/-! ## 5. `arcCover` — the bridge's `ArcCover`, verbatim -/

/-- **The six translates of the open fundamental arc cover the circle off a null set.**
This is exactly the bridge's `def ArcCover` (`A6-Bridge-m2.lean`, section 8). -/
theorem arcCover : ∀ᵐ θ ∂angularMeasure, ∃ t ∈ arc, ∃ j : Fin 6, θ = t + sixAngle j := by
  filter_upwards [measure_eq_zero_iff_ae_notMem.mp badSet_measure_zero] with θ hθ
  obtain ⟨r, rfl⟩ := QuotientAddGroup.mk_surjective θ
  refine exists_arc_of_not_bad r fun m hrm => hθ ⟨m, ?_⟩
  rw [hrm]

end A6
end EuclideanFiveColor
end OAI

#print axioms OAI.EuclideanFiveColor.A6.arcCover
