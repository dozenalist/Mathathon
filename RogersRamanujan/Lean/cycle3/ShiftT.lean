-- GENERATED FILE -- do not edit. Assembled by build.py from
--   RogersRamanujan/Lean/Staircase.lean (sha256 c7acbcd74866958596acc458a7231939ebe01969a0723179bfdaaf263cbeb280)
-- plus the cycle-3 block(s) listed in Lean/cycle3/README.md.
-- The Staircase.lean part is byte-identical to the source slice.
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

/-! ## Cycle 3, member m2, direction B: the same-weight shift `T` -/

namespace Shift

/-! ### Definitions -/

/-- The same-weight shift, on a list of length `k`:
`T(lam)_i = lam_i - k + 2i - 1`  (1-based `i`).
Encoded as "subtract the staircase of `Staircase.lean`, then add the constant
`k`", i.e. `T(lam) = (subStair lam).map (· + k)`, which is literally
`T(lam)_i = mu_i + k`.  The subtraction is the staircase subtraction, whose
non-truncation is exactly `head_bound`; the addition of `k` never truncates. -/
def shiftT (l : List Nat) : List Nat := (subStair l).map (fun x => x + l.length)

/-- The candidate inverse of `shiftT`: `lam_i = b_i + k - 2i + 1`, encoded as
"add the staircase back, then subtract the constant `k`". -/
def shiftInv (l : List Nat) : List Nat := (addStair l).map (fun x => x - l.length)

/-- Weakly decreasing list (a partition is allowed to be empty, and ties are
allowed; `Gap` is the strict two-step version). -/
def WeakDec : List Nat → Prop
  | [] => True
  | [_] => True
  | a :: b :: rest => b ≤ a ∧ WeakDec (b :: rest)

/-! ### Elementary list arithmetic -/

theorem sum_map_add : ∀ (l : List Nat) (c : Nat),
    (l.map (fun x => x + c)).sum = l.sum + c * l.length
  | [], _ => rfl
  | x :: xs, c => by
    have ih : (xs.map (fun x => x + c)).sum = xs.sum + c * xs.length := sum_map_add xs c
    show x + c + (xs.map (fun x => x + c)).sum = x + xs.sum + c * (xs.length + 1)
    rw [ih, Nat.mul_succ]
    omega

theorem addStair_map_add : ∀ (l : List Nat) (c : Nat),
    addStair (l.map (fun x => x + c)) = (addStair l).map (fun x => x + c)
  | [], _ => rfl
  | x :: xs, c => by
    have ih := addStair_map_add xs c
    have hlen : (List.map (fun x => x + c) xs).length = xs.length := List.length_map ..
    show ((x + c) + (2 * (List.map (fun x => x + c) xs).length + 1))
          :: addStair (List.map (fun x => x + c) xs)
        = ((x + (2 * xs.length + 1)) + c) :: List.map (fun x => x + c) (addStair xs)
    rw [hlen, ih]
    congr 1
    omega

theorem map_add_sub_cancel (l : List Nat) (c : Nat) :
    (l.map (fun x => x + c)).map (fun x => x - c) = l := by
  induction l with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons, ih, Nat.add_sub_cancel]

theorem map_sub_add_of_le : ∀ (l : List Nat) (c : Nat), (∀ x ∈ l, c ≤ x) →
    (l.map (fun x => x - c)).map (fun x => x + c) = l
  | [], _, _ => rfl
  | x :: xs, c, h => by
    have hx : c ≤ x := h x (List.mem_cons_self ..)
    have hxs : ∀ y ∈ xs, c ≤ y := fun y hy => h y (List.mem_cons_of_mem _ hy)
    have ih := map_sub_add_of_le xs c hxs
    simp only [List.map_cons, ih, Nat.sub_add_cancel hx]

/-- Adding the staircase and then subtracting a constant cancels against the
staircase subtraction: no hypothesis on the list is needed, `omega` disposes of
the truncation. -/
theorem subStair_addStair_map_sub : ∀ (l : List Nat) (c : Nat),
    subStair ((addStair l).map (fun x => x - c)) = l.map (fun x => x - c)
  | [], _ => rfl
  | x :: xs, c => by
    have ih := subStair_addStair_map_sub xs c
    simp only [addStair, List.map_cons, subStair, List.length_map, ih]
    congr 1
    omega

/-! ### Length is retained as data -/

@[simp] theorem length_shiftT (l : List Nat) : (shiftT l).length = l.length := by
  simp [shiftT]

@[simp] theorem length_shiftInv (l : List Nat) : (shiftInv l).length = l.length := by
  simp [shiftInv]

/-! ### (i) `T` preserves the weight exactly -/

