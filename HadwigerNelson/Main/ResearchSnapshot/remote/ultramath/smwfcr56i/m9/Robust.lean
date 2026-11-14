/-
# Robustness of the lower bound `chi(R^2) >= 6` under deleting small sets

`no_proper_five_coloring` (paper Theorem 1.1, formalized in `OAI/.../Five.lean`) is combined
with the de Bruijn--Erdos compactness step `exists_properColoring_of_finset`
(`OAI/.../Converse.lean`) to prove:

  * `exists_translate_disjoint_null`: a finite point set has a translate avoiding any
    Lebesgue-null set;
  * `not_properColoring_off_null`: if the plane has no proper `k`-colouring then neither has
    `C \ Z` for every Lebesgue-null `Z`;
  * `no_five_coloring_off_null`: consequently `C \ Z` is not 5-colourable for every null `Z`.

Nothing here depends on the particular value `5`; the general statement is `k`-uniform.
-/
import OAI.Geometry.PlaneColoring.Five
import OAI.Geometry.PlaneColoring.Converse

namespace OAI

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace EuclideanFiveColor

/-- **Translate lemma, null case.**  A finite set of points can be translated off any
Lebesgue-null set: the set of bad translation vectors is a finite union of null sets. -/
theorem exists_translate_disjoint_null {F : Finset ℂ} {Z : Set ℂ} (hZ : volume Z = 0) :
    ∃ t : ℂ, ∀ w ∈ F, w + t ∉ Z := by
  classical
  -- the bad translation vectors for one point `w`
  set A : ℂ → Set ℂ := fun w => (fun t : ℂ => w + t) ⁻¹' Z with hA
  have hAnull : ∀ w, volume (A w) = 0 := by
    intro w
    have h : volume (A w) = volume Z := by
      rw [hA]
      exact measure_preimage_add volume w Z
    rw [h, hZ]
  -- finitely many bad vectors still form a null set
  have hU : volume (⋃ w ∈ (F : Set ℂ), A w) = 0 := by
    rw [measure_biUnion_null_iff (F.finite_toSet.countable)]
    intro w _
    exact hAnull w
  by_contra h
  have h' : ∀ t : ℂ, ∃ w ∈ F, w + t ∈ Z := by
    intro t
    by_contra hc
    exact h ⟨t, fun w hw hmem => hc ⟨w, hw, hmem⟩⟩
  -- every translation is bad, so the whole plane sits in the null set `U`
  have hsub : (Set.univ : Set ℂ) ⊆ ⋃ w ∈ (F : Set ℂ), A w := by
    intro t _
    obtain ⟨w, hw, hwt⟩ := h' t
    exact Set.mem_iUnion₂.mpr ⟨w, hw, hwt⟩
  have hzero : volume (Set.univ : Set ℂ) = 0 := measure_mono_null hsub hU
  have hpos : volume (Metric.ball (0 : ℂ) 1) ≠ 0 :=
    (Metric.measure_ball_pos volume 0 one_pos).ne'
  exact hpos (measure_mono_null (Set.subset_univ _) hzero)

