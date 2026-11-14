/-
  Repair of m16's Corollary 3.1 at k = 6 -- machine-checked core.

  Direction d7, member m8.  See REPORT.md in this directory.

  What is checked here:

  (1) GEOMETRY.  With  u = 5/6 + i*sqrt(11)/6  (= e^{i gamma_0}, the paper's
      constant  cos gamma_0 = 5/6,  so that |1 - u| = 1/sqrt 3)  and
      omega = e^{2 pi i/3}, the three points  z_j = lam * omega^j,  lam = 1 - u,
      are pairwise at distance exactly 1 and satisfy |z_j| = 1/sqrt 3.  Hence the
      three forced sums  x + e^{i(t+2j kappa)} + e^{i(t+pi+gamma_0+2j kappa)}  of
      the alternation engine form a unit equilateral triangle.  (The engine's own
      statement uses only that; the measure-theoretic inputs are the paper's
      Lemma 5.2, which is not formalised here.)

  (2) PIGEONHOLE.  Three pairwise unit-distance points cannot be properly coloured
      with two labels.  This is the last step of the engine (Lemma 6.4 of the
      paper, Theorem A of m16, Theorem R1 of REPORT.md).

  (3) RIGIDITY.  If v lies on the unit circle and |1 + v|^2 = 1/3 then Re v = -5/6.
      So the shift delta of the engine is forced to cos delta = -5/6 (delta =
      +-(pi - gamma_0)): the engine has no freedom in the shift, hence no
      adaptive-shift strengthening can turn the confined statement into the
      global one.  (Used in REPORT.md, Section 3.)

  (4) TWO-VALUED SECTOR FIELDS.  Let n = 6m sector positions (rotation by
      kappa = pi/3 is the shift i -> i + m) and let V : ZMod n -> Bool be a
      two-valued sector palette field.  If the sixty-degree exclusion (5.7) holds,
      V (i + m) = !(V i), and if the transport (5.3) holds at the sector offsets
      m + k, k in {-1,0,1}, then V is constant, contradicting (5.7).  Hence NO
      two-valued translation-invariant sector field satisfies (5.7) + (5.3) at
      any resolution.  This is the finite content of REPORT.md Section 5; the
      three-valued and six-valued free-label models that DO satisfy (5.7) + (5.3)
      are checked exhaustively in verify_sector.py.

  Build:   source scripts/env4341.sh && lean repair31.lean        (Lean 4.34.1)
-/
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FinCases

namespace Repair31

open Complex

noncomputable section

/-- `omega = e^{2 pi i / 3}`, a primitive cube root of unity. -/
def w : ℂ := ⟨-1 / 2, Real.sqrt 3 / 2⟩

/-- `u = e^{i gamma_0}` with `cos gamma_0 = 5/6`, `sin gamma_0 = sqrt 11 / 6`. -/
def u : ℂ := ⟨5 / 6, Real.sqrt 11 / 6⟩

/-- `lam = 1 - u`: the vector of the forced equilateral triangle. -/
def lam : ℂ := 1 - u

/-- The three forced points, translated so that the centre is `0`. -/
def z (j : Fin 3) : ℂ := lam * w ^ (j : ℕ)

lemma sq_sqrt3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
lemma sq_sqrt11 : Real.sqrt 11 ^ 2 = 11 := Real.sq_sqrt (by norm_num)

lemma normSq_w : normSq w = 1 := by
  rw [normSq_apply]
  simp only [w]
  nlinarith [sq_sqrt3]

lemma normSq_lam : normSq lam = 1 / 3 := by
  rw [normSq_apply]
  simp only [lam, u, Complex.sub_re, Complex.sub_im, Complex.one_re, Complex.one_im]
  nlinarith [sq_sqrt11]

lemma normSq_one_sub_w : normSq (1 - w) = 3 := by
  rw [normSq_apply]
  simp only [w, Complex.sub_re, Complex.sub_im, Complex.one_re, Complex.one_im]
  nlinarith [sq_sqrt3]

lemma normSq_one_add_w : normSq (1 + w) = 1 := by
  rw [normSq_apply]
  simp only [w, Complex.add_re, Complex.add_im, Complex.one_re, Complex.one_im]
  nlinarith [sq_sqrt3]

/-- `|1 - u| = 1/sqrt 3`: the forced triangle has circumradius `1/sqrt 3`. -/
lemma normSq_one_sub_u : normSq (1 - u) = 1 / 3 := normSq_lam

lemma norm_eq_one_of_normSq (a : ℂ) (h : normSq a = 1) : ‖a‖ = 1 := by
  have h2 : ‖a‖ ^ 2 = 1 := by rw [← normSq_eq_norm_sq, h]
  nlinarith [norm_nonneg a]

lemma z_zero : z 0 = lam := by simp [z]
lemma z_one : z 1 = lam * w := by simp [z]
lemma z_two : z 2 = lam * w ^ 2 := by simp [z]

