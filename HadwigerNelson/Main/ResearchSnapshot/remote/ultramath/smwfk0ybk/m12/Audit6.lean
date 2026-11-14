import OAI.Geometry.PlaneColoring.Chromatic

/-! ### The measurable weak chromatic number of the plane is 6 or 7

`Chromatic.lean` proves `6 <= chi <= 7` for `Problem160.planeChromaticNumber` (proper colourings of
the `Plane` vocabulary).  The bundle has no monotonicity for the *weak* predicate
`EuclideanFiveColor.WeakColoring`, so "no weak measurable 5-colouring" does not by itself give
"no weak measurable k-colouring for k <= 5".  Below: monotonicity, and hence the same two-sided
bound for the weak predicate — i.e. the measurability removal does not move the threshold. -/

namespace Audit

noncomputable section

open OAI

/-- Monotonicity of the weak predicate in the number of colours. -/
theorem weakColoring_mono {k m : ℕ} (hkm : k ≤ m) {c : ℂ → Fin k}
    (hc : Measurable c) (hw : EuclideanFiveColor.WeakColoring k c) :
    ∃ d : ℂ → Fin m, Measurable d ∧ EuclideanFiveColor.WeakColoring m d := by
  have hcm : Measurable (Fin.castLE hkm) := measurable_of_countable _
  have hmeas : Measurable (fun x : ℂ => Fin.castLE hkm (c x)) := hcm.comp hc
  refine ⟨fun x => Fin.castLE hkm (c x), hmeas, hmeas.aemeasurable, ?_⟩
  filter_upwards [hw.2] with p hp hcontra
  exact hp (Fin.castLE_injective hkm hcontra)

/-- Least number of colours of a measurable weak colouring (null-set predicate). -/
def weakChromaticNumber : ℕ :=
  sInf {k : ℕ | ∃ c : ℂ → Fin k, Measurable c ∧ EuclideanFiveColor.WeakColoring k c}

/-- The seven-colouring, transferred, is an inhabited weak colouring. -/
theorem weak_seven : ∃ c : ℂ → Fin 7, Measurable c ∧ EuclideanFiveColor.WeakColoring 7 c := by
  obtain ⟨c, hc⟩ := Problem160.properColoring_seven
  exact EuclideanFiveColor.proper_to_borel_weak (Problem160.properColoring_of_plane hc)

theorem six_le_weakChromaticNumber : 6 ≤ weakChromaticNumber := by
  rw [weakChromaticNumber]
  refine le_csInf ⟨7, weak_seven⟩ ?_
  intro k hk
  by_contra h
  push Not at h
  obtain ⟨d, hd, hw⟩ := hk
  obtain ⟨e, he₁, he₂⟩ := weakColoring_mono (m := 5) (by omega) hd hw
  exact EuclideanFiveColor.no_measurable_weak_five_coloring he₁ he₂

theorem weakChromaticNumber_le_seven : weakChromaticNumber ≤ 7 := by
  rw [weakChromaticNumber]
  exact Nat.sInf_le weak_seven

theorem weakChromaticNumber_bounds : 6 ≤ weakChromaticNumber ∧ weakChromaticNumber ≤ 7 :=
  ⟨six_le_weakChromaticNumber, weakChromaticNumber_le_seven⟩

/-- For every k <= 5 there is no measurable weak colouring at all. -/
theorem no_weak_of_le_five (k : ℕ) (hk : k ≤ 5) :
    ¬ ∃ c : ℂ → Fin k, Measurable c ∧ EuclideanFiveColor.WeakColoring k c := by
  rintro ⟨c, hc, hw⟩
  obtain ⟨e, he₁, he₂⟩ := weakColoring_mono (m := 5) hk hc hw
  exact EuclideanFiveColor.no_measurable_weak_five_coloring he₁ he₂

#print axioms weakChromaticNumber_bounds
#print axioms no_weak_of_le_five

end

end Audit