/-- **Key step.**  If `C \ Z` has a proper `k`-colouring, `Z` being null, then every finite
configuration of points is `k`-colourable: translate it into `C \ Z` and pull back. -/
theorem finite_colorable_of_colorable_off_null {k : ℕ} [NeZero k] {Z : Set ℂ} (hZ : volume Z = 0)
    {c : {z : ℂ // z ∉ Z} → Fin k}
    (hc : ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y) :
    ∀ F : Finset ℂ, ∃ d : ℂ → Fin k, ∀ x ∈ F, ∀ y ∈ F, ‖x - y‖ = 1 → d x ≠ d y := by
  intro F
  classical
  obtain ⟨t, ht⟩ := exists_translate_disjoint_null (F := F) hZ
  refine ⟨fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0, ?_⟩
  intro x hx y hy hxy
  have hx' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) x
      = c ⟨x + t, ht x hx⟩ := dite_eq_left hx
  have hy' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) y
      = c ⟨y + t, ht y hy⟩ := dite_eq_left hy
  rw [hx', hy']
  exact hc ⟨x + t, ht x hx⟩ ⟨y + t, ht y hy⟩ (by simpa using hxy)

/-- **Robustness, null case, arbitrary `k`.**  If the plane has no proper `k`-colouring, then
`C \ Z` has none, for every Lebesgue-null `Z`. -/
theorem not_properColoring_off_null {k : ℕ} [NeZero k] {Z : Set ℂ} (hZ : volume Z = 0)
    (h : ¬ ∃ c : ℂ → Fin k, ProperColoring k c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin k,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
  exact h (exists_properColoring_of_finset (finite_colorable_of_colorable_off_null hZ hc))

/-- **Five colours survive the deletion of any null set.**  `C \ Z` is not 5-colourable for
every Lebesgue-null `Z`; with the hexagonal 7-colouring its chromatic number is therefore `6`
or `7`. -/
theorem no_five_coloring_off_null (Z : Set ℂ) (hZ : volume Z = 0) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin 5,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y :=
  not_properColoring_off_null hZ no_proper_five_coloring

/-- Special case: deleting a single point does not make the plane 5-colourable. -/
theorem no_five_coloring_off_singleton (p : ℂ) :
    ¬ ∃ c : {z : ℂ // z ≠ p} → Fin 5,
      ∀ x y : {z : ℂ // z ≠ p}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  refine no_five_coloring_off_null {p} ?_
  simp

end EuclideanFiveColor

end

end OAI

namespace OAI

noncomputable section

open MeasureTheory

namespace EuclideanFiveColor

/-! ### Meagre case -/

/-- **Translate lemma, meagre case.** -/
theorem exists_translate_disjoint_isMeagre {F : Finset ℂ} {Z : Set ℂ} (hZ : IsMeagre Z) :
    ∃ t : ℂ, ∀ w ∈ F, w + t ∉ Z := by
  classical
  set A : ℂ → Set ℂ := fun w => (fun t : ℂ => w + t) ⁻¹' Z with hA
  have hAme : ∀ w, IsMeagre (A w) := by
    intro w
    rw [hA]
    exact IsMeagre.preimage_of_isOpenMap (f := fun t : ℂ => w + t)
      (continuous_const.add continuous_id) (isOpenMap_add_left w) hZ
  have hU : IsMeagre (⋃ w ∈ (F : Set ℂ), A w) := by
    induction F using Finset.induction_on with
    | empty => simpa using (IsMeagre.empty : IsMeagre (∅ : Set ℂ))
    | insert a s ha ih =>
        rw [Finset.coe_insert, Set.biUnion_insert]
        exact (hAme a).union ih
  by_contra h
  have h' : ∀ t : ℂ, ∃ w ∈ F, w + t ∈ Z := by
    intro t
    by_contra hc
    exact h ⟨t, fun w hw hmem => hc ⟨w, hw, hmem⟩⟩
  have hsub : (Set.univ : Set ℂ) ⊆ ⋃ w ∈ (F : Set ℂ), A w := by
    intro t _
    obtain ⟨w, hw, hwt⟩ := h' t
    exact Set.mem_iUnion₂.mpr ⟨w, hw, hwt⟩
  exact not_isMeagre_of_isOpen isOpen_univ Set.univ_nonempty (hU.mono hsub)

/-- **Translate lemma, countable case** (a special case of cardinality `< continuum`). -/
theorem exists_translate_disjoint_countable {F : Finset ℂ} {Z : Set ℂ} (hZ : Z.Countable) :
    ∃ t : ℂ, ∀ w ∈ F, w + t ∉ Z := by
  classical
  set A : ℂ → Set ℂ := fun w => (fun t : ℂ => w + t) ⁻¹' Z with hA
  have hpre : ∀ w : ℂ, (fun t : ℂ => w + t) ⁻¹' Z = (fun z : ℂ => z - w) '' Z := by
    intro w
    ext t
    constructor
    · intro ht
      exact ⟨w + t, ht, by ring⟩
    · rintro ⟨z, hz, rfl⟩
      simpa using hz
  have hAc : ∀ w, (A w).Countable := by
    intro w
    rw [hA]
    change ((fun t : ℂ => w + t) ⁻¹' Z).Countable
    rw [hpre w]
    exact hZ.image _
  have hU : (⋃ w ∈ (F : Set ℂ), A w).Countable := by
    induction F using Finset.induction_on with
    | empty => simp
    | insert a s ha ih =>
        rw [Finset.coe_insert, Set.biUnion_insert]
        exact (hAc a).union ih
  by_contra h
  have h' : ∀ t : ℂ, ∃ w ∈ F, w + t ∈ Z := by
    intro t
    by_contra hc
    exact h ⟨t, fun w hw hmem => hc ⟨w, hw, hmem⟩⟩
  have hsub : (Set.univ : Set ℂ) ⊆ ⋃ w ∈ (F : Set ℂ), A w := by
    intro t _
    obtain ⟨w, hw, hwt⟩ := h' t
    exact Set.mem_iUnion₂.mpr ⟨w, hw, hwt⟩
  have huniv : (Set.univ : Set ℂ).Countable := hU.mono hsub
  have hmk : Cardinal.mk (Set.univ : Set ℂ) ≤ Cardinal.aleph0 :=
    Cardinal.mk_le_aleph0_iff.mpr huniv
  rw [Cardinal.mk_univ, Cardinal.mk_complex] at hmk
  exact absurd hmk (not_le.mpr Cardinal.aleph0_lt_continuum)

/-- **Translate lemma, half-plane case.**  Any set contained in a vertical closed half-plane
`{z : z.re ≤ c}` can be avoided by a translate of a finite set. -/
theorem exists_translate_disjoint_halfplane {F : Finset ℂ} {Z : Set ℂ} {c : ℝ}
    (hZ : ∀ z ∈ Z, z.re ≤ c) : ∃ t : ℂ, ∀ w ∈ F, w + t ∉ Z := by
  classical
  refine ⟨((c + (∑ w ∈ F, |w.re|) + 1 : ℝ) : ℂ), ?_⟩
  intro w hw hmem
  have h1 : (w + ((c + (∑ w ∈ F, |w.re|) + 1 : ℝ) : ℂ)).re ≤ c := hZ _ hmem
  rw [Complex.add_re, Complex.ofReal_re] at h1
  have h2 : |w.re| ≤ ∑ w ∈ F, |w.re| :=
    Finset.single_le_sum (fun i _ => abs_nonneg i.re) hw
  have h3 : -|w.re| ≤ w.re := neg_abs_le w.re
  linarith

/-! ### Robustness theorems -/

/-- **Robustness, meagre case.** -/
theorem not_properColoring_off_isMeagre {k : ℕ} [NeZero k] {Z : Set ℂ} (hZ : IsMeagre Z)
    (h : ¬ ∃ c : ℂ → Fin k, ProperColoring k c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin k,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
  refine h (exists_properColoring_of_finset ?_)
  intro F
  classical
  obtain ⟨t, ht⟩ := exists_translate_disjoint_isMeagre (F := F) hZ
  refine ⟨fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0, ?_⟩
  intro x hx y hy hxy
  have hx' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) x
      = c ⟨x + t, ht x hx⟩ := dite_eq_left hx
  have hy' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) y
      = c ⟨y + t, ht y hy⟩ := dite_eq_left hy
  rw [hx', hy']
  exact hc ⟨x + t, ht x hx⟩ ⟨y + t, ht y hy⟩ (by simpa using hxy)

/-- **Robustness, countable case.** -/
theorem not_properColoring_off_countable {k : ℕ} [NeZero k] {Z : Set ℂ} (hZ : Z.Countable)
    (h : ¬ ∃ c : ℂ → Fin k, ProperColoring k c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin k,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
  refine h (exists_properColoring_of_finset ?_)
  intro F
  classical
  obtain ⟨t, ht⟩ := exists_translate_disjoint_countable (F := F) hZ
  refine ⟨fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0, ?_⟩
  intro x hx y hy hxy
  have hx' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) x
      = c ⟨x + t, ht x hx⟩ := dite_eq_left hx
  have hy' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) y
      = c ⟨y + t, ht y hy⟩ := dite_eq_left hy
  rw [hx', hy']
  exact hc ⟨x + t, ht x hx⟩ ⟨y + t, ht y hy⟩ (by simpa using hxy)

/-- **Robustness, half-plane case.** -/
theorem not_properColoring_off_halfplane {k : ℕ} [NeZero k] {Z : Set ℂ} {c : ℝ}
    (hZ : ∀ z ∈ Z, z.re ≤ c) (h : ¬ ∃ c : ℂ → Fin k, ProperColoring k c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin k,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
  refine h (exists_properColoring_of_finset ?_)
  intro F
  classical
  obtain ⟨t, ht⟩ := exists_translate_disjoint_halfplane (F := F) hZ
  refine ⟨fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0, ?_⟩
  intro x hx y hy hxy
  have hx' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) x
      = c ⟨x + t, ht x hx⟩ := dite_eq_left hx
  have hy' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) y
      = c ⟨y + t, ht y hy⟩ := dite_eq_left hy
  rw [hx', hy']
  exact hc ⟨x + t, ht x hx⟩ ⟨y + t, ht y hy⟩ (by simpa using hxy)

/-- **Corollaries at five colours.** -/
theorem no_five_coloring_off_isMeagre (Z : Set ℂ) (hZ : IsMeagre Z) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin 5,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y :=
  not_properColoring_off_isMeagre hZ no_proper_five_coloring

theorem no_five_coloring_off_countable (Z : Set ℂ) (hZ : Z.Countable) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin 5,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y :=
  not_properColoring_off_countable hZ no_proper_five_coloring

theorem no_five_coloring_off_halfplane (Z : Set ℂ) {c : ℝ} (hZ : ∀ z ∈ Z, z.re ≤ c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin 5,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y :=
  not_properColoring_off_halfplane hZ no_proper_five_coloring

end EuclideanFiveColor

end

end OAI

namespace OAI

noncomputable section

open MeasureTheory

namespace EuclideanFiveColor

/-! ### Finite outer measure case -/

/-- The plane has infinite Lebesgue measure (via the explicit area of balls). -/
theorem volume_univ_complex : volume (Set.univ : Set ℂ) = ⊤ := by
  by_contra h
  set y : ℝ := (volume (Set.univ : Set ℂ)).toReal with hy
  have hof : ENNReal.ofReal y = volume (Set.univ : Set ℂ) := ENNReal.ofReal_toReal h
  have hπ1 : (1 : ℝ) ≤ Real.pi := le_of_lt (by linarith [Real.pi_gt_three])
  have hlt : y < (y + 1) ^ 2 * Real.pi := by
    have h1 : y < (y + 1) ^ 2 := by nlinarith [sq_nonneg (y + 1)]
    have h2 : (y + 1) ^ 2 ≤ (y + 1) ^ 2 * Real.pi := by
      nlinarith [sq_nonneg (y + 1)]
    linarith
  have hR : 0 < (y + 1) ^ 2 * Real.pi := by positivity
  have hball : volume (Metric.ball (0 : ℂ) (y + 1))
      = ENNReal.ofReal ((y + 1) ^ 2 * Real.pi) := by
    rw [Complex.volume_ball, ← ENNReal.ofReal_pow (show (0:ℝ) ≤ y + 1 by positivity),
      ENNReal.coe_nnreal_eq, ← ENNReal.ofReal_mul (by positivity)]
    simp
  have h1 : ENNReal.ofReal y < volume (Metric.ball (0 : ℂ) (y + 1)) := by
    rw [hball]
    exact (ENNReal.ofReal_lt_ofReal_iff hR).mpr hlt
  rw [hof] at h1
  exact absurd h1 (not_lt.mpr (measure_mono (Set.subset_univ _)))

/-- **Translate lemma, finite outer measure case.** -/
theorem exists_translate_disjoint_finite {F : Finset ℂ} {Z : Set ℂ} (hZ : volume Z ≠ ⊤) :
    ∃ t : ℂ, ∀ w ∈ F, w + t ∉ Z := by
  classical
  set A : ℂ → Set ℂ := fun w => (fun t : ℂ => w + t) ⁻¹' Z with hA
  have hAn : ∀ w, volume (A w) = volume Z := by
    intro w
    rw [hA]
    exact measure_preimage_add volume w Z
  have hle : volume (⋃ w ∈ (F : Set ℂ), A w) ≤ ∑ w ∈ F, volume (A w) := by
    induction F using Finset.induction_on with
    | empty => simp
    | insert a s ha ih =>
        rw [Finset.coe_insert, Set.biUnion_insert, Finset.sum_insert ha]
        exact le_trans (measure_union_le _ _) (add_le_add_right ih _)
  have hsum : ∑ w ∈ F, volume (A w) = (F.card : ENNReal) * volume Z := by
    simp only [hAn, Finset.sum_const, nsmul_eq_mul]
  have hne : (F.card : ENNReal) * volume Z ≠ ⊤ :=
    ENNReal.mul_ne_top (ENNReal.natCast_ne_top _) hZ
  have hUfin : volume (⋃ w ∈ (F : Set ℂ), A w) < ⊤ := by
    refine lt_of_le_of_lt hle ?_
    rw [hsum]
    exact lt_top_iff_ne_top.mpr hne
  by_contra h
  have h' : ∀ t : ℂ, ∃ w ∈ F, w + t ∈ Z := by
    intro t
    by_contra hc
    exact h ⟨t, fun w hw hmem => hc ⟨w, hw, hmem⟩⟩
  have hsub : (Set.univ : Set ℂ) ⊆ ⋃ w ∈ (F : Set ℂ), A w := by
    intro t _
    obtain ⟨w, hw, hwt⟩ := h' t
    exact Set.mem_iUnion₂.mpr ⟨w, hw, hwt⟩
  have htop : volume (Set.univ : Set ℂ) < ⊤ := lt_of_le_of_lt (measure_mono hsub) hUfin
  rw [volume_univ_complex] at htop
  exact absurd htop (lt_irrefl (⊤ : ENNReal))

/-- **Robustness, finite outer measure case.** -/
theorem not_properColoring_off_finite {k : ℕ} [NeZero k] {Z : Set ℂ} (hZ : volume Z ≠ ⊤)
    (h : ¬ ∃ c : ℂ → Fin k, ProperColoring k c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin k,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
  refine h (exists_properColoring_of_finset ?_)
  intro F
  classical
  obtain ⟨t, ht⟩ := exists_translate_disjoint_finite (F := F) hZ
  refine ⟨fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0, ?_⟩
  intro x hx y hy hxy
  have hx' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) x
      = c ⟨x + t, ht x hx⟩ := dite_eq_left hx
  have hy' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) y
      = c ⟨y + t, ht y hy⟩ := dite_eq_left hy
  rw [hx', hy']
  exact hc ⟨x + t, ht x hx⟩ ⟨y + t, ht y hy⟩ (by simpa using hxy)

/-- **Five colours survive the deletion of any set of finite outer measure.** -/
theorem no_five_coloring_off_finite (Z : Set ℂ) (hZ : volume Z ≠ ⊤) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin 5,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y :=
  not_properColoring_off_finite hZ no_proper_five_coloring

end EuclideanFiveColor

end

end OAI

namespace OAI

noncomputable section

open MeasureTheory

namespace EuclideanFiveColor

/-- **Refinement of the translate lemma.**  For a null `Z` and any set `A` of positive outer
measure, the good translation vectors meet `A`: the whole plane cannot be a finite union of
translates of `Z`.  (So the witness can be placed "where one likes", up to positive measure.) -/
theorem exists_translate_disjoint_null_mem {F : Finset ℂ} {Z : Set ℂ} (hZ : volume Z = 0)
    {A : Set ℂ} (hA : volume A ≠ 0) :
    ∃ t ∈ A, ∀ w ∈ F, w + t ∉ Z := by
  classical
  set B : Set ℂ := ⋃ w ∈ (F : Set ℂ), (fun t : ℂ => w + t) ⁻¹' Z with hB
  have hBnull : volume B = 0 := by
    rw [hB, measure_biUnion_null_iff (F.finite_toSet.countable)]
    intro w _
    have h : volume ((fun t : ℂ => w + t) ⁻¹' Z) = volume Z := measure_preimage_add volume w Z
    rw [h, hZ]
  by_contra h
  push Not at h
  have hsub : A ⊆ B := by
    intro t ht
    obtain ⟨w, hw, hmem⟩ := h t ht
    exact Set.mem_iUnion₂.mpr ⟨w, hw, hmem⟩
  have hzero : volume A = 0 :=
    le_antisymm (le_of_le_of_eq (measure_mono hsub) hBnull) (zero_le : (0 : ENNReal) ≤ volume A)
  exact hA hzero

end EuclideanFiveColor

end

end OAI

namespace OAI

noncomputable section

open MeasureTheory

namespace EuclideanFiveColor

/-! ### Cardinality case -/

/-- **Translate lemma, cardinality case.**  A set of cardinality below the continuum can be
avoided by a translate of any finite set: the bad translations are a finite union of copies of
`Z`, of cardinality `< c`. -/
theorem exists_translate_disjoint_card_lt {F : Finset ℂ} {Z : Set ℂ}
    (hZ : Cardinal.mk Z < Cardinal.continuum) : ∃ t : ℂ, ∀ w ∈ F, w + t ∉ Z := by
  classical
  have hpre : ∀ w : ℂ, (fun t : ℂ => w + t) ⁻¹' Z = (fun z : ℂ => z - w) '' Z := by
    intro w
    ext t
    constructor
    · intro ht
      exact ⟨w + t, ht, by ring⟩
    · rintro ⟨z, hz, rfl⟩
      simpa using hz
  set A : ℂ → Set ℂ := fun w => (fun t : ℂ => w + t) ⁻¹' Z with hA
  have hAle : ∀ w, Cardinal.mk (A w) ≤ Cardinal.mk Z := by
    intro w
    rw [hA]
    change Cardinal.mk ↥((fun t : ℂ => w + t) ⁻¹' Z) ≤ Cardinal.mk ↥Z
    rw [hpre w]
    exact Cardinal.mk_image_le
  -- union bound, by induction on the finite set
  have hUle : ∀ s : Finset ℂ, Cardinal.mk ↥(⋃ w ∈ (s : Set ℂ), A w)
      ≤ (s.card : Cardinal) * Cardinal.mk ↥Z := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp
    | insert a s ha ih =>
        rw [Finset.coe_insert, Set.biUnion_insert]
        calc Cardinal.mk ↥(A a ∪ ⋃ w ∈ (s : Set ℂ), A w)
            ≤ Cardinal.mk ↥(A a) + Cardinal.mk ↥(⋃ w ∈ (s : Set ℂ), A w) :=
              Cardinal.mk_union_le _ _
          _ ≤ Cardinal.mk ↥Z + (s.card : Cardinal) * Cardinal.mk ↥Z :=
              add_le_add (hAle a) ih
          _ = ((insert a s).card : Cardinal) * Cardinal.mk ↥Z := by
              rw [Finset.card_insert_of_notMem ha, Nat.cast_add, Nat.cast_one, add_mul,
                one_mul, add_comm]
  have hcard : (F.card : Cardinal) ≤ Cardinal.aleph0 := le_of_lt (Cardinal.natCast_lt_aleph0 (n := F.card))
  have hcont : Cardinal.aleph0 ≤ Cardinal.continuum := le_of_lt Cardinal.aleph0_lt_continuum
  have hlt : Cardinal.mk ↥(⋃ w ∈ (F : Set ℂ), A w) < Cardinal.continuum := by
    by_cases hfin : (Z : Set ℂ).Finite
    · have hAfin : ∀ w : ℂ, (A w).Finite := by
        intro w
        rw [hA]
        change ((fun t : ℂ => w + t) ⁻¹' Z).Finite
        rw [hpre w]
        exact hfin.image _
      have hUfin : (⋃ w ∈ (F : Set ℂ), A w).Finite :=
        F.finite_toSet.biUnion fun w _ => hAfin w
      exact lt_of_lt_of_le (Cardinal.lt_aleph0_iff_finite.mpr hUfin.to_subtype) hcont
    · have hI : Infinite ↥Z := Set.infinite_coe_iff.mpr hfin
      have hinf : Cardinal.aleph0 ≤ Cardinal.mk ↥Z := Cardinal.aleph0_le_mk ↥Z
      calc Cardinal.mk ↥(⋃ w ∈ (F : Set ℂ), A w)
          ≤ (F.card : Cardinal) * Cardinal.mk ↥Z := hUle F
        _ ≤ Cardinal.aleph0 * Cardinal.mk ↥Z := mul_le_mul' hcard le_rfl
        _ = Cardinal.mk ↥Z := Cardinal.aleph0_mul_eq hinf
        _ < Cardinal.continuum := hZ
  by_contra h
  have h' : ∀ t : ℂ, ∃ w ∈ F, w + t ∈ Z := by
    intro t
    by_contra hc
    exact h ⟨t, fun w hw hmem => hc ⟨w, hw, hmem⟩⟩
  have hsub : (Set.univ : Set ℂ) ⊆ ⋃ w ∈ (F : Set ℂ), A w := by
    intro t _
    obtain ⟨w, hw, hwt⟩ := h' t
    exact Set.mem_iUnion₂.mpr ⟨w, hw, hwt⟩
  have hmk : Cardinal.continuum ≤ Cardinal.mk ↥(⋃ w ∈ (F : Set ℂ), A w) := by
    calc Cardinal.continuum = Cardinal.mk (Set.univ : Set ℂ) := by
          rw [Cardinal.mk_univ, Cardinal.mk_complex]
      _ ≤ _ := Cardinal.mk_le_mk_of_subset hsub
  exact absurd hlt (not_lt.mpr hmk)

/-- **Robustness, cardinality case.** -/
theorem not_properColoring_off_card_lt {k : ℕ} [NeZero k] {Z : Set ℂ}
    (hZ : Cardinal.mk Z < Cardinal.continuum)
    (h : ¬ ∃ c : ℂ → Fin k, ProperColoring k c) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin k,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y := by
  rintro ⟨c, hc⟩
  refine h (exists_properColoring_of_finset ?_)
  intro F
  classical
  obtain ⟨t, ht⟩ := exists_translate_disjoint_card_lt (F := F) hZ
  refine ⟨fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0, ?_⟩
  intro x hx y hy hxy
  have hx' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) x
      = c ⟨x + t, ht x hx⟩ := dite_eq_left hx
  have hy' : (fun w => if hw : w ∈ F then c ⟨w + t, ht w hw⟩ else 0) y
      = c ⟨y + t, ht y hy⟩ := dite_eq_left hy
  rw [hx', hy']
  exact hc ⟨x + t, ht x hx⟩ ⟨y + t, ht y hy⟩ (by simpa using hxy)

/-- **Five colours survive the deletion of any set of cardinality below the continuum.** -/
theorem no_five_coloring_off_card_lt (Z : Set ℂ) (hZ : Cardinal.mk Z < Cardinal.continuum) :
    ¬ ∃ c : {z : ℂ // z ∉ Z} → Fin 5,
      ∀ x y : {z : ℂ // z ∉ Z}, ‖(x : ℂ) - (y : ℂ)‖ = 1 → c x ≠ c y :=
  not_properColoring_off_card_lt hZ no_proper_five_coloring

end EuclideanFiveColor

end

end OAI