lemma dist_z01 : ‖z 0 - z 1‖ = 1 := by
  apply norm_eq_one_of_normSq
  rw [z_zero, z_one, show lam - lam * w = lam * (1 - w) by ring, normSq_mul, normSq_lam,
    normSq_one_sub_w]
  norm_num

lemma dist_z12 : ‖z 1 - z 2‖ = 1 := by
  apply norm_eq_one_of_normSq
  rw [z_one, z_two, show lam * w - lam * w ^ 2 = lam * w * (1 - w) by ring, normSq_mul,
    normSq_mul, normSq_lam, normSq_w, normSq_one_sub_w]
  norm_num

lemma dist_z02 : ‖z 0 - z 2‖ = 1 := by
  apply norm_eq_one_of_normSq
  rw [z_zero, z_two]
  have h : lam - lam * w ^ 2 = lam * (1 - w) * (1 + w) := by ring
  rw [h, normSq_mul, normSq_mul, normSq_lam, normSq_one_sub_w, normSq_one_add_w]
  norm_num

/-- Two labels cannot properly colour three pairwise unit-distance points. -/
theorem fin2_three_distinct (a b c : Fin 2) (h1 : a ≠ b) (h2 : b ≠ c) (h3 : a ≠ c) :
    False := by
  fin_cases a <;> fin_cases b <;> fin_cases c <;> simp_all

/-- **The engine's last step, machine-checked with the paper's explicit constants.**
No function on the plane that separates every unit-distance pair can take only two
values -- already because the three forced points `z 0, z 1, z 2` are pairwise at
distance one. -/
theorem no_proper_two_colouring (f : ℂ → Fin 2)
    (hprop : ∀ p q : ℂ, ‖p - q‖ = 1 → f p ≠ f q) : False :=
  fin2_three_distinct (f (z 0)) (f (z 1)) (f (z 2))
    (hprop _ _ dist_z01) (hprop _ _ dist_z12) (hprop _ _ dist_z02)

/-! ### Rigidity of the engine's shift -/

lemma normSq_one_add (v : ℂ) : normSq (1 + v) = normSq v + 2 * v.re + 1 := by
  rw [normSq_apply, normSq_apply]
  simp
  ring

/-- **Rigidity.**  If `v` is a unit vector and `|1 + v|^2 = 1/3` (the size that makes the
three forced sums an equilateral triangle of side one), then `Re v = -5/6`, i.e.
`v = e^{+-i (pi - gamma_0)}`.  So the shift of the sum construction is forced. -/
theorem rigidity (v : ℂ) (hv : normSq v = 1) (h : normSq (1 + v) = 1 / 3) :
    v.re = -5 / 6 := by
  rw [normSq_one_add, hv] at h
  linarith

/-! ### Two-valued sector fields -/

/-- **No two-valued sector field satisfies (5.7) and the transport (5.3).**
`n = 6 * m` sector positions; the rotation by `kappa = pi/3` is the shift `i ↦ i + m`,
and the transport offsets are `m + k`, `k ∈ {-1,0,1}`: `hplus` is `k = 1`, `hminus` is
`k = -1`, `h57` is `k = 0`.  Two values force `V` to be constant, which contradicts the
sixty-degree exclusion.  (The proof uses `hplus` only.) -/
theorem no_two_valued_sector_field (n m : ℕ) (V : ZMod n → Bool)
    (h57 : ∀ i : ZMod n, V (i + (m : ZMod n)) = !(V i))
    (hplus : ∀ i : ZMod n, V (i + (m : ZMod n) + 1) = !(V i))
    (_hminus : ∀ i : ZMod n, V (i + (m : ZMod n) - 1) = !(V i)) : False := by
  have step : ∀ j : ZMod n, V (j + 1) = V j := by
    intro j
    have h1 := h57 (j - (m : ZMod n))
    have h2 := hplus (j - (m : ZMod n))
    rw [show j - (m : ZMod n) + (m : ZMod n) = j by ring] at h1
    rw [show j - (m : ZMod n) + (m : ZMod n) + 1 = j + 1 by ring] at h2
    rw [← h1] at h2
    exact h2
  have const : ∀ (t : ℕ) (j : ZMod n), V (j + (t : ZMod n)) = V j := by
    intro t
    induction t with
    | zero => intro j; simp
    | succ s ih =>
      intro j
      rw [show j + ((s + 1 : ℕ) : ZMod n) = (j + (s : ZMod n)) + 1 by push_cast; ring,
        step, ih]
  have h0 := const m 0
  rw [zero_add] at h0
  have h1 := h57 0
  rw [zero_add] at h1
  rw [← h0] at h1
  exact (by cases V (0 : ZMod n) <;> simp_all)

end

end Repair31

/-! ### Axiom audit (the three headline statements) -/

#print axioms Repair31.no_proper_two_colouring
#print axioms Repair31.rigidity
#print axioms Repair31.no_two_valued_sector_field
