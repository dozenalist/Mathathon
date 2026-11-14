/-
  OAI / Hadwiger–Nelson audit, member m6.
  Exact, machine-checked verification of the finite geometric certificate of
  paper section 8.5 / 8.6:
  "The Euclidean plane is not five-colorable" (OpenAI, 23 Sep 2026),
  eq. (8.5), Lemma 8.9, Proposition 8.10.

  The seven-vertex Moser unit-distance graph of (8.5):
      A = (√3 + i)/2,  B = (√3 − i)/2,  T = √3,  u = (5 + i√11)/6,
      G = {0, A, B, T, uA, uB, uT}
  is realized here with the exact coordinates of the paper.  We prove, in
  Mathlib and with no `sorry`, no `axiom`, no `native_decide`:

    * `edges_unit`        : the eleven drawn edges have length exactly one;
    * `nonedges_not_unit` : no other pair of the seven points is at distance one,
                            i.e. the unit-distance graph on these points is
                            exactly the eleven-edge graph;
    * `P_injective`       : the seven points are pairwise distinct
                            (no duplicated or merged vertices);
    * `not_three_colorable`: the graph has no proper 3-colouring;
    * `placed_edges_unit`, `placed_nonedges_not_unit`, `Q_injective`
                          : the same three distance/vertex facts for the
                            *placed* coordinates `z_g` of eq. (8.6),
                            `z_g = ((35+12i)/37)(g + (−290+149i)/250)`,
                            which is a direct similarity since
                            `|(35+12i)/37| = 1` (because 35²+12² = 37²).

  `not_three_colorable` is exactly the finite input to Proposition 8.10: the
  open three-label region of Lemma 8.8 contains a translate of the placed graph,
  so a proper colouring of the region by three labels would properly 3-colour it.
  (The strict region membership (8.4) of all seven placed points is verified
  exactly, but not in Lean: see `verify_sec8.py` / `exact_certificate.py`.)

  Check with:  lean OAI_Audit_Moser.lean
-/
import Mathlib

set_option maxHeartbeats 1000000

open Complex

namespace OAI.Audit.Moser

/-- The seven vertices `0, A, B, T, uA, uB, uT` of eq. (8.5), as points of `ℂ ≅ ℝ²`. -/
noncomputable def P : Fin 7 → ℂ
  | 0 => 0                                            -- 0
  | 1 => ⟨Real.sqrt 3 / 2, 1 / 2⟩                     -- A = (√3 + i)/2
  | 2 => ⟨Real.sqrt 3 / 2, -(1 / 2)⟩                  -- B = (√3 − i)/2
  | 3 => ⟨Real.sqrt 3, 0⟩                             -- T = √3
  | 4 => ⟨(5 * Real.sqrt 3 - Real.sqrt 11) / 12,
          (Real.sqrt 3 * Real.sqrt 11 + 5) / 12⟩      -- uA
  | 5 => ⟨(5 * Real.sqrt 3 + Real.sqrt 11) / 12,
          (Real.sqrt 3 * Real.sqrt 11 - 5) / 12⟩      -- uB
  | 6 => ⟨5 * Real.sqrt 3 / 6, Real.sqrt 3 * Real.sqrt 11 / 6⟩  -- uT

/-- The eleven unit-distance edges drawn in Figure 3 of the paper (symmetric form). -/
abbrev Adj (a b : Fin 7) : Prop :=
  (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 0) ∨ (a = 0 ∧ b = 2) ∨ (a = 2 ∧ b = 0) ∨
  (a = 1 ∧ b = 2) ∨ (a = 2 ∧ b = 1) ∨ (a = 1 ∧ b = 3) ∨ (a = 3 ∧ b = 1) ∨
  (a = 2 ∧ b = 3) ∨ (a = 3 ∧ b = 2) ∨ (a = 0 ∧ b = 4) ∨ (a = 4 ∧ b = 0) ∨
  (a = 0 ∧ b = 5) ∨ (a = 5 ∧ b = 0) ∨ (a = 4 ∧ b = 5) ∨ (a = 5 ∧ b = 4) ∨
  (a = 4 ∧ b = 6) ∨ (a = 6 ∧ b = 4) ∨ (a = 5 ∧ b = 6) ∨ (a = 6 ∧ b = 5) ∨
  (a = 3 ∧ b = 6) ∨ (a = 6 ∧ b = 3)

