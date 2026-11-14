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

/-- The cyclic locus is not locally finite. -/
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
  have hidx : Nat.find hex = n := by
    by_contra hne
    exact Set.disjoint_left.mp (hdisj (Nat.find hex) n hne) hm hx
  simp only [construction, dif_pos hex, hidx]

lemma construction_of_forall_not_mem {g : ℂ → Fin 7} {p : ℂ} {L : ℝ} {q : ℕ → ℂ}
    {r : ℕ → ℝ} {x : ℂ} (hx : ∀ n, ¬ ‖x - q n‖ < r n) :
    construction g p L q r x = if x ∈ square p L then 0 else g x := by
  have h : ¬ ∃ n, ‖x - q n‖ < r n := fun ⟨n, hn⟩ => hx n hn
  simp only [construction, dif_neg h]

lemma construction_of_not_mem_square {g : ℂ → Fin 7} {p : ℂ} {L : ℝ} {q : ℕ → ℂ}
    {r : ℕ → ℝ} {x : ℂ} (hx : ∀ n, ¬ ‖x - q n‖ < r n) (hsq : x ∉ square p L) :
    construction g p L q r x = g x := by
  rw [construction_of_forall_not_mem hx]
  simp only [hsq, if_false]

/-! ## 7. Elementary geometry of the square -/

lemma sq_norm_re_im (z : ℂ) : ‖z‖ ^ 2 = z.re ^ 2 + z.im ^ 2 := by
  rw [Complex.sq_norm, Complex.normSq_apply]; ring

lemma norm_sub_le_of_mem_square {p : ℂ} {L : ℝ} {x y : ℂ} (hx : x ∈ square p L)
    (hy : y ∈ square p L) (hL : 0 ≤ L) : ‖x - y‖ ≤ L * Real.sqrt 2 := by
  have h1 : |(x - p).re| ≤ L/2 := hx.1
  have h2 : |(x - p).im| ≤ L/2 := hx.2
  have h3 : |(y - p).re| ≤ L/2 := hy.1
  have h4 : |(y - p).im| ≤ L/2 := hy.2
  have hre : ((x - y).re) ^ 2 ≤ L ^ 2 := by
    have : (x - y).re = (x - p).re - (y - p).re := by simp [Complex.sub_re]
    rw [this]
    have a1 := abs_le.mp h1; have a2 := abs_le.mp h3
    nlinarith
  have him : ((x - y).im) ^ 2 ≤ L ^ 2 := by
    have : (x - y).im = (x - p).im - (y - p).im := by simp [Complex.sub_im]
    rw [this]
    have a1 := abs_le.mp h2; have a2 := abs_le.mp h4
    nlinarith
  have hsq := sq_norm_re_im (x - y)
  have hsqrt : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hgoal : (L * Real.sqrt 2) ^ 2 = 2 * L ^ 2 := by rw [mul_pow, hsqrt]; ring
  nlinarith [norm_nonneg (x - y), Real.sqrt_nonneg 2]

lemma norm_sub_center_le_of_mem_square {p : ℂ} {L : ℝ} {x : ℂ} (hx : x ∈ square p L)
    (hL : 0 ≤ L) : ‖x - p‖ ≤ L * Real.sqrt 2 / 2 := by
  have h1 : |(x - p).re| ≤ L/2 := hx.1
  have h2 : |(x - p).im| ≤ L/2 := hx.2
  have hre : ((x - p).re) ^ 2 ≤ (L/2) ^ 2 := by
    have a1 := abs_le.mp h1; nlinarith
  have him : ((x - p).im) ^ 2 ≤ (L/2) ^ 2 := by
    have a2 := abs_le.mp h2; nlinarith
  have hsq := sq_norm_re_im (x - p)
  have hsqrt : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hgoal : (L * Real.sqrt 2 / 2) ^ 2 = L ^ 2 / 2 := by
    rw [div_pow, mul_pow, hsqrt]; ring
  nlinarith [norm_nonneg (x - p), Real.sqrt_nonneg 2]