theorem sum_shiftT {lam : List Nat} (hp : Pos lam) (hg : Gap lam) :
    (shiftT lam).sum = lam.sum := by
  have h1 : (shiftT lam).sum = (subStair lam).sum + lam.length * lam.length := by
    simp only [shiftT, length_subStair, sum_map_add]
  have h2 : lam.sum = (subStair lam).sum + lam.length * lam.length := by
    have key : (addStair (subStair lam)).sum
        = (subStair lam).sum + lam.length * lam.length := by
      rw [sum_addStair, length_subStair]
    rw [addStair_subStair lam hp hg] at key
    exact key
  rw [h1, h2]

/-! ### (ii) The image satisfies the `B_n` membership condition `k <= entry` -/

theorem mem_shiftT_ge {lam : List Nat} :
    ∀ x ∈ shiftT lam, lam.length ≤ x := by
  intro x hx
  obtain ⟨y, _, rfl⟩ := List.mem_map.1 hx
  omega

/-- The `(iv)` statement in pointwise membership form: the entries of `T(lam)`
are exactly the staircase coordinates shifted up by `k`. -/
theorem mem_shiftT_iff (l : List Nat) (x : Nat) :
    x ∈ shiftT l ↔ ∃ y ∈ subStair l, x = y + l.length := by
  simp only [shiftT, List.mem_map]
  constructor
  · rintro ⟨y, hy, h⟩; exact ⟨y, hy, h.symm⟩
  · rintro ⟨y, hy, h⟩; exact ⟨y, hy, h.symm⟩

/-- `(iv)` literally, as a pointwise statement on indices (`getElem?` so that no
length bookkeeping is needed). -/
theorem shiftT_entry (l : List Nat) (i : Nat) :
    (shiftT l)[i]? = ((subStair l)[i]?).map (fun x => x + l.length) := by
  simp [shiftT]

/-- The inverse formula, pointwise. -/
theorem shiftInv_entry (l : List Nat) (i : Nat) :
    (shiftInv l)[i]? = ((addStair l)[i]?).map (fun x => x - l.length) := by
  simp [shiftInv]

/-! ### (iii) Both inverse laws, on the correctly stated subtypes -/

/-- `shiftInv` is a left inverse of `shiftT` on positive gap partitions (so `T`
is injective there).  Hypotheses `Pos`/`Gap` are the domain `D_n`. -/
theorem shiftInv_shiftT {lam : List Nat} (hp : Pos lam) (hg : Gap lam) :
    shiftInv (shiftT lam) = lam := by
  have h1 : shiftInv (shiftT lam)
      = (addStair (shiftT lam)).map (fun x => x - lam.length) := by
    simp only [shiftInv, length_shiftT]
  rw [h1]
  have h2 : addStair (shiftT lam)
      = (addStair (subStair lam)).map (fun x => x + lam.length) := by
    simp only [shiftT]
    exact addStair_map_add (subStair lam) lam.length
  rw [h2, addStair_subStair lam hp hg, map_add_sub_cancel]

/-- `shiftT` is a left inverse of `shiftInv` on the `B_n`-shaped subtype:
every entry at least the length.  Length is retained as data (it is the
`l.length` in the statement). -/
theorem shiftT_shiftInv {b : List Nat} (h : ∀ x ∈ b, b.length ≤ x) :
    shiftT (shiftInv b) = b := by
  have h1 : shiftT (shiftInv b)
      = (subStair (shiftInv b)).map (fun x => x + b.length) := by
    simp only [shiftT, length_shiftInv]
  rw [h1]
  have h2 : subStair (shiftInv b) = b.map (fun x => x - b.length) := by
    simp only [shiftInv]
    exact subStair_addStair_map_sub b b.length
  rw [h2, map_sub_add_of_le b b.length h]

end Shift

#print axioms RR127.sum_map_add
#print axioms RR127.Shift.addStair_map_add
#print axioms RR127.Shift.map_add_sub_cancel
#print axioms RR127.Shift.map_sub_add_of_le
#print axioms RR127.Shift.subStair_addStair_map_sub
#print axioms RR127.Shift.length_shiftT
#print axioms RR127.Shift.length_shiftInv
#print axioms RR127.Shift.sum_shiftT
#print axioms RR127.Shift.mem_shiftT_ge
#print axioms RR127.Shift.mem_shiftT_iff
#print axioms RR127.Shift.shiftT_entry
#print axioms RR127.Shift.shiftInv_entry
#print axioms RR127.Shift.shiftInv_shiftT
#print axioms RR127.Shift.shiftT_shiftInv

end RR127

#print axioms RR127.head_bound
#print axioms RR127.addStair_subStair
#print axioms RR127.subStair_addStair
#print axioms RR127.sum_addStair
#print axioms RR127.weight_subStair
#print axioms RR127.subStair_nonneg