/-! ### Elementary facts about √3, √11, √33 -/

private lemma sq3 : Real.sqrt 3 * Real.sqrt 3 = 3 := Real.mul_self_sqrt (by norm_num)
private lemma sq11 : Real.sqrt 11 * Real.sqrt 11 = 11 := Real.mul_self_sqrt (by norm_num)
private lemma sq33 : Real.sqrt 3 * Real.sqrt 11 = Real.sqrt 33 := by
  rw [← Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 3) 11]; norm_num
private lemma sqq33 : Real.sqrt 33 * Real.sqrt 33 = 33 := Real.mul_self_sqrt (by norm_num)

private lemma dist_sq_eq (a b : Fin 7) :
    dist (P a) (P b) ^ 2
      = ((P a).re - (P b).re) ^ 2 + ((P a).im - (P b).im) ^ 2 := by
  rw [Complex.dist_eq_re_im]
  exact Real.sq_sqrt (by positivity)

/-! ### The eleven edges have length exactly one -/

private lemma dist_of_sq {z w : ℂ} (h : (z.re - w.re) ^ 2 + (z.im - w.im) ^ 2 = 1) :
    dist z w = 1 := by
  rw [Complex.dist_eq_re_im, h]; norm_num

theorem edges_unit : ∀ a b : Fin 7, Adj a b → dist (P a) (P b) = 1 := by
  intro a b h
  fin_cases a <;> fin_cases b <;> simp [Adj] at h ⊢ <;>
    (apply dist_of_sq; simp only [P]; norm_num <;> nlinarith [sq3, sq11, sq33, sqq33])

/-! ### The unit-distance graph on the seven points is exactly these eleven edges -/

theorem nonedges_not_unit : ∀ a b : Fin 7, ¬ Adj a b → dist (P a) (P b) ≠ 1 := by
  intro a b hna hd
  have h2 : ((P a).re - (P b).re) ^ 2 + ((P a).im - (P b).im) ^ 2 = 1 := by
    rw [← dist_sq_eq, hd]; norm_num
  fin_cases a <;> fin_cases b <;>
    first
      | (exfalso; revert hna; decide)
      | (simp only [P, Complex.zero_re, Complex.zero_im] at h2
         ring_nf at h2
         try rw [sq33] at h2
         norm_num at h2 <;> nlinarith [sq3, sq11, sq33, sqq33])

/-! ### No duplicated or merged vertices -/

theorem P_injective : Function.Injective P := by
  intro a b h
  by_contra hab
  have hd : ((P a).re - (P b).re) ^ 2 + ((P a).im - (P b).im) ^ 2 = 0 := by
    have h1 : dist (P a) (P b) = 0 := by rw [h, dist_self]
    rw [← dist_sq_eq, h1]; norm_num
  fin_cases a <;> fin_cases b <;>
    first
      | exact absurd rfl hab
      | (simp only [P, Complex.zero_re, Complex.zero_im] at hd
         ring_nf at hd
         try rw [sq33] at hd
         norm_num at hd <;> nlinarith [sq3, sq11, sq33, sqq33])

/-! ### No proper 3-colouring -/

/-- In `Fin 3`, two elements different from a given pair `a ≠ b` coincide. -/
private lemma fin3_third {a b x y : Fin 3} (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b)
    (hya : y ≠ a) (hyb : y ≠ b) : x = y := by
  revert a b x y
  decide

