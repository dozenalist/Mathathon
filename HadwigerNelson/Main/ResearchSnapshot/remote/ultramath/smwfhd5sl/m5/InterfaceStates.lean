/-
Interface state system at a cyclic centre: the k = 4 impossibility and the k = 6 models.

Machine-checked statements of INTERFACE-NOGO.md (Theorems 2 and 4):

  k4_ell3, k4_ell4 : at k = 4 the interface state system is unsatisfiable for EVERY sign matrix
                     and every cycle length ell in {3,4}  (the calibration, Theorem 2);
  k6_ell3, k6_ell4 : at k = 6 a palette system exists for ell = 3, 4 and EVERY sign matrix;
  k6_ell5, k6_ell6 : at k = 6 a palette system exists for ell = 5, 6 for the explicit ray
                     geometries of interface_csp_results.json (the no-go, Theorem 4).

Definitions are the paper's.  Labels are `Fin k`, the cycle labels are the labels `< ell`.
`inO σ i l` says `l` is not an endpoint of any positive edge at orbit position `i` (paper's
`O(e)`, Lemma 8.1); `inI` the same for negative edges.  A palette system has
`1 ≤ |P i| ≤ k-3` (general-k palette bound), each `P i` meets `O i` and `I i` (display (8.1)),
and consecutive palettes are disjoint (Corollary 5.4, display (5.7)).
-/
import Mathlib

namespace InterfaceStates

/-- Sign matrix: `σ i j = true` means `e_i · v_j > 0`. -/
abbrev Sig (ell : Nat) := Fin 6 → Fin ell → Bool

variable {k ell : Nat}

/-- `l` is not an endpoint of any positive edge: the paper's `O(e)`. -/
def inO (σ : Sig ell) (i : Fin 6) (l : Fin k) : Prop :=
  ∀ j : Fin ell, σ i j = true → l.val ≠ j.val ∧ l.val ≠ (j.val + 1) % ell

/-- `l` is not an endpoint of any negative edge: the paper's `I(e)`. -/
def inI (σ : Sig ell) (i : Fin 6) (l : Fin k) : Prop :=
  ∀ j : Fin ell, σ i j = false → l.val ≠ j.val ∧ l.val ≠ (j.val + 1) % ell

/-- Successor position on the six-cycle of directions. -/
def nxt (i : Fin 6) : Fin 6 := ⟨(i.val + 1) % 6, Nat.mod_lt _ (by norm_num)⟩

/-- A palette system satisfying (C1), (C2), (C3). -/
structure IsModel (σ : Sig ell) (P : Fin 6 → Finset (Fin k)) : Prop where
  card_pos : ∀ i, 1 ≤ (P i).card
  card_le : ∀ i, (P i).card ≤ k - 3
  meets_O : ∀ i, ∃ l ∈ P i, inO σ i l
  meets_I : ∀ i, ∃ l ∈ P i, inI σ i l
  disj : ∀ i, Disjoint (P i) (P (nxt i))

