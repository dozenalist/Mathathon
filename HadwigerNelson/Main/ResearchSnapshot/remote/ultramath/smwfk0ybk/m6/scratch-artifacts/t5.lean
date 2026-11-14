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
def P5 : Fin 6 → Finset (Fin 6) := fun i => if i.val % 2 = 0 then {5} else {1, 4}
def sig5 := cellSig 5 (fun j => if j = 3 ∨ j = 4 then 3 else 0)
example : Decidable (∀ i : Fin 6, 1 ≤ (P5 i).card) := inferInstance
example : Decidable (∀ i : Fin 6, (P5 i ∩ allowedO 6 5 (by norm_num) sig5 i).Nonempty) := inferInstance
example : Decidable (∀ i : Fin 6, Disjoint (P5 i) (P5 (i + 1))) := inferInstance
example : Decidable (∀ i : Fin 6, ∀ j : Fin 6, ¬ ((P5 i).card = 3 ∧ (P5 j).card = 3 ∧ P5 i ∪ P5 j = Finset.univ)) := inferInstance
example : Decidable ((Finset.univ.filter (fun i : Fin 6 => (P5 i).card = 3)).card ≤ 3) := inferInstance
example : Decidable (∀ i : Fin 6, (P5 i).card ≤ 6 - 3) := inferInstance
end T