/--
The Moser graph of (8.5) is not 3-colourable: the triangles `{0,A,B}` and `{T,A,B}`
force `0` and `T` to have the same colour, the triangles `{0,uA,uB}` and
`{uT,uA,uB}` force `0` and `uT` to have the same colour, yet `T` and `uT` are at
unit distance.
-/
theorem not_three_colorable :
    ¬ ∃ c : Fin 7 → Fin 3, ∀ a b, Adj a b → c a ≠ c b := by
  rintro ⟨c, hc⟩
  have e01 : c 0 ≠ c 1 := hc 0 1 (by decide)
  have e02 : c 0 ≠ c 2 := hc 0 2 (by decide)
  have e12 : c 1 ≠ c 2 := hc 1 2 (by decide)
  have e13 : c 1 ≠ c 3 := hc 1 3 (by decide)
  have e23 : c 2 ≠ c 3 := hc 2 3 (by decide)
  have e04 : c 0 ≠ c 4 := hc 0 4 (by decide)
  have e05 : c 0 ≠ c 5 := hc 0 5 (by decide)
  have e45 : c 4 ≠ c 5 := hc 4 5 (by decide)
  have e46 : c 4 ≠ c 6 := hc 4 6 (by decide)
  have e56 : c 5 ≠ c 6 := hc 5 6 (by decide)
  have e36 : c 3 ≠ c 6 := hc 3 6 (by decide)
  have h03 : c 0 = c 3 :=
    fin3_third (a := c 1) (b := c 2) e12 e01 e02 (Ne.symm e13) (Ne.symm e23)
  have h06 : c 0 = c 6 :=
    fin3_third (a := c 4) (b := c 5) e45 e04 e05 (Ne.symm e46) (Ne.symm e56)
  exact e36 (h03.symm.trans h06)

/-! ### The placed graph of (8.6)

`z_g = ((35+12i)/37) · ( g + (−290+149i)/250 )`.  The multiplier `μ = (35+12i)/37`
has modulus one because `35² + 12² = 37²`, so the placement is a direct similarity
and preserves all distances.  Hence the seven placed points are again a
unit-distance realization of the same graph, and it is still not 3-colourable. -/

/-- `μ = (35 + 12i)/37`, the multiplier of (8.6). -/
noncomputable def mu : ℂ := ⟨35 / 37, 12 / 37⟩
/-- `τ = (−290 + 149i)/250`, the translation of (8.6). -/
noncomputable def tau : ℂ := ⟨-(290 / 250), 149 / 250⟩
/-- The placed vertex `z_g` of (8.6). -/
noncomputable def Q (a : Fin 7) : ℂ := mu * (P a + tau)

theorem mu_norm : ‖mu‖ = 1 := by
  rw [Complex.norm_def, Complex.normSq_mk]
  simp only [mu]
  norm_num

theorem mu_ne_zero : mu ≠ 0 := by
  intro h
  have h1 := mu_norm
  rw [h] at h1
  simp at h1

theorem Q_sub (a b : Fin 7) : Q a - Q b = mu * (P a - P b) := by
  simp only [Q]
  ring

theorem placed_dist (a b : Fin 7) : dist (Q a) (Q b) = dist (P a) (P b) := by
  rw [dist_eq_norm, dist_eq_norm, Q_sub, norm_mul, mu_norm, one_mul]

/-- The eleven edges of the placed graph of (8.6) still have length exactly one. -/
theorem placed_edges_unit : ∀ a b : Fin 7, Adj a b → dist (Q a) (Q b) = 1 :=
  fun a b h => by rw [placed_dist]; exact edges_unit a b h

/-- All twenty-one pairwise distances of the placed points are unchanged. -/
theorem placed_nonedges_not_unit : ∀ a b : Fin 7, ¬ Adj a b → dist (Q a) (Q b) ≠ 1 :=
  fun a b h => by rw [placed_dist]; exact nonedges_not_unit a b h

/-- The seven placed points are pairwise distinct. -/
theorem Q_injective : Function.Injective Q := by
  intro a b h
  apply P_injective
  have h2 : mu * (P a - P b) = 0 := by
    have h3 : Q a - Q b = 0 := by rw [h]; ring
    rwa [Q_sub] at h3
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 mu_ne_zero
  · exact sub_eq_zero.mp h3

#print axioms OAI.Audit.Moser.edges_unit
#print axioms OAI.Audit.Moser.nonedges_not_unit
#print axioms OAI.Audit.Moser.P_injective
#print axioms OAI.Audit.Moser.not_three_colorable
#print axioms OAI.Audit.Moser.placed_edges_unit
#print axioms OAI.Audit.Moser.placed_nonedges_not_unit
#print axioms OAI.Audit.Moser.Q_injective

end OAI.Audit.Moser
