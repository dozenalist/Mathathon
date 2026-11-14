/-
  Sector transition lemma for the k ≥ 7 counterexample (machine-checked).

  Machine-checks the analytic step of the construction
  "a proper measurable colouring whose cyclic locus accumulates":
  paper Definition 6.1 (the transition graph) and the sector transition lemma.
-/
import Mathlib.MeasureTheory.Measure.Lebesgue.Complex
import Mathlib.Order.LiminfLimsup

open MeasureTheory Filter Topology Set
open scoped ENNReal

namespace SectorGadget

variable {k : ℕ}

/-! ## 1. The transition data of the paper (Definition 6.1) -/

/-- The transition set of the pair `(i,j)` at centre `x`, radius `R` and shift `h`. -/
def transitionSet (c : ℂ → Fin k) (i j : Fin k) (x : ℂ) (R : ℝ) (h : ℂ) : Set ℂ :=
  {q | q ∈ Metric.ball x R ∧ ((c q = i ∧ c (q + h) = j) ∨ (c q = j ∧ c (q + h) = i))}

/-- The transition ratio `|D_ij(x,R,h)| / |h|`. -/
noncomputable def transitionRatio (c : ℂ → Fin k) (i j : Fin k) (x : ℂ) (R : ℝ)
    (h : ℂ) : ℝ≥0∞ :=
  volume (transitionSet c i j x R h) / ENNReal.ofReal ‖h‖

/-- `(i,j)` is an edge of the transition graph at `x`. -/
def TransitionEdge (c : ℂ → Fin k) (i j : Fin k) (x : ℂ) : Prop :=
  i ≠ j ∧ ∀ R : ℝ, 0 < R → 0 < limsup (transitionRatio c i j x R) (𝓝[≠] (0 : ℂ))

lemma transitionSet_symm (c : ℂ → Fin k) (i j : Fin k) (x : ℂ) (R : ℝ) (h : ℂ) :
    transitionSet c j i x R h = transitionSet c i j x R h := by
  ext q
  simp only [transitionSet, Set.mem_setOf_eq]
  tauto

lemma transitionRatio_symm (c : ℂ → Fin k) (i j : Fin k) (x : ℂ) (R : ℝ) :
    transitionRatio c j i x R = transitionRatio c i j x R := by
  funext h
  simp only [transitionRatio, transitionSet_symm]

lemma TransitionEdge.symm {c : ℂ → Fin k} {i j : Fin k} {x : ℂ}
    (h : TransitionEdge c i j x) : TransitionEdge c j i x := by
  obtain ⟨hne, hpos⟩ := h
  refine ⟨hne.symm, fun R hR => ?_⟩
  rw [transitionRatio_symm]
  exact hpos R hR

/-! ## 2. Areas of axis-parallel rectangles in `ℂ` -/

lemma volume_rect {a b c d : ℝ} (hab : a ≤ b) (hcd : c ≤ d) :
    volume {z : ℂ | a < z.re ∧ z.re < b ∧ c < z.im ∧ z.im < d}
      = ENNReal.ofReal ((b - a) * (d - c)) := by
  have hset : {z : ℂ | a < z.re ∧ z.re < b ∧ c < z.im ∧ z.im < d}
      = Complex.measurableEquivRealProd ⁻¹' (Set.Ioo a b ×ˢ Set.Ioo c d) := by
    ext z
    simp only [Set.mem_setOf_eq, Set.mem_preimage, Set.mem_prod, Set.mem_Ioo,
      Complex.measurableEquivRealProd]
    tauto
  rw [hset, Complex.volume_preserving_equiv_real_prod.measure_preimage_equiv]
  change volume.prod volume (Set.Ioo a b ×ˢ Set.Ioo c d) = ENNReal.ofReal ((b - a) * (d - c))
  rw [Measure.prod_prod, Real.volume_Ioo, Real.volume_Ioo,
    ← ENNReal.ofReal_mul (sub_nonneg.2 hab)]