/-- A cycle label has both an incident edge of each sign, so it is never in `O` and `I`. -/
theorem not_inO_and_inI {σ : Sig ell} {i : Fin 6} {l : Fin k} (hlt : l.val < ell) :
    ¬ (inO σ i l ∧ inI σ i l) := by
  by_cases h : σ i ⟨l.val, hlt⟩ = true
  · intro hO
    exact absurd rfl (hO.1 ⟨l.val, hlt⟩ h).1
  · intro hI
    have h' : σ i ⟨l.val, hlt⟩ = false := by simpa using h
    exact absurd rfl (hI.2 ⟨l.val, hlt⟩ h').1

/-- An outsider (label `≥ ell`) lies in `O` and in `I`. -/
theorem outsider_inO {σ : Sig ell} {i : Fin 6} {l : Fin k} (hell : 0 < ell)
    (h : ell ≤ l.val) : inO σ i l := by
  intro j _
  refine ⟨by omega, ?_⟩
  have := Nat.mod_lt (j.val + 1) hell
  omega

theorem outsider_inI {σ : Sig ell} {i : Fin 6} {l : Fin k} (hell : 0 < ell)
    (h : ell ≤ l.val) : inI σ i l := by
  intro j _
  refine ⟨by omega, ?_⟩
  have := Nat.mod_lt (j.val + 1) hell
  omega

/-! ### k = 4: unsatisfiable for every sign matrix (Theorem 2) -/

/-- `ell = 4`: no palette meets both `O` and `I`, since `|P| ≤ 1` and `O ∩ I` is empty. -/
theorem k4_ell4 (σ : Sig 4) : ¬ ∃ P : Fin 6 → Finset (Fin 4), IsModel σ P := by
  rintro ⟨P, h⟩
  obtain ⟨l, hlP, hlO⟩ := h.meets_O 0
  obtain ⟨l', hl'P, hl'I⟩ := h.meets_I 0
  have hc : (P 0).card ≤ 1 := by have := h.card_le 0; omega
  have hll : l = l' := Finset.card_le_one.mp hc l hlP l' hl'P
  subst hll
  exact not_inO_and_inI (ell := 4) (by omega) ⟨hlO, hl'I⟩

/-- `ell = 3`: the only admissible label is the outsider `3`, so consecutive palettes meet. -/
theorem k4_ell3 (σ : Sig 3) : ¬ ∃ P : Fin 6 → Finset (Fin 4), IsModel σ P := by
  rintro ⟨P, h⟩
  have key : ∀ i, (⟨3, by norm_num⟩ : Fin 4) ∈ P i := by
    intro i
    obtain ⟨l, hlP, hlO⟩ := h.meets_O i
    obtain ⟨l', hl'P, hl'I⟩ := h.meets_I i
    have hc : (P i).card ≤ 1 := by have := h.card_le i; omega
    have hll : l = l' := Finset.card_le_one.mp hc l hlP l' hl'P
    subst hll
    have hl3 : l.val = 3 := by
      by_contra hne
      have hlt : l.val < 3 := by have := l.isLt; omega
      exact not_inO_and_inI (ell := 3) hlt ⟨hlO, hl'I⟩
    have hl : l = (⟨3, by norm_num⟩ : Fin 4) := Fin.ext hl3
    simpa [hl] using hlP
  exact (Finset.disjoint_left.mp (h.disj 0)) (key 0) (key (nxt 0))

/-! ### k = 6: models exist at all four lengths (Theorem 4) -/

/-- The alternating two-outsider palette, which works for every sign matrix. -/
def altPal (a b : Fin 6) : Fin 6 → Finset (Fin 6)
  | ⟨0, _⟩ => {a}
  | ⟨1, _⟩ => {b}
  | ⟨2, _⟩ => {a}
  | ⟨3, _⟩ => {b}
  | ⟨4, _⟩ => {a}
  | ⟨5, _⟩ => {b}

/-- Successor, made explicit so that `fin_cases` reduces it. -/
def nxt' : Fin 6 → Fin 6
  | ⟨0, _⟩ => ⟨1, by norm_num⟩
  | ⟨1, _⟩ => ⟨2, by norm_num⟩
  | ⟨2, _⟩ => ⟨3, by norm_num⟩
  | ⟨3, _⟩ => ⟨4, by norm_num⟩
  | ⟨4, _⟩ => ⟨5, by norm_num⟩
  | ⟨5, _⟩ => ⟨0, by norm_num⟩

theorem k6_ell3 (σ : Sig 3) :
    IsModel σ (altPal ⟨3, by norm_num⟩ ⟨4, by norm_num⟩) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [altPal]
  · intro i; fin_cases i <;> simp [altPal]
  · intro i; fin_cases i <;> simp [altPal] <;>
      exact outsider_inO (ell := 3) (by norm_num) (by norm_num)
  · intro i; fin_cases i <;> simp [altPal] <;>
      exact outsider_inI (ell := 3) (by norm_num) (by norm_num)
  · intro i; fin_cases i <;> simp [altPal, nxt]

theorem k6_ell4 (σ : Sig 4) :
    IsModel σ (altPal ⟨4, by norm_num⟩ ⟨5, by norm_num⟩) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [altPal]
  · intro i; fin_cases i <;> simp [altPal]
  · intro i; fin_cases i <;> simp [altPal] <;>
      exact outsider_inO (ell := 4) (by norm_num) (by norm_num)
  · intro i; fin_cases i <;> simp [altPal] <;>
      exact outsider_inI (ell := 4) (by norm_num) (by norm_num)
  · intro i; fin_cases i <;> simp [altPal, nxt]

/-- Ray cells of a geometry: `σ i j` is the sign of `cos(θ_j - i π/3)` for `θ_j` in cell
`c j`, using the six-cell description of INTERFACE-NOGO.md §1. -/
def cellSig (c : Fin ell → Nat) (i : Fin 6) (j : Fin ell) : Bool :=
  let m := (c j + 1 + 6 - i.val) % 6
  m == 0 || m == 1 || m == 5

/-- Palettes for the `ell = 5` model of interface_csp_results.json (cells 0,0,0,3,3). -/
def P5 : Fin 6 → Finset (Fin 6)
  | ⟨0, _⟩ => {⟨5, by norm_num⟩}
  | ⟨1, _⟩ => {⟨1, by norm_num⟩, ⟨4, by norm_num⟩}
  | ⟨2, _⟩ => {⟨5, by norm_num⟩}
  | ⟨3, _⟩ => {⟨1, by norm_num⟩, ⟨4, by norm_num⟩}
  | ⟨4, _⟩ => {⟨5, by norm_num⟩}
  | ⟨5, _⟩ => {⟨1, by norm_num⟩, ⟨4, by norm_num⟩}

/-- Palettes for the `ell = 6` model (cells 0,0,0,3,3,3). -/
def P6 : Fin 6 → Finset (Fin 6)
  | ⟨0, _⟩ => {⟨1, by norm_num⟩, ⟨4, by norm_num⟩}
  | ⟨1, _⟩ => {⟨2, by norm_num⟩, ⟨5, by norm_num⟩}
  | ⟨2, _⟩ => {⟨1, by norm_num⟩, ⟨4, by norm_num⟩}
  | ⟨3, _⟩ => {⟨2, by norm_num⟩, ⟨5, by norm_num⟩}
  | ⟨4, _⟩ => {⟨1, by norm_num⟩, ⟨4, by norm_num⟩}
  | ⟨5, _⟩ => {⟨2, by norm_num⟩, ⟨5, by norm_num⟩}

/-- Cells `0,0,0,3,3` for `ell = 5`. -/
def c5 : Fin 5 → Nat := fun j => if j.val < 3 then 0 else 3

/-- Cells `0,0,0,3,3,3` for `ell = 6`. -/
def c6 : Fin 6 → Nat := fun j => if j.val < 3 then 0 else 3

theorem k6_ell5 : IsModel (k := 6) (ell := 5) (cellSig c5) P5 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [P5]
  · intro i; fin_cases i <;> simp [P5]
  · intro i; fin_cases i <;> simp [P5]; all_goals (simp only [inO, cellSig]; decide)
  · intro i; fin_cases i <;> simp [P5]; all_goals (simp only [inI, cellSig]; decide)
  · intro i; fin_cases i <;> simp [P5, nxt]

theorem k6_ell6 : IsModel (k := 6) (ell := 6) (cellSig c6) P6 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [P6]
  · intro i; fin_cases i <;> simp [P6]
  · intro i; fin_cases i <;> simp [P6]; all_goals (simp only [inO, cellSig]; decide)
  · intro i; fin_cases i <;> simp [P6]; all_goals (simp only [inI, cellSig]; decide)
  · intro i; fin_cases i <;> simp [P6, nxt]

/-! ### The two packaged statements -/

/-- **Calibration.**  At `k = 4` the state level refutes every interface length in the range
`3 ≤ ell ≤ k` supplied by Proposition 7.1, for every sign matrix. -/
theorem state_level_complete_at_four :
    (∀ σ : Sig 3, ¬ ∃ P : Fin 6 → Finset (Fin 4), IsModel σ P) ∧
    (∀ σ : Sig 4, ¬ ∃ P : Fin 6 → Finset (Fin 4), IsModel σ P) :=
  ⟨k4_ell3, k4_ell4⟩

/-- **No-go.**  At `k = 6` the state level is silent: for every interface length
`ell ∈ {3,4,5,6}` some ray geometry admits a palette system, so no argument whose only
hypotheses are (C1)-(C3) can conclude `⊥`. -/
theorem state_level_silent_at_six :
    (∀ σ : Sig 3, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) ∧
    (∀ σ : Sig 4, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) ∧
    (∃ σ : Sig 5, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) ∧
    (∃ σ : Sig 6, ∃ P : Fin 6 → Finset (Fin 6), IsModel σ P) :=
  ⟨fun σ => ⟨_, k6_ell3 σ⟩, fun σ => ⟨_, k6_ell4 σ⟩,
   ⟨_, _, k6_ell5⟩, ⟨_, _, k6_ell6⟩⟩

end InterfaceStates
