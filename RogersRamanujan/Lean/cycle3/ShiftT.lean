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
    simp only [addStair, List.map_cons, subStair, List.length_map, length_addStair, ih]
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

#print axioms RR127.Shift.sum_map_add
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

/-! ### Bonus: the order facts that make `T : D_n → B_n` a bijection -/

namespace Shift

/-! #### The order half: `T(lam)` is a partition -/

theorem weakDec_map_add : ∀ (l : List Nat) (c : Nat), WeakDec l →
    WeakDec (l.map (fun x => x + c))
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | a :: b :: t, c, h => by
    have hba : b ≤ a := h.1
    have ih := weakDec_map_add (b :: t) c h.2
    simp only [List.map_cons]
    exact ⟨by omega, ih⟩

/-- The staircase coordinates of a positive gap partition are weakly decreasing.
(Same proof as `RogersRamanujan/Lean/StaircaseOrder.lean`;
restated here so this file stays a single self-contained target.) -/
theorem weakDec_subStair : ∀ l : List Nat, Pos l → Gap l → WeakDec (subStair l)
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | a :: b :: t, hp, hg => by
    have hba : b + 2 ≤ a := hg.1
    have ih : WeakDec (subStair (b :: t)) :=
      weakDec_subStair (b :: t) (pos_of_cons hp) hg.2
    cases t with
    | nil =>
      show b - 1 ≤ a - 3 ∧ WeakDec (subStair (b :: []))
      exact ⟨by omega, ih⟩
    | cons c t =>
      show b - (2 * (t.length + 1) + 1) ≤
        a - (2 * ((t.length + 1) + 1) + 1) ∧ WeakDec (subStair (b :: c :: t))
      exact ⟨by omega, ih⟩

/-- `T` sends `D_n` to partitions (`WeakDec`). -/
theorem weakDec_shiftT {l : List Nat} (hp : Pos l) (hg : Gap l) : WeakDec (shiftT l) :=
  weakDec_map_add (subStair l) l.length (weakDec_subStair l hp hg)

/-! #### The codomain half: `shiftInv` lands back in `D_n` on `B_n` -/

theorem addStair_pos : ∀ l : List Nat, Pos (addStair l)
  | [] => by
    intro x hx
    simp [addStair] at hx
  | m :: ms => by
    intro x hx
    simp only [addStair, List.mem_cons] at hx
    rcases hx with rfl | hx
    · omega
    · exact addStair_pos ms x hx

theorem weakDec_addStair : ∀ (l : List Nat), WeakDec l → Gap (addStair l)
  | [], _ => trivial
  | [_], _ => trivial
  | a :: b :: t, hwd => by
    have hba : b ≤ a := hwd.1
    have ih : Gap (addStair (b :: t)) := weakDec_addStair (b :: t) hwd.2
    show b + (2 * t.length + 1) + 2 ≤ a + (2 * (t.length + 1) + 1) ∧
      Gap (addStair (b :: t))
    exact ⟨by omega, ih⟩

/-- Every entry of `addStair b` strictly exceeds any bound on the entries of `b`.
This is what makes the "subtract the constant `k`" step non-truncating. -/
theorem addStair_gt : ∀ (b : List Nat) (c : Nat), (∀ x ∈ b, c ≤ x) →
    ∀ y ∈ addStair b, c < y
  | [], c, _ => by
    intro y hy
    simp [addStair] at hy
  | x :: xs, c, h => by
    have hx : c ≤ x := h x (List.mem_cons_self ..)
    have hxs : ∀ y ∈ xs, c ≤ y := fun y hy => h y (List.mem_cons_of_mem _ hy)
    have ih := addStair_gt xs c hxs
    intro y hy
    simp only [addStair, List.mem_cons] at hy
    rcases hy with rfl | hy
    · omega
    · exact ih y hy

theorem pos_map_sub (l : List Nat) (c : Nat) (h : ∀ y ∈ l, c < y) :
    Pos (l.map (fun x => x - c)) := by
  intro x hx
  obtain ⟨y, hy, rfl⟩ := List.mem_map.1 hx
  have := h y hy
  omega

theorem gap_map_sub : ∀ (l : List Nat) (c : Nat), Gap l → (∀ y ∈ l, c ≤ y) →
    Gap (l.map (fun x => x - c))
  | [], _, _, _ => trivial
  | [_], _, _, _ => trivial
  | a :: b :: t, c, hg, h => by
    have hba : b + 2 ≤ a := hg.1
    have hb : c ≤ b := h b (by simp)
    have htail : ∀ y ∈ (b :: t), c ≤ y := fun y hy => h y (List.mem_cons_of_mem _ hy)
    have ih : Gap (List.map (fun x => x - c) (b :: t)) := gap_map_sub (b :: t) c hg.2 htail
    show b - c + 2 ≤ a - c ∧ Gap (List.map (fun x => x - c) (b :: t))
    exact ⟨by omega, ih⟩