lemma volume_rect_shift (x : ℂ) {a b c d : ℝ} (hab : a ≤ b) (hcd : c ≤ d) :
    volume {q : ℂ | a < (q - x).re ∧ (q - x).re < b ∧ c < (q - x).im ∧ (q - x).im < d}
      = ENNReal.ofReal ((b - a) * (d - c)) := by
  have hset : {q : ℂ | a < (q - x).re ∧ (q - x).re < b ∧ c < (q - x).im ∧ (q - x).im < d}
      = {q : ℂ | x.re + a < q.re ∧ q.re < x.re + b ∧ x.im + c < q.im ∧ q.im < x.im + d} := by
    ext q
    simp only [Complex.sub_re, Complex.sub_im, Set.mem_setOf_eq]
    constructor
    · rintro ⟨h1, h2, h3, h4⟩; exact ⟨by linarith, by linarith, by linarith, by linarith⟩
    · rintro ⟨h1, h2, h3, h4⟩; exact ⟨by linarith, by linarith, by linarith, by linarith⟩
  rw [hset, volume_rect (by linarith) (by linarith)]
  congr 1
  ring

/-- Area of a rectangle in the coordinates `(s * re, im)` relative to `x`, for `s = ±1`. -/
lemma volume_rect_smul (x : ℂ) {s : ℝ} (hs : s = 1 ∨ s = -1) {a b c d : ℝ}
    (hab : a ≤ b) (hcd : c ≤ d) :
    volume {q : ℂ | s * (q - x).re ∈ Set.Ioo a b ∧ (q - x).im ∈ Set.Ioo c d}
      = ENNReal.ofReal ((b - a) * (d - c)) := by
  rcases hs with h | h
  · have hset2 : {q : ℂ | s * (q - x).re ∈ Set.Ioo a b ∧ (q - x).im ∈ Set.Ioo c d}
        = {q : ℂ | a < (q - x).re ∧ (q - x).re < b ∧ c < (q - x).im ∧
            (q - x).im < d} := by
      ext q; simp only [Set.mem_setOf_eq, Set.mem_Ioo, h, one_mul]; tauto
    rw [hset2]
    exact volume_rect_shift x hab hcd
  · have hset : {q : ℂ | s * (q - x).re ∈ Set.Ioo a b ∧ (q - x).im ∈ Set.Ioo c d}
        = {q : ℂ | -b < (q - x).re ∧ (q - x).re < -a ∧ c < (q - x).im ∧
            (q - x).im < d} := by
      ext q
      simp only [Set.mem_setOf_eq, Set.mem_Ioo, h, neg_one_mul]
      constructor
      · rintro ⟨⟨h1, h2⟩, h3, h4⟩; exact ⟨by linarith, by linarith, h3, h4⟩
      · rintro ⟨h1, h2, h3, h4⟩; exact ⟨⟨by linarith, by linarith⟩, h3, h4⟩
    rw [hset, volume_rect_shift x (by linarith) hcd]
    congr 1
    ring

/-! ## 3. The sector transition lemma -/

/-- **Sector transition lemma, horizontal interface.**

