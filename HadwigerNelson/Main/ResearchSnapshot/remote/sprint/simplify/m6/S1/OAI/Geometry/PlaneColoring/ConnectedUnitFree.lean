import Mathlib

namespace OAI

noncomputable section

namespace EuclideanFiveColor

/-- **Connected unit-free sets have diameter at most one.**

If `C` is preconnected and contains no pair of points at distance exactly one, then every
distance inside `C` is at most one.  This is the whole geometric content of the paper's
connected-set exclusion for `Delta(K_j)` (Proposition 7.1): only connectedness and continuity
of the distance are used, not planarity, compactness or any topology of the plane.

Sharp: the open ball of radius `1/2` is connected and unit-free, and its diameter is exactly `1`
(not attained). -/
theorem diam_le_one_of_preconnected_unitFree {E : Type*} [NormedAddCommGroup E]
    {C : Set E} (hC : IsPreconnected C)
    (h : ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≠ 1) :
    ∀ x ∈ C, ∀ y ∈ C, ‖x - y‖ ≤ 1 := by
  intro x hx y hy
  by_contra hcon
  push Not at hcon
  have hcont : ContinuousOn (fun p : E × E => ‖p.1 - p.2‖) (C ×ˢ C) :=
    (continuous_fst.sub continuous_snd).norm.continuousOn
  have hpre : IsPreconnected ((fun p : E × E => ‖p.1 - p.2‖) '' (C ×ˢ C)) :=
    (hC.prod hC).image _ hcont
  have h0 : (0 : ℝ) ∈ (fun p : E × E => ‖p.1 - p.2‖) '' (C ×ˢ C) :=
    ⟨(x, x), ⟨hx, hx⟩, by simp⟩
  have hd : ‖x - y‖ ∈ (fun p : E × E => ‖p.1 - p.2‖) '' (C ×ˢ C) :=
    ⟨(x, y), ⟨hx, hy⟩, rfl⟩
  have hone : (1 : ℝ) ∈ (fun p : E × E => ‖p.1 - p.2‖) '' (C ×ˢ C) :=
    hpre.Icc_subset h0 hd ⟨by norm_num, le_of_lt hcon⟩
  obtain ⟨p, hp, hpp⟩ := hone
  exact h p.1 hp.1 p.2 hp.2 hpp

/-- **The connected-set exclusion used for `Delta(K_j)`** (paper, Proposition 7.1).

If `C` is preconnected and no point of `C` is at distance exactly one from `z`, then `C` cannot
have points both strictly inside and strictly outside the unit circle about `z`. Equivalently: a
set that is connected, lies in one colour class, and is hit by the circle of radius one at no
point, cannot straddle that circle.  This is the a.e. exclusion the paper applies with
`C = K_j` and `z` a point carrying an endpoint label of edge `j`. -/
theorem not_straddle_of_isPreconnected {E : Type*} [NormedAddCommGroup E]
    {C : Set E} (hC : IsPreconnected C) {z : E} (h : ∀ q ∈ C, ‖z - q‖ ≠ 1) :
    ¬ ((∃ q ∈ C, ‖z - q‖ < 1) ∧ ∃ q ∈ C, 1 < ‖z - q‖) := by
  rintro ⟨⟨q₁, hq₁, h₁⟩, q₂, hq₂, h₂⟩
  have hcont : ContinuousOn (fun q : E => ‖z - q‖) C :=
    (continuous_const.sub continuous_id).norm.continuousOn
  have hpre : IsPreconnected ((fun q : E => ‖z - q‖) '' C) := hC.image _ hcont
  have ha : ‖z - q₁‖ ∈ (fun q : E => ‖z - q‖) '' C := ⟨q₁, hq₁, rfl⟩
  have hb : ‖z - q₂‖ ∈ (fun q : E => ‖z - q‖) '' C := ⟨q₂, hq₂, rfl⟩
  have hone : (1 : ℝ) ∈ (fun q : E => ‖z - q‖) '' C :=
    hpre.Icc_subset ha hb ⟨le_of_lt h₁, le_of_lt h₂⟩
  obtain ⟨q, hq, hq1⟩ := hone
  exact h q hq hq1


end EuclideanFiveColor
end
end OAI