lemma construction_mem_square {g : ℂ → Fin 7} {p : ℂ} {L : ℝ} {q : ℕ → ℂ} {r : ℕ → ℝ}
    {x : ℂ} (hx : x ∈ square p L) :
    construction g p L q r x ∈ ({0, 2, 3} : Set (Fin 7)) := by
  unfold construction
  split_ifs with h
  · exact ySector_mem _ _
  · simp

/-! ## 8. The main assembly theorem -/

/-- **A proper colouring with non-locally-finite cyclic locus.**

If `g` is a proper 7-colouring, `p` a point, `L > 0` with `L√2 < 1`, and every point of the
unit-distance annulus `1-ε ≤ |x-p| ≤ 1+ε` (with `ε > L√2/2`) avoids the three labels
`0, 2, 3`, then the modified colouring is proper and its cyclic locus accumulates. -/
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
    by_cases hx : x ∈ square p L
    · by_cases hy : y ∈ square p L
      · -- both inside the square: its diameter is too small
        have hle := norm_sub_le_of_mem_square hx hy hL.le
        rw [hxy] at hle
        linarith
      · -- x inside, y outside: labels {0,2,3} versus the annulus labels
        have hcx : construction g p L q r x ∈ ({0, 2, 3} : Set (Fin 7)) :=
          construction_mem_square hx
        have hcy : construction g p L q r y = g y := by
          refine construction_of_not_mem_square (x := y) (fun n => ?_) hy
          intro hcon
          exact hy (hsub n (by simpa [Complex.dist_eq] using Metric.mem_ball.mp hcon))
        have hxp : ‖x - p‖ ≤ L * Real.sqrt 2 / 2 :=
          norm_sub_center_le_of_mem_square hx hL.le
        have h1 : ‖y - p‖ ≤ 1 + ε := by
          have := norm_add_le (y - x) (x - p)
          have hnorm : ‖y - x‖ = 1 := by rw [norm_sub_rev]; exact hxy
          rw [hnorm] at this
          have : ‖(y - x) + (x - p)‖ = ‖y - p‖ := by congr 1; ring
          linarith
        have h2 : 1 - ε ≤ ‖y - p‖ := by
          have h3 : ‖y - x‖ ≤ ‖y - p‖ + ‖p - x‖ := by
            have := norm_add_le (y - p) (p - x)
            have heq : (y - p) + (p - x) = y - x := by ring
            rw [heq] at this
            exact this
          have hnorm : ‖y - x‖ = 1 := by rw [norm_sub_rev]; exact hxy
          rw [hnorm, norm_sub_rev x p] at h3
          linarith
        rw [hcol] at hcx
        exact hsh y hy h2 h1 hcx
    · -- x outside
      by_cases hy : y ∈ square p L
      · have hcy : construction g p L q r y ∈ ({0, 2, 3} : Set (Fin 7)) :=
          construction_mem_square hy
        have hcx : construction g p L q r x = g x := by
          refine construction_of_not_mem_square (x := x) (fun n => ?_) hx
          intro hcon
          exact hx (hsub n (by simpa [Complex.dist_eq] using Metric.mem_ball.mp hcon))
        rw [← hcol, hcx] at hcy
        -- hcy : g x ∈ {0,2,3}
        have hxp : ‖y - p‖ ≤ L * Real.sqrt 2 / 2 :=
          norm_sub_center_le_of_mem_square hy hL.le
        have h1 : ‖x - p‖ ≤ 1 + ε := by
          have := norm_add_le (x - y) (y - p)
          have : ‖(x - y) + (y - p)‖ = ‖x - p‖ := by congr 1; ring
          rw [hxy] at this
          linarith
        have h2 : 1 - ε ≤ ‖x - p‖ := by
          have h3 : ‖x - y‖ ≤ ‖x - p‖ + ‖p - y‖ := by
            have := norm_add_le (x - p) (p - y)
            have heq : (x - p) + (p - y) = x - y := by ring
            rw [heq] at this
            exact this
          rw [hxy, norm_sub_rev y p] at h3
          linarith
        exact hsh x hx h2 h1 hcy
      · -- both outside: reduce to properness of g
        have hcx : construction g p L q r x = g x := by
          rw [construction_of_forall_not_mem (x := x) (fun n => ?_)]
          simp only [hx, if_false]
          intro hcon
          exact hx (hsub n (Metric.mem_ball.mp hcon))
        have hcy : construction g p L q r y = g y := by
          refine construction_of_not_mem_square (x := y) (fun n => ?_) hy
          intro hcon
          exact hy (hsub n (by simpa [Complex.dist_eq] using Metric.mem_ball.mp hcon))
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
          have : (q n).im < y.im := by simpa [Complex.sub_im] using hyim
          simp [ySector, this]
        · intro y hy hyim hre
          rw [hagree y hy]
          have him : ¬ ((q n).im < y.im) := by
            have : y.im < (q n).im := by simpa [Complex.sub_im] using hyim
            exact not_lt.mpr this.le
          have hre' : (q n).re < y.re := by
            have : 0 < (y - q n).re := by linarith
            simpa [Complex.sub_re] using this
          simp [ySector, him, hre']
      have e2 : TransitionEdge (construction g p L q r) 2 3 (q n) := by
        refine transitionEdge_of_vertical (k := 7) (hρ := hr n) (hij := by decide) ?_ ?_
        · intro y hy hre him
          rw [hagree y hy]
          have him' : ¬ ((q n).im < y.im) := by
            have : y.im < (q n).im := by simpa [Complex.sub_im] using him
            exact not_lt.mpr this.le
          have hre' : (q n).re < y.re := by
            have : 0 < (y - q n).re := by simpa [Complex.sub_re] using hre
            simpa [Complex.sub_re] using this
          simp [ySector, him', hre']
        · intro y hy hre him
          rw [hagree y hy]
          have him' : ¬ ((q n).im < y.im) := by
            have : y.im < (q n).im := by simpa [Complex.sub_im] using him
            exact not_lt.mpr this.le
          have hre' : ¬ ((q n).re < y.re) := by
            have : y.re < (q n).re := by simpa [Complex.sub_re] using hre
            exact not_lt.mpr this.le
          simp [ySector, him', hre']
      have e3 : TransitionEdge (construction g p L q r) 0 3 (q n) := by
        refine transitionEdge_of_horizontal (k := 7) (hρ := hr n) (hij := by decide)
          (-1) (Or.inr rfl) ?_ ?_
        · intro y hy hyim
          rw [hagree y hy]
          have : (q n).im < y.im := by simpa [Complex.sub_im] using hyim
          simp [ySector, this]
        · intro y hy hyim hre
          rw [hagree y hy]
          have him : ¬ ((q n).im < y.im) := by
            have : y.im < (q n).im := by simpa [Complex.sub_im] using hyim
            exact not_lt.mpr this.le
          have hre' : ¬ ((q n).re < y.re) := by
            intro h
            have h2 : 0 < -1 * (y - q n).re := hre
            have : (y - q n).re < 0 := by linarith
            have : y.re < (q n).re := by simpa [Complex.sub_re] using this
            linarith
          simp [ySector, him, hre']
      exact mem_cyclicLocus_of_triangle e1 e2 e3
    have hsub2 : Set.range q ⊆ CyclicLocus (construction g p L q r) ∩
        Metric.closedBall p 1 := by
      rintro _ ⟨n, rfl⟩
      exact ⟨hcyc n, by rw [Metric.mem_closedBall, Complex.dist_eq]; exact hball n⟩
    have hfinrange : (Set.range q).Finite :=
      (hfin _ isCompact_closedBall).subset hsub2
    have hinfin : (Set.range q).Infinite := Set.infinite_range_of_injective hinj
    exact hinfin hfinrange

end SectorGadget