Suppose that inside `B(x,ρ)` the colouring equals `i` strictly above the horizontal line
through `x`, and equals `j` strictly below that line on one chosen side (`s = 1`: the right
side, `s = -1`: the left side). Then `(i,j)` is an edge of the transition graph at `x`. -/
theorem transitionEdge_of_horizontal {c : ℂ → Fin k} {x : ℂ} {ρ : ℝ} (hρ : 0 < ρ)
    {i j : Fin k} (hij : i ≠ j) (s : ℝ) (hs : s = 1 ∨ s = -1)
    (hi : ∀ q : ℂ, ‖q - x‖ < ρ → 0 < (q - x).im → c q = i)
    (hj : ∀ q : ℂ, ‖q - x‖ < ρ → (q - x).im < 0 → 0 < s * (q - x).re → c q = j) :
    TransitionEdge c i j x := by
  have habs : |s| = 1 := by rcases hs with h | h <;> simp [h]
  refine ⟨hij, fun R hR => ?_⟩
  set r : ℝ := min R ρ with hr
  have hr0 : 0 < r := lt_min hR hρ
  have hrR : r ≤ R := min_le_left _ _
  have hrρ : r ≤ ρ := min_le_right _ _
  have hr4 : (0:ℝ) < r/4 := by linarith
  have key : ∀ τ : ℝ, 0 < τ → τ ≤ r/8 →
      ENNReal.ofReal (r/4) ≤ transitionRatio c i j x R ((τ : ℂ) * Complex.I) := by
    intro τ hτ hτr
    set S : Set ℂ := {q : ℂ | s * (q - x).re ∈ Set.Ioo (r/4) (r/2) ∧
      (q - x).im ∈ Set.Ioo (-τ) 0} with hS
    have hsub : S ⊆ transitionSet c i j x R ((τ : ℂ) * Complex.I) := by
      intro q hq
      obtain ⟨⟨h1a, h1b⟩, h3, h4⟩ := hq
      have hspos : 0 < s * (q - x).re := by linarith
      have him : (q - x).im < 0 := h4
      have habs_re : |(q - x).re| < r/2 := by
        have h2 : |s * (q - x).re| = |(q - x).re| := by rw [abs_mul, habs, one_mul]
        rw [← h2, abs_lt]
        exact ⟨by linarith, by linarith⟩
      have him_abs : |(q - x).im| < τ := by rw [abs_lt]; constructor <;> linarith
      have hsq : ‖q - x‖ ^ 2 = (q - x).re ^ 2 + (q - x).im ^ 2 := by
        rw [Complex.sq_norm, Complex.normSq_apply]; ring
      have hnorm : ‖q - x‖ < r := by
        have h1' : (q - x).re ^ 2 < (r/2) ^ 2 := by nlinarith [abs_lt.mp habs_re]
        have h4' : (q - x).im ^ 2 < (r/8) ^ 2 := by nlinarith [abs_lt.mp him_abs, hτr]
        nlinarith [hr0]
      have hmemR : q ∈ Metric.ball x R := by
        rw [Metric.mem_ball, Complex.dist_eq]; linarith
      have hmemρ : ‖q - x‖ < ρ := by linarith
      have hshift_im : ((q + (τ : ℂ) * Complex.I) - x).im = (q - x).im + τ := by
        simp only [Complex.sub_im, Complex.add_im, Complex.mul_im, Complex.mul_re,
          Complex.ofReal_im, Complex.ofReal_re, Complex.I_re, Complex.I_im]
        ring
      have hshift_norm : ‖(q + (τ : ℂ) * Complex.I) - x‖ < ρ := by
        have h1 : ‖(q + (τ : ℂ) * Complex.I) - x‖ ≤ ‖q - x‖ + ‖(τ : ℂ) * Complex.I‖ := by
          calc ‖(q + (τ : ℂ) * Complex.I) - x‖ = ‖(q - x) + (τ : ℂ) * Complex.I‖ := by ring_nf
            _ ≤ ‖q - x‖ + ‖(τ : ℂ) * Complex.I‖ := norm_add_le _ _
        have h2 : ‖(τ : ℂ) * Complex.I‖ = τ := by
          rw [Complex.norm_mul, Complex.norm_I, mul_one, Complex.norm_real, Real.norm_eq_abs,
            abs_of_pos hτ]
        rw [h2] at h1
        have h4 : ‖q - x‖ < r / 2 + r / 8 := by
          have h1' : (q - x).re ^ 2 < (r/2) ^ 2 := by nlinarith [abs_lt.mp habs_re]
          have h3' : (q - x).im ^ 2 < (r/8) ^ 2 := by nlinarith [abs_lt.mp him_abs, hτr]
          nlinarith [norm_nonneg (q - x), hr0]
        nlinarith [hrρ]
      refine ⟨hmemR, Or.inr ⟨hj q hmemρ him hspos, hi _ hshift_norm ?_⟩⟩
      rw [hshift_im]; linarith
    have hvol : ENNReal.ofReal (r/4) * ENNReal.ofReal τ ≤
        volume (transitionSet c i j x R ((τ : ℂ) * Complex.I)) := by
      have hS' : volume S = ENNReal.ofReal (r/4) * ENNReal.ofReal τ := by
        rw [volume_rect_smul x hs (by linarith) (by linarith), ← ENNReal.ofReal_mul hr4.le]
        congr 1
        ring
      rw [← hS']
      exact measure_mono hsub
    have hnormh : (ENNReal.ofReal ‖(τ : ℂ) * Complex.I‖ : ℝ≥0∞) = ENNReal.ofReal τ := by
      rw [Complex.norm_mul, Complex.norm_I, mul_one, Complex.norm_real, Real.norm_eq_abs,
        abs_of_pos hτ]
    rw [transitionRatio, hnormh]
    rw [ENNReal.le_div_iff_mul_le (Or.inl (ENNReal.ofReal_pos.mpr hτ).ne')
      (Or.inl ENNReal.ofReal_ne_top)]
    exact hvol
  have hfreq : ∃ᶠ h in 𝓝[≠] (0 : ℂ),
      ENNReal.ofReal (r/4) ≤ transitionRatio c i j x R h := by
    rw [Filter.frequently_iff]
    intro t ht
    obtain ⟨ε, hε, hsub⟩ := Metric.mem_nhdsWithin_iff.mp ht
    set τ : ℝ := min ε (r/8) / 2 with hτdef
    have hτ0 : 0 < τ := by
      rw [hτdef]; have := lt_min hε (by linarith : (0:ℝ) < r/8); linarith
    have hτε : τ < ε := by
      have := min_le_left ε (r/8); rw [hτdef]; linarith
    have hτr : τ ≤ r/8 := by
      have := min_le_right ε (r/8); rw [hτdef]; linarith
    refine ⟨(τ : ℂ) * Complex.I, ?_, key τ hτ0 hτr⟩
    refine hsub ⟨?_, ?_⟩
    · rw [Metric.mem_ball, Complex.dist_eq, sub_zero, Complex.norm_mul, Complex.norm_I,
        mul_one, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hτ0]
      exact hτε
    · simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
      intro h0
      have h1 : ((τ : ℂ) * Complex.I).im = ((0 : ℂ)).im := by rw [h0]
      simp at h1
      linarith
  exact lt_of_lt_of_le (ENNReal.ofReal_pos.mpr hr4) (le_limsup_of_frequently_le hfreq)

/-- **Sector transition lemma, vertical interface.**

Inside `B(x,ρ)`: label `i` on the right of the vertical line through `x` below the horizontal
line, label `j` on the left of that line below it. Then `(i,j)` is an edge of the transition
graph at `x` (the shift is taken along the negative real axis). -/
theorem transitionEdge_of_vertical {c : ℂ → Fin k} {x : ℂ} {ρ : ℝ} (hρ : 0 < ρ)
    {i j : Fin k} (hij : i ≠ j)
    (hi : ∀ q : ℂ, ‖q - x‖ < ρ → 0 < (q - x).re → (q - x).im < 0 → c q = i)
    (hj : ∀ q : ℂ, ‖q - x‖ < ρ → (q - x).re < 0 → (q - x).im < 0 → c q = j) :
    TransitionEdge c i j x := by
  refine ⟨hij, fun R hR => ?_⟩
  set r : ℝ := min R ρ with hr
  have hr0 : 0 < r := lt_min hR hρ
  have hrR : r ≤ R := min_le_left _ _
  have hrρ : r ≤ ρ := min_le_right _ _
  have hr4 : (0:ℝ) < r/4 := by linarith
  have key : ∀ τ : ℝ, 0 < τ → τ ≤ r/8 →
      ENNReal.ofReal (r/4) ≤ transitionRatio c i j x R (-(τ : ℂ)) := by
    intro τ hτ hτr
    set S : Set ℂ := {q : ℂ | (q - x).re ∈ Set.Ioo (0:ℝ) τ ∧
      (q - x).im ∈ Set.Ioo (-(r/2)) (-(r/4))} with hS
    have hsub : S ⊆ transitionSet c i j x R (-(τ : ℂ)) := by
      intro q hq
      obtain ⟨⟨h1a, h1b⟩, h3, h4⟩ := hq
      have hre : 0 < (q - x).re := h1a
      have him : (q - x).im < 0 := by linarith
      have hre2 : (q - x).re ^ 2 < (r/8) ^ 2 := by nlinarith [h1b, hτr, hτ]
      have him_abs : |(q - x).im| < r/2 := by rw [abs_lt]; constructor <;> linarith
      have him2 : (q - x).im ^ 2 < (r/2) ^ 2 := by nlinarith [abs_lt.mp him_abs]
      have hsq : ‖q - x‖ ^ 2 = (q - x).re ^ 2 + (q - x).im ^ 2 := by
        rw [Complex.sq_norm, Complex.normSq_apply]; ring
      have hnorm : ‖q - x‖ < r := by nlinarith [hr0]
      have hmemR : q ∈ Metric.ball x R := by
        rw [Metric.mem_ball, Complex.dist_eq]; linarith
      have hmemρ : ‖q - x‖ < ρ := by linarith
      have hshift_re : ((q + -(τ : ℂ)) - x).re = (q - x).re - τ := by
        simp only [Complex.sub_re, Complex.add_re, Complex.neg_re, Complex.ofReal_re]
        ring
      have hshift_im : ((q + -(τ : ℂ)) - x).im = (q - x).im := by
        simp [Complex.sub_im, Complex.add_im]
      have hnormsq : ‖q - x‖ ^ 2 = (q - x).re ^ 2 + (q - x).im ^ 2 := hsq
      have hshift_norm : ‖(q + -(τ : ℂ)) - x‖ < ρ := by
        have h1 : ‖(q + -(τ : ℂ)) - x‖ ≤ ‖q - x‖ + ‖-(τ : ℂ)‖ := by
          calc ‖(q + -(τ : ℂ)) - x‖ = ‖(q - x) + -(τ : ℂ)‖ := by ring_nf
            _ ≤ ‖q - x‖ + ‖-(τ : ℂ)‖ := norm_add_le _ _
        have h2 : ‖-(τ : ℂ)‖ = τ := by
          rw [norm_neg, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hτ]
        rw [h2] at h1
        have h4 : ‖q - x‖ < r / 8 + r / 2 := by
          have h1' : (q - x).re ^ 2 < (r/8) ^ 2 := hre2
          have h3' : (q - x).im ^ 2 < (r/2) ^ 2 := him2
          nlinarith [norm_nonneg (q - x), hr0]
        linarith
      refine ⟨hmemR, Or.inl ⟨hi q hmemρ hre him, hj _ hshift_norm ?_ ?_⟩⟩
      · rw [hshift_re]; linarith
      · rw [hshift_im]; exact him
    have hvol : ENNReal.ofReal (r/4) * ENNReal.ofReal τ ≤
        volume (transitionSet c i j x R (-(τ : ℂ))) := by
      have hS' : volume S = ENNReal.ofReal (r/4) * ENNReal.ofReal τ := by
        have hset : S = {q : ℂ | 0 < (q - x).re ∧ (q - x).re < τ ∧ -(r/2) < (q - x).im ∧
            (q - x).im < -(r/4)} := by
          ext q; simp only [hS, Set.mem_setOf_eq, Set.mem_Ioo]; tauto
        rw [hset, volume_rect_shift x (by linarith) (by linarith),
          ← ENNReal.ofReal_mul hr4.le]
        congr 1
        ring
      rw [← hS']
      exact measure_mono hsub
    have hnormh : (ENNReal.ofReal ‖(-(τ : ℂ))‖ : ℝ≥0∞) = ENNReal.ofReal τ := by
      rw [norm_neg, Complex.norm_real, Real.norm_eq_abs, abs_of_pos hτ]
    rw [transitionRatio, hnormh]
    rw [ENNReal.le_div_iff_mul_le (Or.inl (ENNReal.ofReal_pos.mpr hτ).ne')
      (Or.inl ENNReal.ofReal_ne_top)]
    exact hvol
  have hfreq : ∃ᶠ h in 𝓝[≠] (0 : ℂ),
      ENNReal.ofReal (r/4) ≤ transitionRatio c i j x R h := by
    rw [Filter.frequently_iff]
    intro t ht
    obtain ⟨ε, hε, hsub⟩ := Metric.mem_nhdsWithin_iff.mp ht
    set τ : ℝ := min ε (r/8) / 2 with hτdef
    have hτ0 : 0 < τ := by
      rw [hτdef]; have := lt_min hε (by linarith : (0:ℝ) < r/8); linarith
    have hτε : τ < ε := by
      have := min_le_left ε (r/8); rw [hτdef]; linarith
    have hτr : τ ≤ r/8 := by
      have := min_le_right ε (r/8); rw [hτdef]; linarith
    refine ⟨-(τ : ℂ), ?_, key τ hτ0 hτr⟩
    refine hsub ⟨?_, ?_⟩
    · rw [Metric.mem_ball, Complex.dist_eq, sub_zero, norm_neg, Complex.norm_real,
        Real.norm_eq_abs, abs_of_pos hτ0]
      exact hτε
    · simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
      intro h0
      have h1 : ((-(τ : ℂ))).re = ((0 : ℂ)).re := by rw [h0]
      simp at h1
      linarith
  exact lt_of_lt_of_le (ENNReal.ofReal_pos.mpr hr4) (le_limsup_of_frequently_le hfreq)

/-! ## 4. The three-sector (Y) gadget -/

/-- The Y gadget about the point `x`: label `0` above the horizontal line through `x`,
label `2` on the lower right, label `3` on the lower left. -/
noncomputable def ySector (x : ℂ) : ℂ → Fin 7 :=
  fun q => if x.im < q.im then 0 else if x.re < q.re then 2 else 3

/-- Insert the Y gadget in the open disk of radius `ρ` about `x`. -/
noncomputable def graft (g : ℂ → Fin 7) (x : ℂ) (ρ : ℝ) : ℂ → Fin 7 :=
  fun q => if ‖q - x‖ < ρ then ySector x q else g q

lemma edge_0_2 {g : ℂ → Fin 7} {x : ℂ} {ρ : ℝ} (hρ : 0 < ρ) :
    TransitionEdge (graft g x ρ) 0 2 x := by
  have hi : ∀ q : ℂ, ‖q - x‖ < ρ → 0 < (q - x).im → graft g x ρ q = 0 := by
    intro q hq him
    have him' : x.im < q.im := by simpa [Complex.sub_im] using him
    simp [graft, hq, ySector, him']
  have hj : ∀ q : ℂ, ‖q - x‖ < ρ → (q - x).im < 0 → 0 < 1 * (q - x).re →
      graft g x ρ q = 2 := by
    intro q hq him hre
    have hre' : 0 < (q - x).re := by linarith
    have hre'' : x.re < q.re := by simpa [Complex.sub_re] using hre'
    have him'' : ¬ (x.im < q.im) := by
      have : q.im < x.im := by simpa [Complex.sub_im] using him
      exact not_lt.mpr this.le
    simp [graft, hq, ySector, him'', hre'']
  exact transitionEdge_of_horizontal (k := 7) hρ (by decide) 1 (Or.inl rfl) hi hj

lemma edge_2_3 {g : ℂ → Fin 7} {x : ℂ} {ρ : ℝ} (hρ : 0 < ρ) :
    TransitionEdge (graft g x ρ) 2 3 x := by
  have hi : ∀ q : ℂ, ‖q - x‖ < ρ → 0 < (q - x).re → (q - x).im < 0 →
      graft g x ρ q = 2 := by
    intro q hq hre him
    have hre' : x.re < q.re := by simpa [Complex.sub_re] using hre
    have him' : ¬ (x.im < q.im) := by
      have : q.im < x.im := by simpa [Complex.sub_im] using him
      exact not_lt.mpr this.le
    simp [graft, hq, ySector, him', hre']
  have hj : ∀ q : ℂ, ‖q - x‖ < ρ → (q - x).re < 0 → (q - x).im < 0 →
      graft g x ρ q = 3 := by
    intro q hq hre him
    have hre' : ¬ (x.re < q.re) := by
      have : q.re < x.re := by simpa [Complex.sub_re] using hre
      exact not_lt.mpr this.le
    have him' : ¬ (x.im < q.im) := by
      have : q.im < x.im := by simpa [Complex.sub_im] using him
      exact not_lt.mpr this.le
    simp [graft, hq, ySector, him', hre']
  exact transitionEdge_of_vertical (k := 7) hρ (by decide) hi hj

lemma edge_0_3 {g : ℂ → Fin 7} {x : ℂ} {ρ : ℝ} (hρ : 0 < ρ) :
    TransitionEdge (graft g x ρ) 0 3 x := by
  have hi : ∀ q : ℂ, ‖q - x‖ < ρ → 0 < (q - x).im → graft g x ρ q = 0 := by
    intro q hq him
    have him' : x.im < q.im := by simpa [Complex.sub_im] using him
    simp [graft, hq, ySector, him']
  have hj : ∀ q : ℂ, ‖q - x‖ < ρ → (q - x).im < 0 → 0 < -1 * (q - x).re →
      graft g x ρ q = 3 := by
    intro q hq him hre
    have hre1 : (q - x).re < 0 := by linarith
    have hre' : ¬ (x.re < q.re) := by
      have : q.re < x.re := by simpa [Complex.sub_re] using hre1
      exact not_lt.mpr this.le
    have him' : ¬ (x.im < q.im) := by
      have : q.im < x.im := by simpa [Complex.sub_im] using him
      exact not_lt.mpr this.le
    simp [graft, hq, ySector, him', hre']
  exact transitionEdge_of_horizontal (k := 7) hρ (by decide) (-1) (Or.inr rfl) hi hj

/-- **A cyclic centre.** The Y gadget produces a triangle in the transition graph. -/
theorem triangle_of_graft {g : ℂ → Fin 7} {x : ℂ} {ρ : ℝ} (hρ : 0 < ρ) :
    TransitionEdge (graft g x ρ) 0 2 x ∧ TransitionEdge (graft g x ρ) 2 3 x ∧
      TransitionEdge (graft g x ρ) 0 3 x :=
  ⟨edge_0_2 hρ, edge_2_3 hρ, edge_0_3 hρ⟩

end SectorGadget
