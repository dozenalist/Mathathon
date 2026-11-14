/-
RR127 / SAIR Mathathon problem 127 -- Level 3 reusable foundation.

The staircase bridge for gap partitions, kernel-checked.

Contract (frozen; see RogersRamanujan/Main/DECISIONS.md):
  A partition is a descending list of positive integers; [] is the partition of 0.
  D_n = {lambda of weight n : lambda_i >= lambda_{i+1} + 2 for every i}.
  For lambda in D_n of length k,  mu_i = lambda_i - (2(k-i)+1)  (1-based i)
  is a nonnegative list of length k and weight n - k^2, and adding the staircase
  back is inverse to subtracting it.

Scope of this file: the staircase subtraction/addition pair as plain maps on
List Nat, with both inverse laws, the `lambda_1 >= 2(k-1)+1` bound that makes
natural-number subtraction non-truncating, the exact weight change, and
nonnegativity of the coordinates.  It is deliberately Mathlib-free: this VM
cannot elaborate `import Mathlib` (the 6.4 GB olean import does not fit the
available memory and page cache; measured, see Lean/README.md).  Only core
`omega` and `simp` automation is used, no `sorry`, no custom axiom.

Verification command:
  lean RogersRamanujan/Lean/Staircase.lean
-/
import Init

namespace RR127

/-- All entries are positive. -/
def Pos (l : List Nat) : Prop := ∀ x ∈ l, 0 < x

/-- The two-sided gap condition, as a structural predicate. -/
def Gap : List Nat → Prop
  | [] => True
  | [_] => True
  | a :: b :: rest => b + 2 ≤ a ∧ Gap (b :: rest)

/-! ## The two staircase maps -/

/-- Subtract the staircase of length `k`: the `i`-th entry of
`subStair [l1,...,lk]` is `l_i - (2(k-i)+1)`.  Recursion is structural on the
tail, so each step sees the length of the part it has not yet processed. -/
def subStair : List Nat → List Nat
  | [] => []
  | a :: rest => (a - (2 * rest.length + 1)) :: subStair rest

/-- Add the staircase back. -/
def addStair : List Nat → List Nat
  | [] => []
  | m :: ms => (m + (2 * ms.length + 1)) :: addStair ms

@[simp] theorem length_subStair : ∀ l : List Nat, (subStair l).length = l.length
  | [] => rfl
  | a :: rest => by simp [subStair, length_subStair rest]

@[simp] theorem length_addStair : ∀ l : List Nat, (addStair l).length = l.length
  | [] => rfl
  | m :: ms => by simp [addStair, length_addStair ms]

/-! ## The bound that makes natural-number subtraction non-truncating -/

theorem pos_of_cons {a : Nat} {rest : List Nat} (h : Pos (a :: rest)) : Pos rest := by
  intro x hx
  exact h x (by simp [hx])

theorem gap_tail {a b : Nat} {rest : List Nat} (h : Gap (a :: b :: rest)) :
    Gap (b :: rest) := h.2

/-- A positive gap partition satisfies `lambda_1 >= 2*(k-1)+1`. -/
theorem head_bound : ∀ {a : Nat} {rest : List Nat},
    Pos (a :: rest) → Gap (a :: rest) → 2 * rest.length + 1 ≤ a
  | a, [], hp, _ => by
    have ha : 0 < a := hp a (by simp)
    simp only [List.length_nil]
    omega
  | a, b :: t, hp, hg => by
    have hb : b + 2 ≤ a := hg.1
    have ih : 2 * t.length + 1 ≤ b := head_bound (pos_of_cons hp) (gap_tail hg)
    simp only [List.length_cons]
    omega

/-! ## Both inverse laws -/

/-- `addStair` is a left inverse of `subStair` on positive gap partitions. -/
theorem addStair_subStair : ∀ (l : List Nat), Pos l → Gap l → addStair (subStair l) = l
  | [], _, _ => rfl
  | a :: rest, hp, hg => by
    have h1 : 2 * rest.length + 1 ≤ a := head_bound hp hg
    have hpos : Pos rest := pos_of_cons hp
    have hgap : Gap rest := by
      cases rest with
      | nil => trivial
      | cons b t => exact gap_tail hg
    have ih : addStair (subStair rest) = rest := addStair_subStair rest hpos hgap
    simp only [subStair, addStair, length_subStair, ih]
    rw [Nat.sub_add_cancel h1]

/-- `subStair` is a left inverse of `addStair`.  No hypothesis is needed: the
staircase entry used at each step is exactly the constant that was added. -/
theorem subStair_addStair : ∀ (l : List Nat), subStair (addStair l) = l
  | [] => rfl
  | m :: ms => by
    have ih : subStair (addStair ms) = ms := subStair_addStair ms
    simp only [addStair, subStair, length_addStair, ih]
    rw [Nat.add_sub_cancel]

/-! ## Exact weight change -/

/-- Adding a staircase of length `k` adds exactly `k * k` to the weight. -/
theorem sum_addStair : ∀ (l : List Nat), (addStair l).sum = l.sum + l.length * l.length
  | [] => by simp [addStair]
  | m :: ms => by
    have ih : (addStair ms).sum = ms.sum + ms.length * ms.length := sum_addStair ms
    simp only [addStair, List.sum_cons, List.length_cons, ih]
    have hsq : (ms.length + 1) * (ms.length + 1)
        = ms.length * ms.length + 2 * ms.length + 1 := by
      rw [Nat.succ_mul, Nat.mul_succ]
      omega
    rw [hsq]
    omega

/-- A member of `D_n` of length `k` has staircase coordinates of weight `n - k^2`. -/
theorem weight_subStair {n : Nat} {lam : List Nat} (hpos : Pos lam) (hgap : Gap lam)
    (hsum : lam.sum = n) : (subStair lam).sum = n - lam.length * lam.length := by
  have key : (addStair (subStair lam)).sum
      = (subStair lam).sum + lam.length * lam.length := by
    rw [sum_addStair, length_subStair]
  rw [addStair_subStair lam hpos hgap] at key
  omega

/-! ## Nonnegativity of the staircase coordinates -/

/-- Every staircase coordinate of a positive gap partition is nonnegative. -/
theorem subStair_nonneg : ∀ (l : List Nat), Pos l → Gap l → ∀ x ∈ subStair l, 0 ≤ x
  | [], _, _, _, hx => by simp [subStair] at hx
  | a :: rest, hp, hg, x, hx => by
    have h1 : 2 * rest.length + 1 ≤ a := head_bound hp hg
    have hpos : Pos rest := pos_of_cons hp
    have hgap : Gap rest := by
      cases rest with
      | nil => trivial
      | cons b t => exact gap_tail hg
    simp only [subStair, List.mem_cons] at hx
    rcases hx with hx | hx
    · rw [hx]; omega
    · exact subStair_nonneg rest hpos hgap x hx

end RR127

#print axioms RR127.head_bound
#print axioms RR127.addStair_subStair
#print axioms RR127.subStair_addStair
#print axioms RR127.sum_addStair
#print axioms RR127.weight_subStair
#print axioms RR127.subStair_nonneg
