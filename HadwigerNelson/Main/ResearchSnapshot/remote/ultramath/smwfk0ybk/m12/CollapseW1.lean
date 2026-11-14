import OAI.Geometry.PlaneColoring.Five
-- PaletteCollapse body copied verbatim from .ultramath/smwfhd5sl/m7/Collapse.lean (from line 23)

namespace PaletteCollapse

/-- Explicit unit complex numbers: the Pythagorean parametrisation of the unit circle. -/
noncomputable def zc (n : ℕ) : ℂ :=
  Complex.mk (((n : ℝ) ^ 2 - 1) / ((n : ℝ) ^ 2 + 1)) (((2 : ℝ) * n) / ((n : ℝ) ^ 2 + 1))

lemma zc_re (n : ℕ) : (zc n).re = ((n : ℝ) ^ 2 - 1) / ((n : ℝ) ^ 2 + 1) := rfl

lemma zc_im (n : ℕ) : (zc n).im = ((2 : ℝ) * n) / ((n : ℝ) ^ 2 + 1) := rfl

lemma zc_normSq (n : ℕ) : Complex.normSq (zc n) = 1 := by
  rw [Complex.normSq_apply, zc_re, zc_im]
  have h : ((n : ℝ) ^ 2 + 1) ≠ 0 := by positivity
  field_simp
  ring

lemma zc_norm (n : ℕ) : ‖zc n‖ = 1 := by
  have h : ‖zc n‖ ^ 2 = 1 := by
    rw [← Complex.normSq_eq_norm_sq, zc_normSq]
  nlinarith [norm_nonneg (zc n)]

/-- Real parts strictly increase along `ℕ`, so `zc` is injective — all the cardinality fact needs. -/
lemma zc_injective : Function.Injective zc := by
  intro m n hmn
  have hre : ((m : ℝ) ^ 2 - 1) / ((m : ℝ) ^ 2 + 1) = ((n : ℝ) ^ 2 - 1) / ((n : ℝ) ^ 2 + 1) := by
    rw [← zc_re m, ← zc_re n, hmn]
  have hm : ((m : ℝ) ^ 2 + 1) ≠ 0 := by positivity
  have hn : ((n : ℝ) ^ 2 + 1) ≠ 0 := by positivity
  rw [div_eq_div_iff hm hn] at hre
  have hsq : (m : ℝ) ^ 2 = (n : ℝ) ^ 2 := by nlinarith
  have hm0 : (0 : ℝ) ≤ (m : ℝ) := by positivity
  have hn0 : (0 : ℝ) ≤ (n : ℝ) := by positivity
  have hcast : (m : ℝ) = (n : ℝ) := by nlinarith
  exact_mod_cast hcast

/-- The cardinality fact: finitely many signed values never exhaust the unit circle. -/
lemma exists_unit_avoiding (k : ℕ) (u : Fin k → ℂ) :
    ∃ s : ℂ, ‖s‖ = 1 ∧ ∀ i, s ≠ u i ∧ s ≠ -(u i) := by
  classical
  set F : Finset ℂ := Finset.univ.image u ∪ Finset.univ.image (fun i => -(u i)) with hF
  have hFcard : F.card ≤ 2 * k := by
    have h1 : (Finset.univ.image u).card ≤ k := by
      simpa using Finset.card_image_le (s := (Finset.univ : Finset (Fin k))) (f := u)
    have h2 : (Finset.univ.image (fun i : Fin k => -(u i))).card ≤ k := by
      simpa using Finset.card_image_le (s := (Finset.univ : Finset (Fin k))) (f := fun i => -(u i))
    calc F.card ≤ (Finset.univ.image u).card + (Finset.univ.image (fun i => -(u i))).card :=
          Finset.card_union_le _ _
      _ ≤ k + k := by omega
      _ = 2 * k := by ring
  have himg : ((Finset.range (2 * k + 1)).image zc).card = 2 * k + 1 := by
    rw [Finset.card_image_of_injOn]
    · simp
    · intro a _ b _ hab
      exact zc_injective hab
  have hlt : F.card < ((Finset.range (2 * k + 1)).image zc).card := by
    rw [himg]; omega
  obtain ⟨s, hs, hsf⟩ := Finset.exists_mem_notMem_of_card_lt_card hlt
  obtain ⟨j, -, rfl⟩ := Finset.mem_image.mp hs
  refine ⟨zc j, zc_norm j, fun i => ⟨?_, ?_⟩⟩
  · intro h
    refine hsf ?_
    rw [hF]
    exact Finset.mem_union_left _ (Finset.mem_image.mpr ⟨i, Finset.mem_univ i, h.symm⟩)
  · intro h
    refine hsf ?_
    rw [hF]
    exact Finset.mem_union_right _ (Finset.mem_image.mpr ⟨i, Finset.mem_univ i, h.symm⟩)

