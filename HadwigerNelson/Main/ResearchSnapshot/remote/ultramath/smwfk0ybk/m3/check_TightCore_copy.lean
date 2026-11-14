/-
  Tightened interface CSP at k = 6: the machine-checked core.

  Main content: the two constraints (C4) and (C5) of the previous run, added to
  the six-position interface system (C1)-(C3) of m5, do not change
  satisfiability at any interface length.  The mechanism is structural: the
  system is already satisfiable with palettes of size 1, where (C4) (no two
  complementary 3-sets) and (C5) (at most three ternary palettes) are vacuous.
  Hence `state_level_silent`: for ANY ray geometry and ANY interface length
  l with l + 2 <= k, there is a model.  At k = 6 this covers l = 3 and l = 4 for
  every ray geometry, with no enumeration.

  Labels are `Fin k`; the interface cycle is indexed by `Fin l` (so l > 0);
  `cellSig c i j = sign(e_i . v_j)` for a ray geometry given by cells
  `c : Fin l -> ZMod 6`, cf. INTERFACE-NOGO.md section 1.
-/
import Mathlib

namespace TightCSP

/-- `sign(cos(m * pi / 3))` for `m : ZMod 6`, as a `Bool` (`true` = `+1`).
There are no zeros: `cos(m pi / 3)` vanishes only for half-integer `m`. -/
def cosSign (m : ZMod 6) : Bool := decide (m = 0 ∨ m = 1 ∨ m = 5)

theorem cosSign_neg (m : ZMod 6) : cosSign (-m) = cosSign m := by
  revert m; decide

/-- The sign matrix of a ray geometry: `cellSig c i j = sign(e_i · v_j)`,
where `e_i = R^i e` and `v_j` is a ray whose cell is `c j`. -/
def cellSig (l : ℕ) (c : Fin l → ZMod 6) : Fin 6 → Fin l → Bool :=
  fun i j => cosSign (c j + 1 - ((i.val : ℕ) : ZMod 6))

/-- the predecessor of a cycle index -/
def predFin {l : ℕ} (hl : 0 < l) (j : Fin l) : Fin l :=
  ⟨(j.val + (l - 1)) % l, Nat.mod_lt _ hl⟩

/-- `O_i` of the paper's (8.1): the labels left after deleting the endpoints of
every positive edge, together with all labels outside the cycle. -/
def allowedO (k l : ℕ) (hl : 0 < l) (σ : Fin 6 → Fin l → Bool) (i : Fin 6) :
    Finset (Fin k) :=
  Finset.univ.filter (fun x : Fin k =>
    l ≤ x.val ∨ ∃ j : Fin l, x.val = j.val ∧ σ i (predFin hl j) = false ∧ σ i j = false)

/-- `I_i` of the paper's (8.1): the labels left after deleting the endpoints of
every negative edge, together with all labels outside the cycle. -/
def allowedI (k l : ℕ) (hl : 0 < l) (σ : Fin 6 → Fin l → Bool) (i : Fin 6) :
    Finset (Fin k) :=
  Finset.univ.filter (fun x : Fin k =>
    l ≤ x.val ∨ ∃ j : Fin l, x.val = j.val ∧ σ i (predFin hl j) = true ∧ σ i j = true)

/-- The six-position interface system with both global constraints:
(C1) `1 ≤ |P_i| ≤ k-3`,  (C2) `P_i` meets `O_i` and `I_i`,  (C3) `P_i ∩ P_{i+1} = ∅`,
(C4) no two of the six palettes are complementary 3-sets,
(C5) at most three of the six palettes are ternary. -/
def IsModel (k l : ℕ) (hl : 0 < l) (σ : Fin 6 → Fin l → Bool)
    (P : Fin 6 → Finset (Fin k)) : Prop :=
  (∀ i, 1 ≤ (P i).card) ∧
  (∀ i, (P i).card ≤ k - 3) ∧
  (∀ i, (P i ∩ allowedO k l hl σ i).Nonempty) ∧
  (∀ i, (P i ∩ allowedI k l hl σ i).Nonempty) ∧
  (∀ i, Disjoint (P i) (P (i + 1))) ∧
  (∀ i j, ¬ ((P i).card = 3 ∧ (P j).card = 3 ∧ P i ∪ P j = Finset.univ)) ∧
  (Finset.univ.filter (fun i : Fin 6 => (P i).card = 3)).card ≤ 3

