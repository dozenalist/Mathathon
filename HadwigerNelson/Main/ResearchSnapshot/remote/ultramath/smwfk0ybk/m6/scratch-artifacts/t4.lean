import Mathlib
namespace T
def cosSign (m : ZMod 6) : Bool := decide (m = 0 ∨ m = 1 ∨ m = 5)
def cellSig (l : ℕ) (c : Fin l → ZMod 6) : Fin 6 → Fin l → Bool :=
  fun i j => cosSign (c j + 1 - ((i.val : ℕ) : ZMod 6))
def predFin {l : ℕ} (hl : 0 < l) (j : Fin l) : Fin l :=
  ⟨(j.val + (l - 1)) % l, Nat.mod_lt _ hl⟩
def allowedO (k l : ℕ) (hl : 0 < l) (σ : Fin 6 → Fin l → Bool) (i : Fin 6) : Finset (Fin k) :=
  Finset.univ.filter (fun x : Fin k =>
    l ≤ x.val ∨ ∃ j : Fin l, x.val = j.val ∧ σ i (predFin hl j) = false ∧ σ i j = false)
def IsModel (k l : ℕ) (hl : 0 < l) (σ : Fin 6 → Fin l → Bool) (P : Fin 6 → Finset (Fin k)) : Prop :=
  (∀ i, 1 ≤ (P i).card) ∧
  (∀ i, (P i ∩ allowedO k l hl σ i).Nonempty) ∧
  (∀ i, Disjoint (P i) (P (i + 1))) ∧
  (∀ i j, ¬ ((P i).card = 3 ∧ (P j).card = 3 ∧ P i ∪ P j = Finset.univ)) ∧
  (Finset.univ.filter (fun i : Fin 6 => (P i).card = 3)).card ≤ 3
example : Decidable (IsModel 6 5 (by norm_num) (cellSig 5 (fun j => if j = 3 ∨ j = 4 then 3 else 0)) (fun i => if i.val % 2 = 0 then {5} else {1,4})) := inferInstance
example : IsModel 6 5 (by norm_num) (cellSig 5 (fun j => if j = 3 ∨ j = 4 then 3 else 0)) (fun i => if i.val % 2 = 0 then {5} else {1,4}) := by decide
end T