/-- **The collapse lemma.**  A nonempty palette field satisfying the pointwise palette-transfer
disjointness forces a proper `k`-colouring of the plane. -/
theorem exists_coloring_of_palette (k : ℕ) (Q : Fin k → ℂ → Set ℂ)
    (hne : ∀ a s : ℂ, ‖s‖ = 1 → ∃ i, s ∈ Q i a)
    (htr : ∀ (a b s f : ℂ), ‖s‖ = 1 → ‖f‖ = 1 → ‖a - b‖ = 1 →
      (∀ r : ℝ, b - a ≠ r • s) → ¬ ∃ i, s ∈ Q i a ∧ f ∈ Q i b)
    (hbig : ∀ u : Fin k → ℂ, ∃ s : ℂ, ‖s‖ = 1 ∧ ∀ i, s ≠ u i ∧ s ≠ -(u i)) :
    ∃ c : ℂ → Fin k, ∀ a b : ℂ, ‖a - b‖ = 1 → c a ≠ c b := by
  classical
  -- the unit part of each palette
  set P : Fin k → ℂ → Set ℂ := fun i a => Q i a ∩ {s : ℂ | ‖s‖ = 1} with hP
  -- a point is `i`-good when label `i` occupies a direction set that is not inside a pair {u,-u}
  set G : Fin k → Set ℂ :=
    fun i => {a : ℂ | (P i a).Nonempty ∧ ∀ u : ℂ, ‖u‖ = 1 → ¬ P i a ⊆ {u, -u}} with hG
  have hPunit : ∀ (i : Fin k) (a s : ℂ), s ∈ P i a → ‖s‖ = 1 := fun i a s hs => hs.2
  have hPQ : ∀ (i : Fin k) (a s : ℂ), s ∈ P i a → s ∈ Q i a := fun i a s hs => hs.1
  -- Step 1: every point is good for at least one label.
  have hcover : ∀ a : ℂ, ∃ i, a ∈ G i := by
    intro a
    by_contra hcon
    have hcon' : ∀ i, ¬ (a ∈ G i) := by simpa using hcon
    have hpair : ∀ i : Fin k, ∃ u : ℂ, ‖u‖ = 1 ∧ P i a ⊆ {u, -u} := by
      intro i
      by_cases h : (P i a).Nonempty
      · by_contra hnp
        exact hcon' i ⟨h, fun u hu hsub => hnp ⟨u, hu, hsub⟩⟩
      · rw [Set.not_nonempty_iff_eq_empty] at h
        exact ⟨1, by norm_num, by rw [h]; exact Set.empty_subset _⟩
    choose u _ hsub using hpair
    obtain ⟨s, hs1, hsne⟩ := hbig u
    obtain ⟨i, hi⟩ := hne a s hs1
    have hmem : s ∈ P i a := ⟨hi, hs1⟩
    have hmem' : s ∈ ({u i, -(u i)} : Set ℂ) := hsub i hmem
    rcases hmem' with h | h
    · exact (hsne i).1 h
    · exact (hsne i).2 h
  -- Step 2: for a good label, every direction in the palette at `a` points along `b - a`.
  have key : ∀ (i : Fin k) (a b t f : ℂ), a ∈ G i → b ∈ G i → ‖a - b‖ = 1 →
      t ∈ P i a → f ∈ P i b → t = b - a ∨ t = -(b - a) := by
    intro i a b t f _ _ hd ht hf
    have ht1 : ‖t‖ = 1 := hPunit i a t ht
    have hf1 : ‖f‖ = 1 := hPunit i b f hf
    have hd' : ‖b - a‖ = 1 := by rwa [norm_sub_rev]
    have hpar : ∃ r : ℝ, b - a = r • t := by
      by_contra hnp
      exact htr a b t f ht1 hf1 hd (fun r hr => hnp ⟨r, hr⟩)
        ⟨i, hPQ i a t ht, hPQ i b f hf⟩
    obtain ⟨r, hr⟩ := hpar
    have hr1 : ‖r‖ = 1 := by
      have h2 : ‖b - a‖ = ‖r‖ * ‖t‖ := by rw [hr, norm_smul]
      rw [hd', ht1, mul_one] at h2
      exact h2.symm
    have h3 : r ^ 2 = 1 := by
      have h4 : |r| = 1 := by simpa [Real.norm_eq_abs] using hr1
      rw [← sq_abs, h4]; norm_num
    rcases sq_eq_one_iff.mp h3 with rfl | rfl
    · left; rw [hr]; simp
    · right; rw [hr]; simp
  -- Step 3: a good set is unit-distance free.
  have hind : ∀ (i : Fin k) (a b : ℂ), a ∈ G i → b ∈ G i → ‖a - b‖ ≠ 1 := by
    intro i a b ha hb hd
    obtain ⟨s, hs⟩ := ha.1
    obtain ⟨f, hf⟩ := hb.1
    have hd' : ‖b - a‖ = 1 := by rwa [norm_sub_rev]
    refine ha.2 (b - a) hd' (fun t ht => ?_)
    rcases key i a b t f ha hb hd ht hf with h | h
    · simp [h]
    · simp [h]
  -- Step 4: choose a good label at every point.
  choose c hc using hcover
  refine ⟨c, fun a b hd heq => ?_⟩
  have hb : b ∈ G (c a) := by rw [heq]; exact hc b
  exact hind (c a) a b (hc a) hb hd


/-- **Corollary A (level 6).**  A palette field at level 6 with nonempty palettes satisfying the
pointwise palette transfer IS a proper 6-colouring of the plane.  Hence the brief's suggested L4
certificate ("an explicit palette system at k = 6 satisfying (a)-(f)") is exactly an explicit
6-colouring, i.e. terminal outcome L2 — not L4. -/
theorem six_coloring_of_palette_six (Q : Fin 6 → ℂ → Set ℂ)
    (hne : ∀ a s : ℂ, ‖s‖ = 1 → ∃ i, s ∈ Q i a)
    (htr : ∀ (a b s f : ℂ), ‖s‖ = 1 → ‖f‖ = 1 → ‖a - b‖ = 1 →
      (∀ r : ℝ, b - a ≠ r • s) → ¬ ∃ i, s ∈ Q i a ∧ f ∈ Q i b) :
    ∃ c : ℂ → Fin 6, ∀ a b : ℂ, ‖a - b‖ = 1 → c a ≠ c b :=
  exists_coloring_of_palette 6 Q hne htr (exists_unit_avoiding 6)

/-- **Corollary B (level 5, non-vacuity).**  The same axioms at level 5 *provably* produce a
proper 5-colouring.  Combined with the project's machine-checked `¬ ∃ c : ℂ → Fin 5, ...`
(`OAI.EuclideanFiveColor.no_proper_five_coloring`, fact W1) this shows the palette-transfer axiom
system is UNSATISFIABLE at k = 5: the class is not a strawman, it refutes five labels. -/
theorem five_coloring_of_palette_five (Q : Fin 5 → ℂ → Set ℂ)
    (hne : ∀ a s : ℂ, ‖s‖ = 1 → ∃ i, s ∈ Q i a)
    (htr : ∀ (a b s f : ℂ), ‖s‖ = 1 → ‖f‖ = 1 → ‖a - b‖ = 1 →
      (∀ r : ℝ, b - a ≠ r • s) → ¬ ∃ i, s ∈ Q i a ∧ f ∈ Q i b) :
    ∃ c : ℂ → Fin 5, ∀ a b : ℂ, ‖a - b‖ = 1 → c a ≠ c b :=
  exists_coloring_of_palette 5 Q hne htr (exists_unit_avoiding 5)


/-- **Corollary B, formal form.**  If the plane has no proper 5-colouring — fact W1,
`OAI.EuclideanFiveColor.no_proper_five_coloring`, machine-checked in this project — then the
palette-transfer axioms (P0)+(P1) at level 5 are unsatisfiable.  This is the non-vacuity
certificate for the class: it refutes five labels, and by `exists_coloring_of_palette` it can
refute six only by deciding χ ≤ 6. -/
theorem no_palette_five_of_no_five_coloring
    (h5 : ¬ ∃ c : ℂ → Fin 5, ∀ a b : ℂ, ‖a - b‖ = 1 → c a ≠ c b) :
    ¬ ∃ Q : Fin 5 → ℂ → Set ℂ,
        (∀ a s : ℂ, ‖s‖ = 1 → ∃ i, s ∈ Q i a) ∧
        (∀ (a b s f : ℂ), ‖s‖ = 1 → ‖f‖ = 1 → ‖a - b‖ = 1 →
          (∀ r : ℝ, b - a ≠ r • s) → ¬ ∃ i, s ∈ Q i a ∧ f ∈ Q i b) := by
  rintro ⟨Q, hne, htr⟩
  exact h5 (five_coloring_of_palette_five Q hne htr)

end PaletteCollapse

#print axioms PaletteCollapse.exists_coloring_of_palette
#print axioms PaletteCollapse.six_coloring_of_palette_six
#print axioms PaletteCollapse.five_coloring_of_palette_five
#print axioms PaletteCollapse.exists_unit_avoiding
#print axioms PaletteCollapse.no_palette_five_of_no_five_coloring

/-! ## Closing a record gap: the level-5 non-vacuity certificate, unconditional

`PaletteCollapse.no_palette_five_of_no_five_coloring` takes the five-colouring obstruction as a
*hypothesis*, and `Collapse.lean` imports only Mathlib, so the record's "the palette-transfer axioms
are unsatisfiable at level 5" was never machine-checked as an unconditional statement.  Here it is,
composed with the development's own `OAI.EuclideanFiveColor.no_proper_five_coloring`. -/
namespace PaletteCollapse

theorem no_palette_five_unconditional :
    ¬ ∃ Q : Fin 5 → ℂ → Set ℂ,
        (∀ a s : ℂ, ‖s‖ = 1 → ∃ i, s ∈ Q i a) ∧
        (∀ (a b s f : ℂ), ‖s‖ = 1 → ‖f‖ = 1 → ‖a - b‖ = 1 →
          (∀ r : ℝ, b - a ≠ r • s) → ¬ ∃ i, s ∈ Q i a ∧ f ∈ Q i b) :=
  no_palette_five_of_no_five_coloring OAI.EuclideanFiveColor.no_proper_five_coloring

end PaletteCollapse

#print axioms PaletteCollapse.no_palette_five_unconditional
#print axioms PaletteCollapse.exists_coloring_of_palette
