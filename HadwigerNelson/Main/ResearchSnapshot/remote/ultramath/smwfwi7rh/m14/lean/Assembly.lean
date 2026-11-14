/-
  Assembly: a proper 7-colouring whose triangle (cyclic) locus is not locally finite,
  given a background proper colouring whose unit-distance annulus around one point misses
  three labels.

  This machine-checks the logical skeleton of the k ≥ 7 counterexample:
  * properness of the modified colouring (the square has diameter < 1, the unit-distance
    shadow of the square lies in the annulus, and the annulus misses three labels);
  * each gadget centre is a cyclic centre (via the sector transition lemma);
  * the gadget centres accumulate, so the cyclic locus is not locally finite.
-/
import SectorGadget

open MeasureTheory Filter Topology Set
open scoped ENNReal

attribute [local instance] Classical.propDecidable

namespace SectorGadget

/-! ## 5. The cyclic locus -/

/-- A point is in the cyclic locus if the transition graph at that point contains a triangle
(in particular a cycle, in the sense of the paper's Definition 6.1 / Theorem 6.5). -/
def CyclicLocus (c : ℂ → Fin 7) : Set ℂ :=
  {x | ∃ i j l : Fin 7, i ≠ j ∧ j ≠ l ∧ l ≠ i ∧
      TransitionEdge c i j x ∧ TransitionEdge c j l x ∧ TransitionEdge c l i x}

lemma mem_cyclicLocus_of_triangle {c : ℂ → Fin 7} {x : ℂ}
    (h1 : TransitionEdge c 0 2 x) (h2 : TransitionEdge c 2 3 x) (h3 : TransitionEdge c 0 3 x) :
    x ∈ CyclicLocus c :=
  ⟨0, 2, 3, by decide, by decide, by decide, h1, h2, h3.symm⟩

/-- Local finiteness of a set in the plane. -/
def LocallyFinite (S : Set ℂ) : Prop := ∀ K : Set ℂ, IsCompact K → (S ∩ K).Finite

/-! ## 6. The construction -/

/-- The closed square of side `L` centred at `p`. -/
def square (p : ℂ) (L : ℝ) : Set ℂ :=
  {x | |(x - p).re| ≤ L/2 ∧ |(x - p).im| ≤ L/2}

lemma ySector_mem (x q : ℂ) : ySector x q ∈ ({0, 2, 3} : Set (Fin 7)) := by
  unfold ySector
  split_ifs <;> simp

/-- The modified colouring: the Y gadget on each of the disjoint disks `B(q n, r n)` (all
inside `square p L`), label `0` on the rest of the square, and `g` outside the square. -/
noncomputable def construction (g : ℂ → Fin 7) (p : ℂ) (L : ℝ) (q : ℕ → ℂ) (r : ℕ → ℝ) :
    ℂ → Fin 7 :=
  fun x => if h : ∃ n, ‖x - q n‖ < r n then ySector (q (Nat.find h)) x
    else if x ∈ square p L then 0 else g x

lemma construction_of_mem_ball {g : ℂ → Fin 7} {p : ℂ} {L : ℝ} {q : ℕ → ℂ} {r : ℕ → ℝ}
    (hdisj : ∀ n m, n ≠ m →
      Disjoint (Metric.ball (q n) (r n)) (Metric.ball (q m) (r m)))
    {x : ℂ} {n : ℕ} (hx : ‖x - q n‖ < r n) :
    construction g p L q r x = ySector (q n) x := by
  have hex : ∃ m, ‖x - q m‖ < r m := ⟨n, hx⟩
  have hm : ‖x - q (Nat.find hex)‖ < r (Nat.find hex) := Nat.find_spec hex
  have hb1 : x ∈ Metric.ball (q (Nat.find hex)) (r (Nat.find hex)) := by
    rw [Metric.mem_ball, Complex.dist_eq]; exact hm
  have hb2 : x ∈ Metric.ball (q n) (r n) := by
    rw [Metric.mem_ball, Complex.dist_eq]; exact hx
  have hidx : Nat.find hex = n := by
    by_contra hne
    exact Set.disjoint_left.mp (hdisj (Nat.find hex) n hne) hb1 hb2
  simp only [construction, dif_pos hex, hidx]

lemma construction_of_not_mem_square {g : ℂ → Fin 7} {p : ℂ} {L : ℝ} {q : ℕ → ℂ}
    {r : ℕ → ℝ} {x : ℂ} (hx : ∀ n, ¬ ‖x - q n‖ < r n) (hsq : x ∉ square p L) :
    construction g p L q r x = g x := by
  have h : ¬ ∃ n, ‖x - q n‖ < r n := fun ⟨n, hn⟩ => hx n hn
  simp only [construction, dif_neg h, hsq, if_false]

/-! ## 7. Elementary geometry of the square -/

lemma sq_norm_re_im (z : ℂ) : ‖z‖ ^ 2 = z.re ^ 2 + z.im ^ 2 := by
  rw [Complex.sq_norm, Complex.normSq_apply]; ring

lemma le_of_sq_le_sq {a b : ℝ} (hb : 0 ≤ b) (h : a ^ 2 ≤ b ^ 2) : a ≤ b := by
  have h1 : a ≤ |a| := le_abs_self a
  have h2 : |a| ≤ b := by
    rw [← Real.sqrt_sq (abs_nonneg a), ← Real.sqrt_sq hb]
    exact Real.sqrt_le_sqrt (by simpa [sq_abs] using h)
  linarith

lemma norm_sub_le_of_mem_square {p : ℂ} {L : ℝ} {x y : ℂ} (hx : x ∈ square p L)
    (hy : y ∈ square p L) (hL : 0 ≤ L) : ‖x - y‖ ≤ L * Real.sqrt 2 := by
  have h1 := abs_le.mp hx.1
  have h2 := abs_le.mp hx.2
  have h3 := abs_le.mp hy.1
  have h4 := abs_le.mp hy.2
  have hre : ((x - y).re) ^ 2 ≤ L ^ 2 := by
    have he : (x - y).re = (x - p).re - (y - p).re := by simp [Complex.sub_re]
    rw [he]; nlinarith
  have him : ((x - y).im) ^ 2 ≤ L ^ 2 := by
    have he : (x - y).im = (x - p).im - (y - p).im := by simp [Complex.sub_im]
    rw [he]; nlinarith
  have hsq := sq_norm_re_im (x - y)
  have hsqrt : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hgoal : (L * Real.sqrt 2) ^ 2 = 2 * L ^ 2 := by rw [mul_pow, hsqrt]; ring
  refine le_of_sq_le_sq (by positivity) ?_
  rw [hgoal]
  nlinarith [norm_nonneg (x - y)]

lemma norm_sub_center_le_of_mem_square {p : ℂ} {L : ℝ} {x : ℂ} (hx : x ∈ square p L)
    (hL : 0 ≤ L) : ‖x - p‖ ≤ L * Real.sqrt 2 / 2 := by
  have h1 := abs_le.mp hx.1
  have h2 := abs_le.mp hx.2
  have hre : ((x - p).re) ^ 2 ≤ (L/2) ^ 2 := by nlinarith
  have him : ((x - p).im) ^ 2 ≤ (L/2) ^ 2 := by nlinarith
  have hsq := sq_norm_re_im (x - p)
  have hsqrt : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hgoal : (L * Real.sqrt 2 / 2) ^ 2 = L ^ 2 / 2 := by
    rw [div_pow, mul_pow, hsqrt]; ring
  refine le_of_sq_le_sq (by positivity) ?_
  rw [hgoal]
  nlinarith [norm_nonneg (x - p)]

lemma construction_mem_square {g : ℂ → Fin 7} {p : ℂ} {L : ℝ} {q : ℕ → ℂ} {r : ℕ → ℝ}
    {x : ℂ} (hx : x ∈ square p L) :
    construction g p L q r x ∈ ({0, 2, 3} : Set (Fin 7)) := by
  unfold construction
  split_ifs with h
  · exact ySector_mem _ _
  · simp

/-- Annulus bounds: a unit-distance neighbour of a point of the square lies in the annulus
`1-ε ≤ · ≤ 1+ε` around the centre, provided `δ < ε` where `δ` bounds the point's distance
to the centre. -/
lemma annulus_bounds {p z x : ℂ} {ε δ : ℝ} (hz : ‖z - p‖ ≤ δ) (hδε : δ < ε)
    (h : ‖x - z‖ = 1) : 1 - ε ≤ ‖x - p‖ ∧ ‖x - p‖ ≤ 1 + ε := by
  constructor
  · have h1 : ‖x - z‖ ≤ ‖x - p‖ + ‖p - z‖ := by
      have := norm_add_le (x - p) (p - z)
      have he : (x - p) + (p - z) = x - z := by ring
      rwa [he] at this
    rw [h, norm_sub_rev p z] at h1
    linarith
  · have h1 : ‖x - p‖ ≤ ‖x - z‖ + ‖z - p‖ := by
      have := norm_add_le (x - z) (z - p)
      have he : (x - z) + (z - p) = x - p := by ring
      rwa [he] at this
    rw [h] at h1
    linarith

/-! ## 8. The main assembly theorem -/

/-- **A proper colouring with non-locally-finite cyclic locus.**

If `g` is a proper 7-colouring, `p` a point, `L > 0` with `L√2 < 1`, and every point of the
unit-distance annulus `1-ε ≤ |x-p| ≤ 1+ε` (with `ε > L√2/2`) avoids the three labels
`0, 2, 3`, then the modified colouring is proper and its cyclic locus is not locally finite. -/
theorem exists_cyclicLocus_not_locallyFinite
    (g : ℂ → Fin 7) (hg : ∀ x y : ℂ, ‖x - y‖ = 1 → g x ≠ g y)
    (p : ℂ) {L ε : ℝ} (hL : 0 < L) (hL1 : L * Real.sqrt 2 < 1)
    (hε : L * Real.sqrt 2 / 2 < ε)
    (hsh : ∀ x : ℂ, x ∉ square p L → 1 - ε ≤ ‖x - p‖ → ‖x - p‖ ≤ 1 + ε →
      g x ∉ ({0, 2, 3} : Set (Fin 7)))
    (q : ℕ → ℂ) (r : ℕ → ℝ) (hr : ∀ n, 0 < r n)
    (hsub : ∀ n, Metric.ball (q n) (r n) ⊆ square p L)
    (hdisj : ∀ n m, n ≠ m →
      Disjoint (Metric.ball (q n) (r n)) (Metric.ball (q m) (r m)))
    (hball : ∀ n, ‖q n - p‖ ≤ 1) (hinj : Function.Injective q) :
    ∃ c : ℂ → Fin 7, (∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y) ∧
      ¬ LocallyFinite (CyclicLocus c) := by
  refine ⟨construction g p L q r, ?_, ?_⟩
  · -- properness
    intro x y hxy hcol
    have hout : ∀ z : ℂ, z ∉ square p L → construction g p L q r z = g z := by
      intro z hz
      refine construction_of_not_mem_square (x := z) (fun n => ?_) hz
      intro hcon
      refine hz (hsub n ?_)
      rw [Metric.mem_ball, Complex.dist_eq]; exact hcon
    by_cases hx : x ∈ square p L
    · by_cases hy : y ∈ square p L
      · have hle := norm_sub_le_of_mem_square hx hy hL.le
        rw [hxy] at hle
        linarith
      · have hcx : construction g p L q r x ∈ ({0, 2, 3} : Set (Fin 7)) :=
          construction_mem_square hx
        have hcy := hout y hy
        have hxp := norm_sub_center_le_of_mem_square hx hL.le
        obtain ⟨h2, h1⟩ := annulus_bounds hxp hε (by rw [norm_sub_rev]; exact hxy)
        have hgy : g y ∈ ({0, 2, 3} : Set (Fin 7)) := by
          rw [← hcy, ← hcol]
          exact hcx
        exact hsh y hy h2 h1 hgy
    · by_cases hy : y ∈ square p L
      · have hcy : construction g p L q r y ∈ ({0, 2, 3} : Set (Fin 7)) :=
          construction_mem_square hy
        have hcx := hout x hx
        have hxp := norm_sub_center_le_of_mem_square hy hL.le
        obtain ⟨h2, h1⟩ := annulus_bounds hxp hε hxy
        have hgx : g x ∈ ({0, 2, 3} : Set (Fin 7)) := by
          rw [← hcol, hcx] at hcy
          exact hcy
        exact hsh x hx h2 h1 hgx
      · have hcx := hout x hx
        have hcy := hout y hy
        exact hg x y hxy (by rw [← hcx, ← hcy]; exact hcol)
  · -- the cyclic locus accumulates at `p`
    intro hfin
    have hcyc : ∀ n, q n ∈ CyclicLocus (construction g p L q r) := by
      intro n
      have hagree : ∀ y : ℂ, ‖y - q n‖ < r n →
          construction g p L q r y = ySector (q n) y := fun y hy =>
        construction_of_mem_ball hdisj hy
      have e1 : TransitionEdge (construction g p L q r) 0 2 (q n) := by
        refine transitionEdge_of_horizontal (k := 7) (hρ := hr n) (hij := by decide)
          1 (Or.inl rfl) ?_ ?_
        · intro y hy hyim
          rw [hagree y hy]
          have him : (q n).im < y.im := by simpa [Complex.sub_im] using hyim
          simp [ySector, him]
        · intro y hy hyim hre
          rw [hagree y hy]
          have him : ¬ ((q n).im < y.im) := by
            have h' : y.im < (q n).im := by simpa [Complex.sub_im] using hyim
            exact not_lt.mpr h'.le
          have hre' : (q n).re < y.re := by
            have h' : 0 < (y - q n).re := by linarith
            simpa [Complex.sub_re] using h'
          simp [ySector, him, hre']
      have e2 : TransitionEdge (construction g p L q r) 2 3 (q n) := by
        refine transitionEdge_of_vertical (k := 7) (hρ := hr n) (hij := by decide) ?_ ?_
        · intro y hy hre him
          rw [hagree y hy]
          have him : ¬ ((q n).im < y.im) := by
            have h' : y.im < (q n).im := by simpa [Complex.sub_im] using him
            exact not_lt.mpr h'.le
          have hre' : (q n).re < y.re := by simpa [Complex.sub_re] using hre
          simp [ySector, him, hre']
        · intro y hy hre him
          rw [hagree y hy]
          have him : ¬ ((q n).im < y.im) := by
            have h' : y.im < (q n).im := by simpa [Complex.sub_im] using him
            exact not_lt.mpr h'.le
          have hre' : ¬ ((q n).re < y.re) := by
            have h' : y.re < (q n).re := by simpa [Complex.sub_re] using hre
            exact not_lt.mpr h'.le
          simp [ySector, him, hre']
      have e3 : TransitionEdge (construction g p L q r) 0 3 (q n) := by
        refine transitionEdge_of_horizontal (k := 7) (hρ := hr n) (hij := by decide)
          (-1) (Or.inr rfl) ?_ ?_
        · intro y hy hyim
          rw [hagree y hy]
          have him : (q n).im < y.im := by simpa [Complex.sub_im] using hyim
          simp [ySector, him]
        · intro y hy hyim hre
          rw [hagree y hy]
          have him : ¬ ((q n).im < y.im) := by
            have h' : y.im < (q n).im := by simpa [Complex.sub_im] using hyim
            exact not_lt.mpr h'.le
          have hre' : ¬ ((q n).re < y.re) := by
            intro hlt
            have h1 : 0 < -1 * (y - q n).re := hre
            have h2 : (y - q n).re < 0 := by linarith
            have h3 : y.re < (q n).re := by simpa [Complex.sub_re] using h2
            linarith
          simp [ySector, him, hre']
      exact mem_cyclicLocus_of_triangle e1 e2 e3
    have hsub2 : Set.range q ⊆ CyclicLocus (construction g p L q r) ∩
        Metric.closedBall p 1 := by
      rintro _ ⟨n, rfl⟩
      exact ⟨hcyc n, by rw [Metric.mem_closedBall, Complex.dist_eq]; exact hball n⟩
    have hfinrange : (Set.range q).Finite :=
      (hfin _ (isCompact_closedBall p 1)).subset hsub2
    exact (Set.infinite_range_of_injective hinj) hfinrange

end SectorGadget