theorem shiftInv_pos {b : List Nat} (h : ∀ x ∈ b, b.length ≤ x) : Pos (shiftInv b) :=
  pos_map_sub (addStair b) b.length (addStair_gt b b.length h)

theorem shiftInv_gap {b : List Nat} (hwd : WeakDec b) (h : ∀ x ∈ b, b.length ≤ x) :
    Gap (shiftInv b) :=
  gap_map_sub (addStair b) b.length (weakDec_addStair b hwd)
    (fun y hy => Nat.le_of_lt (addStair_gt b b.length h y hy))

/-! #### The packaged bijection `D_n ≃ B_n`, and the weight identity -/

/-- Domain: positive descending-with-gap-two lists (length retained). -/
abbrev DGap := { l : List Nat // Pos l ∧ Gap l }

/-- Codomain: partitions whose smallest part is at least the length. -/
abbrev BSmall := { b : List Nat // WeakDec b ∧ ∀ x ∈ b, b.length ≤ x }

def toB (l : DGap) : BSmall :=
  ⟨shiftT l.1, weakDec_shiftT l.2.1 l.2.2, fun x hx => by
    rw [length_shiftT]
    exact mem_shiftT_ge x hx⟩

def toD (b : BSmall) : DGap :=
  ⟨shiftInv b.1, shiftInv_pos b.2.2, shiftInv_gap b.2.1 b.2.2⟩

theorem toD_toB (l : DGap) : toD (toB l) = l := by
  apply Subtype.ext
  exact shiftInv_shiftT l.2.1 l.2.2

theorem toB_toD (b : BSmall) : toB (toD b) = b := by
  apply Subtype.ext
  exact shiftT_shiftInv b.2.2

/-- Same weight, at the subtype level. -/
theorem weight_toB (l : DGap) : (toB l).1.sum = l.1.sum :=
  sum_shiftT l.2.1 l.2.2

/-! #### Witnesses: the theorems are not vacuous, and the hypotheses are needed -/

theorem witness_T_531 : shiftT [5, 3, 1] = [3, 3, 3] := by decide
theorem witness_T_41 : shiftT [4, 1] = [3, 2] := by decide
theorem witness_T_641 : shiftT [6, 4, 1] = [4, 4, 3] := by decide
theorem witness_inv_443 : shiftInv [4, 4, 3] = [6, 4, 1] := by decide

/-- `Gap` is needed for weight preservation: `[1,3]` is positive but not a gap
partition, and `T` there loses weight (`[2,4]`, weight 6 against 4). -/
theorem witness_gap_needed : (shiftT [1, 3]).sum ≠ [1, 3].sum := by decide

/-- `Pos` is needed for injectivity: `T` collapses `[0]` and `[1]`. -/
theorem witness_not_injective : shiftT [0] = shiftT [1] ∧ [0] ≠ [1] := by decide

/-- The `WeakDec` half of the `B_n` condition is not implied by "smallest part
at least the length": `[2,5]` is positive, has length 2 and every entry at
least 2, but `shiftInv [2,5] = [3,4]` is not a gap partition.  This is why
`shiftT_shiftInv` carries only the entry bound while `shiftInv_gap` carries
`WeakDec`. -/
theorem witness_weakDec_needed : ¬ Gap (shiftInv [2, 5]) := by
  intro h
  exact absurd h.1 (by decide)

end Shift

#print axioms RR127.Shift.weakDec_map_add
#print axioms RR127.Shift.weakDec_subStair
#print axioms RR127.Shift.weakDec_shiftT
#print axioms RR127.Shift.addStair_pos
#print axioms RR127.Shift.weakDec_addStair
#print axioms RR127.Shift.addStair_gt
#print axioms RR127.Shift.pos_map_sub
#print axioms RR127.Shift.gap_map_sub
#print axioms RR127.Shift.shiftInv_pos
#print axioms RR127.Shift.shiftInv_gap
#print axioms RR127.Shift.toD_toB
#print axioms RR127.Shift.toB_toD
#print axioms RR127.Shift.weight_toB
#print axioms RR127.Shift.witness_T_531
#print axioms RR127.Shift.witness_T_41
#print axioms RR127.Shift.witness_T_641
#print axioms RR127.Shift.witness_inv_443
#print axioms RR127.Shift.witness_gap_needed
#print axioms RR127.Shift.witness_not_injective
#print axioms RR127.Shift.witness_weakDec_needed

end RR127

#print axioms RR127.head_bound
#print axioms RR127.addStair_subStair
#print axioms RR127.subStair_addStair
#print axioms RR127.sum_addStair
#print axioms RR127.weight_subStair
#print axioms RR127.subStair_nonneg