/-! ### The two-outsider model: silence for every `l ≤ k - 2` -/

theorem parity_succ (i : Fin 6) :
    (((i + 1).val) % 2 = 0) ↔ ¬ (i.val % 2 = 0) := by
  fin_cases i <;> decide

/-- The alternating-singleton assignment is a model of the FULL tightened
system, for every sign matrix, whenever there are two labels outside the
cycle.  Here `u0`, `u1` are two such labels. -/
theorem alternating_isModel (k l : ℕ) (hl : 0 < l) (h4 : 4 ≤ k)
    (σ : Fin 6 → Fin l → Bool) (u0 u1 : Fin k) (h0 : l ≤ u0.val) (h1 : l ≤ u1.val)
    (hne : u0 ≠ u1) :
    IsModel k l hl σ (fun i => if i.val % 2 = 0 then {u0} else {u1}) := by
  have key : ∀ i : Fin 6,
      ((fun i : Fin 6 => if i.val % 2 = 0 then ({u0} : Finset (Fin k)) else {u1}) i).card
        = 1 := by
    intro i
    show (if i.val % 2 = 0 then ({u0} : Finset (Fin k)) else {u1}).card = 1
    split <;> simp
  have hO : ∀ i, u0 ∈ allowedO k l hl σ i := by
    intro i; simp [allowedO, h0]
  have hI : ∀ i, u0 ∈ allowedI k l hl σ i := by
    intro i; simp [allowedI, h0]
  have hO1 : ∀ i, u1 ∈ allowedO k l hl σ i := by
    intro i; simp [allowedO, h1]
  have hI1 : ∀ i, u1 ∈ allowedI k l hl σ i := by
    intro i; simp [allowedI, h1]
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i; rw [key i]
  · intro i; rw [key i]; omega
  · intro i
    by_cases hi : i.val % 2 = 0
    · refine ⟨u0, ?_⟩
      simp only [hi, if_true]
      exact Finset.mem_inter.mpr ⟨by simp, hO i⟩
    · refine ⟨u1, ?_⟩
      simp only [hi, if_false]
      exact Finset.mem_inter.mpr ⟨by simp, hO1 i⟩
  · intro i
    by_cases hi : i.val % 2 = 0
    · refine ⟨u0, ?_⟩
      simp only [hi, if_true]
      exact Finset.mem_inter.mpr ⟨by simp, hI i⟩
    · refine ⟨u1, ?_⟩
      simp only [hi, if_false]
      exact Finset.mem_inter.mpr ⟨by simp, hI1 i⟩
  · intro i
    have hpar := parity_succ i
    show Disjoint (if i.val % 2 = 0 then ({u0} : Finset (Fin k)) else {u1})
      (if (i + 1).val % 2 = 0 then ({u0} : Finset (Fin k)) else {u1})
    by_cases hi : i.val % 2 = 0
    · have hi' : ¬ ((i + 1).val % 2 = 0) := fun h => (hpar.mp h) hi
      rw [if_pos hi, if_neg hi']
      simp [hne]
    · have hi' : (i + 1).val % 2 = 0 := hpar.mpr hi
      rw [if_neg hi, if_pos hi']
      simp [Ne.symm hne]
  · intro i j h
    have h1 : ((fun i : Fin 6 => if i.val % 2 = 0 then ({u0} : Finset (Fin k))
      else {u1}) i).card = 3 := h.1
    rw [key i] at h1
    omega
  · have hempty : (Finset.univ.filter (fun i : Fin 6 =>
        ((fun i : Fin 6 => if i.val % 2 = 0 then ({u0} : Finset (Fin k))
          else {u1}) i).card = 3)) = ∅ := by
      apply Finset.filter_false_of_mem
      intro i _
      have := key i
      omega
    rw [hempty]
    simp

/-- **The state level is silent at every length `l ≤ k - 2`.**
For any ray geometry and any interface length `l` with `l + 2 ≤ k` and `k ≥ 4`,
the tightened system (C1)-(C5) has a model. -/
theorem state_level_silent (k l : ℕ) (hl : 0 < l) (hk : l + 2 ≤ k) (h4 : 4 ≤ k)
    (σ : Fin 6 → Fin l → Bool) :
    ∃ P : Fin 6 → Finset (Fin k), IsModel k l hl σ P := by
  have hlt : l < k := by omega
  refine ⟨fun i => if i.val % 2 = 0 then {(⟨l, hlt⟩ : Fin k)} else {(⟨l + 1, by omega⟩ : Fin k)},
    alternating_isModel k l hl h4 σ ⟨l, hlt⟩ ⟨l + 1, by omega⟩ (le_refl l) (by simp) ?_⟩
  intro h
  have := congrArg Fin.val h
  simp at this

/-! ### Explicit models at `l = 5` and `l = 6` at `k = 6` -/

/-- the ray geometry of the `l = 5` witness: cells `(0,0,0,3,3)` -/
def cells5 : Fin 5 → ZMod 6 := fun j => if j = 3 ∨ j = 4 then 3 else 0

/-- the ray geometry of the `l = 6` witness: cells `(0,0,0,3,3,3)` -/
def cells6 : Fin 6 → ZMod 6 := fun j => if 3 ≤ j.val then 3 else 0

/-- palettes `{5}, {1,4}, {5}, {1,4}, {5}, {1,4}` (labels `0..5`) -/
def P5 : Fin 6 → Finset (Fin 6) := fun i => if i.val % 2 = 0 then {5} else {1, 4}

/-- palettes `{1,4}, {2,5}, {1,4}, {2,5}, {1,4}, {2,5}` -/
def P6 : Fin 6 → Finset (Fin 6) := fun i => if i.val % 2 = 0 then {1, 4} else {2, 5}

/-- `l = 5` is satisfiable at `k = 6`, with (C1)-(C5): cells `(0,0,0,3,3)`.
Each conjunct is decided separately (the conjunction is too deep for the
instance search but each component is a finite decidable computation). -/
theorem model_five : IsModel 6 5 (by norm_num) (cellSig 5 cells5) P5 := by
  unfold IsModel
  exact ⟨by decide, by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- `l = 6` is satisfiable at `k = 6`, with (C1)-(C5): cells `(0,0,0,3,3,3)`. -/
theorem model_six : IsModel 6 6 (by norm_num) (cellSig 6 cells6) P6 := by
  unfold IsModel
  exact ⟨by decide, by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- Both witnesses use only palettes of size 1 or 2, so `(C4)` and `(C5)` hold
vacuously; this is the structural reason the tightening cannot bite. -/
theorem model_five_sizes : ∀ i, (P5 i).card ≤ 2 := by
  intro i; fin_cases i <;> decide

theorem model_six_sizes : ∀ i, (P6 i).card ≤ 2 := by
  intro i; fin_cases i <;> decide

/-! ### Cross-check of the encoding against the Python enumeration

The values below are the ones computed independently by `tight_csp.py`
(`oi_masks`); they pin down that the Lean `allowedO`/`allowedI` and the Python
`O_i`/`I_i` are the same object. -/

theorem O5_values : ∀ i : Fin 6, allowedO 6 5 (by norm_num) (cellSig 5 cells5) i =
    (if i.val < 3 then ({4, 5} : Finset (Fin 6)) else {1, 2, 5}) := by
  intro i; fin_cases i <;> decide

theorem I5_values : ∀ i : Fin 6, allowedI 6 5 (by norm_num) (cellSig 5 cells5) i =
    (if i.val < 3 then ({1, 2, 5} : Finset (Fin 6)) else {4, 5}) := by
  intro i; fin_cases i <;> decide

theorem O6_values : ∀ i : Fin 6, allowedO 6 6 (by norm_num) (cellSig 6 cells6) i =
    (if i.val < 3 then ({4, 5} : Finset (Fin 6)) else {1, 2}) := by
  intro i; fin_cases i <;> decide

theorem I6_values : ∀ i : Fin 6, allowedI 6 6 (by norm_num) (cellSig 6 cells6) i =
    (if i.val < 3 then ({1, 2} : Finset (Fin 6)) else {4, 5}) := by
  intro i; fin_cases i <;> decide

/-! ### The verdict at `k = 6` -/

/-- At `k = 6` the tightened system is satisfiable at interface lengths 3 and 4
for **every** ray geometry (36 resp. 216 geometries). -/
theorem k6_silent_three_four :
    (∀ σ : Fin 6 → Fin 3 → Bool,
        ∃ P : Fin 6 → Finset (Fin 6), IsModel 6 3 (by norm_num) σ P) ∧
      (∀ σ : Fin 6 → Fin 4 → Bool,
        ∃ P : Fin 6 → Finset (Fin 6), IsModel 6 4 (by norm_num) σ P) :=
  ⟨fun σ => state_level_silent 6 3 (by norm_num) (by norm_num) (by norm_num) σ,
   fun σ => state_level_silent 6 4 (by norm_num) (by norm_num) (by norm_num) σ⟩

/-- Hence the tightened system is satisfiable at `k = 6` at every interface
length `3 ≤ l ≤ k`, and no contradiction can be derived from `(C1)-(C5)`. -/
theorem k6_sat_all_lengths :
    (∃ σ : Fin 6 → Fin 3 → Bool, ∃ P : Fin 6 → Finset (Fin 6), IsModel 6 3 (by norm_num) σ P) ∧
    (∃ σ : Fin 6 → Fin 4 → Bool, ∃ P : Fin 6 → Finset (Fin 6), IsModel 6 4 (by norm_num) σ P) ∧
    (∃ σ : Fin 6 → Fin 5 → Bool, ∃ P : Fin 6 → Finset (Fin 6), IsModel 6 5 (by norm_num) σ P) ∧
    (∃ σ : Fin 6 → Fin 6 → Bool, ∃ P : Fin 6 → Finset (Fin 6), IsModel 6 6 (by norm_num) σ P) := by
  obtain ⟨P3, h3⟩ := state_level_silent 6 3 (by norm_num) (by norm_num) (by norm_num)
    (fun _ _ => true)
  obtain ⟨P4, h4⟩ := state_level_silent 6 4 (by norm_num) (by norm_num) (by norm_num)
    (fun _ _ => true)
  exact ⟨⟨_, P3, h3⟩, ⟨_, P4, h4⟩, ⟨_, P5, model_five⟩, ⟨_, P6, model_six⟩⟩

/-! ### The tightening is inert as a theorem (no enumeration)

Every model of (C1)-(C3) at `k >= 5` shrinks coordinatewise to a model with all
palettes of size `<= 2`, and such a model satisfies (C4) and (C5) vacuously.
Hence (C1)-(C3) is satisfiable iff (C1)-(C5) is, for every `k >= 5`, every `l`
and every sign matrix: the tightened decision problem is *provably* the same
problem.  (Found independently by member m10 on the board; verified and
machine-checked here.) -/

/-- the interface system with only (C1)-(C3) -/
def IsPlain (k l : ℕ) (hl : 0 < l) (σ : Fin 6 → Fin l → Bool)
    (P : Fin 6 → Finset (Fin k)) : Prop :=
  (∀ i, 1 ≤ (P i).card) ∧
  (∀ i, (P i).card ≤ k - 3) ∧
  (∀ i, (P i ∩ allowedO k l hl σ i).Nonempty) ∧
  (∀ i, (P i ∩ allowedI k l hl σ i).Nonempty) ∧
  (∀ i, Disjoint (P i) (P (i + 1)))

/-- **The shrinking step.** A palette meeting both allowed sets contains a
sub-palette of at most two labels meeting both. -/
theorem exists_small_subset {k : ℕ} {s O I : Finset (Fin k)}
    (hO : (s ∩ O).Nonempty) (hI : (s ∩ I).Nonempty) :
    ∃ q : Finset (Fin k), q ⊆ s ∧ q.Nonempty ∧ q.card ≤ 2 ∧
      (q ∩ O).Nonempty ∧ (q ∩ I).Nonempty := by
  obtain ⟨a, ha⟩ := hO
  obtain ⟨b, hb⟩ := hI
  rw [Finset.mem_inter] at ha hb
  rcases eq_or_ne a b with rfl | hne
  · exact ⟨{a}, by intro x hx; rw [Finset.mem_singleton] at hx; rw [hx]; exact ha.1,
      ⟨a, Finset.mem_singleton_self a⟩, by simp,
      ⟨a, Finset.mem_inter.mpr ⟨Finset.mem_singleton_self a, ha.2⟩⟩,
      ⟨a, Finset.mem_inter.mpr ⟨Finset.mem_singleton_self a, hb.2⟩⟩⟩
  · refine ⟨{a, b}, ?_, ⟨a, Finset.mem_insert_self a {b}⟩, ?_,
      ⟨a, Finset.mem_inter.mpr ⟨Finset.mem_insert_self a {b}, ha.2⟩⟩,
      ⟨b, Finset.mem_inter.mpr ⟨Finset.mem_insert_of_mem (Finset.mem_singleton_self b), hb.2⟩⟩⟩
    · intro x hx
      rw [Finset.mem_insert, Finset.mem_singleton] at hx
      rcases hx with rfl | rfl
      · exact ha.1
      · exact hb.1
    · rw [Finset.card_insert_of_notMem (by simp [hne]), Finset.card_singleton]

/-- **(C1)-(C3) satisfiable implies (C1)-(C5) satisfiable with all palettes of
size `<= 2`**, at every `k >= 5`. -/
theorem tight_of_plain (k l : ℕ) (hl : 0 < l) (hk : 5 ≤ k)
    (σ : Fin 6 → Fin l → Bool) (P : Fin 6 → Finset (Fin k)) (h : IsPlain k l hl σ P) :
    ∃ Q : Fin 6 → Finset (Fin k), (∀ i, (Q i).card ≤ 2) ∧ IsModel k l hl σ Q := by
  obtain ⟨-, h2, hO, hI, hdisj⟩ := h
  have key : ∀ i, ∃ q : Finset (Fin k), q ⊆ P i ∧ q.Nonempty ∧ q.card ≤ 2 ∧
      (q ∩ allowedO k l hl σ i).Nonempty ∧ (q ∩ allowedI k l hl σ i).Nonempty :=
    fun i => exists_small_subset (hO i) (hI i)
  let Q : Fin 6 → Finset (Fin k) := fun i => Classical.choose (key i)
  have hQsub : ∀ i, Q i ⊆ P i := fun i => (Classical.choose_spec (key i)).1
  have hQne : ∀ i, (Q i).Nonempty := fun i => (Classical.choose_spec (key i)).2.1
  have hQcard : ∀ i, (Q i).card ≤ 2 := fun i => (Classical.choose_spec (key i)).2.2.1
  have hQO : ∀ i, (Q i ∩ allowedO k l hl σ i).Nonempty :=
    fun i => (Classical.choose_spec (key i)).2.2.2.1
  have hQI : ∀ i, (Q i ∩ allowedI k l hl σ i).Nonempty :=
    fun i => (Classical.choose_spec (key i)).2.2.2.2
  refine ⟨Q, hQcard, fun i => ?_, fun i => ?_, hQO, hQI, fun i => ?_, fun i j hcon => ?_, ?_⟩
  · exact Finset.card_pos.mpr (hQne i)
  · have := hQcard i; omega
  · exact (hdisj i).mono (hQsub i) (hQsub (i + 1))
  · have := hQcard i; omega
  · have hempty : (Finset.univ.filter (fun i : Fin 6 => (Q i).card = 3)) = ∅ := by
      apply Finset.filter_false_of_mem
      intro i _
      have := hQcard i; omega
    rw [hempty]; simp

/-- **The tightened decision problem is the plain one**, for every `k >= 5`,
every interface length `l` and every sign matrix. -/
theorem sat_tight_iff_sat_plain (k l : ℕ) (hl : 0 < l) (hk : 5 ≤ k)
    (σ : Fin 6 → Fin l → Bool) :
    (∃ P : Fin 6 → Finset (Fin k), IsModel k l hl σ P) ↔
      (∃ P : Fin 6 → Finset (Fin k), IsPlain k l hl σ P) := by
  constructor
  · rintro ⟨P, h1, h2, hO, hI, hd, -, -⟩
    exact ⟨P, h1, h2, hO, hI, hd⟩
  · rintro ⟨P, h⟩
    obtain ⟨Q, -, hQ⟩ := tight_of_plain k l hl hk σ P h
    exact ⟨Q, hQ⟩


end TightCSP

#print axioms TightCSP.state_level_silent
#print axioms TightCSP.k6_silent_three_four
#print axioms TightCSP.model_five
#print axioms TightCSP.model_six
#print axioms TightCSP.O5_values
#print axioms TightCSP.I6_values
#print axioms TightCSP.tight_of_plain
#print axioms TightCSP.sat_tight_iff_sat_plain
